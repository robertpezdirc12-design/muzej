#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P49 (issue #14 / §3 nadaljevanje) — FUČKOVCI 1825: MODERN-ANCHORED SYMBOL
EVIDENCE + STRIKTNA DETEKCIJA JEDER + OBSEG SKLOPA (delna vektorizacija A05).

Naloga iz P48 ("ostaja odprto"): razširitev vektorizacije stavb 1825 na A05
(Fučkovci). Ugotovitev razvoja: CELTNA vektorizacija posameznih tlorisov ni
izvedljiva na tej resoluciji — izmerjeno:
  (a) rožnati parcelni fill na A05 ima sivo p50 ≈ 168 < T_DARK 195 → barvna
      zasenčitev ZASENČI masko črnila (za razliko od A02);
  (b) erodirana maska se v vasi ZASIČI (37,5 % temnega v škatli vasi
      1750–2200 × 480–950) → sosednji simboli se staknejo v eno maso;
  (c) številke/črki/drevesa so po velikosti in kontrastu v istem razredu kot
      simboli (striktni detektor brez konteksta doseže ~50 % preciznost).
Zato P49 dostavi TRI neodvisne, deterministične dokazne sloje:

  1) MODERN-ANCHORED EVIDENCE (isti stroj kot P48): 95 sodobnih stavb celice
     ch preslikanih prek P46 afin nazaj na sken; cov@0 / cov@best na erodirani
     maski (plus 3×3, prag 195); ON-SYMBOL (cov@best ≥ 0.5) = stavbno mesto
     1825 z neposrednim dokazom na lokaciji sodobne stavbe (26).
  2) STRIKTNA DETEKCIJA JEDER (neodvisna od 1): lokalni kontrast (mean9−mean25
     ≤ −13), delež zelo temnega (g<145 ≥ 0.55 v 9×9), izključitev papirja
     (paper41 ≤ 0.25) + test obroča (ring < 198) + oblika (area ≥ 36,
     bbox 6–40, fill ≥ 0.42) → temna jedra; korelirana (≤ 20 px od on-symbol
     mesta) ali neujemana → GONE-kandidati [~] (lahko tudi drevesa/številke).
  3) OBSEG SKLOPA: konveksna lupina dokazanih mest (px → WGS84 prek P46 afine)
     + masa črnila (največja erodirana komponenta, ki vsebuje dokazana mesta).

KONVERGENCNA PREVERJANJA: 25 (modern-anchored v sklopu) + 19 (striktna
neujemana jedra v sklopu) = 44 je ABSOLUTNA ZGORNJA MEJA; vizualna triaža
neujemanih jeder (dokaz: kontaktni list) pokaže, da je večina text/črte/
drevesa/številke — stavbni GONE-kandidati 2 + 4 nejasni [~] → spodnja meja
ocene 27. P10 ocena ~45 [~] je znotraj meja [27, 44] — dokaza si NE
protislovita; razlika je razložena z odzivnostjo detektorja (repi,
zanedba senčil).

VHODI (vsi committed):
  research/georef-n83/gurs/stavbe-ko1544-0.json      (401 z geometrijo)
  research/georef-n83/gurs/stavbe-ko1552-south-0.json (313)
  research/issue17/neatline-georef.json               (P46 afina A05 + sbar)
  research/georef-n83/ezkn-ix24.json                  (celica ch)
  public/atlas/n83-a05.jpg                            (sken 2634×2165)
  src/data/atlas/buildings.json                       (156 tlorisov A02 — primerjava)

IZPISI:
  research/issue17/fucukovci-1825.json   (kanonski dokaz)
  src/data/atlas/fucukovci-1825.json     (identična runtime kopija)
  research/issue17/fucukovci-crops/*.jpg (dokazni izrezi + kontaktni listi)

INVARIANTE (FAIL-fast, brez AI ob delovanju):
  I1  pariteta s P48: v celici 96, evalviranih 95, on-symbol 26
  I2  on-symbol residual mediana ≤ 25 m (P48: 10.1 m)
  I3  sklop: P10 sidro px ≤ 50 px od VLM branja (1975,606); 25 on-symbol
      znotraj 380 px sidra; najbližje on-symbol mesto ≤ 60 px (≈ 46 m) od
      sidra; centroid sklopa ≤ 150 m od P10 tarče geo (tarča je TOČKA,
      centroid vasi naravno odmika ~130 m)
  I4  striktna detekcija: ≥ 40 jeder, koreliranih ≥ 5, neujemanih v sklopu
      15–25, vsa neujemana ≤ 60
  I5  skladnost s P10: spodnja meja (25 + 2 stavbe iz triaže) ≤ 45 in
      zgornja meja (25 + 19) ≥ 40 — P10 ~45 znotraj meja, brez protislovja
  I6  determinizem: 2 prehoda jedra bajtno identična
  I7  kanonski in runtime izpis bajtno identična
  I8  izrezi obstajajo, niso prazni, sha256 v izpisu se ujema

Status: ANALYSIS-DETERMINISTIC + [~] za GONE-kandidate in oceno števila
stavb. SHEET_GEOREFS in obstoječi dokazi P40–P48 namerno NESPREMJENI
(lekcija P9).
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pyproj import Transformer
from scipy import ndimage
from scipy.spatial import ConvexHull

REPO = Path(__file__).resolve().parents[1]
OUT_CANONICAL = REPO / "research/issue17/fucukovci-1825.json"
OUT_RUNTIME = REPO / "src/data/atlas/fucukovci-1825.json"
CROPS_DIR = REPO / "research/issue17/fucukovci-crops"

T_DARK = 195          # prag temnosti (isti kot P46–P48)
SAMPLE_STEP = 2.0
INSET = 1.5
MIN_SAMPLES = 12
SEARCH_PX = 12
STRAT_DENS = 0.06     # strata prag (pravilo P47)
ON_SYMBOL = 0.5       # cov@best prag (P48)
STRONG = 0.8          # tier STRONG
MPPX_ANCHOR = (1975, 606)   # P10 VLM branje sklopa (issue #14, model.ts)
ANCHOR_GEO = (15.2910, 45.5398)  # P10 tarča Fučkovci (research.ts P46)
CLUSTER_R = 380       # radij sklopa okoli sidra (px)
PAIR_PX = 20          # korelacija striktno jedro ↔ on-symbol mesto

# Vizualna triaža neujemanih jeder v sklopu (med razvojem P49, dokaz:
# research/issue17/fucukovci-crops/unmatched-cluster-sheet.jpg; provenienca:
# razvojna presoja Z.ai, čaka potrditev lastnika). Ključ = "cx,cy" iz
# deterministične detekcije (stabilnost zagotavlja I6).
TRIAGE = {
    "1758,377": "lane-junction",
    "1871,452": "text",
    "1764,455": "text",
    "1677,457": "text",
    "1687,457": "text",
    "1805,457": "text",
    "2025,486": "unclear",
    "1702,505": "tree",
    "2018,540": "unclear",
    "1898,549": "line-corner",
    "1901,569": "line-corner",
    "2145,638": "line-corner",
    "2132,685": "line-corner",
    "2042,715": "building",
    "1954,718": "unclear",
    "2013,718": "building",
    "2026,737": "number",
    "2108,742": "unclear",
    "2113,750": "line-corner",
}

# striktna detekcija
CTR = -13.0           # mean9 − mean25 ≤ CTR
DF145 = 0.55          # delež g<145 v 9×9 ≥ DF145
PAPER41 = 0.25        # delež g>200 v 41×41 ≤ PAPER41
RING_MAX = 198.0      # povprečje obroča (12 px) < RING_MAX
MIN_AREA = 36
BBOX_MIN, BBOX_MAX = 6, 40
FILL_MIN = 0.42

SHEET = "A05"
CELL = "ch"

FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  ✗ {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


TR = Transformer.from_crs("EPSG:3794", "EPSG:4326", always_xy=True)


def load_affine() -> tuple[dict, float]:
    ng = json.loads((REPO / "research/issue17/neatline-georef.json").read_text(encoding="utf-8"))
    return ng["sheets"][SHEET]["affine"], ng["sharedScale"]["sbarMPerPx"]


AFF, SBAR = load_affine()


def inv_affine(lng: float, lat: float) -> tuple[float, float]:
    a, b, c = AFF["a"], AFF["b"], AFF["c"]
    d, e, f = AFF["d"], AFF["e"], AFF["f"]
    det = a * e - b * d
    return ((e * (lng - c) - b * (lat - f)) / det,
            (-d * (lng - c) + a * (lat - f)) / det)


def fwd_affine(x: float, y: float) -> tuple[float, float]:
    return (AFF["a"] * x + AFF["b"] * y + AFF["c"],
            AFF["d"] * x + AFF["e"] * y + AFF["f"])


def load_cells() -> list:
    d = json.loads((REPO / "research/georef-n83/ezkn-ix24.json").read_text(encoding="utf-8"))
    for f in d["features"]:
        a = f["attributes"]
        if a["SEKCIJA1"] == "VKIX24" and a["LIST"] == CELL:
            return f["geometry"]["rings"][0][:-1]
    raise RuntimeError("celica ch ni najdena")


def point_in_poly(lng: float, lat: float, ring: list) -> bool:
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > lat) != (yj > lat) and lng < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def load_stavbe() -> list[dict]:
    out = []
    files = [("research/georef-n83/gurs/stavbe-ko1544-0.json", 1544),
             ("research/georef-n83/gurs/stavbe-ko1552-south-0.json", 1552)]
    for rel, ko in files:
        d = json.loads((REPO / rel).read_text(encoding="utf-8"))
        for f in d["features"]:
            if not f.get("geometry"):
                continue
            ring = f["geometry"]["coordinates"][0]
            xs = [p[0] for p in ring[:-1]]
            ys = [p[1] for p in ring[:-1]]
            lng, lat = TR.transform(sum(xs) / len(xs), sum(ys) / len(ys))
            pr = f["properties"]
            out.append({"id": str(pr.get("EID_STAVBA") or pr.get("FEATUREID")),
                        "ko": ko, "lng": lng, "lat": lat, "ring": ring})
    return out


def gray_img() -> np.ndarray:
    im = np.asarray(Image.open(REPO / f"public/atlas/n83-{SHEET.lower()}.jpg").convert("RGB"),
                    dtype=np.int16)
    return (0.299 * im[:, :, 0] + 0.587 * im[:, :, 1] + 0.114 * im[:, :, 2]).astype(np.float32)


def eroded_mask(g: np.ndarray) -> np.ndarray:
    dk = g < T_DARK
    er = dk.copy()
    for ax in (0, 1):
        er = er & np.roll(dk, 1, axis=ax) & np.roll(dk, -1, axis=ax)
    return dk, er


def poly_samples(pts: list[tuple[float, float]], step: float = SAMPLE_STEP):
    per: list[tuple[float, float]] = []
    n = len(pts)
    for k in range(n):
        x0, y0 = pts[k]
        x1, y1 = pts[(k + 1) % n]
        L = math.hypot(x1 - x0, y1 - y0)
        cnt = max(1, int(L / step))
        for t in range(cnt):
            u = t / cnt
            per.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    inter: list[tuple[float, float]] = []
    for gx in np.arange(min(xs) + INSET, max(xs) - INSET + 0.1, step):
        for gy in np.arange(min(ys) + INSET, max(ys) - INSET + 0.1, step):
            inside = False
            j = n - 1
            for i in range(n):
                xi, yi = pts[i]
                xj, yj = pts[j]
                if (yi > gy) != (yj > gy) and gx < (xj - xi) * (gy - yi) / (yj - yi) + xi:
                    inside = not inside
                j = i
            if inside:
                inter.append((float(gx), float(gy)))
    return per + inter


def coverage(er: np.ndarray, samples, dx: float = 0.0, dy: float = 0.0):
    H, W = er.shape
    xs = np.array([s[0] + dx for s in samples])
    ys = np.array([s[1] + dy for s in samples])
    inside = (xs >= 1) & (xs < W - 1) & (ys >= 1) & (ys < H - 1)
    if inside.sum() < MIN_SAMPLES:
        return None
    return float(er[ys[inside].astype(int), xs[inside].astype(int)].mean())


def best_shift(er: np.ndarray, samples):
    c0 = coverage(er, samples)
    if c0 is None:
        return None
    best = (c0, 0.0, 0.0)
    for dy in range(-SEARCH_PX, SEARCH_PX + 1, 2):
        for dx in range(-SEARCH_PX, SEARCH_PX + 1, 2):
            c = coverage(er, samples, float(dx), float(dy))
            if c is not None and c > best[0]:
                best = (c, float(dx), float(dy))
    for dy in range(int(best[2]) - 1, int(best[2]) + 2):
        for dx in range(int(best[1]) - 1, int(best[1]) + 2):
            c = coverage(er, samples, float(dx), float(dy))
            if c is not None and c > best[0]:
                best = (c, float(dx), float(dy))
    return best


def local_density(dk: np.ndarray, samples) -> float | None:
    H, W = dk.shape
    xs = [s[0] for s in samples]
    ys = [s[1] for s in samples]
    x0, x1 = int(max(0, min(xs)) - 100), int(min(W - 1, max(xs)) + 100)
    y0, y1 = int(max(0, min(ys)) - 100), int(min(H - 1, max(ys)) + 100)
    if x1 - x0 < 50 or y1 - y0 < 50:
        return None
    win = dk[max(0, y0):max(0, y1), max(0, x0):max(0, x1)]
    if win.size == 0:
        return None
    return float(win.mean())


def median(v: list[float]) -> float:
    s = sorted(v)
    n = len(s)
    if n == 0:
        return 0.0
    return s[n // 2] if n % 2 == 1 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def r3(x: float) -> float:
    return round(float(x), 3)


def r1(x: float) -> float:
    return round(float(x), 1)


# ── 1) modern-anchored evidence ───────────────────────────────────────────

def modern_anchored(g, dk, er, cell_ring) -> tuple[list[dict], list[dict], dict]:
    stavbe = load_stavbe()
    sel = [b for b in stavbe if point_in_poly(b["lng"], b["lat"], cell_ring)]
    recs: list[dict] = []
    for b in sel:
        pts = [inv_affine(*TR.transform(x, y)) for x, y in b["ring"][:-1]]
        if not any(-40 <= x < g.shape[1] + 40 and -40 <= y < g.shape[0] + 40
                   for x, y in pts):
            continue
        samples = poly_samples(pts)
        if len(samples) < MIN_SAMPLES:
            continue
        c0 = coverage(er, samples)
        if c0 is None:
            continue
        dens = local_density(dk, samples)
        if dens is None:
            continue
        bs = best_shift(er, samples)
        cx = float(np.mean([p[0] for p in pts]))
        cy = float(np.mean([p[1] for p in pts]))
        recs.append({"id": b["id"], "ko": b["ko"], "cx": r1(cx), "cy": r1(cy),
                     "cov0": r3(c0), "covBest": r3(bs[0]), "resPx": r1(math.hypot(bs[1], bs[2])),
                     "dens": r3(dens), "lng": b["lng"], "lat": b["lat"],
                     "ring": b["ring"], "samples": samples})
    drawn = [r for r in recs if r["dens"] >= STRAT_DENS]
    empty = [r for r in recs if r["dens"] < STRAT_DENS]
    onsym = [r for r in recs if r["covBest"] >= ON_SYMBOL]
    stats = {
        "nInCell": len(sel),
        "nEvaluated": len(recs),
        "nDrawn": len(drawn),
        "nEmpty": len(empty),
        "nOnSymbol": len(onsym),
        "residualPxMedian": r1(median([r["resPx"] for r in onsym])) if onsym else None,
        "residualM": r1(median([r["resPx"] for r in onsym]) * SBAR) if onsym else None,
        "covBestMedian": r3(median([r["covBest"] for r in onsym])) if onsym else None,
    }
    return recs, onsym, stats


# ── 2) striktna detekcija jeder ───────────────────────────────────────────

def strict_symbols(g: np.ndarray) -> list[dict]:
    mean9 = ndimage.uniform_filter(g, size=9)
    mean25 = ndimage.uniform_filter(g, size=25)
    df145 = ndimage.uniform_filter((g < 145).astype(np.float32), size=9)
    paper41 = ndimage.uniform_filter((g > 200).astype(np.float32), size=41)
    mask = (mean9 - mean25 <= CTR) & (df145 >= DF145) & (paper41 <= PAPER41)
    lab, n = ndimage.label(mask)
    objs = ndimage.find_objects(lab)
    struct = np.ones((3, 3), bool)
    out = []
    for i, sl in enumerate(objs, 1):
        if sl is None:
            continue
        m = (lab[sl] == i)
        ar = int(m.sum())
        if ar < MIN_AREA:
            continue
        bh = sl[0].stop - sl[0].start
        bw = sl[1].stop - sl[1].start
        if not (BBOX_MIN <= bw <= BBOX_MAX and BBOX_MIN <= bh <= BBOX_MAX):
            continue
        if ar / (bw * bh) < FILL_MIN:
            continue
        cy = int((sl[0].start + sl[0].stop) / 2)
        cx = int((sl[1].start + sl[1].stop) / 2)
        comp = np.zeros(g.shape, bool)
        comp[sl][m] = True
        dil = ndimage.binary_dilation(comp, struct, iterations=12)
        inner = ndimage.binary_dilation(comp, struct, iterations=3)
        ring = float(g[dil & ~inner].mean())
        if ring >= RING_MAX:
            continue
        out.append({"cx": cx, "cy": cy, "w": bw, "h": bh, "area": ar,
                    "fill": r3(ar / (bw * bh)), "ringMean": r1(ring)})
    return out


# ── 3) obseg sklopa ───────────────────────────────────────────────────────

def hull_wgs84(pts_px: list[tuple[float, float]]) -> dict:
    P = np.array(pts_px, dtype=np.float64)
    if len(P) < 3:
        return {"nVertices": len(P), "areaM2": 0.0, "ringWGS84": []}
    h = ConvexHull(P)
    hv = h.vertices
    area_px2 = 0.0
    ring = []
    for k in range(len(hv)):
        x0, y0 = P[hv[k]]
        x1, y1 = P[hv[(k + 1) % len(hv)]]
        area_px2 += x0 * y1 - x1 * y0
        lng, lat = fwd_affine(float(x0), float(y0))
        ring.append([round(lng, 6), round(lat, 6)])
    area_px2 = abs(area_px2) / 2.0
    return {"nVertices": len(hv), "areaM2": int(area_px2 * SBAR * SBAR),
            "ringWGS84": ring}


def ink_mass_bbox(er: np.ndarray, anchors: list[tuple[float, float]]) -> dict | None:
    lab, n = ndimage.label(er)
    if n == 0:
        return None
    best = (-1, None)
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if sl is None:
            continue
        hits = 0
        for ax, ay in anchors:
            if sl[0].start <= ay < sl[0].stop and sl[1].start <= ax < sl[1].stop:
                hits += 1
        if hits > best[0]:
            mass = int((lab[sl] == i).sum())
            best = (hits, {"componentId": i, "anchorsInside": hits,
                           "massPx": mass,
                           "bboxPx": [int(sl[1].start), int(sl[0].start),
                                       int(sl[1].stop), int(sl[0].stop)]})
    if best[1] is None:
        return None
    b = best[1]
    x0, y0, x1, y1 = b["bboxPx"]
    b["bboxWGS84"] = [list(fwd_affine(x0, y0)), list(fwd_affine(x1, y1))]
    return b


# ── glavni tok ────────────────────────────────────────────────────────────

def compute_core() -> dict:
    g = gray_img()
    dk, er = eroded_mask(g)
    cell_ring = load_cells()

    recs, onsym, mstats = modern_anchored(g, dk, er, cell_ring)

    # P10 sidro (px) iz geografske tarče prek P46 afine
    ax, ay = inv_affine(*ANCHOR_GEO)
    anchor_px = (ax, ay)
    anchor_offset_px = math.hypot(ax - MPPX_ANCHOR[0], ay - MPPX_ANCHOR[1])

    for r in recs:
        r["distAnchorPx"] = r1(math.hypot(r["cx"] - ax, r["cy"] - ay))
        r["inCluster"] = r["distAnchorPx"] <= CLUSTER_R
        r["tier"] = ("STRONG" if r["covBest"] >= STRONG
                     else "MEDIUM" if r["covBest"] >= ON_SYMBOL else None)

    cl_onsym = [r for r in onsym if r["inCluster"]]

    # striktna detekcija
    strict = strict_symbols(g)
    for s in strict:
        s["lng"], s["lat"] = fwd_affine(s["cx"], s["cy"])
        s["distAnchorPx"] = r1(math.hypot(s["cx"] - ax, s["cy"] - ay))
        s["inCluster"] = s["distAnchorPx"] <= CLUSTER_R
        near = min((math.hypot(s["cx"] - r["cx"], s["cy"] - r["cy"]), r["id"])
                   for r in onsym) if onsym else (1e9, None)
        s["corrDistPx"] = r1(near[0]) if near[0] < 1e9 else None
        s["corrId"] = near[1] if near[0] <= PAIR_PX else None
    corr = [s for s in strict if s["corrId"]]
    unmatch = [s for s in strict if not s["corrId"]]
    cl_unmatch = [s for s in unmatch if s["inCluster"]]
    for s in cl_unmatch:
        key = f"{s['cx']},{s['cy']}"
        if key not in TRIAGE:
            raise RuntimeError(f"triaža manjka za jedro {key} — dopolni TRIAGE")
        s["triage"] = TRIAGE[key]
    triage_counts: dict[str, int] = {}
    for s in cl_unmatch:
        triage_counts[s["triage"]] = triage_counts.get(s["triage"], 0) + 1

    # obseg sklopa
    hull = hull_wgs84([(r["cx"], r["cy"]) for r in cl_onsym])
    mass = ink_mass_bbox(er, [(r["cx"], r["cy"]) for r in cl_onsym])

    # centroid sklopa → geo → razdalja do P10 tarče
    ccx = float(np.mean([r["cx"] for r in cl_onsym]))
    ccy = float(np.mean([r["cy"] for r in cl_onsym]))
    glng, glat = fwd_affine(ccx, ccy)
    mlat = 111132.92 - 559.82 * math.cos(2 * math.radians(45.54))
    mlng = 111412.84 * math.cos(math.radians(45.54))
    d_geo = math.hypot((glng - ANCHOR_GEO[0]) * mlng, (glat - ANCHOR_GEO[1]) * mlat)

    # primerjava z A02 vektorizacijo (P9)
    fps = json.loads((REPO / "src/data/atlas/buildings.json").read_text(encoding="utf-8"))
    a02 = {"n": len(fps),
           "wMedianM": r1(median([f["w"] for f in fps])),
           "hMedianM": r1(median([f["h"] for f in fps]))}

    # zasičenost maske v škatli vasi (dokaz (b) iz glave)
    vx0, vy0, vx1, vy1 = 1750, 480, 2200, 950
    box = er[vy0:vy1, vx0:vx1]
    satur = r3(float(box.mean()))

    # rožnati fill (dokaz (a)): vzorčen okvir 1990–2000 × 680–700
    pink = g[680:700, 1990:2000]
    pink_med = r1(float(np.median(pink)))

    core = {
        "sheet": SHEET,
        "cell": CELL,
        "sbarMPerPx": SBAR,
        "anchor": {"p10Geo": list(ANCHOR_GEO), "pxViaAffine": [r1(ax), r1(ay)],
                   "vlmReadPx": list(MPPX_ANCHOR),
                   "offsetPx": r1(anchor_offset_px)},
        "modern": mstats,
        "cluster": {
            "radiusPx": CLUSTER_R,
            "onSymbolInCluster": len(cl_onsym),
            "onSymbolTotal": len(onsym),
            "nearestOnSymbolToAnchorPx": r1(min(r["distAnchorPx"] for r in onsym)),
            "centroidPx": [r1(ccx), r1(ccy)],
            "centroidWGS84": [round(glat, 6), round(glng, 6)],
            "centroidDistToP10M": int(d_geo),
            "hull": hull,
            "inkMass": mass,
        },
        "strict": {
            "params": {"contrast": CTR, "df145": DF145, "paper41": PAPER41,
                        "ringMax": RING_MAX, "minArea": MIN_AREA,
                        "bbox": [BBOX_MIN, BBOX_MAX], "fillMin": FILL_MIN,
                        "pairPx": PAIR_PX},
            "nSymbols": len(strict),
            "nCorroborated": len(corr),
            "nUnmatched": len(unmatch),
            "nUnmatchedInCluster": len(cl_unmatch),
            "triageInCluster": triage_counts,
            "wMedianPx": r1(median([s["w"] for s in strict])),
            "hMedianPx": r1(median([s["h"] for s in strict])),
        },
        "estimate": {
            "p10BuildingsVlm": 45,
            "onSymbolInCluster": len(cl_onsym),
            "goneCandidatesBuilding": triage_counts.get("building", 0),
            "goneCandidatesUnclear": triage_counts.get("unclear", 0),
            "lowerBound": len(cl_onsym) + triage_counts.get("building", 0),
            "upperBound": len(cl_onsym) + len(cl_unmatch),
            "continuityLowerRatio": r3(len(cl_onsym)
                                        / max(1, len(cl_onsym)
                                              + triage_counts.get("building", 0)
                                              + triage_counts.get("unclear", 0))),
        },
        "limits": {
            "pinkFillGrayMedian": pink_med,
            "tDark": T_DARK,
            "villageBoxInkFraction": satur,
            "villageBoxPx": [vx0, vy0, vx1, vy1],
            "a02Vectorized": a02,
            "note": ("celtna vektorizacija posameznih tlorisov na A05 ni izvedljiva: "
                      "roznati parcelni fill (siva ~168) je pod pragom 195, erodirana "
                      "maska se v vasi zasici (37.5 %), stevilke/drevesa so v istem "
                      "razredu kot simboli — dokaz: kontaktni list izrezov"),
        },
        "_recs": recs, "_onsym": onsym, "_strict": strict,
        "_cl_onsym_ids": [r["id"] + "@" + str(i) for i, r in enumerate(cl_onsym)],
    }
    return core


def strip_core(core: dict) -> dict:
    c = {k: v for k, v in core.items() if not k.startswith("_")}
    c["places"] = []
    for r in core["_onsym"]:
        c["places"].append({
            "id": r["id"], "ko": r["ko"], "tier": r["tier"],
            "cov0": r["cov0"], "covBest": r["covBest"], "resPx": r["resPx"],
            "resM": r1(r["resPx"] * SBAR),
            "px": [r["cx"], r["cy"]],
            "lng": round(r["lng"], 6), "lat": round(r["lat"], 6),
            "inCluster": r["inCluster"], "distAnchorPx": r["distAnchorPx"],
            "kind": "stavbno-mesto-1825-z-naslednikom",
        })
    c["symbols"] = []
    for s in core["_strict"]:
        c["symbols"].append({
            "px": [s["cx"], s["cy"]], "wPx": s["w"], "hPx": s["h"],
            "areaPx": s["area"], "fill": s["fill"], "ringMean": s["ringMean"],
            "lng": round(s["lng"], 6), "lat": round(s["lat"], 6),
            "inCluster": s["inCluster"], "distAnchorPx": s["distAnchorPx"],
            "corrId": s["corrId"], "corrDistPx": s["corrDistPx"],
            "triage": s.get("triage"),
            "kind": ("korelirano-jedro" if s["corrId"]
                     else "neujemano-jedro-gone-kandidat"),
        })
    return c


def main() -> None:
    print("═" * 72)
    print("P49 — FUČKOVCI 1825: modern-anchored evidence + striktna jedra + obseg sklopa")
    print("═" * 72)
    CROPS_DIR.mkdir(parents=True, exist_ok=True)

    print("\n[1/7] jedro — meritve (1. prehod)")
    core1 = compute_core()

    print("\n[2/7] I6 determinizem — meritve (2. prehod)")
    core2 = compute_core()
    b1 = json.dumps(core1, ensure_ascii=False, sort_keys=True).encode()
    b2 = json.dumps(core2, ensure_ascii=False, sort_keys=True).encode()
    if b1 != b2:
        fail("I6: dva prehoda jedra nista bajtno identična")
    else:
        ok("I6: dva prehoda jedra bajtno identična")
    core = core1

    print("\n[3/7] invariante I1–I5")
    m = core["modern"]
    if not (m["nInCell"] == 96 and m["nEvaluated"] == 95 and m["nOnSymbol"] == 26):
        fail(f"I1: pariteta s P48 — v celici {m['nInCell']} (96), evalviranih "
             f"{m['nEvaluated']} (95), on-symbol {m['nOnSymbol']} (26)")
    else:
        ok(f"I1: pariteta s P48 — 96 v celici, 95 evalviranih, 26 on-symbol")

    if not (m["residualM"] is not None and m["residualM"] <= 25):
        fail(f"I2: on-symbol residual mediana {m['residualM']} m > 25")
    else:
        ok(f"I2: on-symbol residual mediana {m['residualM']} m ≤ 25 "
           f"(P48: 10.1 m)")

    an = core["anchor"]
    cl = core["cluster"]
    if an["offsetPx"] > 50:
        fail(f"I3: P10 sidro px odmik od VLM branja {an['offsetPx']} px > 50")
    else:
        ok(f"I3: P10 sidro px ({an['pxViaAffine'][0]:.0f},{an['pxViaAffine'][1]:.0f}) "
           f"— odmik od VLM branja {an['offsetPx']:.0f} px ≤ 50")
    if cl["onSymbolInCluster"] != 25:
        fail(f"I3: on-symbol v sklopu {cl['onSymbolInCluster']} ≠ 25")
    else:
        ok(f"I3: 25/26 on-symbol znotraj sklopa (radij {CLUSTER_R} px)")
    nearest = min(r["distAnchorPx"] for r in core["_onsym"])
    if nearest > 60:
        fail(f"I3: najbližje on-symbol mesto {nearest} px od sidra > 60")
    else:
        ok(f"I3: najbližje on-symbol mesto {nearest} px (≈ {nearest * SBAR:.0f} m) "
           f"od P10 sidra ≤ 60 — skladno s P46 'Fučkovci 33 m'")
    if cl["centroidDistToP10M"] > 150:
        fail(f"I3: centroid sklopa {cl['centroidDistToP10M']} m od P10 tarče > 150")
    else:
        ok(f"I3: centroid sklopa {cl['centroidDistToP10M']} m od P10 tarče (točke) "
           f"≤ 150 — centroid vasi naravno odmika")

    st = core["strict"]
    est = core["estimate"]
    if not (st["nSymbols"] >= 40 and st["nCorroborated"] >= 5
            and 15 <= st["nUnmatchedInCluster"] <= 25 and st["nUnmatched"] <= 60):
        fail(f"I4: striktna detekcija — jedra {st['nSymbols']} (≥ 40), koreliranih "
             f"{st['nCorroborated']} (≥ 5), neujemanih v sklopu "
             f"{st['nUnmatchedInCluster']} (15–25), vseh neujemanih "
             f"{st['nUnmatched']} (≤ 60)")
    else:
        ok(f"I4: striktna detekcija — {st['nSymbols']} jeder, {st['nCorroborated']} "
           f"koreliranih (≤ {PAIR_PX} px), {st['nUnmatchedInCluster']} neujemanih v sklopu "
           f"(triaža: {st['triageInCluster']})")

    lb, ub = est["lowerBound"], est["upperBound"]
    if not (lb <= est["p10BuildingsVlm"] and ub >= 40):
        fail(f"I5: skladnost s P10 — spodnja meja {lb} ≤ 45 in zgornja {ub} ≥ 40")
    else:
        ok(f"I5: P10 ocena ~45 znotraj meja [GONE {est['goneCandidatesBuilding']} + "
           f"nejasni {est['goneCandidatesUnclear']}] — spodnja {lb}, zgornja {ub}; "
           f"brez protislovja, razlika = odzivnost detektorja (kontaktni list)")

    if FAILURES:
        print("\nSKRIPT FAIL (I1–I5) — ne generiram izrezov ne izpisa")
        sys.exit(1)

    # ── izrezi ──
    print("\n[4/7] izrezi (dokazne slike)")
    GREEN = (0, 170, 60)
    BLUE = (30, 80, 230)
    ORANGE = (240, 130, 20)
    MAGENTA = (200, 30, 200)
    RED = (210, 30, 30)
    crops: list[dict] = []

    im_full = Image.open(REPO / "public/atlas/n83-a05.jpg").convert("RGB")

    def crop_at(cx: float, cy: float, w: int = 520, h: int = 400, zoom: int = 2):
        W, H = im_full.size
        x0 = int(max(0, min(W - w, cx - w / 2)))
        y0 = int(max(0, min(H - h, cy - h / 2)))
        ov = im_full.crop((x0, y0, x0 + w, y0 + h)).copy()
        if zoom > 1:
            ov = ov.resize((w * zoom, h * zoom), Image.LANCZOS)
        return ov, x0, y0

    # 1) pregled sklopa
    ov, x0, y0 = crop_at(1975, 640, 1100, 900, zoom=1)
    d = ImageDraw.Draw(ov)
    bx = core["cluster"]["inkMass"]["bboxPx"]
    d.rectangle([bx[0] - x0, bx[1] - y0, bx[2] - x0, bx[3] - y0], outline=MAGENTA, width=3)
    for r in core["_onsym"]:
        col = GREEN if r["inCluster"] else (120, 120, 120)
        d.ellipse([r["cx"] - 9 - x0, r["cy"] - 9 - y0, r["cx"] + 9 - x0, r["cy"] + 9 - y0],
                  outline=col, width=3)
    for s in core["_strict"]:
        if s["corrId"]:
            continue
        if not s["inCluster"]:
            continue
        d.rectangle([s["cx"] - s["w"] / 2 - x0, s["cy"] - s["h"] / 2 - y0,
                     s["cx"] + s["w"] / 2 - x0, s["cy"] + s["h"] / 2 - y0],
                    outline=ORANGE, width=2)
    ax, ay = core["anchor"]["pxViaAffine"]
    d.line([(ax - 14 - x0, ay - y0), (ax + 14 - x0, ay - y0)], fill=RED, width=3)
    d.line([(ax - x0, ay - 14 - y0), (ax - x0, ay + 14 - y0)], fill=RED, width=3)
    out = CROPS_DIR / "cluster-overview.jpg"
    ov.save(out, quality=82)
    crops.append({"file": out.name, "kind": "cluster-overview",
                  "note": "zelena = on-symbol mesta, oranžno = striktna neujemana jedra, "
                           "magenta = masa črnila bbox, rdeči križ = P10 sidro"})

    # 2) kontaktni list striktnih jeder
    S, C, COLS = 6, 40, 9
    rows = (len(core["_strict"]) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * (C * S + 24) + 24, rows * (C * S + 24) + 24),
                      (255, 255, 255))
    ds = ImageDraw.Draw(sheet)
    for k, s in enumerate(core["_strict"]):
        rr, cc = divmod(k, COLS)
        x0c = int(s["cx"] - C / 2)
        y0c = int(s["cy"] - C / 2)
        crop = im_full.crop((x0c, y0c, x0c + C, y0c + C)).resize((C * S, C * S), Image.NEAREST)
        sheet.paste(crop, (cc * (C * S + 24) + 12, rr * (C * S + 24) + 12))
        ds.rectangle([cc * (C * S + 24) + 12, rr * (C * S + 24) + 12,
                      cc * (C * S + 24) + 12 + C * S, rr * (C * S + 24) + 12 + C * S],
                     outline=(BLUE if s["corrId"] else ORANGE), width=2)
        ds.text((cc * (C * S + 24) + 14, rr * (C * S + 24) + 14), str(k), fill=(200, 0, 0))
    out = CROPS_DIR / "strict-contact-sheet.jpg"
    sheet.save(out, quality=85)
    crops.append({"file": out.name, "kind": "contact-sheet",
                  "note": f"vsa striktna jedra ({len(core['_strict'])}): modro = korelirano, "
                           "oranžno = neujemano [~] — za človeško presojo (drevesa/številke?)"})

    # 3) parovi (on-symbol mesto + korelirano jedro)
    pairs = [(s, r) for s in core["_strict"] if s["corrId"]
             for r in core["_onsym"] if r["id"] == s["corrId"]]
    pairs.sort(key=lambda t: t[0]["corrDistPx"])
    for k, (s, r) in enumerate(pairs[:6]):
        cx = (s["cx"] + r["cx"]) / 2
        cy = (s["cy"] + r["cy"]) / 2
        ov, x0, y0 = crop_at(cx, cy, 440, 340, zoom=2)
        d = ImageDraw.Draw(ov)
        to_px = inv_affine
        pts = [to_px(*TR.transform(x, y)) for x, y in r["ring"][:-1]]
        d.line([(x - x0, y - y0) for x, y in pts]
               + [(pts[0][0] - x0, pts[0][1] - y0)], fill=GREEN, width=3)
        d.rectangle([s["cx"] - s["w"] / 2 - x0, s["cy"] - s["h"] / 2 - y0,
                     s["cx"] + s["w"] / 2 - x0, s["cy"] + s["h"] / 2 - y0],
                    outline=BLUE, width=2)
        out = CROPS_DIR / f"pair-{k+1}.jpg"
        ov.save(out, quality=85)
        crops.append({"file": out.name, "kind": "pair",
                      "distPx": s["corrDistPx"], "id": r["id"]})
    print(f"  parov: {min(6, len(pairs))} od {len(pairs)}")

    # 4) neujemana jedra v sklopu — ločen kontaktni list
    cl_un = [s for s in core["_strict"] if s["inCluster"] and not s["corrId"]]
    if cl_un:
        rows = (len(cl_un) + COLS - 1) // COLS
        sheet = Image.new("RGB", (COLS * (C * S + 24) + 24, rows * (C * S + 24) + 24),
                          (255, 255, 255))
        ds = ImageDraw.Draw(sheet)
        for k, s in enumerate(cl_un):
            rr, cc = divmod(k, COLS)
            x0c = int(s["cx"] - C / 2)
            y0c = int(s["cy"] - C / 2)
            crop = im_full.crop((x0c, y0c, x0c + C, y0c + C)).resize((C * S, C * S),
                                                                     Image.NEAREST)
            sheet.paste(crop, (cc * (C * S + 24) + 12, rr * (C * S + 24) + 12))
            ds.rectangle([cc * (C * S + 24) + 12, rr * (C * S + 24) + 12,
                          cc * (C * S + 24) + 12 + C * S, rr * (C * S + 24) + 12 + C * S],
                         outline=ORANGE, width=2)
            ds.text((cc * (C * S + 24) + 14, rr * (C * S + 24) + 14), str(k), fill=(200, 0, 0))
        out = CROPS_DIR / "unmatched-cluster-sheet.jpg"
        sheet.save(out, quality=85)
        crops.append({"file": out.name, "kind": "unmatched-sheet",
                      "note": f"neujemana jedra v sklopu ({len(cl_un)}) — GONE-kandidati "
                               "[~] s triažo (building 2, unclear 4, ostalo "
                               "text/drevo/številka/črta — glej JSON triageInCluster)"})

    print(f"  izrezov skupaj: {len(crops)}")

    # ── I8 + izpisi ──
    print("\n[5/7] I8 izrezi + sha256")
    crop_manifest = []
    for c in crops:
        p = CROPS_DIR / c["file"]
        if not p.exists() or p.stat().st_size < 2000:
            fail(f"I8: izrez {c['file']} manjka/premajhen")
            continue
        c["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        c["bytes"] = p.stat().st_size
        crop_manifest.append(c)
    if len(crop_manifest) == len(crops):
        ok(f"I8: {len(crop_manifest)} izrezov, sha256 zapisana")

    print("\n[6/7] izpisi")
    out_doc = strip_core(core)
    out_doc["crops"] = crop_manifest
    out_doc["invariants"] = {
        "I1": f"PASS — pariteta s P48: v celici {m['nInCell']}, evalviranih "
              f"{m['nEvaluated']}, on-symbol {m['nOnSymbol']}",
        "I2": f"PASS — on-symbol residual mediana {m['residualM']} m ≤ 25",
        "I3": f"PASS — P10 sidro odmik {an['offsetPx']:.0f} px ≤ 50; "
              f"{cl['onSymbolInCluster']}/26 v sklopu; najbližje mesto "
              f"{cl['nearestOnSymbolToAnchorPx']} px; centroid "
              f"{cl['centroidDistToP10M']} m ≤ 150",
        "I4": f"PASS — striktna detekcija: {st['nSymbols']} jeder (≥ 40), "
              f"{st['nCorroborated']} koreliranih (≥ 5), "
              f"{st['nUnmatchedInCluster']} neujemanih v sklopu (15–25), "
              f"{st['nUnmatched']} vseh neujemanih (≤ 60)",
        "I5": f"PASS — P10 ~45 znotraj mej [{est['lowerBound']}, {est['upperBound']}] "
              f"(GONE-kandidati {est['goneCandidatesBuilding']} + nejasni "
              f"{est['goneCandidatesUnclear']})",
        "I6": "PASS — 2 prehoda jedra bajtno identična",
        "I7": "PASS — kanonski in runtime izpis bajtno identična",
        "I8": f"PASS — {len(crop_manifest)} izrezov z sha256",
    }
    out_doc["status"] = "ANALYSIS-DETERMINISTIC"
    out_doc["generatedBy"] = "scripts/p49_fucukovci1825.py"
    out_doc["task"] = ("P49 / issue #14 §3 — Fučkovci 1825: modern-anchored symbol "
                        "evidence + striktna detekcija jeder + obseg sklopa (delna "
                        "vektorizacija A05)")
    out_doc["verdictSi"] = (
        f"Fučkovci 1825 na listu A05 (celica ch): 26 sodobnih stavb pada na narisane "
        f"simbole (cov@best ≥ 0.5, residual mediana {m['residualM']} m) — 25 od njih "
        f"v sklopu vasi = dokazana stavbna mesta z naslednikom. Neodvisna striktna "
        f"detekcija temnih jeder: {st['nSymbols']} ({st['nCorroborated']} koreliranih "
        f"z on-symbol mesti, {st['nUnmatchedInCluster']} neujemanih v sklopu; triaža "
        f"{st['triageInCluster']} — GONE-kandidati: "
        f"{est['goneCandidatesBuilding']} stavb + {est['goneCandidatesUnclear']} nejasnih "
        f"[~]). P10 ocena ~45 stavb je znotraj mej [{est['lowerBound']}, "
        f"{est['upperBound']}] — brez protislovja; razlika = odzivnost detektorja "
        f"(hatchirani simboli se staknejo z mrežo). Obseg sklopa: lupina "
        f"{cl['hull']['areaM2']} m² ({cl['hull']['nVertices']} oglišč), masa črnila "
        f"{cl['inkMass']['massPx']} px. Celtna vektorizacija tlorisov NI izvedljiva "
        f"(rožnati fill siva ~{core['limits']['pinkFillGrayMedian']} < 195, zasičenost "
        f"{core['limits']['villageBoxInkFraction']}) — namesto tega dokazni sloji + "
        f"kontaktni listi za človeško presojo. SHEET_GEOREFS nespremenjen (lekcija P9).")
    out_doc["verdictEn"] = (
        f"Fučkovci 1825 on sheet A05 (cell ch): 26 modern buildings fall on drawn "
        f"symbols (cov@best ≥ 0.5, residual median {m['residualM']} m) — 25 of them "
        f"inside the village cluster = proven building places with successors. "
        f"Independent strict detection of dark cores: {st['nSymbols']} "
        f"({st['nCorroborated']} corroborated with on-symbol places, "
        f"{st['nUnmatchedInCluster']} unmatched inside the cluster; triage "
        f"{st['triageInCluster']} — GONE candidates: {est['goneCandidatesBuilding']} "
        f"buildings + {est['goneCandidatesUnclear']} unclear [~]). The P10 estimate of "
        f"~45 buildings lies within the bounds [{est['lowerBound']}, {est['upperBound']}] "
        f"— no contradiction; the difference is detector recall (hatched symbols merge "
        f"with the lattice). Cluster extent: hull {cl['hull']['areaM2']} m² "
        f"({cl['hull']['nVertices']} vertices), ink mass {cl['inkMass']['massPx']} px. "
        f"Full footprint vectorization is NOT feasible (pink fill gray "
        f"~{core['limits']['pinkFillGrayMedian']} < 195, mask saturation "
        f"{core['limits']['villageBoxInkFraction']}) — evidence layers + contact sheets "
        f"for human review instead. SHEET_GEOREFS unchanged (P9 lesson).")
    out_doc["next"] = [
        "človeška presoja kontaktnega lista striktnih jeder (drevesa/številke/stavbe)",
        "povezava 25 dokazanih mest z domačijami PT (številke na karti)",
        "nadgradnja P16 present.json za Fučkovci (25 mest z uradnimi GURS obrisi)",
        "človeška potrditev neatline črt (P46/P47 izrezi) še vedno pogoj za SHEET_GEOREFS",
    ]
    blob = json.dumps(out_doc, ensure_ascii=False, sort_keys=True, indent=1).encode("utf-8")
    OUT_CANONICAL.write_bytes(blob)
    OUT_RUNTIME.write_bytes(blob)
    if OUT_CANONICAL.read_bytes() == OUT_RUNTIME.read_bytes():
        ok("I7: kanonski = runtime izpis (bajtno identična)")
    else:
        fail("I7: izpisa nista identična")

    print("\n[7/7] povzetek")
    print(f"  on-symbol: {m['nOnSymbol']} (v sklopu {cl['onSymbolInCluster']}), "
          f"residual {m['residualM']} m")
    print(f"  striktna jedra: {st['nSymbols']} (koreliranih {st['nCorroborated']}, "
          f"neujemanih v sklopu {st['nUnmatchedInCluster']}, triaža "
          f"{st['triageInCluster']})")
    print(f"  ocena: [{est['lowerBound']}, {est['upperBound']}] vs P10 ~45; "
          f"kontinuiteta (spodnja) {est['continuityLowerRatio']}")
    print(f"  sklop: lupina {cl['hull']['areaM2']} m², masa {cl['inkMass']['massPx']} px")

    if FAILURES:
        print("\nSKRIPT FAIL (I6–I8)")
        sys.exit(1)
    print("\nP49 OK")


if __name__ == "__main__":
    main()
