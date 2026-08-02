# Limitations and deviations

- The author repository omits the imported OT/MFPCA implementation; this route uses the exact cited public CNF implementation and reconstructs the private adapter.
- The immutable public artifact produces 50+49 retained days under the author's own cleaning/split semantics, not the claimed 50+50. This is a scientific blocker, not an assumption-satisfying counterexample.
- The learned CNF barycenter is sampled at 512 points, matching the released wrapper's `n_bary` default but not an explicit Reddit-specific paper value.
- PCA is fitted on Phase I only to avoid monitoring leakage; the paper does not state its fitting scope.
- The released minimum-20 and capped-split semantics conflict with the camera-ready minimum-30 and fixed endpoint description; this route reports the selected endpoints and does not silently call them identical protocols.
- F-CPD, NEWMA, and Scan-B configurations remain unavailable and are not substituted in this route.
- This sixth route exactly matches the pinned author's unusual treatment of missing text as the literal string `nan`, then uses replies only and the released minimum 20 and capped split. The paper appendix instead says minimum 30, but its timing section reports `N_t` beginning at 20. Fixed-window routes produced only 38+48 days (replies/minimum 30), 43+49 (all records/minimum 30), or 50+49 (replies/minimum 20).
- The 2048-sample training objective is accumulated in 256-sample chunks to bound CPU memory; the objective and optimizer update frequency are unchanged.
