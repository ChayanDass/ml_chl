# Second Audit: Multilingual Matching and France

## Executive summary

This audit confirms the data risks, but does not find a measured full-scale pipeline failure because the repository contains no full-scale candidate/feature/scoring trace. The available end-to-end artifacts are 50-row smoke/recovery runs. Their `candidate_report.json` has 1,444 generated pairs and a `candidate_raecall` value of `0.0`; this is not a valid full-dataset recall result because the artifact has no positive-count/ground-truth evaluation attached and is explicitly a smoke-sized run.

The frozen pipeline is structurally capable of trying to recover cross-script matches through address retrieval and hashed character-trigram embeddings. Exact, token, and ordinary character-fuzzy name methods cannot bridge fully different scripts when there is no shared text. France is not hard-coded as an allowed-country requirement: country is an open string and is used for prioritization, so unseen `France` labels are not automatically rejected. However, no labeled French validation set exists, so French recall, precision, and classifier generalization remain unmeasured.

**Conclusion:** do not change the frozen design based on the current evidence alone. A design change becomes justified only if a full labeled candidate trace shows material recall loss for Latin-to-non-Latin pairs or French records.

## Dataset and scope

The preceding dataset audit reports 7,638,365 training ground-truth pairs, including 551,240 Latin-to-non-Latin pairs (7.22%). It reports training countries `US` and `India`, and test-only `France`: 259,452 S1, 703,378 S2, and 731,615 S3 records. It also reports nonempty S2/S3 addresses as overwhelmingly Latin-script. These figures are taken from `docs/dataset_audit.md` and `reports/dataset_analysis/DATASET_ANALYSIS_SUMMARY.md`.

The repository's validation manifests point to 50 rows per source, not the full files. The available recovery artifact contains 1,444 candidate rows. No full-scale ground-truth candidate trace, per-script candidate trace, timing trace, memory trace, or French labels were found.

## Cross-script candidate recall

| Group | GT pairs | Candidates | Missed | Recall |
|---|---:|---:|---:|---:|
| Latin-to-non-Latin overall | 551,240 reported in prior audit | Not measured | Not measurable | Not measurable |
| S2 / S3 split | Not present in pipeline artifacts | Not measured | Not measurable | Not measurable |
| Devanagari, Tamil, Telugu, Kannada, Gujarati, Bengali, Malayalam, Odia, Gurmukhi | Counts exist in prior data audit | Not measured | Not measurable | Not measurable |

The pipeline's normalizer and lexical methods operate on normalized text and character trigrams. Therefore exact-name, token-name, and ordinary character-fuzzy retrieval have no lexical bridge for a fully transliterated pair with zero shared characters. This is a code-path conclusion, not a measured recall percentage. Address and embedding methods may still retrieve such pairs.

## Retrieval-method contribution

The configured limits are token 30, fuzzy 20, address 30, country 15, embedding 20, and maximum postings 5,000 (`config/default.json`). The candidate schema retains method-hit indicators for `exact_name`, `token_name`, `fuzzy_name`, `address`, `country`, and `embedding_ann` (`artifacts/experiments/recovery-verify/model_manifest.json`).

The only available smoke artifact reports method hit totals of address 21, country 333, embedding 1,000, fuzzy 531, and token 357 over 1,444 candidate rows. It does not provide ground-truth intersections or incremental-only hits, and exact-name is absent from that summary. Consequently method recall contribution, overlap, and all-method misses are not measurable from current artifacts.

## Address-based recovery

Prior data analysis reports that most nonempty S2/S3 addresses are Latin-script, making address retrieval a plausible bridge for name-script mismatch. The implementation has exact normalized-address and token-overlap address retrieval, with limit 30, and address features include exactness, token Jaccard, character similarity, and comparability.

The requested slices are not available: cross-script recall with both addresses, either address missing, address-only recall, address-only recovery, unretrieved-with-both-addresses, and S1-S2/S1-S3 breakdowns all require joining full ground truth to per-method candidate output. No such output is present. The claim that address recovery works is therefore a hypothesis supported by data shape, not an observed result.

## France generalization

The prior inventory reports France only in test: 259,452 S1, 703,378 S2, and 731,615 S3 records. It reports Latin-script French data with accented characters and terms/legal suffixes such as `SARL`, `SAS`, `EURL`, and `Société`. No French ground truth is available, so true candidate recall and final matching quality on France cannot be measured.

The frozen design treats country as an open string and uses country-aware retrieval to prioritize same-country postings; it is not a hard candidate filter. Other retrieval families run without country agreement. This means there is no inspected rule that assumes only US and India or categorically rejects France. Accent handling is through the shared Unicode normalization path; French-specific suffix parsing is not implemented.

## Classifier audit

The model has 27 features, including name/address similarities, country agreement, missingness, retrieval count, and one hit indicator per retrieval family. The stored model manifest reports threshold `0.30` and validation macro-F0.5 `1.0`, but this is from the 50-row smoke/recovery validation artifact and is not representative. No subgroup labels or candidate-level predictions are stored for Latin-to-Latin versus Latin-to-non-Latin, S2 versus S3, or individual scripts.

Thus classifier false negatives/positives and F0.5 by subgroup are not measurable. The correct attribution rule remains: pairs absent from candidate output are retrieval failures, not classifier rejections; current artifacts do not permit applying that rule at full scale.

## End-to-end performance

No trustworthy runtime or memory benchmark is present. The configuration requests CPU execution, 20 workers, 96 GiB soft RAM, 112 GiB hard RAM, and FAISS IVF-PQ with 64 dimensions, `nlist=4096`, `nprobe=32`, `pq_m=8`, and `pq_nbits=8`; GPU is disabled. The model manifest notes that selected training matrices materialize in RAM. Full-scale candidate time, feature time, scoring time, candidate counts, memory peak, and resource bottlenecks remain unmeasured.

## Findings against the frozen design

| Finding | Evidence | Stage | Impact | Possible improvement | Risk | Additional validation |
|---|---|---|---|---|---|---|
| Full cross-script recall is unknown | No full candidate trace; 551,240 pairs reported in prior audit | Candidate generation | Potentially high | Multilingual/transliteration retrieval | Candidate explosion and false positives | Full labeled per-method trace by script and source |
| Lexical name methods cannot bridge fully different scripts | Normalized token/trigram methods require shared normalized text | Candidate generation/features | Confirmed mechanism; impact unmeasured | Transliteration or multilingual representation | Incorrect transliteration collisions | Controlled recall/precision comparison |
| Address may bridge script gap | Latin-heavy nonempty addresses in prior audit; address retrieval exists | Candidate generation | Potentially positive, unmeasured | Address component/geographic retrieval | Shared addresses create false positives | Both-address/missing-address slices |
| France is unseen in training | Prior country inventory; no French labels | Preprocessing/retrieval/model | Generalization risk | Multilingual normalization/training coverage | Overfitting to France-specific rules | Labeled French diagnostic set |
| Smoke F0.5 is not evidence of generalization | 50-row validation, F0.5 1.0 | Classifier | Cannot support release claim | Better stratified validation | Threshold overfitting | Full entity-level validation by script/country |

## Recommended next experiments

1. Run candidate generation on a bounded, reproducible full-data sample with ground truth, preserving per-method candidate IDs and timings.
2. Compute the requested script, source-pair, address-availability, and method-only recall intersections before changing code.
3. Add a held-out diagnostic slice containing Latin-to-non-Latin matches and French records; keep it separate from training.
4. Score the existing model on that slice and report retrieval failures separately from classifier failures.
5. Benchmark FAISS IVF-PQ recall and resource use before extrapolating workstation behavior.

## Final conclusion

The multilingual and France findings are credible dataset risks, and the current name-only lexical methods have a confirmed representational limitation for fully different scripts. The existing design includes two plausible recovery paths, address retrieval and embeddings, and does not hard-reject France. Because the required full-scale measurements are absent, a design change is **not yet justified**. The next decision should be based on the targeted labeled trace described above.

### References

- [Frozen design](../design_freeze.md)
- [Dataset audit](../dataset_audit.md)
- [Pipeline approach audit](../../approach_audit.md)
- [Configuration](../../config/default.json)
- [Stored model manifest](../../artifacts/experiments/recovery-verify/model_manifest.json)
