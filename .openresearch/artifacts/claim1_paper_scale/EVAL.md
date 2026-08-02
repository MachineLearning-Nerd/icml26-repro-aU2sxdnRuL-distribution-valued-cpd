# Evaluator entry: current Claim 1 verifier

Status is not accepted until the Hugging Face run completes and the fail-closed verifier exits zero. The current executable is `src/verify_claim1_paper_scale.py`; `src/claim1_paper_scale.py` regenerates all raw files. Historical Claim 1 pages are preserved but are superseded by this multivariate paper-scale route if it passes.

Raw outputs are written to `raw/affine_parameters.csv`, `raw/statistics.csv`, and `raw/result.json`. The run prints their SHA-256 hashes. Limitations are embedded in the JSON and must remain visible in the candidate logbook.
