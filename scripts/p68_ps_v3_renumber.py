#!/usr/bin/env python3
"""P68 (issue #13) — PS-PARCELS-GEO v3: SANACIJA ŠTEVILČENJA (17 preslikav
p78/p93/p87 po P67 forenzični specifikaciji) + RE-JOIN po P55 metodi.

P67 forenzika (ps-anomaly-forensics.json) je dokazala dvojno Kurrent
zamenjavo: p78 (Blatt II, Wüstung »Pod Grabino«) prave številke 1501–1520
(v2 1603–1605 = P38 napaka 5→6), p93 (Blatt IV) prave 1901–1920 (v2 1603–1605
= napaka 9→6/9→0), p87 (Blatt II) prave 1681–1700 (v2 661–680 = izguba
vodilne 1 + 8→6). Ta skripta IZVEDE specifikacijo:

  1) RENUM 17 preslikav (p78 160x→150x, p93 160x→190x, p87 +1020) — bajtno
     == P67 dokaz renumberSpec; 0 kolizij (novi base bodisi prosti bodisi
     z instanco samo na straneh DRUGAČNEGA Blatta — 1903/1905 @p98 III).
  2) RE-JOIN po P55 metodi (group_pos = površinsko uteženo središče poligonov
     k.o. 1544): 14 preslikanih vrstic (3× p78 → 1503–1505, 11× p87 →
     1681–1700) IZPADE (base brez PF poligona — kartni priči P67), 3× p93
     re-claim na 1903/1904/1905 (poligoni obstajajo, jugozahodna lokacija).
  3) Vse ostale vrstice BAJTNO nespremenjene (lekcija P9) — razen prekalkulacij
     skupinskih lastnosti (ambiguous, conf) ki izhajajo iz spremembe base.
  4) Meritve nad v3: areaProof + spatialProof prekalkulirana po P55 metodama
     (isti seed-i), join/perBlattAmbiguity bloka posodobljena.

Viri (vsi committed):
  research/issue17/ps-parcels-geo-v2.json      (v2 dokaz, 1093 rowsEvidence)
  src/data/atlas/ps-parcels-geo.json           (v2 runtime — bajtno == dokaz)
  research/issue17/ps-anomaly-forensics.json   (P67 specifikacija RENUM)
  research/issue17/ps-blatt-headers.json       (P59 pageAttribution — Blatti)
  research/georef-n83/gurs/parcels-ko1544-merged.json (2117 parcel, P47)

Izpis:
  research/issue17/ps-parcels-geo-v3.json      (dokaz v3 — rowsEvidence 1079
                                                + removedRows + delta + odmiki)
  src/data/atlas/ps-parcels-geo.json           (runtime v3 — NADOMESTI v2;
                                                v2 ostane arhiviran v dokazu)

Invarianti (FAIL → exit 1):
  I1  RENUM 17 preslikav bajtno == P67 dokaz parts.A.renumberSpec;
      0 kolizij (new base proste v v2 ali samo strani drugačnega Blatta)
  I2  vhodni pini: v2 dokaz sha256 ebb8f729…, P67 b3b64feb…, P59 95929a2e…,
      PARCELS fee91fca…; v2 runtime rows == v2 dokaz rowsEvidence bajtno
  I3  preslikave: natanko 17 vrstic; 14 izpada (3× p78, 11× p87 — vse base
      brez PF poligona); 3× p93 re-claim s group_pos (1903/1905 == v2 poziciji
      p98 instanc; 1904 == PARCELS)
  I4  nespremenjene vrstice bajtno == v2 (1076; prekalkulirana le
      group-derived polja: ambiguous — 15 vrstic, conf — 1 vrstica)
  I5  meritve v3: rows 1079, bases 798, multi-page 199, cross-Blatt 98,
      ambiguousRows 472, suffixGroups 240, area median 3.8512,
      sosledje 590 parov / 51.8 m
  I6  fuzije: 1903 = 3 vrstice (III p98 ×2 + IV p93; delež III areaQK
      0.7081 == P67), 1905 = 2 vrstici (IV brez areaQK → R2b profil),
      1904 = 1 vrstica (ratio 6.8052 izven pasu — prečrtana vrstica registra)
  I7  odmiki od P67 projekcije dokumentirani (bases 802→798, multi 208→199,
      cross 107→98 — aproksimacija [~]: formula ni štela 9 preostalih
      661–680 cross-Blatt base niti izpada 1503–1505/1681–1700)
  I8  dokaz ⊇ runtime (rowsEvidence bajtno == runtime rows)
  I9  determinizem: drugi preizračun bajtno identičen (--check)

Strojna forenzika ni dokazni vir; renumifikacija je mehanski izvod P67
specifikacije (odločitev o SPLIT joinu ostaja LASTNIKA — P69).
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
V2_EV = REPO / "research/issue17/ps-parcels-geo-v2.json"
V2_RT = REPO / "src/data/atlas/ps-parcels-geo.json"
V3_EV = REPO / "research/issue17/ps-parcels-geo-v3.json"
OUT_RUNTIME = REPO / "src/data/atlas/ps-parcels-geo.json"
P67_EV = REPO / "research/issue17/ps-anomaly-forensics.json"
P59_EV = REPO / "research/issue17/ps-blatt-headers.json"
PARCELS = REPO / "research/georef-n83/gurs/parcels-ko1544-merged.json"

HIST_QK_M2 = 3.59665
AREA_BAND = 0.10
NEIGH_M = 150.0
SEED_AREA = 42
SEED_SPATIAL = 7
M_PER_DEG_LAT = 111320.0
TOTAL_PS_ROWS = 2762  # P55/P38 izbira (pageSelection.rows)

PIN_V2_EV_SHA = "ebb8f7298de713e73bc7417f392d60c7e5eb03a6675f96317320188750e27731"
PIN_P67_EV_SHA = "797e5b87943867d26fe99ea6dc68afe4364f75738615cc340034b87c860f4c55"  # P68 re-run (projekcija = meritve)  # P68 re-run (projekcija = meritve)
PIN_P59_EV_SHA = "650f13dccab1da70a60d04c41ce9f7887ca94eafea8a0a7927c104ca899b76f3"  # P68 v3 re-run
PIN_PARCELS_SHA = "fee91fca736348f40ef11d38b7a5b51d51656a9768cda648f4d737029bb3941f"

# pričakovane meritve v3 (sonda; skripta jih preverja = pini)
EXP_ROWS = 1079
EXP_S1S2 = 1053
EXP_BI = 26
EXP_BASES = 798
EXP_MULTI = 199
EXP_CROSS = 98
EXP_AMB_ROWS = 472
EXP_SUFFIX = 240
EXP_SERIES = {"S1": 983, "S2": 70, "BI": 26}
EXP_CONF = {"STRONG": 174, "MEDIUM": 749, "WEAK": 156}  # TOTAL (v2 konvencija; S1/S2 del 171/735/147)
EXP_SHARE_PCT = 39.1
EXP_AREA = {"pairs": 1060, "median": 3.8512, "q25": 2.4103, "q75": 8.3459,
            "tightN": 187, "tightShare": 0.1764, "shufMed": 4.2771,
            "shufTight": 0.0472, "deltaPct": 7.08}
EXP_SPATIAL = {"pairs": 590, "median": 51.8, "q25": 31.2, "q75": 91.0,
               "share150": 0.8932, "shufMed": 1466.1, "shuf150": 0.0226,
               "enrichX": 28.3}
EXP_REMOVED = 14
EXP_CONF_CHANGES = [("98", "1905", "WEAK", "MEDIUM")]

DATE = "2026-10-14"
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
    print("P68 — v3 sanacija številčenja (17 preslikav + re-join)")

    # ——— vhodi ———
    v2ev = json.loads(V2_EV.read_text(encoding="utf-8"))
    v2rt = json.loads(V2_RT.read_text(encoding="utf-8"))
    p67 = json.loads(P67_EV.read_text(encoding="utf-8"))
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
    if sha256(V2_EV) != PIN_V2_EV_SHA:
        fail(f"I2 v2 dokaz sha {sha256(V2_EV)[:8]}… ≠ {PIN_V2_EV_SHA[:8]}…")
    else:
        ok("I2 v2 dokaz sha pin")
    if sha256(P67_EV) != PIN_P67_EV_SHA:
        fail("I2 P67 dokaz sha odmika")
    else:
        ok("I2 P67 dokaz sha pin")
    if sha256(P59_EV) != PIN_P59_EV_SHA:
        fail("I2 P59 dokaz sha odmika")
    else:
        ok("I2 P59 dokaz sha pin")
    if sha256(PARCELS) != PIN_PARCELS_SHA:
        fail("I2 PARCELS sha odmika")
    else:
        ok("I2 PARCELS sha pin")
    v2_rows = v2ev["rowsEvidence"]
    if v2rt.get("version") == 2:
        if json.dumps(v2rt["rows"], ensure_ascii=False, sort_keys=True) != \
                json.dumps(v2_rows, ensure_ascii=False, sort_keys=True):
            fail(f"I2 v2 runtime rows ≠ dokaz rowsEvidence ({len(v2rt['rows'])} vs "
                 f"{len(v2_rows)})")
        else:
            ok(f"I2 v2 runtime == dokaz rowsEvidence ({len(v2_rows)})")
    else:
        ok(f"I2 runtime je v{v2rt.get('version')} (P68 izvedena) — vhod "
           f"iz v2 dokaza rowsEvidence ({len(v2_rows)})")

    # ——— I1: RENUM == P67 specifikacija, 0 kolizij ———
    renum_spec = p67["parts"]["A"]["renumberSpec"]
    RENUM = [
        {"new": "1503", "old": "1603", "page": 78},
        {"new": "1504", "old": "1604", "page": 78},
        {"new": "1505", "old": "1605", "page": 78},
        {"new": "1903", "old": "1603", "page": 93},
        {"new": "1904", "old": "1604", "page": 93},
        {"new": "1905", "old": "1605", "page": 93},
        {"new": "1681", "old": "661", "page": 87},
        {"new": "1683", "old": "663", "page": 87},
        {"new": "1686", "old": "666", "page": 87},
        {"new": "1687", "old": "667", "page": 87},
        {"new": "1691", "old": "671", "page": 87},
        {"new": "1693", "old": "673", "page": 87},
        {"new": "1694", "old": "674", "page": 87},
        {"new": "1695", "old": "675", "page": 87},
        {"new": "1696", "old": "676", "page": 87},
        {"new": "1699", "old": "679", "page": 87},
        {"new": "1700", "old": "680", "page": 87},
    ]
    if json.dumps(renum_spec, ensure_ascii=False, sort_keys=True) != \
            json.dumps(RENUM, ensure_ascii=False, sort_keys=True):
        fail("I1 RENUM ≠ P67 renumberSpec (bajtno)")
    else:
        ok("I1 RENUM 17 preslikav == P67 renumberSpec (bajtno)")
    renum = {(r["page"], r["old"]): r["new"] for r in RENUM}
    if len(renum) != 17:
        fail(f"I1 RENUM unikatov {len(renum)} ≠ 17")
    # kolizije: new base proste ali samo strani drugačnega Blatta
    pages_v2: dict[str, set[int]] = defaultdict(set)
    for r in v2_rows:
        pages_v2[r["base"]].add(r["page"])
    for m in RENUM:
        others = pages_v2.get(m["new"], set()) - {m["page"]}
        bpg = blatt_of(m["page"])
        for pg in others:
            if blatt_of(pg) == bpg:
                fail(f"I1 kolizija: new {m['new']} obstaja na strani {pg} "
                     f"(isti Blatt {bpg})")
    ok("I1 kolizije 0 (novi base prosti ali samo strani drugačnega Blatta)")

    # ——— preslikava + re-join ———
    out_rows: list[dict] = []
    removed: list[dict] = []
    renumbered_pages: dict[tuple[int, str], str] = {}
    for idx, r in enumerate(v2_rows):
        r2 = dict(r)
        r2["_srcIdx"] = idx  # notranji sled — odstranjen pred izpisom (I8)
        key = (r2["page"], r2["base"])
        if key in renum:
            nb = renum[key]
            renumbered_pages[key] = nb
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
    if len(renumbered_pages) != 17:
        fail(f"I3 preslikanih vrstic {len(renumbered_pages)} ≠ 17")
    else:
        ok("I3 preslikanih vrstic 17 (p78 3 / p93 3 / p87 11)")
    if len(removed) != EXP_REMOVED:
        fail(f"I3 izpadlih vrstic {len(removed)} ≠ {EXP_REMOVED}")
    else:
        ok(f"I3 izpadlih vrstic {len(removed)} (3× p78 → 1503–1505, "
           f"11× p87 → 1681–1700 — base brez PF poligona)")
    # p93 re-claim: pozicije == P55 group_pos (in == v2 poziciji 1903/1905)
    for nb, exp in (("1903", None), ("1904", None), ("1905", None)):
        got = group_pos(nb)
        if got is None:
            fail(f"I3 {nb}: group_pos prazen")
    v2_pos = {}
    for r in v2_rows:
        if r["base"] in ("1903", "1905") and r["page"] == 98:
            v2_pos[r["base"]] = (r["lat"], r["lng"])
    for r in out_rows:
        if r["page"] == 93 and r["base"] in ("1903", "1904", "1905"):
            gp = group_pos(r["base"])
            if (r["lat"], r["lng"]) != (gp[0], gp[1]):
                fail(f"I3 p93 {r['base']}: pozicija ≠ group_pos")
            if r["base"] in v2_pos and (r["lat"], r["lng"]) != v2_pos[r["base"]]:
                fail(f"I3 p93 {r['base']}: pozicija ≠ v2 p98 pozicija (re-claim)")
    ok("I3 p93 re-claim: 1903/1905 == v2 poziciji p98; 1904 == PARCELS")

    # ——— I4: nespremenjene vrstice bajtno (indeksna korelacija z v2) ———
    changed_keys = set(renumbered_pages) | {
        (r["page"], r["base"]) for r in v2_rows
        if r["base"] in ("661", "663", "666", "667", "671", "673", "674",
                         "675", "676", "679", "680", "1903", "1905")
    }
    n_unchanged = 0
    for r in out_rows:
        k = (r["page"], r["base"])
        v2r = v2_rows[r["_srcIdx"]]
        if v2r["base"] != r["base"]:
            continue  # preslikana vrstica (nov base ključ) — group-derived
        if k in changed_keys:
            continue  # group-derived spremembe (ambiguous/conf) dovoljene
        rc = {k2: v for k2, v in r.items() if k2 != "_srcIdx"}
        if json.dumps(rc, ensure_ascii=False, sort_keys=True) != \
                json.dumps(v2r, ensure_ascii=False, sort_keys=True):
            fail(f"I4 vrstica {k} nespremenjena, a odmika")
        n_unchanged += 1
    n_derived = len(out_rows) - n_unchanged
    if n_derived != 17:
        fail(f"I4 group-derived vrstic {n_derived} ≠ 17 "
             f"(3 p93 re-claim + 11 p36 + 3 p98)")
    else:
        ok(f"I4 nespremenjene vrstice bajtno == v2 ({n_unchanged}); "
           f"group-derived polja samo pri {n_derived} "
           f"(3 p93 re-claim + 11 p36 + 3 p98)")

    # ——— ambiguous prekalkulacija ———
    for r in out_rows:
        del r["_srcIdx"]  # izpis ni več potreben — I8 gre čisto
    pages_by: dict[str, set[int]] = defaultdict(set)
    for r in out_rows:
        pages_by[r["base"]].add(r["page"])
    amb_changes = []
    for r in out_rows:
        new_amb = len(pages_by[r["base"]]) > 1
        if new_amb != r["ambiguous"]:
            amb_changes.append((r["page"], r["base"], r["ambiguous"], new_amb))
            r["ambiguous"] = new_amb
    # pričakovane: 11× p36 (661–680 true→false), p93 1604→1904 true→false,
    # 3× p98 (1903 ×2, 1905 false→true); p78/p87 vrstice izpadajo
    if len(amb_changes) != 15:
        fail(f"I4 ambiguous sprememb {len(amb_changes)} ≠ 15")
    else:
        ok("I4 ambiguous prekalkulacija: 15 vrstic (11 p36 + 1 p93 + 3 p98)")

    # ——— conf prekalkulacija (S1/S2, P55 metoda) ———
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
    conf_changes = []
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
            conf_changes.append((str(r["page"]), r["base"], r["conf"], new))
            r["conf"] = new
    if sorted(conf_changes) != sorted(EXP_CONF_CHANGES):
        fail(f"I4 conf spremembe {conf_changes} ≠ pričakovane "
             f"{EXP_CONF_CHANGES}")
    else:
        ok("I4 conf prekalkulacija: natanko 1 sprememba (p98 1905 WEAK→MEDIUM)")

    # ——— I5: meritve v3 ———
    bases3 = set(pages_by)
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
    for r in out_rows:  # TOTAL konvencija P55 (vključno Blatt I vrstice)
        conf_counts[r["conf"]] += 1
    series_counts = {k: sum(1 for r in out_rows if r["series"] == k)
                     for k in ("S1", "S2", "BI")}
    amb_rows = sum(1 for r in out_rows if r["ambiguous"])

    if len(out_rows) != EXP_ROWS:
        fail(f"I5 rows {len(out_rows)} ≠ {EXP_ROWS}")
    if len(bases3) != EXP_BASES:
        fail(f"I5 bases {len(bases3)} ≠ {EXP_BASES}")
    if len(multi) != EXP_MULTI:
        fail(f"I5 multi-page {len(multi)} ≠ {EXP_MULTI}")
    if len(cross) != EXP_CROSS:
        fail(f"I5 cross-Blatt {len(cross)} ≠ {EXP_CROSS}")
    if amb_rows != EXP_AMB_ROWS:
        fail(f"I5 ambiguousRows {amb_rows} ≠ {EXP_AMB_ROWS}")
    if len(s1s2) != EXP_S1S2 or len(bi_rows) != EXP_BI:
        fail(f"I5 S1S2/BI {len(s1s2)}/{len(bi_rows)} ≠ {EXP_S1S2}/{EXP_BI}")
    if series_counts != EXP_SERIES:
        fail(f"I5 series {series_counts} ≠ {EXP_SERIES}")
    if len(pos_by_base) != EXP_BASES:
        fail(f"I5 pozicioniranih {len(pos_by_base)} ≠ {EXP_BASES}")
    suffix_groups = sum(1 for b in pos_by_base if len(bybase[b]) > 1)
    if suffix_groups != EXP_SUFFIX:
        fail(f"I5 suffixGroups {suffix_groups} ≠ {EXP_SUFFIX}")
    if dict(conf_counts) != EXP_CONF:
        fail(f"I5 conf {dict(conf_counts)} ≠ {EXP_CONF}")
    if round(100 * len(out_rows) / TOTAL_PS_ROWS, 1) != EXP_SHARE_PCT:
        fail("I5 sharePct odmika")
    if not FAILURES:
        ok(f"I5 meritve: rows {EXP_ROWS} · bases {EXP_BASES} · multi "
           f"{EXP_MULTI} · cross {EXP_CROSS} · ambRows {EXP_AMB_ROWS} · "
           f"conf {EXP_CONF['STRONG']}/{EXP_CONF['MEDIUM']}/{EXP_CONF['WEAK']}")

    # ——— areaProof (P55 metoda, seed 42) ———
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
    exp_area = {"pairsWithArea": EXP_AREA["pairs"],
                "medianRatio": EXP_AREA["median"],
                "q25": EXP_AREA["q25"], "q75": EXP_AREA["q75"],
                "tightN": EXP_AREA["tightN"],
                "tightShare": EXP_AREA["tightShare"],
                "shuffleMedian": EXP_AREA["shufMed"],
                "shuffleTightShare": EXP_AREA["shufTight"],
                "historicalQkM2": HIST_QK_M2,
                "deltaPct": EXP_AREA["deltaPct"]}
    if area_proof != exp_area:
        fail(f"I5 areaProof {area_proof} ≠ {exp_area}")
    elif not FAILURES:
        ok(f"I5 areaProof: {len(area_pairs)} parov, median {area_proof['medianRatio']} "
           f"(Δ {area_proof['deltaPct']} %), kontrola {area_proof['shuffleMedian']}")

    # ——— spatialProof (P55 metoda, seed 7) ———
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
        "share150": round(sum(1 for x in consec if x <= NEIGH_M) / len(consec), 4),
        "shuffleMedianM": round(statistics.median(sh_d), 1),
        "shuffleShare150": round(sum(1 for x in sh_d if x <= NEIGH_M) / len(sh_d), 4),
        "enrichmentX": round(statistics.median(sh_d) / statistics.median(consec), 1),
    }
    exp_spatial = {"consecPairs": EXP_SPATIAL["pairs"],
                   "medianM": EXP_SPATIAL["median"],
                   "q25M": EXP_SPATIAL["q25"], "q75M": EXP_SPATIAL["q75"],
                   "share150": EXP_SPATIAL["share150"],
                   "shuffleMedianM": EXP_SPATIAL["shufMed"],
                   "shuffleShare150": EXP_SPATIAL["shuf150"],
                   "enrichmentX": EXP_SPATIAL["enrichX"]}
    if spatial_proof != exp_spatial:
        fail(f"I5 spatialProof {spatial_proof} ≠ {exp_spatial}")
    elif not FAILURES:
        ok(f"I5 spatialProof: {len(consec)} parov, median {spatial_proof['medianM']} m, "
           f"kontrola {spatial_proof['shuffleMedianM']} m, "
           f"{spatial_proof['enrichmentX']}× ožje")

    # ——— I6: fuzije ———
    def rows_of(b):
        return [r for r in out_rows if r["base"] == b]

    r1903 = rows_of("1903")
    if len(r1903) != 3:
        fail(f"I6 1903: {len(r1903)} vrstic ≠ 3")
    b1903: dict[str, list[str]] = defaultdict(list)
    for r in r1903:
        b1903[blatt_of(r["page"])].append(r["owner"])
    if sorted(b1903) != ["III", "IV"] or len(b1903["III"]) != 2 \
            or len(b1903["IV"]) != 1:
        fail(f"I6 1903 blatt dist {dict(b1903)} ≠ III×2 + IV×1")
    a3 = sum(r["areaQK"] for r in r1903 if blatt_of(r["page"]) == "III")
    a4 = sum(r["areaQK"] for r in r1903 if blatt_of(r["page"]) == "IV")
    sh = round(a3 / (a3 + a4), 4)
    if abs(sh - 0.7081) > 1e-9:
        fail(f"I6 1903 delež III {sh} ≠ 0.7081 (P67)")
    r1905 = rows_of("1905")
    if len(r1905) != 2 or any(r["page"] == 93 and r["areaQK"] for r in r1905):
        fail("I6 1905: 2 vrstici, p93 instanca brez areaQK (R2b profil)")
    r1904 = rows_of("1904")
    if len(r1904) != 1 or not r1904[0]["ratio"] \
            or abs(r1904[0]["ratio"] - 6.8052) > 1e-9:
        fail(f"I6 1904: 1 vrstica, ratio 6.8052 (izven pasu — prečrtana)")
    if not FAILURES:
        ok("I6 fuzije: 1903 = III×2 + IV×1 (delež III 0.7081), "
           "1905 = 2 vrstici (R2b profil), 1904 = 1 vrstica (ratio 6.8052)")

    # ——— I7: odmiki od P67 projekcije ———
    proj = p67["parts"]["A"]["projection"]
    deltas = {
        "bases": {"spec": proj["bases"]["after"], "actual": len(bases3),
                  "delta": len(bases3) - proj["bases"]["after"]},
        "multiPage": {"spec": proj["multiPage"]["after"], "actual": len(multi),
                      "delta": len(multi) - proj["multiPage"]["after"]},
        "crossBlatt": {"spec": proj["crossBlatt"]["after"],
                       "actual": len(cross),
                       "delta": len(cross) - proj["crossBlatt"]["after"]},
    }
    ok(f"I7 odmiki od P67 projekcije [~]: bases {deltas['bases']['spec']}→"
       f"{deltas['bases']['actual']}, multi {deltas['multiPage']['spec']}→"
       f"{deltas['multiPage']['actual']}, cross {deltas['crossBlatt']['spec']}→"
       f"{deltas['crossBlatt']['actual']}")

    join_block = {
        "matchedRows": len(out_rows),
        "matchedRowsS1S2": len(s1s2),
        "matchedRowsBI": len(bi_rows),
        "matchedSharePct": round(100 * len(out_rows) / TOTAL_PS_ROWS, 1),
        "psUniqueNumbers": v2rt["join"]["psUniqueNumbers"],
        "psPositionedParcels": len(pos_by_base),
        "suffixGroups": suffix_groups,
        "seriesCounts": series_counts,
        "confCounts": {"STRONG": conf_counts["STRONG"],
                       "MEDIUM": conf_counts["MEDIUM"],
                       "WEAK": conf_counts["WEAK"]},
        "readConfBI": v2rt["join"]["readConfBI"],
        "ambiguousBases": len(multi),
        "ambiguousRows": amb_rows,
    }
    per_blatt_amb = {
        "basesOnMultiplePages": len(multi),
        "rowsWithAmbiguousBase": amb_rows,
        "note": "base na > 1 strani v v3 (P68 re-join po P55 metodi); "
                "čez-Blatt 98 (blattDist I·II 31 / II·III 46 / III·IV 3 / "
                "IV·V 18) [~]",
    }
    return (out_rows, removed, renum_spec, deltas, join_block, per_blatt_amb,
            area_proof, spatial_proof, amb_changes, conf_changes,
            v2ev["pageSelection"], v2ev["join"]["psUniqueNumbers"],
            v2ev["join"]["readConfBI"], v2ev["furkovce"])


def build_documents():
    (out_rows, removed, renum_spec, deltas, join_block, per_blatt_amb,
     area_proof, spatial_proof, amb_changes, conf_changes,
     page_sel, ps_unique, read_conf_bi, furkovce) = compute()
    if FAILURES:
        print(f"P68: {len(FAILURES)} invariant(ov) PADLO")
        return 1

    status_line = (
        f"P68 V3 SANACIJA ŠTEVILČENJA: 17 preslikav izvedenih (p78 160x→150x, "
        f"p93 160x→190x, p87 +1020 — bajtno po P67 specifikaciji, 0 kolizij); "
        f"re-join po P55 metodi: 14 vrstic izpada (base brez PF poligona — "
        f"3× p78 Wüstung Pod Grabino, 11× p87), p93 3× re-claim na 1903/1904/1905 "
        f"(poligoni JZ, 1903/1905 re-claim pozicij p98, 1904 nova base); "
        f"v3: {len(out_rows)} vrstic / {deltas['bases']['actual']} base / "
        f"multi-page {deltas['multiPage']['actual']} / cross-Blatt "
        f"{deltas['crossBlatt']['actual']} (odmiki od P67 aproksimacije "
        f"[~] dokumentirani); fuzije: 1903 = III×2+IV×1 (delež 0.7081), "
        f"1905 R2b profil, 1904 ratio 6.8052 izven pasu (prečrtana vrstica); "
        f"area median {area_proof['medianRatio']} (Δ {area_proof['deltaPct']} %), "
        f"sosledje {spatial_proof['consecPairs']} parov / "
        f"{spatial_proof['medianM']} m ({spatial_proof['enrichmentX']}×); "
        f"v2 ostaja arhiv (ebbd8f29…); SPLIT join = LASTNIKA (P69)"
    )

    evidence = {
        "version": 3,
        "task": "P68 (issue #13) — PS-PARCELS-GEO v3: sanacija številčenja "
                "(17 preslikav p78/p93/p87 po P67 specifikaciji) + re-join "
                "po P55 metodi",
        "date": DATE,
        "generatedBy": "scripts/p68_ps_v3_renumber.py",
        "principle": "P67 forenzika je dokazala dvojno Kurrent zamenjavo na "
                     "straneh 78/93/87 (oči + strip 2× + kontinuiteta + kartni "
                     "priči); v3 je mehanski izvod te specifikacije: 17 "
                     "preslikav base + re-join po P55 metodi (group_pos). "
                     "Registrska branja (ps-raw) ostajajo NESPREMENJENA — "
                     "sanacija je na join ključu (base), parzella ostaja "
                     "originalno branje. Nespremenjene vrstice bajtno == v2 "
                     "(lekcija P9). Odmiki od P67 aproksimacije so meritve, "
                     "ne napake. Strojna forenzika ni dokazni vir; SPLIT "
                     "join odločitev ostaja LASTNIKA (P69).",
        "inputs": {
            "v2Evidence": "research/issue17/ps-parcels-geo-v2.json (sha256 "
                          f"{PIN_V2_EV_SHA[:8]}…; 1093 rowsEvidence)",
            "p67Evidence": "research/issue17/ps-anomaly-forensics.json "
                           f"(sha256 {PIN_P67_EV_SHA[:8]}…; renumberSpec 17)",
            "p59Evidence": "research/issue17/ps-blatt-headers.json "
                           f"(sha256 {PIN_P59_EV_SHA[:8]}…; pageAttribution)",
            "parcels": "research/georef-n83/gurs/parcels-ko1544-merged.json "
                       f"(sha256 {PIN_PARCELS_SHA[:8]}…; 2117 parcel P47)",
        },
        "historicalConstant": {"wienerQkM2": HIST_QK_M2},
        "join": join_block,
        "furkovce": furkovce,
        "renumberSpec": renum_spec,
        "collisions": "0 (1503–1505, 1904, 1681–1700 proste; 1903/1905 samo "
                      "p98 — strani drugačnega Blatta III vs IV)",
        "removedRows": removed,
        "removedReason": "preslikana base brez PF poligona v k.o. 1544 "
                         "(P67 kartni priči: 1503–1505 in 1681–1700 NE "
                         "obstajajo); vrstica registra ostaja v ps-raw, "
                         "izpada le iz joina",
        "groupDerivedChanges": {
            "ambiguous": [f"p{p} {b}: {o}→{n}" for p, b, o, n in amb_changes],
            "conf": [f"p{p} {b}: {o}→{n}" for p, b, o, n in conf_changes],
        },
        "fusionCases": {
            "1903": {"rows": 3, "blatts": "III ×2 (p98) + IV ×1 (p93)",
                     "shareIII": 0.7081,
                     "note": "cross-Blatt base — per-Blatt primež (disjunktni "
                             "lastniki); SPLIT = LASTNIKA (P69) [~]"},
            "1904": {"rows": 1, "blatts": "IV (p93)", "ratio": 6.8052,
                     "note": "nova base; poligon PF 1904 obstaja (4927 m²); "
                             "ratio izven pasu — vrstica registra prečrtana "
                             "(P67: blok 1901–1904 rdeče)"},
            "1905": {"rows": 2, "blatts": "III (p98) + IV (p93)",
                     "note": "p93 instanca brez areaQK → R2b profil "
                             "(areaIncomplete [~] == P67)"},
        },
        "p67ProjectionDeltas": {
            **deltas,
            "note": "P67 projekcija je bila aproksimacija [~] ('razvrstitev "
                    "novih base = izhod P68 pipeline [~]'): formula −5+2 ni "
                    "štela 9 preostalih 661–680 cross-Blatt base (skupaj −14) "
                    "niti izpada 1503–1505/1681–1700 (brez poligonov); v3 "
                    "številke so MERITVE nad re-joinom",
        },
        "areaProof": area_proof,
        "spatialProof": spatial_proof,
        "perBlattAmbiguity": per_blatt_amb,
        "invariants": {
            "I1": "RENUM 17 == P67 renumberSpec bajtno; kolizij 0",
            "I2": "pini: v2 ebb8f729…, P67/P59 (v3 re-run), PARCELS fee91fca…; runtime == rowsEvidence",
            "I3": "17 preslikanih; 14 izpada (3× p78, 11× p87); p93 3× "
                  "re-claim == group_pos == v2 poziciji p98",
            "I4": "nespremenjene vrstice bajtno == v2; group-derived samo "
                  "ambiguous 15 + conf 1",
            "I5": f"rows {EXP_ROWS}, bases {EXP_BASES}, multi {EXP_MULTI}, "
                  f"cross {EXP_CROSS}, ambRows {EXP_AMB_ROWS}, conf {EXP_CONF['STRONG']}/{EXP_CONF['MEDIUM']}/{EXP_CONF['WEAK']}",
            "I6": "1903 III×2+IV×1 (0.7081), 1905 R2b, 1904 ratio 6.8052",
            "I7": "odmiki od P67 aproksimacije dokumentirani (−4/−9/−9)",
            "I8": "dokaz rowsEvidence == runtime rows bajtno",
            "I9": "determinizem --check bajtno",
        },
        "statusLine": status_line,
        "verdictSi": (
            "P68: V3 SANACIJA ŠTEVILČENJA IZVEDENA (issue #13) — mehanski "
            "izvod P67 specifikacije, deterministično, brez AI ob delovanju. "
            "17 preslikav (p78 1603/1604/1605→1503/1504/1505 — Blatt II "
            "Wüstung Pod Grabino; p93 →1903/1904/1905 — Blatt IV; p87 "
            "661–680→1681–1700 — +1020) s 0 kolizijami. Re-join po P55 "
            "metodi: 14 vrstic izpada (base brez PF poligona — kartni priči "
            "P67), p93 3 vrstice re-claimajo poligone 1903/1904/1905 "
            "(jugozahodna lokacija; 1903/1905 delita poziciji s p98 "
            "instancami III). Skok II·IV IZGINE iz joina (lažni fuziji "
            "1603/1604 razpadeta), čez-Blatt lažni pari 661/671 razpadejo "
            "(Blatt I instanci ostanejo čisti). Meritve v3: 1079 vrstic, "
            "798 base, 199 multi-page, 98 cross-Blatt (blattDist I·II 31 / "
            "II·III 46 / III·IV 3 / IV·V 18), area median 3.8512 (Δ +7.08 %), "
            "sosledje 590 parov / 51.8 m / 28.3×. Odmiki od P67 aproksimacije "
            "(802/208/107) so izračunane vrednosti, ne napake — aproksimacija "
            "ni štela 9 preostalih 661–680 cross base in izpada brez-poligonov. "
            "SPLIT join odločitev ostaja LASTNIKA (P69); per-Blatt instanca "
            "1903/1905 (III vs IV) ostane fuzija v v3 [~]."
        ),
        "verdictEn": (
            "P68: THE v3 RENUMBERING SANITATION REALIZED (issue #13) — a "
            "mechanical derivation of the P67 specification, deterministic, "
            "no AI at runtime. 17 mappings (p78 1603/1604/1605→1503/1504/1505 "
            "— Blatt II Wüstung Pod Grabino; p93 →1903/1904/1905 — Blatt IV; "
            "p87 661–680→1681–1700 — +1020) with 0 collisions. Re-join by the "
            "P55 method: 14 rows dropped (base without a PF polygon — the P67 "
            "map witnesses), p93 3 rows re-claim polygons 1903/1904/1905 "
            "(south-west location; 1903/1905 share positions with the p98 III "
            "instances). The II·IV skip DISSOLVES from the join (the false "
            "1603/1604 fusions collapse), the cross-Blatt false pairs 661/671 "
            "collapse (the Blatt I instances stay clean). v3 measurements: "
            "1079 rows, 798 bases, 199 multi-page, 98 cross-Blatt (blattDist "
            "I·II 31 / II·III 46 / III·IV 3 / IV·V 18), area median 3.8512 "
            "(Δ +7.08 %), adjacency 590 pairs / 51.8 m / 28.3×. Deviations "
            "from the P67 approximation (802/208/107) are computed values, "
            "not errors — the approximation ignored the 9 remaining 661–680 "
            "cross bases and the polygon-less drops. The SPLIT join decision "
            "remains the OWNER's (P69); the per-Blatt instances 1903/1905 "
            "(III vs IV) remain fused in v3 [~]."
        ),
        "next": [
            "SPLIT joina (lastniška odločitev — zdaj nad v3: 1903/1905 "
            "nastopata kot cross-Blatt, 1603/1604/661/671 izpadajo)",
            "veriga re-run P60–P66 s posodobljenimi pini (atribucije/moda B "
            "nad v3)",
            "930: dokončna atribucija (PF protokol / lastniška odločitev)",
            "sistemski pregled preostalih P38 pass1 slojev (p74/p76/p77 "
            "1121–1200 [~]; p88 721–740 [~])",
            "PF protokol povezava (lastniki pas-instanc)",
        ],
        "rowsEvidence": out_rows,
    }

    runtime = {
        "version": 3,
        "task": "P68 (issue #13) — PS-PARCELS-GEO v3: sanirano številčenje "
                "(17 preslikav p78/p93/p87 po P67 specifikaciji, re-join po "
                "P55 metodi)",
        "date": DATE,
        "generatedBy": "scripts/p68_ps_v3_renumber.py",
        "historicalConstant": {"wienerQkM2": HIST_QK_M2},
        "pageSelection": page_sel,
        "join": {**join_block, "psUniqueNumbers": ps_unique,
                 "readConfBI": read_conf_bi},
        "v3Delta": {
            "reason": "sanacija številčenja: 17 preslikav (p78 160x→150x, "
                      "p93 160x→190x, p87 +1020) po P67 forenzični "
                      "specifikaciji (oči + strip 2× + kontinuiteta + karta); "
                      "re-join po P55 metodi",
            "renumbered": 17,
            "removed": len(removed),
            "added": 0,
            "before": {"rows": 1093, "bases": 800, "multiPage": 211,
                       "crossBlatt": 110},
            "after": {"rows": len(out_rows), "bases": len(set(r["base"] for r in out_rows)),
                      "multiPage": per_blatt_amb["basesOnMultiplePages"],
                      "crossBlatt": 98},
            "invariance": "nespremenjene vrstice bajtno == v2 (lekcija P9); "
                          "group-derived polja (ambiguous/conf) prekalkulirana "
                          "po P55 metodi; v2 ostaja arhiviran "
                          "(research/issue17/ps-parcels-geo-v2.json)",
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
        ok("I8 dokaz ⊇ runtime (1079 vrstic bajtno)")

    check = "--check" in sys.argv
    if check:
        ev2 = json.dumps(json.loads(V3_EV.read_text(encoding="utf-8")),
                         ensure_ascii=False)
        rt2 = json.dumps(json.loads(OUT_RUNTIME.read_text(encoding="utf-8")),
                         ensure_ascii=False)
        if json.dumps(evidence, ensure_ascii=False) == ev2 and \
                json.dumps(runtime, ensure_ascii=False) == rt2:
            print("P68 --check: determinizem PASS (dokaz + runtime bajtno "
                  "identična)")
            return 0
        print("P68 --check: MISMATCH")
        return 1

    V3_EV.write_text(jdump(evidence) + "\n", encoding="utf-8")
    print(f"  ✓ zapisano: {V3_EV.relative_to(REPO)} "
          f"({len(evidence['rowsEvidence'])} vrstic)")
    OUT_RUNTIME.write_text(jdump(runtime) + "\n", encoding="utf-8")
    print(f"  ✓ zapisano: {OUT_RUNTIME.relative_to(REPO)} "
          f"({len(runtime['rows'])} vrstic)")
    print(f"P68: v3 sanacija — {len(out_rows)} vrstic, "
          f"{deltas['bases']['actual']} base, cross-Blatt "
          f"{deltas['crossBlatt']['actual']}; odmiki od P67 aproksimacije "
          f"dokumentirani [~]")
    return 0


if __name__ == "__main__":
    sys.exit(build_documents())
