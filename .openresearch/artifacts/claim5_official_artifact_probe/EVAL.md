# Evaluator note

Run exactly:

```text
uv sync --frozen && uv run --frozen python scripts/run_campaign.py
```

The run prints `CLAIM5_OFFICIAL_ARTIFACT_PROBE` and the fail-closed verifier output. The generated `raw/result.json` contains all numerical and schema evidence. This is an additional verification route, not a full-credit result.
