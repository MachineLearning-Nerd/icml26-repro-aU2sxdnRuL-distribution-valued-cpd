# Claim 3: synthetic delay reduction


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_6bfedd1375dc", "created_at": "2026-07-30T07:37:48+00:00", "title": "Claim 3 evidence"}
-->
## Exact claim

On high-variance Gaussian-translation streams, IDD achieves up to a 95% delay reduction over the best-tuned Log-KDE at matched ARL0.

## Evidence and outcome

**Falsified for literal source-table scope.** The source-faithful generator completed the full `d=5, sigma=2, delta=0.1` input family (10 deterministic replicates, 200 Phase-I/200 IC/200 OC distributions, 100 particles). The unavailable `Rscript`/funcharts mFPCA dependency prevented the full Table-1 rerun, so the generated inputs are not represented as table reproduction. Parsing all pinned Table-1 rows found the largest high-variance reduction against the best displayed Log-KDE is **72.5%** (`1.1` vs `4.0`), not 95%; no row reaches 95% against the best baseline. The matched-ARL raw threshold outputs are also unreleased.

Evidence: `outputs/claim3_attempt1_audit.md`, `outputs/claim3_attempt1/`, `src/claim3_attempt1_source_audit.py`, and `tests/test_claim3_attempt1.py`.

Source pin: [official code commit](https://github.com/yyzeng43/IDD-icml/tree/c5b1db4060e5081e5c487f91792dc18c17603fd0). No Hub model/dataset/Job/Bucket was used.
