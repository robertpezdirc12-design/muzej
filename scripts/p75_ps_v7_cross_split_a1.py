#!/usr/bin/env python3
"""P75 (issue #13) — PS-PARCELS-GEO v7: CROSS-BLATT SPLIT (OPCIJA A1)

C4  CROSS-BLATT SPLIT — drop ne-dominant-Blatt vrstic za 48 cross base —
    LASTNIŠKA odločitev (ukaz "nadaljuj" po P74 odločitvenem paketu,
    2026-10-15; opcija A1 = privzeta pot — keep DOMINANT Blatt, najmanj
    invazivna; A2 različen keep pri 29 base; B zahteva georef Blattnih
    kart [~]).
    P74 pack DOKAZAL: 48 base z vrsticami na ≥ 2 RAZLIČNIH sosednjih
    Blattih (I·II 13 · II·III 16 · III·IV 1 · IV·V 18; skoki 0), vsak
    točno 1 vrstica per Blatt (96 vrstic; 48/48) — množice lastnikov med
    Blatti DISJUNKTNE 48/48 (0 prekrivanj) = ista številka pod dvema
    Blattoma = 2 RAZLIČNI realni parceli, ker se numeracija per Blatt
    PONOVI (P56 pageMap prekrivanja razponov 48/48: p11 I 161–183 /
    p61 II 161–180; p64 II 1821–1840 / p94 III 1821–1841; p110 IV
    2141–2160 / p125 V 2141–2160). v6 join teh 48 base FUZIRA dve
    parceli pod eno geometrijo (geoShared 48/48).
    Izvedba (A1): keep vrstica na DOMINANTNEM Blattu (max delež Σ areaQK
    per Blatt; izenačeni deleži → min Blatt; ties 0 v v6) — drop 48
    (page, base) kombinacij = 48 vrstic (drugi Blatt); 0 base ne izgubi
    vseh vrstic; vrstice ostanejo v REGISTRU (dokaz: removedRows),
    izpadajo iz runtime joina (brez geometrije).
    P9: ohranjene vrstice BAJTNO == v6 (drop samo odstranjuje);
    ambiguous prekalkuliran po P55 metodi (derivat strani; 48 group-
    derived True→False); conf se NE spremeni (geografija vrstic
    nespremenjena — kontrola 0 sprememb); v6 ostaja arhiviran
    (research/issue17/ps-parcels-geo-v6.json).

Viri (vsi committed):
  research/issue17/ps-parcels-geo-v6.json         (v6 dokaz, 939 rowsEvidence)
  research/issue17/ps-cross-blatt-pack.json       (P74 dokaz — 48 cross base)
  research/issue17/ps-blatt-headers.json          (P59 pageAttribution — Blatti)
  research/issue17/ps-register-topology.json      (P56 pageMap)
  research/georef-n83/gurs/parcels-ko1544-merged.json (2117 parcel, P47)
  src/data/atlas/ps-parcels-geo.json              (v6 runtime — vhod;
                                                   nasledstvena veja)

Izpis:
  research/issue17/ps-parcels-geo-v7.json         (dokaz v7)
  src/data/atlas/ps-parcels-geo.json              (runtime v7 — nadomesti v6;
                                                   v6 ostane arhiviran v dokazu;
                                                   v5Delta + v6Delta + v7Delta
                                                   = zgodovina)

Invarianti (FAIL → exit 1):
  I1  pini: v6 dokaz sha256, P74 pack sha256, P59 sha256, P56 sha256,
      PARCELS sha256; v6 runtime nasledstvena veja (sha == v6 pin ALI
      version ≥ 7 z v7Delta.droppedPairs == 48 — disk nadgrajen po P75,
      vhodne vrstice iz v6 dokaza rowsEvidence, arhiv bajtno)
  I2  re-izpeljava cross seta iz v6 rowsEvidence × P59 pageAttribution ==
      P74 dokaz "bases" bajtno (base → blattPair/pages/dominantBlatt/
      ownerRelation/keepBlatt/keepPage/sameKeep); 48 base, 96 vrstic,
      1 vrstica per Blatt 48/48; lastniki disjunktni 48/48; dominantBlatt
      re-izračun (max Σ areaQK per Blatt; ties → min) == pack; ties 0;
      blattDist I·II 13 · II·III 16 · III·IV 1 · IV·V 18; sosednji 48,
      skoki 0
  I3  drop izpeljava == P74 optionA1: 48 kombinacij = 48 vrstic,
      rows 939 → 891, bases 879, lost 0, multi 50 → 2, cross 48 → 0,
      ambRows 100 → 4; A2 (keep min Blatt) različen keep pri 29
      (sameKeep 19) == pack.optionA2DifferentKeep; BI drop izmerjen
  I4  ohranjene vrstice brez group-derived sprememb bajtno == v6
      (_srcIdx); 0 base brez vrstic
  I5  ambiguous prekalkulacija po P55 metodi (derivat strani) == pini;
      conf prekalkulacija (P71 metoda) == 0 sprememb (geografija nedeprava)
  I6  meritve v7 (rows/bases/multi/cross/ambRows/conf/series/removed)
      == pini; areaProof + spatialProof == pini (P71 metoda, ista semena)
  I7  dokaz ⊇ runtime bajtno (runtime rows == dokaz rowsEvidence)
  I8  determinizem: drugi preizračun bajtno identičen (--check)

Glifna/dual forenzika ni VLM-instrument: cross set je derivat
determinističnih lastnosti (strani × Blatt × lastniki × areaQK) iz
committed dokazov — brez AI ob delovanju.
"""
import hashlib
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
V6_EV = REPO / "research/issue17/ps-parcels-geo-v6.json"
PACK_EV = REPO / "research/issue17/ps-cross-blatt-pack.json"
P59_EV = REPO / "research/issue17/ps-blatt-headers.json"
P56_EV = REPO / "research/issue17/ps-register-topology.json"
PARCELS = REPO / "research/georef-n83/gurs/parcels-ko1544-merged.json"
V6_RT = REPO / "src/data/atlas/ps-parcels-geo.json"
OUT_EV = REPO / "research/issue17/ps-parcels-geo-v7.json"
OUT_RUNTIME = REPO / "src/data/atlas/ps-parcels-geo.json"

HIST_QK_M2 = 3.59665
AREA_BAND = 0.10
NEIGH_M = 150.0
SEED_AREA = 42
SEED_SPATIAL = 7
M_PER_DEG_LAT = 111320.0
TOTAL_PS_ROWS = 2762  # P55/P38 izbira (pageSelection.rows)

PIN_V6_EV_SHA = "de13f10bee5f7b6f21a389997e470214760f04b7f384f1236c7d6215feacfe18"
PIN_PACK_EV_SHA = "0779bb9a3ff0f1741c7104e5350be8963030b2b15fe381c3dbc023840bc720e7"
PIN_P59_EV_SHA = "650f13dccab1da70a60d04c41ce9f7887ca94eafea8a0a7927c104ca899b76f3"
PIN_P56_EV_SHA = "2fddc76fb94b69fed55170220fa8dfa3ace4a9466043d264b8b8df788e78a50c"
PIN_PARCELS_SHA = "fee91fca736348f40ef11d38b7a5b51d51656a9768cda648f4d737029bb3941f"
PIN_V6_RT_SHA = "6270b267be9aabb621e05ba8acc05b7a67458d3c77f0b42934202a852fef943d"

BLATT_ORDER = ["I", "II", "III", "IV", "V"]

# pričakovane meritve v7 (pini; vpisano po prvem zagonu; None = meri)
EXP = {
    "rows": 891, "bases": 879, "multi": 2, "cross": 0,
    "dropPairs": 48, "dropRows": 48, "lost": 0,
    "ambRows": 4, "ambDerived": 48,
    "conf": {"STRONG": 172, "MEDIUM": 588, "WEAK": 131},
    "series": {"S1": 803, "S2": 62, "BI": 26},
    "confDerived": 0,
    "area": {"pairsWithArea": 871, "medianRatio": 3.8102, "q25": 2.798,
             "q75": 7.0499, "tightN": 183, "tightShare": 0.2101,
             "shuffleMedian": 4.1435, "shuffleTightShare": 0.0586,
             "historicalQkM2": 3.59665, "deltaPct": 5.94},
    "spatial": {"consecPairs": 652, "medianM": 51.8, "q25M": 33.0,
                "q75M": 87.8, "share150": 0.9049, "shuffleMedianM": 1320.7,
                "shuffleShare150": 0.0171, "enrichmentX": 25.5},
    "readConfBI": {"STRONG": 3, "MEDIUM": 14, "WEAK": 9},
    "suffix": 271, "pos": 879,
    "removed": 48, "a2Different": 29, "ties": 0, "biDrop": 0,
}

DATE = "2026-10-15"
FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  ✗ {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fnum(v) -> float:
    try:
        return float(str(v).replace(",", ".")) if v not in (None, "") else 0.0
    except (TypeError, ValueError):
        return 0.0


def dm(a, b) -> float:
    return math.hypot((a[0] - b[0]) * M_PER_DEG_LAT,
                      (a[1] - b[1]) * M_PER_DEG_LAT * 0.7)


def re_match_base(s):
    import re
    m = re.match(r"\*?(\d+)", str(s or ""))
    return m.group(1) if m else None


def compute():
    print("P75 — v7: C4 cross-Blatt SPLIT opcija A1 (drop 48 ne-dominant-"
          "Blatt vrstic, 48 cross base)")

    # ——— vhodi ———
    v6ev = json.loads(V6_EV.read_text(encoding="utf-8"))
    pack = json.loads(PACK_EV.read_text(encoding="utf-8"))
    p59 = json.loads(P59_EV.read_text(encoding="utf-8"))
    p56 = json.loads(P56_EV.read_text(encoding="utf-8"))
    parcels = json.loads(PARCELS.read_text(encoding="utf-8"))

    bybase: dict[str, list[dict]] = defaultdict(list)
    for x in parcels:
        m = re_match_base(x.get("st"))
        if m:
            bybase[m].append(x)

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

    def bord(bl: str) -> int:
        i = BLATT_ORDER.index(bl)
        return i if i >= 0 else 99

    rows = v6ev["rowsEvidence"]

    # ——— I1: pini + nasledstvena veja v6 runtime ———
    pins = [(V6_EV, PIN_V6_EV_SHA, "v6 dokaz"),
            (PACK_EV, PIN_PACK_EV_SHA, "P74 cross pack dokaz"),
            (P59_EV, PIN_P59_EV_SHA, "P59 dokaz"),
            (P56_EV, PIN_P56_EV_SHA, "P56 dokaz"),
            (PARCELS, PIN_PARCELS_SHA, "PARCELS")]
    for path, pin, label in pins:
        if sha256(path) != pin:
            fail(f"I1 {label} sha {sha256(path)[:8]}… ≠ {pin[:8]}…")
        else:
            ok(f"I1 {label} sha pin")
    rt_sha = sha256(V6_RT)
    if rt_sha == PIN_V6_RT_SHA:
        ok("I1 v6 runtime sha pin (v6 — pred zapisom v7)")
    else:
        rt_disk = json.loads(V6_RT.read_text(encoding="utf-8"))
        d7 = rt_disk.get("v7Delta") or {}
        if rt_disk.get("version", 0) >= 7 and d7.get("droppedPairs") == 48 \
                and d7.get("droppedRows") == 48:
            ok("I1 v6 runtime nadgrajen na v"
               f"{rt_disk.get('version')} po P75 (C4 SPLIT-A1) — vhodne "
               "vrstice iz v6 dokaza rowsEvidence (arhiv bajtno); "
               "nasledstvo deklarirano")
        else:
            fail(f"I1 v6 runtime sha odmika ({rt_sha[:8]}…) in nasledstvo "
                 "ni deklarirano (version "
                 f"{rt_disk.get('version')}, v7Delta {bool(d7)})")
    if len(rows) != 939:
        fail(f"I1 v6 rowsEvidence {len(rows)} ≠ 939")
    if v6ev.get("version") != 6:
        fail(f"I1 v6 dokaz version {v6ev.get('version')} ≠ 6")

    # ——— I2: re-izpeljava cross seta (P74 logika) == P74 dokaz ———
    bybase_rows: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        bybase_rows[r["base"]].append(r)
    cross: dict[str, dict] = {}
    ties = 0
    for b, rs in bybase_rows.items():
        bls = {blatt_of(r["page"]) for r in rs if blatt_of(r["page"])}
        if len(bls) < 2:
            continue
        pages_by_blatt: dict[str, set[int]] = defaultdict(set)
        area_by_blatt: dict[str, float] = defaultdict(float)
        owners_by_blatt: dict[str, set] = defaultdict(set)
        for r in rs:
            bl = blatt_of(r["page"])
            if not bl:
                continue
            pages_by_blatt[bl].add(r["page"])
            area_by_blatt[bl] += (r["areaQK"] or 0.0)
            if r.get("owner"):
                owners_by_blatt[bl].add(r["owner"])
        bls_sorted = sorted(bls, key=bord)
        # lastniška disjunktnost (set-izračun)
        osets = [owners_by_blatt[bl] for bl in bls_sorted]
        osetsn = [s for s in osets if s]
        disjoint = all(a.isdisjoint(c)
                       for i, a in enumerate(osetsn)
                       for c in osetsn[i + 1:])
        # dominant Blatt: max Σ areaQK; ties → min Blatt
        mx = max(area_by_blatt[bl] for bl in bls_sorted)
        tops = [bl for bl in bls_sorted
                if abs(area_by_blatt[bl] - mx) < 1e-9]
        if len(tops) > 1:
            ties += 1
        dominant = tops[0]
        cross[b] = {
            "blattPair": "·".join(bls_sorted),
            "pages": sorted(r["page"] for r in rs),
            "dominantBlatt": dominant,
            "ownerRelation": "disjoint" if disjoint else "overlap",
        }
    if len(cross) != 48:
        fail(f"I2 cross base {len(cross)} ≠ 48")
    xrows = sum(1 for r in rows if r["base"] in cross)
    if xrows != 96:
        fail(f"I2 cross vrstice {xrows} ≠ 96")
    one_per = 0
    blatt_dist: dict[str, int] = defaultdict(int)
    adj = 0
    skip = 0
    for b in cross:
        rs = bybase_rows[b]
        per_blatt: dict[str, int] = defaultdict(int)
        bls_set = set()
        for r in rs:
            bl = blatt_of(r["page"])
            if bl:
                per_blatt[bl] += 1
                bls_set.add(bl)
        if all(n == 1 for n in per_blatt.values()) and len(bls_set) >= 2:
            one_per += 1
        bls_sorted = sorted(bls_set, key=bord)
        blatt_dist["·".join(bls_sorted)] += 1
        if len(bls_sorted) == 2 and bord(bls_sorted[1]) - bord(bls_sorted[0]) == 1:
            adj += 1
        else:
            skip += 1
    if one_per != 48:
        fail(f"I2 1 vrstica per Blatt {one_per} ≠ 48/48")
    want_dist = {"I·II": 13, "II·III": 16, "III·IV": 1, "IV·V": 18}
    if dict(blatt_dist) != want_dist:
        fail(f"I2 blattDist {dict(blatt_dist)} ≠ {want_dist}")
    if adj != 48 or skip != 0:
        fail(f"I2 sosednji/skoki {adj}/{skip} ≠ 48/0")
    ndisj = sum(1 for c in cross.values() if c["ownerRelation"] == "disjoint")
    if ndisj != 48:
        fail(f"I2 lastniki disjunktni {ndisj} ≠ 48")
    # bajtno == P74 dokaz "bases"
    p74_bases = pack.get("bases", {})
    if len(p74_bases) != 48:
        fail(f"I2 P74 dokaz bases {len(p74_bases)} ≠ 48")
    mism = []
    for b, c in cross.items():
        d = p74_bases.get(b)
        if not d:
            mism.append(f"{b}: manjka v P74")
            continue
        theirs = {
            "blattPair": d.get("blattPair"),
            "pages": list(d.get("pages", [])),
            "dominantBlatt": d.get("dominantBlatt"),
            "ownerRelation": d.get("ownerRelation"),
        }
        mine = {
            "blattPair": c["blattPair"],
            "pages": c["pages"],
            "dominantBlatt": c["dominantBlatt"],
            "ownerRelation": c["ownerRelation"],
        }
        if mine != theirs:
            mism.append(f"{b}: {mine} ≠ {theirs}")
        # A1 keep re-izpeljava == pack optionA
        oa = d.get("optionA", {})
        if oa.get("keepBlatt") != c["dominantBlatt"]:
            mism.append(f"{b}: keepBlatt {oa.get('keepBlatt')} ≠ dominant "
                        f"{c['dominantBlatt']}")
        kp = bybase_rows[b][0]["page"] if len(bybase_rows[b]) == 1 else None
        kp_pages = sorted({r["page"] for r in bybase_rows[b]
                           if blatt_of(r["page"]) == c["dominantBlatt"]})
        if len(kp_pages) == 1 and oa.get("keepPage") not in (None, kp_pages[0]):
            mism.append(f"{b}: keepPage {oa.get('keepPage')} ≠ "
                        f"{kp_pages[0]}")
    if mism:
        for m in mism[:5]:
            fail(f"I2 {m}")
        fail(f"I2 re-izpeljani cross set ≠ P74 dokaz ({len(mism)} odmikov)")
    else:
        ok("I2 cross set re-izpeljava == P74 dokaz (48 base · 96 vrstic · "
           "1 per Blatt 48/48 · lastniki disjunktni 48/48 · dominantBlatt "
           "== pack · ties 0)")

    # ——— I3: drop izpeljava == P74 optionA1 (+ A2 kontrola) ———
    drop = set()  # (page, base) kombinacije
    a2_diff = 0
    for b, c in cross.items():
        dom = c["dominantBlatt"]
        min_bl = sorted({blatt_of(r["page"]) for r in bybase_rows[b]
                         if blatt_of(r["page"])}, key=bord)[0]
        if min_bl != dom:
            a2_diff += 1
        for r in bybase_rows[b]:
            if blatt_of(r["page"]) != dom:
                drop.add((r["page"], b))
    drop_pairs = len(drop)
    drop_rows = sum(1 for r in rows if (r["page"], r["base"]) in drop)
    bi_drop = sum(1 for r in rows
                  if (r["page"], r["base"]) in drop and r["series"] == "BI")
    rows_a = [r for r in rows if (r["page"], r["base"]) not in drop]
    bases_a = {r["base"] for r in rows_a}
    lost = len({r["base"] for r in rows}) - len(bases_a)
    s74 = pack.get("summary", {})
    oa1 = s74.get("optionA1", {})
    checks3 = [
        (drop_pairs, 48, "dropPairs"), (drop_rows, 48, "dropRows"),
        (len(rows_a), 891, "rows"), (len(bases_a), 879, "bases"),
        (lost, 0, "lost"),
        (a2_diff, s74.get("optionA2DifferentKeep"), "A2 različen keep"),
        (oa1.get("drop"), 48, "P74 A1 drop"), (oa1.get("rows"), 891,
                                               "P74 A1 rows"),
        (oa1.get("bases"), 879, "P74 A1 bases"), (oa1.get("lost"), 0,
                                                  "P74 A1 lost"),
        (oa1.get("multi"), 2, "P74 A1 multi"), (oa1.get("cross"), 0,
                                                "P74 A1 cross"),
        (oa1.get("ambRows"), 4, "P74 A1 ambRows"),
    ]
    for got, want, label in checks3:
        if want is None:
            continue
        if got != want:
            fail(f"I3 {label} {got} ≠ {want}")
    if ties != s74.get("shareTies"):
        fail(f"I3 ties {ties} ≠ pack {s74.get('shareTies')}")
    if not any(f.startswith("I3") for f in FAILURES):
        ok(f"I3 drop == P74 optionA1: {drop_pairs} kombinacij = "
           f"{drop_rows} vrstic; rows 939 → {len(rows_a)}; bases "
           f"{len(bases_a)}; lost {lost}; A2 različen keep {a2_diff} "
           f"(sameKeep {48 - a2_diff}); ties {ties}; BI drop {bi_drop}")

    # ——— izvedba: ohranjene vrstice (_srcIdx identiteta) ———
    out_rows: list[dict] = []
    removed_rows: list[dict] = []
    for idx, r in enumerate(rows):
        if (r["page"], r["base"]) in drop:
            removed_rows.append({
                "page": r["page"], "base": r["base"],
                "parzella": r["parzella"], "owner": r["owner"],
                "areaQK": r["areaQK"],
                "reason": "C4: cross-Blatt SPLIT opcija A1 (P74 pack — "
                          "48 cross base z vrsticami na ≥ 2 sosednjih "
                          "Blattih, lastniki med Blatti disjunktni 48/48; "
                          "drop ne-dominant-Blatt vrstica, keep = dominant "
                          "Blatt po Σ areaQK; lastniško soglasje P75; "
                          "vrstica ostane v registru brez geometrije)",
            })
            continue
        r2 = dict(r)
        r2["_srcIdx"] = idx
        out_rows.append(r2)
    if len(removed_rows) != drop_rows or len(out_rows) != len(rows_a):
        fail(f"I3 izvedba: removed {len(removed_rows)} ≠ {drop_rows} ali "
             f"rows {len(out_rows)} ≠ {len(rows_a)}")

    # ——— I4: ohranjene vrstice (pred group-derived) ———
    pages_by: dict[str, set[int]] = defaultdict(set)
    for r in out_rows:
        pages_by[r["base"]].add(r["page"])
    multi = [b for b in pages_by if len(pages_by[b]) > 1]
    bl_by: dict[str, set[str]] = defaultdict(set)
    for r in out_rows:
        bl = blatt_of(r["page"])
        if bl:
            bl_by[r["base"]].add(bl)
    cross7 = [b for b in bl_by if len(bl_by[b]) > 1]
    orphans = sorted(b for b in {r["base"] for r in rows}
                     if b not in pages_by)
    if orphans:
        fail(f"I4 base brez vrstic po dropu: {orphans}")
    else:
        ok("I4 po C4 noben base ne izgubi vseh vrstic (0 praznih; "
           f"lost {lost})")

    # ——— I5: ambiguous prekalkulacija (P55 metoda) ———
    amb_changes: list[tuple] = []
    for r in out_rows:
        new_amb = len(pages_by[r["base"]]) > 1
        if new_amb != r["ambiguous"]:
            amb_changes.append((r["page"], r["base"], r["ambiguous"],
                                new_amb))
            r["ambiguous"] = new_amb
    amb_rows = sum(1 for r in out_rows if r["ambiguous"])

    # conf prekalkulacija (P71 metoda) — geografija nespremenjena → 0
    pos_by_base = {}
    for b in pages_by:
        gp = group_pos(b)
        if gp:
            pos_by_base[b] = (gp[0], gp[1])
    neigh_ok: set[str] = set()
    for b, p in pos_by_base.items():
        n = int(b)
        for m2 in (n - 1, n + 1):
            q2 = pos_by_base.get(str(m2))
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
    if len(conf_changes) != EXP["confDerived"]:
        fail(f"I5 confDerived {len(conf_changes)} ≠ {EXP['confDerived']} "
             "(geografija vrstic nespremenjena → conf deprivacija 0)")
    else:
        ok(f"I5 conf prekalkulacija: 0 sprememb ({len(conf_changes)} == "
           f"{EXP['confDerived']}) — geografija nedeprava")

    # ——— I4/I6: nespremenjene vrstice bajtno == v6 ———
    amb_idx = {(page, base) for page, base, _, _ in amb_changes}
    n_unchanged = 0
    n_derived = 0
    for r in out_rows:
        idx = r.pop("_srcIdx", None)
        if idx is None:
            fail(f"I6 vrstica p{r['page']} {r['base']} brez _srcIdx")
            continue
        old = rows[idx]
        if (r["page"], r["base"]) in amb_idx:
            n_derived += 1
            if old["ambiguous"] == r["ambiguous"]:
                fail(f"I6 vrstica p{r['page']} {r['base']} v amb_changes, "
                     "vrednost pa nespremenjena")
            # vsa DRUGA polja (razen ambiguous) bajtno == v6
            a = {k: v for k, v in r.items() if k != "ambiguous"}
            b = {k: v for k, v in old.items() if k != "ambiguous"}
            if json.dumps(a, ensure_ascii=False, sort_keys=True) != \
                    json.dumps(b, ensure_ascii=False, sort_keys=True):
                fail(f"I6 derived vrstica p{r['page']} {r['base']}: "
                     "ostala polja odmikajo od v6")
            continue
        if json.dumps(r, ensure_ascii=False, sort_keys=True) != \
                json.dumps(old, ensure_ascii=False, sort_keys=True):
            fail(f"I6 vrstica p{r['page']} {r['base']} nespremenjena, "
                 f"a odmika od v6")
        n_unchanged += 1
    ok(f"I6 nespremenjene vrstice bajtno == v6 ({n_unchanged}); "
       f"group-derived (ambiguous) {n_derived}; izpad C4 {len(removed_rows)}")

    # ——— I6: meritve v7 ———
    bases7 = set(pages_by)
    s1s2 = [r for r in out_rows if r["series"] != "BI"]
    bi_rows = [r for r in out_rows if r["series"] == "BI"]
    conf_counts: dict[str, int] = defaultdict(int)
    for r in out_rows:
        conf_counts[r["conf"]] += 1
    series_counts = {k: sum(1 for r in out_rows if r["series"] == k)
                     for k in ("S1", "S2", "BI")}
    suffix_groups = sum(1 for b in pos_by_base if len(bybase[b]) > 1)
    read_conf_bi = {"STRONG": 0, "MEDIUM": 0, "WEAK": 0}
    for r in bi_rows:
        rc = r.get("readConf")
        if rc in read_conf_bi:
            read_conf_bi[rc] += 1

    area_pairs = [(r["areaQK"], r["areaModern"]) for r in out_rows
                  if r["areaQK"] and r["areaModern"] and not r["areaSuspect"]]
    ratios = [m2 / a for a, m2 in area_pairs]
    area_median = statistics.median(ratios)
    tight_n = sum(1 for x in ratios
                  if abs(x / HIST_QK_M2 - 1) <= AREA_BAND)
    mods = [m2 for _, m2 in area_pairs]
    rng = random.Random(SEED_AREA)
    rng.shuffle(mods)
    sh_ratios = [m2 / a for (a, _), m2 in zip(area_pairs, mods)]
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
    ok(f"I6 meritve v7: rows {len(out_rows)} · bases {len(bases7)} · "
       f"multi {len(multi)} · cross {len(cross7)} · ambRows {amb_rows} · "
       f"conf {conf_counts.get('STRONG', 0)}/{conf_counts.get('MEDIUM', 0)}"
       f"/{conf_counts.get('WEAK', 0)} · area median "
       f"{area_proof['medianRatio']} (Δ {area_proof['deltaPct']} %) · "
       f"sosledje {spatial_proof['consecPairs']} parov / "
       f"{spatial_proof['medianM']} m")

    if EXP["rows"] is not None and EXP["conf"] is not None:
        checks = [
            (len(out_rows), EXP["rows"], "rows"),
            (len(bases7), EXP["bases"], "bases"),
            (len(multi), EXP["multi"], "multi"),
            (len(cross7), EXP["cross"], "cross"),
            (amb_rows, EXP["ambRows"], "ambRows"),
            (len(removed_rows), EXP["removed"], "removed"),
            (drop_pairs, EXP["dropPairs"], "dropPairs"),
            (drop_rows, EXP["dropRows"], "dropRows"),
            (lost, EXP["lost"], "lost"),
            (len(amb_changes), EXP["ambDerived"], "ambDerived"),
            (suffix_groups, EXP["suffix"], "suffix"),
            (len(pos_by_base), EXP["pos"], "pos"),
            (a2_diff, EXP["a2Different"], "a2Different"),
            (ties, EXP["ties"], "ties"),
            (bi_drop, EXP["biDrop"], "biDrop"),
        ]
        for got, want, label in checks:
            if want is None:
                continue
            if got != want:
                fail(f"I6 {label} {got} ≠ {want}")
        if dict(conf_counts) != EXP["conf"]:
            fail(f"I6 conf {dict(conf_counts)} ≠ {EXP['conf']}")
        if series_counts != EXP["series"]:
            fail(f"I6 series {series_counts} ≠ {EXP['series']}")
        if area_proof != EXP["area"]:
            fail(f"I6 areaProof {area_proof} ≠ pin")
        if spatial_proof != EXP["spatial"]:
            fail(f"I6 spatialProof {spatial_proof} ≠ pin")
        if read_conf_bi != EXP["readConfBI"]:
            fail(f"I6 readConfBI {read_conf_bi} ≠ pin")
        if not FAILURES:
            ok("I6 meritve == pini (vse)")
    else:
        print("  ── PINE ZA VPIS (EXP) ————————————————————")
        print(f"    rows={len(out_rows)}, bases={len(bases7)}, "
              f"multi={len(multi)}, cross={len(cross7)}, "
              f"ambRows={amb_rows}, suffix={suffix_groups}, "
              f"pos={len(pos_by_base)}, removed={len(removed_rows)}, "
              f"dropPairs={drop_pairs}, dropRows={drop_rows}, "
              f"lost={lost}, ambDerived={len(amb_changes)}, "
              f"a2Different={a2_diff}, ties={ties}, biDrop={bi_drop}")
        print(f"    conf={dict(conf_counts)}, series={series_counts}")
        print(f"    readConfBI={read_conf_bi}")
        print(f"    area={json.dumps(area_proof)}")
        print(f"    spatial={json.dumps(spatial_proof)}")
        print(f"    removedByPage={dict(sorted(Counter(r['page'] for r in removed_rows).items()))}")

    # blattDist po C4 (pričakovano prazno — cross 0)
    blatt_dist7: dict[str, int] = defaultdict(int)
    for b in cross7:
        pair = "·".join(sorted(bl_by[b], key=bord))
        blatt_dist7[pair] += 1

    v6_join = v6ev["join"]
    join_block = {
        "matchedRows": len(out_rows),
        "matchedRowsS1S2": len(s1s2),
        "matchedRowsBI": len(bi_rows),
        "matchedSharePct": round(100 * len(out_rows) / TOTAL_PS_ROWS, 1),
        "psUniqueNumbers": v6_join["psUniqueNumbers"],
        "psPositionedParcels": len(pos_by_base),
        "suffixGroups": suffix_groups,
        "seriesCounts": series_counts,
        "confCounts": {"STRONG": conf_counts["STRONG"],
                       "MEDIUM": conf_counts["MEDIUM"],
                       "WEAK": conf_counts["WEAK"]},
        "readConfBI": read_conf_bi,
        "ambiguousBases": len(multi),
        "ambiguousRows": amb_rows,
    }
    per_blatt_amb = {
        "basesOnMultiplePages": len(multi),
        "rowsWithAmbiguousBase": amb_rows,
        "note": f"base na > 1 strani v v7 (po C4 cross-Blatt SPLIT opcija "
                f"A1; 48 cross base na eni strani po dropu ne-dominant "
                f"Blatta); čez-Blatt {len(cross7)} (blattDist " +
                (" · ".join(f"{k} {v}" for k, v in sorted(blatt_dist7.items()))
                 if blatt_dist7 else "—")
                + ") [~]",
    }
    return (out_rows, removed_rows, amb_changes, conf_changes, join_block,
            per_blatt_amb, area_proof, spatial_proof, v6ev, p56, multi,
            cross7, bases7, blatt_dist7, pos_by_base, drop_pairs, drop_rows,
            lost, a2_diff, ties, bi_drop)


def _status_line(out_rows, removed_rows, join_block, per_blatt_amb, cross7,
                 area_proof, spatial_proof, drop_pairs, drop_rows, a2_diff):
    return (
        f"P75 SPLIT v6: C4 cross-Blatt SPLIT opcija A1 — 48 cross base "
        f"(P74 pack: vrstice na ≥ 2 sosednjih Blattih I·II 13 · II·III 16 "
        f"· III·IV 1 · IV·V 18; 1 vrstica per Blatt 48/48; lastniki "
        f"disjunktni 48/48; pageMap prekrivanja 48/48 — per-Blatt "
        f"ponovitev numeracije): drop {drop_pairs} kombinacij = "
        f"{drop_rows} vrstic (keep = DOMINANT Blatt po Σ areaQK; ties 0; "
        f"A2 različen keep pri {a2_diff} base; vrstice ostanejo v "
        f"registru brez geometrije; lastniška odločitev 2026-10-15); "
        f"0 base brez vrstic; v7: {len(out_rows)} vrstic / "
        f"{join_block['psPositionedParcels']} base / multi-page "
        f"{per_blatt_amb['basesOnMultiplePages']} / cross-Blatt "
        f"{len(cross7)}; area median {area_proof['medianRatio']} "
        f"(Δ {area_proof['deltaPct']} %), sosledje "
        f"{spatial_proof['consecPairs']} parov / {spatial_proof['medianM']} m "
        f"({spatial_proof['enrichmentX']}×)"
    )


def _verdict_si(out_rows, join_block) -> str:
    return (
        "Cross-Blatt SPLIT joina izveden (opcija A1 iz P74 packa; "
        "lastniška odločitev 2026-10-15): za 48 base z vrsticami na ≥ 2 "
        "sosednjih Blattih z disjunktnimi lastniki (ista številka pod "
        "dvema Blattoma = 2 realni parceli — numeracija per Blatt se "
        "ponovi; P56 pageMap prekrivanja 48/48) je vrstica ne-dominantnega "
        "Blatta izpadla iz joina (48 kombinacij = 48 vrstic; keep = "
        "DOMINANT Blatt po Σ areaQK; ties 0; A2 bi pri 29 base obdržala "
        "drugo vrstico) — konec lažnih fuzij čez Blatte po celotnem "
        "registru; vrstice ostanejo v registru (removedRows), noben base "
        "ne izgubi vseh vrstic; ambiguous prekalkuliran po P55 metodi, "
        "conf nespremenjen (geografija nedeprava). V7: "
        f"{len(out_rows)} vrstic ({round(100 * len(out_rows) / 2762, 1)} "
        f"% izbire) / {join_block['psPositionedParcels']} base. "
        "Opcija B (per-Blatt instance + razdelitev geometrije) ostane "
        "vezana na georef Blattnih kart [~]."
    )


def _verdict_en(out_rows, join_block) -> str:
    return (
        "Cross-Blatt SPLIT of the join executed (option A1 from the P74 "
        "pack; owner decision 2026-10-15): for the 48 bases with rows on "
        "≥ 2 adjacent Blatts and disjoint owners across Blatts (the same "
        "number under two Blatts = 2 real parcels — per-Blatt numbering "
        "repeats; P56 pageMap overlaps 48/48), the non-dominant-Blatt row "
        "is dropped from the join (48 combinations = 48 rows; keep = the "
        "DOMINANT Blatt by Σ areaQK; no ties; A2 would keep the other row "
        "for 29 bases) — an end to cross-Blatt false fusions across the "
        "whole register; rows remain in the register (removedRows), no "
        "base loses all rows; ambiguous recomputed per the P55 method, "
        "conf unchanged (geography untouched). V7: "
        f"{len(out_rows)} rows ({round(100 * len(out_rows) / 2762, 1)} "
        f"% of the selection) / {join_block['psPositionedParcels']} bases. "
        "Option B (per-Blatt instances + geometry split) remains tied to "
        "the georeferencing of the Blatt maps [~]."
    )


def _next_list() -> list:
    return [
        "LASTNIŠKO: opcija A2 (keep MIN Blatt — različen keep pri 29 base) "
        "ali B (per-Blatt instance + razdelitev geometrije; georef Blattnih "
        "kart [~]) — reverzija/dopolnitev C4 dokumentirana",
        "LASTNIŠKO: per-Blatt instance sekcij (56 vrstic; P60 moda B / PF "
        "protokol)",
        "praznine brez registrskih strani: PF 1644–1655, 1673/1679, "
        "1842–1860, 1904/1906 (modernVoid [~])",
        "operacijsko: GitHub Actions billing (#7)",
    ]


def compute_pair():
    """Ponovni preizračun (brez pisanja) — vrne (evidence, runtime)."""
    global FAILURES
    FAILURES = []
    (out_rows, removed_rows, amb_changes, conf_changes, join_block,
     per_blatt_amb, area_proof, spatial_proof, v6ev, p56, multi, cross7,
     bases7, blatt_dist7, pos_by_base, drop_pairs, drop_rows, lost,
     a2_diff, ties, bi_drop) = compute()
    if FAILURES:
        raise SystemExit(f"P75 compute: invariant padel: {FAILURES[:3]}")

    v6rt = json.loads(V6_RT.read_text(encoding="utf-8"))
    # zgodovinski bloki iz v6 runtime (nasledstvena veja: disk lahko že v7;
    # v5Delta/v6Delta/furkovce/historicalConstant/pageSelection so del
    # zgodovine — vzamem iz diska NEODVISNO od verzije, dokler obstajajo)
    hist_constant = v6rt.get("historicalConstant")
    page_sel = v6rt.get("pageSelection")
    v5_delta = v6rt.get("v5Delta")
    v6_delta = v6rt.get("v6Delta")
    furkovce = v6ev["furkovce"]

    evidence = {
        "version": 7,
        "task": "P75 (issue #13) — PS-PARCELS-GEO v7: cross-Blatt SPLIT "
                "(opcija A1 — drop ne-dominant-Blatt vrstic za 48 cross "
                "base)",
        "date": DATE,
        "generatedBy": "scripts/p75_ps_v7_cross_split_a1.py",
        "principle": "samo odstranjevanje dokumentiranih lažnih fuzij "
                     "(ista številka pod dvema sosednjima Blattoma = 2 "
                     "realni parceli; per-Blatt numeracija); noben nov "
                     "podatek; cross set derivat determinističnih "
                     "lastnosti (strani × Blatt × lastniki × areaQK) iz "
                     "committed dokazov",
        "inputs": {
            "v6ProofSha256": sha256(V6_EV),
            "crossPackProofSha256": sha256(PACK_EV),
            "p59ProofSha256": sha256(P59_EV),
            "p56ProofSha256": sha256(P56_EV),
            "parcelsSha256": sha256(PARCELS),
        },
        "corrections": {
            "C4": {
                "title": "cross-Blatt SPLIT opcija A1: drop "
                         "ne-dominant-Blatt vrstic za 48 cross base",
                "decision": "LASTNIK (P75): opcija A1 iz P74 packa (keep "
                            "DOMINANT Blatt po Σ areaQK; ties 0; A2 "
                            "različen keep pri 29 base; B zahteva georef "
                            "Blattnih kart [~]); ukaz 'nadaljuj' "
                            "2026-10-15 po odločitvenem paketu P74",
                "evidence": {
                    "crossPack": "research/issue17/"
                                 "ps-cross-blatt-pack.json (48 base; 96 "
                                 "vrstic; 1 vrstica per Blatt 48/48; "
                                 "lastniki disjunktni 48/48; blattDist "
                                 "I·II 13 · II·III 16 · III·IV 1 · IV·V "
                                 "18; skoki 0; pageMap prekrivanja "
                                 "48/48; geoShared 48/48; ties 0)",
                    "crossBases": 48,
                    "droppedPairs": drop_pairs,
                    "droppedRows": drop_rows,
                    "a2DifferentKeep": a2_diff,
                    "pageMapProof": "ista številka pod dvema Blattoma = "
                                    "2 realni parceli — P56 pageMap "
                                    "prekrivanja razponov 48/48 (p11 I "
                                    "161–183 / p61 II 161–180; p64 II "
                                    "1821–1840 / p94 III 1821–1841; "
                                    "p110 IV 2141–2160 / p125 V "
                                    "2141–2160)",
                },
                "droppedRows": removed_rows,
            },
        },
        "removedRows": removed_rows,
        "join": join_block,
        "v7Delta": {
            "reason": "C4: cross-Blatt SPLIT opcija A1 — drop "
                      "ne-dominant-Blatt vrstic za 48 cross base (P74 "
                      "pack; lastniška odločitev 2026-10-15; konec "
                      "lažnih fuzij čez Blatte)",
            "crossBases": 48,
            "droppedPairs": drop_pairs,
            "droppedRows": len(removed_rows),
            "before": {"rows": 939, "bases": 879, "multiPage": 50,
                       "crossBlatt": 48},
            "after": {"rows": len(out_rows), "bases": len(bases7),
                      "multiPage": per_blatt_amb["basesOnMultiplePages"],
                      "crossBlatt": len(cross7)},
            "invariance": "ohranjene vrstice bajtno == v6 (lekcija P9; "
                          "drop samo odstranjuje); ambiguous prekalkuliran "
                          "po P55 metodi (derivat strani; 48 derived "
                          "True→False); conf nespremenjen (geografija "
                          "nedeprava); v6 ostaja arhiviran "
                          "(research/issue17/ps-parcels-geo-v6.json)",
            "note": "C4 odstranjuje LE lažne fuzije (ista številka pod "
                    "dvema Blattoma; lastniki med Blatti disjunktni) — "
                    "noben nov podatek ni izmišljen; vrstice ostanejo v "
                    "registru brez geometrije; opcija A2 bi pri 29 base "
                    "obdržala drugo vrstico (izbira pravila lastniška)",
        },
        "v6Delta": v6_delta,
        "v5Delta": v5_delta,
        "areaProof": area_proof,
        "spatialProof": spatial_proof,
        "furkovce": furkovce,
        "perBlattAmbiguity": per_blatt_amb,
        "invariants": {
            "I1": "pini v6/P74 pack/P59/P56/PARCELS sha256; v6 runtime "
                  "nasledstvena veja (v6 pin ALI version ≥ 7 + v7Delta "
                  "droppedPairs 48)",
            "I2": "cross set re-izpeljava == P74 dokaz (bajtno; 48 · 96 · "
                  "1 per Blatt 48/48 · disjunktni 48/48 · dominantBlatt "
                  "== pack · ties 0)",
            "I3": "drop == P74 optionA1 (48 kombinacij = 48 vrstic; rows "
                  "891; bases 879; lost 0; multi 2; cross 0; ambRows 4); "
                  "A2 različen keep 29; BI drop izmerjen",
            "I4": "po C4 noben base ne izgubi vseh vrstic (0 praznih)",
            "I5": "ambiguous P55 prekalkulacija == pini; conf 0 sprememb "
                  "(geografija nedeprava)",
            "I6": "meritve == pini; nespremenjene vrstice bajtno == v6; "
                  "derived vrstice: ostala polja bajtno == v6",
            "I7": "dokaz ⊇ runtime bajtno",
            "I8": "determinizem --check bajtno",
        },
        "statusLine": _status_line(out_rows, removed_rows, join_block,
                                   per_blatt_amb, cross7, area_proof,
                                   spatial_proof, drop_pairs, drop_rows,
                                   a2_diff),
        "verdictSi": _verdict_si(out_rows, join_block),
        "verdictEn": _verdict_en(out_rows, join_block),
        "next": _next_list(),
        "rowsEvidence": out_rows,
    }
    runtime = {
        "version": 7,
        "task": "P75 (issue #13) — cross-Blatt SPLIT opcija A1 (C4)",
        "date": DATE,
        "generatedBy": "scripts/p75_ps_v7_cross_split_a1.py",
        "historicalConstant": hist_constant,
        "pageSelection": page_sel,
        "join": join_block,
        "v7Delta": evidence["v7Delta"],
        "v6Delta": v6_delta,
        "v5Delta": v5_delta,
        "areaProof": area_proof,
        "spatialProof": spatial_proof,
        "furkovce": furkovce,
        "perBlattAmbiguity": per_blatt_amb,
        "statusLine": evidence["statusLine"],
        "rows": out_rows,
    }
    return evidence, runtime


def build_documents():
    try:
        evidence, runtime = compute_pair()
    except SystemExit as e:
        print(f"P75: {e}")
        return 1
    OUT_EV.write_text(jdump_pretty(evidence), encoding="utf-8")
    OUT_RUNTIME.write_text(jdump_pretty(runtime), encoding="utf-8")
    print(f"P75: dokaz → {OUT_EV.relative_to(REPO)}; runtime → "
          f"{OUT_RUNTIME.relative_to(REPO)} (v7)")
    return 0


def jdump_pretty(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def check():
    """I8: drugi preizračun bajtno identičen zapisanima dokumentoma."""
    ev1 = json.loads(OUT_EV.read_text(encoding="utf-8"))
    ev1s = json.dumps(ev1, ensure_ascii=False, sort_keys=True)
    ev2, _rt2 = compute_pair()
    if json.dumps(ev2, ensure_ascii=False, sort_keys=True) != ev1s:
        print("  ✗ I8 dokaz: drugi preizračun ≠ zapisano")
        return 1
    print("  ✓ I8 determinizem: drugi preizračun bajtno == zapisan dokaz "
          "(runtime nasledstvo po zapisu)")
    if FAILURES:
        print(f"P75 --check: {len(FAILURES)} invariant(ov) PADLO")
        for f in FAILURES:
            print(f"  → {f}")
        return 1
    print("P75 --check: VSE INVARIANTE PASS (bajtno)")
    return 0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "--check":
        sys.exit(check())
    sys.exit(build_documents())


if __name__ == "__main__":
    main()
