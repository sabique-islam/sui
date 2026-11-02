#!/usr/bin/env python3
"""Resolve Sui skills by frontmatter after reconciliation and check pack integrity."""
import argparse,json,re
from pathlib import Path

NAMES=['sui','sui-discovery','sui-architecture','sui-implementation','sui-review','sui-testing','sui-debugging','sui-delivery','sui-reliability','sui-security','sui-ai-systems','sui-evidence','sui-maintenance']
def resolve(root):
 found={}
 for p in sorted(Path(root).glob('*/SKILL.md')):
  raw=p.read_text()
  match=re.match(r'\A---\s*\nname:\s*([a-z0-9-]+)\s*\n',raw)
  if match and match.group(1) in NAMES:found.setdefault(match.group(1),[]).append(p.parent)
 return found

def validate(root):
 found=resolve(root);errors=[]
 for name in NAMES:
  paths=found.get(name,[])
  if len(paths)!=1:errors.append(f'{name}: expected one active skill, found {len(paths)}');continue
  path=paths[0];text=(path/'SKILL.md').read_text()
  if '[TODO' in text:errors.append(f'{name}: unresolved placeholder')
  if len(text.splitlines())>=500:errors.append(f'{name}: body too large')
  if not (path/'agents/openai.yaml').is_file():errors.append(f'{name}: missing UI metadata')
  for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',text):
   if '://' not in target and not target.startswith('#') and not (path/target.split('#')[0]).is_file():errors.append(f'{name}: broken resource link {target}')
  for target in re.findall(r'(?<![\w/])((?:scripts|assets|references)/[a-zA-Z0-9_./-]+\.(?:py|json|md|yaml))',text):
   if not (path/target).is_file():errors.append(f'{name}: missing referenced file {target}')
 if len(found.get('sui',[]))==1:
  core=found['sui'][0]
  try:
   pack=json.loads((core/'assets/pack.json').read_text())
   if set(pack['skills'])!=set(NAMES):errors.append('pack manifest membership differs')
   registry=json.loads((core/'references/sources.json').read_text())
   if pack.get('sourceCount')!=len(registry['sources']):errors.append('source count differs from manifest')
   inventory=pack.get('requiredFiles')
   if pack.get('schemaVersion')!=2:errors.append('pack schemaVersion must be 2')
   if inventory is None:errors.append('required file inventory is mandatory')
   else:
    if not isinstance(inventory,dict) or set(inventory)!=set(NAMES):errors.append('required file inventory membership differs')
    else:
     for name,files in inventory.items():
      if not isinstance(files,list) or not files or any(not isinstance(f,str) for f in files):errors.append(f'{name}: invalid required file list');continue
      if len(files)!=len(set(files)):errors.append(f'{name}: duplicate required file')
      for essential in ['SKILL.md','agents/openai.yaml','references/field-guide.md' if name!='sui' else 'scripts/validate_pack.py']:
       if essential not in files:errors.append(f'{name}: essential file omitted from inventory: {essential}')
      if name=='sui-delivery' and 'scripts/file_scope.py' not in files:errors.append('sui-delivery: mandatory import helper omitted')
      for f in files:
       rel=Path(f)
       if rel.is_absolute() or '..' in rel.parts:errors.append(f'{name}: unsafe required file path');continue
       paths=found.get(name,[])
       if len(paths)==1 and not (paths[0]/rel).is_file():errors.append(f'{name}: required file missing: {f}')
  except (OSError,ValueError,KeyError,TypeError):errors.append('missing or invalid corpus/manifest')
 return {'ok':not errors,'errors':errors,'resolved':{k:[str(p) for p in v] for k,v in found.items()}}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('skills_root');a=p.parse_args();r=validate(a.skills_root);print(json.dumps(r,indent=2));raise SystemExit(0 if r['ok'] else 1)
