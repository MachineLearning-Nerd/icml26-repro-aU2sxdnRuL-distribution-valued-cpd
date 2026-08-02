# Claim 2 — FALSIFIED

## Exact claim and quantifier

The live Claim 2 reads Theorem 3.10 as a sequential guarantee `ARL0 >= n0 + 1 + 1/(alpha_T2 + alpha_SPE)` under empirical-quantile calibration. At `n0=200` and both alphas `.01`, the literal lower bound is `251`. The source's finite-sample empirical-quantile corollary instead adds `2/(n0+1)` in the denominator, yielding `234.3887`.

## Direct result

Across 4,000 deterministic null streams of independent chi-square(1) T²/SPE pairs, horizon 5,000, the calibrated monitoring run length is `40.4` and global ARL proxy is `241.4`. Thus `241.4 < 251`, contradicting the literal claim, while `241.4 > 234.3887`, consistent with the corrected result. No run censored at the horizon.

The half-threshold negative control increases false alarms and falls to `207.556`. Tests independently check empirical order-statistic selection, first-crossing semantics, and no-alarm censoring. The verifier exits nonzero unless the literal inequality is contradicted and the corrected inequality retained.

## Reproduce and inspect

- Code: [`claim2_attempt1_empirical_arl.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/src/claim2_attempt1_empirical_arl.py)
- Checker: [`test_claim2_attempt1.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/tests/test_claim2_attempt1.py)
- [Raw 4,000-replication JSON](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/resolve/main/outputs/claim2_attempt1_empirical_arl.json)

Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`. Seed `20260730`; baseline cumulative commit `11fc4b67a00b32d8066816983628bf2a7092d66d`; run `762e490b-9c2d-4394-be5b-a28e1355cd96`; HF `cpu-upgrade` provider allocation 8 vCPU, affinity diagnostic 64; GPU false; cumulative runtime 37 s.

Limitation: this falsifies the literal live formula, not the corrected finite-sample corollary.
