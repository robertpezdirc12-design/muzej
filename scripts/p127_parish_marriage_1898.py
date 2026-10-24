#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P127 — župnija Podzemelj: poročna knjiga 04455, polno leto 1898
(s104–s109 == Pag. 103–108) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P126 = 1897): okvir POTRJEN —
s104–s109 == Pag. 103–108 (Pag. == sken − 1, **13. potrditev; velja v
61–108**); **ROKOPISNA GLAVA »1898.« POTRJENA na s104** + **rokopisna glava
»1899.« + v1–5/1899 ŽE na s110** (P128 lead!). **27 vpisov = REKORD LINIJE**
(prej 21 — P122/1887!): jan 2 + feb 8 + maj 4 + jun 3 + jul 2 + okt 1 +
nov 7 (brez mar/avg/sep/dec!); **21.11. ×6 porok (v22–v27) = 2. največji dan
linije** (rekord 7 — P122!).

NOVELE: **★ GRIBLJE poroke ×6 = NOVI REKORD LINIJE** (prej 5 — P126 1897!:
v2 h48 + v7 h22×h67 + v9 h22 + v11 h54×h62 + v15 h70 + v20 h34×h46 —
9 poročnih blokov!) + **★ BRAT/SESTRA ŽUPANIČ cross-entry** (v8 ženin Johann
+ v13 nevesta Dorothea = otroka Mathiasa Županiča ½ griblar × Catharine
Šaradinič, Krasinec 18 — 1. tak cross-entry link poročne linije!) + **★ ⅛
griblar** (v23 oče Franz Tomič — NOVI najnižji ulomek, prej 3/16 v6!) +
**★ k.k. LANDESREGIERUNG Laibach Z:12527 (28.8.1898) za OBA mladoletna**
(v20!) + **★ MÖTTLING = nemško METLIKA 5.–6. dokaz** (v9 + v17 + tiskar
»Bindig in Möttlig.«) + **★ KURRENT-REŠITEV: »in Gegenwart obiger
Beystände« ×5** (v10/v15/v19/v20/v27 — faza-1 »in Ungarnwärts obige
Varpända« = misread!) + **★ SLOVENSKI EKVIVALENT ×2** (v11 polna + v12 rep
[~] — skupaj 7!) + **★ Herms ×2 ZAPORED** (v13 coop. + v14 coad. —
Rauy 25/27!) + **★ UMRTVENI LIST PRVE ŽENE ženinove** (v23!) + **★
Decanatsamt Rudolfswert + Bischofs-Akt L:275** (v21!) + **★ JAMŠKI LIST
BOROVNICA** (v25!) + **A6: GRIBLJE 22 ×2 ženina ISTI DAN** (v7 Straus +
v9 Milek — domačija »Nikolaus«!) + občinske vrste: Podzemelj 7→14 | Griblje
1→2→4 | Gradac 31→35 POPOLNA.

Skripta scripts/p127_parish_marriage_1898.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p127_parish_marriage_1898.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES_MIN = 190
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1898.json"
DOKAZ_P126 = "research/issue17/parish-marriage-1897.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
EXPECTED_ENTRIES = 27          # v1–v27, vse leto 1898 (brez ext)
EXPECTED_ROWS = list(range(1, 28))
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 11
EXPECTED_CROSSCHECKS = 14
GRIBLJE_ROWS = [2, 7, 9, 11, 15, 20]
GRIBLJE_MARRIAGES = 6          # NOVI REKORD LINIJE (prej 5 — P126!)
GRIBLJE_BLOCKS = 9             # h48 + h22×2 + h67 + h54 + h62 + h70 + h34 + h46
RAUY_COUNT = 25                # 25/27 — v13+v14 Franz Herms (coop. + coad., ×2 ZAPORED)
GREGWART_FORMULA = 7           # DE ×5 (v10/v15/v19/v20/v27) + SLO ×2 (v11/v12)
ZAIFLNER = 6
MOTTILING = 6
VITALS = 664                   # 587 (P127) + 6 (P128) + 2 (P129) + 4 bloki 1902 (P131) + 12 blokov 1903 (P132)
BLOCKS_04455 = 147               # 61 (P126) + 9
P80_HOUSES = 58                # 52 (P126) + 6 NOVIH v vzorcu (h48/h22/h67/h70/h34/h46 prek 04455-1898!)
P80_PT_GAP = 12                # 10 + h46 + h48 (v luknji 41–60!)
SIDRA_TS = 63                  # 70 − 7 okvir 1886 (pass-1 »60« = POPRAVEK)
RAZPORED = {104: 1, 105: 6, 106: 6, 107: 5, 108: 4, 109: 5}
DATE_COUNTS_1898 = {"januar": 2, "februar": 8, "marec": 0, "april": 0, "maj": 4,
                    "junij": 3, "julij": 2, "avgust": 0, "september": 0,
                    "oktober": 1, "november": 7, "december": 0}
SAME_DAY = {
    "13.2.1898": [3, 4],
    "20.2.1898": [7, 8, 9, 10],
    "9.5.1898": [11, 12],
    "6.6.1898": [15, 16, 17],
    "4.7.1898": [18, 19],
    "21.11.1898": [22, 23, 24, 25, 26, 27],
}
# P127 pini (blok-houseNo → obvezen fragment v whatSi; cf. qa-p127)
BLOCK_PINS = [
    ("48", "1. POROČNI DOKAZ h48"), ("48", "KLOBUČAR"), ("48", "Pniloxje"),
    ("22", "1. POROČNI DOKAZ h22"), ("22", "STRAUS"), ("22", "A6"), ("22", "MILEK"),
    ("67", "1. POROČNI DOKAZ h67"), ("67", "JAKOFČIČ"),
    ("54", "2. POROČNI DOKAZ h54"), ("54", "SIMEC"),
    ("62", "1. POROČNI DOKAZ h62"), ("62", "KURE"),
    ("70", "1. POROČNI DOKAZ h70"), ("70", "PERDINEC"),
    ("34", "1. POROČNI DOKAZ h34"), ("34", "FILAK"),
    ("46", "1. POROČNI DOKAZ h46"), ("46", "KLOBUČAR"),
]
# I8 regresija: stare hiše po letih (iz p126 verifierja) + NOVO 1898
HISTORIC_HOUSES = {
    "1898": "22,22,34,46,48,54,62,67,70",
    "1897": "8,18,27,28,29,33,39,40,40",
    "1896": "18",
    "1895": "14,16,24,27,52",
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
    check("I1b entries=27", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1c excluded=0", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1d anomalije=11", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=14", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (27/27; v1 starši [~ pass-1] označena)", not bad, str(bad) if bad else "vse ✓")
    rows = [e["row"] for e in d["entries"]]
    check("I1g vrstice 1–27", rows == EXPECTED_ROWS, str(rows))
    ext = [e["row"] for e in d["entries"] if e.get("ext")]
    yrs = sorted({e["year"] if "year" in e else 1898 for e in d["entries"]})
    check("I1h brez ext + vsi 1898", not ext and yrs == [1898], f"ext {ext}; leta {yrs}")
    sc = [e["scan"] for e in d["entries"]]
    check("I1i skeni 104–109", all(104 <= s <= 109 for s in sc), str(sorted(set(sc))))

    # ---------- I2: okvir ----------
    st = d["stats"]
    fr = d["frame"]
    check("I2 skeni 104–109", st.get("scans") == [104, 105, 106, 107, 108, 109], str(st.get("scans")))
    check("I2b strani 103–108", st.get("pages") == [103, 104, 105, 106, 107, 108], str(st.get("pages")))
    check("I2c Pag. == sken − 1 (13. potrditev)", "sken − 1" in st.get("pagRule", "")
          and "13. potrditev" in st.get("pagRule", ""), st.get("pagRule", "")[:60])
    check("I2d rokopisna glava 1898 na s104", "1898" in fr.get("bigHeader", "")
          and "s104" in fr.get("bigHeader", ""), fr.get("bigHeader", "")[:70])
    check("I2e glava 1899 + v1–5 ŽE na s110 (P128 lead)", "1899" in fr.get("bigHeader", "")
          and "s110" in fr.get("bigHeader", ""), fr.get("bigHeader", "")[-70:])
    check("I2f entriesTotal=27", fr.get("counts", {}).get("entries") == 27 and st.get("entries") == 27,
          f'{fr.get("counts", {}).get("entries")}/{st.get("entries")}')
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2g razpored 1+6+6+5+4+5", raz == RAZPORED, str(raz))
    check("I2h distribution s104: v1 … s109: v23–27", "s104: v1" in str(fr.get("distribution", ""))
          and "s109: v23–27" in str(fr.get("distribution", "")), str(fr.get("distribution"))[:60])
    lead = d.get("lead", "")
    check("I2i lead: REKORD 27/27", "1898" in lead and "27/27" in lead, lead[:60])
    dc = fr.get("dateCounts1898", {})
    check("I2j dateCounts (jan2 feb8 maj4 jun3 jul2 okt1 nov7)",
          dc == DATE_COUNTS_1898, str(dc))
    sd = fr.get("sameDay", {})
    check("I2k sameDay 6 dni (21.11. = [22–27] ×6 = 2. največji dan!)",
          sd == SAME_DAY, str(sd))

    # ---------- I3: ključni vpisi ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [2,7,9,11,15,20] (×6 NOVI REKORD!)", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 6 (NOVI REKORD LINIJE)", st.get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(st.get("gribljeMarriages")))
    check("I3a Griblje bloki = 9 (h48 + h22×2 + h67 + h54 + h62 + h70 + h34 + h46)",
          st.get("gribljeBlocks") == GRIBLJE_BLOCKS
          and "×2" in str(st.get("gribljeBlocksNote", "")), str(st.get("gribljeBlocksNote"))[:60])

    def E(r):
        return next(e for e in d["entries"] if e["row"] == r)

    e2 = E(2)
    check("I3b v2 nevesta GRIBLJE 48 (1. dokaz h48 — NOVA!) + ženin »z güblarštofa« + Pniloxje 30 [~]",
          e2["bride"]["place"].startswith("GRIBLJE 48")
          and "güblarštofa" in str(e2["groom"].get("stand", ""))
          and "Pniloxje" in e2["groom"]["place"],
          f'{e2["groom"]["name"][:24]} × {e2["bride"]["name"]}')
    e7, e9 = E(7), E(9)
    check("I3c v7+v9 GRIBLJE 22 ×2 ženina ISTI DAN (A6 — domačija »Nikolaus«!)",
          e7["groom"]["place"].startswith("GRIBLJE 22") and e9["groom"]["place"].startswith("GRIBLJE 22")
          and e7["date"] == e9["date"],
          f'v7 {e7["date"]} + v9 {e9["date"]}')
    check("I3d v9 MÖTTLING (k.k. Bez. Ger. — 5. dokaz!) + obe mati KRIŽAN",
          "möttling" in str(e9.get("urkunden", "")).lower()
          and "KRIŽAN" in e9["parentsGroom"].upper() and "KRIŽAN" in e9["parentsBride"].upper(),
          str(e9.get("urkunden", ""))[:70])
    e8, e13 = E(8), E(13)
    check("I3e BRAT/SESTRA ŽUPANIČ (v8 starši ženina == v13 starši neveste — Krasinec 18!)",
          "Mathias Županič" in e8["parentsGroom"] and "Šaradinič" in e8["parentsGroom"]
          and "Mathias Županič" in e13["parentsBride"] and "Šaradinič" in e13["parentsBride"],
          f'v8 PG: {e8["parentsGroom"][:40]}')
    e11 = E(11)
    check("I3f v11 GRIBLJE × GRIBLJE (h54 × h62 — OBE!) + SLOV. formula »v navzočnosti«",
          e11["groom"]["place"].startswith("GRIBLJE 54") and e11["bride"]["place"].startswith("GRIBLJE 62")
          and "navzočnosti" in str(e11.get("urkunden", "")),
          f'{e11["groom"]["place"]} × {e11["bride"]["place"]}')
    check("I3g v13 ženin 55 (Pedirec-varianta!) × Krasinec 18 + zglasmica Gradac št:31",
          e13["groom"]["age"] == 55 and "Pedirec" in e13["groom"]["name"]
          and e13["bride"]["place"].startswith("Krasinec 18")
          and "št:31" in str(e13.get("urkunden", "")),
          f'v13: {e13["groom"]["age"]} × {e13["bride"]["age"]}')
    e17 = E(17)
    check("I3h v17 ženin 54 + madžarska dovolba br. 3363 (Marceu? [~]) + MÖTTLING [?]amte",
          e17["groom"]["age"] == 54 and "3363" in str(e17.get("urkunden", ""))
          and "möttling" in str(e17.get("urkunden", "")).lower(),
          str(e17.get("urkunden", ""))[:70])
    e20 = E(20)
    check("I3i v20 GRIBLJE × GRIBLJE (h34 × h46 — OBA mladoletna 20+21!) + LANDESREGIERUNG Z:12527",
          e20["groom"]["place"].startswith("GRIBLJE 34") and e20["bride"]["place"].startswith("GRIBLJE 46")
          and e20["groom"]["age"] == 20 and e20["bride"]["age"] == 21
          and "12527" in str(e20.get("urkunden", "")) and "LANDESREGIERUNG" in str(e20.get("urkunden", "")).upper(),
          f'v20: {e20["groom"]["age"]} + {e20["bride"]["age"]}')
    e21 = E(21)
    check("I3j v21 Rudolfswert 257 = METLIKA + Krasinec štev:13 + Bischofs-Akt L:275 + DECANATSAMT RUDOLFSWERT",
          "Rudolfswert" in e21["groom"]["place"] and "METLIKA" in e21["groom"]["place"].upper()
          and "KRASINEC" in str(e21.get("urkunden", "")).upper()
          and "275" in str(e21.get("urkunden", ""))
          and "DECANATSAMTE IN RUDOLFSWERT" in str(e21.get("urkunden", "")).upper(),
          e21["groom"]["place"][:50])
    e23 = E(23)
    check("I3k v23 oče ⅛ GRIBLAR (NOVI NAJNIŽJI ULOMEK!) + UMRTVENI LIST PRVE ŽENE + ČRNI VRH",
          "⅛" in e23["parentsGroom"] and "Tomič" in e23["parentsGroom"]
          and "UMRTVENI LIST PRVE ŽENE" in str(e23.get("urkunden", "")).upper()
          and "ČRNI VRH" in str(e23.get("urkunden", "")).upper(),
          e23["parentsGroom"][:60])
    e6 = E(6)
    check("I3l v6 ženin 3/16 griblar (pass 1 zoom ✓) — 2. najnižji ulomek",
          "3/16 griblar" in str(e6["groom"].get("stand", "")),
          str(e6["groom"].get("stand", ""))[:50])
    nov21 = [e["row"] for e in d["entries"] if e["date"].startswith("21. november")]
    check("I3m 21.11. = [22,23,24,25,26,27] (×6 = 2. največji dan linije!)",
          nov21 == [22, 23, 24, 25, 26, 27], str(nov21))
    de_f = sorted(e["row"] for e in d["entries"] if "Gegenwart obiger" in str(e.get("urkunden", "")))
    slo_f = sorted(e["row"] for e in d["entries"] if "navzočnosti" in str(e.get("urkunden", "")))
    check("I3n formula: DE ×5 (v10/v15/v19/v20/v27) + SLO ×2 (v11/v12) = 7 (pass-1 ×4 POPRAVLJENO)",
          de_f == [10, 15, 19, 20, 27] and slo_f == [11, 12] and st.get("gregwartFormula") == GREGWART_FORMULA,
          f"DE {de_f} + SLO {slo_f}")
    mo = sorted(e["row"] for e in d["entries"] if "möttling" in str(e.get("urkunden", "")).lower())
    check("I3o Möttling = Metlika (v9 + v17 — 5.–6. dokaz linije)", mo == [9, 17] and st.get("mottiling") == MOTTILING,
          str(mo))

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
    mc = {k: 0 for k in names.values()}
    for e in d["entries"]:
        m = mes(e["date"])
        if m:
            mc[names[m]] += 1
    badm = {k: v for k, v in mc.items() if v != DATE_COUNTS_1898[k]}
    check("I4 meseči 1898 (vsota 27; februar 8 + november 7)", not badm and sum(mc.values()) == 27,
          str(badm or sum(mc.values())))

    # ---------- I5: stats ključne številke ----------
    check("I5 Rauy 25/27 (v13+v14 Herms ×2 ZAPORED!)",
          st.get("rauyCount") == RAUY_COUNT and "Herms" in str(st.get("rauyNote", "")),
          f'{st.get("rauyCount")}; {str(st.get("rauyNote"))[:50]}')
    rauy_live = sum(1 for e in d["entries"] if e["priest"].startswith("Jos. Rauy"))
    check("I5b Rauy podpisi v podatkih = 25", rauy_live == RAUY_COUNT, str(rauy_live))
    check("I5c Zaiflner ×6", st.get("zaiflner") == ZAIFLNER, str(st.get("zaiflner")))
    check("I5d frakcije: ⅛ (v23 — NAJNIŽJI!) + 3/16 (v6)", "⅛" in str(st.get("fractions", ""))
          and "3/16" in str(st.get("fractions", "")), str(st.get("fractions", ""))[:60])
    check("I5e minors: v20 OBA (20+21) + v12 + v16", "v20" in str(st.get("minors", ""))
          and "OBA" in str(st.get("minors", "")), str(st.get("minors", ""))[:60])
    check("I5f ageRecords: v13 55×35 · v17 54×40 · v6 51×25", "v13" in str(st.get("ageRecords", ""))
          and "v17" in str(st.get("ageRecords", "")) and "v6" in str(st.get("ageRecords", "")),
          str(st.get("ageRecords", ""))[:60])
    check("I5g p80 hiše 58 (6 NOVIH v vzorcu prek 04455-1898!)", st.get("p80Houses") == P80_HOUSES
          and d.get("honesty", {}).get("noNewHouses"), f'{st.get("p80Houses")}; {str(st.get("p80HousesNote"))[:40]}')
    check("I5h PT luknja 12 (+h46/h48!)", st.get("ptGap") == P80_PT_GAP, str(st.get("ptGap")))
    check("I5i vitalsTS=587 + blocks04455TS=70 + sidraTS=63 (P127 ZGODOVINSKI — P128 +6/76/69 po tem)",
          st.get("vitalsTS") == 587 and st.get("blocks04455TS") == 70
          and st.get("sidraTS") == 63,
          f'v{st.get("vitalsTS")} b{st.get("blocks04455TS")} s{st.get("sidraTS")}')

    # ---------- I6: anomalije A1–A11 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A11", ids == [f"A{i}" for i in range(1, 12)], str(ids))

    # ---------- I7: crossChecks ----------
    cc_ids = [c.get("id") for c in d["crossChecks"]]
    check("I7 crossChecks C1–C14", cc_ids == [f"C{i}" for i in range(1, 15)], str(cc_ids[-3:]))
    c_txt = {c.get("id"): str(c.get("what", "")) for c in d["crossChecks"]}
    check("I7b C1 = BRAT/SESTRA ŽUPANIč (v8 == v13)", "Županič" in c_txt.get("C1", "")
          and "BRAT" in c_txt.get("C1", "").upper(), c_txt.get("C1", "")[:60])
    check("I7c C2 = v20 OBA mladoletna (Z:12527)", "12527" in c_txt.get("C2", "")
          or "OBA mladoletna" in c_txt.get("C2", ""), c_txt.get("C2", "")[:60])
    check("I7d C3 = Rudolfswert = Metlika (v21)", "Rudolfswert" in c_txt.get("C3", "")
          and "Metlika" in c_txt.get("C3", ""), c_txt.get("C3", "")[:60])
    # P126 dokaz ostaja nespremenjen (regresijska zaščita — lastna kumulativa)
    try:
        d126 = json.load(open(DOKAZ_P126))
        check("I7e P126 dokaz: 18 vpisov + GRIBLJE 5/9 + Rauy 17",
              d126["stats"].get("entries") == 18 and d126["stats"].get("gribljeMarriages") == 5
              and d126["stats"].get("gribljeBlocks") == 9 and d126["stats"].get("rauyCount") == 17,
              f'e{d126["stats"].get("entries")} g{d126["stats"].get("gribljeMarriages")}/{d126["stats"].get("gribljeBlocks")} r{d126["stats"].get("rauyCount")}')
    except Exception as e:  # noqa: BLE001
        check("I7e P126 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 94 (P126 61 + P127 9 + P129 2 + P129 +2 + P131 +4!)", len(blocks_m) == BLOCKS_04455, str(len(blocks_m)))
    h1898 = sorted((h for h, y, _ in blocks_m if y == "1898"), key=int)
    check("I8b hiše 1898 = [22,22,34,46,48,54,62,67,70] (h22 ×2!)",
          ",".join(h1898) == "22,22,34,46,48,54,62,67,70", ",".join(h1898))
    for yr, exp in HISTORIC_HOUSES.items():
        hs = sorted((h for h, y, _ in blocks_m if y == yr), key=int)
        check(f"I8c hiše {yr} nespremenjene", ",".join(hs) == exp, ",".join(hs))
    # pini novih brani (P127 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1898,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8d pini P127 (19)", not missing, str(missing) if missing else "vse ✓")
    # regresija: P126 pini še vedno v drevesu (h8-1897 Ž:1307 + h40-1897 BRODARIČ)
    p126_ok = any(m.group(1) == "40" and "BRODARIČ" in m.group(2).upper()
                  for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1897,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S))
    check("I8e regresija P126: h40-1897 BRODARIČ", p126_ok, "h40-1897 pin")
    vitals_n = len(re.findall(r'houseNo:\s*"', ts))
    check("I8f HOUSE_VITALS = 664 (587 + 6 + 2 + 4 + 12 + 13 + 5 + 9 + 8 + 5)", vitals_n == VITALS, str(vitals_n))

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p127", '"qa-p127-parish-marriage-1898"' in qa)
    check("I9b p80 bloki 78", "poročni vpisi (04455) ≠ 142" in qa)
    check("I9c p80 sidra 71 (1898×9 · 1899×6 · 1900×2)", "poročna sidra ≠ 140" in qa)
    check("I9d p80 hiše 1898 = [22×2,34,46,48,54,62,67,70]",
          "hiše 1898 (04455) ≠ [22×2,34,46,48,54,62,67,70]" in qa)
    check("I9e p80 hiše 58", "različnih hiš (vse tri knjige) ≠ 68" in qa)
    check("I9f PT luknja 12", "PT luknja ≠ 13 hiš" in qa)
    check("I9g vitals 637 zaščita (P128)", "HOUSE_VITALS.length !== 664" in qa)
    check("I9h Rauy 1898 bloki ×9 zaščita", "Rauy podpisi 1898 blokov ≠ 9" in qa)
    check("I9i stari 537/544/548/550/554/559/563/566/569/578 iztekla",
          "HOUSE_VITALS.length !== 537" not in qa and "HOUSE_VITALS.length !== 544" not in qa
          and "HOUSE_VITALS.length !== 548" not in qa and "HOUSE_VITALS.length !== 550" not in qa
          and "HOUSE_VITALS.length !== 554" not in qa and "HOUSE_VITALS.length !== 559" not in qa
          and "HOUSE_VITALS.length !== 563" not in qa and "HOUSE_VITALS.length !== 566" not in qa
          and "HOUSE_VITALS.length !== 569" not in qa and "HOUSE_VITALS.length !== 578" not in qa)
    check("I9j stari sidra-60 + bloki-61 pini iztekla",
          "poročna sidra ≠ 60" not in qa and "poročni vpisi (04455) ≠ 61" not in qa)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P127", "P127" in rd and ("128/128" in rd or "po P127" in rd))
    nt = open("research/issue17/parish-marriage-1898-notes.md").read()
    check("I10b notes faza 2 + GRIBLJE + Županič", "FAZA 2" in nt and "GRIBLJE" in nt
          and "ŽUPANIČ" in nt.upper())

    # ---------- live ----------
    if live:
        st_, body = http_get(BOOK_URL)
        check("I11 live knjiga 200", st_ == 200, str(st_))
        m = re.search(r'"files":\s*\[(.*?)\]', body.decode("utf-8", "ignore"), re.S)
        n = len(re.findall(r'/image/', m.group(1))) if m else 0
        check("I11b slike ≥ 190", n >= EXPECTED_IMAGES_MIN, str(n))

    # ---------- izpis ----------
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    print(f"\n{passed}/{total} PASS")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
