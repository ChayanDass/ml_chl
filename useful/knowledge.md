# Knowledge Base

## Dataset facts confirmed from direct inspection

- The project contains seven TSV files: three training source files, three test source files, and one training ground-truth file.
- Every observed source file has the same schema: `entity_id`, `business_name`, `business_address`, `country`.
- The training ground-truth file has exactly two columns: `source1_entity_id` and `matched_entity_ids`.
- Source 1 is the reference dataset, and the right-hand side of the ground truth contains Source 2 and/or Source 3 IDs only.
- Training data is US + India only; the test split adds France.
- The training Source 1 file has no empty values in any of its four fields and no duplicate `entity_id` values.
- Duplicate `entity_id` values are not present in the observed Source 2 and Source 3 files either.
- The ground-truth mapping is list-based, not pairwise. Each Source 1 entity appears once with a comma-separated list of matching Source 2/3 IDs.

## Important variation patterns discovered

- Business names include legal-suffix variation (`LLC`, `LLP`, `Ltd`, `Private`, `Limited`, `Pvt`) and corporate templates like `Group`, `Associates`, and `Office of ...`.
- Business names are multilingual and mixed-script; examples include Hindi and other non-Latin strings in the data.
- Addresses vary widely by abbreviation, region, ordering, landmark references, and partial information. They are not normalized strings.
- Generic repeated names increase ambiguity and make name-only matching unsafe.
- Partial or local addresses can be highly similar across different businesses, especially in dense service sectors.

## Matching-related lessons

- A simple exact-match heuristic is insufficient because the data contains transliteration, punctuation changes, abbreviations, and source-specific formatting.
- Candidate generation must preserve recall for valid name/address variants while still controlling candidate explosion.
- The training labels include many multi-match cases, not just one-to-one matches.
- Singleton predictions are significant: a non-trivial portion of Source 1 entities has an empty match list.
- The evaluation metric is precision-heavy (`F_0.5`), so false merges are riskier than missed matches.

## Decisions and assumptions

- Verified: Source 1 is the reference set.
- Verified: The project expects open country labels and not a closed US/India-only set.
- Verified: `matched_entity_ids` is a comma-separated list, not a pairwise table.
- Open question: exact full-dataset duplicate-name and duplicate-address counts remain to be quantified if a specific normalization strategy depends on them.
- Open question: exact per-file completeness and malformed-row statistics beyond the inspected Source 1 training file should be validated before finalizing any strict data-quality constraints.

## Link to detailed analysis

See `docs/DATASET_ANALYSIS.md` for the full evidence-based write-up and supporting observations.
