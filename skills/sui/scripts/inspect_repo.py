#!/usr/bin/env python3
"""Bounded metadata inspection. Never imports or executes repository code."""
import argparse,json,os,subprocess
from pathlib import Path

EXCLUDE={'.git','node_modules','.venv','venv','dist','build','coverage','.next','vendor','__pycache__','.cache'}
MANIFESTS={'package.json','pyproject.toml','Cargo.toml','go.mod','Gemfile','pom.xml','build.gradle','Makefile','Dockerfile','docker-compose.yml','compose.yaml','AGENTS.md'}
LOCKS={'package-lock.json','pnpm-lock.yaml','yarn.lock','bun.lock','bun.lockb','uv.lock','poetry.lock','Cargo.lock','go.sum','Gemfile.lock'}
def inspect(root,max_files=20000):
 root=Path(root).resolve()
 if not root.is_dir():raise ValueError('root must be a directory')
 if not 1<=max_files<=1000000:raise ValueError('max_files out of range')
 manifests=[];locks=[];tests=[];configs=[];count=0;truncated=False
 for parent,dirs,files in os.walk(root,followlinks=False):
  dirs[:]=sorted(d for d in dirs if d not in EXCLUDE and not (Path(parent)/d).is_symlink())
  for name in sorted(files):
   p=Path(parent)/name
   if p.is_symlink():continue
   count+=1
   if count>max_files:truncated=True;break
   rel=p.relative_to(root).as_posix()
   if name in MANIFESTS:manifests.append(rel)
   if name in LOCKS:locks.append(rel)
   if name.startswith('test_') or '.test.' in name or '.spec.' in name:tests.append(rel)
   if rel.startswith('.github/workflows/') or name in {'pytest.ini','tox.ini','tsconfig.json','eslint.config.js'}:configs.append(rel)
  if truncated:break
 result={'root':str(root),'fileCount':min(count,max_files),'truncated':truncated,'manifests':manifests,'lockfiles':locks,'testFiles':tests[:100],'ciAndChecks':configs[:100],'executedProjectCode':False,'contentsRead':False}
 # No remotes or manifest values: they can contain credentials or executable hooks.
 try:
  p=subprocess.run(['git','-c','core.fsmonitor=false','-c','core.untrackedCache=false','-C',str(root),'status','--porcelain','--untracked-files=no'],capture_output=True,text=True,timeout=5,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
  result['trackedChanges']=p.stdout.splitlines()[:100] if p.returncode==0 else None
 except (OSError,subprocess.TimeoutExpired):result['trackedChanges']=None
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root');p.add_argument('--max-files',type=int,default=20000);a=p.parse_args()
 try:print(json.dumps(inspect(a.root,a.max_files),indent=2))
 except (ValueError,OSError) as e:print(json.dumps({'error':str(e)}));raise SystemExit(2)
