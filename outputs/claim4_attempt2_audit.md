# Claim 4 — Attempt 2: authoritative public-data availability audit

## Scope

This attempt searched only authoritative public sources for the exact FlowCAP-II AML files and protocol required by the live claim. It does **not** substitute another cytometry dataset or synthetic stream for the paper-scale result.

## Sources and retained evidence

- Paper source: `https://export.arxiv.org/e-print/2602.07252`
- Pinned author release: `https://github.com/yyzeng43/IDD-icml@c5b1db4060e5081e5c487f91792dc18c17603fd0`
- FlowCAP-II official URL checked: `https://flowcap.org/flowcap2/`
- Retained official-page response: `evidence/claim4_attempt2/flowcap2_official.html`
- Retrieval headers: `evidence/claim4_attempt2/official_endpoint_headers.txt`
- Search transcript: `evidence/claim4_attempt2/search_transcript.txt`
- Machine-readable audit: `outputs/claim4_attempt2_public_availability.json`
- Hash manifest: `outputs/claim4_attempt2_SHA256SUMS.txt`

## Protocol that is specified

The paper supplies aggregate experiment details: 7 dimensions, 2,000 cells per measurement, 316 healthy donors and 43 AML patients, 300 healthy calibration samples, a 300-sample monitoring stream, and 80% AML-positive injection. It does not supply the per-measurement files/labels, preprocessing, stream seed/order, or executable runner.

Critically, the paper acknowledgement states that Dr. Ryan Brinkman shared the FlowCAP-II data **directly** with the authors. The retrieved official FlowCAP-II URL is a `Coming Soon` page, and the pinned author release contains no FlowCAP/AML/cytometry/FCS data, loader, or runner.

## Outcome

**Inconclusive for a source-faithful CPU re-evaluation.** Exact public files, labels, preprocessing, and stream construction are unavailable, so the reported F1/ARL metrics cannot be recomputed honestly. This availability finding is not itself a dataset-level refutation. The literal wording/source discrepancies found in Attempt 1 remain separately recorded.

## Validation

```bash
python3 src/claim4_attempt2_public_availability.py
.venv-claim1-attempt2/bin/pytest -q tests/test_claim4_attempt2_public_availability.py
```

The focused test passed (`1 passed`).

## Next action

Claim 4 has had two distinct attempts. Preserve this audit and move to the next controller-selected claim rather than inventing a substitute dataset.
