#!/usr/bin/env python3
"""Reject stale/mismatched local check evidence. Consistency checking, not signed attestation."""
import argparse,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from file_scope import capture,canonical
from run_gate import validate

def verify(report,plan,root,max_age_hours=24,now=None):
 errors=[]
 if not isinstance(report,dict) or not isinstance(plan,dict):return {'ok':False,'errors':['report and plan must be objects']}
 plan_errors=validate(plan,root)
 if plan_errors:return {'ok':False,'errors':['invalid plan: '+e for e in plan_errors]}
 if type(max_age_hours) not in {int,float} or not 0<max_age_hours<=168:raise ValueError('max age must be >0 and <=168 hours')
 if report.get('status')!='passed' or report.get('executed') is not True:errors.append('report does not contain a passed executed gate')
 if report.get('evidenceScope')!='bound':errors.append('report is not bound to an input scope')
 if report.get('inputBinding')!='endpoint-content-equality':errors.append('missing or unsupported input-binding guarantee; regenerate legacy reports')
 if report.get('planSha256')!=hashlib.sha256(canonical(plan)).hexdigest():errors.append('check plan differs from evidence')
 if report.get('projectRoot')!=str(Path(root).resolve()):errors.append('project root differs')
 try:
  stamp=datetime.fromisoformat(report['finishedAt'])
  started=datetime.fromisoformat(report['startedAt'])
  if stamp.tzinfo is None or started.tzinfo is None or started>stamp:raise ValueError('invalid time interval')
  current=now or datetime.now(timezone.utc);age=(current-stamp).total_seconds()/3600
  if not 0<=age<=max_age_hours:errors.append('evidence is future-dated or older than permitted')
 except (KeyError,ValueError,TypeError):errors.append('invalid completion timestamp')
 try:
  snapshot=capture(root,plan.get('inputs'))
  if report.get('inputSnapshot')!=snapshot:errors.append('source inputs changed or evidence is unbound')
 except (ValueError,OSError) as e:errors.append('cannot validate input scope: '+str(e))
 checks=report.get('checks');expected=plan.get('checks')
 if not isinstance(checks,list) or not isinstance(expected,list) or not expected:errors.append('check records missing')
 else:
  ids=[c.get('id') for c in checks if isinstance(c,dict)]
  if len(ids)!=len(checks) or len(ids)!=len(set(str(x) for x in ids)) or ids!=[c.get('id') for c in expected if isinstance(c,dict)]:errors.append('check identity/order differs')
  required=[c for c in expected if isinstance(c,dict) and c.get('required',True)]
  if not required:errors.append('no required checks')
  observed={c.get('id'):c for c in checks if isinstance(c,dict) and isinstance(c.get('id'),str)}
  for c in expected:
   row=observed.get(c['id'],{})
   if type(row.get('required')) is not bool or row['required']!=c.get('required',True):errors.append('required flag differs from plan')
   if type(row.get('outputLimited')) is not bool or (row['outputLimited'] and row.get('status')!='output_limit'):errors.append('invalid output-limit record')
  for c in required:
   row=observed.get(c.get('id'),{})
   if row.get('status')!='passed' or type(row.get('returnCode')) is not int or row['returnCode']!=0 or row.get('outputLimited') is True:errors.append('required check is not an observed success')
 return {'ok':not errors,'errors':errors,'inputBinding':'endpoint-content-equality','limitations':'Only declared file contents at capture endpoints and local report consistency are checked. Temporary changes restored during execution are not detected. External services, dependency installations, omitted files and forged reports are not independently verified.'}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--plan',required=True);p.add_argument('--root',required=True);p.add_argument('--max-age-hours',type=float,default=24);a=p.parse_args()
 try:
  r=verify(json.loads(Path(a.report).read_text()),json.loads(Path(a.plan).read_text()),a.root,a.max_age_hours)
  print(json.dumps(r,indent=2));raise SystemExit(0 if r['ok'] else 1)
 except (ValueError,OSError) as e:print(json.dumps({'ok':False,'errors':[str(e)]}));raise SystemExit(2)
