"""Deterministic CPU toy audit for live Claim 1.

This does not reproduce the paper-scale monitoring experiments.  It checks the
radial tangent-map identity in the exactly solvable 1-D equal-variance Gaussian
translation case, then applies a small NumPy PCA/T²/SPE monitor to the resulting
translation tangent vectors.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

SEED = 20260730


def pca_scores(phase1: np.ndarray, query: np.ndarray) -> tuple[float, float]:
    """Return rank-1 Hotelling T² and residual SPE for row-vector tangents."""
    center = phase1.mean(axis=0)
    centered = phase1 - center
    _, singular, vt = np.linalg.svd(centered, full_matrices=False)
    component = vt[0]
    eigenvalue = singular[0] ** 2 / (len(phase1) - 1)
    displacement = query - center
    score = float(displacement @ component)
    t2 = score * score / eigenvalue
    residual = displacement - score * component
    spe = float(residual @ residual)
    return float(t2), spe


def run() -> dict:
    rng = np.random.default_rng(SEED)
    n_points = 256
    # In this exact model mu_bar=N(0,1), mu=N(delta,1), T(x)=x+delta.
    barycenter_support = np.sort(rng.normal(0.0, 1.0, n_points))
    delta = 0.75
    transport = barycenter_support + delta
    tangent = transport - barycenter_support
    radial_norm_sq = float(np.mean(tangent**2))
    analytic_w2_sq = delta**2

    # Negative control: identity map omits the distribution translation.
    identity_norm_sq = float(np.mean((barycenter_support - barycenter_support) ** 2))

    # Phase-I tangent vectors are small 2-D translation perturbations; the
    # Phase-II query has a deterministic larger shift. This only tests the
    # stated tangent-space monitor mechanics, not the Table-1 claim.
    phase1_shifts = rng.normal(0.0, 0.04, size=(40, 2))
    phase2_shift = np.array([0.75, 0.05])
    t2, spe = pca_scores(phase1_shifts, phase2_shift)
    return {
        "seed": SEED,
        "model": "1-D equal-variance Gaussian translation; analytic radial map",
        "n_points": n_points,
        "delta": delta,
        "radial_norm_sq": radial_norm_sq,
        "analytic_w2_sq": analytic_w2_sq,
        "absolute_error": abs(radial_norm_sq - analytic_w2_sq),
        "negative_control_identity_norm_sq": identity_norm_sq,
        "negative_control_separation": radial_norm_sq - identity_norm_sq,
        "phase1_vectors": 40,
        "phase2_shift": phase2_shift.tolist(),
        "hotelling_t2_rank1": t2,
        "spe_rank1": spe,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
