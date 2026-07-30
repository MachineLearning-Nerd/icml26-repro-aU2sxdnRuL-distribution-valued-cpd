"""Claim 6 attempt 1: source-pinned epsilon-isometry theorem audit.

This is not an empirical proof of an infinite-dimensional theorem.  It checks
that the pinned manuscript contains the stated assumptions and finite-K bound,
and numerically verifies the theorem's explicit K-versus-epsilon algebra.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "paper_source" / "main0.tex"
OUT = ROOT / "outputs" / "claim6_attempt1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def theorem_block(tex: str) -> str:
    start = tex.index(r"\begin{theorem}[$\varepsilon$-Isometry]")
    end = tex.index(r"\end{theorem}", start) + len(r"\end{theorem}")
    return tex[start:end]


def required_k(a_times_c: float, epsilon: float, trace: float, dimension: int) -> float:
    """The lower bound printed in the theorem, with A_X*C_K combined."""
    return (a_times_c / (epsilon**2 * trace)) ** dimension


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tex = TEX.read_text()
    block = theorem_block(tex)
    required_assumption_markers = {
        "bounded convex domain": r"convex, bounded domain",
        "Holder densities": r"$\alpha$-Hölder continuous",
        "uniform Lipschitz tangent fields": r"\text{Lip}(v_t) \le L",
        "uniform bounded tangent fields": r"\|v_t\|_{L^\infty",
        "kernel Lipschitz condition": r"conditions of Proposition~\ref{prop:kernel_lipschitz}",
    }
    theorem_markers = {
        "eigenvalue tail": r"\sum_{m > K} \lambda_m \le A_{\mathcal{X}} C_{\mathcal{K}} K^{-1/d}",
        "relative error target": r"relative reconstruction error",
        "component lower bound": r"K \ge \left( \frac{A_{\mathcal{X}} C_{\mathcal{K}}}{\varepsilon^2 \operatorname{tr}(\Gamma)} \right)^d",
    }
    missing = [label for label, marker in required_assumption_markers.items() if marker not in tex]
    missing += [label for label, marker in theorem_markers.items() if marker not in block]
    if missing:
        raise RuntimeError(f"missing source markers: {missing}")

    # Fixed dimension and constants: the displayed lower bound is polynomial
    # in epsilon^{-1}, specifically epsilon^{-2d}.
    a_times_c, trace = 3.0, 2.0
    epsilon_pairs = [(0.4, 0.2), (0.2, 0.1), (0.1, 0.05)]
    scaling = []
    for dimension in (1, 2, 5):
        for coarse, fine in epsilon_pairs:
            ratio = required_k(a_times_c, fine, trace, dimension) / required_k(a_times_c, coarse, trace, dimension)
            expected = (coarse / fine) ** (2 * dimension)
            scaling.append({
                "dimension": dimension,
                "epsilon_coarse": coarse,
                "epsilon_fine": fine,
                "observed_k_ratio": ratio,
                "expected_epsilon_minus_2d_ratio": expected,
                "absolute_error": abs(ratio - expected),
            })

    # Negative control: omitting the exponent d would predict epsilon^{-2}; it
    # agrees only in d=1 and is wrong for dimensions explicitly covered by the theorem.
    negative_controls = []
    for dimension in (2, 5):
        coarse, fine = 0.2, 0.1
        actual = required_k(a_times_c, fine, trace, dimension) / required_k(a_times_c, coarse, trace, dimension)
        dropped_dimension_prediction = (coarse / fine) ** 2
        negative_controls.append({
            "dimension": dimension,
            "actual_ratio": actual,
            "dropped_dimension_prediction": dropped_dimension_prediction,
            "control_rejected": actual != dropped_dimension_prediction,
        })

    result = {
        "attempt": "claim_6_attempt_1",
        "scope": "source-pinned theorem/assumption audit plus finite-K algebra check",
        "source": {"file": str(TEX.relative_to(ROOT)), "sha256": sha256(TEX)},
        "theorem_source_excerpt": block,
        "assumptions_found": list(required_assumption_markers),
        "theorem_markers_found": list(theorem_markers),
        "fixed_constants": {"A_X_times_C_K": a_times_c, "trace_Gamma": trace},
        "epsilon_scaling_checks": scaling,
        "negative_controls": negative_controls,
        "verdict": "verified_scoped",
        "verdict_reason": (
            "The source establishes K >= (A_X C_K/(epsilon^2 tr(Gamma)))^d under its stated regularity chain. "
            "For fixed d this is polynomial in target precision; the numerical algebra checks epsilon^{-2d} scaling and rejects the dropped-dimension reading."
        ),
        "limitations": [
            "This is a source/proof-route audit, not an empirical proof of the theorem.",
            "The polynomial degree is 2d, so the guarantee is not dimension-free.",
            "The source requires bounded convex domain, Holder-density/OT regularity, uniform Lipschitz and bounded tangent fields, and the covariance-kernel condition."
        ],
    }
    (OUT / "result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({"verdict": result["verdict"], "checks": len(scaling), "negative_controls": negative_controls}, indent=2))


if __name__ == "__main__":
    main()
