#!/usr/bin/env python3
"""Preview or execute a reviewed argv-based check plan. No shell; bounded output and process-group timeout."""
import argparse,hashlib,json,math,os,signal,subprocess,threading,time
from datetime import datetime,timezone
from pathlib import Path
from file_scope import capture,canonical

def validate(plan,root):
 root=Path(root).resolve();errors=[]
 if not root.is_dir():return ['root must be a directory']
 if not isinstance(plan,dict) or not isinstance(plan.get('checks'),list) or not plan['checks']:return ['checks must be nonempty']
 if 'inputs' in plan:
  try:capture(root,plan['inputs'])
  except (ValueError,OSError) as e:errors.append('invalid input scope: '+str(e))
 ids=set()
 for i,c in enumerate(plan['checks']):
  if not isinstance(c,dict):errors.append(f'check {i}: must be object');continue
  cid=c.get('id')
  if not isinstance(cid,str) or not cid.strip():errors.append(f'check {i}: missing id')
  elif cid in ids:errors.append(f'{cid}: duplicate id')
  else:ids.add(cid)
  argv=c.get('argv')
  if not isinstance(argv,list) or not argv or any(not isinstance(s,str) or not s or '\x00' in s for s in argv):errors.append(f'check {i}: argv must be nonempty strings')
  if type(c.get('required',True)) is not bool:errors.append(f'check {i}: required must be boolean')
  timeout=c.get('timeoutSeconds',120)
  if type(timeout) not in {int,float} or not 0<timeout<=3600 or not math.isfinite(timeout):errors.append(f'check {i}: invalid timeout')
  cwd=c.get('cwd','.')
  if not isinstance(cwd,str):errors.append(f'check {i}: cwd must be a string');continue
  loc=(root/cwd).resolve()
  if not loc.is_relative_to(root) or not loc.is_dir():errors.append(f'check {i}: cwd must remain under root')
 return errors

def run(plan,root,execute=False):
 errors=validate(plan,root)
 if errors:return {'status':'invalid','errors':errors,'checks':[]}
 if not execute:return {'status':'preview','checks':plan['checks'],'executed':False}
 if os.name!='posix':return {'status':'blocked','errors':['Execution requires POSIX process-group isolation; preview remains available.'],'checks':[],'executed':False}
 started=datetime.now(timezone.utc).isoformat()
 before=capture(root,plan['inputs']) if 'inputs' in plan else None
 # Never store or print check output: it may contain credentials or personal data.
 # Hash at most 2 MiB, then stop the process group. Investigate logs separately.
 rows=[]
 for c in plan['checks']:
  start=time.monotonic();status='blocked';code=None
  state={'size':0,'hash':hashlib.sha256()};limited=threading.Event()
  def consume(stream):
   try:
    while True:
     chunk=stream.read(65536)
     if not chunk:break
     remaining=2097152-state['size']
     state['hash'].update(chunk[:remaining]);state['size']+=min(len(chunk),remaining)
     if len(chunk)>remaining:limited.set();break
   finally:stream.close()
  def stop(proc):
   try:
    if os.name=='posix':os.killpg(proc.pid,signal.SIGTERM)
    else:proc.terminate()
   except ProcessLookupError:return
   try:proc.wait(timeout=0.5)
   except subprocess.TimeoutExpired:pass
   # Kill descendants too, even if their parent already exited after SIGTERM.
   try:
    if os.name=='posix':os.killpg(proc.pid,signal.SIGKILL)
    elif proc.poll() is None:proc.kill()
   except ProcessLookupError:pass
   proc.wait()
  try:
   proc=subprocess.Popen(c['argv'],cwd=(Path(root)/c.get('cwd','.')).resolve(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=(os.name=='posix'))
   reader=threading.Thread(target=consume,args=(proc.stdout,),daemon=True);reader.start()
   deadline=start+c.get('timeoutSeconds',120)
   while proc.poll() is None and time.monotonic()<deadline and not limited.is_set():
    try:proc.wait(timeout=min(.02,max(.001,deadline-time.monotonic())))
    except subprocess.TimeoutExpired:pass
   if limited.is_set():status='output_limit';stop(proc)
   elif proc.poll() is None:status='timeout';stop(proc)
   else:status='passed' if proc.returncode==0 else 'failed'
   reader.join(timeout=.3)
   if reader.is_alive():status='descendants_running';stop(proc);reader.join(timeout=1)
   # A detached-output descendant can remain even after both parent and reader exit.
   # Commands that intentionally start persistent services are not completion checks.
   try:
    os.killpg(proc.pid,0)
   except ProcessLookupError:pass
   else:
    if status=='passed':status='descendants_running'
    stop(proc)
   if limited.is_set():status='output_limit'
   code=proc.returncode
  except OSError:status='blocked'
  rows.append({'id':c['id'],'required':c.get('required',True),'status':status,'returnCode':code,'durationSeconds':round(time.monotonic()-start,4),'outputBytes':state['size'],'outputSha256':state['hash'].hexdigest(),'outputSuppressed':True,'outputLimited':limited.is_set()})
 required=[r for r in rows if r['required']]
 overall='failed' if any(r['status']!='passed' for r in required) else ('passed' if required else 'incomplete')
 if before is not None:
  try:unchanged=capture(root,plan['inputs'])==before
  except (ValueError,OSError):unchanged=False
  if not unchanged:overall='inputs_changed'
 return {'status':overall,'checks':rows,'executed':True,'startedAt':started,'finishedAt':datetime.now(timezone.utc).isoformat(),'projectRoot':str(Path(root).resolve()),'planSha256':hashlib.sha256(canonical(plan)).hexdigest(),'inputSnapshot':before,'evidenceScope':'bound' if before else 'unbound','inputBinding':'endpoint-content-equality' if before else 'none','limitations':'Only declared local input contents at the before/after endpoints are compared. Temporary changes restored during execution (ABA) are not detected. This is not immutable execution, a filesystem sandbox, or proof of what a process read. Environment/dependency changes, omitted files and external service state need separate validation. Commands can have side effects; output was suppressed.'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan');p.add_argument('--root',required=True);p.add_argument('--execute',action='store_true');a=p.parse_args()
 try:
  with open(a.plan) as f:r=run(json.load(f),a.root,a.execute)
  print(json.dumps(r,indent=2));raise SystemExit(0 if r['status'] in {'passed','preview'} else 1)
 except (ValueError,OSError) as e:print(json.dumps({'error':str(e)}));raise SystemExit(2)
