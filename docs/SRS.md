# 1. Document Control

## 1.1 Document Information

| Field                        | Details                                                                                                                     |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Document Title**           | Software Requirements Specification (SRS)                                                                                   |
| **Project**                  | Business Entity Resolution Challenge                                                                                        |
| **Document Type**            | Software Requirements Specification                                                                                         |
| **Document Version**         | 0.1                                                                                                                         |
| **Document Status**          | Draft                                                                                                                       |
| **Primary Purpose**          | Define the complete software/system requirements for the entity-resolution solution to be developed for the challenge.      |
| **Intended Audience**        | Project developers, AI coding agents, reviewers, testers, and project maintainers                                           |
| **Source of Requirements**   | Official challenge problem statement, challenge rules/constraints, dataset characteristics, and validated project decisions |
| **Implementation Reference** | This document will serve as the authoritative requirements specification for the implementation.                            |

---

## 1.2 Version History

| Version | Date       | Status | Description                                                                                     |
| ------- | ---------- | ------ | ----------------------------------------------------------------------------------------------- |
| **0.1** | 2026-09-26 | Draft  | Initial SRS structure and document-control section created.                                     |
| **TBD** | TBD        | TBD    | Subsequent revisions will record substantive requirement changes, additions, or clarifications. |

### Versioning Rules

The SRS shall use version numbers to distinguish between revisions.

* **Major version**: Used when fundamental requirements or system scope change.
* **Minor version**: Used when requirements are added, removed, or materially changed without changing the overall project purpose.
* **Patch/revision-level change**: Used for corrections, clarifications, formatting improvements, or other non-substantive changes.

Requirement changes shall be documented in the Version History and, where applicable, reflected in the Requirement Traceability Matrix.

---

## 1.3 Document Status

The current status of this document is:

> **DRAFT — UNDER DEVELOPMENT**

This SRS will be developed progressively as the challenge requirements, dataset characteristics, constraints, and system requirements are analyzed.

The document shall not be considered final until:

1. The official challenge requirements have been fully represented.
2. All applicable constraints have been documented.
3. Required system behavior has been specified.
4. Input and output requirements have been defined.
5. Evaluation requirements have been documented.
6. Acceptance criteria have been established.
7. Requirements have been reviewed for consistency with the official problem statement.

### Important Status Rule

The SRS defines **requirements**, not premature implementation decisions.

Specific implementation choices such as the final normalization algorithms, candidate-generation strategies, feature set, ML model, model hyperparameters, thresholds, and other algorithmic decisions shall be documented in the **Technical Design** after sufficient dataset analysis and experimentation.

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


