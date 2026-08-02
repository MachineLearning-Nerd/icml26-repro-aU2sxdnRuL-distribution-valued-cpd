# Claim 4 — FALSIFIED

## Exact claim and predeclared contract

The live claim states: on 7-D FlowCAP-II, IDD has F1 approximately `.75` and ARL1 approximately `1`, versus Hotelling T² F1 below `.4`. Before inspecting pixel coordinates, the falsification contract generously defined “approximately 1” as at most `1.5`. The paper's original `tradeoff_F1_vs_ARL0_singlecol.png` is calibrated from its printed F1-linear and ARL1-logarithmic grid lines.

## Direct result

Six filled IDD diamond markers have ARL1 values `2.6314, 2.8383, 2.8383, 3.3742, 3.3742, 3.3742`; every point exceeds `2` and the `1.5` contract bound. IDD F1 reaches `.7849`; Hotelling's maximum digitized F1 is `.3734`.

Independent checker and negative control: a separate column-density checker finds four uncollapsed vertical positions, all above `2` (`2.6314, 3.1966, 3.5233, 3.6003`). Filled-patch areas and range endpoints agree. The negative control deliberately reads the explicitly logarithmic ARL1 axis as linear, gives impossible negative delays, and is rejected.

## Reproduce and inspect

- Code: [`claim4_figure_falsification.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/src/claim4_figure_falsification.py)
- Fail-closed verifier: [`verify_claim4_figure_falsification.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/src/verify_claim4_figure_falsification.py)
- [Raw digitization JSON](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/resolve/main/.openresearch/artifacts/claim4_figure_falsification/raw/result.json)
- Paper archive SHA-256 `6d4af865d403a1c4f72ed3ef8057069212ac1633aa79410b4607b04a8b9edb87`; figure SHA-256 `e788172329eb5886009265a37733a037a158efecf7e85089a790cc8bd1af363a`; anchors `main0.tex:986, 998–1000, 1751, 1798–1810`.

Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`. Scientific commit `85e1638f63bd040cc409b1ceb96c8af550a682d8`; run `d6b62e85-3b6d-4271-b6f3-ffd6d1276413`; estimated 2 cores; HF `cpu-upgrade` provider allocation 8 vCPU, affinity diagnostic 64; GPU false; run 69 s.

Limitation: this directly falsifies the literal figure-backed ARL1 statement. It is not a FlowCAP FCS rerun; those files and a public runner remain unavailable.
