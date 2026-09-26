# Multilingual Retrieval Baseline Comparison

Date: 2026-09-26  
Status: implementation smoke check; not a full-scale quality benchmark.

## Configuration

The baseline preserves the six existing retrieval families. The updated pipeline adds the optional `multilingual_name` family, backed by the configured `intfloat/multilingual-e5-small` candidate and disabled by default until model availability, license, supported-script coverage, and resource use are validated. The model package is not installed in this environment (`ModuleNotFoundError: sentence_transformers`), so no model download or semantic retrieval claim was made.

## Results

| Measurement | Baseline | Updated code path | Evidence type |
|---|---:|---:|---|
| Unit tests | 14 passed before extension | 15 passed after extension | Local test suite |
| Existing retrieval methods | 6 | 6 retained | Code inspection/test |
| Added method | None | `multilingual_name`, disabled | Code inspection/test |
| Added provenance feature | None | `multilingual_name_hit` | Schema/test |
| Cross-script candidate recall | Not measured | Not measured | No semantic model installed / no full trace |
| Macro-F0.5 | Existing smoke artifacts only | Not run | No retraining |
| Full-scale runtime/memory | Not measured | Not measured | No full-scale run |

The disabled updated path returns no multilingual candidates and therefore preserves baseline candidate behavior. Index/model/checkpoint hashes now include the multilingual configuration, preventing incompatible artifact reuse when the method is enabled or its model/device/limits change.

## Remaining benchmark steps

1. Install and license-review the selected compact multilingual model in an isolated environment.
2. Run a labeled sample containing Latin-to-non-Latin positives, same-script controls, S2/S3 rows, and address-missing cases.
3. Compare candidate recall, incremental discoveries, overlap, candidate volume, encoding/index/query throughput, peak memory, classifier metrics, and macro-F0.5 using the same entity-level split.
4. Enable the method for full-scale execution only if the resource and quality gates in `docs/MULTILINGUAL_ARCHITECTURE_ADDENDUM.md` pass.
