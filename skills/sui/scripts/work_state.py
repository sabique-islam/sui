#!/usr/bin/env python3
"""Validate and checkpoint explicit task state. Writes are opt-in, atomic, exclusive-lock and version guarded."""
import argparse,hashlib,json,os,tempfile
from pathlib import Path
from file_scope import capture,canonical,safe_path

STATUSES={'planned','in_progress','done','blocked','deferred'}
def analyze(data):
 errors=[]
 if not isinstance(data,dict):return {'ok':False,'errors':['state must be object'],'ready':[]}
 if type(data.get('schemaVersion')) is not int or data['schemaVersion']!=1:errors.append('unsupported schemaVersion')
 if not isinstance(data.get('goal'),str) or not data['goal'].strip():errors.append('goal is required')
 reqs=data.get('requirements');tasks=data.get('tasks');checks=data.get('checks',[])
 if not isinstance(reqs,list) or not reqs or any(not isinstance(r,str) or not r for r in reqs):return {'ok':False,'errors':errors+['requirements must be nonempty IDs'],'ready':[]}
 if len(set(reqs))!=len(reqs):errors.append('duplicate requirement IDs')
 if not isinstance(tasks,list) or not tasks or len(tasks)>1000:return {'ok':False,'errors':errors+['tasks must contain 1..1000 items'],'ready':[]}
 if not isinstance(checks,list):return {'ok':False,'errors':errors+['checks must be an array'],'ready':[]}
 checkmap={}
 for c in checks:
  if not isinstance(c,dict) or not isinstance(c.get('id'),str) or not c['id']:errors.append('invalid check');continue
  if c['id'] in checkmap:errors.append('duplicate check ID')
  checkmap[c['id']]=c
  if not isinstance(c.get('status'),str) or c['status'] not in ('planned','passed','failed','blocked','skipped'):errors.append('invalid check status')
  if c.get('status')=='passed' and (not isinstance(c.get('evidenceRef'),str) or not c['evidenceRef'].strip()):errors.append('passed check requires evidenceRef')
 taskmap={};covered=set()
 for t in tasks:
  if not isinstance(t,dict) or not isinstance(t.get('id'),str) or not t['id']:errors.append('invalid task');continue
  tid=t['id']
  if tid in taskmap:errors.append(f'{tid}: duplicate task')
  taskmap[tid]=t
  if not isinstance(t.get('title'),str) or not t['title'].strip():errors.append(f'{tid}: missing title')
  if not isinstance(t.get('status'),str) or t['status'] not in STATUSES:errors.append(f'{tid}: invalid status')
  refs=t.get('requirements')
  if not isinstance(refs,list) or not refs:errors.append(f'{tid}: missing requirement links');refs=[]
  for r in refs:
   if not isinstance(r,str) or r not in reqs:errors.append(f'{tid}: unknown requirement')
   else:covered.add(r)
  for field in ['dependsOn','checks']:
   if not isinstance(t.get(field,[]),list) or any(not isinstance(v,str) for v in t.get(field,[])):errors.append(f'{tid}: {field} must be string IDs')
  if isinstance(t.get('checks',[]),list):
   for cid in t.get('checks',[]):
    if not isinstance(cid,str) or cid not in checkmap:errors.append(f'{tid}: unknown check')
  if t.get('status')=='done':
   linked=t.get('checks',[])
   if not linked:errors.append(f'{tid}: done needs verification checks')
   if isinstance(linked,list) and any(not isinstance(c,str) or checkmap.get(c,{}).get('status')!='passed' for c in linked):errors.append(f'{tid}: done has unpassed checks')
  if t.get('status')=='blocked' and (not isinstance(t.get('blocker'),str) or not t['blocker'].strip()):errors.append(f'{tid}: blocked needs a reason')
 for r in sorted(set(reqs)-covered):errors.append(f'{r}: no task implements requirement')
 graph={}
 for tid,t in taskmap.items():
  deps=t.get('dependsOn',[])
  if not isinstance(deps,list) or any(not isinstance(d,str) for d in deps):continue
  graph[tid]=deps
  for dep in deps:
   if dep not in taskmap:errors.append(f'{tid}: unknown dependency')
   elif t.get('status') in ('done','in_progress') and taskmap[dep].get('status')!='done':errors.append(f'{tid}: dependency not done')
 # Iterative dependency elimination avoids recursive-stack failure on long plans.
 remaining=set(graph);done=set()
 while remaining:
  ready={t for t in remaining if set(graph[t])<=done}
  if not ready:errors.append('dependency cycle or unresolved dependency');break
  done|=ready;remaining-=ready
 ready=[tid for tid,t in taskmap.items() if t.get('status')=='planned' and isinstance(t.get('dependsOn',[]),list) and all(isinstance(d,str) and taskmap.get(d,{}).get('status')=='done' for d in t.get('dependsOn',[]))]
 return {'ok':not errors,'errors':errors,'ready':ready if not errors else [],'declaredComplete':bool(taskmap) and not errors and all(t.get('status')=='done' for t in taskmap.values()),'evidenceVerified':False}

def checkpoint(data,root,out,expected_sha256):
 r=analyze(data)
 if not r['ok']:raise ValueError('; '.join(r['errors']))
 root=Path(root).resolve();out=Path(out)
 if not out.is_absolute():out=root/out
 try:rel=out.relative_to(root).as_posix()
 except ValueError:raise ValueError('state path must remain inside project root')
 out=safe_path(root,rel)
 inputs=data.get('inputs',[])
 snap=capture(root,inputs)
 if rel in inputs:raise ValueError('state output cannot be an input')
 out.parent.mkdir(parents=True,exist_ok=True)
 lock=out.with_name(out.name+'.lock');fd=None;tmp=None
 try:
  fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
  previous=hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None
  if expected_sha256 is None:raise ValueError('supply expected SHA-256, or new for first creation')
  if (expected_sha256=='new' and previous is not None) or (expected_sha256!='new' and previous!=expected_sha256):raise ValueError('state changed; read the current state before overwriting')
  value={**data,'snapshot':snap,'projectRoot':str(root)}
  handle,tmp=tempfile.mkstemp(prefix='.'+out.name+'.',dir=out.parent)
  with os.fdopen(handle,'wb') as f:f.write(canonical(value)+b'\n');f.flush();os.fsync(f.fileno())
  os.replace(tmp,out);tmp=None
  return {'path':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'snapshotDigest':snap['digest']}
 finally:
  if fd is not None:os.close(fd);lock.unlink(missing_ok=True)
  if tmp is not None:Path(tmp).unlink(missing_ok=True)

def resume(data,root):
 r=analyze(data)
 if not r['ok']:return r
 if data.get('projectRoot')!=str(Path(root).resolve()):return {**r,'ok':False,'errors':['project root differs; reconcile the checkpoint']}
 old=data.get('snapshot')
 if not isinstance(old,dict) or not isinstance(old.get('files'),list):return {**r,'ok':False,'errors':['checkpoint has no source snapshot']}
 try:
  if data.get('inputs')!=[p['path'] for p in old['files']] and sorted(data.get('inputs',[]))!=[p['path'] for p in old['files']]:raise ValueError('declared input scope differs')
  new=capture(root,data.get('inputs'))
 except (KeyError,TypeError,ValueError,OSError) as e:return {**r,'ok':False,'errors':['cannot validate checkpoint inputs: '+str(e)]}
 if new!=old:return {**r,'ok':False,'declaredComplete':False,'errors':['source changed since checkpoint; revalidate affected work'],'ready':[]}
 return {**r,'snapshotMatches':True,'note':'Task declarations and source snapshot match. Verify linked reports independently before asserting completion.'}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('state');p.add_argument('--root');p.add_argument('--write');p.add_argument('--expected-sha256');p.add_argument('--resume',action='store_true');a=p.parse_args()
 try:
  data=json.loads(Path(a.state).read_text())
  if a.write:
   if not a.root:p.error('--write requires --root')
   r=checkpoint(data,a.root,a.write,a.expected_sha256)
  elif a.resume:
   if not a.root:p.error('--resume requires --root')
   r=resume(data,a.root)
  else:r=analyze(data)
  print(json.dumps(r,indent=2));raise SystemExit(1 if r.get('ok') is False else 0)
 except (ValueError,OSError) as e:print(json.dumps({'ok':False,'errors':[str(e)]}));raise SystemExit(2)
