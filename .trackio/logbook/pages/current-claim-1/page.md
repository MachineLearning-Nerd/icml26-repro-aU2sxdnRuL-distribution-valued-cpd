# Claim 1 — VERIFIED

## Exact claim and assumptions

Equation 6 and Proposition 3.4 map each streaming empirical distribution to the tangent space at the pre-change Fréchet barycenter using `W2²(mu_bar, mu) = ||T(mu_bar→mu) − Id||²_L2(mu_bar)`, then apply MFPCA, Hotelling T², and SPE. The audit uses an absolutely continuous `N(0,I_5)` reference and positive diagonal affine gradients of convex quadratics, so deterministic Monge maps exist and finite second moments hold.

## Direct result

The paper-scale audit uses 300 Phase-I plus 300 Phase-II distributions in `d=5`, with 300 points per distribution. Six independently assigned distributions have maximum radial-isometry error `6.94e-18`. Nine components explain `0.9620` variance. Independent Gram/SVD checks have maximum errors: eigenvalues `1.04e-17`, SPE `2.46e-16`, T² `1.35e-13`. The changed-half alarm rate is `0.9933` for either statistic.

Independent checker and negative controls: the separate Gram/SVD checker agrees through the errors above. The identity map misses true W2² by `0.03712`; an indexed wrong-reference plan is suboptimal by `5.9856`; omitting Hotelling scaling changes T² by `80.7605`.

## Reproduce and inspect

- Code: [`claim1_paper_scale.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/src/claim1_paper_scale.py)
- Fail-closed verifier: [`verify_claim1_paper_scale.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/src/verify_claim1_paper_scale.py)
- [Raw result JSON](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/resolve/main/.openresearch/artifacts/claim1_paper_scale/raw/result.json)
- Contract, method, source audit, and limitations are in [the evidence directory](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/tree/main/.openresearch/artifacts/claim1_paper_scale).

Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`. Seed `260207252`; scientific commit `e96eec21e70eac70bbf63b909e8e3859688ce8a4`; run `5c29b642-79de-43d2-ac18-6a1637bb9053`; estimated 8 cores; HF `cpu-upgrade` provider allocation 8 vCPU, process affinity diagnostic 64; GPU false; total run 79 s.

Limitation: this verifies the complete multivariate mechanism and equations on controlled distributions, not the paper's performance tables or unavailable R/funcharts byte parity.
