#!/usr/bin/env python3
"""Bounded HTTP load probe. Preview by default; loopback only unless an exact host is explicitly allowed."""
import argparse
import concurrent.futures
import hashlib
import ipaddress
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def validate(url,requests=20,concurrency=2,timeout=2,allowed_host=None):
    parsed=urllib.parse.urlsplit(url)
    if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password:raise ValueError('need HTTP(S) URL without embedded credentials')
    try:local=ipaddress.ip_address(parsed.hostname).is_loopback
    except ValueError:local=False
    if not local and parsed.hostname!=allowed_host:raise ValueError('target must be a literal loopback address or an explicitly authorized exact --allowed-host')
    if type(requests) is not int or not 1<=requests<=1000 or type(concurrency) is not int or not 1<=concurrency<=16:raise ValueError('requests1..1000 and concurrency1..16 required')
    if type(timeout) not in (int,float) or not 0<timeout<=5 or not math.isfinite(timeout):raise ValueError('request timeout must be >0 and <=5seconds')
    return parsed

def worker(job):
    url=job['url'];requests=job['requests'];concurrency=job['concurrency'];timeout=job['timeout']
    validate(url,requests,concurrency,timeout,job.get('allowed_host'))
    def request(_):
        begin=time.monotonic();status=None;good=False;size=0
        try:
            opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
            with opener.open(url,timeout=timeout) as response:
                status=response.status;body=response.read(1048577);size=len(body);good=200<=status<300 and size<=1048576
        except urllib.error.HTTPError as error:status=error.code;error.close()
        except (OSError,ValueError):pass
        return {'latencyMs':(time.monotonic()-begin)*1000,'good':good,'status':status,'bytesRead':size}
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures=[executor.submit(request,i) for i in range(requests)]
        for future in concurrent.futures.as_completed(futures):
            print(json.dumps(future.result(),allow_nan=False),flush=True)

def probe(url,requests=20,concurrency=2,timeout=2,allowed_host=None,execute=False,max_p95_ms=1000,max_error_rate=0,max_seconds=60):
    parsed=validate(url,requests,concurrency,timeout,allowed_host)
    if type(max_p95_ms) not in (int,float) or not 0<max_p95_ms<=60000 or not math.isfinite(max_p95_ms):raise ValueError('invalid p95 threshold')
    if type(max_error_rate) not in (int,float) or not 0<=max_error_rate<=1 or not math.isfinite(max_error_rate):raise ValueError('invalid error threshold')
    if type(max_seconds) not in (int,float) or not 0<max_seconds<=60 or not math.isfinite(max_seconds):raise ValueError('wall deadline must be >0 and <=60seconds')
    plan={'host':parsed.hostname,'port':parsed.port or (443 if parsed.scheme=='https' else 80),'pathSha256':hashlib.sha256((parsed.path+'?'+parsed.query).encode()).hexdigest(),'requests':requests,'concurrency':concurrency,'timeoutSeconds':timeout,'maxP95Ms':max_p95_ms,'maxErrorRate':max_error_rate,'wallDeadlineSeconds':max_seconds}
    if not execute:return {'status':'preview','executed':False,'plan':plan}
    start=time.monotonic();deadline_hit=False
    # Socket timeouts are idle timeouts: a trickling server can defeat them.
    # Isolate the entire campaign so a parent wall deadline can kill all IO threads.
    proc=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--worker'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,start_new_session=(os.name=='posix'))
    payload=json.dumps({'url':url,'requests':requests,'concurrency':concurrency,'timeout':timeout,'allowed_host':allowed_host}).encode()
    try:output,_=proc.communicate(payload,timeout=max_seconds)
    except subprocess.TimeoutExpired:
        deadline_hit=True
        if os.name=='posix':
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
        else:proc.kill()
        output,_=proc.communicate(timeout=2)
    samples=[]
    for line in output.splitlines():
        row=json.loads(line)
        if not isinstance(row,dict) or type(row.get('good')) is not bool or type(row.get('latencyMs')) not in (int,float):raise ValueError('invalid worker sample')
        samples.append(row)
    if len(samples)>requests:raise ValueError('worker exceeded request budget')
    elapsed=time.monotonic()-start
    if not samples:return {'status':'timeout' if deadline_hit else 'no_data','executed':True,'plan':plan,'deadlineReached':deadline_hit,'elapsedSeconds':elapsed}
    latencies=sorted(r['latencyMs'] for r in samples);errors=sum(not r['good'] for r in samples)
    percentiles={f'p{q}Ms':latencies[math.ceil(q/100*len(latencies))-1] for q in (50,95,99)}
    failed=deadline_hit or proc.returncode!=0 or len(samples)!=requests or errors/len(samples)>max_error_rate or percentiles['p95Ms']>max_p95_ms
    return {'status':'failed' if failed else 'passed','executed':True,'plan':plan,'sampleCount':len(samples),'errors':errors,'errorRate':errors/len(samples),'elapsedSeconds':elapsed,'throughputPerSecond':len(samples)/elapsed,**percentiles,'saturation':'not_collected','deadlineReached':deadline_hit,
            'limitations':'Client-side observations for this bounded workload only. No production capacity, saturation, causality, reliability-over-time or user-population representativeness is inferred. Redirects are not followed and response bodies are not retained.'}

def demo(**options):
    if not options.get('execute',False):return probe('http://127.0.0.1:0/',**options)
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body=b'ok';self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:return probe(f'http://127.0.0.1:{server.server_port}/',**options)
    finally:server.shutdown();server.server_close();thread.join(2)

if __name__=='__main__':
    if sys.argv[1:]==['--worker']:
        worker(json.loads(sys.stdin.buffer.read(16384)));raise SystemExit(0)
    p=argparse.ArgumentParser(description=__doc__);target=p.add_mutually_exclusive_group(required=True);target.add_argument('--url');target.add_argument('--demo',action='store_true');p.add_argument('--requests',type=int,default=20);p.add_argument('--concurrency',type=int,default=2);p.add_argument('--timeout',type=float,default=2);p.add_argument('--allowed-host');p.add_argument('--max-p95-ms',type=float,default=1000);p.add_argument('--max-error-rate',type=float,default=0);p.add_argument('--max-seconds',type=float,default=60);p.add_argument('--execute',action='store_true');a=p.parse_args()
    try:
        opts={'requests':a.requests,'concurrency':a.concurrency,'timeout':a.timeout,'allowed_host':a.allowed_host,'execute':a.execute,'max_p95_ms':a.max_p95_ms,'max_error_rate':a.max_error_rate,'max_seconds':a.max_seconds}
        r=demo(**opts) if a.demo else probe(a.url,**opts);print(json.dumps(r,indent=2,allow_nan=False));raise SystemExit(0 if r['status'] in ('passed','preview') else 1)
    except (ValueError,OSError,OverflowError) as error:
        print(json.dumps({'status':'invalid','error':str(error)}));raise SystemExit(2)
