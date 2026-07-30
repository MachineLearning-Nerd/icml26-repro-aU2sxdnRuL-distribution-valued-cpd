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
# POT 0.9.6 has a supported wheel for CPython 3.12; use uv's managed 3.12
# rather than the host CPython 3.14, for which this upstream dependency cannot
# be built reproducibly.
command -v uv >/dev/null || { echo "uv is required to provision CPython 3.12" >&2; exit 1; }
uv venv --seed --python 3.12 "$ROOT/.venv-repro"
"$ROOT/.venv-repro/bin/python" -m pip install --upgrade pip
"$ROOT/.venv-repro/bin/python" -m pip install -r "$ROOT/requirements.txt"
# The pinned upstream empirical-OT module imports torch and POT. Install the
# CPU-only PyTorch wheel explicitly so the documented bootstrap stays CPU-only.
"$ROOT/.venv-repro/bin/python" -m pip install --index-url https://download.pytorch.org/whl/cpu 'torch==2.7.1+cpu'
"$ROOT/.venv-repro/bin/python" -c 'import numpy, scipy, ot, pytest, torch; print("runtime imports: numpy/scipy/ot/pytest/torch OK")'
echo "Bootstrap complete. Run: $ROOT/.venv-repro/bin/python -m pytest -q"
