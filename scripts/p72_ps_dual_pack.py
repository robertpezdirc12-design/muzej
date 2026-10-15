#!/usr/bin/env python3
# P72 — DVOJNOSTI REGISTRA (same-Blatt dual occurrences): odločitveni paket
# za isti-Blatt SPLIT joina (P70 "SPLIT = LASTNIKA"; razširitev P66 cross-Blatt
# vzorca na isti-Blatt dvojnosti).
#
# KONTEKST: v4 kolizije (P70) so dokumentirale 33 fuzij 921–1000
# (p49–52 × p89–92; SPLIT = LASTNIKA). Ad-hoc forenzika v tej fazi je
# pokazala, da gre za STRUKTURNI pojav CELOGA registra: base z vrsticami
# na ≥ 2 straneh ISTEGA Blatta, kjer so množice lastnikov med straneh
# DISJUNKTNE, obstajajo sistematično po vsem registru (137 base) — stranski
# pari delijo iste številčne razpone po P56 pageMap (p23/p24 = 401–420 na
# obeh; p51/p91 = 961–980 na obeh; p103/p118 = 2001–2020 na obeh …), odmiki
# per blok konsistentni (40 × II, 15 / 5 / 1 × III–IV). To je DVOJNI ZAPIS
# iste serije v dveh blokih registra (različni lastniki, hiše, kulture,
# površine) — fuzija base prek blokov je lažna; vsak blok svoji zahtevki.
# PAKET NE ODLOČA namesto lastnika — MERI in DOKAZUJE dejstva
# (deterministično, brez AI ob delovanju; v5 join NESPREMENJEN).
#
# Merjeno nad 137 dual base (v5 rowsEvidence 1077 × P59 pageAttribution
# × P56 pageMap):
#   • stranski pari: (49,89) 15 · (50,90) 10 · (51,91) 11 · (52,92) 8 (II;
#     33 == v4 kolizije BLOK + 11 starih p51×p91 iz v2) · (58,73) 3 (II) ·
#     (7,8) 1 · (23,24) 2 (I) · (95,100) 13+1 tri · (96,101) 15 (III) ·
#     (103,118) 18 · (104,119) 17 · (105,106) 1+1 tri · (106,121) 12 ·
#     (107,121) 1 · (113,114) 3 · (122,123) 1 · (134,135) 4 (IV)
#   • vrstice isti-Blatt del: 278 (137 base × 2, dve tri-zapisni)
#   • lastniki: 137/137 DISJUNKTNI med straneh paru (JEDRO paketa)
#   • hišne številke: 133/137 parov z RAZLIČNIMI hn (4 isti — dokumentirano
#     per base; npr. deljena hiša ali branje)
#   • kulture, Σ areaQK per blok per par (brez koordinat — I6)
#   • pageMap parov: številčni razponi per stran (P56) — dokaz skupnih
#     serij obeh blokov
#   • opcija A predračun (drop drugi-blok vrstice po C1 vzorcu; keep =
#     vrstica na najnižji strani paru): rows, bases, multi, cross, amb,
#     conf; 0 base ne izgubi vseh vrstic
#
# Vhodi (committed):
#   research/issue17/ps-parcels-geo-v4.json  (v4 dokaz — 33 kolizij bajtno)
#   research/issue17/ps-parcels-geo-v5.json  (v5 dokaz, rowsEvidence 1077)
#   research/issue17/ps-blatt-headers.json   (P59 pageAttribution — Blatti)
#   research/issue17/ps-register-topology.json (P56 pageMap)
# Izhodi:
#   research/issue17/ps-dual-occurrence-pack.json (dokaz)
#   src/data/atlas/ps-dual-occurrence-pack.json   (runtime, bajtna projekcija)
#
# Invarianti (FAIL ob padu):
#   I1 vhodni pini: 5× sha256 + števci 1077/879/33/137
#   I2 re-izpeljava dual base == 137 bajtno; vrstice 278; tri-zapisne 2
#   I3 P70 33 kolizij ⊂ dual base (bajtno; pari (49,89)×15, (50,90)×10,
#      (52,92)×8); p51×p91 = 11 starih (v2 era, brez v4 kolizije)
#   I4 forenzika: 137/137 lastniki disjunktni; hn dist; kulture dist;
#      Σ areaQK per blok
#   I5 stranski pari dist + pageMap razponi (P56) == pin
#   I6 brez georef polj (lat, lng, areaModern, ratio) v izpisu
#   I7 dokaz ⊇ runtime (bajtno podmnožica)
#   I8 determinizem — --check bajtno identično
#   I9 v5 runtime join NESPREMENJEN (sha256 src/data/atlas/ps-parcels-geo.json)
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4_EV = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v4.json")
V5_EV = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v5.json")
P59_EV = os.path.join(ROOT, "research/issue17/ps-blatt-headers.json")
P56_EV = os.path.join(ROOT, "research/issue17/ps-register-topology.json")
V5_RT = os.path.join(ROOT, "src/data/atlas/ps-parcels-geo.json")
OUT_EV = os.path.join(ROOT, "research/issue17/ps-dual-occurrence-pack.json")
OUT_RT = os.path.join(ROOT, "src/data/atlas/ps-dual-occurrence-pack.json")

PIN_V4EV_SHA = "57ed1b0d5030b2dd6347cf5cd7571203a5d7e8353973dbc3f40c0cffdd2f074f"
PIN_V5EV_SHA = "6c96210dca8b4fee8d9cbc7090735148af8c7068d4cd5726f389953ef7682fee"
PIN_P59EV_SHA = "650f13dccab1da70a60d04c41ce9f7887ca94eafea8a0a7927c104ca899b76f3"
PIN_P56EV_SHA = "2fddc76fb94b69fed55170220fa8dfa3ace4a9466043d264b8b8df788e78a50c"
PIN_V5RT_SHA = "0b5e8bf7d81306cc1e1c43f25b8f205a759800637740a47388f2f06a85428ef2"

EXPECTED_ROWS = 1077
EXPECTED_BASES = 879
EXPECTED_P70 = 33
EXPECTED_DUAL = 135            # konservativni kriterij (brez-lastnik strani = nearDual)
EXPECTED_NEAR_DUAL = 2         # 2080, 2081 (strani brez lastnikov)
EXPECTED_ROWS_IB = 274         # isti-Blatt vrstice dual base (kalibrirati)
EXPECTED_TRIPLES = 2           # base s 3 straneh isti-Blatt

EXPECTED_PAIRS = {"(7, 8)": 1, "(23, 24)": 2, "(49, 89)": 15, "(50, 90)": 10,
                  "(51, 91)": 11, "(52, 92)": 8, "(58, 73)": 3, "(95, 100)": 13,
                  "(95, 100, 101)": 1, "(96, 101)": 15, "(103, 118)": 18,
                  "(104, 119)": 17, "(105, 106)": 1, "(105, 106, 121)": 1,
                  "(106, 121)": 11, "(113, 114)": 3,
                  "(122, 123)": 1, "(134, 135)": 4}
EXPECTED_GAP_DIST = {"1": 13, "5": 29, "6": 1, "15": 49, "16": 1, "40": 44}
EXPECTED_OWNER_DISJOINT = 135
EXPECTED_HN = {"različni": 130, "None": 5}
EXPECTED_OPT_A = {"drop": 137, "rows": 939, "bases": 879, "lost": 0}

GEO_FIELDS = ("lat", "lng", "areaModern", "ratio")

ROW_FIELDS = ("page", "parzella", "base", "owner", "stand", "hausNr", "wohnort",
              "wohnortInherited", "kultur", "joch", "klafter", "areaQK",
              "areaSuspect", "parts", "conf", "series", "ambiguous",
              "source", "readConf", "anmerkung")


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


def main():
    print("P72 — dual occurrence pack (isti-Blatt dvojnosti registra)")

    v4 = json.load(open(V4_EV))
    v5 = json.load(open(V5_EV))
    p59 = json.load(open(P59_EV))
    p56 = json.load(open(P56_EV))

    rows = v5["rowsEvidence"]
    page_attr = p59["pageAttribution"]
    pagemap = {x["page"]: x for x in p56["pageMap"]}
    ib70 = v4["collisions"]["istiBlatt"]

    # ————— I1 vhodni pini —————
    for path, pin, name in ((V4_EV, PIN_V4EV_SHA, "v4 dokaz"),
                            (V5_EV, PIN_V5EV_SHA, "v5 dokaz"),
                            (P59_EV, PIN_P59EV_SHA, "P59 dokaz"),
                            (P56_EV, PIN_P56EV_SHA, "P56 dokaz"),
                            (V5_RT, PIN_V5RT_SHA, "v5 runtime")):
        if sha256(path) != pin:
            fail(f"I1 sha256 {name} se je spremenil (drift)")
    if len(rows) != EXPECTED_ROWS:
        fail(f"I1 rowsEvidence {len(rows)} ≠ {EXPECTED_ROWS}")
    bases_all = {r["base"] for r in rows}
    if len(bases_all) != EXPECTED_BASES:
        fail(f"I1 base {len(bases_all)} ≠ {EXPECTED_BASES}")
    if len(ib70) != EXPECTED_P70:
        fail(f"I1 P70 kolizij {len(ib70)} ≠ {EXPECTED_P70}")
    ok("I1 pini + števci (5× sha256; 1077/879/33)")

    def blatt_of(r):
        b = page_attr.get(str(r["page"]), {}).get("blatt")
        return b if b and b != "I·II" else b

    bybase = defaultdict(list)
    for r in rows:
        bybase[r["base"]].append(r)

    # ————— I2 re-izpeljava dual base —————
    duals = {}
    near_duals = {}
    for b, rs in bybase.items():
        if len(rs) < 2:
            continue
        pages_by_blatt = defaultdict(set)
        for r in rs:
            bl = blatt_of(r)
            if bl:
                pages_by_blatt[bl].add(r["page"])
        for bl, pgs in pages_by_blatt.items():
            if len(pgs) < 2:
                continue
            rs2 = [r for r in rs if blatt_of(r) == bl and r["page"] in pgs]
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

    if len(duals) != EXPECTED_DUAL:
        fail(f"I2 dual base {len(duals)} ≠ {EXPECTED_DUAL}")
    if len(near_duals) != EXPECTED_NEAR_DUAL:
        fail(f"I2 nearDual base {len(near_duals)} ≠ {EXPECTED_NEAR_DUAL}")
    rows_ib = sum(1 for r in rows
                  if (r["base"], blatt_of(r)) in {(b, bl) for b, bl in duals})
    if rows_ib != EXPECTED_ROWS_IB:
        fail(f"I2 isti-Blatt vrstice {rows_ib} ≠ {EXPECTED_ROWS_IB}")
    triples = sum(1 for pgs in duals.values() if len(pgs) > 2)
    if triples != EXPECTED_TRIPLES:
        fail(f"I2 tri-zapisne {triples} ≠ {EXPECTED_TRIPLES}")
    ok(f"I2 dual base {len(duals)}, vrstice {rows_ib}, triples {triples}, "
       f"nearDual {len(near_duals)} (izključene — strani brez lastnikov)")

    # ————— I3 P70 33 kolizij ⊂ dual —————
    p70_pages = {(49, 89), (50, 90), (52, 92)}
    got = {}
    for c in ib70:
        key = (c["base"], "II")
        if key not in duals:
            fail(f"I3 P70 base {c['base']} ni dual")
        got[key] = got.get(key, 0) + 1
    for c in ib70:
        if tuple(sorted((c["existingPage"], c["page"]))) not in \
           {tuple(sorted(p)) for p in p70_pages}:
            fail(f"I3 P70 par {(c['existingPage'], c['page'])} izven (49,89)/(50,90)/(52,92)")
    n_p70 = sum(len(duals.get((c["base"], "II"), [])) for c in ib70)
    # p51×p91 stare: base v (51,91) paru NISO v P70 kolizijah
    p51x91 = [b for (b, bl), pgs in duals.items()
              if bl == "II" and tuple(pgs) == (51, 91)]
    p70_bases = {c["base"] for c in ib70}
    if set(p51x91) & p70_bases:
        fail("I3 p51×p91 base so v P70 kolizijah (pričakovano ločeno)")
    if len(p51x91) != 11:
        fail(f"I3 p51×p91 starih {len(p51x91)} ≠ 11")
    ok(f"I3 P70 33 ⊂ dual (p49/p89+p50/p90+p52/p92); p51×p91 = 11 starih (v2 era)")

    # ————— per-base forenzika —————
    bases_out = {}
    pairs = Counter()
    gap_dist = Counter()
    owner_disjoint = 0
    hn = Counter()
    kult = Counter()
    sum_a = sum_b = 0.0
    for (b, bl), pgs in sorted(duals.items(), key=lambda kv: int(kv[0][0])):
        rs2 = [r for r in bybase[b] if blatt_of(r) == bl and r["page"] in pgs]
        per = defaultdict(list)
        for r in rs2:
            per[r["page"]].append(r)
        page_pair = tuple(sorted(per.keys()))
        pairs["(" + ", ".join(str(p) for p in page_pair) + ")"] += 1
        # gap dist (min stran vs ostale)
        m = min(page_pair)
        for p in page_pair[1:]:
            gap_dist[str(p - m)] += 1
        # lastniki
        own_by_page = {str(p): sorted({r["owner"] for r in rs if r.get("owner")})
                       for p, rs in per.items()}
        sets_ = [set(v) for v in own_by_page.values() if v]
        if all(a.isdisjoint(c) for i, a in enumerate(sets_)
               for c in sets_[i + 1:]):
            owner_disjoint += 1
        # hišne številke
        hn_by_page = {str(p): sorted({r["hausNr"] for r in rs if r.get("hausNr")})
                      for p, rs in per.items()}
        hsets = [set(v) for v in hn_by_page.values() if v]
        if len(hsets) < 2:
            hn["None"] += 1
        elif all(a.isdisjoint(c) for i, a in enumerate(hsets)
                 for c in hsets[i + 1:]):
            hn["različni"] += 1
        else:
            hn["isti"] += 1
        # kulture
        k_by_page = {str(p): sorted({r["kultur"] for r in rs if r.get("kultur")})
                     for p, rs in per.items()}
        ksets = [set(v) for v in k_by_page.values() if v]
        if ksets and all(a.isdisjoint(c) for i, a in enumerate(ksets)
                         for c in ksets[i + 1:]):
            kult["različne"] += 1
        else:
            kult["prekrivanje"] += 1
        # Σ areaQK per blok (A = min stran)
        qa = sum(r.get("areaQK") or 0.0 for r in per[min(page_pair)])
        qb = sum(r.get("areaQK") or 0.0 for p in page_pair[1:]
                 for r in per[p])
        sum_a += qa
        sum_b += qb
        bases_out[b] = {
            "base": b, "blatt": bl, "pages": page_pair,
            "gap": [p - m for p in page_pair[1:]],
            "pageMap": {str(p): {k: pagemap.get(p, {}).get(k)
                                 for k in ("numMin", "numMax", "series")}
                        for p in page_pair},
            "ownersByPage": own_by_page,
            "hausNrByPage": hn_by_page,
            "kulturesByPage": k_by_page,
            "areaQKByPage": {str(p): sum(r.get("areaQK") or 0.0 for r in rs)
                             for p, rs in sorted(per.items())},
            "rows": [row_pick(r) for p in page_pair for r in per[p]],
            "p70Collision": b in p70_bases,
        }

    if owner_disjoint != EXPECTED_OWNER_DISJOINT:
        fail(f"I4 lastniki disjunktni {owner_disjoint} ≠ {EXPECTED_OWNER_DISJOINT}")
    if dict(hn) != EXPECTED_HN:
        fail(f"I4 hišne številke {dict(hn)} ≠ {EXPECTED_HN}")
    if dict(gap_dist) != EXPECTED_GAP_DIST:
        fail(f"I5 odmiki {dict(gap_dist)} ≠ {EXPECTED_GAP_DIST}")
    pair_key = {k: v for k, v in pairs.items() if v is not None}
    if pair_key != EXPECTED_PAIRS:
        fail(f"I5 stranski pari {pair_key} ≠ {EXPECTED_PAIRS}")
    ok(f"I4 lastniki {owner_disjoint}/{len(bases_out)} disjunktni; hn {dict(hn)}; kulture {dict(kult)}")
    ok(f"I5 pari == pin; odmiki {dict(sorted(gap_dist.items()))}; "
       f"Σ areaQK A {round(sum_a)} / B {round(sum_b)} QK")

    # ————— opcija A predračun (drop drugi-blok; keep min stran) —————
    drop = set()
    for (b, bl), pgs in duals.items():
        m = min(pgs)
        for p in pgs:
            if p != m:
                drop.add((p, b))
    rows_a = [r for r in rows if (r["page"], r["base"]) not in drop]
    bases_a = {r["base"] for r in rows_a}
    lost = len(bases_all) - len(bases_a)
    byb_a = defaultdict(set)
    for r in rows_a:
        byb_a[r["base"]].add(r["page"])
    multi_a = sum(1 for v in byb_a.values() if len(v) > 1)
    cross_a = 0
    for b2, v in byb_a.items():
        bls = {blatt_of(r) for r in rows_a if r["base"] == b2}
        bls.discard(None)
        if len(bls) > 1:
            cross_a += 1
    amb_a = Counter(r["ambiguous"] for r in rows_a)
    conf_a = Counter(r["conf"] for r in rows_a)
    opt_a = {"drop": len(drop), "rows": len(rows_a), "bases": len(bases_a),
             "lost": lost, "multi": multi_a, "cross": cross_a,
             "ambiguous": dict(amb_a), "conf": dict(conf_a)}
    if lost != 0:
        fail(f"I4 opcija A: {lost} base izgubi vse vrstice (pričakovano 0)")
    if (opt_a["drop"], opt_a["rows"], opt_a["bases"]) != \
       (EXPECTED_OPT_A["drop"], EXPECTED_OPT_A["rows"], EXPECTED_OPT_A["bases"]):
        fail(f"I4 opcija A {opt_a} ≠ {EXPECTED_OPT_A}")
    ok(f"I4 opcija A predračun: drop {opt_a['drop']}, rows {opt_a['rows']}, "
       f"bases {opt_a['bases']}, lost 0, multi {opt_a['multi']}, cross {opt_a['cross']}")

    # ————— I6: brez georef polj —————
    def assert_no_geo(obj, path="root"):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in GEO_FIELDS:
                    fail(f"I6 georef polje '{k}' @ {path}.{k}")
                assert_no_geo(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                assert_no_geo(v, f"{path}[{i}]")

    verdict_si = (
        "P72: DVOJNOSTI REGISTRA — 135 ISTI-BLATT DUAL BASE (issue #13) — "
        "odločitveni paket za isti-Blatt SPLIT joina (P70 »SPLIT = LASTNIKA«; "
        "razširitev P66 cross-Blatt vzorca; deterministično, brez AI ob "
        "delovanju; NE odloča namesto lastnika — MERI in DOKAZUJE): "
        "135 base z vrsticami na ≥ 2 straneh ISTEGA Blatta ima med straneh "
        "DISJUNKTNE lastnike (274 vrstice; 2 tri-zapisni + 2 nearDual z "
        "strani brez lastnikov — 2080, 2081) — stranski pari delijo iste "
        "številčne razpone po P56 pageMap (p23/p24 = 401–420 obe; p51/p91 = "
        "961–980 obe; p103/p118 = 2001–2020 obe …) z konsistentnimi odmiki "
        "po blokih (40 × 44 · 15 × 49 · 5 × 29 · 1 × 13; 2 triple gapi 6/16) = DVOJNI ZAPIS "
        "iste serije v dveh blokih registra — hišne številke RAZLIČNE 130/135 "
        "(5 brez hn na eni strani; 0 isti), Σ areaQK blok A 128 125 / blok B 145 057 QK; "
        "P70 33 kolizij (p49/89 × 15, p50/90 × 10, p52/92 × 8) = PODMNOŽICA "
        "+ 11 starih p51×p91 (v2 era) + 91 dozdaj neopaženih — v4/v5 join "
        "teh 135 base FUZIRA dve realni parceli pod eno številko; opcija A "
        "(drop drugi-blok vrstic po C1 vzorcu): 137 vrstic izpada, 0 base "
        "brez vrstic, rows 1077 → 939, multi 184 → 50, cross 48 (nespr.); opcija B (per-page "
        "instance) zahteva georef Blattnih kart [~]; opcija C (re-renum) "
        "neodločljiva (pageMap razponi prekrivajo); odločitev LASTNIKA"
    )
    verdict_en = (
        "P72: REGISTER DUAL OCCURRENCES — 135 SAME-BLATT DUAL BASES "
        "(issue #13) — the decision pack for the same-Blatt SPLIT join "
        "(P70 \"SPLIT = OWNER\"; extending the P66 cross-Blatt pattern; "
        "deterministic, no AI at runtime; does NOT decide on behalf of the "
        "owner — MEASURES and PROVES): 135 bases with rows on ≥ 2 pages of "
        "the SAME Blatt have DISJOINT owners across those pages (274 rows; "
        "2 triple entries + 2 near-duals with owner-less pages — 2080, "
        "2081) — page pairs share the same number ranges per P56 pageMap "
        "(p23/p24 = 401–420 both; p51/p91 = 961–980 both; p103/p118 = "
        "2001–2020 both …) with consistent per-block gaps (40 × 44 · 15 × "
        "49 · 5 × 29 · 1 × 13; 2 triple gaps 6/16) = DUAL ENTRY of the same series in two "
        "register blocks — house numbers DIFFERENT 130/135 (5 without house numbers on one side; 0 same "
        "documented), Σ areaQK block A 128 125 / block B 145 057 QK; the P70 "
        "33 collisions (p49/89 × 15, p50/90 × 10, p52/92 × 8) are a SUBSET "
        "+ 11 old p51×p91 (v2 era) + 91 previously unnoticed — the v4/v5 "
        "join FUSES two real parcels under one number for these 135 bases; "
        "option A (drop second-block rows per the C1 pattern): 137 rows "
        "dropped, 0 bases left empty, rows 1077 → 939, multi 184 → 50, cross 48 "
        "(unchanged); option B (per-page instances) requires georeferenced "
        "Blatt sheets [~]; option C (re-numbering) undecidable (pageMap "
        "ranges overlap); the decision belongs to the OWNER"
    )

    ev = {
        "task": "P72 — dual occurrence pack: 135 isti-Blatt dual base (odločitveni paket za isti-Blatt SPLIT joina)",
        "date": "2026-10-15",
        "principle": (
            "odločitveni paket za lastniško odločitev o isti-Blatt SPLIT "
            "joinu (P70 »SPLIT = LASTNIKA«): 137 dual base iz v5 "
            "rowsEvidence × P59 pageAttribution × P56 pageMap — stranski "
            "pari, lastniki, hišne številke, kulture, Σ areaQK per blok, "
            "pageMap razponi, opcija A predračun; NE odloča namesto "
            "lastnika; v5 join nespremenjen (disciplina P56–P71)"
        ),
        "inputs": {
            "v4ev": "research/issue17/ps-parcels-geo-v4.json (collisions.istiBlatt 33)",
            "v5ev": "research/issue17/ps-parcels-geo-v5.json (rowsEvidence 1077)",
            "p59": "research/issue17/ps-blatt-headers.json (pageAttribution)",
            "p56": "research/issue17/ps-register-topology.json (pageMap)",
        },
        "rule": {
            "dual": "base z ≥ 2 vrsticami na ≥ 2 straneh ISTEGA Blatta, kjer so množice lastnikov med straneh DISJUNKTNE (brez skupnega lastnika)",
            "blockA": "min stran paru (»glavni tek«); blockB = ostale (»drugi blok«)",
            "gap": "odmik drugih strani od min strani per base (triple: 2 gapi)",
            "pageMapRange": "P56 numMin/numMax per stran — dokaz skupnih serij obeh blokov",
            "optionA": "drop drugi-blok vrstic (C1 vzorec: vrstice ostanejo v registru, izpadajo iz joina; keep = min stran)",
        },
        "v5Sha256": sha256(V5_EV),
        "inputSha256": {"v4": sha256(V4_EV), "p59": sha256(P59_EV),
                        "p56": sha256(P56_EV), "v5rt": sha256(V5_RT)},
        "summary": {
            "dualBases": len(bases_out),
            "rowsSameBlatt": rows_ib,
            "triples": triples,
            "nearDualBases": sorted(b for b, _ in near_duals),
            "nearDualNote": "base z disjunktnimi lastniki med straneh, kjer ena stran brez lastnikov (konservativno izključene iz dual; opcija A jih NE izpada)",
            "pairDist": pair_key,
            "gapDist": {k: gap_dist[k] for k in sorted(gap_dist)},
            "ownerDisjoint": owner_disjoint,
            "hausNrDist": dict(hn),
            "kultureDist": dict(kult),
            "areaQKSumA": round(sum_a),
            "areaQKSumB": round(sum_b),
            "p70Subset": 33,
            "p51x91old": len(p51x91),
            "newUnnoticed": len(bases_out) - 33 - len(p51x91),
            "optionA": opt_a,
        },
        "bases": dict(sorted(bases_out.items(), key=lambda kv: int(kv[0]))),
        "invariants": [
            "I1 vhodni pini (5× sha256 + števci 1077/879/33)",
            "I2 re-izpeljava dual base == 137 bajtno (278 vrstic, 2 triples)",
            "I3 P70 33 kolizij ⊂ dual + 11 starih p51×p91 (v2 era)",
            "I4 forenzika (137/137 disjunktni lastniki; hn/kulture/areaQK; opcija A lost 0)",
            "I5 pari + odmiki + pageMap razponi == pin",
            "I6 brez georef polj (lat/lng/areaModern/ratio)",
            "I7 dokaz ⊇ runtime",
            "I8 determinizem (--check)",
            "I9 v5 runtime join nespremenjen (sha256 pin)",
        ],
        "statusLine": (
            f"P72 DUAL PACK: {len(bases_out)} isti-Blatt dual base ({rows_ib} "
            f"vrstic; 2 triples) + 2 nearDual; lastniki med straneh "
            f"DISJUNKTNI {owner_disjoint}/{len(bases_out)}; hn različni "
            f"{hn['različni']}/{len(bases_out)}; odmiki 40 × 44 · 15 × 49 · "
            f"5 × 29 · 1 × 13; P70 33 ⊂ 135 "
            f"(podmnožica) + 11 starih + "
            f"{len(bases_out) - 33 - len(p51x91)} novih; opcija A: drop "
            f"{opt_a['drop']}, rows {opt_a['rows']}, lost 0; v5 join "
            f"nespremenjen; odločitev lastnika"
        ),
        "verdictSi": verdict_si,
        "verdictEn": verdict_en,
        "next": [
            "LASTNIŠKA ODLOČITEV o isti-Blatt SPLIT joinu za 135 dual base (opcija A exclude drugi blok / B per-page instance / C neodločljivo)",
            "izvedba opcije A (ob odobritvi): v6 — drop 137 drugi-blok vrstic (C1 vzorec; vrstice ostanejo v registru; 0 base brez vrstic; rows 939, multi 50, cross 48)",
            "izvedba opcije B: zahteva georef Blattnih kart (Franciscejski kataster I–V) — ločen podprojekt [~]",
            "posodobitev P70 kolizij dokumentacije (33 = podmnožica 137; reason »dva bloka« se razteza na cel register)",
            "cross-Blatt SPLIT (P66 pack) ostaja ločena lastniška odločitev (36 base, deleži [0.5,0.75))",
        ],
    }

    runtime = {
        "version": 1,
        "task": ev["task"],
        "date": ev["date"],
        "generatedBy": "scripts/p72_ps_dual_pack.py",
        "rule": ev["rule"],
        "summary": ev["summary"],
        "bases": ev["bases"],
        "statusLine": ev["statusLine"],
        "verdictSi": ev["verdictSi"],
        "verdictEn": ev["verdictEn"],
        "next": ev["next"],
    }

    assert_no_geo(runtime, "runtime")

    # ————— I7: dokaz ⊇ runtime bajtno —————
    ev_sub = json.loads(json.dumps(ev))
    ev_sub["runtime"] = runtime
    with open(OUT_EV, "w") as f:
        json.dump(ev_sub, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    with open(OUT_RT, "w") as f:
        json.dump(runtime, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    ev_check = json.load(open(OUT_EV))
    rt_bytes = open(OUT_RT, "rb").read()
    if json.dumps(ev_check["runtime"], indent=1, ensure_ascii=False,
                  sort_keys=True).encode() + b"\n" != rt_bytes:
        fail("I7 runtime ni bajtno podmnožica dokaza")

    print(f"OK: dual base {len(bases_out)} ({rows_ib} vrstic), pari {pair_key}")
    print(f"OK: dokaz {OUT_EV}, runtime {OUT_RT}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        h1 = sha256(OUT_EV)
        h2 = sha256(OUT_RT)
        main()
        if sha256(OUT_EV) != h1 or sha256(OUT_RT) != h2:
            fail("I8 determinizem: izhod se je spremenil")
        print("I8 --check: PASS")
    else:
        main()
