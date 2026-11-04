# Strait of Great Fortune: wargame theater map (handoff package)

A fictional trade-strait theater modeled on the Strait of Malacca. This package has the finished map, structured data about it, and the Python that generates it. The map is **v10**. v10 is v9 with Camas Island and everything on it moved about 140 mi southwest, so the Camas air base sits inside PrSM range (~310 mi) of B-10 in Omak Interior (Z12): about 290 mi. The bypass route and the dividers were redrawn to fit.

## 1. Premise

The strait is the only practical route between the western and eastern approaches. Every alternative is long and expensive, and that cost is the central lore of the game.

| Fact | Value |
| --- | --- |
| Chokepoint width (The Narrows, Z8) | about 25 mi (24.7 measured) |
| Direct route through the strait (west to east, across the map) | about 1,363 mi |
| Strait length (West Approach to East Approach) | about 750 mi |
| Southern bypass around the island of Omak | about 1,993 mi, which is **+650 mi (+45%)**, about 2 extra days at 15 kt |
| Northern bypass around the Latah-Tekoa landmass | about **+4,600 mi** (about 11 extra days); the landmass continues off the map |
| Scale | 1.05 px per mile; one grid square = about 100 mi; the map shows about 1,463 x 975 mi |
| Omak island | about 1,322 mi long and about 182 mi at its widest (Sumatra-like, long and thin) |

## 2. Zones (Z1 to Z13)

Grid references use the printed A-O (columns) and 1-10 (rows) margin labels. Data: `data/map_data.json`.

| Zone | Name | Side | Type | Where on the map | Notes |
| --- | --- | --- | --- | --- | --- |
| Z1 | Cosmopolis | REDFOR patron | off-map box | NE corner (N1-O2) | about 8,000 mi away; bombers, airlift, space, cyber |
| Z2 | Asotin | supports BLUEFOR | off-map box | W edge (A5) | about 1,200 mi away |
| Z3 | Latah | REDFOR | land | NW (A1-E6) | air base + city at C4 |
| Z4 | Tekoa Highlands | neutral | land | N (F1-L5) | mountainous; continues off-map to the north |
| Z5 | Tekoa Coast | neutral | land | north shore of the strait (F4-J6) | naval port at G6 |
| Z6 | Camas Island | REDFOR | island | E (L4-M5) | port M5, air base L5 |
| Z7 | West Approach | sea | sea | west entrance to the strait (C5-D6) | |
| Z8 | The Narrows | sea | chokepoint | about I6, the narrowest point (about 25 mi) | |
| Z9 | East Approach | sea | sea | east exit (J6) | |
| Z10 | Omak Coast (Fortune Harbor) | BLUEFOR | land | Omak's north shore facing the strait (D6-G7) | naval base at F7 |
| Z11 | Omak City (capital) | BLUEFOR | land | east end of Omak (K8) | capital at J8, air base at K8 |
| Z12 | Omak Interior | BLUEFOR | land | rest of Omak (G7-H8) | mountain ridge on the SW side |
| Z13 | Open Ocean | sea | sea | far east (N3, beyond Camas) | the southern bypass arrives here |

The sea zones (Z7, Z8, Z9, Z13) are not hard polygons. They are bounded by dashed divider lines on the map and by the position of their labels, so use `label_px` in the JSON as their anchor. The land zones (Z3-Z6, Z10-Z12) are exact polygons in `data/zones_px.geojson`.

Key places (px and grid) are in `map_data.json` under `key_places`: Latah city and air base, Tekoa port, Camas port and air base, Fortune Harbor, the capital and its air base.

## 3. Map symbology

- **Sides:** REDFOR = salmon tint; BLUEFOR = pale blue; neutral Tekoa = pale green; Tekoa coast = tan.
- **Icons:** star = capital, plane = air base, anchor = naval base or port, ring = town.
- **Linework:** primary roads (red with a black casing), secondary roads (white), rivers (blue), brown contours with spot heights, zone boundaries (purple dash-dot), and the bypass route (orange dashed).
- **Terrain (all fictional):** Omak has a mountain ridge along its SW side, rivers flowing NE to delta coasts, and a flat NE lowland with the main road. Tekoa Highlands is a mountain mass. Islands cluster off Omak's NE coast and in a chain off its SW coast.
- Style reference: a muted USGS topographic sheet, with a title and notes footer.

## 4. Files

```text
maps/                               built by tools/build_map.sh (not in git)
  strait_map_v10.svg                master vector map, 1580 x 1140 px
  strait_map_v10.png                2x raster of the same map
  strait_map_v10_full.pdf           one page, 31.5 x 22.7 in (the same scale as the assembled tiles)
  strait_map_v10_tiles_letter.pdf   9 letter pages, 3 x 3 (portrait, the map turned on the page) that butt together into the full map
data/
  map_data.json                     scale, lore numbers, zone table (centroids, bounding boxes, areas, grid cells), key places, bypass waypoints
  zones_px.geojson                  land zone polygons, islets and bypass line, in map pixels (see below)
fonts/                              fonts.conf so Chromium uses the Inter OTFs (SIL Open Font License; fetched by tools/fetch_third_party.py)
source/
  make_map.py                       geometry, labels, QA checks, then the SVG writer (after the RENDER marker)
  render_png.py                     SVG -> PNG in Chromium
  build_pdfs.py                     SVG -> full-sheet PDF and portrait letter tiles
  export_data.py                    runs the geometry half of make_map.py and writes data/
```

**Coordinates:** all geometry is in *map pixels*, not lat/lon. The origin is the top-left of the map frame, x increases right, y increases down, the map frame is 1536 x 1024, and one grid cell is 105 px. The SVG has a 22 px margin, so add 22 to both coordinates to get SVG coordinates. Miles = pixels / 1.05.

## 5. Regenerating or editing

- Needs Python 3, `numpy`, `shapely` 2.x, `Pillow`, `playwright` with Chromium, and the Inter font. The code reads Inter from `fonts/` (override with `INTER_FONT_DIR`).
- Edit `make_map.py`. Its first half is the geometry, labels, and QA checks; after the `RENDER` marker comes the SVG writer. `export_data.py` runs only the first half. Every random choice is seeded, so the output is identical on each run.
- Camas is placed with `CAM_D` in `make_map.py`: everything on or around the island is written in v9 coordinates and shifted by that offset.
- Build with `tools/build_map.sh` from the project root. It writes `maps/` and `data/`, then refreshes `handouts/assets/game-map.png`, the image the Scenario Brief embeds. On NixOS it pulls the Python packages with `nix-shell`; elsewhere install them first. It sets `FONTCONFIG_FILE` to `fonts/fonts.conf` so Chromium uses Inter.
- If a distance changes, update `scenario/00-overview.md` §3.3 and `handouts/common/scenario-brief.md` §3, and check R-01's limitation and the worked example turn (`RULES.md` §10).
- The built-in QA prints to stderr: roads and rivers outside land, overlapping roads, label overlaps, and islet overlaps should all report zero.

## 6. Caveats for integration

- The geography is procedurally generated. Roads and rivers follow hand-tuned rules and are not simulated terrain.
- Elevations (contour interval and spot heights) and the distances in the footer are invented for the fiction. Nothing on the map encodes depth, movement cost, or terrain effects. The bypass distances come from the drawn route.
- The bypass route drawn is the southern one only. The northern bypass is stated in the callout and is not drawn.
- Sea zones Z7, Z9 and Z13 and the off-map boxes do not have exact polygons.
- Depth soundings were deliberately removed.
