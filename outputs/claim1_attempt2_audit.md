# Claim 1 — Attempt 2: pinned empirical-OT CPU path

## Scope and verdict

**Verdict: toy.** This attempt exercised the pinned upstream empirical barycenter and EMD barycentric-projection path on a deterministic 1-D Gaussian-translation stream. It does not establish the full live claim because it uses three Phase-I clouds, two Phase-II clouds, and four points per cloud; the released R/`funcharts` mFPCA step was unavailable because `Rscript` is not installed.

## Pinned implementation

- Upstream repository: `yyzeng43/IDD-icml@c5b1db4060e5081e5c487f91792dc18c17603fd0`
- Exercised source: `upstream/IDD-icml/gaussian_translation/ot_mfpca.py`
- Isolated environment: `.venv-claim1-attempt2` created with `uv`, Python 3.12.
- Packages: recorded in `claim1_attempt2_environment.txt`; includes NumPy, SciPy, POT, CPU PyTorch, and pytest.

## Executed evidence

`src/claim1_attempt2_empirical.py` calls the upstream `barycenter_estimation`, `barycentric_projection_map`, `process_phaseI`, and `process_phaseII` functions. The source selects EMD for this 1-D/4-point case.

| Check | Result |
|---|---:|
| Direct EMD translation-map maximum absolute error | `8.88e-16` |
| Direct radial norm | `0.3600000000` |
| Expected translation norm (`0.6²`) | `0.36` |
| Upstream Phase-II translated-stream tangent norm | `0.35999999999999893` |
| Independent NumPy PCA/T² score for translated stream | `35.99999999999996` |
| Identity-map negative-control norm | `0.0` |
| Negative control rejected expected translation norm | pass |

The transparent NumPy PCA/T²/SPE diagnostic is retained only as an independent check; it does not substitute for the missing upstream R/`funcharts` mFPCA result.

## Commands and artifacts

```bash
uv venv --python 3.12 .venv-claim1-attempt2
uv pip install --python .venv-claim1-attempt2/bin/python 'numpy<3' 'scipy<2' POT torch pytest
.venv-claim1-attempt2/bin/python src/claim1_attempt2_empirical.py
.venv-claim1-attempt2/bin/python -m pytest -q tests/test_contract.py tests/test_claim1_attempt2.py
```

- Raw result: `claim1_attempt2_empirical.json`
- Run transcript: `claim1_attempt2_run.log`
- Test transcript: `claim1_attempt2_test.log` (`3 passed`)
- Environment versions and R availability: `claim1_attempt2_environment.txt`
- Checksums: `claim1_attempt2_SHA256SUMS.txt`

## Next action

Claim 1 Attempt 3 should use a distinct source-faithful route: install/run the released R `funcharts` stage in an isolated CPU environment if possible, or independently reproduce the same empirical-OT stream through a separate OT implementation while preserving the paper metric.
