#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P136 — župnija Podzemelj: poročna knjiga 04455, polno leto 1907
(s132–s134 == Pag. 131–133) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P135 = 1906): okvir POTRJEN
— s132–s134 == Pag. 131–133 (Pag. == sken − 1, **22. potrditev; velja
61–133**); **ROKOPISNA GLAVA »1907« POTRJENA na s132** (P135-lead!) +
**ROKOPISNA GLAVA »1908« na s134 = P137 LEAD** (1908-v1 Jän 26 + v2 že
vidna!). **P136-lead KOREKCIJE: »min 5 vpisov s132« → 12 vpisov s132–s134
(2,4× podcenjano — 22. leto zapored!) + VSI lead-datumi NAPAČNI** (»Jän 13
· Jän 24? · Febr 14? · Mär 9? · Okt 6?« → pravilno Jän 28 · Febr 4/11/18/25
· Mär 4 · Apr 22 · Mai 13 · Jun 3 · Jul 8 · Sep 16/30 — **12/12 PONEDELJKOV
= 2. POPOLNO PONEDELJKOVSKO LETO** po P134 11/11!).

NOVELE: **★ v11 DISPENSA OD KRVNEGA SORODSTVA V 2. KOLENU STRANSKE VRSTE**
(od knj. čh. ordinarijata v LJUBLJANI od 28/8. 1907 — 1. dispensa po
P134-1905!) + **★ DVE KOVAČ-DRUŽINI NA GRIBLJE 6** (v5-oče Nicolaus +
v11-oče Georg — brata?!; h6 = 2 bloka v letu = 3. dokaz po 1903!) + **★
v5 GRIBLJE-DRUBEL h6 × h7** (sosednji hiši!) + **★ 20-LETNA LUKNJA h3**
(1887→1907 — 2. najdaljša po h21!) + **★ NOVA HIŠA h19** (66. poročna hiša!)
→ vitals 637 → **642**; bloki 04455 120 → **125**; sidra 113 → **118**
(+1907:5); p80 hiše 65 → **66** (+h19) + **★ PEZDIREC-mreža ×5 + MUC ×3 +
NOVAK ×3 + JAKŠA ×2 + ŠARADINIČ 9-letna kontinuiteta h42** (1898 v26!) +
**★ 1. NE-RAUY PODPIS 1907** (v7 [~ Jos. Pavlič?] — RAUY 11/12) + **★
pokojni oče Žugelj †** (v12 — 1. po P132!) + **★ zglašnica št. 119**
(občina Dobliče? [~]) + **★ 5 mladoletnih nevest + 2 mladoletna ženina**
(rekord 7 dokumentov!) + VOJNA VAS 4 (2. dokaz!) + LAHINJA pf. Črnomelj (2.
vas fare!) + NOVI PRIIMKI ×7+.

Skripta scripts/p136_parish_marriage_1907.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p136_parish_marriage_1907.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1907.json"
DOKAZ_P135 = "research/issue17/parish-marriage-1906.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1907-notes.md"
EXPECTED_ENTRIES = 12           # v1–v12 (vsi oštevilčeni)
EXPECTED_EXCLUDED = []
EXPECTED_ANOMALIES = 15
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [4, 5, 9, 11]
GRIBLJE_HOUSES = ["3", "6", "7", "19"]
GRIBLJE_BLOCKS = 5              # +5 blokov (h6 ×2!)
VITALS_TOTAL = 642              # 637 + 5
BLOKI_04455 = 125               # 120 + 5
SIDRA_TOTAL = 118               # 113 + 5 (1907:5)
RAUY_COUNT = 5                  # 5/5 GRIBLJE blokov (celo leto: Rauy 11/12 + 1 [~ Pavlič?])
EXPECTED_MONDAYS = 12           # 12/12 — 2. popolno leto!

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
    check("I1c obojestransko 12/12", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [str(e["row"]) for e in ent]
    check("I2 vrste 1–12", rows == [str(i) for i in range(1, 13)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\d+\. (\w+)", dt)
        if m:
            months[m.group(1)] = months.get(m.group(1), 0) + 1
    check("I2b meseci 1+4+1+1+1+1+1+1+2", months.get("januar") == 1 and months.get("februar") == 4 and months.get("marec") == 1 and months.get("april") == 1 and months.get("maj") == 1 and months.get("junij") == 1 and months.get("julij") == 1 and months.get("september") == 2, str(months))
    check("I2c 12/12 ponedeljkov (2. popolno leto!)", sum(1 for dt in dates if "(ponedeljek)" in dt) == EXPECTED_MONDAYS, str(sum(1 for dt in dates if "(ponedeljek)" in dt)))

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (22. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [132,133,134]", scans == [132, 133, 134], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = e.get("groom", {}).get("place", "") + " " + e.get("bride", {}).get("place", "")
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = [str(r) for r in griblje_rows(ent)]
    check("I4 Griblje vrste [4, 5, 9, 11]", g == ["4", "5", "9", "11"], str(g))
    houses = []
    for e in ent:
        for pl in (e.get("groom", {}).get("place", ""), e.get("bride", {}).get("place", "")):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 4 GRIBLJE [3,6,7,19]", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c h6 ×2 (v5 ženin + v11 nevesta — DVE Kovač-družini!)", allsi.count("GRIBLJE 6") >= 2, str(allsi.count("GRIBLJE 6")))
    check("I4d NOVA HIŠA h19", "NOVA HIŠA" in allsi, "")
    check("I4e 20-LETNA LUKNJA h3", "20-LETNA LUKNJA" in allsi, "")
    check("I4f DISPENSA 2. kolena", "DISPENSA OD KRVNEGA SORODSTVA" in allsi and "LJUBLJANI" in allsi, "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1907 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1907,', ts))
    check("I5a parish.ts bloki 1907 = 5", n_04455_1907 == GRIBLJE_BLOCKS, str(n_04455_1907))
    pins = [("19", "NOVA HIŠA"), ("19", "HRANC"), ("6", "DRUBEL sosednjih hiš"), ("6", "DVE Kovač-družini"),
            ("7", "3. poročni dokaz h7"), ("3", "20-LETNA LUKNJA"), ("3", "PEZDIREC-mreža")]
    for hn, pin in pins:
        m = re.search(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1907,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = bool(m) and pin.lower() in m.group(1).lower()
        check(f"I5b pin h{hn} ({pin})", ok, m.group(1)[:60] if m else "BLOK MANJKA")
    check("I5c P136 sekcija", "P136 razširitev: POROČNA KNJIGA 04455 — polno leto 1907" in ts)
    check("I5d DISPENSA v ts", "DISPENSA OD KRVNEGA SORODSTVA" in ts and "LJUBLJANI" in ts)
    check("I5e 2. BLOK hiše v letu v ts", "2. BLOK hiše v letu" in ts)

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p136 id", "qa-p136-parish-marriage-1907" in qa)
    n642 = qa.count("HOUSE_VITALS.length !== 642")
    check("I6b vitals pini 642", n642 >= 50, str(n642))
    n125 = qa.count("bloki 04455 ≠ 125")
    check("I6c bloki pini 125", n125 >= 12, str(n125))
    check("I6d sidra 118 + 1907:5", "poročna sidra ≠ 118" in qa and "h.year === 1907).length !== 5" in qa)
    check("I6e hiše 1907 pin", '"3,6,6,7,19"' in qa)
    check("I6f ostanki 637/120/113", "!== 637" not in qa and "bloki 04455 ≠ 120" not in qa and "poročna sidra ≠ 113" not in qa, "stale pini!")
    check("I6g izjema p96-h19-1907", 'h.bookSignature === "04455" && h.year === 1907' in qa)
    check("I6h izjema p85-h7-1907", 'v.bookSignature === "04455" && v.year === 1907 && hn === "7"' in qa)

    # ---------- I7: duhovniki + dnevi ----------
    priests = [e["priest"] for e in ent]
    rauy = sum(1 for p in priests if "Rauy" in p)
    check("I7 Rauy 11/12 + 1 [~ Pavlič?]", rauy == 11, str(rauy))
    neray = sum(1 for p in priests if "Rauy" not in p)
    check("I7b 1 ne-Rauy (v7 [~ Pavlič?])", neray == 1, str(neray))
    wd = d["stats"].get("mondays", "")
    check("I7c 12/12 ponedeljkov (2. popolno leto)", "12/12" in wd and "POPOLNO" in wd, wd[:60])

    # ---------- I8: Parish stats ----------
    st = d["stats"]
    check("I8a stats vitals", st.get("vitals") == "637 → 642", str(st.get("vitals")))
    check("I8b stats bloki", st.get("bloki04455") == "120 → 125", str(st.get("bloki04455")))
    check("I8c stats sidra", "113" in str(st.get("sidra", "")) and "118" in str(st.get("sidra", "")) and "1907:5" in str(st.get("sidra", "")), str(st.get("sidra")))
    check("I8d stats entries 12", st.get("entries") == 12, str(st.get("entries")))
    check("I8e stats gribljeHousesNewFirst", st.get("gribljeHousesNewFirst") == ["19"], str(st.get("gribljeHousesNewFirst")))
    check("I8f stats gribljeWeddings 4", st.get("gribljeWeddings") == 4, str(st.get("gribljeWeddings")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 15", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 20", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P136" in notes and "SAMPLE-TRANSCRIPTION-M1907" in notes)
    check("I9d honesty v dokazu", "uncertainReadings" in d.get("honesty", {}) and len(d["honesty"]["uncertainReadings"]) >= 40, str(len(d.get("honesty", {}).get("uncertainReadings", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P136 bullet", "po P136" in rd)
    check("I10b README 642/125", "642" in rd and "125" in rd)
    check("I10c README P137 lead", "P137" in rd)

    # ---------- I11: P135 dokaz nespremenjen (lekcija P9) ----------
    d135 = json.load(open(DOKAZ_P135))
    check("I11 P135 dokaz 12 vpisov", len(d135["entries"]) == 12, str(len(d135["entries"])))

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
