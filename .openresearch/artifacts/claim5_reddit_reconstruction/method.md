# Method

The mandatory fourth route uses the pinned released runner's non-root filter, minimum-20/maximum-500 daily window rule, and last-50/first-50 cutoff split at 2021-01-31. It encodes the checksum-matched comments with normalized embeddings from the pinned SBERT revision, fits PCA-20 on Phase I only, estimates a deterministic 64-support free Wasserstein barycenter, computes exact-EMD barycentric projections, and reconstructs MFPCA T2/SPE from the paper equations. A Gram-matrix eigendecomposition independently checks the SVD statistics. Hotelling T2 monitors daily PCA-space means. The date-shuffle control permutes the observed alarm count across the retained Phase-II dates and counts alarm/event coincidences.

The date-shuffle control estimates chance response-date overlap without changing alarms or selecting windows from the claimed answer. Identity tangents must be rejected as degenerate.
