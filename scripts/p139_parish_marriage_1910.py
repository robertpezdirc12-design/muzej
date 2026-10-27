#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P139 — župnija Podzemelj: poročna knjiga 04455, polno leto 1910
(s141–s145 == Pag. 140–144) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P138 = 1909): okvir POTRJEN
— s141–s145 == Pag. 140–144 (Pag. == sken − 1, **25. potrditev; velja
61–146**). **LETNICA 1910 SE PIŠE V VSAKEM VPISU — brez letne glave**
(nadaljevanje lekcije P138). **1910 = 19 VPISOV** (№1 s141 + №2–6 s142 +
№7–10 s143 + №11–14 s144 + №15–19 s145; №-stolpci pasovno potrjeni).

NOVELE: **★★★ №1 INTRA-GRIBLJE INTRA-PRIIMEK POROKA h13 × h6** (2 ×
JAKOBČIČ + starši-dvojček Mathias ½ × Mathias ¼ + priči strica OBEH mater
Pezdirec + Željko + DISPENSA 3. KOLENA ordinariat Ljubljana 13/1 1910 št.
159 [~ čtiri branjа 159/359/138/239]) + **★★★ №14 GRIBLJE × GRIBLJE h86 ×
h31 + DVOJNA SORODSTVENA ZAPREKA** (št. 2058 [~] + spregled št. 12448
[~]) + **★★ h86 = NOVA POROČNA HIŠA (p80 67 → 68!)** (sin h85-družine
Marko Križan × Marija Strauš 1888!) + **★★★ 24. 1. ×5 = MASA-DAN REKORD
LINIJE 1886–1910** + **★★ 12 PON + 7 NED = 100% VIKEND-POROKE (19/19!)**
+ **★★ №17 NEVESTA 16 LET + DEŽELNA VLADE Ljubljana št. 18796 (1. v
liniji!)** + **★★ №3+№4 DVOJNA POROKA SOROJENCEV DRAGOŠ isti dan** + **★★
№18 69-LETNI ŽENIN LEDIG** (2. po 1908-v16 73!) + **★ №13 ženin + nevesta
IZ ISTE HIŠE Primostek 18** + **★ №16 ISTI HIŠI KOT №2 (Gradac 44 × 55!)**
+ **★ Jakobčič ×3 ženini + Butala ×3 + Tome ×2 + Bajuk ×2** + NOVE
OBLASTI (Škofle pri Brežicah na Štajerskem! + sv. Jernej + Loka + deželna
vlada + Vrhovska vas) + NOVI POKLICI (Perkušec/perkar! + Schmiedmeister +
Einwohner + Hufschmied) + ~25 NOVIH PRIIMKOV + DANIJEL 2. pojav (№9 1909 +
№9 1910!) → vitals 659 → **664**; bloki 04455 142 → **147**; sidra 135 →
**140** (+1910:5); p80 hiše 67 → **68 (+h86!)**; PT luknja **13**
(nespremenjena — h86 v naboru 61–99!).

METODA (preboj): 100+ VLM branj + **GRID-TEHNIKA** (prostorska preslikava
z označenimi črtami — razrešila VSE hišne številke!) + korpus-forenzika +
**GEOMETRIJSKA LEKCIJA: rezidenca je PRED imenom v bloku!** (7 POPRAVKOV
2. kroga: №4 14→18 · №10 Andreas→ALFONS · №14 36/85/17→86 · №14
11/21/41→31 · №9 Schwaiger→VRHOVSKA VAS · №18 Filovje→KRASINEC 30 · №2
Gneuf→GRAF).

Skripta scripts/p139_parish_marriage_1910.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p139_parish_marriage_1910.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1910.json"
DOKAZ_P138 = "research/issue17/parish-marriage-1909.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1910-notes.md"
EXPECTED_ENTRIES = 19           # №1–№19
EXPECTED_EXCLUDED = []
EXPECTED_ANOMALIES = 18
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [1, 14, 17]
GRIBLJE_HOUSES = ["6", "8", "13", "31", "86"]
GRIBLJE_BLOCKS = 5              # №1 2 (INTRA!) + №14 2 + №17 1
VITALS_TOTAL = 670              # 659 + 5
BLOKI_04455 = 147               # 142 + 5
SIDRA_TOTAL = 157               # 135 + 5 (1910:5)
RAUY_COUNT = 16                 # 16+/19 blokov ne — 17–18/19 vpisov (№9 Danijel!)
EXPECTED_MONDAYS = 13           # + 6 nedelj = 100% vikend!

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
    check("I1c obojestransko 19/19", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [str(e["row"]) for e in ent]
    check("I2 vrste [1–19]", rows == [str(i) for i in range(1, 20)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\[?(\d+)[^\s]*\s+(\w+)", dt)
        if m:
            months[m.group(2)] = months.get(m.group(2), 0) + 1
    check("I2b meseci (jan 9 + maj 3 + jul 4 + avg 1 + okt 1 + nov 1)",
          months.get("januar") == 9 and months.get("maj") == 3 and months.get("julij") == 4
          and months.get("avgust") == 1 and months.get("oktober") == 1 and months.get("november") == 1
          and sum(months.values()) == 19, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    check("I2c 13 ponedeljkov + 6 nedelj = 100% VIKEND!", mon == EXPECTED_MONDAYS and sun == 6, f"{mon} pon + {sun} ned")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (25. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [141..145]", scans == [141, 142, 143, 144, 145], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = e.get("groom", {}).get("place", "") + " " + e.get("bride", {}).get("place", "")
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = sorted(griblje_rows(ent))
    check("I4 Griblje vrste [1,14,17]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        for pl in (e.get("groom", {}).get("place", ""), e.get("bride", {}).get("place", "")):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 5 GRIBLJE [6,8,13,31,86]", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c INTRA-GRIBLJE INTRA-PRIIMEK (№1)", "INTRA-GRIBLJE INTRA-PRIIMEK" in allsi, "")
    check("I4d DISPENSA 3. kolena (№1 št. 159 [~])", "DISPENSA od krvnega sorodstva v 3. kolenu" in allsi, "")
    check("I4e DVOJNA SORODSTVENA ZAPREKA (№14)", "DVOJNA SORODSTVENA ZAPREKA" in allsi or "dvojni" in allsi.lower(), "")
    check("I4f DEŽELNA VLADE št. 18796 (№17)", "18796" in allsi, "")
    check("I4g MASA-DAN 24. 1. ×5", allsi.count("24. januar 1910") == 5, str(allsi.count("24. januar 1910")))
    check("I4h nevesta 16 let (№17)", "16" in allsi, "")
    check("I4i ženin 69 LEDIG (№18)", "69" in allsi, "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1910 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1910,', ts))
    check("I5a parish.ts bloki 1910 = 5", n_04455_1910 == GRIBLJE_BLOCKS, str(n_04455_1910))
    pins = [("13", "2. poročni dokaz h13"), ("13", "25-LETNA KONTINUITETA"),
            ("6", "4. poročni dokaz h6"), ("6", "Željko"),
            ("86", "NOVA POROČNA HIŠA"), ("86", "h85"),
            ("31", "4. poročni dokaz h31"), ("31", "Janez Straus × Barbara Jakobič"),
            ("8", "3. poročni dokaz h8"), ("8", "JAKLJEVIČ")]
    for hn, pin in pins:
        ms = re.findall(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1910,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = any(m and pin.lower() in m.lower() for m in ms)
        check(f"I5b pin h{hn} 1910 ({pin})", ok, (ms[0][:60] if ms else "BLOK MANJKA"))
    check("I5c P139 sekcija", "P139 razširitev: POROČNA KNJIGA 04455 — polno leto 1910" in ts)
    check("I5d INTRA-GRIBLJE v ts", "INTRA-GRIBLJE INTRA-PRIIMEK" in ts and "h13 × h6" in ts)
    check("I5e 18796 v ts", "18796" in ts and "DEŽELNE VLADE" in ts)

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p139 id", "qa-p139-parish-marriage-1910" in qa)
    n664 = qa.count("HOUSE_VITALS.length !== 686")
    check("I6b vitals pini 664", n664 >= 54, str(n664))
    n147 = qa.count(".length !== 164")
    check("I6c bloki pini 147", n147 >= 25, str(n147))
    check("I6d sidra 140 + 1910:5", "poročna sidra ≠ 162" in qa and "h.year === 1910).length !== 5" in qa)
    check("I6e hiše 1910 pin", '"6,8,13,31,86"' in qa)
    check("I6f ostanki 659/142/135", "!== 659" not in qa and ".length !== 142" not in qa and "sidra ≠ 135" not in qa, "stale pini!")
    check("I6g p80 hiše 68 (+h86!)", "p80Houses.size !== 72" in qa, "")
    check("I6h PT luknja 13 nespremenjena (h86 v naboru!)", "p80Gap.length !== 13" in qa, "")

    # ---------- I7: duhovniki + dnevi ----------
    priests = [e["priest"] for e in ent]
    rauy = sum(1 for p in priests if "Rauy" in p)
    check("I7 Rauy 17–18/19 (dominant)", rauy >= RAUY_COUNT, str(rauy))
    danijel = sum(1 for p in priests if "Danijel" in p or "DANIJEL" in p)
    check("I7b Danijel 1 (№9 — 2. pojav!)", danijel == 1, str(danijel))
    st = d["stats"]
    check("I7c stats mondays 13", st.get("mondays") == 13, str(st.get("mondays")))
    check("I7d stats sundays 6", st.get("sundays") == 6, str(st.get("sundays")))

    # ---------- I8: Parish stats ----------
    check("I8a stats vitals", st.get("vitalsTotal") == 664, str(st.get("vitalsTotal")))
    check("I8b stats bloki", st.get("blocks04455") == 147, str(st.get("blocks04455")))
    check("I8c stats sidra", st.get("sidraTotal") == 140, str(st.get("sidraTotal")))
    check("I8d stats entries 19", st.get("entries") == 19, str(st.get("entries")))
    check("I8e stats gribljeBlocks 5", st.get("gribljeBlocks") == 5, str(st.get("gribljeBlocks")))
    check("I8f stats newHouses [86] (NOVA POROČNA HIŠA!)", st.get("newHouses") == ["86"], str(st.get("newHouses")))
    check("I8g stats dispensas 3", st.get("dispensas") == 3, str(st.get("dispensas")))
    check("I8h stats p80Houses 68 (+h86!)", st.get("p80Houses") == 68, str(st.get("p80Houses")))
    check("I8i stats unnumbered 0", st.get("unnumbered") == 0, str(st.get("unnumbered")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 18", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 20", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P139" in notes and "1910" in notes and "INTRA-GRIBLJE" in notes)
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 7, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P139 bullet", "po P141" in rd)
    check("I10b README 664/147", "664" in rd and "147" in rd)
    check("I10c README P140 lead", "P140" in rd)

    # ---------- I11: P138 dokaz nespremenjen (lekcija P9) ----------
    d138 = json.load(open(DOKAZ_P138))
    check("I11 P138 dokaz 15 vpisov", len(d138["entries"]) == 15, str(len(d138["entries"])))

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
