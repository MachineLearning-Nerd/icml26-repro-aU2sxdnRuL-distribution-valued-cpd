#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM="$ROOT/upstream/IDD-icml"
PIN="c5b1db4060e5081e5c487f91792dc18c17603fd0"
if [[ ! -d "$UPSTREAM/.git" ]]; then
  rm -rf "$UPSTREAM"
  git clone https://github.com/yyzeng43/IDD-icml.git "$UPSTREAM"
fi
git -C "$UPSTREAM" fetch --tags origin
git -C "$UPSTREAM" checkout --detach "$PIN"
test "$(git -C "$UPSTREAM" rev-parse HEAD)" = "$PIN"
command -v uv >/dev/null || { echo "uv is required to provision CPython 3.12" >&2; exit 1; }
cd "$ROOT"
uv sync --frozen
uv run --frozen python -c 'import numpy, scipy, ot, pytest, torch; print("runtime imports: numpy/scipy/ot/pytest/torch OK")'
echo "Bootstrap complete. Run: uv run --frozen python scripts/run_campaign.py"
