#!/usr/bin/env python3
"""Summarize supplied held-out AI judgments, weighting cases equally. Does not grade outputs."""
import argparse,json,math

def percentile(values,q):
 vals=sorted(values)
 return vals[max(0,math.ceil(q*len(vals))-1)] if vals else None

def report(data):
 if not isinstance(data,dict) or not isinstance(data.get('trials'),list) or not data['trials']:raise ValueError('trials must be nonempty')
 groups={};splits={};trialids=set()
 for i,r in enumerate(data['trials']):
  if not isinstance(r,dict):raise ValueError(f'trial {i}: must be object')
  for f in ('caseId','variant'):
   if not isinstance(r.get(f),str) or not r[f].strip():raise ValueError(f'trial {i}: missing {f}')
  split=r.get('split')
  if not isinstance(split,str) or split not in {'train','dev','test'}:raise ValueError(f'trial {i}: invalid split')
  splits.setdefault(r['caseId'],set()).add(split)
  if type(r.get('passed')) is not bool:raise ValueError(f'trial {i}: passed must be boolean')
  for f in ('latencyMs','costUsd'):
   n=r.get(f)
   if type(n) not in {int,float} or n<0:raise ValueError(f'trial {i}: invalid {f}')
   try:finite=math.isfinite(n)
   except OverflowError:finite=False
   if not finite:raise ValueError(f'trial {i}: invalid {f}')
  if 'trialId' in r:
   tid=r['trialId']
   if not isinstance(tid,str) or not tid:raise ValueError('trialId must be nonempty string')
   key=(r['variant'],r['caseId'],tid)
   if key in trialids:raise ValueError('duplicate trialId for case/variant')
   trialids.add(key)
  if split=='test':groups.setdefault(r['variant'],{}).setdefault(r['caseId'],[]).append(r)
 if any('test' in s and len(s)>1 for s in splits.values()):raise ValueError('caseId appears in held-out and train/dev data')
 if not groups:raise ValueError('no held-out test trials')
 result={}
 for variant,cases in groups.items():
  rates={cid:sum(r['passed'] for r in rows)/len(rows) for cid,rows in cases.items()}
  rows=[r for v in cases.values() for r in v]
  try:total_cost=math.fsum(r['costUsd'] for r in rows)
  except OverflowError:raise ValueError('total cost exceeds finite numeric range')
  result[variant]={'caseCount':len(cases),'trialCount':len(rows),'caseWeightedPassRate':sum(rates.values())/len(rates),'perCasePassRate':rates,'allTrialsPassCaseCount':sum(v==1 for v in rates.values()),'latencyP50Ms':percentile([r['latencyMs'] for r in rows],.5),'latencyP95Ms':percentile([r['latencyMs'] for r in rows],.95),'totalCostUsd':total_cost,'meanCostPerTrialUsd':total_cost/len(rows)}
 comparisons=[]
 if 'baseline' in result:
  base=result['baseline']['perCasePassRate']
  for variant,row in result.items():
   if variant=='baseline':continue
   rates=row['perCasePassRate'];shared=sorted(set(base)&set(rates))
   comparisons.append({'variant':variant,'pairedCaseCount':len(shared),'sameCaseSet':set(base)==set(rates),'pairedMeanPassRateDelta':sum(rates[c]-base[c] for c in shared)/len(shared) if shared else None,'unpairedCaseCount':len(set(base)^set(rates))})
 return {'variants':result,'comparisons':comparisons,'percentileMethod':'nearest-rank','limitations':['Supplied pass/fail judgments are not independently validated.','Cases are weighted equally; repeated trials are not independent tasks.','No confidence interval or significance claim is inferred from this summary.','Different case sets require investigation before ranking.']}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('results');a=p.parse_args()
 try:
  with open(a.results) as f:r=report(json.load(f))
  print(json.dumps(r,indent=2))
 except (ValueError,OSError) as e:print(json.dumps({'error':str(e)}));raise SystemExit(2)
