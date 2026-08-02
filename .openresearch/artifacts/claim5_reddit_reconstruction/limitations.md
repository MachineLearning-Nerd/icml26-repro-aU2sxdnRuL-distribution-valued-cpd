# Limitations and deviations

- The author repository omits the imported OT/MFPCA implementation; this route reconstructs the equations.
- Barycenter support 64 is declared here but unspecified in the paper.
- PCA is fitted on Phase I only to avoid monitoring leakage; the paper does not state its fitting scope.
- F-CPD, NEWMA, and Scan-B configurations remain unavailable and are not substituted in this route.
- This third route uses replies only and the released runner's minimum 20. The paper appendix instead says minimum 30, but its timing section reports `N_t` beginning at 20. Routes using minimum 30 produced only 38+48 days (replies) or 43+49 (all records).
