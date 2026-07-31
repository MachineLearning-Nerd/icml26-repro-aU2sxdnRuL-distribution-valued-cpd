# Claim 1: tangent-space IDD mapping


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_c68f92cb01d3", "created_at": "2026-07-30T07:37:47+00:00", "title": "Claim 1 evidence"}
-->
## Exact claim

The IDD method maps distributions to the pre-change Fréchet-barycenter tangent space using the stated radial isometry and applies Hotelling T²/SPE.

## Evidence and outcome

**Inconclusive; toy evidence retained.** Three distinct reduced-scale CPU audits verify the 1-D translation/scale/non-affine empirical-quantile transport identity and reject identity-map, wrong-reference, and uncentered-map controls. The pinned empirical OT path also passed at reduced scale, but the source-faithful paper-scale R/funcharts mFPCA route is unavailable. A one-time atomic non-Monge counterexample shows the equality is not unconditional, but violates the intended regularity conditions and therefore is not a refutation.

Commands and raw evidence: `outputs/claim1_attempt{1,2,3}_*.{md,json,log}` and `outputs/claim1_falsification_*`; tests include `tests/test_claim1_attempt*.py` and `tests/test_claim1_falsification.py` (7 tests passed in the retained suite).

Source pin: [yyzeng43/IDD-icml@c5b1db4](https://github.com/yyzeng43/IDD-icml/tree/c5b1db4060e5081e5c487f91792dc18c17603fd0). No Hub model/dataset/Job/Bucket was used.
