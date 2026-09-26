# SRS Baseline Record

**Baseline Establishment Date:** September 26, 2026  
**Baseline Identifier:** `SRS-BL-1.0`  
**Status:** Active – Frozen Baseline Established  
**Authority:** Project Requirements Governance

---

## 1. Baseline Identification

### 1.1 Baseline Document

| Attribute | Value |
| --------- | ----- |
| **Document Name** | Software Requirements Specification (SRS) |
| **Baseline Version** | 1.0 |
| **SRS File Path** | `/home/vikaspal/Desktop/ml_chl/docs/SRS.md` |
| **Baseline Identifier** | `SRS-BL-1.0` |
| **Baseline Establishment Date** | September 26, 2026 |
| **Approval Status** | Approved – Final |
| **Document Status (SRS Section 1.3)** | APPROVED — FINAL VERSION 1.0 |

### 1.2 Document Scope

The frozen SRS encompasses the complete software requirements for the Business Entity Resolution Challenge, incorporating:

* All official challenge requirements from the problem statement
* All six frozen architectural decisions from `design_freeze.md` (Design 1–6)
* Complete system behavior specification for candidate generation, feature extraction, matching, training, inference, and evaluation
* All data-quality, reproducibility, and testing requirements
* Explicit distinction between frozen [FROZEN] and experimental [EXPERIMENTAL] requirements

**Total Frozen Requirements in Baseline:** 47 requirements marked [FROZEN]  
**Total Functional Requirements in SRS v1.0:** 200+ requirements across all sections

### 1.3 Baseline Content Verification

The following sources were verified for consistency with the frozen SRS:

| Source Document | Verification Status | Notes |
| --------------- | ------------------- | ----- |
| `docs/SRS.md` v1.0 | ✓ Consistent | Approved – Final status confirmed |
| `docs/SRS_REVISION_SUMMARY.md` | ✓ Consistent | Confirms v1.0 incorporates Design 1-6 |
| `docs/SRS_RECONCILIATION_REPORT.md` | ✓ Consistent | Post-revision assessment: "APPROVED FOR IMPLEMENTATION" |
| `docs/design_freeze.md` | ✓ Consistent | All six frozen designs are fully covered in SRS v1.0 |

---

## 2. Baseline Authority and Purpose

### 2.1 Authority Statement

**The frozen SRS v1.0 (`SRS-BL-1.0`) is the authoritative requirements baseline for this project.**

This baseline:

* Defines all mandatory system behavior, constraints, and acceptance criteria
* Is binding for all downstream technical design, implementation, testing, and verification activities
* Supersedes draft requirements, preliminary specifications, or informal documentation
* Shall not be unilaterally modified without formal change control

### 2.2 Baseline Applicability

The frozen SRS applies to:

* **Technical Design:** All design decisions must satisfy SRS requirements; design deviations require documented change control
* **Implementation:** All code must implement SRS-specified behavior; implementation changes affecting SRS coverage require change control
* **Testing:** All acceptance tests must verify SRS compliance; test coverage gaps must be resolved before release
* **Verification:** All audits and quality assurance must reference SRS requirements and confirm traceability

### 2.3 Purpose

Establishment of this baseline ensures:

1. **Requirement Stability:** Prevents ad-hoc requirement changes during implementation
2. **Traceability:** All design, code, and test artifacts can be traced to baseline requirements
3. **Change Control:** All modifications follow documented governance procedures
4. **Accountability:** Clear record of approved requirements and authorized changes
5. **Quality Assurance:** Verifiable compliance against a stable, approved specification

---

## 3. Change-Control Rules

### 3.1 Change Authorization

All changes to the frozen SRS baseline must follow this procedure:

1. **Proposal:** Document the proposed change, including:
   - Clear statement of the change (what is being added, removed, or modified)
   - Affected requirement IDs and SRS sections (e.g., FR-7.5.6, Section 11.3)
   - Reason for the change (e.g., discovered requirement gap, design constraint, clarification)
   - Impact assessment: effects on technical design, implementation, testing, and verification

2. **Justification:** Provide explicit justification demonstrating that:
   - The change is necessary and not a clarification of existing requirements
   - The change does not contradict frozen architectural decisions in `design_freeze.md`
   - The impact on project schedule, cost, and risk has been evaluated
   - Alternative solutions have been considered

3. **Review:** Submit for review by:
   - Project requirements authority (if established)
   - Technical design lead
   - Any other stakeholders affected by the change

4. **Approval:** Change must be explicitly approved in writing. Unapproved changes must **not** be incorporated into the baseline.

5. **Implementation:** Upon approval:
   - Update the baseline SRS with the approved change
   - Assign a new version number (minor or patch version per Section 1.2 versioning rules)
   - Record the change in the Change Log (Section 4 of this document)
   - Update the SRS Version History table
   - Regenerate the baseline checksum and update Section 4.3

6. **Notification:** Notify all stakeholders that the baseline has been updated and identify which requirements changed

### 3.2 Unapproved Changes

**Unapproved changes to the baseline are prohibited.**

This includes:
- Silent modifications to SRS requirement text without change control
- Additions of new requirements without formal approval
- Removal of requirements without justification and documented approval
- Changes to frozen requirement status ([FROZEN] → [EXPERIMENTAL] or vice versa)

Violations of the change-control rule must be detected and corrected through:
- Baseline integrity checks (checksum verification, diff audits)
- Code review procedures that validate implementation against baseline
- Test design review procedures that validate test coverage against baseline

### 3.3 Emergency Changes

In exceptional circumstances where stability of the baseline must be maintained while permitting urgent modifications:

- A proposed emergency change may be implemented with **provisional approval** (documented as "Provisional – Pending Formal Approval")
- Provisional changes must be explicitly marked in the SRS with an annotation, e.g., `[PROVISIONAL CHANGE: Change-ID-001]`
- Provisional changes must receive formal approval within one business cycle
- If formal approval is not granted, provisional changes must be reverted

---

## 4. Change Log

### 4.1 Baseline Establishment

**Change ID:** N/A (Baseline Establishment)  
**Date:** September 26, 2026  
**Version:** 1.0  
**Change Type:** Baseline Establishment  
**Status:** Approved

**Description:**

Formal establishment of SRS v1.0 as the approved requirements baseline (`SRS-BL-1.0`). 

SRS v1.0 incorporates all six frozen architectural decisions from `design_freeze.md`:
- Design 1: Hybrid six-method candidate-generation architecture
- Design 2: Six-group feature-extraction architecture with shared schema
- Design 3: LightGBM binary classification with entity-level train/validation split and validation-based threshold selection
- Design 4: Single-workstation batch processing with reusable indexes and checkpointing
- Design 5: Inference pipeline with configuration validation and preprocessing consistency
- Design 6: Separate candidate-recall evaluation with controlled experiments and error analysis

**Requirements Added in v1.0:** 70+ frozen requirements across all design areas (FR-7.5.6 through FR-15.1.8)

**Approval Authority:** Project Requirements Governance  
**Baseline Checksum:** `60d0b24476d1dff470babe1d138252ea2760e112926969fac8fbe22f35e7a46a`

**Affected Sections:** 
- Section 1 (Document Control) – updated version history and status
- Section 7.5-7.6 (Candidate Generation) – added frozen architecture requirements
- Section 7.8 (Feature Extraction) – added frozen six-group architecture requirements
- Section 11.1-11.6 (Training and Evaluation) – added frozen training, validation, and evaluation requirements
- Section 12.1-12.4 (System Architecture) – added frozen architecture and checkpointing requirements
- Sections 13.4, 15.1 – added reproducibility and testing requirements

**Rationale:**

Prior to baseline establishment, the SRS v0.1 (Draft) identified high-level requirements but lacked explicit formalization of approved frozen designs. This created risk of:
- Implementation divergence from approved architecture
- Ambiguity in downstream technical design
- Gaps in test coverage verification

Formalization of v1.0 as the baseline ensures all future work traces directly to approved requirements and frozen architectural decisions.

**Next Action:** Proceed with Technical Design development; all technical design decisions must satisfy SRS v1.0 requirements.

---

### 4.2 Change Log Template (for Future Changes)

**Change ID:** [Auto-assigned identifier, e.g., SRS-CHG-00002]  
**Date:** [YYYY-MM-DD]  
**Version:** [New version number]  
**Change Type:** [Addition | Modification | Removal | Clarification | Design Impact]  
**Status:** [Approved | Provisional | Rejected | Pending]

**Description:**
[Clear statement of the change]

**Affected Requirement IDs:**
[List of changed FR-IDs and sections, e.g., FR-7.5.6, Section 11.3]

**Justification:**
[Reason for the change, impact assessment, alternatives considered]

**Approval Authority:**
[Name/title of decision maker]

**New Checksum:**
[SHA-256 hash of updated SRS]

**Implementation Notes:**
[Any additional guidance for implementers or testers]

---

## 5. Baseline Integrity

### 5.1 Checksum Verification

The SHA-256 checksum provides a mechanism to detect unauthorized changes to the frozen SRS file.

**SRS v1.0 Baseline Checksum (Establishment Date: September 26, 2026):**

```
60d0b24476d1dff470babe1d138252ea2760e112926969fac8fbe22f35e7a46a  /home/vikaspal/Desktop/ml_chl/docs/SRS.md
```

**To Verify Baseline Integrity:**

Run the following command on the SRS file to regenerate the checksum:

```bash
sha256sum /home/vikaspal/Desktop/ml_chl/docs/SRS.md
```

If the output checksum **matches** the baseline checksum above:
- ✓ The baseline file has not been modified
- ✓ Baseline integrity is verified

If the output checksum **does not match** the baseline checksum:
- ✗ The file has been modified (either intentionally or unintentionally)
- ✗ Identify the changes using a diff tool: `diff SRS.md <previous-version>`
- ✗ If the modification was intentional, it must have been approved under the change-control procedure (Section 3)
- ✗ If the modification was unintentional, the file must be reverted to the baseline version

### 5.2 Integrity Checks

**Recommended Baseline Integrity Checks (to be performed periodically or before major milestones):**

1. **Checksum Verification:** Run checksum command to confirm file has not been modified
2. **Version History Audit:** Confirm SRS Section 1.2 (Version History) reflects all approved changes
3. **Requirement Traceability:** Spot-check that 10-20 random requirements can be traced to their source (design_freeze.md, problem_statement.md, or challenge rules)
4. **Frozen Requirement Count:** Confirm count of [FROZEN] requirements matches expected count (baseline: 47 [FROZEN] requirements)
5. **Approval Status Consistency:** Confirm SRS Section 1.3 (Document Status) shows "Approved – Final Version 1.0"

### 5.3 Change Detection

If unauthorized changes are detected:

1. **Stop implementation work** until the baseline status is resolved
2. **Identify the change** using version-control history (if available) or file comparison
3. **Determine the cause:** Accidental modification, unauthorized change, or approved change not recorded in change log
4. **Take corrective action:**
   - If accidental: Revert file to baseline checksum
   - If unauthorized: Reject the change and revert
   - If approved but not recorded: Update change log retroactively and document the approval gap

---

## 6. Release and Distribution

### 6.1 Baseline Distribution

**SRS v1.0 Baseline Distribution Date:** September 26, 2026

The frozen SRS is distributed to:

* **Technical Design Author** – for designing systems that satisfy requirements
* **Implementation Team** – for developing code that implements requirements
* **Test Team** – for designing tests that verify requirement compliance
* **Project Stakeholders** – for reviewing and approving the requirements
* **Project Archive** – for historical reference and compliance audits

### 6.2 Baseline Record Distribution

This Baseline Record (`SRS_BASELINE.md`) is distributed alongside the frozen SRS to:

* **Stakeholders:** Document the baseline status, change-control rules, and governance procedures
* **Technical Design / Implementation / Test:** Provide guidance on requirement change procedures
* **Project Archive:** Establish a formal record of baseline governance

---

## 7. Approval and Sign-Off

### 7.1 Baseline Establishment Approval

**Baseline Identifier:** `SRS-BL-1.0`  
**Frozen SRS Version:** 1.0  
**Baseline Establishment Date:** September 26, 2026

The SRS v1.0 baseline is formally established and is **APPROVED FOR USE** in:

* ✓ Technical Design development
* ✓ Implementation
* ✓ Testing and Verification
* ✓ Project Governance

---

## 8. Related Documents

| Document | Path | Purpose |
| --------- | ---- | --------- |
| **Software Requirements Specification** | `docs/SRS.md` | Authoritative requirements baseline (frozen) |
| **SRS Revision Summary** | `docs/SRS_REVISION_SUMMARY.md` | Documents changes from v0.1 → v1.0 and Design 1-6 incorporation |
| **SRS Reconciliation Report** | `docs/SRS_RECONCILIATION_REPORT.md` | Post-revision audit confirming 100% design coverage and approval |
| **Design Freeze Document** | `docs/design_freeze.md` | Authority for six frozen architectural decisions (Design 1-6) |
| **Problem Statement** | `docs/problem_statement.md` | Authority for official challenge requirements |
| **Knowledge Document** | `useful/knowledge.md` | Dataset facts and specifications |

---

**Baseline Record Version:** 1.0  
**Last Updated:** September 26, 2026  
**Next Review Date:** Upon first change request or at 90-day project milestone
