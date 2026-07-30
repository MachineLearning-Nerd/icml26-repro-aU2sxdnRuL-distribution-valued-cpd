# Claim 6: finite-dimensional epsilon-isometry


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_0d4c9cf2c327", "created_at": "2026-07-30T07:37:49+00:00", "title": "Claim 6 evidence"}
-->
## Exact claim

Theorem 3.14 gives an epsilon-isometry finite-dimensional tangent approximation with principal-component count polynomial in precision under Lipschitz regularity.

## Evidence and outcome

**Verified, scoped theorem/numerical audit.** The pinned theorem gives `K >= (A_X C_K/(epsilon² tr(Gamma)))^d` under bounded-domain, Hölder-density, optimal-transport, Lipschitz-kernel, and trace conditions. A CPU algebra audit over dimensions 1/2/5 and three epsilon-halving pairs passed all nine checks, recovering epsilon^(-2d) scaling. A control dropping `d` failed: at epsilon .2→.1, actual K ratios were 16 (`d=2`) and 1024 (`d=5`), versus invalid dimension-free ratio 4.

Evidence: `outputs/claim6_attempt1_audit.md`, `outputs/claim6_attempt1/result.json`, `src/claim6_attempt1_theorem_audit.py`, `tests/test_claim6_attempt1.py`, logs, and hashes. This is not an empirical proof and does not establish dimension-free behavior.

Source pin: [official code commit](https://github.com/yyzeng43/IDD-icml/tree/c5b1db4060e5081e5c487f91792dc18c17603fd0). No Hub model/dataset/Job/Bucket was used.
