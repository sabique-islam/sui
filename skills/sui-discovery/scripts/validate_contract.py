#!/usr/bin/env python3
"""Validate lightweight requirement traceability; not semantic requirements correctness."""
import argparse,json

def validate(data):
 errors=[]
 if not isinstance(data,dict):return ['contract must be an object']
 reqs=data.get('requirements');checks=data.get('checks')
 if not isinstance(reqs,list) or not reqs:return ['requirements must be a nonempty array']
 if not isinstance(checks,list) or not checks:return ['checks must be a nonempty array']
 ids=set();checkids=set();covered=set()
 for i,r in enumerate(reqs):
  if not isinstance(r,dict):errors.append(f'requirement {i}: must be an object');continue
  rid=r.get('id')
  if not isinstance(rid,str) or not rid.strip():errors.append(f'requirement {i}: missing id');continue
  if rid in ids:errors.append(f'{rid}: duplicate requirement')
  ids.add(rid)
  if not isinstance(r.get('behavior'),str) or not r['behavior'].strip():errors.append(f'{rid}: missing behavior')
  ac=r.get('acceptance')
  if not isinstance(ac,list) or not ac or any(not isinstance(x,str) or not x.strip() for x in ac):errors.append(f'{rid}: acceptance must contain nonempty checks')
 for i,c in enumerate(checks):
  if not isinstance(c,dict):errors.append(f'check {i}: must be an object');continue
  cid=c.get('id')
  if not isinstance(cid,str) or not cid.strip():errors.append(f'check {i}: missing id')
  elif cid in checkids:errors.append(f'{cid}: duplicate check')
  else:checkids.add(cid)
  refs=c.get('requirements')
  if not isinstance(refs,list) or not refs:errors.append(f'check {i}: missing requirement links');refs=[]
  for ref in refs:
   if not isinstance(ref,str) or ref not in ids:errors.append(f'check {i}: unknown requirement')
   else:covered.add(ref)
  if not isinstance(c.get('oracle'),str) or not c['oracle'].strip():errors.append(f'check {i}: missing oracle')
  status=c.get('status')
  if status not in ('planned','passed','failed','blocked','skipped'):errors.append(f'check {i}: invalid status')
  if status in ('passed','failed') and (not isinstance(c.get('evidence'),str) or not c['evidence'].strip()):errors.append(f'check {i}: execution status needs evidence')
 for rid in sorted(ids-covered):errors.append(f'{rid}: no linked check')
 return errors
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('contract');a=p.parse_args()
 try:
  with open(a.contract) as f:errors=validate(json.load(f))
  print(json.dumps({'ok':not errors,'errors':errors,'semanticValidation':False},indent=2));raise SystemExit(1 if errors else 0)
 except (ValueError,OSError) as e:print(json.dumps({'error':str(e)}));raise SystemExit(2)
