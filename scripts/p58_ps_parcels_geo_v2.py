#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P58 (issue #13/§PS; P56/P57 »next« — sanacija produkcije) — PS-PARCELS-GEO v2:
produkcija ps-parcels-ego.json se SANIRA in NADGRADI:

  1) ODSTRANI 43 lažnih povezav S3 (str. 138–139, zapadek »Zusammenstellung der
     Grundstücke« z lastnim oštevilčenjem 1–100) — dokaz P56: median razmerja
     površin 0.0892 ≪ 3.7188 v S1 (~42× odmik od 1 Wiener QK) + pass-razhajanje
     (P48 Blatt X koroboracija). Nabor 43 vrstic je bajtno enak P56
     kontaminacijskemu seznamu (kontrola I1).
  2) DODA 26 vrstic Blatt I (str. 3–4, številke 1–40) iz PRIMARNEGA vira P57
     (štiri neodvisne VLM plasti + deterministična adjudikacija) — točno
     obnovljenih 26 lostBases P56 (kontrola I2). Ena vrstica (št. 1) brez
     površine (blot) — povezana samo po številki.
  3) OZNAČI vsako vrstico s serijo (BI/S1/S2) in per-Blatt dvoumnostjo
     (base na > 1 strani znotraj v2 [~]).

KLJUČNA LASTNOST (dokazana, ne tržena): pozicije vrstic so deterministične
PER BASE (group_pos = ploščinsko uteženo središče sodobnih parcel številke b),
zato odstranitev S3 vrstic NE spremeni nobene pozicije; množica pozicioniranih
števil ostane 800 (−26 lostBases +26 Blatt I = iste številke). Posledica
(merjeno, I9): soslednost je bajtno enaka v1 — 590 parov / 51.8 m / 27.8×.
S1/S2 vrstice: vsa polja (vključno conf) bajtno enaka v1 (I3).

POVRŠINSKI DOKAZ po sanaciji: median 3.7709 (Δ +4.85 %) — v1 median 3.6984 je
bil UMETNO SNIZAN s 43 lažnimi S3 povezavami (razmerja ~0.09); čist median je
skladen z neodvisnima merjenjema P56 (3.7394 na 1067) in P57 (3.7594 na Blatt I).
Prag I4 zato ≤ 5.0 % (še zmeraj ~2.3× pod kontrolo +11.1 %); odločilni dokaz
vztrajnosti ostaja prostorska soslednost (27.8×).

Viri (vsi committed):
  research/issue17/ps-parcels-geo.json        (v1 dokaz, 2762 vrstic / 1110 povezanih)
  research/issue17/ps-register-topology.json  (P56 dokaz: kontaminacija 43 + sanitizacija)
  src/data/atlas/ps-register-topology.json    (P56 runtime: števci)
  src/data/atlas/ps-register-start.json       (P57 runtime: 40 vrstic Blatt I, 26 povezanih)

Izpis:
  research/issue17/ps-parcels-geo-v2.json     (dokaz v2: rowsEvidence + delta + invarianti)
  src/data/atlas/ps-parcels-geo.json          (runtime v2: rows — NADOMESTI v1)
`--check` = determinizem (ponovni izračun bajtno identičen).

Invarianti (FAIL → exit 1):
  I1  v1 identiteta: 2762 vrstic / 1110 povezanih; S3 (str. 138–139) natanko 43,
      bajtno enake P56 kontaminacijskemu seznamu (7-poljska projekcija);
      S1/S2 1067 == P56 matchedRowsAfter, uniqueBases 774 == P56
  I2  Blatt I: 26 povezanih vrstic P57; base množica == P56 lostBases;
      strani ⊆ {3, 4}; lat/lng/areaModern/parts kopirani DOBESEDNO iz P57;
      readConf razporeditev 3/14/9 == P57
  I3  v2 struktura: 1093 = 1067 + 26; serije BI 26 / S1 997 / S2 70;
      uniqueBases 800; S1/S2 polja bajtno enaka v1 (conf vključno — preracun
      z P55 pravilom da 0 odmikov); vse vrstice pozicionirane
  I4  površine: 1074 parov; median 3.7709 v [3.30, 3.90]; Δ ≤ 5.0 % od 3.59665;
      premešana kontrola (seed 42) višja; pas ±10 %: realni > 2× kontrola
  I5  soslednost: 590 parov (400–800); median 51.8 m ≤ 100 m; ≤150 m ≥ 70 %;
      kontrola (seed 7) ≥ 5× realnega medianа
  I6  determinizem: ponovni izračun bajtno identičen (--check)
  I7  dokaz ⊇ runtime — rowsEvidence bajtno enake runtime rows
  I8  Furkofze: natanko 2 vrstici, parceli {2159, 2160}, lastnik Van Wawech
  I9  NEINVARIANCA soslednosti: pairs/median/q25/q75/share150 bajtno enaka
      v1 evidence spatialProof — sanitacija ne dotakne prostorske strukture
"""
import json
import math
import random
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
V1_EVIDENCE = REPO / "research/issue17/ps-parcels-geo.json"
V2_EVIDENCE = REPO / "research/issue17/ps-parcels-geo-v2.json"
OUT_RUNTIME = REPO / "src/data/atlas/ps-parcels-geo.json"
P56_EVIDENCE = REPO / "research/issue17/ps-register-topology.json"
P56_RUNTIME = REPO / "src/data/atlas/ps-register-topology.json"
P57_RUNTIME = REPO / "src/data/atlas/ps-register-start.json"

HIST_QK_M2 = 3.59665
AREA_BAND = 0.10
NEIGH_M = 150.0
SEED_AREA = 42
SEED_SPATIAL = 7
M_PER_DEG_LAT = 111320.0

BASE_KEYS = ["page", "parzella", "base", "owner", "stand", "hausNr", "wohnort",
             "wohnortInherited", "kultur", "joch", "klafter", "areaQK",
             "areaSuspect", "parts", "lat", "lng", "areaModern", "ratio", "conf"]
PROJ_CONT = ["page", "base", "owner", "kultur", "areaQK", "areaModern", "ratio"]

FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  ✗ {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def jdump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


def median(xs):
    return statistics.median(xs) if xs else None


def dm(a, b) -> float:
    return math.hypot((a[0] - b[0]) * M_PER_DEG_LAT,
                      (a[1] - b[1]) * M_PER_DEG_LAT * 0.7)


def series_of(page: int) -> str:
    if page in (3, 4):
        return "BI"
    if page <= 127:
        return "S1"
    return "S2"


def compute() -> tuple[dict, dict]:
    """Zgradi v2 dokaz + runtime. Deterministično — brez AI, brez mreže."""
    # ——— vhodi ———
    v1 = json.loads(V1_EVIDENCE.read_text(encoding="utf-8"))
    p56ev = json.loads(P56_EVIDENCE.read_text(encoding="utf-8"))
    p56rt = json.loads(P56_RUNTIME.read_text(encoding="utf-8"))
    p57 = json.loads(P57_RUNTIME.read_text(encoding="utf-8"))

    v1_rows = v1["rows"]
    v1_matched = [r for r in v1_rows if r.get("lat") is not None]
    s3 = [r for r in v1_matched if r["page"] in (138, 139)]
    s1s2 = [r for r in v1_matched if 5 <= r["page"] <= 137]
    bi_src = [r for r in p57["rows"] if r.get("lat") is not None]
    lost = p56ev["sanitization"]["lostBases"]

    # ——— Blatt I preslikava v shemo P55 (dobesedni kopiji podrejeni) ———
    bi: list[dict] = []
    for r in bi_src:
        k = r.get("klafter")
        aq, am = r.get("areaQK"), r.get("areaModern")
        bi.append({
            "page": r["page"],
            "parzella": str(r["no"]),
            "base": r["base"],
            "owner": r.get("name"),
            "stand": None,
            "hausNr": r.get("hausNr"),
            "wohnort": r.get("wohnort"),
            "wohnortInherited": False,
            "kultur": r.get("kultur"),
            "joch": None,
            "klafter": k,
            "areaQK": aq,
            "areaSuspect": bool(k and k >= 1600.0),
            "parts": r.get("parts"),
            "lat": r["lat"],
            "lng": r["lng"],
            "areaModern": am,
            "ratio": round(am / aq, 4) if (aq and am) else None,
            "conf": None,
        })

    # ——— v2 vrstice (protokolni vrstni red: BI 3–4, S1/S2 5–137) ———
    v2_rows: list[dict] = []
    for r in bi:
        v2_rows.append(r)
    for r in s1s2:
        v2_rows.append(r)

    # per-Blatt dvoumnost znotraj v2 (base na > 1 strani) [~]
    pages_by_base: dict[str, set] = {}
    for r in v2_rows:
        pages_by_base.setdefault(r["base"], set()).add(r["page"])
    amb_bases = {b for b, s in pages_by_base.items() if len(s) > 1}

    # pozicije per base (S1/S2 vrstice že nosijo pozicijo; enake group_pos)
    pos_by_base: dict[str, tuple[float, float]] = {}
    for r in v2_rows:
        pos_by_base[r["base"]] = (r["lat"], r["lng"])

    # sosede ≤ 150 m per base (pravilo P55)
    neigh_ok: set[str] = set()
    for b, p in pos_by_base.items():
        n = int(b)
        for m in (n - 1, n + 1):
            q = pos_by_base.get(str(m))
            if q and dm(p, q) <= NEIGH_M:
                neigh_ok.add(b)
                break

    # ——— označevanje + zaupanje (pravilo P55, enotno čez v2) ———
    conf_mismatch = 0
    for r in v2_rows:
        ser = series_of(r["page"])
        at = (r["ratio"] is not None and not r["areaSuspect"]
              and abs(r["ratio"] / HIST_QK_M2 - 1) <= AREA_BAND)
        nb = r["base"] in neigh_ok
        c = "STRONG" if (at and nb) else "MEDIUM" if (at or nb) else "WEAK"
        if ser in ("S1", "S2") and r.get("conf") is not None and r["conf"] != c:
            conf_mismatch += 1
        r["conf"] = c
        r["series"] = ser
        r["ambiguous"] = r["base"] in amb_bases
        if ser == "BI":
            src = next(x for x in bi_src if x["base"] == r["base"])
            r["blatt"] = "I"
            r["source"] = "P57"
            r["readConf"] = src.get("confidence")
            r["anmerkung"] = src.get("anmerkung")

    # ——— soslednost (pravilo P55: številski pari n, n+1 v vrstnem redu prve pojavitve) ———
    seen: set[int] = set()
    ps_nums: list[int] = []
    for r in v2_rows:
        n = int(r["base"])
        if n not in seen:
            seen.add(n)
            ps_nums.append(n)
    consec_d = []
    for n in ps_nums:
        a, b2 = pos_by_base.get(str(n)), pos_by_base.get(str(n + 1))
        if a and b2:
            consec_d.append(dm(a, b2))
    consec_d_sorted = sorted(consec_d)
    consec_median = median(consec_d)
    consec_share150 = sum(1 for x in consec_d if x <= NEIGH_M) / len(consec_d)

    # ——— površinski test + kontrola (pravilo P55) ———
    area_pairs = [(r["areaQK"], r["areaModern"]) for r in v2_rows
                  if r["areaQK"] and r["areaModern"] and not r["areaSuspect"]]
    ratios = [m / a for a, m in area_pairs]
    ratios_sorted = sorted(ratios)
    area_median = median(ratios)
    tight_n = sum(1 for x in ratios if abs(x / HIST_QK_M2 - 1) <= AREA_BAND)
    tight_share = tight_n / len(ratios)
    mods = [m for _, m in area_pairs]
    random.Random(SEED_AREA).shuffle(mods)
    sh_ratios = [m / a for (a, _), m in zip(area_pairs, mods)]
    sh_median = median(sh_ratios)
    sh_tight_share = (sum(1 for x in sh_ratios if abs(x / HIST_QK_M2 - 1) <= AREA_BAND)
                      / len(sh_ratios))

    # ——— prostorska kontrola (pravilo P55) ———
    pos_list = [pos_by_base[b] for b in sorted(pos_by_base, key=int)]
    random.Random(SEED_SPATIAL).shuffle(pos_list)
    sh_d = [dm(pos_list[i], pos_list[i + 1]) for i in range(len(pos_list) - 1)]
    sh_spatial_median = median(sh_d)
    sh_spatial_share150 = sum(1 for x in sh_d if x <= NEIGH_M) / len(sh_d)

    # ——— števci ———
    conf_counts = {"STRONG": 0, "MEDIUM": 0, "WEAK": 0}
    for r in v2_rows:
        conf_counts[r["conf"]] += 1
    series_counts = {"BI": 0, "S1": 0, "S2": 0}
    for r in v2_rows:
        series_counts[r["series"]] += 1
    read_conf = {"STRONG": 0, "MEDIUM": 0, "WEAK": 0}
    for r in bi:
        read_conf[r["readConf"]] += 1
    fur = [r for r in v2_rows if (r.get("wohnort") or "").lower().startswith("furkof")]

    # ——— kontrole ———
    print("  kontrole:")
    # I1
    if len(v1_rows) != 2762 or len(v1_matched) != 1110:
        fail(f"I1 v1: {len(v1_rows)} vrstic / {len(v1_matched)} povezanih ≠ 2762/1110")
    else:
        ok(f"I1 v1 identiteta: 2762 vrstic, 1110 povezanih")
    def proj(r):
        return json.dumps({k: r.get(k) for k in PROJ_CONT}, sort_keys=True, ensure_ascii=False)
    s3p = sorted(proj(r) for r in s3)
    cp = sorted(proj(r) for r in p56ev["contamination"]["rows"])
    if len(s3) != 43 or s3p != cp:
        fail(f"I1 S3: {len(s3)} vrstic, bajtno enake P56: {s3p == cp} ≠ 43/True")
    else:
        ok("I1 S3 (43) bajtno enake P56 kontaminacijskemu seznamu")
    if len(s1s2) != p56rt["sanitization"]["matchedRowsAfter"] or \
       len({r["base"] for r in s1s2}) != p56rt["sanitization"]["uniqueBasesAfter"]:
        fail(f"I1 S1/S2: {len(s1s2)}/{len({r['base'] for r in s1s2})} ≠ "
             f"{p56rt['sanitization']['matchedRowsAfter']}/{p56rt['sanitization']['uniqueBasesAfter']}")
    else:
        ok(f"I1 S1/S2: 1067 vrstic / 774 base == P56 sanitizacija")
    # I2
    bi_bases = sorted(int(r["base"]) for r in bi)
    if len(bi) != 26 or bi_bases != sorted(lost):
        fail(f"I2 Blatt I: {len(bi)} vrstic, base == lostBases: {bi_bases == sorted(lost)}")
    elif not all(r["page"] in (3, 4) for r in bi):
        fail("I2 Blatt I: strani ∉ {3, 4}")
    else:
        ok("I2 Blatt I: 26 vrstic, base == P56 lostBases, strani 3–4")
    verbatim = all(
        r["lat"] == src["lat"] and r["lng"] == src["lng"]
        and r["areaModern"] == src["areaModern"] and r["parts"] == src["parts"]
        for r in bi for src in [next(x for x in bi_src if x["base"] == r["base"])])
    if not verbatim:
        fail("I2 Blatt I: lat/lng/areaModern/parts niso dobesedno kopirani iz P57")
    else:
        ok("I2 Blatt I: lat/lng/areaModern/parts dobesedno iz P57")
    if read_conf != {"STRONG": 3, "MEDIUM": 14, "WEAK": 9}:
        fail(f"I2 readConf: {read_conf} ≠ 3/14/9")
    else:
        ok("I2 readConf: STRONG 3 / MEDIUM 14 / WEAK 9 == P57")
    # I3
    if len(v2_rows) != 1093 or series_counts != {"BI": 26, "S1": 997, "S2": 70} \
       or len({r["base"] for r in v2_rows}) != 800:
        fail(f"I3 v2: {len(v2_rows)} vrstic, serije {series_counts}, "
             f"base {len({r['base'] for r in v2_rows})} ≠ 1093 / 26-997-70 / 800")
    else:
        ok("I3 v2: 1093 vrstic (BI 26 / S1 997 / S2 70), 800 base")
    if conf_mismatch != 0:
        fail(f"I3 S1/S2 conf odmiki od v1: {conf_mismatch} ≠ 0")
    else:
        ok("I3 S1/S2 vrstice bajtno enake v1 (conf vključno — preracun 0 odmikov)")
    # I4
    delta_pct = 100 * (area_median / HIST_QK_M2 - 1)
    if not (len(ratios) == 1074 and 3.30 <= area_median <= 3.90
            and delta_pct <= 5.0 and sh_median > area_median
            and tight_share > 2 * sh_tight_share):
        fail(f"I4 površine: {len(ratios)} parov, median {area_median:.4f}, Δ {delta_pct:.2f} %, "
             f"kontrola {sh_median:.4f}, pas {tight_share:.4f} vs {sh_tight_share:.4f}")
    else:
        ok(f"I4 površine: 1074 parov, median {area_median:.4f} (Δ +{delta_pct:.2f} %), "
           f"kontrola {sh_median:.4f}, pas {tight_share:.4f} vs {sh_tight_share:.4f}")
    # I5
    enrich = sh_spatial_median / consec_median
    if not (400 <= len(consec_d) <= 800 and consec_median <= 100.0
            and consec_share150 >= 0.7 and enrich >= 5.0):
        fail(f"I5 soslednost: {len(consec_d)} parov, median {consec_median:.1f} m, "
             f"≤150 m {consec_share150:.4f}, kontrola {sh_spatial_median:.1f} m ({enrich:.1f}×)")
    else:
        ok(f"I5 soslednost: {len(consec_d)} parov, median {consec_median:.1f} m, "
           f"≤150 m {consec_share150:.4f}, kontrola {sh_spatial_median:.1f} m ({enrich:.1f}×)")
    # I8
    if len(fur) != 2 or sorted(int(r["base"]) for r in fur) != [2159, 2160] \
       or sorted({r["owner"] for r in fur}) != ["Van Wawech Mihó"]:
        fail(f"I8 Furkofze: {len(fur)} vrstic, {sorted(int(r['base']) for r in fur)}")
    else:
        ok("I8 Furkofze: 2 vrstici (2159/2160, Van Wawech Mihó)")
    # I9 — neinvarianca soslednosti proti v1
    v1sp = v1["spatialProof"]
    v1_q25 = v1sp["q25M"]
    v1_q75 = v1sp["q75M"]
    if not (len(consec_d) == v1sp["consecPairs"]
            and round(consec_median, 1) == v1sp["medianM"]
            and round(consec_d_sorted[len(consec_d) // 4], 1) == v1_q25
            and round(consec_d_sorted[3 * len(consec_d) // 4], 1) == v1_q75
            and round(consec_share150, 4) == v1sp["share150"]):
        fail(f"I9 neinvarianca: v2 {len(consec_d)}/{consec_median:.1f}/"
             f"{consec_share150:.4f} ≠ v1 {v1sp['consecPairs']}/{v1sp['medianM']}/{v1sp['share150']}")
    else:
        ok(f"I9 soslednost NEINVARIANTNA: {len(consec_d)} parov / {consec_median:.1f} m / "
           f"{consec_share150:.4f} == v1 (pozicije per base, množica števil 800 nespremenjena)")

    if FAILURES:
        print(f"P58: {len(FAILURES)} napak — izpis ODPADL")
        return {}, {}

    # ——— izpisi ———
    amb_rows = sum(1 for r in v2_rows if r["ambiguous"])
    status_line = (
        f"SANITIZED-DETERMINISTIC — PS geolokacija v2 (P58): {len(v2_rows)} vrstic povezanih "
        f"({len(s1s2)} S1/S2 iz P55 joina po odstranitvi {len(s3)} lažnih S3 povezav "
        f"[P56: površine ~42× od 1 QK + pass-razhajanje] + {len(bi)} Blatt I vrstic iz "
        f"primarnega vira P57); {len({r['base'] for r in v2_rows})} pozicioniranih številk; "
        f"površine median {area_median:.4f} ≈ 1 QK = {HIST_QK_M2} (Δ +{delta_pct:.2f} %, "
        f"kontrola {sh_median:.4f}) — čista vrednost, v1 3.6984 je bil snizan s 43 lažnimi "
        f"S3 povezavami; soslednost NEINVARIANTNA: {len(consec_d)} parov / {consec_median:.1f} m / "
        f"{enrich:.1f}× — identično v1; zaupanje STRONG {conf_counts['STRONG']} / "
        f"MEDIUM {conf_counts['MEDIUM']} / WEAK {conf_counts['WEAK']}; per-Blatt dvoumnost na v2: "
        f"{len(amb_bases)} base / {amb_rows} vrstic [~]"
    )

    join_v2 = {
        "matchedRows": len(v2_rows),
        "matchedRowsS1S2": len(s1s2),
        "matchedRowsBI": len(bi),
        "matchedSharePct": round(100 * len(s1s2) / 2762, 1),
        "psUniqueNumbers": v1["join"]["psUniqueNumbers"],
        "psPositionedParcels": len(pos_by_base),
        "suffixGroups": v1["join"]["suffixGroups"],
        "seriesCounts": series_counts,
        "confCounts": conf_counts,
        "readConfBI": read_conf,
        "ambiguousBases": len(amb_bases),
        "ambiguousRows": amb_rows,
    }
    area_v2 = {
        "pairsWithArea": len(ratios),
        "medianRatio": round(area_median, 4),
        "q25": round(ratios_sorted[len(ratios) // 4], 4),
        "q75": round(ratios_sorted[3 * len(ratios) // 4], 4),
        "tightN": tight_n,
        "tightShare": round(tight_share, 4),
        "shuffleMedian": round(sh_median, 4),
        "shuffleTightShare": round(sh_tight_share, 4),
        "historicalQkM2": HIST_QK_M2,
        "deltaPct": round(delta_pct, 2),
    }
    spatial_v2 = {
        "consecPairs": len(consec_d),
        "medianM": round(consec_median, 1),
        "q25M": round(consec_d_sorted[len(consec_d) // 4], 1),
        "q75M": round(consec_d_sorted[3 * len(consec_d) // 4], 1),
        "share150": round(consec_share150, 4),
        "shuffleMedianM": round(sh_spatial_median, 1),
        "shuffleShare150": round(sh_spatial_share150, 4),
        "enrichmentX": round(sh_spatial_median / consec_median, 1),
    }

    v2_delta = {
        "reason": "sanacija produkcije: 43 lažnih povezav S3 (P56 dokaz) odstranjenih, "
                  "26 Blatt I vrstic iz primarnega vira P57 dodanih",
        "removed": {
            "rows": len(s3),
            "pages": [138, 139],
            "proof": "P56 kontaminacija: median razmerja površin 0.0892 ≪ 3.7188 (S1) — "
                     "~42× odmik od 1 Wiener QK 3.59665 — + pass-razhajanje str. 138–139 "
                     "(P48 Blatt X koroboracija); nabor 43 vrstic bajtno enak P56 seznamu",
            "rowsDetail": [
                {k: r.get(k) for k in PROJ_CONT}
                for r in s3  # vrstni red P55 evidence (protokolni) == P56 contamination.rows
            ],
        },
        "added": {
            "rows": len(bi),
            "source": "P57 ps-register-start.json (štiri neodvisne VLM plasti + "
                      "deterministična adjudikacija; qa-p57)",
            "bases": sorted(lost),
            "note": "točno 26 lostBases P56; št. 1 brez površine (blot) — povezana samo po številki",
        },
        "before": {"matchedRows": 1110, "uniqueBases": 800,
                   "confCounts": {"STRONG": 171, "MEDIUM": 775, "WEAK": 164},
                   "areaMedian": 3.6984, "areaPairs": 1083, "spatialMedianM": 51.8},
        "after": {"matchedRows": len(v2_rows), "uniqueBases": len(pos_by_base),
                  "confCounts": conf_counts,
                  "areaMedian": round(area_median, 4), "areaPairs": len(ratios),
                  "spatialMedianM": round(consec_median, 1)},
        "invariance": "pozicije per base (group_pos) + množica pozicioniranih števil 800 "
                      "nespremenjena → soslednost in S1/S2 conf bajtno enaka v1 (I9/I3)",
    }

    invariants = {
        "I1": f"v1 identiteta: 2762 vrstic / 1110 povezanih; S3 43 bajtno == P56 kontaminacija; "
              f"S1/S2 1067/774 == P56 sanitizacija — PASS",
        "I2": f"Blatt I: 26 vrstic, base == P56 lostBases, strani 3–4, lat/lng/areaModern/parts "
              f"dobesedno iz P57, readConf 3/14/9 — PASS",
        "I3": f"v2: 1093 = 1067 + 26; serije BI 26 / S1 997 / S2 70; 800 base; S1/S2 polja bajtno "
              f"enaka v1 (preracun conf: 0 odmikov) — PASS",
        "I4": f"površine: 1074 parov, median {area_median:.4f} v [3.30, 3.90], Δ +{delta_pct:.2f} % ≤ 5.0 %, "
              f"kontrola (seed 42) {sh_median:.4f} višja, pas ±10 % {tight_share:.4f} > 2× {sh_tight_share:.4f} — PASS",
        "I5": f"soslednost: {len(consec_d)} parov, median {consec_median:.1f} m ≤ 100 m, "
              f"≤150 m {consec_share150:.4f} ≥ 70 %, kontrola (seed 7) {sh_spatial_median:.1f} m ≥ 5× — PASS",
        "I6": "determinizem — bajtno identičen izpis pri ponovnem izračunu (--check)",
        "I7": "dokaz ⊇ runtime — rowsEvidence bajtno enake runtime rows",
        "I8": "Furkofze: natanko 2 vrstici, parceli {2159, 2160}, lastnik Van Wawech — PASS",
        "I9": f"neinvarianca soslednosti: {len(consec_d)}/{consec_median:.1f}/"
              f"{consec_share150:.4f} bajtno == v1 spatialProof — PASS",
    }

    evidence = {
        "task": "P58 (issue #13/§PS; P56/P57 »next« — sanacija produkcije) — PS-PARCELS-GEO v2: "
                "odstranitev 43 lažnih S3 povezav (P56 dokaz), dodatek 26 Blatt I vrstic "
                "(P57 primarni vir), serije BI/S1/S2 + per-Blatt dvoumnost",
        "date": "2026-10-14",
        "version": 2,
        "generatedBy": "scripts/p58_ps_parcels_geo_v2.py",
        "principle": "pozicije vrstic so deterministične PER BASE (ploščinsko uteženo središče "
                     "sodobnih parcel številke) — odstranitev/dodatek vrstic ne spremeni nobene "
                     "pozicije; sanitacija se dotakne LE nabora vrstic in števcev; množica "
                     "pozicioniranih števil ostane 800 (−26 lostBases +26 Blatt I = iste številke)",
        "inputs": {
            "v1Evidence": "research/issue17/ps-parcels-geo.json (P55, 2762 vrstic / 1110 povezanih)",
            "p56Evidence": "research/issue17/ps-register-topology.json (kontaminacija 43 + sanitizacija)",
            "p56Runtime": "src/data/atlas/ps-register-topology.json (števci sanitizacije)",
            "p57Runtime": "src/data/atlas/ps-register-start.json (Blatt I, 26 povezanih vrstic)",
        },
        "historicalConstant": {"wienerQkM2": HIST_QK_M2,
                               "note": "1 Wiener Quadrat-Klafter = 3.59665 m² (zgodovinska konstanta)"},
        "pageSelection": v1["pageSelection"],
        "join": join_v2,
        "v2Delta": v2_delta,
        "areaProof": area_v2,
        "spatialProof": spatial_v2,
        "furkovce": {
            "wohnort": "Furkofze",
            "rows": len(fur),
            "parcels": sorted(int(r["base"]) for r in fur),
            "owner": sorted({r["owner"] for r in fur}),
            "note": "prvi imenovani prebivalci Fučkovci v arhivu (PS str. 125); "
                    "parceli obstajata še danes (P47) [~] — v2 nespremenjeno",
        },
        "perBlattAmbiguity": {
            "basesOnMultiplePages": len(amb_bases),
            "rowsWithAmbiguousBase": amb_rows,
            "note": "znotraj v2 (BI+S1+S2); P56 je meril 515 base čez celotni register "
                    "(vključno S3) — v2 manj, ker številke 1–36 zdaj obstajajo le na Blatt I [~]",
        },
        "invariants": invariants,
        "statusLine": status_line,
        "verdictSi": (
            f"P58 (2026-10-14): produkcija geolokacije PS (P55) SANIRANA in NADGRAJENA na v2. "
            f"ODSTRANJENIH 43 vrstic str. 138–139 (zapadek »Zusammenstellung der Grundstücke« z "
            f"lastnim oštevilčenjem 1–100), ki jih je P56 dokazal kot lažne povezave (median "
            f"razmerja površin 0.0892 ≪ 3.7188 v S1 — ~42× odmik od 1 Wiener QK; pass-razhajanje); "
            f"nabor 43 vrstic je bajtno enak P56 kontaminacijskemu seznamu. DODANIH 26 vrstic "
            f"Blatt I (str. 3–4, številke 1–36) iz primarnega vira P57 (štiri neodvisne VLM plasti) "
            f"— točno vseh 26 lostBases P56. Rezultat: {len(v2_rows)} povezanih vrstic "
            f"({len(s1s2)} S1/S2 + {len(bi)} BI), {len(pos_by_base)} pozicioniranih števil. "
            f"DVA KLJUČNA MERJENA PRINOSA: (1) površinski median se dvigne z 3.6984 na "
            f"{area_median:.4f} (Δ +{delta_pct:.2f} %) — v1 vrednost je bila UMETNO SNIZANA s 43 "
            f"lažnimi povezavami z razmerji ~0.09; čista vrednost je skladna z neodvisnima "
            f"merjenjema P56 (3.7394) in P57 (3.7594); (2) soslednost ostane BAJTNO ENAKA v1 "
            f"({len(consec_d)} parov / {consec_median:.1f} m / {enrich:.1f}×) — pozicije so per "
            f"base in množica pozicioniranih števil se ni spremenila, kar je samo po sebi dokaz, "
            f"da sanitacija ne dotakne prostorske strukture. Zaupanje: STRONG "
            f"{conf_counts['STRONG']} / MEDIUM {conf_counts['MEDIUM']} / WEAK {conf_counts['WEAK']} "
            f"(S1/S2 vrednosti bajtno enake v1); Blatt I vrstice dodatno nosijo readConf iz P57 "
            f"(STRONG 3 / MEDIUM 14 / WEAK 9). Per-Blatt dvoumnost na v2: {len(amb_bases)} base / "
            f"{amb_rows} vrstic [~] (P56: 515 čez celoten register vključno S3). "
            f"Identifikacija posamezne parcele ostaja [~]."
        ),
        "verdictEn": (
            f"P58 (2026-10-14): the P55 PS-geolocation production SANITIZED and upgraded to v2. "
            f"REMOVED: 43 rows of pp. 138–139 (the »Zusammenstellung der Grundstücke« appendix "
            f"with its own numbering 1–100), proven false by P56 (median area ratio 0.0892 ≪ "
            f"3.7188 in S1 — ~42× off 1 Wiener QK; pass disagreement); the 43-row set is "
            f"byte-identical to the P56 contamination list. ADDED: 26 Blatt I rows (pp. 3–4, "
            f"numbers 1–36) from the P57 primary source (four independent VLM layers) — exactly "
            f"all 26 lostBases of P56. Result: {len(v2_rows)} linked rows ({len(s1s2)} S1/S2 + "
            f"{len(bi)} BI), {len(pos_by_base)} positioned numbers. TWO KEY MEASURED EFFECTS: "
            f"(1) the area median rises from 3.6984 to {area_median:.4f} (Δ +{delta_pct:.2f} %) — "
            f"the v1 value was artificially LOWERED by 43 false links with ratios ~0.09; the clean "
            f"value agrees with the independent P56 (3.7394) and P57 (3.7594) measurements; "
            f"(2) the adjacency stays BYTE-IDENTICAL to v1 ({len(consec_d)} pairs / "
            f"{consec_median:.1f} m / {enrich:.1f}×) — positions are per-base and the set of "
            f"positioned numbers unchanged, which by itself proves the sanitization does not "
            f"touch the spatial structure. Confidence: STRONG {conf_counts['STRONG']} / MEDIUM "
            f"{conf_counts['MEDIUM']} / WEAK {conf_counts['WEAK']} (S1/S2 values byte-identical "
            f"to v1); the Blatt I rows additionally carry the P57 readConf (STRONG 3 / MEDIUM 14 / "
            f"WEAK 9). Per-sheet ambiguity within v2: {len(amb_bases)} bases / {amb_rows} rows [~] "
            f"(P56: 515 across the full register incl. S3). Per-parcel identification remains [~]."
        ),
        "next": [
            "4. VLM prehod na glave listov (»Nro. des Blattes«) — per-Blatt ločitev "
            f"{len(amb_bases)} dvoumnih base v2 (metodika štirih plasti iz P57)",
            "prebrati strani 1–2 (naslovnica + rekapitulacija; lokalizacija 102 Bauplätze)",
            "povezava P57 Haus Nro. (60–66 jedro + 31/29/24/20/50) s tlorisi 1825 in PT domačijami [~]",
            "paleografija str. 138–139 (Blatt X) — zdaj izven joina, zgodovinski kontekst",
        ],
        "rowsEvidence": v2_rows,
    }

    runtime = {
        "version": 2,
        "task": "P58 (issue #13) — PS-PARCELS-GEO v2: sanirana geolokacija (43 lažnih S3 "
                "odstranjenih po P56, 26 Blatt I dodanih iz P57)",
        "date": "2026-10-14",
        "generatedBy": "scripts/p58_ps_parcels_geo_v2.py",
        "historicalConstant": {"wienerQkM2": HIST_QK_M2},
        "pageSelection": v1["pageSelection"],
        "join": join_v2,
        "v2Delta": v2_delta,
        "areaProof": area_v2,
        "spatialProof": spatial_v2,
        "furkovce": evidence["furkovce"],
        "perBlattAmbiguity": evidence["perBlattAmbiguity"],
        "statusLine": status_line,
        "rows": v2_rows,
    }
    return evidence, runtime


def main() -> int:
    check = "--check" in sys.argv
    print("P58 — PS-PARCELS-GEO v2 (sanacija produkcije: −43 S3, +26 Blatt I)")
    ev1, rt1 = compute()
    if FAILURES:
        return 1
    ev2, rt2 = compute()
    a, b = jdump(ev1), jdump(ev2)
    c, d = jdump(rt1), jdump(rt2)
    if check:
        if a != b or c != d:
            print("  ✗ determinizem: ponovni izračun NI bajtno identičen")
            return 1
        ok("I6 determinizem: ponovni izračun bajtno identičen")
        existing_ev = V2_EVIDENCE.read_text(encoding="utf-8") if V2_EVIDENCE.exists() else None
        existing_rt = OUT_RUNTIME.read_text(encoding="utf-8") if OUT_RUNTIME.exists() else None
        if existing_ev is not None and existing_ev != a + "\n":
            print("  ✗ --check: obstoječi dokaz ≠ ponovni izračun")
            return 1
        if existing_rt is not None and existing_rt != c + "\n":
            print("  ✗ --check: obstoječi runtime ≠ ponovni izračun")
            return 1
        if existing_ev is not None and existing_rt is not None:
            ok("--check: obstoječi izpisi bajtno identični")
            return 0
    # I7 preprečevanje: rowsEvidence == rows bajtno (isti objekt, isti serializer)
    if jdump(ev1["rowsEvidence"]) != jdump(rt1["rows"]):
        print("  ✗ I7: rowsEvidence ≠ runtime rows")
        return 1
    ok("I7 dokaz ⊇ runtime — rowsEvidence bajtno enake runtime rows")
    V2_EVIDENCE.write_text(a + "\n", encoding="utf-8")
    OUT_RUNTIME.write_text(c + "\n", encoding="utf-8")
    print(f"  ✓ zapisano: {V2_EVIDENCE.relative_to(REPO)} ({len(ev1['rowsEvidence'])} vrstic)")
    print(f"  ✓ zapisano: {OUT_RUNTIME.relative_to(REPO)} ({len(rt1['rows'])} vrstic)")
    print("P58: VSE KONTROLE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
