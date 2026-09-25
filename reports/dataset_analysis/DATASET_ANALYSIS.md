# Dataset Analysis for the Business Entity Resolution Challenge

Date: 2026-09-26
Repository root: `/home/vikaspal/Desktop/ml_chl`

## 1. Scope and evidence

This analysis is based on direct inspection of the actual files in:

- `6ab10eb3b23ba_student_resource/student_resource/dataset/train/`
- `6ab10eb3b23ba_student_resource/student_resource/dataset/test/`
- the challenge requirements in `docs/problem_statement.md`
- the project README at `6ab10eb3b23ba_student_resource/student_resource/README.md`

The analysis is intentionally limited to dataset understanding and does not implement a model, pipeline, blocking system, or output generation.

## 2. File inventory and schema

The project contains seven actual TSV files, matching the documented structure:

| Split | File | Rows | Observed schema |
| --- | --- | ---: | --- |
| train | `train_source1.tsv` | 2,206,822 total lines; 2,206,821 data rows | `entity_id`, `business_name`, `business_address`, `country` |
| train | `train_source2.tsv` | 5,034,617 total lines; 5,034,616 data rows | `entity_id`, `business_name`, `business_address`, `country` |
| train | `train_source3.tsv` | 5,285,604 total lines; 5,285,603 data rows | `entity_id`, `business_name`, `business_address`, `country` |
| train | `train_ground_truth.tsv` | 2,206,822 total lines; 2,206,821 data rows | `source1_entity_id`, `matched_entity_ids` |
| test | `test_source1.tsv` | 1,732,545 total lines; 1,732,544 data rows | `entity_id`, `business_name`, `business_address`, `country` |
| test | `test_source2.tsv` | 4,887,274 total lines; 4,887,273 data rows | `entity_id`, `business_name`, `business_address`, `country` |
| test | `test_source3.tsv` | 5,082,317 total lines; 5,082,316 data rows | `entity_id`, `business_name`, `business_address`, `country` |

Representative rows confirm the schema and value patterns:

- `S1-925783039	Orelee's Barbershop	1795 Westchester Drive, High Point, NC	US`
- `S2-166376419	राम मार्केटिंग प्राइवेट लिमिटेड	KH NO. -570/13, NEW DELHI, WEST DELHI, Delhi	India`
- `S3-202863386	wilfordhancock.com	Mack Rd, Haltom City, Texas	US`
- `S1-965667	S2-681193310,S2-743505751,S3-775321672,S3-11291185,S3-860443364`

The dataset is therefore a classic one-to-many entity-resolution task centered on Source 1 as the reference set, with Source 2 and Source 3 as candidate match sources.

## 3. Data quality and integrity

### 3.1 Confirmed integrity on the inspected Source 1 training file

A full pass over `train_source1.tsv` produced the following verified results:

- `entity_id`: 0 empty values
- `business_name`: 0 empty values
- `business_address`: 0 empty values
- `country`: 0 empty values
- unique `entity_id` count = row count = 2,206,821
- duplicate `entity_id` values = 0

This means the inspected training Source 1 file is structurally clean at the field-population and identifier-uniqueness level.

### 3.2 Country coverage

The observed country labels are:

| File | Country counts |
| --- | --- |
| `train_source1.tsv` | US = 1,323,633; India = 883,188 |
| `train_source2.tsv` | US = 3,016,817; India = 2,017,799 |
| `train_source3.tsv` | US = 3,170,056; India = 2,115,547 |
| `test_source1.tsv` | US = 663,106; India = 809,986; France = 259,452 |
| `test_source2.tsv` | US = 1,871,330; India = 2,312,565; France = 703,378 |
| `test_source3.tsv` | US = 1,945,701; India = 2,405,000; France = 731,615 |

The training split is confirmed to be US + India only. The test split adds France, which is a documented challenge feature and is present across all three test sources.

### 3.3 Exact-ID uniqueness across the full observed source files

Additional direct checks for Source 2 and Source 3 show that:

- `train_source2.tsv`: unique IDs = 5,034,616; duplicate IDs = 0
- `train_source3.tsv`: unique IDs = 5,285,603; duplicate IDs = 0
- `test_source2.tsv`: unique IDs = 4,887,273; duplicate IDs = 0
- `test_source3.tsv`: unique IDs = 5,082,316; duplicate IDs = 0

The same pattern holds for Source 1 training and test files: exact duplicate `entity_id` values are not present in the observed source files.

### 3.4 Ground-truth integrity

For `train_ground_truth.tsv`:

- total rows after header: 2,206,821
- `source1_entity_id` unique count: 2,206,821
- duplicate `source1_entity_id` values in the ground-truth: 0
- rows with non-empty `matched_entity_ids`: 2,083,574
- rows with empty `matched_entity_ids`: 123,247

That means 5.6% of Source 1 training entities are singletons (empty match list), while 94.4% have at least one positive match. This is a major challenge fact because the scoring metric treats correct singleton predictions as full-credit cases.

## 4. Business name analysis

### 4.1 Name format and structure

The business name field contains mixed-language, mixed-script, and structurally varied values. Examples include:

- `Orelee's Barbershop`
- `राम मार्केटिंग प्राइवेट लिमिटेड`
- `wilfordhancock.com`
- `Marina Ecole France Sarl`
- `मॉडर्न फाइनेंस`

These examples show the field is not limited to Latin script and includes transliteration, legal suffixes, abbreviations, and informal or brand-style naming.

### 4.2 Exact repetition and common naming patterns

A 50k-row sample from `train_source1.tsv` showed repeated exact names. The most common examples in that sample were:

- `Chiropractic Group` (9 occurrences)
- `Internal Medicine Group` (8)
- `Primary Care Group` (7)
- `Meridian LLC` (7)
- `Urgent Care Physicians LLC` (6)

This tells us that many businesses are not unique in the name field alone, and that generic, corporate, or group-style names can create ambiguity. These patterns matter because name-only matching would produce many false positives.

### 4.3 Token-level patterns

From the same 50k-row sample of `train_source1.tsv`, the most frequent normalized tokens were:

- `limited` (11,921)
- `private` (9,890)
- `llc` (8,078)
- `inc` (5,515)
- `ltd` (3,366)
- `pvt` (2,717)
- `associates` (998)
- `care` (1,257)
- `of` (990)
- `llp` (936)

This confirms that the dataset contains substantial legal-suffix variation and corporate naming conventions, including:

- `LLC`, `LLP`, `Inc`, `Ltd`, `Pvt`, `Private`, `Limited`
- mixed formatting such as `Pvt` vs `Private` vs `Limited`
- frequent multi-word business naming conventions like `Medical Group`, `Care`, `Associates`, `Office of ...`

### 4.4 Observed noise types in names

The actual data supports several variation classes beyond the challenge description:

- legal suffix inconsistency: `Pvt`, `Private`, `Limited`, `Ltd`, `LLC`, `LLP` 
- punctuation differences: apostrophes, periods, commas, slashes, ampersands, hyphens
- mixed scripts: Latin + Devanagari + Hindi + other scripts
- transliterated or locally branded names: `राम मार्केटिंग प्राइवेट लिमिटेड`
- short-form and brand names: `wilfordhancock.com`, `Marina Ecole France Sarl`
- repeated generic corporate names: `Care`, `Group`, `Office`, `Medical`, `Dental`, etc.

These patterns will create ambiguity unless candidate generation and matching features incorporate both lexical normalization and contextual context such as address or country.

## 5. Business address analysis

### 5.1 Address structure and noise

The address field is highly variable and often contains partial, noisy, localized, or region-specific formats. Examples include:

- `1795 Westchester Drive, High Point, NC`
- `KH NO. -570/13, NEW DELHI, WEST DELHI, Delhi`
- `Mack Rd, Haltom City, Texas`
- `COIMATORE COLONY, HUNSUR TQMYSORE DIST., Karnataka`
- `No 10 Enkay Square, 448A, Udyog Vihar Phase V, Gurugram, Gurgaon, HR`
- `63 R. DE DIEPPE, LILLE, Hauts-de-France`

This confirms that addresses are not normalized strings. They vary by:

- abbreviation style (`Rd`, `St`, `Ct`, `No`, `KH`, `R.`)
- component ordering
- missing postal codes or state names
- local formatting conventions and transliteration
- landmark or locality references
- mixed language and region-specific labels

### 5.2 Address repetition and token patterns

In a 50k-row sample of `test_source2.tsv`, the repeated exact addresses are rare, but some address tokens are highly frequent. The dataset clearly contains numerous region-specific locality references and component variations like:

- `Road`, `Street`, `No`, `Plot`, `Sector`, `Near`, `Colony`, `Town`, `District`, `Maharashtra`, `Tamil Nadu`, `Uttar Pradesh`

This matters for candidate generation because exact address matches can be useful but are not reliable enough by themselves, especially in multi-country and multi-source data.

### 5.3 Address ambiguity risk

Some businesses may share the same street neighborhood, city, or locality string while representing different businesses. Repeated names and repeated generic localities can create false positives if matching is based only on address tokens without name or country context.

The dataset shows that the challenge is not only about textual noise but also about the fact that many addresses are partial and overloaded across multiple businesses.

## 6. Cross-source comparisons

### 6.1 Source 1 as the anchor set

The evidence supports the challenge description that Source 1 is the deduplicated reference source. This is not only documented in the README; it is also reflected in the ground truth structure, which maps each Source 1 record to one or more Source 2/3 IDs.

### 6.2 Source-specific naming conventions

The data shows source-dependent writing habits:

- Source 2 and 3 include more Hindi-language and local-language business names than Source 1.
- Source 1 tends to include more conventional English-style names and legal-suffix patterns.
- Source 2 and 3 may include more localized address formats, such as `KH NO.`, `Colony`, `District`, and Indian locality patterns.
- Test includes France entries with French business names and addresses, which are not present in training.

### 6.3 Cross-source overlap is meaningful but not exact-match dominated

The ground-truth file confirms that many Source 1 entities have multiple matching Source 2 and/or Source 3 records. The distribution is not trivial: for training, match counts vary from 1 to 11, and the most common counts include 3 and 4 matches. This reflects real-world multi-match scenarios rather than simple one-to-one matching.

### 6.4 Structural evidence of candidate-generation difficulty

The full training ground truth shows:

- 2,083,574 records with at least one match
- 123,247 singleton Source 1 entities
- 1,776,047 Source 1 rows with at least one match in both S2 and S3
- 1,919,076 rows with at least one S2 match
- 1,940,545 rows with at least one S3 match

This means the dataset is not sparse: many Source 1 entities are matched to multiple records, and a large fraction have matches in both Source 2 and Source 3.

## 7. Ground-truth analysis

### 7.1 Ground-truth representation

The ground truth is a two-column TSV:

- `source1_entity_id`
- `matched_entity_ids`

The second field is a comma-separated list of Source 2 and/or Source 3 IDs. There is no separate pairwise row for each match; instead, each Source 1 entity is represented once, with a list of all matching IDs.

This is a key design fact for both evaluation and validation.

### 7.2 Match-count distribution

From the training ground-truth file:

| Match count per S1 row | Count |
| --- | ---: |
| 1 | 119,157 |
| 2 | 375,212 |
| 3 | 530,841 |
| 4 | 484,115 |
| 5 | 321,957 |
| 6 | 164,868 |
| 7 | 63,968 |
| 8 | 18,680 |
| 9 | 4,205 |
| 10 | 534 |
| 11 | 37 |

The distribution is broad and heavy-tailed. Many S1 entities have multiple matches, which means candidate generation must support multi-match cases rather than assuming one-to-one pairing.

### 7.3 Singleton behavior

The training set contains 123,247 singleton Source 1 entries. These are important because false positives on singletons are heavily penalized by F_0.5.

This fact strongly suggests that a robust solution should not aggressively match every Source 1 record; it should rely on strong evidence and carefully calibrated candidate selection.

## 8. Actual noise and variation patterns discovered

### Pattern 1: legal-suffix and corporate naming variability

Observed evidence:

- `LLC`, `LLP`, `Inc`, `Ltd`, `Pvt`, `Private`, `Limited`
- `Pvt` and `Private` represent the same concept in different sources
- `Medical Group`, `Primary Care Group`, `Dental Group`, `Associates`, `Office of ...`

Impact: name-normalization must account for legal suffix differences and generic corporate descriptors, or candidate generation becomes too restrictive.

### Pattern 2: mixed scripts and multilingual names

Observed evidence:

- `राम मार्केटिंग प्राइवेट लिमिटेड`
- `मॉडर्न फाइनेंस`

Impact: matching features must handle Unicode text, transliteration, or language-specific tokens; naive ASCII-only normalization would miss valid matches.

### Pattern 3: localized address formatting and abbreviated components

Observed evidence:

- `KH NO. -570/13, NEW DELHI, WEST DELHI, Delhi`
- `Mack Rd, Haltom City, Texas`
- `No 10 Enkay Square, 448A, Udyog Vihar Phase V, Gurugram, Gurgaon, HR`

Impact: address matching must tolerate abbreviation, reordering, and country-specific formatting.

### Pattern 4: country-specific and region-specific geographic labels

Observed evidence:

- US records include many US city/state patterns.
- Indian records include `Tamil Nadu`, `Maharashtra`, `Uttar Pradesh`, and localized Indian address language.
- French records appear in the test set and use French locality and naming conventions.

Impact: country and geography are useful context features, but they cannot be treated as a closed set of just US/India. France is part of the test domain.

### Pattern 5: repeated generic names across distinct records

Observed evidence from the first 50k rows of `train_source1.tsv`:

- `Chiropractic Group` appears 9 times
- `Internal Medicine Group` appears 8 times
- `Primary Care Group` appears 7 times

Impact: generic names produce ambiguity and require additional evidence from address and country to resolve correctly.

### Pattern 6: partial or incomplete addresses

Observed evidence:

- many addresses are missing postal codes or country-specific locality detail
- repeated neighborhoods or cities do not uniquely identify a business

Impact: candidate-generation features that overuse address text without name context can create high false-positive rates.

## 9. Matching ambiguity and difficulty

Several dataset characteristics make the problem difficult:

1. Generic or repeated names are common, especially in healthcare and service-sector businesses.
2. Addresses are often partial and cannot resolve many ambiguous name matches by themselves.
3. Source 2 and 3 names often contain localized or transliterated text that differs from Source 1.
4. The same Source 1 entity may match multiple S2/S3 records, and the match count distribution is wide.
5. The test set includes a third country, France, which is absent from training.
6. The F_0.5 metric penalizes false merges very strongly, so aggressive merging is riskier than missing some matches.

The evidence therefore supports the conclusion that the challenge is primarily a precision-sensitive entity-resolution problem, not a simple exact-match problem.

## 10. Candidate-generation feasibility

Even without implementing a blocking system, the dataset strongly suggests the following:

- The full cross-source comparison space is enormous: S1 rows are about 2.2M, with S2 and S3 together over 10M rows.
- Exact-name or exact-address blocking alone would create large candidate sets or miss matches when names and addresses vary by source and country.
- Candidate generation should rely on a combination of approximate textual similarity, country compatibility, token normalization, and perhaps source-specific normalization strategies.
- Generic names and repeated localities are the main sources of candidate explosion.
- The risk of under-generation is high if the blocking logic is too strict, because valid matches may be missing due to transliteration, abbreviation, localization, or formatting differences.

The important design implication is that candidate generation must preserve recall while still controlling the search space; the data supports a candidate set that is rich enough to include true matches but not so broad that it becomes computationally infeasible.

## 11. Training vs. test distribution comparison

The evidence clearly shows that the train and test splits differ in geography and possibly in naming/address style.

### Confirmed differences

- Train countries: US and India only.
- Test countries: US, India, and France.
- France appears in test data at significant scale: 259,452 in S1, 703,378 in S2, 731,615 in S3.

This matters because a model or heuristic trained only on US/India observations may underperform on French records if it relies too heavily on training-country priors.

### Additional distribution differences

The training and test source counts are different in absolute volume and in the relative contribution of each source:

- Train S1: 2,206,821
- Train S2: 5,034,616
- Train S3: 5,285,603
- Test S1: 1,732,544
- Test S2: 4,887,273
- Test S3: 5,082,316

The country distribution and absolute source counts show that the challenge is not a trivial static benchmark. Generalization to France and to source-specific naming conventions is necessary.

## 12. Additional discoveries

Several additional characteristics are worth noting:

- The dataset is large enough that exact pairwise comparison is infeasible; the challenge is by design about efficient candidate generation.
- Source 1 records have unique IDs and no empty fields in the inspected training data, which implies the main difficulty is not missing identifiers but textual and semantic mismatch.
- Ground truth is a mapping from S1 to many S2/S3 records, not a list of pairwise edges.
- The business name and address fields are genuinely noisy and need normalization beyond simple lowercasing.
- Exact duplicate ID counts are zero in the observed files, which means the main risk is false merge rather than duplicate ID collisions.

## 13. Conclusions

The dataset is a real-world, noisy multi-source business entity-resolution task with the following confirmed characteristics:

- one-to-many S1-to-S2/S3 matching
- large scale and high data volume
- exact identifier uniqueness within source files
- no empty fields in the inspected Source 1 training dataset
- multi-country generalization required, including France in test
- significant business-name and address variability
- a ground-truth representation built around Source 1 as the reference entity set
- high precision sensitivity because F_0.5 rewards careful merging and punishes false positive matches

The core implication for future technical design is that this is not a simple fuzzy-match task: it is a structured entity-resolution problem that requires robust normalization, careful candidate generation, and a precision-conscious final decision process.

## 14. Limitations and uncertainties

This analysis did not attempt to build or validate a production blocking or matching model. The following are explicitly left as unresolved unless further validation is run:

- exact duplicate names and addresses across the entire dataset beyond sample-based checks
- exact field completeness across all files beyond Source 1 training inspection
- exact validation of every candidate relationship against the full file graph
- full distributional modeling for every token and entity family across all rows

These are not contradictions of the observed data; they are simply areas that require focused follow-up verification if a specific design decision depends on them.
