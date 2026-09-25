# 1. Document Control

## 1.1 Document Information

| Field                        | Details                                                                                                                     |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Document Title**           | Software Requirements Specification (SRS)                                                                                   |
| **Project**                  | Business Entity Resolution Challenge                                                                                        |
| **Document Type**            | Software Requirements Specification                                                                                         |
| **Document Version**         | 1.0                                                                                                                         |
| **Document Status**          | Approved – Final                                                                                                            |
| **Last Revision Date**       | 2026-09-26                                                                                                                  |
| **Primary Purpose**          | Define the complete software/system requirements for the entity-resolution solution, incorporating all frozen architectural decisions from design_freeze.md. |
| **Intended Audience**        | Project developers, AI coding agents, reviewers, testers, and project maintainers                                           |
| **Source of Requirements**   | Official challenge problem statement, challenge rules/constraints, dataset characteristics, and design_freeze.md approved decisions |
| **Implementation Reference** | This document is the authoritative requirements specification for implementation. Technical design decisions SHALL satisfy these requirements. |

---

## 1.2 Version History

| Version | Date       | Status    | Description                                                                                     |
| ------- | ---------- | --------- | ----------------------------------------------------------------------------------------------- |
| **0.1** | 2026-09-26 | Draft     | Initial SRS structure and document-control section created.                                     |
| **1.0** | 2026-09-26 | Approved  | Comprehensive revision incorporating all six frozen architectural decisions from design_freeze.md. |

#### Revision 1.0 Summary (2026-09-26)

Major revision to align SRS with approved frozen architectural decisions:
- Added Design 1 frozen requirements: six-method hybrid candidate-generation architecture with union semantics and retrieval provenance retention (FR-7.5.6 through FR-7.5.13, FR-7.6.6).
- Added Design 2 frozen requirements: six-group feature architecture with shared schema and Fellegi-Sunter principles (FR-7.8.6 through FR-7.8.15).
- Added Design 3 frozen requirements: LightGBM binary classifier, entity-level train/validation split, training data from generated candidates, validation-based threshold optimization, and final model retraining (FR-11.1.3 through FR-11.3.9, FR-11.4.1 through FR-11.4.4).
- Added Design 4 frozen requirements: single-workstation batch architecture with reusable indexes, disk-backed artifacts, checkpointing, and recovery (FR-12.1.3 through FR-12.1.14, FR-12.4.1 through FR-12.4.4).
- Added Design 5 frozen requirements: inference configuration validation, preprocessing consistency, feature schema consistency, candidate scoring, threshold application (FR-12.2.5 through FR-12.2.20).
- Added Design 6 frozen requirements: separate candidate-recall evaluation, controlled experimentation, validation discipline, error analysis (FR-11.6.1 through FR-11.6.7, FR-15.1.1 through FR-15.1.8).
- Added comprehensive artifact retention and reproducibility requirements.
- Clarified distinction between [FROZEN] architectural decisions and [EXPERIMENTAL] parameters subject to tuning.
- Updated section 11.2 to formalize validation discipline and data-leakage prevention per Design 6.

### Versioning Rules

The SRS shall use version numbers to distinguish between revisions.

* **Major version**: Used when fundamental requirements or system scope change.
* **Minor version**: Used when requirements are added, removed, or materially changed without changing the overall project purpose.
* **Patch/revision-level change**: Used for corrections, clarifications, formatting improvements, or other non-substantive changes.

Requirement changes shall be documented in the Version History and, where applicable, reflected in the Requirement Traceability Matrix.

---

## 1.3 Document Status

The current status of this document is:

> **APPROVED — FINAL VERSION 1.0**

This SRS has been comprehensively revised to incorporate all six frozen architectural decisions from `design_freeze.md` and has been approved for implementation and technical design.

The document satisfies the following completion criteria:

1. ✓ All official challenge requirements are represented.
2. ✓ All six frozen architectural decisions have been formalized as explicit requirements.
3. ✓ System behavior has been specified for all major functional areas.
4. ✓ Input and output requirements have been defined with precise schemas.
5. ✓ Evaluation requirements including candidate recall separate from model scoring have been documented.
6. ✓ Acceptance criteria have been established.
7. ✓ Requirements have been reviewed for consistency with official sources.
8. ✓ Clear distinction is made between frozen requirements [FROZEN] and experimental parameters [EXPERIMENTAL].
9. ✓ Traceability to source documents has been established throughout.

### Important Status Rule

The SRS defines **requirements**, not premature implementation decisions.

The SRS is intentionally separated from the Technical Design to avoid conflating requirements with implementation specifics. Specific implementation choices such as:
- Final normalization algorithms detail
- Specific candidate-generation tuning parameters
- Individual feature formulas and weights
- Model hyperparameters
- Exact storage formats

...shall be documented in **`TECHNICAL_DESIGN.md`** after sufficient dataset analysis and experimentation.

---

## 1.4 Purpose of This SRS

The purpose of this Software Requirements Specification is to provide a complete, unambiguous, and implementation-oriented specification of the software system required to solve the Business Entity Resolution Challenge.

The SRS translates the challenge's stated problem, rules, constraints, input/output requirements, and evaluation requirements into explicit requirements for the software solution.

The SRS shall define:

* what the system must accomplish;
* what data the system must accept;
* how input data must be validated and handled;
* what processing capabilities the system must provide;
* what entity-resolution functionality must be supported;
* what candidate-generation and matching capabilities are required;
* what training and validation capabilities are required;
* how the system must evaluate its own results;
* what output files must be generated;
* what submission-format requirements must be satisfied;
* what challenge constraints the implementation must obey;
* what quality, reliability, reproducibility, and performance requirements apply;
* how the completed system will be tested and accepted.

This document is also intended to act as the **primary requirements reference for the coding/implementation agent**.

The coding agent shall use this SRS to understand **what the implementation is required to do** and shall not independently introduce behavior that conflicts with the requirements specified here.

The SRS intentionally separates requirements from implementation-specific decisions. The exact algorithms, mathematical formulations, model architecture, feature definitions, hyperparameters, and code-level design decisions will be specified in `TECHNICAL_DESIGN.md` once they have been established through appropriate analysis and experimentation.

---

## 1.5 Relationship to Other Project Documents

This SRS is part of a set of project documents. Each document has a distinct purpose and shall not unnecessarily duplicate the responsibility of another document.

### 1.5.1 `problem_statement.md`

`problem_statement.md` contains the official challenge problem statement and serves as the primary reference for what the challenge organizers require.

It should be treated as the **source-of-truth representation of the original challenge statement**.

The SRS interprets and organizes those requirements into software/system requirements but shall not contradict the official problem statement.

---

### 1.5.2 `useful.md`

`useful.md` is the project's living knowledge base.

It records important information discovered during project development, including:

* dataset observations;
* observed noise patterns;
* data-quality findings;
* useful technical observations;
* experimental lessons;
* important warnings;
* assumptions;
* validated discoveries;
* decisions that should be remembered during implementation.

Information discovered during dataset analysis may first be recorded in `useful.md` and may subsequently result in updates to the SRS or Technical Design when the discovery affects a formal requirement or implementation decision.

---

### 1.5.3 `TECHNICAL_DESIGN.md`

`TECHNICAL_DESIGN.md` will define **how the requirements in this SRS will actually be implemented**.

It will contain the detailed implementation blueprint, including, where applicable:

* system architecture;
* pipeline architecture;
* data structures;
* preprocessing algorithms;
* normalization rules;
* candidate-generation algorithms;
* candidate-ranking methods;
* feature engineering;
* mathematical formulations;
* training-data construction;
* negative-sampling strategy;
* model selection;
* model architecture;
* training procedure;
* loss function;
* hyperparameters;
* threshold-selection procedure;
* evaluation implementation;
* post-processing;
* code/module architecture;
* runtime and complexity considerations;
* configuration;
* testing architecture;
* reproducibility mechanisms.

The Technical Design must satisfy the requirements established by this SRS.

---

### 1.5.4 Source Code

The source code is the executable implementation of the requirements specified by this SRS and the technical decisions specified by `TECHNICAL_DESIGN.md`.

The code shall not be considered the authority for requirements. If the implementation and the SRS disagree, the discrepancy must be identified and resolved rather than allowing undocumented behavior to become an implicit requirement.

---

### 1.5.5 Experiments

The `experiments/` area will contain experimental configurations, results, measurements, and experiment-specific observations.

Experiments are used to determine and validate technical decisions.

An experimental result may lead to an update in:

```text
experiments/
      ↓
useful.md
      ↓
TECHNICAL_DESIGN.md
```

and, when the result changes a formal system requirement:

```text
SRS.md
```

---

### 1.5.6 Tests

Tests provide evidence that the implemented system satisfies the requirements.

The relationship is:

```text
SRS
  ↓
Requirement
  ↓
Technical Design
  ↓
Implementation
  ↓
Test
  ↓
Evidence of Compliance
```

Requirements that can be objectively tested should have corresponding validation or test procedures where practical.

---

### 1.5.7 Document Authority and Conflict Resolution

The project documents shall generally be interpreted according to the following hierarchy:

```text
Official Challenge Requirements
        ↓
SRS
        ↓
Technical Design
        ↓
Implementation
        ↓
Experimental/Operational Artifacts
```

`problem_statement.md` represents the official challenge requirements.

The SRS converts those requirements into system requirements.

The Technical Design specifies how those requirements will be implemented.

The source code implements the approved design.

If a conflict is discovered, the conflict shall be explicitly identified and resolved rather than silently choosing one interpretation.

No implementation decision may override an explicit challenge constraint.


# 2. System Overview

## 2.1 Project Overview

The Business Entity Resolution Challenge is a data-matching project focused on identifying records that refer to the same real-world business across multiple data sources.

The system processes business records obtained from three sources: Source 1 (S1), Source 2 (S2), and Source 3 (S3). These records may contain differences in business names, addresses, formatting, and other attributes, even when they refer to the same business.

The project aims to develop a software system that can analyze these records, identify potential matches, determine which records represent the same business, and generate the required output files in the format specified by the challenge.

The system will be developed in accordance with the official challenge requirements, available datasets, evaluation criteria, and submission constraints.

## 2.2 System Purpose

The purpose of the system is to automate the identification and matching of business records across multiple data sources.

The system is intended to:

* Process business records from the provided datasets.
* Identify records that may refer to the same real-world business.
* Determine which candidate record pairs represent matching business entities.
* Handle variations and inconsistencies in the available business information.
* Generate the required matching results and candidate pair outputs.
* Produce outputs that comply with the challenge's submission requirements.

The system should reduce the need for manual record-by-record comparison while maintaining the matching quality required by the challenge's evaluation criteria.

## 2.3 Problem Being Solved

Business information collected from different sources may describe the same real-world business in different ways.

For example, a business may appear under slightly different names, use different address formats, or have incomplete or inconsistent information across sources. As a result, directly comparing records using exact string equality may fail to identify records that refer to the same business.

At the same time, different businesses may have similar names or addresses, making it difficult to determine whether two records refer to the same entity.

The system must therefore address two related challenges:

1. **Identifying potential matches:** Finding relevant record pairs across the available sources without unnecessarily comparing every possible pair.
2. **Determining actual matches:** Distinguishing records that represent the same business from records that refer to different businesses.

The system must perform these tasks while respecting the challenge's data, evaluation, and submission requirements.

The exact methods used to address these challenges will be defined in the Technical Design document after the dataset analysis and experimentation stages.

## 2.4 System Boundary

The system boundary defines the responsibilities of the Business Entity Resolution system and distinguishes them from activities performed outside the system.

### 2.4.1 In-Scope Activities

The system is responsible for:

* Reading the provided input datasets.
* Validating the input data and required fields.
* Processing business records for matching.
* Identifying potential matching record pairs.
* Evaluating candidate pairs to determine whether they represent the same business.
* Managing matching results according to the challenge's requirements.
* Generating the required output files.
* Validating the generated outputs against the submission requirements.
* Supporting training, validation, testing, and inference workflows as required by the challenge.

### 2.4.2 Out-of-Scope Activities

Unless explicitly required by the official challenge rules, the system does not include:

* Creating or collecting new business datasets independently.
* Manually verifying every predicted match.
* Modifying the original source datasets.
* Building a general-purpose business directory or business information management platform.
* Deploying a public-facing application or service.
* Accessing external data sources or services in ways prohibited by the challenge rules.

Any additional scope restrictions imposed by the official challenge statement will take precedence over this overview.

### 2.4.3 External Inputs and Outputs

The system interacts with the following external elements:

**Inputs:**

* Business records from the provided source datasets.
* Ground-truth data for training and evaluation, where permitted.
* Configuration and execution parameters required to run the system.

**Outputs:**

* `matching_results.tsv` containing the generated matching results.
* `candidate_pairs.tsv` containing the generated candidate record pairs.
* Supporting logs, evaluation results, and experiment artifacts used during development and validation.

The exact schemas and validation rules for these files are defined in the relevant requirements sections of this document.

## 2.5 High-Level System Workflow

At a high level, the system follows a pipeline that transforms the provided business records into validated matching outputs.

The workflow consists of the following stages:

1. **Input loading:** Read the provided business records and any permitted supporting data.
2. **Input validation:** Check the structure, required fields, and basic integrity of the input data.
3. **Data preparation:** Prepare the records for comparison while preserving the information required for matching.
4. **Candidate generation:** Identify record pairs that may refer to the same business.
5. **Candidate pair preparation:** Organize and validate the generated candidate pairs for further processing.
6. **Matching:** Evaluate candidate pairs and determine which pairs represent the same business entity.
7. **Result processing:** Organize the matching decisions and apply the result-handling requirements specified by the challenge.
8. **Output generation:** Produce the required matching results and candidate pair files.
9. **Output validation:** Verify that the generated files satisfy the challenge's format and consistency requirements.

The exact algorithms, data transformations, model architecture, and decision rules used at each stage will be specified in the Technical Design document.

### High-Level Workflow Diagram

```text
Provided Business Records
(S1, S2, S3)
        |
        v
  Input Loading
        |
        v
  Input Validation
        |
        v
  Data Preparation
        |
        v
 Candidate Generation
        |
        v
 Candidate Pair Preparation
        |
        v
     Matching
        |
        v
   Result Processing
        |
        v
   Output Generation
        |
        v
  Output Validation
        |
        v
Required Output Files
- matching_results.tsv
- candidate_pairs.tsv
```

This workflow represents the system's conceptual processing sequence. The detailed implementation and any additional stages will be documented in the Technical Design.


# 3. Scope

## 3.1 In-Scope Functionality

The scope of the Business Entity Resolution system includes the development of a software solution that identifies matching business records across the provided data sources and generates the required challenge outputs.

The following functionality is included within the scope of the project:

### 3.1.1 Data Processing

* Loading the provided business datasets from Source 1 (S1), Source 2 (S2), and Source 3 (S3).
* Validating input data structure, required fields, and basic data integrity.
* Preparing business records for comparison while preserving the information needed for matching.

### 3.1.2 Candidate Generation and Matching

* Identifying potential matching record pairs across the provided data sources.
* Evaluating candidate pairs to determine whether they refer to the same real-world business.
* Handling variations, inconsistencies, and missing information in business records.
* Managing matching decisions in accordance with the challenge requirements.

### 3.1.3 Training and Validation

* Using permitted training data and ground-truth information to develop and evaluate the matching solution.
* Supporting validation and experimentation to assess matching quality.
* Evaluating the solution using the challenge's specified evaluation criteria.

### 3.1.4 Output Generation and Validation

* Generating the required matching results file.
* Generating the required candidate pairs file.
* Validating the structure, contents, and consistency of the generated outputs.
* Supporting the preparation of the final challenge submission.

### 3.1.5 Development and Reproducibility

* Organizing the codebase into maintainable and testable modules.
* Maintaining configurations, experiment records, and documentation.
* Supporting repeatable execution of the training, validation, and inference workflows.

## 3.2 Out-of-Scope Functionality

The following activities are outside the intended scope of the project unless explicitly required by the official challenge specifications.

### 3.2.1 General-Purpose Business Information Management

* Building a general-purpose business directory or business information management platform.
* Maintaining or continuously updating business information after the challenge is completed.
* Providing a public-facing business search or discovery service.

### 3.2.2 Manual Record Verification

* Manually reviewing and confirming every predicted match.
* Building a human-in-the-loop review interface for resolving ambiguous matches.

### 3.2.3 Independent Data Collection

* Independently collecting additional business records from external sources.
* Modifying the original datasets to change their underlying business information.
* Introducing external information or data sources that are not permitted by the challenge rules.

### 3.2.4 Production Deployment

* Deploying the system as a public-facing application or commercial service.
* Building a production monitoring platform or long-term business data maintenance infrastructure.

### 3.2.5 Unrelated Functionality

* Implementing functionality unrelated to the identification of matching business entities and the generation of the required challenge outputs.

These exclusions describe the intended project scope and do not override any explicit requirement imposed by the official challenge specifications.

## 3.3 Challenge-Specific Boundaries

The system must operate within the boundaries established by the official challenge statement, dataset documentation, evaluation requirements, and submission instructions.

The following boundaries apply to the project:

### 3.3.1 Data Boundary

The system must use the datasets and supporting information made available for the challenge.

The use of additional data sources, external information, or supplementary datasets must comply with the official challenge rules.

### 3.3.2 Training and Evaluation Boundary

Training, validation, and testing activities must respect the permitted use of the available datasets and ground-truth information.

Information reserved for evaluation must not be used in a manner that violates the challenge's rules or compromises the validity of the evaluation.

### 3.3.3 Output Boundary

The system must generate the output files and data structures required by the challenge.

The output format, required fields, record relationships, and submission packaging must comply with the official specifications.

### 3.3.4 Technical and Computational Boundary

The system must comply with any restrictions imposed by the challenge concerning programming languages, dependencies, model usage, computational resources, runtime, and model size.

The specific restrictions applicable to the project must be documented using the official challenge requirements.

### 3.3.5 Evaluation Boundary

The system must be developed and evaluated according to the evaluation criteria defined by the challenge.

Internal validation results must be distinguished from official evaluation results.

### 3.3.6 Submission Boundary

The final submission must contain the required artifacts and follow the submission format, naming conventions, and delivery requirements specified by the challenge organizers.

The system must not depend on files, data, or services that are unavailable or prohibited in the official evaluation environment.

---

# 4. Stakeholders and System Users

This section identifies the individuals, tools, and external systems that interact with the project during development, execution, and evaluation.

The stakeholders and actors described here have different responsibilities. Some participate in the development process, while others provide inputs, evaluate outputs, or establish the challenge requirements.

## 4.1 Challenge Participant

**Role:** Project owner and challenge participant.

The challenge participant is responsible for developing, validating, and submitting the Business Entity Resolution solution.

### Responsibilities

* Understand the official challenge requirements and constraints.
* Define and maintain the project's requirements and technical documentation.
* Review dataset analysis findings and approve technical decisions.
* Guide the development process and use automation tools where appropriate.
* Review implementation results, experiments, and validation findings.
* Ensure that the final solution complies with the challenge rules.
* Prepare and submit the final deliverables.

The challenge participant retains responsibility for the final technical decisions and submission.

## 4.2 Coding/Automation Agent

**Role:** Development and automation assistant.

The coding/automation agent is an AI-assisted tool used during the development of the project. It helps carry out development tasks based on the project's requirements, technical design, and instructions.

### Responsibilities

* Analyze the provided datasets and identify relevant data characteristics.
* Assist in documenting observed data quality issues and noise patterns.
* Implement the system according to the approved requirements and technical design.
* Assist with code organization, testing, debugging, and validation.
* Run permitted experiments and report their results.
* Maintain relevant technical documentation and experiment records.
* Identify implementation issues, inconsistencies, and potential requirement violations.

### Limitations

* The agent must follow the official challenge constraints and approved project requirements.
* It must not independently change the project's requirements or make undocumented technical decisions.
* It must not use prohibited data sources or services.
* Its implementation and outputs must be validated before they are accepted as part of the final solution.

The coding/automation agent is a development-time actor. It is not necessarily part of the final system's runtime architecture.

## 4.3 Evaluation System

**Role:** External system responsible for evaluating the submitted solution.

The evaluation system represents the mechanism used by the challenge organizers to assess the submitted outputs against the applicable evaluation criteria.

### Responsibilities

* Receive or access the submitted deliverables in the required format.
* Validate the submission according to the challenge's evaluation procedures.
* Evaluate the matching results using the specified evaluation criteria.
* Produce evaluation results or scores according to the official evaluation process.

The exact evaluation procedures, metrics, and execution environment are determined by the official challenge specifications.

The evaluation system is external to the solution being developed and is not part of the project's implementation unless explicitly required.

## 4.4 Other Relevant Actors

### 4.4.1 Challenge Organizers

**Role:** Providers of the challenge requirements and evaluation framework.

The challenge organizers define the official problem statement, rules, constraints, dataset availability, evaluation criteria, and submission requirements.

Their published specifications serve as the authoritative source for challenge-specific requirements.

### 4.4.2 Dataset Provider

**Role:** Provider of the business records and associated data files.

The dataset provider makes the source datasets, training data, ground-truth information, and other permitted supporting data available for the challenge.

The system uses these materials as inputs according to the applicable data usage restrictions.

### 4.4.3 Development Environment

**Role:** Environment used to develop, execute, test, and validate the system.

The development environment provides the software runtime, libraries, storage, and computational resources required for project development and execution.

The environment must satisfy the technical and computational constraints applicable to the challenge.

### 4.4.4 External Evaluation Environment

**Role:** Environment in which the final submission is evaluated, where applicable.

The external evaluation environment executes or evaluates the submitted solution according to the challenge's procedures.

The solution must comply with any restrictions imposed by this environment, including available resources, dependencies, input access, and execution requirements.


# 5. Input Data Requirements

## 5.1 Dataset Structure

The system shall process the business entity resolution challenge datasets provided in the project directory.

The dataset is organized into separate training and test directories. Each directory contains three source-specific business record files. The training directory additionally contains a ground-truth file describing the matching relationships for the training records.

### 5.1.1 Training Dataset

The training dataset consists of the following files:

| File                     | Description                     | Data rows |
| ------------------------ | ------------------------------- | --------: |
| `train_source1.tsv`      | Source 1 training records       | 2,206,821 |
| `train_source2.tsv`      | Source 2 training records       | 5,034,616 |
| `train_source3.tsv`      | Source 3 training records       | 5,285,603 |
| `train_ground_truth.tsv` | Training matching relationships | 2,206,821 |

### 5.1.2 Test Dataset

The test dataset consists of the following files:

| File               | Description           | Data rows |
| ------------------ | --------------------- | --------: |
| `test_source1.tsv` | Source 1 test records | 1,732,544 |
| `test_source2.tsv` | Source 2 test records | 4,887,273 |
| `test_source3.tsv` | Source 3 test records | 5,082,316 |

The test dataset does not include a ground-truth file.

### 5.1.3 Dataset Organization

The expected dataset directory structure is:

```text
dataset/
├── train/
│   ├── train_source1.tsv
│   ├── train_source2.tsv
│   ├── train_source3.tsv
│   └── train_ground_truth.tsv
└── test/
    ├── test_source1.tsv
    ├── test_source2.tsv
    └── test_source3.tsv
```

The file paths above represent the dataset organization observed during the audit. The system shall support the configured dataset locations without requiring hard-coded absolute paths.

## 5.2 Source 1 Requirements

Source 1 is the deduplicated reference source for the entity resolution task.

The system shall use Source 1 records as the reference side of the matching process.

### 5.2.1 Input Files

* Training: `train_source1.tsv`
* Test: `test_source1.tsv`

### 5.2.2 Schema

Source 1 records shall contain the following fields:

| Field              | Type   | Description                                 |
| ------------------ | ------ | ------------------------------------------- |
| `entity_id`        | String | Unique identifier of the Source 1 record    |
| `business_name`    | String | Business name                               |
| `business_address` | String | Business address                            |
| `country`          | String | Country associated with the business record |

### 5.2.3 Record Identification

Source 1 record identifiers use the `S1-` prefix.

The system shall preserve the original record identifiers and use them to associate matching results with their corresponding reference records.

### 5.2.4 Reference Role

Each Source 1 record shall serve as the reference for identifying zero or more matching records from Source 2 and Source 3, according to the challenge's matching requirements.

## 5.3 Source 2 Requirements

Source 2 contains business records that may correspond to records in Source 1.

### 5.3.1 Input Files

* Training: `train_source2.tsv`
* Test: `test_source2.tsv`

### 5.3.2 Schema

Source 2 records shall contain the following fields:

| Field              | Type   | Description                                 |
| ------------------ | ------ | ------------------------------------------- |
| `entity_id`        | String | Unique identifier of the Source 2 record    |
| `business_name`    | String | Business name                               |
| `business_address` | String | Business address                            |
| `country`          | String | Country associated with the business record |

### 5.3.3 Record Identification

Source 2 record identifiers use the `S2-` prefix.

The system shall preserve the original identifiers and use them to identify Source 2 records in candidate pairs and matching results.

### 5.3.4 Matching Role

Source 2 records shall be eligible to match Source 1 reference records when the records represent the same real-world business.

The system shall not assume that every Source 2 record has a corresponding Source 1 match.

## 5.4 Source 3 Requirements

Source 3 contains business records that may correspond to records in Source 1.

### 5.4.1 Input Files

* Training: `train_source3.tsv`
* Test: `test_source3.tsv`

### 5.4.2 Schema

Source 3 records shall contain the following fields:

| Field              | Type   | Description                                 |
| ------------------ | ------ | ------------------------------------------- |
| `entity_id`        | String | Unique identifier of the Source 3 record    |
| `business_name`    | String | Business name                               |
| `business_address` | String | Business address                            |
| `country`          | String | Country associated with the business record |

### 5.4.3 Record Identification

Source 3 record identifiers use the `S3-` prefix.

The system shall preserve the original identifiers and use them to identify Source 3 records in candidate pairs and matching results.

### 5.4.4 Matching Role

Source 3 records shall be eligible to match Source 1 reference records when the records represent the same real-world business.

The system shall not assume that every Source 3 record has a corresponding Source 1 match.

## 5.5 Training Data

The training data consists of three source-specific business record files and one ground-truth file.

### 5.5.1 Training Source Records

The system shall load the training records from:

* `train_source1.tsv`
* `train_source2.tsv`
* `train_source3.tsv`

These files contain the business attributes used for developing and validating the matching solution.

### 5.5.2 Training Ground Truth

The system shall use `train_ground_truth.tsv` as the source of labeled matching relationships, subject to the challenge's data usage restrictions.

The ground-truth file maps each Source 1 reference record to zero or more matching records from Source 2 and Source 3.

### 5.5.3 Training Data Usage

The system shall support using the training records and their ground-truth relationships for model development, validation, and evaluation as permitted by the challenge.

The training data shall not be assumed to represent every possible data variation present in the test dataset.

## 5.6 Test Data

The test dataset contains unlabeled business records from Sources 1, 2, and 3.

### 5.6.1 Test Input Files

The system shall load the following test files:

* `test_source1.tsv`
* `test_source2.tsv`
* `test_source3.tsv`

### 5.6.2 Test Data Characteristics

The test source files follow the same observed four-field schema as the training source files.

The official challenge documentation states that the training data covers the United States and India, while the test data additionally includes France.

The `country` field shall therefore be treated as an open textual field rather than a fixed enumeration limited to the countries observed in training.

### 5.6.3 Test Data Usage

The system shall use the test records to generate matching results and candidate pairs according to the challenge requirements.

The system shall not assume that test ground-truth labels are available.

The system shall preserve the identifiers of the test records and generate outputs that reference the appropriate test records.

## 5.7 Ground Truth

The training ground-truth file provides the labeled matching relationships used to develop and validate the entity resolution system.

### 5.7.1 Ground-Truth File

File: `train_ground_truth.tsv`

The file contains the following fields:

| Field                | Type   | Description                                                               |
| -------------------- | ------ | ------------------------------------------------------------------------- |
| `source1_entity_id`  | String | Identifier of the Source 1 reference record                               |
| `matched_entity_ids` | String | Comma-separated list of matching Source 2 and Source 3 record identifiers |

### 5.7.2 Ground-Truth Representation

Each ground-truth row represents the matching relationship for one Source 1 reference record.

The `source1_entity_id` field identifies the reference record.

The `matched_entity_ids` field contains zero or more matching record identifiers from Source 2 and Source 3.

An empty match list represents a Source 1 record with no matching records in the other sources.

A non-empty match list may contain one or multiple matching record identifiers.

### 5.7.3 Ground-Truth Integrity

The system shall validate the ground-truth structure and check that:

* Each reference identifier corresponds to a valid Source 1 training record.
* Each matched identifier corresponds to a valid Source 2 or Source 3 training record.
* Match identifiers use the expected source-specific prefixes.
* The matching relationships follow the official challenge's ground-truth representation.

Any invalid or ambiguous references shall be reported rather than silently accepted.

## 5.8 Data Formats

### 5.8.1 File Format

The source datasets and training ground-truth file use tab-separated values (TSV) format.

The expected file extension is `.tsv`.

The system shall parse the files using tab characters as field separators.

### 5.8.2 Text Encoding

The files appear to use UTF-8 encoding based on the dataset audit.

The system shall support UTF-8 text, including multilingual business names and address values.

### 5.8.3 Header and Column Names

The observed source files contain a header row with the following fields:

`entity_id`, `business_name`, `business_address`, `country`

The ground-truth file contains a header row with:

`source1_entity_id`, `matched_entity_ids`

The system shall validate the presence of the expected headers before processing the files.

### 5.8.4 Identifier and Match-List Representation

Record identifiers shall be handled as strings to preserve their original representation.

The `matched_entity_ids` field shall be interpreted as a comma-separated list of record identifiers, with the tab character serving as the field delimiter for the ground-truth file.

The system shall not interpret commas within business names or addresses as TSV field separators.

## 5.9 Required Fields

### 5.9.1 Required Source Fields

The following fields are required by the observed source schema and official dataset documentation:

| Field              | Requirement                               |
| ------------------ | ----------------------------------------- |
| `entity_id`        | Required; must identify the source record |
| `business_name`    | Required source field                     |
| `business_address` | Required source field                     |
| `country`          | Required source field                     |

These fields shall be present in each source file.

The presence of a field does not guarantee that every record contains a meaningful value. Missing and blank values shall be detected through data validation.

### 5.9.2 Required Ground-Truth Fields

The ground-truth file shall contain:

* `source1_entity_id`
* `matched_entity_ids`

The first field identifies the reference record, and the second field represents its matching record identifiers.

### 5.9.3 Source Identification

The system shall identify records according to their source-specific identifier prefixes:

* `S1-` for Source 1
* `S2-` for Source 2
* `S3-` for Source 3

The source identity shall also be consistent with the file from which the record was loaded.

The system shall not require an additional `source` column in the input files.

## 5.10 Data Integrity Requirements

The system shall validate the input datasets before using them in training, validation, or inference.

### 5.10.1 File Integrity

The system shall:

* Verify that all required input files are available.
* Verify that files can be read using the expected format and encoding.
* Verify that required columns are present.
* Detect malformed rows and unexpected column counts.
* Report files that do not conform to the expected schema.

### 5.10.2 Identifier Integrity

The system shall:

* Verify that record identifiers are present and non-empty.
* Validate identifier prefixes against the expected source.
* Detect duplicate identifiers within each source dataset.
* Verify that identifiers referenced by ground truth exist in the appropriate source datasets.
* Preserve original identifiers without unintended modification.

### 5.10.3 Field Integrity

The system shall:

* Detect missing or blank values in required fields.
* Report unexpected data types or malformed values.
* Preserve multilingual text and original source information during input loading.
* Distinguish missing values from valid non-empty text values.

The exact treatment of missing values during preprocessing shall be specified in the Technical Design.

### 5.10.4 Ground-Truth Integrity

The system shall:

* Verify that ground-truth reference IDs correspond to Source 1 training records.
* Verify that matched IDs correspond to Source 2 or Source 3 training records.
* Detect malformed match lists and invalid identifiers.
* Detect duplicate identifiers within a match list.
* Report inconsistencies between ground-truth relationships and the source datasets.

### 5.10.5 Dataset Consistency

The system shall verify that:

* The training and test source files conform to their expected schemas.
* Source identity is consistent with the identifier prefix and file membership.
* Ground-truth references use the appropriate source identifiers.
* Data inconsistencies are reported before they can silently affect matching results.

### 5.10.6 Validation Reporting

The system shall produce a validation report that records:

* Files inspected.
* Record counts.
* Schema validation results.
* Missing-value statistics.
* Duplicate identifier statistics.
* Invalid or unresolved ground-truth references.
* Other detected data integrity issues.

The validation report shall distinguish between confirmed data errors, warnings, and conditions that require further investigation.

The actual data-quality statistics shall be established by running the validation process against the complete datasets. The audit findings shall not be interpreted as proof that every input file is free from integrity issues.


# 6. Output Requirements

This section defines the required output files, their schemas, record coverage, identifier validity, duplicate handling, empty-match representation, consistency expectations, and validation requirements.

The system shall generate two tab-separated output files:

1. `output/matching_results.tsv`
2. `output/candidate_pairs.tsv`

Both files shall conform to the official challenge format and cover every Source 1 entity in the test dataset.

## 6.1 matching_results.tsv

### 6.1.1 Purpose

The `matching_results.tsv` file shall contain the final matching results produced by the system for the test Source 1 entities.

### 6.1.2 File Format

* **File name:** `matching_results.tsv`
* **Location:** `output/matching_results.tsv`
* **Format:** Tab-separated values (TSV)
* **Encoding:** UTF-8
* **Header:** Required, with exact column names and order.

### 6.1.3 Schema

| Column Name          | Description                                                                |
| -------------------- | -------------------------------------------------------------------------- |
| `source1_entity_id`  | Entity ID of the Source 1 record being matched.                            |
| `matched_entity_ids` | Comma-separated list of matching entity IDs from Source 2 and/or Source 3. |

The header shall be exactly:

`source1_entity_id    matched_entity_ids`

The separator between the two columns shall be a tab character.

### 6.1.4 Record Requirements

* Every Source 1 entity in `test_source1.tsv` shall have exactly one row.
* A Source 1 entity may have zero, one, or multiple matching entity IDs.
* The `matched_entity_ids` field shall contain only Source 2 and/or Source 3 entity IDs.
* Source 1 self-matches shall not be permitted.
* The row order shall preserve the original order of Source 1 entities in `test_source1.tsv`.

## 6.2 candidate_pairs.tsv

### 6.2.1 Purpose

The `candidate_pairs.tsv` file shall contain the candidate entity IDs generated for each Source 1 entity before final matching decisions are made.

It shall represent the candidate set produced by the candidate-generation stage and supplied to the matching model for inference.

### 6.2.2 File Format

* **File name:** `candidate_pairs.tsv`
* **Location:** `output/candidate_pairs.tsv`
* **Format:** Tab-separated values (TSV)
* **Encoding:** UTF-8
* **Header:** Required, with exact column names and order.

### 6.2.3 Schema

| Column Name            | Description                                                                 |
| ---------------------- | --------------------------------------------------------------------------- |
| `source1_entity_id`    | Entity ID of the Source 1 record for which candidates are generated.        |
| `candidate_entity_ids` | Comma-separated list of candidate entity IDs from Source 2 and/or Source 3. |

The header shall be exactly:

`source1_entity_id    candidate_entity_ids`

The separator between the two columns shall be a tab character.

### 6.2.4 Record Requirements

* Every Source 1 entity in `test_source1.tsv` shall have exactly one row.
* Candidate IDs shall be drawn only from Source 2 and/or Source 3.
* The `candidate_entity_ids` field shall contain a comma-separated list of candidate IDs.
* An empty candidate list shall represent a Source 1 entity for which no candidates were generated.
* The row order shall preserve the original order of Source 1 entities in `test_source1.tsv`.

## 6.3 Required Output Records

The system shall satisfy the following record-coverage requirements:

1. Every Source 1 entity in the test dataset shall appear exactly once in `matching_results.tsv`.
2. Every Source 1 entity in the test dataset shall appear exactly once in `candidate_pairs.tsv`.
3. Both output files shall cover the same set of test Source 1 entity IDs.
4. Each Source 1 entity shall support the following possible matching outcomes:

   * **Zero matches:** No matching entity IDs.
   * **One match:** A single matching entity ID.
   * **Multiple matches:** Two or more matching entity IDs.
5. The output row order shall follow the original order of Source 1 records in `test_source1.tsv`.

## 6.4 ID Validity Requirements

### 6.4.1 Source Identification

Entity IDs shall identify their corresponding source through their prefixes:

| Prefix | Source   |
| ------ | -------- |
| `S1-`  | Source 1 |
| `S2-`  | Source 2 |
| `S3-`  | Source 3 |

### 6.4.2 Identifier Constraints

* The `source1_entity_id` field shall contain valid Source 1 entity IDs from the test dataset.
* The `matched_entity_ids` field shall contain only Source 2 and/or Source 3 entity IDs.
* The `candidate_entity_ids` field shall contain only Source 2 and/or Source 3 entity IDs.
* Source 1 IDs shall not appear as matching or candidate IDs.
* IDs referenced in the output should correspond to entities in the respective test source files.
* Invalid source prefixes and IDs that do not belong to the permitted source categories shall be rejected by validation.

The exact numeric width or padding convention of entity IDs is not formally specified beyond the source prefixes and examples provided by the challenge.

## 6.5 Duplicate Handling

The system shall prevent duplicate records and repeated IDs within the output files.

The following constraints shall apply:

1. A `source1_entity_id` shall appear exactly once in each output file.
2. An entity ID shall not be repeated within a single `matched_entity_ids` list.
3. An entity ID shall not be repeated within a single `candidate_entity_ids` list.
4. Duplicate Source 1 rows and duplicate IDs within an individual list shall be treated as invalid output.
5. The same Source 2 or Source 3 entity ID may appear in lists associated with different Source 1 entities, as no prohibition on such reuse is specified by the challenge.

## 6.6 Empty Match Handling

### 6.6.1 Empty Final Match List

When a Source 1 entity has no matching entities:

* Its row shall still be present in `matching_results.tsv`.
* The `matched_entity_ids` field shall be left empty.
* No placeholder such as `NA`, `NULL`, or `[]` shall be used.
* An empty list shall represent a singleton Source 1 entity with no matches.

### 6.6.2 Empty Candidate List

When no candidates are generated for a Source 1 entity:

* Its row shall still be present in `candidate_pairs.tsv`.
* The `candidate_entity_ids` field shall be left empty.
* No placeholder such as `NA`, `NULL`, or `[]` shall be used.

An empty candidate list indicates that the candidate-generation stage did not produce any candidates for that entity.

## 6.7 Candidate/Match Consistency

The candidate-generation stage shall produce the candidate set considered by the final matching stage.

The intended relationship is that final matches should be drawn from the candidate set generated for the corresponding Source 1 entity.

The following consistency expectations shall apply:

1. Final matched IDs should be present in the corresponding `candidate_entity_ids` list.
2. Candidate lists may contain IDs that are not included in the final matching results.
3. Candidate–match consistency shall be treated as an advisory validation check rather than a strict output acceptance requirement.
4. If a final matched ID is absent from the corresponding candidate list, the system should report the inconsistency as a warning for investigation.

The challenge validator treats missing candidate coverage as a warning rather than a hard validation failure.

## 6.8 Output Validation

Before submission, the system shall validate the generated output files against the official challenge requirements.

### 6.8.1 File-Level Validation

The system shall verify that:

* Both required output files exist in the `output/` directory.
* Both files use the TSV format.
* Both files contain the exact required headers in the correct order.
* Both files contain the expected number of columns.

### 6.8.2 Record-Level Validation

The system shall verify that:

* Every test Source 1 entity appears exactly once in each output file.
* No required Source 1 entity is missing.
* No extra Source 1 entity is included.
* No duplicate Source 1 rows exist.
* No repeated IDs occur within a single match or candidate list.
* No Source 1 IDs appear in match or candidate lists.
* Only permitted Source 2 and Source 3 identifiers appear in those lists.

### 6.8.3 Cross-File Validation

The system shall verify that:

* Both output files cover the same set of Source 1 entity IDs.
* The row ordering in both files follows the original order of Source 1 entities in the test dataset.
* Candidate–match consistency is checked and any violations are reported as warnings.

### 6.8.4 Identifier Existence Validation

The system should support an optional identifier-existence check to verify that referenced Source 2 and Source 3 IDs exist in the corresponding test source files.

The official validator provides an optional `--check-ids` mode for this purpose. The check is not enabled by default because it can require substantial memory.

### 6.8.5 Submission Requirements

The final submission package shall include both files:

* `output/matching_results.tsv`
* `output/candidate_pairs.tsv`

The output files shall conform to the official challenge schema and validation constraints. Submissions that fail the required validation checks shall not be evaluated.


# 7. Functional Requirements

This section defines the functional capabilities and behaviors required of the business entity matching system. It describes the processing stages from input data loading through matching, result processing, output generation, and submission validation.

The system shall process business records from Source 1, Source 2, and Source 3 to identify records that refer to the same real-world business. It shall support zero, one, or multiple matches for each Source 1 entity.

The specific algorithms, data structures, normalization methods, feature set, and model architecture shall be defined separately in the Technical Design document.

## 7.1 Data Loading

**FR-7.1.1** The system shall load the provided training datasets from the following files:

* `dataset/train/train_source1.tsv`
* `dataset/train/train_source2.tsv`
* `dataset/train/train_source3.tsv`
* `dataset/train/train_ground_truth.tsv`

**FR-7.1.2** The system shall load the provided test datasets from the following files:

* `dataset/test/test_source1.tsv`
* `dataset/test/test_source2.tsv`
* `dataset/test/test_source3.tsv`

**FR-7.1.3** The system shall interpret the input files as tab-separated values (TSV) and preserve the original entity identifiers.

**FR-7.1.4** The system shall identify each record's source using the source dataset and the corresponding entity ID prefix.

**FR-7.1.5** The system shall load the training ground-truth relationships for model development and evaluation in accordance with the challenge requirements.

**FR-7.1.6** The system shall support processing the provided datasets at their full scale without requiring changes to the official input file formats.

## 7.2 Data Validation

**FR-7.2.1** The system shall verify that all required input files exist and are readable before processing begins.

**FR-7.2.2** The system shall validate that each input file contains the required columns and conforms to its expected schema.

**FR-7.2.3** The system shall validate entity identifiers for missing values, duplicates, and source-prefix consistency.

**FR-7.2.4** The system shall identify missing, malformed, or invalid values in the input records.

**FR-7.2.5** The system shall validate the integrity of the training ground-truth references against the corresponding source datasets.

**FR-7.2.6** The system shall report detected data-integrity issues and distinguish confirmed errors from warnings or issues requiring further investigation.

**FR-7.2.7** The system shall prevent invalid input data from being silently treated as valid matching evidence.

## 7.3 Data Preprocessing

**FR-7.3.1** The system shall prepare business records for comparison while preserving the original entity identifiers and source-record relationships.

**FR-7.3.2** The system shall accommodate variations in business names and addresses, including punctuation differences, abbreviations, legal suffix variations, transliterations, and incomplete address information.

**FR-7.3.3** The system shall handle missing or malformed business attributes without treating missing information as evidence of a match.

**FR-7.3.4** The system shall preserve the information necessary for subsequent candidate generation, feature generation, and matching.

**FR-7.3.5** The specific preprocessing sequence and transformation methods shall be defined in the Technical Design document.

## 7.4 Normalization

**FR-7.4.1** The system shall support the preparation of business names, addresses, and country values for comparison across the three sources.

**FR-7.4.2** The system shall accommodate variations in text formatting, abbreviations, punctuation, and language representation when comparing business records.

**FR-7.4.3** The system shall treat country as an open textual attribute and shall not restrict processing to only the countries present in the training dataset.

**FR-7.4.4** The system shall preserve the original business attributes so that normalized representations do not replace the source data.

**FR-7.4.5** The specific normalization rules, canonicalization methods, and language-specific transformations shall be defined in the Technical Design document.

## 7.5 Candidate Generation

### 7.5.1 Overall Candidate Generation Requirements

**FR-7.5.1** The system shall generate a set of candidate Source 2 and Source 3 records for each Source 1 entity.

**FR-7.5.2** The candidate-generation stage shall reduce the search space by selecting plausible matching records instead of requiring exhaustive comparison against all records in the target sources.

**FR-7.5.3** The system shall seek to retain potential true matches while controlling the number of candidates generated for each Source 1 entity.

**FR-7.5.4** Candidate generation shall support matching against both Source 2 and Source 3.

**FR-7.5.5** The system shall retain the candidate set produced for each Source 1 entity for use by the matching stage and subsequent output generation.

### 7.5.2 Frozen Hybrid Multi-Method Architecture **[FROZEN]**

**FR-7.5.6** **[FROZEN per Design 1.3]** The system shall implement candidate generation using a hybrid architecture consisting of exactly six independently executed retrieval method families:

1. **Exact and normalized-name blocking:** Retrieve target records whose business names exactly match or match after agreed normalization (case, punctuation, whitespace, legal-suffix formatting).
2. **Token-based name retrieval:** Retrieve candidates using tokens present in business names, recovering records where tokens are reordered, partially overlapping, or vary in formatting.
3. **Character n-gram and fuzzy-name retrieval:** Retrieve candidates using character-level representations and approximate name similarity, handling spelling variations, abbreviations, and minor character differences.
4. **Address-based retrieval:** Retrieve candidates using business-address evidence independently of name-based retrieval, including exact normalized-address matching, address-token matching, and fuzzy address similarity.
5. **Country-aware retrieval:** Use country information as contextual evidence to organize indexes, prioritize search spaces, or refine retrieval behavior, without imposing universal hard country-equality filters.
6. **Embedding-based nearest-neighbor retrieval:** Use semantic or learned vector representations to retrieve records close in embedding space, supplementing lexical and token-based methods.

**FR-7.5.7** **[FROZEN per Design 1.3]** Each retrieval method shall be executed independently. The results of all configured methods shall be combined using union semantics and deduplicated by candidate entity ID.

**FR-7.5.8** **[FROZEN per Design 1.5]** If a candidate is retrieved by multiple retrieval methods, it shall appear only once in the unified candidate set, but its retrieval provenance shall record all applicable methods.

**FR-7.5.9** **[FROZEN per Design 1.3]** The architecture is frozen at the method-family level. Exact algorithms, normalization rules, indexes, retrieval limits, ranking methods, and method-specific parameters remain subject to experimental tuning and shall be documented in `TECHNICAL_DESIGN.md`.

### 7.5.3 Candidate Filtering Rules **[FROZEN]**

**FR-7.5.10** **[FROZEN per Design 1.6]** The following candidate-selection and filtering rules are mandatory:

* Candidates must come exclusively from Source 2 or Source 3.
* Candidates must be associated with the relevant S1 entity.
* Candidate IDs must be unique within each S1 entity's candidate list.
* A candidate retrieved by any configured retrieval method is eligible for inclusion in the unified candidate set.
* **No universal hard country-equality filter shall be applied.** A candidate shall not be rejected solely because its country differs from the reference entity's country.
* **Candidates shall not be rejected solely because name and address evidence disagree.** Candidates with high name similarity but weaker address similarity, or vice versa, must not be automatically discarded.
* No arbitrary global candidate cap shall be imposed. Retrieval limits and candidate budgets may be introduced and tuned as explicit configurable parameters subject to measurement.

**FR-7.5.11** **[FROZEN per Design 1.6]** Candidate generation shall not use ground-truth match labels to inject known positive candidates during training or inference.

### 7.5.4 Training and Inference Consistency **[FROZEN]**

**FR-7.5.12** **[FROZEN per Design 1.7]** Candidate generation shall use the same configured retrieval architecture during training and inference. The following must remain consistent:
* Normalization rules.
* Retrieval method definitions.
* Indexing and query conventions.
* Method-specific retrieval configuration.
* Candidate deduplication and provenance handling.
* Candidate output semantics.

**FR-7.5.13** **[FROZEN per Design 1.7]** Training candidate generation must not inject ground-truth matches into the candidate set. A genuine match that is absent from the generated candidates must be recorded as a candidate-generation miss rather than silently repaired using ground-truth information.

## 7.6 Candidate Management

**FR-7.6.1** The system shall associate each candidate record with the corresponding Source 1 entity.

**FR-7.6.2** The system shall ensure that candidate records originate only from Source 2 and Source 3.

**FR-7.6.3** The system shall prevent duplicate candidate identifiers within the candidate list of a given Source 1 entity.

**FR-7.6.4** The system shall support Source 1 entities for which candidate generation produces an empty candidate list.

**FR-7.6.5** The system shall retain sufficient candidate information to support matching, result processing, and generation of `candidate_pairs.tsv`.

**FR-7.6.6** **[FROZEN per Design 1.2 and 1.5]** The system shall retain retrieval provenance indicating which retrieval methods retrieved each candidate. When multiple methods retrieve the same candidate, the provenance shall record all applicable methods. Retrieval scores or method-specific evidence shall be preserved where applicable for use in downstream feature extraction and model scoring.

**FR-7.6.7** The internal candidate-management representation and provenance tracking details shall be defined in the Technical Design document.

## 7.7 Candidate Pair Construction

**FR-7.7.1** The system shall construct candidate relationships between Source 1 entities and their associated Source 2 and Source 3 candidates.

**FR-7.7.2** Each candidate relationship shall identify the Source 1 entity and the corresponding candidate entity.

**FR-7.7.3** The system shall ensure that candidate relationships do not represent Source 1 self-matches.

**FR-7.7.4** The system shall make the constructed candidate relationships available to the matching stage.

**FR-7.7.5** The system shall support conversion of the internal candidate representation into the required per-Source-1 candidate lists for `candidate_pairs.tsv`.

**FR-7.7.6** The internal representation and construction method for candidate relationships shall be defined in the Technical Design document.

## 7.8 Feature Generation

### 7.8.1 General Feature Generation Requirements

**FR-7.8.1** The system shall generate comparison information for candidate relationships to support the matching decision.

**FR-7.8.2** The comparison information shall support the evaluation of business-name and address similarity and other relevant attributes available in the input records.

**FR-7.8.3** The system shall support the use of country information as contextual evidence when comparing candidate records.

**FR-7.8.4** The system shall handle missing or unavailable attributes during feature generation without treating missing values as positive match evidence.

**FR-7.8.5** The feature-generation process shall produce information suitable for the selected matching method.

### 7.8.2 Frozen Six-Group Feature Architecture **[FROZEN]**

**FR-7.8.6** **[FROZEN per Design 2.3]** The system shall organize pairwise features into six groups:

1. **Business-name features:** Similarity measures, token-based comparisons, and matching statistics derived from the `business_name` fields.
2. **Address features:** Similarity measures, token-based comparisons, component-level matching, and statistics derived from the `business_address` fields.
3. **Country and geographic features:** Comparison of country values, geographic-proximity indicators, and country-based contextual evidence.
4. **Cross-field interaction features:** Features capturing relationships among multiple fields, such as name-address agreement or name-address disagreement patterns.
5. **Candidate-generation evidence features:** Features representing which retrieval methods retrieved each candidate and their associated retrieval scores or confidence values.
6. **Data-quality and context features:** Features capturing data completeness, field reliability, potential data-quality issues, and contextual information about the candidate pair.

**FR-7.8.7** **[FROZEN per Design 2.3]** Feature extraction shall draw on Fellegi–Sunter record-linkage principles, representing agreement, disagreement, and missing information distinctly rather than conflating them.

### 7.8.3 Shared Feature Schema **[FROZEN]**

**FR-7.8.8** **[FROZEN per Design 2.10]** A single shared feature schema shall be used for all candidate pairs, including both S1-S2 and S1-S3 pairs. Feature names, ordering, data types, and numerical representations shall be consistent across all pairs.

**FR-7.8.9** **[FROZEN per Design 2.10]** The feature schema shall include a source-pair indicator identifying whether each pair is an S1-S2 or S1-S3 comparison.

**FR-7.8.10** **[FROZEN per Design 2.11]** The feature schema shall distinguish among: (1) agreement between available values, (2) disagreement between available values, (3) missing or unavailable information, and (4) evidence that cannot be reliably compared. Missing values shall not be treated as equivalent to disagreement.

### 7.8.4 Candidate-Generation Evidence in Features **[FROZEN]**

**FR-7.8.11** **[FROZEN per Design 2.8]** The feature schema shall include features representing candidate-generation evidence, including which retrieval methods retrieved each candidate and their associated retrieval scores or confidence values. These features shall help the downstream model distinguish candidates retrieved through different evidence sources.

### 7.8.5 Feature Schema Versioning

**FR-7.8.12** The feature schema shall be versioned and explicitly documented.

**FR-7.8.13** Any change to feature definitions, preprocessing, normalization, or ordering that affects model inputs shall require a new schema version.

**FR-7.8.14** The trained model shall be associated with the feature-schema version used during training. Inference shall use the exact feature schema corresponding to the trained model.

**FR-7.8.15** The exact feature set, individual feature formulas, numerical representations, and implementation details shall be defined in the Technical Design document.

## 7.9 Matching

**FR-7.9.1** The system shall evaluate candidate relationships to determine whether the corresponding records refer to the same real-world business.

**FR-7.9.2** The matching stage shall use the comparison information generated for candidate relationships.

**FR-7.9.3** The system shall support matching Source 1 entities against candidates from both Source 2 and Source 3.

**FR-7.9.4** The matching process shall support zero, one, or multiple accepted matches for each Source 1 entity.

**FR-7.9.5** The matching process shall account for the possibility of noisy, incomplete, and inconsistent business attributes.

**FR-7.9.6** **[FROZEN per Design 3.2]** The matching model shall be a binary classifier that estimates the likelihood that a candidate pair represents the same real-world business. Each scoring example shall consist of a candidate pair and its extracted features, producing a probability or confidence score.

**FR-7.9.7** The matching algorithm, model architecture, and detailed scoring method shall be defined in the Technical Design document.

## 7.10 Match Decision

**FR-7.10.1** The system shall convert matching-stage outputs into final accepted match relationships.

**FR-7.10.2** The system shall permit a Source 1 entity to have zero, one, or multiple accepted matching entity IDs.

**FR-7.10.3** The system shall ensure that accepted match identifiers belong only to Source 2 or Source 3.

**FR-7.10.4** The system shall support leaving the final match list empty when no candidate is accepted as a match.

**FR-7.10.5** The system shall support the use of a decision rule that distinguishes accepted matches from rejected candidates.

**FR-7.10.6** The decision thresholds, confidence rules, and match-acceptance policy shall be defined in the Technical Design document.

## 7.11 Multiple-Match Handling

**FR-7.11.1** The system shall support multiple accepted matching records for a single Source 1 entity.

**FR-7.11.2** The system shall allow accepted matches to originate from Source 2, Source 3, or both sources for the same Source 1 entity.

**FR-7.11.3** The system shall retain all accepted matching entity IDs associated with a Source 1 entity.

**FR-7.11.4** The system shall prevent duplicate matching entity IDs within the final match list for a given Source 1 entity.

**FR-7.11.5** The system shall not impose a one-to-one matching restriction that prevents valid multiple-match relationships.

## 7.12 No-Match/Singleton Handling

**FR-7.12.1** The system shall support Source 1 entities for which no matching records exist in Source 2 or Source 3.

**FR-7.12.2** The system shall represent an entity with no accepted matches using an empty final match list.

**FR-7.12.3** The system shall retain every Source 1 entity in the final output, including entities with no accepted matches.

**FR-7.12.4** The system shall distinguish between an empty candidate list and a non-empty candidate list for which no candidate is accepted as a match.

**FR-7.12.5** The system shall support singleton handling as part of the final matching decision without requiring every Source 1 entity to have a positive match.

## 7.13 Post-Processing

**FR-7.13.1** The system shall process accepted matching relationships before generating the final output files.

**FR-7.13.2** The system shall remove or prevent duplicate matching entity IDs within each Source 1 entity's final match list.

**FR-7.13.3** The system shall ensure that final match identifiers conform to the permitted source categories.

**FR-7.13.4** The system shall check candidate–match consistency and report cases in which a final matched ID is absent from the corresponding candidate list as warnings.

**FR-7.13.5** The system shall preserve the association between each Source 1 entity and its final matching entity IDs.

**FR-7.13.6** The system shall prepare the processed candidate and matching relationships for output generation.

## 7.14 Output Generation

**FR-7.14.1** The system shall generate the final matching results file at `output/matching_results.tsv`.

**FR-7.14.2** The system shall generate the candidate-pair output file at `output/candidate_pairs.tsv`.

**FR-7.14.3** The system shall conform to the exact file schemas and output requirements defined in Section 6 of this SRS.

**FR-7.14.4** The system shall generate exactly one row for every Source 1 entity in the test dataset in each output file.

**FR-7.14.5** The system shall preserve the original order of Source 1 entities from `test_source1.tsv` in both output files.

**FR-7.14.6** The system shall represent candidate IDs and final matched IDs as comma-separated lists in their respective output fields.

**FR-7.14.7** The system shall represent empty candidate and final match lists using empty fields, without placeholder values.

**FR-7.14.8** The system shall generate both files in the required TSV format with the exact headers and column order defined in Section 6.

## 7.15 Submission Validation

**FR-7.15.1** The system shall validate the generated output files before submission using the official challenge validator.

**FR-7.15.2** The system shall verify the existence of both required output files and their compliance with the official file format and schema.

**FR-7.15.3** The system shall validate that every test Source 1 entity appears exactly once in each output file.

**FR-7.15.4** The system shall validate that no extra Source 1 entities or duplicate Source 1 rows are present.

**FR-7.15.5** The system shall validate that matching and candidate lists contain no duplicate IDs and no Source 1 self-matches.

**FR-7.15.6** The system shall validate that match and candidate identifiers use the permitted Source 2 and Source 3 prefixes.

**FR-7.15.7** The system shall support optional identifier-existence validation against the corresponding test source files.

**FR-7.15.8** The system shall report candidate–match consistency violations as warnings rather than treating them as mandatory submission-blocking failures.

**FR-7.15.9** The system shall identify validation failures that must be corrected before submission.

**FR-7.15.10** The final submission package shall include both required output files in the `output/` directory and conform to the official submission requirements.


# 8. Entity Resolution Requirements

This section defines the entities, records, matching relationships, and valid match outcomes handled by the entity resolution system. It establishes the meaning of a match independently of the technical methods used to identify one.

## 8.1 Entity Definition

An **entity** represents a real-world business whose identity may be represented by records in one or more data sources.

The system shall treat Source 1 as the reference set of business entities and identify records from Source 2 and Source 3 that refer to the same real-world business.

The entity concept refers to business identity, while a record represents a source-specific representation of that business.

The challenge does not provide a formal legal-identity definition or a complete set of rules for determining business identity.

## 8.2 Record Definition

A **record** is a source-specific representation of a business in one of the three provided data sources.

Each record contains the following fields:

* `entity_id`: Unique identifier used to identify the record within its source.
* `business_name`: Name of the business.
* `business_address`: Address associated with the business.
* `country`: Country associated with the business.

The source is identified through the record's source file and ID prefix.

The three sources have the following roles:

* **Source 1:** Deduplicated reference dataset containing the records for which matches must be identified.
* **Source 2:** Dataset containing records that may match Source 1 records.
* **Source 3:** Dataset containing records that may match Source 1 records.

A record is not itself equivalent to a real-world business identity. Different records may represent the same business.

## 8.3 Matching Definition

**Matching** is the process of determining whether a record from Source 2 or Source 3 refers to the same real-world business as a given Source 1 record.

A record shall be considered a confirmed match only when the system's matching decision accepts the relationship between the records.

The matching process may use business names, addresses, country information, and other available record attributes as evidence of identity.

The challenge does not prescribe an exact matching rule, similarity threshold, or algorithm. These implementation details shall be defined in the Technical Design.

## 8.4 Match Relationship

The required match relationship is defined from a Source 1 record to zero or more matching records from Source 2 and Source 3.

For each Source 1 record, the system shall produce a list of accepted matching record IDs.

The relationship shall support:

* Zero matching records.
* Exactly one matching record.
* Multiple matching records.

The system shall not impose a one-to-one restriction on the number of matches associated with a Source 1 record.

The challenge does not establish a universal exclusivity rule preventing a Source 2 or Source 3 record from being associated with multiple Source 1 records.

## 8.5 Zero-Match Entities

A **zero-match entity** is a Source 1 entity for which no matching record is accepted from either Source 2 or Source 3.

The system shall:

* Retain the Source 1 record in the final output.
* Represent the absence of accepted matches using an empty `matched_entity_ids` field.
* Treat zero-match outcomes as valid results.

A zero-match outcome does not necessarily mean that no candidates were generated. Candidates may have been considered and subsequently rejected.

The challenge does not require a separate output classification distinguishing the reasons for a zero-match outcome.

## 8.6 Single-Match Entities

A **single-match entity** is a Source 1 entity for which exactly one matching record is accepted from Source 2 or Source 3.

The system shall:

* Include the accepted matching record's ID in `matched_entity_ids`.
* Retain the Source 1 record in the final output.
* Ensure that the matching record ID belongs to Source 2 or Source 3.

No additional matching rule or priority policy is imposed specifically for single-match entities.

## 8.7 Multi-Match Entities

A **multi-match entity** is a Source 1 entity for which two or more matching records are accepted from Source 2, Source 3, or both.

The system shall:

* Include all accepted matching record IDs in `matched_entity_ids`.
* Support multiple matches from the same source and matches across both sources.
* Avoid duplicate IDs within a single match list.
* Retain the Source 1 record in the final output.

The challenge does not specify a maximum number of matches per Source 1 record or a required ordering of IDs within the match list.

## 8.8 Ambiguous Entities

An **ambiguous entity** refers to a business record or potential match relationship for which the available information does not clearly establish whether two records represent the same real-world business.

Ambiguity may arise from incomplete, inconsistent, generic, or conflicting business names and addresses.

The system shall distinguish a potential candidate from an accepted match. The presence of a candidate alone shall not establish that two records represent the same business.

The challenge does not define a formal ambiguity category, require an uncertainty label, or prescribe a separate output status for ambiguous cases.

The handling of uncertain candidate relationships, including the criteria for accepting or rejecting a match, shall be specified in the Technical Design.

## 8.9 Cross-Source Matching

The system shall perform entity resolution with Source 1 as the reference dataset and Source 2 and Source 3 as the matching datasets.

The required matching relationships are:

* Source 1 → Source 2
* Source 1 → Source 3

The system shall:

* Associate accepted matches with the corresponding Source 1 record.
* Include only Source 2 and Source 3 record IDs in the final match lists.
* Exclude Source 1 record IDs from the matching record lists.
* Preserve the Source 1-centric structure of the required output.

The challenge does not require direct Source 2-to-Source 3 matching as a separate output relationship. Whether such comparisons are used internally is an implementation decision, provided the required output semantics are preserved.

No additional same-source matching behavior or cross-source exclusivity rule is imposed by this section.


# 9. Data Characteristics and Quality Requirements

## 9.1 Relevant Data Quality Constraints

The system shall accommodate noisy, inconsistent, and incomplete business records across the three data sources.

The system shall:

* Support variations in business names, addresses, and country values.
* Treat country as an open-text field rather than restricting it to a fixed list of countries.
* Preserve original source records and their identifying information.

The detailed data schema and input validation requirements are defined in earlier sections of this SRS.

## 9.2 Handling Missing and Inconsistent Data

The system shall detect and report missing required values and malformed records during input validation.

The system shall distinguish missing values from valid text and shall not silently accept invalid records.

Specific preprocessing, normalization, and missing-value handling methods shall be defined in the Technical Design.

## 9.3 Data Quality Limitations

The system shall not assume that training data covers every variation present in the test data.

Known data-quality limitations, including name and address ambiguity, incomplete information, and formatting variation, shall be considered when designing and evaluating the matching system.

Detailed examples, statistics, and observed noise patterns shall remain documented in the dataset analysis reports.

# 10. Candidate Generation and Matching Requirements

## 10.1 Candidate Generation Requirements

The system shall generate a candidate set of Source 2 and Source 3 records for each Source 1 record before making final match decisions.

Candidate generation shall reduce the search space while supporting the identification of valid matches.

The system shall generate the required `candidate_pairs.tsv` output as defined in Section 6.

The specific candidate-generation algorithms, blocking strategies, and candidate-size targets shall be defined in the Technical Design.

## 10.2 Candidate Validity and Deduplication

The system shall ensure that candidate lists contain only valid Source 2 and Source 3 record IDs and do not contain duplicate IDs within a list. Empty candidate lists shall be permitted. The complete output requirements and validation rules are defined in Section 6.

## 10.3 Match Decision Requirements

The system shall determine whether each candidate record represents the same real-world business as its associated Source 1 record.

Match decisions shall support the official evaluation objective, which uses the F_β Score (β = 0.5) and places greater emphasis on precision than recall. The implementation-specific decision rule, thresholding, and feature logic shall be defined in the Technical Design.

## 10.4 Multiple-Match and No-Match Handling

The system shall support zero, one, or multiple accepted matches for each Source 1 record. Source 1 records with no accepted matches shall remain in the output with an empty match list. For the complete output semantics, ordering requirements, and validation rules, see Sections 6 and 8.

## 10.5 Candidate and Match Consistency

The system should ensure that final accepted matches are included in the corresponding candidate lists.

A final match that is absent from the candidate list shall trigger an advisory warning rather than a hard validation failure.

The consistency check shall not override the established output-validation requirements or the official submission validator's behavior.

# 11. Training and Evaluation Requirements

# 11. Training and Evaluation Requirements

## 11.1 Training and Validation Data Requirements

### 11.1.1 Data Preparation and Separation

**FR-11.1.1** The system shall use the provided training data and ground-truth labels for model development and validation. Training and validation data usage shall be consistent with the challenge's data constraints.

**FR-11.1.2** The system shall not use test-set ground-truth labels for training, model selection, or threshold tuning.

### 11.1.2 Entity-Level Train/Validation Split **[FROZEN]**

**FR-11.1.3** **[FROZEN per Design 3.5.1]** Training and validation data shall be separated at the Source 1 entity level. All candidate pairs associated with a given S1 entity shall be assigned to the same partition (either training or validation).

**FR-11.1.4** **[FROZEN per Design 3.5.1]** This entity-level separation prevents candidate pairs from the same reference entity from being split across training and validation, avoiding data-leakage risks.

**FR-11.1.5** An initial proposed split of 90% training / 10% validation shall be used as a default, with stratification applied to preserve match-count and source-pair distributions where practical. Adjustments to this split may be made through controlled experimentation.

### 11.1.3 Training Data Construction from Generated Candidates **[FROZEN]**

**FR-11.1.6** **[FROZEN per Design 3.3.1]** Training examples shall be constructed directly from candidate pairs generated by the frozen candidate-generation pipeline (Section 7.5). Candidate generation and feature extraction shall use the same configuration in training as in inference.

**FR-11.1.7** **[FROZEN per Design 1.7 and 3.3.1]** Ground-truth labels shall not be used to inject known positive candidates into the generated candidate set during training. A genuine match that is absent from the generated candidates must be recorded and evaluated separately as a candidate-generation miss.

### 11.1.4 Binary Label Convention **[FROZEN]**

**FR-11.1.8** **[FROZEN per Design 3.4.1]** For each generated candidate pair, the binary label shall be determined as follows: positive (1) if the candidate entity ID appears in the ground-truth match list for the corresponding S1 entity; negative (0) otherwise.

**FR-11.1.9** **[FROZEN per Design 3.4.1]** No soft labels, confidence weighting, or probabilistic labels shall be applied during this initial labeling stage.

### 11.1.5 Positive Example Retention **[FROZEN]**

**FR-11.1.10** **[FROZEN per Design 3.4.1]** All generated positive pairs (candidate pairs labeled as positive matches according to ground truth) shall be retained during training. No reduction or sampling of positive examples shall artificially decrease true-match representation.

### 11.1.6 Hard-Negative Sampling

**FR-11.1.11** The negative training set may use a controlled mixture of hard negatives and representative ordinary negatives to improve model robustness.

**FR-11.1.12** Hard negatives may be selected to include candidates that resemble the reference entity or were retrieved through high-similarity retrieval methods.

**FR-11.1.13** Hard-negative mining, if employed, shall operate only within the training partition and shall exclude all known ground-truth positive pairs from the training dataset.

**FR-11.1.14** The specific hard-negative sampling strategy, selection criteria, and ratios shall be documented in `TECHNICAL_DESIGN.md`.

## 11.2 Data Leakage Prevention

### 11.2.1 Training/Validation Separation

**FR-11.2.1** The system shall prevent information from validation or test data labels from influencing model training.

**FR-11.2.2** Data preparation, feature generation, and model selection shall avoid using information that would not be available during test-time inference.

**FR-11.2.3** **[FROZEN per Design 6.5.1]** Validation data shall not be used to train the model.

**FR-11.2.4** **[FROZEN per Design 6.5.1]** Validation labels shall not be used to construct training-only artifacts such as hard-negative sets.

**FR-11.2.5** **[FROZEN per Design 6.5.1]** The validation split shall be generated once, saved, and reused for comparable experiments.

### 11.2.2 Test Data Isolation

**FR-11.2.6** **[FROZEN per Design 6.5.1]** Test data ground-truth labels must never be used for training, validation, or threshold selection.

### 11.2.3 Leakage Prevention Details

**FR-11.2.7** The specific leakage-prevention procedures, including any candidate-generation modifications that must not be applied, shall be documented in the Technical Design.

## 11.3 Model Training and Validation Requirements

### 11.3.1 Primary Model Family **[FROZEN]**

**FR-11.3.1** **[FROZEN per Design 3.2]** The system shall use LightGBM as the primary model family for binary classification of candidate pairs.

**FR-11.3.2** **[FROZEN per Design 3.2]** XGBoost may be considered as a challenger model for controlled comparison, subject to documented experimentation and validation.

**FR-11.3.3** **[FROZEN per Design 3.2]** The primary architecture shall remain LightGBM unless experimentation explicitly demonstrates a justified alternative and that change is approved.

### 11.3.2 Training Procedure

**FR-11.3.4** The system shall support training and validation of the LightGBM binary classifier using the training data and extracted features as prepared in Section 11.1.

**FR-11.3.5** The model shall be trained to estimate the probability that a candidate pair represents the same real-world business.

**FR-11.3.6** Hyperparameter selection, regularization strategy, loss function, training convergence criteria, and other model-configuration details shall be documented in `TECHNICAL_DESIGN.md`.

### 11.3.3 Final Model Retraining **[FROZEN]**

**FR-11.3.7** **[FROZEN per Design 3.6.1]** After model configuration and decision-threshold selection, the selected model shall be retrained on all eligible training data (combined training and validation partitions, excluding only the test set).

**FR-11.3.8** **[FROZEN per Design 3.6.1]** The selected feature schema, candidate-generation configuration, and decision threshold shall remain frozen during retraining.

**FR-11.3.9** **[FROZEN per Design 3.6.1]** The final model artifact and decision threshold shall be recorded and associated with their configuration versions for reproducibility.

## 11.4 Threshold Selection and Evaluation

### 11.4.1 Validation-Based Threshold Optimization **[FROZEN]**

**FR-11.4.1** **[FROZEN per Design 3.9.1 and Design 6.7.2]** The matching decision threshold shall be selected through validation experimentation using the designated validation set.

**FR-11.4.2** **[FROZEN per Design 3.9.1]** The threshold shall be chosen to maximize the official macro F₀.₅ score on the validation set.

**FR-11.4.3** **[FROZEN per Design 3.9.1]** A range of candidate thresholds shall be evaluated, and the threshold stability around the selected value shall be assessed to ensure robustness.

**FR-11.4.4** **[FROZEN per Design 3.9.1]** The default decision policy shall use a single global probability threshold applied to all candidate pairs. Source-pair-specific (S1-S2 vs. S1-S3) thresholds may be considered only if controlled validation experiments explicitly justify and document their necessity.

### 11.4.2 Validation as a Development Aid

**FR-11.4.5** The system may perform internal validation experiments to estimate matching quality and to support threshold and model selection.

**FR-11.4.6** Such internal validation may use a held-out split of the training data and may report a validation score such as a Macro F₀.₅.

**FR-11.4.7** Internal validation results are development aids and shall not be treated as official challenge scores.

**FR-11.4.8** The validation context, threshold value, selection procedure, and associated validation metrics shall be documented in `TECHNICAL_DESIGN.md` or the relevant experiment documentation.

## 11.5 Official Evaluation Metric and Scoring Constraints

---

## 11.6 Candidate-Generation Evaluation **[FROZEN per Design 6.4]**

### 11.6.1 Independent Candidate-Recall Measurement **[FROZEN]**

**FR-11.6.1** **[FROZEN per Design 6.4.1]** Candidate-generation quality shall be evaluated independently of the downstream matching model.

**FR-11.6.2** **[FROZEN per Design 6.4.1]** Candidate recall shall be measured as the proportion of ground-truth matches that are retrieved as candidates, computed per S1 entity and macro-averaged.

**FR-11.6.3** **[FROZEN per Design 6.4.1]** A true match that is not retrieved during candidate generation cannot be recovered by the model and must be recorded as a candidate-generation miss (separate from downstream model-ranking or threshold errors).

### 11.6.2 Candidate-Recall Metrics

**FR-11.6.4** **[FROZEN per Design 6.4.2]** Candidate recall shall be reported broken down by:
* Overall candidate recall (all S1 entities).
* Source pair (S1-S2 recall and S1-S3 recall).
* Candidate-generation method (per retrieval method).
* Relevant data subsets (e.g., by country, match-count groups, or data-quality categories).

**FR-11.6.5** **[FROZEN per Design 6.4.2]** Supporting metrics shall include:
* Total number of generated candidate pairs.
* Average candidate count per S1 entity.
* Candidate-count distribution.
* Candidate volume by source pair.
* Reduction ratio (reduction in comparisons relative to exhaustive S1-to-S2 and S1-to-S3 comparisons).

### 11.6.3 Per-Method Contribution Analysis

**FR-11.6.6** **[FROZEN per Design 6.4.3]** For each candidate-generation retrieval method, the system shall measure or analyze:
* Candidates uniquely contributed by that method.
* Ground-truth matches recovered by that method alone.
* Incremental true matches recovered when the method is added to the existing union.
* Candidate volume introduced by the method.
* Effect on overall candidate recall and computational cost.

**FR-11.6.7** These measurements shall support decisions about retrieval limits, method configuration, and the value of each retrieval family.

---

# 12. System Architecture and Execution Requirements

## 12.1 Pipeline Stages

### 12.1.1 Major Pipeline Stages

**FR-12.1.1** The system shall implement a pipeline that supports the following stages:

1. Input data loading and validation.
2. Candidate generation for Source 1 records against Sources 2 and 3.
3. Candidate feature preparation and match prediction.
4. Final match selection.
5. Generation and validation of the required submission files.

**FR-12.1.2** The specific algorithms and internal implementation of each stage shall be documented in the Technical Design.

### 12.1.2 Frozen Single-Workstation Batch Architecture **[FROZEN]**

**FR-12.1.3** **[FROZEN per Design 4.3.1]** The system shall use a single-workstation, batch-oriented architecture as the primary execution mode.

**FR-12.1.4** **[FROZEN per Design 4.3.1]** Large workloads shall be processed deterministically in batches to keep working memory within available resource limits.

**FR-12.1.5** **[FROZEN per Design 4.3.1]** A distributed multi-machine architecture is not part of the default design.

### 12.1.3 Batch-Oriented Processing **[FROZEN]**

**FR-12.1.6** **[FROZEN per Design 4.9.1]** All major processing stages (candidate generation, feature extraction, model training, inference) shall support batch-oriented execution.

**FR-12.1.7** **[FROZEN per Design 4.9.1]** Batch sizes shall be configurable and selected based on memory usage, throughput, and failure-recovery considerations.

**FR-12.1.8** **[FROZEN per Design 4.9.1]** Batching shall permit deterministic, reproducible processing without requiring entire datasets in memory.

### 12.1.4 Reusable Indexes **[FROZEN]**

**FR-12.1.9** **[FROZEN per Design 4.8.1]** The system shall construct and reuse versioned indexes for Source 2 and Source 3 records.

**FR-12.1.10** **[FROZEN per Design 4.8.1]** Indexes shall be reconstructed when their associated preprocessing or configuration changes.

**FR-12.1.11** **[FROZEN per Design 4.8.1]** Index versions shall be recorded and used to detect incompatibility with changed configurations.

### 12.1.5 Disk-Backed Intermediate Artifacts **[FROZEN]**

**FR-12.1.12** **[FROZEN per Design 4.7]** The system shall persist intermediate artifacts such as normalized records, candidate pairs, and feature vectors using disk-backed storage.

**FR-12.1.13** **[FROZEN per Design 4.7]** Intermediate data shall not be required to fit entirely in memory.

**FR-12.1.14** **[FROZEN per Design 4.7]** Storage formats such as Parquet, compressed arrays, or structured layouts shall be used to balance storage efficiency against retrieval speed.

## 12.2 Training and Inference Workflows

### 12.2.1 Workflow Overview

**FR-12.2.1** The system shall support separate training and inference workflows.

**FR-12.2.2** **Training workflow:** Load training data and ground-truth labels, prepare training and validation data (entity-level split), train the LightGBM matching model, evaluate validation performance, select decision threshold, and retrain final model on all training data.

**FR-12.2.3** **Inference workflow:** Load test data and the trained model with associated configuration, generate candidates, extract features, predict match scores, apply the selected decision threshold, and produce the required output files.

**FR-12.2.4** The workflows shall comply with the official challenge data and submission constraints.

### 12.2.2 Inference Configuration Validation **[FROZEN]**

**FR-12.2.5** **[FROZEN per Design 5.4]** Before inference begins, the system shall load and verify that the selected model, feature schema, preprocessing configuration, candidate-generation configuration, and decision threshold are compatible.

**FR-12.2.6** **[FROZEN per Design 5.4]** If required artifacts are missing or incompatible, the system shall fail clearly with diagnostic information.

**FR-12.2.7** **[FROZEN per Design 5.4]** The system shall not silently substitute a different configuration.

### 12.2.3 Inference Preprocessing Consistency **[FROZEN]**

**FR-12.2.8** **[FROZEN per Design 5.5]** During inference, test records shall be processed using the exact same preprocessing and normalization rules applied during training.

**FR-12.2.9** **[FROZEN per Design 5.5]** No test-specific transformations shall be introduced.

**FR-12.2.10** **[FROZEN per Design 5.5]** The preprocessing configuration associated with the trained model shall be applied without modification.

### 12.2.4 Inference Feature Schema Consistency **[FROZEN]**

**FR-12.2.11** **[FROZEN per Design 5.7]** During inference, the feature-extraction pipeline shall produce features that exactly match the schema and processing used during training.

**FR-12.2.12** **[FROZEN per Design 5.7]** Feature names, ordering, data types, and numerical representations shall be identical between training and inference.

**FR-12.2.13** **[FROZEN per Design 5.7]** The system shall not omit or reorder features expected by the trained model.

### 12.2.5 Candidate Scoring **[FROZEN]**

**FR-12.2.14** **[FROZEN per Design 5.6]** The trained LightGBM model shall score each candidate pair using its extracted feature vector.

**FR-12.2.15** **[FROZEN per Design 5.6]** The system shall process candidate pairs in batches to manage memory usage.

**FR-12.2.16** **[FROZEN per Design 5.6]** Each score shall remain associated with its corresponding candidate pair for use in the final decision stage.

### 12.2.6 Decision Threshold Application **[FROZEN]**

**FR-12.2.17** **[FROZEN per Design 5.8]** The final matching decision shall apply the selected decision threshold to each candidate's score.

**FR-12.2.18** **[FROZEN per Design 5.8]** A candidate is accepted as a final match when its score satisfies the selected decision policy.

**FR-12.2.19** **[FROZEN per Design 5.8]** The system shall apply the exact validated threshold loaded from the model's associated configuration.

**FR-12.2.20** **[FROZEN per Design 5.8]** No substitution or modification of the threshold shall occur without explicit approval and validation.

### 12.2.7 Detailed Training and Inference Documentation

**FR-12.2.21** The detailed training procedure, model selection, and threshold logic are documented in `TECHNICAL_DESIGN.md`.

## 12.4 Checkpointing and Recovery **[FROZEN]**

**FR-12.4.1** **[FROZEN per Design 4.10.1]** The system shall support batch-level checkpointing and resumable execution.

**FR-12.4.2** **[FROZEN per Design 4.10.1]** Batch identity shall be derived from input partition and processing configuration.

**FR-12.4.3** **[FROZEN per Design 4.10.1]** The system shall verify that completed batch outputs are valid and compatible with the current configuration before reusing them.

**FR-12.4.4** **[FROZEN per Design 4.10.1]** Incomplete or incompatible batches shall be reprocessed safely without creating duplicate records.

## 12.4 Submission Generation Workflow

The system shall generate the required `matching_results.tsv` and `candidate_pairs.tsv` files in the prescribed format.

Each output shall contain one row per test Source 1 entity, preserving the original Source 1 row order.

The submission-generation process shall validate the output schema, record coverage, identifier validity, and list formatting before submission.

Candidate-match consistency shall be checked and reported as an advisory warning rather than a strict validation failure, consistent with Section 6.7 and the official challenge validator behavior.

# 13. Non-Functional Requirements

## 13.1 Scalability and Resource Constraints

The system shall support processing the challenge datasets at the required scale without relying on exhaustive pairwise comparison across all records.

The resource assumptions and candidate-generation strategy shall be documented in `TECHNICAL_DESIGN.md`.

No fixed memory, hardware, or runtime limit is mandated by the available challenge requirements.

## 13.2 Performance Requirements

The system shall support entity matching at the scale of the provided challenge datasets.

The official challenge evaluation metric is defined in Section 11.5. Internal validation may inform model and threshold selection, but no fixed runtime, throughput, or numerical performance threshold is mandated by the challenge.

## 13.3 Reliability and Error Handling

The system shall validate inputs and generated outputs before submission.

The implementation shall distinguish validation errors, warnings, and non-blocking inconsistencies.

Malformed inputs and invalid outputs shall not be silently accepted.

Error-handling and logging procedures shall be documented in the Technical Design.

## 13.4 Reproducibility and Determinism

### 13.4.1 Reproducibility Requirements

**FR-13.4.1** The implementation shall provide documented execution instructions and identify the environment required to run the solution.

**FR-13.4.2** The Technical Design shall document relevant reproducibility controls, including random seeds and deterministic settings where applicable.

**FR-13.4.3** A strict bit-for-bit determinism requirement is not established by the available project evidence or official challenge rules.

### 13.4.2 Experiment Artifact Retention **[FROZEN]**

**FR-13.4.4** **[FROZEN per Design 6.9.1]** All completed experiments shall be preserved with sufficient metadata to reproduce their results.

**FR-13.4.5** **[FROZEN per Design 6.9.1]** Artifacts shall include: dataset fingerprints or versions, train/validation split definitions, candidate-generation configuration, feature schema, trained model files, prediction records, and evaluation metrics.

**FR-13.4.6** **[FROZEN per Design 6.9.1]** Random seeds shall be fixed where supported; nondeterministic operations shall be documented.

**FR-13.4.7** **[FROZEN per Design 6.9.1]** Experiment artifacts shall be stored in a structured directory with unique experiment identifiers.

### 13.4.3 Final Configuration Reproducibility **[FROZEN]**

**FR-13.4.8** **[FROZEN per Design 6.10.1]** The final selected model configuration shall be explicitly recorded and versioned.

**FR-13.4.9** **[FROZEN per Design 6.10.1]** The final model artifact shall be accompanied by versioned metadata identifying the feature schema, preprocessing configuration, candidate-generation configuration, selected decision threshold, and trained model file.

**FR-13.4.10** **[FROZEN per Design 6.10.1]** The final configuration shall be reproducible by executing the training pipeline with the recorded versions and settings.

## 13.5 Maintainability and Modularity

The system shall organize data loading, validation, candidate generation, matching, evaluation, and submission generation into components with clearly defined responsibilities.

The implementation shall support independent testing and maintenance of these components without conflating requirement-level behavior with implementation-specific design choices.

Detailed module structure, interfaces, and implementation dependencies shall be documented in `TECHNICAL_DESIGN.md`. See also Section 12.3 for the high-level component boundaries.

---

# 14. Challenge Constraints and Environment

## 14.1 External Data and API Restrictions

The system shall not use external business databases, APIs, geocoding services, or internet-based lookup services to augment the provided challenge data.

The official challenge rules strictly prohibit external data lookup and external enrichment that would allow participants to resolve business entities using external services or databases. This includes, but is not limited to, using commercial entity-resolution APIs, business-registration lookups, geocoding APIs, and other internet-based data augmentation or lookup methods.

Training and matching shall use the provided challenge data and other materials permitted by the official challenge rules. Any exception must be explicitly supported by the challenge rules.

## 14.2 Model and Submission Restrictions

The final model shall comply with the challenge's official licensing and parameter-count restrictions. The challenge statement specifies that the final model shall be a MIT/Apache 2.0 license model and up to 8 billion parameters.

The final submission shall include the required output files and shall comply with the official submission package structure described by the challenge.

No additional model-family, architecture, parameter-count, or licensing restriction shall be introduced unless it is explicitly established by the official challenge rules or an approved project decision.

## 14.3 Software and Dependency Requirements

The challenge requires the final submission package to include a runnable code directory with a `README.md` and a dependency declaration such as `requirements.txt` or an equivalent environment file.

This requirement applies to the final submission package and shall not be treated as a blanket requirement that every project artifact or development file must include a dependency manifest.

The project shall therefore treat dependency declaration as a submission-packaging requirement when it is part of the final deliverable, while keeping the actual implementation dependency choices in `TECHNICAL_DESIGN.md`.

## 14.4 Runtime and Hardware Constraints

The available challenge requirements do not establish a fixed CPU, GPU, memory, or execution-time limit.

The implementation shall document relevant resource assumptions and any hardware requirements in the Technical Design.

## 14.5 Configuration and Path Requirements

The implementation shall use the provided challenge directory structure for input data unless a documented configuration override is defined.

The required submission files shall be generated in the prescribed output directory and follow the official naming and formatting conventions.

Detailed path handling and configuration mechanisms shall be documented in the Technical Design.

---

# 15. Testing and Acceptance Criteria

## 15.1 Functional and Integration Testing

### 15.1.1 Major Pipeline Testing

The implementation shall support testing of the major functional stages of the entity-resolution workflow, including:

* input loading and validation;
* dataset integrity checks;
* preprocessing and normalization;
* candidate generation;
* matching and decision selection;
* output formatting and validation;
* final submission preparation.

The project may include validation and analysis utilities, but the SRS states the testing that the system must support and pass without implying that a complete automated test suite already exists.

### 15.1.2 Controlled Experimentation **[FROZEN]**

**FR-15.1.1** **[FROZEN per Design 6.6.1]** All significant model and configuration changes shall be executed as controlled experiments.

**FR-15.1.2** **[FROZEN per Design 6.6.1]** Each experiment shall have a clearly stated objective, hypothesis, and single major change (where practical).

**FR-15.1.3** **[FROZEN per Design 6.6.1]** Experiments shall record: experiment ID, date, objective, dataset version, candidate-generation configuration, feature schema, model parameters, decision threshold, evaluation metrics, runtime, and resource usage.

**FR-15.1.4** **[FROZEN per Design 6.6.1]** Experiments shall be compared against a stable baseline using the same validation split and evaluation implementation.

### 15.1.3 Error Analysis and Diagnostics **[FROZEN]**

**FR-15.1.5** **[FROZEN per Design 6.8.1]** Validation errors shall be systematically analyzed and categorized.

**FR-15.1.6** **[FROZEN per Design 6.8.1]** False-positive errors (predicted matches that are not ground-truth matches) shall be aggregated into patterns indicating ambiguous names, shared addresses, generic names, or conflicting evidence.

**FR-15.1.7** **[FROZEN per Design 6.8.1]** False-negative errors (known matches not predicted) shall be separated into candidate-generation misses versus model-ranking or threshold errors.

**FR-15.1.8** **[FROZEN per Design 6.8.1]** Error analysis shall inform targeted improvements and validate that corrective changes produce measurable benefits.

## 15.2 Matching and Evaluation Testing

The system shall evaluate matching performance using validation data without using test-set ground-truth labels.

Internal evaluation shall use the official F_β Score (β = 0.5) as the primary matching-performance measure. Internal validation results shall be distinguished from official challenge evaluation results.

## 15.3 Output and Submission Validation

The generated submission files shall be validated against the official challenge requirements using the provided validator.

Validation shall cover output structure, required record coverage, identifier validity, and list formatting.

Candidate-match inconsistency shall remain an advisory warning rather than a strict rejection condition, consistent with the established project decision.

## 15.4 End-to-End Testing

The implementation shall support an end-to-end workflow from input data loading through candidate generation, match prediction, and generation of the required submission files.

The workflow shall be tested to verify that the expected output files are generated in the prescribed format and location.

Execution instructions and relevant test procedures shall be documented.

## 15.5 Acceptance Criteria

The submission shall satisfy the official challenge's output-format and validation requirements.

Output validation and matching-quality evaluation are distinct acceptance concerns. A file that passes the schema and validation checks does not automatically prove that the underlying matching decisions are high quality, because challenge score is determined by the official evaluation metric and the hidden evaluation set.

The following acceptance interpretations shall apply:

* Required output schema, record coverage, ID validity, and duplicate handling are acceptance criteria for output validity.
* Matching quality is evaluated using the official challenge F_0.5 metric and is not established merely by passing the output validator.
* Candidate-match inconsistency shall be treated as an advisory warning rather than a strict validation failure unless the official challenge rules explicitly classify it as a hard rejection.

---

# 16. Documentation and Traceability

## 16.1 Required Project Documentation

The project shall maintain the documentation required to understand, reproduce, and validate the challenge solution.

The core project documentation shall include:

* `docs/problem_statement.md` — the official challenge statement and source-of-truth requirements.
* `docs/SRS.md` — the system requirements and constraints.
* `docs/TECHNICAL_DESIGN.md` — the implementation design and technical decisions.
* The project's knowledge or decisions document(s), such as `docs/knowledge.md` or `useful/knowledge.md` — to record validated findings and project decisions.

Dataset analysis reports, experiment reports, and other supporting artifacts are relevant project materials, but they shall be treated as supporting documentation rather than as mandatory deliverables unless explicitly required by the challenge or an approved project decision.

## 16.2 Requirement Traceability

Requirements shall be traceable to their originating challenge rules, validation checks, approved project decisions, or other relevant evidence.

A formal traceability matrix is not required unless it is explicitly approved by the project owner. The project shall maintain enough traceability to support review, validation, and implementation alignment without introducing a separate tracking burden.

## 16.3 Glossary and References

The SRS shall define the core terms required to understand the challenge and its requirements.

Existing definitions in earlier SRS sections shall be reused rather than duplicated.

References shall identify the official challenge documentation and relevant project materials used to establish requirements.

---
