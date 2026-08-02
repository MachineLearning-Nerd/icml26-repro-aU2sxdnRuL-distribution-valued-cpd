# Evaluator entry

Run the fixed campaign command:

```text
uv sync --frozen && uv run --frozen python scripts/run_campaign.py
```

Current verifier: `src/verify_claim4_figure_falsification.py`. It exits nonzero if coordinate extraction, the independent checker, the negative control, or the predeclared falsification condition fails. Raw outputs are `raw/result.json` and `raw/digitized_points.csv` after the HF cpu-upgrade run.

This supersedes source-only textual discrepancy notes for the ARL1 numerical clause. It does not supersede the preserved acquisition attempts or claim that the raw-data pipeline was rerun.
