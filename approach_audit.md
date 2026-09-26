# Approach Audit: Business Entity Resolution Challenge

## 1. Executive Summary

This repository implements a six-family, pairwise entity-resolution pipeline. It validates the provided UTF-8 TSV inputs, normalizes fields, builds reusable target indexes, generates and unions candidate pairs from S2 and S3, derives one shared feature schema, trains a LightGBM binary classifier, selects a global threshold on an entity-level validation partition, and writes the two required TSVs.

The implementation is deliberately conservative about claims: local smoke tests and recovery tests have run, but no full-data training, candidate-recall study, workstation ANN benchmark, or final challenge output has been produced. The configured full-scale embedding path is FAISS IVF-PQ; development uses a strictly bounded exact fallback.

## 2. Candidate Generation Architecture

### 2.1 Method 1: Exact/Normalized Names

`norm()` applies Unicode NFKC, case-folding, ampersand-to-`and` replacement, punctuation removal, and whitespace collapse. A compact inverted index maps normalized names to unsigned-32-bit target positions; retrieved positions are converted back to the original S2/S3 IDs.

### 2.2 Method 2: Token-Based Names

Names are normalized then split on whitespace; tokens of length one are excluded. A token inverted index counts overlapping target postings and ranks by overlap count divided by query-token count. The configured top-K is `token_limit=30`; per-token postings are bounded by `max_postings=5000`.

### 2.3 Method 3: N-gram/Fuzzy Names

The implementation indexes normalized character trigrams. It obtains candidates by trigram posting overlap, evaluates the top `4 × fuzzy_limit` candidates with `difflib.SequenceMatcher(..., autojunk=False)`, retains similarities at least `0.35`, and returns the configured top `fuzzy_limit=20`.

### 2.4 Method 4: Address-Based

Addresses use the same Unicode/punctuation/whitespace normalization. Retrieval includes exact normalized-address lookup and token-overlap retrieval, with an `address_limit=30`. There is no address component parser or geographic lookup in the current implementation.

### 2.5 Method 5: Country-Aware

Country is normalized as an open string and used only to prioritize name-token retrieval within same-country postings (`country_limit=15`). It is **not** a hard filter; all other methods run without country agreement, and France/unseen labels are handled as ordinary strings.

### 2.6 Method 6: Embedding-Based

The vectors are deterministic, local 64-dimensional hashed character-trigram vectors, not an external pretrained language model. Both name-only and name-plus-address vectors are represented. The configured full-scale backend is FAISS inner-product IVF-PQ with `nlist=4096`, `nprobe=32`, `pq_m=8`, `pq_nbits=8`, and `embedding_limit=20`; these are starting settings, not validation-selected final values. Small development corpora may use bounded exact cosine; it refuses targets above `bruteforce_max_targets=100000`. No external service, business database, or model download is used by this representation.

### 2.7 Union & Deduplication

Each method writes a deterministic S1-batch checkpoint. The union key is `(s1_id, candidate_id)`; one row retains the candidate source, all method names, and a method-to-score evidence map. Methods cannot veto one another. Candidate IDs are validated against the target index and candidates are never injected from ground truth.

### 2.8 Candidate Evaluation

`candidate_report()` calculates total pairs, mean pairs, reduction ratio, overall generated-positive recall, misses, and method hit counts when training truth is available. No full-data candidate recall or per-method incremental-recall result is claimed yet; this must be measured on the workstation benchmark.

## 3. Feature Engineering

### 3.1 Business-Name Features

`name_exact`, `name_token_jaccard`, `name_char_similarity`, `name_length_ratio`, and `name_comparable`.

### 3.2 Address Features

`address_exact`, `address_token_jaccard`, `address_char_similarity`, and `address_comparable`. No postal/city/street component parser is currently implemented.

### 3.3 Country Features

`country_agree`, `country_disagree`, and `country_missing`. They support arbitrary country strings and distinguish missing from available disagreement.

### 3.4 Cross-Field Features

`cross_name_address_mean` is the mean of name and address character similarity; `cross_both_exact` is the product of normalized exact-name and exact-address indicators.

### 3.5 Blocking Evidence Features

`retrieval_count` plus one hit indicator for each family: `exact_name_hit`, `token_name_hit`, `fuzzy_name_hit`, `address_hit`, `country_hit`, and `embedding_ann_hit`. The current model schema has method indicators, not the continuous per-method retrieval scores retained in candidate provenance.

### 3.6 Data-Quality Features

`source_s2`, `source_s3`, `s1_name_missing`, `candidate_name_missing`, `s1_address_missing`, and `candidate_address_missing` provide source-pair and missingness context.

### 3.7 Feature Count

The shared ordered schema contains **27 float-compatible features**. Candidate IDs, S1 IDs, source, and methods remain lineage fields and are not model features.

## 4. Model Architecture and Training

### 4.1 Model Choice

The implemented primary classifier is `lightgbm.LGBMClassifier` with binary objective. No challenger model or ensemble has been implemented or evaluated.

### 4.2 Training Data

The split is deterministic and S1-entity-level, stratified only by whether an entity has at least one labelled match. `validation_fraction=0.10`. Generated pairs are labelled positive only when their candidate ID occurs in that S1’s ground-truth set. All generated positives are retained. Negatives are deterministically shuffled with the configured seed and capped at `max(positive_count × negative_ratio, 100)`, with `negative_ratio=4`. There is no separate hard-negative mining implementation beyond the generated candidate distribution.

### 4.3 LightGBM Hyperparameters

Current configured values are `n_estimators=300`, `learning_rate=0.05`, `num_leaves=31`, `min_child_samples=20`, and `random_state=20260926`. Max depth, L1/L2 regularization, feature subsampling, early stopping, GPU mode, and class weighting are not configured.

### 4.4 Final Model Retraining

Not yet implemented as a separate all-eligible-data retraining step after threshold selection. Current training fits on the training split, selects the validation threshold, and persists that model. Full-scale final-retraining behavior remains a known implementation item before a final submission model is claimed.

## 5. Threshold Selection

### 5.1 Validation-Based Optimization

The configured sweep is `[0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]`; macro F0.5 is evaluated by S1, including singleton behavior. The smoke run selected `0.30` and reported `1.0`, but that tiny sampled result is not representative and is not a performance claim.

### 5.2 Precision vs Recall

The evaluator uses F0.5, which weights precision more heavily. A global threshold is chosen from validation only; no one-to-one rule, top-one rule, or maximum-match cap is applied.

## 6. Data Leakage Prevention

### 6.1 Train/Validation/Test Separation

Every generated pair for an S1 ID is assigned to its one persisted train or validation partition. Validation labels are not used in the training sample. Test truth is never loaded by the inference path.

### 6.2 Candidate Generation

The same configured normalizer, index, six retrieval families, union rule, and feature schema are used by training and inference. Ground truth labels label only already-generated training pairs; they never insert a candidate.

## 7. System Architecture

### 7.1 Batch Processing

S1 processing is deterministic, currently configured at 5,000 records per candidate/feature/scoring partition. Candidate method, union, feature, and score JSONL partitions are atomically written with checksum manifests. Inference streams one partition through retrieval, feature extraction, scoring, staged TSV writing, and streaming output validation. JSONL is the current persisted representation, not Parquet/HDF5.

### 7.2 Indexes

S2/S3 records are indexed together in a versioned pickle under `artifacts/indexes/<split>/<hash>.pkl`. The manifest binds input fingerprint, normalizer identifier, and retrieval/embedding configuration hash. Compact posting arrays store target positions; target records and lexical dictionaries still reside in RAM.

## 8. Evaluation

### 8.1 Candidate Recall

Candidate recall is implemented as a generated-positive fraction and candidate misses are recorded. No official-scale candidate-recall measurement, source-pair slice, country slice, or incremental method contribution has been run.

### 8.2 F0.5 Metric

`macro_f05()` computes per-S1 F0.5 and averages it, treating correctly predicted/true empty sets as 1.0 and one-empty cases as 0.0. It is used for threshold selection. The only recorded result is the nonrepresentative small smoke result described above.

## 9. Reproducibility

### 9.1 Configuration

`config/default.json` is JSON. It controls seed, partitions, validation fraction, negative ratio, thresholds, retrieval limits, embedding/FAISS settings, LightGBM parameters, workers, and RAM/disk/VRAM guardrails.

### 9.2 Random Seeds

The configured seed is `20260926`. It controls stratified split shuffling and negative shuffle. LightGBM receives `random_state=20260926`.

### 9.3 Artifacts Saved

The pipeline persists validation fingerprints; normalized partitions; target indexes; method candidates, unions, features, scores; split/sample checkpoints; candidate report; model checkpoints; model/threshold manifests; and inference output hashes. Checkpoints have status, row count, checksum, lineage hash, and atomic commit behavior.

### 9.4 Environment

The development run used Python 3.12.3. `requirements.txt` pins LightGBM 4.5.0, NumPy 1.26.4, scikit-learn 1.4.1.post1, and declares FAISS CPU support. The exact workstation FAISS/GPU build remains to be validated.

## 10. Submission Package

### 10.1 Output Files

Inference produces `matching_results.tsv` and `candidate_pairs.tsv`. Streaming validation checks headers, original S1 order, coverage, target-source membership, uniqueness, empty fields, and match-subset-of-candidate. The official validator was run only against a deliberately partial smoke output; it correctly rejected it for missing full-test rows, so no final output is claimed.

### 10.2 Code Package

The repository has `src/`, `README.md`, requirements, configuration, and documentation. The exact required `code/business_entity_resolution/` submission-archive layout has not been assembled or verified.

## 11. External Compliance

### 11.1 No External APIs

Confirmed: no geocoding, business lookup, external database, or external identity-resolution service is called. The embedding representation is generated locally from provided text.

## 12. Known Challenges

### 12.1 How You Handle

Noisy names/addresses are covered by normalization, token overlap, trigrams/fuzzy similarity, address retrieval, and learned pairwise features. Missing fields have explicit indicators and are not treated as disagreement. Generic/shared-name and shared-address ambiguity are left for LightGBM evidence rather than hard blocking rejection. France is handled as an open country string; it is not hard-coded or filtered.

## 13. Clarifications

### 13.1 Questions During Implementation

The implementation resolved country as contextual rather than mandatory equality, candidate generation as label-independent, multi-match output as unrestricted by one-to-one constraints, and full-scale embeddings as ANN rather than exhaustive cosine. Workstation-specific FAISS/GPU choices, ANN recall tuning, resource envelope, final retraining, and final model settings remain evidence-dependent rather than assumed.

## 14. Timeline

### 14.1 Development Phases

Implementation proceeded through foundation/input validation; normalization/indexing; six retrieval families; shared features; split/labelling/sampling; LightGBM/thresholding; inference/output validation; checkpoints/recovery; compact lexical postings; FAISS IVF-PQ integration; and partitioned inference. Calendar time per phase was not tracked. Full-scale benchmarking, final parameter selection, final retraining, output generation, and submission-package assembly remain pending workstation execution.
