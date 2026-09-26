from pathlib import Path
def check(root):
 required=['output/matching_results.tsv','output/candidate_pairs.tsv','src','README.md','requirements.txt']
 missing=[x for x in required if not (Path(root)/x).exists()]
 if missing: raise ValueError('missing submission paths: '+', '.join(missing))
 return True
