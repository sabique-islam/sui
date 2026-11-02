#!/usr/bin/env python3
"""Audit test matrix links and evidence fields; never claims tests were executed."""
import argparse,json

def validate(data):
 if not isinstance(data,dict):return ['matrix must be an object']
 requirements=data.get('requirements');cases=data.get('cases');errors=[]
 if not isinstance(requirements,list) or not requirements or any(not isinstance(x,str) or not x.strip() for x in requirements):return ['requirements must be nonempty strings']
 if len(set(requirements))!=len(requirements):errors.append('duplicate requirement ids')
 if not isinstance(cases,list) or not cases:return errors+['cases must be nonempty']
 ids=set();covered=set()
 for i,c in enumerate(cases):
  if not isinstance(c,dict):errors.append(f'case {i}: must be an object');continue
  cid=c.get('id')
  if not isinstance(cid,str) or not cid.strip():errors.append(f'case {i}: missing id')
  elif cid in ids:errors.append(f'{cid}: duplicate case')
  else:ids.add(cid)
  for field in ('risk','oracle'):
   if not isinstance(c.get(field),str) or not c[field].strip():errors.append(f'case {i}: missing {field}')
  if c.get('level') not in ('unit','component','integration','contract','system','acceptance','property','fuzz','performance','manual'):errors.append(f'case {i}: invalid level')
  refs=c.get('requirements')
  if not isinstance(refs,list) or not refs:errors.append(f'case {i}: missing requirement links');refs=[]
  for ref in refs:
   if not isinstance(ref,str) or ref not in requirements:errors.append(f'case {i}: unknown requirement')
   else:covered.add(ref)
  status=c.get('status')
  if status not in ('planned','passed','failed','blocked','skipped'):errors.append(f'case {i}: invalid status')
  if status in ('passed','failed','blocked','skipped') and (not isinstance(c.get('evidence'),str) or not c['evidence'].strip()):errors.append(f'case {i}: status needs execution evidence or reason')
  argv=c.get('command')
  if c.get('level')!='manual' and (not isinstance(argv,list) or not argv or any(not isinstance(x,str) or not x for x in argv)):errors.append(f'case {i}: command must be argv array')
 for rid in sorted(set(requirements)-covered):errors.append(f'{rid}: no test case')
 return errors
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('matrix');a=p.parse_args()
 try:
  with open(a.matrix) as f:errors=validate(json.load(f))
  print(json.dumps({'ok':not errors,'errors':errors,'executedTests':False},indent=2));raise SystemExit(1 if errors else 0)
 except (ValueError,OSError) as e:print(json.dumps({'error':str(e)}));raise SystemExit(2)
