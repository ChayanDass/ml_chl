from __future__ import annotations
import argparse,json,os,pickle,platform,shutil,subprocess,time
from pathlib import Path
from .core import *
from .operations.checkpoint import CheckpointStore, atomic_pickle, valid_pickle
from .operations.resources import assert_capacity, resource_snapshot
from .operations.progress import PipelineProgress

def paths(data,split):
 root=Path(data)/split; p={'s1':root/f'{split}_source1.tsv','s2':root/f'{split}_source2.tsv','s3':root/f'{split}_source3.tsv'}
 if split=='train':p['truth']=root/'train_ground_truth.tsv'
 return p
def cfg(path): return json.loads(Path(path).read_text())
def candidate_config(c): return {'retrieval':c['retrieval'],'embedding':c.get('embedding',{}),'multilingual':c.get('multilingual',{})}
def normalized(data,split,art,sample=None):
 d,rep=validation_report(paths(data,split),Path(art)/'validation'/f'{split}.json',sample)
 store=CheckpointStore(Path(art)/'recovery'/split,{'input_hash':rep['fingerprint'],'preprocess':'nfkc-casefold-v1','sample':sample})
 # Input is still validated on each invocation; normalization partitions are only re-written when invalid.
 store.run('normalized','s1',lambda:d['s1']); store.run('normalized','targets',lambda:d['s2']+d['s3'])
 return d,rep
def index_for(data,split,art,c,sample=None):
 d,rep=normalized(data,split,art,sample); retrieval_config=candidate_config(c); h=stable_hash({'input':rep['fingerprint'],'config':retrieval_config,'version':VERSION}); path=Path(art)/'indexes'/split/(h+'.pkl'); expected={'input_hash':rep['fingerprint'],'preprocess_hash':stable_hash('nfkc-casefold-v1'),'config_hash':stable_hash(retrieval_config)}
 if path.exists():
  try: return d,Index.load(path,expected),h
  except (ValueError,OSError,EOFError,pickle.UnpicklingError):
   # Preserve the bad index for inspection; rebuild only this incompatible index.
   os.replace(path,path.with_name(path.name+f'.corrupt-{int(time.time()*1000)}'))
   mp=path.with_suffix('.manifest.json')
   if mp.exists(): os.replace(mp,mp.with_name(mp.name+f'.corrupt-{int(time.time()*1000)}'))
 idx=Index(d['s2']+d['s3'],c); idx.save(path,expected); return d,idx,h
def run_train(a):
 c=cfg(a.config); ui=PipelineProgress(a.experiment,a.artifacts); ui.update('Dataset Preparation','Running'); assert_capacity(a.artifacts,c['resources']); d,idx,h=index_for(a.data,'train',a.artifacts,c,a.sample); ui.update('Dataset Preparation','Completed'); base=Path(a.artifacts)/'experiments'/a.experiment
 lineage={'input_hash':stable_hash([x['entity_id'] for x in d['s1']]),'index_hash':h,'candidate_config':candidate_config(c),'schema_hash':schema_manifest()['schema_hash'],'training_config':{'seed':c['seed'],'validation_fraction':c['validation_fraction'],'negative_ratio':c['negative_ratio'],'model':c['model']},'run':'train'}; store=CheckpointStore(base/'recovery',lineage)
 splitrows=store.run('training_prep','split',lambda:[{'kind':'train','id':x} for x in sorted(split_ids([x['entity_id'] for x in d['s1']],d['truth'],c['validation_fraction'],c['seed'])[0])]+[{'kind':'validation','id':x} for x in sorted(split_ids([x['entity_id'] for x in d['s1']],d['truth'],c['validation_fraction'],c['seed'])[1])])
 train_ids={x['id'] for x in splitrows if x['kind']=='train'}; val_ids={x['id'] for x in splitrows if x['kind']=='validation'}
 # Stream partitions through recovery. Only labelled train/validation rows remain resident;
 # this removes the former all-candidates + all-features duplication from peak RAM.
 train_labelled=[]; validation_rows=[]; by=defaultdict(set); meth=Counter()
 def stream_training():
  partitions=iter_resumable_candidates(d['s1'],idx,store,c['batch_size'],c['resources'].get('candidate_method_workers',1))
  total_parts=max(1,(len(d['s1'])+c['batch_size']-1)//c['batch_size'])
  for part_no,(bid,part,pairs) in enumerate(partitions,1):
   for r in pairs: by[r['s1_id']].add(r['candidate_id']); meth.update(r['methods'])
   frows=store.run('features',bid,lambda p=pairs,s=part:feature_rows(p,s,idx.targets),{'pair_count':len(pairs),'schema_hash':schema_manifest()['schema_hash']})
   keys=[(r['s1_id'],r['candidate_id']) for r in frows]
   if len(keys)!=len(set(keys)) or set(keys)!={(r['s1_id'],r['candidate_id']) for r in pairs}: raise ValueError(f'feature/candidate alignment failure in {bid}')
   for r in frows:
    if r['s1_id'] in train_ids: train_labelled.append({**r,'label':int(r['candidate_id'] in d['truth'][r['s1_id']])})
    elif r['s1_id'] in val_ids: validation_rows.append({**r,'label':int(r['candidate_id'] in d['truth'][r['s1_id']])})
   ui.update('Candidate Generation','Running',part_no,total_parts); ui.update('Feature Extraction','Running',part_no,total_parts)
  return {'pairs':sum(map(len,by.values())),'mean_pairs':sum(map(len,by.values()))/max(len(d['s1']),1),'reduction_ratio':1-sum(map(len,by.values()))/max(len(d['s1'])*len(idx.targets),1),'candidate_recall':sum(len(by[k]&v) for k,v in d['truth'].items())/max(sum(map(len,d['truth'].values())),1),'candidate_misses':sum(len(v-by[k]) for k,v in d['truth'].items()),'method_hits':dict(meth)}
 ui.update('Candidate Generation','Running'); ui.update('Feature Extraction','Running')
 report=store.run('training_prep','stream',stream_training,{'train_count':len(train_ids),'validation_count':len(val_ids)})
 ui.update('Candidate Generation','Completed'); ui.update('Feature Extraction','Completed')
 labelled=store.run('training_prep','sample',lambda:label_and_sample(train_labelled,d['truth'],train_ids,c['negative_ratio'],c['seed']))
 tr=labelled; va=validation_rows
 atomic_json(base/'split.json',{'train_ids':sorted(train_ids),'validation_ids':sorted(val_ids),'seed':c['seed']}); atomic_json(base/'candidate_report.json',report)
 model=valid_pickle(base/'best_model.pkl',store.lineage)
 if model is None:
  ui.update('Model Training','Running')
  atomic_json(base/'training_state.json',{'status':'running','latest_resumable':'training_prep/sample','best_model':'best_model.pkl'})
  model,Xv=train_model(tr,va,c['model']); atomic_pickle(base/'latest_model.pkl',model,store.lineage); atomic_pickle(base/'best_model.pkl',model,store.lineage); ui.update('Model Training','Completed')
 else: Xv=feature_matrix(va)
 probs=model.predict_proba(Xv)[:,1]; best=(-1,None,None)
 for t in c['thresholds']:
  pred=defaultdict(set)
  for r,p in zip(va,probs):
   if p>=t:pred[r['s1_id']].add(r['candidate_id'])
  score=macro_f05(pred,{i:d['truth'][i] for i in val_ids})
  if score>best[0]:best=(score,t,pred)
 ui.update('Validation','Completed'); ui.resource_line(); ui.finish()
 atomic_pickle(base/'model.pkl',model,store.lineage)
 manifest={'version':VERSION,'schema':schema_manifest(),'threshold':best[1],'validation_macro_f05':best[0],'candidate_config_hash':stable_hash(candidate_config(c)),'index_hash':h,'config':c,'matrix_storage':{'dtype':'float32','train_rows':len(tr),'validation_rows':len(va),'feature_count':len(FEATURES),'train_bytes':len(tr)*len(FEATURES)*4,'validation_bytes':len(va)*len(FEATURES)*4,'out_of_core':False},'created_at':time.time()}; atomic_json(base/'model_manifest.json',manifest); atomic_json(base/'threshold_sweep.json',{'selected_threshold':best[1],'selected_macro_f05':best[0]}); print(json.dumps(manifest,indent=2))
def run_infer(a):
 c=cfg(a.config); ui=PipelineProgress(a.experiment,a.artifacts); ui.update('Dataset Preparation','Running'); assert_capacity(a.artifacts,c['resources']); base=Path(a.artifacts)/'experiments'/a.experiment; man=json.loads((base/'model_manifest.json').read_text());
 if man['schema']['schema_hash']!=schema_manifest()['schema_hash'] or man['candidate_config_hash']!=stable_hash(candidate_config(c)):raise ValueError('model/config/schema compatibility failure')
 d,idx,h=index_for(a.data,'test',a.artifacts,c,a.sample); ui.update('Dataset Preparation','Completed'); ui.update('Candidate Generation','Running'); ui.update('Feature Extraction','Running'); store=CheckpointStore(Path(a.artifacts)/'runs'/f'inference_{a.experiment}'/'recovery',{'input_hash':stable_hash([x['entity_id'] for x in d['s1']]),'index_hash':h,'candidate_config':candidate_config(c),'schema_hash':schema_manifest()['schema_hash'],'model':file_hash(base/'model.pkl')})
 with (base/'model.pkl').open('rb') as f:model=pickle.load(f)
 out=Path(a.output); stage=out/'staging'; stage.mkdir(parents=True,exist_ok=True)
 mt,ct=stage/'matching_results.tsv.tmp',stage/'candidate_pairs.tsv.tmp'; total=0
 with mt.open('w',encoding='utf8',newline='') as mf,ct.open('w',encoding='utf8',newline='') as cf:
  mw,cw=csv.writer(mf,delimiter='\t',lineterminator='\n'),csv.writer(cf,delimiter='\t',lineterminator='\n');mw.writerow(['source1_entity_id','matched_entity_ids']);cw.writerow(['source1_entity_id','candidate_entity_ids'])
  partitions=iter_resumable_candidates(d['s1'],idx,store,c['batch_size'],c['resources'].get('candidate_method_workers',1))
  for bid,part,pairs,features in iter_resumable_features(partitions,idx.targets,store):
   scored=store.run('scores',bid,lambda r=features:score_partition(r,model),{'pair_count':len(features),'threshold':man['threshold']}); by_s1=defaultdict(list);accepted=defaultdict(list)
   for r in scored:
    by_s1[r['s1_id']].append(r['candidate_id']);total+=1
    if r['probability']>=man['threshold']:accepted[r['s1_id']].append(r['candidate_id'])
   for r in part:
    i=r['entity_id']; cw.writerow([i,','.join(dict.fromkeys(by_s1[i]))]);mw.writerow([i,','.join(dict.fromkeys(accepted[i]))])
   ui.update('Candidate Generation','Running',min(total+1,len(d['s1'])),len(d['s1'])); ui.update('Feature Extraction','Running',min(total+1,len(d['s1'])),len(d['s1']))
 ui.update('Candidate Generation','Completed'); ui.update('Feature Extraction','Completed'); ui.update('Inference','Completed'); ui.update('Output Writing','Running'); validate_outputs_streaming(mt,ct,d['s1'],set(idx.targets)); out.mkdir(parents=True,exist_ok=True); os.replace(mt,out/'matching_results.tsv');os.replace(ct,out/'candidate_pairs.tsv'); atomic_json(Path(a.artifacts)/'runs'/f'inference_{a.experiment}.json',{'status':'complete','pairs':total,'index_hash':h,'model':a.experiment,'outputs':{'matching_sha256':file_hash(out/'matching_results.tsv'),'candidate_sha256':file_hash(out/'candidate_pairs.tsv')}}); ui.update('Output Writing','Completed'); ui.resource_line(); ui.finish(); print('validated outputs:',out)
def preflight(a):
 Path(a.artifacts).mkdir(parents=True,exist_ok=True); c=cfg(a.config); snap=resource_snapshot(a.artifacts); result={'platform':platform.platform(),'python':sys.version,'cpu_count':os.cpu_count(),**snap,'configured_resources':c['resources'],'gpu_note':'GPU remains disabled until a representative benchmark confirms a compatible LightGBM/embedding runtime.'};
 try: assert_capacity(a.artifacts,c['resources']); result['capacity_check']='pass'
 except RuntimeError as e: result['capacity_check']='fail';result['capacity_error']=str(e)
 print(json.dumps(result,indent=2))
def main():
 p=argparse.ArgumentParser();sp=p.add_subparsers(dest='command',required=True); 
 for n in ('train','infer'):
  q=sp.add_parser(n);q.add_argument('--data',required=True);q.add_argument('--artifacts',default='artifacts');q.add_argument('--config',default='config/default.json');q.add_argument('--sample',type=int);q.add_argument('--experiment',default='baseline');q.add_argument('--output',default='output')
 q=sp.add_parser('preflight');q.add_argument('--artifacts',default='artifacts');q.add_argument('--config',default='config/default.json')
 a=p.parse_args(); {'train':run_train,'infer':run_infer,'preflight':preflight}[a.command](a)
if __name__=='__main__':main()
