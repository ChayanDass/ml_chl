# Workstation Retrieval and Resource Execution

## Implemented architecture

Target indexes are built once per compatible target fingerprint and retrieval/embedding configuration, then persisted at `artifacts/indexes/<split>/<hash>.pkl` with a checksum manifest. Normalized records are stored under `artifacts/recovery/<split>/normalized/`. Candidate-method, union, feature, training-preparation, and scoring units remain under their experiment/run recovery roots, each with a checksum, lineage hash, deterministic S1 range, and atomic commit.

Embedding retrieval uses two local 64-dimensional representations: name-only and name-plus-address. The full-scale configured backend is FAISS IVF-PQ. Each query unions both ANN result sets into the existing `embedding_ann` provenance; it never removes candidates retrieved by any other family. IVF-PQ parameters are configuration values, not final tuning decisions. They must be selected only after candidate-recall and throughput tests on the workstation.

`backend=faiss_ivfpq` fails safely if FAISS is unavailable. `backend=bruteforce` is a bounded development-only fallback and refuses target sets above `bruteforce_max_targets`. This prevents accidental exhaustive embedding search during a full run.

## Resource policy

The starting workstation envelope reserves 16 GiB RAM headroom (96 GiB soft / 112 GiB hard target), 4 GiB VRAM headroom, and 80 GiB free disk reserve. Preflight reports current RAM/disk capacity; train and infer fail before processing if disk reserve is unavailable. CPU workers are configured as an upper ceiling only and require a representative workstation benchmark before enabling parallel candidate workers. GPU use is disabled until compatible FAISS/LightGBM builds and a benchmark demonstrate benefit.

Illustrative embedding storage estimate (not a total-index estimate): 10.3M records × 64 FP32 dimensions × two representations is about 4.9 GiB of raw vectors during index construction. IVF-PQ codes with `m=8` are about 0.15 GiB for two code sets, excluding IVF centroids, IDs, training buffers, and Python-side lexical indexes. Build-time vectors, token/gram maps, and target records are the dominant unmeasured RAM risks; validate them on a workstation subset before full execution.

## Required workstation validation

```bash
python3 -m pip install -r requirements.txt
python3 -m src.cli preflight --artifacts artifacts --config config/default.json
python3 -m src.cli train --data /path/to/dataset --sample 10000 --experiment workstation-benchmark
```

Record index RSS, disk size, candidate recall/volume, ANN recall contribution, and elapsed time. Only then choose IVF `nlist`, `nprobe`, PQ settings, batch size, worker count, and optional GPU backend. Do not run full scale until this checkpoint succeeds.

To begin/resume an approved full run, use the same command:

```bash
python3 -m src.cli train --data /path/to/dataset --artifacts artifacts --experiment full-v1
```

Changing input, normalization, retrieval or embedding configuration changes the index and checkpoint lineage and rebuilds dependent units while preserving unrelated valid artifacts.
