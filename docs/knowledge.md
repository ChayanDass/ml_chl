# Dataset Investigation Findings

## 1. Dataset Structure and Scale

### 1.1 Source Structure

The challenge uses three business data sources:

* **Source 1 (S1):** The reference entity set. Every S1 entity must be matched against zero, one, or multiple entities from Source 2 and Source 3.
* **Source 2 (S2):** A candidate matching source.
* **Source 3 (S3):** A candidate matching source.

The ground truth maps each S1 entity to a comma-separated list of matching S2 and S3 entity IDs.

### 1.2 Dataset Sizes

| Split |  Source 1 |  Source 2 |  Source 3 |
| ----- | --------: | --------: | --------: |
| Train | 2,206,821 | 5,034,616 | 5,285,603 |
| Test  | 1,732,544 | 4,887,273 | 5,082,316 |

The training ground-truth file contains 2,206,821 records, corresponding to the training Source 1 entities.

### 1.3 Identifier Integrity

The dataset analysis reports that entity IDs are unique within the inspected source files, with no duplicate IDs found in the reported checks.

A full field-completeness check was explicitly documented for `train_source1.tsv`, where all four fields were populated and entity IDs were unique.

**Limitation:** Complete field-level missing-value verification across every file should not be considered established solely from the current report.

---

## 2. Geographic Coverage and Generalization

### 2.1 Country Distribution

The training split contains records from:

* United States (US)
* India

The test split contains records from:

* United States (US)
* India
* France

France is absent from the training split but appears at significant scale in all three test sources.

| Test source | France records |
| ----------- | -------------: |
| Source 1    |        259,452 |
| Source 2    |        703,378 |
| Source 3    |        731,615 |

### 2.2 Technical Implication

The solution must account for geographic generalization beyond the countries represented in training.

Country-aware processing may be useful, but the system must not assume that the only valid countries are the United States and India.

French business names and addresses introduce a test-domain variation that should be considered during normalization, candidate generation, and matching.

---

## 3. Ground-Truth Structure and Match Distribution

### 3.1 Ground-Truth Representation

The training ground truth contains two fields:

* `source1_entity_id`
* `matched_entity_ids`

The `matched_entity_ids` field contains a comma-separated list of matching S2 and S3 IDs. An empty list represents an S1 entity with no matching records.

Each S1 entity has one ground-truth row, and the matching relationship is one-to-many rather than strictly one-to-one.

### 3.2 Match Coverage

The reported training ground-truth statistics are:

| Category                                |     Count |
| --------------------------------------- | --------: |
| Total S1 entities                       | 2,206,821 |
| Entities with at least one match        | 2,083,574 |
| Entities with no matches                |   123,247 |
| Entities with at least one S2 match     | 1,919,076 |
| Entities with at least one S3 match     | 1,940,545 |
| Entities with matches in both S2 and S3 | 1,776,047 |

Approximately 94.4% of training S1 entities have at least one match, while approximately 5.6% have no matches.

### 3.3 Match-Count Distribution

| Number of matching records | S1 entity count |
| -------------------------- | --------------: |
| 1                          |         119,157 |
| 2                          |         375,212 |
| 3                          |         530,841 |
| 4                          |         484,115 |
| 5                          |         321,957 |
| 6                          |         164,868 |
| 7                          |          63,968 |
| 8                          |          18,680 |
| 9                          |           4,205 |
| 10                         |             534 |
| 11                         |              37 |

The reported number of matches per S1 entity ranges from 1 to 11 among entities with non-empty match lists.

### 3.4 Technical Implications

* Matching must support multiple valid records per S1 entity.
* The system must preserve the possibility that an S1 entity has no matches.
* Candidate generation and final matching must not assume a one-to-one relationship.
* False-positive matches are particularly important to control because the challenge uses precision-weighted F0.5 scoring.

---

## 4. Business Name Characteristics

### 4.1 Observed Naming Variations

The dataset contains:

* Legal suffixes and corporate designations such as `LLC`, `LLP`, `Inc`, `Ltd`, `Pvt`, `Private`, and `Limited`.
* Punctuation differences involving apostrophes, periods, commas, slashes, ampersands, and hyphens.
* Mixed-language and mixed-script names, including Devanagari.
* Brand-style names, abbreviated names, and domain-like names.
* Generic business descriptors such as `Care`, `Group`, `Medical`, `Dental`, `Associates`, and `Office`.

Examples include:

* `Orelee's Barbershop`
* `राम मार्केटिंग प्राइवेट लिमिटेड`
* `wilfordhancock.com`
* `मॉडर्न फाइनेंस`
* `Marina Ecole France Sarl`

### 4.2 Name Ambiguity

Repeated generic names occur in the dataset. A 50,000-row sample of training Source 1 contained repeated names such as:

* `Chiropractic Group`
* `Internal Medicine Group`
* `Primary Care Group`
* `Meridian LLC`
* `Urgent Care Physicians LLC`

This demonstrates that a business name alone may not uniquely identify an entity.

**Technical implication:** Name normalization and name similarity should be evaluated alongside address and geographic evidence. Generic names require particular care during candidate generation and final matching.

**Evidence limitation:** The reported name-frequency observations are sample-based and should not be interpreted as full-dataset frequency estimates.

---

## 5. Business Address Characteristics

### 5.1 Observed Address Variations

Addresses contain substantial formatting and structural variation, including:

* Abbreviations such as `Rd`, `St`, `Ct`, `No`, and `R.`
* Different ordering of street, locality, city, and regional components.
* Missing postal codes or other geographic details.
* Locality, landmark, district, colony, and sector references.
* Country-specific address conventions and mixed-language formatting.

Examples include:

* `1795 Westchester Drive, High Point, NC`
* `KH NO. -570/13, NEW DELHI, WEST DELHI, Delhi`
* `Mack Rd, Haltom City, Texas`
* `COIMATORE COLONY, HUNSUR TQMYSORE DIST., Karnataka`
* `63 R. DE DIEPPE, LILLE, Hauts-de-France`

### 5.2 Address Ambiguity

Addresses may be incomplete or shared across businesses in the same locality.

Exact address matching alone may miss valid matches, while broad address-token matching may introduce false positives.

**Technical implication:** Address normalization and similarity should account for abbreviations, component variation, and geographic context. Address evidence should be evaluated together with business-name evidence.

**Evidence limitation:** Some address repetition and token observations in the report are based on a 50,000-row sample of test Source 2 rather than a complete dataset-wide analysis.

---

## 6. Cross-Source Matching Characteristics

### 6.1 Source-Specific Variations

The dataset analysis reports differences in naming and address conventions across sources:

* Source 2 and Source 3 contain localized names and address formats, including Indian locality patterns.
* Source 1 contains conventional English-style business names and corporate suffix patterns.
* France appears in the test data with French names and addresses.

These are observed tendencies, not proof that every source follows a fixed naming convention.

### 6.2 Matching Implications

The following factors may contribute to cross-source matching difficulty:

* Legal-suffix and punctuation differences.
* Mixed scripts and language variation.
* Abbreviated or partial addresses.
* Generic names shared by different businesses.
* Multiple valid matches for a single S1 entity.
* Geographic variation between training and test data.

These observations support investigating multiple complementary candidate-generation strategies rather than relying exclusively on exact name or exact address equality.

---

## 7. Candidate-Generation Considerations

### 7.1 Scale Constraint

The combined training Source 2 and Source 3 datasets contain more than 10 million records. Exhaustive comparison of every S1 record against every S2 and S3 record would create an extremely large comparison space.

Candidate generation is therefore a central design requirement.

### 7.2 Risks to Investigate

Candidate generation must balance two competing risks:

1. **Under-generation:** True matches are excluded because of spelling, abbreviation, transliteration, address variation, or overly strict blocking.
2. **Over-generation:** Generic names, common locality tokens, or broad similarity criteria produce too many unrelated candidates.

### 7.3 Candidate-Generation Design Considerations

Potential approaches to investigate include:

* Normalized exact-name and exact-address matching.
* Country-aware candidate partitioning.
* Multiple complementary blocking strategies.
* Name and address similarity-based candidate retrieval.
* Handling of generic names and common geographic tokens.
* Candidate recall and candidate-set size measurement.

These are investigation directions, not finalized technical decisions.

**Important:** No candidate-generation strategy has been established as effective by the dataset analysis alone. Recall, candidate volume, and computational feasibility still require empirical validation.

---

## 8. Evaluation and Matching Principles

The challenge uses the precision-weighted F0.5 metric.

The ground truth contains both matched entities and entities with empty match lists. Consequently, a matching system must handle both positive and negative cases.

The following principles should guide future technical investigation:

* Avoid assuming every S1 entity has a match.
* Avoid assuming each S1 entity has only one match.
* Measure false-positive and false-negative behavior separately.
* Evaluate candidate-generation recall independently from final matching quality.
* Validate that output construction preserves all required matching IDs and correctly represents empty match lists.

These are design considerations derived from the challenge structure and reported ground-truth distribution.

---

## 9. Open Questions and Unverified Areas

The following items remain unresolved or require stronger evidence:

1. Full field-level completeness and missing-value counts across all seven TSV files.
2. Full-dataset distributions of exact duplicate business names and addresses.
3. Comprehensive cross-source name and address similarity distributions.
4. Validation of every ground-truth ID against the corresponding source files.
5. Detailed characterization of false-positive ambiguity among similar but unrelated businesses.
6. Candidate-generation recall and candidate-set size under alternative blocking strategies.
7. Full train/test distribution comparisons beyond country counts and source sizes.
8. Quantitative analysis of name and address differences for confirmed matching pairs.
9. Detailed evaluation of how French records differ from US and Indian records at the field and matching-pattern levels.

These questions should be investigated before their answers are used as firm technical-design assumptions.

---

## 10. Source of Findings

The findings in this section are based on the dataset investigation report dated 2026-09-26.

The report documents direct inspection of the dataset files, full-file ground-truth statistics, selected integrity checks, and sample-based text analysis.

Where a result is sample-based or incompletely verified, that limitation is explicitly retained rather than treating the result as a full-dataset fact.

For the detailed evidence, examples, and reported statistics, refer to `docs/DATASET_ANALYSIS.md`.
