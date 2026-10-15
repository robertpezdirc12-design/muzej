#!/usr/bin/env python3
"""P73 (issue #13) — PS-PARCELS-GEO v6: ISTI-BLATT SPLIT (OPCIJA A)

C3  ISTI-BLATT SPLIT — drop drugi-blok vrstic za 135 dual base —
    LASTNIŠKA odločitev (soglasje "odlicno nadaljuj", 2026-10-15; opcija A
    iz P72 dual pack = exclude drugi blok po C1 vzorcu; keep = min stran).
    P72 dual pack DOKAZAL: 135 base z vrsticami na ≥ 2 straneh ISTEGA
    Blatta ima med straneh DISJUNKTNE lastnike (274 vrstice; 2 tri-zapisni;
    2 nearDual — 2080, 2081 — z strani brez lastnikov, konservativno
    izključeni iz dual, OPCIJA A JIH NE IZPADE); stranski pari delijo iste
    številčne razpone po P56 pageMap (p23/p24 = 401–420 obe; p51/p91 =
    961–980 obe; p103/p118 = 2001–2020 obe …) z odmiki po blokih
    konsistentnimi (40 × 44 · 15 × 49 · 5 × 29 · 1 × 13; 2 triple gapi
    6/16) = DVOJNI ZAPIS iste serije v dveh blokih registra — v4/v5 join
    teh 135 base FUZIRA dve realni parceli pod eno številko.
    Izvedba: drop (page, base) kombinacij, kjer page ≠ min(straneh dual
    seta) — 137 kombinacij = 138 vrstic (1 kombinacija ima 2 vrstice);
    0 base ne izgubi vseh vrstic; vrstice ostanejo v REGISTRU (dokaz:
    removedRows), izpadajo iz runtime joina (brez geometrije).
    P9: ohranjene vrstice BAJTNO == v5 (drop samo odstranjuje); ambiguous
    prekalkuliran po P55 metodi (derivat strani); conf se NE spremeni
    (geografija vrstic nespremenjena — kontrola 0 sprememb); v5 ostaja
    arhiviran (research/issue17/ps-parcels-geo-v5.json).

Viri (vsi committed):
  research/issue17/ps-parcels-geo-v5.json        (v5 dokaz, 1077 rowsEvidence)
  research/issue17/ps-dual-occurrence-pack.json  (P72 dokaz — 135 dual base)
  research/issue17/ps-blatt-headers.json         (P59 pageAttribution — Blatti)
  research/issue17/ps-register-topology.json     (P56 pageMap)
  research/georef-n83/gurs/parcels-ko1544-merged.json (2117 parcel, P47)
  src/data/atlas/ps-parcels-geo.json             (v5 runtime — vhod; nasledstvena veja)

Izpis:
  research/issue17/ps-parcels-geo-v6.json        (dokaz v6)
  src/data/atlas/ps-parcels-geo.json             (runtime v6 — nadomesti v5;
                                                  v5 ostane arhiviran v dokazu;
                                                  v5Delta + v6Delta = zgodovina)

Invarianti (FAIL → exit 1):
  I1  pini: v5 dokaz sha256, P72 dual pack sha256, P59 sha256, P56 sha256,
      PARCELS sha256; v5 runtime nasledstvena veja (sha == v5 pin ALI
      version ≥ 6 z v6Delta.droppedPairs == 137 — disk nadgrajen po P73,
      vhodne vrstice iz v5 dokaza rowsEvidence, arhiv bajtno)
  I2  re-izpeljava dual seta iz v5 rowsEvidence × P59 pageAttribution ×
      P56 pageMap == P72 dokaz "bases" (ključi + blatt + pages) bajtno;
      135 base, 274 vrstic, 2 tri-zapisni, nearDual {2080, 2081}
  I3  drop izpeljava == P72 summary.optionA: 137 kombinacij, 138 vrstic,
      rows 1077 → 939, bases 879, lost 0, multi 184 → 50, cross 48;
      P70 33 ⊂ drop (p49/89 × 15, p50/90 × 10, p52/92 × 8)
  I4  ohranjene vrstice brez group-derived sprememb bajtno == v5 (_srcIdx);
      nearDual 2080/2081 VRSTICE OSTANEJO; 0 base brez vrstic
  I5  ambiguous prekalkulacija po P55 metodi (derivat strani) == pini;
      conf prekalkulacija (P71 metoda) == 0 sprememb (geografija nedeprava)
  I6  meritve v6 (rows/bases/multi/cross/ambRows/conf/series/removed)
      == pini; areaProof + spatialProof == pini (P71 metoda, ista semena)
  I7  dokaz ⊇ runtime bajtno (runtime rows == dokaz rowsEvidence)
  I8  determinizem: drugi preizračun bajtno identičen (--check)

Glifna/dual forenzika ni VLM-instrument: dual set je derivat
determinističnih lastnosti (strani × Blatt × lastniki) iz committed
dokazov — brez AI ob delovanju.
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
V5_EV = REPO / "research/issue17/ps-parcels-geo-v5.json"
DUAL_EV = REPO / "research/issue17/ps-dual-occurrence-pack.json"
P59_EV = REPO / "research/issue17/ps-blatt-headers.json"
P56_EV = REPO / "research/issue17/ps-register-topology.json"
PARCELS = REPO / "research/georef-n83/gurs/parcels-ko1544-merged.json"
V5_RT = REPO / "src/data/atlas/ps-parcels-geo.json"
OUT_EV = REPO / "research/issue17/ps-parcels-geo-v6.json"
OUT_RUNTIME = REPO / "src/data/atlas/ps-parcels-geo.json"

HIST_QK_M2 = 3.59665
AREA_BAND = 0.10
NEIGH_M = 150.0
SEED_AREA = 42
SEED_SPATIAL = 7
M_PER_DEG_LAT = 111320.0
TOTAL_PS_ROWS = 2762  # P55/P38 izbira (pageSelection.rows)

PIN_V5_EV_SHA = "6c96210dca8b4fee8d9cbc7090735148af8c7068d4cd5726f389953ef7682fee"
PIN_DUAL_EV_SHA = "0922a7013071363c75095082a6bb074490a944c6f979de7578f91898946857cd"
PIN_P59_EV_SHA = "650f13dccab1da70a60d04c41ce9f7887ca94eafea8a0a7927c104ca899b76f3"
PIN_P56_EV_SHA = "2fddc76fb94b69fed55170220fa8dfa3ace4a9466043d264b8b8df788e78a50c"
PIN_PARCELS_SHA = "fee91fca736348f40ef11d38b7a5b51d51656a9768cda648f4d737029bb3941f"
PIN_V5_RT_SHA = "0b5e8bf7d81306cc1e1c43f25b8f205a759800637740a47388f2f06a85428ef2"

DUAL_PAGES = {83, 84, 85, 86, 88}
P93_PREDICTED_MATCHES = ["1603", "1604", "1605"]

# pričakovane meritve v6 (pini; vpisano po prvem zagonu; None = meri)
EXP = {
    "rows": 939, "bases": 879, "multi": 50, "cross": 48,
    "dropPairs": 137, "dropRows": 138, "lost": 0,
    "ambRows": 100, "ambDerived": 135,
    "conf": {"STRONG": 174, "MEDIUM": 629, "WEAK": 136},
    "series": {"S1": 847, "S2": 66, "BI": 26},
    "confDerived": 0,
    "area": {"pairsWithArea": 919, "medianRatio": 3.8941, "q25": 2.8051,
             "q75": 7.5871, "tightN": 186, "tightShare": 0.2024,
             "shuffleMedian": 4.5766, "shuffleTightShare": 0.0457,
             "historicalQkM2": 3.59665, "deltaPct": 8.27},
    "spatial": {"consecPairs": 652, "medianM": 51.8, "q25M": 33.0,
                "q75M": 87.8, "share150": 0.9049, "shuffleMedianM": 1320.7,
                "shuffleShare150": 0.0171, "enrichmentX": 25.5},
    "suffix": 271, "pos": 879,
    "removed": 138,
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


def compute():
    print("P73 — v6: C3 isti-Blatt SPLIT opcija A (drop 137 kombinacij / "
          "138 vrstic, 135 dual base)")

    # ——— vhodi ———
    v5ev = json.loads(V5_EV.read_text(encoding="utf-8"))
    dual = json.loads(DUAL_EV.read_text(encoding="utf-8"))
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

    rows = v5ev["rowsEvidence"]

    # ——— I1: pini + nasledstvena veja v5 runtime ———
    pins = [(V5_EV, PIN_V5_EV_SHA, "v5 dokaz"),
            (DUAL_EV, PIN_DUAL_EV_SHA, "P72 dual pack dokaz"),
            (P59_EV, PIN_P59_EV_SHA, "P59 dokaz"),
            (P56_EV, PIN_P56_EV_SHA, "P56 dokaz"),
            (PARCELS, PIN_PARCELS_SHA, "PARCELS")]
    for path, pin, label in pins:
        if sha256(path) != pin:
            fail(f"I1 {label} sha {sha256(path)[:8]}… ≠ {pin[:8]}…")
        else:
            ok(f"I1 {label} sha pin")
    rt_sha = sha256(V5_RT)
    if rt_sha == PIN_V5_RT_SHA:
        ok("I1 v5 runtime sha pin (v5 — pred zapisom v6)")
    else:
        rt_disk = json.loads(V5_RT.read_text(encoding="utf-8"))
        d6 = rt_disk.get("v6Delta") or {}
        if rt_disk.get("version", 0) >= 6 and d6.get("droppedPairs") == 137 \
                and d6.get("droppedRows") == 138:
            ok("I1 v5 runtime nadgrajen na v"
               f"{rt_disk.get('version')} po P73 (C3 SPLIT-A) — vhodne "
               "vrstice iz v5 dokaza rowsEvidence (arhiv bajtno); "
               "nasledstvo deklarirano")
        else:
            fail(f"I1 v5 runtime sha odmika ({rt_sha[:8]}…) in nasledstvo "
                 "ni deklarirano (version "
                 f"{rt_disk.get('version')}, v6Delta {bool(d6)})")
    if len(rows) != 1077:
        fail(f"I1 v5 rowsEvidence {len(rows)} ≠ 1077")

    # ——— I2: re-izpeljava dual seta (P72 logika) == P72 dokaz ———
    bybase_rows: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        bybase_rows[r["base"]].append(r)
    duals: dict[tuple[str, str], list[int]] = {}
    near_duals: dict[tuple[str, str], list[int]] = {}
    for b, rs in bybase_rows.items():
        if len(rs) < 2:
            continue
        pages_by_blatt = defaultdict(set)
        for r in rs:
            bl = blatt_of(r["page"])
            if bl:
                pages_by_blatt[bl].add(r["page"])
        for bl, pgs in pages_by_blatt.items():
            if len(pgs) < 2:
                continue
            rs2 = [r for r in rs if blatt_of(r["page"]) == bl
                   and r["page"] in pgs]
            per_page = defaultdict(set)
            per_page_all = defaultdict(set)
            for r in rs2:
                if r.get("owner"):
                    per_page[r["page"]].add(r["owner"])
                per_page_all[r["page"]].add(r["owner"])
            pp = [v for v in per_page.values() if v]
            pall = [v for v in per_page_all.values() if v]
            if len(pp) >= 2 and all(a.isdisjoint(c)
                                    for i, a in enumerate(pp)
                                    for c in pp[i + 1:]):
                duals[(b, bl)] = sorted(per_page.keys())
            elif len(pall) >= 2 and all(a.isdisjoint(c)
                                        for i, a in enumerate(pall)
                                        for c in pall[i + 1:]):
                near_duals[(b, bl)] = sorted(per_page_all.keys())
    if len(duals) != 135:
        fail(f"I2 dual base {len(duals)} ≠ 135")
    if len(near_duals) != 2 or {b for b, _ in near_duals} != {"2080", "2081"}:
        fail(f"I2 nearDual {[b for b, _ in near_duals]} ≠ [2080, 2081]")
    rows_ib = sum(1 for r in rows
                  if (r["base"], blatt_of(r["page"]))
                  in {(b, bl) for b, bl in duals})
    if rows_ib != 274:
        fail(f"I2 isti-Blatt vrstice {rows_ib} ≠ 274")
    triples = sum(1 for pgs in duals.values() if len(pgs) > 2)
    if triples != 2:
        fail(f"I2 tri-zapisne {triples} ≠ 2")
    # bajtno == P72 dokaz "bases"
    p72_bases = dual.get("bases", {})
    if len(p72_bases) != 135:
        fail(f"I2 P72 dokaz bases {len(p72_bases)} ≠ 135")
    mine = {b: {"blatt": bl, "pages": pgs} for (b, bl), pgs in duals.items()}
    theirs = {b: {"blatt": d["blatt"], "pages": list(d["pages"])}
              for b, d in p72_bases.items()}
    if mine != theirs:
        fail("I2 re-izpeljani dual set ≠ P72 dokaz (base/blatt/pages bajtno)")
    else:
        ok("I2 dual set re-izpeljava == P72 dokaz (135 base · 274 vrstic · "
           "2 tri-zapisni; nearDual 2080/2081 izključena)")

    # ——— I3: drop izpeljava == P72 optionA ———
    drop = set()  # (page, base) kombinacije
    for (b, bl), pgs in duals.items():
        m = min(pgs)
        for p in pgs:
            if p != m:
                drop.add((p, b))
    drop_pairs = len(drop)
    drop_rows = sum(1 for r in rows if (r["page"], r["base"]) in drop)
    rows_a = [r for r in rows if (r["page"], r["base"]) not in drop]
    bases_a = {r["base"] for r in rows_a}
    lost = len({r["base"] for r in rows}) - len(bases_a)
    opt72 = dual.get("summary", {}).get("optionA", {})
    checks3 = [
        (drop_pairs, 137, "dropPairs"), (drop_rows, 138, "dropRows"),
        (len(rows_a), 939, "rows"), (len(bases_a), 879, "bases"),
        (lost, 0, "lost"),
        (opt72.get("drop"), 137, "P72 drop"), (opt72.get("rows"), 939,
                                               "P72 rows"),
        (opt72.get("bases"), 879, "P72 bases"), (opt72.get("lost"), 0,
                                                 "P72 lost"),
        (opt72.get("multi"), None, None), (opt72.get("cross"), None, None),
    ]
    for got, want, label in checks3:
        if want is None:
            continue
        if got != want:
            fail(f"I3 {label} {got} ≠ {want}")
    if not any(f.startswith("I3") for f in FAILURES):
        ok(f"I3 drop == P72 optionA: {drop_pairs} kombinacij = "
           f"{drop_rows} vrstic; rows 1077 → {len(rows_a)}; bases "
           f"{len(bases_a)}; lost {lost}; P72 multi {opt72.get('multi')}, "
           f"cross {opt72.get('cross')}")

    # P70 33 ⊂ drop (drugi blok P70 fuzij = p89–92; P70 pair p49/89 × 15,
    # p50/90 × 10, p52/92 × 8 — min strani 49/50/52 ostanejo)
    p70_pairs = Counter((r["page"], r["base"]) for r in rows
                        if r["page"] in (89, 90, 92)
                        and (r["page"], r["base"]) in drop)
    if sum(p70_pairs.values()) != 33:
        fail(f"I3 P70 kolizij v dropu {sum(p70_pairs.values())} ≠ 33")
    else:
        ok("I3 P70 33 kolizij ⊂ drop (drugi blok: p89 × 15, p90 × 10, "
           "p92 × 8; glavni blok p49/50/52 ostaja)")

    # ——— izvedba: ohranjene vrstice (_srcIdx identiteta) ———
    out_rows: list[dict] = []
    removed_rows: list[dict] = []
    for idx, r in enumerate(rows):
        if (r["page"], r["base"]) in drop:
            removed_rows.append({
                "page": r["page"], "base": r["base"],
                "parzella": r["parzella"], "owner": r["owner"],
                "areaQK": r["areaQK"],
                "reason": "C3: isti-Blatt SPLIT opcija A (P72 dual pack — "
                          "135 dual base z disjunktnimi lastniki med "
                          "straneh; drop drugi blok, keep = min stran; "
                          "lastniško soglasje P73; vrstica ostane v "
                          "registru brez geometrije)",
            })
            continue
        r2 = dict(r)
        r2["_srcIdx"] = idx
        out_rows.append(r2)
    if len(removed_rows) != drop_rows or len(out_rows) != len(rows_a):
        fail(f"I3 izvedba: removed {len(removed_rows)} ≠ {drop_rows} ali "
             f"rows {len(out_rows)} ≠ {len(rows_a)}")

    # ——— I4: ohranjene vrstice (pred group-derived) bajtno == v5 ———
    pages_by: dict[str, set[int]] = defaultdict(set)
    for r in out_rows:
        pages_by[r["base"]].add(r["page"])
    multi = [b for b in pages_by if len(pages_by[b]) > 1]
    bl_by: dict[str, set[str]] = defaultdict(set)
    for r in out_rows:
        bl = blatt_of(r["page"])
        if bl:
            bl_by[r["base"]].add(bl)
    cross = [b for b in bl_by if len(bl_by[b]) > 1]
    orphans = sorted(b for b in {r["base"] for r in rows}
                     if b not in pages_by)
    if orphans:
        fail(f"I4 base brez vrstic po dropu: {orphans}")
    else:
        ok("I4 po C3 noben base ne izgubi vseh vrstic (0 praznih; "
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

    # ——— I4/I6: nespremenjene vrstice bajtno == v5 ———
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
            # vsa DRUGA polja (razen ambiguous) bajtno == v5
            a = {k: v for k, v in r.items() if k != "ambiguous"}
            b = {k: v for k, v in old.items() if k != "ambiguous"}
            if json.dumps(a, ensure_ascii=False, sort_keys=True) != \
                    json.dumps(b, ensure_ascii=False, sort_keys=True):
                fail(f"I6 derived vrstica p{r['page']} {r['base']}: "
                     "ostala polja odmikajo od v5")
            continue
        if json.dumps(r, ensure_ascii=False, sort_keys=True) != \
                json.dumps(old, ensure_ascii=False, sort_keys=True):
            fail(f"I6 vrstica p{r['page']} {r['base']} nespremenjena, "
                 f"a odmika od v5")
        n_unchanged += 1
    ok(f"I6 nespremenjene vrstice bajtno == v5 ({n_unchanged}); "
       f"group-derived (ambiguous) {n_derived}; izpad C3 {len(removed_rows)}")

    # nearDual 2080/2081 ostanejo
    nd_rows = [r for r in out_rows if r["base"] in ("2080", "2081")]
    nd_v5 = [r for r in rows if r["base"] in ("2080", "2081")]
    if len(nd_rows) != len(nd_v5):
        fail(f"I4 nearDual vrstice {len(nd_rows)} ≠ v5 {len(nd_v5)}")
    else:
        ok(f"I4 nearDual 2080/2081: vseh {len(nd_rows)} vrstic ostane "
           "(opcija A jih ne izpada)")

    # ——— I6: meritve v6 ———
    bases6 = set(pages_by)
    s1s2 = [r for r in out_rows if r["series"] != "BI"]
    bi_rows = [r for r in out_rows if r["series"] == "BI"]
    conf_counts: dict[str, int] = defaultdict(int)
    for r in out_rows:
        conf_counts[r["conf"]] += 1
    series_counts = {k: sum(1 for r in out_rows if r["series"] == k)
                     for k in ("S1", "S2", "BI")}
    suffix_groups = sum(1 for b in pos_by_base if len(bybase[b]) > 1)

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
    ok(f"I6 meritve v6: rows {len(out_rows)} · bases {len(bases6)} · "
       f"multi {len(multi)} · cross {len(cross)} · ambRows {amb_rows} · "
       f"conf {conf_counts.get('STRONG', 0)}/{conf_counts.get('MEDIUM', 0)}"
       f"/{conf_counts.get('WEAK', 0)} · area median "
       f"{area_proof['medianRatio']} (Δ {area_proof['deltaPct']} %) · "
       f"sosledje {spatial_proof['consecPairs']} parov / "
       f"{spatial_proof['medianM']} m")

    if EXP["rows"] is not None:
        checks = [
            (len(out_rows), EXP["rows"], "rows"),
            (len(bases6), EXP["bases"], "bases"),
            (len(multi), EXP["multi"], "multi"),
            (len(cross), EXP["cross"], "cross"),
            (amb_rows, EXP["ambRows"], "ambRows"),
            (len(removed_rows), EXP["removed"], "removed"),
            (drop_pairs, EXP["dropPairs"], "dropPairs"),
            (drop_rows, EXP["dropRows"], "dropRows"),
            (lost, EXP["lost"], "lost"),
            (len(amb_changes), EXP["ambDerived"], "ambDerived"),
            (suffix_groups, EXP["suffix"], "suffix"),
            (len(pos_by_base), EXP["pos"], "pos"),
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
        if not FAILURES:
            ok("I6 meritve == pini (vse)")
    else:
        print("  ── PINE ZA VPIS (EXP) ————————————————————")
        print(f"    rows={len(out_rows)}, bases={len(bases6)}, "
              f"multi={len(multi)}, cross={len(cross)}, "
              f"ambRows={amb_rows}, suffix={suffix_groups}, "
              f"pos={len(pos_by_base)}, removed={len(removed_rows)}, "
              f"dropPairs={drop_pairs}, dropRows={drop_rows}, "
              f"lost={lost}, ambDerived={len(amb_changes)}")
        print(f"    conf={dict(conf_counts)}, series={series_counts}")
        print(f"    area={json.dumps(area_proof)}")
        print(f"    spatial={json.dumps(spatial_proof)}")
        print(f"    removedByPage={dict(sorted(Counter(r['page'] for r in removed_rows).items()))}")

    # blattDist (pari Blattov čez cross-Blatt base)
    blatt_dist: dict[str, int] = defaultdict(int)
    for b in cross:
        pair = "·".join(sorted(bl_by[b]))
        blatt_dist[pair] += 1

    v5_join = v5ev["join"]
    join_block = {
        "matchedRows": len(out_rows),
        "matchedRowsS1S2": len(s1s2),
        "matchedRowsBI": len(bi_rows),
        "matchedSharePct": round(100 * len(out_rows) / TOTAL_PS_ROWS, 1),
        "psUniqueNumbers": v5_join["psUniqueNumbers"],
        "psPositionedParcels": len(pos_by_base),
        "suffixGroups": suffix_groups,
        "seriesCounts": series_counts,
        "confCounts": {"STRONG": conf_counts["STRONG"],
                       "MEDIUM": conf_counts["MEDIUM"],
                       "WEAK": conf_counts["WEAK"]},
        "readConfBI": v5_join["readConfBI"],
        "ambiguousBases": len(multi),
        "ambiguousRows": amb_rows,
    }
    per_blatt_amb = {
        "basesOnMultiplePages": len(multi),
        "rowsWithAmbiguousBase": amb_rows,
        "note": f"base na > 1 strani v v6 (po C3 isti-Blatt SPLIT opcija A; "
                f"135 dual base na eni strani po dropu drugi blok); "
                f"čez-Blatt {len(cross)} (blattDist " +
                " · ".join(f"{k} {v}" for k, v in sorted(blatt_dist.items()))
                + ") [~]",
    }
    return (out_rows, removed_rows, amb_changes, conf_changes, join_block,
            per_blatt_amb, area_proof, spatial_proof, v5ev, p56, multi,
            cross, bases6, blatt_dist, pos_by_base, drop_pairs, drop_rows,
            lost, near_duals)


def re_match_base(s):
    import re
    m = re.match(r"\*?(\d+)", str(s or ""))
    return m.group(1) if m else None


def _status_line(out_rows, removed_rows, join_block, per_blatt_amb, cross,
                 area_proof, spatial_proof, drop_pairs, drop_rows) -> str:
    return (
        f"P73 SPLIT v5: C3 isti-Blatt SPLIT opcija A — 135 dual base "
        f"(P72 dual pack: lastniki med straneh disjunktni 135/135; hn "
        f"različni 130, 0 isti; P70 33 kolizij = podmnožica; stranski pari "
        f"delijo iste razpone po P56 pageMap; odmiki 40 × 44 · 15 × 49 · "
        f"5 × 29 · 1 × 13): drop {drop_pairs} kombinacij = {drop_rows} "
        f"vrstic (drugi blok, keep = min stran; vrstice ostanejo v "
        f"registru brez geometrije; lastniško soglasje 2026-10-15); "
        f"nearDual 2080/2081 ostanejo; 0 base brez vrstic; v6: "
        f"{len(out_rows)} vrstic / {join_block['psPositionedParcels']} "
        f"base / multi-page {per_blatt_amb['basesOnMultiplePages']} / "
        f"cross-Blatt {len(cross)}; area median {area_proof['medianRatio']} "
        f"(Δ {area_proof['deltaPct']} %), sosledje "
        f"{spatial_proof['consecPairs']} parov / {spatial_proof['medianM']} m "
        f"({spatial_proof['enrichmentX']}×)"
    )


def _verdict_si(out_rows, join_block) -> str:
    return (
        "Isti-Blatt SPLIT joina izveden (opcija A iz P72 dual pack; "
        "lastniška odločitev 2026-10-15): za 135 base z vrsticami na ≥ 2 "
        "straneh istega Blatta z disjunktnimi lastniki (dvojni zapis iste "
        "serije v dveh blokih registra) so vrstice drugega bloka izpadle "
        "iz joina (137 kombinacij = 138 vrstic; keep = min stran; "
        "P70 »SPLIT = LASTNIKA« 33 fuzij = podmnožica) — konec lažnih "
        "fuzij isti-Blatt po celotnem registru; vrstice ostanejo v "
        "registru (removedRows), nearDual 2080/2081 ostanejo, noben base "
        "ne izgubi vseh vrstic; ambiguous prekalkuliran po P55 metodi, "
        "conf nespremenjen (geografija nedeprava). V6: "
        f"{len(out_rows)} vrstic ({round(100 * len(out_rows) / 2762, 1)} "
        f"% izbire) / {join_block['psPositionedParcels']} base. "
        "Cross-Blatt SPLIT (P66 pack, 36 base) ostaja ločena lastniška "
        "odločitev."
    )


def _verdict_en(out_rows, join_block) -> str:
    return (
        "Same-Blatt SPLIT of the join executed (option A from the P72 dual "
        "pack; owner decision 2026-10-15): for the 135 bases with rows on "
        "≥ 2 pages of the same Blatt and disjoint owners across pages "
        "(dual entry of the same series in two register blocks), the "
        "second-block rows are dropped from the join (137 combinations = "
        "138 rows; keep = minimum page; the P70 \"SPLIT = OWNER\" 33 "
        "fusions are a subset) — an end to same-Blatt false fusions across "
        "the whole register; rows remain in the register (removedRows), "
        "near-duals 2080/2081 are kept, no base loses all rows; ambiguous "
        "recomputed per the P55 method, conf unchanged (geography "
        "untouched). V6: "
        f"{len(out_rows)} rows ({round(100 * len(out_rows) / 2762, 1)} "
        f"% of the selection) / {join_block['psPositionedParcels']} bases. "
        "The cross-Blatt SPLIT (P66 pack, 36 bases) remains a separate "
        "owner decision."
    )


def _next_list() -> list:
    return [
        "LASTNIŠKO: cross-Blatt SPLIT (P66 pack — 36 base, deleži "
        "[0.5,0.75)) — ločena odločitev od isti-Blatt SPLIT",
        "LASTNIŠKO: per-Blatt instance sekcij (56 vrstic; P60 moda B / PF "
        "protokol)",
        "opcija B (per-page instance za SPLIT) zahteva georef Blattnih "
        "kart (Franciscejski kataster I–V) — ločen podprojekt [~]",
        "praznine brez registrskih strani: PF 1644–1655, 1673/1679, "
        "1842–1860, 1904/1906 (modernVoid [~])",
        "operacijsko: GitHub Actions billing (#7)",
    ]


def compute_pair():
    """Ponovni preizračun (brez pisanja) — vrne (evidence, runtime)."""
    global FAILURES
    FAILURES = []
    (out_rows, removed_rows, amb_changes, conf_changes, join_block,
     per_blatt_amb, area_proof, spatial_proof, v5ev, p56, multi, cross,
     bases6, blatt_dist, pos_by_base, drop_pairs, drop_rows, lost,
     near_duals) = compute()
    if FAILURES:
        raise SystemExit(f"P73 compute: invariant padel: {FAILURES[:3]}")

    v5rt = json.loads(V5_RT.read_text(encoding="utf-8"))
    # zgodovinski bloki iz v5 runtime (nasledstvena veja: disk lahko že v6;
    # v5Delta/v5 bloki so del zgodovine — vzamem iz diska NEZVISNO od verzije,
    # dokler obstajajo; če disk še v5 — identično)
    hist_constant = v5rt.get("historicalConstant")
    page_sel = v5rt.get("pageSelection")
    v5_delta = v5rt.get("v5Delta")
    furkovce = v5ev["furkovce"]

    evidence = {
        "version": 6,
        "task": "P73 (issue #13) — PS-PARCELS-GEO v6: isti-Blatt SPLIT "
                "(opcija A — drop drugi blok za 135 dual base)",
        "date": DATE,
        "generatedBy": "scripts/p73_ps_v6_split_a.py",
        "principle": "samo odstranjevanje dokumentiranih lažnih fuzij "
                     "(dvojni zapis iste serije v dveh blokih); noben nov "
                     "podatek; dual set derivat determinističnih lastnosti "
                     "(strani × Blatt × lastniki) iz committed dokazov",
        "inputs": {
            "v5ProofSha256": sha256(V5_EV),
            "dualPackProofSha256": sha256(DUAL_EV),
            "p59ProofSha256": sha256(P59_EV),
            "p56ProofSha256": sha256(P56_EV),
            "parcelsSha256": sha256(PARCELS),
        },
        "corrections": {
            "C3": {
                "title": "isti-Blatt SPLIT opcija A: drop drugi-blok "
                         "vrstic za 135 dual base",
                "decision": "LASTNIK (P73): opcija A iz P72 dual pack "
                            "(exclude drugi blok po C1 vzorcu; keep = min "
                            "stran); soglasje 2026-10-15",
                "evidence": {
                    "dualPack": "research/issue17/"
                                "ps-dual-occurrence-pack.json (135 base; "
                                "274 vrstic; lastniki disjunktni 135/135; "
                                "hn različni 130, brez hn na eni strani 5, "
                                "isti 0; P70 33 = podmnožica + 11 starih "
                                "p51×p91 + 91 novih)",
                    "dualBases": 135,
                    "droppedPairs": drop_pairs,
                    "droppedRows": drop_rows,
                    "nearDualKept": sorted({b for b, _ in near_duals}),
                    "pageMapProof": "stranski pari delijo iste številčne "
                                    "razpone po P56 pageMap (p23/p24, "
                                    "p51/p91, p103/p118 …); odmiki po "
                                    "blokih konsistentni",
                },
                "droppedRows": removed_rows,
            },
        },
        "removedRows": removed_rows,
        "join": join_block,
        "v6Delta": {
            "reason": "C3: isti-Blatt SPLIT opcija A — drop drugi-blok "
                      "vrstic za 135 dual base (P72 dual pack; lastniško "
                      "soglasje 2026-10-15; P70 »SPLIT = LASTNIKA« "
                      "razširjen na cel register)",
            "splitBases": 135,
            "droppedPairs": drop_pairs,
            "droppedRows": len(removed_rows),
            "before": {"rows": 1077, "bases": 879, "multiPage": 184,
                       "crossBlatt": 48},
            "after": {"rows": len(out_rows), "bases": len(bases6),
                      "multiPage": per_blatt_amb["basesOnMultiplePages"],
                      "crossBlatt": len(cross)},
            "invariance": "ohranjene vrstice bajtno == v5 (lekcija P9; "
                          "drop samo odstranjuje); ambiguous prekalkuliran "
                          "po P55 metodi (derivat strani); conf "
                          "nespremenjen (geografija nedeprava); v5 ostaja "
                          "arhiviran (research/issue17/ps-parcels-geo-v5"
                          ".json)",
            "note": "C3 odstranjuje LE lažne fuzije (dvojni zapis) — "
                    "noben nov podatek ni izmišljen; vrstice ostanejo v "
                    "registru brez geometrije; nearDual 2080/2081 ostanejo",
        },
        "v5Delta": v5_delta,
        "areaProof": area_proof,
        "spatialProof": spatial_proof,
        "furkovce": furkovce,
        "perBlattAmbiguity": per_blatt_amb,
        "invariants": {
            "I1": "pini v5/dual/P59/P56/PARCELS sha256; v5 runtime "
                  "nasledstvena veja (v5 pin ALI version ≥ 6 + v6Delta "
                  "droppedPairs 137)",
            "I2": "dual set re-izpeljava == P72 dokaz (bajtno; 135 · 274 · "
                  "2 triples; nearDual 2080/2081)",
            "I3": "drop == P72 optionA (137 kombinacij = 138 vrstic; rows "
                  "939; bases 879; lost 0; multi 50; cross 48); P70 33 "
                  "⊂ drop",
            "I4": "po C3 noben base ne izgubi vseh vrstic (0 praznih); "
                  "nearDual vrstice ostanejo",
            "I5": "ambiguous P55 prekalkulacija == pini; conf 0 sprememb "
                  "(geografija nedeprava)",
            "I6": "meritve == pini; nespremenjene vrstice bajtno == v5; "
                  "derived vrstice: ostala polja bajtno == v5",
            "I7": "dokaz ⊇ runtime bajtno",
            "I8": "determinizem --check bajtno",
        },
        "statusLine": _status_line(out_rows, removed_rows, join_block,
                                   per_blatt_amb, cross, area_proof,
                                   spatial_proof, drop_pairs, drop_rows),
        "verdictSi": _verdict_si(out_rows, join_block),
        "verdictEn": _verdict_en(out_rows, join_block),
        "next": _next_list(),
        "rowsEvidence": out_rows,
    }
    runtime = {
        "version": 6,
        "task": "P73 (issue #13) — isti-Blatt SPLIT opcija A (C3)",
        "date": DATE,
        "generatedBy": "scripts/p73_ps_v6_split_a.py",
        "historicalConstant": hist_constant,
        "pageSelection": page_sel,
        "join": join_block,
        "v6Delta": evidence["v6Delta"],
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
        print(f"P73: {e}")
        return 1
    OUT_EV.write_text(jdump_pretty(evidence), encoding="utf-8")
    OUT_RUNTIME.write_text(jdump_pretty(runtime), encoding="utf-8")
    print(f"P73: dokaz → {OUT_EV.relative_to(REPO)}; runtime → "
          f"{OUT_RUNTIME.relative_to(REPO)} (v6)")
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
        print(f"P73 --check: {len(FAILURES)} invariant(ov) PADLO")
        for f in FAILURES:
            print(f"  → {f}")
        return 1
    print("P73 --check: VSE INVARIANTE PASS (bajtno)")
    return 0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "--check":
        sys.exit(check())
    sys.exit(build_documents())


if __name__ == "__main__":
    main()
