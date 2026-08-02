# Limitations and deviations

- The author repository omits the imported OT/MFPCA implementation; this route reconstructs the equations.
- Barycenter support 64 is declared here but unspecified in the paper.
- PCA is fitted on Phase I only to avoid monitoring leakage; the paper does not state its fitting scope.
- The released minimum-20 and capped-split semantics conflict with the camera-ready minimum-30 and fixed endpoint description; this route reports the selected endpoints and does not silently call them identical protocols.
- F-CPD, NEWMA, and Scan-B configurations remain unavailable and are not substituted in this route.
- This sixth route uses the separate official comments-only file rather than the All file named by the pinned runner. It follows the paper's minimum 30, while the timing section reports `N_t` beginning at 20. Earlier All-file routes produced only 38+48 days (replies/minimum 30), 43+49 (all records/minimum 30), or 50+49 (replies/minimum 20); exact author text cleaning also produced 50+49.
