# Claim 1 method

The experiment creates 600 five-dimensional empirical distributions with 300 observations each. Every distribution is a positive diagonal affine pushforward of one common N(0,I5) reference grid. The 300 Phase-I affine coefficients have exactly zero sample mean, so their compatible Wasserstein barycenter is the reference. The last 150 Phase-II distributions receive a predeclared scale and translation change.

Displacement fields are flattened with quadrature weight 1/300. The implementation follows the paper equations directly: Phase-I mean centering, SVD of the empirical covariance, the smallest K explaining 95% variance, score-space T2, and orthogonal residual SPE. Thresholds are Phase-I empirical 0.99 quantiles.

An independent checker uses the 300-by-300 sample Gram matrix and `eigh`, rather than the primary feature-space SVD. Six selected empirical transports are solved from their full cost matrices with the Hungarian algorithm. Identity-map, wrong-reference indexed-plan, and uncentered-MFPCA controls must each be rejected.

Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`

Estimated compute: 8 cores. Selected compute: Hugging Face `cpu-upgrade`, CPU only. Actual allocation and runtime are emitted into `raw/result.json` and the OpenResearch run log.
