#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P126 — župnija Podzemelj: poročna knjiga 04455, polno leto 1897
(s101–s104 == Pag. 100–103) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P125 = 1896): okvir POTRJEN —
s101 = Pag. 100 (v15/1896 nad glavo!) + s102–s104 == Pag. 101–103 (Pag. ==
sken − 1, **12. potrditev; velja v 61–104**); **ROKOPISNA GLAVA »1897«
(dvopodčrtana) POTRJENA na s101** + **rokopisna glava »1898.« + v1/1898 ŽE na
s104** (P127 lead!). **18 vpisov** (jan 1 + feb 8 + maj 2 + jul 2 + avg 2 +
okt 2 + nov 1; **15.2. ×5 = 2. največji dan linije za rekordom 7 P122!**).

NOVELE: **★ GRIBLJE poroke ×5 = REKORD LINIJE** (prej 3 — P121 1892!: v5 h8 ×
Krasinec + v9 h40×h29 + v10 h18×h27 + v11 h40×h39 + v18 h33×h28 — 9 poročnih
blokov!) + **★ 2. prekinitev Rauy-monopola: v1 Johann Hofstetter [~], Dechant?
in ADELSBERG (Postojna!), per deleg.** (Rauy 17/18!) + **★ 1. FOTOGRAF-PRIČA
LINIJE** (v1 Pfüllkojf? [~] PHOTOGRAPH!) + **★ MEGA CROSS-LINK v10: Mathias
Simec h18 × Anna Kuchar h27 = PAR iz krstne 04105 1898 h18** (»izmena
gospodinjstva« P125 bloka h18 REŠENA!) + **★ DVOJNA SODNA POLNOLETNOST v15**
(Rudolfovo 23/8. + Metlika 22/8. — 4 dokumenti!) + **★ SAMSKI LIST v16**
(Dragatus 23/9.97 št:405!) + **★ NADOARSTVENO dovoljenje v12** (Metlika 1/7.
štev:103!) + **★ SLOVENSKA sodna polnoletnost v5** (Ž:1307!) + **★ 1.
MÜTTERLICH sodna privolitev v10** (Ž:3791!) + **★ »in UNGARN« ×8 = REKORD** +
**★ v3: ženin 55½ NEZAKONSKI** (mati ledig.; nevesta 41!) + **A6: DVA ženina
h40 v enem letu** (v9 Brodarič + v11 Predanic!) + **A7: Predanic/Perdinec
varianta** + občinske vrste: Podzemelj 1→2–6 (MEŠANI vrstni red 12/2.!)→9→10 |
Griblje 1→2→3→4 POPOLNA | Gradac 26→8?[~A5]→27 | Smihel? Škofjič? 46.

Skripta scripts/p126_parish_marriage_1897.py (I1–I11, --check izpiše PASS/FAIL
in vrne exit code; --live omogoči HTTP preverjanje matricula-online.eu).
Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p126_parish_marriage_1897.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES = 192
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1897.json"
DOKAZ_P125 = "research/issue17/parish-marriage-1896.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
EXPECTED_ENTRIES = 18          # v1–v18, vse leto 1897 (brez ext)
EXPECTED_ROWS = list(range(1, 19))
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 11
EXPECTED_CROSSCHECKS = 21
GRIBLJE_ROWS = [5, 9, 10, 11, 18]
GRIBLJE_MARRIAGES = 5          # REKORD LINIJE (prej 3 — P121 1892!)
GRIBLJE_BLOCKS = 9             # h8 + h40×2 + h29 + h18 + h27 + h39 + h33 + h28
RAUY_COUNT = 17                # 17/18 — v1 Hofstetter (2. prekinitev)
UNGARN_COUNT = 8               # REKORD (P124/P125: ×4)
VITALS = 587                   # 578 (P126) + 9 blokov 1898
BLOCKS_04455 = 115              # 61 (P126) + 9 blokov 1898 (P127) + 2 bloka 1900 (P129)
P80_HOUSES = 52                # 51 (P125) + h28 EDINA NOVA
P80_PT_GAP = 10                # nespremenjeno
RAZPORED = {101: 3, 102: 7, 103: 5, 104: 3}
DATE_COUNTS_1897 = {"januar": 1, "februar": 8, "marec": 0, "april": 0, "maj": 2,
                    "junij": 0, "julij": 2, "avgust": 2, "september": 0,
                    "oktober": 2, "november": 1, "december": 0}
ANOM_ROWS = {  # A1–A11 → vrstica (None = splošna)
    "A1": 1, "A2": 1, "A3": 3, "A4": 4, "A5": 14, "A6": 11, "A7": 11,
    "A8": 16, "A9": None, "A10": None, "A11": 13,
}
# P126 pini (blok-houseNo → obvezen fragment v whatSi; cf. qa-p126)
BLOCK_PINS = [
    ("8", "1. POROČNI DOKAZ h8"), ("8", "JAKOBČIČ"), ("8", "Ž:1307"),
    ("40", "1. POROČNI DOKAZ h40"), ("40", "BRODARIČ"), ("40", "A6"),
    ("29", "1. POROČNI DOKAZ h29"), ("29", "KRIŽAN"),
    ("18", "2. POROČNI DOKAZ h18"), ("18", "MEGA CROSS-LINK"), ("18", "KUCHAR"),
    ("27", "Ž:3791"), ("27", "MLADOLETNA"),
    ("39", "1. POROČNI DOKAZ h39"), ("39", "PREDANIC"), ("39", "Ž:3584"),
    ("33", "1. POROČNI DOKAZ h33"), ("33", "DEBLIČ"), ("33", "št:4"),
    ("28", "1. POROČNI DOKAZ h28"), ("28", "LOŽEK"),
]
# I8 regresija: stare hiše po letih (iz p125 verifierja) + NOVO 1897
HISTORIC_HOUSES = {
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
    check("I1b entries=18", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1c excluded=0", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1d anomalije=11", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=21", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (18/18)", not bad, str(bad) if bad else "vse ✓")
    rows = [e["row"] for e in d["entries"]]
    check("I1g vrstice 1–18", rows == EXPECTED_ROWS, str(rows))
    ext = [e["row"] for e in d["entries"] if e.get("ext")]
    yrs = sorted({e["year"] for e in d["entries"]})
    check("I1h brez ext + vsi 1897", not ext and yrs == [1897], f"ext {ext}; leta {yrs}")

    # ---------- I2: okvir ----------
    st = d["stats"]
    fr = d["frame"]
    check("I2 skeni 101–104", st.get("scans") == [101, 102, 103, 104], str(st.get("scans")))
    check("I2b strani 100–103", st.get("pages") == [100, 101, 102, 103], str(st.get("pages")))
    check("I2c Pag. == sken − 1 (12. potrditev)", "sken − 1" in st.get("pagRule", "")
          and "12. potrditev" in st.get("pagRule", ""), st.get("pagRule", "")[:60])
    check("I2d rokopisna glava 1897 na s101", "s101" in fr.get("bigHeader", "")
          and "1897" in fr.get("bigHeader", ""), fr.get("bigHeader", "")[:70])
    check("I2e glava 1898 + v1 ŽE na s104 (P127 lead)", "1898" in fr.get("bigHeader", "")
          and "s104" in fr.get("bigHeader", ""), fr.get("bigHeader", "")[-70:])
    check("I2f entriesTotal=18", fr.get("entries") == 18 and st.get("entries") == 18,
          f'{fr.get("entries")}/{st.get("entries")}')
    sc = [e["scan"] for e in d["entries"]]
    check("I2g skeni znotraj 101–104", all(101 <= s <= 104 for s in sc), str(sorted(set(sc))))
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2h razpored 3+6+6+3", raz == RAZPORED, str(raz))
    check("I2i distribution", "s101: v1–3" in str(fr.get("distribution", ""))
          and "s104: v16–18" in str(fr.get("distribution", "")), str(fr.get("distribution"))[:60])
    lead = d.get("lead", "")
    check("I2j lead: polno leto 1897", "1897" in lead and "18/18" in lead, lead[:60])
    dc = fr.get("dateCounts1897", {})
    check("I2k dateCounts (jan1 feb8 maj2 jul2 avg2 okt2 nov1)",
          dc == DATE_COUNTS_1897, str(dc))
    sd = fr.get("sameDay", {})
    check("I2l sameDay 15.2=[4–8] + 31.5=[10,11]",
          sd.get("15.2.1897") == [4, 5, 6, 7, 8] and sd.get("31.5.1897") == [10, 11], str(sd))

    # ---------- I3: ključni vpisi ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [5,9,10,11,18] (×5 REKORD!)", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 5 (REKORD LINIJE)", st.get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(st.get("gribljeMarriages")))
    check("I3a Griblje bloki = 9 (h8 + h40×2 + h29 + h18 + h27 + h39 + h33 + h28)",
          st.get("gribljeBlocks") == GRIBLJE_BLOCKS
          and "×2" in str(st.get("gribljeBlocksNote", "")), str(st.get("gribljeBlocksNote"))[:60])
    e1 = d["entries"][0]
    check("I3b v1 Hofstetter Adelsberg per deleg. (2. prekinitev Rauy!) + PHOTOGRAPH priča + Podzemelj št:1 + Möttling",
          "Hofstetter" in e1["priest"] and "Adelsberg" in e1["priest"] and "per deleg" in e1["priest"]
          and "PHOTOGRAPH" in e1["witnesses"].upper()
          and "Podzemelj" in e1["urkunden"] and "št:1" in e1["urkunden"]
          and "Möttling" in e1["urkunden"],
          f'v1 duhovnik: {e1["priest"][:40]}')
    e3 = next(e for e in d["entries"] if e["row"] == 3)
    check("I3c v3 ženin 55½ NEZAKONSKI (mati Gertrud Koplan ledig. — brez očeta!) + nevesta 41",
          e3["groom"]["age"] == 55.5 and e3["bride"]["age"] == 41
          and "NEZAKONSKI" in e3["parentsGroom"] and "Koplan" in e3["parentsGroom"]
          and "ledig" in e3["parentsGroom"],
          f'v3: {e3["groom"]["age"]} × {e3["bride"]["age"]}; starši: {e3["parentsGroom"][:40]}')
    e5 = next(e for e in d["entries"] if e["row"] == 5)
    check("I3d v5 GRIBLJE 8 (1. poročni dokaz h8!) + SLOVENSKA polnoletnost Ž:1307 + Podzemelj št:3",
          e5["bride"]["place"].startswith("GRIBLJE 8")
          and "Ž:1307" in e5["urkunden"] and "št:3" in e5["urkunden"],
          f'{e5["groom"]["name"][:24]} × {e5["bride"]["name"]}')
    e9 = next(e for e in d["entries"] if e["row"] == 9)
    check("I3e v9 GRIBLJE × GRIBLJE (h40 × h29 — OBE NOVI!) + Griblje štev:1",
          e9["groom"]["place"].startswith("GRIBLJE 40") and e9["bride"]["place"].startswith("GRIBLJE 29")
          and "štev:1" in e9["urkunden"].replace("št", "štev") or "štev:1" in e9["urkunden"],
          f'{e9["groom"]["place"]} × {e9["bride"]["place"]}')
    e10 = next(e for e in d["entries"] if e["row"] == 10)
    check("I3f v10 MEGA CROSS-LINK (h18 × h27) + 1. MÜTTERLICH Ž:3791 + mladoletna 16",
          e10["groom"]["place"].startswith("GRIBLJE 18") and e10["bride"]["place"].startswith("GRIBLJE 27")
          and "Ž:3791" in e10["urkunden"] and "mütterlich" in e10["urkunden"].lower()
          and e10["bride"]["age"] == 16.5,
          f'{e10["groom"]["name"][:24]} × {e10["bride"]["name"]}; nevesta {e10["bride"]["age"]}')
    e11 = next(e for e in d["entries"] if e["row"] == 11)
    check("I3g v11 h40×h39 + PREDANIC/PERDINEC varianta (A7) + in UNGARN + Griblje št:2 (PRED št:3!)",
          e11["groom"]["place"].startswith("GRIBLJE 40") and e11["bride"]["place"].startswith("GRIBLJE 39")
          and "Predanic" in e11["groom"]["name"] and "PERDINEC" in e11["parentsGroom"].upper()
          and "in UNGARN" in e11["urkunden"] and "št:2" in e11["urkunden"],
          f'{e11["groom"]["name"][:30]}; starši ženina: {e11["parentsGroom"][:36]}')
    e12 = next(e for e in d["entries"] if e["row"] == 12)
    check("I3h v12 NADOARSTVENO dovoljenje (sodišče Metlika 1/7. štev:103 — SKRBNIŠKO!)",
          "NADOARSTVENO" in e12["urkunden"] and "Metliki" in e12["urkunden"]
          and "1/7" in e12["urkunden"] and "štev:103" in e12["urkunden"],
          e12["urkunden"][:80])
    e13 = next(e for e in d["entries"] if e["row"] == 13)
    check("I3i v13 DVOJNI status »½ gbl. Sohn und Zimmermann«",
          e13["groom"]["stand"].startswith("½ gbl. Sohn und Zimmermann"),
          f'v13 stand: {e13["groom"]["stand"][:44]}')
    e15 = next(e for e in d["entries"] if e["row"] == 15)
    check("I3j v15 DVOJNA SODNA POLNOLETNOST (Rudolfovo 23/8. + Metlika 22/8.) + Smihel? št:46 + Vavti vasi",
          "Rudolfovem" in e15["urkunden"] and "23/8" in e15["urkunden"]
          and "Metliki" in e15["urkunden"] and "22/8" in e15["urkunden"]
          and "št:46" in e15["urkunden"] and "Vavti" in e15["urkunden"],
          e15["urkunden"][:80])
    e16 = next(e for e in d["entries"] if e["row"] == 16)
    check("I3k v16 SAMSKI LIST (»Upričevalo samskiga stana« Dragatus 23/9.97 št:405!)",
          "samskiga stana" in e16["urkunden"] and "405" in e16["urkunden"]
          and "Dragatu" in e16["urkunden"] and "23/9" in e16["urkunden"],
          e16["urkunden"][:90])
    e18 = d["entries"][17]
    check("I3l v18 GRIBLJE × GRIBLJE (h33 × h28 — 5. in ZADNJA poroka rekordnega leta!) + Griblje št:4",
          e18["groom"]["place"].startswith("GRIBLJE 33") and e18["bride"]["place"].startswith("GRIBLJE 28")
          and "št:4" in e18["urkunden"],
          f'{e18["groom"]["name"][:24]} × {e18["bride"]["name"]}')
    sd1 = [e["row"] for e in d["entries"] if e["date"].startswith("15. februar")]
    sd2 = [e["row"] for e in d["entries"] if e["date"].startswith("31. maj")]
    check("I3m 15.2. = [4,5,6,7,8] (2. največji dan linije!) + 31.5. = [10,11]",
          sd1 == [4, 5, 6, 7, 8] and sd2 == [10, 11], f"{sd1} + {sd2}")
    un = [e["row"] for e in d["entries"] if "ungarn" in e["urkunden"].lower()]
    check("I3n formula »in Ungarn« ×8 = REKORD (v4[~]/v6/v7/v8/v11/v14/v16/v17)",
          un == [4, 6, 7, 8, 11, 14, 16, 17] and st.get("ungarnFormula") == UNGARN_COUNT,
          f"x{len(un)}: {un}")
    mo = [e["row"] for e in d["entries"] if "Möttling" in e["urkunden"]]
    check("I3o Möttling = Metlika (v1 — 4. leto potrditve!)", 1 in mo, str(mo))

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
    badm = {k: v for k, v in mc.items() if v != DATE_COUNTS_1897[k]}
    check("I4 meseči 1897 (vsota 18; februar 8)", not badm and sum(mc.values()) == 18,
          str(badm or sum(mc.values())))

    # ---------- I5: stats ključne številke ----------
    check("I5 Rauy 17/18 (v1 Hofstetter = 2. prekinitev!)", st.get("rauyCount") == RAUY_COUNT
          and "Hofstetter" in str(st.get("rauyNote", "")),
          f'{st.get("rauyCount")}; {str(st.get("rauyNote"))[:50]}')
    ag = st.get("ages", {})
    check("I5b ženin max=55½ (v3 nezakonski!) + nevesta max=41",
          ag.get("maxGroom") == 55.5 and ag.get("maxBride") == 41, str(ag)[:70])
    check("I5c mladoletne neveste = 3 (v10 16½ + v11 17½ + v17 16½)",
          st.get("minorBrides") == 3, str(st.get("minorBrides")))
    ill = st.get("illegitimate", {})
    check("I5d nezakonski: ženin v3 + nevesta v16 (oče »—«)",
          "v3" in str(ill.get("grooms", "")) and "v16" in str(ill.get("brides", "")), str(ill)[:70])
    check("I5e PHOTOGRAPH priča (v1 — 1. linije!)", "Photograph" in str(st.get("photographWitness", ""))
          or "PHOTOGRAPH" in str(st.get("photographWitness", "")),
          str(st.get("photographWitness"))[:60])
    check("I5f samski list (v16 Dragatus št:405)", "št:405" in str(st.get("samskiList", ""))
          or "405" in str(st.get("samskiList", "")), str(st.get("samskiList"))[:60])
    fam = st.get("families", {})
    check("I5g familije: Perdinec ×6 (7. leto!) + Jakobčič ×5 + Klepec ×5",
          fam.get("Perdinec/Perdinec-mreža") == 6 and fam.get("Jakobčič") == 5 and fam.get("Klepec") == 5,
          str(fam)[:80])
    cd = str(st.get("courtDocs", ""))
    check("I5h sodni dokumenti ×5: v5 Ž:1307 + v10 Ž:3791 + v11 Ž:3584 + v12 št:103 + v15 Rudolfovo DVOJNA",
          "Ž:1307" in cd and "Ž:3791" in cd and "103" in cd and "Rudolfovo" in cd
          and "Ž:3584" in cd and len(st.get("courtDocs", [])) == 5, cd[:80])
    zg = str(st.get("zglasmice", ""))
    check("I5i zglasmice: Podzemelj 1→2–6 MEŠANO→9→10 + Griblje 1–4 POPOLNA",
          "2–6" in zg and "Griblje" in zg and "Gradac" in zg, zg[:80])

    # ---------- I6: anomalije A1–A11 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A11", ids == [f"A{i}" for i in range(1, 12)], str(ids))
    for aid, arow in ANOM_ROWS.items():
        a = next((x for x in d["anomalies"] if x["id"] == aid), {})
        if arow is None:
            check(f"I6b {aid} obstaja", bool(a), str(a.get("what", ""))[:40])
        else:
            check(f"I6b {aid} @v{arow}", a.get("row") == arow, f'row {a.get("row")}')

    # ---------- I7: crossChecks ----------
    cc_ids = [c.get("id") for c in d["crossChecks"]]
    check("I7 crossChecks C1–C21", cc_ids == [f"C{i}" for i in range(1, 22)], str(cc_ids[-3:]))
    c_txt = {c.get("id"): str(c.get("what", "")) for c in d["crossChecks"]}
    check("I7b C1 = Podzemelj monotona vrsta", "monotona" in c_txt.get("C1", "").lower()
          and "2–6" in c_txt.get("C1", ""), c_txt.get("C1", "")[:60])
    check("I7c C2 = Griblje POPOLNA vrsta 1→2→3→4", "POPOLNA" in c_txt.get("C2", "")
          and "4 (21/11.)" in c_txt.get("C2", ""), c_txt.get("C2", "")[:60])
    check("I7d C3 = Rauy podpis-oblika 17 (identična 1896!)", "17" in c_txt.get("C3", "")
          and "Rauy" in c_txt.get("C3", ""), c_txt.get("C3", "")[:60])
    check("I7e C4 = Möttling = Metlika (P124)", "Möttling" in c_txt.get("C4", "")
          and "P124" in c_txt.get("C4", ""), c_txt.get("C4", "")[:60])
    check("I7f C5 = Rudolfswert/Rudolfovo (P124 Beamte-oče)", "Rudolfov" in c_txt.get("C5", "")
          and "P124" in c_txt.get("C5", ""), c_txt.get("C5", "")[:60])
    c21 = next((c for c in d["crossChecks"] if c.get("id") == "C21"), {})
    check("I7g C21 MEGA CROSS-LINK (v10 = PAR iz krstne 04105 1898 h18)",
          "04105" in c21.get("what", "") and "MEGA" in c21.get("what", ""), c21.get("what", "")[:60])
    # P125 dokaz ostaja nespremenjen (regresijska zaščita — lastna kumulativa)
    try:
        d125 = json.load(open(DOKAZ_P125))
        check("I7h P125 dokaz stats vitals=569 + bloki=52",
              d125["stats"].get("vitals") == 569 and d125["stats"].get("blocks04455") == 52,
              f'v{d125["stats"].get("vitals")} b{d125["stats"].get("blocks04455")}')
    except Exception as e:  # noqa: BLE001
        check("I7h P125 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 94 (P126 61 + P127 9 + P129 +2 + P131 +4 + P132 +12!)", len(blocks_m) == BLOCKS_04455, str(len(blocks_m)))
    h1897 = sorted((h for h, y, _ in blocks_m if y == "1897"), key=int)
    check("I8b hiše 1897 = [8,18,27,28,29,33,39,40,40] (h40 ×2!)",
          ",".join(h1897) == "8,18,27,28,29,33,39,40,40", ",".join(h1897))
    for yr, exp in HISTORIC_HOUSES.items():
        hs = sorted((h for h, y, _ in blocks_m if y == yr), key=int)
        check(f"I8c hiše {yr} nespremenjene", ",".join(hs) == exp, ",".join(hs))
    # pini novih brani (P126 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1897,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8d pini P126 (21)", not missing, str(missing) if missing else "vse ✓")
    # regresija: P125 pini še vedno v drevesu (h18-1896 + h24/h14-1895)
    p125_ok = any(m.group(1) == "18" and "GROSSJÄHRIGKEITS" in m.group(2).upper()
                  for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1896,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S))
    check("I8e regresija P125: h18-1896 GROSSJÄHRIGKEITS", p125_ok, "h18-1896 pin")

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p126", '"qa-p126-parish-marriage-1897"' in qa)
    check("I9b p80 bloki 78", "poročni vpisi (04455) ≠ 115" in qa)
    check("I9c p80 sidra 71 (1897×9 + 1898×9 · 1899×6 · 1900×2)", "poročna sidra ≠ 108" in qa)
    check("I9d p80 hiše 1897 = [8,18,27,28,29,33,39,40×2]",
          "hiše 1897 (04455) ≠ [8,18,27,28,29,33,39,40×2]" in qa)
    check("I9e p80 hiše 58 (+6 NOVIH 1898 — P127!)", "različnih hiš (vse tri knjige) ≠ 64" in qa)
    check("I9f PT luknja 12 (+h46/h48 — P127!)", "PT luknja ≠ 12 hiš" in qa)
    check("I9g vitals 595 zaščita (P128)", "HOUSE_VITALS.length !== 632" in qa)
    check("I9h Rauy 1897 bloki ×9 zaščita", "Rauy podpisi 1897 blokov ≠ 9" in qa)
    check("I9i stari 537/544/548/550/554/559/563/566/569 iztekla",
          "HOUSE_VITALS.length !== 537" not in qa and "HOUSE_VITALS.length !== 544" not in qa
          and "HOUSE_VITALS.length !== 548" not in qa and "HOUSE_VITALS.length !== 550" not in qa
          and "HOUSE_VITALS.length !== 554" not in qa and "HOUSE_VITALS.length !== 559" not in qa
          and "HOUSE_VITALS.length !== 563" not in qa and "HOUSE_VITALS.length !== 566" not in qa
          and "HOUSE_VITALS.length !== 569" not in qa)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P126", "P126" in rd and ("127/127" in rd or "po P126" in rd))
    nt = open("research/issue17/parish-marriage-1897-notes.md").read()
    check("I10b notes faza 2 + GRIBLJE + fotograf-priča", "FAZA 2" in nt and "GRIBLJE" in nt
          and "fotograf" in nt.lower())

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
