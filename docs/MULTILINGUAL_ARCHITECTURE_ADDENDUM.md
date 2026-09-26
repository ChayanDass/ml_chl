# Multilingual Entity Matching Architecture Addendum

Status: **Proposed extension, pending benchmark validation**  
Revision: 1  
Scope: final-training architecture only; no retrieval implementation or model retraining in this revision.

## 1. Purpose and unchanged decisions

The dataset audit reports 551,240 Latin-to-non-Latin ground-truth pairs and France in test data. This addendum extends the existing frozen architecture to test those risks without redesigning the system.

The following remain unchanged:

- The six existing candidate-generation families and their union semantics.
- LightGBM as the primary pair classifier.
- Existing feature groups, output schema, and official macro-F0.5 objective.
- Entity-level train/validation separation and test-label isolation.
- Open-valued country handling; no hard country filter or country-specific threshold.
- Raw name/address preservation and the official output contract in `SRS_BASELINE.md`.

No performance improvement is claimed until the extension is benchmarked.

## 2. Proposed script-aware retrieval family

Add a seventh, independently measurable retrieval family, provisionally named `multilingual_name`, alongside the existing six families. It is complementary: existing exact, token, fuzzy, address, country-aware, and embedding retrieval continue to run.

Two candidate implementations must be evaluated as alternatives, not assumed equivalent:

1. A multilingual name representation that compares names across scripts.
2. Transliteration-based retrieval that generates or compares plausible cross-script forms.

The selected approach, if any, must preserve the original name and address fields and store the representation/transliteration version in lineage metadata. It must emit the same candidate record contract as existing methods: S1 ID, target ID/source, method name, method score/evidence, configuration hash, and batch/input lineage.

The union continues to deduplicate on `(s1_id, candidate_id)`, merge all method provenance, and never allow disagreement from one method to veto another. The new family must use deterministic, resumable checkpoints compatible with existing input, preprocessing, index, and configuration fingerprints.

### Resource and candidate-budget rules

The extension must declare per-query limits, index size, representation memory, build time, query time, and fallback behavior. A global cap must not silently discard candidates. Any safety budget must be validation-selected, report pre-limit and post-limit counts plus exclusion reasons, and demonstrate its recall/volume/resource trade-off. If a method cannot operate within the configured resource envelope, it must fail explicitly or use a documented bounded fallback; it must not silently reduce recall.

## 3. Proposed multilingual features

The existing feature schema remains the compatibility baseline. Candidate evidence alone is not a model feature until validated. A schema revision may add only clearly defined, typed, train/inference-identical features such as:

| Proposed feature | Definition requirement | Validation requirement |
|---|---|---|
| `name_script_relation` | Deterministic category for same, mixed, or different scripts, with missing/unknown state | Missingness and subgroup stability; no leakage |
| `name_multilingual_similarity` | Similarity from the selected multilingual representation, with comparable/unavailable state | Calibration, range checks, ablation, and cross-script performance |
| `name_transliteration_similarity` | Similarity between versioned transliteration forms, including failure/multiple-form semantics | Precision impact, collision analysis, and ablation |

These are proposals, not additions to the current 27-feature schema. A feature-schema version, ordered names, types, producer version, preprocessing dependency, and model lineage must change together. Training and inference must fail on incompatible schemas rather than coerce columns.

## 4. Training-data policy

The existing entity-level split, positive labeling, and negative-sampling policy remain in force while evidence is collected. Do not oversample cross-script positives, rebalance classes, or alter negative sampling before subgroup results show a need. Any later sampling experiment must preserve all generated positives, prevent S1 leakage, record its seed/configuration, and compare against the unchanged baseline.

Training diagnostics must report the representation of Latin-to-Latin and Latin-to-non-Latin positives separately for S2 and S3, including each script category with adequate support. Ground-truth pairs missed before candidate generation remain retrieval misses and must not be relabeled as classifier negatives.

## 5. Required validation extension

Every benchmark compares the frozen six-family baseline with the proposed seventh family and, separately, any proposed feature additions. Report:

- Candidate recall before classification, by source pair, script relation, and target script.
- New-family-only discoveries, overlap with each existing family, and matches missed by all methods.
- Recall with both addresses present versus either address missing.
- Candidate count, reduction ratio, pre/post-limit counts, runtime, peak RAM/disk/VRAM, and checkpoint/recovery behavior.
- Same-script versus cross-script classifier precision, recall, F0.5, false negatives, false positives, and threshold effects.
- Official macro-F0.5 and supporting precision/recall diagnostics.

French results remain **unverified** unless a suitable labeled French diagnostic or validation set is available. Unlabeled French test records can be used for preprocessing, candidate-volume, resource, and qualitative diagnostics only; they cannot establish recall or final matching quality.

## 6. France and Unicode requirements

Country remains an open string used as contextual evidence, not a hard filter. No France-specific threshold or rule is allowed in this architecture revision. The same UTF-8 decoding, Unicode normalization, case handling, punctuation handling, and missingness semantics must run in training and inference. Accented French characters and French legal/address terms must be measured as data categories; French-specific suffix parsing or language rules are optional hypotheses requiring benchmark evidence.

## 7. Decision gate

Implementation approval requires a reproducible report showing:

1. Material candidate recall improvement for the target cross-script subgroup without unacceptable candidate explosion.
2. No unacceptable precision/F0.5 regression after classification.
3. Resource use within the workstation envelope and deterministic checkpoint compatibility.
4. Benefit that persists on a held-out entity-level validation slice.
5. No violation of the output contract or SRS baseline.

If these conditions are not met, retain the frozen architecture and record the negative result.

## 8. Change log

| Revision | Change | Status |
|---|---|---|
| 1 | Added proposed script-aware multilingual retrieval family; retained six existing families and union provenance | Pending benchmark |
| 1 | Defined optional script, multilingual-similarity, and transliteration-similarity feature candidates | Pending schema validation/ablation |
| 1 | Added subgroup, method-contribution, resource, and France verification requirements | Required for decision |
| 1 | Explicitly preserved open country handling, LightGBM, output schema, macro-F0.5, and train/validation separation | Frozen |

## 9. Open implementation decisions requiring evidence

- Which multilingual representation, transliteration library/model, or both are permitted by resource and licensing constraints.
- How multiple transliteration forms are generated, ranked, deduplicated, and versioned.
- Per-query limits and any validation-selected budget.
- Whether the proposed features improve the classifier after candidate recall is accounted for.
- Whether address evidence is sufficient to bridge the cross-script gap without a new name representation.
- French diagnostic-label source and its representativeness.
- Workstation index build/query time and peak memory.
