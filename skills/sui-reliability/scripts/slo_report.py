#!/usr/bin/env python3
"""Request-based error-budget arithmetic. No time-based availability inference."""
import argparse,json,math

def report(data,target):
 if not isinstance(data,dict):raise ValueError('events must be object')
 eligible=data.get('eligible');good=data.get('good')
 if type(eligible) is not int or type(good) is not int or not 0<=good<=eligible:raise ValueError('need integer 0 <= good <= eligible')
 if type(target) not in {int,float} or not math.isfinite(target) or not 0<target<1:raise ValueError('target must be between 0 and 1 exclusively')
 if not isinstance(data.get('window'),str) or not data['window'].strip():raise ValueError('window must be explicit')
 if data.get('unit')!='requests':raise ValueError('unit must be requests')
 if eligible==0:return {'status':'no_data','sli':None,'eligible':0,'window':data['window'],'budgetConsumedFraction':None}
 bad=eligible-good;allowed=(1-target)*eligible;remaining=allowed-bad
 return {'status':'within_objective' if remaining>=-1e-9 else 'exceeded','eligible':eligible,'good':good,'bad':bad,'sli':good/eligible,'target':target,'window':data['window'],'allowedBadRequests':round(allowed,9),'remainingBadRequests':round(remaining,9),'budgetConsumedFraction':bad/allowed,'burnRate':(bad/eligible)/(1-target),'unit':'requests','limitations':'Eligible request counts for one explicit window; does not infer traffic representativeness, time availability or an SLA.'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('events');p.add_argument('--target',type=float,required=True);a=p.parse_args()
 try:
  with open(a.events) as f:r=report(json.load(f),a.target)
  print(json.dumps(r,indent=2));raise SystemExit(1 if r['status']=='exceeded' else (2 if r['status']=='no_data' else 0))
 except (ValueError,OSError) as e:print(json.dumps({'error':str(e)}));raise SystemExit(2)
