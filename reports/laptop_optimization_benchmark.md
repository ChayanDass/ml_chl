# Laptop Optimization Benchmark

Date: 2026-09-26  
Scope: bounded code optimization only; no full-scale training, inference, AWS resources, or checkpoint deletion.

## Bottlenecks identified

- Feature extraction repeatedly resolved cached token/address views inside the candidate loop.
- Candidate generation remains dominated by per-query lexical work and, when explicitly enabled, multilingual model encoding/query work.
- Full-scale memory and runtime remain dominated by target indexes, model vectors, and ANN/model process overhead; this laptop phase does not establish AWS capacity.

## Changes implemented

In `src/core.py`, `feature_rows()` now builds S1 and target token/address view maps once per feature batch and reuses them for every pair. Feature formulas, missingness semantics, provenance, schema order, and values are unchanged. The fallback path still supports lightweight test fixtures without precomputed views.

The optional multilingual configuration continues to default to disabled and now records the selected HNSW settings (`M=32`, `efConstruction=80`, `efSearch=64`) for explicit experimental runs. No retrieval family was removed or bypassed.

## Before and after benchmark

Benchmark input: the existing bounded sample loader, 300 S1 records, 3,350 targets, and 18,777 baseline candidate rows. The optimized implementation was compared with an in-process reference copy of the prior feature loop using identical candidate rows.

| Measurement | Before | After | Change |
|---|---:|---:|---:|
| Candidate-generation time | 4.0275 s | 4.0275 s | unchanged |
| Feature extraction time | 1.9655 s | 1.9325 s | 1.7% faster |
| Feature rows | 18,777 | 18,777 | unchanged |
| Feature equivalence | reference | exact equality | passed |
| Optimized throughput | n/a | 9,716.6 rows/s | measured |

This is a small safe improvement, not a claim of full-scale runtime reduction. The benchmark did not materialize a full dataset matrix.

## Quality and compatibility

- Existing candidate rows and method provenance were unchanged.
- Feature dictionaries were exactly equal to the prior implementation on the bounded sample.
- Multilingual retrieval remains available only when explicitly enabled; default execution remains disabled.
- HNSW settings remain configurable and are included in the existing candidate configuration lineage hash.
- Output schema and ordering code were not changed.

## Resource measurements

The bounded process used the existing sample and did not create large persistent artifacts. No additional disk usage or large cache was introduced. The earlier ANN benchmark measured approximately 7.47 seconds for 300-S1 HNSW `efSearch=64` queries and approximately 1.74 GB process high-water RSS in a separate isolated benchmark process; those figures are retained as reference, not repeated or improved by this feature-only optimization.

No full-scale laptop resource conclusion is made. AWS representative benchmarking remains required for approximately 10M target records, especially vector/index memory, model encoding throughput, worker scaling, and checkpoint growth.

## Tests

- Existing regression suite: **15 passed**.
- Python compilation for `src/core.py` and `scripts/benchmark_multilingual.py`: passed.
- `git diff --check`: passed.
- Feature equivalence against the prior loop: passed.

## Known limitations and next bottlenecks

- The measured feature speedup is only 1.7%; larger gains require profiling full candidate and index stages rather than speculative rewrites.
- Multilingual HNSW quality/resource validation remains bounded to the previous 300-S1 benchmark.
- Peak RSS in sequential ANN comparisons was a process high-water mark, not an isolated per-index measurement.
- No full-scale training or inference feasibility claim is supported by this laptop run.

## AWS readiness

The code is ready to proceed to Phase 3 AWS setup and representative benchmarking, with conditions: use an isolated AWS environment, preserve the disabled default, begin with a bounded representative sample, measure isolated per-stage CPU/RAM/disk/throughput, and compare HNSW `efSearch=64` against exact/reference quality before any full-scale run. The project is **not** ready to begin full-scale training or inference solely from this laptop result.
