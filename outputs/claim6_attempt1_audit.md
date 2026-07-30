# Claim 6 — Attempt 1 theorem audit

## Exact live claim

> Theorem 3.14 establishes an epsilon-isometry result showing the number of principal components needed for a finite-dimensional tangent-space approximation scales polynomially with the target precision under Lipschitz regularity.

## Pinned source evidence

`paper_source/main0.tex` (SHA-256 in `outputs/claim6_attempt1/SHA256SUMS`) states the epsilon-isometry theorem at lines 788–798. It assumes the covariance-kernel conditions of Proposition `prop:kernel_lipschitz`, then gives:

```tex
sum_{m > K} lambda_m <= A_X C_K K^{-1/d}
K >= (A_X C_K / (epsilon^2 tr(Gamma)))^d
```

The regularity chain is stated at lines 763–781: i.i.d. distributions on a bounded convex domain; bounded, alpha-Holder densities; and uniform Lipschitz/bounded tangent fields. The covariance-kernel proposition then supplies the required Lipschitz condition.

## CPU check and control

`src/claim6_attempt1_theorem_audit.py` parses the theorem and required assumptions from the pinned TeX and checks the displayed finite-K algebra for dimensions 1, 2, and 5 over three epsilon-halving pairs. All nine checks recover the required epsilon^(-2d) scaling exactly.

The negative control drops the exponent `d`. For epsilon 0.2 to 0.1, the actual K ratio is 16 for d=2 and 1024 for d=5, while the invalid dimension-free prediction is 4 in each case. The control is rejected in both dimensions.

## Verdict

**Verified, scoped.** For fixed dimension and the source's stated regularity/trace conditions, the printed K lower bound is polynomial in target precision. This is a theorem/source audit, not an empirical proof. The live wording should not be read as dimension-free: the polynomial degree is `2d` and the source requires more than Lipschitz regularity alone.

## Artifacts

- `src/claim6_attempt1_theorem_audit.py`
- `tests/test_claim6_attempt1.py`
- `outputs/claim6_attempt1/result.json`
- `outputs/claim6_attempt1/run.log`
- `outputs/claim6_attempt1/test.log`
- `outputs/claim6_attempt1/SHA256SUMS`
