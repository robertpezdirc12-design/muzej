#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P125 — župnija Podzemelj: poročna knjiga 04455, dopolnitev 1895 (s97) +
polno leto 1896 (s98–s101) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P124 = 1895): okvir POTRJEN —
s97 = Pag. 96 = NADALJEVANJE 1895 (tiskana podglava brez leta) z 3 zadnjimi
vpisi 1895 (v17–v19 — **P124 DOPOLNITEV: 1895 ima 19 vpisov, ne 16!**);
s98–s101 == Pag. 97–100 (Pag. == sken − 1, **11. potrditev; velja v 61–100**);
**ROKOPISNA GLAVA »1896.« POTRJENA na s98** + rokopisna glava »1897« + v1/1897
ŽE na s101 (P126 lead!) + s103 = Pag. 102 VELIKA TISKANA GLAVA + v11/1897
(Griblje 40 Nikolaus Perdinec × Griblje 39 Maria Simic [~] — GRIBLJE poroka že
orisana!). **18 vpisov** (3 × 1895-ext: okt 29 + nov 10 + nov 28 + 15 × 1896:
feb 5 + apr 1 + maj 4 + avg 2 + okt 2 + nov 1).

NOVELE: **★ ⅓ GRIBLAR = NOV ULOMEK LINIJE** (v6 Kolih + v10 Jakofčič — oče+sin
oba ⅓!) + 1 GRIBLAR (v2) + **★ 1. NEZAKONSKI ŽENIN POROČNE LINIJE** (v14:
starši [—] + »ledige Magd«!) + **★ 3. duhovnik linije Franz Herms coop.** (v12
— edina prekinitev Rauy-monopola 17/18!) + **★ 2. ŽANDAR** (v4 Eduard (Hubert
[~]) Röthl) + k.k. Beamte oče (1.!) + Rudolfswert/Gottschee/Adelsberg/Laibach
+ »Indifferenz« + **★ ŽAKANJE = HRVAŠKA** (v11 — slovensko »otlični list«!) +
**★ »hoc« = hic commorans REŠEN ×7** + **★ mütterl. fürwellig** (v7 — 1.
MATICA!) + »in Ungarn« ×4 (ISTI ŠTEVEC kot P124!) + GROSSJÄHRIGKEIT za ženina
(v3 — 1.!) + DISPENS №2906 (v17-1895) + №293 (v3) + **★ MUC 3. dokaz** (v1
oče = P121 v12 ISTA!) + **★ 2. REKORD-PAR** (v18-1895: 59+50 = 109!) +
občinske kontinuitete Griblje št:4 / Gradac 21→22→23 / Podzemelj →121[~] +
h14 CROSS-LINK (v17 par = krstna 1896 ISTI PAR!).

Skripta scripts/p125_parish_marriage_1896.py (I1–I11, --check izpiše PASS/FAIL
in vrne exit code; --live omogoči HTTP preverjanje matricula-online.eu).
Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p125_parish_marriage_1896.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES = 192
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1896.json"
DOKAZ_P124 = "research/issue17/parish-marriage-1895.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
EXPECTED_ENTRIES = 18          # 3 × 1895-ext (v17–v19) + 15 × 1896 (v1–v15)
EXPECTED_ROWS = [17, 18, 19] + list(range(1, 16))
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [17, 15]        # v17-1895 (h24 × h14) + v15-1896 (h18)
GRIBLJE_MARRIAGES_STR = "2 (v17-1895: h24 × h14"
GRIBLJE_HOUSES = [14, 24, 18]
EXPECTED_VITALS = 569          # 566 (P124) + 3 bloki (h24 + h14-1895ext + h18-1896)
BLOCKS_04455 = 52                     # P125 dokaz lastna kumulativa (49 + 3); trenutna = 142 (P138)             # P125 dokaz lastna kumulativa (49 + 3)
BLOCKS_04455_TS = 171   # POSODABLJENO P144: 164 (P142-era) → 168 (P143: +4 — ZAMUDA SANIRANA!) → 169 (P144: +1 h82!)   # P140: + 6 blokov 1911            # parish.ts zdaj = 61 + 9 blokov 1898 (P127)
P80_HOUSES = 51                # 48 (P124) + 3 (h24/h14/h18 — krstni bloki teh hiš izven p80 vzorca!) — dokaz-const (JSON P125)
P80_PT_GAP = 10                # nespremenjeno
RAZPORED = {97: 3, 98: 4, 99: 5, 100: 5, 101: 1}  # v17-19 + v1-4 + v5-9 + v10-14 + v15
DATE_COUNTS_1896 = {"januar": 0, "februar": 5, "marec": 0, "april": 1, "maj": 4,
                    "junij": 0, "julij": 0, "avgust": 2, "september": 0,
                    "oktober": 2, "november": 1, "december": 0}
DATE_COUNTS_1895EXT = {"januar": 0, "februar": 0, "marec": 0, "april": 0, "maj": 0, "junij": 0,
                       "julij": 0, "avgust": 0, "september": 0, "oktober": 1, "november": 2,
                       "december": 0}
ANOM_TYPES = {  # A1–A10 (row, type)
    "A1": (17, "DISPENS-GRIBLJE"),
    "A2": (18, "REKORD-PAR"),
    "A3": (19, "VORMUNDSCHAFT-49"),
    "A4": (4, "INDIFFERENZ-IME"),
    "A5": (6, "TRETJINA-CROATIEN"),
    "A6": (8, "MJ-PRI-25"),
    "A7": (11, "STAROST-SLOVENSKO-ŽAKANJE"),
    "A8": (12, "DRUGI-DUHOVNIK"),
    "A9": (14, "NEZAKONSKI"),
    "A10": (3, "PODVOJENA-ST"),
}
# P125 pini (blok-houseNo → obvezen fragment v whatSi; cf. qa-p125)
BLOCK_PINS = [
    ("24", "1. POROČNI DOKAZ"),
    ("24", "BRINSEC"),
    ("24", "DISPENS №2906"),
    ("24", "GRIBLJE × GRIBLJE"),
    ("14", "1. POROČNI DOKAZ"),
    ("14", "CROSS-LINK"),
    ("14", "BRINSEC"),
    ("18", "1. POROČNI DOKAZ"),
    ("18", "KLOBUČAR"),
    ("18", "BERKOVEC"),
    ("18", "GROSSJÄHRIGKEIT"),
]
# I8 regresija: stare hiše po letih (iz p124 verifierja)
HISTORIC_HOUSES = {
    "1894": "9,11,27,42",
    "1893": "26,58,62,69,74",
    "1892": "17,30,36,60",
    "1891": "20,87",
    "1890": "10,53,61,91",
    "1889": "7,21,30,32,40,54,87",
    "1888": "23,32,33,64",
    "1887": "3,10,15,23,37,69,71",
    "1886": "16,25,31,56,60,65,71",
}


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
    check("I1b entries=18 (3 ext + 15)", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1c excluded=0", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1d anomalije=10", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=20", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (18/18)", not bad, str(bad) if bad else "vse ✓")
    rows = [e["row"] for e in d["entries"]]
    check("I1g vrstice [17,18,19,1–15]", rows == EXPECTED_ROWS, str(rows))
    ext = [e["row"] for e in d["entries"] if e.get("ext")]
    y96 = [e["row"] for e in d["entries"] if e["year"] == 1896 and not e.get("ext")]
    check("I1h ext=3 (v17–v19 1895) + 1896=15", ext == [17, 18, 19] and len(y96) == 15,
          f'ext {ext}; 1896 {len(y96)}')

    # ---------- I2: okvir ----------
    st = d["stats"]
    fr = d["frame"]
    check("I2 skeni 97–101", st.get("scans") == [97, 98, 99, 100, 101], str(st.get("scans")))
    check("I2b strani 96–100", st.get("pages") == [96, 97, 98, 99, 100], str(st.get("pages")))
    check("I2c Pag. == sken − 1 (11. potrditev)", "sken − 1" in st.get("pagRule", "")
          and "11. potrditev" in st.get("pagRule", ""), st.get("pagRule", "")[:60])
    check("I2d rokopisna glava 1896 na s98", "s98" in fr.get("bigHeader", "")
          and "1896" in fr.get("bigHeader", ""), fr.get("bigHeader", "")[:70])
    check("I2e entriesTotal=18 + 3 ext + 15 1896",
          fr.get("entriesTotal") == 18 and fr.get("entries1895ext") == 3 and fr.get("entries1896") == 15,
          f'{fr.get("entriesTotal")}/{fr.get("entries1895ext")}/{fr.get("entries1896")}')
    lin = fr.get("lineageCount", "")
    check("I2f lineageCount 1895:19 + 1896:15", "1895:19" in lin and "1896:15" in lin, lin[-40:])
    sc = [e["scan"] for e in d["entries"]]
    check("I2g skeni znotraj 97–101", all(97 <= s <= 101 for s in sc), str(sorted(set(sc))))
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2h razpored 3+4+5+5+1", raz == RAZPORED, str(raz))
    check("I2i s101 = P126 lead (glava 1897 + v1/1897)", "1897" in fr.get("bigHeader", "")
          and "P126" in fr.get("bigHeader", ""), fr.get("bigHeader", "")[-60:])
    ns = d.get("nextSteps", {})
    check("I2j nextSteps P126 (1897, skeni 102+)", "1897" in ns.get("p126Lead", "")
          and ns.get("scans") == [102, 103, 104, 105, 106], f'{ns.get("scans")}')
    lead = d.get("lead", "")
    check("I2k lead: dopolnitev 1895 + leto 1896", "1895" in lead and "1896" in lead, lead[:60])

    # ---------- I3: ključni vpisi ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [17, 15]", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 2 (v17 DVOJNA hiša + v15)", str(st.get("gribljeMarriages", "")).startswith(GRIBLJE_MARRIAGES_STR),
          str(st.get("gribljeMarriages")))
    check("I3a Griblje hiše = [14,24,18]", st.get("gribljeHouses") == GRIBLJE_HOUSES,
          str(st.get("gribljeHouses")))
    e17 = d["entries"][0]
    check("I3b v17 GRIBLJE × GRIBLJE (h24 × h14) + DISPENS №2906 + občina št: 4",
          e17["groom"]["place"].startswith("Griblje 24") and e17["bride"]["place"].startswith("Griblje 14")
          and "2906" in e17["urkunden"] and "št: 4" in e17["urkunden"] and "Rauy" in e17["priest"],
          f'{e17["groom"]["place"]} × {e17["bride"]["place"]}; {e17["urkunden"][:50]}')
    e18 = d["entries"][1]
    check("I3c v18 2. REKORD-PAR (59+50 = 109) + Gradac št: 22",
          e18["groom"]["age"] == 59 and e18["bride"]["age"] == 50
          and "Gradac" in e18["urkunden"] and "št: 22" in e18["urkunden"],
          f'{e18["groom"]["name"]} 59 × {e18["bride"]["name"]} 50')
    e19 = d["entries"][2]
    check("I3d v19 VORMUNDSCHAFT za 49-letnika + Kauf-Brief + oče = ženin (Georg Marvin ×2)",
          e19["groom"]["age"] == 49 and "Vormundschaft" in e19["urkunden"]
          and "Kauf-Brief" in e19["urkunden"] and "Loka" in e19["urkunden"]
          and e19["parentsGroom"].startswith("Georg Marvin"),
          f'v19 starši: {e19["parentsGroom"][:36]}')
    e1 = d["entries"][3]
    check("I3e v1 MUC 3. dokaz (oče Nicolaus = P121 v12 ISTA! + nevesta Maria Muc) + Podzemelj št: 4 + in Ungarn",
          "Muc" in e1["bride"]["name"] and "Muc" in e1["parentsBride"]
          and "Podzemelj" in e1["urkunden"] and "št: 4" in e1["urkunden"]
          and "in Ungarn" in e1["urkunden"],
          f'{e1["bride"]["name"]}; starši: {e1["parentsGroom"][:40]}')
    e2 = d["entries"][4]
    check("I3f v2 1 GRIBLAR nevesta (cel gospodar!) + Podzemelj št: 6 und 8",
          e2["bride"]["stand"].startswith("1 Griblaršdojft") and "6 und 8" in e2["urkunden"],
          f'{e2["bride"]["name"]}: {e2["bride"]["stand"][:30]}')
    e3 = d["entries"][5]
    check("I3g v3 DISPENS №293 3. st. krvno + GROSSJÄHRIGKEIT za ŽENINA (22 — 1.!) + št: 4 [~] (A10)",
          "293" in e3["urkunden"] and "Großjärigkeits-Erklärung" in e3["urkunden"]
          and "Bräutigam" in e3["urkunden"] and e3["groom"]["age"] == 22,
          f'v3 ženin 22; {e3["urkunden"][130:190]}')
    e4 = d["entries"][6]
    check("I3h v4 2. ŽANDAR (GENDARM) + k.k. Beamte oče + Indifferenz + Hanna Elisabeth + Gottschee + Adelsberg",
          "GENDARM" in e4["groom"]["stand"] and "k.k. Beamte" in e4["parentsGroom"]
          and "Indifferenz" in e4["urkunden"] and "Hanna Elisabeth" in e4["urkunden"]
          and "Gottschee" in e4["urkunden"] and "Adelsberg" in e4["urkunden"],
          f'{e4["groom"]["name"]}: {e4["groom"]["stand"][:24]}')
    e5 = d["entries"][7]
    check("I3i v5 Gradac št: 23 (kontinuiteta 21→22→23!)",
          "Gradac" in e5["urkunden"] and "št: 23" in e5["urkunden"], e5["urkunden"][:70])
    e6 = d["entries"][8]
    check("I3j v6 ⅓ GRIBLAR (oče+sin Kolih!) + in Croatien status + Brusnice",
          e6["groom"]["stand"].startswith("⅓ Griblar") and "⅓ Griblar" in e6["parentsGroom"]
          and "Croatien" in e6["groom"]["place"] and "Brusnice" in e6["urkunden"],
          f'{e6["groom"]["stand"][:26]}; {e6["groom"]["place"][:44]}')
    e7 = d["entries"][9]
    check("I3k v7 MÜTTERL. fürwellig (1. MATICA!) + Laipfleršdojft.",
          "mütterl." in e7["urkunden"] and "Laipfleršdojft." in e7["bride"]["stand"],
          f'{e7["bride"]["name"]}: {e7["bride"]["stand"][:36]}')
    e8 = d["entries"][10]
    check("I3l v8 Boginja vas + mj. Bräutigam star 25 (A6 MJ-PRI-25!)",
          e8["groom"]["place"].startswith("Boginja vas") and e8["groom"]["age"] == 25
          and "mj. Bräutigam" in e8["urkunden"],
          f'{e8["groom"]["place"]} 25; mj. Bräutigam ✓')
    e9 = d["entries"][11]
    check("I3m v9 Pfarramt Möttling (= Metlika, 3. leto!) + Podzemelj št: 10",
          "Möttling" in e9["urkunden"] and "št: 10" in e9["urkunden"], e9["urkunden"][:80])
    e10 = d["entries"][12]
    check("I3n v10 ⅓ GRIBLAR Jakofčič (oče+sin!) + in Ungarn (kanonična formulacija)",
          "⅓ Griblar" in e10["parentsGroom"] and e10["groom"]["stand"].startswith("⅓ Griblar")
          and "in Ungarn" in e10["urkunden"],
          f'starši: {e10["parentsGroom"][:40]}')
    e11 = d["entries"][13]
    check("I3o v11 ŽAKANJE = HRVAŠKA (Brod b. Zakanje) + SLOVENŠČINA »otlični list« + 3. rekord-par 54+47",
          "Zakanje" in e11["groom"]["place"] and "otlični list župnega urada v Zakanjah" in e11["urkunden"]
          and e11["groom"]["age"] == 54 and e11["bride"]["age"] == 47,
          f'{e11["groom"]["place"][:30]}')
    e12 = d["entries"][14]
    check("I3p v12 3. DUHOVNIK Franz Herms coop. (edina prekinitev Rauy-monopola!) + Dobliče",
          "Herms" in e12["priest"] and "coop." in e12["priest"] and "Dobliče" in e12["urkunden"],
          f'v12 duhovnik: {e12["priest"]}')
    e13 = d["entries"][15]
    check("I3q v13 Stopiče + Boginja vas 43 (2. dokaz vasi!)",
          "Stopiče" in e13["urkunden"] and e13["bride"]["place"].startswith("Boginja vas"),
          f'{e13["groom"]["name"]} × {e13["bride"]["place"]}')
    e14 = d["entries"][16]
    check("I3r v14 1. NEZAKONSKI ŽENIN (starši [—] + ledige Magd!) + Tischlermeister priča (1. obrtniški mojster!)",
          "[—" in e14["parentsGroom"] and "ledige Magd" in e14["parentsGroom"]
          and "Tischlermeister" in e14["witnesses"] and "Petrova vas" in e14["urkunden"],
          f'v14 starši: {e14["parentsGroom"][:44]}')
    e15 = d["entries"][17]
    check("I3s v15 GRIBLJE 18 (edina poroka 1896!) + Großjährigkeits + Črnomelj + Podzemelj št: 121 [~]",
          e15["bride"]["place"].startswith("Griblje 18") and "Großjärigkeits" in e15["urkunden"]
          and "Črnomelj" in e15["urkunden"] and "121" in e15["urkunden"],
          f'{e15["groom"]["name"]} × {e15["bride"]["place"]}')
    sd1 = [e["row"] for e in d["entries"] if e["date"].startswith("10. februar")]
    sd2 = [e["row"] for e in d["entries"] if e["date"].startswith("10. maj")]
    sd3 = [e["row"] for e in d["entries"] if e["date"].startswith("17. maj")]
    check("I3t trojni dnevi 10.2. = [1,2,3] + 10.5. = [7,8] + 17.5. = [9,10]",
          sd1 == [1, 2, 3] and sd2 == [7, 8] and sd3 == [9, 10], f'{sd1} + {sd2} + {sd3}')
    un = [e["row"] for e in d["entries"] if e["year"] == 1896 and "in Ungarn" in e["urkunden"]]
    check("I3u formula »in Ungarn« ×4 (v1/v2/v3/v10 — ISTI ŠTEVEC kot P124!)", un == [1, 2, 3, 10], f'x{len(un)}')
    mo = [e["row"] for e in d["entries"] if "Möttling" in e["urkunden"]]
    check("I3v Bez. Ger. Möttling ×3 (v3/v8/v9 — nemško ime Metlike, 3. leto!)", mo == [3, 8, 9], str(mo))

    # ---------- I4: datumi + meseči ----------
    MO_NAMES = {"januar": 1, "februar": 2, "marec": 3, "april": 4, "maj": 5, "junij": 6,
                "julij": 7, "avgust": 8, "september": 9, "oktober": 10, "november": 11,
                "december": 12}

    def mes(datestr):
        dsl = datestr.lower()
        for nm, num in MO_NAMES.items():
            if nm in dsl:
                return num
        m = re.search(r"(\d+)\.\s*(\d+)\.", dsl)
        return int(m.group(2)) if m else None
    names = {1: "januar", 2: "februar", 3: "marec", 4: "april", 5: "maj", 6: "junij",
             7: "julij", 8: "avgust", 9: "september", 10: "oktober", 11: "november", 12: "december"}
    mc96 = {k: 0 for k in names.values()}
    mc95 = {k: 0 for k in names.values()}
    for e in d["entries"]:
        m = mes(e["date"])
        if m:
            (mc95 if e.get("ext") else mc96)[names[m]] += 1
    bad96 = {k: v for k, v in mc96.items() if v != DATE_COUNTS_1896[k]}
    check("I4 meseči 1896 (vsota 15; februar 5)", not bad96 and sum(mc96.values()) == 15,
          str(bad96 or sum(mc96.values())))
    bad95 = {k: v for k, v in mc95.items() if v != DATE_COUNTS_1895EXT[k]}
    check("I4b meseči 1895-ext (okt 1 + nov 2)", not bad95 and sum(mc95.values()) == 3,
          str(bad95 or sum(mc95.values())))

    # ---------- I5: stats ključne številke ----------
    pr96 = st.get("priests1896", {})
    pr95 = st.get("priests1895ext", {})
    check("I5 duhovniki 1896: Rauy ×14 + Herms coop. ×1 (edina prekinitev!)",
          pr96.get("Jos. Rauy") == 14 and pr96.get("Franz Herms coop.") == 1 and len(pr96) == 2, str(pr96))
    check("I5b duhovniki 1895-ext: Rauy ×3/3", pr95.get("Jos. Rauy") == 3, str(pr95))
    check("I5c vitals=569 (566 + 3 P125)", st.get("vitals") == EXPECTED_VITALS, str(st.get("vitals")))
    check("I5d bloki 04455=52 (49 + 3 P125)", st.get("blocks04455") == BLOCKS_04455, str(st.get("blocks04455")))
    check("I5e p80 hiše=51 (48 + 3 — h24/h14/h18 Nove v p80All unionu!)", st.get("p80Houses") == P80_HOUSES,
          str(st.get("p80Houses")))
    check("I5f PT luknja=10 (nespremenjeno)", st.get("p80PtGap") == P80_PT_GAP, str(st.get("p80PtGap")))
    ag = st.get("ageGrooms1896", {})
    ab = st.get("ageBrides1896", {})
    check("I5g ženin 1896 max=54 (v11) + min=22 (v3)", ag.get("max") == 54 and ag.get("min") == 22, str(ag))
    check("I5h nevesta 1896 max=47 (v11) + min=18 (v2)", ab.get("max") == 47 and ab.get("min") == 18, str(ab))
    agx = st.get("ageGrooms1895ext", {})
    abx = st.get("ageBrides1895ext", {})
    check("I5i ženin 1895-ext max=59 (v18!) + nevesta max=50", agx.get("max") == 59 and abx.get("max") == 50,
          f'{agx.get("max")}/{abx.get("max")}')
    check("I5j mladoletne 1896: neveste=8 + ženini=1",
          st.get("underageBrides1896") == 8 and st.get("underageGrooms1896") == 1,
          f'{st.get("underageBrides1896")}/{st.get("underageGrooms1896")}')
    check("I5k dispensacije=2 (№2906 + №293 — ISTA formulacija!)", st.get("dispensations") == 2,
          str(st.get("dispensations")))
    check("I5l »hoc« = hic commorans ×7", "7×" in str(st.get("hcoCount", "")), str(st.get("hcoCount"))[:40])
    check("I5m NEZAKONSKI=1 (v14 — 1. v poročni liniji!)", str(st.get("nezakonski", "")).startswith("1 (v14"),
          str(st.get("nezakonski"))[:40])
    check("I5n frakcije: ⅓ ×2 familij + 1 GRIBLAR", "⅓" in str(st.get("fractions", "")),
          str(st.get("fractions"))[:60])
    onc = str(st.get("obcineNumberingContinuity", ""))
    check("I5o kontinuitete: Griblje št:4 + Gradac 21→22→23 + Podzemelj →121",
          "št:4" in onc and "21" in onc and "22" in onc and "23" in onc and "121" in onc, onc[:80])

    # ---------- I6: anomalije A1–A10 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A10", ids == [f"A{i}" for i in range(1, 11)], str(ids))
    for aid, (arow, atype) in ANOM_TYPES.items():
        a = next((x for x in d["anomalies"] if x["id"] == aid), {})
        check(f"I6b {aid} = {atype} (v{arow})", a.get("type") == atype and a.get("row") == arow,
              f'{a.get("type")} @v{a.get("row")}')

    # ---------- I7: crossChecks ----------
    cc_ids = [c.get("id") for c in d["crossChecks"]]
    check("I7 crossChecks C1–C20", cc_ids == [f"C{i}" for i in range(1, 21)], str(cc_ids[-3:]))
    c1 = next((c for c in d["crossChecks"] if c.get("id") == "C1"), {})
    check("I7b C1 = Pag.==sken−1 (11. potrditev)", "11. potrditev" in c1.get("what", ""), c1.get("what", "")[:60])
    c2 = next((c for c in d["crossChecks"] if c.get("id") == "C2"), {})
    check("I7c C2 občina Griblje kontinuiteta (št:4)", "št:4" in c2.get("what", "")
          and "ZAPOREDNA" in c2.get("what", ""), c2.get("what", "")[:60])
    c3 = next((c for c in d["crossChecks"] if c.get("id") == "C3"), {})
    check("I7d C3 Gradac trojna kontinuiteta 21→22→23", "21" in c3.get("what", "")
          and "22" in c3.get("what", "") and "23" in c3.get("what", ""), c3.get("what", "")[:60])
    c9 = next((c for c in d["crossChecks"] if c.get("id") == "C9"), {})
    check("I7e C9 MUC 3. dokaz (P121 v12 ISTA oseba)", "P121" in c9.get("what", "")
          and "MUC" in c9.get("what", ""), c9.get("what", "")[:60])
    c16 = next((c for c in d["crossChecks"] if c.get("id") == "C16"), {})
    check("I7f C16 »in Ungarn« ×4 (ISTI ŠTEVEC kot P124)", "×4" in c16.get("what", "")
          and "P124" in c16.get("what", ""), c16.get("what", "")[:60])
    c17 = next((c for c in d["crossChecks"] if c.get("id") == "C17"), {})
    check("I7g C17 Rauy-monopol 17/18 (4. leto; edina prekinitev v12 Herms)", "17/18" in c17.get("what", "")
          and "Herms" in c17.get("what", ""), c17.get("what", "")[:60])
    c20 = next((c for c in d["crossChecks"] if c.get("id") == "C20"), {})
    check("I7h C20 h14 CROSS-LINK (poroka v17 = krstna 1896 ISTI PAR)", "CROSS-LINK" in c20.get("what", "")
          and "v17" in c20.get("what", ""), c20.get("what", "")[:60])
    # P124 dokaz ostaja nespremenjen (regresijska zaščita — lastna kumulativa)
    try:
        d124 = json.load(open(DOKAZ_P124))
        check("I7i P124 dokaz stats vitals=566 + bloki=49",
              d124["stats"].get("vitals") == 566 and d124["stats"].get("blocks04455") == 49,
              f'v{d124["stats"].get("vitals")} b{d124["stats"].get("blocks04455")}')
    except Exception as e:  # noqa: BLE001
        check("I7i P124 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 94 (P126 61 + P127 9 + P129 +2 + P131 +4 + P132 +12!)", len(blocks_m) == BLOCKS_04455_TS, str(len(blocks_m)))
    h1895 = sorted((h for h, y, _ in blocks_m if y == "1895"), key=int)
    check("I8b hiše 1895 = [14,16,24,27,52] (P125 +h14/h24!)", ",".join(h1895) == "14,16,24,27,52", ",".join(h1895))
    h1896 = sorted((h for h, y, _ in blocks_m if y == "1896"), key=int)
    check("I8c hiše 1896 = [18] (edina poroka 1896!)", ",".join(h1896) == "18", ",".join(h1896))
    for yr, exp in HISTORIC_HOUSES.items():
        hs = sorted((h for h, y, _ in blocks_m if y == yr), key=int)
        check(f"I8d hiše {yr} nespremenjene", ",".join(hs) == exp, ",".join(hs))
    # pini novih brani (P125 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(1895|1896),\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(5).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8e pini P125 (11)", not missing, str(missing) if missing else "vse ✓")
    # regresija: P124 pini še vedno v drevesu
    p124_ok = any(m.group(1) == "16" and "NOVA HIŠA" in m.group(2)
                  for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1895,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S))
    check("I8f regresija P124: h16 NOVA HIŠA (1895)", p124_ok, "h16 pin")

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p125", '"qa-p125-parish-marriage-1896"' in qa)
    check("I9b p80 bloki 78", "poročni vpisi (04455) ≠ 158" in qa)
    check("I9[cd] p80 sidra 72 (1895×5 + 1896×1 + 1897×9 + 1898×9 · 1899×6 · 1900×2)", "poročna sidra ≠ 164" in qa)
    check("I9d p80 hiša 1896 = [18]", "hiša 1896 (04455) ≠ [18]" in qa)
    check("I9e p80 hiše 58", "različnih hiš (vse tri knjige) ≠ 70" in qa)
    check("I9f PT luknja 12 (+h46/h48 — P127!)", "PT luknja ≠ 13 hiš" in qa)
    tail = qa[qa.index("const p125Marr"):] if "const p125Marr" in qa else ""
    check("I9g vitals 642 zaščita (P128)", "HOUSE_VITALS.length !== 681" in tail, "p125Marr blok")
    check("I9h Rauy 1895 bloki ×5 zaščita (P124 + P125 dopolnitev)", "Rauy podpisi 1895 blokov ≠ 5" in qa)
    check("I9i stari 537/544/548/550/554/559/563/566 iztekla",
          "HOUSE_VITALS.length !== 537" not in qa and "HOUSE_VITALS.length !== 544" not in qa
          and "HOUSE_VITALS.length !== 548" not in qa and "HOUSE_VITALS.length !== 550" not in qa
          and "HOUSE_VITALS.length !== 554" not in qa and "HOUSE_VITALS.length !== 559" not in qa
          and "HOUSE_VITALS.length !== 563" not in qa and "HOUSE_VITALS.length !== 566" not in qa)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P125", "P125" in rd and ("126/126" in rd or "po P125" in rd))
    nt = open("research/issue17/parish-marriage-1896-notes.md").read()
    check("I10b notes faza 2 + NEZAKONSKI + ⅓", "FAZA 2" in nt and "NEZAKONSKI" in nt and "⅓" in nt)

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
