#!/usr/bin/env python3
"""Check audit-to-resource integrity and support tiers, not semantic completeness or live integrations."""
import argparse
import json
from pathlib import Path
from validate_pack import resolve

TIERS=('method_ready','native_trial_passed','report_adapter_tested','schema_and_inventory_adapter','procedure_ready','mixed_integration_support')

def check(root,ledger=None):
    found=resolve(root);errors=[]
    if len(found.get('sui',[]))!=1:return {'ok':False,'errors':['core skill missing or ambiguous']}
    core=found['sui'][0]
    baseline=json.loads((core/'assets/capability-baseline.json').read_text())['items']
    data=ledger if ledger is not None else json.loads((core/'assets/capability-coverage.json').read_text())
    if not isinstance(data,dict) or data.get('schemaVersion')!=1 or not isinstance(data.get('items'),list):return {'ok':False,'errors':['invalid ledger schema']}
    expected={r['id']:r for r in baseline};seen=set();tiers={tier:0 for tier in TIERS}
    if len(expected)!=163:errors.append('baseline item count differs')
    for row in data['items']:
        if not isinstance(row,dict):errors.append('invalid ledger record');continue
        key=row.get('id');tier=row.get('resolutionTier')
        if not isinstance(key,str) or key not in expected:errors.append('unknown/missing audit id');continue
        if key in seen:errors.append(f'{key}: duplicate resolution')
        seen.add(key)
        if row.get('baselineDisposition')!=expected[key]['disposition']:errors.append(f'{key}: baseline disposition changed')
        if not isinstance(tier,str) or tier not in TIERS:errors.append(f'{key}: invalid support tier')
        else:tiers[tier]+=1
        refs=row.get('resources')
        if not isinstance(refs,list) or not refs:errors.append(f'{key}: no resource');continue
        for ref in refs:
            if not isinstance(ref,dict) or not isinstance(ref.get('skill'),str) or not isinstance(ref.get('path'),str):errors.append(f'{key}: malformed resource');continue
            paths=found.get(ref['skill'],[]);rel=Path(ref['path'])
            if rel.is_absolute() or '..' in rel.parts or len(paths)!=1:errors.append(f'{key}: unsafe/unresolved resource');continue
            file=paths[0]/rel
            if not file.is_file() or not file.resolve().is_relative_to(paths[0].resolve()):errors.append(f'{key}: missing/outside resource {ref["path"]}')
        if expected[key]['disposition']=='conditional_integration' and not isinstance(row.get('externalValidation'),str):errors.append(f'{key}: missing external-validation limitation')
    for key in sorted(set(expected)-seen):errors.append(f'{key}: unresolved audit entry')
    return {'ok':not errors,'errors':errors,'mappedItems':len(seen),'tiers':tiers,'semanticValidation':False,'limitations':'Checks ID and resource integrity only. Read resources and actual validation evidence to assess method quality, supported schemas and target integration.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('skills_root');a=p.parse_args()
    try:
        r=check(a.skills_root);print(json.dumps(r,indent=2));raise SystemExit(0 if r['ok'] else 1)
    except (OSError,ValueError,KeyError,TypeError) as error:print(json.dumps({'ok':False,'error':str(error)}));raise SystemExit(2)
