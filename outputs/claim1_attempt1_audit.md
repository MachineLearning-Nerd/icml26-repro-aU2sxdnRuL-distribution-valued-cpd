# Claim 1 — Attempt 1 source audit and CPU toy result

## Scope and verdict

This is a deterministic **toy** mechanism audit, not a paper-scale reproduction of Claim 1. It verifies the radial tangent-map identity in an exactly solvable one-dimensional equal-variance Gaussian translation and demonstrates finite rank-1 T²/SPE calculations on small tangent vectors. It does not establish Proposition 3.4 at the paper's full empirical/general scope.

## Pinned upstream audit

Pinned source: `yyzeng43/IDD-icml@c5b1db4060e5081e5c487f91792dc18c17603fd0`.

Relevant source path: `upstream/IDD-icml/gaussian_translation/ot_mfpca.py`.

- `barycenter_estimation` pools Phase-I clouds and calls POT `ot.lp.free_support_barycenter` with uniform within-cloud and barycenter weights.
- `barycentric_projection_map` constructs squared Euclidean cost, computes an EMD or Sinkhorn coupling, and returns the source-support barycentric projection `Pi @ X_tgt / Pi.sum(axis=1)`.
- `process_phaseI` and `process_phaseII` form tangent vectors as `T(x)-x` and save their mean squared norms.
- The Gaussian generator uses seeded `N(m, sigma^2 I)` phase-I clouds and `N(m+delta, sigma^2 I)` phase-II clouds.
- The full upstream pipeline delegates mFPCA to R. The current CPU environment has NumPy but lacks POT, pytest, R, and `funcharts`; an attempted package installation failed because this workspace venv has no `pip` (`outputs/pip_install.log`). Therefore the unmodified upstream OT/mFPCA pipeline was not executed in Attempt 1.

## Independent deterministic check

For `mu_bar=N(0,1)`, `mu=N(delta,1)`, the radial optimal map is exactly `T(x)=x+delta`. With `delta=0.75`, the toy check computes

```text
mean((T(x)-x)^2) = 0.5625 = W2^2(mu_bar, mu)
```

with absolute error `0.0`. The negative control replaces `T` with the identity map, giving tangent norm `0.0`, separated from the correct value by `0.5625`.

A deterministic two-dimensional tangent-vector PCA monitor gives finite rank-1 `T²=177.4332755488297` and `SPE=0.2976867114700875`. This supports only the operational tangent-to-monitoring mechanism.

## Evidence

- `src/claim1_attempt1.py` — independent deterministic computation, seed `20260730`.
- `tests/test_claim1_attempt1.py` — invariant and negative-control assertions.
- `outputs/claim1_attempt1_toy.json` — raw metrics.
- `outputs/claim1_attempt1_test.log` — manual test execution.
- `outputs/claim1_attempt1_SHA256SUMS.txt` — hashes of source, test, raw outputs, and audited upstream file.

## Next action

Attempt 2 must create an isolated CPU environment with POT and, if feasible, R/funcharts, then run the pinned upstream empirical-OT path on a small seeded Gaussian stream and independently compare the computed map/norm invariants. The full claim remains unverified.
