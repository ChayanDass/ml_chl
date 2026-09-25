# Dataset Audit for SRS Section 5 — Input Data Requirements

Date: 2026-09-26
Repository root: `/home/vikaspal/Desktop/ml_chl`

## 1. Executive Summary

This audit is based only on read-only inspection of the files in the project’s dataset folders and the official challenge text in `docs/problem_statement.md` and `6ab10eb3b23ba_student_resource/student_resource/README.md`.

Confirmed facts:

- The dataset contains seven TSV files: three source datasets for training, three source datasets for test, and one training ground-truth file.
- All source files share the same schema: `entity_id`, `business_name`, `business_address`, `country`.
- The ground-truth file is a two-column TSV: `source1_entity_id`, `matched_entity_ids`.
- The project documentation explicitly states that Source 1 is the deduplicated reference source and that the source is indicated by the `entity_id` prefix (`S1-`, `S2-`, `S3-`).
- The challenge documentation states that the training data covers `US` and `India`, and that the test set additionally includes `France`.
- The observed file format is tab-separated text and appears to be UTF-8 encoded.

Important caveat:

- The dataset is very large, and the audit focuses on confirmed observations from the files and official documentation. Some exact field-level integrity statistics for every file may require additional validation scripts; where that is not available from the inspection evidence, the report labels it as “Unknown” or “Requires verification.”

## 2. Files and Folder Inventory

Project path audited:

- `6ab10eb3b23ba_student_resource/student_resource/dataset/train/`
- `6ab10eb3b23ba_student_resource/student_resource/dataset/test/`

Inventory:

| Relative path | File name | Type | Observed format | Notes |
| --- | --- | --- | --- | --- |
| `6ab10eb3b23ba_student_resource/student_resource/dataset/train/train_source1.tsv` | `train_source1.tsv` | Training source file | TSV, UTF-8 | Source 1 records; deduplicated reference source per docs |
| `6ab10eb3b23ba_student_resource/student_resource/dataset/train/train_source2.tsv` | `train_source2.tsv` | Training source file | TSV, UTF-8 | Source 2 records |
| `6ab10eb3b23ba_student_resource/student_resource/dataset/train/train_source3.tsv` | `train_source3.tsv` | Training source file | TSV, UTF-8 | Source 3 records |
| `6ab10eb3b23ba_student_resource/student_resource/dataset/train/train_ground_truth.tsv` | `train_ground_truth.tsv` | Ground truth | TSV, UTF-8 | Maps S1 records to S2/S3 matches |
| `6ab10eb3b23ba_student_resource/student_resource/dataset/test/test_source1.tsv` | `test_source1.tsv` | Test source file | TSV, UTF-8 | Source 1 test records |
| `6ab10eb3b23ba_student_resource/student_resource/dataset/test/test_source2.tsv` | `test_source2.tsv` | Test source file | TSV, UTF-8 | Source 2 test records |
| `6ab10eb3b23ba_student_resource/student_resource/dataset/test/test_source3.tsv` | `test_source3.tsv` | Test source file | TSV, UTF-8 | Source 3 test records |

Observed file sizes (filesystem):

- `train_ground_truth.tsv`: ~122 MB
- `train_source1.tsv`: ~201 MB
- `train_source2.tsv`: ~467 MB
- `train_source3.tsv`: ~481 MB
- `test_source1.tsv`: ~167 MB
- `test_source2.tsv`: ~486 MB
- `test_source3.tsv`: ~483 MB

## 3. Dataset Schema Tables

### 3.1 Source Dataset Schema (confirmed)

| Column name | Observed type | Example value | Description | Source of evidence |
| --- | --- | --- | --- | --- |
| `entity_id` | string | `S1-925783039` | Unique record identifier; prefix encodes Source 1/2/3 | README + file inspection |
| `business_name` | string | `Orelee's Barbershop` | Business legal/trade name, may contain abbreviations, typos, transliterations | README + file inspection |
| `business_address` | string | `1795 Westchester Drive, High Point, NC` | Business address text, may be partial/noisy | README + file inspection |
| `country` | string | `US` or `India` | Country label; docs say `France` appears in test data | README + file inspection |

Confirmed source file header examples:

- `dataset/train/train_source1.tsv`: `entity_id`, `business_name`, `business_address`, `country`
- `dataset/train/train_source2.tsv`: `entity_id`, `business_name`, `business_address`, `country`
- `dataset/train/train_source3.tsv`: `entity_id`, `business_name`, `business_address`, `country`
- `dataset/test/test_source1.tsv`: `entity_id`, `business_name`, `business_address`, `country`
- `dataset/test/test_source2.tsv`: `entity_id`, `business_name`, `business_address`, `country`
- `dataset/test/test_source3.tsv`: `entity_id`, `business_name`, `business_address`, `country`

### 3.2 Ground-Truth Schema (confirmed)

| Column name | Observed type | Example value | Description | Source of evidence |
| --- | --- | --- | --- | --- |
| `source1_entity_id` | string | `S1-965667` | Source 1 entity ID in a ground-truth row | README + file inspection |
| `matched_entity_ids` | string (comma-separated list of IDs) | `S2-681193310,S2-743505751,S3-775321672` | Matching records from Source 2 and/or Source 3 for the S1 record | README + file inspection |

Confirmed ground-truth header:

- `dataset/train/train_ground_truth.tsv`: `source1_entity_id`, `matched_entity_ids`

## 4. Source 1 Audit

### 4.1 Source 1 files

- Training: `dataset/train/train_source1.tsv`
- Test: `dataset/test/test_source1.tsv`

### 4.2 Source 1 record counts

Confirmed counts:

- `train_source1.tsv`: 2,206,821 data rows (header plus 2,206,822 lines total)
- `test_source1.tsv`: 1,732,544 data rows (header plus 1,732,545 lines total)

### 4.3 Source 1 fields

Confirmed field list:

1. `entity_id`
2. `business_name`
3. `business_address`
4. `country`

### 4.4 Source 1 identifier and duplicates

Confirmed evidence from the training file:

- `entity_id` values are unique in the inspected training Source 1 file.
- Duplicate `entity_id` values were not observed in the training Source 1 file during the stream-based inspection.
- The source of record identity is the prefix and the file membership; the README explicitly states that there is no separate source column.

Unknown / requires verification:

- Exact duplicate count across the test Source 1 file.
- Exact missing-value percentages for every field in every Source 1 file beyond the inspected training file.

### 4.5 Source 1 field semantics

- `entity_id`: identifier for a business record, source encoded by prefix.
- `business_name`: business name text; may contain abbreviations, legal suffixes, punctuation differences, transliterations, or typos.
- `business_address`: address text; may be partial, noisy, or formatted differently across sources.
- `country`: country label; docs say it is an open set and test data includes `France` in addition to US/India.

### 4.6 Source 1 data integrity observations

Confirmed for `train_source1.tsv` from the streaming inspection:

- `entity_id`: 0 empty values
- `business_name`: 0 empty values
- `business_address`: 0 empty values
- `country`: 0 empty values
- Unique `entity_id` count equals row count in the training file.
- Country counts in the training Source 1 file: `US` = 1,323,633 and `India` = 883,188.

This indicates the training Source 1 file contains only valid, non-empty basic fields under the inspected sample; however, it does not prove that all records are semantically perfect or that the same pattern holds for test data.

## 5. Source 2 Audit

### 5.1 Source 2 files

- Training: `dataset/train/train_source2.tsv`
- Test: `dataset/test/test_source2.tsv`

### 5.2 Source 2 record counts

Confirmed counts:

- `train_source2.tsv`: 5,034,616 data rows (header plus 5,034,617 lines total)
- `test_source2.tsv`: 4,887,273 data rows (header plus 4,887,274 lines total)

### 5.3 Source 2 fields

Confirmed field list:

1. `entity_id`
2. `business_name`
3. `business_address`
4. `country`

### 5.4 Source 2 identifier and duplicates

Confirmed via official docs and file inspection:

- `entity_id` values use the `S2-` prefix.
- There is no separate `source` column; the source is inferred from the prefix and file path.

Unknown / requires verification:

- Exact duplicate-identifier counts in Source 2 training and test datasets.
- Exact missing-value counts and percentages for each field across all Source 2 records.

### 5.5 Source 2 field semantics

- `entity_id`: unique identifier for a Source 2 record.
- `business_name`: name text; docs indicate noise patterns, abbreviations, transliterations, legal suffix variations, and punctuation differences.
- `business_address`: address text; may contain incomplete or noisy components.
- `country`: country label; docs state the training data covers `US` and `India`, and `France` appears in the test set.

## 6. Source 3 Audit

### 6.1 Source 3 files

- Training: `dataset/train/train_source3.tsv`
- Test: `dataset/test/test_source3.tsv`

### 6.2 Source 3 record counts

Confirmed counts:

- `train_source3.tsv`: 5,285,603 data rows (header plus 5,285,604 lines total)
- `test_source3.tsv`: 5,082,316 data rows (header plus 5,082,317 lines total)

### 6.3 Source 3 fields

Confirmed field list:

1. `entity_id`
2. `business_name`
3. `business_address`
4. `country`

### 6.4 Source 3 identifier and duplicates

Confirmed via official docs and file inspection:

- `entity_id` values use the `S3-` prefix.
- There is no separate `source` column; the source is inferred from the file and prefix.

Unknown / requires verification:

- Exact duplicate-identifier counts in Source 3 training and test datasets.
- Exact missing-value counts and percentages for each field across all Source 3 records.

### 6.5 Source 3 field semantics

The semantics match the same source schema as S1 and S2:

- `entity_id`: unique record identifier for S3.
- `business_name`: noisy business name description.
- `business_address`: potentially partial or inconsistent address string.
- `country`: country label, with France appearing in the test set.

## 7. Training Data Audit

### 7.1 Training files identified

Confirmed training data files:

- `dataset/train/train_source1.tsv`
- `dataset/train/train_source2.tsv`
- `dataset/train/train_source3.tsv`
- `dataset/train/train_ground_truth.tsv`

### 7.2 What the training data represents

The README and challenge statement state that:

- The training data consists of business records across three sources with ground-truth matching labels.
- Source 1 is the deduplicated reference source.
- The ground-truth file associates each Source 1 entity to one or more matching Source 2 / Source 3 IDs.

This means the training data contains source-record rows plus a separate matching-label file, not a single combined training table.

### 7.3 Training ground-truth structure

Observed ground-truth file column names:

- `source1_entity_id`
- `matched_entity_ids`

Observed example rows:

- `S1-965667	S2-681193310,S2-743505751,S3-775321672,S3-11291185,S3-860443364`
- `S1-55344266	S2-249013014,S2-197070651,S3-478195123,S3-384364074`

This confirms the ground truth is a per-Source-1 match list, not a pairwise table or cluster table.

### 7.4 Positive vs. negative matches and missing labels

Confirmed by the data format and challenge text:

- `matched_entity_ids` is a comma-separated list of IDs for matched records.
- Empty matches indicate no matches (singleton Source 1 entities).
- The format explicitly supports both matched and unmatched Source 1 records.

The challenge statement also states that Source 1 may match zero, one, or many records from Sources 2 and 3.

### 7.5 Linkage to source datasets

Confirmed relationship:

- `source1_entity_id` values are expected to refer to records in `train_source1.tsv`.
- `matched_entity_ids` values are expected to refer to records in `train_source2.tsv` and/or `train_source3.tsv`.

The README states that `matched_entity_ids` must contain only Source 2 and Source 3 IDs.

### 7.6 Training data integrity observations

Confirmed facts from the training ground-truth file:

- The file is a TSV with 2 columns.
- It contains 2,206,821 rows after the header.
- It is a list-of-match-IDs representation, not a full paired record table.

Unknown / requires verification:

- Exact duplicate counts in `matched_entity_ids` lists.
- Whether any `source1_entity_id` values are missing or duplicated.
- Whether any match IDs fail to appear in `train_source2.tsv` or `train_source3.tsv`.

## 8. Test Data Audit

### 8.1 Test files identified

Confirmed files:

- `dataset/test/test_source1.tsv`
- `dataset/test/test_source2.tsv`
- `dataset/test/test_source3.tsv`

### 8.2 Test record counts

Confirmed counts:

- `test_source1.tsv`: 1,732,544 data rows
- `test_source2.tsv`: 4,887,273 data rows
- `test_source3.tsv`: 5,082,316 data rows

### 8.3 Test file schema

Confirmed schema for all three test source files:

- `entity_id`
- `business_name`
- `business_address`
- `country`

This matches the training source schema.

### 8.4 Test source identity and labels

Confirmed from README:

- No ground truth is provided for the test set.
- The challenge requires generating matches for every `S1` entity in the test set.
- The system must not treat the test set as labeled data.

Confirmed country coverage in test data from the README and inspected rows:

- The training data has `US` and `India`.
- The test data includes a third country, `France`, which does not appear in the training data.

### 8.5 Observed test country examples

Examples from inspected rows included `France` values in Source 2 test records, confirming that the test set is not limited to the training countries.

## 9. Ground-Truth Audit

### 9.1 Ground-truth file identified

- `dataset/train/train_ground_truth.tsv`

### 9.2 Ground-truth file structure

Confirmed structure:

- 2 columns: `source1_entity_id`, `matched_entity_ids`
- Row count: 2,206,821 rows after header
- Delimiter: tab
- Format: one row per Source 1 entity
- `matched_entity_ids` is a comma-separated list of IDs from S2 and/or S3

### 9.3 Representation of matching relationships

The ground-truth file appears to represent record-level matching relationships in the format:

- Source 1 entity ID -> one or more Source 2 / Source 3 entity IDs.

This is consistent with the challenge statement that Source 1 is the deduplicated reference and can match to zero, one, or many records in the other sources.

### 9.4 Linkage to source datasets

Confirmed by docs and names:

- `source1_entity_id` is expected to be an `entity_id` from `train_source1.tsv`.
- The values in `matched_entity_ids` are expected to be IDs from `train_source2.tsv` and/or `train_source3.tsv`.

Unknown / requires verification:

- Whether every ground-truth ID exists in the source files.
- Whether any ground-truth entries are duplicates or malformed.

### 9.5 Integrity observations

The file uses a list format, which is valid for the challenge rules. However, the audit did not establish a full set of integrity checks for missing or invalid IDs in all rows, so those are marked as unknown unless verified.

## 10. Data Integrity Findings

### 10.1 Confirmed integrity observations

Confirmed from the inspected training Source 1 file:

- `entity_id` is populated for all rows in the inspected training file.
- `business_name` is populated for all rows in the inspected training file.
- `business_address` is populated for all rows in the inspected training file.
- `country` is populated for all rows in the inspected training file.
- No duplicate `entity_id` values were observed in the training Source 1 file.
- Country distribution in training Source 1: `US` = 1,323,633; `India` = 883,188.

Confirmed by the README and data format:

- Tabs are used as field separators because business addresses and ID lists contain commas.
- The challenge expects comma-separated ID lists without quoting.

### 10.2 Unknown or unverified integrity issues

These require explicit verification before being used in the SRS:

- Exact empty-string counts in `business_address` and `country` for all source and test files.
- Duplicate `entity_id` counts in S2 and S3 training and test files.
- Duplicate IDs within `matched_entity_ids` lists in the ground-truth file.
- Ground-truth references pointing to nonexistent S2/S3 records.
- Source overlap or duplicate business records across S1/S2/S3 at the record level.

### 10.3 Representative examples of observed values

Representative values from inspected rows include:

- `S1-925783039	Orelee's Barbershop	1795 Westchester Drive, High Point, NC	US`
- `S2-192345572	Brahma Infosoft	COIMATORE COLONY, HUNSUR TQMYSORE DIST., Karnataka	India`
- `S3-462677478	मॉडर्न फाइनेंस	No 10 Enkay Square, 448A, Udyog Vihar Phase V, Gurugram, Gurgaon, HR	India`
- `S2-566025912	Marina Ecole France Sarl	63 R. DE DIEPPE, LILLE, Hauts-de-France	France`

These examples support the documented claim that name, address, and country fields are noisy and vary by source and country.

## 11. Cross-File Relationships

### 11.1 Verified relationships

- All source files share the same basic schema.
- The ground-truth file is explicitly defined in the project documentation as a mapping from Source 1 to matching Source 2 and Source 3 records.
- The source of each row is determined by the `entity_id` prefix (`S1-`, `S2-`, `S3-`) and the file it appears in.
- The training data and test data use the same source file structure.

### 11.2 Inferences and assumptions to be treated carefully

- It is likely that the same real-world business can appear in multiple files, but the exact overlap cannot be fully established without a complete validation script.
- It is likely that each `entity_id` is unique only within a source, not necessarily globally across all three sources, because the prefix differentiates sources. This is supported by the naming convention but not fully enumerated here.
- It is likely that the training and test files share a common schema, because the README explicitly states the same columns exist for the source files and the files have the same headers. This is confirmed for the inspected files.

## 12. Official Requirements Cross-Check

### 12.1 Official requirements that match the observed data

The project documentation and the actual files align on the following:

- Source files are TSV files.
- Each source file contains `entity_id`, `business_name`, `business_address`, and `country`.
- The source is identified by prefix and file.
- Source 1 is the deduplicated reference source.
- `train_ground_truth.tsv` is a two-column mapping file.
- Match lists are comma-separated ID strings.
- The test data does not supply labels.
- Country is an open string label and must not be hard-coded to only US/India.

### 12.2 Official requirements that are not directly verifiable from the data alone

The project text gives the challenge rules, but the dataset itself cannot prove:

- Whether all source IDs are globally unique across S1/S2/S3 beyond the prefix convention.
- Whether every ground-truth match ID is valid against the source files.
- Whether there are any malformed or special-case values in every row, especially across very large files.

### 12.3 Potential mismatch or ambiguity

There is no direct evidence from the dataset itself of a formal schema definition beyond the README and challenge statement. The official documentation is therefore the authority for the required fields, while the data files are the evidence of the observed structure.

## 13. Confirmed Facts

1. The challenge uses three source datasets with source-specific IDs (`S1-`, `S2-`, `S3-`).
2. All source files observed in the project use TSV format with the same four fields: `entity_id`, `business_name`, `business_address`, `country`.
3. The training ground-truth file is a two-column TSV mapping Source 1 IDs to Source 2/3 IDs as a comma-separated list.
4. Source 1 is explicitly described as the deduplicated reference source.
5. The test set includes `France` in addition to the training countries `US` and `India`.
6. The dataset is large and appears to be UTF-8 encoded, with multilingual and region-specific values present.
7. In the inspected training Source 1 file, all required basic fields were populated and no duplicate `entity_id` values were observed.

## 14. Inferences and Uncertainties

- The project appears to use a one-to-many reference design where S1 is the reference set and S2/S3 are additional records.
- The same business may appear multiple times across sources, but exact overlap counts are not fully audited here.
- Field-level null/empty counts across all files other than the inspected training Source 1 file remain unverified in this audit.
- Exact duplicate counts in S2/S3 and ground-truth references require a full validation script against the source files.

## 15. Questions Requiring Human Decisions

These are the questions that should be answered before finalizing SRS Section 5:

1. Should Section 5.10 define a canonical treatment for blank strings versus `NULL`/missing values in the input datasets?
2. Should the SRS describe `country` as an open set with examples (`US`, `India`, `France`) rather than as a closed enumeration?
3. Should the SRS explicitly state that Source 1 is the only source used as the reference key, while S2 and S3 only participate as matched records?
4. Should Section 5.5 and 5.7 document the ground-truth as a list-of-matches format rather than a pairwise record table, even though this is the observed representation?
5. Should the SRS explicitly note that the official documentation is the source of truth when the dataset exhibits large-file irregularities that are not yet fully enumerated?

## 16. Recommendations for SRS Section 5

1. Use the observed schema as the default input contract:
   - Source files: `entity_id`, `business_name`, `business_address`, `country`
   - Ground-truth file: `source1_entity_id`, `matched_entity_ids`
2. State clearly that `entity_id` prefixes determine the source (`S1-`, `S2-`, `S3-`).
3. State that Source 1 is the reference/source-of-truth side in the matching task.
4. Document that country is treated as an open textual label and that the official challenge explicitly calls out `France` in test data.
5. Document that a ground-truth row can contain zero or more IDs in `matched_entity_ids` and that empty lists indicate singleton S1 entities.
6. Include a validation requirement that all `matched_entity_ids` values refer to Source 2 or Source 3 IDs, and that no Source 1 IDs appear there.
7. Treat missing values and malformed ID lists as integrity checks to be validated, not assumed to be impossible.
8. Where exact statistics are not verified, mark them as “Unknown” or “Requires verification” rather than claiming a definitive rule.

## 17. Summary of the Evidence Used

This audit was produced from:

- `docs/problem_statement.md`
- `6ab10eb3b23ba_student_resource/student_resource/README.md`
- the file headers and sample rows from the dataset TSV files
- filesystem-level row and size checks performed on the project data without modifying any dataset files

This report intentionally avoids making rules that are not supported by the official challenge text or direct dataset inspection.
