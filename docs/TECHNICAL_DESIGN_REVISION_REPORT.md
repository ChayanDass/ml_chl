# Technical Design Revision Report

## Scope and Status

This report records documentation-only remediation of audit findings F-01 through F-07. The SRS, baseline, problem statement, frozen design, project knowledge, and audit report were not modified. No code, datasets, training, or implementation work was performed.

## Finding Resolution

| Finding | Resolution status | Revision made |
|---|---|---|
| F-01 — hardware evidence | Resolved | TDD §10.1 now records the verified workstation and laptop specifications, treats ~336 GB free SSD as a recheckable observation, and adds Windows/dependency, storage-preflight, and peak-space controls. |
| F-02 — UTF-8 input contract | Resolved | TDD §§4–5 now require UTF-8 decoding, preserve original decoded values, and distinguish blocking decode/schema failures from recoverable data-quality conditions. |
| F-03 — submission package | Resolved | TDD §11.7, §13, and §18 define package assembly/completeness verification for outputs, runnable source, README, dependency declaration, and methodology template. |
| F-04 — candidate-budget audit trail | Resolved | TDD §§6.9–6.10 and §13 define per-batch candidate reports with pre/post-limit counts, provenance, exclusion reasons, budget/limit settings, and scored counts. |
| F-05 — invalid/non-auditable RTM | Resolved | RTM now has one row for every individually extracted SRS FR; invalid ranges and invented IDs were removed, with non-FR constraints separated. |
| F-06 — non-addressable headings | Resolved | TDD has individually addressable §6.2–§6.10, §7.1–§7.10, §9.1–§9.4, §10.1–§10.6, and §11.1–§11.7 headings; RTM uses these existing anchors. |
| F-07 — vague verification | Resolved | Every RTM row now names a responsible component, a planned verification artifact/method, and an observable pass criterion. Planned verification is explicitly not represented as executed. |

## FR Extraction and RTM Coverage Results

The following checks were executed against the revised files:

| Check | Result |
|---|---:|
| Unique requirement-definition IDs extracted from `docs/SRS.md` | 213 |
| Individually enumerated RTM mapping rows | 213 |
| Defined SRS IDs missing from RTM | 0 |
| RTM IDs absent from SRS definitions | 0 |
| Duplicate RTM IDs | 0 |
| RTM rows lacking required mapping/component/verification/pass-criterion cells | 0 |
| Invalid FR ranges | 0 |

The extraction used only SRS requirement-definition lines in the form `**FR-x.y.z**`, rather than references in revision history or narrative text.

## Remaining Open Decisions

The frozen design intentionally leaves normalization, retrieval libraries and limits, embedding/index implementation, candidate budget selection, feature formulas, sampling ratios, model settings, threshold value, worker/batch settings, storage/compression, and workload-specific GPU use open. The revised TDD retains them as validation/approval decisions. Current usable disk space, dependency/driver compatibility, artifact-size estimates, and performance benchmarks remain required preflight evidence; no values were invented.

## Final Status

**Ready for fresh audit.** The seven audit findings were addressed in the two revised draft documents. This status is not an approval claim and does not assert that planned implementation verification has been performed.
