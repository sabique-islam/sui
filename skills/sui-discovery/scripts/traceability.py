#!/usr/bin/env python3
"""Audit an SDLC artifact graph, reverse orphans and requirement-change records."""
import argparse
import json
from pathlib import Path

KINDS=('requirement','architecture','design','code','unit','functional','system','acceptance','security')

def validate(data, root=None):
    errors=[]
    if not isinstance(data,dict):return ['traceability document must be an object']
    records=data.get('artifacts');links=data.get('links');required=data.get('requiredKinds')
    if not isinstance(records,list) or not records:return ['artifacts must be nonempty']
    if not isinstance(links,list):return ['links must be a list']
    if not isinstance(required,list) or not required or any(not isinstance(k,str) or k not in KINDS[1:] for k in required) or len(set(required))!=len(required):
        return ['requiredKinds must explicitly name unique non-requirement artifact kinds']
    nodes={}
    for i,row in enumerate(records):
        if not isinstance(row,dict):errors.append(f'artifact {i}: must be object');continue
        key=row.get('id');kind=row.get('kind')
        if not isinstance(key,str) or not key.strip():errors.append(f'artifact {i}: invalid id');continue
        if key in nodes:errors.append(f'{key}: duplicate artifact');continue
        if not isinstance(kind,str) or kind not in KINDS:errors.append(f'{key}: invalid kind')
        if not isinstance(row.get('locator'),str) or not row['locator'].strip():errors.append(f'{key}: missing locator')
        if not isinstance(row.get('owner'),str) or not row['owner'].strip():errors.append(f'{key}: missing owner')
        nodes[key]=row
        if root is not None and kind=='code':
            locator=row.get('locator','');rel=Path(locator)
            if rel.is_absolute() or '..' in rel.parts or not (Path(root)/rel).is_file() or not (Path(root)/rel).resolve().is_relative_to(Path(root).resolve()):errors.append(f'{key}: code locator missing or outside root')
    forward={key:set() for key in nodes};reverse={key:set() for key in nodes};seen=set()
    for edge in links:
        if not isinstance(edge,list) or len(edge)!=2 or any(not isinstance(k,str) or k not in nodes for k in edge):errors.append('invalid or dangling link');continue
        a,b=edge
        if (a,b) in seen:errors.append('duplicate link')
        if a==b:errors.append('self link')
        seen.add((a,b));forward[a].add(b);reverse[b].add(a)
    def reachable(start, graph):
        found=set();pending=list(graph[start])
        while pending:
            key=pending.pop()
            if key in found:continue
            found.add(key);pending.extend(graph[key]-found)
        return found
    requirements=[k for k,r in nodes.items() if r.get('kind')=='requirement']
    if not requirements:errors.append('no requirements')
    for key in requirements:
        related=reachable(key,forward)
        if key in related:errors.append(f'{key}: cyclic traceability')
        kinds={nodes[k].get('kind') for k in related}
        waivers=nodes[key].get('waivers',{})
        if not isinstance(waivers,dict):errors.append(f'{key}: invalid waivers');waivers={}
        for kind in required:
            if kind not in kinds and (not isinstance(waivers.get(kind),str) or not waivers[kind].strip()):errors.append(f'{key}: missing {kind} trace or reasoned waiver')
    for key,row in nodes.items():
        if row.get('kind')!='requirement' and not any(nodes[k].get('kind')=='requirement' for k in reachable(key,reverse)):
            errors.append(f'{key}: reverse orphan, no originating requirement')
    changes=data.get('changes',[])
    if not isinstance(changes,list):errors.append('changes must be a list');changes=[]
    changeids=set()
    for row in changes:
        if not isinstance(row,dict):errors.append('change must be object');continue
        for field in ['id','baseline','requester','rationale','alternatives','impact','decisionOwner','targetRelease']:
            if not isinstance(row.get(field),str) or not row[field].strip():errors.append(f'change: missing {field}')
        key=row.get('id')
        if isinstance(key,str):
            if key in changeids:errors.append('duplicate change id')
            changeids.add(key)
        if row.get('status') not in ('proposed','accepted','rejected','deferred','implemented','verified'):errors.append('invalid change status')
        affected=row.get('affected')
        if not isinstance(affected,list) or not affected or any(not isinstance(k,str) or k not in nodes for k in affected):errors.append('change needs known affected artifacts')
        if row.get('status')=='verified' and (not isinstance(row.get('evidence'),str) or not row['evidence'].strip()):errors.append('verified change needs evidence')
    return errors

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--root');a=p.parse_args()
    try:
        errors=validate(json.loads(Path(a.input).read_text()),a.root)
        print(json.dumps({'ok':not errors,'errors':errors,'semanticValidation':False},indent=2));raise SystemExit(bool(errors))
    except (OSError,ValueError) as error:
        print(json.dumps({'ok':False,'error':str(error)}));raise SystemExit(2)
