# Release report

- Previous live judged score: `7/12`
- Conservative projected score range after the proposed change: `7–10/12`
- Best-supported possible new score: `10/12` — forecast only, not a judge result

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 1 | 2 | HIGH | VERIFIED | Full d=5 mechanism, exact OT identities, independent statistics, three rejecting controls; risk is evaluator interpretation of “full pipeline” versus performance tables. |
| 2 | 2 | 2 | HIGH | FALSIFIED | 4,000 null streams contradict literal 251 while satisfying corrected 234.39; retained unchanged and rerun cumulatively. |
| 3 | 2 | 2 | HIGH | FALSIFIED | Exhaustive pinned-table parsing gives maximum 72.5%, with tied-delay control; retained unchanged and rerun cumulatively. |
| 4 | 0 | 2 | MEDIUM | FALSIFIED | Two quantitative methods place every original-figure IDD ARL1 point above 2.6; risk is lack of raw FlowCAP rerun and ambiguity in “approximately.” |
| 5 | 0 | 0 | LOW | BLOCKED | Seven routes include official representations and full closest-stream mechanics, but exact 50+50 input/private configurations remain absent. |
| 6 | 2 | 2 | HIGH | VERIFIED | Pinned symbolic derivation plus nine exact algebra checks and dimension-free negative control; retained unchanged and rerun cumulatively. |

Current live total remains `7/12`. The conservative projected total is `7–10/12`; the best-supported possible total is `10/12`. Only the live judge can change it.

## Evaluator-visible visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | current-claim-1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | VERIFIED |
| 2 | current-claim-2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | FALSIFIED |
| 3 | current-claim-3 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | FALSIFIED |
| 4 | current-claim-4 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | FALSIFIED |
| 5 | current-claim-5 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | BLOCKED |
| 6 | current-claim-6 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | VERIFIED |

## What changed

Claim 1 changes from toy evidence to a full paper-scale multivariate mechanism audit. Claim 4 changes from inconclusive to a literal-source falsification using the paper's original figure and two independent marker methods. Claim 5 remains blocked, but now has the complete mandatory route sequence plus additional official-data and full-mechanics evidence. Claims 2, 3, and 6 retain and rerun their accepted evidence.

## Remaining blocker

Claim 5 is the only blocked claim. Three materially different verification routes and the mandatory fourth falsification route were completed before further routes: public/source reconstruction, alternate paper/release window semantics, source-archive/figure audit, and exact-assumption counterexample search. Additional exact author-cleaning, official comments-only, and full CNF/Sinkhorn routes did not produce the unavailable 50+50 stream. Unblocking requires the paper-era dated embedding/comment stream and private IDD/baseline configuration.

## Reproduction contract and compute

Exact command on every node: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`.

Environment: Python 3.12, one repository `.venv`, `pyproject.toml`, `uv.lock`, author commit `c5b1db4060e5081e5c487f91792dc18c17603fd0`. Selected hardware: Hugging Face `cpu-upgrade`, provider specification 8 vCPU/32 GB; the process affinity diagnostic reported 64 logical CPUs. No GPU was requested or used.

Through the accepted cumulative candidate, 30 HF runs used 12,210 seconds (3 h 23 m 30 s) of listed wall time. At the official `cpu-upgrade` price of `$0.0005/min` (`$0.03/h`), the duration-based estimate is `$0.1018`; the blind-review child will be added before publication. Billing is provider-metered by minute, so this is an evidence-based estimate rather than an invoice.

## Evaluator-blind review

The first review started only from the fresh candidate's `README.md` and `logbook.json`, then opened the 17 navigation files listed in the [downloadable review record](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/resolve/main/release/evaluator_blind_review.md). It found the current verifier, exact contract, code, inline numbers, raw evidence, checker, control, and limitation for every claim. No visibility cell was missing. Claim 5's exact scientific conclusion remained unverifiable and is therefore exposed as `BLOCKED`, not PASS. Publication is gated on a second clean HF traversal after these review additions.

## Evidence paths

- Claim 1: `.openresearch/artifacts/claim1_paper_scale/`
- Claim 2: `outputs/claim2_attempt1_empirical_arl.json`, source and test under `src/` and `tests/`
- Claim 3: `outputs/claim3_attempt1/result.json`, source and test under `src/` and `tests/`
- Claim 4: `.openresearch/artifacts/claim4_figure_falsification/`
- Claim 5: `.openresearch/artifacts/claim5_reddit_reconstruction/` and `.openresearch/artifacts/claim5_official_artifact_probe/`
- Claim 6: `outputs/claim6_attempt1/result.json`, source and test under `src/` and `tests/`
- Illustrated report: `reports/campaign/report.md`; notebook: `notebooks/reproduction.py`

## Publication action

After all remaining gates pass, upload the exact text allowlist to the existing Space `DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd` through the Hugging Face text API, verify the published revision and hashes from a fresh download, mark the paper awaiting judge, then mirror the exact published text paths to GitHub `main` and confirm with `git ls-remote`. No second Space will be created.
