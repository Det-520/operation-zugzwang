import json, sys
src = open('make_map.py').read().split("# ============================================================ RENDER")[0]
exec(src)
from shapely.geometry import mapping
def gref(x, y):
    return f"{chr(65+min(14,max(0,int(x//105))))}{min(10,max(1,int(y//105)+1))}"
def cells(g):
    b = g.bounds; out = []
    for i in range(15):
        for j in range(10):
            if g.intersects(box(i*105, j*105, i*105+105, j*105+105)) and g.intersection(box(i*105, j*105, i*105+105, j*105+105)).area > 400: out.append(f"{chr(65+i)}{j+1}")
    return out
def info(g):
    g = g.intersection(MAP)
    c = g.centroid
    return dict(centroid_px=[round(c.x), round(c.y)], centroid_grid=gref(c.x, c.y), bbox_px=[round(v) for v in g.bounds],
                visible_area_sq_mi=round(g.area / SC**2), grid_cells=cells(g))
zones = {
 "Z1": dict(name="Cosmopolis", type="off-map box", note="REDFOR patron, ~8,000 mi away: bombers, airlift, space, cyber", box_px=[1318, 0, 1536, 142], grid="N1-O2"),
 "Z2": dict(name="Asotin", type="off-map box", note="Supports BLUEFOR, ~1,200 mi away", box_px=[0, 418, 164, 522], grid="A5"),
 "Z3": dict(name="Latah", side="REDFOR", type="land", **info(Z3)),
 "Z4": dict(name="Tekoa Highlands", side="Neutral", type="land", **info(Z4)),
 "Z5": dict(name="Tekoa Coast", side="Neutral", type="land (strait north shore)", **info(Z5)),
 "Z6": dict(name="Camas Island", side="REDFOR", type="island", **info(camas)),
 "Z7": dict(name="West Approach", type="sea", label_px=[round(l['cx']), round(l['cy'])] if False else None),
 "Z8": dict(name="The Narrows", type="sea chokepoint", width_mi=round(NARROWS_MI, 1), narrows_px=[[round(gn_pt[0]), round(gn_pt[1])], [round(gs_pt[0]), round(gs_pt[1])]], grid=gref(*((gn_pt+gs_pt)/2))),
 "Z9": dict(name="East Approach", type="sea"),
 "Z10": dict(name="Omak Coast (Fortune Harbor)", side="BLUEFOR", type="land (strait south shore)", **info(Z10)),
 "Z11": dict(name="Omak City (capital)", side="BLUEFOR", type="land", **info(Z11)),
 "Z12": dict(name="Omak Interior", side="BLUEFOR", type="land", **info(Z12)),
 "Z13": dict(name="Open Ocean", type="sea"),
}
for l in LABELS:
    if l['z'] in zones: zones[l['z']]['label_px'] = [round(l['cx']), round(l['cy'])]; zones[l['z']]['label_grid'] = gref(l['cx'], l['cy'])
zones["Z7"].pop("label_px", None) if zones["Z7"].get("label_px") is None else None
# sea zone approximate bounds from dividers
places = {k: dict(px=[round(float(p[0])), round(float(p[1]))], grid=gref(*p)) for k, p in {
  "Latah city": LAT_CITY, "Latah air base": LAT_AB, "Tekoa port (naval)": PORT, "Camas port (naval)": CAM_PORT, "Camas air base": CAM_AB,
  "Fortune Harbor (naval)": HARB, "Omak City (capital)": CAP, "Capital air base": CAP_AB}.items()}
data = dict(
  map=dict(name="Strait of Great Fortune", map_px=[W0, H0], svg_px=[1580, 1140], map_origin_in_svg_px=[22, 22], grid_cell_px=105, grid_cols="A-O (x)", grid_rows="1-10 (y)",
           px_per_mile=SC, miles_per_grid_cell=round(105 / SC), map_extent_mi=[round(W0 / SC), round(H0 / SC)], north="up"),
  lore=dict(narrows_width_mi=round(NARROWS_MI, 1), direct_strait_route_mi=round(dir_mi), southern_bypass_mi=round(byp_mi),
            southern_bypass_extra_mi=extra_mi, southern_bypass_extra_pct=pct, southern_bypass_extra_days_at_15kt=days,
            northern_bypass_extra_mi=4600, northern_bypass_extra_days=11, speed_assumed_kt=15),
  zones=zones, key_places=places,
  omak_island=dict(length_mi=round(LAX / SC), max_width_mi=round((100 + 91) / SC), area_sq_mi=round(omak.area / SC**2)),
  bypass_route_px=[[round(float(x)), round(float(y))] for x, y in bypass[::25]],
)
json.dump(data, open('map_data.json', 'w'), indent=1)
feats = []
for z, g in [("Z3", Z3), ("Z4", Z4), ("Z5", Z5), ("Z6", camas), ("Z10", Z10), ("Z11", Z11), ("Z12", Z12)]:
    feats.append(dict(type="Feature", properties=dict(zone=z, name=zones[z]["name"], side=zones[z].get("side")), geometry=mapping(g.simplify(1.0))))
for i, p in enumerate(islets):
    feats.append(dict(type="Feature", properties=dict(zone="islet", id=i), geometry=mapping(p.simplify(0.5))))
feats.append(dict(type="Feature", properties=dict(zone="bypass", name="Southern bypass around Omak"), geometry=mapping(bypass_ls.simplify(1.0))))
json.dump(dict(type="FeatureCollection", note="Coordinates are map pixels (x right, y down, origin top-left of map frame, 105 px per grid cell, 1.05 px per mile), NOT lat/lon.", features=feats), open('zones_px.geojson', 'w'))
print(json.dumps(data, indent=1)[:3500])
