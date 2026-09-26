# Business entity resolution

All source data remain read-only. The pipeline validates UTF-8 TSVs, normalizes records, builds reusable S2/S3 indexes, executes six retrieval families, keeps union provenance, creates six-group features, uses entity-level validation, trains LightGBM, selects macro-F0.5 threshold, and writes validated output TSVs.

```bash
python3 -m pip install -r requirements.txt
python3 -m src.cli preflight --artifacts artifacts --config config/default.json
python3 -m src.cli train --data 6ab10eb3b23ba_student_resource/student_resource/dataset --sample 5000 --experiment laptop-smoke
python3 -m src.cli infer --data 6ab10eb3b23ba_student_resource/student_resource/dataset --sample 5000 --experiment laptop-smoke --output output_smoke
```

Workstation full-scale commands (omit `--sample`):

```bash
python3 -m src.cli preflight --artifacts artifacts
python3 -m src.cli train --data /path/to/dataset --artifacts artifacts --experiment full-v1
python3 -m src.cli infer --data /path/to/dataset --artifacts artifacts --experiment full-v1 --output output
python3 6ab10eb3b23ba_student_resource/student_resource/utils/validate_submission.py --matching output/matching_results.tsv --candidate output/candidate_pairs.tsv --test-dir /path/to/dataset/test
```

Indexes and JSONL partitions have checksum manifests and atomic promotion. Re-running compatible index construction reuses the index; mismatches are rejected.

## Recovery

No separate resume command is needed: repeat the exact command that failed. Completed units are reused only when their manifest status, checksum, row count, input fingerprint, retrieval configuration, and feature-schema lineage match. Invalid payloads are renamed with a `.corrupt-<timestamp>` suffix and rebuilt without deleting valid sibling partitions.

```bash
# Resume an interrupted training run
python3 -m src.cli train --data /path/to/dataset --artifacts artifacts --experiment full-v1
# Resume an interrupted inference/output run
python3 -m src.cli infer --data /path/to/dataset --artifacts artifacts --experiment full-v1 --output output
```

Candidate recovery is per S1 batch and retrieval family; union and features are per S1 batch; training split/sample is a distinct checkpoint; scoring is checkpointed as an inference stage. Model fitting is an atomic model-level unit: `latest_model.pkl` and `best_model.pkl` survive later-stage failures, but an interruption during a single LightGBM `.fit()` restarts that fit after reusing all data preparation artifacts.

Inference processes one deterministic S1 partition at a time from candidate retrieval through feature extraction, scoring, output staging, and streaming output validation. Training uses persisted partitions for recovery but the selected LightGBM sklearn interface still materializes its selected training matrix in RAM.

## Workstation resource guardrails

`config/default.json` carries the primary-workstation starting guardrails: 5,000 S1 records per partition, 20 CPU workers as a ceiling, 96/112 GiB RAM soft/hard targets, an 80 GiB disk reserve, and a 4 GiB GPU-VRAM reserve. `train` and `infer` refuse to start when the configured disk reserve is unavailable. Run preflight on the workstation before changing `gpu_enabled` or the worker ceiling.

The full-scale embedding path is configurable FAISS IVF-PQ; see [workstation execution guidance](docs/WORKSTATION_EXECUTION.md). The exact bounded cosine path is retained only for tests and small development samples. GPU acceleration remains disabled until a representative workstation benchmark validates a compatible FAISS/LightGBM runtime.
