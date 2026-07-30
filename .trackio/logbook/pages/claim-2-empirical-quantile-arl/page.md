# Claim 2: empirical-quantile ARL


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_49090d38f409", "created_at": "2026-07-30T07:37:47+00:00", "title": "Claim 2 evidence"}
-->
## Exact claim

Theorem 3.10 gives `ARL0 >= n0 + 1 + 1/(alpha_T2 + alpha_SPE)` via empirical quantile calibration.

## Evidence and outcome

**Falsified as literally written.** The pinned theorem gives the displayed fixed-threshold result under its marginal-exceedance assumptions. The source's empirical-quantile finite-sample corollary instead has denominator `alpha_T2 + alpha_SPE + 2/(n0+1)`. A deterministic CPU null-stream audit (4,000 seeded replications, `n0=200`) produced a calibrated global-ARL proxy 241.4: below the literal 251 bound but above the corrected 234.39 bound; the half-threshold control fell to 207.56.

Evidence: `outputs/claim2_attempt1_audit.md`, `outputs/claim2_attempt1_empirical_arl.json`, logs/hashes, `src/claim2_attempt1_empirical_arl.py`, and `tests/test_claim2_attempt1.py`. This does not challenge the corrected theorem.

Source pin: [official code commit](https://github.com/yyzeng43/IDD-icml/tree/c5b1db4060e5081e5c487f91792dc18c17603fd0). No Hub model/dataset/Job/Bucket was used.
