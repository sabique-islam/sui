#!/usr/bin/env python3
"""Score supplied routing choices against explicit gold labels. Never generates model predictions."""
import argparse,json
from pathlib import Path

def score(gold,prediction):
 if not isinstance(gold,dict) or not isinstance(gold.get('cases'),list) or not gold['cases']:raise ValueError('nonempty gold cases required')
 if not isinstance(prediction,dict) or not isinstance(prediction.get('predictions'),list):raise ValueError('prediction rows required')
 expected={};seen=set()
 for c in gold['cases']:
  if not isinstance(c,dict) or not isinstance(c.get('id'),str) or not c['id'] or c['id'] in expected:raise ValueError('invalid or duplicate gold ID')
  labels=c.get('acceptablePrimary')
  if not isinstance(labels,list) or not labels or any(x is not None and not isinstance(x,str) for x in labels):raise ValueError('invalid gold labels')
  if c.get('mode') not in (None,'light','standard','critical'):raise ValueError('invalid gold mode')
  expected[c['id']]=c
 observed={}
 for p in prediction['predictions']:
  if not isinstance(p,dict) or not isinstance(p.get('id'),str) or p['id'] in observed or p['id'] not in expected:raise ValueError('invalid, unknown or duplicate prediction ID')
  if p.get('primary') is not None and not isinstance(p['primary'],str):raise ValueError('invalid primary')
  if p.get('mode') not in (None,'light','standard','critical'):raise ValueError('invalid mode')
  observed[p['id']]=p
 rows=[];tp=fp=fn=0
 for cid,c in expected.items():
  p=observed.get(cid);primary=p.get('primary') if p else '__missing__';mode=p.get('mode') if p else '__missing__'
  correct=primary in c['acceptablePrimary'];mode_ok=mode==c.get('mode')
  out=c['acceptablePrimary']==[None]
  if out and primary not in (None,'__missing__'):fp+=1
  if not out and primary is None:fn+=1
  if not out and correct:tp+=1
  rows.append({'id':cid,'present':p is not None,'primaryCorrect':correct,'modeCorrect':mode_ok,'jointCorrect':correct and mode_ok})
 n=len(rows)
 return {'variant':prediction.get('variant'),'caseCount':n,'predictedCount':len(observed),'primaryAccuracy':sum(r['primaryCorrect'] for r in rows)/n,'modeAccuracy':sum(r['modeCorrect'] for r in rows)/n,'jointAccuracy':sum(r['jointCorrect'] for r in rows)/n,'outOfScopeFalsePositives':fp,'inScopeNullSelections':fn,'missingIds':[r['id'] for r in rows if not r['present']],'rows':rows,'limitations':'One labelled routing dataset; not end-to-end SWE performance. Missing cases count as failures; no model calls or significance claims.'}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('gold');p.add_argument('prediction',nargs='+');a=p.parse_args()
 try:
  gold=json.loads(Path(a.gold).read_text());reports=[score(gold,json.loads(Path(x).read_text())) for x in a.prediction]
  print(json.dumps({'reports':reports,'jointDeltaFromFirst':[{'variant':r['variant'],'delta':r['jointAccuracy']-reports[0]['jointAccuracy']} for r in reports[1:]]},indent=2))
 except (ValueError,OSError) as e:print(json.dumps({'error':str(e)}));raise SystemExit(2)
