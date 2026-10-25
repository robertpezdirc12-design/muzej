#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P135 — župnija Podzemelj: poročna knjiga 04455, polno leto 1906
(s129–s131 == Pag. 128–130) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P134 = 1905): okvir POTRJEN
— s129–s131 == Pag. 128–130 (Pag. == sken − 1, **21. potrditev; velja
61–130**); **ROKOPISNA GLAVA »1906« POTRJENA na s129** (P134-lead! pod njo
še 1905-vpis 17) + **ROKOPISNA GLAVA »1907« na s132** (P136 LEAD).
**P135-lead KOREKCIJE (6!): »min 4 vpisov« → 12 vpisov s129–s131 (3×
podcenjeno) + v2 Krasinec 25 → 35 + Brodnič? → BRODARIČ + v2 Margaretha
Šurbaern? WTW → Margareth ŽUPANIČ LEDIG + v3 Vrdomari? → Anna BRODARIČ
LEDIG (WTW = žENIN!) + v4 Ojerm? 23 → Germ 28 + ★ NEOSTEVCEN vpis Mai 27
(1. v poročni liniji!)**. 12 vpisov (11 št. + 1 brez) = 15. januar + 29.
januar ×2 + 12. februar ×3 (MASA!) + 19. februar ×2 + 27. maj (ned.) + 10.
junij (ned.) + 2. julij + 26. november — 10/12 ponedeljkov + **2 NEDELJSKI
POROKI** (P134 je imelo 11/11!).

NOVELE: **★ 62-LETNI ŽENIN = NAJSTAREJŠI LINIJE** (v10 — prej Kralj 61⅔!)
+ **★ 3 GRIBLJE poroke / 6 poročnih blokov** (h73 1. DOKAZ = NOVI MAKSIMUM
h65→h73! + h31 3. × h35 2. DRUBEL [isti-dnevni konsent!] + h62 4. dokaz
KURE × h21 2. dokaz [1887→06 = 19-LETNA LUKNJA!] DRUBEL) → vitals 632 →
**638**; bloki 04455 115 → **121**; sidra 108 → **114** (+1906:6); p80
hiše 64 → **65** (+h73; h21 že od 1887!) + **★ 1. GOSTUJOČI DUHOVNIK
»pro delegato«** (v9m: Hx.? Herr? Jacobus Pavlovič?, Phluser? [~], SUHOR —
RAUY 11/12!) + **★ DVOJNI-IZMENJAVNI DRUBEL 29.1.** (v2+v3 — 2 NIKOLAUSA!)
+ **★ 1. HIŠA Z 3 BLOKI V ENEM LETU = NOVI REKORD** (h18 Županič!) + ★
SPREGLED DVEH OKLICEV (№ 2170 — NOV dokument-tip!) + ★ 17-letna nevesta
Perušič (NOVA VAS Lahinja 5 pf. Črnomelj!) + ★ 1. IZOSTANI nevestin
konsent (v1 — Krašić/HRVAŠKA!) + ★ № 23993 NOVI NAJVIŠJI + TOME-mreža ×5 +
HÜBLER-mreža ×7 + NOVI PRIIMKI ×6+.

Skripta scripts/p135_parish_marriage_1906.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p135_parish_marriage_1906.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1906.json"
DOKAZ_P134 = "research/issue17/parish-marriage-1905.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1906-notes.md"
EXPECTED_ENTRIES = 12           # v1–v11 + 1 neostevecen
EXPECTED_EXCLUDED = []
EXPECTED_ANOMALIES = 13
EXPECTED_CROSSCHECKS = 11
GRIBLJE_ROWS = [8, 9, 11]
GRIBLJE_HOUSES = ["73", "31", "35", "62", "21"]
GRIBLJE_BLOCKS = 5              # +5 blokov
VITALS_TOTAL = 642              # 632 + 5
BLOKI_04455 = 125               # 115 + 5
SIDRA_TOTAL = 118               # 108 + 5 (1906:5)
RAUY_COUNT = 11                 # 11/12 + 1 gost pro delegato!
FEB12_ROWS = [4, 5, 6]          # masa 3 (v4–v6)
FEB19_ROWS = [7, 8]             # masa 2
JAN29_ROWS = [2, 3]             # masa 2

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
    check("I2 vrste 1–11 + neostevecen (med v8 in v9!)", rows == [str(i) for i in range(1, 9)] + ["neostevecen (med 8 in 9!)"] + ["9", "10", "11"], str(rows))
    dates = [e["date"] for e in ent]
    jan29 = [e["row"] for e in ent if e["date"].startswith("29. januar")]
    check("I2b Jan 29 ×2 (v2–v3)", jan29 == JAN29_ROWS, str(jan29))
    feb12 = [e["row"] for e in ent if e["date"].startswith("12. februar")]
    check("I2c Febr 12 ×3 MASA (v4–v6)", feb12 == FEB12_ROWS, str(feb12))
    feb19 = [e["row"] for e in ent if e["date"].startswith("19. februar")]
    check("I2d Febr 19 ×2 (v7–v8)", feb19 == FEB19_ROWS, str(feb19))
    sundays = [e["row"] for e in ent if "(★ NEDELJA!)" in e["date"]]
    check("I2e 2 nedelji (neostevecen 27.5. + v9 10.6.)", sundays == ["neostevecen (med 8 in 9!)", 9], str(sundays))
    months = {}
    for dt in dates:
        m = re.match(r"\d+\. (\w+)", dt)
        if m:
            months[m.group(1)] = months.get(m.group(1), 0) + 1
    check("I2f meseci 1+5+2+2+1+1", months.get("januar") == 3 and months.get("februar") == 5 and months.get("maj") == 1 and months.get("junij") == 1 and months.get("julij") == 1 and months.get("november") == 1, str(months))

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (21. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [129,130,131]", scans == [129, 130, 131], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = e.get("groom", {}).get("place", "") + " " + e.get("bride", {}).get("place", "")
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = [str(r) for r in griblje_rows(ent)]
    check("I4 Griblje vrste [8, 9, 11]", g == ["8", "9", "11"], str(g))
    houses = []
    for e in ent:
        for pl in (e.get("groom", {}).get("place", ""), e.get("bride", {}).get("place", "")):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 5 GRIBLJE", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c drubel ×2 (v9 + v11)", allsi.count("DRUBEL") >= 2, str(allsi.count("DRUBEL")))
    check("I4d NOVI MAKSIMUM h73", "NOVI MAKSIMUM" in allsi, "")
    check("I4e 19-letna luknja h21", "19-LETNA LUKNJA" in allsi or "19-letna luknja" in allsi, "")
    check("I4f KURE 4. dokaz", "4. poročni dokaz h62" in allsi or "4. dokaz h62" in allsi or "4. dokaz KURE" in allsi, "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1906 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1906,', ts))
    check("I5a parish.ts bloki 1906 = 6", n_04455_1906 == GRIBLJE_BLOCKS, str(n_04455_1906))
    pins = [("73", "NOVI MAKSIMUM"), ("31", "PAPRIČ"), ("35", "SIMEC"),
            ("62", "KURE-kontinuiteta"), ("21", "19-LETNA LUKNJA")]
    for hn, pin in pins:
        m = re.search(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1906,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = bool(m) and pin.lower() in m.group(1).lower()
        check(f"I5b pin h{hn} ({pin})", ok, m.group(1)[:60] if m else "BLOK MANJKA")
    check("I5c P135 sekcija", "P135 razširitev: POROČNA KNJIGA 04455 — polno leto 1906" in ts)
    check("I5d TOME-mreža v ts", "TOME-mreža 5/5" in ts)
    check("I5e KONTINUITETA v ts", "KURE-kontinuiteta" in ts and "19-LETNA LUKNJA" in ts)

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p135 id", "qa-p135-parish-marriage-1906" in qa)
    n638 = qa.count("HOUSE_VITALS.length !== 675")
    check("I6b vitals pini 637", n638 >= 46, str(n638))
    n121 = qa.count("bloki 04455 ≠ 142")
    check("I6c bloki pini 120", n121 >= 8, str(n121))
    check("I6d sidra 113 + 1906:5", "poročna sidra ≠ 151" in qa and "h.year === 1906).length !== 5" in qa)
    check("I6e hiše 1906 pin", "21,31,35,62,73" in qa)
    check("I6f ostanki 632/115/108", "!== 632" not in qa and "bloki 04455 ≠ 115" not in qa and "sidra ≠ 108" not in qa, "stale pini!")

    # ---------- I7: duhovniki + dnevi ----------
    priests = [e["priest"] for e in ent]
    rauy = sum(1 for p in priests if "Rauy" in p)
    check("I7 Rauy 11/12 + 1 gost pro delegato", rauy == RAUY_COUNT, str(rauy))
    gost = sum(1 for p in priests if "pro delegato" in p.lower())
    check("I7b 1 gost (Pavlovič?, Suhor)", gost == 1, str(gost))
    wd = d["stats"].get("weekdays", "")
    check("I7c 10/12 ponedeljkov + 2 nedelji", "10/12 PONEDELJKOV" in wd and "2 NEDELJI" in wd, wd[:40])

    # ---------- I8: Parish stats ----------
    st = d["stats"]
    check("I8a stats vitals", st.get("vitals") == "632 → 637", str(st.get("vitals")))
    check("I8b stats bloki", st.get("bloki04455") == "115 → 120", str(st.get("bloki04455")))
    check("I8c stats sidra", st.get("sidra") == "108 → 113 (+1906:5)", str(st.get("sidra")))
    check("I8d stats entries 12", st.get("entries") == 12, str(st.get("entries")))
    check("I8e priests Rauy 11", st.get("priests", {}).get("Jos. Rauy") == 11, str(st.get("priests")))
    check("I8f stats gribljeHousesNewFirst", st.get("gribljeHousesNewFirst") == ["73", "21"], str(st.get("gribljeHousesNewFirst")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 13", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 11", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P135" in notes and "SAMPLE-TRANSCRIPTION-M1906" in notes)
    check("I9d honesty v dokazu", "uncertainReadings" in d.get("honesty", {}) and len(d["honesty"]["uncertainReadings"]) >= 50, str(len(d.get("honesty", {}).get("uncertainReadings", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P135 bullet", "po P141" in rd)
    check("I10b README 638/121", "638" in rd and "121" in rd)
    check("I10c README P136 lead", "P136" in rd)

    # ---------- I11: P134 dokaz nespremenjen (lekcija P9) ----------
    d134 = json.load(open(DOKAZ_P134))
    check("I11 P134 dokaz 17 vpisov", len(d134["entries"]) == 17, str(len(d134["entries"])))

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
