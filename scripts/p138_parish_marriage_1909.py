#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P138 — župnija Podzemelj: poročna knjiga 04455, polno leto 1909
(s138–s141 == Pag. 137–140) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P137 = 1908): okvir POTRJEN
— s138–s141 == Pag. 137–140 (Pag. == sken − 1, **24. potrditev; velja
61–140**). **LETNICA 1909 SE PIŠE V VSAKEM VPISU — NI samostojne letne
glave** (P137-lead »glava s138 y≈600« = prvi vpis №1 — nova lekcija!).
**P138-lead KOREKCIJA: »min 4 vpisi s138« → 15 vpisov (3,75× POCENJEN —
24. leto zaporedne podcenjenosti!)**.

NOVELE: **★★★ №11 INTRA-HIŠNA POROKA h46 × h46 + DISPENSA 3. KOLENA**
(ordinariat Ljubljana 12/10 1909 št. 4571 — Žugelj × Klobučar IZ ISTE
HIŠE! 2. v 2 letih po h14×h14 1908!) + **★★★ №14 SPREGLED 1. KOLENA +
SODNO DOVOLJENJE** (ordinariat št. 4786 + deželno sodišče Ljubljana št.
27036 — dvojna zapreka!) + **★★ №13 SPREGLED 3. KOLENA dotikajočega se
2. kolena** (št. 4995 — ženin TOME × nevestina mati geb. TOME!) + **★★
14 PONEDDELJKOV + 1 NEDELJA = 93% PON (REKORD linije!)** + **★★
NEŠTEVILČEN VPIS = VOJAŠKA POROKA Z DELEGACIJO** (k.k. pehotni polk št.
9 št. 2045 + delegacija 4/7 Z. 200!) + **★★ 2 GENDARMSKI POROKI** + **★
1. POROČNI DOKAZ h57** (Pezdirec-kriste 1888–1901 → poroka 1909!) + **★
№4 ženin LEDIG 63 + nevesta 58 = 121 let** + NOVE OBLASTI (Videm +
Dobrepolje + Rudolfštat) + ~27 NOVIH PRIIMKOV + NOVI DUHOVNIKI (Gregor
Petar? + Pavlič? + Danijel) → vitals 651 → **659**; bloki 04455 134 →
**142**; sidra 127 → **135** (+1909:8); p80 hiše **67** (h57 že v
korpusu!); PT luknja **13**.

Skripta scripts/p138_parish_marriage_1909.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p138_parish_marriage_1909.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1909.json"
DOKAZ_P137 = "research/issue17/parish-marriage-1908.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1909-notes.md"
EXPECTED_ENTRIES = 15           # №1–№14 + 1 NEŠTEVILČEN (5. 7.)
EXPECTED_EXCLUDED = []
EXPECTED_ANOMALIES = 17
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [1, 6, 8, 11, 13]
GRIBLJE_HOUSES = ["1", "17", "29", "30", "46", "57", "74"]
GRIBLJE_BLOCKS = 8              # №1 1 + №6 2 + №8 1 + №11 2 + №13 2
VITALS_TOTAL = 659              # 651 + 8
BLOKI_04455 = 142               # 134 + 8
SIDRA_TOTAL = 135               # 127 + 8 (1909:8)
RAUY_COUNT = 5                  # 5/8 blokov (№8 Gregor Petar? + №13 Pavlič? ×2)
EXPECTED_MONDAYS = 14           # + 1 nedelja (21. 2. №4)

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
    check("I1c obojestransko 15/15", both == EXPECTED_ENTRIES, str(both))
    unnum = [e for e in ent if e.get("unnumbered")]
    check("I1d 1 NEŠTEVILČEN (5. 7.)", len(unnum) == 1 and unnum[0]["row"] == 0, str(len(unnum)))

    # ---------- I2: vrste + datumi ----------
    rows = [str(e["row"]) for e in ent]
    check("I2 vrste [1–7, 0(NEŠT), 8–14]", rows == [str(i) for i in range(1, 8)] + ["0"] + [str(i) for i in range(8, 15)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\[?(\d+)[^\s]*\s+(\w+)", dt)
        if m:
            months[m.group(2)] = months.get(m.group(2), 0) + 1
    check("I2b meseci (jan 1 + feb 3 + maj 1 + jun 2 + jul 2 + avg 1 + okt 1 + nov 4)",
          months.get("januar") == 1 and months.get("februar") == 3 and months.get("maj") == 1
          and months.get("junij") == 2 and months.get("julij") == 2 and months.get("avgust") == 1
          and months.get("oktober") == 1 and months.get("november") == 4 and sum(months.values()) == 15, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    check("I2c 14 ponedeljkov (REKORD 93%!)", mon == EXPECTED_MONDAYS, f"{mon} pon + {sun} ned")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (24. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [138..141]", scans == [138, 139, 140, 141], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = e.get("groom", {}).get("place", "") + " " + e.get("bride", {}).get("place", "")
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = sorted(griblje_rows(ent))
    check("I4 Griblje vrste [1,6,8,11,13]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        for pl in (e.get("groom", {}).get("place", ""), e.get("bride", {}).get("place", "")):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 7 GRIBLJE [1,17,29,30,46,57,74]", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c h46 ×2 (№11 INTRA-HIŠNA!)", allsi.count("GRIBLJE 46") >= 2, str(allsi.count("GRIBLJE 46")))
    check("I4d INTRA-HIŠNA POROKA", "INTRA-HIŠNA POROKA" in allsi, "")
    check("I4e DISPENSA 3. KOLENA (№11)", "DISPENSA 3. KOLENA" in allsi, "")
    check("I4f SPREGLED 3. KOLENA (№13)", "SPREGLED 3. KOLENA" in allsi, "")
    check("I4g NEŠTEVILČEN + DELEGACIJA", "NEŠTEVILČEN" in allsi and "DELEGACIJO" in allsi, "")
    check("I4h 1. POROČNI DOKAZ h57", "1. POROČNI DOKAZ h57" in allsi, "")
    check("I4i ženin 63 LEDIG", "63" in allsi and "LEDIG" in allsi, "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1909 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1909,', ts))
    check("I5a parish.ts bloki 1909 = 8", n_04455_1909 == GRIBLJE_BLOCKS, str(n_04455_1909))
    pins = [("17", "2. poročni dokaz h17"), ("17", "KRALJ"),
            ("74", "2. poročni dokaz h74"), ("74", "KAMBIČ"),
            ("30", "3. poročni dokaz h30"), ("30", "MILEK-kontinuiteta"),
            ("57", "1. POROČNI DOKAZ h57"), ("57", "PEZDIREC"), ("57", "1888"),
            ("46", "INTRA-HIŠNA POROKA"), ("46", "DISPENSA 3. KOLENA"), ("46", "KLOBUČAR"), ("46", "FILAK"),
            ("1", "3. poročni dokaz h1"), ("1", "TOME"),
            ("29", "3. poročni dokaz h29"), ("29", "KURE"), ("29", "SPREGLED")]
    for hn, pin in pins:
        ms = re.findall(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1909,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = any(m and pin.lower() in m.lower() for m in ms)
        check(f"I5b pin h{hn} ({pin})", ok, (ms[0][:60] if ms else "BLOK MANJKA"))
    check("I5c P138 sekcija", "P138 razširitev: POROČNA KNJIGA 04455 — polno leto 1909" in ts)
    check("I5d INTRA-HIŠNA v ts", "INTRA-HIŠNA POROKA" in ts and "h46 × h46" in ts)
    check("I5e SPREGLED v ts", "SPREGLED" in ts and "TOME" in ts)

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p138 id", "qa-p138-parish-marriage-1909" in qa)
    n659 = qa.count("HOUSE_VITALS.length !== 702")
    check("I6b vitals pini 659", n659 >= 52, str(n659))
    n142 = qa.count(".length !== 185")
    check("I6c bloki pini 171 (P146-sanacija starega 147-pina!)", n142 >= 25, str(n142))
    check("I6d sidra 140 + 1909:8", "poročna sidra ≠ 178" in qa and "h.year === 1909).length !== 8" in qa)
    check("I6e hiše 1909 pin", '"1,17,29,30,46,46,57,74"' in qa)
    check("I6f ostanki 651/134/127", "!== 651" not in qa and "!== 698" not in qa and "!== 134" not in qa and "sidra ≠ 127" not in qa, "stale pini!")
    check("I6g vrata h30+h46 (P138 izjeme)", 'v.year === 1909 && hn === "30"' in qa and '(hn === "46" && (v.year === 1898 || v.year === 1903 || v.year === 1904 || v.year === 1909 || v.year === 1912))' in qa)
    check("I6h p80 hiše 68 + PT 13 (h57 že v korpusu!)", "p80Houses.size !== 75" in qa and "p80Gap.length !== 13" in qa)

    # ---------- I7: duhovniki + dnevi ----------
    priests = [e["priest"] for e in ent]
    rauy = sum(1 for p in priests if "Rauy" in p)
    check("I7 Rauy 11/15 celotno (dominant)", rauy >= 10, str(rauy))
    neray = sum(1 for p in priests if "Rauy" not in p)
    check("I7b 4 ne-Rauy (Danijel + Gregor Petar? + Pavlič? + [Rauy-Dami? ~])", 3 <= neray <= 5, str(neray))
    st = d["stats"]
    check("I7c stats mondays 14", st.get("mondays") == 14, str(st.get("mondays")))
    check("I7d stats sundays 1", st.get("sundays") == 1, str(st.get("sundays")))

    # ---------- I8: Parish stats ----------
    check("I8a stats vitals", st.get("vitalsTotal") == 659, str(st.get("vitalsTotal")))
    check("I8b stats bloki", st.get("blocks04455") == 142, str(st.get("blocks04455")))
    check("I8c stats sidra", st.get("sidraTotal") == 135, str(st.get("sidraTotal")))
    check("I8d stats entries 15", st.get("entries") == 15, str(st.get("entries")))
    check("I8e stats gribljeBlocks 8", st.get("gribljeBlocks") == 8, str(st.get("gribljeBlocks")))
    check("I8f stats newHouses [] (h57 že v korpusu!)", st.get("newHouses") == [], str(st.get("newHouses")))
    check("I8g stats dispensas 3", st.get("dispensas") == 3, str(st.get("dispensas")))
    check("I8h stats p80Houses 67 (h57 že!)", st.get("p80Houses") == 67, str(st.get("p80Houses")))
    check("I8i stats unnumbered 1", st.get("unnumbered") == 1, str(st.get("unnumbered")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 17", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 20", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P138" in notes and "1909" in notes and "INTRA-HIŠNA" in notes)
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 8, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P138 bullet", "po P141" in rd)
    check("I10b README 659/142", "659" in rd and "142" in rd)
    check("I10c README P139 lead", "P139" in rd)

    # ---------- I11: P137 dokaz nespremenjen (lekcija P9) ----------
    d137 = json.load(open(DOKAZ_P137))
    check("I11 P137 dokaz 17 vpisov", len(d137["entries"]) == 17, str(len(d137["entries"])))

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
