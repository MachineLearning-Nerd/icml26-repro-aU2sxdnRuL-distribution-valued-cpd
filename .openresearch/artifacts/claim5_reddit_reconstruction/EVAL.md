# Evaluator entry

Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`.

Current route verifier: `src/verify_claim5_reddit_reconstruction.py`. It fails closed on protocol, independent-checker, control, or empty-alarm failures. Exact parity is required for a VERIFIED verdict; a mechanically valid but divergent reconstruction remains BLOCKED rather than being overclaimed as a falsification. This is the mandatory fourth Claim-5 route dedicated to seeking a counterexample under the pinned released split semantics.
