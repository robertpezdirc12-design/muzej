#!/usr/bin/env python3
"""P70 (issue #13) — PS-PARCELS-GEO v4: IZVEDBA P69 SPECIFIKACIJE
(77 renum preslikav + 95 rejoin po P55 metodi).

P69 (ps-pass1-layers.json) je očesno forenzično klasificiral 166 v3 vrstic cone
p73–93/p99: 33 pravilnih / 77 napačnih ključev (sistematski Kurrent artefakti
starega P38 sloja: 4→1, 5→8, 5→6, fantom-1 ±1000, +9 zamik) / 56 sekijskih
(LASTNIŠKA odločitev čaka). Ta skripta IZVEDE specifikacijo:

  1) RENUM 77 preslikav (bajtno == P69 renumSpec.mappings; p74 2× +300,
     p79 17× −300, p80 8× −100, p81 2× −100, p89 9× −1000, p90 15× −1000,
     p92 9× −9, p99 15× +1000) + re-join po P55 metodi (group_pos).
  2) REJOIN 95 novih vrstic iz ps-raw starih P38 branj — kandidati =
     P69 rejoinSpec.candidates (98; že filtrirani na cardPolys − preslikani
     to); sloj po strani (tabela SLOJI, dokumentirana po P69 perPage
     »artifact« + P38 izbira + pass1-je-pravilen opombah); ključ =
     candidate − offset; 3 kandidati p80 (1541–1543) brez vira (p1 odrez
     blok 62–81, identiteta [~]).
  3) Kolizije isti-Blatt: 32 pričakovanih fuzij — register vsebuje 921–1000
     v dveh blokih (p49–52 »glavni tek« + p89–92 »stolpec«; P69) — vse
     p89/p90/p92 preslikane + nove base instancess kolidirajo s p49/p50/p52;
     fuzije dokumentirane, SPLIT join odločitev = LASTNIKA.
  4) 56 sekijskih vrstic (p83–86, p88) NESPREMENJENIH — lastniška odločitev
     (exclude ali per-Blatt) čaka.
  5) Meritve v4: areaProof + spatialProof po P55 metodi (isti seed-i),
     join/furkovce bloki, perBlattAmbiguity, ambiguous/conf prekalkulacija.

Viri (vsi committed):
  research/issue17/ps-parcels-geo-v3.json      (v3 dokaz, 1079 rowsEvidence)
  src/data/atlas/ps-parcels-geo.json           (v3 runtime)
  research/issue17/ps-pass1-layers.json        (P69 spec: renum + rejoin)
  research/issue17/ps-blatt-headers.json       (P59 pageAttribution — Blatti)
  research/issue17/ps-raw/ps-0NN{,-pass2}.json (P38 branja — vir novih)
  research/georef-n83/gurs/parcels-ko1544-merged.json (2117 parcel, P47)

Izpis:
  research/issue17/ps-parcels-geo-v4.json      (dokaz v4)
  src/data/atlas/ps-parcels-geo.json           (runtime v4 — nadomesti v3;
                                                v3 ostane arhiviran v dokazu)

Invarianti (FAIL → exit 1):
  I1  RENUM 77 bajtno == P69 renumSpec.mappings; preslikani ključi ∈ v3
      točno 77; kolizije isti-Blatt == 32 pričakovanih fuzij
  I2  pini: v3 dokaz sha256, P69 dokaz sha256, P59 dokaz sha256,
      PARCELS sha256; v3 runtime rows == v3 dokaz rowsEvidence bajtno
  I3  rejoin kandidati == P69 rejoinSpec (bajtno, po strani); 95 dodanih;
      3 brez vira [~] (p80)
  I4  NOVI vrstice: P55 normalizacija (areaQK = j·1600+k, wohnort
      propagate), kolizije pokrite s 33 fuzijami, ostale 0
  I5  meritve v4 (rows/bases/multi/cross/ambRows/conf/series) — pini
  I6  nespremenjene vrstice: vsi ključi razen preslikanih (base + group
      derived) in prekalkuliranih (ambiguous/conf) bajtno == v3
  I7  sekcije 56 (p83–86, p88) nespremenjene
  I8  dokaz ⊇ runtime bajtno
  I9  determinizem: drugi preizračun bajtno identičen (--check)

Strojna forenzika ni dokazni vir; v4 je mehanski izvod P69 specifikacije
(odločitvi o 56 sekijskih in SPLIT joinu ostajata LASTNIKA).
"""
import hashlib
import json
import math
import random
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
V3_EV = REPO / "research/issue17/ps-parcels-geo-v3.json"
V3_RT = REPO / "src/data/atlas/ps-parcels-geo.json"
V4_EV = REPO / "research/issue17/ps-parcels-geo-v4.json"
OUT_RUNTIME = REPO / "src/data/atlas/ps-parcels-geo.json"
P69_EV = REPO / "research/issue17/ps-pass1-layers.json"
P59_EV = REPO / "research/issue17/ps-blatt-headers.json"
PARCELS = REPO / "research/georef-n83/gurs/parcels-ko1544-merged.json"
RAW_DIR = REPO / "research/issue17/ps-raw"

HIST_QK_M2 = 3.59665
AREA_BAND = 0.10
NEIGH_M = 150.0
SEED_AREA = 42
SEED_SPATIAL = 7
M_PER_DEG_LAT = 111320.0
TOTAL_PS_ROWS = 2762  # P55/P38 izbira (pageSelection.rows)

PIN_V3_EV_SHA = "af7479e428182f381d3a2537896493d7cf86210fac7027221e22ac2aea218b53"
PIN_P69_EV_SHA = "99962e24dc129a253e7100cb297aa6b73989f96b1d5ff7c95d55d8735c52829e"  # p69 zamrznjen na v3 dokaz (P70)
PIN_P59_EV_SHA = "650f13dccab1da70a60d04c41ce9f7887ca94eafea8a0a7927c104ca899b76f3"  # P68 v3 re-run
PIN_PARCELS_SHA = "fee91fca736348f40ef11d38b7a5b51d51656a9768cda648f4d737029bb3941f"

# pričakovane meritve v4 (pini; vpisano po prvem zagonu)
EXP = {
    "rows": 1145, "bases": 878, "multi": 215, "cross": 79,
    "ambRows": 475, "conf": {"STRONG": 188, "MEDIUM": 797, "WEAK": 160},
    "series": {"S1": 1049, "S2": 70, "BI": 26}, "removed": 29,
    "area": {"pairsWithArea": 1124, "medianRatio": 3.8843, "q25": 2.5402,
             "q75": 7.942, "tightN": 201, "tightShare": 0.1788,
             "shuffleMedian": 4.2701, "shuffleTightShare": 0.0552,
             "historicalQkM2": 3.59665, "deltaPct": 8.0},
    "spatial": {"consecPairs": 654, "medianM": 52.0, "q25M": 33.0,
                "q75M": 87.7, "share150": 0.9052, "shuffleMedianM": 1434.0,
                "shuffleShare150": 0.0182, "enrichmentX": 27.6},
    "suffix": 270, "pos": 878,
    "added": 95, "ambDerived": 93, "confDerived": 15,
}

# ——— sloji ps-raw branj za REJOIN (P69 perPage artefakti + P38 izbira +
#      pass1-je-pravilen opombe; offset na pravi base prostor) ———
SLOJI: dict[int, tuple[str, int]] = {
    73: ("pass2", 0),      # P38 izbira; 0 kandidatov (v3 1118–1120 pravilne)
    74: ("pass1", 300),    # »pass1 edini« (P69); 1121–1140 → 1421–1440
    75: ("pass2", 0),      # P38 izbira; 0 kandidatov (stari passi pravilna)
    76: ("pass2", 300),    # P38 izbira; 1161–1180 → 1461–1480 (4→1)
    77: ("pass2", 0),      # »pass2 pravilen« (P69); 1481–1500 direktno
    78: ("pass2", -100),   # P38 izbira; 160x → 150x (P67 5→6)
    79: ("pass2", -300),   # P38 izbira; 182x → 152x (5→8)
    80: ("pass2", -100),   # P38 izbira == v3 sloj; 164x → 154x (5→6)
    81: ("pass2", -100),   # P38 izbira; 166x → 156x (5→6)
    82: ("pass1", 0),      # »pass1 PRAVILEN (1581+); join je vzel p2« (P69)
    87: ("pass3", 0),      # P38 izbira (pass3 → pass1 datoteka); 0 kandidatov
    89: ("pass1", 0),      # »pass1 PRAVILEN (921+); join je vzel p2« (P69)
    90: ("pass1", 0),      # »pass1 PRAVILEN« (P69)
    91: ("pass1", 0),      # samo pass1; 0 kandidatov (stari passi pravilna)
    92: ("pass2", -9),     # P38 izbira; 990–1008 → 981–999 (+9 zamik)
    93: ("pass2", 300),    # P38 izbira; 160x → 190x (P67 9→6/9→0)
    99: ("pass2", 1000),   # P38 izbira; 92x → 192x (−1000 izgubljena 1)
}
# pričakovane fuzije isti-Blatt (dva bloka registra 921–1000: p49–52 + p89–92;
# SPLIT = LASTNIKA) — (page_nov, base, page_obstojeca)
FUZIJE_EXP = sorted([
    (89, "922", 49), (89, "923", 49), (89, "924", 49), (89, "925", 49),
    (89, "926", 49), (89, "927", 49), (89, "928", 49), (89, "929", 49),
    (89, "930", 49), (89, "931", 49), (89, "934", 49), (89, "936", 49),
    (89, "937", 49), (89, "938", 49), (89, "939", 49),
    (90, "942", 50), (90, "945", 50), (90, "946", 50), (90, "947", 50),
    (90, "949", 50), (90, "951", 50), (90, "952", 50), (90, "955", 50),
    (90, "959", 50), (90, "960", 50),
    (92, "982", 52), (92, "983", 52), (92, "984", 52), (92, "985", 52),
    (92, "986", 52), (92, "987", 52), (92, "988", 52), (92, "989", 52),
])
# pričakovano brez vira (p80 p1 odrez blok 62–81; identiteta [~])
BREZ_VIRA_EXP = sorted([(80, "1541"), (80, "1542"), (80, "1543")])

DATE = "2026-10-15"
FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  ✗ {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def jdump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fnum(v) -> float:
    try:
        return float(str(v).replace(",", ".")) if v not in (None, "") else 0.0
    except (TypeError, ValueError):
        return 0.0


def base_of(s) -> str | None:
    m = re.match(r"\*?(\d+)", str(s or ""))
    return m.group(1) if m else None


def dm(a, b) -> float:
    return math.hypot((a[0] - b[0]) * M_PER_DEG_LAT,
                      (a[1] - b[1]) * M_PER_DEG_LAT * 0.7)


def compute():
    print("P70 — v4 izvedba P69 specifikacije (77 renum + 95 rejoin)")

    # ——— vhodi ———
    v3ev = json.loads(V3_EV.read_text(encoding="utf-8"))
    v3rt = json.loads(V3_RT.read_text(encoding="utf-8"))
    p69 = json.loads(P69_EV.read_text(encoding="utf-8"))
    p59 = json.loads(P59_EV.read_text(encoding="utf-8"))
    parcels = json.loads(PARCELS.read_text(encoding="utf-8"))

    bybase: dict[str, list[dict]] = defaultdict(list)
    for x in parcels:
        b = base_of(x.get("st"))
        if b:
            bybase[b].append(x)

    def group_pos(b: str):
        grp = bybase.get(b)
        if not grp:
            return None
        tot = sum(fnum(x.get("povrsina")) for x in grp)
        if tot > 0:
            lat = sum(x["lat"] * fnum(x.get("povrsina")) for x in grp) / tot
            lng = sum(x["lng"] * fnum(x.get("povrsina")) for x in grp) / tot
        else:
            lat = sum(x["lat"] for x in grp) / len(grp)
            lng = sum(x["lng"] for x in grp) / len(grp)
        return round(lat, 7), round(lng, 7), round(tot, 0) or None, len(grp)

    page_attr = p59["pageAttribution"]

    def blatt_of(page: int):
        return page_attr.get(str(page), {}).get("blatt")

    # ——— I2: pini ———
    if PIN_V3_EV_SHA is None or PIN_P69_EV_SHA is None:
        ok(f"I2 pini v3/P69 še ne vpisani — dejanski sha: "
           f"v3 {sha256(V3_EV)[:8]}…, P69 {sha256(P69_EV)[:8]}…")
    else:
        if sha256(V3_EV) != PIN_V3_EV_SHA:
            fail(f"I2 v3 dokaz sha {sha256(V3_EV)[:8]}… ≠ {PIN_V3_EV_SHA[:8]}…")
        else:
            ok("I2 v3 dokaz sha pin")
        if sha256(P69_EV) != PIN_P69_EV_SHA:
            fail(f"I2 P69 dokaz sha {sha256(P69_EV)[:8]}… ≠ "
                 f"{PIN_P69_EV_SHA[:8]}…")
        else:
            ok("I2 P69 dokaz sha pin")
    if sha256(P59_EV) != PIN_P59_EV_SHA:
        fail("I2 P59 dokaz sha odmika")
    else:
        ok("I2 P59 dokaz sha pin")
    if sha256(PARCELS) != PIN_PARCELS_SHA:
        fail("I2 PARCELS sha odmika")
    else:
        ok("I2 PARCELS sha pin")
    v3_rows = v3ev["rowsEvidence"]
    if v3rt.get("version") == 3:
        if json.dumps(v3rt["rows"], ensure_ascii=False, sort_keys=True) != \
                json.dumps(v3_rows, ensure_ascii=False, sort_keys=True):
            fail(f"I2 v3 runtime rows ≠ dokaz rowsEvidence "
                 f"({len(v3rt['rows'])} vs {len(v3_rows)})")
        else:
            ok(f"I2 v3 runtime == dokaz rowsEvidence ({len(v3_rows)})")
    else:
        ok(f"I2 runtime je v{v3rt.get('version')} (P70 izvedena) — vhod iz "
           f"v3 dokaza rowsEvidence ({len(v3_rows)})")

    # ——— I1: RENUM == P69 renumSpec, kolizije == 33 fuzij ———
    renum_spec = p69["renumSpec"]["mappings"]
    if len(renum_spec) != 77:
        fail(f"I1 RENUM {len(renum_spec)} ≠ 77")
    renum = {(r["page"], r["from"]): r["to"] for r in renum_spec}
    if len(renum) != 77:
        fail(f"I1 RENUM unikatov {len(renum)} ≠ 77")
    v3_keys = {(r["page"], r["base"]) for r in v3_rows}
    missing = [k for k in renum if k not in v3_keys]
    if missing:
        fail(f"I1 preslikanih ključev ni v v3: {missing[:6]}")
    else:
        ok("I1 RENUM 77 preslikav == P69 renumSpec (bajtno); ključi ∈ v3")
    # kolizije isti-Blatt (preslikani to proti v3 instancam drugih strani)
    pages_v3: dict[str, set[int]] = defaultdict(set)
    for r in v3_rows:
        pages_v3[r["base"]].add(r["page"])
    coll_set: set[tuple[int, str, int]] = set()
    for m in renum_spec:
        others = pages_v3.get(m["to"], set()) - {m["page"]}
        bpg = blatt_of(m["page"])
        for pg in sorted(others):
            if blatt_of(pg) == bpg:
                coll_set.add((m["page"], m["to"], pg))

    # ——— preslikava v3 vrstic ———
    out_rows: list[dict] = []
    removed: list[dict] = []
    renumbered_idx: set[int] = set()
    pres_to_by_page: dict[int, set[str]] = defaultdict(set)
    for idx, r in enumerate(v3_rows):
        r2 = dict(r)
        r2["_srcIdx"] = idx
        key = (r2["page"], r2["base"])
        if key in renum:
            nb = renum[key]
            renumbered_idx.add(idx)
            pres_to_by_page[r2["page"]].add(nb)
            gp = group_pos(nb)
            if gp is None:
                removed.append({"page": r2["page"], "oldBase": r2["base"],
                                "newBase": nb, "owner": r2["owner"],
                                "areaQK": r2["areaQK"]})
                continue
            r2["base"] = nb
            r2["lat"], r2["lng"], r2["areaModern"], r2["parts"] = gp
            r2["ratio"] = (round(r2["areaModern"] / r2["areaQK"], 4)
                           if r2["areaModern"] and r2["areaQK"] else None)
        out_rows.append(r2)
    n_renum_rows = len(renumbered_idx)
    if n_renum_rows != 77:
        fail(f"I3 preslikanih vrstic {n_renum_rows} ≠ 77")
    else:
        ok("I3 preslikanih vrstic 77 (p74 2 / p79 17 / p80 8 / p81 2 / "
           "p89 9 / p90 15 / p92 9 / p99 15)")

    # ——— I3: rejoin kandidati == P69 rejoinSpec; NOVI iz ps-raw slojev ———
    rejoin_spec = p69["rejoinSpec"]
    if set(rejoin_spec) != {str(k) for k in SLOJI}:
        fail(f"I3 rejoinSpec strani {sorted(rejoin_spec)} ≠ "
             f"SLOJI {sorted(SLOJI)}")
    n_cands = 0
    brez_vira: list[dict] = []
    added: list[dict] = []
    dup_notes: list[str] = []
    for pg, (sloj, offset) in sorted(SLOJI.items()):
        spec = rejoin_spec[str(pg)]
        cands = [str(c) for c in spec["candidates"]]
        n_cands += len(cands)
        if len(cands) != spec["n"]:
            fail(f"I3 p{pg} kandidatov {len(cands)} ≠ spec n {spec['n']}")
        pres = pres_to_by_page.get(pg, set())
        novi = [c for c in cands if c not in pres]
        fn = RAW_DIR / (f"ps-{pg:03d}-pass2.json" if sloj == "pass2"
                        else f"ps-{pg:03d}.json")  # pass1/pass3 → pass1 datoteka
        d = json.loads(fn.read_text(encoding="utf-8"))
        vr = (d.get("parsed") or {}).get("vrstice") or []
        wohnort_rows: list[dict] = []
        cur = None
        for v0 in vr:
            v = dict(v0)
            w = (v.get("wohnort") or "").strip()
            if w and w not in ('"', "''", "'"):
                cur = w
                v["_wInh"] = False
            else:
                v["_wInh"] = cur is not None
            v["_wohnort"] = cur
            wohnort_rows.append(v)
        for c in novi:
            want = str(int(c) - offset)
            hits = [v for v in wohnort_rows
                    if base_of(v.get("parzella")) == want]
            if not hits:
                brez_vira.append({"page": pg, "base": c,
                                  "reason": "sloj ne podaja vrstice"})
                continue
            if len(hits) > 1:
                dup_notes.append(f"p{pg} {c}: {len(hits)} duplikatov "
                                 f"(vzeta prva)")
            v = hits[0]
            gp = group_pos(c)
            if gp is None:
                brez_vira.append({"page": pg, "base": c,
                                  "reason": "base brez PF poligona"})
                continue
            j = fnum(v.get("joch"))
            k = fnum(v.get("klafter"))
            a_qk = j * 1600.0 + k
            rec = {
                "page": pg,
                "parzella": str(v.get("parzella") or ""),
                "base": c,
                "owner": (v.get("name") or "").strip() or None,
                "stand": (v.get("stand") or "").strip() or None,
                "hausNr": (v.get("hausNr") or "").strip() or None,
                "wohnort": v["_wohnort"],
                "wohnortInherited": v["_wInh"],
                "kultur": (v.get("kultur") or "").strip() or None,
                "joch": j or None,
                "klafter": k or None,
                "areaQK": round(a_qk, 1) if a_qk > 0 else None,
                "areaSuspect": k >= 1600.0,
                "parts": gp[3],
                "lat": gp[0],
                "lng": gp[1],
                "areaModern": gp[2],
                "ratio": (round(gp[2] / a_qk, 4)
                          if gp[2] and a_qk > 0 else None),
                "conf": None,
                "series": "S1",
                "ambiguous": False,
            }
            if v.get("anmerkung"):
                rec["anmerkung"] = v["anmerkung"]
            added.append(rec)
    if n_cands != 98:
        fail(f"I3 kandidatov skupaj {n_cands} ≠ 98")
    else:
        ok("I3 rejoin kandidati == P69 rejoinSpec (98, po strani bajtno)")
    if len(added) != EXP["added"]:
        fail(f"I3 dodanih vrstic {len(added)} ≠ {EXP['added']}")
    else:
        ok(f"I3 dodanih vrstic {len(added)} iz ps-raw slojev "
           f"(P55 normalizacija)")
    got_bv = sorted([(b["page"], b["base"]) for b in brez_vira])
    if got_bv != BREZ_VIRA_EXP:
        fail(f"I3 brez vira {got_bv} ≠ {BREZ_VIRA_EXP}")
    else:
        ok("I3 brez vira: natanko 3 (p80 1541–1543 — p1 odrez blok 62–81, "
           "identiteta [~])")
    for note in dup_notes:
        ok(f"I3 {note}")

    # ——— kolizije NOVIh ———
    for rec in added:
        others = pages_v3.get(rec["base"], set()) - {rec["page"]}
        bpg = blatt_of(rec["page"])
        for pg in sorted(others):
            if blatt_of(pg) == bpg:
                coll_set.add((rec["page"], rec["base"], pg))
    got_fuz = sorted(coll_set)
    if got_fuz != FUZIJE_EXP:
        fail(f"I1/I4 kolizije isti-Blatt {got_fuz} ≠ pričakovane "
             f"{FUZIJE_EXP}")
    else:
        ok("I1/I4 kolizije isti-Blatt == 32 pričakovanih fuzij "
           "(dva bloka registra 921–1000: p49–52 + p89–92; SPLIT = "
           "LASTNIKA)")

    # ——— dodaj nove (na koncu, sortirane po (page, base) — dokumentirano) ———
    added.sort(key=lambda r: (r["page"], int(r["base"])))
    out_rows.extend(added)

    # ——— ambiguous prekalkulacija ———
    pages_by: dict[str, set[int]] = defaultdict(set)
    for r in out_rows:
        pages_by[r["base"]].add(r["page"])
    amb_changes: list[tuple] = []
    for r in out_rows:
        new_amb = len(pages_by[r["base"]]) > 1
        if new_amb != r["ambiguous"]:
            amb_changes.append((r["page"], r["base"], r["ambiguous"], new_amb))
            r["ambiguous"] = new_amb

    # ——— conf prekalkulacija (P55 metoda) ———
    pos_by_base = {}
    for b in pages_by:
        gp = group_pos(b)
        if gp:
            pos_by_base[b] = (gp[0], gp[1])
    neigh_ok: set[str] = set()
    for b, p in pos_by_base.items():
        n = int(b)
        for m in (n - 1, n + 1):
            q2 = pos_by_base.get(str(m))
            if q2 and dm(p, q2) <= NEIGH_M:
                neigh_ok.add(b)
                break
    conf_changes: list[tuple] = []
    for r in out_rows:
        if r["series"] == "BI":
            continue
        if r["lat"] is None:
            new = None
        else:
            area_tight = (r["ratio"] is not None and not r["areaSuspect"]
                          and abs(r["ratio"] / HIST_QK_M2 - 1) <= AREA_BAND)
            nb = r["base"] in neigh_ok
            new = ("STRONG" if (area_tight and nb)
                   else "MEDIUM" if (area_tight or nb) else "WEAK")
        if new != r["conf"]:
            conf_changes.append((r["page"], r["base"], r["conf"], new))
            r["conf"] = new
    conf_changes = [c for c in conf_changes if c[2] is not None]

    # ——— I6: nespremenjene vrstice bajtno == v3 (razen preslikanih in
    #      prekalkuliranih) — po _srcIdx ———
    n_unchanged = 0
    n_derived = 0
    for r in out_rows:
        idx = r.pop("_srcIdx", None)
        if idx is None:
            continue  # nova (rejoin) vrstica
        if idx in renumbered_idx:
            continue  # preslikana vrstica (base + group derived)
        v3r = v3_rows[idx]
        if r["ambiguous"] != v3r["ambiguous"] or r["conf"] != v3r["conf"]:
            n_derived += 1
            continue
        if json.dumps(r, ensure_ascii=False, sort_keys=True) != \
                json.dumps(v3r, ensure_ascii=False, sort_keys=True):
            fail(f"I6 vrstica p{r['page']} {r['base']} nespremenjena, "
                 f"a odmika")
        n_unchanged += 1
    ok(f"I6 nespremenjene vrstice bajtno == v3 ({n_unchanged}); "
       f"group-derived (ambiguous/conf) {n_derived}; preslikane "
       f"{n_renum_rows}; nove {len(added)}")

    # ——— I7: sekcije nespremenjene ———
    sec_pages = p69["sectionClass"]["pages"]
    sec_rows = p69["counts"]["sectionRows"]
    n_sec = sum(1 for r in out_rows if r["page"] in sec_pages)
    if n_sec != sec_rows:
        fail(f"I7 sekcij vrstic {n_sec} ≠ {sec_rows}")
    else:
        ok(f"I7 sekcije {sec_pages}: {n_sec} vrstic nespremenjenih "
           f"(lastniška odločitev čaka)")

    # ——— I5: meritve v4 ———
    bases4 = set(pages_by)
    multi = [b for b in pages_by if len(pages_by[b]) > 1]
    bl_by: dict[str, set[str]] = defaultdict(set)
    for r in out_rows:
        bl = blatt_of(r["page"])
        if bl:
            bl_by[r["base"]].add(bl)
    cross = [b for b in bl_by if len(bl_by[b]) > 1]
    s1s2 = [r for r in out_rows if r["series"] != "BI"]
    bi_rows = [r for r in out_rows if r["series"] == "BI"]
    conf_counts: dict[str, int] = defaultdict(int)
    for r in out_rows:
        conf_counts[r["conf"]] += 1
    series_counts = {k: sum(1 for r in out_rows if r["series"] == k)
                     for k in ("S1", "S2", "BI")}
    amb_rows = sum(1 for r in out_rows if r["ambiguous"])
    suffix_groups = sum(1 for b in pos_by_base if len(bybase[b]) > 1)
    area_pairs = [(r["areaQK"], r["areaModern"]) for r in out_rows
                  if r["areaQK"] and r["areaModern"] and not r["areaSuspect"]]
    ratios = [m / a for a, m in area_pairs]
    area_median = statistics.median(ratios)
    tight_n = sum(1 for x in ratios if abs(x / HIST_QK_M2 - 1) <= AREA_BAND)
    mods = [m for _, m in area_pairs]
    rng = random.Random(SEED_AREA)
    rng.shuffle(mods)
    sh_ratios = [m / a for (a, _), m in zip(area_pairs, mods)]
    sh_median = statistics.median(sh_ratios)
    sh_tight = sum(1 for x in sh_ratios
                   if abs(x / HIST_QK_M2 - 1) <= AREA_BAND) / len(sh_ratios)
    area_proof = {
        "pairsWithArea": len(area_pairs),
        "medianRatio": round(area_median, 4),
        "q25": round(sorted(ratios)[len(ratios) // 4], 4),
        "q75": round(sorted(ratios)[3 * len(ratios) // 4], 4),
        "tightN": tight_n,
        "tightShare": round(tight_n / len(ratios), 4),
        "shuffleMedian": round(sh_median, 4),
        "shuffleTightShare": round(sh_tight, 4),
        "historicalQkM2": HIST_QK_M2,
        "deltaPct": round((area_median / HIST_QK_M2 - 1) * 100, 2),
    }
    nums = sorted(int(b) for b in pos_by_base)
    consec = [dm(pos_by_base[str(n)], pos_by_base[str(n + 1)])
              for n in nums if str(n + 1) in pos_by_base]
    consec_s = sorted(consec)
    pl = [pos_by_base[str(n)] for n in nums]
    rng2 = random.Random(SEED_SPATIAL)
    rng2.shuffle(pl)
    sh_d = [dm(pl[i], pl[i + 1]) for i in range(len(pl) - 1)]
    spatial_proof = {
        "consecPairs": len(consec),
        "medianM": round(statistics.median(consec), 1),
        "q25M": round(consec_s[len(consec) // 4], 1),
        "q75M": round(consec_s[3 * len(consec) // 4], 1),
        "share150": round(sum(1 for x in consec if x <= NEIGH_M)
                          / len(consec), 4),
        "shuffleMedianM": round(statistics.median(sh_d), 1),
        "shuffleShare150": round(sum(1 for x in sh_d if x <= NEIGH_M)
                                 / len(sh_d), 4),
        "enrichmentX": round(statistics.median(sh_d)
                             / statistics.median(consec), 1),
    }
    ok(f"I5 meritve v4: rows {len(out_rows)} · bases {len(bases4)} · "
       f"multi {len(multi)} · cross {len(cross)} · ambRows {amb_rows} · "
       f"conf {conf_counts.get('STRONG', 0)}/{conf_counts.get('MEDIUM', 0)}"
       f"/{conf_counts.get('WEAK', 0)} · area median "
       f"{area_proof['medianRatio']} (Δ {area_proof['deltaPct']} %) · "
       f"sosledje {spatial_proof['consecPairs']} parov / "
       f"{spatial_proof['medianM']} m")

    # ——— I5: preverjanja proti pinom ———
    if EXP["rows"] is not None:
        if len(out_rows) != EXP["rows"]:
            fail(f"I5 rows {len(out_rows)} ≠ {EXP['rows']}")
        if len(bases4) != EXP["bases"]:
            fail(f"I5 bases {len(bases4)} ≠ {EXP['bases']}")
        if len(multi) != EXP["multi"]:
            fail(f"I5 multi {len(multi)} ≠ {EXP['multi']}")
        if len(cross) != EXP["cross"]:
            fail(f"I5 cross {len(cross)} ≠ {EXP['cross']}")
        if amb_rows != EXP["ambRows"]:
            fail(f"I5 ambRows {amb_rows} ≠ {EXP['ambRows']}")
        if dict(conf_counts) != EXP["conf"]:
            fail(f"I5 conf {dict(conf_counts)} ≠ {EXP['conf']}")
        if series_counts != EXP["series"]:
            fail(f"I5 series {series_counts} ≠ {EXP['series']}")
        if len(removed) != EXP["removed"]:
            fail(f"I5 removed {len(removed)} ≠ {EXP['removed']}")
        if suffix_groups != EXP["suffix"]:
            fail(f"I5 suffix {suffix_groups} ≠ {EXP['suffix']}")
        if len(pos_by_base) != EXP["pos"]:
            fail(f"I5 pos {len(pos_by_base)} ≠ {EXP['pos']}")
        if area_proof != EXP["area"]:
            fail(f"I5 areaProof meritev {area_proof} ≠ pin")
        if spatial_proof != EXP["spatial"]:
            fail(f"I5 spatialProof meritev {spatial_proof} ≠ pin")
        if len(amb_changes) != EXP["ambDerived"]:
            fail(f"I5 ambiguous sprememb {len(amb_changes)} ≠ "
                 f"{EXP['ambDerived']}")
        if len(conf_changes) != EXP["confDerived"]:
            fail(f"I5 conf sprememb {len(conf_changes)} ≠ "
                 f"{EXP['confDerived']}")
        if not FAILURES:
            ok("I5 meritve == pini (vse)")
    else:
        print("  ── PINE ZA VPIS (EXP) ————————————————————")
        print(f"    rows={len(out_rows)}, bases={len(bases4)}, "
              f"multi={len(multi)}, cross={len(cross)}, "
              f"ambRows={amb_rows}, suffix={suffix_groups}, "
              f"pos={len(pos_by_base)}, removed={len(removed)}, "
              f"added={len(added)}, "
              f"ambDerived={len(amb_changes)}, "
              f"confDerived={len(conf_changes)}")
        print(f"    conf={dict(conf_counts)}, series={series_counts}")
        print(f"    area={area_proof}")
        print(f"    spatial={spatial_proof}")
        from collections import Counter as _C
        print(f"    removedByPage={dict(sorted(_C(x['page'] for x in removed).items()))}")
        print(f"    addedByPage={dict(sorted(_C(x['page'] for x in added).items()))}")

    # blattDist (pari Blattov čez cross-Blatt base)
    blatt_dist: dict[str, int] = defaultdict(int)
    for b in cross:
        pair = "·".join(sorted(bl_by[b]))
        blatt_dist[pair] += 1

    page_sel = v3ev.get("pageSelection")

    v3_join = v3ev["join"]
    join_block = {
        "matchedRows": len(out_rows),
        "matchedRowsS1S2": len(s1s2),
        "matchedRowsBI": len(bi_rows),
        "matchedSharePct": round(100 * len(out_rows) / TOTAL_PS_ROWS, 1),
        "psUniqueNumbers": v3_join["psUniqueNumbers"],
        "psPositionedParcels": len(pos_by_base),
        "suffixGroups": suffix_groups,
        "seriesCounts": series_counts,
        "confCounts": {"STRONG": conf_counts["STRONG"],
                       "MEDIUM": conf_counts["MEDIUM"],
                       "WEAK": conf_counts["WEAK"]},
        "readConfBI": v3_join["readConfBI"],
        "ambiguousBases": len(multi),
        "ambiguousRows": amb_rows,
    }
    per_blatt_amb = {
        "basesOnMultiplePages": len(multi),
        "rowsWithAmbiguousBase": amb_rows,
        "note": f"base na > 1 strani v v4 (P70 renum 77 + rejoin 95 po "
                f"P55 metodi); čez-Blatt {len(cross)} (blattDist " +
                " · ".join(f"{k} {v}" for k, v in sorted(blatt_dist.items()))
                + ") [~]",
    }
    return (out_rows, removed, added, brez_vira, renum_spec, coll_set,
            amb_changes, conf_changes, join_block, per_blatt_amb,
            area_proof, spatial_proof, page_sel,
            v3ev["join"]["psUniqueNumbers"], v3ev["join"]["readConfBI"],
            v3ev["furkovce"], rejoin_spec, multi, cross, bases4)


def build_documents():
    (out_rows, removed, added, brez_vira, renum_spec, coll_set, amb_changes,
     conf_changes, join_block, per_blatt_amb, area_proof, spatial_proof,
     page_sel, ps_unique, read_conf_bi, furkovce, rejoin_spec, multi,
     cross, bases4) = compute()
    page_sel = page_sel or json.loads(
        (REPO / "src/data/atlas/ps-parcels-geo.json").read_text(
            encoding="utf-8"))["pageSelection"]
    if FAILURES:
        print(f"P70: {len(FAILURES)} invariant(ov) PADLO")
        for f in FAILURES:
            print(f"  → {f}")
        return 1

    status_line = (
        f"P70 IZVEDBA P69 SPECIFIKACIJE: 77 renum preslikav (bajtno po "
        f"P69; p74 +300, p79 −300, p80/p81 −100, p89/p90 ±1000, p92 −9, "
        f"p99 +1000) + 95 rejoin vrstic iz ps-raw slojev po P55 metodi "
        f"(p74 14 · p76 18 · p77 2 · p78 10 · p79 2 · p80 3 · p81 3 · "
        f"p82 16 · p89 9 · p90 2 · p92 1 · p93 12 · p99 3); 3 kandidati "
        f"p80 (1541–1543) brez vira (p1 odrez blok 62–81, identiteta [~]); "
        f"33 fuzij isti-Blatt (dva bloka registra 921–1000: p49–52 + "
        f"p89–92; SPLIT = LASTNIKA); izpadlih preslikanih brez poligona "
        f"{len(removed)}; v4: {len(out_rows)} vrstic / "
        f"{join_block['psPositionedParcels']} base / multi-page "
        f"{per_blatt_amb['basesOnMultiplePages']} / cross-Blatt "
        f"{len(cross)}; area median {area_proof['medianRatio']} "
        f"(Δ {area_proof['deltaPct']} %), sosledje "
        f"{spatial_proof['consecPairs']} parov / {spatial_proof['medianM']} m "
        f"({spatial_proof['enrichmentX']}×); 56 sekijskih vrstic (p83–86, "
        f"p88) nespremenjenih — lastniška odločitev čaka"
    )

    evidence = {
        "version": 4,
        "task": "P70 (issue #13) — PS-PARCELS-GEO v4: izvedba P69 "
                "specifikacije (77 renum preslikav + 95 rejoin po P55 "
                "metodi)",
        "date": DATE,
        "generatedBy": "scripts/p70_ps_v4_rejoin.py",
        "principle": "P69 očesna forenzika je klasificirala 166 v3 vrstic "
                     "cone p73–93/p99 (33 pravilnih / 77 napačnih / 56 "
                     "sekijskih) in specifikirala 77 preslikav + 98 rejoin "
                     "kandidatov. v4 je mehanski izvod te specifikacije: "
                     "preslikave base + re-join po P55 metodi (group_pos). "
                     "Registrska branja (ps-raw) ostajajo NESPREMENJENA — "
                     "sanacija je na join ključu (base), parzella ostaja "
                     "originalno branje. Nespremenjene vrstice bajtno == v3 "
                     "(lekcija P9). 56 sekijskih vrstic (p83–86, p88) in "
                     "SPLIT join odločitvi ostajata LASTNIKA.",
        "inputs": {
            "v3Evidence": "research/issue17/ps-parcels-geo-v3.json (sha256 "
                          f"{sha256(V3_EV)[:8]}…; 1079 rowsEvidence)",
            "p69Evidence": "research/issue17/ps-pass1-layers.json "
                           f"(sha256 {sha256(P69_EV)[:8]}…; renumSpec 77 + "
                           f"rejoinSpec 98)",
            "p59Evidence": "research/issue17/ps-blatt-headers.json "
                           f"(sha256 {sha256(P59_EV)[:8]}…; pageAttribution)",
            "parcels": "research/georef-n83/gurs/parcels-ko1544-merged.json "
                       f"(sha256 {sha256(PARCELS)[:8]}…; 2117 parcel P47)",
            "psRaw": "research/issue17/ps-raw/ps-0NN{,-pass2}.json (P38 "
                     "branja — vir 95 rejoin vrstic; sloji po strani: "
                     + ", ".join(f"p{pg} {s} {o:+d}" for pg, (s, o)
                                 in sorted(SLOJI.items())) + ")",
        },
        "historicalConstant": {"wienerQkM2": HIST_QK_M2},
        "join": join_block,
        "furkovce": furkovce,
        "renumberSpec": renum_spec,
        "rejoinSpec": rejoin_spec,
        "rejoinSources": {str(pg): {"sloj": s, "offset": o}
                          for pg, (s, o) in sorted(SLOJI.items())},
        "collisions": {
            "istiBlatt": [
                {"page": p, "base": b, "existingPage": ep}
                for p, b, ep in sorted(coll_set)
            ],
            "reason": "register vsebuje 921–1000 v dveh blokih (p49–52 "
                      "»glavni tek« + p89–92 »stolpec«; P69) — 33 fuzij "
                      "dokumentirane; SPLIT join odločitev = LASTNIKA",
        },
        "removedRows": removed,
        "removedReason": "preslikana base brez PF poligona v k.o. 1544; "
                         "vrstica registra ostaja v ps-raw, izpada le iz "
                         "joina",
        "addedRows": added,
        "noSourceCandidates": brez_vira,
        "groupDerivedChanges": {
            "ambiguous": [f"p{p} {b}: {o}→{n}" for p, b, o, n in amb_changes],
            "conf": [f"p{p} {b}: {o}→{n}" for p, b, o, n in conf_changes],
        },
        "areaProof": area_proof,
        "spatialProof": spatial_proof,
        "perBlattAmbiguity": per_blatt_amb,
        "invariants": {
            "I1": "RENUM 77 == P69 renumSpec bajtno; kolizije == 33 fuzij",
            "I2": "pini v3/P69/P59/PARCELS; runtime == rowsEvidence",
            "I3": "98 kandidatov == P69 rejoinSpec; 95 dodanih; 3 brez vira",
            "I4": "NOVI P55 normalizacija; kolizije NOVI pokrite",
            "I5": "meritve v4 (rows/bases/multi/cross/amb/conf/series)",
            "I6": "nespremenjene vrstice bajtno == v3; group-derived "
                  "dokumentirane",
            "I7": "sekcije 56 (p83–86, p88) nespremenjene",
            "I8": "dokaz ⊇ runtime bajtno",
            "I9": "determinizem --check bajtno",
        },
        "statusLine": status_line,
        "verdictSi": (
            "P70: IZVEDBA P69 SPECIFIKACIJE (issue #13) — mehanski izvod, "
            "deterministično, brez AI ob delovanju. 77 renum preslikav "
            "(bajtno po P69 očesni forenziki) + 95 rejoin vrstic iz starih "
            "P38 slojev (ključi po korekciji, P55 normalizacija, group_pos "
            "poligoni). Konec lažnih fuzij: p74 1121–1140 → 1421–1440 "
            "(4→1 artefakt), p76 1161–1180 → 1461–1480, p79 182x → 152x "
            "(5→8), p80/p81 16xx → 15xx (5→6), p89/p90 19xx → 9xx "
            "(fantom-1 ±1000 — 9 dolgi ascender ≠ vodilna 1), p92 +9 "
            "zamik, p99 92x → 192x (Blatt III). 33 fuzij isti-Blatt (dva "
            "bloka registra 921–1000: p49–52 + p89–92 — P69 "
            "dokumentirano) — SPLIT = LASTNIKA. 56 sekijskih vrstic "
            "(p83–86, p88) nespremenjenih — exclude ali per-Blatt "
            "instance = lastniška odločitev."
        ),
        "verdictEn": (
            "P70: THE P69 SPECIFICATION REALIZED (issue #13) — a mechanical "
            "derivation, deterministic, no AI at runtime. 77 renumber "
            "mappings (byte-equal to P69 ocular forensics) + 95 rejoined "
            "rows from the old P38 layers (keys corrected, P55 "
            "normalization, group_pos polygons). End of false fusions: "
            "p74 1121–1140 → 1421–1440 (4→1 artifact), p76 1161–1180 → "
            "1461–1480, p79 182x → 152x (5→8), p80/p81 16xx → 15xx (5→6), "
            "p89/p90 19xx → 9xx (phantom-1 ±1000 — a long ascender 9 is "
            "not a leading 1), p92 +9 shift, p99 92x → 192x (Blatt III). "
            "6 same-Blatt fusions (the register holds 921–1000 in two "
            "blocks: p49–52 'main run' + p89–92 'column') — SPLIT = "
            "OWNER's call. 56 section rows (p83–86, p88) unchanged — "
            "exclude or per-Blatt instances = owner's decision."
        ),
        "next": [
            "LASTNIŠKI: 56 sekijskih vrstic (p83–86, p88) — exclude iz "
            "joina ali per-Blatt instance (P60 moda B / PF protokol)",
            "LASTNIŠKI: SPLIT joina (6 fuzij isti-Blatt + cross-Blatt)",
            "III/IV cona p94+ — sistemski pregled preostalih slojev "
            "(openQuestions #3 P69)",
            "PF protokol povezava (lastniki pas-instanc)",
            "veriga re-run P60–P61 s posodobljenimi pini (atribucije nad "
            "v4)",
        ],
        "rowsEvidence": out_rows,
    }

    runtime = {
        "version": 4,
        "task": "P70 (issue #13) — PS-PARCELS-GEO v4: izvedba P69 "
                "specifikacije (77 renum + 95 rejoin po P55 metodi)",
        "date": DATE,
        "generatedBy": "scripts/p70_ps_v4_rejoin.py",
        "historicalConstant": {"wienerQkM2": HIST_QK_M2},
        "pageSelection": page_sel,
        "join": {**join_block, "psUniqueNumbers": ps_unique,
                 "readConfBI": read_conf_bi},
        "v4Delta": {
            "reason": "izvedba P69 specifikacije: 77 renum preslikav "
                      "(očesna forenzika Kurrent artefaktov) + 95 rejoin "
                      "vrstic iz ps-raw slojev (P55 metoda)",
            "renumbered": 77,
            "removed": len(removed),
            "added": len(added),
            "noSource": [f"p{b['page']} {b['base']}" for b in brez_vira],
            "fuzijeIstiBlatt": 32,
            "before": {"rows": 1079, "bases": 798, "multiPage": 199,
                       "crossBlatt": 98},
            "after": {"rows": len(out_rows),
                      "bases": len(set(r["base"] for r in out_rows)),
                      "multiPage": per_blatt_amb["basesOnMultiplePages"],
                      "crossBlatt": len(cross)},
            "invariance": "nespremenjene vrstice bajtno == v3 (lekcija P9); "
                          "group-derived polja (ambiguous/conf) "
                          "prekalkulirana po P55 metodi; v3 ostaje "
                          "arhiviran (research/issue17/"
                          "ps-parcels-geo-v3.json)",
            "note": "psUniqueNumbers 2106 = meritev registra (branja "
                    "ps-raw nespremenjena — sanacija le na join ključu)",
        },
        "areaProof": area_proof,
        "spatialProof": spatial_proof,
        "furkovce": furkovce,
        "perBlattAmbiguity": per_blatt_amb,
        "statusLine": status_line,
        "rows": out_rows,
    }

    # ——— I8: dokaz ⊇ runtime ———
    if json.dumps(evidence["rowsEvidence"], ensure_ascii=False) != \
            json.dumps(runtime["rows"], ensure_ascii=False):
        fail("I8 dokaz rowsEvidence ≠ runtime rows")
    else:
        ok(f"I8 dokaz ⊇ runtime ({len(out_rows)} vrstic bajtno)")

    check = "--check" in sys.argv
    if check:
        ev2 = json.dumps(json.loads(V4_EV.read_text(encoding="utf-8")),
                         ensure_ascii=False)
        if json.dumps(evidence, ensure_ascii=False) != ev2:
            print("P70 --check: MISMATCH (dokaz)")
            return 1
        rt_disk = json.loads(OUT_RUNTIME.read_text(encoding="utf-8"))
        if rt_disk.get("version") == 4:
            if json.dumps(runtime, ensure_ascii=False) == \
                    json.dumps(rt_disk, ensure_ascii=False):
                print("P70 --check: determinizem PASS (dokaz + runtime "
                      "bajtno identična)")
                return 0
            print("P70 --check: MISMATCH (runtime v4)")
            return 1
        # runtime je napredoval (P71 v5) — dokaz ostaja zamrznjen arhiv
        # (vsebina v4 runtime živi v dokazu); disk runtime mora deklarirati
        # nasledstvo (version ≥ 5 + v5Delta z dokumentiranimi korekcijami)
        d = rt_disk.get("v5Delta") or {}
        if not (rt_disk.get("version", 0) >= 5
                and d.get("excludedSections") == 56
                and d.get("revertedP93") == 15):
            print("P70 --check: MISMATCH (runtime nasledstvo ni "
                  "deklarirano: version "
                  f"{rt_disk.get('version')}, v5Delta {bool(d)})")
            return 1
        print("P70 --check: determinizem PASS (dokaz bajtno; runtime "
              "nadgrajen na v" + str(rt_disk.get("version")) + " po P71 "
              "(C1 sekcije + C2 p93) — v4 arhiviran v dokazu)")
        return 0

    V4_EV.write_text(jdump(evidence) + "\n", encoding="utf-8")
    print(f"  ✓ zapisano: {V4_EV.relative_to(REPO)} "
          f"({len(evidence['rowsEvidence'])} vrstic)")
    OUT_RUNTIME.write_text(jdump(runtime) + "\n", encoding="utf-8")
    print(f"  ✓ zapisano: {OUT_RUNTIME.relative_to(REPO)} "
          f"({len(runtime['rows'])} vrstic)")
    print(f"P70: v4 izvedba P69 specifikacije — {len(out_rows)} vrstic, "
          f"{join_block['psPositionedParcels']} base, multi-page "
          f"{per_blatt_amb['basesOnMultiplePages']}, cross-Blatt {len(cross)}")
    return 0


if __name__ == "__main__":
    sys.exit(build_documents())
