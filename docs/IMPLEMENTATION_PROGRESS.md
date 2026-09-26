# Implementation Progress

Status: implementation complete; full-scale training/inference intentionally not run on this laptop.

Implemented: UTF-8 TSV validation/fingerprints; NFKC normalization; versioned persisted target indexes; exact-name, token-name, fuzzy char n-gram, address, country-context, and deterministic hashed-vector ANN retrieval; union/provenance; six feature groups in a schema-bound matrix; entity-level stratified split, generated-pair-only labels and deterministic negative sampling; LightGBM training; macro F0.5 threshold selection; manifest compatibility checks; atomic output validation; checkpoint-compatible index/partition manifests; and resource preflight.

Laptop smoke commands and primary-workstation commands are in `README.md`. Full scale needs sufficient free workspace for indexes/partitions, LightGBM installed, and GPU validation with `nvidia-smi` before any GPU option is selected. No full-scale result is claimed.

## Recovery update

Every normalized dataset, retrieval method × deterministic S1 batch, candidate-union batch, feature batch, training split/sample, inference score payload, model binary, and final output is now protected by an atomic payload-plus-manifest checkpoint. A payload is reused only when its checksum, row count, schema/config/input lineage, and completion state agree; incomplete, corrupt, or stale artifacts are quarantined and only that unit is rebuilt. Re-run the same `train` or `infer` command to resume. The model boundary persists `latest_model.pkl` and `best_model.pkl` separately after a completed fit; iterative LightGBM boosting is not currently resumed mid-fit, so an interruption during that single model-fit unit restarts only model fitting after all prepared partitions are reused.

Recovery verification (2026-09-26): six focused tests passed. They cover method-level partial candidate recovery, union/feature partition reuse and alignment, corrupted payload rebuild, incompatible lineage rejection, interrupted temporary-write rejection, and distinct lineage-bound latest/best model artifacts. A 50-record train/inference smoke run and repeat-resume run completed, with the inference completion manifest recording SHA-256 checksums for both staged-and-promoted output TSVs. A defect allowing a model checkpoint without training-lineage validation was fixed before this verification.

## Resource-safety update

Added portable RAM/disk preflight checks and configurable workstation guardrails. Candidate recovery now executes only its requested retrieval family rather than recomputing all six families for each method checkpoint. A 500-target synthetic benchmark measured 0.181 s for ten direct six-family retrieval passes versus 1.1702 s for the prior redundant pattern (6.47× faster); it is a microbenchmark, not a full-scale estimate. The current development host has no usable NVIDIA driver, so GPU claims are deliberately deferred. The local hashed-vector retrieval remains exhaustive CPU cosine over its target vectors and the index remains memory-resident; these are full-scale risks requiring a workstation benchmark and likely a validated ANN/index storage decision before a production-scale run.

## Workstation ANN update

Implemented the configured FAISS IVF-PQ full-scale embedding path with persisted index serialization, separate name and name-plus-address ANN retrieval, bounded development-only exact fallback, and embedding configuration included in index/model/checkpoint compatibility hashes. The fallback rejects over-limit target sets rather than silently doing exhaustive full-scale search. Eight focused tests passed, including persisted index reload and ANN-backend safe-failure behavior when FAISS is unavailable. FAISS build/GPU compatibility, ANN candidate recall, index RSS/disk size, and final nlist/nprobe/PQ settings remain workstation-only validation decisions; see `docs/WORKSTATION_EXECUTION.md`.

## Lexical-index hardening update

Lexical postings now store compact unsigned 32-bit target positions instead of repeated Python entity-ID strings; target IDs are converted back only at retrieval boundaries, preserving candidate IDs/provenance. ANN configuration is validated before index construction (backend, fixed vector dimension, and PQ divisibility), and compact-posting statistics are exposed by the index. On a bounded 2,000-target synthetic index, measured posting payload was 275,516 bytes for 68,879 posting references, index construction took 1.446 seconds, and peak traced Python allocations were 5.47 MiB. This is not a full-scale extrapolation. Ten focused unit tests passed. The target-record dictionary and lexical key dictionaries remain memory-resident, and pipeline orchestration still aggregates stage rows in memory; a true disk-backed target-record/partitioned aggregation implementation remains a workstation-scale engineering risk rather than a solved claim.

## Disk-backed intermediate update

Inference now streams deterministic candidate-union partitions through feature extraction, checkpointed scoring, staged TSV writing, and streaming validation. It no longer concatenates candidate rows, feature rows, scores, or output maps across the corpus. Candidate methods, union, features, and scores retain their independent atomic manifests and are loaded one partition at a time. Eleven focused tests passed, including streaming output order/subset/empty-list validation. Training is not out-of-core: LightGBM's sklearn interface and current label/sampling path still materialize the selected training/validation matrix; this remains an explicit workstation-memory limitation. A 30-record CLI smoke was intentionally refused because the development host had only 0.87 GiB free RAM, confirming the guard fails safely rather than swapping or weakening limits.

## Final matrix-memory hardening

LightGBM input conversion now creates one float32 NumPy matrix rather than a duplicate Python list-of-lists. Matrix row count, feature count, byte size, dtype, and the explicit `out_of_core: false` limitation are written into the model manifest. A 10,000-row/27-feature bounded check measured 1.03 MiB for the float32 matrix; twelve focused tests passed. This eliminates a high-overhead transient copy but does not make model fitting out-of-core: selected feature rows, labels, split/truth maps, target records, and LightGBM's internal Dataset still require workstation RAM. Native LightGBM binary Dataset support was not adopted because it does not provide verified streaming training from multiple persisted feature partitions in this implementation; claiming otherwise would be misleading.

## Retrieval CPU optimization

Normalization now caches label-independent name/address tokens, name trigrams, and name/name-plus-address vectors once per loaded record. Index construction and all six method queries reuse these cached values. An equivalence test confirms cached and uncached records return identical candidates/scores. On a 1,000-target bounded synthetic test, 20 complete retrieval calls took 0.5878 seconds uncached and 0.5571 seconds cached (5.2% faster). This is a small CPU microbenchmark, not an end-to-end or workstation estimate. No measured basis exists yet to claim the 4–5-hour full-run target or even the 8-hour limit is achievable.

## Partition threading and feature-cache update

Candidate method checkpoints can now use bounded shared-index threads via `resources.candidate_method_workers`; it defaults to 1 because Python process workers would duplicate the workstation-scale index and the lexical/fuzzy loops are largely GIL-bound. Threaded and sequential unions were tested for exact equality. Feature extraction now reuses the same cached tokens and normalized strings rather than re-tokenizing/re-normalizing per pair. A 500-target/200-S1 synthetic feature benchmark measured 1.5155 seconds without record caches and 1.2045 seconds with caches (20.5% faster), with identical feature semantics by construction and regression tests. This is bounded CPU evidence only; worker count should stay at 1 until a workstation profile proves benefit without index-RAM or disk-I/O regressions.
