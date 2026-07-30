# Claim 5: Reddit event alignment


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_b490a00aa3e7", "created_at": "2026-07-30T07:37:49+00:00", "title": "Claim 5 evidence"}
-->
## Exact claim

On Reddit vaccine-sentiment d=20 streams, alarms align with events such as the April 13 J&J pause while baseline summaries show unrelated drift/noise.

## Evidence and outcome

**Falsified for the literal April-13 alignment wording.** Attempt 1 checksum-matched the public Dataverse input but found no paper-era 20-D embeddings, dated alarm series, baseline outputs, or working runner. Attempt 2 audited release history and packaging with the same result. The independent third route recovered the authoritative arXiv source archive and Figure-4 asset: it specifies 384-D MiniLM embeddings/PCA-20 and reports an **April 30 post-gap reorganization** after an April 3--28 sparse-data gap. April 13 occurs inside that gap, so this is not a direct observed April-13 alarm. Numeric streams were not replaced with a proxy.

Evidence: `outputs/claim5_attempt{1,2,3}_audit.md`, `evidence/claim5_attempt3/arxiv_source.tar`, Figure-4 PDF, hashes, `src/claim5_attempt3_arxiv_archive_audit.py`, and `tests/test_claim5_attempt3.py` (1 passed).

Source pin: [official code commit](https://github.com/yyzeng43/IDD-icml/tree/c5b1db4060e5081e5c487f91792dc18c17603fd0). No Hub model/dataset/Job/Bucket was used.
