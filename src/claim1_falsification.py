"""Claim 1 scope test: a source-aligned non-Monge empirical OT construction.

The pinned implementation returns the barycentric projection of an optimal
coupling. That projection is not generally a deterministic transport map, so
its squared tangent norm need not equal the coupling's W2^2 cost when mass is
split. This script uses the smallest such example.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream" / "IDD-icml" / "gaussian_translation" / "ot_mfpca.py"
OUTPUT = ROOT / "outputs" / "claim1_falsification_scope.json"


def load_upstream():
    spec = importlib.util.spec_from_file_location("idd_ot_mfpca", UPSTREAM)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load pinned upstream source: {UPSTREAM}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    # mu_bar = delta_0 and mu = (delta_-1 + delta_1)/2.  Any deterministic map
    # from the one-point source has a point-mass pushforward and cannot equal mu.
    source = np.array([[0.0]])
    source_weights = np.array([1.0])
    target = np.array([[-1.0], [1.0]])
    target_weights = np.array([0.5, 0.5])

    upstream = load_upstream()
    projection = upstream.barycentric_projection_map(
        source, source_weights, target, target_weights, method="emd"
    )
    tangent = projection - source
    source_tangent_norm = float(np.sum(source_weights[:, None] * tangent**2))

    # The only feasible coupling is [1/2, 1/2], so its transport cost is 1.
    coupling = np.array([[0.5, 0.5]])
    squared_cost = (source[:, None, :] - target[None, :, :]) ** 2
    coupling_w2_squared = float(np.sum(coupling[:, :, None] * squared_cost))

    result = {
        "construction": {
            "source": "delta_0",
            "target": "0.5*delta_-1 + 0.5*delta_1",
            "source_support": source.tolist(),
            "target_support": target.tolist(),
            "coupling": coupling.tolist(),
        },
        "pinned_upstream_projection": projection.tolist(),
        "source_tangent_norm_squared": source_tangent_norm,
        "coupling_w2_squared": coupling_w2_squared,
        "equality_gap": coupling_w2_squared - source_tangent_norm,
        "deterministic_map_exists": False,
        "interpretation": (
            "The source implementation's barycentric projection is [0], yielding "
            "zero tangent norm, while the optimal-coupling W2^2 is 1. The radial "
            "isometry therefore cannot be applied to this non-Monge, atomic source "
            "construction without additional assumptions. This tests an over-broad "
            "literal reading only; it does not refute Equation 6/Proposition 3.4 "
            "under their intended regularity/Monge-map conditions."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
