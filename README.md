# Reproduction: Beyond Euclidean Summaries: Online Change Point Detection for Distribution-Valued Data

ICML 2026 paper #30280 (`aU2sxdnRuL`). This is a CPU-upgrade-first audit of the six live challenge claims.

- Paper: https://openreview.net/forum?id=aU2sxdnRuL
- arXiv: https://arxiv.org/abs/2602.07252
- Official code pin: https://github.com/yyzeng43/IDD-icml/tree/c5b1db4060e5081e5c487f91792dc18c17603fd0
- Live contract: `contract/live_claims.json` (six claims / twelve possible points)

## Current outcomes

- Claim 1: inconclusive; three toy mechanism audits, not a full paper-scale rerun.
- Claims 2–4: literal-source falsifications retained with source and control evidence.
- Claim 5: inconclusive; the source supports post-pause event alignment but the released artifacts do not permit a source-faithful numeric rerun.
- Claim 6: verified only as a scoped finite-dimensional theorem/algebra audit.

## Clean-clone reproduction

```bash
./scripts/bootstrap_reproduction.sh
uv run --frozen python scripts/run_campaign.py
```

The bootstrap script clones the official upstream repository and verifies the exact commit before installing pinned Python dependencies. It intentionally does not claim to recreate unavailable R/funcharts, FlowCAP-II, or paper-era Reddit embedding artifacts.

For Claim 5’s source-archive audit, `src/claim5_attempt3_arxiv_archive_audit.py` downloads and SHA-256-verifies the official arXiv source archive when the local cache is absent.

See `STATUS.md`, `logbook/`, and the tracked `outputs/` evidence for commands, limitations, and claim-specific results.
