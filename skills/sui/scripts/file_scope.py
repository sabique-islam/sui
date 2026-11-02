"""Content fingerprints for explicit local input files; not a filesystem sandbox."""
import hashlib,json,stat
from pathlib import Path,PurePosixPath

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def safe_path(root,name):
 if not isinstance(name,str) or not name or chr(92) in name or chr(0) in name:raise ValueError('input paths must be canonical relative POSIX paths')
 p=PurePosixPath(name)
 if p.is_absolute() or '..' in p.parts or name!=p.as_posix() or name=='.':raise ValueError('input path escapes or is not canonical')
 if '.git' in p.parts:raise ValueError('do not fingerprint internal repository metadata')
 if (p.name.startswith('.env') and p.name not in {'.env.example','.env.sample'}) or p.suffix in {'.pem','.key'}:raise ValueError('do not fingerprint credential files')
 root=Path(root).resolve();current=root
 for part in p.parts:
  current=current/part
  if current.is_symlink():raise ValueError('symlink inputs are not supported')
 if not current.resolve().is_relative_to(root):raise ValueError('input escapes root')
 return current

def capture(root,inputs):
 if not Path(root).is_dir():raise ValueError('root must be a directory')
 if not isinstance(inputs,list) or not inputs or len(inputs)>1000 or any(not isinstance(p,str) for p in inputs):raise ValueError('inputs must contain 1..1000 relative file paths')
 if len(set(inputs))!=len(inputs):raise ValueError('duplicate input paths')
 rows=[];total=0;present=0
 for name in sorted(inputs):
  p=safe_path(root,name)
  if not p.exists():rows.append({'path':name,'sha256':None,'bytes':0,'executable':0});continue
  if not p.is_file():raise ValueError('inputs must be files, not directories or special devices')
  meta=p.stat()
  if meta.st_size>8388608:raise ValueError('input exceeds 8 MiB; choose a bounded relevant scope')
  total+=meta.st_size
  if total>67108864:raise ValueError('input scope exceeds 64 MiB')
  h=hashlib.sha256()
  with p.open('rb') as f:
   read=0
   while True:
    block=f.read(65536)
    if not block:break
    read+=len(block)
    if read>8388608:raise ValueError('input grew beyond scope limit')
    h.update(block)
  rows.append({'path':name,'sha256':h.hexdigest(),'bytes':read,'executable':stat.S_IMODE(meta.st_mode)&0o111});present+=1
 if not present:raise ValueError('scope needs at least one existing file')
 return {'files':rows,'digest':hashlib.sha256(canonical(rows)).hexdigest()}
