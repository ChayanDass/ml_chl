# Requirements Traceability Matrix

## Document Control

| Field | Value |
|---|---|
| Baseline | `SRS-BL-1.0`, `docs/SRS.md` v1.0 |
| Design artifact | `docs/TECHNICAL_DESIGN.md` v0.2 (Draft — revised pending fresh audit) |
| Mapping basis | 213 unique requirement-definition IDs independently extracted from SRS requirement-definition lines |
| Status | Planned verification only; no implementation test is claimed as executed |

Each defined SRS functional requirement is enumerated exactly once below. “Planned” identifies future verification; it is not a pass result. Section references are precise existing TDD headings.

## Functional Requirement Mapping

| SRS ID | Exact TDD location | Responsible component | Verification method / artifact | Observable pass criterion |
|---|---|---|---|---|
| FR-7.1.1 | §5 | Ingestion | Planned `T-ING-7.1.1` | Required TSV is UTF-8 decoded, schema-valid, source-tagged, and fingerprinted. |
| FR-7.1.2 | §5 | Ingestion | Planned `T-ING-7.1.2` | Required TSV is UTF-8 decoded, schema-valid, source-tagged, and fingerprinted. |
| FR-7.1.3 | §5 | Ingestion | Planned `T-ING-7.1.3` | Required TSV is UTF-8 decoded, schema-valid, source-tagged, and fingerprinted. |
| FR-7.1.4 | §5 | Ingestion | Planned `T-ING-7.1.4` | Required TSV is UTF-8 decoded, schema-valid, source-tagged, and fingerprinted. |
| FR-7.1.5 | §5 | Ingestion | Planned `T-ING-7.1.5` | Required TSV is UTF-8 decoded, schema-valid, source-tagged, and fingerprinted. |
| FR-7.1.6 | §5 | Ingestion | Planned `T-ING-7.1.6` | Required TSV is UTF-8 decoded, schema-valid, source-tagged, and fingerprinted. |
| FR-7.2.1 | §5 | Input validation | Planned `T-VAL-7.2.1` | Invalid fixture is classified correctly and does not become matching evidence. |
| FR-7.2.2 | §5 | Input validation | Planned `T-VAL-7.2.2` | Invalid fixture is classified correctly and does not become matching evidence. |
| FR-7.2.3 | §5 | Input validation | Planned `T-VAL-7.2.3` | Invalid fixture is classified correctly and does not become matching evidence. |
| FR-7.2.4 | §5 | Input validation | Planned `T-VAL-7.2.4` | Invalid fixture is classified correctly and does not become matching evidence. |
| FR-7.2.5 | §5 | Input validation | Planned `T-VAL-7.2.5` | Invalid fixture is classified correctly and does not become matching evidence. |
| FR-7.2.6 | §5 | Input validation | Planned `T-VAL-7.2.6` | Invalid fixture is classified correctly and does not become matching evidence. |
| FR-7.2.7 | §5 | Input validation | Planned `T-VAL-7.2.7` | Invalid fixture is classified correctly and does not become matching evidence. |
| FR-7.3.1 | §5 | Preprocessing | Planned `T-PRE-7.3.1` | Raw value is retained and configured normalized/missing representation is reproducible. |
| FR-7.3.2 | §5 | Preprocessing | Planned `T-PRE-7.3.2` | Raw value is retained and configured normalized/missing representation is reproducible. |
| FR-7.3.3 | §5 | Preprocessing | Planned `T-PRE-7.3.3` | Raw value is retained and configured normalized/missing representation is reproducible. |
| FR-7.3.4 | §5 | Preprocessing | Planned `T-PRE-7.3.4` | Raw value is retained and configured normalized/missing representation is reproducible. |
| FR-7.3.5 | §5 | Preprocessing | Planned `T-PRE-7.3.5` | Raw value is retained and configured normalized/missing representation is reproducible. |
| FR-7.4.1 | §5 | Preprocessing | Planned `T-PRE-7.4.1` | Raw value is retained and configured normalized/missing representation is reproducible. |
| FR-7.4.2 | §5 | Preprocessing | Planned `T-PRE-7.4.2` | Raw value is retained and configured normalized/missing representation is reproducible. |
| FR-7.4.3 | §5 | Preprocessing | Planned `T-PRE-7.4.3` | Raw value is retained and configured normalized/missing representation is reproducible. |
| FR-7.4.4 | §5 | Preprocessing | Planned `T-PRE-7.4.4` | Raw value is retained and configured normalized/missing representation is reproducible. |
| FR-7.4.5 | §5 | Preprocessing | Planned `T-PRE-7.4.5` | Raw value is retained and configured normalized/missing representation is reproducible. |
| FR-7.5.1 | §6.2–§6.7 | Candidate generation | Planned `T-CG-7.5.1` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.2 | §6.2–§6.7 | Candidate generation | Planned `T-CG-7.5.2` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.3 | §6.2–§6.7 | Candidate generation | Planned `T-CG-7.5.3` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.4 | §6.2–§6.7 | Candidate generation | Planned `T-CG-7.5.4` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.5 | §6.2–§6.7 | Candidate generation | Planned `T-CG-7.5.5` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.6 | §6.2–§6.7 | Candidate generation | Planned `T-CG-7.5.6` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.7 | §6.8–§6.10 | Candidate generation | Planned `T-CG-7.5.7` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.8 | §6.8–§6.10 | Candidate generation | Planned `T-CG-7.5.8` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.9 | §6.8–§6.10 | Candidate generation | Planned `T-CG-7.5.9` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.10 | §6.8–§6.10 | Candidate generation | Planned `T-CG-7.5.10` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.11 | §6.8–§6.10 | Candidate generation | Planned `T-CG-7.5.11` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.12 | §6.8–§6.10 | Candidate generation | Planned `T-CG-7.5.12` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.5.13 | §6.8–§6.10 | Candidate generation | Planned `T-CG-7.5.13` | Candidate result and manifest satisfy the stated retrieval, union, provenance, and no-label-injection invariant. |
| FR-7.6.1 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.6.1` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.6.2 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.6.2` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.6.3 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.6.3` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.6.4 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.6.4` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.6.5 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.6.5` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.6.6 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.6.6` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.6.7 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.6.7` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.7.1 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.7.1` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.7.2 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.7.2` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.7.3 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.7.3` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.7.4 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.7.4` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.7.5 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.7.5` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.7.6 | §6.8–§6.10 | Candidate management | Planned `T-CAND-7.7.6` | Pair/source/ID/provenance contract check passes for a deterministic batch. |
| FR-7.8.1 | §7.1–§7.7 | Feature extraction | Planned `T-FEAT-7.8.1` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.2 | §7.1–§7.7 | Feature extraction | Planned `T-FEAT-7.8.2` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.3 | §7.1–§7.7 | Feature extraction | Planned `T-FEAT-7.8.3` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.4 | §7.1–§7.7 | Feature extraction | Planned `T-FEAT-7.8.4` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.5 | §7.1–§7.7 | Feature extraction | Planned `T-FEAT-7.8.5` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.6 | §7.1–§7.7 | Feature extraction | Planned `T-FEAT-7.8.6` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.7 | §7.1–§7.7 | Feature extraction | Planned `T-FEAT-7.8.7` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.8 | §7.8–§7.10 | Feature extraction | Planned `T-FEAT-7.8.8` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.9 | §7.8–§7.10 | Feature extraction | Planned `T-FEAT-7.8.9` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.10 | §7.8–§7.10 | Feature extraction | Planned `T-FEAT-7.8.10` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.11 | §7.8–§7.10 | Feature extraction | Planned `T-FEAT-7.8.11` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.12 | §7.8–§7.10 | Feature extraction | Planned `T-FEAT-7.8.12` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.13 | §7.8–§7.10 | Feature extraction | Planned `T-FEAT-7.8.13` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.14 | §7.8–§7.10 | Feature extraction | Planned `T-FEAT-7.8.14` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.8.15 | §7.8–§7.10 | Feature extraction | Planned `T-FEAT-7.8.15` | Feature fixture has required schema, state handling, and lineage. |
| FR-7.9.1 | §9.1 | Pair scoring | Planned `T-MOD-7.9.1` | Candidate feature row produces a schema-compatible binary-model score. |
| FR-7.9.2 | §9.1 | Pair scoring | Planned `T-MOD-7.9.2` | Candidate feature row produces a schema-compatible binary-model score. |
| FR-7.9.3 | §9.1 | Pair scoring | Planned `T-MOD-7.9.3` | Candidate feature row produces a schema-compatible binary-model score. |
| FR-7.9.4 | §9.1 | Pair scoring | Planned `T-MOD-7.9.4` | Candidate feature row produces a schema-compatible binary-model score. |
| FR-7.9.5 | §9.1 | Pair scoring | Planned `T-MOD-7.9.5` | Candidate feature row produces a schema-compatible binary-model score. |
| FR-7.9.6 | §9.1 | Pair scoring | Planned `T-MOD-7.9.6` | Candidate feature row produces a schema-compatible binary-model score. |
| FR-7.9.7 | §9.1 | Pair scoring | Planned `T-MOD-7.9.7` | Candidate feature row produces a schema-compatible binary-model score. |
| FR-7.10.1 | §9.4; §11.6 | Match selection | Planned `T-DEC-7.10.1` | Threshold decision retains only eligible S2/S3 IDs with stated cardinality behavior. |
| FR-7.10.2 | §9.4; §11.6 | Match selection | Planned `T-DEC-7.10.2` | Threshold decision retains only eligible S2/S3 IDs with stated cardinality behavior. |
| FR-7.10.3 | §9.4; §11.6 | Match selection | Planned `T-DEC-7.10.3` | Threshold decision retains only eligible S2/S3 IDs with stated cardinality behavior. |
| FR-7.10.4 | §9.4; §11.6 | Match selection | Planned `T-DEC-7.10.4` | Threshold decision retains only eligible S2/S3 IDs with stated cardinality behavior. |
| FR-7.10.5 | §9.4; §11.6 | Match selection | Planned `T-DEC-7.10.5` | Threshold decision retains only eligible S2/S3 IDs with stated cardinality behavior. |
| FR-7.10.6 | §9.4; §11.6 | Match selection | Planned `T-DEC-7.10.6` | Threshold decision retains only eligible S2/S3 IDs with stated cardinality behavior. |
| FR-7.11.1 | §11.6 | Result assembly | Planned `T-RES-7.11.1` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.11.2 | §11.6 | Result assembly | Planned `T-RES-7.11.2` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.11.3 | §11.6 | Result assembly | Planned `T-RES-7.11.3` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.11.4 | §11.6 | Result assembly | Planned `T-RES-7.11.4` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.11.5 | §11.6 | Result assembly | Planned `T-RES-7.11.5` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.12.1 | §11.6 | Result assembly | Planned `T-RES-7.12.1` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.12.2 | §11.6 | Result assembly | Planned `T-RES-7.12.2` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.12.3 | §11.6 | Result assembly | Planned `T-RES-7.12.3` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.12.4 | §11.6 | Result assembly | Planned `T-RES-7.12.4` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.12.5 | §11.6 | Result assembly | Planned `T-RES-7.12.5` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.13.1 | §11.6 | Result assembly | Planned `T-RES-7.13.1` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.13.2 | §11.6 | Result assembly | Planned `T-RES-7.13.2` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.13.3 | §11.6 | Result assembly | Planned `T-RES-7.13.3` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.13.4 | §11.6 | Result assembly | Planned `T-RES-7.13.4` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.13.5 | §11.6 | Result assembly | Planned `T-RES-7.13.5` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.13.6 | §11.6 | Result assembly | Planned `T-RES-7.13.6` | Multi-match, singleton, duplicate, and candidate-match consistency fixture meets contract. |
| FR-7.14.1 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.14.1` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.14.2 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.14.2` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.14.3 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.14.3` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.14.4 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.14.4` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.14.5 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.14.5` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.14.6 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.14.6` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.14.7 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.14.7` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.14.8 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.14.8` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.15.1 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.15.1` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.15.2 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.15.2` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.15.3 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.15.3` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.15.4 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.15.4` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.15.5 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.15.5` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.15.6 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.15.6` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.15.7 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.15.7` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.15.8 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.15.8` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.15.9 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.15.9` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-7.15.10 | §11.6; §11.7 | Output and package validation | Planned `T-OUT-7.15.10` | Output/package fixture has required paths, headers, order, IDs, and validation result. |
| FR-11.1.1 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.1` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.2 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.2` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.3 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.3` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.4 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.4` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.5 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.5` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.6 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.6` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.7 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.7` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.8 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.8` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.9 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.9` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.10 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.10` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.11 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.11` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.12 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.12` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.13 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.13` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.1.14 | §8 | Training-data construction | Planned `T-TRAIN-DATA-11.1.14` | Persisted split/labels/sample metadata satisfy the stated leakage and retention rule. |
| FR-11.2.1 | §8; §12 | Leakage control | Planned `T-LEAK-11.2.1` | Audit shows validation/test labels do not influence training artifacts. |
| FR-11.2.2 | §8; §12 | Leakage control | Planned `T-LEAK-11.2.2` | Audit shows validation/test labels do not influence training artifacts. |
| FR-11.2.3 | §8; §12 | Leakage control | Planned `T-LEAK-11.2.3` | Audit shows validation/test labels do not influence training artifacts. |
| FR-11.2.4 | §8; §12 | Leakage control | Planned `T-LEAK-11.2.4` | Audit shows validation/test labels do not influence training artifacts. |
| FR-11.2.5 | §8; §12 | Leakage control | Planned `T-LEAK-11.2.5` | Audit shows validation/test labels do not influence training artifacts. |
| FR-11.2.6 | §8; §12 | Leakage control | Planned `T-LEAK-11.2.6` | Audit shows validation/test labels do not influence training artifacts. |
| FR-11.2.7 | §8; §12 | Leakage control | Planned `T-LEAK-11.2.7` | Audit shows validation/test labels do not influence training artifacts. |
| FR-11.3.1 | §9.1–§9.3 | Model training | Planned `T-TRAIN-11.3.1` | Model/manifest inspection satisfies family, probability, retraining, and version-binding rule. |
| FR-11.3.2 | §9.1–§9.3 | Model training | Planned `T-TRAIN-11.3.2` | Model/manifest inspection satisfies family, probability, retraining, and version-binding rule. |
| FR-11.3.3 | §9.1–§9.3 | Model training | Planned `T-TRAIN-11.3.3` | Model/manifest inspection satisfies family, probability, retraining, and version-binding rule. |
| FR-11.3.4 | §9.1–§9.3 | Model training | Planned `T-TRAIN-11.3.4` | Model/manifest inspection satisfies family, probability, retraining, and version-binding rule. |
| FR-11.3.5 | §9.1–§9.3 | Model training | Planned `T-TRAIN-11.3.5` | Model/manifest inspection satisfies family, probability, retraining, and version-binding rule. |
| FR-11.3.6 | §9.1–§9.3 | Model training | Planned `T-TRAIN-11.3.6` | Model/manifest inspection satisfies family, probability, retraining, and version-binding rule. |
| FR-11.3.7 | §9.1–§9.3 | Model training | Planned `T-TRAIN-11.3.7` | Model/manifest inspection satisfies family, probability, retraining, and version-binding rule. |
| FR-11.3.8 | §9.1–§9.3 | Model training | Planned `T-TRAIN-11.3.8` | Model/manifest inspection satisfies family, probability, retraining, and version-binding rule. |
| FR-11.3.9 | §9.1–§9.3 | Model training | Planned `T-TRAIN-11.3.9` | Model/manifest inspection satisfies family, probability, retraining, and version-binding rule. |
| FR-11.4.1 | §9.4; §12 | Threshold evaluation | Planned `T-THR-11.4.1` | Validation sweep record documents metric, selected threshold, and stability. |
| FR-11.4.2 | §9.4; §12 | Threshold evaluation | Planned `T-THR-11.4.2` | Validation sweep record documents metric, selected threshold, and stability. |
| FR-11.4.3 | §9.4; §12 | Threshold evaluation | Planned `T-THR-11.4.3` | Validation sweep record documents metric, selected threshold, and stability. |
| FR-11.4.4 | §9.4; §12 | Threshold evaluation | Planned `T-THR-11.4.4` | Validation sweep record documents metric, selected threshold, and stability. |
| FR-11.4.5 | §9.4; §12 | Threshold evaluation | Planned `T-THR-11.4.5` | Validation sweep record documents metric, selected threshold, and stability. |
| FR-11.4.6 | §9.4; §12 | Threshold evaluation | Planned `T-THR-11.4.6` | Validation sweep record documents metric, selected threshold, and stability. |
| FR-11.4.7 | §9.4; §12 | Threshold evaluation | Planned `T-THR-11.4.7` | Validation sweep record documents metric, selected threshold, and stability. |
| FR-11.4.8 | §9.4; §12 | Threshold evaluation | Planned `T-THR-11.4.8` | Validation sweep record documents metric, selected threshold, and stability. |
| FR-11.6.1 | §6.10; §12 | Candidate evaluation | Planned `T-CG-EVAL-11.6.1` | Candidate report contains required macro recall, miss, volume, and method contribution measure. |
| FR-11.6.2 | §6.10; §12 | Candidate evaluation | Planned `T-CG-EVAL-11.6.2` | Candidate report contains required macro recall, miss, volume, and method contribution measure. |
| FR-11.6.3 | §6.10; §12 | Candidate evaluation | Planned `T-CG-EVAL-11.6.3` | Candidate report contains required macro recall, miss, volume, and method contribution measure. |
| FR-11.6.4 | §6.10; §12 | Candidate evaluation | Planned `T-CG-EVAL-11.6.4` | Candidate report contains required macro recall, miss, volume, and method contribution measure. |
| FR-11.6.5 | §6.10; §12 | Candidate evaluation | Planned `T-CG-EVAL-11.6.5` | Candidate report contains required macro recall, miss, volume, and method contribution measure. |
| FR-11.6.6 | §6.10; §12 | Candidate evaluation | Planned `T-CG-EVAL-11.6.6` | Candidate report contains required macro recall, miss, volume, and method contribution measure. |
| FR-11.6.7 | §6.10; §12 | Candidate evaluation | Planned `T-CG-EVAL-11.6.7` | Candidate report contains required macro recall, miss, volume, and method contribution measure. |
| FR-12.1.1 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.1` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.2 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.2` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.3 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.3` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.4 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.4` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.5 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.5` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.6 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.6` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.7 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.7` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.8 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.8` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.9 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.9` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.10 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.10` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.11 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.11` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.12 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.12` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.13 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.13` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.1.14 | §3; §10.1–§10.5 | Batch architecture | Planned `T-ARCH-12.1.14` | Batch/index/artifact inspection shows configured deterministic disk-backed execution. |
| FR-12.2.1 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.1` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.2 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.2` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.3 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.3` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.4 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.4` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.5 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.5` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.6 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.6` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.7 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.7` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.8 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.8` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.9 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.9` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.10 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.10` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.11 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.11` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.12 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.12` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.13 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.13` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.14 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.14` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.15 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.15` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.16 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.16` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.17 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.17` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.18 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.18` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.19 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.19` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.20 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.20` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.2.21 | §11.1–§11.6 | Inference pipeline | Planned `T-INF-12.2.21` | Compatibility and batch-scoring fixture fails safely on mismatch and preserves pair/threshold association. |
| FR-12.4.1 | §10.5 | Checkpoint and recovery | Planned `T-REC-12.4.1` | Interrupted/corrupt batch recovery reuses only compatible artifacts without duplicates. |
| FR-12.4.2 | §10.5 | Checkpoint and recovery | Planned `T-REC-12.4.2` | Interrupted/corrupt batch recovery reuses only compatible artifacts without duplicates. |
| FR-12.4.3 | §10.5 | Checkpoint and recovery | Planned `T-REC-12.4.3` | Interrupted/corrupt batch recovery reuses only compatible artifacts without duplicates. |
| FR-12.4.4 | §10.5 | Checkpoint and recovery | Planned `T-REC-12.4.4` | Interrupted/corrupt batch recovery reuses only compatible artifacts without duplicates. |
| FR-13.4.1 | §10.6; §12; §13; §15 | Reproducibility | Planned `T-REPRO-13.4.1` | Experiment/model manifest contains required versions, seeds, dependencies, and artifact links. |
| FR-13.4.2 | §10.6; §12; §13; §15 | Reproducibility | Planned `T-REPRO-13.4.2` | Experiment/model manifest contains required versions, seeds, dependencies, and artifact links. |
| FR-13.4.3 | §10.6; §12; §13; §15 | Reproducibility | Planned `T-REPRO-13.4.3` | Experiment/model manifest contains required versions, seeds, dependencies, and artifact links. |
| FR-13.4.4 | §10.6; §12; §13; §15 | Reproducibility | Planned `T-REPRO-13.4.4` | Experiment/model manifest contains required versions, seeds, dependencies, and artifact links. |
| FR-13.4.5 | §10.6; §12; §13; §15 | Reproducibility | Planned `T-REPRO-13.4.5` | Experiment/model manifest contains required versions, seeds, dependencies, and artifact links. |
| FR-13.4.6 | §10.6; §12; §13; §15 | Reproducibility | Planned `T-REPRO-13.4.6` | Experiment/model manifest contains required versions, seeds, dependencies, and artifact links. |
| FR-13.4.7 | §10.6; §12; §13; §15 | Reproducibility | Planned `T-REPRO-13.4.7` | Experiment/model manifest contains required versions, seeds, dependencies, and artifact links. |
| FR-13.4.8 | §10.6; §12; §13; §15 | Reproducibility | Planned `T-REPRO-13.4.8` | Experiment/model manifest contains required versions, seeds, dependencies, and artifact links. |
| FR-13.4.9 | §10.6; §12; §13; §15 | Reproducibility | Planned `T-REPRO-13.4.9` | Experiment/model manifest contains required versions, seeds, dependencies, and artifact links. |
| FR-13.4.10 | §10.6; §12; §13; §15 | Reproducibility | Planned `T-REPRO-13.4.10` | Experiment/model manifest contains required versions, seeds, dependencies, and artifact links. |
| FR-15.1.1 | §12; §18 | Experiment management | Planned `T-EXP-15.1.1` | Experiment/error-analysis record has required objective, baseline, metrics, and categorized errors. |
| FR-15.1.2 | §12; §18 | Experiment management | Planned `T-EXP-15.1.2` | Experiment/error-analysis record has required objective, baseline, metrics, and categorized errors. |
| FR-15.1.3 | §12; §18 | Experiment management | Planned `T-EXP-15.1.3` | Experiment/error-analysis record has required objective, baseline, metrics, and categorized errors. |
| FR-15.1.4 | §12; §18 | Experiment management | Planned `T-EXP-15.1.4` | Experiment/error-analysis record has required objective, baseline, metrics, and categorized errors. |
| FR-15.1.5 | §12; §18 | Experiment management | Planned `T-EXP-15.1.5` | Experiment/error-analysis record has required objective, baseline, metrics, and categorized errors. |
| FR-15.1.6 | §12; §18 | Experiment management | Planned `T-EXP-15.1.6` | Experiment/error-analysis record has required objective, baseline, metrics, and categorized errors. |
| FR-15.1.7 | §12; §18 | Experiment management | Planned `T-EXP-15.1.7` | Experiment/error-analysis record has required objective, baseline, metrics, and categorized errors. |
| FR-15.1.8 | §12; §18 | Experiment management | Planned `T-EXP-15.1.8` | Experiment/error-analysis record has required objective, baseline, metrics, and categorized errors. |

## Non-FR Challenge Constraints

The following are authoritative narrative constraints, not FR IDs; they are intentionally separate from the 213-row functional mapping.

| Constraint | TDD location | Planned verification / observable criterion |
|---|---|---|
| No external business lookup, API, geocoding, or enrichment | §15 | Code/package review finds no prohibited external data lookup dependency or call. |
| MIT/Apache 2.0 model license and up-to-8B parameter constraint | §6.7; §15 | Selected embedding/model manifest records license and parameter evidence before packaging. |
| Final package includes outputs, runnable source, README, dependency declaration, and methodology template | §11.7; §13; §18 | Package completeness manifest lists every official required path before archive creation. |
| UTF-8 multilingual input/output handling | §4; §5; §11.6 | UTF-8 fixture parses and output validation preserves required text/format behavior. |

## Validation Notes

- Extracted SRS FR definitions: **213**.
- RTM rows: **213**, one row per extracted ID.
- No ranges, inferred FR IDs, or status claims of completed testing are used.
- A future audit can compare the first column directly with SRS requirement-definition IDs and inspect each named planned artifact/pass criterion.

