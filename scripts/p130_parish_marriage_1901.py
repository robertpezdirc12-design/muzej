#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P130 — župnija Podzemelj: poročna knjiga 04455, polno leto 1901
(s114–s116 == Pag. 113–115) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P129 = 1900): okvir POTRJEN —
s114–s116 == Pag. 113–115 (Pag. == sken − 1, **16. potrditev; velja v
61–115**); **ROKOPISNA GLAVA »1901.« POTRJENA na s114** + **rokopisna glava
»1902.« POTRJENA ŽE na s116** (P131 lead KOREKCIJA — P129-lead pričakoval
s117!). **11 vpisov = 4. najmanjše leto linije** (min 1886:7 → 1900:8 →
1899:9 → 1901:11): jan 1 + feb 2 + ★ **feb 11 ×6 MASA!** + jul 1 + nov 2.

NOVELE: **★ 6 POROK NA 11.2.** (v3–v8 = 2. največji dan linije — rekord
1893:7 6.2.!; 3× P129-rekord) + **★ RAUY 11/11 = 100%** (ABSOLUTNI rekord!
) + **★ 0 OMEMB GRIBLJE** (1. leto linije 1886–1901 brez Griblje — ASIMETRIJA
s krstno 1901 P96 = vsi Griblje!) + **★ ¾ griblar 2. dokaz** (v7 Ignac
Prevec + hči Engelbetha == P128 v7 Žugelj vzorec) + **★ 1. DISPENS
AFINOSTI** (v1 Anverwandtschaft № 138? [~]) + v8 consanguinitas 4. kolena
№ 236 + potestate delegata + **★ POLNOLETNOST ZA ŽENINA** (v4 21! + v11 OBA
) + **★ MUC ×3** (P128 v3 priča == v11 Weißstand!) + **★ Vranoviče 8** =
6. hiša + **★ 1. činovniki-priče** (c.k. poštni asistent + zagrebški
arhivar robno!) + **P130-lead KOREKCIJE ×4** (Jan 28 · Otok 34 · KRIŽAN ·
PALČIČ!) + P131-lead korekcija (s116!).

Skripta scripts/p130_parish_marriage_1901.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p130_parish_marriage_1901.py [--live]
"""
import json
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1901.json"
DOKAZ_P129 = "research/issue17/parish-marriage-1900.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1901-notes.md"
EXPECTED_ENTRIES = 11           # v1–v11, vse leto 1901
EXPECTED_ROWS = list(range(1, 12))
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 11
EXPECTED_CROSSCHECKS = 18
GRIBLJE_ROWS = []               # 1901: 0 omemb Griblje!
GRIBLJE_BLOCKS = 0              # 0 novih blokov (vitals 595 nespremenjen!)
VITALS_TOTAL = 595              # nespremenjen (P129)
BLOKI_04455 = 78                # nespremenjen (P129)
SIDRA_TOTAL = 71                # nespremenjen (0 Griblje sidra)
RAUY_COUNT = 11                 # Jos. Rauy v vseh 11 vpisih = 100%!
MASS_DAY = "11. februar 1901"  # 6 porok!
MASS_ROWS = [3, 4, 5, 6, 7, 8]

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
    check("I1b excluded 0", d.get("excluded") == [], str(d.get("excluded")))
    both = all(
        e.get("groom", {}).get("name") and e.get("bride", {}).get("name")
        for e in ent
    )
    check("I1c obojestransko 11/11", both, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste 1–11", rows == EXPECTED_ROWS, str(rows))
    dates = [e["date"] for e in ent]
    mass = sum(1 for x in dates if x == MASS_DAY)
    check("I2b MASA 11.2. ×6", mass == 6, str(mass))
    got_mass = [e["row"] for e in ent if e["date"] == MASS_DAY]
    check("I2c masa vrste 3–8", got_mass == MASS_ROWS, str(got_mass))
    feb = sum(1 for x in dates if "februar" in x)
    check("I2d februar ×7", feb == 7, str(feb))
    jul = sum(1 for x in dates if "julij" in x)
    nov = sum(1 for x in dates if "november" in x)
    jan = sum(1 for x in dates if "januar" in x)
    check("I2e jan1+jul1+nov2", (jan, jul, nov) == (1, 1, 2), f"{jan}/{jul}/{nov}")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [
        (e["scan"], e["page"])
        for e in ent
        if e["page"] != e["scan"] - 1
    ]
    check("I3 Pag == sken − 1 (16. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [114,115,116]", scans == [114, 115, 116], str(scans))

    # ---------- I4: Griblje 0 ----------
    g = [e["row"] for e in ent if e.get("griblje")]
    check("I4 Griblje vrste = 0 (1. leto!)", g == GRIBLJE_ROWS, str(g))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b ASIMETRIJA opomba", "ASIMETRIJA" in allsi and "P96" in allsi)

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_1901 = ts.count("year: 1901")
    check("I5a parish.ts year:1901 (samo P96 krstne!)", n_1901 >= 8, str(n_1901))
    n_04455_1901 = len([
        1 for i in range(len(ts))
        if ts.startswith("bookSignature: \"04455\"", i)
    ])
    check("I5b brez novih 04455 blokov 1901 (0!)", "P130" in ts, "P130 sekcija v parish.ts")
    check("I5c P130 lead korekcije v ts", "P130" in ts and ("Križan" in ts or "KRIZAN" in ts.upper()))
    n595 = ts.count("595")
    n78 = ts.count("78")

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p130 test", "qa-p130-parish-marriage-1901" in qa)
    check("I6b masa 11.2. v qa", "11" in qa and "6" in qa)
    check("I6c Rauy 11/11 v qa", "11/11" in qa)

    # ---------- I7: duhovnik ----------
    rauy = sum(1 for e in ent if "Rauy" in e.get("priest", ""))
    check("I7 RAUY 11/11 = 100% (rekord!)", rauy == RAUY_COUNT, f"{rauy}/{RAUY_COUNT}")

    # ---------- I8: anomalije + crossChecks ----------
    check("I8 anomalije", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I8b crossChecks", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    ids = [c["id"] for c in d["crossChecks"]]
    check("I8c C16 glava 1902 s116", "C16" in ids and "s116" in d["crossChecks"][15]["what"])
    check("I8d C5 ¾ v7", "C5" in ids and "P128 v7" in d["crossChecks"][4]["what"])

    # ---------- I9: kontinuiteta ----------
    d129 = json.load(open(DOKAZ_P129))
    check("I9 P129 dokaz nespremenjen (8)", len(d129["entries"]) == 8)
    check("I9b korekcije ×4", all(k in allsi for k in ["Jänner 28", "Otok 34", "KRIŽAN", "PALČIČ"]))
    check("I9c dispensi ×2", "Anverwantschaft" in allsi and "236" in allsi)

    # ---------- I10: README + notes ----------
    rd = open(README).read()
    check("I10 README po P130", "P130" in rd)
    nt = open(NOTES).read()
    check("I10b notes faza 2 + masa", "FAZA 2" in nt and "6 POROK" in nt.upper() and "REKONSTRUKCIJA" in nt.upper())

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
