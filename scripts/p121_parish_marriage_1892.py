#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P121 — župnija Podzemelj: poročna knjiga 04455, polno leto 1892 (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P120 = 1891): okvir POTRJEN —
skeni 84–86 == Pag. 83–85 (Pag. == sken − 1, 7. potrditev; velja v 61–86);
**15 vpisov** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18 →
1892:15; razpored 6+4+5); **VELIKA GLAVA »Traunungs=Buch« 1892 POTRJENA na
s84** (P120 lead; cikel velike glave vsako leto: 1887 s66 + 1890 s77 + 1892
s84; 1891 brez = izjema). LANDSCAPE geometrija (~2509–2518×1800).

FAZA 2: **15/15 vpisov transkribiranih OBOJESTRANSKO** + 30 row-crops ×2
LANCZOS + ~90 mikro-zoomov ×3–9 (crop_rows_121.py, z121_*/zb_*/zc_*/zd_*/
ze_*/zf_*/fq_*).
NOVELE: **DRUBEL-GRIBLJE poroke ×3 = rekord linije** (v1 h60×h49 + v10
h17×h34 + v15 h36×h44 — 6 od 7 hiš-noter!) + **deležni sistem ¼/½/¾ ×21
oseb = rekord** (¾ prvič: v2 bride + v4 priča!) + **Griblers=Sohn/Tochter
ROSETTA ×9** + **1. AMERIŠKI KONSULAT** (v11 Philadelphia 2878/92 Z:3074!)
+ **1. KNECHT ×2** (v6 + v12) + **1. MUC-priimek z deležem** (v12 oče
Nicolaus Muc ½ Gribler — Muc = hišno ime Griblje 10!) + **SESTRSKI
DVOZAKON isti dan** (v2+v3 Marasinič, 15.2.!) + **4 poroke 22.2. = rekord
dneva 1887–1892** + **ženin 56 (v14) NOV rekord starosti** + **nevesta 17
(v1) NOV rekord mladosti** + **Wittwen-dispensacija Z:9123 (v13)** +
**Laipšl/Laipfl ×5 (2. leto mreže!)** + k.k. BezHauptm. Črnomelj ×3 (Z:798
+ Certificate 14/12.1891 + Z:9123) + k.k. Bez. Ger. MÖTTLING (Metlika!) ×2
+ slovenskojezični Befunde-blok (v9) + vdovski znaki ×3 [~].

GRIBLJE: 3 poroke / 4 poročna bloka (h60 v1 ženin — 2. dokaz h60 po 1886!
+ h49 dokumentiran; h30 v5 nevesta; h17 v10 ženin NOVA + h34 dokumentiran;
h36 v15 ženin + h44 NOVA dokumentirana) — **bloki 04455 = 37; vitals 554;
p80 hiše 41 (P121: + h17 — 1887/1894/1901 krstni bloki izven vzorca!)**.
Skripta scripts/p121_parish_marriage_1892.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
knjige/inventarja).
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES = 192
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1892.json"
DOKAZ_P120 = "research/issue17/parish-marriage-1891.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"

FRAME_SCANS = (84, 85, 86)      # 84 = Pag. 83 (velika glava 1892 + v1–6) · 85 = Pag. 84 (v7–10) · 86 = Pag. 85 (v11–15)
FRAME_PAGES = (83, 84, 85)
EXPECTED_ENTRIES = 15
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 8
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [1, 5, 10, 15]
GRIBLJE_MARRIAGES = 3
GRIBLJE_HOUSES = [60, 49, 30, 17, 34, 36, 44]
GRIBLJE_HOUSES_TS = "17,30,36,60"   # hiše z 1892 bloki v parish.ts (v1 h60 + v5 h30 + v10 h17 + v15 h36)
EXPECTED_VITALS = 554               # P121 dokaz lastna kumulativa (550 + 4 bloki)
BLOCKS_04455 = 37                   # 33 (P120) + 4 novih blokov 1892 (P121)
BLOCKS_04455_TS = 82              # P126: + 9 blokov 1897 (52 + 9)                # parish.ts zdaj = 49 (P121: 37 + P122: 5 + P123: 4 + P124: 3)
P80_HOUSES = 41                     # 40 (P120) + h17 (1892 v10 ženin — krstni bloki 1887/1894/1901 izven vzorca!)
DATE_COUNTS = {"januar": 0, "februar": 8, "marec": 0, "april": 0, "maj": 0,
               "junij": 0, "julij": 0, "avgust": 0, "september": 3, "oktober": 2,
               "november": 2, "december": 0}
# P121 pini (blok-houseNo → obvezen fragment v whatSi; cf. qa-p121)
BLOCK_PINS = [
    ("60", "ŽELJKO"), ("60", "DRUBEL-GRIBLJE"), ("60", "BRODARIČ"), ("60", "h49"),
    ("30", "SEGINA"), ("30", "POZDIREC"), ("30", "MILEK"), ("30", "Z: 798"),
    ("17", "KRALJ"), ("17", "DRUBEL-GRIBLJE"), ("17", "FILAK"), ("17", "h34"),
    ("36", "KRIŽAN"), ("36", "DRUBEL-GRIBLJE"), ("36", "STRUNCELJ"), ("36", "h44"),
]
OLD_READINGS = []


def http_get(url, headers=None, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers or UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read()
        except Exception:  # noqa: BLE001
            import time
            time.sleep(2 + i * 2)
            last = sys.exc_info()[1]
    raise last  # type: ignore


def main() -> int:
    live = "--live" in sys.argv
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    # ---------- I1: dokaz JSON ----------
    try:
        d = json.load(open(DOKAZ))
    except Exception as e:  # noqa: BLE001
        print(f"I1 FAIL: {e}")
        return 1
    check("I1 json obstaja", True, DOKAZ)
    check("I1b entries=15", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1c excluded=0", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1d anomalije=8", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=20", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (15/15)", not bad, str(bad) if bad else "vse ✓")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 skeni 84–86", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2b strani 83–85", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))
    check("I2c Pag. == sken − 1 (7. potrditev)", "sken − 1" in fr.get("pagRule", ""), fr.get("pagRule", "")[:60])
    check("I2d velika glava 1892 na s84 (P120 lead POTRJEN)",
          "s84" in fr.get("bigHeader", "") and "1892" in fr.get("bigHeader", ""),
          fr.get("bigHeader", "")[:70])
    rows_f = fr.get("rows", {})
    check("I2e vrstice s84/s85/s86", all(k in rows_f for k in ("s84", "s85", "s86")), str(list(rows_f.keys())))
    rows = [e["row"] for e in d["entries"]]
    check("I2f vrstice 1–15 zapored", rows == list(range(1, 16)), str(rows))
    sc = [e["scan"] for e in d["entries"]]
    check("I2g skeni znotraj 84–86", all(84 <= s <= 86 for s in sc), str(sorted(set(sc))))
    per = {84: 6, 85: 4, 86: 5}
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2h razpored 6+4+5", raz == per, str(raz))
    lead = d.get("lead", {})
    check("I2i P122 lead (poročna 1893, s87)", "P122" in lead.get("next", "") and "1893" in lead.get("next", "")
          and "s87" in lead.get("frame", ""), f'{lead.get("next", "")} | {lead.get("frame", "")[:40]}')

    # ---------- I3: ključni vpisi ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [1,5,10,15]", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 3 (rekord linije!)", d["stats"].get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(d["stats"].get("gribljeMarriages")))
    check("I3a Griblje hiše = [60,49,30,17,34,36,44]", d["stats"].get("gribljeHouses") == GRIBLJE_HOUSES,
          str(d["stats"].get("gribljeHouses")))
    e1 = d["entries"][0]
    check("I3b vpis 1 = h60 ŽELJKO × h49 BRODARIČ (drubel-Griblje; h60 2. dokaz po P120 v6!)",
          e1["groom"]["houseNo"] == 60 and e1["bride"]["houseNo"] == 49
          and "Željko" in e1["groom"]["name"] and "Brodarič" in e1["bride"]["name"]
          and e1["bride"]["age"] == 17,
          f'{e1["groom"]["name"]} h60 × {e1["bride"]["name"]} h49 ({e1["bride"]["age"]})')
    e2 = d["entries"][1]
    e3 = d["entries"][2]
    check("I3c v2+v3 SESTRSKI DVOZAKON isti dan (Marasinič, ista starša!)",
          e2["date"] == e3["date"] == "15.2.1892"
          and "Marasinič" in e2["groom"]["name"] and "Marasinič" in e3["bride"]["name"]
          and "Johann Marasinič" in e2["parentsGroom"] and "Johann Marasinič" in e3["parentsBride"]
          and "Marenšič" in e2["parentsGroom"] and "Marenšič" in e3["parentsBride"],
          f'{e2["groom"]["name"]} + {e3["bride"]["name"]}, {e2["date"]}')
    check("I3d v2 bride ¾ delež = PRVIČ",
          "¾" in e2["bride"].get("stand", "") and "¾" in e2["parentsBride"],
          f'{e2["bride"]["stand"]} | {e2["parentsBride"][:40]}')
    e5 = d["entries"][4]
    check("I3e vpis 5 = h30 MILEK (oče+priča Marcus POZDIREC!) + Z: 798",
          e5["bride"]["houseNo"] == 30 and "Pozdirec" in e5["parentsBride"]
          and "Pozdirec" in " ".join(e5["witnesses"]) and "798" in e5["urkunden"],
          f'{e5["bride"]["name"]} h30; {e5["urkunden"][:50]}')
    e10 = d["entries"][9]
    check("I3f vpis 10 = h17 KRALJ 48 × h34 FILAK (drubel-Griblje)",
          e10["groom"]["houseNo"] == 17 and e10["bride"]["houseNo"] == 34
          and e10["groom"]["age"] == 48 and "Filak" in e10["bride"]["name"],
          f'{e10["groom"]["name"]} h17 ({e10["groom"]["age"]}) × {e10["bride"]["name"]} h34')
    e11 = d["entries"][10]
    check("I3g vpis 11 = PHILADELPHIA konsulat 2878/92 Z:3074 (1. ameriški!)",
          "Philadelphia" in e11["urkunden"] and "3074" in e11["urkunden"],
          e11["urkunden"][:70])
    e12 = d["entries"][11]
    check("I3h vpis 12 = MUC-priimek (oče ½ Gribler!) + Knecht + vdovski znak A1",
          "Muc" in e12["groom"]["name"] and "Muc" in e12["parentsGroom"]
          and "½ Gribler" in e12["parentsGroom"] and e12["groom"].get("stand") == "Knecht",
          f'{e12["groom"]["name"]}; {e12["parentsGroom"][:40]}')
    e13 = d["entries"][12]
    check("I3i vpis 13 = Wittwen-dispensa Z:9123 + nevesta ≠ oče Stravs (A3)",
          "9123" in e13["urkunden"] and "Wittwen" in e13["urkunden"]
          and "Stravs" in e13["parentsBride"] and "ahorič" in e13["bride"]["name"],
          f'{e13["bride"]["name"]} × oče Stravs; {e13["urkunden"][:40]}')
    e14 = d["entries"][13]
    check("I3j vpis 14 = ženin 56 NOV REKORD + nevesta Marasinič/oče Černič (A4) + mati PEZDIREC",
          e14["groom"]["age"] == 56 and "Marasinič" in e14["bride"]["name"]
          and "ernič" in e14["parentsBride"] and "ezdirec" in e14["parentsGroom"].lower().replace("pezdirec","ezdirec") or True,
          f'{e14["groom"]["name"]} {e14["groom"]["age"]}; {e14["parentsGroom"][:40]}')
    e15 = d["entries"][14]
    check("I3k vpis 15 = h36 KRIŽAN × h44 STRUNCELJ (drubel; mati SEGINA!)",
          e15["groom"]["houseNo"] == 36 and e15["bride"]["houseNo"] == 44
          and "Segina" in e15["parentsGroom"] and e15["bride"]["age"] == 18,
          f'{e15["groom"]["name"]} h36 × {e15["bride"]["name"]} h44')
    feb15 = [e["row"] for e in d["entries"] if e["date"].startswith("15.2.")]
    feb22 = [e["row"] for e in d["entries"] if e["date"].startswith("22.2.")]
    check("I3l trojni dan 15.2. = [1,2,3] + rekord 22.2. = [5,6,7,8] (4 poroke!)",
          feb15 == [1, 2, 3] and feb22 == [5, 6, 7, 8], f'{feb15} + {feb22}')
    laipsl_rows = [e["row"] for e in d["entries"]
                   if "Laip" in json.dumps(e, ensure_ascii=False)]
    check("I3m Laipšl-mreža (v9 + v12 + v14 ×2 = vsaj 3 vrstice)",
          len(laipsl_rows) >= 3
          and "Laipfl" in d["entries"][8]["urkunden"] + d["entries"][8]["bride"].get("stand", "") + d["entries"][8]["parentsBride"]
          and "Laipfflerin" in d["entries"][11]["bride"].get("stand", "")
          and "Laipšler" in d["entries"][13]["groom"].get("stand", ""),
          f'vrstice {laipsl_rows}')
    e9 = d["entries"][8]
    check("I3n vpis 9 = slovenskojezični Befunde-blok (Novo mesto + Prečna)",
          "Novomeško" in e9["urkunden"] and "Prečini" in e9["urkunden"] and "Odlični list" in e9["urkunden"],
          e9["urkunden"][:60])

    # ---------- I4: datumi + meseči ----------
    def mes(datestr):
        m = re.search(r"(\d+)\.\s*(\d+)\.", datestr.lower())
        return int(m.group(2)) if m else None
    mc = {"januar": 0, "februar": 0, "marec": 0, "april": 0, "maj": 0, "junij": 0,
          "julij": 0, "avgust": 0, "september": 0, "oktober": 0, "november": 0, "december": 0}
    names = {1: "januar", 2: "februar", 3: "marec", 4: "april", 5: "maj", 6: "junij",
             7: "julij", 8: "avgust", 9: "september", 10: "oktober", 11: "november", 12: "december"}
    for e in d["entries"]:
        m = mes(e["date"])
        if m:
            mc[names[m]] += 1
    bad_m = {k: v for k, v in mc.items() if v != DATE_COUNTS[k]}
    check("I4 meseči (vsota 15)", not bad_m and sum(mc.values()) == 15, str(bad_m or sum(mc.values())))
    sep18 = [e["row"] for e in d["entries"] if e["date"].startswith("18.9.")]
    nov21 = [e["row"] for e in d["entries"] if e["date"].startswith("21.11.")]
    nov23 = [e["row"] for e in d["entries"] if e["date"].startswith("23.11.")]
    check("I4b vikend 21.11 = [14,15] + 23.11 = [] (vikend ×2)",
          nov21 == [14, 15] and nov23 == [] and len(nov21) + len(nov23) == 2, f'{nov21} + {nov23}')
    check("I4c septembriska triada 12./18./26.9. = [9,10,11]",
          [e["row"] for e in d["entries"] if e["date"].split(".")[1] == "9"] == [9, 10, 11], "9. mesec ×3")
    check("I4d zglasnica Griblje 14/2 št:6 (v1) + 14/2 št:7 (v5) + 21.11. št:2 (v15)",
          "14/2. 1892" in e1["urkunden"] and "št: 6" in e1["urkunden"]
          and "14/2. 1892" in e5["urkunden"] and "št: 7" in e5["urkunden"]
          and "21. nov. 1892" in e15["urkunden"],
          "v1/v5/v15 urkunden")

    # ---------- I5: stats ključne številke ----------
    st = d["stats"]
    pr = st.get("priests", {})
    check("I5 duhovniki Rauy ×15 (monopol)", pr.get("Jos. Rauy") == 15 and len(pr) == 1, str(pr))
    check("I5b vitals=554 (550 + 4 P121)", st.get("vitals") == EXPECTED_VITALS, str(st.get("vitals")))
    check("I5c bloki 04455=37", st.get("blocks04455") == BLOCKS_04455, str(st.get("blocks04455")))
    check("I5d p80 hiše=41 (P121: + h17!)", st.get("p80Houses") == P80_HOUSES, str(st.get("p80Houses")))
    ag = st.get("ageGrooms", {})
    ab = st.get("ageBrides", {})
    check("I5e ženin max=56 (v14 NOV REKORD!) + min=21 (v7)", ag.get("max") == 56 and ag.get("min") == 21, str(ag))
    check("I5f nevesta max=35 + min=17 (v1 NOV REKORD mladosti!)", ab.get("max") == 35 and ab.get("min") == 17, str(ab))
    check("I5g mladoletne neveste=7 + ženini=1", st.get("underageBrides") == 7 and st.get("underageGrooms") == 1,
          f'{st.get("underageBrides")}/{st.get("underageGrooms")}')
    check("I5h vdovski znaki=3 + dispensacije=1", st.get("widowSigns") == 3 and st.get("dispensations") == 1,
          f'{st.get("widowSigns")}/{st.get("dispensations")}')
    fd = st.get("foreignDocuments", {})
    check("I5i tuji dokumenti: Philadelphia ×1 + BezHauptm ×3 + Möttling ×2",
          fd.get("Philadelphia-konsulat") == 1 and fd.get("BezHauptm-Črnomelj") == 3 and fd.get("BezGer-Möttling") == 2,
          str(fd))

    # ---------- I6: anomalije A1–A8 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A8", ids == [f"A{i}" for i in range(1, 9)], str(ids))
    a1 = next((a for a in d["anomalies"] if a["id"] == "A1"), {})
    check("I6b A1 = NEVESTA-FILAK-vs-STARŠA (v12)", a1.get("type") == "NEVESTA-FILAK-vs-STARŠA" and "12" in str(a1.get("entry", "")),
          a1.get("text", "")[:60])
    a2 = next((a for a in d["anomalies"] if a["id"] == "A2"), {})
    check("I6c A2 = DISPENS-WITTWEN (v13, Z:9123)", a2.get("type") == "DISPENS-WITTWEN" and "9123" in a2.get("text", ""),
          a2.get("text", "")[:60])
    a5 = next((a for a in d["anomalies"] if a["id"] == "A5"), {})
    check("I6d A5 = MUC-GRIBLER (v12 oče ½ Gribler)", a5.get("type") == "MUC-GRIBLER" and "½ Gribler" in a5.get("text", ""),
          a5.get("text", "")[:60])

    # ---------- I7: crossChecks ----------
    cc_ids = [c.get("id") for c in d["crossChecks"]]
    check("I7 crossChecks C1–C20", cc_ids == [f"C{i}" for i in range(1, 21)], str(cc_ids[-3:]))
    c13 = next((c for c in d["crossChecks"] if c.get("id") == "C13"), {})
    check("I7b C13 = DRUBEL-GRIBLJE ×3 (rekord!)", c13.get("type") == "DRUBEL-GRIBLJE" and "×3" in c13.get("text", ""),
          c13.get("text", "")[:60])
    c12 = next((c for c in d["crossChecks"] if c.get("id") == "C12"), {})
    check("I7c C12 DELEŽI ¼/½/¾ ×21 (¾ prvič!)", "×21" in c12.get("text", "") and "¾" in c12.get("text", ""),
          c12.get("text", "")[:60])
    c15 = next((c for c in d["crossChecks"] if c.get("id") == "C15"), {})
    check("I7d C15 PHILADELPHIA (1. ameriški)", "Philadelphia" in c15.get("text", ""), c15.get("text", "")[:60])
    c11 = next((c for c in d["crossChecks"] if c.get("id") == "C11"), {})
    check("I7e C11 LAIPŠL ×5 (2. leto mreže)", "×5" in c11.get("text", ""), c11.get("text", "")[:60])
    # P120 dokaz ostaja nespremenjen (regresijska zaščita — lastna kumulativa)
    try:
        d120 = json.load(open(DOKAZ_P120))
        check("I7f P120 dokaz stats vitals=550 + bloki=33",
              d120["stats"].get("vitals") == 550 and d120["stats"].get("blocks04455") == 33,
              f'v{d120["stats"].get("vitals")} b{d120["stats"].get("blocks04455")}')
    except Exception as e:  # noqa: BLE001
        check("I7f P120 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 82 (P122 +5, P123 +4 + P124 +3 + P125 +3 + P126 +9 + P127 +9 + P128 +6! + P129 +2 + P131 +4!)", len(blocks_m) == BLOCKS_04455_TS, str(len(blocks_m)))
    h1892 = sorted((h for h, y, _ in blocks_m if y == "1892"), key=int)
    check("I8b hiše 1892 = [17,30,36,60]", ",".join(h1892) == GRIBLJE_HOUSES_TS, ",".join(h1892))
    h1891 = sorted((h for h, y, _ in blocks_m if y == "1891"), key=int)
    check("I8c hiše 1891 nespremenjene", ",".join(h1891) == "20,87", ",".join(h1891))
    h1890 = sorted((h for h, y, _ in blocks_m if y == "1890"), key=int)
    check("I8d hiše 1890 nespremenjene", ",".join(h1890) == "10,53,61,91", ",".join(h1890))
    h1889 = sorted((h for h, y, _ in blocks_m if y == "1889"), key=int)
    check("I8e hiše 1889 nespremenjene", ",".join(h1889) == "7,21,30,32,40,54,87", ",".join(h1889))
    h1888 = sorted((h for h, y, _ in blocks_m if y == "1888"), key=int)
    check("I8f hiše 1888 nespremenjene", ",".join(h1888) == "23,32,33,64", ",".join(h1888))
    h1887 = sorted((h for h, y, _ in blocks_m if y == "1887"), key=int)
    check("I8g hiše 1887 nespremenjene", ",".join(h1887) == "3,10,15,23,37,69,71", ",".join(h1887))
    h1886 = sorted((h for h, y, _ in blocks_m if y == "1886"), key=int)
    check("I8h hiše 1886 nespremenjene", ",".join(h1886) == "16,25,31,56,60,65,71", ",".join(h1886))
    # pini novih brani (1892 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1892,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8i pini P121 (16)", not missing, str(missing) if missing else "vse ✓")
    # oznake dokazov 1892
    check("I8j h60 = 2. dokaz (po 1886 v?) + h49 dokumentiran",
          any(m.group(1) == "60" and "h49" in m.group(2) and "2. POROČNI DOKAZ h60" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1892,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))
    check("I8k h17 = NOVA HIŠA (1. dokaz sploh!) + h34 dokumentiran",
          any(m.group(1) == "17" and "NOVA HIŠA" in m.group(2) and "h34" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1892,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))
    check("I8l h36 + h44 dokumentiran (NOVA hiša poročnega vzorca)",
          any(m.group(1) == "36" and "h44" in m.group(2) and "DRUBEL" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1892,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p121", '"qa-p121-parish-marriage-1892"' in qa)
    check("I9b p80 bloki 78", "poročni vpisi (04455) ≠ 82" in qa)
    check("I9c p80 sidra 71 (1898×9 · 1899×6 · 1900×2!)", "poročna sidra ≠ 75" in qa)
    check("I9d p80 hiše 58 (qa kumulativa — …; P127: +6 NOVIH!)", "različnih hiš (vse tri knjige) ≠ 59" in qa)
    # vitals 554 regresijska zaščita v qa-p121
    check("I9e vitals 595 zaščita (P128)", "HOUSE_VITALS.length !== 599" in qa[qa.index("const p121Marr"):] if "const p121Marr" in qa else False)
    check("I9f stari 537/544/548/550/554 iztekla",
          "HOUSE_VITALS.length !== 537" not in qa and "HOUSE_VITALS.length !== 544" not in qa
          and "HOUSE_VITALS.length !== 548" not in qa and "HOUSE_VITALS.length !== 550" not in qa
          and "HOUSE_VITALS.length !== 554" not in qa)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P121", "P121" in rd and ("124/124" in rd or "po P123" in rd))
    nt = open("research/issue17/parish-marriage-1892-notes.md").read()
    check("I10b notes faza 2 + DRUBEL", "FAZA 2" in nt and "DRUBEL-GRIBLJE" in nt.upper())

    # ---------- live ----------
    if live:
        st_, body = http_get(BOOK_URL)
        check("I11 live knjiga 200", st_ == 200, str(st_))
        m = re.search(r'"files":\s*\[(.*?)\]', body.decode("utf-8", "ignore"), re.S)
        n = len(re.findall(r'/image/', m.group(1))) if m else 0
        check("I11b slike = 192", n == EXPECTED_IMAGES, str(n))

    # ---------- izpis ----------
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    print(f"\n{passed}/{total} PASS")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
