# Multilingual Retrieval Benchmark

Date: 2026-09-26  
Decision: **Defer full-scale enablement; retain the extension for ANN/scaling optimization.**

## 1. Environment and model

The benchmark used an isolated environment at `/tmp/ml_chl_multilingual_bench` with CPU-only PyTorch, `sentence-transformers 6.1.0`, `LightGBM 4.5.0`, `numpy 1.26.4`, and `scikit-learn 1.4.1.post1`. The project environment was not modified.

The configured candidate is `intfloat/multilingual-e5-small`. The model card identifies an MIT license and multilingual support; the published model specification is approximately 118M parameters, 384-dimensional output, and 512-token context. The model coverage includes the observed Latin, French, Devanagari/Hindi, Tamil, Telugu, Gujarati, Kannada, Bengali, Malayalam, Odia/Oriya, and Punjabi/Gurmukhi language families, with some language/script variants represented separately. Sources: [model card](https://huggingface.co/intfloat/multilingual-e5-small), [MTEB model entry](https://leaderboard.mteb.org/models/intfloat/multilingual-e5-small), and [published model-size table](https://neurips2024-enlsp.github.io/papers/paper_83.pdf).

Representative names encoded successfully in Latin, Tamil, Devanagari, Gujarati, and French text. Six-name encoding produced 384-dimensional vectors in 0.075 seconds after model load; model load took 46.8 seconds and peak process RSS was approximately 936 MB. A cross-script example produced cosine similarity 0.859. This is an encoding sanity check, not a quality claim.

## 2. Labeled benchmark sample

The benchmark used the supplied training files and ground truth. It selected the first 300 S1 records, loaded every corresponding ground-truth target, and added sampled ordinary target records from S2/S3. The sample contained:

| Item | Count |
|---|---:|
| S1 records | 300 |
| S2/S3 target records | 3,350 |
| Ground-truth pairs | 1,065 |
| Cross-script positive pairs | 79 |
| Same-script positive pairs | 986 |
| Validation S1 entities for classifier | 60 |
| Validation candidate pairs, baseline | 3,668 |
| Validation candidate pairs, updated | 4,415 |

The entity-level split used the existing deterministic `split_ids` procedure and seed `20260926`, with 20% of this bounded sample held out. Ground-truth labels were used only for evaluation/training labels; no truth pair was injected into inference candidates. Both address-present and address-missing cases occur naturally in the selected records, but this benchmark does not have enough power for a reliable missingness subgroup conclusion.

The reproducible driver is [`scripts/benchmark_multilingual.py`](../scripts/benchmark_multilingual.py). The updated retrieval code was run with the configured model, CPU device, top-20 multilingual limit, and zero minimum similarity threshold. Existing retrieval settings remained token 30, fuzzy 20, address 30, country 15, embedding 20, and maximum postings 5,000.

## 3. Candidate-generation results

| Metric | Existing six families | Six + `multilingual_name` | Change |
|---|---:|---:|---:|
| Candidate pairs | 18,783 | 22,512 | +19.9% |
| Candidates per S1 | 62.61 | 75.04 | +12.43 |
| Overall candidate recall | 96.90% (1,032/1,065) | 99.72% (1,062/1,065) | +2.82 pp |
| Cross-script recall | 60.76% (48/79) | 97.47% (77/79) | +36.71 pp |
| Same-script recall | 99.80% | 99.90% | +0.10 pp |
| S2 recall | 96.34% | 99.80% | +3.46 pp |
| S3 recall | 97.38% | 99.65% | +2.27 pp |
| True pairs retrieved by multilingual method | 0 | 1,019 | New method output |
| Incremental true pairs recovered only by multilingual method | 0 | 30 | New method contribution |
| Multilingual candidate overlap with existing methods | 0 | 2,271 | Provenance overlap |

The new family materially improves candidate recall in this sample, especially across scripts. The 30 incremental true pairs are the most direct evidence that the method adds retrieval coverage rather than merely duplicating existing methods.

## 4. Classifier results

Both configurations trained a fresh LightGBM model with the existing settings: 300 estimators, learning rate 0.05, 31 leaves, minimum child samples 20, random state 20260926. Thresholds were selected from the existing `[0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]` sweep on the held-out S1 entities.

| Metric | Existing six families | Six + `multilingual_name` | Change |
|---|---:|---:|---:|
| Selected threshold | 0.30 | 0.30 | 0 |
| Validation macro-F0.5 | 0.9779 | 0.9865 | +0.0086 |
| Precision diagnostic | 0.9945 (180/181) | 0.9845 (190/193) | -0.0100 |
| Recall diagnostic | 0.9278 (180/194) | 0.9794 (190/194) | +0.0516 |

This is a bounded labeled validation result, not a full-data model-selection result. It indicates that the extra candidates improved recall enough to raise macro-F0.5, with a measurable precision trade-off.

## 5. Runtime and resource results

The current benchmark path uses exact cosine search over persisted in-memory semantic vectors, not the final full-scale ANN implementation. This makes the resource result conservative for query cost and is the reason full-scale enablement is deferred.

| Measurement | Baseline | Updated | Change |
|---|---:|---:|---:|
| Index build time | 0.018 s | 23.36 s | model load/encoding cost |
| Query time for 300 S1 | 4.074 s | 30.347 s | 7.45x |
| Peak process RSS | 82.9 MB | 1,273.2 MB | +1,190.3 MB |
| Estimated 3,350 x 384 FP32 vectors | n/a | 4.9 MB | vector payload only |

The updated run was feasible on the bounded sample, but direct extrapolation to approximately 10M targets is not justified. The model process footprint and exact-search query cost require an ANN index, batched/vectorized query implementation, or another resource-efficient design before full training/inference.

## 6. Limitations and reproducibility

- The sample is 300 S1 records rather than the full training set; the S1 selection is deterministic but not a formal stratified random sample.
- Cross-script positives numbered 79, so the 97.47% estimate has meaningful sampling uncertainty.
- France has no ground truth in the supplied data; no France precision/recall/F0.5 claim is made.
- The benchmark did not run the full production FAISS multilingual ANN path because the current implementation stores exact semantic vectors and the task requires resource safety.
- Classifier results are sample-trained models, not the existing stored model and not final retraining.
- No hidden-test labels, AWS resources, full-scale training, or full-scale inference were used.

Re-running requires the isolated environment, cached model, `PYTHONPATH=.`, and:

```bash
PYTHONPATH=. /tmp/ml_chl_multilingual_bench/bin/python scripts/benchmark_multilingual.py
```

## 7. Decision gate and next experiment

Quality gates passed on the bounded sample: candidate recall improved, 30 incremental true pairs were recovered, and sample macro-F0.5 improved. Compatibility and output tests remain passing from the implementation phase. The resource gate is not yet passed for full-scale execution because exact semantic search is too costly to extrapolate safely.

**Recommendation: defer enabling `multilingual_name` for final full-scale training and inference.** Retain the implementation and benchmark evidence, then run the smallest next experiment: encode the same labeled sample once, build a FAISS inner-product ANN index over the 384-dimensional vectors, compare ANN recall at several `k`/probe settings against exact semantic retrieval, and measure peak RSS/query throughput. Enable the family only if ANN preserves the observed recall gain within the workstation runtime and memory budget.
