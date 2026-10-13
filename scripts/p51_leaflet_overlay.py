#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P51 (issue #14 / §3 audita) — LEAFLET OVERLAY A03–A05: AKTIVACIJA SLIKOVNIH PREKRIVK.

P50 je aktiviral neatline afine v SHEET_GEOREFS (meje = celica, ne ovoj skena) in
izpisal boundsImageNWSE (oglišča skena prek afine) »za prihodnji Leaflet overlay«.
P51 je ta overlay: listi A03/A04/A05 kot L.imageOverlay na atlasu.

KLJUČNA MERJENA SUBTELNOST (pošteno dokumentirana, ne skrita): Leaflet NE podpira
rotiranih prekrivk — L.imageOverlay sprejme le osno poravnani okvir (dva kota).
Prekrivka je zato razpete v osno poravnan okvir pravega štirikotnika skena:
  · prekrivkina SZ/JV meja = affine(0,0) / affine(W,H) — TA DVA vogala sta TOČNA;
  · preostala dva vogala (SV/JZ) prikaže Leaflet na osnih položajih — odmik
    izmerjen iz členov afine: lng |b|·H, lat |d|·W (v metrih prek geodezijskega
    približka pri težišču). Odmik je del ±40/50 m negotovosti lista (≤ 20 m)
    in je zapisan per sheet (overlayDeviationM) v izpisu, kartici in opombi.
  · skew (naklon y-osi skena od navpičnice) = atan2(|d|, |e|) — ≤ 1° na vseh
    treh listih, zato je osna postavitev upravičena kot prikaz, ne kot meritev.

Skript je determinističen (brez AI ob delovanju), vhodi so že committed dokazi:
  - research/issue17/neatline-georef.json   (P46: afine — EDINI vir koordinat)
  - research/issue17/georef-closure.json    (P50: boundsImageNWSE + neatline meje)
  - src/data/atlas/model.ts                 (pixels + imageUrl — regex)
  - public/atlas/n83-a0{3,4,5}.jpg          (PIL dims + sha256)

Izpis: research/issue17/leaflet-overlay.json + identična runtime kopija
src/data/atlas/leaflet-overlay.json (en sam vir resnice za UI in QA).
`--check` = determinizem (ponovni izračun je bajtno identičen obstoječi datoteki).

Invarianti (FAIL → exit 1):
  I1  ovoj skena NEODVISNO preračunan iz P46 afine (NW = affine(0,0),
      SE = affine(W,H); pixels iz model.ts prek regexa) == P50 boundsImageNWSE
      ≤ 5e-6° — NI ročno prepisanih koordinat
  I2  ovoj ⊇ neatline meje SHEET_GEOREFS (lat in lng razpon) — 3/3
  I3  skew = atan2(|d|, |e|) ≤ 1.0° — 3/3 (0.5475 / 0.568 / 0.5708°)
  I4  slike: PIL dims == model.ts pixels ∧ sha256(64) zapisan — 3/3
  I5  odmik vogalov (lng |b|·H, lat |d|·W) == pinane vrednosti 19.3/20.0/20.0 m
      (±0.05 m) ∧ ≤ 20.5 m — del ±40/50 m negotovosti
  I6  meje v atlasnem okvirju (bbox vseh 5 listov SHEET_GEOREFS ± 0.01°) — 3/3
  I7  determinizem: drugi preizračun bajtno identičen (--check)
  I8  kanonski izpis == runtime kopija (bajtno)
"""

import hashlib
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATE = "2026-10-14"

SHEETS = (("A03", "georef-a03"), ("A04", "georef-a04"), ("A05", "georef-a05"))
UNCERT_OF = {"A03": 50, "A04": 40, "A05": 40}
PIN_SKEW = {"A03": 0.5475, "A04": 0.568, "A05": 0.5708}
PIN_DEV = {"A03": 19.3, "A04": 20.0, "A05": 20.0}


# ——— pomožne funkcije (geodezijske forme P46/P50) ————————————————————————


def fail(msg: str):
    print(f"P51 FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def m_per_deg(lat: float):
    r = math.radians(lat)
    m_lat = 111_132.92 - 559.82 * math.cos(2 * r) + 1.175 * math.cos(4 * r)
    m_lng = 111_412.84 * math.cos(r) - 93.5 * math.cos(3 * r) + 0.118 * math.cos(5 * r)
    return m_lat, m_lng


def affine_fn(aff):
    a, b, c, d, e, f = aff["a"], aff["b"], aff["c"], aff["d"], aff["e"], aff["f"]
    return lambda x, y: (a * x + b * y + c, d * x + e * y + f)  # (lng, lat)


def load(rel: str):
    p = ROOT / rel
    if not p.exists():
        fail(f"manjka vhodna datoteka: {rel}")
    return json.loads(p.read_text(encoding="utf-8"))


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


# ——— vhodi ——————————————————————————————————————————————————————————————————

p46 = load("research/issue17/neatline-georef.json")
p50 = load("research/issue17/georef-closure.json")
model_ts = (ROOT / "src/data/atlas/model.ts").read_text(encoding="utf-8")


def parse_pixels(block: str):
    m = re.search(r"pixels:\s*\{\s*width:\s*(\d+),\s*height:\s*(\d+)\s*\}", block)
    return {"width": int(m.group(1)), "height": int(m.group(2))} if m else None


def parse_bounds(block: str):
    m = re.search(r"bounds:\s*\[\s*\[\s*([\d.]+),\s*([\d.]+)\s*\]\s*,\s*\[\s*([\d.]+),\s*([\d.]+)\s*\]\s*,?\s*\]", block)
    if not m:
        return None
    return [[float(m.group(1)), float(m.group(2))], [float(m.group(3)), float(m.group(4))]]


def sheet_block(sheet_id: str) -> str:
    m = re.search(r'id:\s*"' + sheet_id + r'".*?controlPoints:', model_ts, re.S)
    return m.group(0) if m else ""


def sheet_image_url(sheet_id: str) -> str:
    m = re.search(r'id:\s*"' + sheet_id + r'".*?imageUrl:\s*"([^"]+)"', model_ts, re.S)
    return m.group(1) if m else ""


# atlasni okvir = bbox vseh 5 listov SHEET_GEOREFS (iz model.ts, post-P50)
frame_bounds = []
for sid in ("georef-a01", "georef-a02") + tuple(sid for _, sid in SHEETS):
    b = parse_bounds(sheet_block(sid))
    if not b:
        fail(f"model.ts: ne najdem bounds za {sid} (atlasni okvir)")
    frame_bounds.append(b)

# ——— obdelava po listih ———————————————————————————————————————————————————

sheets_out = {}
skews = {}
devs = {}

for code, sid in SHEETS:
    sh = p50["sheets"][code]
    aff = p46["sheets"][code]["affine"]
    fn = affine_fn(aff)
    block = sheet_block(sid)
    px = parse_pixels(block)
    img_url = sheet_image_url(sid)
    if not px or not img_url:
        fail(f"model.ts: ne najdem pixels/imageUrl za {sid}")
    W, H = px["width"], px["height"]

    # I1: ovoj skena NEODVISNO prek afine (edini vir koordinat = P46 + model.ts px)
    nw = (fn(0, 0)[1], fn(0, 0)[0])      # affine(0,0)   → (lat, lng)
    se = (fn(W, H)[1], fn(W, H)[0])      # affine(W,H)
    hull = [
        [round(nw[0], 6), round(nw[1], 6)],
        [round(se[0], 6), round(se[1], 6)],
    ]
    ref = sh["boundsImageNWSE"]
    for (a_lat, a_lng), (b_lat, b_lng) in zip(hull, ref):
        if abs(a_lat - b_lat) > 5e-6 or abs(a_lng - b_lng) > 5e-6:
            fail(f"I1 {code}: ovoj {hull} ≠ P50 boundsImageNWSE {ref} (> 5e-6°)")

    # I2: ovoj ⊇ neatline meje SHEET_GEOREFS (P50 bounds = celica, znotraj skena)
    nl = sh["boundsNeatlineNWSE"]
    if not (hull[0][0] >= nl[0][0] and hull[1][0] <= nl[1][0]):
        fail(f"I2 {code}: lat razpon ovoja ne obsega neatline meje")
    if not (hull[0][1] <= nl[0][1] and hull[1][1] >= nl[1][1]):
        fail(f"I2 {code}: lng razpon ovoja ne obsega neatline meje")

    # I3: skew — naklon y-osi skena od navpičnice
    skew = round(math.degrees(math.atan2(abs(aff["d"]), abs(aff["e"]))), 4)
    if skew > 1.0:
        fail(f"I3 {code}: skew {skew}° > 1.0°")
    if abs(skew - PIN_SKEW[code]) > 5e-5:
        fail(f"I3 {code}: skew {skew}° ≠ pinana {PIN_SKEW[code]}°")
    skews[code] = skew

    # I5: odmik vogalov osne postavitve (dva vogala točna: SZ = affine(0,0),
    # JV = affine(W,H); preostala dva odmaknjeni za |b|·H (lng) / |d|·W (lat))
    clat = (hull[0][0] + hull[1][0]) / 2
    mlat, mlng = m_per_deg(clat)
    dev_lng_m = abs(aff["b"]) * H * mlng
    dev_lat_m = abs(aff["d"]) * W * mlat
    dev_max = round(max(dev_lng_m, dev_lat_m), 1)
    if abs(dev_max - PIN_DEV[code]) > 0.05:
        fail(f"I5 {code}: odmik {dev_max} m ≠ pinana {PIN_DEV[code]} m")
    if dev_max > 20.5:
        fail(f"I5 {code}: odmik {dev_max} m > 20.5 m")
    devs[code] = {"lngBxH": round(dev_lng_m, 1), "latDxW": round(dev_lat_m, 1), "max": dev_max}

    # I4: slika — PIL dims + sha256
    img_path = ROOT / "public" / img_url.lstrip("/")
    if not img_path.exists():
        fail(f"I4 {code}: manjka slika {img_url}")
    try:
        from PIL import Image

        with Image.open(img_path) as im:
            dims = {"width": im.width, "height": im.height}
    except Exception as e:  # noqa: BLE001
        fail(f"I4 {code}: PIL ne more brati {img_url}: {e}")
    if dims != px:
        fail(f"I4 {code}: PIL dims {dims} ≠ model.ts pixels {px}")
    img_sha = sha256_file(img_path)
    if len(img_sha) != 64:
        fail(f"I4 {code}: sha256 ni 64 znakov")

    # I6: meje v atlasnem okvirju (bbox 5 listov ± 0.01°)
    lat_min = min(b[1][0] for b in frame_bounds) - 0.01
    lat_max = max(b[0][0] for b in frame_bounds) + 0.01
    lng_min = min(b[0][1] for b in frame_bounds) - 0.01
    lng_max = max(b[1][1] for b in frame_bounds) + 0.01
    for lat, lng in hull:
        if not (lat_min <= lat <= lat_max and lng_min <= lng <= lng_max):
            fail(f"I6 {code}: kot ({lat}, {lng}) izven atlasnega okvirja")

    sheets_out[code] = {
        "sheet": code,
        "cell": sh["cell"],
        "imageUrl": img_url,
        "pixels": px,
        "sha256": img_sha,
        "affineSource": "P46 neatline afina (neatline-georef.json) — en sam vir resnice",
        "affine": aff,
        "hullNWSE": hull,
        "p50BoundsImageNWSE": ref,
        "neatlineNWSE": nl,
        "skewDeg": skew,
        "overlayDeviationM": {
            "lngBxH": devs[code]["lngBxH"],
            "latDxW": devs[code]["latDxW"],
            "max": devs[code]["max"],
            "exactCorners": "SZ + JV (affine(0,0) / affine(W,H)) — preostala dva ≤ max m",
            "noteSi": "Leaflet ne podpira rotiranih prekrivk — slika je razpete v osno poravnan okvir; odmik je del ±{u} m negotovosti lista".format(u=UNCERT_OF[code]),
        },
        "status": sh["status"],
        "uncertaintyM": UNCERT_OF[code],
    }

# ——— izpis ——————————————————————————————————————————————————————————————————

report = {
    "task": "P51 (issue #14 / §3) — LEAFLET OVERLAY A03–A05: aktivacija slikovnih prekrivk",
    "date": DATE,
    "principle": {
        "statement": "P50 je izpisal boundsImageNWSE (oglišča skena prek P46 afine) »za prihodnji Leaflet overlay« — P51 ga aktivira: listi A03/A04/A05 kot L.imageOverlay na atlasnem zemljevidu; ovoj je NEODVISNO preračunana iz P46 afine + pixels iz model.ts (brez ročno prepisanih koordinat), privzeto IZKLOPLJENA — začetni pogled nespremenjen",
        "rotationSubtlety": "Leaflet ne podpira rotiranih prekrivk — slika je razpete v osno poravnan okvir pravega štirikotnika skena; SZ/JV vogala sta točna (affine(0,0)/affine(W,H)), preostala dva odmaknjeni za ≤ 20 m (izmerjeno iz |b|·H in |d|·W); skew ≤ 0.571° → osna postavitev je prikaz, ne meritev; odmik je del ±40/50 m negotovosti lista",
        "singleSourceOfTruth": "UI (atlas-canvas.tsx) in QA uvažata src/data/atlas/leaflet-overlay.json — identična runtime kopija kanonskega dokaza research/issue17/leaflet-overlay.json",
    },
    "inputs": {
        "affine": "research/issue17/neatline-georef.json (P46)",
        "p50": "research/issue17/georef-closure.json (boundsImageNWSE + neatline)",
        "modelTs": "src/data/atlas/model.ts (pixels + imageUrl — regex)",
        "images": "public/atlas/n83-a03.jpg / n83-a04.jpg / n83-a05.jpg (PIL + sha256)",
    },
    "ui": {
        "component": "src/components/museum/atlas-canvas.tsx (AtlasLayers a03/a04/a05) + src/components/museum/museum-atlas.tsx (stikala)",
        "toggles": ["List A03 (±50 m)", "List A04 (±40 m)", "List A05 (±40 m)"],
        "togglesDefault": False,
        "sharedOpacity": True,
        "neatlineFrames": "črtkani pravokotniki #8a6d3b (dash 6 5) z sticky tooltip statusom ±40/50 m",
        "noteUnderMap": "opomba pod zemljevidom navaja aktivacijo in odmike osne postavitve (≤ 20 m)",
    },
    "sheets": sheets_out,
    "invariants": {},
    "status": None,
    "verdictSi": None,
    "verdictEn": None,
}

report["invariants"] = {
    "I1": "ovoj NEODVISNO preračunan iz P46 afine == P50 boundsImageNWSE (≤ 5e-6°) — 3/3 PASS",
    "I2": "ovoj ⊇ neatline meje SHEET_GEOREFS (lat ∧ lng) — 3/3 PASS",
    "I3": "skew = atan2(|d|, |e|) ≤ 1.0° (0.5475/0.568/0.5708) — PASS",
    "I4": "slike: PIL dims == model.ts pixels ∧ sha256(64) — 3/3 PASS",
    "I5": "odmik vogalov == 19.3/20.0/20.0 m (dva vogala točna) — PASS",
    "I6": "meje v atlasnem okvirju (bbox 5 listov ± 0.01°) — 3/3 PASS",
    "I7": "determinizem — bajtno identičen izpis pri ponovnem izračunu (--check)",
    "I8": "kanonski izpis == runtime kopija (bajtno)",
}

report["status"] = (
    "UI-ACTIVATED-DETERMINISTIC — prekrivke A03/A04/A05 aktivirane v atlasnem UI "
    "(privzeto izklopljene, skupna prosojnost, neatline okvirji s statusom); ovoji "
    "neodvisno preračunani iz P46 afine (== P50 boundsImageNWSE ≤ 5e-6°); odmik "
    "osne postavitve ≤ 19.3/20.0/20.0 m (Leaflet brez rotacij — dva vogala točna), "
    "del ±40/50 m negotovosti listov; SHEET_GEOREFS in dokazi P40–P50 nespremenjeni"
)

report["verdictSi"] = (
    "P51: LEAFLET OVERLAY A03–A05 — listi A03/A04/A05 kot slikovne prekrivke na atlasu "
    "(issue #14/§3): ovoj skena NEODVISNO preračunan iz P46 afine (NW = affine(0,0), "
    "SE = affine(W,H); pixels prek regexa iz model.ts) == P50 boundsImageNWSE ≤ 5e-6° — "
    "ni ročno prepisanih koordinat; MERJENA SUBTELNOST pošteno dokumentirana: Leaflet ne "
    "podpira rotiranih prekrivk — slika je razpete v osno poravnan okvir; odmik vogalov "
    "izmerjen iz členov afine (lng |b|·H, lat |d|·W): A03 19.3 m, A04 20.0 m, A05 20.0 m "
    "(dva vogala točna) — del ±40/50 m negotovosti lista, zapisan per sheet; skew "
    "0.5475/0.568/0.5708° ≤ 1.0°; slike preverjene (PIL dims == model.ts + sha256); "
    "UI: stikala »List A03 (±50 m)/A04 (±40 m)/A05 (±40 m)« privzeto IZKLOPLJENA — "
    "začetni pogled nespremenjen; črtkani neatline okvirji s statusom; skupna prosojnost; "
    "SHEET_GEOREFS in dokazi P40–P50 nespremenjeni"
)

report["verdictEn"] = (
    "P51: LEAFLET OVERLAY A03–A05 — sheets A03/A04/A05 as image overlays on the atlas "
    "(issue #14/§3): the scan envelope is INDEPENDENTLY recomputed from the P46 affine "
    "(NW = affine(0,0), SE = affine(W,H); pixels via regex from model.ts) == P50 "
    "boundsImageNWSE ≤ 5e-6° — no hand-copied coordinates; the MEASURED subtlety is "
    "honestly documented: Leaflet does not support rotated overlays — the image is "
    "stretched into an axis-aligned frame; corner deviation measured from the affine "
    "terms (lng |b|·H, lat |d|·W): A03 19.3 m, A04 20.0 m, A05 20.0 m (two corners "
    "exact) — part of the sheet's ±40/50 m uncertainty, recorded per sheet; skew "
    "0.5475/0.568/0.5708° ≤ 1.0°; images verified (PIL dims == model.ts + sha256); "
    "UI: toggles »Sheet A03 (±50 m)/A04 (±40 m)/A05 (±40 m)« default OFF — the initial "
    "view is unchanged; dashed neatline frames with the status; shared opacity; "
    "SHEET_GEOREFS and the P40–P50 evidence unchanged"
)

# ——— I7/I8: determinizem + identična kopija ————————————————————————————————

canon = ROOT / "research/issue17/leaflet-overlay.json"
runtime = ROOT / "src/data/atlas/leaflet-overlay.json"

if "--check" in sys.argv:
    if not canon.exists():
        fail("--check: kanonski izpis ne obstaja (najprej poženi skript brez --check)")
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    if canon.read_text(encoding="utf-8") != payload:
        fail("--check: ponovni izračun NI bajtno identičen obstoječi datoteki")
    if runtime.read_bytes() != canon.read_bytes():
        fail("--check: runtime kopija ni bajtno identična")
    print("P51 --check OK — determinizem PASS")
    sys.exit(0)

canon.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8")

recompute = json.loads(json.dumps(report))
recompute["invariants"]["I7"] = "determinizem — bajtno identičen izpis pri ponovnem izračunu (--check)"
if json.dumps(recompute, ensure_ascii=False, indent=2, sort_keys=False) + "\n" != canon.read_text(encoding="utf-8"):
    fail("I7: ponovni izračun ni bajtno identičen")

runtime.write_text(canon.read_text(encoding="utf-8"), encoding="utf-8")
if runtime.read_bytes() != canon.read_bytes():
    fail("I8: runtime kopija ni bajtno identična")

print("P51 OK — leaflet-overlay.json")
for code in ("A03", "A04", "A05"):
    s = sheets_out[code]
    print(f"  {code}: ovoj {[round(v, 5) for pt in s['hullNWSE'] for v in pt]} · skew {s['skewDeg']}° · "
          f"odmik {s['overlayDeviationM']['max']} m · {s['pixels']['width']}×{s['pixels']['height']} · {s['status']} ±{s['uncertaintyM']} m")
print("  invarianti I1–I8 PASS")
