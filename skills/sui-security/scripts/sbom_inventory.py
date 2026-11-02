#!/usr/bin/env python3
"""Normalize supported SPDX/CycloneDX/SWID inventory subsets and flag unresolved license policy."""
import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def text(value,field):
    if not isinstance(value,str) or not value.strip():raise ValueError(f'missing/invalid {field}')
    return value

def normalize(data):
    rows=[];edges=[]
    if isinstance(data,str):
        if '<!DOCTYPE' in data.upper() or '<!ENTITY' in data.upper():raise ValueError('DTD/entities unsupported')
        try:root=ET.fromstring(data)
        except ET.ParseError as error:raise ValueError('malformed SWID XML') from error
        if root.tag!='{http://standards.iso.org/iso/19770/-2/2015/schema.xsd}SoftwareIdentity':raise ValueError('unsupported SWID namespace/root')
        rows.append({'id':text(root.get('tagId'),'tagId'),'name':text(root.get('name'),'name'),'version':root.get('version'),'purl':None,'licenses':['NOASSERTION']})
        format_='SWID-2015';scope='one software identity tag; not a full dependency graph'
    elif isinstance(data,dict) and data.get('bomFormat')=='CycloneDX':
        version=data.get('specVersion')
        if version not in ('1.5','1.6','1.7'):raise ValueError('supported CycloneDX JSON versions: 1.5/1.6/1.7')
        components=data.get('components')
        if not isinstance(components,list) or not components:raise ValueError('empty/missing components')
        if any(isinstance(c,dict) and c.get('components') for c in components):raise ValueError('nested CycloneDX components need full schema/tool handling')
        for c in components:
            if not isinstance(c,dict):raise ValueError('component must be object')
            licenses=c.get('licenses',[])
            if not isinstance(licenses,list):raise ValueError('licenses must be a list')
            values=[]
            for lic in licenses:
                if not isinstance(lic,dict):raise ValueError('license must be object')
                if 'expression' in lic:values.append(text(lic['expression'],'license expression'))
                else:
                    entry=lic.get('license')
                    if not isinstance(entry,dict):raise ValueError('invalid license entry')
                    values.append(text(entry.get('id') or entry.get('name'),'license id/name'))
            rows.append({'id':text(c.get('bom-ref'),'bom-ref'),'name':text(c.get('name'),'component name'),'version':c.get('version'),'purl':c.get('purl'),'licenses':values or ['NOASSERTION']})
        deps=data.get('dependencies',[])
        if not isinstance(deps,list):raise ValueError('dependencies must be list')
        for dep in deps:
            if not isinstance(dep,dict) or not isinstance(dep.get('dependsOn'),list):raise ValueError('invalid dependency')
            edges.extend([[text(dep.get('ref'),'dependency ref'),text(target,'dependency target')] for target in dep['dependsOn']])
        format_='CycloneDX-'+version;scope='flat top-level components and dependencies'
        # A metadata root component may anchor the graph without being a packaged dependency.
        meta=data.get('metadata',{})
        if not isinstance(meta,dict):raise ValueError('metadata must be object')
        root_component=meta.get('component',{})
        if not isinstance(root_component,dict):raise ValueError('metadata.component must be object')
        root_id=root_component.get('bom-ref')
    elif isinstance(data,dict) and data.get('spdxVersion')=='SPDX-2.3':
        text(data.get('SPDXID'),'document SPDXID');text(data.get('documentNamespace'),'documentNamespace')
        packages=data.get('packages')
        if not isinstance(packages,list) or not packages:raise ValueError('empty/missing packages')
        for c in packages:
            if not isinstance(c,dict):raise ValueError('package must be object')
            refs=c.get('externalRefs',[])
            if not isinstance(refs,list) or any(not isinstance(r,dict) for r in refs):raise ValueError('invalid externalRefs')
            purls=[r.get('referenceLocator') for r in refs if r.get('referenceType')=='purl']
            rows.append({'id':text(c.get('SPDXID'),'package SPDXID'),'name':text(c.get('name'),'package name'),'version':c.get('versionInfo'),'purl':purls[0] if purls else None,'licenses':[c.get('licenseConcluded') or c.get('licenseDeclared') or 'NOASSERTION']})
        relations=data.get('relationships',[])
        if not isinstance(relations,list) or any(not isinstance(r,dict) for r in relations):raise ValueError('invalid relationships')
        for rel in relations:
            if rel.get('relationshipType')=='DEPENDS_ON':edges.append([text(rel.get('spdxElementId'),'relationship source'),text(rel.get('relatedSpdxElement'),'relationship target')])
        format_='SPDX-2.3';scope='package dependency relationships; other relationship kinds retained only in original'
    else:raise ValueError('unsupported SBOM format/version')
    ids=set()
    for row in rows:
        if row['id'] in ids:raise ValueError('duplicate component identity')
        ids.add(row['id'])
        for field in ('version','purl'):
            if row[field] is not None and not isinstance(row[field],str):raise ValueError(f'invalid {field}')
        if any(not isinstance(x,str) or not x.strip() for x in row['licenses']):raise ValueError('invalid license value')
    known=ids|({root_id} if 'root_id' in locals() and isinstance(root_id,str) else set())
    if any(a not in known or b not in known for a,b in edges):raise ValueError('dangling dependency identity')
    return {'format':format_,'components':rows,'dependencies':edges,'subset':scope,
            'limitations':'Inventory normalization only, not full official schema conformance, completeness, authenticity, vulnerability scanning or legal clearance. Preserve the original report and use its exact official schema for full validation.'}

def policy(inventory,config):
    if not isinstance(config,dict):raise ValueError('policy must be object')
    allowed=config.get('allow',[]);denied=config.get('deny',[])
    if not isinstance(allowed,list) or not isinstance(denied,list) or any(not isinstance(x,str) or not x for x in allowed+denied):raise ValueError('allow/deny must be license-id lists')
    if set(allowed)&set(denied):raise ValueError('license appears in both allow and deny')
    decisions=[]
    for row in inventory['components']:
        statuses=[]
        for expression in row['licenses']:
            # Do not collapse OR alternatives or AND/WITH exceptions into a boolean legal opinion.
            simple=bool(re.fullmatch(r'[A-Za-z0-9.+-]+',expression)) and expression not in ('NOASSERTION','NONE')
            statuses.append('deny' if simple and expression in denied else 'allow' if simple and expression in allowed else 'review')
        status='deny' if 'deny' in statuses else 'allow' if statuses and all(s=='allow' for s in statuses) else 'review'
        decisions.append({'id':row['id'],'status':status,'licenses':row['licenses']})
    return {'decisions':decisions,'needsReview':sum(x['status']=='review' for x in decisions),'denied':sum(x['status']=='deny' for x in decisions),'legalConclusion':False}

def load(path):
    p=Path(path)
    if p.stat().st_size>8388608:raise ValueError('SBOM exceeds8MiB')
    raw=p.read_text();return raw if raw.lstrip().startswith('<') else json.loads(raw)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--policy');p.add_argument('--compare');a=p.parse_args()
    try:
        result=normalize(load(a.input))
        if a.policy:result['policy']=policy(result,json.loads(Path(a.policy).read_text()))
        if a.compare:
            other=normalize(load(a.compare));old={x['purl'] or x['id'] for x in other['components']};new={x['purl'] or x['id'] for x in result['components']}
            result['diff']={'added':sorted(new-old),'removed':sorted(old-new),'note':'Identity diff; a versioned purl upgrade appears as removal plus addition. No upgrade equivalence is inferred.'}
        print(json.dumps(result,indent=2,allow_nan=False));raise SystemExit(1 if result.get('policy',{}).get('denied',0) or result.get('policy',{}).get('needsReview',0) else 0)
    except (OSError,ValueError,TypeError,AttributeError,RecursionError) as error:
        print(json.dumps({'ok':False,'error':'invalid or unsupported SBOM/policy: '+str(error)}));raise SystemExit(2)
