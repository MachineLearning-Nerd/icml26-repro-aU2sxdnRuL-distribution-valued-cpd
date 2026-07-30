"""Independent 1-D empirical quantile audit for Claim 1, Attempt 3.

No upstream OT helper is imported.  Equal-mass empirical measures are represented
by sorted quantiles.  In 1-D, their optimal map is paired quantiles and
W2^2(mean) is mean((q_target-q_reference)^2).  A phase-I barycenter is the
pointwise average of the phase-I quantile functions.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "claim1_attempt3_quantile_audit.json"


def q(samples: np.ndarray) -> np.ndarray:
    values = np.asarray(samples, dtype=float).reshape(-1)
    if values.size == 0 or not np.isfinite(values).all():
        raise ValueError("empirical support must be finite and nonempty")
    return np.sort(values)


def transport(reference: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, float]:
    """Exact equal-weight 1-D empirical Monge map and squared W2 distance."""
    reference, target = q(reference), q(target)
    if reference.shape != target.shape:
        raise ValueError("this clean-room equal-weight audit requires equal support sizes")
    displacement = target - reference
    return target, float(np.mean(displacement**2))


def tangent_monitor(phase1_tangents: np.ndarray, phase2_tangent: np.ndarray) -> dict[str, float]:
    """Transparent rank-1 PCA/T2/SPE monitor on flattened tangent fields."""
    x = np.asarray(phase1_tangents, dtype=float)
    z = np.asarray(phase2_tangent, dtype=float)
    mean = x.mean(axis=0)
    centered = x - mean
    _, singular, vt = np.linalg.svd(centered, full_matrices=False)
    component = vt[0]
    eig = float(singular[0] ** 2 / (len(x) - 1))
    score = float((z - mean) @ component)
    reconstruction = mean + score * component
    return {
        "t2": float(score**2 / eig),
        "spe": float(np.sum((z - reconstruction) ** 2)),
        "leading_eigenvalue": eig,
    }


def main() -> None:
    # 12 equal-mass points.  The families include translation, scale, and a
    # non-affine shape deformation; all are independently evaluated in quantile
    # space rather than using the prior Gaussian-only or upstream-POT route.
    base = np.linspace(-1.1, 1.1, 12)
    phase1 = np.stack([base - 0.08, base, base + 0.08, base + 0.02])
    barycenter = np.mean(np.sort(phase1, axis=1), axis=0)
    families = {
        "translation": barycenter + 0.65,
        "scale": 1.45 * barycenter,
        "non_affine_shape": barycenter + 0.28 * barycenter**2 - 0.12,
    }
    results: dict[str, dict[str, float]] = {}
    for name, target in families.items():
        mapped, w2_sq = transport(barycenter, target)
        tangent = mapped - barycenter
        results[name] = {
            "radial_tangent_mean_square": float(np.mean(tangent**2)),
            "quantile_w2_square": w2_sq,
            "identity_map_mean_square": 0.0,
            "identity_control_gap": w2_sq,
        }

    # Negative controls use the non-affine target.  Wrong reference changes the
    # quantile coupling; omitting the -Id centering turns a displacement field
    # into an absolute position vector and must not equal W2^2 in general.
    target = families["non_affine_shape"]
    _, correct_w2 = transport(barycenter, target)
    wrong_reference = barycenter + 0.3
    _, wrong_reference_w2 = transport(wrong_reference, target)
    raw_map_second_moment = float(np.mean(q(target) ** 2))
    phase1_tangents = np.stack([q(cloud) - barycenter for cloud in phase1])
    phase2_tangent = q(target) - barycenter
    monitor = tangent_monitor(phase1_tangents, phase2_tangent)

    payload = {
        "method": "clean_room_equal_weight_1d_quantile_transport",
        "seed_or_construction": "deterministic linspace support, no RNG",
        "n_support": int(base.size),
        "phase1_clouds": int(phase1.shape[0]),
        "families": results,
        "negative_controls": {
            "correct_non_affine_w2_square": correct_w2,
            "wrong_reference_w2_square": wrong_reference_w2,
            "wrong_reference_gap": abs(wrong_reference_w2 - correct_w2),
            "uncentered_raw_map_second_moment": raw_map_second_moment,
            "uncentered_gap": abs(raw_map_second_moment - correct_w2),
        },
        "independent_pca_t2_spe": monitor,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
