#!/usr/bin/env python3
"""Check claim provenance structure, not the truth of claims or authority of URLs."""
import argparse,json
from datetime import date
from urllib.parse import urlparse

def audit(data,as_of):
 if not isinstance(data,dict):return ['evidence must be object']
 today=date.fromisoformat(as_of);errors=[];sources=data.get('sources');claims=data.get('claims')
 if not isinstance(sources,list) or not sources:return ['sources must be nonempty']
 if not isinstance(claims,list) or not claims:return ['claims must be nonempty']
 ids=set();cids=set()
 for i,s in enumerate(sources):
  if not isinstance(s,dict):errors.append(f'source {i}: must be object');continue
  sid=s.get('id')
  if not isinstance(sid,str) or not sid:errors.append(f'source {i}: missing id')
  elif sid in ids:errors.append(f'{sid}: duplicate source')
  else:ids.add(sid)
  u=urlparse(str(s.get('url','')))
  if u.scheme!='https' or not u.netloc or u.username or u.password:errors.append(f'source {i}: invalid HTTPS URL')
  try:
   age=(today-date.fromisoformat(s['checkedAt'])).days
   if age<0:errors.append(f'source {i}: future checkedAt')
   if s.get('kind') in ('evolving','versioned') and age>90:errors.append(f'source {i}: refresh volatile evidence')
  except (KeyError,ValueError,TypeError):errors.append(f'source {i}: invalid checkedAt')
 for i,c in enumerate(claims):
  if not isinstance(c,dict):errors.append(f'claim {i}: must be object');continue
  cid=c.get('id')
  if not isinstance(cid,str) or not cid:errors.append(f'claim {i}: missing id')
  elif cid in cids:errors.append(f'{cid}: duplicate claim')
  else:cids.add(cid)
  for field in ('text','applicability'):
   if not isinstance(c.get(field),str) or not c[field].strip():errors.append(f'claim {i}: missing {field}')
  status=c.get('status')
  if status not in ('supported','inference','unverified','contradicted'):errors.append(f'claim {i}: invalid status')
  refs=c.get('sources',[])
  if not isinstance(refs,list):errors.append(f'claim {i}: sources must be array');refs=[]
  if status in ('supported','inference') and not refs:errors.append(f'claim {i}: missing source support')
  for ref in refs:
   if not isinstance(ref,str) or ref not in ids:errors.append(f'claim {i}: unknown source')
 return errors
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('evidence');p.add_argument('--as-of',default=date.today().isoformat());a=p.parse_args()
 try:
  with open(a.evidence) as f:errors=audit(json.load(f),a.as_of)
  print(json.dumps({'ok':not errors,'errors':errors,'truthVerified':False,'networkChecked':False},indent=2));raise SystemExit(1 if errors else 0)
 except (ValueError,OSError) as e:print(json.dumps({'error':str(e)}));raise SystemExit(2)
