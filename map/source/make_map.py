import math, sys
import numpy as np
from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, Point, box
from shapely.ops import unary_union, nearest_points
from shapely import affinity
from shapely.validation import make_valid
from PIL import ImageFont

W0, H0 = 1536, 1024
MAP = box(0, 0, W0, H0)
SC = 1.05                       # px per mile
INK = "#1f2a33"

def log(*a): print(*a, file=sys.stderr)

# ------------------------------------------------------------------ helpers
def catmull(pts, closed=False, step=3.0):
    pts = [np.array(p, float) for p in pts]
    n = len(pts); out = []
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1 = pts[i]; p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        m = max(2, int(np.linalg.norm(p2 - p1) / step))
        for t in np.linspace(0, 1, m, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed: out.append(pts[-1])
    return np.array(out)

def noise_offsets(n, seg, amp=1.0, seed=0):
    r = np.random.default_rng(seed)
    s = np.arange(n) * seg
    tot = np.zeros(n)
    for wl in np.geomspace(720, 9, 16):
        a = 0.11 * wl ** 0.85 * r.uniform(0.5, 1.15)
        env = 0.55 + 0.45 * np.sin(2 * np.pi * s / (wl * r.uniform(2.5, 5)) + r.uniform(0, 6.28))
        tot += a * amp * np.sin(2 * np.pi * s / wl + r.uniform(0, 6.28)) * env
    return tot

def displace(P, amp=1.0, seed=0, weight=None):
    n = len(P)
    seg = np.mean(np.linalg.norm(np.diff(P, axis=0), axis=1))
    T = np.gradient(P, axis=0); T /= (np.linalg.norm(T, axis=1)[:, None] + 1e-9)
    N = np.stack([-T[:, 1], T[:, 0]], axis=1)
    off = noise_offsets(n, seg, amp, seed)
    if weight is not None: off = off * weight(P)
    return P + N * off[:, None]

def path_d(P, close=True):
    P = np.asarray(P)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in P)
    return d + (" Z" if close else "")

def polys_of(g):
    if g is None or g.is_empty: return []
    if g.geom_type == 'Polygon': return [g]
    if g.geom_type in ('MultiPolygon', 'GeometryCollection'):
        r = []
        for x in g.geoms: r += polys_of(x)
        return r
    return []

def flat_lines(g):
    out = []
    if g is None or g.is_empty: return out
    t = g.geom_type
    if t == 'LineString': out.append(g)
    elif t == 'LinearRing': out.append(LineString(g.coords))
    elif t == 'Polygon':
        out += flat_lines(g.exterior)
        for h in g.interiors: out += flat_lines(h)
    elif t in ('MultiLineString', 'GeometryCollection', 'MultiPolygon'):
        for x in g.geoms: out += flat_lines(x)
    return out

def poly_d(g):
    ds = []
    for p in polys_of(g):
        ds.append(path_d(np.array(p.exterior.coords)[:-1]))
        for h in p.interiors: ds.append(path_d(np.array(h.coords)[:-1]))
    return " ".join(ds)

def clean(g, r=1.1):
    g = make_valid(g)
    ps = polys_of(g)
    g = max(ps, key=lambda x: x.area)
    g = g.buffer(r, join_style=1).buffer(-2 * r, join_style=1).buffer(r, join_style=1)
    ps = polys_of(g)
    g = max(ps, key=lambda x: x.area)
    return Polygon(g.exterior)

def star_blob(cx, cy, rx, ry, seed, rot=0.0, amp=0.18, n=64):
    r = np.random.default_rng(seed)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rad = np.ones(n)
    for k in (2, 3, 4, 5):
        rad += amp / (k - 0.5) * r.uniform(0.4, 1.0) * np.cos(k * th + r.uniform(0, 6.28))
    rad = np.clip(rad, 0.55, None)
    x, y = rx * rad * np.cos(th), ry * rad * np.sin(th)
    c, s = math.cos(rot), math.sin(rot)
    return Polygon(np.stack([cx + x * c - y * s, cy + x * s + y * c], axis=1))

# ------------------------------------------------------------------ text measurement
import os
_FD = os.environ.get("INTER_FONT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")) + "/"
_FF = {400: "Inter-Regular.otf", 650: "Inter-SemiBold.otf", 700: "Inter-Bold.otf"}
_fc = {}
def tw(text, size, weight=650, ls=0.0):
    k = (weight, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(_FD + _FF[weight], int(size * 10))
    return _fc[k].getlength(text) / 10.0 + ls * len(text)

# ------------------------------------------------------------------ geography
P0 = np.array([90., 545.]); P1 = np.array([1425., 925.])
AX = P1 - P0; LAX = np.linalg.norm(AX); DV = AX / LAX
NV = np.array([-DV[1], DV[0]])
ANG = math.degrees(math.atan2(DV[1], DV[0]))
ROT = math.radians(ANG)
def axis(t): return P0 + AX * t + NV * (22 * np.sin(2 * np.pi * t + 0.4) + 10 * np.sin(5 * np.pi * t + 1.0))
def wprof(t):
    t = np.clip(t, 0, 1)
    return 100 * np.sin(np.pi * t) ** 0.46 * (1 + 0.07 * np.sin(11 * t + 1) + 0.11 * np.sin(23 * t + 2) + 0.06 * np.sin(41 * t + .5))
T_H = 0.40
IN_HW, IN_D = 0.02, 34.0
def inlet_depth(t):
    u = (t - T_H) / IN_HW
    return IN_D * math.cos(math.pi * u / 2) ** 2 if abs(u) < 1 else 0.0
def Nbase(t): return axis(t) - NV * wprof(t)
def delta(t): return sum(12 * math.exp(-((t - c) / 0.016) ** 2) for c in (.56, .665, .775, .885))
def Ncoast(t): return Nbase(t) + NV * inlet_depth(t) - NV * delta(t)
def wprofS(t):
    t = np.clip(t, 0, 1)
    return 91 * np.sin(np.pi * t) ** 0.46 * (1 + 0.025 * np.sin(11 * t + 1) + 0.03 * np.sin(23 * t + 2))
def Scoast(t): return axis(t) + NV * wprofS(t)
_gt = [0, .08, .16, .24, .30, .34, .42, .47, .50]
_gg = [110, 100, 88, 66, 38, 26.5, 55, 110, 175]
def gap(t): return float(np.interp(t, _gt, _gg))
def shore(t): return Nbase(t) - NV * gap(t)
def mid(t): return 0.5 * (shore(t) + Nbase(t))

ANCH = [mid(0.34), Nbase(T_H) + NV * 20]
def wfun(P):
    d = np.min([np.hypot(P[:, 0] - a[0], P[:, 1] - a[1]) for a in ANCH], axis=0)
    w = np.clip((d - 30) / 150, 0.12, 1.0)
    west = np.clip((P[:, 0] - 110) / 110, 0.3, 1.0)
    return np.where(P[:, 1] < 470, w * west, w)

tg = np.unique(np.concatenate([np.linspace(0, 1, 90), np.linspace(T_H - 1.12 * IN_HW, T_H + 1.12 * IN_HW, 21)]))
omak_ctrl = [tuple(Ncoast(t)) for t in tg] + [tuple(Scoast(t)) for t in tg[::-1][1:-1]]
_omak_base = catmull(omak_ctrl, closed=True, step=3)

def build_north_base():
    global _north_base, ANCH
    ANCH = [mid(0.34), Nbase(T_H) + NV * 20]
    ts_sh = np.linspace(0.50, 0.07, 26)
    nctrl = [(1135, -120), (1142, -20), (1165, 55), (1192, 130), (1196, 200), (1170, 255), (1115, 305), (1040, 360), (960, 410), (895, 450)]
    nctrl += [tuple(shore(t)) for t in ts_sh]
    nctrl += [(190, 410), (150, 391), (100, 381), (0, 375), (-120, 373)]
    _north_base = catmull(nctrl, step=3)

def raw_coasts(sn, ss):
    nc = displace(_north_base, amp=1.3, seed=sn, weight=wfun)
    sc = displace(_omak_base, amp=0.8, seed=ss, weight=wfun)
    return nc, sc

def try_coasts(sn, ss):
    build_north_base()
    nc, sc = raw_coasts(sn, ss)
    north = clean(Polygon(np.vstack([[(1135, -120)], nc[1:], [(-120, -120)]])))
    omak = clean(Polygon(sc))
    return north, omak

_found = None
for gv in np.arange(22.0, 40.0, 0.25):
    _gg[5] = gv
    north, omak = try_coasts(4, 5)
    d = north.distance(omak) / SC
    a_ = nearest_points(north, omak)[0]
    if 24.6 <= d <= 25.4 and 420 < a_.x < 700:
        _found = (4, 5, gv, d); break
if _found is None:
    cand = [(a, b) for a in range(3, 40) for b in range(5, 25)]
    for sn, ss in cand:
        _gg[5] = 26.5
        north, omak = try_coasts(sn, ss)
        d = north.distance(omak) / SC
        a_ = nearest_points(north, omak)[0]
        if 24.4 <= d <= 25.6 and 420 < a_.x < 700:
            _found = (sn, ss, 26.5, d); break
log("coast seeds / gap param", _found)
gn_pt = np.array(nearest_points(north, omak)[0].coords[0]); gs_pt = np.array(nearest_points(north, omak)[1].coords[0])
NARROWS_MI = north.distance(omak) / SC

# Camas sits ~135 mi SW of its v9 position so its air base is inside PrSM range (~310 mi) of Omak Interior (Z12).
# Everything drawn on or around the island is placed in v9 coordinates and shifted by CAM_D.
CAM_D = np.array([-100.0, 100.0])
def cam(x, y): return tuple(np.array([x, y]) + CAM_D)
camas_ctrl = [cam(*p) for p in [(1272, 318), (1286, 290), (1315, 268), (1350, 258), (1392, 264), (1425, 282), (1442, 312),
              (1432, 340), (1402, 358), (1360, 364), (1318, 356), (1288, 342)]]
camas = clean(Polygon(displace(catmull(camas_ctrl, closed=True, step=2.5), amp=0.55, seed=5)))
land = unary_union([north, omak, camas])

# ------------------------------------------------------------------ route around Omak
byp = [(46, 534), (24, 584), (32, 634)]
byp += [tuple(Scoast(t) + NV * 62) for t in np.linspace(0.04, 0.99, 22)]
byp += [(1478, 962), (1506, 912), (1512, 830), (1502, 730), (1478, 640), (1450, 570), (1420, 520)]
bypass = catmull(byp, step=2)
bypass_ls = LineString(bypass)
direct = catmull([(46, 470)] + [tuple(mid(t)) for t in np.linspace(0.08, 0.50, 12)] + [(1100, 470), (1300, 490), (1420, 520)], step=2)
byp_mi, dir_mi = bypass_ls.length / SC, LineString(direct).length / SC
extra_mi = int(round((byp_mi - dir_mi) / 50.0) * 50)
days = max(1, round((byp_mi - dir_mi) / 414))
pct = int(round(100 * (byp_mi - dir_mi) / dir_mi / 5.0) * 5)
log(f"narrows {NARROWS_MI:.1f} mi; bypass {byp_mi:.0f} direct {dir_mi:.0f} extra {extra_mi} (+{pct}%)")

# ------------------------------------------------------------------ UI rectangles (map coordinates)
UI = {
    "legend": box(24, 830, 370, 1012), "tag_n": box(572, 10, 1024, 48), "tag_s": box(486, 968, 936, 1006),
    "z1": box(1318, 0, 1536, 142), "z2": box(0, 418, 164, 522), "scale": box(80, 14, 340, 56),
}
UI_ALL = unary_union(list(UI.values()))

# ------------------------------------------------------------------ zones
def noisy_line(pts, amp, seed, step=3):
    P = catmull(pts, step=step)
    return displace(P, amp=amp, seed=seed)
z3_border = noisy_line([(430, -200), (432, 40), (448, 140), (470, 230), (492, 330), (494, 420), (506, 520), (512, 700), (512, 900)], 0.75, 31)
Z3 = north.intersection(Polygon(np.vstack([z3_border, [(-300, 900), (-300, -200)]])).buffer(0))
Z3 = max(polys_of(Z3), key=lambda x: x.area)
rest_n = north.difference(Z3)

# Tekoa Coast band along the strait shore
_ext = np.array(north.exterior.coords)
i_w = int(np.argmin(np.hypot(_ext[:, 0] - 500, _ext[:, 1] - 545))); i_e = int(np.argmin(np.hypot(_ext[:, 0] - 1115, _ext[:, 1] - 305)))
def arc(i, j):
    n = len(_ext) - 1
    k = (j - i) % n; idx = [(i + q) % n for q in range(k + 1)]
    return _ext[idx]
a1, a2 = arc(i_w, i_e), arc(i_e, i_w)[::-1]
coast_arc = a1 if LineString(a1).length < LineString(a2).length else a2
cl = LineString(coast_arc)
circ = []
for s in np.arange(0, cl.length, 8.0):
    u = s / cl.length
    r = 14 + 104 * min(1.0, (1 - u) / 0.38) ** 0.75
    p = cl.interpolate(s); circ.append(p.buffer(r, 24))
band = unary_union(circ)
Z5 = rest_n.intersection(band)
Z5 = Z5.buffer(-9, join_style=1).buffer(18, join_style=1).buffer(-9, join_style=1).intersection(rest_n)
Z5 = max(polys_of(Z5), key=lambda x: x.area)
Z4 = rest_n.difference(Z5)
Z4 = max(polys_of(Z4), key=lambda x: x.area)

# Omak zones
CAP = axis(0.70)
_E = affinity.rotate(affinity.scale(Point(0, 0).buffer(1, 48), 150, 86), ANG, origin=(0, 0))
Z11 = omak.intersection(affinity.translate(_E, *(CAP + DV * 34)))
_west = Polygon([tuple(axis(0.60) - NV * 260), tuple(axis(0.60) + NV * 260), tuple(axis(-0.3) + NV * 260), tuple(axis(-0.3) - NV * 260)])
_ncl = LineString([tuple(Ncoast(t)) for t in np.linspace(0.0, 0.62, 80)])
Z10 = omak.intersection(_ncl.buffer(64)).intersection(_west).difference(Z11)
Z10 = max(polys_of(Z10), key=lambda x: x.area)
Z12 = omak.difference(Z10).difference(Z11)
Z12 = max(polys_of(Z12), key=lambda x: x.area)

# ------------------------------------------------------------------ lakes
def lake(t, off, rx, ry, sd):
    c = axis(t) + NV * off
    return star_blob(c[0], c[1], rx, ry, sd, ROT, 0.2)
lakes = [lake(.19, -17, 28, 9, 301), lake(.31, 36, 30, 11, 302), lake(.47, -20, 24, 8, 303), lake(.60, -30, 24, 9, 304)]
for i, L in enumerate(lakes):
    if not omak.buffer(-10).contains(L): log("WARNING lake outside inset", i)
lakes_u = unary_union(lakes)

# ------------------------------------------------------------------ key places
def snap_inside(pt, geom, margin):
    p = Point(pt); g = geom.buffer(-margin)
    if g.contains(p): return np.array(pt, float)
    q = nearest_points(g, p)[0]; return np.array(q.coords[0])
LAT_CITY = snap_inside((210, 321), Z3, 12)
LAT_AB = snap_inside((250, 316), Z3, 12)
PORT = snap_inside(tuple(shore(0.44) - NV * 12), Z5, 12)
CAM_PORT = snap_inside(cam(1385, 360), camas, 9)
CAM_AB = snap_inside(cam(1298, 352), camas, 12)
HARB = Ncoast(T_H) + NV * 10
CAP_AB = snap_inside(tuple(CAP + DV * 46 + NV * 12), omak, 14)

# ------------------------------------------------------------------ roads
def smooth_line(pts, step=3.0, wob=0.0, seed=0):
    P = catmull(pts, step=step)
    if wob > 0: P = displace(P, amp=wob, seed=seed)
    return LineString(P)

ROADS = []        # (LineString, region)  region = land polygon to clip to
def add_road(ls, region, margin=6):
    ROADS.append((ls, region.buffer(-margin)))

# Latah / Tekoa
add_road(smooth_line([tuple(LAT_CITY), tuple(LAT_AB), (312, 268), (390, 226), (466, 184), (530, 130), (524, 60), (518, -10)], wob=0.12, seed=1), north)
add_road(smooth_line([(312, 268), (290, 190), (310, 110), (340, 50), (346, -10)], wob=0.12, seed=2), north)
add_road(smooth_line([(390, 226), (440, 300), (520, 380), (590, 450), (650, 500), tuple(PORT)], wob=0.1, seed=3), north)
add_road(smooth_line([tuple(LAT_AB), (252, 352), (300, 372)], wob=0.1, seed=4), north)
# Tekoa coastal road (inset coast)
_ins = north.buffer(-30)
_ring = np.array(max(polys_of(_ins), key=lambda x: x.area).exterior.coords)
_sel = _ring[(_ring[:, 0] > 560) & (_ring[:, 0] < 1010) & (_ring[:, 1] > 350)]
_order = np.argsort(_sel[:, 0]); _sel = _sel[_order]
_sel = _sel[::6]
add_road(smooth_line([tuple(p) for p in _sel], wob=0.0), north, 8)
add_road(smooth_line([(1090, -10), (1052, 80), (990, 150), (940, 220), (910, 300), (905, 380), (960, 400)], wob=0.1, seed=5), north)
add_road(smooth_line([(740, -10), (722, 90), (730, 190), (770, 280), (820, 340), (880, 380)], wob=0.1, seed=6), north)
# Camas
add_road(LineString([tuple(CAM_PORT), tuple((CAM_PORT + CAM_AB) / 2 + np.array([-6, 0])), tuple(CAM_AB)]), camas, 5)

# Omak
def ease(t, a=0.075, b=0.935, w=0.17):
    x = max(0.0, min(1.0, min((t - a) / w, (b - t) / w))); return x * x * (3 - 2 * x)
def P_N(t, off=34, bump=24):
    o = off + bump * math.exp(-((t - T_H) / 0.022) ** 2)
    return axis(t) - NV * (wprof(t) - o)
def P_S(t, off=34): return axis(t) + NV * (wprofS(t) - off)
ts = np.linspace(0.13, 0.86, 60)
add_road(LineString([tuple(P_N(t)) for t in ts]), omak, 7)
PS_LS = LineString(displace(np.array([P_S(t) for t in ts]), amp=0.45, seed=9))
add_road(PS_LS, omak, 7)
add_road(LineString(displace(np.array([axis(t) for t in np.linspace(0.06, 0.94, 60)]), amp=0.35, seed=12)), omak, 7)
TOWNS = []
CRIT = []
for k, t in enumerate([.13, .27, .52, .70, .86]):
    fs = np.linspace(0, 1, 9)
    pts = []
    for f in fs:
        _ps = np.array(PS_LS.interpolate(PS_LS.project(Point(*P_S(t)))).coords[0])
        base = P_N(t) * (1 - f) + _ps * f
        pts.append(tuple(base + DV * 7 * math.sin(2 * math.pi * f + k)))
    _l = smooth_line(pts); CRIT.append(_l); add_road(_l, omak, 7)
    TOWNS += [tuple(pts[0]), tuple(pts[-1])]
_l = LineString([tuple(HARB), tuple(P_N(T_H)), tuple(axis(T_H))]); CRIT.append(_l); add_road(_l, omak, 4)
_l = LineString([tuple(CAP), tuple(CAP_AB)]); CRIT.append(_l); add_road(_l, omak, 4)

roads = []
for ls, region in ROADS:
    g = ls.intersection(region).difference(lakes_u.buffer(3))
    for piece in flat_lines(g):
        if piece.length > 22: roads.append(piece)
road_cut = sum(ls.length for ls, _ in ROADS) - sum(r.length for r in roads)
log(f"roads: {len(roads)} pieces; length removed by clipping {road_cut:.0f}px")

# ------------------------------------------------------------------ rivers
def river(src, mouth, seed, meander=14, n=7, ext=None):
    src = np.array(src, float); mouth = np.array(mouth, float)
    d = mouth - src; L = np.linalg.norm(d); u = d / L; nrm = np.array([-u[1], u[0]])
    r = np.random.default_rng(seed)
    pts = []
    for f in np.linspace(0, 1, n):
        pts.append(src + d * f + nrm * meander * math.sin(math.pi * f) * r.uniform(-1, 1) * 1.4 + nrm * r.normal(0, meander * 0.25) * (0 < f < 1))
    if ext is not None: pts.append(mouth + np.array(ext))
    return LineString(catmull(pts, step=3))
rivers = []
def add_river(ls, region):
    g = ls.intersection(region).difference(lakes_u.buffer(1))
    for piece in flat_lines(g):
        if piece.length > 18:
            if any(piece.crosses(o) for o in rivers): continue
            rivers.append(piece)
for sd, (src, t) in enumerate([((330, 40), .10), ((250, 100), .07), ((700, 170), .34), ((900, 150), .47)]):
    mo = shore(t) - NV * 2
    add_river(river(src, mo, 40 + sd, 22, 8, tuple(-NV * 6 * -1)), north)
add_river(river((1000, 120), (1150, 300), 45, 18, 7, (10, 6)), north)
add_river(river(cam(1380, 312), cam(1400, 266), 46, 3, 4, (2, -8)), camas)
_lc = lambda k: np.array(lakes[k].centroid.coords[0])
def add_trib(main, f, side, L, seed, region):
    q = np.array(main.interpolate(f, normalized=True).coords[0])
    p0 = np.array(main.interpolate(max(f - 0.04, 0), normalized=True).coords[0]); p1 = np.array(main.interpolate(min(f + 0.04, 1), normalized=True).coords[0])
    d = p1 - p0; d /= np.linalg.norm(d) + 1e-9
    nrm = np.array([-d[1], d[0]]) * side
    src = q - d * L * 0.6 + nrm * L * 0.8
    g = river(src, q, seed, 5, 6).intersection(region).difference(lakes_u.buffer(1))
    for piece in flat_lines(g):
        if piece.length > 18: rivers.append(piece)
def omak_river(src, tm, seed, mer=13, tribs=((.45, 1), (.72, -1))):
    m = river(src, Nbase(tm) - NV * 7, seed, mer, 11)
    n0 = len(rivers); add_river(m, omak)
    if len(rivers) > n0:
        for k, (f, sd_) in enumerate(tribs): add_trib(m, f, sd_, 38, seed + 10 + k, omak)
for sd, (src, tm) in enumerate([(axis(.10) + NV * 38, .13), (_lc(1), .285), (axis(.49) + NV * 42, .52), (axis(.60) + NV * 40, .635), (axis(.74) + NV * 38, .775), (axis(.88) + NV * 26, .915)]):
    omak_river(src, tm, 60 + sd * 3)
for sd, t in enumerate([.2, .38, .58, .71, .85]):
    add_river(river(axis(t) + NV * 50, Scoast(t + .01) + NV * 6, 90 + sd, 4, 5), omak)
# Tekoa / Latah tributaries
for sd, (idx, f, side) in enumerate([(0, .5, 1), (2, .55, -1), (3, .45, 1)]):
    if idx < len(rivers): add_trib(rivers[idx], f, side, 42, 120 + sd, north)

# ------------------------------------------------------------------ icons
ICONS = [("plane", LAT_AB, 1.0), ("city", LAT_CITY, .8), ("anchor", PORT, .85), ("anchor", CAM_PORT, .85), ("plane", CAM_AB, 1.0),
         ("anchor", HARB, .85), ("star", CAP, 1.0), ("plane", CAP_AB, 1.0)]
ICONS += [("city", p, .7) for p in TOWNS]
icon_geoms = [Point(*p).buffer(13.5 * s) for _, p, s in ICONS]
icons_u = unary_union(icon_geoms)

# ------------------------------------------------------------------ labels
LABELS = []     # dicts
def label_dims(z, name, sub, ns, subs):
    wb = 8 + 7.4 * len(z)
    wn = tw(name, ns, 650, 1.6) - 1.6
    ws = (tw(sub, subs, 400, 0.3) - 0.3) if sub else 0.0
    return wb, wn, ws, wb + 8 + wn
def label_poly(cx, cy, z, name, sub, rot, ns, subs, layout="inline"):
    wb, wn, ws, w1 = label_dims(z, name, sub, ns, subs)
    if layout == "stack":
        wm = max(wb, wn, ws); top = cy - 32; bot = (cy + 13.5 + 0.3 * subs + 1) if sub else (cy + 4.5)
    else:
        wm = max(w1, ws); top = cy - 14.5; bot = (cy + 13.5 + 0.3 * subs + 1) if sub else (cy + 4.5)
    return affinity.rotate(box(cx - wm / 2 - 2.5, top, cx + wm / 2 + 2.5, bot), rot, origin=(cx, cy))
def reg_label(key, cx, cy, z, name, sub=None, rot=0.0, ns=13, subs=10.5, kind="land", halo=None, layout="inline"):
    poly = label_poly(cx, cy, z, name, sub, rot, ns, subs, layout)
    LABELS.append(dict(key=key, cx=cx, cy=cy, z=z, name=name, sub=sub, rot=rot, ns=ns, subs=subs, kind=kind, halo=halo, poly=poly, layout=layout))
    return poly
def labels_u(): return unary_union([l["poly"] for l in LABELS]) if LABELS else Polygon()

roads_u = unary_union(roads)
def pick_land(key, zone, cands, z, name, sub=None, rot=0.0, ns=13, subs=10.5, halo=None, extra_block=None, layout="inline", pref=None):
    best = None
    block = unary_union([lakes_u.buffer(3), icons_u.buffer(3), UI_ALL.buffer(4), labels_u().buffer(5)] + ([extra_block] if extra_block is not None else []))
    for c in cands:
        cx, cy = c[0], c[1]; rt = c[2] if len(c) > 2 else rot
        p = label_poly(cx, cy, z, name, sub, rt, ns, subs, layout)
        if not zone.buffer(-2).contains(p): continue
        if p.intersects(block): continue
        sc_ = roads_u.intersection(p).length + rivers_len(p)
        if pref is not None: sc_ += 0.3 * math.hypot(cx - pref[0], cy - pref[1])
        if best is None or sc_ < best[0] - 1e-6: best = (sc_, cx, cy, rt)
    if best is None:
        log("!! no clean spot for", key); cx, cy = cands[0][0], cands[0][1]; rt = rot
    else: _, cx, cy, rt = best
    log(f"label {key}: ({cx:.0f},{cy:.0f}) score={best[0] if best else -1:.0f}")
    reg_label(key, cx, cy, z, name, sub, rt, ns, subs, "land", halo, layout)

riv_u = unary_union(rivers)
def rivers_len(p): return riv_u.intersection(p).length

def grid(cx, cy, dx, dy, nx, ny, step):
    pts = [(cx + i * step, cy + j * step) for i in range(-nx, nx + 1) for j in range(-ny, ny + 1)]
    pts.sort(key=lambda q: (q[0] - cx) ** 2 + (q[1] - cy) ** 2)
    return pts

def axis_rot(t):
    d = axis(t + .012) - axis(t - .012); return math.degrees(math.atan2(d[1], d[0]))
RED, BLUE, GREY, SAND = "#d0807a", "#86a9c8", "#c1bcae", "#dcd6c0"
pick_land("Z3", Z3, grid(215, 235, 0, 0, 6, 6, 12), "Z3", "LATAH", halo=RED)
pick_land("Z4", Z4, grid(870, 230, 0, 0, 6, 6, 14), "Z4", "TEKOA HIGHLANDS", halo=GREY)
_c5 = [tuple(shore(t) - NV * o) for t in np.linspace(0.30, 0.44, 8) for o in (36, 46, 56, 68)]
pick_land("Z5", Z5, _c5, "Z5", "TEKOA COAST", rot=ANG, halo=SAND)
pick_land("Z6", camas, grid(*cam(1350, 318), 0, 0, 14, 8, 3), "Z6", "CAMAS ISLAND", ns=10.5, halo=RED, layout="stack")
_c10 = [tuple(Nbase(t) + NV * o) + (axis_rot(t),) for t in np.linspace(0.07, 0.36, 30) for o in (22, 28, 34, 40, 46)]
pick_land("Z10", Z10, _c10, "Z10", "OMAK COAST", "Fortune Harbor", halo=BLUE, extra_block=unary_union(CRIT).buffer(4), pref=tuple(Nbase(.19) + NV * 34))
_c11 = [tuple(axis(t) + NV * o) + (axis_rot(t),) for t in np.linspace(0.60, 0.90, 31) for o in (-34, -26, -18, 18, 26, 34)]
pick_land("Z11", Z11, _c11, "Z11", "OMAK CITY", "Capital", halo=BLUE, extra_block=unary_union(CRIT).buffer(4), pref=tuple(axis(.78) + NV * 26))
_c12 = [tuple(axis(t) + NV * o) + (axis_rot(t),) for t in np.linspace(0.28, 0.72, 45) for o in (-32, -24, -16, 16, 24, 32, 40, 46, 52, 58)]
pick_land("Z12", Z12, _c12, "Z12", "OMAK INTERIOR", halo=BLUE, extra_block=unary_union(CRIT).buffer(4), pref=tuple(axis(.47) + NV * 22))

# sea labels
sea_block_base = unary_union([land.buffer(9), UI_ALL.buffer(4), bypass_ls.buffer(9)])
def pick_sea(key, cands, z, name, sub=None, rot=0.0, ns=13, subs=10.5, extra=None):
    block = unary_union([sea_block_base, labels_u().buffer(5)] + ([extra] if extra is not None else []))
    for (cx, cy) in cands:
        p = label_poly(cx, cy, z, name, sub, rot, ns, subs)
        if p.intersects(block) or not MAP.buffer(-6).contains(p): continue
        log(f"label {key}: ({cx:.0f},{cy:.0f})"); reg_label(key, cx, cy, z, name, sub, rot, ns, subs, "sea"); return
    log("!! no clean sea spot for", key); cx, cy = cands[0]; reg_label(key, cx, cy, z, name, sub, rot, ns, subs, "sea")
_seaP = MAP.difference(land)
def true_mid(t):
    c = mid(t); ln = LineString([tuple(c - NV * 170), tuple(c + NV * 170)])
    best = None
    for p in flat_lines(ln.intersection(_seaP)):
        d = p.distance(Point(*c))
        if d < 40 and (best is None or d < best[0]): best = (d, p)
    if best is None: return c
    a, b = np.array(best[1].coords[0]), np.array(best[1].coords[-1]); return (a + b) / 2
STRAIT_PTS = [tuple(true_mid(t)) for t in np.linspace(0.185, 0.315, 12)]
STRAIT_LS = LineString(catmull(STRAIT_PTS, step=3))
log("strait-name path clear of land:", not STRAIT_LS.buffer(7).intersects(land), f"len {STRAIT_LS.length:.0f}px")
sea_block_base = unary_union([sea_block_base, STRAIT_LS.buffer(8)])
def loc_rot(t):
    d = mid(t + .012) - mid(t - .012); return math.degrees(math.atan2(d[1], d[0]))
_cz7 = [(tuple(mid(t) + NV * o), loc_rot(t)) for t in np.linspace(.075, .15, 31) for o in (0, -6, 6, -12, 12)]
def pick_sea_rot(key, cands, z, name, sub, ns, subs):
    block = unary_union([sea_block_base, labels_u().buffer(5)])
    for ((cx, cy), rt) in cands:
        p = label_poly(cx, cy, z, name, sub, rt, ns, subs)
        if p.intersects(block) or not MAP.buffer(-6).contains(p): continue
        log(f"label {key}: ({cx:.0f},{cy:.0f}) rot {rt:.1f}"); reg_label(key, cx, cy, z, name, sub, rt, ns, subs, "sea"); return
    log("!! no clean sea spot for", key); (cx, cy), rt = cands[0]; reg_label(key, cx, cy, z, name, sub, rt, ns, subs, "sea")
pick_sea_rot("Z7", _cz7, "Z7", "WEST APPROACH", None, 12, 10)
pick_sea("Z9", grid(1020, 612, 0, 0, 9, 9, 10), "Z9", "EAST APPROACH")
pick_sea("Z13", grid(1410, 300, 0, 0, 6, 6, 8), "Z13", "OPEN OCEAN")

# Z8 callout: label in the widening strait east of the Narrows, leader follows the channel centreline
_gm = (gn_pt + gs_pt) / 2
def z8_poly(cx, cy): return label_poly(cx, cy, "Z8", "THE NARROWS", "chokepoint, ~25 mi", ANG, 12, 10)
_blk = unary_union([sea_block_base, labels_u().buffer(5)])
Z8_POS = None
for tc in np.linspace(.43, .62, 39):
    for o in (0, -8, 8, -16, 16):
        c = mid(tc) + NV * o
        p = z8_poly(c[0], c[1])
        if p.intersects(_blk) or not MAP.buffer(-6).contains(p): continue
        tl = np.linspace(.345, tc - 0.02, 8)
        lp = [tuple(_gm)] + [tuple(mid(t) + NV * o * (t - .345) / max(tc - .345, 1e-6)) for t in tl]
        ld = LineString(lp).difference(p.buffer(1))
        if LineString(lp).intersects(land.buffer(1.5)): continue
        Z8_POS = (c[0], c[1], ld); break
    if Z8_POS: break
log("Z8 label at", Z8_POS[:2] if Z8_POS else None)
if Z8_POS: reg_label("Z8", Z8_POS[0], Z8_POS[1], "Z8", "THE NARROWS", "chokepoint, ~25 mi", ANG, 12, 10, "sea")
labels_all = labels_u()

# ------------------------------------------------------------------ islets
sea = MAP.difference(land)
rs_i = np.random.default_rng(7)
isl_cands = []
def add_isl(cx, cy, rx, ry, rr=0.0, amp=0.22):
    sd = 100 + len(isl_cands)
    if rx > 11:
        u_ = np.array([math.cos(rr), math.sin(rr)]); lobes = []
        nl = 3 if rx < 25 else 5
        for q in range(nl):
            f = (q / (nl - 1) - 0.5) * 2 * rx * 0.62
            e = 1 - abs(f) / (rx * 0.9)
            lobes.append(star_blob(cx + u_[0] * f, cy + u_[1] * f, rx * 0.42, ry * (0.6 + 0.5 * e) * np.random.default_rng(sd + q).uniform(.8, 1.2), sd + q, rr, 0.25, 48))
        g = unary_union(lobes).buffer(1.5).buffer(-1.5)
        P = np.array(max(polys_of(g), key=lambda x: x.area).exterior.coords)[:-1]
        try:
            g2 = clean(Polygon(displace(P, amp=0.09, seed=sd)))
            if g2.area > 0.5 * g.area: isl_cands.append(g2); return
        except Exception: pass
        isl_cands.append(max(polys_of(g), key=lambda x: x.area))
    else:
        isl_cands.append(star_blob(cx, cy, rx, ry, sd, rr, amp, 72))
def cluster(t, lo, hi, n, side, big=1.0):
    for _ in range(n):
        tt = float(np.clip(t + rs_i.normal(0, .028), .03, .97))
        w = wprof(tt) if side < 0 else wprofS(tt)
        c = axis(tt) + NV * side * (w + rs_i.uniform(lo, hi))
        rx = float(np.clip(rs_i.lognormal(math.log(9), 0.65), 3, 34)) * big
        add_isl(c[0], c[1], rx, rx * rs_i.uniform(.3, .65), ROT + rs_i.normal(0, .14), 0.26)
for t, n in [(.50, 6), (.60, 7), (.71, 8), (.82, 8), (.93, 6)]: cluster(t, 22, 80, n, -1)
for t, n in [(.12, 2), (.30, 3), (.47, 3), (.64, 3), (.80, 3), (.93, 2)]: cluster(t, 6, 40, n, 1, .7)
for t, w_ in [(.14, 1.0), (.27, .85), (.40, 1.1), (.54, 1.0), (.68, .9), (.80, .7)]:
    c = axis(t) + NV * (wprofS(t) + 96 + rs_i.uniform(-6, 6))
    add_isl(c[0], c[1], 40 * w_, 7.5 * w_, ROT + rs_i.normal(0, .06), 0.2)
for t in rs_i.uniform(0.05, 0.26, 5):
    c = shore(t) + NV * rs_i.uniform(12, 22); add_isl(c[0], c[1], rs_i.uniform(4, 8), rs_i.uniform(3, 5), ROT)
for t in rs_i.uniform(0.39, 0.5, 5):
    c = shore(t) + NV * rs_i.uniform(12, 24); add_isl(c[0], c[1], rs_i.uniform(3, 6), rs_i.uniform(2.5, 4), ROT)
for (cx, cy, rx, ry, rr) in [(1215, 330, 13, 6, 1.2), (1240, 372, 6, 4, .5), (1228, 288, 5, 3, 0), (1475, 300, 13, 6, .3), (1500, 360, 6, 4, 0), (1480, 420, 8, 4, .6),
                             (1255, 440, 5, 3, 0), (1330, 450, 6, 3, .2), (1450, 252, 5, 3, 0), (1517, 482, 6, 4, 0)]:
    add_isl(*cam(cx, cy), rx, ry, rr)      # Camas's islets move with it
for (cx, cy, rx, ry, rr) in [(60, 405, 7, 4, 0), (255, 412, 6, 4, 0)]:
    add_isl(cx, cy, rx, ry, rr)
# sea-zone divider lines (computed first so islets keep clear of them)
def divider_line(t):
    p1 = shore(t) - NV * 24; p2 = Nbase(t) + NV * 60
    return LineString([tuple(p1), tuple(p2)])
dividers_raw = [divider_line(0.06), divider_line(0.27), divider_line(0.375), LineString([(1292, 332 + CAM_D[1] + 30), (1292, 900)])]
div_u = unary_union(dividers_raw)
keep_block = unary_union([land.buffer(8), UI_ALL.buffer(8), bypass_ls.buffer(12), labels_all.buffer(6), div_u.buffer(8)] + ([Z8_POS[2].buffer(10)] if Z8_POS else []))
islets = []
for p in isl_cands:
    if p.intersects(keep_block): continue
    if any(p.buffer(4).intersects(q) for q in islets): continue
    if not MAP.buffer(-8).contains(p): continue
    islets.append(p)
log("islets kept", len(islets), "of", len(isl_cands))
islets_u = unary_union(islets) if islets else Polygon()
land_all = unary_union([land, islets_u])

# ------------------------------------------------------------------ decorative linework
cutters = unary_union([labels_all.buffer(3), icons_u.buffer(3), UI_ALL.buffer(2)])
sea_poly = MAP.difference(land_all.buffer(1.5))
dividers = []
for dl in dividers_raw:
    for piece in flat_lines(dl.intersection(sea_poly).difference(labels_all.buffer(4)).difference(UI_ALL.buffer(2)).difference(STRAIT_LS.buffer(9)).difference(Z8_POS[2].buffer(4) if Z8_POS else Polygon())):
        if piece.length > 22: dividers.append(piece)

# Contours in the Tekoa Highlands (nested, merged across peaks)
contours = []
peaks = [(700, 140, 1.1, .25), (960, 170, 1.05, .1), (780, 300, 0.8, -.2)]
z4_in = Z4.buffer(-8)
for lvl in (1.0, 0.68, 0.38):
    shapes = []
    for k, (cx, cy, r, rr) in enumerate(peaks):
        b = star_blob(cx, cy, 120 * r * lvl, 82 * r * lvl, 500 + k, rr, 0.16)
        shapes.append(b)
    u = unary_union(shapes)
    for ls in flat_lines(u.boundary):
        g = ls.intersection(z4_in).difference(cutters)
        for piece in flat_lines(g):
            if piece.length > 25: contours.append(piece)

SPOT = []
_cl = []
ridge = []
for k, t in enumerate(np.linspace(.07, .93, 15)):
    c = axis(t) + NV * (31 + 7 * math.sin(2.3 * k)); sz = math.sin(math.pi * t) ** .5 * (0.75 + .4 * abs(math.sin(1.7 * k + .4)))
    ridge.append((c, sz, k))
o_in = omak.buffer(-8).difference(lakes_u.buffer(2))
for lvl in (1.0, .76, .52, .28):
    u = unary_union([star_blob(c[0], c[1], 66 * sz * lvl, 19 * sz * lvl, 700 + k, ROT, .18) for c, sz, k in ridge])
    for ls in flat_lines(u.boundary):
        for piece in flat_lines(ls.intersection(o_in).difference(cutters)):
            if piece.length > 25: contours.append(piece)
_pk = [(700, 140, "4,310"), (960, 170, "3,980"), (780, 300, "3,120")]
for k in (2, 5, 8, 11, 13):
    c, sz, _ = ridge[k]; _pk.append((c[0], c[1], f"{int(5200 + 900 * math.sin(k) + 400 * sz):,}"))
SPOT_RAW = _pk

# Zone boundaries (dashed) on land
inner_n = north.buffer(-1.6)
zb_lines = []
def add_zb(poly, inner, exclude=None):
    g = poly.boundary.intersection(inner)
    if exclude is not None: g = g.difference(exclude)
    g = g.difference(cutters)
    for piece in flat_lines(g):
        if piece.length > 25: zb_lines.append(piece)
add_zb(Z3, inner_n)
add_zb(Z5, inner_n, exclude=Z3.buffer(1.0))
inner_o = omak.buffer(-1.6)
add_zb(Z11, inner_o)
add_zb(Z10, inner_o, exclude=Z11.buffer(1.0))

# ------------------------------------------------------------------ cut roads/rivers around labels
def cut_lines(lines, cut):
    out = []
    for ls in lines:
        for piece in flat_lines(ls.difference(cut)):
            if piece.length > 30: out.append(piece)
    return out
labels_cut = unary_union([labels_all.buffer(2.5), UI_ALL.buffer(1)])
roads_f = cut_lines(roads, labels_cut)
rivers_f = cut_lines(rivers, labels_cut)

_blk = unary_union([labels_all.buffer(5), unary_union(roads_f).buffer(2.5), unary_union(rivers_f).buffer(2), icons_u.buffer(4), lakes_u.buffer(3), UI_ALL.buffer(3)])
for (x, y, txt) in SPOT_RAW:
    bx = box(x - 5, y - 6, x + 8 + 5 * len(txt), y + 5)
    if not bx.intersects(_blk) and land.buffer(-4).contains(bx): SPOT.append((x, y, txt))
log("spot heights", len(SPOT), "of", len(SPOT_RAW))
SOUND = []
_rs = np.random.default_rng(11)
_sea2 = MAP.buffer(-14).difference(land_all.buffer(7)).difference(UI_ALL.buffer(6)).difference(labels_all.buffer(8)).difference(bypass_ls.buffer(9)).difference(div_u.buffer(7)).difference(STRAIT_LS.buffer(11))
if Z8_POS: _sea2 = _sea2.difference(Z8_POS[2].buffer(8))
for _ in range(6000):
    p = Point(_rs.uniform(10, W0 - 10), _rs.uniform(10, H0 - 10))
    if not _sea2.contains(p.buffer(9)): continue
    d = land_all.distance(p)
    if d > 52 or d < 12: continue
    if any(math.hypot(p.x - q[0], p.y - q[1]) < 34 for q in SOUND): continue
    SOUND.append((p.x, p.y, str(int(3 + d * 0.5 * _rs.uniform(.7, 1.4)))))
    if len(SOUND) >= 58: break
log("soundings", len(SOUND))
urban = star_blob(CAP[0], CAP[1], 27, 18, 77, ROT, 0.22)
urban = urban.intersection(omak.buffer(-4))
# ------------------------------------------------------------------ QA
def qa():
    ok = True
    for nm, g in [("north", north), ("omak", omak), ("camas", camas)]:
        if not g.is_valid: log("INVALID", nm); ok = False
    allr = unary_union([LineString(r) if not hasattr(r, 'coords') else r for r in roads_f])
    outside = sum(r.difference(land.buffer(0.5)).length for r in roads_f)
    log(f"QA roads outside land: {outside:.2f}px")
    outside_r = sum(r.difference(land.buffer(0.5)).length for r in rivers_f)
    log(f"QA rivers outside land: {outside_r:.2f}px")
    # parallel overlaps between different road pieces
    n_ov = 0
    for i in range(len(roads_f)):
        for j in range(i + 1, len(roads_f)):
            a, b = roads_f[i], roads_f[j]
            if not a.buffer(2.2).intersects(b): continue
            ov = a.buffer(2.2).intersection(b).length
            if ov > 14: n_ov += 1; log(f"  road overlap {i}-{j}: {ov:.0f}px")
    log("QA overlapping road pairs:", n_ov)
    log("QA islet/land overlaps:", sum(1 for p in islets if p.intersects(land)))
    log("QA islet/islet overlaps:", sum(1 for i in range(len(islets)) for j in range(i + 1, len(islets)) if islets[i].intersects(islets[j])))
    log("QA islet vs route:", sum(1 for p in islets if p.intersects(bypass_ls.buffer(4))))
    log("QA route vs land/UI:", bypass_ls.buffer(4).intersects(land), bypass_ls.buffer(2).intersects(UI_ALL))
    ll = [l["poly"] for l in LABELS]
    log("QA label/label overlaps:", sum(1 for i in range(len(ll)) for j in range(i + 1, len(ll)) if ll[i].intersects(ll[j])))
    for l in LABELS:
        if l["kind"] == "sea":
            if l["poly"].intersects(land_all): log("  sea label hits land/islet:", l["key"])
        else:
            if not land.contains(l["poly"]): log("  land label leaves land:", l["key"])
            if l["poly"].intersects(lakes_u): log("  land label over lake:", l["key"])
    log("QA icons on land:", all(land.buffer(-3).intersects(Point(*p)) for _, p, _ in ICONS))
    log("QA icon overlaps labels:", sum(1 for l in LABELS if l["poly"].intersects(icons_u)))
    log("QA lakes vs roads:", sum(lakes_u.intersection(r).length for r in roads_f))
    log("QA Z2 box vs land:", UI["z2"].intersects(land.buffer(2)), "| Z1 box vs land:", UI["z1"].intersects(land.buffer(2)))
qa()

# ============================================================ RENDER (flat, utilitarian)
OW, OH, MG = 1580, 1140, 22
SEA, SH1, SH2, ISO = "#b3cad6", "#c8dae3", "#dae6eb", "#8aa8b9"
PAPER = "#fbfaf4"
TR, TB, TG, TS = "#eed9d3", "#d6dee8", "#e0e7d4", "#f0ebd9"   # topo tints for REDFOR / BLUEFOR / Tekoa / coast
TINT = {RED: TR, BLUE: TB, GREY: TG, SAND: TS}
BRN, WATER, PURP = "#a98462", "#5588b0", "#85567f"
ROUTE = "#d9672a"
SEAC = "#2f6486"
FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"

out = []
A = out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{OW}" height="{OH}" viewBox="0 0 {OW} {OH}" font-family="{FONT}">')
A('<title>Strait of Great Fortune - topographic map</title>')
A(f'<rect width="{OW}" height="{OH}" fill="{PAPER}"/>')

land_all_d = poly_d(land_all)
north_d, omak_d, camas_d = poly_d(north), poly_d(omak), poly_d(camas)

# strait name path
def pts_d(P, close=False): return path_d(np.array(P), close)
A(f'''<defs>
<clipPath id="mapclip"><rect x="0" y="0" width="{W0}" height="{H0}"/></clipPath>
<path id="straitpath" d="{pts_d(STRAIT_LS.coords)}"/>
<symbol id="i-star" viewBox="-14 -14 28 28" overflow="visible"><circle r="11" fill="{INK}" stroke="#fff" stroke-width="1.4"/><polygon fill="#fff" points="0,-7 2,-2.3 7,-2.2 3.1,1 4.5,6 0,3.2 -4.5,6 -3.1,1 -7,-2.2 -2,-2.3"/></symbol>
<symbol id="i-anchor" viewBox="-14 -14 28 28" overflow="visible"><circle r="11" fill="{INK}" stroke="#fff" stroke-width="1.4"/><g fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="0" cy="-5.6" r="1.7"/><path d="M0,-3.9 V6.6 M-3.2,-1.2 H3.2 M-6,1.8 Q-5.5,6.7 0,6.9 Q5.5,6.7 6,1.8"/></g></symbol>
<symbol id="i-plane" viewBox="-14 -14 28 28" overflow="visible"><path d="M0,-11 L1.9,-7 L1.9,-2.6 L11,2.8 L11,5.6 L1.9,3 L1.9,7.4 L4.7,9.2 L4.7,11 L0,10 L-4.7,11 L-4.7,9.2 L-1.9,7.4 L-1.9,3 L-11,5.6 L-11,2.8 L-1.9,-2.6 L-1.9,-7 Z" fill="{INK}" stroke="#fff" stroke-width="1.6" stroke-linejoin="round" paint-order="stroke"/></symbol>
<symbol id="i-city" viewBox="-14 -14 28 28" overflow="visible"><circle r="6.5" fill="#fff" stroke="{INK}" stroke-width="2"/></symbol>
</defs>''')

A(f'<g transform="translate({MG},{MG})"><g clip-path="url(#mapclip)">')

# ---- sea + flat bathymetric steps
A(f'<rect width="{W0}" height="{H0}" fill="{SEA}"/>')
A('<g fill="none" stroke-linejoin="round">')
_ld = poly_d(land); _id = poly_d(islets_u)
A(f'<path d="{_ld}" stroke="{ISO}" stroke-width="84" opacity=".55"/><path d="{_ld}" stroke="{SH1}" stroke-width="83"/>')
A(f'<path d="{_id}" stroke="{ISO}" stroke-width="22" opacity=".5"/><path d="{_id}" stroke="{SH1}" stroke-width="21"/>')
A(f'<path d="{_ld}" stroke="{ISO}" stroke-width="36" opacity=".55"/><path d="{_ld}" stroke="{SH2}" stroke-width="35"/>')
A(f'<path d="{_id}" stroke="{SH2}" stroke-width="12"/>')
A('</g>')

A(f'<g font-size="7.5" font-style="italic" fill="{SEAC}" text-anchor="middle" opacity=".8">')
for (x, y, tx_) in []: A(f'<text x="{x:.1f}" y="{y+2.5:.1f}">{tx_}</text>')
A('</g>')
# ---- sea-zone dividers
for ls in dividers:
    A(f'<path d="{pts_d(ls.coords)}" fill="none" stroke="{PURP}" stroke-width="1.2" stroke-dasharray="7 2.5 1.5 2.5" opacity=".9"/>')

# ---- land fills (zones are exact polygons, no overlap seams)
A(f'<path d="{land_all_d}" fill="{PAPER}"/>')
A(f'<path d="{north_d}" fill="{TG}"/>')
A(f'<path d="{poly_d(Z3)}" fill="{TR}"/><path d="{poly_d(Z5)}" fill="{TS}"/>')
A(f'<path d="{omak_d}" fill="{TB}"/><path d="{camas_d}" fill="{TR}"/>')
_zones = [(Z3, RED), (Z4, GREY), (Z5, SAND), (omak, BLUE), (camas, RED)]
for p in islets:
    c = Point(*p.centroid.coords[0])
    col = TINT[min(_zones, key=lambda zc: zc[0].distance(c))[1]]
    A(f'<path d="{poly_d(p)}" fill="{col}"/>')

# ---- grid (under all land linework)
A(f'<g stroke="{INK}" stroke-width=".7" opacity=".55">')
for i in range(1, 15):
    for j in range(1, 10):
        x, y = 105*i, 105*j
        A(f'<path d="M{x-5},{y} H{x+5} M{x},{y-5} V{y+5}"/>')
for k in range(1, 15): A(f'<path d="M{105*k},0 v8 M{105*k},{H0} v-8"/>')
for k in range(1, 10): A(f'<path d="M0,{105*k} h8 M{W0},{105*k} h-8"/>')
A('</g>')

# ---- terrain
A(f'<g fill="none" stroke="{BRN}" stroke-linejoin="round" stroke-linecap="round">')
for i, ls in enumerate(contours):
    A(f'<path d="{pts_d(ls.coords)}" stroke-width="{1.1 if i % 5 == 0 else .6}" opacity="{.95 if i % 5 == 0 else .8}"/>')
A('</g>')
A(f'<path d="{poly_d(urban)}" fill="#d8d0c0" stroke="#a89d88" stroke-width=".6"/>')
for Lk in lakes: A(f'<path d="{poly_d(Lk)}" fill="{SH1}" stroke="{WATER}" stroke-width=".9"/>')

# ---- zone boundaries
A(f'<g fill="none" stroke="{PURP}" stroke-width="1.3" stroke-dasharray="7 2.5 1.5 2.5" opacity=".95" stroke-linejoin="round">')
for ls in zb_lines: A(f'<path d="{pts_d(ls.coords)}"/>')
A('</g>')

# ---- rivers
A(f'<g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.1" stroke="{WATER}">')
for ls in rivers_f:
    A(f'<path d="{pts_d(ls.coords)}"/>')
A('</g>')

# ---- roads (white casing gives clean bridges over rivers)
A('<g fill="none" stroke-linecap="round" stroke-linejoin="round">')
_sref = PS_LS.buffer(6)
_prim = [ls for ls in roads_f if ls.length > 260 and not ls.within(_sref)]; _sec = [ls for ls in roads_f if not (ls.length > 260 and not ls.within(_sref))]
log("roads primary/secondary", len(_prim), len(_sec))
for ls in _sec: A(f'<path d="{pts_d(ls.coords)}" stroke="{INK}" stroke-width="2.3"/>')
for ls in _prim: A(f'<path d="{pts_d(ls.coords)}" stroke="{INK}" stroke-width="2.7"/>')
for ls in _sec: A(f'<path d="{pts_d(ls.coords)}" stroke="#fffdf0" stroke-width="1.15"/>')
for ls in _prim: A(f'<path d="{pts_d(ls.coords)}" stroke="#cf6a58" stroke-width="1.6"/>')
A('</g>')

A(f'<g font-size="8" fill="{BRN}" text-anchor="start">')
for (x, y, tx_) in SPOT:
    A(f'<path d="M{x-3.2:.1f},{y+2.6:.1f} L{x+3.2:.1f},{y+2.6:.1f} L{x:.1f},{y-3.4:.1f} Z" fill="{BRN}"/><text x="{x+5.5:.1f}" y="{y+3:.1f}" stroke="{PAPER}" stroke-width="2.2" paint-order="stroke" font-weight="600">{tx_}</text>')
A('</g>')
# ---- coastlines
A(f'<path d="{land_all_d}" fill="none" stroke="#3d5a70" stroke-width="1" stroke-linejoin="round"/>')

# ---- bypass route
_bd = pts_d(bypass)
A(f'<path d="{_bd}" fill="none" stroke="{ROUTE}" stroke-width="2.2" stroke-dasharray="9 6" stroke-linecap="round"/>')
_a, _b = bypass[-1], bypass[-6]
_dir = (_a - _b) / np.linalg.norm(_a - _b); _perp = np.array([-_dir[1], _dir[0]])
_tip = _a + _dir * 6; _l = _a - _dir * 9 + _perp * 6; _r = _a - _dir * 9 - _perp * 6
A(f'<polygon points="{_tip[0]:.1f},{_tip[1]:.1f} {_l[0]:.1f},{_l[1]:.1f} {_r[0]:.1f},{_r[1]:.1f}" fill="{ROUTE}"/>')
A(f'<circle cx="{bypass[0][0]:.1f}" cy="{bypass[0][1]:.1f}" r="4" fill="#fff" stroke="{ROUTE}" stroke-width="2"/>')

# ---- Narrows bracket + leader
A(f'<g stroke="{INK}" stroke-linecap="round" fill="none"><line x1="{gn_pt[0]:.1f}" y1="{gn_pt[1]:.1f}" x2="{gs_pt[0]:.1f}" y2="{gs_pt[1]:.1f}" stroke-width="1.6"/>'
  f'<line x1="{gn_pt[0]-6*DV[0]:.1f}" y1="{gn_pt[1]-6*DV[1]:.1f}" x2="{gn_pt[0]+6*DV[0]:.1f}" y2="{gn_pt[1]+6*DV[1]:.1f}" stroke-width="1.1"/>'
  f'<line x1="{gs_pt[0]-6*DV[0]:.1f}" y1="{gs_pt[1]-6*DV[1]:.1f}" x2="{gs_pt[0]+6*DV[0]:.1f}" y2="{gs_pt[1]+6*DV[1]:.1f}" stroke-width="1.1"/></g>')
if Z8_POS:
    for ls in flat_lines(Z8_POS[2]):
        A(f'<path d="{pts_d(ls.coords)}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="2 3" stroke-linecap="round"/>')

# ---- strait name along the channel
_txt = "STRAIT OF GREAT FORTUNE"
_ls = max(0.8, min(3.0, (STRAIT_LS.length * 0.86 - tw(_txt, 9.5, 400)) / len(_txt)))
A(f'<text font-size="9.5" font-style="italic" fill="{SEAC}" letter-spacing="{_ls:.2f}" dy="3"><textPath xlink:href="#straitpath" href="#straitpath" startOffset="50%" text-anchor="middle">{_txt}</textPath></text>')

# ---- icons
def icon(kind, p, s=1.0):
    A(f'<use xlink:href="#i-{kind}" x="{p[0]-14*s:.1f}" y="{p[1]-14*s:.1f}" width="{28*s}" height="{28*s}"/>')
for kind, p, sc_ in ICONS: icon(kind, p, sc_)

# ---- labels
def draw_label(l):
    cx, cy, z, name, sub, rot_, ns, subs = l["cx"], l["cy"], l["z"], l["name"], l["sub"], l["rot"], l["ns"], l["subs"]
    sea = l["kind"] == "sea"
    wb, wn, ws, w1 = label_dims(z, name, sub, ns, subs)
    bfill, bstroke, btext = ("#fff", INK, INK) if sea else (INK, INK, "#fff")
    col = SEAC if sea else INK
    it = ' font-style="italic"' if sea else ''
    halo = "" if (sea or not l.get("halo")) else f' stroke="{TINT[l["halo"]]}" stroke-width="3" stroke-linejoin="round" paint-order="stroke"'
    A(f'<g transform="rotate({rot_:.2f} {cx:.1f} {cy:.1f})">')
    if l["layout"] == "stack":
        A(f'<rect x="{cx-wb/2:.1f}" y="{cy-31:.1f}" width="{wb:.1f}" height="16" rx="2" fill="{bfill}" stroke="{bstroke}" stroke-width="1"/>')
        A(f'<text x="{cx:.1f}" y="{cy-19.2:.1f}" font-size="11" font-weight="700" text-anchor="middle" fill="{btext}" letter-spacing=".5">{z}</text>')
        A(f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="{ns}" font-weight="650" text-anchor="middle" fill="{col}" letter-spacing="1.6"{halo}{it}>{name}</text>')
    else:
        x0 = cx - w1 / 2
        A(f'<rect x="{x0:.1f}" y="{cy-13:.1f}" width="{wb:.1f}" height="16" rx="2" fill="{bfill}" stroke="{bstroke}" stroke-width="1"/>')
        A(f'<text x="{x0+wb/2:.1f}" y="{cy-1.2:.1f}" font-size="11" font-weight="700" text-anchor="middle" fill="{btext}" letter-spacing=".5">{z}</text>')
        A(f'<text x="{x0+wb+8:.1f}" y="{cy:.1f}" font-size="{ns}" font-weight="650" fill="{col}" letter-spacing="1.6"{halo}{it}>{name}</text>')
    if sub:
        A(f'<text x="{cx:.1f}" y="{cy+13.5:.1f}" font-size="{subs}" text-anchor="middle" fill="{col}" letter-spacing=".3"{halo}{it}>{sub}</text>')
    A('</g>')
for l in LABELS: draw_label(l)

# ---- off-map tiles
A(f'<rect x="1318" y="0" width="218" height="142" fill="{TR}" stroke="{INK}" stroke-width="1"/>')
A(f'<g text-anchor="middle"><rect x="1411" y="26" width="34" height="16" rx="2" fill="{INK}"/><text x="1428" y="38" font-size="11" font-weight="700" fill="#fff">Z1</text>'
  f'<text x="1428" y="70" font-size="15" font-weight="650" fill="{INK}" letter-spacing="1.6">COSMOPOLIS</text>'
  f'<text x="1428" y="90" font-size="11" fill="{INK}">off-map, ~8,000 mi</text>'
  f'<text x="1428" y="112" font-size="9.5" fill="{INK}" letter-spacing=".8">BOMBERS · AIRLIFT · SPACE · CYBER</text></g>')
A(f'<path d="M1496,56 L1514,38 M1502,38 H1514 V50" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
zy = 418
A(f'<rect x="0" y="{zy}" width="164" height="104" fill="{TB}" stroke="{INK}" stroke-width="1"/>')
A(f'<g text-anchor="middle"><rect x="92" y="{zy+14}" width="34" height="16" rx="2" fill="{INK}"/><text x="109" y="{zy+26}" font-size="11" font-weight="700" fill="#fff">Z2</text>'
  f'<text x="100" y="{zy+56}" font-size="15" font-weight="650" fill="{INK}" letter-spacing="1.6">ASOTIN</text>'
  f'<text x="100" y="{zy+75}" font-size="11" fill="{INK}">off-map, ~1,200 mi</text>'
  f'<text x="100" y="{zy+92}" font-size="9.5" fill="{INK}" letter-spacing=".8">SUPPORT TO BLUEFOR</text></g>')
A(f'<path d="M30,{zy+38} L12,{zy+50} L30,{zy+62} M12,{zy+50} H34" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')

# ---- Z13 arrow (to the right of the Z13 label)
_z13 = next(l for l in LABELS if l["key"] == "Z13")
_ax, _ay = _z13["poly"].bounds[2] + 6, _z13["cy"] - 5
A(f'<path d="M{_ax:.0f},{_ay:.0f} H{_ax+28:.0f} M{_ax+18:.0f},{_ay-8:.0f} L{_ax+28:.0f},{_ay:.0f} L{_ax+18:.0f},{_ay+8:.0f}" fill="none" stroke="{SEAC}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')

# ---- callout tags
def tag(x, y, w, l1, l2, kind):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="38" rx="2" fill="#fff" stroke="{INK}" stroke-width="1"/>')
    if kind == "up":
        A(f'<path d="M{x+16},{y+27} V{y+11} M{x+9},{y+17} L{x+16},{y+9} L{x+23},{y+17}" fill="none" stroke="{ROUTE}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        A(f'<line x1="{x+8}" y1="{y+19}" x2="{x+26}" y2="{y+19}" stroke="{ROUTE}" stroke-width="2.4" stroke-dasharray="6 4" stroke-linecap="round"/>')
    A(f'<text x="{x+38}" y="{y+16}" font-size="10" font-weight="700" fill="{INK}" letter-spacing="1">{l1}</text>'
      f'<text x="{x+38}" y="{y+30}" font-size="11" fill="{INK}">{l2}</text>')
tag(572, 10, 452, "LANDMASS CONTINUES OFF-MAP", "Northern bypass around Latah-Tekoa: about +4,600 mi (~11 days)", "up")
tag(486, 968, 450, "SOUTHERN BYPASS AROUND OMAK", f"about +{extra_mi:,} mi (+{pct}%, ~{days} day{'s' if days != 1 else ''} at 15 kt) vs. the strait", "route")

# ---- north arrow + scale bar
A(f'<g><path d="M43,28 L52,56 L43,50 L34,56 Z" fill="{INK}"/><text x="43" y="22" font-size="11" font-weight="700" text-anchor="middle" fill="{INK}">N</text></g>')
A(f'<g font-size="10" fill="{INK}" font-weight="600"><rect x="88" y="40" width="52.5" height="6" fill="{INK}"/><rect x="140.5" y="40" width="52.5" height="6" fill="#fff" stroke="{INK}" stroke-width="1"/><rect x="193" y="40" width="105" height="6" fill="{INK}"/>'
  f'<text x="88" y="34" text-anchor="middle">0</text><text x="140.5" y="34" text-anchor="middle">50</text><text x="193" y="34" text-anchor="middle">100</text><text x="298" y="34" text-anchor="middle">200 mi</text></g>')

# ---- legend
LX, LY, LW, LH = 24, 830, 346, 182
A(f'<rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" fill="#fff" stroke="{INK}" stroke-width="1"/>')
A(f'<text x="{LX+14}" y="{LY+22}" font-size="10" font-weight="700" letter-spacing="1.6" fill="{INK}">LEGEND</text><line x1="{LX+14}" y1="{LY+30}" x2="{LX+LW-14}" y2="{LY+30}" stroke="{INK}" stroke-width=".8"/>')
for k, (col, tx) in enumerate([(TR, "REDFOR (Cosmopolis-aligned)"), (TB, "BLUEFOR (Omak)"), (TG, "Neutral / other (Tekoa)")]):
    yy = LY + 44 + k * 24
    A(f'<rect x="{LX+14}" y="{yy}" width="16" height="14" fill="{col}" stroke="{INK}" stroke-width=".8"/><text x="{LX+38}" y="{yy+11}" font-size="10.5" fill="{INK}">{tx}</text>')
yy = LY + 44 + 3 * 24
A(f'<line x1="{LX+12}" y1="{yy+7}" x2="{LX+32}" y2="{yy+7}" stroke="{ROUTE}" stroke-width="2.2" stroke-dasharray="6 4"/><text x="{LX+38}" y="{yy+11}" font-size="10.5" fill="{INK}">Bypass route (off the strait)</text>')
A(f'<path d="M{LX+12},{yy+27} Q{LX+22},{yy+21} {LX+32},{yy+27}" fill="none" stroke="{BRN}" stroke-width="1"/><text x="{LX+38}" y="{yy+31}" font-size="10.5" fill="{INK}">Contour / spot height</text>')
A(f'<rect x="{LX+14}" y="{yy+38}" width="16" height="11" fill="#d8d0c0" stroke="#a89d88" stroke-width=".8"/><text x="{LX+38}" y="{yy+47}" font-size="10.5" fill="{INK}">Built-up area</text>')
RX = LX + 196
rows = [("star", "Capital"), ("plane", "Air base"), ("anchor", "Naval base / port")]
for k, (ic, tx) in enumerate(rows):
    yy = LY + 46 + k * 21
    A(f'<use xlink:href="#i-{ic}" x="{RX-1}" y="{yy-12}" width="22" height="22"/><text x="{RX+28}" y="{yy+3}" font-size="10.5" fill="{INK}">{tx}</text>')
yb = LY + 46 + 3 * 21 + 6
A(f'<path d="M{RX},{yb+4} Q{RX+10},{yb-2} {RX+20},{yb+4}" fill="none" stroke="{INK}" stroke-width="2.7"/><path d="M{RX},{yb+4} Q{RX+10},{yb-2} {RX+20},{yb+4}" fill="none" stroke="#cf6a58" stroke-width="1.6"/><text x="{RX+28}" y="{yb+5}" font-size="10.5" fill="{INK}">Primary road</text>')
yb += 18
A(f'<path d="M{RX},{yb+4} Q{RX+10},{yb-2} {RX+20},{yb+4}" fill="none" stroke="{INK}" stroke-width="2.3"/><path d="M{RX},{yb+4} Q{RX+10},{yb-2} {RX+20},{yb+4}" fill="none" stroke="#fffdf0" stroke-width="1.15"/><text x="{RX+28}" y="{yb+5}" font-size="10.5" fill="{INK}">Secondary road</text>')
yb += 18
A(f'<path d="M{RX},{yb+4} Q{RX+10},{yb-2} {RX+20},{yb+4}" fill="none" stroke="{WATER}" stroke-width="1.2"/><text x="{RX+28}" y="{yb+5}" font-size="10.5" fill="{INK}">River</text>')
yb += 18
A(f'<line x1="{RX}" y1="{yb+2}" x2="{RX+20}" y2="{yb+2}" stroke="{PURP}" stroke-width="1.3" stroke-dasharray="7 2.5 1.5 2.5"/><text x="{RX+28}" y="{yb+5}" font-size="10.5" fill="{INK}">Zone boundary</text>')

A('</g>')  # end clip
A(f'<rect x="0" y="0" width="{W0}" height="{H0}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
A('</g>')
A(f'<g font-size="9" font-weight="600" fill="{INK}" text-anchor="middle" letter-spacing=".5">')
for k in range(15):
    x = MG + 105 * k + 52
    A(f'<text x="{x}" y="{MG-8}">{chr(65+k)}</text><text x="{x}" y="{MG+H0+16}">{chr(65+k)}</text>')
for k in range(10):
    y = MG + 105 * k + 56
    A(f'<text x="{MG-11}" y="{y}">{k+1}</text><text x="{MG+W0+11}" y="{y}">{k+1}</text>')
A('</g>')
# collar (USGS-style marginalia)
cy0 = MG + H0 + 30
A(f'<line x1="{MG}" y1="{cy0}" x2="{MG+W0}" y2="{cy0}" stroke="{INK}" stroke-width=".6"/>')
A(f'<g fill="{INK}"><text x="{MG}" y="{cy0+30}" font-size="19" font-weight="700" letter-spacing="2.5">STRAIT OF GREAT FORTUNE</text>'
  f'<text x="{MG}" y="{cy0+48}" font-size="10.5" letter-spacing="1.2">THEATER MAP  \u00b7  ZONES Z1\u2013Z13  \u00b7  OMAK / TEKOA / LATAH</text>'
  f'<text x="{MG+560}" y="{cy0+22}" font-size="10" font-weight="700" letter-spacing="1">SCALE</text>'
  f'<text x="{MG+560}" y="{cy0+37}" font-size="10">One grid square = 100 statute miles</text>'
  f'<text x="{MG+560}" y="{cy0+51}" font-size="10">Bypass distances at 15 kt, strait = 25 mi</text>'
  f'<text x="{MG+940}" y="{cy0+22}" font-size="10" font-weight="700" letter-spacing="1">CONTOUR INTERVAL</text>'
  f'<text x="{MG+940}" y="{cy0+37}" font-size="10">Fictional elevations, interval 500 ft</text>'
  f'<text x="{MG+940}" y="{cy0+51}" font-size="10">Shaded bands show approximate shelf</text>'
  f'<text x="{MG+W0}" y="{cy0+22}" font-size="10" font-weight="700" letter-spacing="1" text-anchor="end">ADJOINING ZONES</text>'
  f'<text x="{MG+W0}" y="{cy0+37}" font-size="10" text-anchor="end">Z1 Cosmopolis NE  \u00b7  Z2 Asotin W</text>'
  f'<text x="{MG+W0}" y="{cy0+51}" font-size="10" text-anchor="end">Z13 Open Ocean E</text></g>')
A(f'<rect x="5" y="5" width="{OW-10}" height="{OH-10}" fill="none" stroke="{INK}" stroke-width=".8"/>')
A('</svg>')
open(sys.argv[1], "w").write("\n".join(out))
log("written", sys.argv[1], f"({sum(len(x) for x in out)//1024} KB)")
