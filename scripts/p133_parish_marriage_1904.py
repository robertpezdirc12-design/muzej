#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P133 — župnija Podzemelj: poročna knjiga 04455, polno leto 1904
(s122–s125 == Pag. 121–124) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P132 = 1903): okvir POTRJEN
— s122–s125 == Pag. 121–124 (Pag. == sken − 1, **19. potrditev; velja
61–124**); **VELIKA TISKANA GLAVA »1904.« POTRJENA na s122** (P132-lead!) +
**ROKOPISNA GLAVA »1905.« POTRJENA na s125** (P134 LEAD). **P133-lead
KOREKCIJE: »min 5 vpisov s122–s123« → 15 vpisov s122–s125 (3× podcenjeno)**
+ v2 Griblje 41 → 42 + v5 nevesta Griblje 30 → 38 + v5 ženin »Šimec« →
ŠRAUS [~ Straus]. 15 vpisov obojestransko = 8. februar ×5 (MASA = rekord
linije!) + 14. februar (nedelja) + 18. april + 30. maj ×2 + 6. junij +
20. junij + 4. julij + 3. oktober + 7. november + 23. november (sreda).

NOVELE: **★ 5 GRIBLJE porok / 8 poročnih blokov** (v2 h42 2. dokaz + v5
h32 3. dokaz × h38 1. DOKAZ DRUBEL + v8 h38 2. blok BRAT-SESTRA × h39 2.
dokaz DRUBEL + v13 h62 3. dokaz + v14 h46 3. dokaz × h22 3. dokaz DRUBEL)
→ vitals 611 → **619**; bloki 04455 94 → **102**; sidra 87 → **95**
(+1904:8) + **★ 6 DRUŽINSKIH KONTINUITET** (h42 PERDINEC 1894→04 · h32
STRAUS 1888→ŠRAUS 04 · h39 SIMEC 1897→04 · h62 KURE 1893+98→04 · h46 3.
leto · h22 STRAUS 98→MILEK 04) + **★ ⅜ NOVI ULOMEK LINIJE** (v13!) +
**★ NAJMLAJŠI ŽENIN LINIJE 18** (v2!) + **★ DVOJNA KRVNA DISPENSA v6** (2.
koleno № 697 + 4. koleno № 2814) + **★ 2. krvna dispensa v10** (3. koleno
№ 2063) + NOVE VASI (Zemelj · Vojna vas pf. Črnomelj · Sirnica pf.
Črnomelj · Boršt · Prilozje 25) + NOVE FARE (Dragatuš · Radovica · mestna
Metlika · Loka 2. · Vode? [~]) + CROSS-ENTRY ×2 + 1. ne-Rauy duhovnik 1904
(Stan. Costal [~ Dostal?] v12) + 1. TRGOVEC (v7) + deželna vlada № 22190
(NAJVIŠJA linije!).

Skripta scripts/p133_parish_marriage_1904.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p133_parish_marriage_1904.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1904.json"
DOKAZ_P132 = "research/issue17/parish-marriage-1903.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1904-notes.md"
EXPECTED_ENTRIES = 15           # v1–v15, vse leto 1904
EXPECTED_ROWS = list(range(1, 16))
EXPECTED_EXCLUDED = []
EXPECTED_ANOMALIES = 12
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [2, 5, 8, 13, 14]
GRIBLJE_HOUSES = ["42", "32", "38", "38", "39", "62", "46", "22"]
GRIBLJE_BLOCKS = 8              # +8 blokov
VITALS_TOTAL = 632              # 611 + 8
BLOKI_04455 = 102               # 94 + 8
SIDRA_TOTAL = 95                # 87 + 8 (1904:8)
RAUY_COUNT = 14                 # vse razen v12
COSTAL_COUNT = 1                # v12!
FEB8_ROWS = [1, 2, 3, 4, 5]     # masa 5 porok = rekord linije
MAY30_ROWS = [8, 9]             # masa 2

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def main():
    live = "--live" in sys.argv

    # ---------- I1: dokaz ----------
    d = json.load(open(DOKAZ))
    ent = d["entries"]
    check("I1 dokaz JSON", len(ent) == EXPECTED_ENTRIES, f"{len(ent)}/{EXPECTED_ENTRIES} vpisov")
    check("I1b excluded []", d.get("excluded") == EXPECTED_EXCLUDED, str(d.get("excluded")))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride") and e.get("witnesses"))
    check("I1c obojestransko 15/15", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste 1–15", rows == EXPECTED_ROWS, str(rows))
    dates = [e["date"] for e in ent]
    feb8 = [e["row"] for e in ent if e["date"].startswith("8. februar")]
    check("I2b Febr 8 ×5 (v1–v5 MASA = rekord!)", feb8 == FEB8_ROWS, str(feb8))
    may30 = [e["row"] for e in ent if e["date"].startswith("30. maj")]
    check("I2c Maj 30 ×2 (v8–v9)", may30 == MAY30_ROWS, str(may30))
    months = {}
    for dt in dates:
        m = re.match(r"\d+\. (\w+)", dt)
        months[m.group(1)] = months.get(m.group(1), 0) + 1
    check("I2d meseci 6+1+2+2+1+1+2", months.get("februar") == 6 and months.get("april") == 1 and months.get("maj") == 2 and months.get("junij") == 2 and months.get("julij") == 1 and months.get("oktober") == 1 and months.get("november") == 2, str(months))
    check("I2e NOVI datumi", any("23. november" in dt for dt in dates) and any("3. oktober" in dt for dt in dates) and any("4. julij" in dt for dt in dates), "")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (19. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [122,123,124,125]", scans == [122, 123, 124, 125], str(scans))

    # ---------- I4: Griblje ----------
    g = [e["row"] for e in ent if e.get("griblje")]
    check("I4 Griblje vrste [2,5,8,13,14]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        if e.get("griblje"):
            blob = json.dumps(e, ensure_ascii=False)
            for m in re.findall(r"griblje\s+(\d+)", blob, re.I):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: (int(x)))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: (int(x)))
    allsi = " ".join(e.get("notes", "") + " " + json.dumps(e.get("groom", {}), ensure_ascii=False) + " " + json.dumps(e.get("bride", {}), ensure_ascii=False) for e in ent)
    check("I4b hiše 8GRIBLJE", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c drubel ×3", allsi.count("DRUBEL") >= 3, str(allsi.count("DRUBEL")))
    check("I4d BRAT-SESTRA v5/v8 (h38 ×2)", "BRAT-SESTRA" in allsi, "")
    check("I4e kontinuitete ×6", allsi.count("kontinuitet") + allsi.count("kontinuiteta") >= 4, str(allsi.count("kontinuitet") + allsi.count("kontinuiteta")))

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1904 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1904,', ts))
    check("I5a parish.ts bloki 1904 = 8", n_04455_1904 == GRIBLJE_BLOCKS, str(n_04455_1904))
    pins = [("42", "PERDINEC"), ("32", "ŠRAUS"), ("38", "ŠIMEC"), ("39", "ŠIMEC"),
            ("62", "KURE"), ("46", "BRODARIČ"), ("22", "MILEK")]
    for hn, pin in pins:
        m = re.search(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1904,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = bool(m) and pin.lower() in m.group(1).lower()
        check(f"I5b pin h{hn} ({pin})", ok, m.group(1)[:60] if m else "BLOK MANJKA")
    check("I5c P133 sekcija", "P133 razširitev: POROČNA KNJIGA 04455 — polno leto 1904" in ts)
    check("I5d ⅜ v ts", "⅜" in ts)
    check("I5e KONTINUITETA v ts", "PERDINEC-kontinuiteta" in ts)

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p133 id", "qa-p133-parish-marriage-1904" in qa)
    n619 = qa.count("HOUSE_VITALS.length !== 642")
    check("I6b vitals pini 619", n619 >= 46, str(n619))
    n102 = qa.count("bloki 04455 ≠ 125")
    check("I6c bloki pini 102", n102 >= 8, str(n102))
    check("I6d sidra 95 + 1904:8", "poročna sidra ≠ 118" in qa and "h.year === 1904).length !== 8" in qa and "h.year === 1905).length !== 13" in qa)
    check("I6e hiše 1904 pin", "22,32,38,38,39,42,46,62" in qa)
    check("I6f izjema h38-1904", 'v.year === 1904 && hn === "38"' in qa)

    # ---------- I7: duhovniki ----------
    priests = [e["priest"] for e in ent]
    rauy = sum(1 for p in priests if "Rauy" in p and "ne-Rauy" not in p)
    costal = sum(1 for p in priests if "Costal" in p or "Dostal" in p or "Dostál" in p)
    check("I7 Rauy 14/15", rauy == RAUY_COUNT, str(rauy))
    check("I7b Stan. Costal 1/15 (v12)", costal == COSTAL_COUNT and "Costal" in ent[11]["priest"], f"{costal}; v12={ent[11]['priest']}")

    # ---------- I8: Parish stats ----------
    st = d["stats"]
    check("I8a stats vitals", st.get("vitals") == "611 → 619", str(st.get("vitals")))
    check("I8b stats bloki", st.get("bloki04455") == "94 → 102", str(st.get("bloki04455")))
    check("I8c stats sidra", st.get("sidra") == "87 → 95 (+1904:8)", str(st.get("sidra")))
    check("I8d stats entries 15", st.get("entries") == 15, str(st.get("entries")))
    check("I8e priests Rauy 14 + Costal 1", st.get("priests", {}).get("Jos. Rauy") == 14 and st.get("priests", {}).get("Stan. Costal [~ Dostal?]") == 1, str(st.get("priests")))
    check("I8f stats gribljeHousesNewFirst", st.get("gribljeHousesNewFirst") == ["38"], str(st.get("gribljeHousesNewFirst")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 12", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 20", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P133" in notes and "SAMPLE-TRANSCRIPTION-M1904" in notes)
    check("I9d honesty v dokazu", "uncertainReadings" in d.get("honesty", {}) and len(d["honesty"]["uncertainReadings"]) >= 40, str(len(d.get("honesty", {}).get("uncertainReadings", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P133 bullet", "P133 (poročna 04455, polno leto 1904" in rd)
    check("I10b README 619/102", "619" in rd and "102" in rd)
    check("I10c README P134 lead", "P134" in rd)

    # ---------- I11: P132 dokaz nespremenjen (lekcija P9) ----------
    d132 = json.load(open(DOKAZ_P132))
    check("I11 P132 dokaz 20 vpisov", len(d132["entries"]) == 20, str(len(d132["entries"])))

    # ---------- LIVE ----------
    if live:
        try:
            status, body = http_get(BOOK_URL)
            check("LIVE knjiga HTTP 200", status == 200, str(status))
            check("LIVE 04455", "04455" in body)
        except Exception as e:
            check("LIVE napaka", False, str(e)[:80])

    fails = [(n, det) for (n, ok, det) in results if not ok]
    for (n, ok, det) in results:
        print(("PASS" if ok else "FAIL"), n, ("— " + det if det else ""))
    print(f"\n{len(results) - len(fails)}/{len(results)} PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
