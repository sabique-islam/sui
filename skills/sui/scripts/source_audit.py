#!/usr/bin/env python3
"""Offline source registry metadata audit. Does not fetch links or verify claims."""
import argparse,json
from datetime import date
from urllib.parse import urlparse

def audit(data,as_of):
 if not isinstance(data,dict):return ['registry must be an object']
 rows=data.get('sources');errors=[];seen=set();today=date.fromisoformat(as_of)
 if not isinstance(rows,list) or not rows:return ['sources must be a nonempty array']
 for i,row in enumerate(rows):
  if not isinstance(row,dict):errors.append(f'source {i}: must be an object');continue
  sid=row.get('id');label=sid or str(i)
  if not isinstance(sid,str) or not sid.strip():errors.append(f'source {i}: missing id')
  elif sid in seen:errors.append(f'{sid}: duplicate id')
  else:seen.add(sid)
  for key in ('title','applicability','kind'):
   if not isinstance(row.get(key),str) or not row[key].strip():errors.append(f'{label}: missing {key}')
  url=urlparse(str(row.get('url','')))
  if url.scheme!='https' or not url.netloc or url.username or url.password:errors.append(f'{label}: URL must be HTTPS without credentials')
  if row.get('status') not in ('retrieved','unavailable','seed'):errors.append(f'{label}: invalid retrieval status')
  try:
   age=(today-date.fromisoformat(row['checkedAt'])).days
   if age<0:errors.append(f'{label}: future checkedAt')
   if row.get('kind') in ('evolving','versioned') and age>90:errors.append(f'{label}: stale volatile source; refresh before relying on current facts')
  except (KeyError,ValueError,TypeError):errors.append(f'{label}: invalid checkedAt')
 return errors
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('registry');p.add_argument('--as-of',default=date.today().isoformat());a=p.parse_args()
 try:
  with open(a.registry) as f:errors=audit(json.load(f),a.as_of)
  print(json.dumps({'ok':not errors,'errors':errors,'networkChecked':False,'claimsVerified':False},indent=2));raise SystemExit(1 if errors else 0)
 except (ValueError,OSError) as e:print(json.dumps({'error':str(e)}));raise SystemExit(2)
