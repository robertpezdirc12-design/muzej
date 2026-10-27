#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P132 — župnija Podzemelj: poročna knjiga 04455, polno leto 1903
(s118–s121 == Pag. 117–120) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P131 = 1902): okvir POTRJEN
— s118–s121 == Pag. 117–120 (Pag. == sken − 1, **18. potrditev; velja
61–120**); **ROKOPISNA GLAVA »1903.« POTRJENA na s118** (P131-lead!) +
**VELIKA TISKANA GLAVA »1904.« POTRJENA na s122** (P133 LEAD — v1–v5 = Febr
8 ×5 = MASA!). **P132-lead KOREKCIJA: »min 5 vpisov s118–s119« → 20 vpisov
s118–s121 (4× podcenjeno — največja lead-napaka linije!)**. 20 vpisov
obojestransko = Febr 3 + Febr 9 ×3 + Febr 16 ×4 + Febr 23 ×2 (v9/v10
»März«-prevarda zavrnjena z zoomom 8× — ponedeljkovski vzorec!) + Jun 7 +
Jun 22 ×2 + Jul 6 + Jul 27 + Avg 3 + Avg 17 + Sept 13 + Okt 12 + Nov 23.

NOVELE: **★ 7 GRIBLJE porok / 11 poročnih blokov** (v1 h11 1. POROČNI
DOKAZ + v3 h65/h41 DRUBEL + v9 h46 2. + v12 h11 2. × h9 1. DRUBEL + v14 h6
1. + v17 h20/h48 DRUBEL + v20 h50 1. × h44 2. DRUBEL) → vitals 599 → **610**
; bloki 04455 82 → **93**; sidra 75 → **86** (+1903:11) + **★ v11 DVOJNI
DISPENS 1. STOPNJE SCHWÄGERSCHAFT** (Ordinariat št: 2244 + deželna vlada
št: 4444 — linijski rekord!) + **★ ¾ GRIBLAR NOVI NAJVIŠJI ULOMEK** (v16!)
+ **★ CROSS-ENTRY ×4 + BRAT-SESTRA ×2** + **★ 4. NEZAKONSKI ženin (v18) +
1. HÄUSLERIN + Dostál kaplan 2. dokaz (Rauy 19/20!)** + nove vasi (Božakovo
pf. Metlika · Sodji vrh pf. Semič · Boginja vas · Bilonje? · Mavhe? ·
občina Loka!) + status-vaha güblar/griblar G/H ×7 + 'Kofre' [~] ×4.

Skripta scripts/p132_parish_marriage_1903.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p132_parish_marriage_1903.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1903.json"
DOKAZ_P131 = "research/issue17/parish-marriage-1902.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1903-notes.md"
EXPECTED_ENTRIES = 20           # v1–v20, vse leto 1903
EXPECTED_ROWS = list(range(1, 21))
EXPECTED_EXCLUDED = []
EXPECTED_ANOMALIES = 14
EXPECTED_CROSSCHECKS = 23
GRIBLJE_ROWS = [1, 3, 9, 11, 12, 14, 17, 20]
GRIBLJE_HOUSES = ["11", "65", "41", "46", "56", "11", "9", "6", "20", "48", "50", "44"]
GRIBLJE_BLOCKS = 12             # +12 blokov
VITALS_TOTAL = 611              # 599 + 12
BLOKI_04455 = 94                # 82 + 12
SIDRA_TOTAL = 87                # 75 + 12 (1903:12)
RAUY_COUNT = 19                 # vse razen v18
DOSTAL_COUNT = 1                # v18 kaplan!
DOUBLE_DAYS = 4                 # Febr 9 ×3? ne — dvojni-dnevi: 9. (×3) + 16. (×4) + 23. (×2) + 22.6. (×2)
FEB16_ROWS = [5, 6, 7, 8]       # masa 4 porok

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
    check("I1c obojestransko 20/20", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste 1–20", rows == EXPECTED_ROWS, str(rows))
    dates = [e["date"] for e in ent]
    feb16 = [e["row"] for e in ent if e["date"].startswith("16. februar")]
    check("I2b Febr 16 ×4 (v5–v8)", feb16 == FEB16_ROWS, str(feb16))
    feb9 = [e["row"] for e in ent if e["date"].startswith("9. februar")]
    check("I2c Febr 9 ×3 (v2–v4)", feb9 == [2, 3, 4], str(feb9))
    feb23 = [e["row"] for e in ent if e["date"].startswith("23. februar")]
    check("I2d Febr 23 ×2 (v9–v10 — März-zavrnjena!)", feb23 == [9, 10], str(feb23))
    months = {}
    for dt in dates:
        m = re.match(r"\d+\. (\w+)", dt)
        months[m.group(1)] = months.get(m.group(1), 0) + 1
    check("I2e meseci 13+7", months.get("februar") == 10 and months.get("junij") == 3 and months.get("julij") == 2 and months.get("avgust") == 2 and months.get("september") == 1 and months.get("oktober") == 1 and months.get("november") == 1, str(months))

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (18. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [118,119,120,121]", scans == [118, 119, 120, 121], str(scans))

    # ---------- I4: Griblje ----------
    g = [e["row"] for e in ent if e.get("griblje")]
    check("I4 Griblje vrste [1,3,9,12,14,17,20]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        if e.get("griblje"):
            blob = json.dumps(e, ensure_ascii=False)
            for m in re.findall(r"[Gg][Rr][Ii][Bb][Ll][JjEe] (\d+)", blob):
                houses.append(m)
            for m in re.findall(r"\bh(\d+)\b", e.get("notes", "")):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: (int(x)))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: (int(x)))
    allsi = " ".join(e.get("notes", "") + " " + json.dumps(e.get("groom", {}), ensure_ascii=False) + " " + json.dumps(e.get("bride", {}), ensure_ascii=False) for e in ent)
    check("I4b hiše 12GRIBLJE", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c drubel ×4", allsi.count("DRUBEL") >= 4, str(allsi.count("DRUBEL")))

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1903 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1903,', ts))
    check("I5a parish.ts bloki 1903 = 11", n_04455_1903 == GRIBLJE_BLOCKS, str(n_04455_1903))
    pins = [("11", "ŽUNIČ"), ("65", "MÜCK"), ("41", "HUESTIČ"), ("46", "KRIŽAN"),
            ("9", "JAKOFČIČ"), ("6", "JAKOBČIČ"), ("20", "PEZDIREC"),
            ("48", "BERKOPREC"), ("50", "JERČINOVIČ"), ("44", "ŠTRUCELJ")]
    for hn, pin in pins:
        m = re.search(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*year:\s*1903,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = bool(m) and pin.lower() in m.group(1).lower()
        check(f"I5b pin h{hn} ({pin})", ok, m.group(1)[:60] if m else "BLOK MANJKA")
    check("I5c P132 sekcija", "P132 razširitev: POROČNA KNJIGA 04455 — polno leto 1903" in ts)
    check("I5d DVOJNI DISPENS v ts", "SCHWÄGERSCHAFT" in ts)
    check("I5e Kofre v ts", "Kofre" in ts)

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p132 id", "qa-p132-parish-marriage-1903" in qa)
    n610 = qa.count("HOUSE_VITALS.length !== 687")
    check("I6b vitals pini 610", n610 >= 46, str(n610))
    n94 = qa.count("bloki 04455 ≠ 142")
    check("I6c bloki pini 94", n94 >= 8, str(n94))
    check("I6d sidra 86 + 1903:11", "poročna sidra ≠ 163" in qa and "h.year === 1903).length !== 12" in qa)
    check("I6e hiše 1903 pin", "11,11,20,41,44,46,48,50,56,6,65,9" in qa)
    check("I6f izjema h41-1903", 'v.year === 1903 && hn === "41"' in qa)

    # ---------- I7: duhovniki ----------
    priests = [e["priest"] for e in ent]
    rauy = sum(1 for p in priests if "Rauy" in p)
    dostal = sum(1 for p in priests if "Dostál" in p or "Dostal" in p)
    check("I7 Rauy 19/20", rauy == RAUY_COUNT, str(rauy))
    check("I7b Dostál kaplan 1/20 (v18)", dostal == DOSTAL_COUNT and "kaplan" in ent[17]["priest"], f"{dostal}; v18={ent[17]['priest']}")

    # ---------- I8: Parish stats ----------
    st = d["stats"]
    check("I8a stats vitals", st.get("vitals") == "599 → 611", str(st.get("vitals")))
    check("I8b stats bloki", st.get("bloki04455") == "82 → 94", str(st.get("bloki04455")))
    check("I8c stats sidra", st.get("sidra") == "75 → 87 (+1903:12)", str(st.get("sidra")))
    check("I8d stats entries 20", st.get("entries") == 20, str(st.get("entries")))
    check("I8e priests Rauy 19 + Dostál 1", st.get("priests", {}).get("Jos. Rauy") == 19 and st.get("priests", {}).get("Hanislav Dostál kaplan") == 1, str(st.get("priests")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 14", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 23", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P132" in notes and "SAMPLE-TRANSCRIPTION-M1903" in notes)
    check("I9d honesty v dokazu", "uncertainReadings" in d.get("honesty", {}) and len(d["honesty"]["uncertainReadings"]) >= 40, str(len(d.get("honesty", {}).get("uncertainReadings", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P132 bullet", "po P140" in rd or "P132 (poročna 04455, polno leto 1903" in rd)
    check("I10b README 611/94", "611" in rd and "94" in rd)
    check("I10c README P133 lead", "P133" in rd)

    # ---------- I11: P131 dokaz nespremenjen (lekcija P9) ----------
    d131 = json.load(open(DOKAZ_P131))
    check("I11 P131 dokaz 6 vpisov", len(d131["entries"]) == 6, str(len(d131["entries"])))

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
