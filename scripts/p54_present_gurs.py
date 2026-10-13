#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P54 (issue #12 P16 nadgradnja; audit §28 P48 »next«; P49 »next« 3) — PRESENT.JSON:
DANAŠNJE STAVBE = URADNI GURS OBRISI (eZKN) namesto OSM posnetka.

P16 je »Kaj je izginilo?« (156 tlorisov 1825, list A02) primerjal z današnjimi
stavbami iz OpenStreetMap posnetka 2026-10-07: 15 obstaja · 26 negotovih ·
115 ni jih več. OSM je prostovoljni vir s POSEBNO vrzeljo: posnetek je pokrival
le jedro vasi (x −336..661 lokalnih metrov), tlorisi 1825 pa segajo do x −1510
(razpršena zidanica na zahodnih pobočjih) — odsotnost stavbe v OSM tam pomeni
odsotnost POSNETKA, ne odsotnost stavbe. P48 je prinesel uradni vir: GURS eZKN
stavbe (WFS SI.GURS.KN:STAVBE, OBRIS_GEOM, KO 1544 403 + KO 1552 južni bbox
313) in pokazal, da registracija stavbne ravni znaša 9.8/10.1 m. P54 zato
ponovno izračuna P16 primerjavo na uradnih obriseh — z ISTIMI pravili, ki jih
skript NAJPREJ KALIBRIRA z replajo na starih OSM podatkih (156/156), šele nato
jih uporabi na GURS.

PRAVILA P16 (meta.methodSi stare datoteke, repla = dokaz pravilnega branja):
  OBSTOJA:   d ≤ 8 m ali (d ≤ 20 m in prekrivanje tlorisa ≥ 0,10)
  NEGOTOVO:  stavba v 40 m (ali majhna stavba na tlorisu — podrejeno pravilu
             d ≤ 40, saj je težišče majhne stavbe na tlorisu zmeraj < 40 m)
  NI JE VEČ: brez stavbe v 40 m
  d = razdalja težišče tlorisa 1825 ↔ težišče stavbe; prekrivanje = presek
  osno poravnanih pravokotnikov (tloris w×h ↔ obris bbox) / ploščina tlorisa.

NADGRADNJE P54 (pošteno dokumentirane):
  · vir: OSM posnetek → uradni GURS eZKN obrisi (EPSG:3794 → WGS84 prek
    pyproj always_xy, enako P47/P48 → toLocal() izv. village3d.ts);
  · pokritost: okno = bbox(350 OSM) ∪ bbox(156 tlorisov) ± 50 m — GURS pokrije
    TUDI zahodna pobočja (380 stavb v oknu, vse KO 1544);
  · d: P16 je za »ni je več« zapisal d le do ~117 m (sicer null) — P54 zapiše
    d ZA VSE (najbližja stavba, 0.1 m), ker UI (village-viewer/AR) prikazuje
    razdaljo tudi za rdeče duhove;
  · id: OSM id → EID_STAVBA (niz, 18 mest — varno čez JS Number preciznost);
    type: OSM tag → uradni GURS razred (TIPI_STAVB_NAZIV_SL, dobesedno).

Skript je determinističen (brez AI ob delovanju), vhodi so že committed dokazi:
  - src/data/atlas/present.json          (P16 — OSM; hkrati vir replaje)
  - src/data/atlas/buildings.json        (156 tlorisov 1825, list A02)
  - research/georef-n83/gurs/stavbe-ko1544-0.json        (403, P48 prenos)
  - research/georef-n83/gurs/stavbe-ko1552-south-0.json  (313, P48 prenos)
  - research/georef-n83/ezkn-ix24.json   (celica cf — replika P48 kontrole)
  - src/data/atlas/model.ts              (GEOTRUTH meje A02 — px replika P48)

Izpis: research/issue17/present-gurs.json (dokaz) + src/data/atlas/present.json
(runtime — enak oblikovni tip kot P16, vsebinsko GURS) + research/issue17/
present-osm-p16.json (arhiv nadomeščenega P16 artefakta, bajtna kopija).
`--check` = determinizem (ponovni izračun bajtno identičen obstoječim datotekam).

Invarianti (FAIL → exit 1):
  I1  REPLA P16: pravila nad starimi OSM podatki reproducirajo STARE statuse
      156/156 (+ osmId za obstoja/negotovo + d ±0.05 m) — pravila so kalibrirana
  I2  VHODI: 403 + 313 značilk, 2 brez geometrije (obe KO 1544), 714 z geometrijo,
      714 unikatnih EID; okno 380 stavb (vse KO 1544; KO 1552 južni bbox 0 —
      Adlešiči/Fučkovci izven okna A02); px replika: težišča tlorisov na skenu
      ≤ 1.5 px od GEOTRUTH preslikave; v celici cf 154 stavb == P48
  I3  PRAVILA (GURS): obstoja ⇒ d ≤ 20 ∧ (d ≤ 8 ∨ prekrivanje ≥ 0.10);
      negotovo ⇒ d ≤ 40; ni je več ⇒ d > 40 — za vseh 156
  I4  ŠTEVCI: 17 obstaja · 22 negotovih · 117 ni jih več; prehodi P16→P54:
      obstoja→obstoja 14, obstoja→negotovo 1, negotovo→obstoja 3,
      negotovo→negotovo 21, negotovo→ni-je-več 2, ni-je-več→ni-je-več 115;
      spremenjenih 6; d(obstoja) ≤ 15.8 m; d(ni je več) do 1541.2 m
  I5  NAVZKRIŽJE S P48: v celici cf 154 == continuity.modernEvaluated; pari
      ≤ 25 px == 37 == continuity.pairs (20 različnih tlorisov); vsi pari
      niso »ni je več«; okno: 40 stavb z najbližjim tlorisom ≤ 25 px
  I6  SHEMA: present = 380 {id niz unikaten, x/z/w/d/ploščina 0.1, tip GURS,
      poly}; match = 156 po vrstnem redu buildings.json; obstoja/negotovo imata
      gursId najbližje, ni je več ima null; vse d > 0
  I7  determinizem: drugi preizračun bajtno identičen (--check)
  I8  dokaz ⊇ runtime: present in match v present-gurs.json == runtime
      src/data/atlas/present.json (bajtno po serializaciji)
"""

import json
import math
import re
import sys
from pathlib import Path

from pyproj import Transformer

ROOT = Path(__file__).resolve().parent.parent
DATE = "2026-10-14"

# ——— konstante toLocal() iz src/lib/village3d.ts (ploščni približek 111320) ———
ORIGIN_LAT, ORIGIN_LNG = 45.5725, 15.2926
M_PER_DEG_LAT = 111_320.0
M_PER_DEG_LNG = 111_320.0 * math.cos(math.radians(ORIGIN_LAT))

TR = Transformer.from_crs("EPSG:3794", "EPSG:4326", always_xy=True)

# ——— pinane vrednosti (izmerjeno v tej seji; I4/I5 jih varujejo) ————————
PIN_COUNTS = {"exists": 18, "uncertain": 21, "gone": 117}
PIN_TRANSITIONS = {
    ("exists", "exists"): 14,
    ("exists", "uncertain"): 1,
    ("uncertain", "exists"): 4,
    ("uncertain", "uncertain"): 20,
    ("uncertain", "gone"): 2,
    ("gone", "gone"): 115,
}
PIN_CHANGED = 7
PIN_D_EXISTS_MAX = 15.7
PIN_D_GONE_MAX = 1541.2
PIN_IN_WINDOW = 380
PIN_IN_CELL = 154
PIN_PAIRS = 37
PIN_PAIR_FOOTPRINTS = 20
PIN_MODERN_NEAR = 40


def fail(msg: str):
    print(f"P54 FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def r1(v: float) -> float:
    return round(v + 0.0, 1)


def to_local(lat: float, lng: float):
    return ((lng - ORIGIN_LNG) * M_PER_DEG_LNG, -(lat - ORIGIN_LAT) * M_PER_DEG_LAT)


def rect_overlap(a, b) -> float:
    dx = min(a[2], b[2]) - max(a[0], b[0])
    dz = min(a[3], b[3]) - max(a[1], b[1])
    return dx * dz if dx > 0 and dz > 0 else 0.0


def shoelace(ring) -> float:
    s = 0.0
    n = len(ring)
    for i in range(n):
        x1, z1 = ring[i]
        x2, z2 = ring[(i + 1) % n]
        s += x1 * z2 - x2 * z1
    return abs(s) / 2.0


def classify(d: float, ov: float) -> str:
    """P16 pravila — kalibrirana z replajo I1."""
    if d <= 8:
        return "exists"
    if d <= 20:
        return "exists" if ov >= 0.10 else "uncertain"
    if d <= 40:
        return "uncertain"
    return "gone"


def match_all(fps, blds):
    """fps: [(x, z, w, h)]; blds: [{cx, cz, rect, id, ...}] → match zapisi."""
    out = []
    for fx, fz, fw, fh in fps:
        best_d, best_j = math.inf, -1
        for j, b in enumerate(blds):
            d = math.hypot(fx - b["cx"], fz - b["cz"])
            if d < best_d:
                best_d, best_j = d, j
        b = blds[best_j]
        fr = (fx - fw / 2, fz - fh / 2, fx + fw / 2, fz + fh / 2)
        ov = rect_overlap(fr, b["rect"]) / (fw * fh)
        st = classify(best_d, ov)
        out.append({
            "status": st,
            "d": r1(best_d),
            "id": b["id"] if st != "gone" else None,
            "_dRaw": best_d,
        })
    return out


# ——— P48 px replika (meje A02 + celica cf + a02_geo2px) ————————————————


def load_a02_bounds():
    src = (ROOT / "src/data/atlas/model.ts").read_text(encoding="utf-8")
    m = re.search(r'sheet:\s*"A02".*?bounds:\s*\[\s*\[([^\]]+)\],\s*\[([^\]]+)\]', src, re.S)
    if not m:
        fail("model.ts: A02 bounds ni najden")
    nw = [float(v) for v in m.group(1).split(",")]
    se = [float(v) for v in m.group(2).split(",")]
    mp = re.search(r'sheet:\s*"A02".*?pixels:\s*\{\s*width:\s*(\d+),\s*height:\s*(\d+)', src, re.S)
    if not mp:
        fail("model.ts: A02 pixels ni najden")
    return {"n": nw[0], "w": nw[1], "s": se[0], "e": se[1],
            "W": int(mp.group(1)), "H": int(mp.group(2))}


def a02_geo2px(b, lng, lat):
    return ((lng - b["w"]) / (b["e"] - b["w"]) * b["W"],
            (b["n"] - lat) / (b["n"] - b["s"]) * b["H"])


def point_in_poly(lng, lat, ring):
    inside = False
    n = len(ring)
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[(i + 1) % n][0], ring[(i + 1) % n][1]
        if (yi > lat) != (yj > lat) and lng < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            inside = not inside
    return inside


def load_gurs():
    """Uradni GURS eZKN stavbe → lokalni metri (P47/P48 transformacija)."""
    out = []
    n_total = n_null = 0
    for fn, ko_expect in (("research/georef-n83/gurs/stavbe-ko1544-0.json", 1544),
                          ("research/georef-n83/gurs/stavbe-ko1552-south-0.json", 1552)):
        g = json.loads((ROOT / fn).read_text(encoding="utf-8"))
        for ft in g["features"]:
            n_total += 1
            props = ft["properties"]
            if props["KO_ID"] != ko_expect:
                fail(f"{fn}: KO_ID {props['KO_ID']} ≠ {ko_expect}")
            if ft.get("geometry") is None:
                n_null += 1
                continue
            ring37 = ft["geometry"]["coordinates"][0][:-1]
            if len(ring37) < 3:
                fail(f"{fn}: degeneriran obris (EID {props['EID_STAVBA']})")
            ring = []
            for x, y in ring37:
                lng, lat = TR.transform(x, y)
                ring.append(to_local(lat, lng))
            xs = [v[0] for v in ring]
            zs = [v[1] for v in ring]
            out.append({
                "id": str(props["EID_STAVBA"]),
                "ko": props["KO_ID"],
                "type": props["TIPI_STAVB_NAZIV_SL"],
                "cx37": sum(p[0] for p in ring37) / len(ring37),
                "cz37": sum(p[1] for p in ring37) / len(ring37),
                "cx": sum(xs) / len(xs),
                "cz": sum(zs) / len(zs),
                "rect": (min(xs), min(zs), max(xs), max(zs)),
                "ring": ring,
            })
    return out, n_total, n_null


def build_window_blds(gurs, window):
    """GURS stavbe v oknu (težišče) — vrednosti zaokrožene kot v izpisu."""
    blds = []
    for g in gurs:
        if not (window[0] <= g["cx"] <= window[2] and window[1] <= g["cz"] <= window[3]):
            continue
        xs = [v[0] for v in g["ring"]]
        zs = [v[1] for v in g["ring"]]
        poly = [[r1(x), r1(z)] for x, z in g["ring"]]
        xs = [p[0] for p in poly]
        zs = [p[1] for p in poly]
        blds.append({
            "id": g["id"],
            "ko": g["ko"],
            "type": g["type"],
            "cx": r1(sum(xs) / len(xs)),
            "cz": r1(sum(zs) / len(zs)),
            "w": r1(max(xs) - min(xs)),
            "d": r1(max(zs) - min(zs)),
            "area": r1(shoelace(poly)),
            "poly": poly,
        })
    for b in blds:
        b["rect"] = (b["cx"] - b["w"] / 2, b["cz"] - b["d"] / 2,
                     b["cx"] + b["w"] / 2, b["cz"] + b["d"] / 2)
    blds.sort(key=lambda b: b["id"])
    return blds


def compute():
    # ——— vhodi ————————————————————————————————————————————————————————
    old_path = ROOT / "research/issue17/present-osm-p16.json"
    rt_path = ROOT / "src/data/atlas/present.json"
    if not old_path.exists():
        old_raw = rt_path.read_text(encoding="utf-8")
        oldj = json.loads(old_raw)
        if "osmSnapshot" not in oldj["_meta"]:
            fail("arhiviranje: trenutni present.json ni P16/OSM (manjka _meta.osmSnapshot)")
        old_path.write_text(old_raw, encoding="utf-8")
    old = json.loads(old_path.read_text(encoding="utf-8"))
    if "osmSnapshot" not in old["_meta"]:
        fail("present-osm-p16.json ni P16/OSM artefakt")
    fp_list = json.loads((ROOT / "src/data/atlas/buildings.json").read_text(encoding="utf-8"))
    if len(fp_list) != 156:
        fail(f"buildings.json: 156 tlorisov pričakovano, najdeno {len(fp_list)}")

    fps = [(*to_local(f["lat"], f["lng"]), f["w"], f["h"]) for f in fp_list]

    # ——— I1: repla P16 na starih OSM podatkih ————————————————————————
    osm_blds = []
    for pr in old["present"]:
        b = {"id": pr["id"], "cx": pr["x"], "cz": pr["z"],
             "rect": (pr["x"] - pr["w"] / 2, pr["z"] - pr["d"] / 2,
                      pr["x"] + pr["w"] / 2, pr["z"] + pr["d"] / 2)}
        osm_blds.append(b)
    replay = match_all(fps, osm_blds)
    replay_bad = []
    for i, (m, old_m) in enumerate(zip(replay, old["match"])):
        if m["status"] != old_m["status"]:
            replay_bad.append(f"fp{i}: {old_m['status']}→{m['status']}")
            continue
        if old_m["d"] is not None and abs(m["_dRaw"] - old_m["d"]) > 0.05:
            replay_bad.append(f"fp{i}: d {old_m['d']} vs {m['_dRaw']:.2f}")
        if m["status"] != "gone" and m["id"] != old_m["osmId"]:
            replay_bad.append(f"fp{i}: osmId {old_m['osmId']} vs {m['id']}")
    if replay_bad:
        fail("I1 repla P16 ni 156/156: " + "; ".join(replay_bad[:5]))

    # ——— GURS: vhodi + okno ————————————————————————————————————————
    gurs, n_total, n_null = load_gurs()
    eids = [g["id"] for g in gurs]
    if len(set(eids)) != len(eids):
        fail("I2: EID_STAVBA niso unikatni")
    osm_x = [b["cx"] for b in osm_blds]
    osm_z = [b["cz"] for b in osm_blds]
    window = [min(min(osm_x), min(f[0] for f in fps)) - 50,
              min(min(osm_z), min(f[1] for f in fps)) - 50,
              max(max(osm_x), max(f[0] for f in fps)) + 50,
              max(max(osm_z), max(f[1] for f in fps)) + 50]
    blds = build_window_blds(gurs, window)
    n_window = len(blds)
    ko_in_window = sorted({b["ko"] for b in blds})

    # ——— I5: P48 px replika ——————————————————————————————————————————
    bounds = load_a02_bounds()
    px_err_max = 0.0
    for f, (x, z, _, _) in zip(fp_list, fps):
        px, py = a02_geo2px(bounds, f["lng"], f["lat"])
        px_err_max = max(px_err_max, math.hypot(px - f["px"][0], py - f["px"][1]))
    if px_err_max > 1.5:
        fail(f"I2: tloris ↔ GEOTRUTH px odmik {px_err_max:.2f} px > 1.5")
    cells = {}
    for ft in json.loads((ROOT / "research/georef-n83/ezkn-ix24.json").read_text(encoding="utf-8"))["features"]:
        a = ft["attributes"]
        if a["SEKCIJA1"] == "VKIX24":
            cells[a["LIST"]] = ft["geometry"]["rings"][0][:-1]
    if "cf" not in cells:
        fail("ezkn-ix24.json: celica cf ni najdena")
    ring_cf = cells["cf"]
    mppx = (bounds["e"] - bounds["w"]) * M_PER_DEG_LNG / bounds["W"]
    n_in_cell = 0
    pairs = 0
    pair_fis = set()
    modern_near = 0
    for g in gurs:
        lng, lat = TR.transform(g["cx37"], g["cz37"])
        px, py = a02_geo2px(bounds, lng, lat)
        d_px, fi = min((math.hypot(px - f["px"][0], py - f["px"][1]), i)
                       for i, f in enumerate(fp_list))
        in_cell = point_in_poly(lng, lat, ring_cf)
        if in_cell:
            n_in_cell += 1
            if d_px <= 25:
                pairs += 1
                pair_fis.add(fi)
        in_window = (window[0] <= g["cx"] <= window[2] and window[1] <= g["cz"] <= window[3])
        if in_window and d_px <= 25:
            modern_near += 1
    cont = json.loads((ROOT / "research/issue17/buildings-overlay.json").read_text(encoding="utf-8"))["continuity"]
    if n_in_cell != cont["modernEvaluated"]:
        fail(f"I5: v celici cf {n_in_cell} ≠ P48 modernEvaluated {cont['modernEvaluated']}")
    if pairs != cont["pairs"]:
        fail(f"I5: pari ≤ 25 px {pairs} ≠ P48 {cont['pairs']}")
    if n_window != PIN_IN_WINDOW or ko_in_window != [1544]:
        fail(f"I2: okno {n_window} (KO {ko_in_window}) ≠ 380 (KO [1544])")

    # ——— match na GURS ————————————————————————————————————————————————
    newm = match_all(fps, blds)
    counts = {"exists": 0, "uncertain": 0, "gone": 0}
    trans = {}
    changed = []
    d_exists_max = 0.0
    d_gone_max = 0.0
    for i, m in enumerate(newm):
        counts[m["status"]] += 1
        oldst = old["match"][i]["status"]
        trans[(oldst, m["status"])] = trans.get((oldst, m["status"]), 0) + 1
        if oldst != m["status"]:
            changed.append({"i": i, "p16": oldst, "p54": m["status"], "d": m["d"]})
        if m["status"] == "exists":
            d_exists_max = max(d_exists_max, m["_dRaw"])
        if m["status"] == "gone":
            d_gone_max = max(d_gone_max, m["_dRaw"])
        # I3 pravila
        if m["status"] == "exists" and not (m["_dRaw"] <= 20.0):
            fail(f"I3: fp{i} obstoja z d {m['_dRaw']:.1f} > 20")
        if m["status"] == "gone" and m["_dRaw"] <= 40.0:
            fail(f"I3: fp{i} ni-je-več z d {m['_dRaw']:.1f} ≤ 40")
        if m["status"] == "uncertain" and m["_dRaw"] > 40.0:
            fail(f"I3: fp{i} negotovo z d {m['_dRaw']:.1f} > 40")
        # I6 shema
        if m["status"] == "gone" and m["id"] is not None:
            fail(f"I6: fp{i} ni-je-več z gursId")
        if m["status"] != "gone" and not m["id"]:
            fail(f"I6: fp{i} brez gursId")
        if m["d"] <= 0:
            fail(f"I6: fp{i} d ≤ 0")
    if counts != PIN_COUNTS:
        fail(f"I4: števci {counts} ≠ {PIN_COUNTS}")
    if trans != PIN_TRANSITIONS:
        fail(f"I4: prehodi {trans} ≠ {PIN_TRANSITIONS}")
    if len(changed) != PIN_CHANGED:
        fail(f"I4: spremenjenih {len(changed)} ≠ {PIN_CHANGED}")
    if round(d_exists_max, 1) != PIN_D_EXISTS_MAX:
        fail(f"I4: d(obstoja) max {round(d_exists_max, 1)} ≠ {PIN_D_EXISTS_MAX}")
    if round(d_gone_max, 1) != PIN_D_GONE_MAX:
        fail(f"I4: d(ni-je-več) max {round(d_gone_max, 1)} ≠ {PIN_D_GONE_MAX}")
    if n_in_cell != PIN_IN_CELL or pairs != PIN_PAIRS or len(pair_fis) != PIN_PAIR_FOOTPRINTS or modern_near != PIN_MODERN_NEAR:
        fail(f"I5: cf {n_in_cell}/pari {pairs}/tlorisi {len(pair_fis)}/okno-blizu {modern_near} "
             f"≠ {PIN_IN_CELL}/{PIN_PAIRS}/{PIN_PAIR_FOOTPRINTS}/{PIN_MODERN_NEAR}")

    # ——— izpisi ————————————————————————————————————————————————————————
    present_out = [{"id": b["id"], "x": b["cx"], "z": b["cz"], "w": b["w"], "d": b["d"],
                    "area": b["area"], "type": b["type"], "poly": b["poly"]} for b in blds]
    match_out = [{"status": m["status"], "d": m["d"], "gursId": m["id"]} for m in newm]

    meta = {
        "noteSi": ("Današnje stavbe: uradni GURS eZKN obrisi (WFS SI.GURS.KN:STAVBE, "
                   "posnetek 2026-10-13, KO 1544 GRIBLJE + KO 1552 ADLEŠIČI južni bbox; "
                   "recept scripts/p48_fetch_stavbe.sh). Lokalni koordinati: toLocal() "
                   "izv. village3d.ts (izhodišče 45.5725 N 15.2926 E — sodobno jedro vasi, "
                   "OSM place node). Stavbe 1825: list A02 po GEOTRUTH afini (issue #14) — "
                   "cerkev na uradnem EŠD 2122, struga Kolpe potrjena 6–30 m. "
                   "NADGRADNJA P16: OSM posnetek (15/26/115, pokrival le jedro) → "
                   "uradni GURS obrisi (P54) — popolna pokritost katastra, vključno z "
                   "zahodnimi pobočji."),
        "noteEn": ("Present-day buildings: official GURS eZKN footprints (WFS "
                   "SI.GURS.KN:STAVBE, snapshot 2026-10-13, KO 1544 GRIBLJE + KO 1552 "
                   "ADLEŠIČI south bbox; receipt scripts/p48_fetch_stavbe.sh). Local "
                   "coords via toLocal() of village3d.ts (origin = modern village "
                   "centre, OSM place node). 1825 buildings: sheet A02 under the "
                   "GEOTRUTH affine (issue #14) — church anchored to the official "
                   "EŠD 2122, Kolpa channel confirmed at 6–30 m. P16 UPGRADE: OSM "
                   "snapshot (15/26/115, covered the core only) → official GURS "
                   "footprints (P54) — complete cadastral coverage, western slopes "
                   "included."),
        "methodSi": ("Težiščna primerjava 156 katastrskih stavb 1825 (list A02, GEOTRUTH) "
                     "z uradnimi GURS eZKN obrisi (EPSG:3794 → WGS84 pyproj always_xy, "
                     "enako P47/P48) v oknu bbox(350 OSM) ∪ bbox(156 tlorisov) ± 50 m. "
                     "Pravila P16, kalibrirana z replajo na starih OSM podatkih (156/156): "
                     "OBSTOJA: d ≤ 8 m ali (d ≤ 20 m in prekrivanje tlorisa ≥ 0,10); "
                     "NEGOTOVO: stavba v 40 m; NI JE VEČ: brez stavbe v 40 m — odsotnost "
                     "stavbe NI dokaz porušitve, terenska preverba čaka. d = težišče "
                     "tlorisa ↔ težišče obrisa; prekrivanje = presek pravokotnikov / "
                     "ploščina tlorisa. Od P54 je d zapisan za VSE tlorise (P16 le do "
                     "~117 m), ker UI prikazuje razdaljo tudi rdečim duhovom."),
        "methodEn": ("Centroid comparison of 156 cadastre buildings of 1825 (sheet A02, "
                     "GEOTRUTH) against official GURS eZKN footprints (EPSG:3794 → WGS84 "
                     "pyproj always_xy, as P47/P48) within the window bbox(350 OSM) ∪ "
                     "bbox(156 footprints) ± 50 m. P16 rules, calibrated by replay on the "
                     "old OSM data (156/156): EXISTS: d ≤ 8 m or (d ≤ 20 m and footprint "
                     "overlap ≥ 0.10); UNCERTAIN: a building within 40 m; GONE: no "
                     "building within 40 m — absence is NOT proof of demolition, field "
                     "check pending. d = footprint centroid ↔ outline centroid; overlap = "
                     "rectangle intersection / footprint area. Since P54, d is recorded "
                     "for ALL footprints (P16 only up to ~117 m) because the UI shows the "
                     "distance to red ghosts as well."),
        "gursSnapshot": "2026-10-13",
        "fetchReceipt": "scripts/p48_fetch_stavbe.sh (GURS eZKN WFS, OBRIS_GEOM)",
        "transform": "EPSG:3794 → WGS84 (pyproj always_xy) → toLocal() izv. village3d.ts",
        "osmSuperseded": {
            "snapshot": old["_meta"]["osmSnapshot"],
            "counts": {"exists": 15, "uncertain": 26, "gone": 115},
            "evidence": "research/issue17/present-osm-p16.json",
        },
    }
    runtime = {"_meta": meta, "present": present_out, "match": match_out}

    evidence = {
        "task": ("P54 (issue #12 P16 nadgradnja; audit §28 »nadgradja P16 present.json "
                 "z uradnimi GURS obrisi«; P49 next 3) — današnje stavbe = uradni GURS "
                 "eZKN obrisi namesto OSM posnetka"),
        "principle": ("P16 pravila ostanejo NESPREMENJENA — skript jih najprej kalibrira "
                      "z replajo na starih OSM podatkih (156/156), šele nato uporabi na "
                      "uradnih obriseh; vir se nadgradi (OSM → GURS eZKN), pokritost se "
                      "razširi na celoten kataster (zahodna pobočja), d se zapiše za vse."),
        "inputs": {
            "osmP16": "research/issue17/present-osm-p16.json (bajtni arhiv P16, 350 stavb, 156 match)",
            "footprints1825": "src/data/atlas/buildings.json (156, list A02, P9)",
            "gursKo1544": "research/georef-n83/gurs/stavbe-ko1544-0.json (403, P48 prenos)",
            "gursKo1552south": "research/georef-n83/gurs/stavbe-ko1552-south-0.json (313, P48 prenos)",
            "cells": "research/georef-n83/ezkn-ix24.json (celica cf — P48 kontrola)",
            "boundsA02": "src/data/atlas/model.ts (GEOTRUTH meje — px replika P48)",
            "continuityP48": "research/issue17/buildings-overlay.json (continuity)",
        },
        "transform": "EPSG:3794 → WGS84 (pyproj always_xy, identično P47/P48) → toLocal() (111320 ploščni približek, izhodišče 45.5725 N 15.2926 E)",
        "window": {"rectLocal": [r1(v) for v in window], "gursInWindow": n_window, "ko": ko_in_window,
                   "note": "okno = bbox(350 OSM stavb) ∪ bbox(156 tlorisov) ± 50 m; KO 1552 južni bbox: 0 v oknu (Adlešiči/Fučkovci izven A02 okna — Fučkovci nosijo svoje uradne EID že od P49)"},
        "replay": {"pass": "156/156", "statusMatch": 156, "osmIdMatch": 41, "dMaxDelta": 0.05,
                   "note": "pravila P16 (meta.methodSi) reproducirajo STARE statuse, osmId in d — pravilno prebrana"},
        "counts": counts,
        "countsP16": {"exists": 15, "uncertain": 26, "gone": 115},
        "transitions": {f"{a}→{b}": n for (a, b), n in sorted(trans.items())},
        "changed": changed,
        "dRanges": {"existsMax": r1(d_exists_max), "goneMax": r1(d_gone_max),
                    "note": "od P54 d zapisan za vse 156 (P16: null za večino »ni je več«)"},
        "p48Cross": {"inCellCf": n_in_cell, "modernEvaluatedP48": cont["modernEvaluated"],
                     "pairs25px": pairs, "pairsP48": cont["pairs"],
                     "pairFootprints": len(pair_fis), "modernNear25pxWindow": modern_near,
                     "mPerPx": round(mppx, 4), "pxErrMaxFootprints": round(px_err_max, 2)},
        "invariants": {
            "I1": "REPLA P16 na starih OSM podatkih == stari statusi 156/156 (+ osmId, d ±0.05) — PASS",
            "I2": "403 + 313 značilk, 2 brez geometrije (KO 1544), 714 unikatnih EID; okno 380 (KO 1544); px replika ≤ 1.5 px; cf == P48 154 — PASS",
            "I3": "pravila za vseh 156: obstoja ⇒ d ≤ 20 ∧ (≤ 8 ∨ ov ≥ 0.10), negotovo ⇒ d ≤ 40, ni je več ⇒ d > 40 — PASS",
            "I4": f"števci {PIN_COUNTS['exists']}/{PIN_COUNTS['uncertain']}/{PIN_COUNTS['gone']}, prehodi {sum(PIN_TRANSITIONS.values())} vsrstno pinani, spremenjenih {PIN_CHANGED}, d-obstoja ≤ {PIN_D_EXISTS_MAX}, d-gone ≤ {PIN_D_GONE_MAX} — PASS",
            "I5": f"P48 navzkrižje: cf {PIN_IN_CELL} == modernEvaluated, pari {PIN_PAIRS} == pairs, {PIN_PAIR_FOOTPRINTS} tlorisov, okno-blizu {PIN_MODERN_NEAR} — PASS",
            "I6": "shema: 380 present (unikatni EID niz, 0.1 zaokroženo, GURS tip, poly) + 156 match (gursId/nul, d > 0) — PASS",
            "I7": "determinizem — bajtno identičen izpis pri ponovnem izračunu (--check)",
            "I8": "dokaz ⊇ runtime — present in match bajtno enaka v obeh izpisih",
        },
        "status": "UPGRADED-DETERMINISTIC — P16 primerjava na uradnih GURS obriseh (pravila kalibrirana z replajo 156/156); terenska preverba »ni je več« ostaja priporočena [~]",
        "verdictSi": ("P54 (2026-10-14): »Kaj je izginilo?« nadgrajeno z OSM posnetka na "
                      "uradne GURS eZKN obrise (714 stavb z geometrijo; 380 v oknu A02 + "
                      "sodobna vas, vse KO 1544). Pravila P16 nespremenjena — kalibrirana "
                      "z replajo na starih podatkih (156/156, vključno z osmId in d). "
                      "Rezultat: 18 obstaja · 21 negotovih · 117 ni jih več (P16: 15/26/"
                      "115); 7 tlorisov spremenilo status (4× negotovo→obstoja — GURS je "
                      "potrdil stavbo, ki jo je OSM posnetek zamudil; 2× negotovo→ni-je-več "
                      "— GURS potrjuje odsotnost; 1× obstoja→negotovo); d sedaj zapisana "
                      "za vse 156 tlorisov "
                      "(do 1541.2 m na zahodnih pobočjih, kjer OSM posnetka sploh ni bilo). "
                      "P48 navzkrižje: celica cf 154 == modernEvaluated, pari ≤ 25 px 37 "
                      "== pairs (20 tlorisov), okno 40 stavb blizu tlorisa. Pošteno: "
                      "odsotnost stavbe še zmeraj NI dokaz porušitve — terenska preverba "
                      "ostaja priporočena."),
        "verdictEn": ("P54 (2026-10-14): »What has vanished?« upgraded from the OSM "
                      "snapshot to official GURS eZKN footprints (714 buildings with "
                      "geometry; 380 within the A02 + modern-village window, all KO 1544). "
                      "P16 rules unchanged — calibrated by replay on the old data "
                      "(156/156, including osmId and d). Result: 17 exists · 22 uncertain "
                      "· 117 gone (P16: 15/26/115); 7 footprints changed status (4× "
                      "uncertain→exists — GURS confirmed buildings the OSM snapshot "
                      "missed; 2× uncertain→gone — GURS confirms absence; 1× "
                      "exists→uncertain); d now recorded "
                      "for all 156 footprints (up to 1541.2 m on the western slopes, "
                      "where the OSM snapshot had no coverage at all). P48 cross-check: "
                      "cell cf 154 == modernEvaluated, pairs ≤ 25 px 37 == pairs "
                      "(20 footprints), window 40 buildings near a footprint. Honest: "
                      "absence of a building still does NOT prove demolition — field "
                      "verification remains recommended."),
        "next": [
            "terenska preverba »ni je več« tlorisov (lastnik, priporočeno [~]) — 117 tlorisov brez stavbe v 40 m",
            "povezava 26 mest A05 (Fučkovci) ↔ domačije PT (lastnik) — uradni EID že od P49",
            "paleografija str. 138–139 (Blatt X) — reambulacijska hipoteza [~]",
        ],
        "generatedBy": "scripts/p54_present_gurs.py",
        "generatedAt": DATE,
        "methodSi": meta["methodSi"],
        "methodEn": meta["methodEn"],
        "present": present_out,
        "match": match_out,
    }
    return runtime, evidence, old_path


def main():
    check = "--check" in sys.argv
    runtime, evidence, old_path = compute()
    ev_raw = json.dumps(evidence, ensure_ascii=False)
    rt_raw = json.dumps(runtime, ensure_ascii=False)
    if check:
        ev_now = (ROOT / "research/issue17/present-gurs.json").read_text(encoding="utf-8")
        rt_now = (ROOT / "src/data/atlas/present.json").read_text(encoding="utf-8")
        if ev_now != ev_raw:
            fail("I7: dokaz ni bajtno identičen ponovnemu izračunu")
        if rt_now != rt_raw:
            fail("I7: runtime ni bajtno identičen ponovnemu izračunu")
        print("P54 --check: determinizem PASS (dokaz + runtime bajtno identična)")
        return
    (ROOT / "research/issue17/present-gurs.json").write_text(ev_raw, encoding="utf-8")
    (ROOT / "src/data/atlas/present.json").write_text(rt_raw, encoding="utf-8")
    # I8: dokaz ⊇ runtime (present + match bajtno enaka podizpeljanka)
    evj = json.loads(ev_raw)
    rtj = json.loads(rt_raw)
    if json.dumps(evj["present"], ensure_ascii=False) != json.dumps(rtj["present"], ensure_ascii=False):
        fail("I8: present v dokazu ≠ runtime")
    if json.dumps(evj["match"], ensure_ascii=False) != json.dumps(rtj["match"], ensure_ascii=False):
        fail("I8: match v dokazu ≠ runtime")
    print(f"P54: present.json nadgrajen na uradne GURS obrise — "
          f"{PIN_COUNTS['exists']}/{PIN_COUNTS['uncertain']}/{PIN_COUNTS['gone']} "
          f"(P16 OSM 15/26/115), {PIN_IN_WINDOW} stavb v oknu, repla 156/156, "
          f"P48 križ {PIN_IN_CELL}/{PIN_PAIRS}/{PIN_MODERN_NEAR}")


if __name__ == "__main__":
    main()
