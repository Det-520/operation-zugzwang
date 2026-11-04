#!/usr/bin/env bash
# Build the v10 map from map/source/make_map.py (see map/README.md §5):
#   map/maps/strait_map_v10.svg, .png, _full.pdf, _tiles_letter.pdf
#   map/data/map_data.json and zones_px.geojson
#   handouts/assets/game-map.png (the image the Scenario Brief embeds)
# Needs the Inter fonts in map/fonts/ (tools/fetch_third_party.py) and pdftoppm (poppler-utils).
# On NixOS this pulls the Python packages with nix-shell. Elsewhere, install
# numpy, shapely 2.x, pillow, and playwright with Chromium.
set -euo pipefail
cd "$(dirname "$0")/../map"
if [ -z "${CHROMIUM_PATH:-}" ]; then
  CHROMIUM_PATH=$(command -v chromium || ls -d /nix/store/*-chromium-*/bin/chromium 2>/dev/null | head -1 || true)
  export CHROMIUM_PATH
fi
export FONTCONFIG_FILE=$PWD/fonts/fonts.conf
mkdir -p maps
STEPS="python3 -I source/make_map.py maps/strait_map_v10.svg
python3 -I source/render_png.py $PWD/maps/strait_map_v10.svg $PWD/maps/strait_map_v10.png 2
python3 -I source/build_pdfs.py maps/strait_map_v10.svg maps strait_map_v10
cd source && python3 -I export_data.py && mv map_data.json zones_px.geojson ../data/"
PY='python3.withPackages (ps: with ps; [numpy shapely pillow playwright])'
if command -v nix-shell >/dev/null; then
  nix-shell -p "$PY" --run "set -e; $STEPS"
else
  bash -ec "$STEPS"
fi
pdftoppm -q -png -scale-to-x 4200 -scale-to-y -1 -singlefile maps/strait_map_v10_full.pdf ../handouts/assets/game-map
echo "wrote map/maps/, map/data/, handouts/assets/game-map.png"
