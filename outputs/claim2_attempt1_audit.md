# Claim 2 — Attempt 1: source and finite-sample ARL audit

## Exact live claim

> Theorem 3.10 gives a sequential false-alarm-control guarantee of the form
> `ARL_0 >= n_0 + 1 + 1/(alpha_T2 + alpha_SPE)` via empirical quantile
> calibration (Section 3, Theorem 3.10).

## Source-faithful audit

Pinned paper source: `paper_source/main0.tex`, extracted from arXiv
`2602.07252` (hash in `claim2_attempt1_SHA256SUMS.txt`).

- Lines 607–613 state the theorem: **with fixed thresholds** and i.i.d.
  monitoring statistics, `ARL_0 = n0 + 1 + 1/p_infty`, and the displayed
  `1/(alpha_T2 + alpha_SPE)` lower bound additionally requires each marginal
  exceedance probability to be bounded by its corresponding alpha.
- Lines 618–630 (commented earlier formulation) make the required independent
  Phase-II monitoring and union-bound assumptions explicit.
- Lines 599 and 728–729 specify empirical `(1-alpha)` Phase-I quantiles for
  the two separate charts. The codebase’s `continuous_streams/common_mfpca.py`
  lines 67–79 defines the run length as the first strict exceedance, one-based,
  and returns `H+1` if no alarm occurs.
- Crucially, lines 656–660 give the paper's empirical-quantile finite-sample
  corollary: each marginal exceedance may be `alpha + 1/(n0+1)`, yielding
  `ARL_0 >= n0 + 1 + 1/(alpha_T2 + alpha_SPE + 2/(n0+1))`.

Thus the theorem's fixed-threshold result and the empirical-quantile result are
not identical at finite `n0`. The live claim joins them without the required
finite-sample correction.

## CPU experiment

`src/claim2_attempt1_empirical_arl.py` uses independent chi-square(1) null
T2/SPE pairs to isolate the stated calibration/run-length logic from the
unavailable full OT/mFPCA stack. For each of 4,000 deterministic seeded
replications it:

1. draws a Phase-I calibration sample of size `n0=200`;
2. uses the stated `k=ceil((1-alpha)n0)` empirical order statistic for each
   chart (`alpha_T2=alpha_SPE=0.01`);
3. monitors independent Phase-II null pairs for 5,000 times and stores the
   first strict union-chart alarm time; and
4. separately repeats with intentionally halved thresholds as a negative
   control.

| Quantity | Value |
|---|---:|
| Literal live bound | 251.0000 |
| Source finite-sample bound | 234.3887 |
| Ordinary calibrated global-ARL proxy | 241.4000 |
| Half-threshold negative-control global-ARL proxy | 207.5560 |

Raw first alarm times and all parameters are in
`outputs/claim2_attempt1_empirical_arl.json`. The normal calibration proxy is
below the literal 251 bound but above the source finite-sample bound; the
miscalibrated control is lower still. This is a finite CPU statistical audit,
not a full distribution-valued IDD experiment.

## Outcome

**Falsified as literally written.** The source's Theorem 3.10 requires fixed
thresholds with marginal exceedance guarantees. With empirical quantiles, the
source itself states the weaker finite-sample denominator including
`2/(n0+1)`. This attempt does not challenge the corrected theorem/corollary
under their stated assumptions.

## Commands

```bash
.venv-claim1-attempt2/bin/python src/claim2_attempt1_empirical_arl.py
PYTHONPATH=. .venv-claim1-attempt2/bin/python -m pytest -q \
  tests/test_claim2_attempt1.py tests/test_contract.py
```
