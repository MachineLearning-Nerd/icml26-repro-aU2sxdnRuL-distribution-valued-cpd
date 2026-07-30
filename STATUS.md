# Status

- OpenReview ID: aU2sxdnRuL
- Submission number: 30280
- Live claim count / maximum points: 6 / 12
- Selection timestamp: 2026-07-30T06:51:28Z
- Contract manifest: contract/contract_manifest.json
- Paper: https://arxiv.org/abs/2602.07252
- Official code pin: https://github.com/yyzeng43/IDD-icml@c5b1db4060e5081e5c487f91792dc18c17603fd0
- Compute policy: Hugging Face cpu-upgrade only; no GPU or paid Jobs without a later explicit documented need.
- GitHub repository: https://github.com/MachineLearning-Nerd/icml26-repro-aU2sxdnRuL-distribution-valued-cpd @ 372314edc6fec88f51673a7b4cea3f012914e5b4
- Current phase: claim_1_attempt_3_toy_complete
- Claim 1 state: Three distinct toy routes are complete; full claim remains unverified. Attempt 3 independently verifies the 1-D empirical quantile radial identity for translation, scale, and non-affine deformation (all absolute errors `0.0`) and rejects identity-map, wrong-reference, and uncentered-map controls. The full released R/funcharts mFPCA/paper-scale path remains absent. See `outputs/claim1_attempt3_quantile_audit.md`.
- Claim 2 state: falsified as literally written. Theorem 3.10 supplies the displayed fixed-threshold bound, while the source empirical-quantile corollary has the finite-sample `+ 2/(n0+1)` denominator correction. See `outputs/claim2_attempt1_audit.md`.
- Claim 3 state: falsified for literal source-table scope; see `outputs/claim3_attempt1_audit.md`.
- Claim 4 state: literal source scope is falsified by Attempt 1. Attempt 2 independently found no source-faithful public evaluation route: the paper acknowledges direct data sharing, the retrieved FlowCAP-II URL is a Coming Soon page, and the pinned release lacks files, labels, preprocessing, seed, and runner. This availability finding is not a dataset-level refutation. See `outputs/claim4_attempt1_audit.md` and `outputs/claim4_attempt2_audit.md`.
- Claim 5 state: Attempt 1 is inconclusive because the checksum-matched data and runner do not supply the paper-era PCA-20 inputs/results; Attempt 2 is also inconclusive after source-history, tag/release, and packaging-path audit found no recoverable paper-era outputs and an absent `simulation` dependency. See `outputs/claim5_attempt1_audit.md` and `outputs/claim5_attempt2_audit.md`.
- Claim 6 state: unverified.
- Next action: Claim 5 Attempt 3 — search paper supplement/author materials for exact Reddit outputs, then falsification if still unavailable.
- Publication status: not started
