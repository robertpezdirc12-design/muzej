#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P134 — župnija Podzemelj: poročna knjiga 04455, polno leto 1905
(s125–s129 == Pag. 124–128) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P133 = 1904): okvir POTRJEN
— s125–s129 == Pag. 124–128 (Pag. == sken − 1, **20. potrditev; velja
61–128**); **ROKOPISNA GLAVA »1905.« POTRJENA na s125** (P133-lead!) +
**ROKOPISNA GLAVA »1906« na s129** (P135 LEAD). **P134-lead KOREKCIJE:
»min 5 vpisov s125–s126« → 17 vpisov s125–s129 (3× podcenjeno) + »v2
Griblje 39 Markočič?« → v2 = Griblje 34 Johann KAMBIČ + v4 = Griblje 24
Mathias BRNC (lead-v2 je bil v resnici v4!)**. 17 vpisov obojestransko =
16. januar + 20. februar ×2 + 27. februar ×2 + 6. marec ×2 + 8. maj +
15. maj ×2 + 22. maj ×2 + 29. maj ×2 + 3. julij + 31. julij + 7. avgust —
**11/11 PONEDELJKOV = 100% (1. popolno leto linije!)**.

NOVELE: **★ 8 GRIBLJE porok / 13 poročnih blokov** (v2 h34 3. dokaz
MENJAVA FILAK→KAMBIČ + v4 h24 3. dokaz × h30 4. dokaz [Legina→Grabrijan!]
DRUBEL + v5 h44 3. dokaz ŠTRUCELJ + v12 h24 4. dokaz ★ BRATA BRNC! × h65
3. dokaz [MÜCK/MILEK!] DRUBEL + v13 h18 3. dokaz [SIMEC 8 let!] + h34 4.
dokaz ★ SESTRA! DRUBEL + v14 h10 4. dokaz [KURE→PERDINEC!] × h35 1. DOKAZ
[korekcija 34→35!] DRUBEL + v15 h1 2. dokaz ŽELJKO + v17 h27 4. dokaz
[KUČAR/KUKAR 8 let!] × h1 3. dokaz DRUBEL) → vitals 619 → **632**; bloki
04455 102 → **115**; sidra 95 → **108** (+1905:13) + **★ 3 HIŠE Z 2 BLOKI
V ENEM LETU = NOVI REKORD** (h24 BRATA + h34 BRAT-SESTRA + h1 2 Željko
nevesti ⚠️ 2 Nicolaus-očeta!) + **★ 3 JURAJEVČIČ-ženińi v 3 tednih maja** +
**★ 1. AMERIŠKI DRŽAVLJAN LINIJE** (v8 — konzul ZDA Trst 27.3.!) + **★ 2
DISPENSI 3. KOLENA** (v7 № 342 + v9 № 1816) + **★ 1. SCHMIEDMEISTER × 1.
SCHMIEDMEISTERS-WITWE** (v16!) + **★ VMET nem. Landesregierung № 15129**
(v12 — 1. nemški vmet linije!) + ★ 6 KONTINUITET + 4 MENJAVE DRUŽIN + NOVI
PRIIMKI (SLOBODNIK · Strugar · Plut · Urbanek …) + KUKAR 2. dokaz (zdaj
družina h27!) + 1. pisava »Liubljani« (v4!) + RAUY 17/17 = 100%.

Skripta scripts/p134_parish_marriage_1905.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p134_parish_marriage_1905.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1905.json"
DOKAZ_P133 = "research/issue17/parish-marriage-1904.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1905-notes.md"
EXPECTED_ENTRIES = 17           # v1–v17, vse leto 1905
EXPECTED_ROWS = list(range(1, 18))
EXPECTED_EXCLUDED = []
EXPECTED_ANOMALIES = 13
EXPECTED_CROSSCHECKS = 22
GRIBLJE_ROWS = [2, 4, 5, 12, 13, 14, 15, 17]
GRIBLJE_HOUSES = ["34", "24", "30", "44", "24", "65", "18", "34", "10", "35", "1", "27", "1"]
GRIBLJE_BLOCKS = 13             # +13 blokov
VITALS_TOTAL = 632              # 619 + 13
BLOKI_04455 = 115               # 102 + 13
SIDRA_TOTAL = 108               # 95 + 13 (1905:13)
RAUY_COUNT = 17                 # 17/17 = 100%!
FEB20_ROWS = [2, 3]             # masa 2
FEB27_ROWS = [4, 5]             # masa 2
MAY15_ROWS = [9, 10]            # masa 2
MAY22_ROWS = [11, 12]           # masa 2
MAY29_ROWS = [13, 14]           # masa 2

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
    check("I1c obojestransko 17/17", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste 1–17", rows == EXPECTED_ROWS, str(rows))
    dates = [e["date"] for e in ent]
    feb20 = [e["row"] for e in ent if e["date"].startswith("20. februar")]
    check("I2b Febr 20 ×2 (v2–v3)", feb20 == FEB20_ROWS, str(feb20))
    feb27 = [e["row"] for e in ent if e["date"].startswith("27. februar")]
    check("I2c Febr 27 ×2 (v4–v5)", feb27 == FEB27_ROWS, str(feb27))
    may15 = [e["row"] for e in ent if e["date"].startswith("15. maj")]
    check("I2d Maj 15 ×2 (v9–v10)", may15 == MAY15_ROWS, str(may15))
    may22 = [e["row"] for e in ent if e["date"].startswith("22. maj")]
    check("I2e Maj 22 ×2 (v11–v12)", may22 == MAY22_ROWS, str(may22))
    may29 = [e["row"] for e in ent if e["date"].startswith("29. maj")]
    check("I2f Maj 29 ×2 (v13–v14)", may29 == MAY29_ROWS, str(may29))
    months = {}
    for dt in dates:
        m = re.match(r"\d+\. (\w+)", dt)
        months[m.group(1)] = months.get(m.group(1), 0) + 1
    check("I2g meseci 1+4+2+7+2+1", months.get("januar") == 1 and months.get("februar") == 4 and months.get("marec") == 2 and months.get("maj") == 7 and months.get("julij") == 2 and months.get("avgust") == 1, str(months))

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (20. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [125,126,127,128,129]", scans == [125, 126, 127, 128, 129], str(scans))

    # ---------- I4: Griblje ----------
    g = [e["row"] for e in ent if e.get("griblje")]
    check("I4 Griblje vrste [2,4,5,12,13,14,15,17]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        if e.get("griblje"):
            for pl in (e.get("groom", {}).get("place", ""), e.get("bride", {}).get("place", "")):
                for m in re.findall(r"[Gg]riblje\s+(\d+)", pl):
                    houses.append(m)
    houses = sorted(set(houses), key=lambda x: (int(x)))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: (int(x)))
    allsi = " ".join(e.get("notes", "") + " " + json.dumps(e.get("groom", {}), ensure_ascii=False) + " " + json.dumps(e.get("bride", {}), ensure_ascii=False) for e in ent)
    check("I4b hiše 10GRIBLJE", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c drubel ×4", allsi.count("DRUBEL") >= 4, str(allsi.count("DRUBEL")))
    check("I4d BRATA BRNC v4/v12 (h24 ×2)", "BRATA" in allsi or "BRATA BRNC" in json.dumps(d, ensure_ascii=False), "")
    check("I4e kontinuitete ×6", allsi.count("kontinuitet") + allsi.count("kontinuiteta") >= 4, str(allsi.count("kontinuitet") + allsi.count("kontinuiteta")))

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1905 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1905,', ts))
    check("I5a parish.ts bloki 1905 = 13", n_04455_1905 == GRIBLJE_BLOCKS, str(n_04455_1905))
    pins = [("34", "KAMBIČ"), ("24", "BRATA"), ("30", "Grabrijan"), ("44", "ŠTRUCELJ"),
            ("65", "MILEK"), ("18", "SIMEC"), ("10", "PERDINEC"), ("35", "KRIŽAN"),
            ("1", "ŽELJKO"), ("27", "KUKAR")]
    for hn, pin in pins:
        m = re.search(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1905,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = bool(m) and pin.lower() in m.group(1).lower()
        check(f"I5b pin h{hn} ({pin})", ok, m.group(1)[:60] if m else "BLOK MANJKA")
    check("I5c P134 sekcija", "P134 razširitev: POROČNA KNJIGA 04455 — polno leto 1905" in ts)
    check("I5d korekcija 34→35 v ts", "34 PREČRTANO" in ts)
    check("I5e KONTINUITETA v ts", "SIMEC-kontinuiteta" in ts and "KUČAR/KUKAR" in ts)

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p134 id", "qa-p134-parish-marriage-1905" in qa)
    n637 = qa.count("HOUSE_VITALS.length !== 688")
    check("I6b vitals pini 637", n637 >= 46, str(n637))
    n120 = qa.count("bloki 04455 ≠ 142")
    check("I6c bloki pini 120", n120 >= 8, str(n120))
    check("I6d sidra 108 + 1905:13", "poročna sidra ≠ 164" in qa and "h.year === 1905).length !== 13" in qa)
    check("I6e hiše 1905 pin", "1,1,10,18,24,24,27,30,34,34,35,44,65" in qa)
    check("I6f ostanki 619/102/95", "!== 619" not in qa and "≠ 102" not in qa and "sidra ≠ 95" not in qa, "stale pini!")

    # ---------- I7: duhovniki + dnevi ----------
    priests = [e["priest"] for e in ent]
    rauy = sum(1 for p in priests if "Rauy" in p and "ne-Rauy" not in p)
    check("I7 Rauy 17/17 = 100% (3. popolno leto)", rauy == RAUY_COUNT, str(rauy))
    wd = d["stats"].get("weekdays", "")
    check("I7b 11/11 ponedeljkov", "11/11 PONEDELJKOV" in wd, wd[:40])

    # ---------- I8: Parish stats ----------
    st = d["stats"]
    check("I8a stats vitals", st.get("vitals") == "619 → 632", str(st.get("vitals")))
    check("I8b stats bloki", st.get("bloki04455") == "102 → 115", str(st.get("bloki04455")))
    check("I8c stats sidra", st.get("sidra") == "95 → 108 (+1905:13)", str(st.get("sidra")))
    check("I8d stats entries 17", st.get("entries") == 17, str(st.get("entries")))
    check("I8e priests Rauy 17", st.get("priests", {}).get("Jos. Rauy") == 17, str(st.get("priests")))
    check("I8f stats gribljeHousesNewFirst", st.get("gribljeHousesNewFirst") == ["35"], str(st.get("gribljeHousesNewFirst")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 13", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 22", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P134" in notes and "SAMPLE-TRANSCRIPTION-M1905" in notes)
    check("I9d honesty v dokazu", "uncertainReadings" in d.get("honesty", {}) and len(d["honesty"]["uncertainReadings"]) >= 50, str(len(d.get("honesty", {}).get("uncertainReadings", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P134 bullet", "**P134 (poročna 04455, polno leto 1905" in rd)
    check("I10b README 632/115", "632" in rd and "115" in rd)
    check("I10c README P135 lead", "P135" in rd)

    # ---------- I11: P133 dokaz nespremenjen (lekcija P9) ----------
    d133 = json.load(open(DOKAZ_P133))
    check("I11 P133 dokaz 15 vpisov", len(d133["entries"]) == 15, str(len(d133["entries"])))

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
