#!/usr/bin/env bash
# Build everything from the sources, in order. From a fresh clone:
#   python3 tools/fetch_third_party.py   # once: references, fonts, site theme
#   tools/build_all.sh                   # map (if missing), counters, Tongue and Quill, build/, site
#   tools/build_all.sh --map             # rebuild the map too
# Then check the markdown with: npx markdownlint-cli2
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -I tools/fetch_third_party.py --check | grep -E '^missing +(map/fonts|tools/fonts|whitecell-site)/' && { echo "Run python3 tools/fetch_third_party.py first."; exit 1; }
if [ "${1:-}" = --map ] || [ ! -f map/maps/strait_map_v10_full.pdf ]; then
  tools/build_map.sh
fi
tools/build_handouts.sh
tools/build_site.sh
