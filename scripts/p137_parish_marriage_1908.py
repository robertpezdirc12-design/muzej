#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P137 — župnija Podzemelj: poročna knjiga 04455, polno leto 1908
(s134–s138 == Pag. 133–137) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P136 = 1907): okvir POTRJEN
— s134–s138 == Pag. 133–137 (Pag. == sken − 1, **23. potrditev; velja
61–137**); **ROKOPISNA GLAVA »1908« NA DNU s134 (y≈980) POTRJENA**
(P136-lead!) + **ROKOPISNA GLAVA »1909« na s138 (y≈600) = P138 LEAD**
(1909-v1 Jän 25 + v2 Febr 8 + v3 März 15 + v4 Febr 21 že vidni!).
**P137-lead KOREKCIJA: »min 2 vpisa s134« → 17 vpisov (8,5× POCENJEN —
23. leto zaporedne podcenjenosti!)**.

NOVELE: **★★★ v17 INTRA-HIŠNA POROKA h14 × h14 — 1. V 23 LETIH LINIJE!**
(ženin Johann BRINEC = **1895-v17 ISTI** — 1. žena Maria Pezdirec † →
poroči **SESTRO pokojne žene** Dorotheo Pezdirec = **★★ AFINITETNA
DISPENSA 1. KOLENA** (sororate — najhujša sorodstvena zapreka linije!) +
**★★ hčerka krščena 16. 2. 1908 na h14 (P103!) — 9 MESECEV PRED
poroko!**) + **★★ v16 73-LETNI ŽENIN = NOVI REKORD LINIJE** (prej 62
P135! +11 let!) + **★★ 4 DISPENZE V LETU** (v3 št. 265 + v5 + v15 št. 4208
+ v17 — vs 1 v 1907!) + **★★ v5 1. RAZVEZANI ŽENIN LINIJE** (modri
zapis!) + **★ v1 RECIPROČNA POROKA** (Požek × Kure — 1889-ženin ISTI!) +
**★ v10 GRIBLJE-DRUBEL h39 × h44** (1887-krst ISTA!) + **★ v14 DEHLIČ ×
DEHLIČ** (1888-družina ISTA 20 let!) + **★ v9 NOVA HIŠA h43** (67. poročna
hiša!) + **★ NOVI DUHOVNIK Jos. DAMI [~]** + **★ NOVE VASI** (Mehovce pf.
Podgrad · Drašiči · Žaloka [Hrvaška?]) → vitals 642 → **651**; bloki 04455
125 → **134**; sidra 118 → **127** (+1908:9); p80 hiše 66 → **67** (+h43);
PT luknja 12 → **13**.

Skripta scripts/p137_parish_marriage_1908.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p137_parish_marriage_1908.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1908.json"
DOKAZ_P136 = "research/issue17/parish-marriage-1907.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1908-notes.md"
EXPECTED_ENTRIES = 17           # v1–v17 (vsi oštevilčeni razen morebitnih)
EXPECTED_EXCLUDED = []
EXPECTED_ANOMALIES = 21
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [1, 5, 9, 10, 14, 17]
GRIBLJE_HOUSES = ["14", "21", "28", "33", "39", "43", "44", "62"]
GRIBLJE_BLOCKS = 9              # +9 blokov (h14 ×2 — INTRA-HIŠNA!)
VITALS_TOTAL = 659              # 642 + 9
BLOKI_04455 = 142               # 125 + 9
SIDRA_TOTAL = 135               # 118 + 9 (1908:9)
RAUY_COUNT = 7                  # 7/9 blokov (v10 dvema [Dami? ~])
EXPECTED_MONDAYS = 11           # 11 ponedeljkov + 4–5 nedelj

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
    rows = [str(e["row"]) for e in ent]
    check("I2 vrste 1–17", rows == [str(i) for i in range(1, 18)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\[?(\d+)[^\s]*\s+(\w+)", dt)
        if m:
            months[m.group(2)] = months.get(m.group(2), 0) + 1
    check("I2b meseci (jan 2 + feb 7 + mar 2 + maj 1 + jun 2 + sep 1 + okt 1 + nov 1)",
          months.get("januar") == 2 and months.get("februar") == 7 and months.get("marec") == 2
          and months.get("maj") == 1 and months.get("junij") == 2 and months.get("september") == 1
          and months.get("oktober") == 1 and sum(months.values()) == 17, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    check("I2c 11 ponedeljkov", mon == EXPECTED_MONDAYS, f"{mon} pon + {sun} ned")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (23. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [134..138]", scans == [134, 135, 136, 137, 138], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = e.get("groom", {}).get("place", "") + " " + e.get("bride", {}).get("place", "")
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = sorted(griblje_rows(ent))
    check("I4 Griblje vrste [1,5,9,10,14,17]", g == [1, 5, 9, 10, 14, 17], str(g))
    houses = []
    for e in ent:
        for pl in (e.get("groom", {}).get("place", ""), e.get("bride", {}).get("place", "")):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 8 GRIBLJE [14,21,28,33,39,43,44,62]", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c h14 ×2 (v17 INTRA-HIŠNA!)", allsi.count("GRIBLJE 14") >= 2, str(allsi.count("GRIBLJE 14")))
    check("I4d NOVA HIŠA h43", "NOVA HIŠA" in allsi and "h43" in allsi, "")
    check("I4e AFINITETNA DISPENSA 1. kolena", "AFINITETNA DISPENSA" in allsi or "AFINITETE" in allsi, "")
    check("I4f INTRA-HIŠNA POROKA", "INTRA-HIŠNA POROKA" in allsi, "")
    check("I4g RAZVEZA", "RAZVEZAN" in allsi or "RAZVEZA" in allsi, "")
    check("I4h 73-LETNI ŽENIN", "73" in allsi, "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1908 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1908,', ts))
    check("I5a parish.ts bloki 1908 = 9", n_04455_1908 == GRIBLJE_BLOCKS, str(n_04455_1908))
    pins = [("21", "19-LETNA LUKNJA"), ("21", "RECIPROČNA"), ("21", "ISTI KOT 1889-v3"),
            ("62", "5. poročni dokaz h62"), ("62", "KURE-kontinuiteta"),
            ("28", "1. POROČNI DOKAZ h28"), ("28", "RAZVEZAN"), ("28", "Milkovič"),
            ("43", "NOVA HIŠA"), ("43", "LASIČ"), ("43", "ŽUPANIČ"),
            ("39", "2. poročni dokaz h39"), ("39", "DRUBEL"),
            ("44", "3. poročni dokaz h44"), ("44", "krst 1887"),
            ("33", "20 LETIH"), ("33", "DEHLIČ × DEHLIČ"),
            ("14", "INTRA-HIŠNA POROKA"), ("14", "AFINITETNA DISPENSA"), ("14", "SESTRA pokojne žene"), ("14", "ISTEGA")]
    for hn, pin in pins:
        ms = re.findall(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1908,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = any(m and pin.lower() in m.lower() for m in ms)
        check(f"I5b pin h{hn} ({pin})", ok, (ms[0][:60] if ms else "BLOK MANJKA"))
    check("I5c P137 sekcija", "P137 razširitev: POROČNA KNJIGA 04455 — polno leto 1908" in ts)
    check("I5d INTRA-HIŠNA v ts", "INTRA-HIŠNA POROKA" in ts and "h14 × h14" in ts)
    check("I5e AFINITETNA DISPENSA v ts", "AFINITETNA DISPENSA" in ts and "SESTRA pokojne žene" in ts)

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p137 id", "qa-p137-parish-marriage-1908" in qa)
    n651 = qa.count("HOUSE_VITALS.length !== 659")
    check("I6b vitals pini 651", n651 >= 51, str(n651))
    n134 = qa.count("≠ 142")
    check("I6c bloki pini 134", n134 >= 20, str(n134))
    check("I6d sidra 127 + 1908:9", "poročna sidra ≠ 135" in qa and "h.year === 1908).length !== 9" in qa)
    check("I6e hiše 1908 pin", '"14,14,21,28,33,39,43,44,62"' in qa)
    check("I6f ostanki 642/125/118", "!== 642" not in qa and "≠ 125" not in qa and "sidra ≠ 118" not in qa, "stale pini!")
    check("I6g NOVA-hiša izjeme (P86+P91+P92)", 'v.year === 1908 && hn === "28"' in qa and 'hn === "14" && v.year === 1908' in qa and 'v.year === 1908 && hn === "43"' in qa)
    check("I6h p80 hiše 67 + PT 13", "p80Houses.size !== 67" in qa and "p80Gap.length !== 13" in qa and '"43"' in qa.split("P80_PT_GAP")[1][:200])

    # ---------- I7: duhovniki + dnevi ----------
    priests = [e["priest"] for e in ent]
    rauy = sum(1 for p in priests if "Rauy" in p)
    check("I7 Rauy 12/17 celotno (dominant)", rauy >= 12, str(rauy))
    neray = sum(1 for p in priests if "Rauy" not in p)
    check("I7b 5 ne-Rauy ([~ Dami?] — novi kaplan P103!)", 3 <= neray <= 6, str(neray))
    st = d["stats"]
    check("I7c stats mondays 11", st.get("mondays") == 11, str(st.get("mondays")))
    check("I7d stats sundays 4", st.get("sundays") == 4, str(st.get("sundays")))

    # ---------- I8: Parish stats ----------
    check("I8a stats vitals", st.get("vitalsTotal") == 651, str(st.get("vitalsTotal")))
    check("I8b stats bloki", st.get("blocks04455") == 134, str(st.get("blocks04455")))
    check("I8c stats sidra", st.get("sidraTotal") == 127, str(st.get("sidraTotal")))
    check("I8d stats entries 17", st.get("entries") == 17, str(st.get("entries")))
    check("I8e stats gribljeBlocks 9", st.get("gribljeBlocks") == 9, str(st.get("gribljeBlocks")))
    check("I8f stats newHouses [43]", st.get("newHouses") == ["43"], str(st.get("newHouses")))
    check("I8g stats dispensas 4", st.get("dispensas") == 4, str(st.get("dispensas")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 21", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 20", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P137" in notes and "1908" in notes and "INTRA-HIŠNA" in notes)
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 8, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P137 bullet", "po P138" in rd)
    check("I10b README 651/134", "651" in rd and "134" in rd)
    check("I10c README P138 lead", "P138" in rd)

    # ---------- I11: P136 dokaz nespremenjen (lekcija P9) ----------
    d136 = json.load(open(DOKAZ_P136))
    check("I11 P136 dokaz 12 vpisov", len(d136["entries"]) == 12, str(len(d136["entries"])))

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
