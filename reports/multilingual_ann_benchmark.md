# FAISS ANN Benchmark for Multilingual Retrieval

Date: 2026-09-26  
Decision: **Recommend HNSW `efSearch=64` as the next candidate configuration; keep multilingual retrieval disabled by default pending an isolated resource run and classifier confirmation.**

## Scope and preserved baseline

This experiment kept the six existing retrieval families and the `multilingual_name` method unchanged at the interface level. It used the same 300-S1 / 3,350-target / 1,065-ground-truth-pair benchmark and the same deterministic seed and labels as [`multilingual_retrieval_benchmark.md`](multilingual_retrieval_benchmark.md). No full-scale index, training, inference, hidden labels, or output-contract changes were used.

The multilingual vectors are normalized 384-dimensional E5 embeddings, so FAISS inner product is cosine similarity. Tested indexes were FlatIP, HNSW-FlatIP, and IVF-FlatIP. The exact semantic search is the reference.

## Tested configurations

| Configuration | Settings |
|---|---|
| Existing baseline | Six retrieval families; no multilingual method |
| Exact reference | Multilingual exact cosine, top-k 20 |
| FAISS Flat | `IndexFlatIP`, top-k 20 |
| FAISS HNSW low effort | HNSW M=32, `efConstruction=80`, `efSearch=32`, top-k 20 |
| FAISS HNSW reference | HNSW M=32, `efConstruction=80`, `efSearch=64`, top-k 20 |
| FAISS IVF | IVF-Flat, `nlist=64`, `nprobe=8`, top-k 20 |

All methods used the same minimum similarity threshold (`0.0`) and multilingual retrieval limit (`20`). The global union remained unchanged and retained method provenance.

## Candidate quality

| Configuration | Candidate pairs | Overall recall | Cross-script recall | Same-script recall | S2 recall | S3 recall | Incremental true pairs |
|---|---:|---:|---:|---:|---:|---:|---:|
| Existing baseline | 18,809 | 96.90% (1,032/1,065) | 60.76% (48/79) | 99.80% | 96.34% | 97.38% | 0 |
| Exact reference | 22,534 | 99.72% (1,062/1,065) | 97.47% (77/79) | 99.90% | 99.80% | 99.65% | 30 |
| FAISS Flat | 22,534 | 99.72% (1,062/1,065) | 97.47% (77/79) | 99.90% | 99.80% | 99.65% | 30 |
| HNSW `ef=32` | 22,704 | 99.72% (1,062/1,065) | 97.47% (77/79) | 99.90% | 99.59% | 99.83% | 30 |
| HNSW `ef=64` | 22,620 | 99.81% (1,063/1,065) | 98.73% (78/79) | 99.90% | 99.59% | 100.00% | 31 |
| IVF `nprobe=8` | 23,146 | 99.81% (1,063/1,065) | 98.73% (78/79) | 99.90% | 99.80% | 99.83% | 31 |

The two HNSW settings lost no measured overall recall relative to exact search. `efSearch=64` recovered one additional labeled pair in this sample, though the difference is within sample uncertainty. IVF also preserved measured recall but produced the largest candidate set.

## ANN recall relative to exact semantic retrieval

The exact method returned 1,019 true pairs through the multilingual method. HNSW `ef=32` returned 885 multilingual true hits, HNSW `ef=64` returned 960, and IVF `nprobe=8` returned 715. These method-hit counts include true pairs also found by existing methods; the final union recovered 30, 31, and 31 incremental pairs respectively. Therefore final union recall is more stable than raw multilingual-method recall, but exact semantic retrieval remains the reference for method-level coverage.

## Runtime and resource measurements

| Configuration | Index build time | Query time for 300 S1 | Candidate pairs/S1 |
|---|---:|---:|---:|
| Existing baseline | 0.019 s | 3.918 s | 62.70 |
| Exact reference | 22.959 s | 30.091 s | 75.11 |
| FAISS Flat | 20.188 s | 7.295 s | 75.11 |
| HNSW `ef=32` | 20.879 s | 7.853 s | 75.68 |
| HNSW `ef=64` | 19.996 s | 7.465 s | 75.40 |
| IVF `nprobe=8` | 20.076 s | 8.253 s | 77.15 |

FAISS Flat reduced query time by about 4.1x versus exact search. HNSW `ef=64` reduced it by about 4.0x while retaining the measured quality. These times include model/index setup effects in the bounded process and should not be treated as full-scale throughput guarantees.

The process high-water RSS reached 1.29 GB for exact, 1.64 GB for Flat, 1.72 GB for HNSW `ef=32`, 1.74 GB for HNSW `ef=64`, and 1.80 GB for IVF. Because configurations ran sequentially in one process, these are conservative process high-water values rather than isolated per-index peaks. They are not suitable for precise index-overhead comparison.

For 3,350 records, the raw vector payload is approximately `3,350 × 384 × 4 = 5.14 MB`. Extrapolated to 10 million targets, normalized FP32 vectors require approximately 14.3 GiB. HNSW M=32 adds roughly `10,000,000 × 32 × 2 × 4 = 2.38 GiB` of raw neighbor-link storage before allocator/index overhead. Flat has negligible graph overhead but retains the 14.3 GiB vector payload. IVF adds centroids, inverted-list IDs, and allocator overhead. These are estimates, not measured full-scale requirements; model/runtime memory must be added.

## Classifier quality

The same sample-trained LightGBM comparison from the exact-retrieval benchmark remains:

| Candidate source | Precision | Recall | Macro-F0.5 |
|---|---:|---:|---:|
| Existing baseline | 0.9945 | 0.9278 | 0.9779 |
| Exact multilingual | 0.9845 | 0.9794 | 0.9865 |

The ANN runs were evaluated at candidate level, but a separate LightGBM retraining/scoring pass was not run for each ANN configuration. This is intentional rather than silently treating candidate recall as classifier quality. Because HNSW/IVF changed the candidate sets slightly, final enablement still requires one isolated classifier comparison for the selected ANN setting.

## Recommendation

Recommend **HNSW M=32, `efSearch=64`, `efConstruction=80`, top-k 20** as the next optimization candidate. It preserved or slightly exceeded exact final candidate recall in this bounded sample and reduced query time from 30.1 seconds to 7.5 seconds. IVF is not preferred yet because it generated more candidates and had lower raw multilingual-method hit coverage at the tested `nprobe`.

Do not enable multilingual retrieval by default or start full-scale training. The remaining decision gate is a clean per-configuration resource measurement and a LightGBM score comparison for HNSW `ef=64` on the same entity split. If that run preserves the macro-F0.5 gain and the isolated 10M-target resource estimate fits the workstation budget, enable it through an experiment-specific configuration only.

## Reproducibility

Install the isolated benchmark dependencies, ensure the E5 model is cached, and run:

```bash
PYTHONPATH=. /tmp/ml_chl_multilingual_bench/bin/python scripts/benchmark_multilingual.py
```

The default production configuration remains `multilingual.enabled=false` and `index_type=exact`. The benchmark script explicitly supplies each ANN configuration; index and model lineage include the multilingual configuration through the existing candidate configuration hash.

Regression tests after the ANN code change: **15 passed**. No full-scale index, full-scale training, AWS resource, hidden label, or production default change was used.
