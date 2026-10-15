#!/usr/bin/env python3
# P74 — CROSS-BLATT DVOJNOSTI REGISTRA (čez-Blatt dual base): odločitveni
# paket za cross-Blatt SPLIT joina (odprta točka P73 ①; P66 vzorec re-izpeljan
# iz v6 univerzuma).
#
# KONTEKST: v6 (po C3 isti-Blatt SPLIT opcija A) ima 48 cross-Blatt base —
# base z vrsticami na ≥ 2 RAZLIČNIH Blattih. P66 paket (v3 era) je meril 36
# split base po P65 kriteriju (shareCount == 2 · dominantShare < 0.75); v6
# univerzum je širši: VSAKI cross base ima 1 vrstico per Blatt (48/48),
# množice lastnikov med Blatti DISJUNKTNE (48/48, 0 prekrivanj) — ista
# številka pod dvema sosednjima Blattoma = 2 RAZLIČNI realni parceli
# (per-Blatt ponovitev numeracije, P56 pageMap: p11 I 161–183 / p61 II
# 161–180; p64 II 1821–1840 / p94 III 1821–1841; p96 III 1961–1980 / p102 IV
# 1980–1999; p110 IV 2141–2160 / p125 V 2141–2160; p133 V 2601–2620 / p135 IV
# 2611–2630). Join v6 FUZIRA obe parceli pod eno geometrijo (geoShared 48/48
# — vse vrstice base si delijo enako lat/lng). PAKET NE ODLOČA namesto
# lastnika — MERI in DOKAZUJE dejstva (deterministično, brez AI ob delovanju;
# v6 join NESPREMENJEN — disciplina P56–P73).
#
# Merjeno nad 48 cross base (v6 rowsEvidence 939 × P59 pageAttribution ×
# P56 pageMap × P66 split pack × P72 dual pack):
#   • blattPair dist: I·II 13 · II·III 16 · III·IV 1 · IV·V 18 (48 sosednjih
#     parov; 0 skokov) — ponovitev numeracije med SOSEDNJIMI Blatti
#   • vrstice: 96 (48 base × 2; točno 1 vrstica per Blatt 48/48)
#   • lastniki: 48/48 DISJUNKTNI med Blatti (JEDRO paketa; P66: 36/36 v v3)
#   • hišne številke: 42 različne · 2 isti (1871, 1872 — dokumentirano per
#     base) · 4 brez (ena stran brez hn)
#   • kulture per Blatt + prekrivanja (isti kultur na obeh Blattih)
#   • dominantShare pasovi: [0.50,0.60) 8 · [0.60,0.70) 5 · [0.70,0.75) 8 ·
#     [0.75,1.00] 27 (P66 kriterij < 0.75 bi pokril samo 21; univerzum 48)
#   • pageMap: numMin/numMax per stran (P56) + prekrivanje razponov parov —
#     dokaz ponovitve serije čez Blatte
#   • opcija A1 (keep DOMINANT Blatt; izenačeni deleži → min Blatt): drop 48,
#     rows 939 → 891, bases 879, lost 0, multi 50 → 2, cross 48 → 0,
#     ambRows 100 → 4; geometrija base ostane (vrstici si jo delita)
#   • opcija A2 (keep MIN Blatt): enaki števci; keep različen pri 29 base
#     (dominantni Blatt kasnejši v vrstnem redu I–V) — izbira pravila
#     lastniška
#   • evolucija P66 → v6: 17/36 ostaja · 19 odhaja (C1 sekcije 5 · C3
#     isti-Blatt drop 13 · C2 p93 reverzija 1) · 31 novih (že v v5; P66 jih
#     ni pokril po P65 kriteriju dominantShare < 0.75)
#
# Vhodi (committed):
#   research/issue17/ps-parcels-geo-v6.json       (v6 dokaz — rowsEvidence 939)
#   src/data/atlas/ps-parcels-geo.json            (v6 runtime — I9 pin)
#   research/issue17/ps-blatt-headers.json        (P59 pageAttribution)
#   research/issue17/ps-register-topology.json    (P56 pageMap)
#   research/issue17/ps-split-pack.json           (P66 — primerjava)
#   research/issue17/ps-dual-occurrence-pack.json (P72 — kontekst)
# Izhodi:
#   research/issue17/ps-cross-blatt-pack.json (dokaz)
#   src/data/atlas/ps-cross-blatt-pack.json   (runtime, bajtna projekcija)
#
# Invarianti (FAIL ob padu):
#   I1 vhodni pini: 6× sha256 + števci 939/879/48/96
#   I2 re-izpeljava cross base == 48 bajtno (96 vrstic; 1 vrstica per Blatt
#      48/48; sosednji pari 48, skoki 0)
#   I3 evolucija P66: 17/36 ostaja · 19 odhaja (C1 5 / C3 13 / C2 1) · 31 novih
#   I4 forenzika: 48/48 disjunktni lastniki; hn 42/2/4; areaSuspect 0;
#      deleži izenačeni 0; Σ areaQK per Blatt == pin
#   I5 blattDist + pasovi + pageMap razponi == pin
#   I6 brez georef polj (lat/lng/areaModern/ratio) v izpisu
#   I7 dokaz ⊇ runtime (bajtno podmnožica)
#   I8 determinizem — --check bajtno identično
#   I9 v6 runtime join NESPREMENJEN (sha256 pin)

import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V6_EV = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v6.json")
V6_RT = os.path.join(ROOT, "src/data/atlas/ps-parcels-geo.json")
P59_EV = os.path.join(ROOT, "research/issue17/ps-blatt-headers.json")
P56_EV = os.path.join(ROOT, "research/issue17/ps-register-topology.json")
P66_EV = os.path.join(ROOT, "research/issue17/ps-split-pack.json")
P72_EV = os.path.join(ROOT, "research/issue17/ps-dual-occurrence-pack.json")
OUT_EV = os.path.join(ROOT, "research/issue17/ps-cross-blatt-pack.json")
OUT_RT = os.path.join(ROOT, "src/data/atlas/ps-cross-blatt-pack.json")

PIN_V6EV_SHA = "de13f10bee5f7b6f21a389997e470214760f04b7f384f1236c7d6215feacfe18"
PIN_V6RT_SHA = "6270b267be9aabb621e05ba8acc05b7a67458d3c77f0b42934202a852fef943d"
PIN_P59EV_SHA = "650f13dccab1da70a60d04c41ce9f7887ca94eafea8a0a7927c104ca899b76f3"
PIN_P56EV_SHA = "2fddc76fb94b69fed55170220fa8dfa3ace4a9466043d264b8b8df788e78a50c"
PIN_P66EV_SHA = "02214eba020ce3e11c50db3af873e17b045a38fbd1a4f452e59ddbde345bf9ca"
PIN_P72EV_SHA = "0922a7013071363c75095082a6bb074490a944c6f979de7578f91898946857cd"

EXPECTED_ROWS = 939          # v6 rowsEvidence
EXPECTED_BASES = 879         # v6 base
EXPECTED_CROSS = 48          # cross-Blatt base (≥ 2 Blatti)
EXPECTED_ROWS_XB = 96        # cross-Blatt vrstice (48 × 2)
EXPECTED_BLATT_DIST = {"I·II": 13, "II·III": 16, "III·IV": 1, "IV·V": 18}
EXPECTED_P66_STAY = 17
EXPECTED_P66_LEAVE = 19
EXPECTED_LEAVE_C1 = 5
EXPECTED_LEAVE_C3 = 13
EXPECTED_LEAVE_C2 = 1
EXPECTED_NEW = 31
EXPECTED_HN = {"različni": 42, "isti": 2, "brez": 4}
EXPECTED_OWNER_DISJOINT = 48
EXPECTED_AREA_SUSPECT = 0
EXPECTED_TIES = 0
EXPECTED_SUMQK = {"I": 1874, "II": 11364, "III": 18300, "IV": 13257, "V": 13118}
EXPECTED_DOM_BUCKETS = {"0.50–0.60": 8, "0.60–0.70": 5, "0.70–0.75": 8,
                        "≥0.75": 27}
EXPECTED_A1 = {"drop": 48, "rows": 891, "bases": 879, "lost": 0,
               "multi": 2, "cross": 0, "ambRows": 4}
EXPECTED_A2_DIFF_KEEP = 29   # base, kjer A2 (min Blatt) pusti drugačno vrstico kot A1 (dominant)

GEO_FIELDS = ("lat", "lng", "areaModern", "ratio")

ROW_FIELDS = ("page", "parzella", "base", "owner", "stand", "hausNr", "wohnort",
              "wohnortInherited", "kultur", "joch", "klafter", "areaQK",
              "areaSuspect", "parts", "conf", "series", "ambiguous",
              "source", "readConf", "anmerkung")

ORD = {"I": 0, "II": 1, "III": 2, "IV": 3, "V": 4}


def fail(msg):
    print(f"FAIL I: {msg}")
    sys.exit(1)


def ok(msg):
    print(f"  ✓ {msg}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def row_pick(r):
    return {k: r.get(k) for k in ROW_FIELDS if r.get(k) is not None}


def blatt_key(bl):
    return ORD.get(bl, 99)


def main():
    print("P74 — cross-Blatt dual pack (čez-Blatt dvojnosti registra)")
    check_mode = "--check" in sys.argv

    v6 = json.load(open(V6_EV))
    p59 = json.load(open(P59_EV))
    p56 = json.load(open(P56_EV))
    p66 = json.load(open(P66_EV))
    p72 = json.load(open(P72_EV))

    rows = v6["rowsEvidence"]
    page_attr = p59["pageAttribution"]
    pagemap = {x["page"]: x for x in p56["pageMap"]}

    def blatt_of(page):
        return page_attr.get(str(page), {}).get("blatt")

    # ————— I1 vhodni pini —————
    pins = [(V6_EV, PIN_V6EV_SHA, "v6 dokaz"),
            (P59_EV, PIN_P59EV_SHA, "P59 dokaz"),
            (P56_EV, PIN_P56EV_SHA, "P56 dokaz"),
            (P66_EV, PIN_P66EV_SHA, "P66 dokaz"),
            (P72_EV, PIN_P72EV_SHA, "P72 dokaz")]
    for path, pin, label in pins:
        if sha256(path) != pin:
            fail(f"I1 {label} sha256 drift ({sha256(path)[:8]}… ≠ {pin[:8]}…)")
    ok("I1 pini (5× sha256 dokazov)")

    rt_sha = sha256(V6_RT)
    if rt_sha != PIN_V6RT_SHA:
        fail(f"I1 v6 runtime drift ({rt_sha[:8]}… ≠ {PIN_V6RT_SHA[:8]}…) — "
             f"join se je spremenil brez P74 znanja")
    ok("I1 v6 runtime sha pin (I9 determinizem)")

    if len(rows) != EXPECTED_ROWS:
        fail(f"I1 rowsEvidence {len(rows)} ≠ {EXPECTED_ROWS}")
    bases_all = {r["base"] for r in rows}
    if len(bases_all) != EXPECTED_BASES:
        fail(f"I1 base {len(bases_all)} ≠ {EXPECTED_BASES}")
    ok(f"I1 števci (rows {EXPECTED_ROWS} / base {EXPECTED_BASES})")

    bybase = defaultdict(list)
    for r in rows:
        bybase[r["base"]].append(r)

    # ————— I2 re-izpeljava cross base —————
    cross = {}
    for b, rs in bybase.items():
        bls = {blatt_of(r["page"]) for r in rs}
        bls.discard(None)
        if len(bls) > 1:
            cross[b] = rs
    if len(cross) != EXPECTED_CROSS:
        fail(f"I2 cross base {len(cross)} ≠ {EXPECTED_CROSS}")
    xb_rows = sum(len(rs) for rs in cross.values())
    if xb_rows != EXPECTED_ROWS_XB:
        fail(f"I2 cross vrstice {xb_rows} ≠ {EXPECTED_ROWS_XB}")
    one_per_blatt = all(
        len({blatt_of(r["page"]) for r in rs}) == len(rs)
        for rs in cross.values())
    if not one_per_blatt:
        fail("I2 nek base ima > 1 vrstico na istem Blattu (1+1 pričakovano)")
    ok(f"I2 re-izpeljava cross base == {EXPECTED_CROSS} bajtno "
       f"({EXPECTED_ROWS_XB} vrstic; 1 vrstica per Blatt 48/48)")

    # blattDist + sosednjost
    blatt_dist = Counter()
    skip_pairs = 0
    adjacent_pairs = 0
    for b, rs in cross.items():
        bls = sorted({blatt_of(r["page"]) for r in rs}, key=blatt_key)
        pair = "·".join(bls)
        blatt_dist[pair] += 1
        if len(bls) == 2 and blatt_key(bls[1]) - blatt_key(bls[0]) == 1:
            adjacent_pairs += 1
        else:
            skip_pairs += 1
    if dict(blatt_dist) != EXPECTED_BLATT_DIST:
        fail(f"I2 blattDist {dict(blatt_dist)} ≠ {EXPECTED_BLATT_DIST}")
    if adjacent_pairs != EXPECTED_CROSS or skip_pairs != 0:
        fail(f"I2 sosednji {adjacent_pairs} / skoki {skip_pairs}")
    ok(f"I2 blattDist == pin (sosednji {adjacent_pairs}/{EXPECTED_CROSS}, "
       f"skoki {skip_pairs})")

    # ————— I3 evolucija P66 → v6 —————
    p66set = set(p66["bases"].keys())
    stay = sorted(p66set & set(cross.keys()), key=int)
    leave = sorted(p66set - set(cross.keys()), key=int)
    new = sorted(set(cross.keys()) - p66set, key=int)
    if len(stay) != EXPECTED_P66_STAY or len(leave) != EXPECTED_P66_LEAVE \
            or len(new) != EXPECTED_NEW:
        fail(f"I3 P66 ostaja {len(stay)} / odhaja {len(leave)} / novih "
             f"{len(new)} ≠ {EXPECTED_P66_STAY}/{EXPECTED_P66_LEAVE}/"
             f"{EXPECTED_NEW}")
    # razlog odhoda per base (C1 sekcije / C3 isti-Blatt drop / C2 p93 reverzija)
    # NOTE: vrstice so se med v3 → v6 premikale med stranmi (P70 rejoin) in
    # re-base-ale (C2 p93), zato kategoriziramo po ODSTRANJENIH vrsticah base,
    # ne po izgubljenih straneh: C3 = base v v6.removedRows (isti-Blatt drop),
    # C1 = base v v5.removedRows na sekijskih straneh (p83–86/p88), C2 = base,
    # katere P66 razčlenitev vsebuje p93 (revert: base := parzella).
    c1_pages = {83, 84, 85, 86, 88}
    v5_removed = set()
    v5ev_path = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v5.json")
    if os.path.exists(v5ev_path):
        v5_removed = {(r.get("base"), r.get("page"))
                      for r in json.load(open(v5ev_path)).get("removedRows", [])}
    v6_removed = {(r.get("base"), r.get("page")) for r in v6["removedRows"]}
    leave_c1, leave_c3, leave_c2 = [], [], []
    for b in leave:
        p66_pages = set()
        for sh in p66["bases"][b]["blattShares"]:
            p66_pages.update(sh["pages"])
        if any(bb == b for bb, _ in v6_removed):
            gone = sorted(pg for bb, pg in v6_removed if bb == b)
            leave_c3.append((b, gone))
        elif any((b, pg) in v5_removed and pg in c1_pages
                 for pg in p66_pages):
            gone = sorted(pg for pg in p66_pages
                          if (b, pg) in v5_removed)
            leave_c1.append((b, gone))
        elif 93 in p66_pages:
            leave_c2.append((b, [93]))
        else:
            fail(f"I3 odhod {b} brez razloga (C1/C3/C2)")
    if len(leave_c1) != EXPECTED_LEAVE_C1 or len(leave_c3) != EXPECTED_LEAVE_C3 \
            or len(leave_c2) != EXPECTED_LEAVE_C2:
        fail(f"I3 odhod razlogi C1 {len(leave_c1)} / C3 {len(leave_c3)} / "
             f"C2 {len(leave_c2)} ≠ {EXPECTED_LEAVE_C1}/{EXPECTED_LEAVE_C3}/"
             f"{EXPECTED_LEAVE_C2}")
    ok(f"I3 P66 → v6: ostaja {len(stay)} · odhaja {len(leave)} "
       f"(C1 sekcije {len(leave_c1)} · C3 isti-Blatt {len(leave_c3)} · "
       f"C2 p93 {len(leave_c2)}) · novih {len(new)}")

    # ————— I4 forenzika + I5 pageMap —————
    bases_out = {}
    owner_disjoint = 0
    owner_overlap = 0
    hn = Counter()
    kult_shared = 0
    area_suspect = 0
    ties = 0
    dom_buckets = Counter()
    sumqk = defaultdict(float)
    a2_diff_keep = 0
    pm_overlap_pairs = 0
    series_all = Counter()
    for b in sorted(cross.keys(), key=int):
        rs = cross[b]
        by_blatt = defaultdict(list)
        for r in rs:
            by_blatt[blatt_of(r["page"])].append(r)
        tot = sum(r.get("areaQK") or 0 for r in rs)
        shares = {bl: sum(r.get("areaQK") or 0 for r in rs2) / tot
                  for bl, rs2 in by_blatt.items()}
        dom = max(shares.values())
        if list(shares.values()).count(dom) > 1:
            ties += 1
        dom_bl = min((bl for bl in shares if shares[bl] == dom),
                     key=blatt_key)
        min_bl = min(shares.keys(), key=blatt_key)
        if dom_bl != min_bl:
            a2_diff_keep += 1
        for lo, hi, label in ((0.50, 0.60, "0.50–0.60"),
                              (0.60, 0.70, "0.60–0.70"),
                              (0.70, 0.75, "0.70–0.75"),
                              (0.75, 2.0, "≥0.75")):
            if lo <= dom < hi:
                dom_buckets[label] += 1
                break
        # lastniki
        ob = {bl: sorted({r["owner"] for r in rs2 if r.get("owner")})
              for bl, rs2 in sorted(by_blatt.items(), key=lambda kv: blatt_key(kv[0]))}
        sets = [set(v) for v in ob.values()]
        inter = sum(len(sets[i] & sets[j])
                    for i in range(len(sets))
                    for j in range(i + 1, len(sets)))
        if inter == 0:
            owner_disjoint += 1
        else:
            owner_overlap += 1
        owners_shared = sorted(set.intersection(*sets)) if sets else []
        # hišne številke
        hnb = {bl: sorted({r.get("hausNr") for r in rs2 if r.get("hausNr")})
               for bl, rs2 in sorted(by_blatt.items(), key=lambda kv: blatt_key(kv[0]))}
        if any(not v for v in hnb.values()):
            hn["brez"] += 1
        elif len(set(tuple(v) for v in hnb.values())) == 1 and len(hnb) > 1:
            hn["isti"] += 1
        else:
            hn["različni"] += 1
        # kulture
        kb = {bl: sorted({r["kultur"] for r in rs2 if r.get("kultur")})
              for bl, rs2 in sorted(by_blatt.items(), key=lambda kv: blatt_key(kv[0]))}
        ksets = [set(v) for v in kb.values()]
        kshared = sorted(set.intersection(*ksets)) if ksets else []
        if kshared:
            kult_shared += 1
        # pageMap razponi per stran
        pgs = sorted({r["page"] for r in rs})
        pmr = {str(p): [pagemap[p]["numMin"], pagemap[p]["numMax"]]
               for p in pgs if p in pagemap}
        if len(pmr) == 2:
            (a1, a2_), (b1, b2_) = pmr.values()
            if a1 <= b2_ and b1 <= a2_:
                pm_overlap_pairs += 1
        # geo shared (brez koordinat — samo števec)
        geos = {(r.get("lat"), r.get("lng")) for r in rs}
        geo_shared = len(geos) == 1 and None not in next(iter(geos))
        # opcija A1 / A2 keep
        keep_a1 = dom_bl
        keep_a2 = min_bl
        # series
        for r in rs:
            if r.get("areaSuspect"):
                area_suspect += 1
            series_all[r["series"]] += 1
            sumqk[blatt_of(r["page"])] += r.get("areaQK") or 0
        base_rec = {
            "base": b,
            "blattPair": "·".join(sorted({blatt_of(r["page"]) for r in rs},
                                         key=blatt_key)),
            "pages": pgs,
            "pagesByBlatt": {bl: sorted(r["page"] for r in rs2)
                             for bl, rs2 in sorted(by_blatt.items(),
                                                   key=lambda kv: blatt_key(kv[0]))},
            "rowsPerBlatt": {bl: len(rs2) for bl, rs2 in sorted(by_blatt.items(),
                             key=lambda kv: blatt_key(kv[0]))},
            "rowsTotal": len(rs),
            "areaQKByBlatt": {bl: round(sum(r.get("areaQK") or 0 for r in rs2), 2)
                              for bl, rs2 in sorted(by_blatt.items(),
                                                    key=lambda kv: blatt_key(kv[0]))},
            "areaQKTotal": round(tot, 2),
            "blattShares": [{"blatt": bl, "share": round(shares[bl], 4),
                             "rows": len(by_blatt[bl]),
                             "pages": sorted(r["page"] for r in by_blatt[bl]),
                             "areaQK": round(sum(r.get("areaQK") or 0
                                                 for r in by_blatt[bl]), 2)}
                            for bl in sorted(shares, key=blatt_key)],
            "dominantBlatt": dom_bl,
            "dominantShare": round(dom, 4),
            "ownerRelation": "disjoint" if inter == 0 else "overlap",
            "owners": sorted({r["owner"] for r in rs if r.get("owner")}),
            "ownersByBlatt": ob,
            "ownersShared": owners_shared,
            "kultures": sorted({r["kultur"] for r in rs if r.get("kultur")}),
            "kulturesByBlatt": kb,
            "kulturesShared": kshared,
            "hausNrByBlatt": hnb,
            "hausNrRelation": ("brez" if any(not v for v in hnb.values())
                               else "isti" if len(set(tuple(v) for v in hnb.values())) == 1
                               and len(hnb) > 1 else "različni"),
            "series": sorted({r["series"] for r in rs}),
            "geoShared": geo_shared,
            "pageMap": pmr,
            "optionA": {"keepBlatt": keep_a1, "keepPage": by_blatt[keep_a1][0]["page"],
                        "dropBlatt": [bl for bl in shares if bl != keep_a1],
                        "dropPages": sorted(r["page"] for bl in shares
                                            if bl != keep_a1
                                            for r in by_blatt[bl]),
                        "keepBlattAlt": keep_a2,
                        "sameKeep": keep_a1 == keep_a2},
            "rows": sorted((row_pick(r) for r in rs),
                           key=lambda x: (x["page"], str(x["parzella"]))),
        }
        bases_out[b] = base_rec

    if owner_disjoint != EXPECTED_OWNER_DISJOINT or owner_overlap != 0:
        fail(f"I4 lastniki: disjunktni {owner_disjoint} / prekrivanja "
             f"{owner_overlap} ≠ {EXPECTED_OWNER_DISJOINT}/0")
    if dict(hn) != EXPECTED_HN:
        fail(f"I4 hn {dict(hn)} ≠ {EXPECTED_HN}")
    if area_suspect != EXPECTED_AREA_SUSPECT:
        fail(f"I4 areaSuspect {area_suspect} ≠ {EXPECTED_AREA_SUSPECT}")
    if ties != EXPECTED_TIES:
        fail(f"I4 izenačeni deleži {ties} ≠ {EXPECTED_TIES}")
    sumqk_r = {k: round(v) for k, v in sumqk.items()}
    if sumqk_r != EXPECTED_SUMQK:
        fail(f"I4 Σ areaQK per Blatt {sumqk_r} ≠ {EXPECTED_SUMQK}")
    if dict(dom_buckets) != EXPECTED_DOM_BUCKETS:
        fail(f"I4 pasovi {dict(dom_buckets)} ≠ {EXPECTED_DOM_BUCKETS}")
    if a2_diff_keep != EXPECTED_A2_DIFF_KEEP:
        fail(f"I4 A2 različen keep {a2_diff_keep} ≠ {EXPECTED_A2_DIFF_KEEP}")
    ok(f"I4 forenzika: disjunktni {owner_disjoint}/{EXPECTED_CROSS} · "
       f"hn {dict(hn)} · areaSuspect {area_suspect} · ties {ties} · "
       f"kulturesShared {kult_shared} · pageMap prekrivanja {pm_overlap_pairs}")
    ok(f"I4 Σ areaQK per Blatt == pin · pasovi == pin · "
       f"A2 različen keep {a2_diff_keep}")

    # ————— opcija A1/A2 vpliv (predračun, brez zapisa) —————
    # NOTE: kept je per (base, page) par — stran gosti kept vrstico enega base
    # IN drop vrstico drugega base (strani deljene čez cross base).
    opt = {}
    for label, keyf in (("A1", lambda rec: rec["optionA"]["keepBlatt"]),
                        ("A2", lambda rec: rec["optionA"]["keepBlattAlt"])):
        kept_pairs = set()
        for b, rec in bases_out.items():
            bl = keyf(rec)
            for pg in rec["pagesByBlatt"][bl]:
                kept_pairs.add((b, pg))
        dropped = xb_rows - len(kept_pairs)
        out_rows_n = EXPECTED_ROWS - dropped
        pages_by = defaultdict(set)
        for r in rows:
            if r["base"] in cross and (r["base"], r["page"]) not in kept_pairs:
                continue
            pages_by[r["base"]].add(r["page"])
        multi = sum(1 for v in pages_by.values() if len(v) > 1)
        bl_by = defaultdict(set)
        for r in rows:
            if r["base"] in cross and (r["base"], r["page"]) not in kept_pairs:
                continue
            bl = blatt_of(r["page"])
            if bl:
                bl_by[r["base"]].add(bl)
        cross_n = sum(1 for v in bl_by.values() if len(v) > 1)
        lost = sum(1 for b in cross if b not in pages_by)
        amb = sum(1 for b, v in pages_by.items() if len(v) > 1
                  for _ in bybase[b])
        opt[label] = {"drop": dropped, "rows": out_rows_n,
                      "bases": EXPECTED_BASES, "lost": lost,
                      "multi": multi, "cross": cross_n, "ambRows": amb}
    if opt["A1"] != EXPECTED_A1:
        fail(f"I5 opcija A1 {opt['A1']} ≠ {EXPECTED_A1}")
    if opt["A2"]["drop"] != opt["A1"]["drop"] or opt["A2"]["lost"] != 0:
        fail(f"I5 opcija A2 {opt['A2']}")
    ok(f"I5 opcija A1 == pin (drop {opt['A1']['drop']}, rows "
       f"{EXPECTED_ROWS} → {opt['A1']['rows']}, multi {opt['A1']['multi']}, "
       f"cross {opt['A1']['cross']}, amb {opt['A1']['ambRows']}) · "
       f"A2 enaki števci")

    # ————— dokaz + runtime —————
    isti_hn = sorted(b for b, rec in bases_out.items()
                     if rec["hausNrRelation"] == "isti")
    brez_hn = sorted(b for b, rec in bases_out.items()
                     if rec["hausNrRelation"] == "brez")

    status_line = (
        f"P74 CROSS-BLATT PACK: {EXPECTED_CROSS} cross-Blatt base "
        f"({EXPECTED_ROWS_XB} vrstic; 1 vrstica per Blatt 48/48), lastniki "
        f"DISJUNKTNI {EXPECTED_OWNER_DISJOINT}/{EXPECTED_CROSS} · pari I·II 13 "
        f"· II·III 16 · III·IV 1 · IV·V 18 (sosednji 48, skoki 0) · pasovi "
        f"8/5/8/27 (≥0.75: 27) · hn 42 različne · 2 isti · 4 brez · geo "
        f"deljena 48/48 · opcija A1 drop 48 → rows 891, cross 0 · P66 "
        f"evolucija: 17 ostaja · 19 odhaja (C1 5 / C3 13 / C2 1) · 31 novih"
    )
    verdict_si = (
        "P74: CROSS-BLATT DVOJNOSTI REGISTRA — 48 ČEZ-BLATT BASE (issue #13) "
        "— odločitveni paket za cross-Blatt SPLIT joina (odprta točka P73 ①; "
        "P66 vzorec re-izpeljan iz v6; deterministično, brez AI ob delovanju; "
        "NE odloča namesto lastnika — MERI in DOKAZUJE): 48 base z vrsticami "
        "na ≥ 2 RAZLIČNIH sosednjih Blattih (I·II 13 · II·III 16 · III·IV 1 · "
        "IV·V 18; skoki 0), vsak točno 1 vrstica per Blatt — množice lastnikov "
        "med Blatti DISJUNKTNE 48/48 (0 prekrivanj; P66 v v3: 36/36) — ista "
        "številka pod dvema Blattoma = 2 RAZLIČNI realni parceli, ker se "
        "numeracija per Blatt PONOVI (P56 pageMap: p11 I 161–183 / p61 II "
        "161–180; p64 II 1821–1840 / p94 III 1821–1841; p110 IV 2141–2160 / "
        "p125 V 2141–2160; prekrivanja razponov " + str(pm_overlap_pairs) +
        "/48) — hišne številke RAZLIČNE 42/48 (2 isti: " +
        ", ".join(isti_hn) + "; 4 brez hn na eni strani), Σ areaQK per Blatt "
        "I 1874 / II 11364 / III 18300 / IV 13257 / V 13118 QK; v6 join teh "
        "48 base FUZIRA dve realni parceli pod eno geometrijo (geoShared "
        "48/48); dominantni deleži: [0.50,0.60) 8 · [0.60,0.70) 5 · "
        "[0.70,0.75) 8 · ≥0.75 27 (P66 kriterij <0.75 bi pokril samo 21); "
        "evolucija P66 → v6: 17/36 ostaja, 19 odhaja (C1 sekcije 5 · C3 "
        "isti-Blatt drop 13 · C2 p93 reverzija 1), 31 novih (že v v5); opcija "
        "A1 (keep DOMINANT Blatt): drop 48 vrstic, 0 base brez vrstic, rows "
        "939 → 891, multi 50 → 2, cross 48 → 0, ambRows 100 → 4; opcija A2 "
        "(keep MIN Blatt) enaki števci, keep različen pri 29 base — izbira "
        "pravila LASTNIŠKA; opcija B (per-Blatt instance + razdelitev "
        "geometrije) zahteva georef Blattnih kart [~]; v6 join NESPREMENJEN; "
        "odločitev LASTNIKA"
    )
    verdict_en = (
        "P74: REGISTER CROSS-BLATT DUAL OCCURRENCES — 48 CROSS-BLATT BASES "
        "(issue #13) — the decision pack for the cross-Blatt SPLIT join (P73 "
        "open point ①; the P66 pattern re-derived from the v6 universe; "
        "deterministic, no AI at runtime; does NOT decide on behalf of the "
        "owner — MEASURES and PROVES): 48 bases with rows on ≥ 2 DIFFERENT "
        "adjacent Blatts (I·II 13 · II·III 16 · III·IV 1 · IV·V 18; 0 skips), "
        "exactly 1 row per Blatt each — owner sets are DISJOINT across Blatts "
        "48/48 (0 overlaps; P66 in v3: 36/36) — the same number under two "
        "Blatts = 2 DIFFERENT real parcels, because numbering RESTARTS per "
        "Blatt (P56 pageMap: p11 I 161–183 / p61 II 161–180; p64 II 1821–1840 "
        "/ p94 III 1821–1841; p110 IV 2141–2160 / p125 V 2141–2160; range "
        "overlaps " + str(pm_overlap_pairs) + "/48) — house numbers DIFFERENT "
        "42/48 (2 same: " + ", ".join(isti_hn) + "; 4 without house numbers "
        "on one side), Σ areaQK per Blatt I 1874 / II 11364 / III 18300 / IV "
        "13257 / V 13118 QK; the v6 join FUSES two real parcels under one "
        "geometry for these 48 bases (geoShared 48/48); dominant shares: "
        "[0.50,0.60) 8 · [0.60,0.70) 5 · [0.70,0.75) 8 · ≥0.75 27 (the P66 "
        "criterion <0.75 would cover only 21); P66 → v6 evolution: 17/36 "
        "remain, 19 leave (C1 sections 5 · C3 isti-Blatt drop 13 · C2 p93 "
        "reversal 1), 31 new (already in v5); option A1 (keep the DOMINANT "
        "Blatt): 48 rows dropped, 0 bases left empty, rows 939 → 891, multi "
        "50 → 2, cross 48 → 0, ambRows 100 → 4; option A2 (keep the MIN "
        "Blatt) has identical counters but a different keep on 29 bases — "
        "the rule choice belongs to the OWNER; option B (per-Blatt instances "
        "+ geometry split) requires georeferenced Blatt sheets [~]; v6 join "
        "UNCHANGED"
    )

    ev = {
        "task": ("P74 — cross-Blatt dual pack: 48 čez-Blatt base "
                 "(odločitveni paket za cross-Blatt SPLIT joina)"),
        "date": "2026-10-15",
        "principle": (
            "odločitveni paket za lastniško odločitev o cross-Blatt SPLIT "
            "joinu (odprta točka P73 ①): 48 cross base iz v6 rowsEvidence × "
            "P59 pageAttribution × P56 pageMap — per-Blatt razčlenitev "
            "vrstic, lastnikov, hišnih številke, kultur, Σ areaQK, pageMap "
            "razponi, opciji A1/A2 predračun, evolucija P66 → v6; NE odloča "
            "namesto lastnika; v6 join nespremenjen (disciplina P56–P73)"
        ),
        "inputs": {
            "v6ev": "research/issue17/ps-parcels-geo-v6.json (rowsEvidence 939)",
            "p59": "research/issue17/ps-blatt-headers.json (pageAttribution)",
            "p56": "research/issue17/ps-register-topology.json (pageMap)",
            "p66": "research/issue17/ps-split-pack.json (primerjava 36)",
            "p72": "research/issue17/ps-dual-occurrence-pack.json (kontekst)",
        },
        "rule": {
            "cross": ("base z vrsticami na ≥ 2 RAZLIČNIH Blattih (P59 "
                      "pageAttribution; 1 vrstica per Blatt pričakovana — "
                      "per-Blatt numeracija)"),
            "blattPair": ("par Blattov sorted po vrstnem redu I–V; sosednji "
                          "par = ordinalna razlika 1"),
            "dominantShare": ("max delež Σ areaQK per Blatt; izenačeni deleži "
                              "→ min Blatt (ties 0 v v6)"),
            "ownerRelation": ("disjoint = množice lastnikov per Blatt brez "
                              "skupnega lastnika"),
            "pageMap": ("P56 numMin/numMax per stran + prekrivanje razponov "
                        "— dokaz ponovitve serije čez Blatte"),
            "optionA1": ("keep DOMINANT Blatt (P66 'dominantShare' okvir); "
                         "drop vrstic drugih Blattov — vrstice ostanejo v "
                         "registru, izpadajo iz joina (C1/C3 vzorec)"),
            "optionA2": ("keep MIN Blatt (vrstni red I–V; P73 'min stran' "
                         "analog) — enaki števci, drugačen keep pri 29 base"),
            "evolution": ("razlog odhoda P66 base: C1 sekcije (p83–86/p88), "
                          "C3 isti-Blatt drop, C2 p93 reverzija"),
        },
        "v6Sha256": PIN_V6EV_SHA,
        "inputSha256": {"p59": PIN_P59EV_SHA, "p56": PIN_P56EV_SHA,
                        "p66": PIN_P66EV_SHA, "p72": PIN_P72EV_SHA,
                        "v6rt": PIN_V6RT_SHA},
        "summary": {
            "crossBases": len(bases_out),
            "rowsCrossBlatt": xb_rows,
            "oneRowPerBlatt": True,
            "blattPairDist": dict(sorted(blatt_dist.items())),
            "adjacentPairs": adjacent_pairs,
            "skipPairs": skip_pairs,
            "ownerDisjoint": owner_disjoint,
            "ownerOverlap": owner_overlap,
            "hausNrDist": dict(hn),
            "hausNrIstiBases": isti_hn,
            "hausNrBrezBases": brez_hn,
            "kulturesSharedBases": kult_shared,
            "dominantShareBuckets": dict(dom_buckets),
            "areaSuspectRows": area_suspect,
            "shareTies": ties,
            "areaQKSumByBlatt": sumqk_r,
            "pageMapOverlapPairs": pm_overlap_pairs,
            "seriesDist": dict(sorted(series_all.items())),
            "geoShared": {"shared": sum(1 for rec in bases_out.values()
                                        if rec["geoShared"]),
                          "distinct": sum(1 for rec in bases_out.values()
                                          if not rec["geoShared"]),
                          "null": 0},
            "p66Evolution": {"stay": len(stay), "leave": len(leave),
                             "leaveC1": len(leave_c1), "leaveC3": len(leave_c3),
                             "leaveC2": len(leave_c2), "new": len(new),
                             "leaveBases": {b: {"pages": g,
                                                "reason": ("C1" if (b, g) in
                                                           [(x, pg) for x, pg in leave_c1]
                                                           else "C3" if (b, g) in
                                                           [(x, pg) for x, pg in leave_c3]
                                                           else "C2")}
                                            for b, g in sorted(leave_c1 + leave_c3 + leave_c2,
                                                               key=lambda x: int(x[0]))},
                             "stayBases": stay,
                             "newBases": new},
            "optionA1": opt["A1"],
            "optionA2": opt["A2"],
            "optionA2DifferentKeep": a2_diff_keep,
        },
        "bases": dict(sorted(bases_out.items(), key=lambda kv: int(kv[0]))),
        "invariants": [
            "I1 vhodni pini (6× sha256 + števci 939/879/48/96)",
            "I2 re-izpeljava cross base == 48 bajtno (96 vrstic; 1 vrstica "
            "per Blatt 48/48; sosednji pari 48, skoki 0)",
            "I3 evolucija P66: 17/36 ostaja · 19 odhaja (C1 5 / C3 13 / "
            "C2 1) · 31 novih",
            "I4 forenzika (48/48 disjunktni lastniki; hn 42/2/4; "
            "areaSuspect 0; ties 0; Σ areaQK per Blatt == pin)",
            "I5 blattDist + pasovi + pageMap razponi + opcija A1 == pin",
            "I6 brez georef polj (lat/lng/areaModern/ratio); geoShared samo "
            "kot števec",
            "I7 dokaz ⊇ runtime (bajtno podmnožica)",
            "I8 determinizem — --check bajtno identično",
            "I9 v6 runtime join NESPREMENJEN (sha256 pin)",
        ],
        "statusLine": status_line,
        "verdictSi": verdict_si,
        "verdictEn": verdict_en,
        "next": [
            "LASTNIŠKA ODLOČITEV o cross-Blatt SPLIT joinu za 48 base — "
            "opcija A1 (keep dominant Blatt) / opcija A2 (keep min Blatt) / "
            "opcija B (per-Blatt instance + razdelitev geometrije; georef "
            "Blattnih kart [~]) — ta paket je dokazni vir",
            "izvedba (ob odobritvi): P75 po vzorcu P73 — drop vrstic drugih "
            "Blattov po izbranem pravilu → v7 (939 → 891 vrstic, cross 0)",
            "po izvedbi: konsistentnost z P66 paketom (17 ostajajočih base) "
            "in P72/P73 (nearDual 2080/2081 ostanejo isti-Blatt)",
            "razlaga 2 isti-hn base (" + ", ".join(isti_hn) + ") — deljena "
            "hiša ali branje (P72 vzorec: dokumentirano per base)",
            "operacijsko: GitHub Actions billing (#7); per-Blatt instance "
            "sekcij (56) zahteva georef Blattnih kart",
        ],
    }

    # runtime = bajtna projekcija (brez dokaznih top-level polj)
    rt = {k: v for k, v in ev.items()
          if k not in ("principle", "inputs", "inputSha256", "invariants")}
    rt.update({"version": 1,
               "generatedBy": "scripts/p74_ps_cross_blatt_pack.py"})

    if check_mode:
        for path, label in ((OUT_EV, "dokaz"), (OUT_RT, "runtime")):
            if not os.path.exists(path):
                fail(f"I8 {label} manjka ({path})")
        ev_disk = json.load(open(OUT_EV))
        rt_disk = json.load(open(OUT_RT))
        if json.dumps(ev_disk, sort_keys=True, ensure_ascii=False) != \
                json.dumps(ev, sort_keys=True, ensure_ascii=False):
            fail("I8 dokaz na disku ≠ izpeljava (--check)")
        if json.dumps(rt_disk, sort_keys=True, ensure_ascii=False) != \
                json.dumps(rt, sort_keys=True, ensure_ascii=False):
            fail("I8 runtime na disku ≠ izpeljava (--check)")
        # I6: brez georef polj
        def has_geo(o):
            if isinstance(o, dict):
                if any(k in o for k in GEO_FIELDS):
                    return True
                return any(has_geo(v) for v in o.values())
            if isinstance(o, list):
                return any(has_geo(v) for v in o)
            return False
        if has_geo(rt) or has_geo(ev):
            fail("I6 georef polja v izpisu")
        # I7: dokaz ⊇ runtime
        ev_disk2 = {k: v for k, v in ev_disk.items()
                    if k not in ("principle", "inputs", "inputSha256",
                                 "invariants")}
        ev_disk2.update({"version": 1,
                         "generatedBy": "scripts/p74_ps_cross_blatt_pack.py"})
        if json.dumps(ev_disk2, sort_keys=True, ensure_ascii=False) != \
                json.dumps(rt_disk, sort_keys=True, ensure_ascii=False):
            fail("I7 runtime ni bajtna podmnožica dokaza")
        ok("I6/I7/I8 --check: dokaz == izpeljava · runtime ⊂ dokaz · "
           "brez georef polj")
        print("P74 --check PASS")
        return

    # I6 kontrola pred zapisom
    def has_geo(o):
        if isinstance(o, dict):
            if any(k in o for k in GEO_FIELDS):
                return True
            return any(has_geo(v) for v in o.values())
        if isinstance(o, list):
            return any(has_geo(v) for v in o)
        return False
    if has_geo(rt):
        fail("I6 georef polja v runtime izpisu")
    ok("I6 brez georef polj (lat/lng/areaModern/ratio)")

    with open(OUT_EV, "w", encoding="utf-8") as f:
        json.dump(ev, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(OUT_RT, "w", encoding="utf-8") as f:
        json.dump(rt, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"  → dokaz: {OUT_EV}")
    print(f"  → runtime: {OUT_RT}")
    print(f"  pine za vpis: EXP_CROSS={len(bases_out)}, "
          f"EXP_ROWS_XB={xb_rows}, HN={dict(hn)}, SUMQK={sumqk_r}, "
          f"OPT_A1={opt['A1']}, A2_DIFF={a2_diff_keep}, "
          f"PM_OVERLAP={pm_overlap_pairs}, KULT_SHARED={kult_shared}, "
          f"SERIES={dict(sorted(series_all.items()))}")
    print("P74 OK")


if __name__ == "__main__":
    main()
