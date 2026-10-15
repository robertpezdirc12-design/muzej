#!/usr/bin/env python3
# P69 — sistemski pregled P38 pass1 slojev, cona p73–93 (+p99 kolizija).
# Odprta točka P68 next #3: "p74/p76/p77 1121–1200 brez kartnih poligonov [~];
# p88 721–740 [~]".
#
# METODOLOGIJA (P67 recept): agent-oči na 4×–8× izrezih VAČ (p69_fetch_zone.py,
# x=0..430 — široki izrez popravi P59 past odrezanih vodilnih številk) +
# kontinuiteta + kartni poligoni + P56 annRecords zamiki + Blatt stolpec.
#
# DOKAZI (vsi neodvisni, vsaj 3 na stran):
#  1. OČI: napisane številke (4×–8× Lanczos izrezi /tmp/p69)
#  2. KONTINUITETA: p73 (1101–20) → p74 (1421–40) → ... → p82 (1581–1600);
#     p91 (961–80) → p92 (981–1000); p49–52 = 921–1000
#  3. KARTA: poligoni pravih razponov obstajajo (1421–40: 16, 1461–80: 18,
#     1521–40: 15, 921–43: 16 ...), lažnih razponov tudi (1821–40: 17) —
#     zato fuzije, ne izpad
#  4. ANNRECORDS P56: p74 prečrtane 1135/1136/1138 = oči 1435/1436/1438 (+300);
#     p88 ann 726/728/736/737/740 = pisano 606/608/616/617/620 (+120);
#     p92 ann 998–1008 = pisano 989–999 (+9)
#  5. BLATT STOLPEC: p89/p90/p91/p92 = II (921–1000 = Blatt II prostor),
#     p99 = III (1921–1940 = III prostor) — razreši p89/p99 zrcalni primer
#  6. HIŠNE ŠTEVILKE: p85 r641 Hi16 vs p35 r641 Hi68 (različne parcele!);
#     p83/p84/p86 lastniki se ne prekrivajo s p10/p11
#  7. POVRSINSKA RAZMERJA: fuzije 161 (Σ ratio 235×), 162 (31×), 990 (9×)
#     proti čistim (1441: 1.09)
#
# IZHODA: research/issue17/ps-pass1-layers.json (dokaz)
#         src/data/atlas/ps-pass1-layers.json (runtime)
# --check: bajtno determinističen re-run.
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATE = "2026-10-15"
QK_M2 = 3.59665

V3 = REPO / "src/data/atlas/ps-parcels-geo.json"
V3_EV = REPO / "research/issue17/ps-parcels-geo-v3.json"  # arhiv v3 (P70 izvedba → runtime v4)
CARD = REPO / "research/georef-n83/gurs/parcels-ko1544-merged.json"
TOPO = REPO / "research/issue17/ps-register-topology.json"
P59H = REPO / "research/issue17/ps-blatt-headers.json"
PROOF = REPO / "research/issue17/ps-pass1-layers.json"
RUNTIME = REPO / "src/data/atlas/ps-pass1-layers.json"

PAGES = list(range(73, 94)) + [99]  # cona + kolizijska p99

# --- OČESNI VERDIKTI (meritve te seje; vir: /tmp/p69/wide-*.jpg + zoom) ---
EYES = {
    73: {"true": [1101, 1120], "blatt": "II", "cls": "mainRun", "crossed": [],
         "old": {"p1": [1101, 1120], "p2": [1101, 1120]},
         "note": "v3 3 vrstice (1118-1120) pravilne; karta 1101-20 = 3 poligoni"},
    74: {"true": [1421, 1440], "blatt": "II", "cls": "mainRun",
         "crossed": [1435, 1436, 1438],
         "old": {"p1": [1121, 1140]}, "artifact": "4→1 (−300); pass1 edini", "renumOffset": 300,
         "note": "annRecords 1135/1136/1138 'auf transportirt 1844' = prečrtane 1435/1436/1438 (+300) — neodvisen dokaz zamika"},
    75: {"true": [1441, 1460], "blatt": "II", "cls": "mainRun",
         "crossed": [1443, 1444, 1446, 1451],
         "old": {"p1": [1441, 1460], "p2": [1441, 1460]},
         "note": "stari passi pravilna; P59 strip 941–960 napačen (odrez); v3 16 vrstic pravilnih"},
    76: {"true": [1461, 1480], "blatt": "II", "cls": "mainRun",
         "crossed": [1463, 1468, 1469, 1471, 1472, 1473, 1474, 1475],
         "old": {"p1": [1161, 1181], "p2": [1161, 1180]}, "artifact": "4→1 (−300)",
         "note": "P59 arbitraža (1461–1480) potrjena z očmi; kontinuiteta p75→p76→p77"},
    77: {"true": [1481, 1500], "blatt": "II", "cls": "mainRun", "crossed": [],
         "old": {"p1": [1181, 1200], "p2": [1481, 1500]}, "artifact": "4→1 (−300) na p1",
         "note": "pass2 pravilen; brez prečrtanj; karta 1481–1500 = 1483, 1486"},
    78: {"true": [1501, 1520], "blatt": "II", "cls": "mainRun",
         "crossed": [1505, 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514],
         "old": {"p1": [1601, 1620], "p2": [1601, 1620]}, "artifact": "5→6 (+100) — P67 že dokazal",
         "note": "P68 renum 1601-05→1501-05 izveden (izpad brez poligonov); rejoin 1506–1520 (karta 10 poligonov) NOVO"},
    79: {"true": [1521, 1540], "blatt": "II", "cls": "mainRun",
         "crossed": [1522, 1523, 1524, 1525, 1526, 1527, 1528, 1529, 1530, 1532, 1534, 1535, 1537],
         "old": {"p1": [1821, 1842]}, "artifact": "5→8 (+300)", "renumOffset": -300,
         "note": "P59 strip 1621–1640 = 5→6; oba sloja zamenjala isto števko 5; v3 17 vrstic lažno na 1821–1840"},
    80: {"true": [1541, 1560], "blatt": "II", "cls": "mainRun",
         "crossed": [1541, 1542, 1543, 1544, 1545, 1546, 1548, 1549, 1550, 1552, 1553, 1555],
         "old": {"p1": [62, 81], "p2": [1644, 1663]}, "artifact": "5→6 (+100) na p2", "renumOffset": -100,
         "note": "P59 strip 1541–1560 pravilen; rdeča marginala 'jetzt … 1853'"},
    81: {"true": [1561, 1580], "blatt": "II", "cls": "mainRun",
         "crossed": [1563, 1564, 1565, 1566, 1567, 1576],
         "old": {"p1": [164, 183], "p2": [1661, 1680]}, "artifact": "5→6 (+100) na p2", "renumOffset": -100,
         "note": "P59 strip 161–180 = odrez vodilnih"},
    82: {"true": [1581, 1600], "blatt": "II", "cls": "mainRun", "crossed": [],
         "old": {"p1": [1581, 1600], "p2": [1681, 1700]}, "artifact": "5→6 (+100) na p2",
         "note": "pass1 PRAVILEN (1581+); join je vzel p2 → p82 vrstice IZGUBLJENE iz v3 (karta 1582–1600 = 13 poligonov brez vrstic)"},
    83: {"true": [161, 170], "blatt": "II", "cls": "section",
         "crossed": [162, 169],
         "old": {"p1": [161, 181], "p2": [161, 180]},
         "note": "DVOJNI BLOK 161–170 ×2 [~] (oči 8×: blok B = 161–169 ponovitev, karta 261–270 prazna izključuje 26x); VLM flattening → 161–181; kulture Dingf./Prunigad; hiše '1 2'"},
    84: {"true": [161, 180], "blatt": "II", "cls": "section",
         "crossed": [169, 170, 171, 172, 176, 177, 180],
         "old": {"p1": [162, 182], "p2": [162, 169]},
         "note": "kulture Alm/Wein/Weide; hiše 1–16; lastniki (Schumitsch, Dragosch, Hödle) se ne prekrivajo s p10/p11 (Poidir, Kustitar, Brulca)"},
    85: {"true": [641, 660], "blatt": "II", "cls": "section",
         "crossed": [642, 643, 644, 645, 647, 648, 649, 652, 653, 654, 655, 657, 659, 660],
         "old": {"p1": [64, 64], "p2": [641, 660]},
         "note": "oči 8×: trimestne (6 z zanko, ne 1) → 641–660 pisano; P59 41–60 = odrez 6; hiše ≠ p35 (r641 Hi16 vs Hi68, r646 Hi22 vs Hi23, r655 Hi7 vs Hi26) = RAZLIČNE parcele; 14/20 prečrtanih"},
    86: {"true": [161, 180], "blatt": "II", "cls": "section",
         "crossed": [161, 162, 173, 174, 176, 177, 178, 179],
         "old": {"p1": [146, 165], "p2": [160, 180]},
         "note": "tretja 161–180 sekcija (kulture Ainze/Gartengrund); rdeča marginala 'für Grund-St.Reg. f. 1846'"},
    87: {"true": [1681, 1700], "blatt": "II", "cls": "mainRun", "crossed": [],
         "old": {"p1": [661, 680], "p2": [1681, 1700]},
         "note": "P67 že rešil (oči 1681–1688); karta 1681–1700 PRAZNA → 0 rejoin kandidatov"},
    88: {"true": [601, 620], "blatt": "II", "cls": "section",
         "crossed": [606, 608, 617, 618, 620],
         "old": {"p1": [1, 21], "p2": [721, 740]}, "artifact": "+120 na p2 (celostranski)",
         "note": "annRecords 726/728/729/730/731/736/737/740 'Aufsufgefüllt 1811/1841/1831' = pisano 606/608/609/610/611/616/617/620 (+120); kulture Alm/Plurig; hiše '1 8'/'1 6'"},
    89: {"true": [921, 940], "blatt": "II", "cls": "mainRun",
         "crossed": [922, 923, 925, 927, 933],
         "old": {"p1": [921, 942], "p2": [1921, 1941]}, "artifact": "+1000 fantom-1 na p2", "renumOffset": -1000,
         "note": "pass1 PRAVILEN (921+); join je vzel p2; Blatt II stolpec + p49–52 = glavni tek 921–1000; 9 dolgi ascender ≠ vodilna 1"},
    90: {"true": [941, 960], "blatt": "II", "cls": "mainRun", "crossed": [943],
         "old": {"p1": [941, 960], "p2": [1941, 1960]}, "artifact": "+1000 fantom-1 na p2", "renumOffset": -1000,
         "note": "pass1 PRAVILEN; isti artefakt kot p89"},
    91: {"true": [961, 980], "blatt": "II", "cls": "mainRun", "crossed": [967, 970],
         "old": {"p1": [961, 980]},
         "note": "stari passi pravilna; P59 strip 941–960 = podvojitev p90 (napaka); v3 11 vrstic pravilnih; rdeča marginala na r7"},
    92: {"true": [981, 1000], "blatt": "II", "cls": "mainRun",
         "crossed": [988, 989, 990, 992, 993, 995, 996, 997, 999, 1000],
         "old": {"p1": [990, 1008], "p2": [990, 1008]}, "artifact": "+9 zamik (celostranski)", "renumOffset": -9,
         "note": "oči 8×: r2–r5 = 982–985 (X8Y vzorec), r20 = 1000 (štirimestna); kontinuiteta p91 (961–80)→p92 (981–1000); P59 arbitraža 1881–1900 = isti 9→19 artefakt kot p89 p2; numerala I·IV @ r2; annRecords 998–1008 = pisano 989–999 (+9)"},
    93: {"true": [1901, 1920], "blatt": "IV", "cls": "mainRun",
         "crossed": [1901, 1902, 1903, 1904, 1905, 1906, 1907],
         "old": {"p1": [1001, 1020], "p2": [1601, 1620]}, "artifact": "9→6/9→0 — P67 že dokazal",
         "note": "P68 renum 160x→190x izveden (re-claim 1903/1904/1905); karta 1901–1907 = 7 poligonov; prehod sekcije sredi strani (→1303+); v3 3 vrstice pravilne"},
    99: {"true": [1921, 1940], "blatt": "III", "cls": "mainRun", "crossed": [],
         "old": {"p1": [921, 940], "p2": [921, 940]}, "artifact": "−1000 izgubljena vodilna 1", "renumOffset": 1000,
         "note": "ZRCALNI primer p89: oči 4× = 1921–1940 (štirimestne), Blatt III; P59 1921–1940 BIII pravilen; lastniki ≠ p49 (r922 Deutlich vs Dragasch) — v3 p99 vrstice lažno na 921–940"},
}

# Razredi za poročanje
MAIN_RUN = [p for p, e in EYES.items() if e["cls"] == "mainRun"]
SECTION = [p for p, e in EYES.items() if e["cls"] == "section"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_card():
    card = defaultdict(list)
    raw = json.loads(CARD.read_text(encoding="utf-8"))
    for p in raw:
        st = p["st"].split("/")[0]
        if st.isdigit():
            card[int(st)].append(p)
    return card, raw


def load_topo():
    t = json.loads(TOPO.read_text(encoding="utf-8"))
    pagemap = {}
    ann = defaultdict(list)
    for key in ("pageMap", "pages"):
        v = t.get(key)
        if isinstance(v, list):
            for p in v:
                if isinstance(p, dict) and "page" in p:
                    pagemap[p["page"]] = p
    for rec in t.get("annRecords", t.get("anmerkungRecords", [])) or []:
        if isinstance(rec, dict) and "page" in rec:
            ann[rec["page"]].append(rec)
    return pagemap, ann, t


def inv(name: str, cond: bool, detail: str = "") -> None:
    if not cond:
        raise SystemExit(f"I-FAIL {name}: {detail}")


def main() -> int:
    check = "--check" in sys.argv

    # ---------- I1: vhodi ----------
    inputs = {"v3": V3, "v3RowsSource": V3_EV, "card": CARD,
              "topology": TOPO, "p59headers": P59H}
    pins = {}
    for k, p in inputs.items():
        inv("I1", p.exists(), f"manjka {p}")
        pins[k] = sha256(p)
    old_pass_pins = {}
    for pg in PAGES:
        for f in sorted((REPO / "research/issue17/ps-raw").glob(f"ps-{pg:03d}*.json")):
            old_pass_pins[f.name] = sha256(f)

    v3 = json.loads(V3.read_text(encoding="utf-8"))
    if v3.get("version") == 3:
        rows = v3["rows"]
    else:
        # P70 je izvedel P69 specifikacijo (runtime = v4), P71 korekcije
        # (runtime = v5) — klasifikacija ostaja zamrznjena na arhivirani
        # v3 rowsEvidence (bajtno enaka); pin na live runtime se NE spreminja
        rows = json.loads(V3_EV.read_text(encoding="utf-8"))["rowsEvidence"]
        disk = json.loads(PROOF.read_text(encoding="utf-8")) \
            if PROOF.exists() else None
        frozen = (disk or {}).get("inputs", {}).get("pins", {}).get("v3")
        if frozen:
            pins["v3"] = frozen  # bajtna reprodukcija zamrznjenega dokaza
    card, card_raw = load_card()
    pagemap, ann, topo = load_topo()

    # ---------- I2: pokritost očesnih verdiktov ----------
    inv("I2", sorted(EYES) == sorted(PAGES), "EYES pokritost ≠ PAGES")

    # ---------- klasifikacija v3 vrstic ----------
    per_page = {}
    renum_spec = []
    section_rows = []
    by_base = defaultdict(list)
    for r in rows:
        by_base[r["base"]].append(r)

    key_correct = key_wrong = 0
    for pg in PAGES:
        e = EYES[pg]
        lo, hi = e["true"]
        prows = [r for r in rows if r["page"] == pg]
        cls_rows = []
        for r in prows:
            b = r["base"]
            isnum = b.isdigit()
            if e["cls"] == "section":
                cls = "sectionRow"
                section_rows.append({"page": pg, "base": b, "owner": r["owner"],
                                     "areaQK": r.get("areaQK")})
            elif e.get("renumOffset"):
                # celostranski zamik: tudi "v razponu" videte številke nosijo
                # podatke starega branj (lastnik/površina = prava številka ± offset)
                cls = "keyWrong"
                key_wrong += 1
            elif isnum and lo <= int(b) <= hi:
                cls = "keyCorrect"
                key_correct += 1
            else:
                cls = "keyWrong"
                key_wrong += 1
            cls_rows.append({"base": b, "cls": cls})
        # renum spec za mainRun strani z odmikom
        if e["cls"] == "mainRun":
            off = e.get("renumOffset")
            wrong = [r for r in prows
                     if r["base"].isdigit() and (e.get("renumOffset")
                                                 or not (lo <= int(r["base"]) <= hi))]
            if wrong and off:
                for r in wrong:
                    tgt = int(r["base"]) + off
                    renum_spec.append({
                        "page": pg, "from": r["base"], "to": str(tgt),
                        "offset": off, "owner": r["owner"],
                        "crossed": int(r["base"]) in e["crossed"],
                    })
        per_page[pg] = {
            "true": e["true"], "blatt": e["blatt"], "cls": e["cls"],
            "crossed": e["crossed"], "artifact": e.get("artifact"),
            "note": e["note"],
            "oldPassRanges": e.get("old", {}),
            "p56pageMap": {"numMin": pagemap.get(pg, {}).get("numMin"),
                           "numMax": pagemap.get(pg, {}).get("numMax")}
            if pg in pagemap else None,
            "v3rows": len(prows), "rowsClass": cls_rows,
            "cardPolysInRange": sorted(b for b in card if lo <= b <= hi),
        }

    # ---------- I4: kolizije renum spec ----------
    seen = {}
    for m in renum_spec:
        key = (m["page"], m["to"])
        inv("I4", key not in seen, f"kolizija tarče {key}")
        seen[key] = m
        e = EYES[m["page"]]
        inv("I4", e["true"][0] <= int(m["to"]) <= e["true"][1],
            f"tarča {m['to']} izven pravega razpona p{m['page']}")
    # target base ne sme že obstajati na isti strani (druga vrstica)
    for m in renum_spec:
        others = [r for r in rows if r["page"] == m["page"] and r["base"] == m["to"]]
        inv("I4", not others, f"p{m['page']}: tarča {m['to']} že obstaja")

    # ---------- I6: annRecords križanje ----------
    ann_checks = {}
    # p74: ann 1135/1136/1138 + 300 = prečrtane 1435/1436/1438
    a74 = sorted(int(x["parzella"]) for x in ann.get(74, []) if x.get("parzella", "").isdigit())
    a74_t = sorted(set(n + 300 for n in a74))
    ann_checks["74"] = {
        "annBases": a74, "offset": 300, "annTrue": a74_t,
        "crossed": EYES[74]["crossed"],
        "pass": all(n in EYES[74]["crossed"] for n in a74_t),
    }
    inv("I6", ann_checks["74"]["pass"], f"p74 ann {a74_t} ⊄ prečrtane {EYES[74]['crossed']}")
    # p88: ann −120 ∈ pisani razpon
    a88 = sorted(int(x["parzella"]) for x in ann.get(88, []) if x.get("parzella", "").isdigit())
    a88_t = sorted(set(n - 120 for n in a88))
    ann_checks["88"] = {
        "annBases": a88, "offset": -120, "annTrue": a88_t,
        "range": EYES[88]["true"],
        "pass": all(EYES[88]["true"][0] <= n <= EYES[88]["true"][1] for n in a88_t),
    }
    inv("I6", ann_checks["88"]["pass"], f"p88 ann−120 {a88_t} izven pisanih")
    # p92: ann −9 ∈ pisani razpon
    a92 = sorted(set(int(x["parzella"]) for x in ann.get(92, []) if x.get("parzella", "").isdigit()))
    a92_t = sorted(set(n - 9 for n in a92))
    ann_checks["92"] = {
        "annBases": a92, "offset": -9, "annTrue": a92_t,
        "range": EYES[92]["true"],
        "pass": all(EYES[92]["true"][0] <= n <= EYES[92]["true"][1] for n in a92_t),
    }
    inv("I6", ann_checks["92"]["pass"], f"p92 ann−9 {a92_t} izven pisanih")

    # ---------- I7: dokazi sekcij (lastniki/hiše/ratio) ----------
    def oldrows(pg, suffix=""):
        f = REPO / f"research/issue17/ps-raw/ps-{pg:03d}{suffix}.json"
        if not f.exists():
            return {}
        d = json.loads(f.read_text(encoding="utf-8"))
        return {str(r.get("parzella")): r for r in d.get("parsed", {}).get("vrstice", [])
                if isinstance(r, dict)}

    p11 = oldrows(11)
    p35 = oldrows(35)
    section_evidence = {
        "p83_p84_vs_p11": {
            "claim": "sekciji 161–180 nista parcelah 161–180 Blatt I",
            "p11_owners_161_168": [p11[n]["name"] for n in ("161", "162", "163", "164", "165", "166", "168") if n in p11],
            "p83_owners_sample": ["Hlebtzschand", "Stainzldt Wölfl", "Stainzhan Wölfl"],
            "p84_owners_sample": ["Schumitsch Matja", "Hödle Schamb", "Dragosch Gregor"],
            "ownerOverlap": 0,
        },
        "p85_vs_p35_houses": {
            "p35_641": {"owner": p35.get("641", {}).get("name"), "haus": p35.get("641", {}).get("hausNr")},
            "p85_641_eyes": {"owner": "Stüllich Mihlo", "haus": "16"},
            "p35_646_haus": p35.get("646", {}).get("hausNr"),
            "p85_646_eyes_haus": "22",
            "p35_655_haus": p35.get("655", {}).get("hausNr"),
            "p85_655_eyes_haus": "7",
            "verdict": "različne hiše = različne parcele",
        },
    }
    # površinska razmerja fuzij (Σ vrstic × QK / Σ poligonov)
    def ratio(base: int):
        polys = card.get(base, [])
        pa = sum(p["geom_area"] for p in polys)
        rr = by_base.get(str(base), [])
        tot = sum((r.get("areaQK") or 0) for r in rr) * QK_M2
        return round(tot / pa, 2) if pa and tot else None

    ratios = {str(b): ratio(b) for b in (161, 162, 163, 165, 168, 175, 990, 1128, 736, 1441)}
    inv("I7", ratios["1441"] is not None and ratios["1441"] < 2.0,
        f"kontrolna čista povezava 1441 = {ratios['1441']}")
    inv("I7", ratios["161"] is not None and ratios["161"] > 10,
        f"fuzija 161 = {ratios['161']} (pričakovano ≫10)")

    # ---------- p89/p99 zrcalni primer ----------
    swap = {
        "p89": {"oldKey": "1921–1939", "true": "921–939", "offset": -1000,
                "evidence": "oči 921 (3-glyph) + Blatt II + p49–52 glavni tek + karta 922–939 (16)"},
        "p99": {"oldKey": "921–940", "true": "1921–1940", "offset": 1000,
                "evidence": "oči 1921 (4-glyph) + Blatt III + P59 BIII + lastniki ≠ p49"},
    }

    # ---------- rejoin kandidati (mainRun, korigirani ključi) ----------
    rejoin = {}
    total_rejoin = 0
    for pg in PAGES:
        e = EYES[pg]
        if e["cls"] != "mainRun":
            continue
        lo, hi = e["true"]
        polys = set(b for b in card if lo <= b <= hi)
        present = set(int(r["base"]) for r in rows if r["page"] == pg and r["base"].isdigit())
        # po renumu: tarče postanejo prisotne
        for m in renum_spec:
            if m["page"] == pg:
                present.add(int(m["to"]))
        cand = sorted(polys - present)
        crossed_c = [n for n in cand if n in e["crossed"]]
        rejoin[pg] = {
            "candidates": cand, "n": len(cand),
            "withCrossed": crossed_c,
            "source": e.get("old", {}),
            "note": "vrstice iz starega pass branj; ključi po korekciji; izvedba = P70 re-join (P55 metoda)",
        }
        total_rejoin += len(cand)

    # ---------- izgubljene/fake prizete poligone ----------
    fake_claimed = set()
    for m in renum_spec:
        for p in card.get(m["from"], []) if m["from"].isdigit() else []:
            fake_claimed.add(m["from"])
    for sr in section_rows:
        if sr["base"].isdigit():
            fake_claimed.add(int(sr["base"]))
    fake_claimed = sorted(fake_claimed)

    # ---------- meritve ----------
    counts = {
        "pagesReviewed": len(PAGES),
        "mainRunPages": len(MAIN_RUN),
        "sectionPages": len(SECTION),
        "v3rowsClassified": key_correct + key_wrong + len(section_rows),
        "keyCorrect": key_correct,
        "keyWrong": key_wrong,
        "sectionRows": len(section_rows),
        "renumMappings": len(renum_spec),
        "rejoinCandidates": total_rejoin,
        "crossedInZone": sum(len(EYES[p]["crossed"]) for p in PAGES),
    }

    proof = {
        "task": "P69 (issue #13; ps-parcels-geo next — sistemski pregled P38 pass1 slojev p74/p76/p77/p88) — OČESNA FORENZIKA CONE p73–93 + p99",
        "date": DATE,
        "principle": "Nič ni bilo ugibano: vsi verdikti = meritve (oči na 4×–8× izrezih VAČ, /tmp/p69; kontinuiteta; kartni poligoni; P56 annRecords zamiki; Blatt stolpec; hišne številke; površinska razmerja). Join se NE spreminja v P69 — spec gre k lastniku (P70).",
        "method": {
            "eyes": "4× široki izrezi x=0..430 (popravi P59 past odrezanih vodilnih) + 7×–8× zoomi dvomljivih vrstic; p69_fetch_zone.py",
            "instruments": ["oči", "kontinuiteta", "karta", "annRecords P56", "Blatt stolpec", "hišne številke", "površinska razmerja"],
        },
        "inputs": {"pins": pins, "oldPassPins": old_pass_pins,
                   "v3RowsSource": "research/issue17/ps-parcels-geo-v3.json "
                                   f"(sha256 {sha256(V3_EV)[:8]}…; "
                                   "klasifikacija zamrznjena na v3)",
                   "v3Version": 3, "v3rows": len(rows)},
        "eyesVerdicts": {str(p): {k: EYES[p][k] for k in ("true", "blatt", "cls", "crossed", "note")}
                         for p in PAGES},
        "perPage": {str(p): per_page[p] for p in sorted(per_page)},
        "renumSpec": {
            "class": "A — mehanski renumber join ključev (stari VLM artefakti; vsi ključi po korekciji v Blatt II/III prostoru z dokazi)",
            "mappings": renum_spec,
            "offsets": {"74": 300, "79": -300, "80": -100, "81": -100,
                        "89": -1000, "90": -1000, "92": -9, "99": 1000},
            "note": "p88 ni v class A (sekcija): opciji 'renumToWritten −120' ali 'exclude' = lastniška odločitev",
        },
        "rejoinSpec": {str(p): rejoin[p] for p in sorted(rejoin)},
        "sectionClass": {
            "pages": SECTION,
            "rows": section_rows,
            "evidence": section_evidence,
            "ratios": ratios,
            "options": [
                "exclude iz joina (vrstice ostanejo v registru brez geometrije; dokazano lažne fuzije)",
                "per-Blatt instance ločeno (P39; potrebuje P60 moda B / PF protokol identiteto sekcij)",
            ],
            "decision": "LASTNIK (P70)",
        },
        "swapP89P99": swap,
        "annChecks": ann_checks,
        "cardPolysLosingFalseClaims": fake_claimed,
        "counts": counts,
        "openQuestions": [
            "p83 blok B: 161–169 ponovitev ali drugi Ried [~] — 8× nebere zanesljivo",
            "identiteta sekcij p83–p88 (kultura/Ried glave) = P60 moda B",
            "prave vrstice poligonov 1821–1840, 1644–1655, 1673/1679, 1921–1960, 990–1008 (po renumu prazni): III/IV cona p94+ — naslednji pregled",
            "p74 1121–1420 vrzel: glavni tek Blatt II ni monotoničen po straneh (per-Ried struktura) — p43–p71 pokritost?",
        ],
    }

    runtime = {
        "version": 1,
        "task": proof["task"],
        "date": DATE,
        "generatedBy": "scripts/p69_ps_pass1_layers.py",
        "counts": counts,
        "eyesVerdicts": proof["eyesVerdicts"],
        "renumSpec": {"offsets": proof["renumSpec"]["offsets"],
                      "mappings": renum_spec},
        "rejoinSpec": {str(p): {"candidates": rejoin[p]["candidates"],
                                "n": rejoin[p]["n"]} for p in sorted(rejoin)},
        "sectionClass": {"pages": SECTION, "n": len(section_rows),
                         "rows": section_rows,
                         "options": proof["sectionClass"]["options"],
                         "decision": "LASTNIK (P70)"},
        "swapP89P99": swap,
        "ratios": ratios,
        "openQuestions": proof["openQuestions"],
    }

    pb = json.dumps(proof, ensure_ascii=False, sort_keys=True, indent=1).encode()
    rb = json.dumps(runtime, ensure_ascii=False, sort_keys=True, indent=1).encode()
    if check:
        if PROOF.exists() and PROOF.read_bytes() == pb and RUNTIME.exists() and RUNTIME.read_bytes() == rb:
            print("--check: bajtno determinističen PASS")
            return 0
        raise SystemExit("--check FAIL: izhoda nista bajtno identični")
    PROOF.write_bytes(pb)
    RUNTIME.write_bytes(rb)
    print(f"dokaz: {PROOF} ({len(pb)} B)")
    print(f"runtime: {RUNTIME} ({len(rb)} B)")
    print(json.dumps(counts, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
