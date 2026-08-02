# Claim 4 route 1: primary archive probe

On Hugging Face CPU compute, fetch the official FlowRepository record with an explicit User-Agent, hash it, and parse all four-digit FCS names plus the `aml` experiment-variable block. Query the official public API used by FlowRepositoryR at `/list/FR-FCM-ZZYA`, verify that all 2,872 direct file records include MD5 hashes and sizes, then request the first 1,024 bytes of one FCS file. A deliberately nonexistent direct-file URL is the negative control and must return 404 or 410.

This descendant mirrors the official FlowRepositoryR implementation more closely by retaining one public cookie jar across the metadata and file requests. It supplies no user credentials and records only the cookie count, never cookie names or values.

The full-file descendant removes the HTTP Range header and downloads the complete first FCS record exactly as FlowRepositoryR does. Acceptance requires its byte count and MD5 to match the API values (`1,467,197` bytes and `73fbac83f89d49fcc742bb596e1760bc`).

Fixed command: `uv sync --frozen && uv run --frozen python scripts/run_campaign.py`

Estimated compute: 2 cores. Selected flavor: Hugging Face `cpu-upgrade`; no GPU. Actual allocation and runtime are emitted in `raw/probe.json` and the run log.
