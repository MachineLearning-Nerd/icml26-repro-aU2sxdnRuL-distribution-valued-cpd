# Claim 4 route 1: primary archive probe

On Hugging Face CPU compute, fetch the official FlowRepository record with an explicit User-Agent, hash it, parse all four-digit FCS names and the `aml` experiment-variable block, then request bytes 0–65,535 from the official archive endpoint. A nonexistent experiment ID is the negative control and must return 404 or 410.

Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`

Estimated compute: 2 cores. Selected flavor: Hugging Face `cpu-upgrade`; no GPU. Actual allocation and runtime are emitted in `raw/probe.json` and the run log.
