# Current verification — five resolved, one blocked

This is the canonical evaluator entrypoint for the candidate superseding judged revision `881cb4f9cda9250f4bb1394b7cee539825ac6ac7`. Current verification appears first; the unchanged judged pages remain reachable under **Historical rejected baseline**.

Previous live judged score: **7/12**. Conservative forecast: **7–10/12**. Best-supported possible score: **10/12**, not a judge result.

| Claim | Current verdict | Canonical page |
|---|---|---|
| 1 | VERIFIED | [paper-scale tangent-space mechanism](#/current-claim-1) |
| 2 | FALSIFIED | [literal empirical-quantile ARL bound](#/current-claim-2) |
| 3 | FALSIFIED | [95% synthetic-delay statement](#/current-claim-3) |
| 4 | FALSIFIED | [FlowCAP ARL1 approximately one](#/current-claim-4) |
| 5 | BLOCKED | [Reddit event alignment](#/current-claim-5) |
| 6 | VERIFIED | [epsilon-isometry scaling](#/current-claim-6) |

[Read the full release report](#/current-release-report), including the evaluator-blind review. The downloadable [blind-review record](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/resolve/main/release/evaluator_blind_review.md) lists every file opened and every conclusion that remained unverifiable.

## Evaluator-visible visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | current-claim-1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | VERIFIED |
| 2 | current-claim-2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | FALSIFIED |
| 3 | current-claim-3 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | FALSIFIED |
| 4 | current-claim-4 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | FALSIFIED |
| 5 | current-claim-5 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | BLOCKED |
| 6 | current-claim-6 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | VERIFIED |

## Fixed contract

Command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`

Environment: Python 3.12, one repository `.venv`, [`pyproject.toml`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/pyproject.toml), and [`uv.lock`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/uv.lock). All scientific work used Hugging Face `cpu-upgrade` (provider allocation 8 vCPU/32 GB; process affinity diagnostic 64 logical CPUs); GPU requested: false.
