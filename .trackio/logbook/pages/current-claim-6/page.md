# Claim 6 — VERIFIED

## Exact claim, theorem, and assumptions

Theorem 3.14 states `sum_(m>K) lambda_m <= A_X C_K K^(-1/d)` and consequently `K >= (A_X C_K/(epsilon² tr(Gamma)))^d` for relative mean-square reconstruction error at most `epsilon²`. The source chain requires a bounded convex domain, Hölder densities and OT regularity, uniformly Lipschitz and bounded tangent fields, a Lipschitz covariance kernel, and positive trace.

## Direct result

An independently reconstructed algebra checker evaluates dimensions 1, 2, and 5 over epsilon halvings `.4→.2`, `.2→.1`, and `.1→.05`. All nine ratios exactly match epsilon^(-2d): `4`, `16`, and `1024`, respectively. The dimension-free negative control drops exponent `d`, predicts `4` for dimensions 2 and 5, and is rejected against actual `16` and `1024`.

Because this is a theorem claim, the verdict rests on the pinned symbolic derivation plus executable exact algebra checks, not finite experiments alone.

## Reproduce and inspect

- Code/checker: [`claim6_attempt1_theorem_audit.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/src/claim6_attempt1_theorem_audit.py)
- Fail-closed test: [`test_claim6_attempt1.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/tests/test_claim6_attempt1.py)
- [Raw theorem and nine checks](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/resolve/main/outputs/claim6_attempt1/result.json)
- Source `paper_source/main0.tex`, SHA-256 `7c88af0f1ccb66458f0b396331bdee3b5aed26c1b041730e891900f38a5591f6`.

Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`. Baseline cumulative commit `11fc4b67a00b32d8066816983628bf2a7092d66d`; run `762e490b-9c2d-4394-be5b-a28e1355cd96`; HF `cpu-upgrade` provider allocation 8 vCPU, affinity diagnostic 64; GPU false; cumulative runtime 37 s.

Limitation: the polynomial degree is `2d`; the result is not dimension-free.
