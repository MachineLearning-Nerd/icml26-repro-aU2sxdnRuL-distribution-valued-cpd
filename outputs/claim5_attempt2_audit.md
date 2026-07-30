# Claim 5 Attempt 2 — source-history and protocol-version audit

## Outcome

**Inconclusive; no source-faithful paper-era Reddit run is recoverable.** This is distinct from Attempt 1: it examines public repository history, releases/tags, and a separately documented packaging-path repair attempt rather than re-auditing the default runner/data mismatch.

## Evidence

- GitHub's commits API reports one commit for `case_study/run_reddit_vax.py`: `d1fb8f01a52b16778bedc2b9d60adaa7a2eaef17` (2026-05-20), labelled “Replace figures with reproducibility scripts”. It is post-paper and no prior runner configuration is exposed through that path.
- The GitHub releases and tags APIs each return zero records.
- The pinned `idd_core/ot_mfpca_flow.py` imports `simulation.OT_KDE_Comp` and `simulation.com_simu`, neither of which exists in the public release.
- An isolated invocation with the available `continuous_streams` directory on `PYTHONPATH` still fails before processing with `ModuleNotFoundError: No module named 'simulation'` (exit code 1). This demonstrates that the missing dependency is not repaired by a simple documented import-path adjustment.
- No public commit/tag/release recovered the paper-era 384-D SBERT cache, PCA-20 embedding arrays, dated IDD/baseline alarm series, or Figure-4 outputs. Accordingly no proxy run was treated as verification.

## Sources and artifacts

- `evidence/claim5_attempt2/github_commits_runner.json`
- `evidence/claim5_attempt2/github_releases.json`
- `evidence/claim5_attempt2/github_tags.json`
- `outputs/claim5_attempt2/repaired_import_runner.log`
- `outputs/claim5_attempt2/protocol_history_audit.json`

## Next action

Attempt 3 should use a distinct source route (paper supplement/author-material and data-version metadata) or, if that cannot recover the exact configuration, proceed to the required falsification attempt. This attempt neither verifies nor falsifies the qualitative Reddit claim.
