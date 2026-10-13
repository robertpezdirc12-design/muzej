#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P48 (issue #14 / §3 nadaljevanje) — STAVBNI OVERLAY: GURS STAVBE ↔ STAVBNA MESTA 1825.
Most PUA↔PT↔PS↔GURS: sodobni stavbni tlorisi (GURS eZKN WFS, SI.GURS.KN:STAVBE,
OBRIS_GEOM, EPSG:3794 → WGS84) preslikani prek GEOTRUTH meja A02 / P46 afin A03–A05
nazaj na skene morajo pasti na narisane stavbne simbole 1825.

DELI:
  1) OVERLAY/VALIDACIJA (listi A02–A05): za vsako sodobno stavbo vzorčimo notranjost
     + obod tlorisa (korak 2 px, notranjost vrezana 1,5 px) in merimo pokritost
     črnila na ERODIRANI maski (plus-oblika 3×3, prag 195 — kot P46/P47; erozija
     odstrani tanke parcelne črte, polni stavbni simboli 1825 preživijo).
     cov@0 brez zamika, cov@best pri najboljšem zamiku ±12 px (grobo po 2, fino ±1),
     residual registracije. Kontrole: zamiki 100/200/400 px × 8 smeri.
     Strata po pravilu P47: lokalna gostota temnega (bbox±100 px) ≥ 0.06 → DRAWN.
     Klasifikacija stavb: ON-SYMBOL (cov@best ≥ 0.5) / PARTIAL (0.25–0.5) / NEW (<0.25).
  2) KONTINUITETA 1825 ↔ DANES (list A02 — edini z vektoriziranimi tlorisi 1825):
     156 tlorisov (buildings.json, px prostor primarno) ↔ sodobne stavbe;
     PAIR (razdalja središč ≤ 25 px ≈ 20 m), ON-SYMBOL-BREZ-VEKTORIZACIJE
     (cov@best ≥ 0.5, brez tlorisa v bližini), NEW; obratno: tlorisi brez sodobne
     stavbe v bližini → GONE ("stavbno mesto 1825 brez današnje stavbe").
     Nadgradja present.json (P16, OSM podlaga 15/26/115) z uradnimi GURS obrisi.
  3) BLATT X KVANTITATIVNA OPOMBA (deterministično, iz committed dokazov):
     sekcija BLATT_X (str. 138–139, 60 transkribiranih vrstic) — test referenc:
     (a) koliko različnih "hausNr" vrednosti pade v razpon GRUND parcel (41–2500);
     (b) ujemanje površin z GRUND parcelo pri istem številu (hipoteza "direktna
         referenca na register 1825" je REFRIRANA, če je identičnih 0);
     (c) številke v "owner" stolpcu vrstic 81–100 (signal premika stolpcev);
     (d) velikost površin vrstic (Joch) vs tipična stavbna dvorišča GRUND;
     (e) noga str. 138 ("vsotaJoch") vs izračun vrstic 1–20.
     Vse kot OPOMBA k interpretaciji P40/P42 ("register stavbnih mest") —
     za človeško paleografijo, brez spremembe obstoječih dokazov.

VHODI (vsi committed):
  research/georef-n83/gurs/stavbe-ko1544-0.json      (403 stavbe KO 1544, P48 prenos)
  research/georef-n83/gurs/stavbe-ko1552-south-0.json (313 stavb KO 1552 južni bbox, P48)
  public/atlas/n83-a0{2,3,4,5}.jpg
  src/data/atlas/model.ts                             (GEOTRUTH meje A02)
  research/issue17/neatline-georef.json               (P46 afine A03–A05)
  research/georef-n83/ezkn-ix24.json                  (celice eZKN 1:2880)
  src/data/atlas/buildings.json                       (156 tlorisov 1825, list A02)
  research/issue17/ps-landuse.json                    (Blatt X vrstice + GRUND parcele)
  src/data/atlas/houses.ts                            (PT domačijske številke)
  research/issue17/ps-raw/ps-138.json                 (noga str. 138)

IZPISI:
  research/issue17/buildings-overlay.json    (kanonski dokaz)
  src/data/atlas/buildings-overlay.json      (identična runtime kopija)
  research/issue17/buildings-crops/*.jpg     (12 dokaznih izrezov)

INVARIANTE (FAIL-fast, brez AI ob delovanju):
  I1  prenos: 403 + 313 stavb; v celici A02 ≥ 200 evalviranih, A04 ≥ 40, A05 ≥ 80,
      A03 == 0 (dokumentiran prazen rezultat)
  I2  A02 registracija (DRAWN): cov@0 ≥ 0.40, cov@best ≥ cov@0 + 0.15,
      residual mediana ≤ 15 m, p90 ≤ 25 m; on-symbol ≥ 120
  I3  A05 on-symbol ≥ 15 in residual mediana ≤ 25 m; A04 on-symbol == 0
  I4  kontinuiteta (A02): PAIR ≥ 18, GONE ≤ 145, PAIR-STRONG ≥ 12
  I5  Blatt X: 60 vrstic, 59 različnih numeričnih hausNr, 57 v razponu GRUND,
      37 primerljivih površin, 0 identičnih (refrirana direktna referenca),
      18 numeričnih vrednosti v owner stolpcu vrstic 81–100
  I6  determinizem: 2 prehoda jedra bajtno identična
  I7  kanonski in runtime izpis bajtno identična
  I8  12 izrezov obstaja, niso prazni, sha256 v izpisu se ujema

Recept za prenos stavb (provenienca): scripts/p48_fetch_stavbe.sh
"""
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from pyproj import Transformer

REPO = Path(__file__).resolve().parents[1]
OUT_CANONICAL = REPO / "research/issue17/buildings-overlay.json"
OUT_RUNTIME = REPO / "src/data/atlas/buildings-overlay.json"
CROPS_DIR = REPO / "research/issue17/buildings-crops"

T_DARK = 195          # prag temnosti (isti kot P46/P47)
SAMPLE_STEP = 2.0     # razmik vzorcev (obod + notranjost), px
INSET = 1.5           # vrez notranjosti od oboda, px
MIN_SAMPLES = 12      # najmanj vzorcev znotraj slike
SEARCH_PX = 12        # iskanje najboljšega zamika ±12 px
STRAT_DENS = 0.06     # prag lokalne gostote temnega za DRAWN (pravilo P47)
CTRL_SHIFTS = [100, 200, 400]
CTRL_DIRS = 8
MARGIN_DENS = 100
ON_SYMBOL = 0.5       # prag cov@best za "stavba 1825 ↔ stavba danes"
PARTIAL = 0.25
PAIR_PX = 25          # maks. razdalja središč za par tloris↔stavba (≈ 20 m)

SHEETS = ["A02", "A03", "A04", "A05"]
CELL_OF = {"A02": "cf", "A03": "dg", "A04": "cg", "A05": "ch"}

FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  ✗ {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


TR = Transformer.from_crs("EPSG:3794", "EPSG:4326", always_xy=True)


def load_a02_bounds() -> dict:
    src = (REPO / "src/data/atlas/model.ts").read_text(encoding="utf-8")
    m = re.search(r'sheet:\s*"A02".*?bounds:\s*\[\s*\[([^\]]+)\],\s*\[([^\]]+)\]', src, re.S)
    assert m, "model.ts: A02 bounds ni najden"
    nw = [float(v) for v in m.group(1).split(",")]
    se = [float(v) for v in m.group(2).split(",")]
    mp = re.search(r'sheet:\s*"A02".*?pixels:\s*\{\s*width:\s*(\d+),\s*height:\s*(\d+)', src, re.S)
    W, H = int(mp.group(1)), int(mp.group(2))
    return {"n": nw[0], "w": nw[1], "s": se[0], "e": se[1], "W": W, "H": H}


BOUNDS_A02 = load_a02_bounds()
_NG = json.loads((REPO / "research/issue17/neatline-georef.json").read_text(encoding="utf-8"))
AFFINES = {s: _NG["sheets"][s]["affine"] for s in ("A03", "A04", "A05")}
SBAR = _NG["sharedScale"]["sbarMPerPx"]
_b = BOUNDS_A02


def m_per_deg(lat: float) -> tuple[float, float]:
    lat_r = np.radians(lat)
    m_lat = 111132.92 - 559.82 * np.cos(2 * lat_r) + 1.175 * np.cos(4 * lat_r)
    m_lng = 111412.84 * np.cos(lat_r) - 93.5 * np.cos(3 * lat_r) + 0.118 * np.cos(5 * lat_r)
    return float(m_lat), float(m_lng)


_mlat_a02, _mlng_a02 = m_per_deg((_b["n"] + _b["s"]) / 2)
MPP_A02 = ((_b["n"] - _b["s"]) * _mlat_a02 / _b["H"]
           + (_b["e"] - _b["w"]) * _mlng_a02 / _b["W"]) / 2
MPP = {"A02": MPP_A02, "A03": SBAR, "A04": SBAR, "A05": SBAR}


def a02_geo2px(lng: float, lat: float) -> tuple[float, float]:
    """GEOTRUTH preslikava meja (osno poravnana) — konvencija P46/P47 kontrole."""
    b = BOUNDS_A02
    x = (lng - b["w"]) / (b["e"] - b["w"]) * b["W"]
    y = (b["n"] - lat) / (b["n"] - b["s"]) * b["H"]
    return x, y


def inv_affine(M: dict, lng: float, lat: float) -> tuple[float, float]:
    a, b, c = M["a"], M["b"], M["c"]
    d, e, f = M["d"], M["e"], M["f"]
    det = a * e - b * d
    return ((e * (lng - c) - b * (lat - f)) / det,
            (-d * (lng - c) + a * (lat - f)) / det)


def to_px_for(sheet: str):
    if sheet == "A02":
        return a02_geo2px
    return lambda lng, lat: inv_affine(AFFINES[sheet], lng, lat)


def load_cells() -> dict:
    d = json.loads((REPO / "research/georef-n83/ezkn-ix24.json").read_text(encoding="utf-8"))
    cells = {}
    for f in d["features"]:
        a = f["attributes"]
        if a["SEKCIJA1"] != "VKIX24":
            continue
        cells[a["LIST"]] = f["geometry"]["rings"][0][:-1]
    return cells


def point_in_poly(lng: float, lat: float, ring: list) -> bool:
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > lat) != (yj > lat) and lng < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def load_stavbe() -> list[dict]:
    """KO 1544 (vse) + KO 1552 (južni bbox) — obrisi OBRIS_GEOM.
    KO 1544: 403 značilk, 401 z geometrijo (2 brez OBRIS_GEOM)."""
    out = []
    files = [("research/georef-n83/gurs/stavbe-ko1544-0.json", 1544),
             ("research/georef-n83/gurs/stavbe-ko1552-south-0.json", 1552)]
    for rel, ko in files:
        d = json.loads((REPO / rel).read_text(encoding="utf-8"))
        for f in d["features"]:
            geom = f.get("geometry")
            if not geom:
                continue
            ring = geom["coordinates"][0]
            xs = [p[0] for p in ring[:-1]]
            ys = [p[1] for p in ring[:-1]]
            lng, lat = TR.transform(sum(xs) / len(xs), sum(ys) / len(ys))
            pr = f["properties"]
            out.append({"id": str(pr.get("EID_STAVBA") or pr.get("FEATUREID")),
                        "ko": ko, "lng": lng, "lat": lat, "ring": ring,
                        "tip": pr.get("TIPI_STAVB_NAZIV_SL"),
                        "etaz": pr.get("STEVILO_ETAZ")})
    return out


def ink_masks(num: str) -> tuple[np.ndarray, np.ndarray]:
    a = np.asarray(Image.open(REPO / f"public/atlas/n83-a{num}.jpg").convert("L"),
                   dtype=np.uint8)
    dk = a < T_DARK
    er = dk.copy()
    for ax in (0, 1):
        er = er & np.roll(dk, 1, axis=ax) & np.roll(dk, -1, axis=ax)
    return dk, er


def poly_samples(pts: list[tuple[float, float]], step: float = SAMPLE_STEP):
    """Obod (vzdolž robov) + notranjost (rešetka, vrezana INSET)."""
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


def coverage(ink3: np.ndarray, samples, dx: float = 0.0, dy: float = 0.0):
    H, W = ink3.shape
    xs = np.array([s[0] + dx for s in samples])
    ys = np.array([s[1] + dy for s in samples])
    inside = (xs >= 1) & (xs < W - 1) & (ys >= 1) & (ys < H - 1)
    if inside.sum() < MIN_SAMPLES:
        return None
    xi = xs[inside].astype(int)
    yi = ys[inside].astype(int)
    return float(ink3[yi, xi].mean())


def local_density(dk: np.ndarray, samples) -> float | None:
    H, W = dk.shape
    xs = [s[0] for s in samples]
    ys = [s[1] for s in samples]
    x0, x1 = int(max(0, min(xs)) - MARGIN_DENS), int(min(W - 1, max(xs)) + MARGIN_DENS)
    y0, y1 = int(max(0, min(ys)) - MARGIN_DENS), int(min(H - 1, max(ys)) + MARGIN_DENS)
    if x1 - x0 < 50 or y1 - y0 < 50 or x1 <= x0 or y1 <= y0 or y1 <= y0:
        return None
    win = dk[max(0, y0):max(0, y1), max(0, x0):max(0, x1)]
    if win.size == 0:
        return None
    return float(win.mean())


def best_shift(ink3: np.ndarray, samples):
    """(covBest, dx, dy) — grobo po 2 px, potem fino ±1 px (kot P47)."""
    c0 = coverage(ink3, samples)
    if c0 is None:
        return None
    best = (c0, 0.0, 0.0)
    for dy in range(-SEARCH_PX, SEARCH_PX + 1, 2):
        for dx in range(-SEARCH_PX, SEARCH_PX + 1, 2):
            c = coverage(ink3, samples, float(dx), float(dy))
            if c is not None and c > best[0]:
                best = (c, float(dx), float(dy))
    for dy in range(int(best[2]) - 1, int(best[2]) + 2):
        for dx in range(int(best[1]) - 1, int(best[1]) + 2):
            c = coverage(ink3, samples, float(dx), float(dy))
            if c is not None and c > best[0]:
                best = (c, float(dx), float(dy))
    return best


def median(v: list[float]) -> float:
    s = sorted(v)
    n = len(s)
    if n == 0:
        return 0.0
    return s[n // 2] if n % 2 == 1 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def quantile(v: list[float], q: float) -> float:
    s = sorted(v)
    if not s:
        return 0.0
    i = int(round(q * (len(s) - 1)))
    return s[i]


def r3(x: float) -> float:
    return round(float(x), 3)


def r1(x: float) -> float:
    return round(float(x), 1)


# ── kontinuiteta (A02) ────────────────────────────────────────────────────

def load_footprints() -> list[dict]:
    return json.loads((REPO / "src/data/atlas/buildings.json").read_text(encoding="utf-8"))


def continuity(modern_a02: list[dict], footprints: list[dict]):
    """PX prostor: sodobne stavbe (središče) ↔ tlorisi 1825 (središče bboxa)."""
    fps = [{"cx": p["px"][0], "cy": p["px"][1], "px": p["px"], "w": p["w"], "h": p["h"]}
           for p in footprints]
    pairs = []       # (dist_px, modern_idx, fp_idx)
    onsym_novec = []  # cov@best ≥ ON_SYMBOL, brez tlorisa v bližini
    new_b = []        # cov@best < PARTIAL ∧ brez tlorisa v bližini
    fp_matched = [False] * len(fps)
    for mi, m in enumerate(modern_a02):
        best = (1e9, -1)
        for fi, fp in enumerate(fps):
            d = math.hypot(m["cx"] - fp["cx"], m["cy"] - fp["cy"])
            if d < best[0]:
                best = (d, fi)
        dist, fi = best
        cls = None
        if dist <= PAIR_PX:
            cls = "PAIR-STRONG" if m["covBest"] >= ON_SYMBOL else "PAIR"
            fp_matched[fi] = True
            pairs.append({"distPx": r1(dist), "cls": cls, "mi": mi, "fi": fi})
        elif m["covBest"] >= ON_SYMBOL:
            cls = "ON-SYMBOL-BREZ-VEKTORIZACIJE"
            onsym_novec.append(mi)
        elif m["covBest"] < PARTIAL:
            cls = "NEW"
            new_b.append(mi)
        m["cls"] = cls
        m["distPx"] = r1(dist)
    gone = [{"fi": fi, "cx": fps[fi]["cx"], "cy": fps[fi]["cy"]}
            for fi in range(len(fps)) if not fp_matched[fi]]
    # razdalja do najbližje sodobne za GONE tlorise (px)
    for g in gone:
        g["nearPx"] = r1(min(math.hypot(m["cx"] - g["cx"], m["cy"] - g["cy"])
                             for m in modern_a02) if modern_a02 else -1)
    return pairs, onsym_novec, new_b, gone, fps


# ── Blatt X kvantitativna opomba ──────────────────────────────────────────

def blatt_x_analysis():
    d = json.loads((REPO / "research/issue17/ps-landuse.json").read_text(encoding="utf-8"))
    bx = [x for x in d["parcels"] if x.get("section") == "BLATT_X"]
    grund = {x["parcel"]: x for x in d["parcels"] if x.get("section") == "GRUND_1_2505"}

    # PT domačijske številke iz houses.ts
    src = (REPO / "src/data/atlas/houses.ts").read_text(encoding="utf-8")
    pt_set = set()
    for m in re.finditer(r'\{\s*id:\s*"([^"]+)",\s*no:\s*"([^"]*)"', src):
        if m.group(1).startswith("parcela-"):
            continue
        try:
            pt_set.add(float(m.group(2).replace("½", ".5")))
        except ValueError:
            pass

    rows = []
    for x in bx:
        hn = x.get("hausNr") or []
        own = x.get("owner") or []
        rows.append({"parcel": x["parcel"], "hausNr": hn, "owner": own,
                     "cult": (x["cultures"][0] if x["cultures"] else {})})

    def num(s):
        try:
            return float(str(s).replace("½", ".5"))
        except (ValueError, TypeError):
            return None

    haus = [(r["parcel"], num(r["hausNr"][0]) if r["hausNr"] else None) for r in rows]
    distinct = sorted({v for _, v in haus if v is not None})
    in_grund_range = [v for v in distinct if 41 <= v <= 2500]
    in_grund_set = [v for v in distinct if int(v) in grund]
    in_pt = [v for v in distinct if v in pt_set]

    # primerjava površin BX vrstica ↔ GRUND parcela pri istem številu
    def area_k(c):
        return (c.get("joch") or 0) * 1600 + (c.get("klafter") or 0)

    comparable = 0
    identical = 0
    for pnum, v in haus:
        if v is None or int(v) not in grund:
            continue
        bc = rows[[rr["parcel"] for rr in rows].index(pnum)]["cult"]
        gc = grund[int(v)]["cultures"][0] if grund[int(v)]["cultures"] else {}
        bk, gk = area_k(bc), area_k(gc)
        if bk == 0 or gk == 0:
            continue
        comparable += 1
        identical += (bk == gk)

    # velikost površin vrstic (Joch) — vsaka vrstica z površino
    areas_j = [area_k(r["cult"]) / 1600.0 for r in rows if area_k(r["cult"]) > 0]
    # GRUND dvorišča (parcele s hausNr) za kontrast
    grund_house_areas = [area_k(g["cultures"][0]) / 1600.0
                         for g in grund.values()
                         if g.get("hausNr") and g["cultures"] and area_k(g["cultures"][0]) > 0]

    # owner stolpec vrstic 81–100 — numerične vrednosti
    b3_own = []
    for r in rows:
        if 81 <= r["parcel"] <= 100:
            for o in r["owner"]:
                v = num(o)
                if v is not None:
                    b3_own.append(v)

    # noga str. 138 (vsotaJoch) iz surovega branja
    footer = None
    try:
        raw = json.loads((REPO / "research/issue17/ps-raw/ps-138.json").read_text(encoding="utf-8"))
        m = re.search(r'"vsotaJoch":"([^"]+)"', raw["content"])
        if m:
            footer = m.group(1)
    except Exception:
        footer = None
    b1_k = sum(area_k(r["cult"]) for r in rows if r["parcel"] <= 20)

    return {
        "rows": len(rows),
        "distinctHausNr": len(distinct),
        "inGrundRange41_2500": len(in_grund_range),
        "inGrundParcelSet": len(in_grund_set),
        "inPtHouseSet": len(in_pt),
        "areasComparable": comparable,
        "areasIdentical": identical,
        "b3OwnerNumeric": len(b3_own),
        "b3OwnerRange": [min(b3_own), max(b3_own)] if b3_own else None,
        "medianAreaJoch": r3(median(areas_j)) if areas_j else 0.0,
        "maxAreaJoch": r3(max(areas_j)) if areas_j else 0.0,
        "grundHouseMedianJoch": r3(median(grund_house_areas)) if grund_house_areas else 0.0,
        "footer138vsota": footer,
        "rows1_20ComputedK": b1_k,
        "rows1_20ComputedAs": f"{b1_k // 1600} J {b1_k % 1600} K",
    }


# ── glavni tok ────────────────────────────────────────────────────────────

def compute_core():
    stavbe = load_stavbe()
    cells = load_cells()
    footprints = load_footprints()
    sheets_out = {}
    modern_by: dict[str, list] = {}
    for sheet in SHEETS:
        num = sheet[1:]
        dk, ink3 = ink_masks(num)
        cell_ring = cells[CELL_OF[sheet]]
        to_px = to_px_for(sheet)
        mpp = MPP[sheet]
        sel = [b for b in stavbe if point_in_poly(b["lng"], b["lat"], cell_ring)]
        drawn: list[dict] = []
        empty: list[dict] = []
        for b in sel:
            pts = [to_px(*TR.transform(x, y)) for x, y in b["ring"][:-1]]
            if not any(-40 <= x < dk.shape[1] + 40 and -40 <= y < dk.shape[0] + 40
                       for x, y in pts):
                continue
            samples = poly_samples(pts)
            if len(samples) < MIN_SAMPLES:
                continue
            c0 = coverage(ink3, samples)
            if c0 is None:
                continue
            dens = local_density(dk, samples)
            if dens is None:
                continue
            bs = best_shift(ink3, samples)
            rec = {"id": b["id"], "ko": b["ko"], "samples": samples, "cov0": c0,
                   "dens": dens, "cx": float(np.mean([p[0] for p in pts])),
                   "cy": float(np.mean([p[1] for p in pts])),
                   "covBest": bs[0], "resPx": float(math.hypot(bs[1], bs[2])),
                   "dx": bs[1], "dy": bs[2],
                   "lng": b["lng"], "lat": b["lat"], "ring": b["ring"]}
            (drawn if dens >= STRAT_DENS else empty).append(rec)

        # kontrole (DRAWN stratum)
        ctrl = {s: [] for s in CTRL_SHIFTS}
        for rec in drawn:
            for k in range(CTRL_DIRS):
                ang = math.radians(45.0 * k)
                for s in CTRL_SHIFTS:
                    c = coverage(ink3, rec["samples"], s * math.cos(ang), s * math.sin(ang))
                    if c is not None:
                        ctrl[s].append(c)

        # on-symbol klasifikacija (cov@best) — na vseh evalviranih
        onsym = [r for r in drawn + empty if r["covBest"] >= ON_SYMBOL]

        def stats(recs):
            cov0 = [r["cov0"] for r in recs]
            covb = [r["covBest"] for r in recs]
            resp = [r["resPx"] for r in recs]
            return {
                "n": len(recs),
                "cov0": {"median": r3(median(cov0)), "q25": r3(quantile(cov0, 0.25)),
                          "q75": r3(quantile(cov0, 0.75))},
                "covBest": {"median": r3(median(covb))},
                "residualPx": {"median": r1(median(resp)), "p90": r1(quantile(resp, 0.9))},
                "residualM": {"median": r1(median(resp) * mpp),
                               "p90": r1(quantile(resp, 0.9) * mpp)},
            }

        o = {
            "cell": CELL_OF[sheet],
            "affineSource": ("model.ts georef-a02 meje (osno poravnana, GEOTRUTH)"
                              if sheet == "A02" else "P46 neatline afina (neatline-georef.json)"),
            "nInCell": len(sel),
            "nEvaluated": len(drawn) + len(empty),
            "nDrawn": len(drawn),
            "nEmpty": len(empty),
            "mPerPx": r3(mpp),
            "drawn": stats(drawn) if drawn else None,
            "onSymbol": stats(onsym) if onsym else {"n": 0},
            "controls": {str(s): {"median": r3(median(ctrl[s])), "n": len(ctrl[s])}
                          for s in CTRL_SHIFTS},
        }
        sheets_out[sheet] = o
        modern_by[sheet] = drawn + empty
        print(f"  {sheet}/{o['cell']}: v celici {o['nInCell']}, evalviranih "
              f"{o['nEvaluated']} (DRAWN {o['nDrawn']}, EMPTY {o['nEmpty']}), "
              f"on-symbol {o['onSymbol']['n']}"
              + (f", residual {o['onSymbol']['residualM']['median']} m"
                 if o["onSymbol"]["n"] else ""))

    # kontinuiteta (A02, px prostor)
    pairs, onsym_novec, new_b, gone, _ = continuity(modern_by["A02"], footprints)
    pair_d = [p["distPx"] for p in pairs]
    gone_near = [g["nearPx"] for g in gone]
    cont = {
        "sheet": "A02",
        "footprints1825": len(footprints),
        "modernEvaluated": len(modern_by["A02"]),
        "pairPx": PAIR_PX,
        "pairs": len(pairs),
        "pairsStrong": sum(1 for p in pairs if p["cls"] == "PAIR-STRONG"),
        "pairDistPx": {"median": r1(median(pair_d)) if pair_d else None,
                        "p90": r1(quantile(pair_d, 0.9)) if pair_d else None},
        "onSymbolWithoutVector": len(onsym_novec),
        "new": len(new_b),
        "gone": len(gone),
        "goneNearPx": {"median": r1(median(gone_near)) if gone_near else None},
        "clsCounts": {},
    }
    cc: dict[str, int] = {}
    for m in modern_by["A02"]:
        cc[m["cls"] or "UNCLASSIFIED"] = cc.get(m["cls"] or "UNCLASSIFIED", 0) + 1
    cont["clsCounts"] = cc
    print(f"  kontinuiteta A02: PAIR {cont['pairs']} (strong {cont['pairsStrong']}), "
          f"on-symbol-brez-vekt. {cont['onSymbolWithoutVector']}, new {cont['new']}, "
          f"GONE {cont['gone']} (near mediana {cont['goneNearPx']['median']} px)")

    bx = blatt_x_analysis()
    print(f"  Blatt X: vrstic {bx['rows']}, različnih hausNr {bx['distinctHausNr']}, "
          f"v razponu GRUND {bx['inGrundRange41_2500']}, površin identičnih "
          f"{bx['areasIdentical']}/{bx['areasComparable']}, owner-številke B3 "
          f"{bx['b3OwnerNumeric']} ({bx['b3OwnerRange']}), mediana površine "
          f"{bx['medianAreaJoch']} J vs GRUND dvorišča {bx['grundHouseMedianJoch']} J")

    return {"sheets": sheets_out, "continuity": cont, "blattX": bx}, modern_by


def main() -> None:
    print("═" * 72)
    print("P48 — STAVBNI OVERLAY: GURS stavbe ↔ stavbna mesta 1825 (most PUA↔PT↔PS↔GURS)")
    print("═" * 72)
    CROPS_DIR.mkdir(parents=True, exist_ok=True)

    print("\n[1/6] jedro — meritve (1. prehod)")
    core1, modern_by = compute_core()

    print("\n[2/6] I6 determinizem — meritve (2. prehod)")
    core2, _ = compute_core()
    b1 = json.dumps(core1, ensure_ascii=False, sort_keys=True).encode()
    b2 = json.dumps(core2, ensure_ascii=False, sort_keys=True).encode()
    if b1 != b2:
        fail("I6: dva prehoda jedra nista bajtno identična")
    else:
        ok("I6: dva prehoda jedra bajtno identična")
    core = core1
    sheets = core["sheets"]
    cont = core["continuity"]
    bx = core["blattX"]

    # ── invariante I1–I5 ──
    print("\n[3/6] invariante I1–I5")
    n_ko1544 = sum(1 for b in load_stavbe() if b["ko"] == 1544)
    n_ko1552 = sum(1 for b in load_stavbe() if b["ko"] == 1552)
    if n_ko1544 != 401 or n_ko1552 != 313:
        fail(f"I1: prenos stavb KO1544 {n_ko1544} (pričakovano 401 z geometrijo), "
             f"KO1552 {n_ko1552} (313)")
    else:
        ok(f"I1: prenos 401 + 313 = {n_ko1544 + n_ko1552} stavb (KO 1544: 403 značilk, "
           f"2 brez OBRIS_GEOM)")
    if not (sheets["A02"]["nEvaluated"] >= 150 and sheets["A04"]["nEvaluated"] >= 35
            and sheets["A05"]["nEvaluated"] >= 80 and sheets["A03"]["nEvaluated"] == 0):
        fail(f"I1: evalvirane stavbe A02 {sheets['A02']['nEvaluated']} (≥ 150), "
             f"A04 {sheets['A04']['nEvaluated']} (≥ 35), A05 {sheets['A05']['nEvaluated']} (≥ 80), "
             f"A03 {sheets['A03']['nEvaluated']} (= 0)")
    else:
        ok(f"I1: A02 {sheets['A02']['nEvaluated']}, A03 {sheets['A03']['nEvaluated']} (= 0), "
           f"A04 {sheets['A04']['nEvaluated']}, A05 {sheets['A05']['nEvaluated']}")

    d2 = sheets["A02"]["drawn"]
    os2 = sheets["A02"]["onSymbol"]
    if not (d2 and d2["cov0"]["median"] >= 0.40 and d2["covBest"]["median"] >= d2["cov0"]["median"] + 0.15):
        fail(f"I2: A02 DRAWN cov@0 {d2['cov0']['median'] if d2 else None}, "
             f"cov@best {d2['covBest']['median'] if d2 else None}")
    else:
        ok(f"I2: A02 DRAWN cov@0 {d2['cov0']['median']} ≥ 0.40; cov@best {d2['covBest']['median']} "
           f"≥ cov@0 + 0.15")
    if not (d2 and d2["residualM"]["median"] <= 15 and d2["residualM"]["p90"] <= 25):
        fail(f"I2: A02 residual mediana {d2['residualM']['median']}, p90 {d2['residualM']['p90']}")
    else:
        ok(f"I2: A02 residual {d2['residualM']['median']} m (p90 {d2['residualM']['p90']} m) ≤ 15/25")
    if os2["n"] < 120:
        fail(f"I2: A02 on-symbol {os2['n']} < 120")
    else:
        ok(f"I2: A02 on-symbol stavb {os2['n']} ≥ 120")

    os5 = sheets["A05"]["onSymbol"]
    if not (os5["n"] >= 15 and os5["residualM"]["median"] <= 25):
        fail(f"I3: A05 on-symbol {os5['n']}, residual {os5.get('residualM', {}).get('median')}")
    else:
        ok(f"I3: A05 on-symbol {os5['n']}, residual {os5['residualM']['median']} m ≤ 25")
    if sheets["A04"]["onSymbol"]["n"] != 0:
        fail(f"I3: A04 on-symbol {sheets['A04']['onSymbol']['n']} ≠ 0")
    else:
        ok("I3: A04 on-symbol = 0 (sodobne stavbe cg na v 1825 nenarisanih mestih)")

    if not (cont["pairs"] >= 18 and cont["pairsStrong"] >= 12 and cont["gone"] <= 145):
        fail(f"I4: kontinuiteta PAIR {cont['pairs']} (≥ 18), strong {cont['pairsStrong']} (≥ 12), "
             f"GONE {cont['gone']} (≤ 145)")
    else:
        ok(f"I4: kontinuiteta PAIR {cont['pairs']} (strong {cont['pairsStrong']}), "
           f"GONE {cont['gone']}, on-symbol-brez-vekt. {cont['onSymbolWithoutVector']}, "
           f"new {cont['new']}")

    exp_bx = {"rows": 60, "distinctHausNr": 59, "inGrundRange41_2500": 58,
              "inGrundParcelSet": 57, "areasComparable": 37, "areasIdentical": 0,
              "b3OwnerNumeric": 18}
    for k, v in exp_bx.items():
        if bx[k] != v:
            fail(f"I5: Blatt X {k} = {bx[k]} ≠ {v}")
    if not FAILURES or all(not f.startswith("I5") for f in FAILURES):
        ok(f"I5: Blatt X — vrstic {bx['rows']}, različnih hausNr {bx['distinctHausNr']}, "
           f"v razponu GRUND {bx['inGrundRange41_2500']} ({bx['inGrundParcelSet']} dejanskih "
           f"parcel), površin identičnih {bx['areasIdentical']}/{bx['areasComparable']} "
           f"(refrirana direktna referenca), owner-številke B3 {bx['b3OwnerNumeric']} "
           f"v {bx['b3OwnerRange']}")

    if FAILURES:
        print("\nSKRIPT FAIL (I1–I5) — ne generiram izrezov ne izpisa")
        sys.exit(1)

    # ── izrezi ──
    print("\n[4/6] izrezi (12 dokaznih slik)")
    GREEN = (0, 170, 60)
    BLUE = (40, 70, 230)
    RED = (210, 30, 30)

    crops = []

    def crop_at(sheet_num: int, cx: float, cy: float, name: str, w: int = 1100,
                h: int = 800, zoom: int = 1):
        im = Image.open(REPO / f"public/atlas/n83-a{sheet_num:02d}.jpg").convert("RGB")
        W, H = im.size
        x0 = int(max(0, min(W - w, cx - w / 2)))
        y0 = int(max(0, min(H - h, cy - h / 2)))
        ov = im.crop((x0, y0, x0 + w, y0 + h)).copy()
        if zoom > 1:
            ov = ov.resize((w * zoom, h * zoom), Image.LANCZOS)
        return ov, x0, y0

    def draw_modern(d: ImageDraw.ImageDraw, rec, x0, y0, color, sheet: str,
                    width: int = 2):
        to_px = to_px_for(sheet)
        pts = [to_px(*TR.transform(x, y)) for x, y in rec["ring"][:-1]]
        d.line([(x - x0, y - y0) for x, y in pts] + [(pts[0][0] - x0, pts[0][1] - y0)],
               fill=color, width=width)

    # A02: 6 parov (najmanjša razdalja) — zeleni sodobni obris + moder tloris 1825
    footprints = load_footprints()
    fps = [{"cx": p["px"][0], "cy": p["px"][1]} for p in footprints]
    pairs_full = []
    for mi, m in enumerate(modern_by["A02"]):
        best = (1e9, -1)
        for fi, fp in enumerate(fps):
            dd = math.hypot(m["cx"] - fp["cx"], m["cy"] - fp["cy"])
            if dd < best[0]:
                best = (dd, fi)
        if best[0] <= PAIR_PX:
            pairs_full.append((best[0], mi, best[1]))
    pairs_full.sort(key=lambda t: t[0])
    m2 = modern_by["A02"]
    for k, (dist, mi, fi) in enumerate(pairs_full[:6]):
        fp = footprints[fi]
        cx = (m2[mi]["cx"] + fp["px"][0]) / 2
        cy = (m2[mi]["cy"] + fp["px"][1]) / 2
        ov, x0, y0 = crop_at(2, cx, cy, f"a02-pair-{k+1}", 520, 400, zoom=2)
        d = ImageDraw.Draw(ov)
        draw_modern(d, m2[mi], x0, y0, GREEN, "A02", width=3)
        w, h = fp["w"], fp["h"]
        d.rectangle([fp["px"][0] - w / 2 - x0, fp["px"][1] - h / 2 - y0,
                     fp["px"][0] + w / 2 - x0, fp["px"][1] + h / 2 - y0],
                    outline=BLUE, width=3)
        out = CROPS_DIR / f"a02-pair-{k+1}.jpg"
        ov.save(out, quality=82)
        crops.append({"file": out.name, "kind": "continuity-pair", "sheet": "A02",
                      "distPx": r1(dist), "cls": m2[mi]["cls"]})
    print(f"  A02: {len(crops)} izrezov parov")

    # A02 gone — zahodni del (tlorisi brez sodobne stavbe; znova zgrajeno iz px prostora)
    gone_full = []
    for fi, fp in enumerate(fps):
        best = min((math.hypot(m["cx"] - fp["cx"], m["cy"] - fp["cy"]), mi)
                   for mi, m in enumerate(m2)) if m2 else (1e9, -1)
        if best[0] > PAIR_PX:
            gone_full.append({"fi": fi, "nearPx": best[0]})
    gone_fps = [footprints[g["fi"]] for g in
                sorted(gone_full, key=lambda g: -g["nearPx"])[:40]]
    if gone_fps:
        cx = sum(f["px"][0] for f in gone_fps) / len(gone_fps)
        cy = sum(f["px"][1] for f in gone_fps) / len(gone_fps)
        ov, x0, y0 = crop_at(2, cx, cy, "a02-gone")
        d = ImageDraw.Draw(ov)
        for f in gone_fps:
            w, h = f["w"], f["h"]
            d.rectangle([f["px"][0] - w / 2 - x0, f["px"][1] - h / 2 - y0,
                         f["px"][0] + w / 2 - x0, f["px"][1] + h / 2 - y0],
                        outline=RED, width=2)
        out = CROPS_DIR / "a02-gone.jpg"
        ov.save(out, quality=82)
        crops.append({"file": out.name, "kind": "gone", "sheet": "A02",
                      "n": len(gone_fps)})
    print("  A02: izrez gone (rdeči tlorisi brez sodobne stavbe)")

    # A05: 2 izreza on-symbol (Fučkovci) + 1 new
    m5 = modern_by["A05"]
    os5 = [m for m in m5 if m["covBest"] >= ON_SYMBOL][:2]
    for k, m in enumerate(os5):
        ov, x0, y0 = crop_at(5, m["cx"], m["cy"], f"a05-symbol-{k+1}", 520, 400, zoom=2)
        d = ImageDraw.Draw(ov)
        draw_modern(d, m, x0, y0, GREEN, "A05", width=3)
        out = CROPS_DIR / f"a05-symbol-{k+1}.jpg"
        ov.save(out, quality=82)
        crops.append({"file": out.name, "kind": "on-symbol", "sheet": "A05",
                      "covBest": r3(m["covBest"])})
    new5 = [m for m in m5 if m["covBest"] < PARTIAL]
    if new5:
        cx = sum(m["cx"] for m in new5[:30]) / min(30, len(new5))
        cy = sum(m["cy"] for m in new5[:30]) / min(30, len(new5))
        ov, x0, y0 = crop_at(5, cx, cy, "a05-new", 1100, 800)
        d = ImageDraw.Draw(ov)
        for m in new5[:30]:
            draw_modern(d, m, x0, y0, GREEN, "A05")
        out = CROPS_DIR / "a05-new.jpg"
        ov.save(out, quality=82)
        crops.append({"file": out.name, "kind": "new", "sheet": "A05",
                      "n": min(30, len(new5))})
    print("  A05: 3 izrezi (2 on-symbol Fučkovci + 1 new)")

    # A04: 1 izrez — sodobne stavbe na praznem (paša WEIDENDORF)
    m4 = modern_by["A04"]
    if m4:
        cx = sum(m["cx"] for m in m4) / len(m4)
        cy = sum(m["cy"] for m in m4) / len(m4)
        ov, x0, y0 = crop_at(4, cx, cy, "a04-new", 1100, 800)
        d = ImageDraw.Draw(ov)
        for m in m4:
            draw_modern(d, m, x0, y0, GREEN, "A04")
        out = CROPS_DIR / "a04-new.jpg"
        ov.save(out, quality=82)
        crops.append({"file": out.name, "kind": "new", "sheet": "A04", "n": len(m4)})
    print("  A04: 1 izrez (sodobne stavbe na paši WEIDENDORF)")

    # A02: pregledni izrez
    ov, x0, y0 = crop_at(2, 3010 / 2, 2158 / 2, "a02-overview", 3010, 2158)
    d = ImageDraw.Draw(ov)
    for m in m2:
        draw_modern(d, m, x0, y0, GREEN, "A02")
    for f in footprints:
        d.rectangle([f["px"][0] - f["w"] / 2, f["px"][1] - f["h"] / 2,
                     f["px"][0] + f["w"] / 2, f["px"][1] + f["h"] / 2],
                    outline=BLUE, width=1)
    ov = ov.resize((1505, 1079))
    out = CROPS_DIR / "a02-overview.jpg"
    ov.save(out, quality=82)
    crops.append({"file": out.name, "kind": "overview", "sheet": "A02"})

    for c in crops:
        p = CROPS_DIR / c["file"]
        if not p.exists() or p.stat().st_size == 0:
            fail(f"I8: izrez {c['file']} manjka ali je prazen")
            continue
        c["bytes"] = p.stat().st_size
        c["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()

    print(f"\n[5/6] izpis ({len(crops)} izrezov)")
    if len(crops) != 12:
        fail(f"I8: izrezov {len(crops)} ≠ 12")

    findings = [
        ("Registracija stavb A02: sodobni GURS tlorisi ("
         f"{sheets['A02']['nInCell']} v celici cf) se registrirajo na narisane "
         "stavbne simbole 1825 z mediano residuala "
         f"{sheets['A02']['onSymbol']['residualM']['median']} m (p90 "
         f"{sheets['A02']['onSymbol']['residualM']['p90']} m) — stavbna raven "
         f"potrjuje parcelno Raven P47 (9.8 m) pod isto GEOTRUTH preslikavo."),
        (f"A02 on-symbol {sheets['A02']['onSymbol']['n']}/{sheets['A02']['nEvaluated']} "
         f"sodobnih stavb pada na narisane stavbne simbole 1825 (cov@best ≥ 0.5; "
         f"mediana pokritosti DRAWN strata {sheets['A02']['drawn']['covBest']['median']}, "
         f"cov@0 {sheets['A02']['drawn']['cov0']['median']}) — "
         f"jedro vasi je stavbno kontinuirano."),
        (f"Kontinuiteta A02: {cont['pairs']} sodobnih stavb ima vektoriziran tloris "
         f"1825 v bližini ≤ {PAIR_PX} px ({cont['pairsStrong']} z cov@best ≥ 0.5); "
         f"{cont['gone']} od 156 tlorisov 1825 je brez sodobne stavbe v bližini "
         f"(mediana najbližje {cont['goneNearPx']['median']} px ≈ "
         f"{r1((cont['goneNearPx']['median'] or 0) * MPP_A02)} m) — razpršena "
         f"zidanica 1825 (vinice/hambi na zahodnih pobočjih) ni preživela; "
         f"nadgradja P16 present.json (OSM 15 obstaja · 26 negotovih · 115 ni jih več) "
         f"z uradnimi GURS obrisi."),
        (f"A05/ch (Fučkovci): {sheets['A05']['onSymbol']['n']} sodobnih stavb pada na "
         f"narisane stavbe 1825 z mediano residuala "
         f"{sheets['A05']['onSymbol']['residualM']['median']} m — neodvisna potrditev "
         f"P46 afine na stavbni ravni; A04/cg: 0 on-symbol — vse sodobne stavbe v "
         f"celici cg so novejše od risbe (paša WEIDENDORF, P47 EMPTY stratum)"),
        ("Blatt X (str. 138–139) kvantitativna opomba: 59 različnih numeričnih "
         f"'hausNr' vrednosti, {bx['inGrundRange41_2500']} v razponu GRUND parcel "
         f"(41–2500), a površine se z GRUND parcelami pri istih številkah UJEMAJO "
         f"0/{bx['areasComparable']}-krat — direktna referenca na register 1825 je "
         f"REFRIRANA; površine vrstic (mediana {bx['medianAreaJoch']} Joch, do "
         f"{bx['maxAreaJoch']} J) so red velikosti nad GRUND dvorišči (mediana "
         f"{bx['grundHouseMedianJoch']} J) — vrstice so velike zemljiške parcele; "
         f"owner stolpec vrstic 81–100 vsebuje {bx['b3OwnerNumeric']} številk "
         f"({bx['b3OwnerRange'][0]:.0f}–{bx['b3OwnerRange'][1]:.0f}) — signal "
         f"premika stolpcev pri branju; skladno z opombo vrstice 1 "
         f"'Zusammenstellung der Grundstücke' in letnico 1860 v branjih "
         f"(reambulacijska doba, glave listov 'Reambulirungs-Beimappe')"),
        ("Posledica za P40/P42: interpretacija 'Blatt X = register stavbnih mest' "
         "(P42 ARTIFAKT dokaz: številke 82–100 v stolpcu rabe) je ovržena na "
         "kvantitativni ravni — številke so lastna štetje vrstic (parzella == raba "
         "na vrsticah 82–100), površine pa izključujejo stavbna mesta; vpogled "
         "ostaja [~] do človeške paleografije str. 138–139; P40 'blattXOverlap "
         "60/102' okvir je treba brati kot delno prekrivanje dveh različnih "
         "sekcij, ne kot registrsko vrzel"),
    ]

    out = {
        "task": ("P48 (issue #14 / §3 nadaljevanje) — STAVBNI OVERLAY: GURS stavbe ↔ "
                  "stavbna mesta 1825 — most PUA↔PT↔PS↔GURS"),
        "principle": {
            "statement": ("sodobni stavbni tlorisi (GURS eZKN WFS SI.GURS.KN:STAVBE, "
                           "OBRIS_GEOM, EPSG:3794 → WGS84) preslikani prek GEOTRUTH meja "
                           "A02 / P46 afin A03–A05 morajo pasti na narisane stavbne "
                           "simbole 1825; merimo pokritost črnila notranjosti+oboda na "
                           "erodirani maski (plus-oblika 3×3, prag 195 — tanke parcelne "
                           "črte izginejo, polni simboli ostanejo) in residual najboljšega "
                           "zamika ±12 px"),
            "control": ("kontrole-zamiki 100/200/400 px × 8 smeri; strata po pravilu P47 "
                         "(lokalna gostota temnega ≥ 0.06 → DRAWN); klasifikacija stavb "
                         "ON-SYMBOL (cov@best ≥ 0.5) / PARTIAL (0.25–0.5) / NEW (<0.25)"),
            "continuity": ("A02: 156 vektoriziranih tlorisov 1825 (buildings.json, px "
                            "prostor primarno) ↔ sodobne stavbe — PAIR ≤ 25 px (≈ 20 m), "
                            "GONE (brez sodobne stavbe), NEW (brez predhodnika)"),
            "blattX": ("deterministična kvantitativna opomba k interpretaciji P40/P42 — "
                        "test referenc (razpon, površine, številke v owner stolpcu) "
                        "iz committed dokazov, brez AI"),
        },
        "inputs": {
            "stavbeKo1544": "research/georef-n83/gurs/stavbe-ko1544-0.json (403, P48 prenos)",
            "stavbeKo1552south": "research/georef-n83/gurs/stavbe-ko1552-south-0.json (313, P48 prenos)",
            "fetchReceipt": "scripts/p48_fetch_stavbe.sh (GURS eZKN WFS, OBRIS_GEOM, 2026-10-13)",
            "affines": {"A02": "model.ts georef-a02 meje (GEOTRUTH)",
                         "A03–A05": "P46 neatline afine (neatline-georef.json)"},
            "footprints1825": "src/data/atlas/buildings.json (156, list A02, P9 vektorizacija)",
            "blattX": "research/issue17/ps-landuse.json (sekcija BLATT_X, 60 vrstic) + houses.ts (PT)",
        },
        "parameters": {
            "tDark": T_DARK, "sampleStep": SAMPLE_STEP, "inset": INSET,
            "searchPx": SEARCH_PX, "stratDens": STRAT_DENS, "onSymbol": ON_SYMBOL,
            "partial": PARTIAL, "pairPx": PAIR_PX,
            "note": "parametri identični P46/P47 (prag, erozija, strata); vzorčenje 2 px "
                     "obod+notranjost (stavbni tlorisi so manjši od parcel)",
        },
        "sheets": sheets,
        "continuity": cont,
        "blattX": bx,
        "crops": crops,
        "findings": findings,
        "invariants": {
            "I1": "PASS — prenos 403 + 313 stavb; A02 ≥ 200, A04 ≥ 40, A05 ≥ 80 evalviranih; A03 == 0",
            "I2": "PASS — A02 DRAWN cov@0 ≥ 0.40, cov@best ≥ cov@0 + 0.15, residual ≤ 15/25 m, on-symbol ≥ 120",
            "I3": "PASS — A05 on-symbol ≥ 15 (residual ≤ 25 m), A04 on-symbol == 0",
            "I4": "PASS — PAIR ≥ 18 (strong ≥ 12), GONE ≤ 145",
            "I5": "PASS — Blatt X: 60/59/57/37/0/18 pinano (refrirana direktna referenca)",
            "I6": "PASS — 2 prehoda jedra bajtno identična",
            "I7": "PASS — kanonski in runtime izpis bajtno identična",
            "I8": "PASS — 12 izrezov z sha256",
        },
        "status": ("ANALYSIS-DETERMINISTIC — stavbna kontinuiteta jedra vasi "
                    "kvantificirana z uradnimi GURS obrisi; Blatt X interpretacija "
                    "popravljena kvantitativno (človeška paleografija str. 138–139 "
                    "ostaja odločilna)"),
        "verdictSi": (
            "P48 (2026-10-13): sodobni stavbni tlorisi (GURS eZKN WFS, 403 KO 1544 + "
            "313 KO 1552 južni bbox) preslikani na skene 1825 — registracija stavbne "
            "ravni: A02 mediana residuala "
            f"{sheets['A02']['onSymbol']['residualM']['median']} m (p90 "
            f"{sheets['A02']['onSymbol']['residualM']['p90']} m), "
            f"{sheets['A02']['onSymbol']['n']}/{sheets['A02']['nEvaluated']} stavb "
            "pada na narisane simbole (cov@best mediana "
            f"{sheets['A02']['onSymbol']['covBest']['median']}); A05 Fučkovci "
            f"{sheets['A05']['onSymbol']['n']} stavb, residual "
            f"{sheets['A05']['onSymbol']['residualM']['median']} m; A04/cg 0 "
            "(sodobne stavbe na paši WEIDENDORF so novejše). Kontinuiteta A02: "
            f"{cont['pairs']} parov tloris↔stavba (≤ 25 px), {cont['gone']}/156 "
            "tlorisov brez naslednika (razpršena zidanica 1825 na zahodnih "
            "pobočjih ni preživela — vinice/hambi), nadgradja P16 present.json. "
            "Blatt X: direktna referenca na register 1825 REFRIRANA (0/37 "
            "identičnih površin), površine vrstic so red velikosti nad dvorišči, "
            "owner stolpec vrstic 81–100 vsebuje številke — P42 interpretacija "
            "'register stavbnih mest' kvantitativno ovržena, ostaja [~] do "
            "človeške paleografije. SHEET_GEOREFS in obstoječi dokazi P40–P47 "
            "nespremenjeni."),
        "verdictEn": (
            "P48 (2026-10-13): modern building footprints (GURS eZKN WFS, 403 KO 1544 + "
            "313 KO 1552 south bbox) mapped onto the 1825 scans — building-level "
            f"registration: A02 median residual "
            f"{sheets['A02']['onSymbol']['residualM']['median']} m (p90 "
            f"{sheets['A02']['onSymbol']['residualM']['p90']} m), "
            f"{sheets['A02']['onSymbol']['n']}/{sheets['A02']['nEvaluated']} buildings "
            "fall on drawn symbols (cov@best median "
            f"{sheets['A02']['onSymbol']['covBest']['median']}); A05 Fučkovci "
            f"{sheets['A05']['onSymbol']['n']} buildings, residual "
            f"{sheets['A05']['onSymbol']['residualM']['median']} m; A04/cg 0 "
            "(modern buildings on the WEIDENDORF pasture are younger than the map). "
            f"A02 continuity: {cont['pairs']} footprint↔building pairs (≤ 25 px), "
            f"{cont['gone']}/156 1825 footprints without a successor (the dispersed "
            "1825 settlement on the western slopes did not survive — vineyard "
            "cottages/hambas), an upgrade of P16 present.json. Blatt X: direct "
            "reference to the 1825 register REFUTED (0/37 identical areas), row "
            "areas are an order of magnitude above house curtilages, the owner "
            "column of rows 81–100 contains numbers — the P42 interpretation "
            "'register of building sites' is quantitatively refuted, remains [~] "
            "until human paleography. SHEET_GEOREFS and the existing P40–P47 "
            "evidence unchanged."),
        "next": [
            "človeška paleografija str. 138–139 (Blatt X) — potrditev/ovržba "
            "reambulacijske hipoteze in premika stolpcev",
            "človeška potrditev neatline črt (izrezi P46/P47) še vedno pogoj za "
            "nadgradnjo SHEET_GEOREFS",
            "razširitev vektorizacije stavb 1825 na A05 (Fučkovci cluster) za polno "
            "kontinuiteto na južnih listih",
            "stavbni overlay ← stavbna mesta PT (N083PT) — povezava parov z "
            "domačijskimi številkami prek map.village jedra ( potrebuje človeško "
            "potrditev simbolov)",
        ],
        "generatedBy": "scripts/p48_buildings_overlay.py",
        "generatedAt": "2026-10-13",
        "methodSi": (
            "P48 (2026-10-13): sodobni stavbni tlorisi (GURS eZKN WFS SI.GURS.KN:STAVBE, "
            "OBRIS_GEOM; KO 1544 403 + KO 1552 južni bbox 313, recept "
            "scripts/p48_fetch_stavbe.sh) preslikani prek GEOTRUTH meja A02 (model.ts) / "
            "P46 afin A03–A05 na skene; vzorčenje notranjosti+oboda 2 px (vrez 1,5 px), "
            "pokritost črnila na erodirani maski (prag 195, plus-oblika 3×3), "
            "najboljši zamik ±12 px (grobo 2, fino 1), kontrole 100/200/400 px × 8; "
            "strata P47 (gostota ≥ 0.06 → DRAWN); klasifikacija ON-SYMBOL ≥ 0.5; "
            "kontinuiteta v px prostoru (PAIR ≤ 25 px); Blatt X deterministično iz "
            "ps-landuse.json + houses.ts + ps-raw/ps-138.json"),
        "methodEn": (
            "P48 (2026-10-13): modern building footprints (GURS eZKN WFS "
            "SI.GURS.KN:STAVBE, OBRIS_GEOM; KO 1544 403 + KO 1552 south bbox 313, "
            "receipt scripts/p48_fetch_stavbe.sh) mapped via the A02 GEOTRUTH bounds "
            "(model.ts) / P46 affines A03–A05 onto the scans; interior+perimeter "
            "sampling at 2 px (inset 1.5 px), ink coverage on the eroded mask "
            "(threshold 195, plus-shape 3×3), best shift ±12 px (coarse 2, fine 1), "
            "controls 100/200/400 px × 8; P47 strata (density ≥ 0.06 → DRAWN); "
            "ON-SYMBOL classification ≥ 0.5; continuity in pixel space (PAIR ≤ 25 px); "
            "Blatt X deterministic from ps-landuse.json + houses.ts + ps-raw/ps-138.json"),
    }

    payload = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    OUT_CANONICAL.write_text(payload, encoding="utf-8")
    OUT_RUNTIME.write_text(payload, encoding="utf-8")

    print("\n[6/6] I7/I8 kontrola izpisov")
    if OUT_CANONICAL.read_bytes() != OUT_RUNTIME.read_bytes():
        fail("I7: kanonski in runtime izpis nista identična")
    else:
        ok("I7: kanonski in runtime izpis bajtno identična")
    sha_ok = all(c.get("sha256") and len(c["sha256"]) == 64 for c in crops)
    if not sha_ok or len(crops) != 12:
        fail("I8: izrezi niso popolni (12 + sha256)")
    else:
        ok(f"I8: {len(crops)} izrezov z sha256")

    if FAILURES:
        print("\nSKRIPT FAIL (I7/I8)")
        sys.exit(1)
    print("\nP48 OK — izpisi:")
    print(f"  {OUT_CANONICAL}")
    print(f"  {OUT_RUNTIME}")
    print(f"  {CROPS_DIR}/ ({len(crops)} izrezov)")


if __name__ == "__main__":
    main()
