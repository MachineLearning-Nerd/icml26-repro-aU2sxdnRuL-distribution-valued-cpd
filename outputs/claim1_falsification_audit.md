# Claim 1 — one falsification attempt: scope of the radial-isometry wording

## Question tested

The live claim states the radial identity

```text
W2²(mu_bar, mu) = ||T_{mu_bar}^{mu} - Id||²_{L2(mu_bar)}
```

and says the method uses it to construct tangent vectors and T²/SPE monitoring. This falsification attempt tests whether that equality is valid without the conditions needed for a deterministic optimal (Monge) map, and whether the pinned empirical implementation can violate it when it returns a barycentric projection instead.

## Source-aligned construction

Use the atomic source and split target

```text
mu_bar = delta_0
mu     = 0.5 delta_-1 + 0.5 delta_1.
```

There is no deterministic map from the one-point support of `mu_bar` whose pushforward is the two-point target. The unique feasible optimal coupling has mass `0.5` from `0` to each target point, hence

```text
W2²(mu_bar, mu) = 0.5 * 1² + 0.5 * 1² = 1.
```

The pinned source's `barycentric_projection_map` (`upstream/IDD-icml/gaussian_translation/ot_mfpca.py`, lines 334–378) computes an OT coupling and returns

```python
Txs = (Pi @ X_tgt) / Pi.sum(axis=1, keepdims=True)
```

(lines 373–378). For the coupling `[0.5, 0.5]`, that projection is `T(0)=0`; consequently `||T-Id||²_L2(delta_0)=0`.

## Executed result

The test imports the pinned source function with the isolated CPU environment and uses its EMD route.

| Quantity | Result |
|---|---:|
| Pinned-source barycentric projection | `[0.0]` |
| Source tangent norm squared | `0.0` |
| Optimal-coupling W2² | `1.0` |
| Equality gap | `1.0` |

Command:

```bash
.venv-claim1-attempt2/bin/python src/claim1_falsification.py
.venv-claim1-attempt2/bin/python -m pytest -q tests/test_contract.py tests/test_claim1_attempt1.py tests/test_claim1_attempt2.py tests/test_claim1_attempt3.py tests/test_claim1_falsification.py
```

The retained test suite reports `7 passed`.

## Conclusion and claim disposition

This is a valid counterexample to an **unqualified** reading of the radial-isometry sentence and demonstrates that the empirical barycentric projection in the pinned code is not always a Monge map with equality of the stated norm and `W2²`.

It is **not** a refutation of the intended Equation 6/Proposition 3.4 result: the construction deliberately violates the regularity/Monge-map conditions under which a Wasserstein tangent-space logarithmic map is defined. The paper's intended continuous empirical setting may satisfy those conditions. Therefore the full Claim 1 remains **inconclusive**, with the three previously retained small-scale mechanism audits explicitly labeled **toy**. No 2-point falsification verdict is claimed.

## Evidence

- `src/claim1_falsification.py` — source-aligned construction.
- `tests/test_claim1_falsification.py` — exact output assertions.
- `outputs/claim1_falsification_scope.json` — raw results.
- `outputs/claim1_falsification_run.log` and `outputs/claim1_falsification_test.log` — execution logs.
- `outputs/claim1_falsification_SHA256SUMS.txt` — hashes of source, test, raw output, and pinned upstream file.
