# Claim 5 Attempt 3 — authoritative arXiv archive provenance audit

## Outcome

**Inconclusive.** This is a source-asset provenance result, not an independent reproduction of the unavailable numeric Reddit stream.

## Distinct route

Attempts 1–2 audited the Dataverse input, public release, runner/history, tags, and dependency path. This attempt instead retrieved the authoritative arXiv source archive (`https://arxiv.org/e-print/2602.07252`) and recovered its embedded Figure-4 PDF asset plus manuscript source.

- Archive: `evidence/claim5_attempt3/arxiv_source.tar`
- Figure asset: `evidence/claim5_attempt3/reddit_figure4_source.pdf`
- Hashes: `evidence/claim5_attempt3/SHA256SUMS`
- Structured audit: `outputs/claim5_attempt3/arxiv_archive_audit.json`

## Recovered protocol and result evidence

The source explicitly documents the `all-MiniLM-L6-v2` 384-dimensional embedding step, PCA to `d=20`, Phase I from Dec 2, 2020 to Jan 30, 2021, and Phase II from Jan 31 to May 5, 2021. It also embeds the Reddit monitoring figure referenced by the manuscript.

However, the camera-ready source says that the relevant post-pause SPE alarm is **Apr 30**, after an **Apr 3–28 sparse-data gap**, with Apr 13 and Apr 23 occurring in that gap. Thus the recovered source documents post-gap reorganization rather than a same-day observation. The broader live wording permits post-pause alignment, so this provenance evidence does not falsify it.

The source asset does not contain the exact 20-D daily embedding array, numeric dated alarm series, or baseline result arrays. Those remain unrecovered, so this result does not claim a fresh full-scale rerun.

## Reproduction

```bash
python3 src/claim5_attempt3_arxiv_archive_audit.py
.venv-claim1-attempt2/bin/python -m pytest -q tests/test_claim5_attempt3.py
```

Result: `1 passed`.

## Next action

Claim 5 remains inconclusive because the released artifacts lack the numeric streams needed for a source-faithful rerun. Do not use a synthetic replacement as a full reproduction. Advance to Claim 6 Attempt 1.
