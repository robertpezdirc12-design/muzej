#!/usr/bin/env python3
"""
GEOTRUTH FIX (issue #14, P0) — re-anchoring A02-derived data to the official church anchor.

Dokazna pot (evidence trail):
 1. EŠD 2122 (Register nepremične kulturne dediščine, GisKD / Ministrstvo za kulturo,
    layer MK_EVRD/3602, STANJE_POD 07-10-2026): Cerkev sv. Vida, Griblje —
    poligon centroid 45.567610 N, 15.290311 E ("na pokopališču, na gričku južno od vasi").
 2. OSM: stavba Sv. Vid (way 284847361, 45.567677/15.290388) + pokopališče
    (way 284847363) — oba znotraj uradnega poligona (≤ 8 m od centroida).
 3. List A02: cerkev narisana na px(1995,577) (apsida, križ, rdeča, pokopališki obrobl);
    stara afina preslikava (bounds v model.ts) je bila KROŽNA — cerkev sama je bila
    kontrolna točka s predpostavljeno (napačno) koordinato 45.5728/15.2922.
 4. Struga Kolpe na listu (desni krak, VLM sledjenje x≈2765–2890 pri y 100–1400)
    se s sodobno strugo (OSM) ujema le pod cerkveno zasidrano afino (6–30 m),
    pod staro pa odstopa 80–130 m.
 5. Kontrolni točki lista A01 se pod popravkom konsistentno re-interpretirata:
    »jedro vasi« (A01 px 2091,1773) je pravzaprav cerkev+ pokopališče (34 m od EŠD 2122),
    »severna skupina« (A01 px 2063,1477) pa severni rob vasi 1825.

Popravek: translacija vseh iz listov izpeljanih podatkov (stavbe 1825, raba tal)
za dlat = −0.005190, dlng = −0.001889 (≈ −147 m E, +578 m J).
Prisotnostne sheme (Kaj je izginilo) se preračunajo na nove lege.
"""

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ——— uradna sidra ———
CHURCH_OFFICIAL = (45.567610, 15.290311)      # EŠD 2122, centroid poligona
CHURCH_OLD = (45.5728, 15.2922)               # stara (krožna) predpostavka
DLAT = CHURCH_OFFICIAL[0] - CHURCH_OLD[0]     # −0.005190
DLNG = CHURCH_OFFICIAL[1] - CHURCH_OLD[1]     # −0.001889

ORIGIN = (45.5725, 15.2926)                    # lokalni izhodiščni okvir (OSTANE — sodobno jedro, OSM)
M_LAT = 111320.0
M_LNG = 111320.0 * math.cos(math.radians(ORIGIN[0]))

def to_local(lat, lng):
    return ((lng - ORIGIN[1]) * M_LNG, -(lat - ORIGIN[0]) * M_LAT)

def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def main():
    # 1) stavbe 1825 — translacija
    bpath = ROOT / "src/data/atlas/buildings.json"
    blds = json.loads(bpath.read_text())
    for b in blds:
        b["lat"] = round(b["lat"] + DLAT, 6)
        b["lng"] = round(b["lng"] + DLNG, 6)
    bpath.write_text(json.dumps(blds, ensure_ascii=False) + "\n")
    print(f"buildings.json: {len(blds)} stavb premaknjenih za dlat={DLAT:.6f}, dlng={DLNG:.6f}")

    # 2) present.json — prisotnostna shema na novih legah (OSM stavbe se NE premikajo)
    ppath = ROOT / "src/data/atlas/present.json"
    data = json.loads(ppath.read_text())
    pres = data["present"]  # x, z, w, d (lokalni metri, res)

    p1825 = []
    for b in blds:
        x, z = to_local(b["lat"], b["lng"])
        p1825.append((x, z, b["w"], b["h"]))

    # prostorski indeks
    cell = 60.0
    idx = {}
    for i, q in enumerate(pres):
        idx.setdefault((int(q["x"] // cell), int(q["z"] // cell)), []).append(i)

    def near_indices(x, z, r=45.0):
        kx, kz = int(x // cell), int(z // cell)
        span = int(r // cell) + 1
        out = []
        for dx in range(-span, span + 1):
            for dz in range(-span, span + 1):
                out.extend(idx.get((kx + dx, kz + dz), []))
        return out

    def rect_overlap(a, wa, da, b, wb, db):
        """prekrivanje dveh osno poravnanih pravokotnikov (m²)"""
        ox = max(0.0, min(a[0] + wa / 2, b[0] + wb / 2) - max(a[0] - wa / 2, b[0] - wb / 2))
        oz = max(0.0, min(a[1] + da / 2, b[1] + db / 2) - max(a[1] - da / 2, b[1] - db / 2))
        return ox * oz

    match = []
    for (x, z, w, d) in p1825:
        cands = near_indices(x, z)
        best_d, best_i, best_ov = None, None, 0.0
        for i in cands:
            q = pres[i]
            dd = math.hypot(x - q["x"], z - q["z"])
            ov = rect_overlap((x, z), w, d, (q["x"], q["z"]), q["w"], q["d"])
            if best_d is None or dd < best_d:
                best_d, best_i = dd, i
            if ov > best_ov:
                best_ov = ov
        own_area = max(w * d, 1e-6)
        if best_d is None:
            match.append({"status": "gone", "d": None, "osmId": None})
            continue
        osm_id = pres[best_i]["id"] if best_i is not None else None
        # metodologija (enaka kot prej): OBSTOJA d≤8 ali (d≤20 & prekrivanje ≥0,10);
        # NEGOTOVO: stavba v 40 m ali majhna stavba na tlorisu (prekrivanje ≥0,05);
        # sicer NI JE VEČ (odsotnost v OSM ni dokaz porušitve).
        if best_d <= 8 or (best_d <= 20 and best_ov / own_area >= 0.10):
            match.append({"status": "exists", "d": round(best_d, 1), "osmId": osm_id})
        elif best_d <= 40 or best_ov / own_area >= 0.05:
            match.append({"status": "uncertain", "d": round(best_d, 1), "osmId": osm_id})
        else:
            match.append({"status": "gone", "d": round(min(best_d, 9000), 1) if best_d < 9000 else None, "osmId": None})

    from collections import Counter
    counts = Counter(m["status"] for m in match)
    data["match"] = match
    data["_meta"]["methodSi"] = (
        "Primerjava težišč 156 katastrskih stavb 1825 z današnjimi OSM stavbami "
        "(hiše/gospodarske, brez garaž/lop) na GEOTRUTH popravljeni georeferenci "
        "(cerkev zasidrana na EŠD 2122, list A02 transliran za −147 m E / +578 m J). "
        "OBSTOJA: d ≤ 8 m ali (d ≤ 20 m in prekrivanje tlorisa ≥ 0,10). NEGOTOVO: "
        "stavba v 40 m ali majhna stavba na tlorisu. NI JE VEČ: brez stavbe v 40 m — "
        "odsotnost v OSM NI dokaz porušitve, terenska preverba čaka."
    )
    data["_meta"]["noteSi"] = (
        "Današnje stavbe: OpenStreetMap (posnetek 2026-10-07, ODbL). Lokalni koordinati: "
        "toLocal() izv. village3d.ts (izhodišče 45.5725 N 15.2926 E — sodobno jedro vasi, "
        "OSM place node). Stavbe 1825: list A02 po GEOTRUTH afini (issue #14) — cerkev na "
        "uradnem EŠD 2122, struga Kolpe potrjena 6–30 m."
    )
    data["_meta"]["noteEn"] = (
        "Present-day buildings: OpenStreetMap snapshot 2026-10-07 (ODbL). Local coords via "
        "toLocal() of village3d.ts (origin = modern village centre, OSM place node). 1825 "
        "buildings: sheet A02 under the GEOTRUTH affine (issue #14) — church anchored to the "
        "official EŠD 2122, Kolpa channel confirmed at 6–30 m."
    )
    ppath.write_text(json.dumps(data, ensure_ascii=False) + "\n")
    print(f"present.json: nova shema — obstaja {counts.get('exists',0)}, negotovo {counts.get('uncertain',0)}, ni jih več {counts.get('gone',0)} (+1 cerkev)")

    # 3) statistika za nadaljnje konstante
    core = [(x, z) for (x, z, w, d) in p1825]
    zs = sorted(z for _, z in core)
    xs = sorted(x for x, _ in core)
    print(f"\n1825 (popravljeno): z {zs[0]:.0f}..{zs[-1]:.0f}, x {xs[0]:.0f}..{xs[-1]:.0f}")
    print(f"  z percentili: p10={zs[15]:.0f} p25={zs[39]:.0f} p50={zs[78]:.0f} p75={zs[117]:.0f} p90={zs[140]:.0f}")

    # jedro = pas vasi (z 155..1050), težišče + severna skupina
    ribbon = [(x, z) for (x, z) in core if 155 <= z <= 1050]
    cx = sum(p[0] for p in ribbon) / len(ribbon)
    cz = sum(p[1] for p in ribbon) / len(ribbon)
    north = [(x, z) for (x, z) in core if 155 <= z <= 520]
    nx = sum(p[0] for p in north) / len(north)
    nz = sum(p[1] for p in north) / len(north)
    print(f"  pas vasi ({len(ribbon)} stavb): težišče ({cx:.0f}, {cz:.0f})")
    print(f"  severna skupina ({len(north)} stavb): ({nx:.0f}, {nz:.0f})")
    def to_latlng(x, z):
        return (ORIGIN[0] - z / M_LAT, ORIGIN[1] + x / M_LNG)
    print(f"  jedro TimeSpot (severna skupina): lat/lng = {to_latlng(nx, nz)[0]:.5f}, {to_latlng(nx, nz)[1]:.5f}")

    # 4) raba tal — zamik con za poročilo
    print("\nRABA TAL (apply dlat/dlng ročno v landuse.ts):")
    lpath = ROOT / "src/data/atlas/landuse.ts"
    txt = lpath.read_text()
    import re
    for m in re.finditer(r"\[\s*\[([0-9.]+),\s*([0-9.]+)\],\s*\[([0-9.]+),\s*([0-9.]+)\]\s*\]", txt):
        n, w, s, e = (float(m.group(i)) for i in (1, 2, 3, 4))
        print(f"  [{n:.4f}, {w:.4f}] → [{s:.4f}, {e:.4f}]  =>  [{n+DLAT:.4f}, {w+DLNG:.4f}] → [{s+DLAT:.4f}, {e+DLNG:.4f}]")

if __name__ == "__main__":
    sys.exit(main())
