# Technical Design and Requirements Traceability Audit

## 1. Executive Summary

This audit reviewed the draft Technical Design (TDD) and Requirements Traceability Matrix (RTM) against `SRS-BL-1.0`, the official problem statement, and all six frozen designs. The core architecture is aligned: the TDD preserves six independent candidate-retrieval families and union semantics, six feature groups and a shared schema, LightGBM, entity-level validation, batch/disk-backed execution, compatibility checks, and no one-to-one constraint.

However, the documents **require revision** before approval. One high-severity frozen-design inconsistency states that no numerical workstation specifications exist even though `design_freeze.md` specifies them. The RTM is not an independently auditable one-to-one matrix: it contains six ranges of non-existent FR identifiers and only 62 literal IDs, rather than the 213 defined SRS IDs. No implementation was inspected or performed; all findings concern documentation/design coverage.

| Severity | Count |
|---|---:|
| Critical | 0 |
| High | 2 |
| Medium | 4 |
| Low | 1 |
| Total | 7 |

## 2. Audit Scope and Sources

Reviewed: `docs/TECHNICAL_DESIGN.md`, `docs/REQUIREMENTS_TRACEABILITY.md`, `docs/SRS.md`, `docs/SRS_BASELINE.md`, `docs/design_freeze.md`, `docs/problem_statement.md`, `docs/knowledge.md`, `useful/knowledge.md`, `docs/SRS_REVISION_SUMMARY.md`, and `docs/SRS_RECONCILIATION_REPORT.md`.

Authority was applied in this order: official challenge contract in `problem_statement.md`; requirements in SRS v1.0 / `SRS-BL-1.0`; frozen architecture in `design_freeze.md`; verified dataset context in `docs/knowledge.md`. `useful/knowledge.md` was reviewed as supporting context only. The audit did not treat the absence of a file named `useful.md` as a gap.

## 3. SRS Compliance Findings

### F-01 — Workstation evidence is incorrectly denied

| Field | Finding |
|---|---|
| Severity / classification | High / Frozen-design violation; documentation inconsistency |
| Affected section | `TECHNICAL_DESIGN.md` §10 |
| Evidence | TDD §10 says authoritative sources establish no numeric workstation specifications. `design_freeze.md` §2.1 specifies Intel Xeon w7-2575X, 22 cores/44 threads, 128 GB RAM, Windows, RTX 4000 Ada with 20 GB VRAM, CUDA 13.2, 2 TB SSD, and approximately 336 GB free; §2.2 specifies the laptop RTX 3050/4 GB VRAM. |
| Explanation | The statement is factually incorrect and weakens the frozen single-workstation resource design. It also prevents a concrete storage feasibility plan around the documented 336 GB working-space constraint. Exact runtime/batch/worker values remain open, but the hardware facts are established. |
| Recommended correction | Replace TDD §10.1 with a verified hardware table, distinguish primary workstation from secondary laptop, require Windows/dependency compatibility checks, and base preflight storage budgeting/monitoring on the approximately 336 GB free-space observation while requiring re-verification before a run. |

### F-02 — Input encoding is absent from the technical data contract

| Field | Finding |
|---|---|
| Severity / classification | Medium / SRS requirement gap |
| Affected section | `TECHNICAL_DESIGN.md` §§4–5 |
| Evidence | SRS §5.8.2 requires UTF-8 support for multilingual text; the challenge data contain mixed scripts. TDD calls the input TSV but never specifies UTF-8 decoding/validation or how decode failures are classified. |
| Explanation | This leaves a concrete ingestion behavior unspecified for a known multilingual input constraint. |
| Recommended correction | In §5, state that TSVs are decoded as UTF-8; define decode/schema failures as blocking input errors and preserve the original decoded raw values separately from normalized forms. |

### F-03 — Submission-package reproducibility obligations are not designed

| Field | Finding |
|---|---|
| Severity / classification | Medium / SRS requirement gap |
| Affected section | `TECHNICAL_DESIGN.md` §§11, 13, 15 |
| Evidence | `problem_statement.md` final-package requirements and SRS §§14.2–14.3 require self-contained runnable code, `README.md`, pinned dependency declaration/equivalent, and methodology documentation in addition to the two output TSVs. The TDD covers `output/` but has no package-assembly artifact/validation plan. |
| Explanation | Outputs can validate while the final reproducibility package remains noncompliant. This is not an implementation request; it is a missing design/verification responsibility. |
| Recommended correction | Add a final-submission artifact row and verification step covering package structure, reproducible run instructions, pinned dependencies/environment, source inclusion, and methodology-template completion. |

### F-04 — Candidate-budget audit trail is underspecified

| Field | Finding |
|---|---|
| Severity / classification | Medium / SRS requirement gap / technical feasibility risk |
| Affected section | `TECHNICAL_DESIGN.md` §6.9 |
| Evidence | The TDD correctly avoids an arbitrary cap, but says rejected candidates must not silently disappear from audit records. It does not define the artifact or required fields that distinguish method retrieval, configured limit/budget trimming, integrity rejection, and downstream scored candidates. SRS FR-7.5.5, FR-7.6.5–7.6.6, FR-11.6.5–11.6.7 require retained candidate/provenance and contribution analysis. |
| Explanation | Without explicit pre/post-limit counts and reason codes, candidate recall and method contribution cannot be reliably attributed when resource controls are tuned. |
| Recommended correction | Define a candidate-generation run report/partition manifest with method, query/batch, configured top-k/budget, retrieved count, retained count, exclusion reason, provenance, and score availability. Make the final candidate partition the sole inference input. |

## 4. Frozen-Design Compliance Findings

The following frozen decisions are substantively present and not weakened: all six retrieval families; independent execution and union/deduplication/provenance; no hard country equality filter; candidate recall separated from model quality; the six feature groups; agreement/disagreement/missing/non-comparable states; LightGBM primary model; generated-candidate labels with positive retention; entity-level split; validation threshold sweep and retraining; single-workstation batch processing; reusable indexes; disk-backed artifacts; checkpoint/resume; inference artifact compatibility; and controlled experiment/error analysis.

F-01 is the only frozen-design violation found. The TDD appropriately leaves retrieval implementations, embeddings, limits, formulas, sampling, hyperparameters, thresholds, batch sizes, storage format, and GPU execution subject to validation.

## 5. Traceability Matrix Verification

### Independent result

The SRS contains **213 unique defined functional-requirement IDs**, counted from requirement-definition lines of the form `**FR-x.y.z**`. No duplicate requirement-definition ID was found. This count is independent of repeated references in the SRS revision history.

The RTM contains **62 literal FR tokens**: **49 valid defined IDs** and **13 invalid endpoint IDs**. It relies on interval notation, so 164 defined IDs are not individually stated. When every valid interval is interpreted inclusively, the actual 213 defined IDs appear intended to be covered; therefore this audit does **not** find an uncovered defined ID. That interpretation is not sufficiently precise for a verification matrix.

### F-05 — RTM contains non-existent requirement ranges and is not mechanically auditable

| Field | Finding |
|---|---|
| Severity / classification | High / Traceability defect |
| Affected section | `REQUIREMENTS_TRACEABILITY.md`, main mapping table |
| Evidence | The rows `FR-8.1.1–FR-8.2.4`, `FR-9.1.1–FR-9.4.4`, `FR-10.1.1–FR-10.3.4`, `FR-11.5.1–FR-11.5.5`, `FR-12.3.1–FR-12.3.8`, and `FR-14.1.1–FR-14.3.8` name sections that have no defined FR IDs. The `FR-13.1.1–FR-13.4.10` interval also begins with a non-existent ID. |
| Explanation | These six rows conflate non-FR narrative SRS sections with functional requirements. Range-only notation also prevents direct ID extraction, duplicate detection, and per-requirement component ownership verification. |
| Recommended correction | Remove non-existent FR ranges. Use one row per actual FR ID (213 rows), or a machine-readable annex enumerating each ID with its parent grouped mapping. Retain a separate “non-FR challenge constraints” table rather than inventing FR identifiers. |

### F-06 — Several RTM mappings point to grouped, non-addressable TDD subsection labels

| Field | Finding |
|---|---|
| Severity / classification | Medium / Traceability defect |
| Affected section | `REQUIREMENTS_TRACEABILITY.md` mapping table; `TECHNICAL_DESIGN.md` §§6, 7, 9, 10 |
| Evidence | The TDD labels content as “6.2–6.7”, “7.1–7.2”, “7.3–7.5”, “9.2–9.4”, and “10.5–10.6”; the RTM maps requirements to individual endpoints such as §9.4 and §10.5. There is no individually headed §9.4 or §10.5 anchor. |
| Explanation | A reviewer cannot navigate from a mapped requirement to one exact owned subsection, nor can completeness of each of the six retrieval methods/features be audited from headings alone. Content exists, but mapping precision is reduced. |
| Recommended correction | Split compound TDD headings into individually numbered required subsections and update RTM pointers to exact headings; or map to the exact compound heading text consistently. |

### F-07 — RTM verification methods are too broad for several FR groups

| Field | Finding |
|---|---|
| Severity / classification | Low / Traceability defect |
| Affected section | `REQUIREMENTS_TRACEABILITY.md`, all grouped rows |
| Evidence | A single “fixture-based” or “contract test” method is assigned to ranges spanning materially distinct requirements, such as output generation, official-validator behavior, package content, and source ordering. |
| Explanation | These are useful test categories but do not establish an observable pass criterion for each requirement. The matrix is a plan, not a claim of implementation, which limits severity. |
| Recommended correction | For each actual ID, identify a component owner, verification artifact/test name, and pass condition; mark validation requiring the official helper as “pending availability” only where genuinely unavailable. |

## 6. Technical Feasibility Review

The system design is coherent: target indexes precede retrieval; union/provenance precedes feature joins; labels are applied only after candidate creation; and model/schema/config manifests bind training to inference. Disk-backed deterministic S1 partitions and atomic manifests are appropriate for the documented scale. No unapproved distributed architecture, fixed candidate cap, one-to-one reconciliation, or external identity lookup was introduced.

Feasibility remains conditional on measurement. Embedding model/index dependency and license compatibility, ANN memory/disk size, storage peak including checkpoint/temporary copies, CPU/GPU compatibility (especially CUDA/library support), candidate volume, and batch/worker settings require benchmark evidence. F-01 and F-04 must be resolved before a full-scale execution plan can be reviewed reliably.

## 7. Knowledge and Hardware Evidence Review

`docs/knowledge.md` facts are accurately reflected: S1 is reference; source schema has four fields; ground truth is list based; multi-match and singleton behavior exists; US/India training and France test require open-country handling; names/addresses are noisy and multilingual; name-only matching is unsafe; and F0.5 is precision-heavy.

`useful/knowledge.md` adds consistent detailed counts and examples but does not override the authoritative knowledge document. It does not introduce a contradictory fact requiring a design change.

Hardware is not missing evidence: `design_freeze.md` records the workstation and laptop specifications cited in F-01. Missing evidence remains the current usable disk on the actual input/work drive at run time, per-artifact size/peak temporary-storage estimates, installed package/driver compatibility, and benchmarked resource settings. These are open verification items, not values to guess.

## 8. Open Decisions and Missing Evidence

The TDD correctly marks normalization/tokenization, retrieval libraries/limits, embedding model/index/metric, candidate budget, feature formulas, negative sampling, LightGBM settings, threshold, batches/workers, formats/compression, and GPU use as open. None is improperly finalized.

No additional finding is raised for open parameters merely because they are unresolved: the frozen design expressly requires validation for them. The evidence gaps listed in §7 should become explicit preflight/benchmark gates, rather than parameter values embedded in the TDD.

## 9. Findings by Severity

| Severity | IDs |
|---|---|
| High | F-01, F-05 |
| Medium | F-02, F-03, F-04, F-06 |
| Low | F-07 |
| Critical | None |

## 10. Recommended Corrections with Exact Document Sections

1. Correct `TECHNICAL_DESIGN.md` §10 / add §10.1 hardware inventory, storage budget, Windows and CPU/GPU compatibility requirements (F-01).
2. Add UTF-8 decode/validation behavior to `TECHNICAL_DESIGN.md` §5 and the data contract in §4 (F-02).
3. Add final submission-package artifact/validation design to TDD §§11 and 13, with a verification phase in §18 (F-03).
4. Add pre-limit/post-limit candidate audit fields and reason-coded retention accounting to TDD §6.9–§6.10 and §13 (F-04).
5. Replace RTM’s invalid range rows and add an explicit 213-ID mapping annex/rows, separating non-FR constraints (F-05).
6. Replace compound TDD subsection labels with individual headings, then update RTM section pointers and verification criteria (F-06, F-07).

## 11. Final Readiness Assessment

**Requires revision.** The architectural core is sound and no critical or broad frozen-design failure was found. Nevertheless, the false hardware-evidence statement is material to the frozen resource design, and the RTM cannot yet serve as a reliable requirement-by-requirement verification instrument. Correcting F-01 and F-05, followed by the four medium issues, is necessary before approval for implementation planning. This assessment does not claim approval or implementation readiness.
