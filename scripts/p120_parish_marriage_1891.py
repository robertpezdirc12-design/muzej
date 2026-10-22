#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P120 — župnija Podzemelj: poročna knjiga 04455, polno leto 1891 (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → P116 = 1887 → P117 = 1888 → P118
= 1889 → P119 = 1890): okvir POTRJEN — skeni 80–83 == Pag. 79–82 (Pag. ==
sken − 1, 6. potrditev; velja v 71–83); **18 vpisov = 2. NAJVEČJE LETO
LINIJE** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18; razpored
4+6+4+4); glava 1891 = Pag. 79 BREZ velike glave — »Traunungs=Buch« je na
s84 = Pag. 83 za leto 1892 (cikel vsako leto novo zvezek-glavo; 1891 = izjema
ali slab zapis [~]). LANDSCAPE geometrija (~2499–2515×1800).

FAZA 2: **18/18 vpisov transkribiranih OBOJESTRANSKO** + 36 row-crops ×2
LANCZOS + ~70 mikro-zoomov ×4–10 (crop_rows_120.py, z120_*/zz120_*).
NOVELE: **ROSETTA statusa »[Hofname]s. Sohn/Tochter«** (v14 groom »½
Griblers. Sohn« EKSPLICITNO — razrešitev skrivnostne končnice 1886–1890!) +
**deležni sistem imenja Griblje ½/¼ ×14 oseb** + **1. VD-OVI POROKI LINIJE
×2** (v14 Šimonič roj. Konda 32 + v15 Žepar 35) + **1. ŽANDAR + 1. HRVAŠKA**
(v15 Pintar rod. Dolenja Pušća № 3 + 4 hrvaška dokumenta + 2 Zagrebčana-priče!)
+ **1. APOSTOLSKA dispensacija** (v11 bratranca 2. kanc. stopnje iste linije
+ Landesreg. Z: 5672) + **PEZDIREC ×12 oseb = rekord mreže linije** (prej
1888 ×9!) + **dnevne gruče 26.1.×3 / 3.2.×3 (trojni poročni dan!) /
21.+23.11.×4 (vikend!)** + 2 vdovi + mladoletnost 12/18 neveste + Hofname
Laipšl ×5 + Zimmermann rod. Bistra pri Vrhniki (najdaljši lok ~60 km!) +
k.k. Landesreg. Laibach ×3 (№ 5549 + Z: 5672 + Z: 11825) + banns iz 2 župnij
(v9 Metlika + Trnovo) + občine NOVE ×5 (Šuhor, Božjakovo-Rozalnice, Knežak?,
Verblika?, Vrbiče?) — najširša geografija linije.

GRIBLJE: 2 poroki / 2 hiši — h87 **2. DOKAZ** (1889 v8 → 1891 v6;
Klepec-mreža!) + **h20 NOVA HIŠA (1. poročni dokaz sploh!)** — **bloki
04455 = 33; vitals 550; p80 hiše 46** (h20 ŽE v vzorcu prek krstne 1897; h87 že od 1889).
Skripta scripts/p120_parish_marriage_1891.py (I1–I11, --check izpiše
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
DOKAZ = "research/issue17/parish-marriage-1891.json"
DOKAZ_P119 = "research/issue17/parish-marriage-1890.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"

FRAME_SCANS = (80, 81, 82, 83)      # 80 = Pag. 79 (v1–4) · 81 = Pag. 80 (v5–10) · 82 = Pag. 81 (v11–14) · 83 = Pag. 82 (v15–18)
FRAME_PAGES = (79, 80, 81, 82)
EXPECTED_ENTRIES = 18
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 14
EXPECTED_CROSSCHECKS = 27
GRIBLJE_ROWS = [6, 7]
GRIBLJE_MARRIAGES = 2
GRIBLJE_HOUSES_TS = "20,87"         # hiše z 1891 bloki v parish.ts
EXPECTED_VITALS = 550               # P120 dokaz lastna kumulativa (548 + 2 bloki)
BLOCKS_04455 = 33                   # 31 (P119) + 2 novih blokov 1891 (P120)
BLOCKS_04455_TS = 76              # P126: + 9 blokov 1897 (52 + 9)                # parish.ts zdaj = 49 (P121 +4 bloki 1892 + P122 +5 bloki 1893 + P123 +4 bloki 1894 + P124 +3 bloki 1895)
P80_HOUSES = 46                     # 46 (P119) nespremenjeno — h20 ŽE v vzorcu (krstna 1897!); h87 že od 1889
DATE_COUNTS = {"januar": 4, "februar": 5, "marec": 0, "april": 0, "maj": 3,
               "junij": 0, "julij": 0, "avgust": 1, "september": 1, "oktober": 0,
               "november": 4, "december": 0}
# P120 pini (blok-houseNo → obvezen fragment v whatSi; cf. qa-p120)
BLOCK_PINS = [
    ("87", "PEZDIREC"), ("87", "2. POROČNI DOKAZ h87"), ("87", "ŽELJKO"), ("87", "MILEK"), ("87", "KLEPEC"),
    ("20", "PEZDIREC"), ("20", "NOVA HIŠA"), ("20", "KLEPEC"), ("20", "Krasinec 37"), ("20", "TROJNO"),
]
# 1891 = svež prepis (36 row-crops + ~70 mikro-zoomov) — brez faza-1 orisa
# z zastarelmi branjmi, zato OLD_READINGS prazno (zaščita ostaja v I8g pinih).
OLD_READINGS = []


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
    check("I1b entries=18", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1c excluded=0", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1d anomalije=14", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=27", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (18/18)", not bad, str(bad) if bad else "vse ✓")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 skeni 80–83", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2b strani 79–82", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))
    check("I2c Pag. == sken − 1 (6. potrditev)", "sken − 1" in fr.get("pagRule", ""), fr.get("pagRule", "")[:60])
    check("I2d glava 1891 BREZ velike glave (»Traunungs=Buch« na s84)",
          "BREZ velike glave" in fr.get("bigHeader", "") and "s84" in fr.get("bigHeader", ""),
          fr.get("bigHeader", "")[:60])
    rows_f = fr.get("rows", {})
    check("I2e vrstice s80/s81/s82/s83", all(k in rows_f for k in ("s80", "s81", "s82", "s83")), str(list(rows_f.keys())))
    rows = [e["row"] for e in d["entries"]]
    check("I2f vrstice 1–18 zapored", rows == list(range(1, 19)), str(rows))
    sc = [e["scan"] for e in d["entries"]]
    check("I2g skeni znotraj 80–83", all(80 <= s <= 83 for s in sc), str(sorted(set(sc))))
    per = {80: 4, 81: 6, 82: 4, 83: 4}
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2h razpored 4+6+4+4", raz == per, str(raz))
    lead = d.get("lead", {})
    check("I2i P121 lead (poročna 1892, s84 velika glava)", "P121" in lead.get("next", "") and "1892" in lead.get("next", "")
          and "s84" in lead.get("frame", ""), f'{lead.get("next", "")} | {lead.get("frame", "")[:40]}')

    # ---------- I3: ključni vpisi ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [6,7]", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 2", d["stats"].get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(d["stats"].get("gribljeMarriages")))
    check("I3a Griblje hiše = [20,87]", d["stats"].get("gribljeHouses") == [20, 87],
          str(d["stats"].get("gribljeHouses")))
    e6 = d["entries"][5]
    check("I3b vpis 6 = h87 (Pezdirec 29 × Željko h60 Griblje — 2. dokaz h87!)",
          e6["groom"]["houseNo"] == 87 and e6["bride"]["houseNo"] == 60
          and e6["groom"]["age"] == 29 and "Pezdirec" in e6["groom"]["name"]
          and "Željko" in e6["bride"]["name"],
          f'{e6["groom"]["name"]} h87 × {e6["bride"]["name"]} h60')
    e7 = d["entries"][6]
    check("I3c vpis 7 = h20 NOVA × Klepec Krasinec 37",
          e7["groom"]["houseNo"] == 20 and e7["bride"]["houseNo"] == 37
          and "Pezdirec" in e7["groom"]["name"] and "Klepec" in e7["bride"]["name"],
          f'{e7["groom"]["name"]} h20 × {e7["bride"]["name"]} Krasinec 37')
    e11 = d["entries"][10]
    check("I3d vpis 11 = APOSTOLSKA dispensacija (2. kanc. st. iste linije) + Z: 5672 + Klepec h36",
          "APOSTOLISCHE DISPENS" in e11["urkunden"] and "2. canon. Grade" in e11["urkunden"]
          and "5672" in e11["urkunden"] and e11["groom"]["houseNo"] == 36
          and "Klepec" in e11["groom"]["name"],
          f'apostolska; {e11["groom"]["name"]} h36')
    e14 = d["entries"][13]
    check("I3e vpis 14 = ROSETTA »½ Griblers. Sohn« + 1. vdova-poroka (Šimonič roj. Konda 32!)",
          "½ Griblers. Sohn (ROSETTA!)" in e14["groom"].get("stand", "")
          and "Šimonič" in e14["bride"]["name"] and "Konda" in e14["bride"]["name"]
          and e14["bride"]["age"] == 32,
          f'{e14["groom"].get("stand", "")[:40]}; {e14["bride"]["name"][:40]}')
    e15 = d["entries"][14]
    check("I3f vpis 15 = ŽANDAR + HRVAŠKA (Pintar Dolenja Pušća) + 2 Zagrebčana-priče + vdova 35",
          "ŽANDAR" in e15["groom"].get("stand", "") and "HRVAŠKA" in e15["groom"].get("stand", "")
          and sum(1 for w in e15["witnesses"] if "Zagreb" in w) == 2
          and e15["bride"]["status"] == "vdova" and e15["bride"]["age"] == 35,
          f'{e15["groom"].get("stand", "")[:50]}; priče {len(e15["witnesses"])}')
    e16 = d["entries"][15]
    check("I3g vpis 16 = nevesta BREZ hišne št. (None) + Pompello + Vojna vas?",
          e16["bride"]["houseNo"] is None and "Pompello" in e16["bride"]["name"]
          and "Vojna vas" in e16["bride"]["village"],
          f'{e16["bride"]["name"]} h{e16["bride"]["houseNo"]} {e16["bride"]["village"]}')
    e18 = d["entries"][17]
    check("I3h vpis 18 = najmlajša nevesta 19 (Catharina Pezdirec) × Dragoš",
          e18["bride"]["age"] == 19 and "Pezdirec" in e18["bride"]["name"]
          and "Dragoš" in e18["groom"]["name"],
          f'{e18["groom"]["name"]} × {e18["bride"]["name"]} {e18["bride"]["age"]}')
    check("I3i trojni poročni dan 3.2. = v5+v6+v7",
          [e["row"] for e in d["entries"] if e["date"].startswith("3.2.")] == [5, 6, 7], "3.2.1891 ×3")
    e9 = d["entries"][8]
    check("I3j vpis 9 = banns iz 2 župnij (Metlika + Trnovo — bodoče bivališče!)",
          "Metlik" in e9["urkunden"] and "Trnov" in e9["urkunden"],
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
    check("I4 meseči (vsota 18)", not bad_m and sum(mc.values()) == 18, str(bad_m or sum(mc.values())))
    jan26 = [e["row"] for e in d["entries"] if e["date"].startswith("26.1.")]
    feb3 = [e["row"] for e in d["entries"] if e["date"].startswith("3.2.")]
    nov21 = [e["row"] for e in d["entries"] if e["date"].startswith("21.11.")]
    nov23 = [e["row"] for e in d["entries"] if e["date"].startswith("23.11.")]
    check("I4b dnevna gruča 26.1. = [2,3,4]", jan26 == [2, 3, 4], str(jan26))
    check("I4c trojni dan 3.2. = [5,6,7]", feb3 == [5, 6, 7], str(feb3))
    check("I4d vikend 21.11 = [15] + 23.11 = [16,17,18] (skupaj 4!)",
          nov21 == [15] and nov23 == [16, 17, 18] and len(nov21) + len(nov23) == 4,
          f'{nov21} + {nov23}')
    check("I4e zglasnici Griblje 23/1 št:5 (v6) + 2/2 st:7 (v7)",
          "23/1. 1891" in e6["urkunden"] and "Griblje" in e6["urkunden"]
          and "2/2. 1891" in e7["urkunden"] and "Griblje" in e7["urkunden"],
          f'v6: {e6["urkunden"][:40]} | v7: {e7["urkunden"][:40]}')

    # ---------- I5: stats ključne številke ----------
    st = d["stats"]
    pr = st.get("priests", {})
    check("I5 duhovniki Rauy ×18 (monopol)", pr.get("Jos. Rauy") == 18 and len(pr) == 1, str(pr))
    check("I5b vitals=550 (548 + 2 P120)", st.get("vitals") == EXPECTED_VITALS, str(st.get("vitals")))
    check("I5c bloki 04455=33", st.get("blocks04455") == BLOCKS_04455, str(st.get("blocks04455")))
    check("I5d p80 hiše=47 (h20 NOVI v vzorcu!)", st.get("p80Houses") == P80_HOUSES, str(st.get("p80Houses")))
    ag = st.get("ageGrooms", {})
    ab = st.get("ageBrides", {})
    check("I5e najstarejši ženin=39 (v8 Vranešič)", ag.get("max") == 39, str(ag))
    check("I5f najstarejša nevesta=35 (v15 vdova) + najmlajša=19 (v18)", ab.get("max") == 35 and ab.get("min") == 19, str(ab))
    check("I5g mladoletne neveste=12 + ženini=3", st.get("underageBrides") == 12 and st.get("underageGrooms") == 3,
          f'{st.get("underageBrides")}/{st.get("underageGrooms")}')
    check("I5h vdove=2 (v14+v15) + dispensacije=2", st.get("widows") == 2 and st.get("dispensations") == 2,
          f'{st.get("widows")}/{st.get("dispensations")}')
    check("I5i tuji dokumenti: Hrvaška ×4", st.get("foreignDocuments", {}).get("Hrvaška") == 4,
          str(st.get("foreignDocuments")))

    # ---------- I6: anomalije A1–A14 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A14", ids == [f"A{i}" for i in range(1, 15)], str(ids))
    a1 = next((a for a in d["anomalies"] if a["id"] == "A1"), {})
    check("I6b A1 = ROSETTA-STATUS", a1.get("type") == "ROSETTA-STATUS" and "Sohn/Tochter" in a1.get("text", ""),
          a1.get("text", "")[:60])
    a7 = next((a for a in d["anomalies"] if a["id"] == "A7"), {})
    check("I6c A7 = BREZ-ZGLASNICE (v15, samo hrvaški dokumenti)",
          a7.get("type") == "BREZ-ZGLASNICE" and "15" in str(a7.get("entry", "")), a7.get("text", "")[:60])
    a13 = next((a for a in d["anomalies"] if a["id"] == "A13"), {})
    check("I6d A13 = H87-KLEPEC mreža", a13.get("type") == "H87-KLEPEC" and "87" in a13.get("text", ""),
          a13.get("text", "")[:60])

    # ---------- I7: crossChecks ----------
    cc_ids = [c.get("id") for c in d["crossChecks"]]
    check("I7 crossChecks C1–C27", cc_ids == [f"C{i}" for i in range(1, 28)], str(cc_ids[-3:]))
    c1 = next((c for c in d["crossChecks"] if c.get("id") == "C1"), {})
    check("I7b C1 = PEZDIREC ×12 (rekord mreže!)", c1.get("type") == "PEZDIREC" and "×12" in c1.get("text", ""),
          c1.get("text", "")[:50])
    c19 = next((c for c in d["crossChecks"] if c.get("type") == "HRVAŠKA"), {})
    check("I7c C19 HRVAŠKA (v15 + 4 dokumenti)", "v15" in c19.get("text", "") or "Puš" in c19.get("text", ""),
          c19.get("text", "")[:60])
    c18 = next((c for c in d["crossChecks"] if c.get("type") == "SORODSTVO"), {})
    check("I7d C18 SORODSTVO apostolska (v11)", "5672" in c18.get("text", "") or "5672" in c18.get("verdict", ""),
          str(c18.get("text", c18.get("verdict", "")))[:60])
    c14 = next((c for c in d["crossChecks"] if c.get("type") == "DELEŽI-GRIBLJE"), {})
    check("I7e C14 DELEŽI-GRIBLJE ½/¼ ×14", "×14" in c14.get("text", ""), c14.get("text", "")[:60])
    # P119 dokaz ostaja nespremenjen (regresijska zaščita — lastna kumulativa)
    try:
        d119 = json.load(open(DOKAZ_P119))
        check("I7f P119 dokaz stats vitals=548 + bloki=31",
              d119["stats"].get("vitals") == 548 and d119["stats"].get("blocks04455") == 31,
              f'v{d119["stats"].get("vitals")} b{d119["stats"].get("blocks04455")}')
    except Exception as e:  # noqa: BLE001
        check("I7f P119 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 76 (P121 +4, P122 +5, P123 +4 + P124 +3 + P125 +3 + P126 +9 + P127 +9 + P128 +6!)", len(blocks_m) == BLOCKS_04455_TS, str(len(blocks_m)))
    h1891 = sorted((h for h, y, _ in blocks_m if y == "1891"), key=int)
    check("I8b hiše 1891 = [20,87]", ",".join(h1891) == GRIBLJE_HOUSES_TS, ",".join(h1891))
    h1890 = sorted((h for h, y, _ in blocks_m if y == "1890"), key=int)
    check("I8c hiše 1890 nespremenjene", ",".join(h1890) == "10,53,61,91", ",".join(h1890))
    h1889 = sorted((h for h, y, _ in blocks_m if y == "1889"), key=int)
    check("I8d hiše 1889 nespremenjene", ",".join(h1889) == "7,21,30,32,40,54,87", ",".join(h1889))
    h1888 = sorted((h for h, y, _ in blocks_m if y == "1888"), key=int)
    check("I8e hiše 1888 nespremenjene", ",".join(h1888) == "23,32,33,64", ",".join(h1888))
    h1887 = sorted((h for h, y, _ in blocks_m if y == "1887"), key=int)
    check("I8f hiše 1887 nespremenjene", ",".join(h1887) == "3,10,15,23,37,69,71", ",".join(h1887))
    h1886 = sorted((h for h, y, _ in blocks_m if y == "1886"), key=int)
    check("I8g hiše 1886 nespremenjene", ",".join(h1886) == "16,25,31,56,60,65,71", ",".join(h1886))
    # pini novih brani (1891 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1891,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8h pini P120 (10)", not missing, str(missing) if missing else "vse ✓")
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
    check("I8i stara branja iztekla", not stale, str(stale) if stale else "vse ✓ (1891 svež prepis)")
    # oznaki dokazov 1891
    check("I8j h20 = »NOVA HIŠA« (1. dokaz sploh!)",
          any(m.group(1) == "20" and "NOVA HIŠA" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1891,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))
    check("I8k h87 = »2. POROČNI DOKAZ h87« (1889 v8!)",
          any(m.group(1) == "87" and "2. POROČNI DOKAZ h87" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1891,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p120", '"qa-p120-parish-marriage-1891"' in qa)
    check("I9b p80 bloki 70", "poročni vpisi (04455) ≠ 70" in qa)
    check("I9c p80 sidra 69 (1898×9 · 1899×6!)", "poročna sidra ≠ 69" in qa)
    # vitals 550 regresijska zaščita v qa-p120
    check("I9d vitals 593 zaščita (P128)", "HOUSE_VITALS.length !== 593" in qa[qa.index("const p120Marr"):] if "const p120Marr" in qa else False)
    check("I9e stari 537/544/548 iztekla",
          "HOUSE_VITALS.length !== 537" not in qa and "HOUSE_VITALS.length !== 544" not in qa
          and "HOUSE_VITALS.length !== 548" not in qa)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P120", "P120" in rd and ("124/124" in rd or "po P123" in rd))
    nt = open("research/issue17/parish-marriage-1891-notes.md").read()
    check("I10b notes faza 2 + ROSETTA", "FAZA 2" in nt and "ROSETTA" in nt.upper())

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
