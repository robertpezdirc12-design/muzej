#!/usr/bin/env python3
# P76 — LOKALNE SEKCIJE: per-Blatt instance odločitveni paket (56 vrstic,
# p83–86 + p88; odprta lastniška točka P70 ① / P71 C1; vzorec P72/P74 —
# paket MERI, NE odloča).
#
# KONTEKST: P69 je klasificiral 56 vrstic na straneh 83/84/85/86/88 kot
# "lokalne sekcije" — pisane številke 161–181 / 641–660 / 721–740 trčijo z
# KO-globalnimi teki (p11 Blatt I 161–183; p35 641–660; p40 721–740) in s
# Blatt II glavnim tekom (p61 161–180). P71 C1 jih je EXCLUDE iz joina
# (dokazane lažne fuzije: Σ ratio 161 = 235.65×; hiše p85 r641 Hi16 vs p35
# r641 Hi68). Opcija "per-Blatt instance ločeno (P39; potrebuje P60 moda B /
# PF protokol identiteto sekcij)" ostaja odprta. Ta paket MERI celotno
# identitetno strukturo nad v7 univerzumom (deterministično, brez AI ob
# delovanju; v7 join NESPREMENJEN — disciplina P56–P75).
#
# Merjeno nad 56 sekcij vrsticami / 31 base (v7 rowsEvidence 891 × P69
# sectionClass × v3 rowsEvidence 1079 × P59 pageAttribution × P56 pageMap ×
# P60 perblatt-attribution):
#   • strukture: p83 13 · p84 12 · p85 14 · p86 14 · p88 3; vse strane
#     Blatt II (P59 5/5); Σ areaQK p83 3708 · p84 10273 · p85 10333 ·
#     p86 9544 · p88 4659 (Σ 38517)
#   • counterpar v v7: 31/31 base ima TOČNO 1 preživelo vrstico
#     (posledica C1 + C3 + C4): 23 Blatt I (p10 1 · p11 5 · p35 14 ·
#     p40 3) + 8 Blatt II (p61 8); vsi 31 z geometrijo (C1 I4 nasledstvo:
#     0 poligonov praznih); conf STRONG 4 / MEDIUM 21 / WEAK 6
#   • evolucija C4: 13/31 base je bilo v v6 cross-Blatt setu (I p11 × II
#     p61) — 8 obdržalo II (161–165, 174, 176, 179), 5 obdržalo I (166,
#     168, 171, 173, 175); 18/31 single-Blatt (160 p10 · 641–659 p35 ·
#     736–738 p40)
#   • JEDRO — identitetna disjunktnost: lastniki sekcija×counterpar
#     0 prekrivanj (56/51 parov base-nivo: 0/31 base) + sekcija×sekcija
#     (isti base, različni strani) 0 prekrivanj; hišne številke isti 0 /
#     različni 31 (31/31 base z hn na obeh straneh) — razširitev P69
#     vzorca (p85 641 Hi16 vs p35 641 Hi68) na CELOTNO množico
#   • P56 pageMap ponovitev bandov (5/5): p83 161–181 / p84 162–182 /
#     p86 160–180 ⊆ [p11 161–183 · p61 161–180]; p85 641–660 == p35;
#     p88 721–740 == p40
#   • P60 moda B band: 8/31 base attributed (163, 176 → inBand strane
#     [61, 83, 84, 86]; 644, 653–657 → inBand [85]) — 12/56 vrstic z
#     band identiteto; 44 [~] brez (PF protokol = manjkajoči vir, ni v
#     repu — P60/P61/P63–P68 next)
#   • v3 forenzika lažnih fuzij (56 vrstic v v3 rowsEvidence): geoShared
#     56/56 (sekcija je delila geometrijo sodobne parcele s counterparom);
#     ratio dist: moda B [0.8, 1.25] 11 · moda A [3.3, 4.3] 5 · absurdni
#     > 4.3 20 (max 134.6786) · median 2.5442; areaSuspect 1; conf
#     STRONG 3 / MEDIUM 42 / WEAK 11 (v3 — lažno); kulture Alm 9 ·
#     Dingf. 6 · Wein 3 … (specifične sekcije); wohnort 56/56
#   • OPCIJE (predračun nad v7, merjeno — izbira LASTNIŠKA):
#     A  status quo (v7): rows 891 / bases 879 / multiPage 2 / crossBlatt 0
#        / ambRows 4 — sekcije v registru brez geometrije (dokaz P69)
#     B1 re-admisija vseh 56 kot vrstic (base-ključ, brez geometrije):
#        rows 947 / multiPage 33 / crossBlatt 23 / ambRows 91 — crossBlatt
#        23 KRŠI C4 NIL-CLAIM (23 base dobi vrstici na I in II) →
#        OBVEZEN per-instanca ključ (base, stran) za sekcije: z njim
#        crossBlatt 0 / multiPage 2 / ambRows 4 (nespremenjeno)
#     B2 samo P60 band subset (12 vrstic, 8 base): rows 903 / multiPage 10
#        / crossBlatt 6 / ambRows 24 (isti problem, manjši); z instance
#        ključem crossBlatt 0 / multiPage 2 / ambRows 4; 44 vrstic ostane
#        izključenih [~]
#     B3 geometrija per Blatt: ZAHTEVA georef Blatt II sekcije karte +
#        PF protokol (vir ni v repu) — [~] neizvedljivo danes
#
# Vhodi (committed):
#   research/issue17/ps-pass1-layers.json         (P69 — sectionClass 56)
#   research/issue17/ps-parcels-geo-v3.json       (v3 dokaz — forenzika)
#   research/issue17/ps-parcels-geo-v7.json       (v7 dokaz — rowsEvidence 891)
#   research/issue17/ps-blatt-headers.json        (P59 pageAttribution)
#   research/issue17/ps-register-topology.json    (P56 pageMap)
#   research/issue17/ps-perblatt-attribution.json (P60 moda B baze)
#   src/data/atlas/ps-parcels-geo.json            (v7 runtime — I9 pin)
# Izhodi:
#   research/issue17/ps-sections-perblatt-pack.json (dokaz)
#   src/data/atlas/ps-sections-perblatt-pack.json   (runtime, bajtna projekcija)
#
# Invarianti (FAIL ob padu):
#   I1 vhodni pini: 6× sha256 dokazov + v7 runtime sha (I9) + števci
#      (sectionClass 56; v3 1079; v7 891/879; P60 bases 14)
#   I2 re-izpeljava sekcij == P69 sectionClass.rows bajtno (56; strani
#      83×13 / 84×12 / 85×14 / 86×14 / 88×3; 31 base); 56/56 najdenih v
#      v3 rowsEvidence (page+base+owner; areaQK == P69)
#   I3 univerzum: sekcije vse Blatt II (5/5); counterpar 31/31 točno 1
#      vrstica (Blatt I 23: p10 1/p11 5/p35 14/p40 3; Blatt II 8: p61 8);
#      lat/lng 31/31; conf STRONG 4/MEDIUM 21/WEAK 6; evolucija C4 13/18
#   I4 identiteta: lastniki sekcija×counterpar 0 (31/31 base); sekcija×
#      sekcija 0; hn isti 0 / različni 31; pageMap ponovitev 5/5
#   I5 forenzika v3: geoShared 56/56; ratio modaB 11/modaA 5/absurdni 20
#      (max pin); median pin; areaSuspect 1; conf 3/42/11; Σ areaQK per
#      stran == pin (Σ 38517); izpis BREZ lat/lng/areaModern
#   I6 P60 band: 8 base == pin; inBand strane == pin; rowsInBand 12
#   I7 opcije predračun == pin (A 891/2/0/4; B1 947/33/23/91 + instance
#      ključ 0/2/4; B2 903/10/6/24 + instance ključ 0/2/4; B3 neizvedljivo)
#   I8 determinizem — --check bajtno identično
#   I9 v7 runtime join NESPREMENJEN (sha256 pin)

import hashlib
import json
import os
import statistics
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P69_EV = os.path.join(ROOT, "research/issue17/ps-pass1-layers.json")
V3_EV = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v3.json")
V7_EV = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v7.json")
P59_EV = os.path.join(ROOT, "research/issue17/ps-blatt-headers.json")
P56_EV = os.path.join(ROOT, "research/issue17/ps-register-topology.json")
P60_EV = os.path.join(ROOT, "research/issue17/ps-perblatt-attribution.json")
V7_RT = os.path.join(ROOT, "src/data/atlas/ps-parcels-geo.json")
OUT_EV = os.path.join(ROOT, "research/issue17/ps-sections-perblatt-pack.json")
OUT_RT = os.path.join(ROOT, "src/data/atlas/ps-sections-perblatt-pack.json")

PIN_P69EV_SHA = "99962e24dc129a253e7100cb297aa6b73989f96b1d5ff7c95d55d8735c52829e"
PIN_V3EV_SHA = "af7479e428182f381d3a2537896493d7cf86210fac7027221e22ac2aea218b53"
PIN_V7EV_SHA = "4d701a71e2cd58a5cd8feefeec8534132ff717f8cb340ec20b4da1ba4a7aad6f"
PIN_P59EV_SHA = "650f13dccab1da70a60d04c41ce9f7887ca94eafea8a0a7927c104ca899b76f3"
PIN_P56EV_SHA = "2fddc76fb94b69fed55170220fa8dfa3ace4a9466043d264b8b8df788e78a50c"
PIN_P60EV_SHA = "2c2b2acec50e5410d489fa3d4cfbc866f4a02403f3d33fb33e425d3c75e5e8f2"
PIN_V7RT_SHA = "4bb4037064f427287061f592ee6ef75a497b1b4ddcf9a5e8173c911c9949234d"

EXPECTED_SEC_ROWS = 56
EXPECTED_SEC_PAGES = {"83": 13, "84": 12, "85": 14, "86": 14, "88": 3}
EXPECTED_SEC_BASES = 31
EXPECTED_V3_ROWS = 1079
EXPECTED_V7_ROWS = 891
EXPECTED_V7_BASES = 879
EXPECTED_P60_BASES = 14

EXPECTED_SEC_BLATT = "II"          # vseh 5 strani (P59)
EXPECTED_CP_TOTAL = 31
EXPECTED_CP_BLATT = {"I": 23, "II": 8}
EXPECTED_CP_PAGES = {"10": 1, "11": 5, "35": 14, "40": 3, "61": 8}
EXPECTED_CP_GEO = 31
EXPECTED_CP_CONF = {"STRONG": 4, "MEDIUM": 21, "WEAK": 6}
EXPECTED_C4_MEMBERS = 13
EXPECTED_C4_SINGLE = 18
EXPECTED_C4_KEPT_II = 8            # 161–165, 174, 176, 179
EXPECTED_C4_KEPT_I = 5             # 166, 168, 171, 173, 175

EXPECTED_OWNER_OVERLAP_CP = 0
EXPECTED_OWNER_OVERLAP_SEC = 0
EXPECTED_HN = {"isti": 0, "različni": 31}

EXPECTED_PAGEMAP_SEC = {"83": [161, 181], "84": [162, 182], "85": [641, 660],
                        "86": [160, 180], "88": [721, 740]}
EXPECTED_PAGEMAP_GLOB = {"11": [161, 183], "61": [161, 180], "35": [641, 660],
                         "40": [721, 740]}

EXPECTED_SUMQK = {"83": 3708, "84": 10273, "85": 10333, "86": 9544, "88": 4659}
EXPECTED_SUMQK_TOTAL = 38517
EXPECTED_V3_GEO_SHARED = 56
EXPECTED_V3_RATIO = {"n": 56, "modaB": 11, "modaA": 5, "absurdniGT43": 20,
                     "median": 2.5442, "max": 134.6786}
EXPECTED_V3_SUSPECT = 1
EXPECTED_V3_CONF = {"STRONG": 3, "MEDIUM": 42, "WEAK": 11}
EXPECTED_KULTURE_TOP = {"Wiese und Gfrett": 11, "Alm": 9, "Dingf.": 6,
                        "Aehn": 4, "Wies": 4, "Wein": 3, "Wald": 3, "Acker": 2}
EXPECTED_WOHNORT = 56
EXPECTED_P60_SEC_BASES = ["163", "176", "644", "653", "654", "655", "656", "657"]
EXPECTED_P60_INBAND_PAGES = {"163": [61, 83, 84, 86], "176": [61, 83, 84, 86],
                             "644": [85], "653": [85], "654": [85],
                             "655": [85], "656": [85], "657": [85]}
EXPECTED_ROWS_IN_BAND = 12

MODA_B = (0.8, 1.25)
MODA_A = (3.3, 4.3)

ROW_FIELDS = ("page", "parzella", "base", "owner", "stand", "hausNr",
              "wohnort", "wohnortInherited", "kultur", "joch", "klafter",
              "areaQK", "areaSuspect", "parts", "conf", "series",
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


def row_pick(r, fields=ROW_FIELDS):
    return {k: r.get(k) for k in fields if r.get(k) is not None}


def main():
    print("P76 — lokalne sekcije: per-Blatt instance pack (56 vrstic)")
    check_mode = "--check" in sys.argv

    p69 = json.load(open(P69_EV))
    v3 = json.load(open(V3_EV))
    v7 = json.load(open(V7_EV))
    p59 = json.load(open(P59_EV))
    p56 = json.load(open(P56_EV))
    p60 = json.load(open(P60_EV))

    sec_cls = p69["sectionClass"]["rows"]
    re3 = v3["rowsEvidence"]
    re7 = v7["rowsEvidence"]
    page_attr = p59["pageAttribution"]
    pagemap = {x["page"]: x for x in p56["pageMap"]}
    p60_bases = p60["bases"]

    def blatt_of(page):
        return page_attr.get(str(page), {}).get("blatt")

    # ————— I1 vhodni pini —————
    pins = [(P69_EV, PIN_P69EV_SHA, "P69 dokaz"),
            (V3_EV, PIN_V3EV_SHA, "v3 dokaz"),
            (V7_EV, PIN_V7EV_SHA, "v7 dokaz"),
            (P59_EV, PIN_P59EV_SHA, "P59 dokaz"),
            (P56_EV, PIN_P56EV_SHA, "P56 dokaz"),
            (P60_EV, PIN_P60EV_SHA, "P60 dokaz")]
    for path, pin, label in pins:
        if sha256(path) != pin:
            fail(f"I1 {label} sha256 drift ({sha256(path)[:8]}… ≠ {pin[:8]}…)")
    ok("I1 pini (6× sha256 dokazov)")

    rt_sha = sha256(V7_RT)
    if rt_sha != PIN_V7RT_SHA:
        fail(f"I1 v7 runtime drift ({rt_sha[:8]}… ≠ {PIN_V7RT_SHA[:8]}…) — "
             "join se je spremenil brez P76 znanja")
    ok("I1 v7 runtime sha pin (I9 disciplina)")

    if len(sec_cls) != EXPECTED_SEC_ROWS:
        fail(f"I1 sectionClass {len(sec_cls)} ≠ {EXPECTED_SEC_ROWS}")
    if len(re3) != EXPECTED_V3_ROWS:
        fail(f"I1 v3 rowsEvidence {len(re3)} ≠ {EXPECTED_V3_ROWS}")
    if len(re7) != EXPECTED_V7_ROWS:
        fail(f"I1 v7 rowsEvidence {len(re7)} ≠ {EXPECTED_V7_ROWS}")
    if len({r["base"] for r in re7}) != EXPECTED_V7_BASES:
        fail("I1 v7 base števec drift")
    if len(p60_bases) != EXPECTED_P60_BASES:
        fail(f"I1 P60 bases {len(p60_bases)} ≠ {EXPECTED_P60_BASES}")
    ok(f"I1 števci (sekcije {EXPECTED_SEC_ROWS} / v3 {EXPECTED_V3_ROWS} / "
       f"v7 {EXPECTED_V7_ROWS} / P60 {EXPECTED_P60_BASES})")

    # ————— I2 re-izpeljava sekcij == P69 bajtno —————
    per_page = Counter(str(s["page"]) for s in sec_cls)
    if dict(per_page) != EXPECTED_SEC_PAGES:
        fail(f"I2 per-page {dict(per_page)} ≠ {EXPECTED_SEC_PAGES}")
    sec_bases = sorted({s["base"] for s in sec_cls}, key=int)
    if len(sec_bases) != EXPECTED_SEC_BASES:
        fail(f"I2 base {len(sec_bases)} ≠ {EXPECTED_SEC_BASES}")

    idx3 = defaultdict(list)
    for r in re3:
        idx3[(r["page"], r["base"], r["owner"])].append(r)
    sec_v3, missing, multi = [], [], []
    for s in sec_cls:
        hits = idx3.get((s["page"], s["base"], s["owner"]), [])
        if len(hits) == 1:
            sec_v3.append(hits[0])
        elif not hits:
            missing.append((s["page"], s["base"], s["owner"]))
        else:
            multi.append((s["page"], s["base"], len(hits)))
    if missing or multi:
        fail(f"I2 v3 match: missing {missing} multi {multi}")
    aq_mismatch = [1 for s, v in zip(sec_cls, sec_v3)
                   if (s.get("areaQK") or None) != (v.get("areaQK") or None)]
    if aq_mismatch:
        fail(f"I2 areaQK P69↔v3 mismatch {len(aq_mismatch)}")
    ok("I2 sekcije 56 bajtno == P69; 56/56 v v3 (areaQK ==)")

    # ————— I3 univerzum: Blatt II + counterparji v v7 + evolucija C4 —————
    for pg in EXPECTED_SEC_PAGES:
        b = blatt_of(int(pg))
        if b != EXPECTED_SEC_BLATT:
            fail(f"I3 stran {pg} blatt {b} ≠ {EXPECTED_SEC_BLATT}")

    c7 = defaultdict(list)
    for r in re7:
        c7[r["base"]].append(r)
    cp_blatt, cp_pages, cp_conf = Counter(), Counter(), Counter()
    cp_no_geo = []
    for b in sec_bases:
        rows = c7.get(b, [])
        if len(rows) != 1:
            fail(f"I3 base {b}: {len(rows)} v7 vrstic ≠ 1")
        r = rows[0]
        cp_blatt[blatt_of(r["page"])] += 1
        cp_pages[str(r["page"])] += 1
        cp_conf[r.get("conf")] += 1
        if r.get("lat") is None or r.get("lng") is None:
            cp_no_geo.append(b)
    if dict(cp_blatt) != EXPECTED_CP_BLATT:
        fail(f"I3 counterpar blatt {dict(cp_blatt)} ≠ {EXPECTED_CP_BLATT}")
    if dict(cp_pages) != EXPECTED_CP_PAGES:
        fail(f"I3 counterpar strani {dict(cp_pages)} ≠ {EXPECTED_CP_PAGES}")
    if cp_no_geo:
        fail(f"I3 counterparji brez geometrije: {cp_no_geo}")
    if dict(cp_conf) != EXPECTED_CP_CONF:
        fail(f"I3 counterpar conf {dict(cp_conf)} ≠ {EXPECTED_CP_CONF}")
    ok("I3 counterparji 31/31 (I 23 / II 8; lat/lng 31/31; conf 4/21/6)")

    v6 = json.load(open(os.path.join(ROOT, "research/issue17/ps-parcels-geo-v6.json")))
    re6 = v6["rowsEvidence"]
    c4drop = {(r["base"], r["page"]) for r in v7["removedRows"]}
    c4_members, c4_single, c4_kept_ii, c4_kept_i = [], [], 0, 0
    for b in sec_bases:
        blatts = sorted({blatt_of(r["page"]) for r in re6 if r["base"] == b})
        if len(blatts) == 1:
            c4_single.append(b)
            continue
        c4_members.append(b)
        kept = {blatt_of(r["page"]) for r in re6
                if r["base"] == b and (b, r["page"]) not in c4drop}
        if kept == {"II"}:
            c4_kept_ii += 1
        elif kept == {"I"}:
            c4_kept_i += 1
        else:
            fail(f"I3 base {b}: C4 kept {kept}")
    if len(c4_members) != EXPECTED_C4_MEMBERS or len(c4_single) != EXPECTED_C4_SINGLE:
        fail(f"I3 C4 {len(c4_members)}/{len(c4_single)} ≠ "
             f"{EXPECTED_C4_MEMBERS}/{EXPECTED_C4_SINGLE}")
    if c4_kept_ii != EXPECTED_C4_KEPT_II or c4_kept_i != EXPECTED_C4_KEPT_I:
        fail(f"I3 C4 kept II/I {c4_kept_ii}/{c4_kept_i} ≠ "
             f"{EXPECTED_C4_KEPT_II}/{EXPECTED_C4_KEPT_I}")
    ok(f"I3 evolucija C4: 13/31 cross (II 8 / I 5) · 18/31 single-Blatt")

    # ————— I4 identitetna disjunktnost + pageMap ponovitev —————
    ov_cp = sum(1 for s in sec_cls
                for r in c7[s["base"]]
                if s["owner"] and r.get("owner") and s["owner"] == r["owner"])
    if ov_cp != EXPECTED_OWNER_OVERLAP_CP:
        fail(f"I4 lastniki sekcija×counterpar {ov_cp} ≠ 0")
    by_sec_base = defaultdict(list)
    for s in sec_cls:
        by_sec_base[s["base"]].append(s)
    ov_sec = sum(1 for rows in by_sec_base.values()
                 for i, a in enumerate(rows)
                 for b2 in rows[i + 1:]
                 if a["owner"] == b2["owner"])
    if ov_sec != EXPECTED_OWNER_OVERLAP_SEC:
        fail(f"I4 lastniki sekcija×sekcija {ov_sec} ≠ 0")
    hn_isti, hn_raz = 0, 0
    hn_detail = {}
    for b in sec_bases:
        sec_hns = sorted({str(v.get("hausNr")) for v in sec_v3
                          if v["base"] == b and v.get("hausNr") is not None})
        cp_hns = sorted({str(r.get("hausNr")) for r in c7[b]
                         if r.get("hausNr") is not None})
        if not sec_hns or not cp_hns:
            fail(f"I4 base {b}: manjkajoče hn (sec {sec_hns} / cp {cp_hns})")
        if set(sec_hns) & set(cp_hns):
            hn_isti += 1
        else:
            hn_raz += 1
        hn_detail[b] = {"sekcije": sec_hns, "counterpar": cp_hns}
    if hn_isti != EXPECTED_HN["isti"] or hn_raz != EXPECTED_HN["različni"]:
        fail(f"I4 hn {hn_isti}/{hn_raz} ≠ {EXPECTED_HN}")
    for pg, rng in EXPECTED_PAGEMAP_SEC.items():
        e = pagemap.get(int(pg))
        if not e or [e.get("numMin"), e.get("numMax")] != rng:
            fail(f"I4 pageMap p{pg} ≠ {rng}")
    for pg, rng in EXPECTED_PAGEMAP_GLOB.items():
        e = pagemap.get(int(pg))
        if not e or [e.get("numMin"), e.get("numMax")] != rng:
            fail(f"I4 pageMap p{pg} ≠ {rng}")
    ok("I4 disjunktnost 0/0 · hn 0 isti / 31 različni · pageMap 5/5")

    # ————— I5 v3 forenzika lažnih fuzij —————
    idx3_geo = defaultdict(list)
    for r in re3:
        idx3_geo[r["base"]].append(r)
    geo_shared = 0
    for v in sec_v3:
        mates = [r for r in idx3_geo[v["base"]]
                 if r.get("lat") == v.get("lat") and r.get("lng") == v.get("lng")
                 and (r["page"], r["base"]) != (v["page"], v["base"])]
        if mates:
            geo_shared += 1
    if geo_shared != EXPECTED_V3_GEO_SHARED:
        fail(f"I5 geoShared {geo_shared} ≠ {EXPECTED_V3_GEO_SHARED}")

    ratios = [v["ratio"] for v in sec_v3 if v.get("ratio") is not None]
    moda_b = sum(1 for x in ratios if MODA_B[0] <= x <= MODA_B[1])
    moda_a = sum(1 for x in ratios if MODA_A[0] <= x <= MODA_A[1])
    absurd = sum(1 for x in ratios if x > MODA_A[1])
    med = round(statistics.median(ratios), 4)
    mx = round(max(ratios), 4)
    got_ratio = {"n": len(ratios), "modaB": moda_b, "modaA": moda_a,
                 "absurdniGT43": absurd, "median": med, "max": mx}
    if got_ratio != EXPECTED_V3_RATIO:
        fail(f"I5 ratio {got_ratio} ≠ {EXPECTED_V3_RATIO}")

    suspect = sum(1 for v in sec_v3 if v.get("areaSuspect"))
    conf3 = Counter(v.get("conf") for v in sec_v3)
    if suspect != EXPECTED_V3_SUSPECT:
        fail(f"I5 areaSuspect {suspect} ≠ {EXPECTED_V3_SUSPECT}")
    if dict(conf3) != EXPECTED_V3_CONF:
        fail(f"I5 conf {dict(conf3)} ≠ {EXPECTED_V3_CONF}")

    sumqk = {pg: sum(s.get("areaQK") or 0 for s in sec_cls if str(s["page"]) == pg)
             for pg in EXPECTED_SEC_PAGES}
    sumqk = {k: int(v) for k, v in sumqk.items()}
    if sumqk != EXPECTED_SUMQK or sum(sumqk.values()) != EXPECTED_SUMQK_TOTAL:
        fail(f"I5 Σ areaQK {sumqk} ≠ {EXPECTED_SUMQK}")
    kult = Counter(v.get("kultur") for v in sec_v3)
    kult_top = {k: n for k, n in kult.most_common(8)}
    if kult_top != EXPECTED_KULTURE_TOP:
        fail(f"I5 kulture {kult_top} ≠ {EXPECTED_KULTURE_TOP}")
    wohn = sum(1 for v in sec_v3 if v.get("wohnort"))
    if wohn != EXPECTED_WOHNORT:
        fail(f"I5 wohnort {wohn} ≠ {EXPECTED_WOHNORT}")
    ok("I5 v3 forenzika: geoShared 56/56 · ratio 11/5/20 (max 134.6786) · "
       "Σ areaQK 38517 · kulture Alm 9/Dingf. 6/Wein 3")

    # ————— I6 P60 moda B band —————
    sec_base_set = set(sec_bases)
    p60_sec = sorted([b for b in p60_bases if b in sec_base_set], key=int)
    if p60_sec != EXPECTED_P60_SEC_BASES:
        fail(f"I6 P60 sekcije base {p60_sec} ≠ {EXPECTED_P60_SEC_BASES}")
    rows_in_band = 0
    for b in p60_sec:
        pages = p60_bases[b]["inBand"]["pages"]
        if sorted(pages) != EXPECTED_P60_INBAND_PAGES[b]:
            fail(f"I6 base {b} inBand {pages} ≠ {EXPECTED_P60_INBAND_PAGES[b]}")
        rows_in_band += sum(1 for s in sec_cls
                            if s["base"] == b and s["page"] in pages)
    if rows_in_band != EXPECTED_ROWS_IN_BAND:
        fail(f"I6 rowsInBand {rows_in_band} ≠ {EXPECTED_ROWS_IN_BAND}")
    ok(f"I6 P60 band: 8 base (163, 176, 644, 653–657) · 12/56 vrstic")

    # ————— I7 opcije predračun (merjeno nad v7) —————
    def counters(rows):
        byb = defaultdict(list)
        for r in rows:
            byb[r["base"]].append(r)
        multi = {b for b, rs in byb.items()
                 if len({r["page"] for r in rs}) > 1}
        cross = {b for b, rs in byb.items()
                 if len({blatt_of(r["page"]) for r in rs}) > 1}
        amb = sum(len(rs) for b, rs in byb.items() if b in multi)
        return {"rows": len(rows), "bases": len(byb), "multiPage": len(multi),
                "crossBlatt": len(cross), "ambRows": amb}

    strip = lambda r: {k: r[k] for k in ROW_FIELDS if r.get(k) is not None}
    a = counters(re7)
    b1_rows = re7 + [strip(v) for v in sec_v3]
    b1 = counters(b1_rows)
    b2_sel = [v for v in sec_v3 if v["base"] in set(EXPECTED_P60_SEC_BASES)]
    b2_rows = re7 + [strip(v) for v in b2_sel]
    b2 = counters(b2_rows)
    exp_a = {"rows": 891, "bases": 879, "multiPage": 2, "crossBlatt": 0,
             "ambRows": 4}
    exp_b1 = {"rows": 947, "bases": 879, "multiPage": 33, "crossBlatt": 23,
              "ambRows": 91}
    exp_b2 = {"rows": 903, "bases": 879, "multiPage": 10, "crossBlatt": 6,
              "ambRows": 24}
    exp_inst = {"rows": None, "bases": 879, "multiPage": 2, "crossBlatt": 0,
                "ambRows": 4}
    if a != exp_a:
        fail(f"I7 opcija A {a} ≠ {exp_a}")
    if b1 != exp_b1:
        fail(f"I7 opcija B1 {b1} ≠ {exp_b1}")
    if b2 != exp_b2:
        fail(f"I7 opcija B2 {b2} ≠ {exp_b2}")
    if len(b2_sel) != EXPECTED_ROWS_IN_BAND:
        fail(f"I7 B2 subset {len(b2_sel)} ≠ {EXPECTED_ROWS_IN_BAND}")
    # instance-ključ (base, stran) za sekcije: vsaka sekcija = lastna
    # single-row instanca (0 kolizij (base, stran) z v7 in med seboj) —
    # sekcije ne fuzirajo po base, crossBlatt/multiPage/amb nespremenjeni
    v7keys = {(r["base"], r["page"]) for r in re7}
    clash = [(s["base"], s["page"]) for s in sec_cls
             if (s["base"], s["page"]) in v7keys]
    dup = [k for k, n in Counter((s["base"], s["page"])
                                 for s in sec_cls).items() if n > 1]
    onsec = sum(1 for r in re7 if r["page"] in (83, 84, 85, 86, 88))
    if clash or dup:
        fail(f"I7 instance ključ kolizije: trk {clash} dup {dup}")
    if onsec != 0:
        fail(f"I7 v7 vrstice na sekcij straneh {onsec} ≠ 0")
    if {k: v for k, v in a.items() if k != "rows"} != \
            {k: v for k, v in exp_inst.items() if k != "rows"}:
        fail(f"I7 instance ključ {a} ≠ {exp_inst}")
    ok("I7 opcije: A 891/2/0/4 · B1 947/33/23/91 (KRŠI NIL-CLAIM → "
       "instance ključ 0/2/4) · B2 903/10/6/24 (+ instance 0/2/4) · "
       "0 vrstic v7 na sekcij straneh (0 kolizij ključev)")

    # ————— dokaz + runtime —————
    status = ("P76: 56 sekcij vrstic (p83–86, p88; Blatt II) × 31 base — "
              "lastniki disjunktni 0/0 · hn 0 isti / 31 različni · "
              "counterpar v v7 31/31 (I 23 / II 8) · P60 band 8 base "
              "(12 vrstic) · opcije A/B1/B2 predračunane · izbira LASTNIŠKA")

    ev_common = {
        "task": "P76 — lokalne sekcije: per-Blatt instance odločitveni paket "
                "(56 vrstic; vzorec P72/P74 — paket MERI, NE odloča)",
        "date": "2026-10-15",
        "generatedBy": "scripts/p76_ps_sections_perblatt_pack.py "
                       "(deterministično, brez AI ob delovanju)",
        "version": 1,
        "summary": {
            "sectionRows": EXPECTED_SEC_ROWS,
            "sectionBases": EXPECTED_SEC_BASES,
            "pages": EXPECTED_SEC_PAGES,
            "blatt": EXPECTED_SEC_BLATT,
            "sumAreaQK": EXPECTED_SUMQK,
            "sumAreaQKTotal": EXPECTED_SUMQK_TOTAL,
            "counterparts": {"total": EXPECTED_CP_TOTAL,
                             "byBlatt": EXPECTED_CP_BLATT,
                             "byPage": EXPECTED_CP_PAGES,
                             "withGeometry": EXPECTED_CP_GEO,
                             "conf": EXPECTED_CP_CONF},
            "c4Evolution": {"members": EXPECTED_C4_MEMBERS,
                            "keptII": EXPECTED_C4_KEPT_II,
                            "keptI": EXPECTED_C4_KEPT_I,
                            "singleBlatt": EXPECTED_C4_SINGLE,
                            "keptIIBases": ["161", "162", "163", "164", "165",
                                            "174", "176", "179"],
                            "keptIBases": ["166", "168", "171", "173", "175"]},
            "identity": {"ownerOverlapVsCounterpart": EXPECTED_OWNER_OVERLAP_CP,
                         "ownerOverlapWithinSections": EXPECTED_OWNER_OVERLAP_SEC,
                         "hausNr": EXPECTED_HN,
                         "pageMapBandOverlap": 5},
            "p60Band": {"attributedBases": EXPECTED_P60_SEC_BASES,
                        "rowsInBand": EXPECTED_ROWS_IN_BAND,
                        "rowsWithoutBand": EXPECTED_SEC_ROWS - EXPECTED_ROWS_IN_BAND},
            "v3Forensics": {"geoShared": EXPECTED_V3_GEO_SHARED,
                            "ratio": EXPECTED_V3_RATIO,
                            "areaSuspect": EXPECTED_V3_SUSPECT,
                            "conf": EXPECTED_V3_CONF,
                            "kultureTop": EXPECTED_KULTURE_TOP,
                            "wohnortRows": EXPECTED_WOHNORT},
        },
        "opcije": {
            "A_statusQuo": {**a,
                            "note": "v7 nespremenjen — sekcije v registru "
                                    "brez geometrije (dokaz P69 sectionClass)"},
            "B1_readmitAll": {**b1,
                              "added": EXPECTED_SEC_ROWS,
                              "nilClaimViolation": True,
                              "violationNote": "crossBlatt 23 krši C4 "
                                               "NIL-CLAIM (23 base dobi "
                                               "vrstici na I in II)",
                              "withInstanceKey": {"crossBlatt": 0,
                                                  "multiPage": 2,
                                                  "ambRows": 4,
                                                  "note": "ključ (base, "
                                                          "stran) za sekcije "
                                                          "— brez fuzije"}},
            "B2_p60Band": {**b2,
                           "added": EXPECTED_ROWS_IN_BAND,
                           "withInstanceKey": {"crossBlatt": 0,
                                               "multiPage": 2,
                                               "ambRows": 4},
                           "leftOut": EXPECTED_SEC_ROWS - EXPECTED_ROWS_IN_BAND},
            "B3_georef": {"executable": False,
                          "prerequisites": ["georef Blatt II sekcije karte",
                                            "PF protokol (vir ni v repu — "
                                            "lastniki pas-instanc ↔ poligoni)"],
                          "status": "[~] neizvedljivo danes"},
        },
        "kulture": dict(sorted(kult.items(), key=lambda x: (-x[1], x[0]))),
        "hausNrDetail": hn_detail,
        "p60Detail": {b: {"attributedBlatt": p60_bases[b]["attributedBlatt"],
                          "inBandPages": p60_bases[b]["inBand"]["pages"],
                          "inBandMedian": p60_bases[b]["inBand"]["medianRatio"],
                          "outInstances": [
                              {"blatt": o["blatt"],
                               "medianRatio": o["medianRatio"]}
                              for o in p60_bases[b]["outInstances"]]}
                      for b in EXPECTED_P60_SEC_BASES},
        "statusLine": status,
        "verdictSi": "56 sekcij vrstic na Blatt II (p83–86, p88; 31 base) je "
                     "identitetno DISJUNKTNO od svojih v7 counterpartov "
                     "(lastniki 0/0, hišne številke 31/31 različne) — "
                     "dokazano na celotni množici, ne samo na P69 vzorcu. "
                     "Per-Blatt instance so merjeno izvedljive: P60 moda B "
                     "pokrije 12/56 vrstic (8 base), PF protokol (ni še v "
                     "repu) je manjkajoči vir za ostale 44. Preprosta "
                     "re-admisija (B1) bi z base-ključem ponovno ustvarila "
                     "23 cross-Blatt fuzij (krši C4 NIL-CLAIM) — zato "
                     "izvedba zahteva per-instanca ključ. Izbira opcije "
                     "(A status quo / B1 / B2 / B3 georef) = LASTNIŠKA.",
        "verdictEn": "56 section rows on Blatt II (p83–86, p88; 31 bases) are "
                     "identity-DISJOINT from their v7 counterparts (owners "
                     "0/0, house numbers 31/31 different) — proven on the "
                     "full set, not just the P69 sample. Per-Blatt instances "
                     "are measurably feasible: P60 mode B covers 12/56 rows "
                     "(8 bases), the PF protocol (not yet in the repo) is "
                     "the missing source for the other 44. Plain re-admission "
                     "(B1) with the base key would re-create 23 cross-Blatt "
                     "fusions (violates the C4 NIL-CLAIM) — execution "
                     "therefore requires a per-instance key. The option "
                     "choice (A status quo / B1 / B2 / B3 georef) = OWNER.",
        "next": [
            "① izbira opcije: A status quo (v7) / B1 vse 56 (obvezen "
            "instance ključ) / B2 samo P60 band 12 / B3 georef [~] = "
            "LASTNIŠKA odločitev",
            "② PF protokol kot vir identitete sekcij (ni v repu; povezati "
            "lastnike pas-instanc s poligoni — P60/P61/P63–P68 next)",
            "③ georef Blatt II sekcije karte (predpogoj B3) [~]",
            "④ p83 dvojni blok 161–170 ×2 ostaja [~] (P69; 8× nebere "
            "zanesljivo)",
        ],
    }

    proof = dict(ev_common)
    proof["principle"] = (
        "Paket MERI, NE odloča (vzorec P72/P74): 56 sekcij vrstic (P69 "
        "sectionClass bajtno) × v7 univerzum × v3 forenzika × P59/P56/P60 "
        "kontekst — vse meritve deterministične, brez AI ob delovanju; "
        "v7 join NESPREMENJEN (I9 sha pin). Opcije A/B1/B2/B3 so PREDRACUNANE "
        "nad v7 (counters re-izračunani, ne deklarirani); izbira = LASTNIKA. "
        "Identitetna disjunktnost (lastniki, hišne številke) je razširjena "
        "iz P69 vzorca (p83/p84 vs p11; p85 vs p35) na celotnih 56 vrstic."
    )
    proof["inputs"] = {
        "p69Sha256": PIN_P69EV_SHA,
        "v3Sha256": PIN_V3EV_SHA,
        "v7Sha256": PIN_V7EV_SHA,
        "p59Sha256": PIN_P59EV_SHA,
        "p56Sha256": PIN_P56EV_SHA,
        "p60Sha256": PIN_P60EV_SHA,
        "v7RuntimeSha256": PIN_V7RT_SHA,
    }
    proof["sectionRows"] = [
        dict(row_pick(v),
             ratioV3=round(v["ratio"], 4) if v.get("ratio") is not None else None,
             geoSharedV3=True,
             pageMapBand=EXPECTED_PAGEMAP_SEC[str(v["page"])])
        for v in sec_v3
    ]
    proof["invariants"] = [
        "I1 vhodni pini (6× sha256 + v7 runtime + števci)",
        "I2 sekcije 56 bajtno == P69; 56/56 v v3 (areaQK ==)",
        "I3 univerzum: Blatt II 5/5; counterpar 31/31 (I 23 / II 8; "
        "lat/lng 31/31; conf 4/21/6); evolucija C4 13 (II 8 / I 5) / 18",
        "I4 identiteta: lastniki 0/0 · hn 0/31 · pageMap 5/5",
        "I5 v3 forenzika: geoShared 56/56 · ratio 11/5/20 · Σ areaQK "
        "38517 · kulture · wohnort 56; izpis brez lat/lng/areaModern",
        "I6 P60 band: 8 base · 12/56 vrstic · inBand strane == pin",
        "I7 opcije predračun == pin (A/B1/B2 + instance ključ; B3 [~])",
        "I8 determinizem (--check bajtno)",
        "I9 v7 runtime join NESPREMENJEN (sha256 pin)",
    ]

    # runtime = bajtna projekcija (brez principle/inputs/invariants/
    # sectionRows.ratioV3/geoSharedV3/pageMapBand)
    runtime = dict(ev_common)
    runtime_rows = [row_pick(v) for v in sec_v3]
    runtime["sectionRows"] = runtime_rows

    if not check_mode:
        with open(OUT_EV, "w", encoding="utf-8") as f:
            json.dump(proof, f, ensure_ascii=False, indent=2, sort_keys=False)
            f.write("\n")
        with open(OUT_RT, "w", encoding="utf-8") as f:
            json.dump(runtime, f, ensure_ascii=False, indent=2, sort_keys=False)
            f.write("\n")
        ok(f"dokaz + runtime zapisana ({OUT_EV}, {OUT_RT})")
    else:
        ev_disk = json.load(open(OUT_EV, encoding="utf-8"))
        rt_disk = json.load(open(OUT_RT, encoding="utf-8"))
        if json.dumps(ev_disk, ensure_ascii=False, sort_keys=True) != \
                json.dumps(proof, ensure_ascii=False, sort_keys=True):
            fail("I8 dokaz drift (--check bajtno)")
        if json.dumps(rt_disk, ensure_ascii=False, sort_keys=True) != \
                json.dumps(runtime, ensure_ascii=False, sort_keys=True):
            fail("I8 runtime drift (--check bajtno)")
        ok("I8 --check bajtno PASS (dokaz + runtime identična)")
        return

    print(f"P76 PASS — 56 vrstic / 31 base · disjunktnost 0/0 · "
          f"hn 31/31 različni · P60 band 12/56 · opcije A/B1/B2/B3")


if __name__ == "__main__":
    main()
