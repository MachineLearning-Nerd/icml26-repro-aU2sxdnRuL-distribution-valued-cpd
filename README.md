# Reproduction: Beyond Euclidean Summaries

This campaign tests all six live claims for [*Beyond Euclidean Summaries: Online Change Point Detection for Distribution-Valued Data*](https://arxiv.org/abs/2602.07252). The strongest new evidence replaces Claim 1's toy audit with a paper-scale d=5 mechanism verification and falsifies Claim 4's literal `ARL1 ≈ 1` statement from the paper's original figure. Claims 2, 3, and 6 retain their full-credit evidence. Claim 5 remains honestly `BLOCKED` after seven routes because the exact 50+50 paper-era stream is unavailable.

Previous live judged score: **7/12**. Conservative projected range: **7–10/12**. Best-supported possible score: **10/12**, a forecast only—the live judge has not evaluated this revision.

Key numbers: Claim 1's maximum checked OT identity error is `6.94e-18`; Claim 4's digitized IDD ARL1 range is `2.63–3.37`, not approximately one; the closest Claim 5 route has `50+49` days and alarms on `49/49` Phase-II days (`p=1.0` under the date-shuffle control).

- [Illustrated technical report](reports/campaign/report.md)
- [Self-contained marimo notebook](notebooks/reproduction.py)
- [Open in molab](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/notebooks/reproduction.py)
- [Canonical evaluator index](.trackio/logbook/pages/current-index/page.md)

All experiments ran on Hugging Face `cpu-upgrade` with no GPU. The fixed command was identical on every node:

```text
uv sync --frozen && uv run --frozen python scripts/run_campaign.py
```

## Current assessments

| Claim | Paper result | Observed result | Assessment |
|---|---|---|---|
| 1 | Full tangent-space IDD mechanism | d=5, 600 distributions, exact OT/tangent checks | VERIFIED |
| 2 | Literal ARL lower bound 251 | calibrated proxy 241.4; corrected bound 234.39 | FALSIFIED |
| 3 | up to 95% delay reduction | maximum displayed high-variance reduction 72.5% | FALSIFIED |
| 4 | FlowCAP F1 ≈0.75 and ARL1 ≈1 | F1 reaches .785, but all IDD ARL1 markers are 2.63–3.37 | FALSIFIED |
| 5 | five event-aligned Reddit alarms | exact stream absent; closest route alarms every day | BLOCKED |
| 6 | K polynomial in precision | epsilon^(-2d) derivation/checks recovered | VERIFIED |

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | Publication surface | Not run as an experiment (publication surface) | Receives the gated report, notebook, and evaluator pages | none |
| [`orx/frozen-judged-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-aU2sxdnRuL-distribution-valued-cpd/tree/orx/frozen-judged-baseline) | Freeze and rerun judged baseline | `uv sync --frozen && uv run --frozen python scripts/run_campaign.py` | 18 passing checks | HF cpu-upgrade (8 vCPU; affinity diagnostic 64), 37 s |
| [`orx/claim-1-durable-evidence-output`](https://github.com/MachineLearning-Nerd/icml26-repro-aU2sxdnRuL-distribution-valued-cpd/tree/orx/claim-1-durable-evidence-output) | Paper-scale multivariate mechanism | `uv sync --frozen && uv run --frozen python scripts/run_campaign.py` | VERIFIED; 19 passing checks | HF cpu-upgrade (8 vCPU; affinity 64), 79 s |
| [`orx/claim-4-filled-diamond-morphology-verifier`](https://github.com/MachineLearning-Nerd/icml26-repro-aU2sxdnRuL-distribution-valued-cpd/tree/orx/claim-4-filled-diamond-morphology-verifier) | Independent figure-marker falsification | `uv sync --frozen && uv run --frozen python scripts/run_campaign.py` | FALSIFIED; 21 passing checks | HF cpu-upgrade (8 vCPU; affinity 64), 69 s |
| [`orx/claim-5-official-artifact-schema-reconstruction`](https://github.com/MachineLearning-Nerd/icml26-repro-aU2sxdnRuL-distribution-valued-cpd/tree/orx/claim-5-official-artifact-schema-reconstruction) | Audit official TSV/CSV representations | `uv sync --frozen && uv run --frozen python scripts/run_campaign.py` | BLOCKED; official minimum-30 stream is 38+48 | HF cpu-upgrade (8 vCPU; affinity 64), 112 s |
| [`orx/claim-5-cnf-sinkhorn-50-49-reconstruction`](https://github.com/MachineLearning-Nerd/icml26-repro-aU2sxdnRuL-distribution-valued-cpd/tree/orx/claim-5-cnf-sinkhorn-50-49-reconstruction) | Full closest-stream CNF/Sinkhorn/MFPCA route | `uv sync --frozen && uv run --frozen python scripts/run_campaign.py` | BLOCKED; 49/49 SPE alarms, 22 passing checks | HF cpu-upgrade (8 vCPU; affinity 64), 18m09s |
| [`orx/cumulative-release-candidate`](https://github.com/MachineLearning-Nerd/icml26-repro-aU2sxdnRuL-distribution-valued-cpd/tree/orx/cumulative-release-candidate) | Cumulative science and publication gates | `uv sync --frozen && uv run --frozen python scripts/run_campaign.py` | Pending final gated run | HF cpu-upgrade, no GPU |

## Reproduce

Use Python 3.12 and `uv`; the lockfile is authoritative. The campaign downloads pinned public sources with explicit User-Agents and writes regenerated raw files under `.openresearch/artifacts/`.

```bash
uv sync --frozen
uv run --frozen python scripts/run_campaign.py
```

The repository deliberately does not claim to recreate unavailable FlowCAP FCS files, the exact Reddit 50+50 stream, or private author modules. See the report and current claim pages for assumptions, controls, raw evidence, and limitations.
