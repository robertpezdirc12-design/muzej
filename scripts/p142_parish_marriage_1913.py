#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P142 — župnija Podzemelj: poročna knjiga 04455, polno leto 1913
(s152–s154-top == Pag. 151–153; s154 y≈780 = letna glava »1914«!) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P141 = 1912): okvir POTRJEN
— s152–s154-top == Pag. 151–153 (Pag. == sken − 1, **28. potrditev; velja
61–154**) + **s154 y≈780 = rokopisna letna glava »1914« = meja leta
DOKAZANA — 1. letna glava po 1908!** (+ »/1913« na s152 y≈50). **1913 =
13 VPISOV** (№1–6 s152 + №7–11 s153 + №12–13 s154-top; štetje: STRIP +
overview + zaporedje + meja; P141-lead je poznal samo №1!). **8 PON + 5 NED
= 13/13 VIKENDI — 1. popolno vikend-leto po 1907!** + postna vrzel 27.1. →
31.3. (3. zapored) + 0 masa-dnevov (1. po 2010!).

NOVELE: **★★★ №13 INTRA-KRALJ + 1. DISPENSA 3. KOLENA** (Jožef Kralj ×
Neža Kralj — 4. intra-priimek poroka linije + ordinariat Ljubljana
31/10.1913 št. 47845 + dvojni 1911-korpus-anker [obenem starša = 1911 №6 +
№13!] + obe mladoletni!) + **★★★ №3 DVOTERNA KORPUS-SINHRONIZACIJA
PEZDIREC** (Marjeta Pezdirec Griblje 53 = krst 14.8.1891 h53 + par-krsti
1915/1918 h53 'Dragos × Pezdirc'!) + **★★★ №10 INTRA-GRIBLJE h76 × h91 +
VSEBOVANA POROKA** (hčer Vilhelmina krščena 9.9.1913 h76 = 7 tednov po
poroki! + h76 = NOVA p80-hiša 69. → 70.!) + **★★ №11 GENETSKA-VAS
'Gorišice' = GRIBLJE 4. pojav** (Rajmund Čeveljak [~ Čeh] — 1. ime Rajmund
linije!) + **★★ №1 DATUMSKA ANKETA** ('24.1.'/'junij 27'/'27.1.' — rešeno:
dokument 25/1 + PON = 27.1.!; Matija Juvančič [~ Janževič] × Marija
Macel) + **★★ PEZDIREC-MREŽA ×7 + JUVANČIČ ×2** + **★ №12 najstarejši par
leta (66+44!)** + **★ №9 drugo-župnijski ženin (Petrova vas!)** + **★ c.k.
POŠTAR №7 (1. poštar linije!)** + **~16 NOVIH PRIIMKOV** → vitals 675 →
**681**; bloki 04455 158 → **164**; sidra 151 → **157** (+1913:6); p80
hiše **69 → 70 (+h76!)**; PT luknja **13** (h76 = nabor — nespremenjena);
P143 LEAD: 1914 №1 = 9.2. Jožef Pajzar × Ana Lipovec GRIBLJE 46 + 3–4
INTRA-GRIBLJE poroke 1914 — rekordno leto prihaja!

METODA: 8 krogov VLM-branj (21 Faza-1 + 26 vrstičnih + 84 finiх zoomov
multi-render o/i/d) + korpus-forenzika (04105-krsti 1885–1919 + 04455-poroke
1886–1912) + SISTEMSKA H/K/M-INITIAL CONFUSION-lekcija (Klepec/Hlepec/
Hlebec · Kralj/Hvali/Mal · Krasinec/Hrašinec · Macel/Mavrel — vsaka H/M
iniciala zahteva korpus-križ!).

Skripta scripts/p142_parish_marriage_1913.py (I1–I12, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I11).

Uporaba: python3 scripts/p142_parish_marriage_1913.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1913.json"
DOKAZ_P141 = "research/issue17/parish-marriage-1912.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1913-notes.md"
EXPECTED_ENTRIES = 13           # №1–№13
EXPECTED_EXCLUDED = 1           # letna glava »1914« s154
EXPECTED_ANOMALIES = 15
EXPECTED_CROSSCHECKS = 18
GRIBLJE_ROWS = [2, 3, 6, 10, 11]
GRIBLJE_HOUSES = ["1", "25", "35", "53", "76", "91"]
GRIBLJE_BLOCKS = 6              # №2 1 + №3 1 + №6 1 + №10 2 (INTRA!) + №11 1
GRIBLJE_INTRA = 1
VITALS_TOTAL = 681              # 675 + 6 (ZAMRNJEN 1913-evidence pin — NE posodabljati v kaskadi!; tekoči korpus = 686 od P144)
BLOKI_04455 = 164               # 158 + 6 (ZAMRNJEN 1913-evidence pin; tekoči = 169 od P144)
SIDRA_TOTAL = 157               # 151 + 6 blokov (+1913:6) (ZAMRNJEN 1913-evidence pin; tekoči = 162 od P144)
EXPECTED_MONDAYS = 9            # + 4 nedelje = 13/13 VIKENDI!
EXPECTED_SUNDAYS = 4

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
    check("I1b excluded 1 (letna glava »1914« s154 — meja leta!)",
          len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride"))
    check("I1c obojestransko 13/13", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [str(e["row"]) for e in ent]
    check("I2 vrste [1–13]", rows == [str(i) for i in range(1, 14)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\[?(\d+)[^\s]*\s+(\w+)", dt)
        if m:
            months[m.group(2)] = months.get(m.group(2), 0) + 1
    # jan 1 + mar 1 + apr 2 + maj 2 + jul 4 + avg 1 + nov 2 = 13
    check("I2b meseci (jan 1 + mar 1 + apr 2 + maj 2 + jul 4 + avg 1 + nov 2)",
          months.get("januar") == 1 and months.get("marec") == 1 and months.get("april") == 2
          and months.get("maj") == 2 and months.get("julij") == 4 and months.get("avgust") == 1
          and months.get("november") == 2 and sum(months.values()) == 13, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    check("I2c 9 ponedeljkov + 4 nedelje = 13/13 VIKENDI (1. popolno po 1907!)",
          mon == EXPECTED_MONDAYS and sun == EXPECTED_SUNDAYS,
          f"{mon} pon + {sun} ned")
    # postna vrzel: jan 27 -> mar 31 (post 5.2.–23.3.)
    lent = any("27. januar" in dt for dt in dates) and any("31. marec" in dt for dt in dates)
    check("I2d postna vrzel 27.1. → 31.3. (3. zapored!)", lent, "")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (28. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [152,153,154]", scans == [152, 153, 154], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = str(e.get("groom", {}).get("place", "")) + " " + str(e.get("bride", {}).get("place", ""))
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = sorted(griblje_rows(ent))
    check("I4 Griblje vrste [2,3,6,10,11]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        for pl in (str(e.get("groom", {}).get("place", "")), str(e.get("bride", {}).get("place", ""))):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 6 GRIBLJE [1,25,35,53,76,91]", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c INTRA-GRIBLJE №10 (h76 × h91 — 5. par linije!)",
          allsi.count("INTRA-GRIBLJE") >= 1, str(allsi.count("INTRA-GRIBLJE")))
    check("I4d DVOTERNA KORPUS-SINHRONIZACIJA №3 (krst 1891 + par 1915/1918!)",
          "DVOTERNA KORPUS-SINHRONIZACIJA" in allsi, "")
    check("I4e INTRA-KRALJ №13 + DISPENSA 3. KOLENA (ordinariat Ljubljana!)",
          "INTRA-KRALJ" in allsi and "DISPENSA 3. KOLENA" in allsi, "")
    check("I4f DVOJNI 1911-KORPUS-ANKER (№6 + №13!)", "KORPUS-ANKER 1911" in allsi and "1911 №13 starša" in allsi, "")
    check("I4g GENETSKA-VAS 'Gorišice' = Griblje 4. pojav (№11!)", "Gorišice" in allsi, "")
    check("I4h VSEBOVANA POROKA №10 (hčer 7 tednov po!)", "VSEBOVANA POROKA" in allsi, "")
    check("I4i DATUM-ANKETA №1 (27.1.!)", "DATUM-ANKETA" in allsi, "")
    check("I4j PEZDIREC-MREŽA ×7 + JUVANČIČ ×2", allsi.count("Pezdirec") >= 7 and "JUVANČIČ" in allsi, str(allsi.count("Pezdirec")))

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1913 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1913,', ts))
    check("I5a parish.ts bloki 1913 = 6", n_04455_1913 == GRIBLJE_BLOCKS, str(n_04455_1913))
    pins = [
        ("25", "KORPUS-HIŠA"),
        ("53", "DVOTERNA KORPUS-SINHRONIZACIJA"), ("53", "PAR-KRSTI"),
        ("1", "Željko-družina"),
        ("76", "1. POROČNI DOKAZ"), ("76", "NOVA p80-hiša"), ("76", "VSEBOVANA POROKA"),
        ("91", "KORPUS-KRST"),
        ("35", "GENETSKA-VAS"),
    ]
    for hn, pin in pins:
        ms = re.findall(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1913,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = any(m and pin.lower() in m.lower() for m in ms)
        check(f"I5b pin h{hn} 1913 ({pin})", ok, (ms[0][:60] if ms else "BLOK MANJKA"))
    check("I5c P142 sekcija", "P142 razširitev: POROČNA KNJIGA 04455 — polno leto 1913" in ts)
    check("I5d INTRA-GRIBLJE v ts (h76 × h91!)", "h76 × h91" in ts and "INTRA-GRIBLJE" in ts, "")
    check("I5e DISPENSA 3. KOLENA v ts", "DISPENSA 3. KOLENA" in ts, "")

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p142 id", "qa-p142-parish-marriage-1913" in qa)
    n686 = qa.count("HOUSE_VITALS.length !== 687")
    check("I6b vitals pini 686", n686 >= 57, str(n686))
    n169 = qa.count('.length !== 170')
    check("I6c bloki pini 169", n169 >= 2, str(n169))
    check("I6d sidra 162 + 1913:6", "poročna sidra ≠ 163" in qa and "p142Marr.length !== 6" in qa, "")
    check("I6e hiše 1913 pin", '"1,25,35,53,76,91"' in qa, "")
    check("I6f ostanki 681/164/157/70", "HOUSE_VITALS.length !== 681" not in qa and ".length !== 164" not in qa
          and "p80MarrAnchors.length !== 157" not in qa and "p80Houses.size !== 70" not in qa, "stare pini! (posodobljeno P143)")
    check("I6g p80 hiše 72 (+h76!)", "p80Houses.size !== 72" in qa, "")
    check("I6h PT luknja 13 nespremenjena", "p80Gap.length !== 13" in qa, "")

    # ---------- I7: dnevi ----------
    st = d["stats"]
    check("I7a stats mondays 8", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7b stats sundays 5", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7c stats sameVillage 1 (№10 INTRA!)", st.get("sameVillageCount") == 1, str(st.get("sameVillageCount")))
    check("I7d stats sameHouse 0", st.get("sameHouseCount") == 0, str(st.get("sameHouseCount")))
    check("I7e letna glava 1914 (1. po 1908!)", "1914" in str(st.get("yearHeading", "")), str(st.get("yearHeading", ""))[:40])

    # ---------- I8: Parish stats ----------
    check("I8a stats vitals 681", st.get("vitalsTotal") == VITALS_TOTAL, str(st.get("vitalsTotal")))
    check("I8b stats bloki 164", st.get("blocks04455") == BLOKI_04455, str(st.get("blocks04455")))
    check("I8c stats sidra 157", st.get("sidraTotal") == SIDRA_TOTAL, str(st.get("sidraTotal")))
    check("I8d stats entries 13", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    check("I8e stats gribljeBlocks 6", st.get("gribljeBlocks") == GRIBLJE_BLOCKS, str(st.get("gribljeBlocks")))
    check("I8f stats newHouses [76]", st.get("newHouses") == ["76"], str(st.get("newHouses")))
    check("I8g stats gribljeIntra 1", st.get("gribljeIntra") == GRIBLJE_INTRA, str(st.get("gribljeIntra")))
    check("I8h stats p80Houses 70 (+h76!)", st.get("p80Houses") == 70, str(st.get("p80Houses")))
    check("I8i stats unnumbered 0", st.get("unnumbered") == 0, str(st.get("unnumbered")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 15", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 18", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P142" in notes and "1913" in notes and "INTRA-KRALJ" in notes, "")
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 5, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P142 bullet", "po P142" in rd, "")
    check("I10b README 681/164", "681" in rd and "164" in rd, "")
    check("I10c README P143 lead", "P143" in rd, "")

    # ---------- I11: P141 dokaz nespremenjen ----------
    d141 = json.load(open(DOKAZ_P141))
    check("I11 P141 dokaz 17 vnosov", len(d141["entries"]) == 17, str(len(d141["entries"])))

    # ---------- I12: lead-korekcija ----------
    lead = d.get("lead", {})
    check("I12 lead-korekcija (13 vpisov NE 1 — P141-lead poznal samo №1!)",
          "13 vpisov" in lead.get("correction", ""), lead.get("correction", "")[:60])

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
