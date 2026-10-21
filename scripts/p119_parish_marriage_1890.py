#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P119 — župnija Podzemelj: poročna knjiga 04455, polno leto 1890 (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → P116 = 1887 → P117 = 1888 → P118
= 1889): okvir POTRJEN — skeni 77–79 == Pag. 76–78 (Pag. == sken − 1, 5.
potrditev; velja v 71–79); **16 vpisov = NAJVEČJE LETO LINIJE** (1886:7 →
1887:21 → 1888:20 → 1889:10 → 1890:16; razpored 6+5+5); velika glava
»Traunungs=Buch« na Pag. 76 (vsako leto novo zvezek-glavo). LANDSCAPE
geometrija (~2484–2525×1800). Glava 1891 = Pag. 79 = s80 (P120 lead).

FAZA 2: **16/16 vpisov transkribiranih OBOJESTRANSKO** + ~40 mega-zoomov
×3–10 + control-stripi ctl77/78/79. **FAZA-1 ORIS POPRAVKI ×12**: v1 »Nuc«
→ MUC (oče Nicolaus!) + v3 »Eva Pirmat« → ROSA Pirmat, Inwohnerina, Gradac
71 + v5 »Maslaving/Guvlášofn« → Hrasinec? / Michaël ŠURAJEVČIČ + v6
GRIBLJE 53 (NOVA hiša!) 51 let + v7 »Pirnosta/Tore« → Primostek 19 / Maria
TOME + v9 rojen Zavrh 41, PF. BOROVNICA + v13 »Haaspić 9 / Johann Wolf« →
CERKVIŠČE 9 / Johann HVALJ × Maria HARASIMIČ 44 (Cerkvišče 14) + v14
»Gufsslor« = Gütlstar? [~] (3. pojav!) + v15 »Nov 21« → Nov 24 + v16 »Nov
27/Kokoljič« → Nov 24 / Johann HARASIMIČ × Maria HVALJ.

NOVELE: **DVOJNI POROČNI VIKEND 23–24.11. = 4 POROKE** (v13+v14 na 23.,
v15+v16 na 24.; zgłasnice Podzemelj 21/11 st:12+13 isti dan!) +
**PREKRIŽANA POROKA HVALJ × HARASIMIČ** (v13 Hvalj 49 × Harasimič 44; v16
Harasimič 24 × Hvalj 24 — sorojenci obeh strani!) + **2 SORODSTVENI
DISPENSACIJI — 1. leto z 2!** (v11 bratranca 3. stopnje, matere Marije
Zugelj = sestri, Ordinariat Laibach 11.8. № 1840; v14 4. kanonska stopnja
10.11. № 2619) + **ZUGELJ bratski par** (v10+v11 Dobravice 11, isti starši
Georg × Anna Vermanič — 2. bratski par po 1888 Brinec!) + **NEVESTA 45
LET** (v5 Ana Agnič = rekord linije!) + **simetrija 41=41** (v4) +
**lomek 19¾** (v7 nevesta; Kurrent »19z«) + NOVI STATUSI: Inwohnerina
(v3), VORMUND v očetovem stolpcu (v3), Kürschner (v5), WIRT-priča (v10),
Gütlarin [~] (v4+v13), **¾ GÜTL ulomek** (v14 — 3. nov ulomek po ⅓ 1889!) +
**4. DUHOVNIK LINIJE = MICHAEL BULOVEC pro t. deleg. Semič** (v4!) +
Ordinariat Laibach številke ×3 (Z:132 v5 + № 1840 v11 + № 2619 v14) +
sodna № 187/208 (v9) + Z:216 (v10) + **mladoletnost 6/16 = 37.5%** (v2 18
edino MÜTTERL. soglasje!) + **zgłasnice 16/16 = 100%** (Podzemelj ×8 +
Gradac ×4 + Griblje ×4; Griblje 1→16→36→39 časovno 1:1!) + Metlika ×2
(v4 h22 + v12 h24) + Pf. Borovnica migracija (v9) + tuje župnije ×8.

MREŽE: **PERDINEC/PEGDIREC ×8** (2 pisavi!) + **MARENTIČ ×5 + ŠURAJEVČIČ
×5 + ZUGELJ ×6 + MUC ×5 + POŽEK ×5 + TOME ×5 + HRIŽAN ×5 + BRINEC ×4 +
JAKŠA ×4 + STRAUS ×4 + SIMEC ×4 + MILEK/KLEPEC/DRAGOŠ/KURE/HARASIMIČ/KURE
×3**; GRIBLJE: 3 poroke / 4 hiše — h53 = **NOVA HIŠA (1. dokaz sploh!)** +
h91/h61 2. familiji (krstna 1887!) + h10 2. poročni dokaz (1887 v20!) —
**bloki 04455 = 31; vitals 548; p80 hiše 46** (h91 + h53 NOVI v vzorcu!).
Skripta scripts/p119_parish_marriage_1890.py (I1–I11, --check izpiše
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
DOKAZ = "research/issue17/parish-marriage-1890.json"
DOKAZ_P118 = "research/issue17/parish-marriage-1889.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"

FRAME_SCANS = (77, 78, 79)          # 77 = Pag. 76 (v1–6) · 78 = Pag. 77 (v7–11) · 79 = Pag. 78 (v12–16)
FRAME_PAGES = (76, 77, 78)
EXPECTED_ENTRIES = 16
EXPECTED_EXCLUDED = 4
EXPECTED_ANOMALIES = 13
EXPECTED_CROSSCHECKS = 26
GRIBLJE_ROWS = [1, 6, 15]
GRIBLJE_MARRIAGES = 3
GRIBLJE_HOUSES_TS = "10,53,61,91"   # hiše z 1890 bloki v parish.ts
EXPECTED_VITALS = 548               # P119 dokaz lastna kumulativa (544 + 4 bloki)
BLOCKS_04455 = 31                   # 27 (P118) + 4 novih blokov 1890 (P119)
BLOCKS_04455_TS = 61              # P126: + 9 blokov 1897 (52 + 9)                # parish.ts zdaj = 49 (P121 +4 bloki 1892 + P122 +5 bloki 1893 + P123 +4 bloki 1894 + P124 +3 bloki 1895)
P80_HOUSES = 46                     # 44 (P118) + h91 + h53 NOVI v vzorcu (h10/h61 že)
DATE_COUNTS = {"januar": 1, "februar": 2, "marec": 0, "april": 1, "maj": 3,
               "junij": 1, "julij": 1, "avgust": 3, "september": 0, "oktober": 0,
               "november": 4, "december": 0}
# P119 pini (blok-houseNo → obvezen fragment v whatSi; cf. qa-p119)
BLOCK_PINS = [
    ("91", "Muc"), ("91", "Vgornjed"), ("91", "Japplič"),
    ("10", "Kure"), ("10", "Magd"), ("10", "Špala"),
    ("53", "Perdinec"), ("53", "NOVA HIŠA"), ("53", "Hrižan"), ("53", "Otok"),
    ("61", "Požek"), ("61", "Dragoš"), ("61", "Straus"), ("61", "Muc bajtar"),
]
# stara branja = IZTELA iz 04455 blokov (natančni faza-1 fragmenti)
OLD_READINGS = [
    "Johann Nuc", "Haaspić", "Kokoljič", "Maslaving", "Guvlášofn", "Pirnosta",
]


def http_get(url, headers=None, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers or UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read()
        except Exception as e:  # noqa: BLE001
            import time
            time.sleep(2 + i * 2)
            last = e
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
    check("I1b entries=16", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1c excluded=4", len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))
    check("I1d anomalije=13", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=26", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (16/16)", not bad, str(bad) if bad else "vse ✓")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 skeni 77–79", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2b strani 76–78", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))
    check("I2c Pag. == sken − 1 (5. potrditev)", "sken − 1" in fr.get("pagRule", ""), fr.get("pagRule", "")[:60])
    check("I2d velika glava Traunungs=Buch", "Traunungs=Buch" in fr.get("bigHeader", ""), fr.get("bigHeader", "")[:60])
    rows_f = fr.get("rows", {})
    check("I2e vrstice s77/s78/s79", all(k in rows_f for k in ("s77", "s78", "s79")), str(list(rows_f.keys())))
    rows = [e["row"] for e in d["entries"]]
    check("I2f vrstice 1–16 zapored", rows == list(range(1, 17)), str(rows))
    sc = [e["scan"] for e in d["entries"]]
    check("I2g skeni znotraj 77–79", all(77 <= s <= 79 for s in sc), str(sorted(set(sc))))
    per = {77: 6, 78: 5, 79: 5}
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2h razpored 6+5+5", raz == per, str(raz))
    lead = d.get("lead", {})
    check("I2i P120 lead (poročna 1891, s80)", "P120" in lead.get("next", "") and "1891" in lead.get("next", "")
          and "s80" in lead.get("frame", ""), f'{lead.get("next", "")} | {lead.get("frame", "")[:40]}')

    # ---------- I3: ključni vpisi ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [1,6,15]", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 3", d["stats"].get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(d["stats"].get("gribljeMarriages")))
    check("I3a Griblje hiše = [10,53,61,91]", d["stats"].get("gribljeHouses") == [10, 53, 61, 91],
          str(d["stats"].get("gribljeHouses")))
    e1 = d["entries"][0]
    check("I3b vpis 1 = h91 × h10 (Muc × Kure; ne »Nuc«!)",
          e1["groom"]["houseNo"] == 91 and e1["bride"]["houseNo"] == 10
          and "Muc" in e1["groom"]["name"] and "Nuc" not in e1["groom"]["name"]
          and "Kure" in e1["bride"]["name"],
          f'{e1["groom"]["name"]} h91 × {e1["bride"]["name"]} h10')
    e6 = d["entries"][5]
    check("I3c vpis 6 = h53 NOVA × Otok 20 (Perdinec 51!)",
          e6["groom"]["houseNo"] == 53 and e6["bride"]["houseNo"] == 20
          and e6["groom"]["age"] == 51 and "Perdinec" in e6["groom"]["name"],
          f'{e6["groom"]["name"]} h53, {e6["groom"]["age"]} let × Otok 20')
    e15 = d["entries"][14]
    check("I3d vpis 15 = h61 (Požek 29 × Dragoš)",
          e15["groom"]["houseNo"] == 61 and e15["groom"]["age"] == 29
          and "Požek" in e15["groom"]["name"] and "Dragoš" in e15["bride"]["name"],
          f'{e15["groom"]["name"]} h61 × {e15["bride"]["name"]}')
    e5 = d["entries"][4]
    check("I3e vpis 5 = NEVESTA 45 LET (rekord linije!)",
          e5["bride"]["age"] == 45 and "Agnič" in e5["bride"]["name"],
          f'{e5["bride"]["name"]}, {e5["bride"]["age"]}')
    e4 = d["entries"][3]
    check("I3f vpis 4 = simetrija 41=41 + Bulovec (4. duhovnik linije!)",
          e4["groom"]["age"] == 41 and e4["bride"]["age"] == 41
          and "Bulovec" in e4["priest"],
          f'{e4["groom"]["age"]} × {e4["bride"]["age"]}; {e4["priest"][:40]}')
    e11 = d["entries"][10]
    check("I3g vpis 11 = dispensacija 3. st. № 1840 + BRATA z v10 (isti starši!)",
          "1840" in e11["urkunden"] and "3 [Verwandtschafts-]Grad" in e11["urkunden"]
          and "ISTI kot v10" in e11["parentsGroom"],
          f'№ 1840; starši: {e11["parentsGroom"][:50]}')
    e14 = d["entries"][13]
    check("I3h vpis 14 = dispensacija 4. st. № 2619 + ¾ Gütl nevesta",
          "2619" in e14["urkunden"] and "4ten Can. Grad" in e14["urkunden"]
          and "¾ Gütlarstochter" in e14["bride"].get("stand", ""),
          f'№ 2619; {e14["bride"].get("stand", "")[:40]}')
    e13 = d["entries"][12]
    e16 = d["entries"][15]
    check("I3i prekrižana poroka HVALJ × HARASIMIČ (v13 ↔ v16!)",
          e13["groom"]["houseNo"] == 9 and e13["bride"]["houseNo"] == 14
          and "Hvalj" in e13["groom"]["name"] and "Harasimič" in e13["bride"]["name"]
          and e16["groom"]["houseNo"] == 14 and e16["bride"]["houseNo"] == 9
          and "Harasimič" in e16["groom"]["name"] and "Hvalj" in e16["bride"]["name"],
          f'v13: h9 × h14; v16: h14 × h9')
    e2 = d["entries"][1]
    check("I3j vpis 2 = MÜTTERL. soglasje (edino! nevesta 18)",
          "mütterliche Einwilligung" in e2["urkunden"] and e2["bride"]["age"] == 18,
          e2["urkunden"][:60])
    e9 = d["entries"][8]
    check("I3k vpis 9 = rojen Zavrh 41 PF. BOROVNICA + № 187/208",
          "Zavrh 41" in e9["groom"].get("village", "") and "Borovnica" in e9["groom"].get("village", "")
          and "187/208" in e9["urkunden"],
          f'{e9["groom"].get("village", "")[:50]}')
    e10 = d["entries"][9]
    check("I3l vpis 10 = Dobravice 11 + Z: 216",
          e10["groom"]["village"] == "Dobravice" and e10["groom"]["houseNo"] == 11
          and "Z: 216" in e10["urkunden"],
          f'{e10["groom"]["village"]} {e10["groom"]["houseNo"]}')

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
    check("I4 meseči (vsota 16)", not bad_m and sum(mc.values()) == 16, str(bad_m or sum(mc.values())))
    nov23 = [e["row"] for e in d["entries"] if e["date"].startswith("23.11.")]
    nov24 = [e["row"] for e in d["entries"] if e["date"].startswith("24.11.")]
    check("I4b dvojni vikend 23.11 = [13,14]", nov23 == [13, 14], str(nov23))
    check("I4c dvojni vikend 24.11 = [15,16]", nov24 == [15, 16], str(nov24))
    zglas13 = "st: 12" in e13["urkunden"] and "21/11" in e13["urkunden"]
    zglas16 = "st: 13" in e16["urkunden"] and "21/11" in e16["urkunden"]
    check("I4d zgłasnici Podzemelj 21/11 st:12+13 (isti dan!)", zglas13 and zglas16,
          f'v13: {e13["urkunden"][:40]} | v16: {e16["urkunden"][:40]}')

    # ---------- I5: stats ključne številke ----------
    st = d["stats"]
    pr = st.get("priests", {})
    check("I5 duhovniki Rauy ×15 + Bulovec ×1",
          pr.get("Jos. Rauy") == 15 and pr.get("Michael Bulovec") == 1, str(pr))
    check("I5b vitals=548 (544 + 4 P119)", st.get("vitals") == EXPECTED_VITALS, str(st.get("vitals")))
    check("I5c bloki 04455=31", st.get("blocks04455") == BLOCKS_04455, str(st.get("blocks04455")))
    check("I5d p80 hiše=46 (h91 + h53 NOVI!)", st.get("p80Houses") == P80_HOUSES, str(st.get("p80Houses")))
    ag = st.get("ageGrooms", {})
    ab = st.get("ageBrides", {})
    check("I5e najstarejši ženin=51 (v6 Perdinec h53)", ag.get("max") == 51, str(ag))
    check("I5f najstarejša nevesta=45 (rekord linije!)", ab.get("max") == 45, str(ab))
    check("I5g najmlajša nevesta=18 (v2 mütterl.)", ab.get("min") == 18, str(ab))
    check("I5h mladoletne neveste=6 (37.5%)", st.get("underageBrides") == 6, str(st.get("underageBrides")))
    check("I5i dispensacije=2 (1. leto z 2!)", st.get("dispensations") == 2, str(st.get("dispensations")))

    # ---------- I6: anomalije A1–A13 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A13", ids == [f"A{i}" for i in range(1, 14)], str(ids))
    a2 = next((a for a in d["anomalies"] if a["id"] == "A2"), {})
    check("I6b A2 = Hvalj/Harasimič mismatch (vdova roj. Hvalj)",
          a2.get("type") == "MISMATCH" and "Hvalj" in a2.get("text", ""), a2.get("text", "")[:60])
    a3 = next((a for a in d["anomalies"] if a["id"] == "A3"), {})
    check("I6c A3 = Gütlstar 3. pojav", "Gütlstar" in a3.get("text", "") and "3. pojav" in a3.get("text", ""),
          a3.get("text", "")[:60])
    a11 = next((a for a in d["anomalies"] if a["id"] == "A11"), {})
    check("I6d A11 = h61 Muc-vs-Požek", "61" in a11.get("text", "") and "Muc" in a11.get("text", "")
          and "Požek" in a11.get("text", ""), a11.get("text", "")[:60])

    # ---------- I7: crossChecks ----------
    cc_ids = [c.get("id") for c in d["crossChecks"]]
    check("I7 crossChecks C1–C26", cc_ids == [f"C{i}" for i in range(1, 27)], str(cc_ids[-3:]))
    c1 = next((c for c in d["crossChecks"] if c.get("id") == "C1"), {})
    check("I7b C1 = MUC ×5", c1.get("type") == "MUC" and "×5" in c1.get("text", ""), c1.get("text", "")[:50])
    c6 = next((c for c in d["crossChecks"] if c.get("type") == "ZUGELJ"), {})
    check("I7c C6 ZUGELJ bratski par (v10+v11)", "bratsk" in c6.get("text", "").lower()
          or "isti starši" in c6.get("text", "").lower(), c6.get("text", "")[:60])
    c23 = next((c for c in d["crossChecks"] if c.get("type") == "SORODSTVO"), {})
    check("I7d C23 SORODSTVO 2 dispensaciji", "1840" in c23.get("text", "") and "2619" in c23.get("text", ""),
          c23.get("text", "")[:60])
    # P118 dokaz ostaja nespremenjen (regresijska zaščita — lastna kumulativa)
    try:
        d118 = json.load(open(DOKAZ_P118))
        check("I7e P118 dokaz stats vitals=544 + bloki=27",
              d118["stats"].get("vitals") == 544 and d118["stats"].get("blocks04455") == 27,
              f'v{d118["stats"].get("vitals")} b{d118["stats"].get("blocks04455")}')
    except Exception as e:  # noqa: BLE001
        check("I7e P118 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 61 (P121 +4, P122 +5, P123 +4 + P124 +3 + P125 +3 + P126 +9!)", len(blocks_m) == BLOCKS_04455_TS, str(len(blocks_m)))
    h1890 = sorted((h for h, y, _ in blocks_m if y == "1890"), key=int)
    check("I8b hiše 1890 = [10,53,61,91]", ",".join(h1890) == GRIBLJE_HOUSES_TS, ",".join(h1890))
    h1889 = sorted((h for h, y, _ in blocks_m if y == "1889"), key=int)
    check("I8c hiše 1889 nespremenjene", ",".join(h1889) == "7,21,30,32,40,54,87", ",".join(h1889))
    h1888 = sorted((h for h, y, _ in blocks_m if y == "1888"), key=int)
    check("I8d hiše 1888 nespremenjene", ",".join(h1888) == "23,32,33,64", ",".join(h1888))
    h1887 = sorted((h for h, y, _ in blocks_m if y == "1887"), key=int)
    check("I8e hiše 1887 nespremenjene", ",".join(h1887) == "3,10,15,23,37,69,71", ",".join(h1887))
    h1886 = sorted((h for h, y, _ in blocks_m if y == "1886"), key=int)
    check("I8f hiše 1886 nespremenjene", ",".join(h1886) == "16,25,31,56,60,65,71", ",".join(h1886))
    # pini novih brani (1890 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1890,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8g pini P119 (14)", not missing, str(missing) if missing else "vse ✓")
    whatsis = [m.group(1) for m in re.finditer(r'bookSignature:\s*"04455",\s*year:\s*\d{4},\s*scan:\s*\d+,\s*page:\s*\d+,\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)]
    stale = []
    for o in OLD_READINGS:
        for w in whatsis:
            i = w.find(o)
            while i != -1:
                ctx = w[max(0, i - 60):i]
                # sklic na popravek (»ne »X«« / »oris ... = popravek« / faza-1) ni staro branje
                if not any(t in ctx for t in ("ne »", "popravek", "faza-1", "oris »")):
                    stale.append((o, w[max(0, i - 30):i + len(o) + 20]))
                    break
                i = w.find(o, i + 1)
    check("I8h stara branja iztekla", not stale, str(stale) if stale else "vse ✓")
    # oznake dokazov 1890
    check("I8i h53 = »NOVA HIŠA« (1. dokaz sploh!)",
          any(m.group(1) == "53" and "NOVA HIŠA" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1890,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))
    check("I8j h10 = »2. poročni dokaz h10« (1887 v20! — v obeh blokih v1!)",
          sum(1 for w in whatsis if "2. poročni dokaz h10" in w) >= 1,
          str(sum(1 for w in whatsis if "2. poročni dokaz h10" in w)))
    check("I8k h91 + h61 = »2. familia« (krstna 1887!)",
          sum(1 for w in whatsis if "2. familia" in w and ("h91" in w or "h61" in w)) == 2,
          str(sum(1 for w in whatsis if "2. familia" in w)))

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p119", '"qa-p119-parish-marriage-1890"' in qa)
    check("I9b qa-p115 bloki 61", "poročni bloki (04455) ≠ 61" in qa)
    check("I9c p80 bloki 61", "poročni vpisi (04455) ≠ 61" in qa)
    check("I9d p80 sidra 54 (1897×9!)", "poročna sidra ≠ 54" in qa)
    # vitals 550 regresijska zaščita v qa-p119
    check("I9e vitals 578 zaščita (P126)", "HOUSE_VITALS.length !== 578" in qa[qa.index("const p119Marr"):] if "const p119Marr" in qa else False)
    check("I9f stari 537/544 iztekla", "HOUSE_VITALS.length !== 537" not in qa and "HOUSE_VITALS.length !== 544" not in qa)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P119", "P119" in rd and ("124/124" in rd or "po P123" in rd))
    nt = open("research/issue17/parish-marriage-1890-notes.md").read()
    check("I10b notes faza 2 + prekrižana", "FAZA 2" in nt and "PREKRIŽANA" in nt.upper())

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
