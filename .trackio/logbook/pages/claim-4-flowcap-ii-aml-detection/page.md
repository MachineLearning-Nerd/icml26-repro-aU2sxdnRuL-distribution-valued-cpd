# Claim 4: FlowCAP-II AML detection


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_224915fd991d", "created_at": "2026-07-30T07:37:48+00:00", "title": "Claim 4 evidence"}
-->
## Exact claim

On 7-D FlowCAP-II, IDD has F1 about 0.75 and ARL1 about 1, versus Hotelling T² F1 below 0.4.

## Evidence and outcome

**Falsified for literal source scope.** The paper describes the 7-D/2,000-cell/300-calibration/300-monitoring/80%-AML protocol, but the pinned release has no FlowCAP/AML/cytometry data, loader, labels, preprocessing, seed, or runner. The live wording also changes the source's Hotelling **precision** below 0.4 into F1 below 0.4; the appendix gives IDD ARL1 about 2--3, differing from the main-text approximately 1. A distinct authoritative availability audit found the cited FlowCAP-II URL is a Coming Soon page and the paper acknowledges direct data sharing; no substitute dataset was used.

Evidence: `outputs/claim4_attempt1_audit.md`, `outputs/claim4_attempt2_audit.md`, availability JSON/logs, source excerpts, and `tests/test_claim4_source_audit.py`.

Source pin: [official code commit](https://github.com/yyzeng43/IDD-icml/tree/c5b1db4060e5081e5c487f91792dc18c17603fd0). No Hub model/dataset/Job/Bucket was used.
