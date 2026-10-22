#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P123 — župnija Podzemelj: poročna knjiga 04455, polno leto 1894 (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P122 = 1893): okvir POTRJEN —
skeni 91–93 == Pag. 90–92 (Pag. == sken − 1, 9. potrditev; velja v 61–93);
**15 vpisov** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18 →
1892:15 → 1893:20 → 1894:15; razpored 6+5+4); **VELIKA GLAVA »Traunungs=Buch«
+ rokopisno »1894« POTRJENA na s91** (P123 lead!; cikel velike glave: 1887 s66
+ 1890 s77 + 1892 s84 + 1893 s87 + 1894 s91; 1891 = izjema). LANDSCAPE
geometrija (2524/2517/2509×1800; s94 = Pag. 93 = glava 1895 = P124 lead).
Ob robu s92: tiskar »Laibach. Druck u. Verlag v. Möttling.«!

FAZA 2: **15/15 vpisov transkribiranih OBOJESTRANSKO** + 30 row-crops ×2
LANCZOS + 38 zoomov z123_* + 15 mikro-zoomov zz_* ×3–8 + 5 primerjalnih
(obrezki za »Prilozje«, »Ans.«, prvočrko G/D, Orašče, Lipmitk).

NOVELE: **★ REKORD-PAR VSEH ČASOV v5** (ženin 64 + nevesta 48 = 112 let
skupaj!) + **REKORD nevesta 56** (v1 Tasič — prej 45 P119!) + **★ 1. PREČRTANI
PRIČA linije** (v12 Đur. Andreas Vojka → Franc Justin zasebnik junior!) +
**★ PFARRAMT IDRIA** (v12 = najdaljši župnijski lok ~110 km!) + **★ VOJSKA**
(v9 k.k. Infanterie-Regiments-Colonel 15/5.94 №267 — ženin aktivni vojak!) +
**★ DISPENS 3. stopnje №2680** (v14 Ordinariat Laibach 25/9. — ZUGELJ × TOME)
+ **★ LANDSREGIERUNG Laibach Ž8667** (v11 — 1. v poročni liniji; datirana
9/9. = 3 TEDNE PO poroki [~]!) + **ENAČNOPRIIMEŠKI poroki ×2** (v3 Perdinec ×
Perdinec h27×h42 + v6 Tome × Tome) + **ZURAJOVIČ očetovski cross-link**
(v2 ženin = sin P122 v6 ženina — Zemelj 18!) + **»1« namesto ulomka** (v12 —
2. primer po P122 v5!) + **občina Orašče [~]** (v15 = 1. neznanka-občina) +
**Laipšl-mreža 4. leto** ×5 + PEZDIREC-cluster ×10 (3 pisave) + Rauy-monopol
nazaj ×15/15 (podpis »M.!« [~] ×13 + »Pf.!« [~] ×2) + tiskar Möttling.

Skripta scripts/p123_parish_marriage_1894.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p123_parish_marriage_1894.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES = 192
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1894.json"
DOKAZ_P122 = "research/issue17/parish-marriage-1893.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
FRAME_SCANS = (91, 92, 93)  # 91 = Pag. 90 (velika glava 1894 + v1–6) · 92 = Pag. 91 (v7–11) · 93 = Pag. 92 (v12–15)
FRAME_PAGES = (90, 91, 92)
EXPECTED_ENTRIES = 15
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 8
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [3, 11]
GRIBLJE_MARRIAGES = 2
GRIBLJE_HOUSES = [9, 11, 27, 42]
GRIBLJE_HOUSES_TS = "11,27,42,9"  # vrstni-red po scan/page (h27+42 s91, h9+11 s92)
EXPECTED_VITALS = 563                 # P123 dokaz lastna kumulativa (559 + 4 blokov)
BLOCKS_04455 = 46                     # P123 dokaz LASTNA kumulativa (42 + 4 — dokaz se ne spreminja!)
BLOCKS_04455_TS = 78              # P126: + 9 blokov 1897 (61) + P127: + 9 blokov 1898 (70)
P80_HOUSES = 47                       # POPRAVEK: 41 → 47 (+h9/h27/h42 NOVE v vzorcu; h11 že prek krstne; P122 pred tem +h26/h58/h62)
DATE_COUNTS = {"januar": 2, "februar": 1, "marec": 0, "april": 1, "maj": 2,
               "junij": 3, "julij": 1, "avgust": 1, "september": 1,
               "oktober": 3, "november": 0, "december": 0}
# P123 pini (blok-houseNo → obvezen fragment v whatSi; cf. qa-p123)
BLOCK_PINS = [
    ("27", "ENAČNOPRIIMEŠKA POROKA Perdinec"),
    ("42", "CERNIČ-hiša"),
    ("9", "LANDSREGIERUNG-dokument poročne linije"),
    ("11", "2. GRIBLJE poroka 1894"),
]


def http_get(url, headers=None, tries=3):
    req = urllib.request.Request(url, headers=headers or UA)
    last = None
    for _ in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read()
        except Exception as e:  # noqa: BLE001
            last = e
    return 0, str(last).encode()


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
    check("I2 skeni 91–93", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2b strani 90–92", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))
    check("I2c Pag. == sken − 1 (9. potrditev)", "sken − 1" in fr.get("pagRule", ""), fr.get("pagRule", "")[:60])
    check("I2d velika glava 1894 na s91 (P123 lead POTRJEN)",
          "s91" in fr.get("bigHeader", "") and "1894" in fr.get("bigHeader", ""),
          fr.get("bigHeader", "")[:70])
    rows_f = fr.get("rows", {})
    check("I2e vrstice s91/s92/s93", all(k in rows_f for k in ("s91", "s92", "s93")), str(list(rows_f.keys())))
    rows = [e["row"] for e in d["entries"]]
    check("I2f vrstice 1–15 zapored", rows == list(range(1, 16)), str(rows))
    sc = [e["scan"] for e in d["entries"]]
    check("I2g skeni znotraj 91–93", all(91 <= s <= 93 for s in sc), str(sorted(set(sc))))
    per = {91: 6, 92: 5, 93: 4}
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2h razpored 6+5+4", raz == per, str(raz))
    lead = d.get("lead", {})
    check("I2i P124 lead (poročna 1895, s94)", "P124" in lead.get("next", "") and "1895" in lead.get("next", "")
          and "s94" in lead.get("frame", ""), f'{lead.get("next", "")} | {lead.get("frame", "")[:40]}')

    # ---------- I3: ključni vpisi ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [3,11]", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 2 (4 bloki!)", d["stats"].get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(d["stats"].get("gribljeMarriages")))
    check("I3a Griblje hiše = [9,11,27,42]", d["stats"].get("gribljeHouses") == GRIBLJE_HOUSES,
          str(d["stats"].get("gribljeHouses")))
    e1 = d["entries"][0]
    e5 = d["entries"][4]
    check("I3b REKORD-PAR v5 (64+48=112!) + REKORD nevesta 56 (v1)",
          e5["groom"]["age"] == 64 and e5["bride"]["age"] == 48
          and e1["bride"]["age"] == 56 and e1["groom"]["age"] == 53,
          f'v5 {e5["groom"]["age"]}+{e5["bride"]["age"]}; v1 {e1["groom"]["age"]}+{e1["bride"]["age"]}')
    check("I3c v1 Tasič + Nemanič Laipfler (P122-lead popravek!) + Prilozje 35 + Boginja vas 13",
          "Tasič" in e1["bride"]["name"] and "Nemanič" in e1["groom"]["name"]
          and e1["groom"]["village"].startswith("Prilozje") and e1["bride"]["village"].startswith("Boginja vas"),
          f'{e1["groom"]["name"]} × {e1["bride"]["name"]}')
    e3 = d["entries"][2]
    check("I3d v3 ENAČNOPRIIMEŠKA Perdinec × Perdinec (h27 × h42 — CERNIČ-hiša!)",
          "Perdinec" in e3["groom"]["name"] and "Perdinec" in e3["bride"]["name"]
          and e3["groom"]["houseNo"] == 27 and e3["bride"]["houseNo"] == 42
          and "Marcus Perdinec" in e3["parentsGroom"] and "Georg Perdinec" in e3["parentsBride"],
          f'{e3["groom"]["name"]} h27 × {e3["bride"]["name"]} h42')
    e4 = d["entries"][3]
    check("I3e v4 Großjährigkeit 30/11.92 (nenavadno zgodaj — A8)",
          "30/11. 92" in e4["urkunden"], e4["urkunden"][-80:])
    e6 = d["entries"][5]
    check("I3f v6 ENAČNOPRIIMEŠKA Tome × Tome + mamina ustna privolitev",
          "Tome" in e6["groom"]["name"] and "Tome" in e6["bride"]["name"]
          and "Mütterlichkeit" in e6["urkunden"],
          f'{e6["groom"]["name"]} × {e6["bride"]["name"]}')
    e9 = d["entries"][8]
    check("I3g v9 VOJSKA: Infanterie-Regiments-Colonel №267 (aktivni vojak!)",
          "Infanterie-Regiments-Colonel" in e9["urkunden"] and "267" in e9["urkunden"],
          e9["urkunden"][40:110])
    e11 = d["entries"][10]
    check("I3h v11 h9 × h11 + LANDSREGIERUNG Laibach Ž8667 (datum po poroki! [~]) + gj. №5642",
          e11["groom"]["houseNo"] == 9 and e11["bride"]["houseNo"] == 11
          and "Landesregierung in Laibach" in e11["urkunden"] and "8667" in e11["urkunden"]
          and "5642" in e11["urkunden"],
          e11["urkunden"][:90])
    e12 = d["entries"][11]
    check("I3i v12 PREČRTANI PRIČA (Vojka→Justin) + IDRIA + »1« ulomek + hf.",
          "PREČRTAN" in json.dumps(e12, ensure_ascii=False) and "Idria" in e12["urkunden"]
          and "1 Griblers" in e12["bride"]["stand"],
          f'{e12["groom"]["name"]}; priče {len(e12.get("witnesses", []))}')
    e13 = d["entries"][12]
    check("I3j v13 razlika 16 let (28 × 44) + Pf. Črnomelj + Kirnšina [~]",
          e13["groom"]["age"] == 28 and e13["bride"]["age"] == 44
          and "Črnomelj" in e13["urkunden"] and "Kirnšina" in json.dumps(e13, ensure_ascii=False),
          f'{e13["groom"]["age"]} × {e13["bride"]["age"]}')
    e14 = d["entries"][13]
    check("I3k v14 DISPENS 3. st. №2680 (ZUGELJ × TOME) + gj. 28.2.94",
          e14["groom"]["houseNo"] == 18 and "Zugelj" in e14["groom"]["name"]
          and "2680" in e14["urkunden"] and "3ten Grade" in e14["urkunden"],
          f'{e14["groom"]["name"]} × {e14["bride"]["name"]}')
    e15 = d["entries"][14]
    check("I3l v15 občina Orašče [~] + Ankündschein Metlika (isti dan!) + Vidošiče",
          "Orašče" in e15["urkunden"] and "Ankündschein" in e15["urkunden"]
          and "Vidoši" in e15["groom"]["village"],
          e15["urkunden"][:70])
    e2 = d["entries"][1]
    check("I3m v2 ZURAJOVIČ cross-link (sin P122 v6 ženina — Zemelj 18!)",
          "Zurajeovič" in e2["groom"]["name"] and e2["groom"]["houseNo"] == 18
          and "Nicolaus" in e2["parentsGroom"],
          f'{e2["groom"]["name"]} Zemelj 18')
    e10 = d["entries"][9]
    check("I3n v10 Hofmann-nov status + obsvormundska Einwilligung 8/7. (isti dan kot zglašnica)",
          "Hofmann" in e10["groom"]["stand"] and "obsvorm" in e10["urkunden"]
          and "8/7. 1894" in e10["urkunden"],
          f'{e10["groom"]["name"]}; {e10["urkunden"][:50]}')
    jun10 = [e["row"] for e in d["entries"] if e["date"].startswith("10.6.")]
    okt28 = [e["row"] for e in d["entries"] if e["date"].startswith("28.10.")]
    maj = [e["row"] for e in d["entries"] if e["date"].endswith(".5.1894")]
    check("I3o dvojna dneva 10.6. = [8,9] + 28.10. = [14,15] + maj 27.+28. = [5,6]",
          jun10 == [8, 9] and okt28 == [14, 15] and maj == [5, 6], f'{jun10} + {okt28} + {maj}')
    laipsl_rows = [e["row"] for e in d["entries"] if "aipfler" in json.dumps(e, ensure_ascii=False)]  # "aipfler" pokrije obe pisavi: Laipfler (v1/v2) + Zaipfler (v5/v8/v10)
    check("I3p Laipšl-mreža 4. leto (Laipfler+Zaipfler ×5 oseb: v1/v2/v5/v8/v10)",
          sorted(set(laipsl_rows)) == [1, 2, 5, 8, 10], f'vrstice {sorted(set(laipsl_rows))}')

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
    check("I4 meseči (vsota 15; oktober 3 = jesenska koncentracija!)",
          not bad_m and sum(mc.values()) == 15, str(bad_m or sum(mc.values())))
    check("I4b v12 zglašnica mestne občine Metlika št: 142 (najvišja št. linije!)",
          "142" in e12["urkunden"] and "mestne občine Metlika" in e12["urkunden"],
          e12["urkunden"][:60])
    check("I4c v14 dispens 25/9.1894 №2680 (mesec dni pred poroko!)",
          "25/9. 1894" in e14["urkunden"] and "2680" in e14["urkunden"], "v14 urkunden")

    # ---------- I5: stats ključne številke ----------
    st = d["stats"]
    pr = st.get("priests", {})
    check("I5 duhovniki: Rauy ×15/15 (monopol Nazaj po P122 Klemenčič!)",
          pr.get("Jos. Rauy") == 15 and len(pr) == 1, str(pr))
    check("I5b vitals=563 (559 + 4 P123)", st.get("vitals") == EXPECTED_VITALS, str(st.get("vitals")))
    check("I5c bloki 04455=46", st.get("blocks04455") == BLOCKS_04455, str(st.get("blocks04455")))
    check("I5d p80 hiše=47 (POPRAVEK: +h9/h27/h42 NOVE — h11 že!)", st.get("p80Houses") == P80_HOUSES,
          str(st.get("p80Houses")))
    ag = st.get("ageGrooms", {})
    ab = st.get("ageBrides", {})
    check("I5e ženin max=64 (v5!) + min=22", ag.get("max") == 64 and ag.get("min") == 22, str(ag))
    check("I5f nevesta max=56 (v1 REKORD!) + min=20", ab.get("max") == 56 and ab.get("min") == 20, str(ab))
    check("I5g mladoletne neveste=7 + ženini=2 (9/30, ABGB-24 8. leto!)",
          st.get("underageBrides") == 7 and st.get("underageGrooms") == 2,
          f'{st.get("underageBrides")}/{st.get("underageGrooms")}')
    check("I5h dispensacije=1 (v14 №2680)", st.get("dispensations") == 1, str(st.get("dispensations")))
    fd = st.get("foreignDocuments", {})
    check("I5i tuji dokumenti: Möttling ×4 + pf-Metlika ×2 + Ordinariat + Landesreg. + Črnomelj + Inf.-Reg. + Idria + pf-Črnomelj",
          fd.get("BezGer-Möttling") == 4 and fd.get("pf-Metlika") == 2
          and fd.get("Ordinariat-Laibach") == 1 and fd.get("Landesregierung-Laibach") == 1
          and fd.get("BezGer-Črnomelj") == 1 and fd.get("Infanterie-Regiment") == 1
          and fd.get("pf-Idria") == 1 and fd.get("pf-Črnomelj") == 1,
          str(fd))

    # ---------- I6: anomalije A1–A8 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A8", ids == [f"A{i}" for i in range(1, 9)], str(ids))
    a1 = next((a for a in d["anomalies"] if a["id"] == "A1"), {})
    check("I6b A1 = REKORD-PAR (v5 112 skupaj + v1 56)", a1.get("type") == "REKORD-PAR" and "112" in a1.get("text", ""),
          a1.get("text", "")[:60])
    a2 = next((a for a in d["anomalies"] if a["id"] == "A2"), {})
    check("I6c A2 = PREČRTANI-PRIČA (v12 Vojka→Justin)", a2.get("type") == "PREČRTANI-PRIČA" and "Justin" in a2.get("text", ""),
          a2.get("text", "")[:60])
    a6 = next((a for a in d["anomalies"] if a["id"] == "A6"), {})
    check("I6d A6 = PFARRAMT-IDRIA (najdaljši lok ~110 km)", a6.get("type") == "PFARRAMT-IDRIA" and "idria" in a6.get("text", "").lower(),
          a6.get("text", "")[:60])
    a7 = next((a for a in d["anomalies"] if a["id"] == "A7"), {})
    check("I6e A7 = LANDSREGIERUNG-Ž8667 (datum po poroki!)", a7.get("type") == "LANDSREGIERUNG-Ž8667" and "8667" in a7.get("text", ""),
          a7.get("text", "")[:60])

    # ---------- I7: crossChecks ----------
    cc_ids = [c.get("id") for c in d["crossChecks"]]
    check("I7 crossChecks C1–C20", cc_ids == [f"C{i}" for i in range(1, 21)], str(cc_ids[-3:]))
    c1 = next((c for c in d["crossChecks"] if c.get("id") == "C1"), {})
    check("I7b C1 = GRIBLJE-POROKE ×2 (4 bloki)", c1.get("type") == "GRIBLJE-POROKE" and "h27" in c1.get("text", ""),
          c1.get("text", "")[:60])
    c3 = next((c for c in d["crossChecks"] if c.get("id") == "C3"), {})
    check("I7c C3 ZURAJOVIČ cross-link 1893→1894", "ZURAJOVIČ" in c3.get("type", "") and "Zemelj 18" in c3.get("text", ""),
          c3.get("text", "")[:60])
    c5 = next((c for c in d["crossChecks"] if c.get("id") == "C5"), {})
    check("I7d C5 LAIPŠL 4. leto (×5 oseb)", "4. LETO" in c5.get("text", ""), c5.get("text", "")[:60])
    c14 = next((c for c in d["crossChecks"] if c.get("id") == "C14"), {})
    check("I7e C14 IDRIA najdaljši lok (~110 km)", "110 km" in c14.get("text", ""), c14.get("text", "")[:60])
    c18 = next((c for c in d["crossChecks"] if c.get("id") == "C18"), {})
    check("I7f C18 status-neznanki ×14", "×14" in c18.get("text", ""), c18.get("text", "")[:60])
    # P122 dokaz ostaja nespremenjen (regresijska zaščita — lastna kumulativa)
    try:
        d122 = json.load(open(DOKAZ_P122))
        check("I7g P122 dokaz stats vitals=559 + bloki=42",
              d122["stats"].get("vitals") == 559 and d122["stats"].get("blocks04455") == 42,
              f'v{d122["stats"].get("vitals")} b{d122["stats"].get("blocks04455")}')
    except Exception as e:  # noqa: BLE001
        check("I7g P122 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 78 (P122 42 + P123 4 + P124 +3 + P125 +3 + P126 +9 + P127 +9 + P128 +6!)", len(blocks_m) == BLOCKS_04455_TS, str(len(blocks_m)))
    h1894 = sorted((h for h, y, _ in blocks_m if y == "1894"), key=int)
    check("I8b hiše 1894 = [9,11,27,42]", ",".join(h1894) == "9,11,27,42", ",".join(h1894))
    h1893 = sorted((h for h, y, _ in blocks_m if y == "1893"), key=int)
    check("I8c hiše 1893 nespremenjene", ",".join(h1893) == "26,58,62,69,74", ",".join(h1893))
    h1892 = sorted((h for h, y, _ in blocks_m if y == "1892"), key=int)
    check("I8d hiše 1892 nespremenjene", ",".join(h1892) == "17,30,36,60", ",".join(h1892))
    h1891 = sorted((h for h, y, _ in blocks_m if y == "1891"), key=int)
    check("I8e hiše 1891 nespremenjene", ",".join(h1891) == "20,87", ",".join(h1891))
    h1890 = sorted((h for h, y, _ in blocks_m if y == "1890"), key=int)
    check("I8f hiše 1890 nespremenjene", ",".join(h1890) == "10,53,61,91", ",".join(h1890))
    h1889 = sorted((h for h, y, _ in blocks_m if y == "1889"), key=int)
    check("I8g hiše 1889 nespremenjene", ",".join(h1889) == "7,21,30,32,40,54,87", ",".join(h1889))
    h1888 = sorted((h for h, y, _ in blocks_m if y == "1888"), key=int)
    check("I8h hiše 1888 nespremenjene", ",".join(h1888) == "23,32,33,64", ",".join(h1888))
    h1887 = sorted((h for h, y, _ in blocks_m if y == "1887"), key=int)
    check("I8i hiše 1887 nespremenjene", ",".join(h1887) == "3,10,15,23,37,69,71", ",".join(h1887))
    h1886 = sorted((h for h, y, _ in blocks_m if y == "1886"), key=int)
    check("I8j hiše 1886 nespremenjene", ",".join(h1886) == "16,25,31,56,60,65,71", ",".join(h1886))
    # pini novih brani (1894 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1894,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8k pini P123 (4)", not missing, str(missing) if missing else "vse ✓")
    # oznake dokazov 1894
    check("I8l h42 = CERNIČ-hiša (3. dokaz, 1. poročni!)",
          any(m.group(1) == "42" and "CERNIČ-hiša" in m.group(2) and "1. POROČNI" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1894,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))
    check("I8m h9/h11 = 2. poročna dokaza + LANDSREGIERING Ž8667",
          any(m.group(1) == "9" and "2. poročni dokaz h9" in m.group(2) and "8667" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1894,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)),
          "h9 pin")
    check("I8n h27 = 2. poročni dokaz + ENAČNOPRIIMEŠKA",
          any(m.group(1) == "27" and "2. poročni dokaz h27" in m.group(2) and "ENAČNOPRIIMEŠKA" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1894,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)),
          "h27 pin")

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p123", '"qa-p123-parish-marriage-1894"' in qa)
    check("I9b p80 bloki 78", "poročni vpisi (04455) ≠ 78" in qa)
    check("I9c p80 sidra 71 (1898×9 · 1899×6 · 1900×2!)", "poročna sidra ≠ 71" in qa)
    check("I9d p80 hiše 58 (qa kumulativa — …; P127: +6 NOVIH!)", "različnih hiš (vse tri knjige) ≠ 59" in qa)
    # vitals 563 regresijska zaščita v qa-p123
    check("I9e vitals 595 zaščita (P128)", "HOUSE_VITALS.length !== 595" in qa[qa.index("const p123Marr"):] if "const p123Marr" in qa else False)
    check("I9f stari 537/544/548/550/554/559 iztekla",
          "HOUSE_VITALS.length !== 537" not in qa and "HOUSE_VITALS.length !== 544" not in qa
          and "HOUSE_VITALS.length !== 548" not in qa and "HOUSE_VITALS.length !== 550" not in qa
          and "HOUSE_VITALS.length !== 554" not in qa and "HOUSE_VITALS.length !== 559" not in qa)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P123", "P123" in rd and ("124/124" in rd or "po P123" in rd))
    nt = open("research/issue17/parish-marriage-1894-notes.md").read()
    check("I10b notes faza 2 + REKORD", "FAZA 2" in nt and "REKORD-PAR" in nt)

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
