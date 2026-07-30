# Claim 1 — Attempt 3: independent empirical-quantile audit

## Scope and verdict

**Verdict: toy.** This is a genuinely independent clean-room numerical route. It does not import POT or the upstream implementation and uses the exact one-dimensional equal-weight empirical quantile representation. It supports the radial-isometry mechanism and a transparent PCA/T²/SPE monitor, but it is not full verification of the literal claim: it does not run the paper-scale distribution-valued stream, released R/`funcharts` mFPCA stage, or the full Proposition 3.4 conditions.

## Independent derivation

For equally weighted one-dimensional empirical measures with sorted supports
`q_bar=(q_bar,i)` and `q=(q_i)`, the monotone optimal transport map pairs equal quantile ranks:

```text
T(q_bar,i) = q_i
W2²(mu_bar, mu) = (1/n) sum_i (q_i - q_bar,i)²
||T - Id||²_L2(mu_bar) = (1/n) sum_i (T(q_bar,i) - q_bar,i)²
```

Thus both quantities are identical by direct substitution. The clean-room Phase-I barycenter is the pointwise mean of four sorted Phase-I empirical quantile vectors, which is the 1-D equal-weight barycenter representation used for this finite audit.

## Multi-family result

The deterministic construction contains 12 support points and four Phase-I clouds. It tests a translation, a scale change, and a non-affine shape deformation rather than repeating the prior Gaussian-only or upstream-POT routes.

| Family | radial tangent mean square | quantile W2² | absolute difference |
|---|---:|---:|---:|
| translation | 0.42250000000000004 | 0.42250000000000004 | 0.0 |
| scale | 0.0965300625 | 0.0965300625 | 0.0 |
| non-affine shape | 0.014136992315666674 | 0.014136992315666674 | 0.0 |

The independent rank-1 flattened-tangent PCA diagnostic for the non-affine target gives `T²=0.0415739755979643`, `SPE=0.16746543146666668`, and leading eigenvalue `0.0524`.

## Negative controls

All controls are deterministic and retained in the raw JSON.

| Control | Result | Why it rejects the altered convention |
|---|---:|---|
| identity map | tangent norm 0 for every non-identical family | misses the positive W2² values (smallest gap 0.014136992315666674) |
| wrong reference/barycenter (`mu_bar + 0.3`) | W2² 0.09605279231566666 instead of 0.014136992315666674 | gap 0.08191579999999998 |
| omit `-Id` centering and use raw mapped positions | second moment 0.4936327289823333 | gap 0.4794957366666666 from the correct W2² |

These controls reject map/reference/centering substitutions, but do not establish the full paper protocol.

## Pinned-source comparison

Pinned source: `yyzeng43/IDD-icml@c5b1db4060e5081e5c487f91792dc18c17603fd0`, `gaussian_translation/ot_mfpca.py`.

- `barycenter_estimation` at line 270 pools Phase-I clouds and calls a free-support Wasserstein barycenter.
- `barycentric_projection_map` at line 334 computes a coupling and returns `Pi @ X_tgt / Pi.sum(axis=1)`, i.e. a map from source/barycenter support to target support.
- `process_phaseI` at line 383 and `process_phaseII` at line 432 form tangents as `Txs - Xb` and record their mean squared norms.

That source direction and centering match the clean-room formula above. The upstream Python code supplies tangent vectors; its monitor pipeline still delegates the mFPCA stage to unavailable R/`funcharts`, so this attempt cannot claim full source-pipeline verification.

## Evidence and commands

```bash
.venv-claim1-attempt2/bin/python src/claim1_attempt3_quantile_audit.py
.venv-claim1-attempt2/bin/python -m pytest -q tests/test_contract.py tests/test_claim1_attempt2.py tests/test_claim1_attempt3.py
```

- Implementation: `src/claim1_attempt3_quantile_audit.py`
- Test: `tests/test_claim1_attempt3.py`
- Raw output: `outputs/claim1_attempt3_quantile_audit.json`
- Run log: `outputs/claim1_attempt3_run.log`
- Test log: `outputs/claim1_attempt3_test.log` (`4 passed`)
- Source/output hashes: `outputs/claim1_attempt3_SHA256SUMS.txt`

## Next action

All three reproduction routes are now complete and each remains toy-scale. Proceed to the single Claim 1 falsification attempt: test whether the full literal source claim can be contradicted by an exact map-direction/reference/centering counterexample or a released-protocol inconsistency. Do not relabel these three toy mechanisms as full verification.
