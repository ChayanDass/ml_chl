# Workstation Retrieval and Resource Execution

## Implemented architecture

Target indexes are built once per compatible target fingerprint and retrieval/embedding configuration, then persisted at `artifacts/indexes/<split>/<hash>.pkl` with a checksum manifest. Normalized records are stored under `artifacts/recovery/<split>/normalized/`. Candidate-method, union, feature, training-preparation, and scoring units remain under their experiment/run recovery roots, each with a checksum, lineage hash, deterministic S1 range, and atomic commit.

Embedding retrieval uses two local 64-dimensional representations: name-only and name-plus-address. The full-scale configured backend is FAISS IVF-PQ. Each query unions both ANN result sets into the existing `embedding_ann` provenance; it never removes candidates retrieved by any other family. IVF-PQ parameters are configuration values, not final tuning decisions. They must be selected only after candidate-recall and throughput tests on the workstation.

`backend=faiss_ivfpq` fails safely if FAISS is unavailable. `backend=bruteforce` is a bounded development-only fallback and refuses target sets above `bruteforce_max_targets`. This prevents accidental exhaustive embedding search during a full run.

## Resource policy

The starting workstation envelope reserves 16 GiB RAM headroom (96 GiB soft / 112 GiB hard target), 4 GiB VRAM headroom, and 80 GiB free disk reserve. Preflight reports current RAM/disk capacity; train and infer fail before processing if disk reserve is unavailable. CPU workers are configured as an upper ceiling only and require a representative workstation benchmark before enabling parallel candidate workers. GPU use is disabled until compatible FAISS/LightGBM builds and a benchmark demonstrate benefit.

The optional multilingual retrieval family is disabled by default. Before enabling it, benchmark model availability/license, supported scripts, encoding throughput, vector/index size, peak RAM/VRAM, candidate volume, incremental recall, and checkpoint recovery. Its configuration is included in index and model lineage hashes so changing the model, device, limit, or enabled state cannot reuse incompatible artifacts.

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










I inspected the repository without changing it.
Current state:
- Git remote: git@github.com:ChayanDass/ml_chl.git
- Current local commit: f9adfbefb909e12ab37f3641250f79f28ec9b0f0
- .gitignore already excludes datasets, artifacts, outputs, JSONL, model/index files, and environments.
- The CLI already supports separate --data, --artifacts, and --output paths, which is ideal for keeping large AWS data outside Git.
- Existing checkpoint lineage binds inputs/config/schema/indexes, but does not explicitly include the Git commit/code fingerprint. This is the critical gap to fix before sharing artifact directories across commits.
Proposed workflow
Use two separate EC2 filesystem locations:
/opt/entity-resolution/code/       # Git clone only; disposable/replaced per commit
/mnt/entity-resolution-data/       # EBS-backed persistent data; never inside Git
  dataset/
  artifacts/
  outputs/
  benchmarks/
  logs/
This means git pull, checkout, rollback, or a fresh clone never touches raw data, indexes, checkpoints, or reports.
Local machine: publish a tested commit
git status
python3 -m unittest discover -s tests -v
git add src tests config docs README.md requirements.txt approach_audit.md .gitignore
git commit -m "Describe the tested change"
git push origin main
git rev-parse HEAD
Record the printed full commit SHA before using AWS.
AWS terminal: first-time setup
sudo mkdir -p /opt/entity-resolution /mnt/entity-resolution-data/{dataset,artifacts,outputs,benchmarks,logs}
sudo chown -R "$USER":"$USER" /opt/entity-resolution /mnt/entity-resolution-data

git clone git@github.com:ChayanDass/ml_chl.git /opt/entity-resolution/code
cd /opt/entity-resolution/code

git checkout --detach <FULL_COMMIT_SHA>
git rev-parse HEAD

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

.venv/bin/python -m src.cli preflight \
  --artifacts /mnt/entity-resolution-data/artifacts \
  --config config/default.json
Copy the official dataset into /mnt/entity-resolution-data/dataset/ outside Git using your chosen secure transfer method. Do not commit it.
AWS terminal: representative benchmark
cd /opt/entity-resolution/code

.venv/bin/python -m src.cli train \
  --data /mnt/entity-resolution-data/dataset \
  --artifacts /mnt/entity-resolution-data/artifacts \
  --config config/default.json \
  --sample 10000 \
  --experiment benchmark-<short-sha>
Later, resume that exact benchmark with the same command.
AWS terminal: update to a newer commit safely
Do not use git pull blindly inside the active release directory. Instead:
cd /opt/entity-resolution/code
git fetch origin
git checkout --detach <NEW_FULL_COMMIT_SHA>
git rev-parse HEAD

.venv/bin/pip install -r requirements.txt
The dataset and artifact paths remain outside the clone. With the proposed code-fingerprint change below, incompatible artifacts will be rejected/rebuilt rather than silently reused.
AWS terminal: rollback
cd /opt/entity-resolution/code
git checkout --detach <PREVIOUS_TESTED_FULL_COMMIT_SHA>
git rev-parse HEAD
Then rerun the exact benchmark/full-run command for that commit. Compatible artifacts can be reused; incompatible ones must be isolated or rebuilt.
Proposed repository changes requiring approval
I recommend adding only these focused changes:
1. docs/AWS_EC2_WORKFLOW.md
   - Beginner-safe clone/setup/update/rollback/benchmark instructions.
   - Dataset/artifact separation, EBS persistence, stopping/terminating guidance, cost reminders.
2. scripts/run_benchmark.sh
   - Requires an explicit confirmation flag such as --confirm-long-run.
   - Captures commit SHA, Git dirty status, config checksum, instance metadata, OS/Python/dependency versions, command, timestamps, preflight output, and artifact paths in a benchmark report outside Git.
3. src artifact lineage enhancement
   - Add the resolved Git commit SHA or deterministic source-tree fingerprint to index/checkpoint/model lineage.
   - This prevents a changed code commit from reusing old artifacts unless explicitly compatible.
4. Possibly config/aws-benchmark.example.json
   - An example only; no AWS dependency or credentials.
   - Keeps AWS-specific paths/resource settings out of the default local config.
5. README link to the workflow document.
AWS safety guidance
- Use an IAM role or least-privilege IAM user; do not put AWS root credentials on the instance.
- Use a dedicated EBS volume for /mnt/entity-resolution-data; EBS volume charges continue while the instance is stopped.
- Stop the EC2 instance whenever not actively benchmarking. Terminate it only after confirming which EBS volumes/snapshots you intend to keep.
- Set AWS Budgets alerts plus Cost Explorer/CloudWatch monitoring, but treat alerts as notifications—not a guaranteed spending cap.
- Never run a long benchmark until you have explicitly reviewed the instance type, EBS volume size/type, current cost estimate, and exact commit SHA.
I will wait for your approval before adding the workflow document, benchmark wrapper, and code-commit lineage protection.
