# Claim 5 — BLOCKED

## Exact claim and required domain

On daily Reddit vaccine-comment distributions from January–May 2021, represented by 20-D reductions of MiniLM embeddings, IDD's alarms align with news shocks including the 13 April J&J pause, while Euclidean/moment baselines show unrelated monotonic drift or noise. The appendix requires 50 Phase-I days (2 Dec–30 Jan), 50 Phase-II days (31 Jan–5 May), and removal of days below 30 comments.

## Seven different routes

1. Public Dataverse/source audit: checksums match, but no paper-era 20-D stream or alarm series exists.
2. Camera-ready minimum-30 reconstruction: available all-records data yields only 38+48 eligible days.
3. Released minimum-20 runner interpretation: protocol differs from the appendix.
4. Split-semantics falsification search: neither reasonable cutoff interpretation yields the exact contract.
5. Exact author cleaning/non-root route: gives 50+49, not 50+50.
6. Official comments-only representations: archival TSV and saved-original CSV independently give the same 11,168 valid rows and 38+48 minimum-30 days.
7. Mandatory falsification/full-mechanics route: executes pinned SBERT, PCA-20, 500-epoch cited CNF, 512-sample barycenter, Sinkhorn maps, MFPCA, Hotelling, checkers, and controls on the closest 50+49 stream.

## Direct numerical evidence

The full closest-stream route embeds 10,735 comments. The CNF loss moves from `22.4716` to `−15.2862`; trained conditional-mean spread is `.02542`, while label erasure is zero. Sinkhorn row/column marginal maximum errors are `3.90e-18` and `1.41e-6`; independent T²/SPE errors are `4.83e-13` and `5.88e-16`.

Observed IDD SPE alarms: `49/49`; IDD T² alarms: `0`; Hotelling alarms: `12`; paper alarms: `5`; exact alarm Jaccard: `.1020`. All five paper dates appear only because every retained Phase-II date alarms. The prespecified three response dates all match, but a 5,000-permutation date-shuffle control has null mean `3.0` and one-sided `p=1.0`.

This does not support event specificity, but it is not a valid exact-stream counterexample. Missing input is not falsification.

## Reproduce and inspect

- Full code: [`claim5_reddit_reconstruction.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/src/claim5_reddit_reconstruction.py)
- Full fail-closed verifier: [`verify_claim5_reddit_reconstruction.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/src/verify_claim5_reddit_reconstruction.py)
- [Full-route raw JSON](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/resolve/main/.openresearch/artifacts/claim5_reddit_reconstruction/raw/result.json)
- Official probe code: [`claim5_official_artifact_probe.py`](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/blob/main/src/claim5_official_artifact_probe.py)
- [Official-representation raw JSON](https://huggingface.co/spaces/DineshAI/repro-aU2sxdnRuL-distribution-valued-cpd/resolve/main/.openresearch/artifacts/claim5_official_artifact_probe/raw/result.json)

Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`. Seed `260207252`; full commit `67be2044cd2346927d9bb678a3942d0209f9357b`; run `018d6794-7bbc-4f96-8a06-e9e61b38d4fd`; estimated 32 useful cores, trained with four intra-op threads; HF `cpu-upgrade` provider allocation 8 vCPU, affinity diagnostic 64; GPU false; 1,047.052 s campaign runtime. Official probe commit `2bdcccfa8cf61664669935df4d7526915cc36b3a`, run `fe1558b8-7421-45c5-82d7-51e485f7df7f`, estimated 2 cores, same provider/diagnostic allocation, 72.096 s campaign runtime.

Unblock requirement: publish the exact paper-era 50+50 dated comment/embedding stream and private IDD/baseline configuration. Confidence remains LOW; all required three verification routes plus the mandatory falsification route—and additional routes—are complete.
