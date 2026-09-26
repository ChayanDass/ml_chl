"""Shared contracts and implementations for the entity-resolution pipeline.

The module deliberately uses only the standard library plus optional LightGBM so
the retrieval/index stages remain runnable on constrained machines.
"""
from __future__ import annotations
import csv, hashlib, json, math, os, pickle, random, re, shutil, sys, time, unicodedata
from array import array
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

REQUIRED=("entity_id","business_name","business_address","country")
METHODS=("exact_name","token_name","fuzzy_name","address","country","embedding_ann")
FEATURES=("name_exact","name_token_jaccard","name_char_similarity","name_length_ratio","name_comparable","address_exact","address_token_jaccard","address_char_similarity","address_comparable","country_agree","country_disagree","country_missing","cross_name_address_mean","cross_both_exact","source_s2","source_s3","retrieval_count","exact_name_hit","token_name_hit","fuzzy_name_hit","address_hit","country_hit","embedding_ann_hit","s1_name_missing","candidate_name_missing","s1_address_missing","candidate_address_missing")
VERSION="1.0.0"

def uint_array(): return array('I')

def stable_hash(x: Any) -> str: return hashlib.sha256(json.dumps(x,sort_keys=True,default=str).encode()).hexdigest()
def file_hash(p: Path) -> str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def atomic_json(path:Path,obj:Any):
 path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_text(json.dumps(obj,indent=2,sort_keys=True),encoding="utf-8"); os.replace(tmp,path)
def norm(x: str) -> str:
 x=unicodedata.normalize("NFKC",x or "").casefold().replace("&"," and ")
 return re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",x,flags=re.UNICODE)).strip()
def tokens(x:str) -> tuple[str,...]: return tuple(t for t in norm(x).split() if len(t)>1)
def jacc(a:Iterable[str],b:Iterable[str]) -> float:
 a,b=set(a),set(b); return len(a&b)/len(a|b) if a|b else 0.0
def chargrams(s:str,n=3):
 s=" "+norm(s)+" "; return {s[i:i+n] for i in range(max(0,len(s)-n+1))}
def sim(a:str,b:str)->float: return SequenceMatcher(None,norm(a),norm(b),autojunk=False).ratio() if a and b else 0.
def embed(s:str, dims=64):
 # deterministic hashed char n-gram vector: local, no external lookup/model.
 v=[0.0]*dims
 for g in chargrams(s): v[int(hashlib.blake2b(g.encode(),digest_size=8).hexdigest(),16)%dims]+=1
 z=math.sqrt(sum(q*q for q in v)); return tuple(q/z for q in v) if z else tuple(v)
def cosine(a,b): return sum(x*y for x,y in zip(a,b))

def load_records(path:Path, source:str, sample:int|None=None) -> list[dict]:
 out=[]; seen=set()
 try: f=path.open("r",encoding="utf-8",newline="")
 except UnicodeDecodeError as e: raise ValueError(f"UTF-8 decoding failure: {path}") from e
 with f:
  rd=csv.DictReader(f,delimiter="\t")
  if tuple(rd.fieldnames or ()) != REQUIRED: raise ValueError(f"{path}: expected headers {REQUIRED}, got {rd.fieldnames}")
  for ordinal,row in enumerate(rd):
   eid=(row.get("entity_id") or "").strip()
   if not eid.startswith(source+"-") or not eid: raise ValueError(f"{path}:{ordinal+2}: invalid {source} id {eid!r}")
   if eid in seen: raise ValueError(f"{path}: duplicate ID {eid}")
   seen.add(eid); row.update(source=source,ordinal=ordinal,name_n=norm(row["business_name"]),address_n=norm(row["business_address"]),country_n=norm(row["country"])); out.append(row)
   if sample and len(out)>=sample: break
 return out
def load_truth(path:Path,s1:set[str], targets:set[str], partial:bool=False) -> dict[str,set[str]]:
 ans={}
 with path.open(encoding="utf-8",newline="") as f:
  rd=csv.DictReader(f,delimiter="\t")
  if tuple(rd.fieldnames or ()) != ("source1_entity_id","matched_entity_ids"): raise ValueError("invalid ground truth header")
  for r in rd:
   i=r["source1_entity_id"]
   if i in ans: raise ValueError(f"invalid/duplicate ground truth S1 ID {i}")
   if i not in s1:
    if partial: continue
    raise ValueError(f"invalid ground truth S1 ID {i}")
   ids={x for x in (r["matched_entity_ids"] or "").split(",") if x}
   if not ids <= targets:
    if partial: ids &= targets
    else: raise ValueError(f"unknown ground truth targets for {i}")
   ans[i]=ids
 if not partial and set(ans)!=s1: raise ValueError("ground truth does not cover all S1 IDs")
 if partial:
  for i in s1: ans.setdefault(i,set())
 return ans
def validation_report(paths:dict[str,Path], artifact:Path, sample:int|None=None):
 data={}; report={"version":VERSION,"files":{},"warnings":[]}
 for k,p in paths.items():
  src={"s1":"S1","s2":"S2","s3":"S3"}.get(k)
  if src:
   data[k]=load_records(p,src,sample); report["files"][k]={"path":str(p),"rows":len(data[k]),"sha256":file_hash(p),"status":"valid"}
 if "truth" in paths:
  data["truth"]=load_truth(paths["truth"],{r['entity_id'] for r in data['s1']},{r['entity_id'] for r in data['s2']+data['s3']},bool(sample)); report["files"]["truth"]={"path":str(paths['truth']),"rows":len(data['truth']),"sha256":file_hash(paths['truth']),"status":"valid"}
 report["fingerprint"]=stable_hash(report["files"]); atomic_json(artifact,report); return data,report

class Index:
 def __init__(self, targets:list[dict], config:dict):
  self.targets={r['entity_id']:r for r in targets}; self.config=config; self.ids=[]; self.maps={k:defaultdict(uint_array) for k in ('name','token','gram','address','country')}; self.vec={}; self.ann=None; self.ann_name=None; self.ann_ids=[]
  for pos,r in enumerate(targets):
   i=r['entity_id']; self.ids.append(i); self.maps['name'][r['name_n']].append(pos) if r['name_n'] else None
   for t in tokens(r['business_name']): self.maps['token'][t].append(pos)
   for g in chargrams(r['business_name']): self.maps['gram'][g].append(pos)
   self.maps['address'][r['address_n']].append(pos) if r['address_n'] else None
   self.maps['country'][r['country_n']].append(pos) if r['country_n'] else None
   self.vec[i]=embed(r['business_name']+' '+r['business_address'])
  self._build_ann()
 def _build_ann(self):
  """Build two persisted FAISS IVF-PQ indexes; bounded exact fallback is dev-only."""
  e=self.config.get('embedding',{}); backend=e.get('backend','bruteforce'); self.ann_ids=list(self.targets)
  if backend not in ('bruteforce','auto','faiss_ivfpq'): raise ValueError(f'unsupported embedding backend {backend!r}')
  if int(e.get('dimensions',64))!=64: raise ValueError('hashed embedding dimension is fixed at 64')
  if int(e.get('pq_m',8)) <= 0 or 64 % int(e.get('pq_m',8)): raise ValueError('pq_m must be a positive divisor of embedding dimension 64')
  if backend=='bruteforce': return
  try: import faiss, numpy as np
  except ImportError:
   if backend=='auto' and len(self.targets)<=e.get('bruteforce_max_targets',100000): return
   raise RuntimeError('FAISS is required for configured full-scale embedding retrieval; install a compatible faiss build')
  d=int(e.get('dimensions',64)); n=len(self.ann_ids)
  if n<max(64,int(e.get('pq_m',8))*2):
   # IVF-PQ cannot be trained robustly on a tiny smoke corpus; bounded exact is explicit.
   return
  nlist=min(int(e.get('nlist',4096)),max(1,n//max(32,int(e.get('pq_m',8))*4)))
  m=int(e.get('pq_m',8)); bits=int(e.get('pq_nbits',8)); sample=min(n,int(e.get('train_samples',200000)))
  def make(vectors):
   x=np.asarray(vectors,dtype='float32'); q=faiss.IndexFlatIP(d); idx=faiss.IndexIVFPQ(q,d,nlist,m,bits,faiss.METRIC_INNER_PRODUCT)
   idx.train(x[:sample]);idx.add(x);idx.nprobe=min(int(e.get('nprobe',32)),nlist);return idx
  self.ann=make([self.vec[i] for i in self.ann_ids]); self.ann_name=make([embed(self.targets[i]['business_name']) for i in self.ann_ids])
  # IVF-PQ owns compact codes; retaining Python tuple vectors would defeat its memory purpose.
  self.vec={}
 def memory_stats(self):
  """Measured compact posting payload; excludes Python dict/string allocator overhead."""
  postings=sum(len(v) for table in self.maps.values() for v in table.values())
  return {'targets':len(self.ids),'posting_references':postings,'posting_payload_bytes':postings*array('I').itemsize,'embedding_backend':self.config.get('embedding',{}).get('backend','bruteforce'),'ann_ready':self.ann is not None}
 def __getstate__(self):
  state=dict(self.__dict__)
  if self.ann is not None:
   import faiss
   state['_ann_bytes']=bytes(faiss.serialize_index(self.ann));state['_ann_name_bytes']=bytes(faiss.serialize_index(self.ann_name));state['ann']=None;state['ann_name']=None
  return state
 def __setstate__(self,state):
  ann_bytes=state.pop('_ann_bytes',None); name_bytes=state.pop('_ann_name_bytes',None);self.__dict__.update(state)
  if ann_bytes is not None:
   try:
    import faiss, numpy as np
    self.ann=faiss.deserialize_index(np.frombuffer(ann_bytes,dtype='uint8'));self.ann_name=faiss.deserialize_index(np.frombuffer(name_bytes,dtype='uint8'))
   except ImportError as e: raise RuntimeError('FAISS is required to load this persisted ANN index') from e
 def save(self,path:Path, manifest:dict):
  path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix('.tmp');
  with tmp.open('wb') as f: pickle.dump(self,f,pickle.HIGHEST_PROTOCOL)
  os.replace(tmp,path); manifest.update(path=str(path),checksum=file_hash(path),status='complete'); atomic_json(path.with_suffix('.manifest.json'),manifest)
 @classmethod
 def load(cls,path:Path, expected:dict):
  m=json.loads(path.with_suffix('.manifest.json').read_text());
  for k in ('input_hash','preprocess_hash','config_hash'):
   if m.get(k)!=expected.get(k): raise ValueError(f'incompatible index {k}')
  if m['checksum']!=file_hash(path): raise ValueError('corrupt index checksum')
  with path.open('rb') as f:return pickle.load(f)
 def _take(self, ids, limit): return list(dict.fromkeys(ids))[:limit]
 def query(self,r:dict):
  return {m:self.query_method(r,m) for m in METHODS}
  c=self.config['retrieval']; mx=c['max_postings']; out={m:{} for m in METHODS}
  for i in self._take(self.maps['name'].get(r['name_n'],[]),mx): out['exact_name'][i]=1.0
  counts=Counter(i for t in tokens(r['business_name']) for i in self.maps['token'].get(t,[])[:mx])
  for i,n in counts.most_common(c['token_limit']): out['token_name'][i]=n/max(1,len(tokens(r['business_name'])))
  gcounts=Counter(i for g in chargrams(r['business_name']) for i in self.maps['gram'].get(g,[])[:mx])
  for i,_ in gcounts.most_common(c['fuzzy_limit']*4):
   q=sim(r['business_name'],self.targets[i]['business_name'])
   if q>=.35: out['fuzzy_name'][i]=q
  out['fuzzy_name']=dict(sorted(out['fuzzy_name'].items(),key=lambda x:(-x[1],x[0]))[:c['fuzzy_limit']])
  for i in self._take(self.maps['address'].get(r['address_n'],[]),c['address_limit']): out['address'][i]=1.0
  ac=Counter(i for t in tokens(r['business_address']) for i in self.maps['token'].get(t,[])[:mx])
  for i,n in ac.most_common(c['address_limit']): out['address'].setdefault(i,n/max(1,len(tokens(r['business_address']))))
  # Country only prioritizes a bounded lexical fallback; never filters other methods.
  country_ids=self.maps['country'].get(r['country_n'],[])[:mx]
  for i,n in Counter(i for t in tokens(r['business_name']) for i in country_ids if t in tokens(self.targets[i]['business_name'])).most_common(c['country_limit']): out['country'][i]=n
  qv=embed(r['business_name']+' '+r['business_address']); ranked=sorted(((cosine(qv,v),i) for i,v in self.vec.items()),reverse=True)
  for score,i in ranked[:c['embedding_limit']]:
   if score>0: out['embedding_ann'][i]=score
  return out

 def query_method(self,r:dict,method:str):
  """Method-level retrieval isolates failed families during recovery."""
  if method not in METHODS: raise ValueError(f'unknown retrieval method {method}')
  c=self.config['retrieval']; mx=c['max_postings']
  if method=='exact_name': return {self.ids[i]:1.0 for i in self._take(self.maps['name'].get(r['name_n'],[]),mx)}
  if method=='token_name':
   counts=Counter(i for t in tokens(r['business_name']) for i in self.maps['token'].get(t,[])[:mx])
   return {self.ids[i]:n/max(1,len(tokens(r['business_name']))) for i,n in counts.most_common(c['token_limit'])}
  if method=='fuzzy_name':
   gcounts=Counter(i for g in chargrams(r['business_name']) for i in self.maps['gram'].get(g,[])[:mx]); hits={}
   for i,_ in gcounts.most_common(c['fuzzy_limit']*4):
    q=sim(r['business_name'],self.targets[self.ids[i]]['business_name'])
    if q>=.35: hits[self.ids[i]]=q
   return dict(sorted(hits.items(),key=lambda x:(-x[1],x[0]))[:c['fuzzy_limit']])
  if method=='address':
   hits={self.ids[i]:1.0 for i in self._take(self.maps['address'].get(r['address_n'],[]),c['address_limit'])}
   counts=Counter(i for t in tokens(r['business_address']) for i in self.maps['token'].get(t,[])[:mx])
   for i,n in counts.most_common(c['address_limit']): hits.setdefault(self.ids[i],n/max(1,len(tokens(r['business_address']))))
   return hits
  if method=='country':
   country_ids=self.maps['country'].get(r['country_n'],[])[:mx]
   return {self.ids[i]:n for i,n in Counter(i for t in tokens(r['business_name']) for i in country_ids if t in tokens(self.targets[self.ids[i]]['business_name'])).most_common(c['country_limit'])}
  e=self.config.get('embedding',{}); k=c['embedding_limit']
  if self.ann is not None:
   import numpy as np
   # Union name-focused and name+address ANN neighbours, retaining maximum score evidence.
   hits={}
   for ann,v in ((self.ann,embed(r['business_name']+' '+r['business_address'])),(self.ann_name,embed(r['business_name']))):
    scores,ids=ann.search(np.asarray([v],dtype='float32'),k)
    for score,pos in zip(scores[0],ids[0]):
     if pos>=0 and score>0:hits[self.ann_ids[int(pos)]]=max(hits.get(self.ann_ids[int(pos)],-1),float(score))
   return dict(sorted(hits.items(),key=lambda x:(-x[1],x[0]))[:k])
  if len(self.targets)>e.get('bruteforce_max_targets',100000): raise RuntimeError('embedding fallback refuses exhaustive full-scale search; build FAISS IVF-PQ index')
  qv=embed(r['business_name']+' '+r['business_address'])
  return {i:score for score,i in sorted(((cosine(qv,v),i) for i,v in self.vec.items()),reverse=True)[:k] if score>0}

def candidates(s1:list[dict], index:Index):
 rows=[]
 for r in s1:
  merged={}
  for method,hits in index.query(r).items():
   for i,score in hits.items(): merged.setdefault(i,{})[method]=score
  for i,evidence in merged.items(): rows.append({'s1_id':r['entity_id'],'candidate_id':i,'candidate_source':index.targets[i]['source'],'methods':sorted(evidence),'evidence':evidence})
 return rows
def candidate_method_rows(s1:list[dict], index:Index, method:str):
 rows=[]
 for r in s1:
  for candidate_id,score in index.query_method(r,method).items():
   rows.append({'s1_id':r['entity_id'],'candidate_id':candidate_id,'candidate_source':index.targets[candidate_id]['source'],'method':method,'score':score})
 return rows
def union_candidate_method_rows(method_rows):
 merged={}
 for r in method_rows:
  key=(r['s1_id'],r['candidate_id']); out=merged.setdefault(key,{'s1_id':r['s1_id'],'candidate_id':r['candidate_id'],'candidate_source':r['candidate_source'],'methods':[],'evidence':{}})
  if r['method'] not in out['methods']: out['methods'].append(r['method'])
  out['evidence'][r['method']]=r['score']
 return [merged[k] for k in sorted(merged)]
def resumable_candidates(s1, index, store, batch_size):
 """Persist each retrieval-family × deterministic S1 batch before unioning it."""
 all_rows=[]
 for start in range(0,len(s1),batch_size):
  part=s1[start:start+batch_size]; bid=f'{start:012d}-{start+len(part):012d}'
  method_rows=[]
  for method in METHODS:
   method_rows.extend(store.run('candidate_methods',f'{bid}.{method}',lambda m=method,p=part:candidate_method_rows(p,index,m),{'method':method,'s1_start':start,'s1_end':start+len(part)}))
  all_rows.extend(store.run('candidate_union',bid,lambda r=method_rows:union_candidate_method_rows(r),{'s1_start':start,'s1_end':start+len(part)}))
 return all_rows
def iter_resumable_candidates(s1,index,store,batch_size):
 """Disk-backed candidate stream: only one S1 partition is resident."""
 for start in range(0,len(s1),batch_size):
  part=s1[start:start+batch_size]; bid=f'{start:012d}-{start+len(part):012d}'; method_rows=[]
  for method in METHODS:
   method_rows.extend(store.run('candidate_methods',f'{bid}.{method}',lambda m=method,p=part:candidate_method_rows(p,index,m),{'method':method,'s1_start':start,'s1_end':start+len(part)}))
  yield bid,part,store.run('candidate_union',bid,lambda r=method_rows:union_candidate_method_rows(r),{'s1_start':start,'s1_end':start+len(part)})
def resumable_features(candidate_rows,s1,targets,store,batch_size):
 by_s1=defaultdict(list)
 for r in candidate_rows: by_s1[r['s1_id']].append(r)
 all_rows=[]
 for start in range(0,len(s1),batch_size):
  part=s1[start:start+batch_size]; bid=f'{start:012d}-{start+len(part):012d}'; pairs=[p for r in part for p in by_s1[r['entity_id']]]
  rows=store.run('features',bid,lambda p=pairs,s=part:feature_rows(p,s,targets),{'s1_start':start,'s1_end':start+len(part),'pair_count':len(pairs),'schema_hash':schema_manifest()['schema_hash']})
  keys=[(r['s1_id'],r['candidate_id']) for r in rows]
  if len(keys)!=len(set(keys)) or set(keys)!={(r['s1_id'],r['candidate_id']) for r in pairs}: raise ValueError(f'feature/candidate alignment failure in {bid}')
  all_rows.extend(rows)
 return all_rows
def iter_resumable_features(candidate_partitions,targets,store):
 """Feature stream aligned to candidate partitions; validates each partition."""
 for bid,part,pairs in candidate_partitions:
  rows=store.run('features',bid,lambda p=pairs,s=part:feature_rows(p,s,targets),{'pair_count':len(pairs),'schema_hash':schema_manifest()['schema_hash']})
  keys=[(r['s1_id'],r['candidate_id']) for r in rows]
  if len(keys)!=len(set(keys)) or set(keys)!={(r['s1_id'],r['candidate_id']) for r in pairs}: raise ValueError(f'feature/candidate alignment failure in {bid}')
  yield bid,part,pairs,rows
def resumable_scores(feature_rows_,s1,store,batch_size,model):
 by_s1=defaultdict(list)
 for r in feature_rows_: by_s1[r['s1_id']].append(r)
 all_rows=[]
 for start in range(0,len(s1),batch_size):
  part=s1[start:start+batch_size]; bid=f'{start:012d}-{start+len(part):012d}'; rows=[r for x in part for r in by_s1[x['entity_id']]]
  def score(rows=rows):
   probs=model.predict_proba([[float(r.get(x,0)) for x in FEATURES] for r in rows])[:,1] if rows else []
   return [{**r,'probability':float(p)} for r,p in zip(rows,probs)]
  all_rows.extend(store.run('scores',bid,score,{'s1_start':start,'s1_end':start+len(part),'pair_count':len(rows)}))
 return all_rows
def score_partition(rows,model):
 x=feature_matrix(rows) if rows else []
 probs=model.predict_proba(x)[:,1] if rows else []
 return [{**r,'probability':float(p)} for r,p in zip(rows,probs)]
def candidate_report(rows, truth, s1_count, target_count):
 by=defaultdict(set); meth=Counter()
 for r in rows: by[r['s1_id']].add(r['candidate_id']); meth.update(r['methods'])
 positives=sum(map(len,truth.values())) if truth else 0; found=sum(len(by[k]&v) for k,v in (truth or {}).items())
 return {'pairs':len(rows),'mean_pairs':len(rows)/max(s1_count,1),'reduction_ratio':1-len(rows)/max(s1_count*target_count,1),'candidate_recall':found/max(positives,1),'candidate_misses':positives-found,'method_hits':dict(meth)}

def feature_rows(rows, s1:list[dict], targets:dict[str,dict]):
 a={x['entity_id']:x for x in s1}; ans=[]
 for p in rows:
  x,y=a[p['s1_id']],targets[p['candidate_id']]; nt,at=tokens(x['business_name']),tokens(y['business_name']); na,aa=tokens(x['business_address']),tokens(y['business_address'])
  nm=bool(x['name_n'] and y['name_n']); am=bool(x['address_n'] and y['address_n']); cm=bool(x['country_n'] and y['country_n'])
  d={'s1_id':p['s1_id'],'candidate_id':p['candidate_id'],'candidate_source':p['candidate_source'],'methods':p['methods']}
  d.update(name_exact=float(nm and x['name_n']==y['name_n']),name_token_jaccard=jacc(nt,at),name_char_similarity=sim(x['business_name'],y['business_name']),name_length_ratio=min(len(x['name_n']),len(y['name_n']))/max(len(x['name_n']),len(y['name_n']),1),name_comparable=float(nm),address_exact=float(am and x['address_n']==y['address_n']),address_token_jaccard=jacc(na,aa),address_char_similarity=sim(x['business_address'],y['business_address']),address_comparable=float(am),country_agree=float(cm and x['country_n']==y['country_n']),country_disagree=float(cm and x['country_n']!=y['country_n']),country_missing=float(not cm),source_s2=float(y['source']=='S2'),source_s3=float(y['source']=='S3'),retrieval_count=float(len(p['methods'])),s1_name_missing=float(not x['name_n']),candidate_name_missing=float(not y['name_n']),s1_address_missing=float(not x['address_n']),candidate_address_missing=float(not y['address_n']))
  d['cross_name_address_mean']=(d['name_char_similarity']+d['address_char_similarity'])/2; d['cross_both_exact']=d['name_exact']*d['address_exact']
  for m in METHODS:d[m+'_hit']=float(m in p['methods'])
  ans.append(d)
 return ans
def schema_manifest(): return {'version':VERSION,'features':list(FEATURES),'schema_hash':stable_hash(FEATURES)}
def split_ids(ids,truth,frac,seed):
 # deterministic stratification by singleton status prevents a singleton-only validation accident.
 groups=defaultdict(list)
 for i in ids: groups[bool(truth[i])].append(i)
 va=set()
 for g,v in groups.items():
  random.Random(seed+int(g)).shuffle(v); va.update(v[:max(1,round(len(v)*frac))])
 return set(ids)-va,va
def label_and_sample(rows,truth,train_ids,negative_ratio,seed):
 pos=[]; neg=[]
 for r in rows:
  d=dict(r); d['label']=int(r['candidate_id'] in truth[r['s1_id']]); (pos if d['label'] else neg).append(d)
 # all positives retained; deterministic negatives, bounded per total positive.
 random.Random(seed).shuffle(neg); return pos+neg[:max(len(pos)*negative_ratio,100)]
def macro_f05(pred:dict[str,set[str]],truth:dict[str,set[str]]):
 scores=[]
 for i,t in truth.items():
  p=pred.get(i,set())
  if not p and not t: scores.append(1.); continue
  if not p or not t: scores.append(0.); continue
  pr=len(p&t)/len(p); rc=len(p&t)/len(t); scores.append(1.25*pr*rc/(.25*pr+rc) if pr+rc else 0.)
 return sum(scores)/max(len(scores),1)
def feature_matrix(rows):
 """One float32 allocation replaces transient Python list-of-list model matrices."""
 import numpy as np
 x=np.empty((len(rows),len(FEATURES)),dtype=np.float32)
 for i,row in enumerate(rows): x[i]=[float(row.get(f,0.0)) for f in FEATURES]
 return x
def train_model(train, valid, model_cfg):
 try:
  import lightgbm as lgb
 except ImportError as e: raise RuntimeError('LightGBM is required for model training; install requirements.txt') from e
 import numpy as np
 xt=feature_matrix(train); yt=np.fromiter((int(x['label']) for x in train),dtype=np.uint8,count=len(train)); xv=feature_matrix(valid); yv=np.fromiter((int(x['label']) for x in valid),dtype=np.uint8,count=len(valid))
 m=lgb.LGBMClassifier(**model_cfg,objective='binary',verbosity=-1); m.fit(xt,yt,eval_set=[(xv,yv)],callbacks=[]); return m,xv
def write_jsonl(path:Path, rows):
 path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix('.tmp')
 with tmp.open('w',encoding='utf8') as f:
  for r in rows:f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n')
 os.replace(tmp,path); atomic_json(path.with_suffix('.manifest.json'),{'status':'complete','rows':len(rows),'checksum':file_hash(path),'version':VERSION})
def read_jsonl(path):
 with path.open(encoding='utf8') as f: return [json.loads(x) for x in f]
def validate_outputs(match:Path,cand:Path,test_s1:list[dict],targets:set[str]):
 expected=[r['entity_id'] for r in test_s1]; cs={}
 parsed={}
 for path,col in ((match,'matched_entity_ids'),(cand,'candidate_entity_ids')):
  with path.open(encoding='utf8',newline='') as f:
   rd=csv.DictReader(f,delimiter='\t'); rows=list(rd)
  if rd.fieldnames != ['source1_entity_id',col] or [x['source1_entity_id'] for x in rows]!=expected: raise ValueError(f'{path}: headers/order/coverage invalid')
  vals={}
  for r in rows:
   ids=[x for x in (r[col] or '').split(',') if x]
   if len(ids)!=len(set(ids)) or not set(ids)<=targets: raise ValueError(f'{path}: invalid list for {r["source1_entity_id"]}')
   vals[r['source1_entity_id']]=set(ids)
  parsed[col]=vals
 cs=parsed['candidate_entity_ids']
 if any(not v<=cs[k] for k,v in parsed['matched_entity_ids'].items()):raise ValueError('prediction outside candidate set')
 return True
def validate_outputs_streaming(match:Path,cand:Path,test_s1,targets:set[str]):
 """Validate output in order without materializing all TSV rows or candidate lists."""
 with match.open(encoding='utf8',newline='') as mf,cand.open(encoding='utf8',newline='') as cf:
  mr,cr=csv.DictReader(mf,delimiter='\t'),csv.DictReader(cf,delimiter='\t')
  if mr.fieldnames!=['source1_entity_id','matched_entity_ids'] or cr.fieldnames!=['source1_entity_id','candidate_entity_ids']: raise ValueError('output headers invalid')
  for s1 in test_s1:
   m,c=next(mr,None),next(cr,None)
   if m is None or c is None or m['source1_entity_id']!=s1['entity_id'] or c['source1_entity_id']!=s1['entity_id']: raise ValueError('output order/coverage invalid')
   mids=[x for x in (m['matched_entity_ids'] or '').split(',') if x]; cids=[x for x in (c['candidate_entity_ids'] or '').split(',') if x]
   if len(mids)!=len(set(mids)) or len(cids)!=len(set(cids)) or not set(mids)<=set(cids) or not set(cids)<=targets: raise ValueError(f'output list invalid for {s1["entity_id"]}')
  if next(mr,None) is not None or next(cr,None) is not None: raise ValueError('extra output rows')
 return True
