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

## Pass 2 — repeat after review changes

- Git SHA: `9c6a7b7e28d1eb71f9604a8716baa7c81960b4fb`
- HF CPU run: `cbd2b56e-466b-40a8-82e8-cc0d3b00e3a0`
- Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`
- Result: `24 passed`; campaign runtime `866.714 s`; `RELEASE_CANDIDATE_AUDIT` verdict `PASS`
- Candidate: 162 files, 143 text upload paths, all 21 judged files preserved as a subset, secret scan PASS
- Candidate tree SHA-256: `52786756316286d4d9ce94ddb8d7307ac3f0061ddf1dc3ab7cd3aa7a37866da8`

Pass 2 repeated the same 17-file canonical traversal after this review record and its links were added. It found no missing visibility cell and no new unverifiable conclusion. Claim 5 remained correctly `BLOCKED`; all other current verdicts remained unchanged. Publication is still gated on the final child rerunning the same full command and artifact audit with zero exit.
