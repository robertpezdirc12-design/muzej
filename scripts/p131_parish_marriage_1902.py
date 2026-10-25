#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P131 — župnija Podzemelj: poročna knjiga 04455, polno leto 1902
(s116–s117 == Pag. 115–116) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P130 = 1901): okvir POTRJEN —
s116–s117 == Pag. 115–116 (Pag. == sken − 1, **17. potrditev; velja v
61–116**); **ROKOPISNA GLAVA »1902.« POTRJENA na s116** (že P130-lead!) +
**glava »1903.« POTRJENA na s118** (P132 lead — r1 = 1903 Febr 3 Dragatuš? 1
× GRIBLJE 11 Agnes Žunjič? [~] = 3. GRIBLJE poroka v vrsti!). **6 vpisov =
NAJMANJŠE LETO POROČNE LINIJE 1886–1902** (prej min 1900:8 po skupnih
vpisih / 1886:7 po okvirni konvenciji — NOVI MINIMUM V OBEH MERAH!): jan 27
×3 TRIPLO + mai 12 + mai 26 + sept 15.

NOVELE: **★ 2 GRIBLJE poroki / 4 poročna bloka** (v2 h5 1. POROČNI DOKAZ ×
h31 1. POROČNI DOKAZ = DRUBEL + v4 h30 3. dokaz × h24 2. dokaz = DRUBEL!)
→ vitals 595 → **599**; bloki 04455 78 → **82**; sidra 71 → **75** + **★ 1.
Hanislav DOSTÁL kaplan** (v5 — 1. nov duhovnik od P128-Sturm; Rauy 5/6!) +
**★ 1. IZRECNA nezakonska-opomba** (v6 oče = črta + »lediga? Ehe.« [~]) +
**★ Bukoraj? pf. Črnomelj NOVA VAS? + očina PLANINA št: 10** + **★ priče
činovniki** (vojak + k.k. Bahndienst!) + **★ ženitovanjska zglašnica =
REŠITEV SERIJSKE FORMULE** (prej »Porifovanjška/žerifovanjška« [~] P128–P130
→ Trauungs-Anzeige!) + **★ ŠTRUPEC NOVI ×3 + LEGINA NOVI ×3 + KOCJAN NOVI**
+ Pezdirec ×3 (7. leto!) + Dragoš (10.+ leto!) + P131-lead KOREKCIJE
([G]pbyke?→GRIBLJE 5 + v6 Sept 15!).

Skripta scripts/p131_parish_marriage_1902.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p131_parish_marriage_1902.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1902.json"
DOKAZ_P130 = "research/issue17/parish-marriage-1901.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1902-notes.md"
EXPECTED_ENTRIES = 6            # v1–v6, vse leto 1902
EXPECTED_ROWS = list(range(1, 7))
EXPECTED_EXCLUDED = []
EXPECTED_ANOMALIES = 7
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [2, 4]           # v2 (h5×h31) + v4 (h30×h24)
GRIBLJE_HOUSES = ["5", "31", "30", "24"]
GRIBLJE_BLOCKS = 4              # +4 bloki
VITALS_TOTAL = 611              # 595 + 4 (1902) + 12 blokov 1903 (P132)
BLOKI_04455 = 82                # 78 + 4
SIDRA_TOTAL = 87                # 71 + 4 (1902:4) + 12 (1903:12)
RAUY_COUNT = 5                  # v1–v4 + v6
DOSTAL_COUNT = 1                # v5 kaplan!
TRIPLE_DAY = "27. januar 1902"  # v1–v3
TRIPLE_ROWS = [1, 2, 3]

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
    both = all(
        e.get("groom", {}).get("name") and e.get("bride", {}).get("name")
        for e in ent
    )
    check("I1c obojestransko 6/6", both, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste 1–6", rows == EXPECTED_ROWS, str(rows))
    dates = [e["date"] for e in ent]
    triple = sum(1 for x in dates if x == TRIPLE_DAY)
    check("I2b TRIPLO 27.1. ×3", triple == 3, str(triple))
    got_triple = [e["row"] for e in ent if e["date"] == TRIPLE_DAY]
    check("I2c triplo vrste 1–3", got_triple == TRIPLE_ROWS, str(got_triple))
    check("I2d datumi set", sorted(set(d for d in dates if d != TRIPLE_DAY)) == ["12. maj 1902", "15. september 1902", "26. maj 1902"], str(sorted(set(dates))))
    jan = sum(1 for x in dates if "januar" in x)
    maj = sum(1 for x in dates if "maj" in x)
    sept = sum(1 for x in dates if "september" in x)
    check("I2e jan3+maj2+sept1", (jan, maj, sept) == (3, 2, 1), f"{jan}/{maj}/{sept}")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (17. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [116,117]", scans == [116, 117], str(scans))

    # ---------- I4: Griblje ----------
    g = [e["row"] for e in ent if e.get("griblje")]
    check("I4 Griblje vrste [2,4]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        if e.get("griblje"):
            houses += [e.get("houseNoGroom", ""), e.get("houseNoBride", "")]
    check("I4b hiše [5,31,30,24]", sorted(houses) == sorted(GRIBLJE_HOUSES), str(houses))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4c drubel ×2", allsi.count("DRUBEL") >= 2, str(allsi.count("DRUBEL")))

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1902 = len(re.findall(r'houseNo:\s*"(\d+)",\s*bookSignature:\s*"04455",\s*year:\s*1902', ts))
    check("I5a parish.ts bloki 1902 = 4", n_04455_1902 == GRIBLJE_BLOCKS, str(n_04455_1902))
    for hn, pin in [("5", "ŠTRUPEC"), ("31", "MULH"), ("30", "LEGINA"), ("24", "BRIŠEC")]:
        m = re.search(r'houseNo:\s*"' + hn + r'",\s*bookSignature:\s*"04455",\s*year:\s*1902.*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)
        ok = bool(m) and pin.lower() in m.group(1).lower()
        check(f"I5b pin h{hn} ({pin})", ok, m.group(1)[:60] if m else "BLOK MANJKA")
    check("I5c P131 sekcija", "P131 razširitev: POROČNA KNJIGA 04455 — polno leto 1902" in ts)
    check("I5d DOSTÁL v ts", "DOSTÁL" in ts)
    check("I5e ženitovanjska v ts", "ženitovanjska" in ts)

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p131 test", "qa-p131-parish-marriage-1902" in qa)
    n599 = qa.count("HOUSE_VITALS.length !== 675")
    n595 = qa.count("HOUSE_VITALS.length !== 595")
    check("I6b vitals pini 610", n599 >= 46, str(n599))
    check("I6c brez stale 595 asercij", n595 == 0, str(n595))
    n82 = qa.count("≠ 142 (")
    n78 = qa.count("≠ 78 (")
    check("I6d bloki pini 125", n82 >= 22, str(n82))
    check("I6e brez stale ≠ 78 asercij", n78 == 0, str(n78))
    check("I6f sidra 75 + 1902:4", "poročna sidra ≠ 151" in qa and "h.year === 1902).length !== 4" in qa and "h.year === 1903).length !== 12" in qa)
    check("I6g p131Marr hiše", '"24,30,31,5"' in qa or '"5,24,30,31"' in qa)
    check("I6h P131-lead korekcija v qa-p130", "P131 korekcija" in qa)

    # ---------- I7: duhovniki ----------
    rauy = sum(1 for e in ent if "Rauy" in e.get("priest", ""))
    dostal = sum(1 for e in ent if "Dostál" in e.get("priest", ""))
    check("I7 Rauy ×5", rauy == RAUY_COUNT, f"{rauy}/{RAUY_COUNT}")
    check("I7b Dostál ×1 (kaplan!)", dostal == DOSTAL_COUNT, str(dostal))

    # ---------- I8: anomalije + crossChecks ----------
    check("I8 anomalije", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I8b crossChecks", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    ids = [c["id"] for c in d["crossChecks"]]
    check("I8c C16 P132 lead", "C16" in ids and "1903" in d["crossChecks"][15]["what"])
    check("I8d C13 ženitovanjska", "C13" in ids and "Trauungs-Anzeige" in d["crossChecks"][12]["what"])

    # ---------- I9: kontinuiteta ----------
    d130 = json.load(open(DOKAZ_P130))
    check("I9 P130 dokaz nespremenjen (11)", len(d130["entries"]) == 11)
    check("I9b lead korekcije", "GRIBLJE 5" in allsi and "Sept 15" in allsi)
    check("I9c Dostál + lediga", "Dostál" in allsi and "lediga" in allsi)
    check("I9d P132 lead v dokazu", "GRIBLJE 11" in allsi and "Žunjič" in allsi)

    # ---------- I10: README + notes ----------
    rd = open(README).read()
    check("I10 README po P131", "P131" in rd)
    check("I10b README 611/94", "611" in rd and "94" in rd)
    nt = open(NOTES).read()
    check("I10c notes faze + rekonstrukcija", "FAZA 0" in nt and "FAZA 2" in nt and "REKONSTRUKCIJA" in nt.upper())
    check("I10d notes drubel + dostál", "DRUBEL" in nt.upper() and "Dostál" in nt)

    # ---------- live ----------
    if live:
        st_, body = http_get(BOOK_URL)
        check("I11 live knjiga 200", st_ == 200, str(st_))

    # ---------- izpis ----------
    passed = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        line = f"[{mark}] {name}"
        if detail:
            line += f" — {detail[:110]}"
        print(line)
    print(f"\n{passed}/{len(results)} PASS")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
