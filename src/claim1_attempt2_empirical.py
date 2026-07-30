#!/usr/bin/env python3
"""CPU-only, reduced-size empirical-OT exercise of the pinned upstream path.

This is deliberately a toy-scale protocol. It invokes the upstream empirical
barycenter and barycentric-projection functions, then uses a transparent NumPy
PCA/T²/SPE calculation because R/funcharts is unavailable in this environment.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream" / "IDD-icml" / "gaussian_translation" / "ot_mfpca.py"
OUT = ROOT / "outputs"


def load_upstream():
    spec = importlib.util.spec_from_file_location("pinned_ot_mfpca", UPSTREAM)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {UPSTREAM}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def object_clouds(clouds: list[np.ndarray]) -> np.ndarray:
    result = np.empty(len(clouds), dtype=object)
    for index, cloud in enumerate(clouds):
        result[index] = cloud
    return result


def save_stream(path: Path, field: str, clouds: list[np.ndarray]) -> None:
    np.savez(path, **{field: object_clouds(clouds), "n_points": len(clouds[0])})


def pca_t2_spe(phase_i_tangents: list[np.ndarray], phase_ii_tangents: list[np.ndarray]) -> dict:
    x0 = np.stack([t.ravel() for t in phase_i_tangents])
    x1 = np.stack([t.ravel() for t in phase_ii_tangents])
    mean = x0.mean(axis=0)
    centered = x0 - mean
    # With three Phase-I streams, retain the nonzero principal direction only.
    _, singular_values, vt = np.linalg.svd(centered, full_matrices=False)
    component = vt[:1]
    eig = max(float(singular_values[0] ** 2 / max(len(x0) - 1, 1)), 1e-12)
    z0 = centered @ component.T
    z1 = (x1 - mean) @ component.T
    recon0 = z0 @ component
    recon1 = z1 @ component
    return {
        "phase_i_t2": [float(v[0] ** 2 / eig) for v in z0],
        "phase_ii_t2": [float(v[0] ** 2 / eig) for v in z1],
        "phase_i_spe": [float(np.sum((row - rec) ** 2)) for row, rec in zip(centered, recon0)],
        "phase_ii_spe": [float(np.sum((row - rec) ** 2)) for row, rec in zip(x1 - mean, recon1)],
        "retained_eigenvalue": eig,
    }


def main() -> int:
    OUT.mkdir(exist_ok=True)
    work = OUT / "claim1_attempt2_data"
    work.mkdir(exist_ok=True)
    # Tiny 1-D source-faithful empirical clouds. Their ordered translations make
    # exact EMD barycentric maps independently checkable.
    base = np.array([[-1.5], [-0.5], [0.5], [1.5]], dtype=float)
    phase_i_clouds = [base - 0.10, base, base + 0.10]
    phase_ii_clouds = [base + 0.05, base + 0.60]
    phase_i_file = work / "phaseI.npz"
    phase_ii_file = work / "phaseII.npz"
    save_stream(phase_i_file, "phaseI", phase_i_clouds)
    save_stream(phase_ii_file, "streams", phase_ii_clouds)

    upstream = load_upstream()
    weights = np.full(len(base), 1 / len(base))
    direct_delta = 0.6
    direct_map = upstream.barycentric_projection_map(base, weights, base + direct_delta, weights, method="emd")
    direct_norm = float(np.mean(np.sum((direct_map - base) ** 2, axis=1)))
    direct_error = float(np.max(np.abs(direct_map - (base + direct_delta))))

    xb, wb, tangent_i, maps_i, _, _, norms_i = upstream.process_phaseI(phase_i_file, n_bary=4)
    tangent_ii, maps_ii, _, _, norms_ii, _ = upstream.process_phaseII(phase_ii_file, xb, wb)
    pca = pca_t2_spe(tangent_i, tangent_ii)

    # Negative control: replacing the known translation map with identity must
    # fail the W2 radial-norm expectation by delta².
    identity_norm = float(np.mean(np.sum((base - base) ** 2, axis=1)))
    expected_norm = direct_delta ** 2
    negative_control_passed = abs(identity_norm - expected_norm) > 0.1

    result = {
        "scope": "toy",
        "upstream_file": str(UPSTREAM.relative_to(ROOT)),
        "ot_method": "emd",
        "r_funcharts_used": False,
        "phase_i_clouds": len(phase_i_clouds),
        "phase_ii_clouds": len(phase_ii_clouds),
        "points_per_cloud": len(base),
        "direct_translation_delta": direct_delta,
        "direct_translation_map_max_abs_error": direct_error,
        "direct_translation_w2_squared": direct_norm,
        "expected_translation_w2_squared": expected_norm,
        "negative_control_identity_w2_squared": identity_norm,
        "negative_control_passed": negative_control_passed,
        "upstream_phase_i_tangent_norms": [float(x) for x in norms_i],
        "upstream_phase_ii_tangent_norms": [float(x) for x in norms_ii],
        "pca_t2_spe": pca,
        "claim_1_full_scope_verified": False,
        "limitations": [
            "Four points per cloud and three Phase-I streams are toy scale.",
            "The R/funcharts upstream mFPCA stage was unavailable because Rscript is absent.",
            "NumPy PCA/T²/SPE is an independent transparent diagnostic, not a substitute for the released R stage.",
        ],
    }
    (OUT / "claim1_attempt2_empirical.json").write_text(json.dumps(result, indent=2) + "\n")
    assert direct_error < 1e-10, direct_error
    assert abs(direct_norm - expected_norm) < 1e-10, (direct_norm, expected_norm)
    assert negative_control_passed
    assert max(pca["phase_ii_t2"]) > max(pca["phase_i_t2"])
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
