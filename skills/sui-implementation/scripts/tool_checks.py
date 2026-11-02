#!/usr/bin/env python3
"""Preview/run scoped native static checks or normalize supplied reports; never install/upload code."""
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import signal
import subprocess
import tempfile
import threading
import time
from pathlib import Path, PurePosixPath
from report_formats import parse, FORMATS

TOOLS={'mypy':'mypy','tsc':'tsc','gcc':'gcc','clang-tidy':'clang-tidy'}

def snapshot(root, names):
    root=Path(root).resolve()
    if not root.is_dir() or not isinstance(names,list) or not names or len(names)>1000:raise ValueError('need project root and 1..1000 explicit source files')
    if any(not isinstance(name,str) for name in names) or len(set(names))!=len(names):raise ValueError('scope must contain unique paths')
    rows=[];total=0
    for name in sorted(names):
        rel=PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts or name!=rel.as_posix() or '\\' in name or '\x00' in name or name=='.' or '.git' in rel.parts:raise ValueError('scope requires canonical relative files')
        if rel.name.startswith('.env') or rel.suffix in ('.pem','.key'):raise ValueError('credential-file scope is not supported')
        current=root
        for part in rel.parts:
            current=current/part
            if current.is_symlink():raise ValueError('symlink scope is not supported')
        if not current.is_file() or not current.resolve().is_relative_to(root):raise ValueError('scope file missing or outside root')
        size=current.stat().st_size;total+=size
        if size>8388608 or total>67108864:raise ValueError('scope exceeds size limit')
        blob=current.read_bytes()
        if len(blob)>8388608:raise ValueError('scope file grew beyond limit')
        rows.append({'path':name,'sha256':hashlib.sha256(blob).hexdigest()})
    return rows

def bounded(argv, root, seconds):
    if type(seconds) not in (int,float) or not 0<seconds<=120 or not math.isfinite(seconds):raise ValueError('timeout must be >0 and <=120 seconds')
    if os.name!='posix':raise ValueError('native execution requires POSIX process groups; report import remains available')
    chunks=[];size=0;limit=2097152;limited=threading.Event()
    proc=subprocess.Popen(argv,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True)
    def consume():
        nonlocal size
        try:
            while True:
                block=proc.stdout.read(65536)
                if not block:break
                room=limit-size;chunks.append(block[:room]);size+=min(len(block),room)
                if len(block)>room:limited.set();break
        finally:proc.stdout.close()
    reader=threading.Thread(target=consume,daemon=True);reader.start();deadline=time.monotonic()+seconds
    def stop():
        try:os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        proc.wait()
    while proc.poll() is None and time.monotonic()<deadline and not limited.is_set():
        try:proc.wait(timeout=.02)
        except subprocess.TimeoutExpired:pass
    status='completed'
    if limited.is_set():status='output_limit';stop()
    elif proc.poll() is None:status='timeout';stop()
    reader.join(.2)
    if reader.is_alive():status='descendants_running';stop();reader.join(1)
    try:os.killpg(proc.pid,0)
    except ProcessLookupError:pass
    else:status='descendants_running';stop()
    if limited.is_set():status='output_limit'
    raw=b''.join(chunks)
    return {'status':status,'returnCode':proc.returncode,'outputBytes':size,'outputSha256':hashlib.sha256(raw).hexdigest()},raw.decode('utf-8',errors='replace')

def command(tool, files, executable=None, build_dir=None):
    if tool not in TOOLS:raise ValueError('unsupported native adapter')
    exe=executable or TOOLS[tool]
    files=['./'+name for name in files]
    if tool=='mypy':return [exe,'--show-column-numbers','--show-error-codes','--no-error-summary','--no-pretty',*files]
    if tool=='tsc':return [exe,'--noEmit','--strict','--pretty','false',*files]
    if tool=='gcc':return [exe,'-fsyntax-only','-Wall','-Wextra',*files]
    if not build_dir:raise ValueError('clang-tidy requires explicit compilation-database directory')
    return [exe,'-p',build_dir,*files]

def public(report, include_messages=False):
    if not include_messages:
        for row in report.get('findings',[]):
            message=row.pop('message',None)
            if message is not None:row['messageSha256']=hashlib.sha256(message.encode()).hexdigest()
    return report

def run(tool,root,files,execute=False,executable=None,seconds=30,build_dir=None):
    root=Path(root).resolve();before=snapshot(root,files)
    if build_dir is not None:
        loc=(root/build_dir).resolve()
        if not loc.is_relative_to(root) or not (loc/'compile_commands.json').is_file():raise ValueError('build directory must contain a project-local compile_commands.json')
    argv=command(tool,files,executable,build_dir)
    if not execute:return {'status':'preview','executed':False,'argv':argv,'scope':before}
    exe=shutil.which(argv[0])
    if not exe:return {'status':'blocked','executed':False,'reason':'tool_not_installed','tool':tool}
    argv[0]=exe
    version_run,version=bounded([exe,'--version'],root,5)
    if version_run['status']!='completed' or version_run['returnCode']!=0:return {'status':'blocked','executed':False,'reason':'version_probe_failed','tool':tool}
    meta,raw=bounded(argv,root,seconds)
    base={'tool':tool,'version':version.strip()[:256],'executed':True,'argv':argv,'scope':before,'inputBinding':'endpoint-content-equality',**meta}
    if meta['status']!='completed':return base
    try:normalized=parse({'gcc':'compiler','clang-tidy':'compiler'}.get(tool,tool),raw,meta['returnCode'])
    except ValueError as error:return {**base,'status':'invalid_report','reason':str(error)}
    if snapshot(root,files)!=before:return {**base,'status':'inputs_changed'}
    finding_count=normalized['findingCount']
    status='findings' if finding_count else ('passed' if meta['returnCode']==0 else 'failed')
    return {**base,**normalized,'status':status,'limitations':'Declared source files are endpoint-bound; imports, compiler defaults, environment/dependencies and temporary restored mutations are not fully bound. Direct TypeScript mode uses explicit files/strict defaults; use project-native commands when project configuration is required. Messages are suppressed by default.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True)
    native=sub.add_parser('run');native.add_argument('--tool',choices=TOOLS,required=True);native.add_argument('--root',required=True);native.add_argument('--scope',nargs='+',required=True);native.add_argument('--execute',action='store_true');native.add_argument('--executable');native.add_argument('--timeout',type=float,default=30);native.add_argument('--build-dir');native.add_argument('--include-messages',action='store_true')
    supplied=sub.add_parser('parse');supplied.add_argument('--format',choices=FORMATS,required=True);supplied.add_argument('--report',required=True);supplied.add_argument('--completed',action='store_true',required=True);supplied.add_argument('--return-code',type=int,required=True);supplied.add_argument('--root',required=True);supplied.add_argument('--scope',nargs='+',required=True);supplied.add_argument('--include-messages',action='store_true')
    a=p.parse_args()
    try:
        if a.action=='run':result=run(a.tool,a.root,a.scope,a.execute,a.executable,a.timeout,a.build_dir)
        else:
            scoped=snapshot(a.root,a.scope);path=Path(a.report)
            if path.stat().st_size>8388608:raise ValueError('report exceeds 8 MiB')
            result={'status':'normalized','evidence':'supplied_report_not_independently_executed','scopeAtImport':scoped,**parse(a.format,path.read_text(),a.return_code)}
            if result.get('failed',0)>0:result['status']='test_failures'
            elif result['findingCount']:result['status']='findings'
        print(json.dumps(public(result,a.include_messages),indent=2,allow_nan=False));raise SystemExit(0 if result['status'] in ('preview','passed','normalized') else 1)
    except (OSError,ValueError,OverflowError) as error:
        print(json.dumps({'status':'invalid','error':str(error)}));raise SystemExit(2)
