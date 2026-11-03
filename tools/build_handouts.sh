#!/usr/bin/env bash
# Build everything in FINALIZED/ from the markdown (see tools/build_handouts.py).
#   tools/build_handouts.sh              # counters, Tongue and Quill documents, then every release PDF
#   tools/build_handouts.sh --only Brief # pass options through to build_handouts.py
# On NixOS this pulls the Python packages with nix-shell. Elsewhere, install
# markdown-it-py, mdit-py-plugins, pypdf, and playwright, then run the two scripts directly.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -z "${CHROMIUM_PATH:-}" ]; then
  CHROMIUM_PATH=$(command -v chromium || ls -d /nix/store/*-chromium-*/bin/chromium 2>/dev/null | head -1 || true)
  export CHROMIUM_PATH
fi
python3 -I tools/check_assets.py
python3 -I tools/make_counters.py
python3 -I tools/tq/build_tq.py
PY='python3.withPackages (ps: with ps; [markdown-it-py mdit-py-plugins pypdf playwright])'
if command -v nix-shell >/dev/null; then
  nix-shell -p "$PY" --run "python3 -I tools/build_handouts.py $*"
else
  python3 -I tools/build_handouts.py "$@"
fi
