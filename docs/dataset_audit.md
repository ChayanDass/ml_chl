# Dataset Audit: Multilingual and Data Quality Analysis of Entity Resolution Dataset

## 1. Executive Summary

This report presents a comprehensive, empirical audit of the business entity resolution dataset located at `/home/vikaspal/Desktop/ml_chl/6ab10eb3b23ba_student_resource`. The audit evaluated all **24,229,173 business records** across the 3 data sources (S1, S2, S3) in both training and test splits, as well as the **2,206,821 ground-truth reference records** representing **7,638,365 matched target pairs**.

### Key Findings:

1. **Source 1 Monolingual Script Rigidity**: Source 1 (S1) is **100.0% Latin script** across both the training dataset (2,206,821 records) and test dataset (1,732,544 records). It contains zero native Indic, Cyrillic, Arabic, or Han script business names or addresses.
2. **Multi-Script Heterogeneity in Source 2 and Source 3**: Source 2 (S2) and Source 3 (S3) contain significant non-Latin writing systems representing **471,061 records in train S2** (~9.36%), **241,857 records in train S3** (~4.58%), **544,657 records in test S2** (~11.14%), and **289,529 records in test S3** (~5.70%). Observed non-Latin scripts include **Devanagari, Tamil, Telugu, Kannada, Gujarati, Bengali, Malayalam, Odia, and Gurmukhi**.
3. **Cross-Script Transliteration Matches in Ground Truth**: Out of 7,638,365 ground-truth matched pairs in the training set, exactly **551,240 pairs (7.22%)** connect a Latin-script S1 entity to a non-Latin script S2 or S3 entity. The largest cross-script match group is **Latin vs Devanagari (312,725 pairs, 4.09%)**, followed by **Latin vs Telugu (45,620 pairs)**, **Latin vs Kannada (43,379 pairs)**, **Latin vs Tamil (39,252 pairs)**, and **Latin vs Gujarati (35,819 pairs)**.
4. **Severe Character N-gram and Token Retrieval Risk**: For cross-script matched entities (e.g. S1 `"Raj Investments LLP"` vs S2 `"ராஜ் இன்வெஸ்ட்மெண்ட்ஸ் எல்எல்பி"`), token Jaccard similarity and character trigram overlap are **0.0**. Standard character trigram indexing, exact/normalized lookup, and 64-dimensional character-trigram hash vectors share **zero overlapping features** across script boundaries.
5. **Address Asymmetry**: While business names in S2 and S3 frequently use native Indic scripts, business addresses in S2 and S3 are overwhelmingly **Latin script (>99.7%)**. This creates a critical cross-field signal where address-based retrieval can successfully bridge cross-script name mismatches.
6. **Country Coverage & Unseen Test Country**: Training data covers `US` and `India`. Test data introduces `France` (**703,378 S2 records**, **731,615 S3 records**, and **259,452 S1 records**). France records are 100% Latin script but feature French linguistic markers (e.g., `SARL`, `SAS`, `EURL`, `Société`, accented Latin characters `é`, `è`, `ê`, `à`, `ç`).
7. **Country Agreement Precision**: Ground-truth cross-source analysis reveals **100.0% country agreement** among matched pairs (0 country mismatches observed across all 7,638,365 ground-truth pairs).

---

## 2. Dataset Inventory and Verified Counts

### 2.1 File System and Schema Inventory

The dataset consists of 7 tab-separated values (`.tsv`) files split into `train` and `test` directories under `6ab10eb3b23ba_student_resource/student_resource/dataset`.

| File Path | Format | Size (Bytes) | Row Count (excl. Header) | Column Names | Data Types |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `train/train_source1.tsv` | UTF-8 TSV | 210,069,713 | **2,206,821** | `entity_id`, `business_name`, `business_address`, `country` | string, string, string, string |
| `train/train_source2.tsv` | UTF-8 TSV | 489,301,488 | **5,034,616** | `entity_id`, `business_name`, `business_address`, `country` | string, string, string, string |
| `train/train_source3.tsv` | UTF-8 TSV | 503,705,637 | **5,285,603** | `entity_id`, `business_name`, `business_address`, `country` | string, string, string, string |
| `train/train_ground_truth.tsv` | UTF-8 TSV | 127,015,583 | **2,206,821** | `source1_entity_id`, `matched_entity_ids` | string, comma-separated strings |
| `test/test_source1.tsv` | UTF-8 TSV | 175,022,086 | **1,732,544** | `entity_id`, `business_name`, `business_address`, `country` | string, string, string, string |
| `test/test_source2.tsv` | UTF-8 TSV | 509,456,422 | **4,887,273** | `entity_id`, `business_name`, `business_address`, `country` | string, string, string, string |
| `test/test_source3.tsv` | UTF-8 TSV | 506,002,772 | **5,082,316** | `entity_id`, `business_name`, `business_address`, `country` | string, string, string, string |

### 2.2 Total Record Counts

* **Training Set Total**: 12,527,040 business records (S1: 2,206,821; S2: 5,034,616; S3: 5,285,603)
* **Test Set Total**: 11,702,133 business records (S1: 1,732,544; S2: 4,887,273; S3: 5,082,316)
* **Grand Total Dataset Records**: **24,229,173** business records across all 6 source files.

### 2.3 Ground-Truth Structure and Match Distribution

`train_ground_truth.tsv` maps every S1 entity in the training split to zero, one, or multiple matching IDs in S2 and/or S3.

* **Total S1 Reference Entities in GT**: **2,206,821** (matches `train_source1.tsv` row count exactly).
* **Singleton S1 Entities (0 matches)**: **123,247** (5.58% of S1 entities).
* **Matched S1 Entities (>=1 match)**: **2,083,574** (94.42% of S1 entities).
* **Total Matched Candidate Pairs**: **7,638,365** pairs.
* **Average Matches per Matched S1 Entity**: 3.67 matched target records (S2/S3).

#### Ground Truth Match Cardinality Breakdown:

| Match Count per S1 Entity | S1 Record Count | Percentage of S1 Total |
| :--- | :--- | :--- |
| **0 matches (Singletons)** | 123,247 | 5.58% |
| **1 match** | 24,198 | 1.10% |
| **2 matches** | 224,960 | 10.19% |
| **3 matches** | 561,424 | 25.44% |
| **4 matches** | 711,283 | 32.23% |
| **5 matches** | 412,854 | 18.71% |
| **6+ matches** | 148,855 | 6.75% |

### 2.4 Missing, Empty, and Duplicate Values Audit

* **Entity IDs**: **0 duplicate entity IDs** found within any file. 100% of entity IDs follow the expected prefix format (`S1-`, `S2-`, `S3-`).
* **Business Names**: **0 missing or empty** business names across all 24.22 million records.
* **Country Labels**: **0 missing or empty** country values across all files.
* **Business Address Missingness**:
  * `train_source1.tsv`: 0 empty addresses (0.00%)
  * `train_source2.tsv`: **168,967 empty addresses** (3.36%)
  * `train_source3.tsv`: **175,916 empty addresses** (3.33%)
  * `test_source1.tsv`: 0 empty addresses (0.00%)
  * `test_source2.tsv`: **129,408 empty addresses** (2.65%)
  * `test_source3.tsv`: **136,098 empty addresses** (2.68%)

---

## 3. Language and Script Distributions by Source

### 3.1 Primary Writing Systems and Scripts Observed

The dataset contains characters from **10 distinct writing systems**:
1. **Latin** (Basic Latin + Latin Extended-A/B for French accents like `é`, `è`, `ê`, `à`, `ç`)
2. **Devanagari** (Hindi, Marathi, Sanskrit)
3. **Tamil**
4. **Telugu**
5. **Kannada**
6. **Gujarati**
7. **Bengali**
8. **Malayalam**
9. **Odia**
10. **Gurmukhi** (Punjabi)

### 3.2 Business Name Primary Script Distribution by Source File

Primary script is determined by the script of the majority of alphabetic characters in the string.

| Source File | Total Rows | Latin | Devanagari | Tamil | Telugu | Kannada | Bengali | Gujarati | Malayalam | Odia | Gurmukhi | Non-Letter |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **train_s1** | 2,206,821 | **2,206,821** (100.0%) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **train_s2** | 5,034,616 | **4,568,872** (90.75%) | 264,239 | 33,162 | 38,673 | 36,584 | 30,163 | 30,353 | 18,475 | 7,362 | 6,539 | 194 |
| **train_s3** | 5,285,603 | **5,022,977** (95.03%) | 148,343 | 18,775 | 21,731 | 20,833 | 17,114 | 16,928 | 10,536 | 4,088 | 3,855 | 423 |
| **test_s1** | 1,732,544 | **1,732,544** (100.0%) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **test_s2** | 4,887,273 | **4,350,108** (89.01%) | 303,467 | 38,310 | 44,429 | 43,203 | 34,964 | 34,713 | 21,673 | 8,534 | 7,761 | 111 |
| **test_s3** | 5,082,316 | **4,780,029** (94.05%) | 170,091 | 21,639 | 25,246 | 24,483 | 19,676 | 19,318 | 12,432 | 4,820 | 4,344 | 238 |

### 3.3 Business Address Primary Script Distribution

Address script distribution exhibits extreme asymmetry compared to business names:

* **S1 Addresses (train & test)**: **100.0% Latin script**.
* **S2 Addresses (train)**: 4,861,174 Latin (96.55%), 168,967 Empty (3.36%), 3,527 Devanagari (0.07%), 397 Tamil, 214 Bengali, 213 Telugu, 79 Gujarati, 40 Kannada, 5 Gurmukhi.
* **S3 Addresses (train)**: 5,096,039 Latin (96.41%), 175,916 Empty (3.33%), 10,442 Devanagari (0.20%), 1,345 Tamil, 812 Bengali, 610 Telugu, 267 Gujarati, 154 Kannada, 9 Malayalam, 8 Odia, 1 Gurmukhi.
* **S2 Addresses (test)**: 4,752,771 Latin (97.25%), 129,408 Empty (2.65%), 3,965 Devanagari (0.08%), 511 Tamil, 269 Bengali, 240 Telugu, 66 Gujarati, 41 Kannada, 1 Gurmukhi, 1 Odia.
* **S3 Addresses (test)**: 4,930,641 Latin (97.02%), 136,098 Empty (2.68%), 11,884 Devanagari (0.23%), 1,548 Tamil, 959 Bengali, 709 Telugu, 269 Gujarati, 181 Kannada, 16 Malayalam, 7 Gurmukhi, 4 Odia.

> [!IMPORTANT]
> Over **99.7% of non-empty addresses in S2 and S3 are written in Latin script**, even when the corresponding business name is written in Devanagari, Tamil, or Telugu!

---

## 4. Multilingual and Transliteration Patterns

### 4.1 Cross-Script Entity Equivalence

Ground-truth matching analysis reveals that many business entities in India are recorded in Latin script in Source 1, but in native Indic scripts in Source 2 or Source 3.

#### Measured Transliteration Patterns in Matched Entities:
1. **Full Transliteration / Romanization**:
   * S1 (Latin): `Raj Investments LLP`
   * S2 (Tamil): `ராஜ் இன்வெஸ்ட்மெண்ட்ஸ் எல்எல்பி`
   * Token Jaccard: **0.0**, Character Trigram Jaccard: **0.0**
2. **Partial Transliteration (Mixed Script)**:
   * S1 (Latin): `Raj Investments LLP`
   * S3 (Mixed Latin + Tamil): `Raj Investments எல்எல்பி`
   * Token Jaccard: **0.40**, Character Trigram Jaccard: **0.556**
3. **Devanagari Phonetic Equivalence**:
   * S1 (Latin): `Ram Marketing Private Limited`
   * S2 (Devanagari): `राम मार्केटिंग प्राइवेट लिमिटेड`
   * Token Jaccard: **0.0**, Character Trigram Jaccard: **0.0**

### 4.2 Legal Suffix Variations and Structural Noise

Business names across all sources exhibit heavy legal suffix variations:
* **Indian Legal Suffixes**: `Pvt Ltd`, `Private Limited`, `Pvt. Ltd.`, `LLP`, `Limited`, `Ltd`, `Inc`, `Co.`, `Company`.
* **French Legal Suffixes** (in test set): `SARL`, `S.A.R.L.`, `SAS`, `S.A.S.`, `EURL`, `SA`, `Société`, `Etablissements`.
* **US Legal Suffixes**: `Inc`, `Incorporated`, `LLC`, `L.L.C.`, `Corp`, `Corporation`, `Co`, `Company`.

---

## 5. Country and Language Analysis

### 5.1 Country Distribution across Data Sources

Country labels in training data are restricted to `US` and `India`. Test data introduces `France`.

| Source & Split | Country | Record Count | Percentage of Split |
| :--- | :--- | :--- | :--- |
| **train_source1** | US | 1,323,633 | 59.98% |
| **train_source1** | India | 883,188 | 40.02% |
| **train_source2** | US | 3,016,817 | 59.92% |
| **train_source2** | India | 2,017,799 | 40.08% |
| **train_source3** | US | 3,170,056 | 59.97% |
| **train_source3** | India | 2,115,547 | 40.03% |
| **test_source1** | India | 809,986 | 46.75% |
| **test_source1** | US | 663,106 | 38.27% |
| **test_source1** | **France** | **259,452** | **14.98%** |
| **test_source2** | India | 2,312,565 | 47.32% |
| **test_source2** | US | 1,871,330 | 38.29% |
| **test_source2** | **France** | **703,378** | **14.39%** |
| **test_source3** | India | 2,405,000 | 47.32% |
| **test_source3** | US | 1,945,701 | 38.28% |
| **test_source3** | **France** | **731,615** | **14.39%** |

### 5.2 Script Distributions within Countries

1. **United States (US)**: **100.0% Latin script** across all sources.
2. **France (France - Test Set)**: **100.0% Latin script** across all sources. Features French diacritics (`é`, `è`, `à`, `ç`, `ô`) and French street/legal terms (`Rue`, `Avenue`, `Boulevard`, `SARL`, `SAS`).
3. **India (India)**:
   * **S1**: **100.0% Latin script** (all Indian entities in S1 are romanized/transliterated).
   * **S2**: 76.9% Latin, 13.1% Devanagari, 1.9% Telugu, 1.8% Kannada, 1.6% Tamil, 1.5% Gujarati, 1.5% Bengali, 0.9% Malayalam, 0.4% Odia, 0.3% Gurmukhi.
   * **S3**: 88.0% Latin, 7.0% Devanagari, 1.0% Telugu, 1.0% Kannada, 0.9% Tamil, 0.8% Gujarati, 0.8% Bengali, 0.5% Malayalam, 0.2% Odia, 0.2% Gurmukhi.

---

## 6. Ground-Truth-Based Cross-Source Analysis

### 6.1 Script Combinations among Ground-Truth Matches

Analysis of **7,638,365 matched pairs** in `train_ground_truth.tsv`:

| S1 Script vs Target (S2/S3) Script | Matched Pair Count | Percentage of Total Matches | Matching Nature |
| :--- | :--- | :--- | :--- |
| **Latin vs Latin** | 7,087,125 | **92.78%** | Monolingual / Same Script |
| **Latin vs Devanagari** | 312,725 | **4.09%** | Cross-Script Transliteration |
| **Latin vs Telugu** | 45,620 | **0.60%** | Cross-Script Transliteration |
| **Latin vs Kannada** | 43,379 | **0.57%** | Cross-Script Transliteration |
| **Latin vs Tamil** | 39,252 | **0.51%** | Cross-Script Transliteration |
| **Latin vs Gujarati** | 35,819 | **0.47%** | Cross-Script Transliteration |
| **Latin vs Bengali** | 35,910 | **0.47%** | Cross-Script Transliteration |
| **Latin vs Malayalam** | 21,930 | **0.29%** | Cross-Script Transliteration |
| **Latin vs Odia** | 8,681 | **0.11%** | Cross-Script Transliteration |
| **Latin vs Gurmukhi** | 7,924 | **0.10%** | Cross-Script Transliteration |
| **Total Cross-Script Matches** | **551,240** | **7.22%** | **Cross-Script Transliteration** |

### 6.2 Lexical Similarity and Exact Matches in Ground Truth

* **Exact Name Match Rate**: **821,025 pairs (10.75%)**. 89.25% of true matches are not exact string matches.
* **Exact Address Match Rate**: **553,282 pairs (7.24%)**.
* **Country Agreement Rate**: **7,638,365 pairs (100.00%)**. **Zero country disagreements** observed in ground truth.

#### Token Jaccard Distribution among Matches:
* **1.0 (Exact Token Overlap)**: 2,118,064 pairs (27.73%)
* **0.80 - 0.99 (High Overlap)**: 303,318 pairs (3.97%)
* **0.50 - 0.79 (Medium Overlap)**: 3,457,398 pairs (45.26%)
* **0.20 - 0.49 (Low Overlap)**: 632,069 pairs (8.27%)
* **< 0.20 (Very Low Overlap / Cross-Script)**: **1,127,516 pairs (14.76%)**

---

## 7. Data Quality Findings and Anomalies

### 7.1 Unicode, Character Encoding, and Control Characters

* **Replacement Characters (`\ufffd`)**: **0 records** contain explicit Unicode replacement characters across all 24.2M rows.
* **ASCII Control Characters (`\x00-\x1f` excl. tab/newline)**:
  * `train_s1`: 69 records
  * `train_s2`: 118 records
  * `train_s3`: 125 records
  * `test_s1`: 72 records
  * `test_s2`: 183 records
  * `test_s3`: 162 records
* **Mojibake Sequences (e.g. `Ã©`, `Ã¢`, `â€™`)**:
  * `train_s1`: 453 records
  * `train_s2`: 1,118 records
  * `train_s3`: 800 records
  * `test_s1`: 405 records
  * `test_s2`: 4,046 records (higher in test due to French accented character encoding artifacts)
  * `test_s3`: 871 records

### 7.2 String Length Extremes

* **Business Name Lengths**:
  * Minimum: 1 character (e.g., `"A"`, `"3"`)
  * Average: 21.4 characters
  * Maximum: 384 characters
* **Business Address Lengths**:
  * Minimum: 0 characters (empty addresses in S2 and S3)
  * Average: 48.2 characters
  * Maximum: 612 characters

---

## 8. Implications for the Existing Matching Design

The system design documented in `approach_audit.md` consists of six candidate retrieval families, candidate unioning, 27 pairwise features, and LightGBM binary classification. Below is the systematic evaluation of each module against measured audit findings:

| Pipeline Component | Observed Evidence | Potential Impact on Matching | Current Frozen Design Status | Further Investigation Needed |
| :--- | :--- | :--- | :--- | :--- |
| **Method 1: Exact / Normalized Names** | 89.25% of GT matches are not exact matches; 551,240 GT matches are cross-script (Latin vs Indic). | Fails completely for cross-script pairs and spelling/suffix variations. Contributes ~10.75% recall ceiling on its own. | **Already Implemented**. Acts as precision anchor for identical strings. | Measure incremental recall on workstation benchmark. |
| **Method 2: Token-Based Names** | 1,127,516 GT matches have token Jaccard < 0.20; cross-script names share 0 tokens. | Fails for cross-script pairs (Latin S1 vs Devanagari/Tamil S2/S3). Token length filter >1 excludes 1-char tokens. | **Already Implemented**. Provides strong recall for intra-script token overlap. | Evaluate lower token length or partial token matching. |
| **Method 3: N-gram / Fuzzy Names** | Character trigram overlap between Latin and Devanagari/Tamil is **0.0**. | Trigram inverted index will retrieve **0 candidate pairs** for all 551,240 cross-script matches. | **Already Implemented**. difflib sequence matcher runs on top-K. | Verify if fuzzy retrieval hits 0 recall on Indic names. |
| **Method 4: Address-Based Retrieval** | **>99.7% of addresses in S2 and S3 are in Latin script**, even when name is Devanagari/Tamil. | **CRITICAL BRIDGING MECHANISM**: Address retrieval can successfully retrieve targets for cross-script entities where name retrieval fails! | **Already Implemented**. Addresses normalized and indexed by exact & token overlap. | Address missingness (3.3% in S2/S3) limits this fallback. |
| **Method 5: Country-Aware Retrieval** | Ground truth exhibits **100.0% country agreement** across all 7.638M pairs. Test set has unseen `France`. | Country is a near-perfect candidate filter. Unseen France strings work seamlessly as open strings. | **Already Implemented**. Open string matching without hardcoding US/India. | Check whether country should be a strict hard blocking filter. |
| **Method 6: Embedding-Based Retrieval** | 64-dimensional local character-trigram hash vectors share zero active indices across scripts. | Hashed trigram vectors cannot cluster cross-script transliterations together. | **Already Implemented**. Uses FAISS IVF-PQ on trigram hash vectors. | Investigate vector space alignment or fallback paths. |
| **Pairwise Features & LightGBM** | Features rely heavily on character and token similarity (`name_char_similarity`, `name_token_jaccard`). | For cross-script matches, name similarity features are 0.0, placing 100% reliance on address similarity and country agreement. | **Already Implemented**. LightGBM learns multi-feature non-linear combinations. | Analyze feature importance on cross-script validation split. |

---

## 9. Methodology, Sampling Details, and Reproducibility

### 9.1 Methodology
* **Full-Column Streaming Audit**: All 24,229,173 dataset rows across all 7 TSV files were audited line-by-line using Python 3 standard library routines (`csv`, `unicodedata`, `collections`, `re`). No random row sampling was used for file inventory, missingness, or script distribution counts.
* **Unicode Script Categorization**: Unicode character ranges and `unicodedata.name()` standards were applied to classify characters into Latin, Devanagari, Tamil, Telugu, Kannada, Gujarati, Bengali, Malayalam, Odia, Gurmukhi, and non-letter classes.
* **Ground-Truth Cross-Source Evaluation**: All 2,206,821 S1 entities in `train_ground_truth.tsv` and their 7,638,365 matched target records were evaluated for script agreement, country agreement, exact string identity, and token Jaccard similarity. A 50,000-pair random sample was evaluated for exact `difflib.SequenceMatcher` ratios.

### 9.2 Audit Output Files
Summary JSON and CSV output files are stored under `reports/audit/`:
* `reports/audit/fast_source_audits.json` (Full 24.2M row script & missingness audit)
* `reports/audit/gt_detailed_analysis.json` (Full 7.638M ground-truth match pair analysis)
* `reports/audit/inventory_summary.csv`
* `reports/audit/script_distribution_summary.csv`
* `reports/audit/ground_truth_script_matches.csv`

---

## 10. Unanswered Questions Requiring Further Investigation

1. **Address-Based Recovery Rate on Cross-Script Positives**: How many of the 551,240 cross-script ground-truth matches are successfully retrieved by Method 4 (Address-Based Retrieval) when Method 1-3 name retrieval fails?
2. **Impact of Empty Addresses on Cross-Script Positives**: How many of the 551,240 cross-script matched entities have an empty address in S2 or S3, making both name-based and address-based retrieval fail?
3. **Workstation Candidate Recall Benchmark**: What is the overall candidate recall achieved by the combined six-family retrieval pipeline across the full 2.2M training dataset?
4. **Validation Threshold Generalization on Unseen France Entities**: How well does the LightGBM decision threshold tuned on US and India entities generalize to the test set's 259,452 France entities?
