# Design 1: Candidate Generation

## 1. Purpose

Candidate generation is the first major stage of the entity-resolution pipeline.

For every record in Source 1 (S1), the system must retrieve a manageable set of potential matching records from Source 2 (S2) and Source 3 (S3).

The full Cartesian comparison of S1 against S2 and S3 is computationally impractical at the challenge's dataset scale. Candidate generation therefore reduces the number of record pairs that need to be evaluated by the downstream feature-extraction and matching-model stages.

The primary objective is to achieve high candidate recall while keeping candidate volume and computational cost manageable.

A true match that is not retrieved during candidate generation cannot be recovered by the downstream model. Candidate recall is therefore a critical independent quality measure.

## 2. Scope and Inputs

### 2.1 Input data

Candidate generation operates on:

* S1: Reference entities for which matches must be found.
* S2: First target source.
* S3: Second target source.

Available entity fields:

* `entity_id`
* `business_name`
* `business_address`
* `country`

The source associated with each record must be identifiable.

### 2.2 Output

For each S1 entity, candidate generation produces a set of unique candidate entity IDs drawn exclusively from S2 and S3.

The candidate-generation output must retain:

* The S1 entity ID.
* The retrieved candidate entity ID.
* The source of the candidate, where needed.
* The retrieval method or methods that produced the candidate.
* The retrieval score or other method-specific evidence, where applicable.

The output is an intermediate representation for feature extraction and model scoring. It is not the final matching result.

## 3. Frozen Architectural Decision: Hybrid Multi-Method Retrieval

The system will use a **hybrid candidate-generation architecture** consisting of six independently executed retrieval methods.

Each method retrieves candidates using a different type of evidence. The results are combined into a single candidate set for each S1 entity.

The six retrieval methods are:

1. Exact and normalized-name blocking.
2. Token-based name retrieval.
3. Character n-gram and fuzzy-name retrieval.
4. Address-based retrieval.
5. Country-aware retrieval.
6. Embedding-based nearest-neighbor retrieval.

The architecture is frozen at the method-family level. Exact algorithms, indexes, retrieval limits, and other implementation parameters remain subject to experimentation.

## 4. Retrieval Methods

### 4.1 Exact and Normalized-Name Blocking

Retrieve target records whose business names exactly match the S1 business name or match after the agreed name-normalization process.

Normalization may account for differences such as:

* Letter case.
* Punctuation.
* Whitespace.
* Common formatting variations.
* Other validated normalization rules.

The purpose is to efficiently recover exact and near-exact name matches without requiring expensive pairwise comparisons.

Normalization rules must be applied consistently during index construction and query processing.

### 4.2 Token-Based Name Retrieval

Retrieve candidates using the tokens present in business names.

This method is intended to recover records where the same or overlapping meaningful words appear in different orders or with variations in formatting.

Examples of useful cases include:

* Reordered name tokens.
* Partial name overlap.
* Names containing additional descriptive words.
* Variations in spacing or token boundaries.

The retrieval strategy must avoid relying exclusively on common tokens that provide little identifying information.

### 4.3 Character N-Gram and Fuzzy-Name Retrieval

Retrieve candidates using character-level representations and approximate name similarity.

This method is intended to handle:

* Minor spelling variations.
* Abbreviations and partial name differences.
* Character insertions, deletions, and substitutions.
* Some transliteration and spelling variations.
* Names that are similar without sharing identical tokens.

Character n-gram retrieval and fuzzy matching are complementary techniques within this retrieval family. Their exact implementation and combination will be determined experimentally.

### 4.4 Address-Based Retrieval

Retrieve candidates using business-address evidence independently of name-based retrieval.

Address retrieval may use:

* Exact normalized-address matching.
* Address-token matching.
* Fuzzy address similarity.
* Address-component matching when reliable components can be extracted.

This method is intended to recover matches where business names differ substantially but address information provides useful identifying evidence.

Address-based retrieval must also account for incomplete, noisy, or inconsistent addresses.

### 4.5 Country-Aware Retrieval

Country information will be used as contextual evidence to improve retrieval efficiency and relevance.

Country-aware retrieval may use country information to organize indexes, prioritize relevant search spaces, or refine retrieval behavior.

**Country must not be used as a universal hard filter.**

The dataset includes multiple countries, and country values may be missing, inconsistent, or noisy. A strict country-equality requirement could eliminate genuine matches.

The retrieval architecture must support the countries represented in the data, including countries such as France, rather than assuming only a fixed subset of countries.

### 4.6 Embedding-Based Nearest-Neighbor Retrieval

Use semantic or learned vector representations to retrieve records that are close in embedding space.

The embedding retrieval family will include:

* Name-focused representations.
* Combined name-and-address representations.

The purpose is to recover candidates that lexical or token-based methods may miss, including some cases involving substantial wording differences.

Embedding generation, vector indexing, similarity measures, and retrieval limits will be selected and validated experimentally.

Embedding retrieval supplements the other methods; it does not replace them.

## 5. Candidate Union, Deduplication, and Provenance

The results of all six retrieval methods will be combined using a union operation.

For a given S1 entity:

1. Execute each configured retrieval method independently.
2. Collect the candidate IDs returned by each method.
3. Combine all retrieved candidate IDs into one candidate set.
4. Deduplicate candidates by entity ID.
5. Retain the retrieval provenance associated with each candidate.

If multiple methods retrieve the same candidate, the candidate appears only once in the unified candidate set, but its provenance records all applicable retrieval methods.

**Retrieval methods do not veto one another.** A candidate retrieved by one method remains in the unified set even if other methods do not retrieve it or provide conflicting evidence.

Candidates with high name similarity but weaker address similarity, or strong address similarity but weaker name similarity, must not be automatically discarded at this stage.

The downstream feature-extraction and matching-model stages will evaluate the combined evidence.

## 6. Candidate Selection and Filtering Rules

The following rules are frozen:

* Candidates must come exclusively from S2 or S3.
* Candidates must be associated with the relevant S1 entity.
* Candidate IDs must be unique within each S1 entity's candidate list.
* A candidate retrieved by any configured method is eligible for inclusion in the unified candidate set.
* No universal hard country-equality filter will be applied.
* No candidate will be rejected solely because name and address evidence disagree.
* Candidate generation must not use ground-truth match labels to inject known positive candidates during training or inference.
* Candidate generation must be consistent between training and inference.

There will be no arbitrary global candidate cap imposed solely for convenience.

Retrieval limits and candidate budgets may be introduced and tuned as explicit, configurable parameters. Their effects on candidate recall, candidate volume, and computational cost must be measured.

## 7. Training and Inference Consistency

Candidate generation must use the same configured retrieval architecture during training and inference.

The following must remain consistent:

* Normalization rules.
* Retrieval method definitions.
* Indexing and query conventions.
* Method-specific retrieval configuration.
* Candidate deduplication and provenance handling.
* Candidate output semantics.

Training candidate generation must not inject ground-truth matches into the candidate set.

A genuine match that is absent from the generated candidates must be recorded as a candidate-generation miss rather than silently repaired using ground-truth information.

Any change to the candidate-generation configuration that affects the candidate distribution must be versioned and evaluated.

## 8. Candidate-Generation Evaluation

Candidate generation must be evaluated independently of the downstream matching model.

### 8.1 Candidate Recall

Measure the proportion of ground-truth match IDs retrieved in the candidate set.

At the entity level, assess whether the candidate set contains the known matching records for each S1 entity.

Candidate recall must account for entities with multiple ground-truth matches and must distinguish retrieval failures from downstream scoring failures.

### 8.2 Candidate Volume

Measure:

* Total number of generated candidate pairs.
* Average candidate count per S1 entity.
* Candidate-count distribution.
* Candidate volume by source pair, where applicable.

### 8.3 Reduction Ratio

Measure the reduction in comparisons achieved relative to exhaustive S1-to-S2 and S1-to-S3 comparisons.

The reduction ratio must be interpreted alongside candidate recall: reducing candidate volume is not sufficient if it removes too many genuine matches.

### 8.4 Per-Method Contribution

For each retrieval method, measure:

* Candidates uniquely contributed by that method.
* Ground-truth matches recovered by that method.
* Incremental true matches recovered when the method is added to the existing union.
* Candidate volume introduced by the method.
* Its effect on overall candidate recall and computational cost.

These measurements will support decisions about retrieval limits, method configuration, and the value of each retrieval family.

### 8.5 Validation Discipline

Candidate-generation evaluation must use the designated training/validation split and the same candidate-generation process used by the downstream pipeline.

Ground-truth labels may be used to measure recall and analyze candidate-generation misses, but must not be used to inject candidates into the generated sets.

## 9. Parameters Requiring Experimental Tuning

The following decisions are not frozen and must be selected through controlled experiments:

| Parameter                       | What must be determined                                                                                   |
| ------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Normalization rules             | Which normalization operations improve retrieval without introducing harmful collisions                   |
| Token retrieval configuration   | Tokenization, weighting, index strategy, and retrieval limits                                             |
| Character n-gram configuration  | N-gram representation, similarity method, and retrieval limits                                            |
| Fuzzy retrieval configuration   | Similarity algorithm, thresholds, and search limits                                                       |
| Address retrieval configuration | Address normalization, component extraction, similarity methods, and retrieval limits                     |
| Country-aware strategy          | How country context is used without suppressing genuine cross-country or inconsistent-country matches     |
| Embedding model                 | Representation model and input construction                                                               |
| Vector retrieval configuration  | Index type, similarity measure, search parameters, and retrieval limits                                   |
| Per-method candidate limits     | How many candidates each method may contribute                                                            |
| Combined candidate volume       | Acceptable candidate volume consistent with recall and resource constraints                               |
| Method inclusion                | Whether each method provides sufficient incremental value under measured resource and quality constraints |

No numerical value should be treated as finalized unless it is explicitly recorded in a later approved configuration or experiment result.

## 10. Resource and Operational Constraints

Candidate generation must support the challenge's large datasets and the available workstation resources.

The architecture must:

* Support reusable indexes for S2 and S3.
* Avoid exhaustive pairwise comparisons.
* Support batch-oriented processing of S1 entities.
* Avoid holding the complete candidate universe in memory.
* Support candidate deduplication and provenance retention.
* Support checkpointing and resumable processing.
* Permit retrieval parameters to be configured and versioned.
* Make it possible to measure runtime, memory usage, and storage consumption.

Exact batch sizes, worker counts, index parameters, and storage formats belong in the Technical Design Document and implementation configuration, not as frozen numerical decisions in this architecture.

## 11. Acceptance and Completion Conditions

Candidate generation is considered architecturally compliant when:

1. All six retrieval method families are implemented or explicitly accounted for in an approved experimental decision.
2. The configured methods can retrieve candidates from both S2 and S3 for every eligible S1 entity.
3. Candidate results are combined through union and deduplicated by candidate entity ID.
4. Retrieval provenance is retained.
5. Candidate selection does not impose an unapproved universal country filter or name-address agreement rule.
6. Training and inference use consistent candidate-generation semantics without ground-truth candidate injection.
7. Candidate recall, candidate volume, reduction ratio, and per-method contribution can be evaluated.
8. Processing supports the project's batch, checkpointing, and resource-management requirements.
9. Numerical retrieval limits and configuration choices are documented with supporting validation results.

**No fixed numerical candidate-recall target, candidate-count cap, or runtime guarantee is established by this design alone.** Such targets must be agreed upon explicitly and supported by empirical evidence.

## 12. Decision Summary

| Decision                                                      | Status                                   |
| ------------------------------------------------------------- | ---------------------------------------- |
| Hybrid six-method candidate-generation architecture           | Frozen                                   |
| Exact and normalized-name blocking                            | Frozen                                   |
| Token-based name retrieval                                    | Frozen                                   |
| Character n-gram and fuzzy-name retrieval                     | Frozen                                   |
| Address-based retrieval                                       | Frozen                                   |
| Country-aware retrieval without a universal hard filter       | Frozen                                   |
| Embedding-based retrieval                                     | Frozen                                   |
| Union and deduplication of candidates                         | Frozen                                   |
| Retention of retrieval provenance                             | Frozen                                   |
| No ground-truth candidate injection                           | Frozen                                   |
| Same candidate-generation semantics in training and inference | Frozen                                   |
| Candidate recall and retrieval efficiency evaluation          | Frozen                                   |
| Exact algorithms, model choices, and retrieval limits         | Experimental                             |
| Candidate budget and method-specific limits                   | Experimental                             |
| Final candidate-generation configuration                      | To be selected using validation evidence |


# Design 2: Pairwise Feature Extraction

## 1. Purpose

Pairwise feature extraction converts each candidate pair into a structured numerical representation that describes the evidence for and against the two records referring to the same real-world business entity.

The system compares an S1 reference entity with a candidate entity from S2 or S3.

The resulting feature vector is passed to the downstream LightGBM binary classifier, which estimates whether the candidate is a match.

Feature extraction must capture similarities, meaningful disagreements, missing information, data quality, and candidate-generation evidence without making the final matching decision itself.

## 2. Scope and Inputs

### 2.1 Input

Each input is a candidate pair consisting of:

* One S1 entity.
* One candidate entity from S2 or S3.
* Candidate-generation provenance and any available retrieval scores.

The available entity fields are:

* `entity_id`
* `business_name`
* `business_address`
* `country`

The source pair must be identifiable as either S1–S2 or S1–S3.

### 2.2 Output

For every candidate pair, the feature-extraction stage produces:

* A stable candidate-pair identifier or equivalent pair association.
* The source pair.
* A structured numerical feature vector with a consistent schema.
* The association between the feature vector and the original candidate pair.

The output must be suitable for model training and inference.

## 3. Frozen Architectural Decision: Structured Multi-Group Features

The system will use a structured, multi-group feature-extraction architecture.

Features will be organized into six groups:

1. Business-name features.
2. Address features.
3. Country and geographic features.
4. Cross-field interaction features.
5. Candidate-generation evidence features.
6. Data-quality and contextual features.

The feature design draws on two complementary principles:

* **Fellegi–Sunter record linkage:** use agreement, disagreement, and the identifying value or rarity of evidence.
* **Machine-learning record linkage:** represent pairwise evidence as features and let a learned model determine how the evidence contributes to the match prediction.

These are guiding principles, not separate matching systems. The final matching decision belongs to the trained model and its selected decision policy.

## 4. Feature Group 1: Business-Name Features

Business-name features capture exact agreement, approximate similarity, token overlap, and distinctive name characteristics.

The feature family includes:

### 4.1 Exact and Normalized Agreement

* Raw name equality.
* Normalized name equality.
* Normalized-name agreement indicators.

Raw and normalized evidence must remain distinguishable.

### 4.2 Character-Level Similarity

* Character-level similarity scores.
* Edit-distance-based similarity, such as normalized Levenshtein similarity.
* Jaro–Winkler similarity.
* Character n-gram similarity.

The exact algorithms and normalization conventions will be validated experimentally.

### 4.3 Token-Level Similarity

* Token Jaccard similarity.
* Token containment or overlap.
* Weighted token similarity using token rarity or informativeness.
* Other validated token-level similarity measures.

The feature design must account for differences in token order and additional or missing name tokens.

### 4.4 Name Structure and Distinctiveness

* Name-length ratio.
* Token-count difference.
* Distinctive-token information.
* Other validated indicators of name structure.

Common words should not be treated as equally informative as rare, distinctive business-name tokens.

## 5. Feature Group 2: Address Features

Address features capture agreement, similarity, overlap, and the reliability of address evidence.

The feature family includes:

### 5.1 Exact and Normalized Agreement

* Raw address equality.
* Normalized address equality.

### 5.2 Similarity and Overlap

* Character-level address similarity.
* Token-level address similarity.
* Weighted address-token similarity.
* Character n-gram similarity.
* Address-token containment or overlap.

### 5.3 Address-Component Evidence

Where reliable components can be extracted, compare:

* Building or street number.
* Postal code.
* City or locality.
* Street name.
* Landmark or other useful address components.

Component extraction must account for differences in address formats and incomplete or noisy text.

### 5.4 Address Completeness and Structure

* Address completeness.
* Address-length ratio.
* Address token-count difference.
* Indicators of available or missing address components.

Missing address evidence must be distinguishable from contradictory address evidence.

## 6. Feature Group 3: Country and Geographic Features

Country and geographic features capture the agreement, disagreement, and availability of country information.

The feature family includes:

* Raw country equality.
* Normalized country equality.
* Country conflict indicators.
* Country missingness indicators.
* Address-country consistency indicators.

Country information is contextual evidence, not an automatic matching rule.

The feature schema must support multiple countries and must not assume that country values are always complete, standardized, or consistent.

## 7. Feature Group 4: Cross-Field Interaction Features

Cross-field features capture relationships between name, address, and country evidence.

The feature family includes:

* Name–address interaction features.
* Name–country consistency features.
* Combined name-and-address evidence.
* Indicators for high name similarity with low address similarity.
* Indicators for low name similarity with high address similarity.
* Other validated cross-field relationships.

These features allow the model to distinguish different patterns of agreement and disagreement.

The feature design must avoid redundant duplication of evidence already represented by individual feature groups, including unnecessary duplication of address-country consistency.

## 8. Feature Group 5: Candidate-Generation Evidence Features

Candidate-generation evidence features describe how a candidate was retrieved and the strength of the retrieval evidence.

The feature family includes:

* Indicator for exact or normalized-name retrieval.
* Indicator for token-based name retrieval.
* Indicator for fuzzy or character-based name retrieval.
* Indicator for address-based retrieval.
* Indicator for embedding-based retrieval.
* Number of retrieval methods that retrieved the candidate.
* Method-specific retrieval scores, where available.

These features allow the model to use candidate-generation provenance as additional evidence.

The feature schema must support candidates retrieved by multiple methods and candidates retrieved by only one method.

Retrieval provenance must be preserved during candidate deduplication so that the model can use the complete evidence.

## 9. Feature Group 6: Data-Quality and Contextual Features

Data-quality and contextual features describe the completeness and structure of the records being compared.

The feature family includes:

* Missingness indicators for relevant fields.
* Name and address text lengths.
* Token counts.
* Distinctive-token counts.
* Other validated data-quality indicators.
* Source-pair indicator identifying S1–S2 versus S1–S3.

These features help the model interpret similarity scores in the context of the available evidence and the source pair.

Missing values must not be silently treated as ordinary disagreement.

## 10. Shared Feature Schema

A single shared feature schema will be used for both:

* S1–S2 candidate pairs.
* S1–S3 candidate pairs.

The source-pair indicator will identify which target source is being compared.

The schema must ensure:

* Identical feature names and ordering across training and inference.
* Consistent data types and numerical representations.
* Consistent normalization and missing-value conventions.
* Consistent feature definitions for both source pairs.
* Explicit versioning of feature definitions and schema changes.

Source-specific differences may be represented through features, but the system must not maintain incompatible feature schemas for S1–S2 and S1–S3.

## 11. Missing Values and Disagreement Handling

The feature-extraction stage must distinguish among:

1. Agreement between available values.
2. Disagreement between available values.
3. Missing information on one or both records.
4. Evidence that cannot be reliably compared.

Examples:

* A missing address is not equivalent to a contradictory address.
* A missing country is not equivalent to a country conflict.
* Low similarity between two available names is different from having no name information.

Missingness must be represented consistently in the feature vector.

The exact encoding strategy, including numerical missing-value handling and any explicit indicators, must be validated with the downstream model.

Feature extraction must not impose hard rejection rules based solely on low similarity or field disagreement.

## 12. Training and Inference Consistency

Training and inference must use the same feature-extraction pipeline and feature schema.

The following must remain consistent:

* Input field interpretation.
* Normalization rules.
* Similarity and comparison algorithms.
* Address-component extraction conventions.
* Missing-value handling.
* Feature definitions and ordering.
* Candidate-generation evidence representation.
* Numerical data types and output structure.

The trained model must be associated with the feature-schema version used to train it.

Any change to feature definitions or preprocessing that affects model inputs must be versioned and evaluated before being adopted.

## 13. Feature Quality and Validation

Feature extraction must be validated for:

* Consistency between training and inference.
* Correct handling of missing and malformed values.
* Correct representation of name and address agreement and disagreement.
* Correct preservation of candidate-generation provenance.
* Stable feature names, ordering, and data types.
* Absence of unintended target leakage.
* Compatibility with the downstream LightGBM model.

Feature quality must also be assessed through controlled experiments to determine whether individual feature groups or features improve validation performance.

Feature importance and ablation experiments may be used to identify redundant, unhelpful, or potentially misleading features.

Feature removal or modification must be based on measured evidence rather than intuition alone.

## 14. Parameters Requiring Experimental Validation

The following are not frozen numerical or algorithmic choices:

| Parameter                    | What must be determined                                                 |
| ---------------------------- | ----------------------------------------------------------------------- |
| Name normalization           | Exact normalization rules and their impact on matching evidence         |
| Address normalization        | Exact address-cleaning and standardization rules                        |
| Similarity algorithms        | Which algorithms and variants provide useful evidence                   |
| Similarity scaling           | How similarity scores are represented numerically                       |
| Token weighting              | How rarity and informativeness are calculated                           |
| Address-component extraction | Which components can be extracted reliably and how they are represented |
| Cross-field interactions     | Which interaction features provide measurable value                     |
| Missing-value encoding       | The numerical representation and explicit missingness strategy          |
| Feature selection            | Which features or feature groups improve validation performance         |
| Feature schema version       | The finalized schema after implementation and validation                |

No exact feature count or final list of numerical parameters is established by this design alone.

## 15. Resource and Operational Constraints

Feature extraction must support large-scale, batch-oriented processing.

The architecture must:

* Process candidate pairs in batches.
* Avoid requiring the entire candidate-pair feature matrix to reside in memory.
* Support partitioned or streamed feature outputs.
* Preserve the association between features and candidate-pair IDs.
* Support checkpointing and resumable processing.
* Use a consistent, versioned feature schema.
* Permit resource usage and processing time to be measured.

The exact storage format, batch size, worker count, and numerical data types will be finalized in the Technical Design Document and implementation configuration.

## 16. Acceptance and Completion Conditions

Feature extraction is considered architecturally compliant when:

1. All six feature groups are represented in the implemented feature schema or their inclusion has been explicitly resolved through validation.
2. Both S1–S2 and S1–S3 pairs use the same shared schema.
3. Name, address, country, and cross-field evidence are represented.
4. Candidate-generation provenance is preserved and represented.
5. Missing information is distinguishable from meaningful disagreement.
6. Feature extraction does not perform the final match/no-match decision.
7. Training and inference use consistent feature definitions and preprocessing.
8. Feature vectors are stable, structured, and suitable for LightGBM.
9. Feature extraction supports batch processing and resumable execution.
10. Feature definitions and schema versions are recorded and reproducible.

## 17. Decision Summary

| Decision                                                   | Status                           |
| ---------------------------------------------------------- | -------------------------------- |
| Structured pairwise feature extraction                     | Frozen                           |
| Six feature groups                                         | Frozen                           |
| Fellegi–Sunter principles as design inspiration            | Frozen                           |
| Shared feature schema for S1–S2 and S1–S3                  | Frozen                           |
| Raw and normalized evidence                                | Frozen                           |
| Representation of agreement, disagreement, and missingness | Frozen                           |
| Candidate-generation provenance as model evidence          | Frozen                           |
| No hard rejection based solely on field disagreement       | Frozen                           |
| Consistent feature pipeline for training and inference     | Frozen                           |
| Exact algorithms and normalization conventions             | Experimental                     |
| Final feature list and feature count                       | To be validated                  |
| Missing-value encoding details                             | Experimental                     |
| Final feature schema version                               | To be finalized after validation |


# Design 3: Model & Training

## 1. Purpose

The Model & Training component learns to distinguish matching and non-matching entity pairs using the structured features produced by the Pairwise Feature Extraction component.

The system will train a binary classification model that estimates the probability or confidence that a candidate pair represents the same real-world business entity.

The model's scores will subsequently be converted into final match decisions through a validated decision policy.

The primary objective is to maximize the official challenge metric, macro-averaged F0.5, while maintaining reproducibility, preventing data leakage, and respecting the system's computational constraints.

## 2. Frozen Architectural Decision: LightGBM Binary Classifier

The primary model family is **LightGBM**, configured as a binary classifier.

The model receives the structured numerical feature vector associated with each candidate pair and produces a score representing the estimated likelihood of a match.

The architecture separates two responsibilities:

1. **Model scoring:** Estimate whether a candidate pair is a match.
2. **Decision policy:** Determine which scored candidates are retained as final matches.

The model must not impose a one-to-one matching constraint or a fixed maximum number of matches per S1 entity.

### 2.1 Model Alternatives

XGBoost is designated as a potential challenger model.

Other model families, such as CatBoost or a logistic regression baseline, may be considered where useful for controlled comparison.

The primary architecture remains LightGBM unless experiments demonstrate a justified change.

No ensemble is assumed by default. An ensemble may be considered only if controlled validation demonstrates a meaningful improvement under the project's evaluation and resource constraints.

No claim is made that LightGBM is guaranteed to outperform alternative models or achieve a particular leaderboard position.

## 3. Training Data Construction

### 3.1 Candidate-Pair Training Examples

Training examples will be constructed from candidate pairs generated by the frozen Candidate Generation pipeline.

Each training example consists of:

* One S1 entity.
* One candidate entity from S2 or S3.
* The feature vector associated with that pair.
* A binary target label.

Each candidate pair represents one training example.

The same candidate-generation and feature-extraction semantics used during inference must be used to construct training examples.

### 3.2 Binary Label Assignment

The ground-truth data identifies the known matching target entity IDs for each S1 entity.

For each generated candidate pair:

* **Positive label (1):** The candidate entity ID is listed among the ground-truth matches for the corresponding S1 entity.
* **Negative label (0):** The candidate entity ID is not listed among the ground-truth matches for that S1 entity, following the challenge's labeling convention.

Candidate pairs that correspond to known ground-truth matches but are absent from the generated candidate set must be recorded as candidate-generation misses.

Ground-truth information must not be used to inject missing positive candidates into the candidate-generation output.

The supplied ground truth is authoritative for challenge training and evaluation. The system must not silently reinterpret unlisted pairs as verified real-world non-matches.

## 4. Positive and Negative Sampling Strategy

### 4.1 Positive Examples

All generated positive candidate pairs must be retained for training.

The training process must not arbitrarily discard known positive candidate pairs to achieve a desired class balance.

The number of positive pairs available for training depends on the recall of the candidate-generation pipeline.

### 4.2 Negative Examples

The negative training set will use a controlled mixture of:

1. **Hard negatives:** Non-matching candidates that resemble the reference entity or were retrieved through multiple or high-similarity retrieval methods.
2. **Representative ordinary negatives:** Other non-matching candidate pairs that reflect the broader candidate distribution.

Hard negatives are intended to help the model distinguish difficult non-matches from genuine matches.

Ordinary negatives are intended to preserve exposure to the broader range of candidate pairs.

### 4.3 Hard-Negative Mining

Hard-negative mining may be used to identify challenging negative examples.

The process must:

* Operate only within the training partition.
* Exclude known ground-truth positive pairs.
* Avoid using validation labels to construct training examples.
* Be reproducible and documented.
* Avoid introducing information from the validation or test targets into training.

The exact hard-negative mining procedure will be selected through controlled experiments.

### 4.4 Sampling Proportions and Weighting

The negative sampling strategy must not assume a fixed 50:50 positive-to-negative class balance.

The proportions of hard negatives and ordinary negatives will be determined experimentally.

Sampling probabilities and the resulting training distribution must be recorded.

Sample weighting may be considered to account for the effects of sampling on the training distribution. Whether weighting is beneficial must be determined empirically.

The validation set must preserve the natural candidate distribution generated by the frozen candidate-generation process, rather than artificially balancing the classes.

## 5. Training and Validation Split

### 5.1 Entity-Level Separation

Training and validation must be separated at the S1 entity level.

All candidate pairs associated with a given S1 entity must belong to the same partition.

This prevents candidate pairs from the same reference entity from being split across training and validation.

### 5.2 Proposed Split

The initial proposed split is:

* 90% training.
* 10% validation.

The split is a starting configuration, not an immutable architectural requirement.

Stratification should be used where practical to preserve relevant distributions, including:

* Match status and match count.
* Source-pair composition.
* Country distribution.

If reliable duplicate or related-entity groups can be identified, the split strategy should account for them where appropriate to reduce leakage.

### 5.3 Validation Data Construction

Candidate generation and feature extraction must follow the same frozen pipeline for both training and validation.

Validation examples must be generated without injecting ground-truth matches.

The validation candidate distribution must reflect the configured candidate-generation process.

Validation labels may be used to evaluate the model, select hyperparameters, select the final decision threshold, and assess calibration.

Validation examples must not be incorporated into the model's training examples during model selection.

## 6. Training Procedure

The training process must support:

1. Constructing candidate-pair training examples.
2. Assigning binary labels using the challenge's ground-truth convention.
3. Applying the configured negative-sampling strategy.
4. Extracting the shared feature schema.
5. Training the LightGBM binary classifier.
6. Evaluating the trained model on validation data.
7. Selecting model hyperparameters and the final decision policy.
8. Recording the experiment configuration, metrics, and artifacts.
9. Retraining the selected configuration on all eligible training data after model selection.

The training pipeline must be reproducible through versioned configurations, recorded data partitions, and model artifacts.

## 7. Hyperparameter Selection and Early Stopping

LightGBM hyperparameters must be selected through controlled validation experiments.

The tuning process may include:

* Tree complexity and leaf configuration.
* Learning rate.
* Number of boosting iterations.
* Regularization.
* Feature and row sampling.
* Other relevant LightGBM parameters.

Early stopping may be used to control overfitting and identify an appropriate number of boosting iterations.

The exact hyperparameter search space, search strategy, and stopping criteria remain experimental.

Hyperparameter selection must prioritize the official macro F0.5 metric, with diagnostic metrics used to understand model behavior.

## 8. Evaluation Metrics and Model Selection

### 8.1 Primary Metric

The primary selection metric is the official challenge's macro-averaged F0.5 score.

F0.5 gives greater weight to precision than recall.

The model and its decision policy must be evaluated at the entity level in accordance with the official challenge evaluation semantics.

### 8.2 Diagnostic Metrics

The following metrics may be used for diagnosis and model comparison:

* Precision.
* Recall.
* PR-AUC.
* Macro F0.5 by source pair.
* Macro F0.5 by country.
* Performance by ground-truth match count.
* Candidate-generation recall.
* Runtime and resource consumption.

Diagnostic metrics must not replace the official challenge metric as the primary selection objective.

### 8.3 Candidate Generation Versus Model Performance

The evaluation must distinguish:

* True matches not retrieved during candidate generation.
* Retrieved true matches incorrectly rejected by the model or decision policy.
* Incorrect candidates accepted as matches.

A model cannot recover a true match that was never included in its candidate set.

Candidate-generation quality and final matching quality must therefore be reported separately.

## 9. Decision Threshold and Matching Policy

### 9.1 Threshold Selection

The LightGBM model produces a score for each candidate pair.

A decision threshold or validated policy is used to determine which candidate pairs are accepted as final matches.

The default architecture uses a **global probability threshold** applied consistently to candidate pairs.

The threshold must be selected using validation data to maximize the official macro F0.5 score.

The threshold must not be assumed to be 0.5 or any other fixed value without experimental evidence.

### 9.2 Multiple Matches and No-Match Cases

The final matching policy must support:

* Zero matches for an S1 entity.
* One match for an S1 entity.
* Multiple matches for an S1 entity.

Every candidate whose score satisfies the selected policy may be retained.

The system must not impose:

* A one-to-one matching constraint.
* An arbitrary maximum number of matches per S1 entity.
* A requirement that every S1 entity receive a match.

An S1 entity with no candidates or no candidates passing the decision policy must produce an empty match list.

### 9.3 Alternative Decision Policies

Source-pair-specific thresholds, entity-level policies, or other decision rules may be considered only if controlled validation demonstrates a reliable improvement in the official metric.

The global threshold remains the default policy.

Any selected alternative must be explicitly documented, versioned, and applied consistently during inference.

## 10. Probability Calibration

Calibration may be considered if it improves the reliability or usefulness of model scores or supports a better final matching policy.

Calibration is not mandatory by default.

If used, the calibration method must be selected using appropriate validation procedures and must not introduce leakage.

The final model artifact and inference configuration must record whether calibration is applied and which calibration configuration is used.

Calibration must be evaluated based on its effect on the final objective rather than assumed to improve macro F0.5.

## 11. Validation Integrity and Leakage Prevention

The training and evaluation process must prevent information leakage between training and validation.

The following rules are frozen:

* All candidate pairs associated with an S1 entity belong to the same partition.
* Hard-negative mining is restricted to the training partition.
* Validation labels are not used to construct training examples.
* Validation data is used for model selection and policy selection, not model fitting.
* Test labels must never be used for training, tuning, or threshold selection.
* Ground-truth matches must not be injected into candidate generation.
* Any learned preprocessing or transformation must be fitted using eligible training data only, unless its design is explicitly label-independent and valid for both partitions.

Validation results must be interpreted with awareness that repeated experimentation can overfit the validation set.

Where data permits, finalists should be evaluated on additional validation subsets or repeated splits, and a separate final holdout may be maintained.

The exact additional validation strategy remains to be finalized based on data availability and computational cost.

## 12. Final Model Retraining

After model and decision-policy selection:

1. Freeze the selected model configuration.
2. Freeze the selected feature schema and candidate-generation configuration.
3. Freeze the selected sampling strategy and decision policy.
4. Retrain the selected model configuration on all eligible training data.
5. Preserve the selected decision threshold or policy.
6. Record the final model artifact and its associated configuration.

The final model must be associated with the exact feature schema, preprocessing configuration, and decision policy required for inference.

Retraining must not incorporate hidden test labels or use hidden test performance to revise the model configuration.

## 13. Model Artifact and Reproducibility

The model artifact must be accompanied by sufficient metadata to reproduce and interpret its use.

At minimum, record:

* Model family and version.
* Training configuration.
* Feature-schema version.
* Candidate-generation configuration version.
* Training and validation partition identifiers.
* Negative-sampling configuration.
* Selected hyperparameters.
* Selected decision threshold or policy.
* Calibration configuration, if applicable.
* Evaluation metrics.
* Relevant software and environment information.
* Artifact location and experiment identifier.

The final artifact must be compatible with the inference pipeline and must not rely on undocumented settings.

## 14. Parameters Requiring Experimental Tuning

| Parameter                   | What must be determined                                          |
| --------------------------- | ---------------------------------------------------------------- |
| Training/validation split   | Final split configuration and any additional validation strategy |
| Negative-sampling ratio     | Proportions of hard and ordinary negatives                       |
| Negative sampling strategy  | Sampling method and candidate selection rules                    |
| Sample weighting            | Whether weighting is beneficial and how it is applied            |
| Hard-negative mining        | Mining strategy and configuration                                |
| LightGBM hyperparameters    | Model configuration selected through validation                  |
| Early stopping              | Stopping criteria and boosting iteration selection               |
| Decision threshold          | Threshold that maximizes validation macro F0.5                   |
| Calibration                 | Whether calibration is useful and which method to use            |
| Alternative decision policy | Whether a non-global policy provides reliable improvement        |
| Final model configuration   | Selected model and policy after controlled experimentation       |

No fixed final threshold, hyperparameter set, or negative-sampling ratio is established by this design.

## 15. Resource and Operational Constraints

Training must support the large candidate-pair dataset and the available workstation resources.

The architecture must:

* Support batch-oriented feature preparation and training-data construction.
* Avoid requiring unnecessary full-dataset copies in memory.
* Support configurable negative sampling.
* Support reproducible training and validation partitions.
* Record runtime and resource consumption.
* Support checkpointing or recoverable execution where appropriate.
* Preserve model artifacts and experiment configurations.

The exact training batch size, worker count, memory allocation, and CPU/GPU execution mode will be determined in the Technical Design Document and validated through benchmarking.

## 16. Acceptance and Completion Conditions

The Model & Training component is considered architecturally compliant when:

1. LightGBM is implemented as the primary binary classifier.
2. Training examples are constructed from the frozen candidate-generation pipeline.
3. Binary labels follow the challenge's ground-truth convention.
4. Positive examples are retained and negative sampling is controlled and documented.
5. Training and validation are separated at the S1 entity level.
6. Leakage-prevention rules are enforced.
7. Hyperparameter selection and decision-threshold selection use validation data.
8. The official macro F0.5 score is the primary model-selection metric.
9. The matching policy supports zero, one, or multiple matches per S1 entity.
10. The final model and decision policy are reproducible and versioned.
11. The selected configuration can be retrained on all eligible training data.
12. The final model artifact is compatible with the inference pipeline.

## 17. Decision Summary

| Decision                                              | Status                               |
| ----------------------------------------------------- | ------------------------------------ |
| LightGBM binary classifier as primary model           | Frozen                               |
| XGBoost as a potential challenger                     | Frozen                               |
| Candidate-pair-based binary classification            | Frozen                               |
| Ground-truth-based positive and negative labels       | Frozen                               |
| Retention of all generated positive pairs             | Frozen                               |
| Mixture of hard and ordinary negatives                | Frozen                               |
| Training/validation separation at S1 entity level     | Frozen                               |
| Proposed initial 90/10 split                          | Proposed starting configuration      |
| Official macro F0.5 as primary selection metric       | Frozen                               |
| Global threshold as default decision policy           | Frozen                               |
| Support for zero, one, or multiple matches            | Frozen                               |
| No one-to-one constraint or arbitrary maximum matches | Frozen                               |
| Validation-based threshold selection                  | Frozen                               |
| Final retraining on eligible training data            | Frozen                               |
| Negative-sampling proportions                         | Experimental                         |
| LightGBM hyperparameters                              | Experimental                         |
| Final decision threshold                              | Experimental                         |
| Calibration and alternative policies                  | Optional, validation-dependent       |
| Final selected model configuration                    | To be determined through experiments |


# Design 4: System Architecture & Resource Management

## 1. Purpose

This design defines the system architecture and resource-management strategy for executing the entity-resolution pipeline on the available hardware.

The system must process millions of records across three sources while managing memory, storage, CPU, and GPU resources.

The architecture must support large-scale candidate generation, feature extraction, model training, inference, evaluation, and experiment management without requiring the entire dataset or all intermediate results to reside in memory simultaneously.

The primary objectives are:

* Reliable execution on the available workstation.
* Efficient use of CPU, RAM, GPU, and SSD resources.
* Reusable indexes and intermediate representations.
* Batch-oriented processing of large datasets.
* Checkpointing and recovery from interrupted execution.
* Reproducibility and controlled resource consumption.

## 2. Available Hardware

### 2.1 Primary Workstation

The workstation is the primary execution environment.

| Component              | Specification                  |
| ---------------------- | ------------------------------ |
| CPU                    | Intel Xeon w7-2575X            |
| Physical CPU cores     | 22                             |
| Logical CPU threads    | 44                             |
| RAM                    | 128 GB                         |
| Operating system       | Windows                        |
| GPU                    | NVIDIA RTX 4000 Ada Generation |
| GPU VRAM               | 20 GB                          |
| CUDA                   | 13.2                           |
| Total storage capacity | 2 TB                           |
| Currently free storage | Approximately 336 GB           |
| Storage type           | SSD                            |

The available free storage is a critical constraint and must be considered when designing intermediate-data storage and processing workflows.

The exact relationship between the free space and the drive containing the input data and working directories must be verified before finalizing storage allocation.

### 2.2 Secondary Laptop

The laptop is a secondary development and support environment.

| Component | Specification   |
| --------- | --------------- |
| GPU       | NVIDIA RTX 3050 |
| GPU VRAM  | 4 GB            |

Other laptop hardware specifications have not been established in this design.

The laptop may be used for:

* Development and documentation.
* Small-scale tests.
* Lightweight experiments.
* Monitoring and analysis.

It is not the default environment for full-scale pipeline execution.

## 3. Frozen Architectural Decision: Single-Workstation Batch Processing

The system will use a **single-workstation, batch-oriented architecture**.

The primary workstation will execute the complete pipeline, including:

1. Data validation and preprocessing.
2. Reusable index construction.
3. Candidate generation.
4. Candidate deduplication and provenance handling.
5. Pairwise feature extraction.
6. Model training and validation.
7. Batch inference and prediction.
8. Evaluation and experiment management.
9. Final output validation and publication.

The system will use reusable indexes, disk-backed intermediate data, and checkpointed processing to support the dataset scale.

A distributed multi-machine architecture is not part of the default design.

The laptop and workstation will not be distributed execution nodes by default because doing so would introduce additional synchronization, data-transfer, and reproducibility complexity.

## 4. High-Level Processing Architecture

The system will be organized as a sequence of independently identifiable processing stages.

The principal execution flow is:

1. Load and validate source data.
2. Normalize and prepare reusable representations.
3. Build or load target-source indexes.
4. Process S1 entities in batches.
5. Retrieve candidates from S2 and S3.
6. Deduplicate candidates and preserve retrieval provenance.
7. Extract pairwise features in batches.
8. Train or load the selected matching model.
9. Score candidate pairs in batches.
10. Apply the selected matching policy.
11. Persist intermediate and final results.
12. Validate final outputs.
13. Publish validated output files.

Training, validation, and inference will reuse the relevant preprocessing, indexing, candidate-generation, and feature-extraction components wherever applicable.

The architecture must make stage boundaries explicit so that completed work can be reused rather than unnecessarily recomputed.

## 5. CPU and GPU Resource Allocation

### 5.1 CPU

The CPU is the primary resource for general data processing.

CPU execution may be used for:

* Data loading and validation.
* Normalization and preprocessing.
* Index construction and retrieval operations.
* Feature extraction.
* Candidate deduplication.
* LightGBM CPU training and inference.
* Data serialization and output validation.

The exact CPU worker count and parallelization strategy must be determined through benchmarking.

### 5.2 GPU

The workstation's NVIDIA RTX 4000 Ada GPU is available for workloads that can benefit from GPU acceleration.

GPU execution may be used for:

* Embedding generation.
* Embedding-related inference.
* GPU-compatible nearest-neighbor operations.
* LightGBM GPU execution, if the installed version and environment support it and benchmarks justify its use.

GPU usage is workload-dependent.

The architecture does not require every stage to execute on the GPU.

CPU and GPU implementations must be evaluated based on practical performance, memory usage, compatibility, and reliability.

### 5.3 Shared Resource Management

CPU, RAM, GPU VRAM, and storage are shared resources.

The system must avoid resource oversubscription and preserve sufficient memory for the operating system and other required processes.

Worker counts, parallel retrieval, embedding batch sizes, and feature-processing batch sizes must be configured and benchmarked together rather than independently assuming maximum parallelism is beneficial.

## 6. Memory Management

The system must be designed around the available 128 GB of RAM.

The following principles are frozen:

* Avoid loading unnecessary full copies of large datasets into memory.
* Reuse normalized representations and indexes where practical.
* Process large candidate and feature datasets in batches.
* Use partitioned or disk-backed intermediate storage where appropriate.
* Avoid retaining large intermediate objects after their stage is complete.
* Reserve sufficient memory for the operating system and concurrent workloads.
* Measure peak memory consumption during representative workloads.

The exact memory allocation, batch size, and concurrency configuration will be established through benchmarking.

The system must not assume that the entire candidate-pair universe or full feature matrix can safely fit in RAM.

## 7. Storage and Intermediate-Data Management

### 7.1 Storage Constraint

Approximately 336 GB of SSD storage is currently free.

This amount must be treated as a limited working-storage budget rather than an assumption that all intermediate datasets can be retained simultaneously.

A storage feasibility assessment must be performed before full-scale execution.

### 7.2 Input Data Preservation

Original input datasets must be preserved as read-only source data.

Preprocessing and pipeline execution must not overwrite or corrupt the original files.

Intermediate artifacts must be stored separately from original inputs and final challenge outputs.

### 7.3 Intermediate Storage Strategy

The architecture supports the use of:

* Columnar formats such as Parquet for normalized records and partitioned intermediate tables.
* Versioned indexes for target-source retrieval.
* Compact numerical arrays for embeddings and other suitable representations.
* Partitioned candidate-pair data.
* Partitioned or streamed feature data.
* Structured experiment artifacts and model files.
* Final TSV output files in the required challenge format.

The exact storage formats must be selected based on compatibility, performance, storage requirements, and implementation simplicity.

### 7.4 Storage Feasibility and Cleanup

Before large-scale processing, the system must:

1. Estimate storage requirements using representative data samples.
2. Measure the size of normalized records, indexes, embeddings, candidates, and features.
3. Estimate peak temporary storage requirements.
4. Verify available disk space.
5. Establish a storage budget and reserve capacity for recovery and final outputs.

The system must monitor storage consumption during execution.

Cleanup must distinguish disposable intermediate artifacts from reusable or required artifacts.

Only artifacts explicitly classified as disposable may be automatically removed.

The system must not silently delete original inputs, final outputs, or required experiment artifacts.

## 8. Reusable Indexes and Intermediate Representations

Target-source indexes for S2 and S3 should be reusable across batches and relevant pipeline stages.

The architecture must support:

* Building indexes once and reusing them where valid.
* Recording index versions and their associated preprocessing configuration.
* Detecting when an index is incompatible with a changed configuration.
* Rebuilding indexes when required.
* Avoiding unnecessary repeated construction of expensive representations.

Normalized records, embeddings, and other reusable representations may also be persisted when doing so is practical and resource-efficient.

Reuse must be governed by version compatibility rather than by the existence of an artifact alone.

## 9. Batch-Oriented Execution

The system will process large workloads in deterministic batches.

### 9.1 Batch Processing

Batch processing applies to:

* S1 entity processing.
* Candidate retrieval.
* Candidate deduplication.
* Feature extraction.
* Model scoring.
* Intermediate-data serialization.
* Output generation.

Batching must keep working memory within measured resource limits.

### 9.2 Batch Identity and Determinism

Each batch must have a stable identity derived from the relevant input partition and processing configuration.

The system should preserve deterministic ordering and processing semantics where applicable.

Repeated processing of the same valid batch under the same configuration should not create duplicate output records or corrupt existing results.

### 9.3 Batch Configuration

Batch sizes must be configurable.

The initial configuration must be selected through representative benchmarks that account for:

* Processing throughput.
* Peak RAM usage.
* GPU VRAM usage where relevant.
* Temporary storage requirements.
* Failure recovery cost.
* CPU and GPU utilization.

No fixed batch size is established by this design.

## 10. Checkpointing and Recovery

Checkpointing and resumable execution are required architectural capabilities.

The system must persist sufficient progress information to resume interrupted processing without restarting all completed work unnecessarily.

### 10.1 Checkpoint Information

Checkpoint records should include:

* Processing stage.
* Batch identity.
* Relevant input identifiers or partition information.
* Configuration and artifact versions.
* Completion status.
* Output artifact references.
* Relevant validation or integrity information.

### 10.2 Recovery Behavior

When execution is interrupted, the system must:

1. Identify completed and incomplete batches.
2. Verify that completed batch outputs are valid and compatible with the current configuration.
3. Skip valid completed batches.
4. Resume incomplete or invalid batches safely.
5. Prevent duplicate records when combining recovered outputs.
6. Preserve the integrity of existing valid artifacts.

A checkpoint must not be treated as proof of completion without validating the corresponding output artifacts.

### 10.3 Atomic Publication

Intermediate and final artifacts must be written in a way that prevents partially written results from being mistaken for completed outputs.

Final output files must not be published as valid challenge deliverables until the required validation checks have passed.

## 11. Windows Environment and Dependency Management

The primary execution environment is Windows.

The project must use a dedicated and documented Python environment.

The environment configuration must record relevant software and dependency versions, including components required for:

* Data processing.
* Candidate retrieval and indexing.
* Embedding generation.
* Feature extraction.
* LightGBM training and inference.
* GPU acceleration, where used.

The system must validate the compatibility of the installed Python environment, GPU drivers, CUDA-dependent libraries, and supported model execution modes.

CUDA availability must not be assumed solely from the installed CUDA version.

The implementation must use configurable paths rather than hard-coded machine-specific absolute paths.

The environment and configuration must be documented sufficiently to reproduce execution on the primary workstation.

## 12. Orchestration and Stage Management

The pipeline will use a simple, explicit orchestration mechanism.

The orchestrator must:

* Execute stages in the required order.
* Pass validated artifacts between stages.
* Track stage and batch completion.
* Enforce configuration and artifact compatibility.
* Support checkpoint-based recovery.
* Record structured logs and execution metadata.
* Fail clearly when required inputs or artifacts are missing or invalid.
* Prevent downstream stages from consuming incomplete or incompatible artifacts.

A distributed processing framework is not required by the frozen architecture.

Additional orchestration complexity should be introduced only if a demonstrated requirement justifies it.

## 13. Logging, Monitoring, and Operational Visibility

The system must record enough information to diagnose failures and understand resource usage.

Relevant information includes:

* Stage start and completion times.
* Batch start and completion status.
* Processing throughput.
* Peak memory usage where available.
* GPU utilization and VRAM usage where available.
* Disk-space consumption.
* Candidate and feature record counts.
* Errors, warnings, and recovery actions.
* Configuration and artifact versions.

Logs must be associated with the relevant experiment or execution identifier.

The logging strategy must avoid excessive output that could itself become a significant storage or performance burden.

## 14. Benchmarking and Resource Profiling

Before full-scale execution, representative benchmarks must be conducted.

The benchmarking process must measure:

* Candidate-generation throughput.
* Index construction time and storage size.
* Feature-extraction throughput.
* Embedding-generation throughput and memory requirements.
* CPU versus GPU execution performance where applicable.
* LightGBM CPU versus GPU performance where supported.
* Batch-size and worker-count effects.
* Peak RAM and VRAM usage.
* Intermediate-data storage requirements.
* End-to-end runtime estimates.

Benchmarks must use representative data and configurations.

The final operating configuration must be selected using measured performance and reliability rather than assumptions about hardware utilization.

## 15. Parameters Requiring Experimental Tuning

| Parameter               | What must be determined                                                  |
| ----------------------- | ------------------------------------------------------------------------ |
| Batch size              | Suitable batch sizes for each major pipeline stage                       |
| CPU worker count        | Worker counts that balance throughput and resource consumption           |
| GPU usage               | Which workloads benefit from GPU execution                               |
| Embedding batch size    | Batch size compatible with VRAM and throughput requirements              |
| Index configuration     | Index parameters, memory usage, and retrieval performance                |
| Storage formats         | Practical formats for each major intermediate artifact                   |
| Memory allocation       | Safe working-memory limits for concurrent stages                         |
| Parallelization         | Which stages should run concurrently and under what limits               |
| Checkpoint frequency    | Appropriate checkpoint granularity and recovery overhead                 |
| Storage budget          | Feasible artifact-retention and temporary-storage strategy               |
| Execution configuration | Final validated combination of batch sizes, workers, and resource limits |

No exact batch size, worker count, memory allocation, or end-to-end runtime is frozen by this design.

## 16. Acceptance and Completion Conditions

The system architecture is considered compliant when:

1. Full-scale execution is supported on the primary workstation.
2. Processing is batch-oriented and does not require the entire workload to fit in memory.
3. Reusable indexes and compatible intermediate artifacts can be persisted and reused.
4. CPU and GPU workloads are assigned according to validated execution configurations.
5. Storage feasibility is assessed before large-scale processing.
6. Original inputs and required artifacts are protected from unintended modification or deletion.
7. Checkpointing and recovery support safe resumption of interrupted execution.
8. Completed artifacts are validated before being reused.
9. Final outputs are published only after validation.
10. Environment and configuration versions are recorded.
11. Processing progress, errors, and relevant resource usage are observable.
12. Execution can be reproduced using the documented environment and configuration.

## 17. Decision Summary

| Decision                                                          | Status                              |
| ----------------------------------------------------------------- | ----------------------------------- |
| Primary workstation for full-scale execution                      | Frozen                              |
| Laptop for secondary development and lightweight work             | Frozen                              |
| Single-workstation architecture by default                        | Frozen                              |
| Batch-oriented processing                                         | Frozen                              |
| Reusable target-source indexes                                    | Frozen                              |
| Disk-backed intermediate artifacts                                | Frozen                              |
| CPU-first general data processing with workload-dependent GPU use | Frozen                              |
| Checkpointing and resumable execution                             | Frozen                              |
| Explicit orchestration without a distributed framework by default | Frozen                              |
| Input preservation and validated artifact reuse                   | Frozen                              |
| Environment and configuration versioning                          | Frozen                              |
| Exact batch sizes and worker counts                               | Experimental                        |
| CPU/GPU execution choices for individual workloads                | To be benchmarked                   |
| Storage layout and artifact-retention policy                      | To be finalized                     |
| Final resource configuration                                      | To be selected through benchmarking |


# Design 5: Inference & Prediction Pipeline

## 1. Purpose

The Inference & Prediction Pipeline processes the challenge's test datasets and produces the final entity-matching predictions.

For every S1 test entity, the pipeline must identify zero, one, or multiple matching entities from S2 and S3.

The pipeline applies the frozen candidate-generation architecture, extracts the shared pairwise feature schema, scores candidate pairs using the selected trained model, applies the selected matching policy, and generates the required output files.

The primary objectives are:

* Correct and complete processing of every test S1 entity.
* Consistency with the training and validation pipelines.
* Reliable candidate generation and model scoring.
* Correct application of the selected decision policy.
* Compliance with the official output schema.
* Deterministic, resumable execution at the full dataset scale.

## 2. Scope and Input Data

### 2.1 Test Inputs

The inference pipeline consumes three test datasets:

* S1: Reference entities for which predictions must be generated.
* S2: First target source.
* S3: Second target source.

The available entity fields are:

* `entity_id`
* `business_name`
* `business_address`
* `country`

The source associated with each record must be identifiable.

### 2.2 Input Validation

Before processing, the system must validate:

* Required input files are available.
* Required columns are present.
* Entity IDs are valid and usable.
* Source membership is consistent with the input dataset.
* Input records can be parsed using the configured data types.
* Missing and malformed values are handled according to the frozen preprocessing conventions.
* The original S1 row order is preserved.

Critical input errors must be reported clearly and must prevent invalid processing from being treated as successful.

## 3. Frozen Architectural Decision: Batch-Oriented Inference

The system will use a batch-oriented inference pipeline that processes S1 entities against reusable target-source indexes for S2 and S3.

The high-level inference flow is:

1. Load and validate test datasets.
2. Load the selected model and its associated configuration.
3. Load or construct compatible target-source indexes.
4. Process S1 entities in batches.
5. Generate candidates using the frozen hybrid candidate-generation architecture.
6. Deduplicate candidates and retain retrieval provenance.
7. Extract pairwise features using the frozen shared feature schema.
8. Score candidate pairs with the selected LightGBM model.
9. Apply the selected matching decision policy.
10. Persist candidate and prediction results.
11. Validate the required output files.
12. Publish the final outputs only after validation succeeds.

The pipeline must not require the entire candidate universe or complete feature matrix to fit in memory.

## 4. Model and Configuration Loading

Before scoring, the pipeline must load the selected final model and its associated metadata.

The loaded artifacts must identify:

* Model family and version.
* Feature-schema version.
* Preprocessing configuration.
* Candidate-generation configuration.
* Selected decision threshold or policy.
* Calibration configuration, if applicable.
* Relevant artifact and experiment identifiers.

The system must verify that the model, feature schema, preprocessing pipeline, candidate-generation configuration, and decision policy are compatible.

If required artifacts are missing or incompatible, the pipeline must fail clearly rather than silently substituting a different configuration.

The inference pipeline must use the selected final model artifact, not an unapproved experimental model.

## 5. Preprocessing and Normalization

Test records must be processed using the same approved preprocessing and normalization conventions used during training.

The system must:

* Preserve raw input values.
* Apply the selected normalization rules consistently.
* Handle missing and malformed values according to the feature schema.
* Avoid introducing test-specific transformations that alter the model's expected feature representation.
* Maintain a consistent relationship between raw records and normalized representations.

Any preprocessing configuration change that affects candidate generation or feature extraction must be versioned and validated before inference.

## 6. Candidate Generation

Candidate generation must follow Design 1: Candidate Generation.

For every S1 entity, the pipeline must retrieve potential matches from both S2 and S3 using the configured retrieval methods:

1. Exact and normalized-name blocking.
2. Token-based name retrieval.
3. Character n-gram and fuzzy-name retrieval.
4. Address-based retrieval.
5. Country-aware retrieval.
6. Embedding-based nearest-neighbor retrieval.

The results must be combined using a union operation and deduplicated by candidate entity ID.

Retrieval provenance and applicable method-specific scores must be retained.

Candidate generation must not inject ground-truth matches or apply unapproved hard-rejection rules.

The resulting unified candidate set is used by both the feature-extraction stage and the candidate-pairs output.

## 7. Pairwise Feature Extraction

For every generated candidate pair, the pipeline must extract the feature vector defined by Design 2: Pairwise Feature Extraction.

The following must remain consistent with training:

* Feature names and ordering.
* Feature data types.
* Name and address normalization.
* Similarity and comparison algorithms.
* Missing-value handling.
* Cross-field interactions.
* Candidate-generation evidence representation.
* Source-pair indicator.
* Numerical representation.

Each feature vector must remain associated with the correct S1 entity and candidate entity.

The pipeline must not omit or silently reorder features expected by the trained model.

## 8. Model Scoring

The selected LightGBM model must score each candidate pair using its extracted feature vector.

The scoring stage must:

* Process candidate pairs in batches.
* Preserve the association between each score and its candidate pair.
* Use the selected model artifact and compatible feature schema.
* Apply calibration only if it is part of the selected and validated configuration.
* Record or preserve the score information needed for decision-making and debugging.

Every candidate pair must be scored according to the selected inference configuration unless a clearly documented and validated operational exception applies.

## 9. Final Matching Decision Policy

### 9.1 Default Policy

The default inference policy is a global decision threshold selected during validation to optimize the official macro F0.5 metric.

A candidate pair is retained as a final match when its model score satisfies the selected threshold policy.

The threshold must be loaded from the selected model's associated inference configuration.

The pipeline must not assume that the threshold is 0.5 or substitute a different threshold without approval and validation.

### 9.2 Multiple and Zero Matches

The matching policy must support:

* Zero matches for an S1 entity.
* One match for an S1 entity.
* Multiple matches for an S1 entity.

All candidate IDs that satisfy the selected decision policy must be retained.

The pipeline must not impose a one-to-one constraint or an arbitrary maximum number of matches per S1 entity.

If no candidate passes the decision policy, the final matched-entity list must be empty.

### 9.3 Policy Consistency

The inference pipeline must apply the exact selected decision policy used for the final model configuration.

Any validated alternative policy, such as source-pair-specific thresholds, must be explicitly recorded and applied consistently.

## 10. Candidate-Pairs Output

The system must produce:

`output/candidate_pairs.tsv`

### 10.1 Required Schema

| Column                 | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| `source1_entity_id`    | Entity ID of the S1 reference record                 |
| `candidate_entity_ids` | Unique candidate entity IDs retrieved from S2 and S3 |

### 10.2 Output Requirements

The candidate-pairs output must:

* Contain exactly one row for every test S1 entity.
* Preserve the original S1 row order.
* Include all unique candidates retrieved before final model thresholding.
* Include candidates from S2 and S3 only.
* Avoid duplicate candidate IDs within each list.
* Represent an empty candidate list using the agreed empty-list serialization.
* Preserve the required column names and ordering.

The candidate-pairs output records retrieval results, not final accepted matches.

## 11. Matching-Results Output

The system must produce:

`output/matching_results.tsv`

### 11.1 Required Schema

| Column               | Description                                        |
| -------------------- | -------------------------------------------------- |
| `source1_entity_id`  | Entity ID of the S1 reference record               |
| `matched_entity_ids` | Unique target entity IDs selected as final matches |

### 11.2 Output Requirements

The matching-results output must:

* Contain exactly one row for every test S1 entity.
* Preserve the original S1 row order.
* Include only matched entity IDs from S2 and S3.
* Include all candidate IDs accepted by the selected decision policy.
* Avoid duplicate matched IDs within each list.
* Represent an empty match list using the agreed empty-list serialization.
* Preserve the required column names and ordering.

The system must not omit an S1 entity merely because no match was found.

## 12. Relationship Between the Two Output Files

The two output files serve different purposes:

* `candidate_pairs.tsv` records all unique retrieved candidates before model thresholding.
* `matching_results.tsv` records the final candidates accepted as matches.

Every final matched entity ID must belong to the candidate set generated for the corresponding S1 entity.

The system must validate that the final matched-ID list is a subset of the candidate-ID list for each S1 entity.

The candidate-pairs file must not be reduced to only the accepted matches.

## 13. Output Serialization and Validation

Before publishing the output files, the system must validate:

### 13.1 File and Schema Validation

* Both required files exist.
* Both files use the required TSV format.
* Column names and ordering are correct.
* Every S1 test entity is represented exactly once.
* Row counts match the number of test S1 entities.

### 13.2 Entity and List Validation

* S1 IDs correspond to the test S1 dataset.
* Candidate IDs belong to S2 or S3.
* Matched IDs belong to S2 or S3.
* Candidate lists contain no duplicate IDs.
* Matched lists contain no duplicate IDs.
* Every matched ID is present in the corresponding candidate list.
* Empty lists are serialized consistently.

### 13.3 Ordering and Integrity Validation

* S1 output order matches the original S1 test order.
* No S1 entities are missing or duplicated.
* No invalid target-source IDs are included.
* The two output files are consistent with one another.

### 13.4 Publication

Final output files must be published only after all required validation checks succeed.

The pipeline must avoid presenting incomplete or partially written files as valid challenge deliverables.

## 14. Batch Processing, Checkpointing, and Recovery

Inference must support resumable, batch-oriented execution in accordance with Design 4: System Architecture & Resource Management.

The pipeline must:

* Process S1 entities in deterministic batches.
* Persist intermediate candidate and prediction results.
* Record batch completion status.
* Verify artifact and configuration compatibility when resuming.
* Skip valid completed batches.
* Reprocess incomplete or invalid batches safely.
* Prevent duplicate rows when combining batch outputs.
* Preserve original S1 order when assembling final outputs.
* Validate completed artifacts before reuse.

A failure in one batch must not require restarting all previously completed valid batches.

## 15. Logging and Execution Metadata

The inference pipeline must record:

* Input dataset identifiers or versions.
* Model and configuration versions.
* Candidate-generation and feature-schema versions.
* Batch identities and completion status.
* Candidate counts and accepted match counts.
* Processing time and relevant resource usage.
* Errors, warnings, and recovery actions.
* Output artifact locations and validation results.

The execution record must be sufficient to identify the configuration that produced the final outputs.

## 16. Parameters Requiring Experimental or Implementation-Level Configuration

| Parameter                   | What must be determined                                                                      |
| --------------------------- | -------------------------------------------------------------------------------------------- |
| Inference batch size        | Suitable S1 and candidate-pair batch sizes                                                   |
| Retrieval limits            | Final candidate-generation limits selected through validation                                |
| Scoring batch size          | Batch size appropriate for model inference and memory usage                                  |
| Decision threshold          | Selected threshold from the final validated model configuration                              |
| Calibration                 | Whether calibration is enabled and which configuration is used                               |
| Intermediate storage format | Format and partitioning for candidate and prediction artifacts                               |
| Checkpoint granularity      | Batch-level checkpoint configuration                                                         |
| Worker count                | Suitable processing concurrency                                                              |
| Final serialization details | Exact representation of empty lists and list delimiters consistent with the challenge format |

The required output filenames, column names, and row-order semantics are frozen. Numerical execution settings remain configurable and must be validated.

## 17. Acceptance and Completion Conditions

The inference pipeline is considered compliant when:

1. All test input datasets are validated before processing.
2. The selected model and associated configurations are loaded and verified.
3. Candidate generation follows the frozen hybrid architecture.
4. Feature extraction uses the same schema and conventions as training.
5. Candidate pairs are scored using the selected model.
6. The validated matching policy is applied consistently.
7. Zero, one, or multiple matches are supported.
8. Both required output files are produced with the exact required columns.
9. Each output contains one row per test S1 entity in original S1 order.
10. Candidate and match IDs belong exclusively to S2 or S3.
11. Candidate and match lists contain no duplicate IDs.
12. Final matches are a subset of the corresponding candidate set.
13. Empty candidate and match lists are represented consistently.
14. Batch processing supports safe checkpointing and recovery.
15. Output validation succeeds before final publication.
16. The execution configuration and artifacts are recorded for reproducibility.

## 18. Decision Summary

| Decision                                                          | Status                                             |
| ----------------------------------------------------------------- | -------------------------------------------------- |
| Batch-oriented inference pipeline                                 | Frozen                                             |
| Reuse of candidate-generation and feature-extraction architecture | Frozen                                             |
| Use of selected LightGBM model artifact                           | Frozen                                             |
| Consistent preprocessing and feature schema                       | Frozen                                             |
| Application of selected decision policy                           | Frozen                                             |
| Support for zero, one, or multiple matches                        | Frozen                                             |
| No one-to-one constraint or arbitrary maximum matches             | Frozen                                             |
| `output/candidate_pairs.tsv` schema and semantics                 | Frozen                                             |
| `output/matching_results.tsv` schema and semantics                | Frozen                                             |
| One output row per test S1 entity in original order               | Frozen                                             |
| Candidate and match list uniqueness                               | Frozen                                             |
| Match list must be a subset of candidate list                     | Frozen                                             |
| Output validation before publication                              | Frozen                                             |
| Checkpointed, resumable inference                                 | Frozen                                             |
| Batch sizes and worker counts                                     | Experimental                                       |
| Final decision threshold                                          | Selected through validation                        |
| Exact serialization conventions for empty lists                   | To be confirmed against the official output format |


# Design 6: Evaluation & Experiment Management

## 1. Purpose

This design defines how the entity-matching system will be evaluated, how experiments will be conducted and compared, how the final model and decision threshold will be selected, and how the final system will be verified before generating the challenge outputs.

The primary objective is to maximize the official **macro-averaged F₀.₅ score**, while ensuring that the evaluation process is reproducible, computationally feasible, and representative of the final inference pipeline.

Evaluation must distinguish between two independent sources of failure:

1. **Candidate-generation failure:** A true match is not retrieved as a candidate and therefore cannot be recovered by the model.
2. **Matching-model failure:** A true match is retrieved as a candidate but is incorrectly classified or excluded by the final decision threshold.

The evaluation framework must measure both independently and jointly.

---

## 2. Evaluation Principles

The following principles are mandatory:

1. Use the official challenge metric as the primary model-selection objective.
2. Evaluate the complete pipeline, not only the classification model.
3. Keep training, validation, and final test data strictly separated.
4. Use the same candidate-generation and feature-extraction logic in training, validation, and inference.
5. Never inject ground-truth matches into candidate generation during validation or inference.
6. Preserve the natural candidate distribution in validation rather than artificially balancing positive and negative pairs.
7. Record every experiment's configuration, dataset version, model parameters, threshold, and evaluation results.
8. Do not select a model or configuration based solely on one favorable metric or one experiment.
9. Prefer reproducible improvements over unverified complexity.
10. Keep the final test set untouched during model selection and threshold tuning.

---

## 3. Evaluation Metrics

### 3.1 Primary Metric: Macro F₀.₅

The official evaluation metric is macro-averaged F₀.₅ over S1 entities.

For each S1 entity, precision and recall are calculated from its predicted matches and ground-truth matches. The per-entity F₀.₅ scores are then averaged across S1 entities according to the official challenge definition.

The F-score is:

$$
F_{0.5} =
\frac{1.25 \times P \times R}
{0.25 \times P + R}
$$

Where:

* \(P\) = precision.
* \(R\) = recall.

The metric gives greater weight to precision than recall. Consequently, false-positive matches can reduce the score substantially.

**Implementation requirement:** The exact official aggregation procedure, treatment of entities with empty ground-truth or predicted match sets, and handling of zero denominators must be confirmed from the challenge evaluator or official scoring implementation. The internal evaluator must reproduce that behavior exactly.

### 3.2 Supporting Metrics

The following metrics must be recorded alongside the primary score.

| Metric                          | Purpose                                                        |
| ------------------------------- | -------------------------------------------------------------- |
| Macro F₀.₅                      | Primary model-selection metric                                 |
| Macro precision                 | Measures the correctness of predicted matches                  |
| Macro recall                    | Measures recovery of known matches                             |
| Candidate recall                | Measures how many ground-truth matches enter the candidate set |
| Candidate volume                | Measures the number of candidates generated                    |
| Candidate reduction ratio       | Measures the reduction from exhaustive pairwise comparison     |
| Pair-level precision and recall | Diagnostic view of individual candidate-pair classification    |
| PR-AUC                          | Diagnostic measure of ranking quality under class imbalance    |
| Inference runtime               | Measures end-to-end processing time                            |
| Peak RAM usage                  | Measures memory consumption                                    |
| Disk usage                      | Measures intermediate and artifact storage requirements        |

Supporting metrics must not replace the official metric during final selection.

---

## 4. Candidate-Generation Evaluation

Candidate generation must be evaluated independently before judging the matching model.

### 4.1 Candidate Recall

For each S1 entity, determine whether each ground-truth match appears in the generated candidate set.

Candidate recall is calculated as:

$$
\text{Candidate Recall} =
\frac{\text{Ground-truth matches retrieved as candidates}}
{\text{Total ground-truth matches}}
$$

The evaluation must also report:

* Overall candidate recall.
* Candidate recall for S1–S2 and S1–S3 separately.
* Candidate recall by country where sufficient examples exist.
* Candidate recall for entities with one match versus multiple matches.
* Candidate recall by candidate-generation method.
* Number of true matches missed by all candidate-generation methods.

### 4.2 Candidate Volume and Efficiency

For each candidate-generation configuration, record:

* Total candidate pairs.
* Average and median candidates per S1 entity.
* Candidate-count distribution, including high-volume entities.
* Candidate reduction ratio relative to exhaustive comparison.
* Runtime and peak memory usage.
* Storage required for candidate outputs.

Candidate-generation configurations must be compared on the trade-off between match recovery and computational cost.

### 4.3 Method Contribution Analysis

Because candidate generation uses multiple retrieval methods, evaluate each method's contribution.

Record:

* True matches uniquely recovered by each method.
* Additional true matches recovered when the method is added to the existing union.
* Number of candidates introduced by each method.
* Incremental candidate recall.
* Additional runtime and storage cost.

A method should not be removed solely because its individual recall is low. Its incremental contribution to the union must be considered.

---

## 5. Validation Strategy

### 5.1 Entity-Level Data Split

The training data must be divided into training and validation partitions at the S1 entity level.

The initial split will use a **90% training / 10% validation** allocation, subject to data availability and computational feasibility.

All candidate pairs associated with an S1 entity must remain in the same partition to prevent leakage between training and validation.

Where practical, the split should preserve the distribution of:

* Entities with and without known matches.
* Match counts per S1 entity.
* S1–S2 and S1–S3 source pairs.
* Countries.

The split must be generated once, saved, and reused for comparable experiments.

### 5.2 Candidate Generation During Validation

Validation candidate generation must follow the same procedure as inference.

The system must:

1. Generate candidates using the configured retrieval methods.
2. Deduplicate candidate IDs.
3. Extract features using the frozen feature schema.
4. Score candidate pairs using the trained model.
5. Apply the selected decision threshold.
6. Evaluate predictions against the validation ground truth.

Ground-truth matches must not be added to the candidate set artificially.

### 5.3 Validation Integrity

The following are prohibited:

* Using validation labels to train the model.
* Using validation results to construct training-only hard negatives.
* Modifying candidate sets based on validation ground truth.
* Repeatedly changing the validation split to obtain a higher score.
* Selecting the final threshold using test labels.
* Reporting training performance as validation performance.

All validation-specific tuning must be recorded in the experiment log.

---

## 6. Controlled Experiment Management

### 6.1 Experiment Categories

Experiments must be organized into clearly defined categories.

| Category             | Objective                                                               |
| -------------------- | ----------------------------------------------------------------------- |
| Baseline             | Establish a reproducible reference score                                |
| Candidate generation | Evaluate retrieval methods, retrieval limits, and candidate recall      |
| Feature engineering  | Measure the effect of feature groups and individual feature changes     |
| Model training       | Compare model parameters and training strategies                        |
| Negative sampling    | Evaluate hard-negative composition and sampling strategies              |
| Threshold tuning     | Identify the decision threshold that maximizes validation macro F₀.₅    |
| System performance   | Measure runtime, memory, storage, and processing throughput             |
| Final verification   | Confirm that the selected configuration reproduces its expected results |

### 6.2 Controlled Changes

Each experiment must have a clearly stated objective and hypothesis.

Whenever possible, change one major factor at a time while keeping the remaining configuration fixed.

For interactions between multiple factors, use a structured experiment that records all changed variables.

Each experiment must include:

* Experiment ID.
* Date and time.
* Objective and hypothesis.
* Dataset and split versions.
* Candidate-generation configuration.
* Feature schema version.
* Model family and parameters.
* Negative-sampling configuration.
* Decision threshold.
* Evaluation metrics.
* Runtime and resource usage.
* Outcome and decision.

### 6.3 Experiment Comparison

Experiments must be compared against a stable baseline using the same validation split and evaluation implementation.

The comparison should include:

* Change in macro F₀.₅.
* Change in precision and recall.
* Change in candidate recall.
* Change in candidate volume.
* Change in runtime and resource requirements.
* Whether the improvement is consistent across relevant subsets.

A more complex configuration must demonstrate a measurable benefit that justifies its additional computational or operational cost.

---

## 7. Model Selection and Threshold Optimization

### 7.1 Model Selection

LightGBM is the primary model family.

The baseline model and subsequent experiments must be evaluated using the same candidate-generation configuration, feature schema, validation split, and official metric implementation.

Alternative models may be evaluated only through controlled experiments.

Model selection must consider:

* Validation macro F₀.₅.
* Precision and recall behavior.
* Performance across source pairs and relevant data subsets.
* Runtime, memory, and storage requirements.
* Reproducibility and inference compatibility.

### 7.2 Threshold Optimization

The model produces a score for each candidate pair. A decision threshold determines which candidates become predicted matches.

The threshold must be selected using validation predictions by evaluating a range of candidate thresholds and computing the official macro F₀.₅ score for each.

The selected threshold must:

1. Maximize validation macro F₀.₅ under the official scoring definition.
2. Be recorded with the model artifact and experiment configuration.
3. Be evaluated for stability around nearby threshold values.
4. Be applied consistently during final inference.

The initial policy is a **single global threshold** across S1–S2 and S1–S3 candidate pairs.

Source-pair-specific thresholds or other entity-level decision policies may be introduced only if controlled validation experiments demonstrate a reliable improvement.

No one-to-one matching constraint or maximum number of predicted matches per S1 entity may be imposed unless explicitly required by the challenge specification.

### 7.3 Threshold Stability

The evaluation must inspect how the validation score changes around the selected threshold.

A narrow peak or large score fluctuation may indicate that the threshold is sensitive to small changes in prediction scores.

The experiment report must record:

* Selected threshold.
* Best validation macro F₀.₅.
* Scores at nearby thresholds.
* Corresponding precision and recall.
* Number of predicted matches at each threshold.

If multiple thresholds produce nearly identical scores, the final selection should favor a stable and operationally reproducible choice rather than relying solely on a tiny score difference.

---

## 8. Error Analysis

Error analysis must be performed on validation predictions to identify the principal sources of matching failure.

### 8.1 False Positives

Analyze predicted matches that are not present in the supplied ground truth.

Group errors by patterns such as:

* Similar or identical business names but different businesses.
* Shared addresses or common locations.
* Generic business names.
* Conflicting address components.
* Country disagreement.
* Common tokens or weakly distinctive names.
* Retrieval methods that generate large numbers of weak candidates.

### 8.2 False Negatives

Analyze known matches that are not predicted.

Separate them into:

1. **Candidate-generation misses:** The true match was never retrieved.
2. **Model-ranking or classification errors:** The true match was retrieved but received a score below the selected threshold.

Investigate patterns involving:

* Name variation and transliteration.
* Missing or incomplete addresses.
* Address disagreement or outdated information.
* Country-field inconsistencies.
* Weak candidate-generation coverage.
* Insufficiently informative features.
* Threshold-related exclusions.

### 8.3 Error Analysis Outputs

Each analysis cycle should produce:

* Error counts and rates.
* Representative anonymized or appropriately protected examples.
* Error categories and their frequency.
* Candidate-generation versus model-related failure breakdown.
* Proposed corrective experiment.
* Measured result of the corrective experiment.

Changes must be validated through controlled experiments rather than assumed to improve performance.

---

## 9. Reproducibility and Experiment Artifacts

Every completed experiment must be reproducible from its recorded configuration and artifacts.

The system must retain, where applicable:

* Dataset version or file fingerprints.
* Training and validation split definitions.
* Candidate-generation configuration.
* Feature schema and preprocessing version.
* Model parameters and trained model artifact.
* Negative-sampling configuration and random seeds.
* Decision threshold and optional calibration settings.
* Validation predictions or sufficient artifacts to reproduce them.
* Evaluation report.
* Runtime and resource measurements.
* Software environment and dependency versions.
* Experiment logs and completion status.

Random seeds must be fixed wherever supported. Any nondeterministic operations must be documented.

Experiment artifacts must be stored in a structured directory layout with unique experiment identifiers. An experiment must not overwrite a previous successful experiment's artifacts.

---

## 10. Final Model Selection and Retraining

After validation experiments are complete:

1. Select the final candidate-generation configuration, feature schema, model configuration, and threshold based on validation evidence.
2. Record the selected configuration as the final experiment.
3. Retrain the selected model on all eligible training data using the finalized training procedure.
4. Preserve the selected feature schema, candidate-generation configuration, and decision policy.
5. Store the final model artifact together with its configuration and version metadata.
6. Run inference on the official test data without using test ground truth.
7. Validate the output files against the challenge's required structure and constraints.

The validation score must remain the reported model-selection score. The final retrained model's training score must not be presented as an independent validation result.

Any material change to the candidate-generation method, features, model family, training strategy, or threshold after final selection requires a new recorded experiment and validation evaluation.

---

## 11. Evaluation and Experiment Acceptance Criteria

An experiment is considered complete only when:

* Its configuration and dataset versions are recorded.
* The training and validation split is respected.
* Candidate generation and feature extraction follow the approved pipeline.
* The evaluation uses the official macro F₀.₅ definition.
* Candidate recall and candidate volume are reported.
* Precision, recall, and supporting metrics are recorded.
* Threshold selection is documented when applicable.
* Runtime and resource usage are recorded where feasible.
* Results are reproducible or any limitations are documented.
* The experiment's outcome and next action are recorded.

The final system is ready for submission only after:

* The final model and threshold are selected and versioned.
* The inference pipeline completes successfully.
* The required output files pass structural and semantic validation.
* All S1 test entities are represented in the required order.
* Candidate and match IDs belong to the permitted sources.
* No duplicate IDs occur within a candidate or match list.
* Every predicted match is included in the corresponding candidate list.
* The final outputs are produced without using test ground truth.

---

## 12. Frozen Decisions vs. Experimental Parameters

| Item                                                          | Status                           |
| ------------------------------------------------------------- | -------------------------------- |
| Official macro F₀.₅ as primary objective                      | Frozen                           |
| Candidate recall evaluated separately                         | Frozen                           |
| Entity-level training/validation separation                   | Frozen                           |
| Same candidate-generation process in validation and inference | Frozen                           |
| Validation ground-truth isolation                             | Frozen                           |
| Controlled and reproducible experiments                       | Frozen                           |
| Validation-based threshold optimization                       | Frozen                           |
| Global threshold as initial decision policy                   | Frozen                           |
| LightGBM as primary model family                              | Frozen                           |
| Exact validation split seed                                   | To be configured                 |
| Candidate-generation limits                                   | To be tuned                      |
| Negative-sampling proportions                                 | To be tuned                      |
| Feature-selection decisions                                   | To be evaluated                  |
| Model hyperparameters                                         | To be tuned                      |
| Threshold value                                               | To be determined from validation |
| Source-pair-specific thresholds                               | Experimental only                |
| Final model configuration                                     | To be selected after evaluation  |

---

## 13. Design Summary

The evaluation and experiment-management system will provide a controlled, reproducible process for improving the complete entity-matching pipeline.

Candidate generation will be evaluated for match recovery and computational efficiency. The matching model will be evaluated using the official macro F₀.₅ metric, with precision, recall, and threshold stability as supporting diagnostics. All experiments will use an entity-level validation split and maintain strict separation between training, validation, and test data.

The final configuration will be selected based on recorded validation evidence, retrained on eligible training data, and verified through the official output requirements before submission.

**Final principle:** Every material change must be supported by a reproducible experiment, and the final system must be evaluated as a complete pipeline rather than as a classifier in isolation.

## 14. Multilingual Matching Extension Addendum

The targeted multilingual architecture revision is documented in [MULTILINGUAL_ARCHITECTURE_ADDENDUM.md](MULTILINGUAL_ARCHITECTURE_ADDENDUM.md). It is a **proposed extension pending benchmark validation**, not an approved production change. The six existing candidate-generation families, LightGBM classifier, feature/output contracts, open-valued country handling, entity-level split, and macro-F0.5 objective remain frozen. The addendum defines the proposed script-aware retrieval path, optional validated multilingual features, subgroup validation, France verification requirements, and the evidence required before implementation approval.
