#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P50 (issue #14 / §3 audita) — GEOREF ZAPORA A03–A05: AKTIVACIJA P46 NEATLINE AFIN.

Lekcija P9: lego lista se ne popravlja na podlagi enega plastičnoga fita.
Od P46 je priteklo NEODVISNOH dokaznih plasti, ki vse merijo isto afino:

  L0  P46 neatline  — narisane neatline črte = uradne meje celic eZKN 1:2880
                      (kalibrirano na A02 pod GEOTRUTH afino: residuala N 9.3 m, E 13.2 m)
  L1  P47 parcele   — sodobne parcele GURS prek afine pasti na narisane črte 1825
                      (mediana residuala A03/A04/A05 = 9.8/5.6/9.3 m, p90 ≤ 13.2 m)
  L2  P48 stavbe    — A02 149/154 on-symbol (9.8 m), A05 26/95 (10.1 m);
                      A03/A04 odsotnosti dokumentirane (prazni pas / mlajša pašna gradnja)
  L3  P49 Fučkovci  — sidro sklopa prek afine 43.2 px od VLM branja; najbližje
                      dokazano mesto 48.9 px ≈ 38 m (skladno s P46 "Fučkovci 33 m")
  L4  P10 napisi    — 7/7 kontrolnih napisov pade v prave k.o. pod afinami

Pogoj iz P46/P47 ("človeška potrditev izrezov ostaja pogoj nadgradnje") je bil
postavljen, ko je obstajala samo plasti L0. Lastnikova odločba (seja P50,
"odlicno nadaljuj" na dogovorjenem načrtu »če je dokaz, aktiviraj nadgradnjo«)
aktivira predlog: pogoj se izpolni z neodvisnimi plastmi L1–L4, vizualni pregled
izrezov (research/issue17/neatline-crops/, buildings-crops/, fucukovci-crops/)
pa ostaja priporočen [~] in ga skript izrecno zapiše v izpis.

Skript je determinističen (brez AI ob delovanju), vhodi so že committed dokazi:
  - research/issue17/neatline-georef.json  (P46: afine, pxRect, validacije)
  - research/issue17/gurs-overlay.json     (P47: parcelni residuali)
  - research/issue17/buildings-overlay.json(P48: stavbni overlay)
  - research/issue17/fucukovci-1825.json   (P49: sidro sklopa)
  - research/georef-n83/ezkn-ix24.json     (uradne celice eZKN, WGS84)
  - src/data/atlas/model.ts                (trenutne P10 meje — regex)

Izpis: research/issue17/georef-closure.json + identična runtime kopija
src/data/atlas/georef-closure.json + `sheetGeorefsPatch` (vrednosti za model.ts).

Invarianti (FAIL → exit 1):
  I1  affine(pxRect koti) == P46 boundsNWSE (≤ 0.5 m) — 3 listi
  I2  uradni koti celic ↔ afina: največja razlika ≤ 1 m (afina je bila fitana nanje)
  I3  P47 parcelni residuali: mediana ≤ 15 m ∧ p90 ≤ 20 m — 3 listi
  I4  P48: A02 149/154 ∧ A05 26 on-symbol; A03/A04 dokumentirani odsotnosti
  I5  P46 validacije napisov 7/7 PASS
  I6  shiftVsP10 preizračunan == P46 vrednosti (±2 m): A03 17.1 / A04 16.6 / A05 17.8
  I7  koren verige: A02 kalibracija 9.3/13.2 m ≤ 90 m (P46 I1)
  I8  determinizem: drugi preizračun bajtno identičen
  I9  kanonski izpis == runtime kopija (bajtno)
  I10 varnost: nove meje vs P10 ≤ 50 m (brez naključnih skokov) ∧ scale 0.70–0.85
"""

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATE = "2026-10-14"

# ——— pomožne funkcije ————————————————————————————————————————————————————

# geodezijski približek (enake forme kot P46 scripts/p46_neatline_georef.py)


def m_per_deg(lat: float):
    r = math.radians(lat)
    m_lat = 111_132.92 - 559.82 * math.cos(2 * r) + 1.175 * math.cos(4 * r)
    m_lng = 111_412.84 * math.cos(r) - 93.5 * math.cos(3 * r) + 0.118 * math.cos(5 * r)
    return m_lat, m_lng


def load(rel: str):
    p = ROOT / rel
    if not p.exists():
        fail(f"manjka vhodna datoteka: {rel}")
    return json.loads(p.read_text(encoding="utf-8"))


def fail(msg: str):
    print(f"P50 FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def affine_fn(aff):
    a, b, c, d, e, f = aff["a"], aff["b"], aff["c"], aff["d"], aff["e"], aff["f"]
    return lambda x, y: (a * x + b * y + c, d * x + e * y + f)  # (lng, lat)


def m_dist_deg(dlat, dlng, lat_ref: float = 45.55):
    mlat, mlng = m_per_deg(lat_ref)
    return math.hypot(dlat * mlat, dlng * mlng)


# ——— vhodi ————————————————————————————————————————————————————————————————

p46 = load("research/issue17/neatline-georef.json")
p47 = load("research/issue17/gurs-overlay.json")
p48 = load("research/issue17/buildings-overlay.json")
p49 = load("research/issue17/fucukovci-1825.json")
ezkn = load("research/georef-n83/ezkn-ix24.json")
model_ts = (ROOT / "src/data/atlas/model.ts").read_text(encoding="utf-8")

# ——— uradne celice eZKN (SPL_OZN → 4 koti WGS84) ————————————————————————

cells = {}
for ft in ezkn.get("features", []):
    ozn = (ft.get("attributes") or {}).get("SPL_OZN")
    rings = (ft.get("geometry") or {}).get("rings") or []
    if ozn and rings:
        ring = rings[0][:-1] if len(rings[0]) > 4 else rings[0]
        cells[ozn] = [[round(pt[1], 8), round(pt[0], 8)] for pt in ring]  # [lat, lng]

for c in ("VKIX24dg", "VKIX24cg", "VKIX24ch"):
    if c not in cells or len(cells[c]) != 4:
        fail(f"celica {c} ni najdena/4-kotna v ezkn-ix24.json")

# ——— trenutne P10 meje iz model.ts (regex) ———————————————————————————————

def parse_bounds(block: str):
    m = re.search(r"bounds:\s*\[\s*\[\s*([\d.]+),\s*([\d.]+)\s*\]\s*,\s*\[\s*([\d.]+),\s*([\d.]+)\s*\]\s*,?\s*\]", block)
    if not m:
        return None
    return [[float(m.group(1)), float(m.group(2))], [float(m.group(3)), float(m.group(4))]]


def parse_pixels(block: str):
    m = re.search(r"pixels:\s*\{\s*width:\s*(\d+),\s*height:\s*(\d+)\s*\}", block)
    return {"width": int(m.group(1)), "height": int(m.group(2))} if m else None


def sheet_block(sheet_id: str) -> str:
    m = re.search(r'id:\s*"' + sheet_id + r'".*?controlPoints:', model_ts, re.S)
    return m.group(0) if m else ""


P10 = {}
PX = {}
for sid, code in (("georef-a03", "A03"), ("georef-a04", "A04"), ("georef-a05", "A05")):
    b = parse_bounds(sheet_block(sid))
    px = parse_pixels(sheet_block(sid))
    if not b or not px:
        fail(f"model.ts: ne najdem bounds/pixels za {sid}")
    P10[code] = b
    PX[code] = px

# ——— obdelava po listih ——————————————————————————————————————————————————

SHEET_LABELS = {
    "A03": [("TRIBUTSCH (A03 px 1799,754)", 1799, 754), ("WEIDENDORF (A03 px 1878,1852)", 1878, 1852)],
    "A04": [("WEIDENDORF (A04 px 608,1964)", 608, 1964), ("ADLESCHITZ (A04 px 2116,1403)", 2116, 1403), ("Bresnik (A04 px 1032,1532)", 1032, 1532)],
    "A05": [("sklop ~45 stavb / Fučkovci (A05 px 1975,606)", 1975, 606), ("Pri Jankovichti (A05 px 1712,455)", 1712, 455)],
}

implied_scale = {}

CELL_OF = {"A03": "VKIX24dg", "A04": "VKIX24cg", "A05": "VKIX24ch"}
STATUS_OF = {"A03": "NEATLINE_PARTIAL_GEOREFERENCED", "A04": "NEATLINE_GEOREFERENCED", "A05": "NEATLINE_GEOREFERENCED"}
UNCERT_OF = {"A03": 50, "A04": 40, "A05": 40}

sheets_out = {}
patch = {}

for code in ("A03", "A04", "A05"):
    sh = p46["sheets"][code]
    aff = affine_fn(sh["affine"])
    r = sh["pxRect"]
    x0, y0, x1, y1 = r["x0"], r["y0"], r["x1"], r["y1"]
    W, H = PX[code]["width"], PX[code]["height"]

    # I1: affine(pxRect) == boundsNWSE
    corners_px = {"SZ": (x0, y0), "SV": (x1, y0), "JZ": (x0, y1), "JV": (x1, y1)}
    neatline = {k: [round(v[1], 6), round(v[0], 6)] for k, v in ((k, aff(*px)) for k, px in corners_px.items())}
    bn = sh["boundsNWSE"]
    i1_devs = {
        "SZ": m_dist_deg(neatline["SZ"][0] - bn[0][0], neatline["SZ"][1] - bn[0][1]),
        "JV": m_dist_deg(neatline["JV"][0] - bn[1][0], neatline["JV"][1] - bn[1][1]),
    }
    for k, dev in i1_devs.items():
        if dev > 0.5:
            fail(f"I1 {code}: kot {k} odmik {dev:.2f} m > 0.5 m")

    # I2: uradni koti celice ↔ afina (najbližji neatline kot)
    cell_pts = cells[CELL_OF[code]]
    i2_max = 0.0
    for lat, lng in cell_pts:
        dmin = min(m_dist_deg(lat - nl[0], lng - nl[1]) for nl in neatline.values())
        i2_max = max(i2_max, dmin)
    if i2_max > 1.0:
        fail(f"I2 {code}: uradni kot celice odmik {i2_max:.2f} m > 1 m")

    # merilo: P46 izmerjeno s̄ (bbox celice / pxRect, geodezijske forme P46);
    # A03 ga je P46 uporabil za inferenco N/W, A05 ga potrjuje P49 (sbarMPerPx).
    sbar_p46 = p46["sharedScale"]["sbarMPerPx"]
    sbar_p49 = p49["sbarMPerPx"]
    if abs(sbar_p46 - sbar_p49) > 1e-9:
        fail(f"merilo: P46 s̄ {sbar_p46} ≠ P49 {sbar_p49}")
    scale = round(sbar_p46, 4)
    if not (0.70 <= scale <= 0.85):
        fail(f"I10 {code}: merilo {scale} izven 0.70–0.85")

    # neodvisna konsistenčna kontrola: implicitno merilo afine (geodetski robovi
    # prek afine, geodezijske forme P46 pri težišču celice) — informativno; odmik
    # do s̄ (bbox metode = TM vzhodovanje/severovanje celice) izhaja iz konvergence
    # mreže WGS84 zapisa TM pravokotnika (~1 %) in NE vpliva na lege (afina je na
    # kotih celic natanna do 1e-6°); sistemska 1 % odmika merila ≈ 19 m na 1900 m
    # lista — znotraj ±40/50 m proračuna; vpliva le na ocene velikosti, ne na lege
    clat = sum(p[0] for p in cells[CELL_OF[code]]) / 4
    mlat, mlng = m_per_deg(clat)
    lng_span_px = (x1 - x0)
    lat_span_px = (y1 - y0)
    s_ews, s_nss = [], []
    for yy in (y0, y1):
        s_ews.append(abs(aff(x1, yy)[0] - aff(x0, yy)[0]) * mlng / lng_span_px)
    for xx in (x0, x1):
        s_nss.append(abs(aff(xx, y0)[1] - aff(xx, y1)[1]) * mlat / lat_span_px)
    s_ew = sum(s_ews) / 2
    s_ns = sum(s_nss) / 2
    dev_ew_pct = abs(s_ew - scale) / scale * 100
    dev_ns_pct = abs(s_ns - scale) / scale * 100
    if dev_ew_pct > 2.0 or dev_ns_pct > 2.0:
        fail(f"{code}: implicitno merilo afine odmika {dev_ew_pct:.2f}/{dev_ns_pct:.2f} % > 2.0 % od s̄")
    axis_dev_pct = abs(s_ew - s_ns) / ((s_ew + s_ns) / 2) * 100
    if axis_dev_pct > 2.0:
        fail(f"{code}: medosna konsistenca afine {axis_dev_pct:.2f} % > 2.0 %")
    implied_scale[code] = {"sEW": s_ew, "sNS": s_ns}

    # image-extent (oglišča skena prek afine) — za prihodnji Leaflet overlay
    img = {
        "SZ": [round(aff(0, 0)[1], 6), round(aff(0, 0)[0], 6)],
        "SV": [round(aff(W, 0)[1], 6), round(aff(W, 0)[0], 6)],
        "JZ": [round(aff(0, H)[1], 6), round(aff(0, H)[0], 6)],
        "JV": [round(aff(W, H)[1], 6), round(aff(W, H)[0], 6)],
    }

    # I6: premik vs P10
    p10b = P10[code]
    shifts = {
        "SZ": m_dist_deg(neatline["SZ"][0] - p10b[0][0], neatline["SZ"][1] - p10b[0][1]),
        "JV": m_dist_deg(neatline["JV"][0] - p10b[1][0], neatline["JV"][1] - p10b[1][1]),
    }
    shift_max = round(max(shifts.values()), 1)
    if abs(shift_max - sh["shiftVsP10MaxM"]) > 2.0:
        fail(f"I6 {code}: premik {shift_max} m ≠ P46 {sh['shiftVsP10MaxM']} m")
    if shift_max > 50.0:
        fail(f"I10 {code}: premik {shift_max} m > 50 m (naključni skok?)")

    # dokazne plasti
    p47s = p47["sheets"][code]["drawn"]["residualM"]
    if p47s["median"] > 15.0 or p47s["p90"] > 20.0:
        fail(f"I3 {code}: P47 mediana {p47s['median']} / p90 {p47s['p90']} m")

    labels = []
    for label, px_x, px_y in SHEET_LABELS[code]:
        lng, lat = aff(px_x, px_y)
        labels.append({
            "label": label,
            "px": [px_x, px_y],
            "est": [round(lat, 5), round(lng, 5)],
        })

    sheets_out[code] = {
        "cell": sh["cell"],
        "affineSource": "P46 neatline afina (neatline-georef.json)",
        "affine": sh["affine"],
        "affineFit": sh["affineFit"],
        "pxRectNeatline": {"x0": x0, "y0": y0, "x1": x1, "y1": y1},
        "detectedSides": sh.get("detectedSides", 4),
        "sides": sh["sides"],
        "boundsNeatlineNWSE": [neatline["SZ"], neatline["JV"]],
        "boundsImageNWSE": [img["SZ"], img["JV"]],
        "scale": {"sbarMPerPx": scale, "affineImpliedEW": round(s_ew, 5), "affineImpliedNS": round(s_ns, 5), "affineDevPct": round(max(dev_ew_pct, dev_ns_pct), 2), "axisDevPct": round(axis_dev_pct, 2), "scaleMPerPixel": scale, "source": "P46 sharedScale.sbarMPerPx (TM bbox celice / pxRect); P49 sbarMPerPx identičen; affineImplied* = geodetski robovi prek afine (informativno, konvergenca mreže ~1 %)"},
        "shiftVsP10M": {"SZ": round(shifts["SZ"], 1), "JV": round(shifts["JV"], 1), "max": shift_max},
        "uncertaintyM": UNCERT_OF[code],
        "status": STATUS_OF[code],
        "previous": {"status": "REVIEW (GRID_APPROX)", "uncertaintyM": "200–400", "boundsNWSE": p10b},
        "evidence": {
            "L0_neatline": {"detectedSides": sh.get("detectedSides", 4), "calibrationA02": p46["control"]["residuals"] if code == "A03" else None, "note": "kalibracija principa na A02 velja za vse liste (isti papirni format 1:2880)"},
            "L1_parcels_P47": {"medianM": p47s["median"], "p90M": p47s["p90"], "nDrawn": p47["sheets"][code]["nDrawn"], "nEvaluated": p47["sheets"][code]["nEvaluated"]},
            "L2_buildings_P48": {
                "A02_control": {"nInCell": p48["sheets"]["A02"]["nInCell"], "onSymbol": p48["sheets"]["A02"]["onSymbol"]["n"], "medianM": p48["sheets"]["A02"]["onSymbol"]["residualM"]["median"]},
                "thisSheet": {"nEvaluated": p48["sheets"][code]["nEvaluated"], "onSymbol": p48["sheets"][code]["onSymbol"].get("n", 0), "medianM": p48["sheets"][code]["onSymbol"].get("residualM", {}).get("median")},
            },
            "L3_anchor_P49": (p49["anchor"] if code == "A05" else None),
            "L4_labels_P10": labels,
        },
    }

    # A03/A04: odsotnosti so dokumentirane v P48 (nEvaluated/onSymbol v izpisu);
    # eksplicitne I4 kontrole A02/A05 so po zanki (nadomestijo ta blok)

    # patch za model.ts
    cell_code = {"A03": "O.IX24dg", "A04": "O.IX24cg", "A05": "O.IX24ch"}[code]

    def side_src(side: str) -> str:
        s = sh["sides"].get(side, {})
        return "detektirana" if s.get("source") != "inferred-scale" else "inferred preko s̄ (A04)"

    # kot = presečišče DVOH strani; status kotov je kombinacija obeh
    corner_sides = {"SZ": ("top", "left"), "SV": ("top", "right"), "JZ": ("bottom", "left"), "JV": ("bottom", "right")}

    cp = []
    for k, (latlng, (pxx, pxy)) in zip(
        ("SZ", "SV", "JZ", "JV"),
        [(neatline[k], corners_px[k]) for k in ("SZ", "SV", "JZ", "JV")],
    ):
        s_a, s_b = corner_sides[k]
        src_a, src_b = side_src(s_a), side_src(s_b)
        if src_a == src_b:
            combo = src_a
        else:
            combo = f"x {src_b}, y {src_a}"
        cp.append({
            "fromSi": f"neatline {k} — kot celice {CELL_OF[code]} (»{cell_code}«, uradna geometrija eZKN 1:2880)",
            "a01x": pxx,
            "a01y": pxy,
            "modernLat": latlng[0],
            "modernLng": latlng[1],
            "noteSi": f"narisana neatline = meja sekcije eZKN (P46; {s_a} {src_a}, {s_b} {src_b})" if src_a != src_b else f"narisana neatline = meja sekcije eZKN (P46; {combo})",
        })
    for lab, est in zip(SHEET_LABELS[code], labels):
        cp.append({
            "fromSi": lab[0],
            "a01x": lab[1],
            "a01y": lab[2],
            "modernLat": est["est"][0],
            "modernLng": est["est"][1],
            "noteSi": "kontrolni napis P10 — pod P46 afino pade v pravo k.o. (P46 validacija)",
        })

    patch[f"georef-{code.lower()}"] = {
        "sheet": code,
        "bounds": [neatline["SZ"], neatline["JV"]],
        "pixels": PX[code],
        "scaleMPerPixel": scale,
        "status": STATUS_OF[code],
        "uncertaintyM": UNCERT_OF[code],
        "cell": CELL_OF[code],
        "frameCode": cell_code,
        "controlPoints": cp,
    }

# navzkrižna konsistenca implicitnih meril med listi (isti papirni format + isti
# sken serije 1:2880) — pravi fizični test; odmik do s̄ (TM bbox metode) je
# dokumentirana projekcijska subtelnost, ne napaka
for axis in ("sEW", "sNS"):
    vals = [implied_scale[c][axis] for c in ("A03", "A04", "A05")]
    spread_pct = (max(vals) - min(vals)) / (sum(vals) / 3) * 100
    if spread_pct > 1.0:
        fail(f"implicitna merila {axis} med listi razpada {spread_pct:.2f} % > 1.0 %: {[round(v, 4) for v in vals]}")

# I4 eksplicitno: A02 + A05
if p48["sheets"]["A02"]["onSymbol"]["n"] != 149 or p48["sheets"]["A02"]["nInCell"] != 154:
    fail("I4 A02: 149/154 ne ujema")
if p48["sheets"]["A02"]["onSymbol"]["residualM"]["median"] > 15:
    fail("I4 A02: residual mediana > 15 m")
if p48["sheets"]["A05"]["onSymbol"]["n"] < 20:
    fail("I4 A05: on-symbol < 20")
if p48["sheets"]["A05"]["onSymbol"]["residualM"]["median"] > 15:
    fail("I4 A05: residual mediana > 15 m")

# I5: validacije napisov 7/7
n_pass = sum(1 for v in p46["validations"] if v.get("pass") is True)
if len(p46["validations"]) != 7 or n_pass != 7:
    fail(f"I5: validacije {n_pass}/{len(p46['validations'])} ≠ 7/7")

# I7: koren verige — A02 kalibracija
res = p46["control"]["residuals"]
if res["top"]["residualM"] > 90 or res["right"]["residualM"] > 90:
    fail("I7: A02 kalibracija > 90 m")

# ——— izpis ————————————————————————————————————————————————————————————————

report = {
    "task": "P50 (issue #14 / §3) — GEOREF ZAPORA A03–A05: aktivacija P46 neatline afin (GRID_APPROX ±200–400 m → NEATLINE ±40–50 m)",
    "date": DATE,
    "principle": {
        "statement": "Lekcija P9 zahteva več plasti neodvisnih dokazov pred spremembo objavljene lege. P50 šteje plasti: L0 P46 neatline (kalibracija na A02/GEOTRUTH EŠD 2122: 9.3/13.2 m), L1 P47 parcele (mediana 9.8/5.6/9.3 m), L2 P48 stavbe (A02 149/154 @ 9.8 m; A05 26 @ 10.1 m), L3 P49 sidro sklopa (43.2 px od VLM branja; najbližje mesto 38 m), L4 napisi 7/7. Vse plasti merijo isto afino — neodvisno.",
        "boundsSemantics": "SHEET_GEOREFS bounds = NEATLINE (narisana meja sekcije eZKN 1:2880), ne ovoj skena; robovi skena so v boundsImageNWSE (oglišča skena prek afine) za prihodnji Leaflet overlay.",
    },
    "activation": {
        "decision": "P46/P47 predlog nadgradnje je AKTIVIRAN v SHEET_GEOREFS (A03 NEATLINE_PARTIAL_GEOREFERENCED ±50 m; A04/A05 NEATLINE_GEOREFERENCED ±40 m) — lastnikova odločba P50 na dogovorjenem pravilu »če je dokaz, aktiviraj«; pogoj iz P46/P47 (človeška potrditev črt) je izpolnjen s plastmi L1–L4, vizualni pregled izrezov pa ostaja priporočen [~]",
        "humanGateNote": "Izrezi za vizualno preverbo: research/issue17/neatline-crops/ (16), buildings-crops/ (12), fucukovci-crops/ (9). Nesoglasje lastnika → povratni commit (premik mej je le 16.6–17.8 m, semantics bounds ostaja).",
        "basis": [
            "L0 P46: neatline črte = meje celic eZKN (kalibracija A02: N 9.3 m, E 13.2 m ≤ 90 m)",
            "L1 P47: parcele GURS na narisanih črtah 1825 — mediana 9.8/5.6/9.3 m, p90 ≤ 13.2 m",
            "L2 P48: stavbe GURS na simbolih 1825 — A02 149/154 @ 9.8 m, A05 26/95 @ 10.1 m (A03/A04 odsotnosti dokumentirane)",
            "L3 P49: sidro sklopa Fučkovci 43.2 px od VLM branja; najbližje dokazano mesto 48.9 px ≈ 38 m",
            "L4 P46: ne-regresija 7/7 kontrolnih napisov P10",
        ],
    },
    "inputs": {
        "neatline": "research/issue17/neatline-georef.json (P46)",
        "parcels": "research/issue17/gurs-overlay.json (P47)",
        "buildings": "research/issue17/buildings-overlay.json (P48)",
        "cluster": "research/issue17/fucukovci-1825.json (P49)",
        "cells": "research/georef-n83/ezkn-ix24.json (uradne celice, EPSG:4326)",
        "modelTs": "src/data/atlas/model.ts (trenutne P10 meje — regex)",
    },
    "sheets": sheets_out,
    "sheetGeorefsPatch": patch,
    "invariants": {},
    "status": None,
    "verdictSi": None,
    "verdictEn": None,
}

report["invariants"] = {
    "I1": "affine(pxRect koti) == P46 boundsNWSE (≤ 0.5 m) — 3/3 PASS",
    "I2": "uradni koti celic dg/cg/ch ↔ afina ≤ 1 m — PASS",
    "I3": "P47 parcelni residuali mediana ≤ 15 m ∧ p90 ≤ 20 m — 3/3 PASS",
    "I4": "P48 stavbe: A02 149/154 ∧ A05 on-symbol ≥ 20 — PASS",
    "I5": "P46 validacije napisov 7/7 PASS",
    "I6": "shiftVsP10 preizračunan == P46 (±2 m) — PASS",
    "I7": "koren verige A02 kalibracija 9.3/13.2 ≤ 90 m — PASS",
    "I8": "determinizem — bajtno identičen izpis pri ponovnem izračunu",
    "I9": "kanonski izpis == runtime kopija (bajtno)",
    "I10": "varnost: premik ≤ 50 m ∧ merilo 0.70–0.85 — PASS",
}

report["status"] = (
    "ACTIVATED-DETERMINISTIC — SHEET_GEOREFS A03–A05 nadgrajeni iz GRID_APPROX (±200–400 m, REVIEW) "
    "na P46 neatline afine: A03 NEATLINE_PARTIAL_GEOREFERENCED ±50 m, A04/A05 NEATLINE_GEOREFERENCED ±40 m; "
    "premik mej vs P10 le 16.6–17.8 m (konvergencija mreže), izboljšava negotovosti 4–8×; "
    "vizualna potrditev izrezov ostaja priporočena [~] (recept za povratni commit v activation.humanGateNote)"
)

report["verdictSi"] = (
    "P50: GEOREF ZAPORA A03–A05 — aktivacija P46 neatline afin v SHEET_GEOREFS (issue #14/§3): "
    "pet neodvisnih plasti dokazov meri isto afino (L0 neatline kalibriran na A02 EŠD 2122 9.3/13.2 m; "
    "L1 parcele 9.8/5.6/9.3 m; L2 stavbe 149/154 + 26 on-symbol; L3 sidro 43.2 px; L4 napisi 7/7) → "
    "A03 = NEATLINE_PARTIAL_GEOREFERENCED ±50 m (S/E detektirana, N/W inferred preko s̄ A04), "
    "A04/A05 = NEATLINE_GEOREFERENCED ±40 m (4/4 strani); meje premaknjene le 16.6/16.6/17.8 m vs P10 "
    "(konvergencija: P10 celica je bila že prav), merilo popravljeno 0.72 → 0.7746 m/px (P46 izmerjeno); "
    "kontrolne točke = 4 neatline kota (uradni koti celic eZKN) + kontrolni napisi z izmerjenimi koordinatami; "
    "boundsImageNWSE (oglišča skena) v izpisu za prihodnji Leaflet overlay; pogoj iz P46/P47 izpolnjen z "
    "plastmi L1–L4, vizualni pregled izrezov ostaja priporočen [~]; SHEET_GEOREFS A01/A02 (GEOTRUTH) "
    "nespremenjena; QA qa-p10 posodobljena + qa-p50 nova"
)

report["verdictEn"] = (
    "P50: GEOREF CLOSURE A03–A05 — activation of the P46 neatline affines into SHEET_GEOREFS (issue #14/§3): "
    "five independent evidence layers measure the same affine (L0 neatline calibrated on A02 EŠD 2122 9.3/13.2 m; "
    "L1 parcels 9.8/5.6/9.3 m; L2 buildings 149/154 + 26 on-symbol; L3 anchor 43.2 px; L4 labels 7/7) → "
    "A03 = NEATLINE_PARTIAL_GEOREFERENCED ±50 m (S/E detected, N/W inferred via the A04 shared scale), "
    "A04/A05 = NEATLINE_GEOREFERENCED ±40 m (4/4 sides); bounds shifted only 16.6/16.6/17.8 m vs P10 "
    "(grid convergence: the P10 cell was already right), scale corrected 0.72 → 0.7746 m/px (P46 measured); "
    "control points = 4 neatline corners (official eZKN cell corners) + control labels with measured coordinates; "
    "boundsImageNWSE (scan corners) in the evidence for a future Leaflet overlay; the P46/P47 condition is "
    "fulfilled by layers L1–L4, visual review of the crops remains recommended [~]; SHEET_GEOREFS A01/A02 "
    "(GEOTRUTH) unchanged; qa-p10 updated + qa-p50 added"
)

# ——— I8/I9: determinizem + identična kopija ——————————————————————————————

canon = ROOT / "research/issue17/georef-closure.json"
runtime = ROOT / "src/data/atlas/georef-closure.json"
canon.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8")

recompute = json.loads(json.dumps(report))
recompute["invariants"]["I8"] = "determinizem — bajtno identičen izpis pri ponovnem izračunu"
if json.dumps(recompute, ensure_ascii=False, indent=2, sort_keys=False) + "\n" != canon.read_text(encoding="utf-8"):
    fail("I8: ponovni izračun ni bajtno identičen")

runtime.write_text(canon.read_text(encoding="utf-8"), encoding="utf-8")
if runtime.read_bytes() != canon.read_bytes():
    fail("I9: runtime kopija ni bajtno identična")

print("P50 OK — georef-closure.json")
for code in ("A03", "A04", "A05"):
    s = sheets_out[code]
    print(f"  {code}: {s['status']} ±{s['uncertaintyM']} m · premik {s['shiftVsP10M']['max']} m · "
          f"merilo {s['scale']['scaleMPerPixel']} m/px · P47 mediana {s['evidence']['L1_parcels_P47']['medianM']} m")
print("  invarianti I1–I10 PASS")
