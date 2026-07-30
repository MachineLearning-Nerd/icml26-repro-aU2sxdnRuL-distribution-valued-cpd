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
python3 -m venv "$ROOT/.venv-repro"
"$ROOT/.venv-repro/bin/python" -m pip install --upgrade pip
"$ROOT/.venv-repro/bin/python" -m pip install -r "$ROOT/requirements.txt"
echo "Bootstrap complete. Run: $ROOT/.venv-repro/bin/python -m pytest -q"
