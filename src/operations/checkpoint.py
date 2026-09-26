"""Atomic, lineage-bound checkpoint units shared by every pipeline stage."""
from __future__ import annotations
import json, os, time
from pathlib import Path
from typing import Callable, Iterable, Any
from ..core import VERSION, atomic_json, file_hash, read_jsonl, stable_hash, write_jsonl

class CheckpointStore:
 """A completed unit is reusable only if its payload and full lineage validate."""
 def __init__(self, root: str | Path, lineage: dict[str, Any]):
  self.root=Path(root); self.lineage={**lineage,'producer_version':VERSION}
 def _payload(self, stage, unit): return self.root/stage/f'{unit}.jsonl'
 def _manifest(self, stage, unit): return self._payload(stage,unit).with_suffix('.manifest.json')
 def _expected(self): return stable_hash(self.lineage)
 def load(self, stage:str, unit:str):
  payload=self._payload(stage,unit); manifest=self._manifest(stage,unit)
  try:
   m=json.loads(manifest.read_text(encoding='utf8'))
   if m.get('status')!='complete' or m.get('lineage_hash')!=self._expected(): raise ValueError('stale or incompatible lineage')
   if m.get('checksum')!=file_hash(payload): raise ValueError('checksum mismatch')
   rows=read_jsonl(payload)
   if len(rows)!=m.get('rows'): raise ValueError('row count mismatch')
   return rows
  except (FileNotFoundError, ValueError, json.JSONDecodeError, OSError):
   for p in (payload,manifest):
    if p.exists(): os.replace(p,p.with_name(p.name+f'.corrupt-{int(time.time()*1000)}'))
   return None
 def valid_payload(self, stage:str, unit:str):
  """Validate manifest/payload without loading a potentially huge JSONL into RAM."""
  payload=self._payload(stage,unit); manifest=self._manifest(stage,unit)
  try:
   m=json.loads(manifest.read_text(encoding='utf8'))
   return (m.get('status')=='complete' and m.get('lineage_hash')==self._expected() and payload.exists() and m.get('checksum')==file_hash(payload))
  except (FileNotFoundError, ValueError, json.JSONDecodeError, OSError):
   return False
 def commit(self, stage:str, unit:str, rows:Iterable[dict], extra:dict|None=None):
  rows=list(rows); payload=self._payload(stage,unit); write_jsonl(payload,rows)
  m=json.loads(self._manifest(stage,unit).read_text(encoding='utf8'))
  m.update({'status':'complete','lineage':self.lineage,'lineage_hash':self._expected(),'stage':stage,'unit':unit,'completed_at':time.time(),**(extra or {})})
  atomic_json(self._manifest(stage,unit),m); return rows
 def run(self, stage:str, unit:str, producer:Callable[[],Iterable[dict]], extra:dict|None=None):
  cached=self.load(stage,unit)
  return cached if cached is not None else self.commit(stage,unit,producer(),extra)
 def iter_stage(self, stage:str):
  """Yield validated deterministic partitions without concatenating them."""
  folder=self.root/stage
  for manifest in sorted(folder.glob('*.manifest.json')) if folder.exists() else ():
   unit=manifest.name.removesuffix('.manifest.json')
   rows=self.load(stage,unit)
   if rows is None: raise ValueError(f'invalid checkpoint {stage}/{unit}')
   yield unit,rows

def atomic_pickle(path:Path, value:Any, lineage:dict|None=None):
 import pickle
 path.parent.mkdir(parents=True,exist_ok=True); temp=path.with_suffix(path.suffix+'.tmp')
 with temp.open('wb') as f: pickle.dump(value,f,pickle.HIGHEST_PROTOCOL)
 os.replace(temp,path)
 atomic_json(path.with_suffix('.manifest.json'),{'status':'complete','checksum':file_hash(path),'version':VERSION,'lineage':lineage,'lineage_hash':stable_hash(lineage) if lineage is not None else None,'completed_at':time.time()})

def valid_pickle(path:Path, lineage:dict|None=None):
 import pickle
 try:
  m=json.loads(path.with_suffix('.manifest.json').read_text())
  if m.get('status')!='complete' or m.get('checksum')!=file_hash(path): return None
  if lineage is not None and m.get('lineage_hash')!=stable_hash(lineage): return None
  with path.open('rb') as f:return pickle.load(f)
 except (OSError,ValueError,json.JSONDecodeError,pickle.UnpicklingError): return None
