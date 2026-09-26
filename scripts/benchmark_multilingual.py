#!/usr/bin/env python3
"""Bounded labeled comparison for six-family vs multilingual retrieval."""
import csv, json, random, resource, time, unicodedata
from pathlib import Path
from src.core import Index, enrich_record, norm

def script(text):
    for ch in text:
        if not ch.isalpha(): continue
        name = unicodedata.name(ch, "")
        for key in ("DEVANAGARI", "TAMIL", "TELUGU", "KANNADA", "GUJARATI", "BENGALI", "MALAYALAM", "ORIYA", "GURMUKHI"):
            if key in name: return key.title()
        return "Latin"
    return "None"

def load_sample(root, n=300, target_cap=2500):
    s1=[]
    with (root / "train_source1.tsv").open(encoding="utf8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if len(s1) >= n: break
            r.update(source="S1", ordinal=len(s1), name_n=norm(r["business_name"]), address_n=norm(r["business_address"]), country_n=norm(r["country"]))
            s1.append(enrich_record(r))
    ids={r["entity_id"] for r in s1}; truth={}
    with (root / "train_ground_truth.tsv").open(encoding="utf8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["source1_entity_id"] in ids: truth[r["source1_entity_id"]]={x for x in (r["matched_entity_ids"] or "").split(",") if x}
    needed=set().union(*truth.values()); targets=[]; random.seed(20260926)
    for fn, source in (("train_source2.tsv", "S2"), ("train_source3.tsv", "S3")):
        with (root / fn).open(encoding="utf8", newline="") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if r["entity_id"] in needed or (len(targets) < target_cap and random.random() < .001):
                    r.update(source=source, ordinal=len(targets), name_n=norm(r["business_name"]), address_n=norm(r["business_address"]), country_n=norm(r["country"]))
                    targets.append(enrich_record(r))
    return s1, targets, truth

def run(s1, targets, truth, multilingual, index_type='exact', **ann):
    cfg={"retrieval":{"token_limit":30,"fuzzy_limit":20,"address_limit":30,"country_limit":15,"embedding_limit":20,"max_postings":5000},"embedding":{"backend":"bruteforce","bruteforce_max_targets":100000},"multilingual":{"enabled":multilingual,"model":"intfloat/multilingual-e5-small","device":"cpu","batch_size":64,"limit":20,"min_similarity":0.0,"index_type":index_type,**ann}}
    t=time.perf_counter(); index=Index(targets,cfg); build=time.perf_counter()-t
    t=time.perf_counter(); by_method={}; pairs=set()
    for q in s1:
        for method,hits in index.query(q).items():
            by_method.setdefault(method,set()).update((q["entity_id"], candidate) for candidate in hits)
            pairs.update((q["entity_id"], candidate) for candidate in hits)
    query=time.perf_counter()-t; gt={(a,b) for a,bs in truth.items() for b in bs}; present=gt & pairs
    existing=set().union(*(v for k,v in by_method.items() if k != "multilingual_name")); multi=by_method.get("multilingual_name",set())
    cross={p for p in gt if script(next(q for q in s1 if q["entity_id"]==p[0])["business_name"]) != script(next(x for x in targets if x["entity_id"]==p[1])["business_name"])}
    def recall(group): return len(present & group)/max(len(group),1)
    return {"enabled":multilingual,"index_type":index_type,"index_build_s":round(build,3),"query_s":round(query,3),"candidate_pairs":len(pairs),"candidate_pairs_per_s1":round(len(pairs)/len(s1),2),"gt_pairs":len(gt),"candidate_found":len(present),"candidate_recall":round(recall(gt),4),"cross_script_gt":len(cross),"cross_script_found":len(present&cross),"cross_script_recall":round(recall(cross),4),"same_script_recall":round(recall(gt-cross),4),"s2_recall":round(recall({p for p in gt if next(x for x in targets if x["entity_id"]==p[1])["source"]=="S2"}),4),"s3_recall":round(recall({p for p in gt if next(x for x in targets if x["entity_id"]==p[1])["source"]=="S3"}),4),"multilingual_truth_hits":len(multi&gt),"multilingual_incremental_truth_hits":len((multi-existing)&gt),"multilingual_candidate_overlap_with_existing":len(multi&existing),"rss_mb":round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,1)}

if __name__ == "__main__":
    root=Path("6ab10eb3b23ba_student_resource/student_resource/dataset/train"); s1,targets,truth=load_sample(root)
    out={"sample_s1":len(s1),"target_rows":len(targets),"ground_truth_pairs":sum(map(len,truth.values())),"baseline":run(s1,targets,truth,False),"exact":run(s1,targets,truth,True,'exact'),"flat":run(s1,targets,truth,True,'flat'),"hnsw_ef32":run(s1,targets,truth,True,'hnsw',ef_search=32),"hnsw_ef64":run(s1,targets,truth,True,'hnsw',ef_search=64),"ivf_nprobe8":run(s1,targets,truth,True,'ivfflat',nlist=64,nprobe=8)}
    print(json.dumps(out,indent=2))
