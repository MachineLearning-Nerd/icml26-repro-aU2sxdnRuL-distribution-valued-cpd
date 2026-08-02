# Claim 3 — FALSIFIED

## Exact claim and scope

Table 1 states that on high-variance (`sigma=2`) Gaussian-translation streams, IDD achieves up to a 95% delay reduction against the best-tuned displayed Log-KDE baseline at matched ARL0. The contract parses every pinned table row and computes `(best_LogKDE − IDD)/best_LogKDE`; it does not select a favorable bandwidth after seeing the answer.

## Direct result

All 18 table rows and all six high-variance rows were parsed. The maximum high-variance reduction is `72.5%`, at `d=5, sigma=2, delta=.5`: IDD `1.1`, best displayed Log-KDE `4.0`. No high-variance row reaches 95%. The low-variance tied-delay control has IDD and Log-KDE both equal to `1.0`, confirming the parser returns zero—not a spurious large percentage—when delays tie.

The released high-variance generator also produced ten deterministic `d=5, sigma=2, delta=.1` replicas (seeds 7052–7061; 200 Phase-I, 200 IC, 200 OC distributions; 100 points). These generated inputs are supporting protocol evidence, not a claimed Table-1 rerun because released R/funcharts execution remains unavailable.

## Reproduce and inspect

- Code: [`claim3_attempt1_source_audit.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/src/claim3_attempt1_source_audit.py)
- Checker/control: [`test_claim3_attempt1.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/tests/test_claim3_attempt1.py)
- [Raw complete-row JSON](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/resolve/main/outputs/claim3_attempt1/result.json)

Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`. Seeds 7052–7061; baseline cumulative commit `11fc4b67a00b32d8066816983628bf2a7092d66d`; run `762e490b-9c2d-4394-be5b-a28e1355cd96`; HF `cpu-upgrade` provider allocation 8 vCPU, affinity diagnostic 64; GPU false; cumulative runtime 37 s.

Limitation: the falsification is the paper's literal table-backed 95% maximum, not an independent matched-ARL rerun.
