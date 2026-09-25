# Dataset Analysis Summary

## Most important findings

1. The challenge uses seven actual TSV files in the expected structure: three training sources, three test sources, and one training ground-truth file.
2. Source 1 is the reference dataset, and the training ground truth maps each Source 1 record to a comma-separated list of Source 2 and/or Source 3 IDs.
3. The inspected Source 1 training file is structurally clean: all fields are populated, there are no empty values, and there are no duplicate `entity_id` values.
4. The dataset is large and heavily noisy at the text level: names and addresses vary by abbreviation, punctuation, transliteration, locale, and local business conventions.
5. The training data is US + India only; the test set adds France across all three sources.
6. The ground-truth file is not a trivial one-to-one mapping. Many Source 1 entities have multiple matches, and some have both Source 2 and Source 3 matches.
7. Singletons are common enough to matter: 123,247 Source 1 training entities have empty match lists.
8. Exact IDs are unique within observed source files, so the main difficulty is not duplicate identifiers but matching semantically equivalent records under noise.

## Data quality highlights

- `train_source1.tsv`: 0 empty values in all four fields
- `train_source1.tsv`: duplicate `entity_id` count = 0
- `train_source2.tsv`: duplicate `entity_id` count = 0
- `train_source3.tsv`: duplicate `entity_id` count = 0
- `test_source2.tsv`: duplicate `entity_id` count = 0
- `test_source3.tsv`: duplicate `entity_id` count = 0
- `train_ground_truth.tsv`: 2,206,821 rows after header; unique `source1_entity_id` count = 2,206,821

## Ground-truth structure

- `train_ground_truth.tsv` rows with non-empty match lists: 2,083,574
- `train_ground_truth.tsv` rows with empty match lists: 123,247
- maximum match count per Source 1 entity: 11
- most common match counts: 3 and 4 matches per Source 1 entity
- `Source 2` and `Source 3` both appear in the same match list for 1,776,047 Source 1 rows

## Matching-related implications

- Candidate generation must handle both one-to-one and one-to-many matching.
- Exact-match candidate selection is not sufficient because abbreviation, transliteration, local formatting, mixed scripts, and legal-suffix differences are all present.
- Training-country assumptions are not safe for the test set because France is present.
- Precision matters greatly: the evaluation metric is F_0.5, so false positive merges are more damaging than missed matches.

## Recommended next step

The next project step should be careful feature and candidate-generation analysis, not model training. The immediate goal is to define and validate a normalization plus candidate-generation strategy that preserves recall while controlling candidate explosion, especially for repeated generic names and partial addresses.
