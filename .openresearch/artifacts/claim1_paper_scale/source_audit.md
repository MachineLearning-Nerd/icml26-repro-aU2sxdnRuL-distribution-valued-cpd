# Claim 1 source audit

The pinned arXiv source is `paper_source/main0.tex`, obtained on 2026-08-02 from arXiv 2602.07252. The source archive SHA-256 is `6d4af865d403a1c4f72ed3ef8057069212ac1633aa79410b4607b04a8b9edb87`.

Proposition 3.4 (source lines 427–451) quantifies over every target in P2(R^d), assuming the reference is absolutely continuous and the cost is squared Euclidean. It states exact equality between squared W2 distance and the L2 norm of the unique Brenier displacement. Lines 516–570 define Phase-I centering, the empirical covariance operator, Hotelling T2, and SPE.

The continuum reference here is N(0,I5), satisfying absolute continuity and finite second moment. Positive diagonal affine maps are gradients of strictly convex quadratics, hence their graph is the unique Brenier transport. The finite empirical audit also solves six complete 300-by-300 assignment problems instead of assuming the known pairing is optimal.

The practical paper uses barycentric projection for arbitrary discrete batches and explicitly notes that its norm can contract when the plan is not deterministic (Proposition 3.6). This experiment deliberately uses deterministic empirical optimal maps, so the exact radial equality—not the weaker contraction—is the applicable contract.
