# Evaluator-blind pre-publication review

## Protocol

The reviewer received only the evaluator rubric and a fresh candidate assembled from the exact judged Space revision `881cb4f9cda9250f4bb1394b7cee539825ac6ac7` plus the committed text allowlist. The review began at `README.md` and `logbook.json`; no internal repository knowledge, experiment dashboard, unpublished branch, or artifact hint was supplied.

## Pass 1 — frozen cumulative candidate

- Git SHA: `f3fc756da134726aea33629efc8be76a3f2afc7a`
- HF CPU run: `079fcf9f-d445-4cc9-b2dd-6b3cce77a782`
- Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`
- Result: `24 passed`; `RELEASE_CANDIDATE_AUDIT` verdict `PASS`
- Candidate: 161 files, 142 text upload paths, all 21 judged files preserved as a subset, secret scan PASS
- Candidate tree SHA-256: `9b332c64dc71b5ddeb41d6b10fcaf2c70359d3ccd2e1dcc3b9bb560ccea69094`

Files opened from canonical navigation, in order:

1. `pages/current-index/page.md`
2. `pages/current-claim-1/page.md`
3. `pages/current-claim-2/page.md`
4. `pages/current-claim-3/page.md`
5. `pages/current-claim-4/page.md`
6. `pages/current-claim-5/page.md`
7. `pages/current-claim-6/page.md`
8. `pages/current-release-report/page.md`
9. `pages/historical-rejected-baseline/page.md`
10. `pages/executive-summary/page.md`
11. `pages/claim-1-tangent-space-idd-mapping/page.md`
12. `pages/claim-2-empirical-quantile-arl/page.md`
13. `pages/claim-3-synthetic-delay-reduction/page.md`
14. `pages/claim-4-flowcap-ii-aml-detection/page.md`
15. `pages/claim-5-reddit-event-alignment/page.md`
16. `pages/claim-6-finite-dimensional-epsilon-isometry/page.md`
17. `pages/conclusion/page.md`

## Claim conclusions from the visible artifact

| Claim | Current verifier found | Exact contract and assumptions | Code/raw/checker/control found | Reviewer conclusion |
|---|---|---|---|---|
| 1 | yes | yes | yes | VERIFIED |
| 2 | yes | yes | yes | FALSIFIED |
| 3 | yes | yes | yes | FALSIFIED |
| 4 | yes | yes | yes | FALSIFIED, with stated figure-only limitation |
| 5 | yes | yes | yes | BLOCKED; exact 50+50 stream remains unavailable |
| 6 | yes | yes | yes | VERIFIED |

No visibility cell was missing. The only scientific conclusion the reviewer could not establish was Claim 5's exact event-alignment claim; the current page correctly exposes that as `BLOCKED`, shows all required routes, and states the external data/configuration needed to unblock it.

## Mandatory repeat after review changes

This record and its canonical links are the only review-driven additions. Publication remains blocked unless the child experiment reruns the same fixed command on HF `cpu-upgrade`, again emits `RELEASE_CANDIDATE_AUDIT` with verdict `PASS`, preserves the judged subset, and exits zero. The final publication candidate will record that second run before upload.
