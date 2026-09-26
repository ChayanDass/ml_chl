import csv, json, tempfile, unittest
from pathlib import Path
from src.core import *
from src.operations.checkpoint import CheckpointStore, atomic_pickle, valid_pickle

class PipelineTest(unittest.TestCase):
 def test_retrieval_features_and_output_contract(self):
  s1=[{'entity_id':'S1-1','business_name':'Acme, Inc.','business_address':'1 Main St','country':'US','source':'S1','ordinal':0,'name_n':norm('Acme, Inc.'),'address_n':norm('1 Main St'),'country_n':'us'}, {'entity_id':'S1-2','business_name':'Unique Cafe','business_address':'2 Rue A','country':'France','source':'S1','ordinal':1,'name_n':norm('Unique Cafe'),'address_n':norm('2 Rue A'),'country_n':'france'}]
  target=[]
  for i,n,a,c,src in [('S2-1','ACME INC','1 Main Street','US','S2'),('S3-1','Acme Incorporated','Main St 1','US','S3'),('S2-2','Other','Elsewhere','India','S2')]: target.append({'entity_id':i,'business_name':n,'business_address':a,'country':c,'source':src,'ordinal':0,'name_n':norm(n),'address_n':norm(a),'country_n':norm(c)})
  conf={'retrieval':{'token_limit':30,'fuzzy_limit':20,'address_limit':30,'country_limit':15,'embedding_limit':20,'max_postings':5000}}
  rows=candidates(s1,Index(target,conf)); self.assertEqual(len({(x['s1_id'],x['candidate_id']) for x in rows}),len(rows)); self.assertTrue(any('exact_name' in x['methods'] for x in rows)); self.assertIn('S2-1',{x['candidate_id'] for x in rows if x['s1_id']=='S1-1'})
  feats=feature_rows(rows,s1,{x['entity_id']:x for x in target}); self.assertEqual(len(rows),len(feats)); self.assertEqual(set(FEATURES),set(feats[0]) & set(FEATURES))
  with tempfile.TemporaryDirectory() as d:
   d=Path(d); m=d/'matching_results.tsv'; c=d/'candidate_pairs.tsv'
   for p,col,vals in [(m,'matched_entity_ids',{'S1-1':'S2-1','S1-2':''}),(c,'candidate_entity_ids',{'S1-1':'S2-1,S3-1','S1-2':''})]:
    with p.open('w',newline='') as f:
     w=csv.writer(f,delimiter='\t');w.writerow(['source1_entity_id',col]);[w.writerow([x['entity_id'],vals[x['entity_id']]]) for x in s1]
   self.assertTrue(validate_outputs(m,c,s1,{x['entity_id'] for x in target}))
 def test_split_and_metric(self):
  truth={'S1-1':{'S2-1'},'S1-2':set(),'S1-3':{'S3-1'},'S1-4':set()}; tr,va=split_ids(list(truth),truth,.5,2);self.assertFalse(tr&va);self.assertEqual(tr|va,set(truth));self.assertEqual(macro_f05({'S1-1':{'S2-1'}},{'S1-1':{'S2-1'}}),1.)
 def test_method_query_matches_combined_query(self):
  target=[{'entity_id':'S2-1','business_name':'Acme Inc','business_address':'One Road','country':'US','source':'S2','ordinal':0,'name_n':'acme inc','address_n':'one road','country_n':'us'}]
  s={'entity_id':'S1-1','business_name':'Acme Inc','business_address':'One Road','country':'US','source':'S1','ordinal':0,'name_n':'acme inc','address_n':'one road','country_n':'us'}
  conf={'retrieval':{'token_limit':3,'fuzzy_limit':3,'address_limit':3,'country_limit':3,'embedding_limit':3,'max_postings':20}}; ix=Index(target,conf); combined=ix.query(s)
  self.assertEqual({m:ix.query_method(s,m) for m in METHODS},combined)

 def test_multilingual_method_is_explicitly_disabled_without_backend(self):
  target=[{'entity_id':'S2-1','business_name':'राम बाजार','business_address':'Road','country':'India','source':'S2','ordinal':0,'name_n':norm('राम बाजार'),'address_n':'road','country_n':'india'}]
  s={'entity_id':'S1-1','business_name':'Ram Bazaar','business_address':'Road','country':'India','source':'S1','ordinal':0,'name_n':norm('Ram Bazaar'),'address_n':'road','country_n':'india'}
  conf={'retrieval':{'token_limit':3,'fuzzy_limit':3,'address_limit':3,'country_limit':3,'embedding_limit':3,'max_postings':20},'multilingual':{'enabled':False}}
  ix=Index(target,conf); self.assertEqual(ix.query_method(s,'multilingual_name'),{}); self.assertIn('multilingual_name',METHODS)
 def test_persisted_bounded_embedding_index_reloads(self):
  target=[{'entity_id':'S2-1','business_name':'Acme','business_address':'Road','country':'US','source':'S2','ordinal':0,'name_n':'acme','address_n':'road','country_n':'us'}]
  conf={'retrieval':{'token_limit':3,'fuzzy_limit':3,'address_limit':3,'country_limit':3,'embedding_limit':3,'max_postings':20},'embedding':{'backend':'bruteforce','bruteforce_max_targets':10}}
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'index.pkl'; ix=Index(target,conf); ix.save(p,{'input_hash':'a','preprocess_hash':'b','config_hash':'c'})
   loaded=Index.load(p,{'input_hash':'a','preprocess_hash':'b','config_hash':'c'}); self.assertEqual(loaded.ann_ids,['S2-1'])
 def test_compact_postings_and_union_provenance(self):
  target=[{'entity_id':'S2-1','business_name':'Acme Acme','business_address':'Road','country':'US','source':'S2','ordinal':0,'name_n':'acme acme','address_n':'road','country_n':'us'}]
  conf={'retrieval':{'token_limit':3,'fuzzy_limit':3,'address_limit':3,'country_limit':3,'embedding_limit':3,'max_postings':20},'embedding':{'backend':'bruteforce','bruteforce_max_targets':10}}
  ix=Index(target,conf); stats=ix.memory_stats(); self.assertGreater(stats['posting_references'],0); self.assertEqual(stats['posting_payload_bytes']%4,0)
  merged=union_candidate_method_rows([{'s1_id':'S1-1','candidate_id':'S2-1','candidate_source':'S2','method':'token_name','score':.5},{'s1_id':'S1-1','candidate_id':'S2-1','candidate_source':'S2','method':'address','score':1.}])
  self.assertEqual(len(merged),1); self.assertEqual(set(merged[0]['methods']),{'token_name','address'});self.assertEqual(merged[0]['evidence']['address'],1.)
 def test_invalid_ann_configuration_fails_before_index_build(self):
  target=[]; conf={'retrieval':{'token_limit':3,'fuzzy_limit':3,'address_limit':3,'country_limit':3,'embedding_limit':3,'max_postings':20},'embedding':{'backend':'bruteforce','dimensions':63,'pq_m':8}}
  with self.assertRaises(ValueError): Index(target,conf)
 def test_streaming_output_validation_and_partition_equivalence(self):
  s1=[{'entity_id':'S1-1'},{'entity_id':'S1-2'}]
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);m=d/'m.tsv';c=d/'c.tsv'
   m.write_text('source1_entity_id\tmatched_entity_ids\nS1-1\tS2-1\nS1-2\t\n');c.write_text('source1_entity_id\tcandidate_entity_ids\nS1-1\tS2-1,S3-1\nS1-2\t\n')
   self.assertTrue(validate_outputs_streaming(m,c,s1,{'S2-1','S3-1'}))
 def test_feature_matrix_is_compact_float32(self):
  rows=[{**{f:1.0 for f in FEATURES},'label':1},{**{f:0.0 for f in FEATURES},'label':0}]
  x=feature_matrix(rows);self.assertEqual(str(x.dtype),'float32');self.assertEqual(x.nbytes,2*len(FEATURES)*4)
 def test_cached_retrieval_is_equivalent_to_uncached_records(self):
  target=[]
  for i in range(3):
   r={'entity_id':f'S2-{i}','business_name':f'Acme Store {i}','business_address':f'{i} Main Road','country':'US','source':'S2','ordinal':i,'name_n':norm(f'Acme Store {i}'),'address_n':norm(f'{i} Main Road'),'country_n':'us'};target.append(enrich_record(r))
  conf={'retrieval':{'token_limit':3,'fuzzy_limit':3,'address_limit':3,'country_limit':3,'embedding_limit':3,'max_postings':20},'embedding':{'backend':'bruteforce','bruteforce_max_targets':10}}
  raw={'entity_id':'S1-1','business_name':'Acme Store 1','business_address':'1 Main Road','country':'US','source':'S1','ordinal':0,'name_n':'acme store 1','address_n':'1 main road','country_n':'us'}
  self.assertEqual(Index(target,conf).query(raw),Index(target,conf).query(enrich_record(dict(raw))))
 def test_threaded_candidate_methods_preserve_union(self):
  s1=[enrich_record({'entity_id':'S1-1','business_name':'Acme','business_address':'One Road','country':'US','source':'S1','ordinal':0,'name_n':'acme','address_n':'one road','country_n':'us'})]
  t=[enrich_record({'entity_id':'S2-1','business_name':'Acme','business_address':'One Road','country':'US','source':'S2','ordinal':0,'name_n':'acme','address_n':'one road','country_n':'us'})]
  conf={'retrieval':{'token_limit':3,'fuzzy_limit':3,'address_limit':3,'country_limit':3,'embedding_limit':3,'max_postings':20},'embedding':{'backend':'bruteforce','bruteforce_max_targets':10}}
  with tempfile.TemporaryDirectory() as d:
   a=resumable_candidates(s1,Index(t,conf),CheckpointStore(Path(d)/'a',{'x':1}),1,1);b=resumable_candidates(s1,Index(t,conf),CheckpointStore(Path(d)/'b',{'x':1}),1,2)
   self.assertEqual(a,b)
 def test_checkpoint_skip_partial_failure_and_corruption(self):
  with tempfile.TemporaryDirectory() as d:
   store=CheckpointStore(d,{'input':'a','config':'v1'}); calls=[]
   def make(unit):
    def f(): calls.append(unit); return [{'unit':unit}]
    return f
   store.run('candidate_methods','batch0.exact_name',make('exact'))
   # Simulated crash: the second method is absent. Restart reuses exact and runs only token.
   self.assertEqual(store.run('candidate_methods','batch0.exact_name',make('exact')), [{'unit':'exact'}])
   store.run('candidate_methods','batch0.token_name',make('token'))
   self.assertEqual(calls,['exact','token'])
   payload=Path(d)/'candidate_methods'/'batch0.token_name.jsonl'; payload.write_text('corrupt\n')
   store.run('candidate_methods','batch0.token_name',make('token-rebuilt'))
   self.assertEqual(calls,['exact','token','token-rebuilt'])
 def test_resumable_candidate_and_feature_partitions(self):
  s1=[]
  for n in range(3): s1.append({'entity_id':f'S1-{n}','business_name':'Acme','business_address':str(n),'country':'US','source':'S1','ordinal':n,'name_n':'acme','address_n':str(n),'country_n':'us'})
  target=[{'entity_id':'S2-1','business_name':'Acme','business_address':'0','country':'US','source':'S2','ordinal':0,'name_n':'acme','address_n':'0','country_n':'us'}]
  conf={'retrieval':{'token_limit':3,'fuzzy_limit':3,'address_limit':3,'country_limit':3,'embedding_limit':3,'max_postings':20}}
  with tempfile.TemporaryDirectory() as d:
   store=CheckpointStore(d,{'input':'x','config':'x'}); rows=resumable_candidates(s1,Index(target,conf),store,2); feats=resumable_features(rows,s1,{'S2-1':target[0]},store,2)
   again=resumable_features(resumable_candidates(s1,Index(target,conf),store,2),s1,{'S2-1':target[0]},store,2)
   self.assertEqual({(x['s1_id'],x['candidate_id']) for x in feats},{(x['s1_id'],x['candidate_id']) for x in again})
 def test_incompatible_and_interrupted_artifacts_are_not_reused(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); first=CheckpointStore(root,{'input':'one','schema':'v1'}); first.run('features','batch0',lambda:[{'x':1}])
   calls=[]; second=CheckpointStore(root,{'input':'two','schema':'v1'}); second.run('features','batch0',lambda:(calls.append(1) or [{'x':2}]))
   self.assertEqual(calls,[1]); self.assertTrue(list((root/'features').glob('*.corrupt-*')))
   # An interrupted temporary write lacks a completion manifest and cannot be reused.
   (root/'features'/'batch1.jsonl.tmp').write_text('{"x": 9}\n'); second.run('features','batch1',lambda:[{'x':3}])
   self.assertEqual(second.load('features','batch1'),[{'x':3}])
 def test_latest_and_best_models_are_separate_and_lineage_bound(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d); latest=d/'latest_model.pkl'; best=d/'best_model.pkl'; lineage={'experiment':'a','model':'v1'}
   atomic_pickle(latest,{'iteration':10},lineage); atomic_pickle(best,{'iteration':7},lineage)
   self.assertEqual(valid_pickle(latest,lineage),{'iteration':10}); self.assertEqual(valid_pickle(best,lineage),{'iteration':7})
   self.assertIsNone(valid_pickle(best,{'experiment':'a','model':'v2'}))
if __name__=='__main__':unittest.main()
