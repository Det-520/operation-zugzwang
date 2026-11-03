#!/usr/bin/env bash
# Generate and build the white cell site (whitecell-site/, see tools/build_site.py).
#   tools/build_site.sh          # pages + jekyll build  -> whitecell-site/_site/
#   tools/build_site.sh serve    # pages + jekyll serve  -> http://127.0.0.1:4000
# Run tools/build_handouts.sh first if the PDFs changed: the site copies FINALIZED/.
set -euo pipefail
cd "$(dirname "$0")/.."
PY='python3.withPackages (ps: with ps; [markdown-it-py mdit-py-plugins])'
if command -v nix-shell >/dev/null; then
  nix-shell -p "$PY" --run "python3 -I tools/build_site.py"
else
  python3 -I tools/build_site.py
fi
cd whitecell-site
if [ "${1:-build}" = serve ]; then
  jekyll serve --livereload
else
  jekyll build
fi
