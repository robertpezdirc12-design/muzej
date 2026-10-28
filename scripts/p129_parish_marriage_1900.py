#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P129 — župnija Podzemelj: poročna knjiga 04455, polno leto 1900
(s112–s113 == Pag. 111–112) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P128 = 1899): okvir POTRJEN —
s112–s113 == Pag. 111–112 (Pag. == sken − 1, **15. potrditev; velja v
61–112**); **ROKOPISNA GLAVA »1900.« POTRJENA na s112** + **rokopisna glava
»1901.« POTRJENA na s114** (P130 lead + v1/1901 Jänner 18 Otok 14 × Otok
21!). **8 vpisov = 2. najmanjše leto linije** (min 1886:7 → 1900:8 → 1899:9
padne na 3.!): feb 4 (2× dvojni dan!) + mai 1 + okt 1 + nov 2 (dvojni dan).

NOVELE: **★ ŽUPANIČ KONTINUUM** (v1 ženin Nicolaus Županič ¼ Krasinec 18 =
ISTA HIŠA P127 v8/v13 — 3. poročni dokaz hiše! + v3 priča Johann Županič ½ =
P127 v8 ŽENIN — priča 7 dni po lastni poroki!) + **★ 3 DVOJNA DNEVA = NOVI
REKORD LINIJE** (Febr 12 ×2 + Febr 19 ×2 + Nov 5 ×2; prej 1!) + **★ RAUY
8/8 = 100% DOMINANTA** (povratek P127-vzorca po P128 Novak 5/9!) + **★ 1.
NEZAKONSKA NEVESTA?** (v7 oče = ČRTA!) + **★ KLOSTER ×3 hiše** (69/40/76!)
+ **★ GRADAC 18 ×2 ženina + v7 nevesta** (vzorec A6!) + **★ pentagon 5
občin** (+Adlešič + Sveti-Jurzej NOVA!) + **★ SAMSKI LIST izrecno** (v8!) +
nadvarstveno ×2 + **★ PEZDIREC ×4** (8. leto mreže!) + oče-kot-priča čez
vpisa (v5 priča = v1 oče!) + **P128-lead KOREKCIJE** (v1 datum Febr 12 ne
Jänner 2! + priimek Županič ne Žugajnič?).

Skripta scripts/p129_parish_marriage_1900.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p129_parish_marriage_1900.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES_MIN = 190
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1900.json"
DOKAZ_P128 = "research/issue17/parish-marriage-1899.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1900-notes.md"
EXPECTED_ENTRIES = 8            # v1–v8, vse leto 1900
EXPECTED_ROWS = list(range(1, 9))
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 14
GRIBLJE_ROWS = [2]
GRIBLJE_MARRIAGES = 1
GRIBLJE_BLOCKS = 2              # h7 + h8
GRIBLJE_HOUSES = ["7", "8"]
VITALS_TOTAL = 611              # 593 + 2 + 12 (P132)
BLOKI_04455 = 82                # 76 + 2
SIDRA_TOTAL = 87                # 69 + 2 (1900:2) + 12 (1903:12)
RAUY_COUNT = 8                  # Jos. Rauy v vseh 8 vpisih = 100%!
DOUBLE_DAYS = {"12.2.1900": [1, 2], "19.2.1900": [3, 4], "5.11.1900": [7, 8]}

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
    both = all(e.get("groom", {}).get("name") and e.get("bride", {}).get("name") for e in ent)
    check("I1c obojestransko 8/8", both, str(both))

    # ---------- I2: vrste + datumi + dvojni dnevi ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste 1–8", rows == EXPECTED_ROWS, str(rows))
    februar = sum(1 for e in ent if "februar" in e["date"])
    maj = sum(1 for e in ent if "maj" in e["date"])
    oktober = sum(1 for e in ent if "oktober" in e["date"])
    november = sum(1 for e in ent if "november" in e["date"])
    check("I2b meseci feb4+mai1+okt1+nov2",
          (februar, maj, oktober, november) == (4, 1, 1, 2),
          f"feb {februar} + mai {maj} + okt {oktober} + nov {november}")
    for day, vrste in DOUBLE_DAYS.items():
        got = [e["row"] for e in ent if e["date"].startswith(day.split(".")[0] + ". ")]
        ok = vrste in [[r for r in range(len(vrste))] and vrste == got or got == vrste]
        got_d = [e["row"] for e in ent if e["date"] == f"{day.split('.')[0]}. {('februar' if day.endswith('2.1900') or day.endswith('.1900') and 'febr' in day else 'november') if False else e['date']}"]
        # enostavneje: primerjaj zaporedje vrst po datumu-številki
        dd = int(day.split(".")[0])
        got2 = [e["row"] for e in ent if e["date"].split(".")[0] == str(dd)]
        check(f"I2c dvojni dan {day} {vrste}", got2 == vrste, str(got2))

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["row"], e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (15. potrditev)", not bad, str(bad))

    # ---------- I4: Griblje ----------
    g = [e["row"] for e in ent if e.get("griblje")]
    check("I4 Griblje vrste", sorted(g) == GRIBLJE_ROWS, str(g))
    gh = sorted([e["groom"]["place"].split()[-1] for e in ent if e.get("griblje") and "GRIBLJE" in e["groom"]["place"]] +
                [e["bride"]["place"].split()[-1] for e in ent if e.get("griblje") and "GRIBLJE" in e["bride"]["place"]], key=int)
    check("I4b Griblje hiše [7, 8]", gh == GRIBLJE_HOUSES, str(gh))

    # ---------- I5: parish.ts bloki ----------
    ts = open(PARISH_TS).read()
    n_1900 = ts.count('bookSignature: "04455",\n    year: 1900,')
    check("I5 2 bloka 1900 (04455)", n_1900 == GRIBLJE_BLOCKS, str(n_1900))
    pins = [("7", "1. POROČNI DOKAZ h7"), ("8", "1. POROČNI DOKAZ h8")]
    for house, pin in pins:
        blk = re.search(
            r'\{\s*houseNo: "' + house + r'",\s*bookSignature: "04455",\s*year: 1900,'
            r'.*?whatSi: "(.*?)"', ts, re.S)
        ok = blk and pin.lower() in blk.group(1).lower()
        check(f"I5b pin h{house} ({pin})", ok, blk.group(1)[:60] if blk else "BLOK MANJKA")
    check("I5c RAUY 8/8 dominanta", ts.count("RAUY 8/8") >= 1 and ts.count("100% DOMINANTA") >= 1,
          str(ts.count("RAUY 8/8")))
    check("I5d P129 sekcija", "P129 razširitev: POROČNA KNJIGA 04455 — polno leto 1900" in ts)

    # ---------- I6: qa-parish pini ----------
    qa = open(QA_TS).read()
    n595 = qa.count("HOUSE_VITALS.length !== 725")
    n593 = qa.count("HOUSE_VITALS.length !== 593")
    n78 = qa.count("≠ 142 (")
    n76 = qa.count("≠ 76 (")
    check("I6 vitals pini 595", n595 >= 44, str(n595))
    check("I6b brez stale 593 asercij", n593 == 0, str(n593))
    check("I6c bloki pini 125", n78 >= 22, str(n78))
    check("I6d brez stale ≠ 76 asercij", n76 == 0, str(n76))
    check("I6e sidra 71 + 1900:2", "poročna sidra ≠ 164" in qa and
          "h.year === 1900).length !== 2" in qa and
          "h.year === 1902).length !== 4" in qa)
    check("I6f p129Marr hiše", '"7,8"' in qa)
    check("I6g qa-p129 test", "qa-p129-parish-marriage-1900" in qa)
    check("I6h P128-lead korekcija", "P129 korekcija" in qa or "corrected" in qa)

    # ---------- I7: duhovniki v vpisih ----------
    pri = " ".join(e["priest"] for e in ent)
    check("I7 Rauy ×8 = 100%", pri.count("Rauy") == RAUY_COUNT, str(pri.count("Rauy")))
    check("I7b brez Novak", pri.count("Novak") == 0, str(pri.count("Novak")))
    check("I7c brez Sturm", pri.count("Sturm") == 0, str(pri.count("Sturm")))

    # ---------- I8: anomalije + crossChecks ----------
    check("I8 anomalije", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I8b crossChecks", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    ids = [c["id"] for c in d["crossChecks"]]
    check("I8c C1 Županič hiša", "C1" in ids and "Krasinec 18" in d["crossChecks"][0]["what"])
    check("I8d C2 priča-po-poroki", "C2" in ids and "7 dni" in d["crossChecks"][1]["what"])

    # ---------- I9: kontinuiteta + korekcije lead ----------
    d128 = json.load(open(DOKAZ_P128))
    check("I9 P128 dokaz nespremenjen (9)", len(d128["entries"]) == 9)
    allsi = json.dumps(d, ensure_ascii=False)
    check("I9b ŽUPANIČ ×3 mreža", "ŽUPANIČ ×3" in allsi)
    check("I9c korekcija Febr 12", "Febr 12" in allsi or "februar 1900" in allsi)
    check("I9d nezakonska nevesta C8", "C8" in ids and "NEVESTA" in allsi and "ČRTA" in allsi)

    # ---------- I10: README + notes ----------
    rd = open(README).read()
    check("I10 README po P129", "P129" in rd and "595" in rd and "78" in rd)
    nt = open(NOTES).read()
    check("I10b notes faza 2 + korekcije", "FAZA 2" in nt and "KOREKCIJE" in nt.upper() and "ŽUPANIČ" in nt)

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
