#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P128 — župnija Podzemelj: poročna knjiga 04455, polno leto 1899
(s110–s111 == Pag. 109–110) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P127 = 1898): okvir POTRJEN —
s110–s111 == Pag. 109–110 (Pag. == sken − 1, **14. potrditev; velja v
61–110**); **ROKOPISNA GLAVA »1899.« POTRJENA na s110** + **rokopisna glava
»1900.« POTRJENA na s112** (P129 lead + v1/1900 Krasinec 18 ŽUPANIČ!).
**9 vpisov = 2. najmanjše leto linije** (min 1886:7; −18 po rekordnem
1898:27!): jan 3 + feb 1 + maj 1 + jun 1 + avg 1 + sep 1 + okt 1.

NOVELE: **★ NAJSTAREJŠI PAR LINIJE** (v1: 66 + 68 = 134, OBA status 1!) +
**★ ¾ GIBLAR = NOVI NAJVIŠJI ULOMEK** (v7 oče + hči Žugelj!) + **★ 1. ženin
izven sistema** (v9 Pf. St. Michel b. Rudolfswerth = Novo mesto!) + **★
zglasmica-PENTAGON 5 občin** + **★ duhovniška menjava: Novak 5/9 + 1. dokaz
STURM Coop. ×2** (krstna 1898 Šturm 3× — P127 »Herms« možen misread [~]!) +
**★ oče kot priča v istem vpisu** (v3!) + **★ CROSS-ENTRY v1→v4** (ženin
Žibak priča!) + priča-link v6→v9 Županič + **★ KURE/MUC kompleks** (v3 ==
h10 1890!) + ŽURAJEVIČ ×4 + **★ GLYPH-FAMILIJA ŠILAK/ŽIBAK/FILAK** (6
dokazov enega priimka) + **★ VRANOVIČE 5 hiš čez 1898–99** + **★ SODRAŽICA
Pfarramt** (v8) + **★ dispens № 2319** (v7) + oklicni list št: 173 (v9).

Skripta scripts/p128_parish_marriage_1899.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p128_parish_marriage_1899.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES_MIN = 190
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1899.json"
DOKAZ_P127 = "research/issue17/parish-marriage-1898.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1899-notes.md"
EXPECTED_ENTRIES = 9            # v1–v9, vse leto 1899
EXPECTED_ROWS = list(range(1, 10))
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 9
EXPECTED_CROSSCHECKS = 12
GRIBLJE_ROWS = [1, 3, 4]
GRIBLJE_MARRIAGES = 3
GRIBLJE_BLOCKS = 6              # h34 + h44 + h1 + h10 + h20 + h16
GRIBLJE_HOUSES = ["1", "10", "16", "20", "34", "44"]
VITALS_TOTAL = 593              # 587 + 6
BLOKI_04455 = 76                # 70 + 6
SIDRA_TOTAL = 69                # 63 + 6 (1899:6)
NOVAK_COUNT = 5                 # Jos. Novak v vseh 9 vpisih
RAUY_COUNT = 2                  # Jos. Rauy (v3 + v9)
STURM_COUNT = 2                 # Franz Sturm Coop. (v4 + v6)

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), str(detail)))


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def main():
    live = "--live" in sys.argv

    # ---------- I1: dokaz ----------
    d = json.load(open(DOKAZ))
    ent = d["entries"]
    check("I1 dokaz JSON", len(ent) == EXPECTED_ENTRIES, f"{len(ent)}/{EXPECTED_ENTRIES} vpisov")
    check("I1b excluded 0", d.get("excluded") == [], str(d.get("excluded")))
    check("I1c obojestransko 9/9", d["frame"]["counts"]["bothSides"] == 9,
          str(d["frame"]["counts"]))

    # ---------- I2: vrste + datumi ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste 1–9", rows == EXPECTED_ROWS, str(rows))
    months = {"januar": 0, "februar": 0, "maj": 0, "junij": 0, "avgust": 0,
              "september": 0, "oktober": 0}
    for e in ent:
        for m in months:
            if f". {m} " in " " + e["date"] + " " or e["date"].endswith(f". {m} 1899"):
                months[m] += 1
    expect_months = {"januar": 3, "februar": 1, "maj": 1, "junij": 1,
                     "avgust": 1, "september": 1, "oktober": 1}
    check("I2b meseci", months == expect_months, str(months))
    sd = d["frame"]["sameDay"]
    check("I2c isti dan 30.1. [2,3]", sd.get("30.1.1899") == [2, 3], str(sd))
    dc = d["frame"]["dateCounts1899"]
    check("I2d dateCounts", all(dc[k] == v for k, v in expect_months.items()) and
          sum(dc.values()) == 9, str({k: dc[k] for k in expect_months}))

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["row"], e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (14. potrditev)", not bad, str(bad))

    # ---------- I4: Griblje ----------
    g = [e["row"] for e in ent if e.get("griblje")]
    check("I4 Griblje vrste", sorted(g) == GRIBLJE_ROWS, str(g))
    houses = sorted({e["griblje"]["house"] for e in ent if e.get("griblje")} |
                    {e["griblje"]["house2"] for e in ent if e.get("griblje")},
                    key=int)
    check("I4b Griblje hiše", houses == GRIBLJE_HOUSES, str(houses))

    # ---------- I5: parish.ts bloki ----------
    ts = open(PARISH_TS).read()
    n_1899 = ts.count('bookSignature: "04455",\n    year: 1899,')
    check("I5 6 blokov 1899 (04455)", n_1899 == GRIBLJE_BLOCKS, str(n_1899))
    pins = [("34", "NAJSTAREJŠI PAR"), ("44", "1. POROČNI DOKAZ h44"),
            ("1", "1. POROČNI DOKAZ h1"), ("10", "KURE"),
            ("20", "Zimmermannsmeister"), ("16", "3. poročni dokaz h16")]
    for house, pin in pins:
        blk = re.search(
            r'\{\s*houseNo: "' + house + r'",\s*bookSignature: "04455",\s*year: 1899,'
            r'.*?whatSi: "(.*?)"', ts, re.S)
        ok = blk and pin.lower() in blk.group(1).lower()
        check(f"I5b pin h{house} ({pin})", ok, blk.group(1)[:60] if blk else "BLOK MANJKA")
    check("I5c STURM v v4+v6", ts.count("Franz STURM Coop.") >= 2, str(ts.count("Franz STURM Coop.")))
    check("I5d P128 sekcija", "P128 razširitev: POROČNA KNJIGA 04455 — polno leto 1899" in ts)

    # ---------- I6: qa-parish pini ----------
    qa = open(QA_TS).read()
    n593 = qa.count("HOUSE_VITALS.length !== 593")
    n587 = qa.count("HOUSE_VITALS.length !== 587")
    n76 = qa.count("bloki 04455 ≠ 76")
    n70 = qa.count("bloki 04455 ≠ 70")
    check("I6 vitals pini 593", n593 >= 42, str(n593))
    check("I6b brez stale 587 asercij", n587 == 0, str(n587))
    check("I6c bloki pini 76", n76 == 4, str(n76))  # p125 + p126 + p127 + p128
    check("I6d brez stale ≠ 70 asercij", n70 == 0, str(n70))
    check("I6e sidra 69 + 1899:6", "poročna sidra ≠ 69" in qa and
          "h.year === 1899).length !== 6" in qa)
    check("I6f p128Marr hiše", '"1,10,16,20,34,44"' in qa)
    check("I6g qa-p128 test", "qa-p128-parish-marriage-1899" in qa)

    # ---------- I7: duhovniki v vpisih ----------
    pri = " ".join(e["priest"] for e in ent)
    check("I7 Novak ×5", pri.count("Novak") == NOVAK_COUNT, str(pri.count("Novak")))
    check("I7b Rauy ×2", pri.count("Rauy") == RAUY_COUNT, str(pri.count("Rauy")))
    check("I7c Sturm ×2", pri.count("Sturm") == STURM_COUNT, str(pri.count("Sturm")))

    # ---------- I8: anomalije + crossChecks ----------
    check("I8 anomalije", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I8b crossChecks", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    ids = [c["id"] for c in d["crossChecks"]]
    check("I8c C1 cross-entry v1→v4", "C1" in ids and "ŽENIN" in d["crossChecks"][0]["what"])

    # ---------- I9: kontinuiteta + glyph-familija ----------
    d127 = json.load(open(DOKAZ_P127))
    check("I9 P127 dokaz nespremenjen (27)", len(d127["entries"]) == 27)
    allsi = json.dumps(d, ensure_ascii=False)
    check("I9b glyph-familija C11", "C11" in ids and "ŠILAK" in allsi and "FILAK" in allsi)
    check("I9c Šturm tension C12", "C12" in ids and "ŠTURM-MISREAD" in allsi)
    check("I9d Vranoviče korekcija C10", "C10" in ids and "Vranoviče" in json.dumps(ent, ensure_ascii=False))

    # ---------- I10: README + notes ----------
    rd = open(README).read()
    check("I10 README po P128", "P128" in rd and "593" in rd and "76" in rd)
    nt = open(NOTES).read()
    check("I10b notes faza 2 + glyph + Šturm", "FAZA 2" in nt and "glyph-familija" in nt and "ŠTURM" in nt)

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
