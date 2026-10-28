#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P140 — župnija Podzemelj: poročna knjiga 04455, polno leto 1911
(s146–s148 == Pag. 145–147) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P139 = 1910): okvir POTRJEN
— s146–s148 == Pag. 145–147 (Pag. == sken − 1, **26. potrditev; velja
61–148**). **LETNICA 1911 SE PIŠE V VSAKEM VPISU — brez letne glave** (3. leto
lekcije: 1909/1910/1911). **1911 = 13 VPISOV** (№1–6 s146 + №7–11 s147 +
№12–13 s148; štetje potrjeno s STRIP-tehniko [celi datumski stolpci 6+5+2!] +
zaporednimi branjí + GRID-№ + r7full=PRAZNA [№7-s146 podvojitev P139-leada
zavrnjena!]).

NOVELE: **★★★ №7 ZGODOVINSKA DUNAJSKA POROKA** (Julius BETETTO k.k.
HOFOPERN-SÄNGER — dvorni operni pevec Dunaja!, 25, Wien IV/8 Wallergasse 3/11
× Irma-Maria STUKELY 19 Rudolfsheim 132 — 4. 7. 1911 TOR = EDINA nevikend
leta [8 PON + 4 NED + 1 TOR]! + listine pri Standesamt Rudolfsheim + RAUY
PER DELEGATIONEM [1. podpis po delegaciji v liniji!] + mati Julia SKRBEC =
slovenske korenine dunajskega zvezdnika + dunajski meščanski priči
[lekarnar + knjigotržec] + nevesta 19 = najmlajša leta!) + **★★★ ISTA-HIŠA
REKORD ×3** (№6 Podzemelj 2 + №8 Vranoviči 3 + №11 Gradac 3 — prejšnji maks
1/leto!) + **★★ INTRA-GRIBLJE ×2** (№1 h31 × h63 [3. leto zapored!] + №2
h15 × h34 — rekord z 1910) + **★★ №1 REHABILITACIJSKA POROKA?** (Katarina
Križan 'samka' h63-1909 [hči Jožefa 12. 6. 1909!] → 30. 1. 1911) + **№1
DVOJNO ZUNANJE SIDRO** (ženinov krst h31-1887 Janez [starost 23 ✓] + EMŠO-1919
'Katarina r. Herian por. 30/1 1911'!) + **№8 BUTALA-SESTRI** (Anna 1911 =
sestra Marije 1910 №5 — ista starša + ista hiša!) + **№12 VDOVEC +
KORPUS-SINHRONIZACIJA** (krst Terezije 5. 10. 1912 Martin Papič × ANA TOMC =
PAR POTRDJEN!; prva žena Marija Mlut — hčeri 1909 + †9 dni 23. 5. 1911) +
**№12 'Giriči' = GRIBLJE** (genetska-vas 3. pojav) + MASA-DAN 6. 2. ×3 +
POSTNA VRZEL 6. 2. → 15. 5. ('15. März' ZAVRNJENO — sredina posta!) + №13
KRALJ ×2 + KLEPEC-trojni mreža + №6 Kralj × Pezdirec starši + №9 MAROVIČ
oče-sin dvojček + №10 ZUCKERMEISTER + ŽUGELJ ×3 + NOVI POKLICI (Hofopern-
Sänger! + Zuckermeister + Köppersohn + Knecht + Gemeinde-Beamter + Doltar
kovaška dinastija) + ~20 NOVIH PRIIMKOV + NOVE OBLASTI (Standesamt Rudolfsheim
Dunaj! + Črnomelj št. 316 + ordinariat 7. 11. 1911 [~] + županstvo Gradac) →
vitals 664 → **670**; bloki 04455 147 → **153**; sidra 140 → **146**
(+1911:6); p80 hiše 68 → **69 (+h63 — 04105-h63 bloki 1887–1909 izven
p80-filtra!)**; PT luknja **13** (nespremenjena — h63 v naboru 61–99!);
P141 LEAD: 1912 №1 = 16. 1. 1912 Anton Lozar 21 Griblje 78 × Barbara Križan
22 Griblje 63 (Lozar ×2 v 3 mesecih + 04105-h78-1915 krst!).

METODA: 65 VLM branj v 4 krogih + STRIP-TEHNIKA (celi datumski stolpec kot
en izrez = avtoritativno število vrstic!) + eko-watchdog V2 (30-min ping po
429, 45-s razmak branj — 26 branj brez ponovnega zaklepa) + POSTNA-koledarska
validacija datuma.

Skripta scripts/p140_parish_marriage_1911.py (I1–I11, --check izpiše PASS/FAIL
in vrne exit code; --live omogoči HTTP preverjanje matricula-online.eu). Brez
--live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p140_parish_marriage_1911.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1911.json"
DOKAZ_P139 = "research/issue17/parish-marriage-1910.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1911-notes.md"
EXPECTED_ENTRIES = 13           # №1–№13
EXPECTED_EXCLUDED = []
EXPECTED_ANOMALIES = 14
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [1, 2, 3, 12]
GRIBLJE_HOUSES = ["9", "15", "31", "33", "34", "63"]
GRIBLJE_BLOCKS = 6              # №1 2 (INTRA!) + №2 2 (INTRA!) + №3 1 + №12 1
GRIBLJE_INTRA = 2
VITALS_TOTAL = 670              # 664 + 6
BLOKI_04455 = 153               # 147 + 6
SIDRA_TOTAL = 146               # 140 + 6 (+1911:6) — ERA-PIN P140 (dokaz nespremenjen!)
RAUY_COUNT = 13                 # 13/13 — №7 per delegationem!
EXPECTED_MONDAYS = 8            # + 4 nedelj + 1 TOR (BETETTO Dunaj!)
EXPECTED_SUNDAYS = 4
SAME_HOUSE_ROWS = [6, 8, 11]    # REKORD ×3!

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
    check("I2b meseci (jan 1 + feb 3 + maj 1 + jun 1 + jul 1 + sep 1 + okt 3 + nov 2)",
          months.get("januar") == 1 and months.get("februar") == 3 and months.get("maj") == 1
          and months.get("junij") == 1 and months.get("julij") == 1 and months.get("september") == 1
          and months.get("oktober") == 3 and months.get("november") == 2
          and sum(months.values()) == 13, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    tor = sum(1 for dt in dates if "torek" in dt)
    check("I2c 8 ponedeljkov + 4 nedelje + 1 torek (BETETTO!)",
          mon == EXPECTED_MONDAYS and sun == EXPECTED_SUNDAYS and tor == 1,
          f"{mon} pon + {sun} ned + {tor} tor")
    masa = sum(1 for dt in dates if "6. februar 1911" in dt)
    check("I2d MASA-DAN 6. 2. ×3 (№2+№3+№4)", masa == 3, str(masa))
    check("I2e POSTNA VRZEL (15. maj po 6. februarju — brez marca/aprila!)",
          not any("marec" in dt or "april" in dt for dt in dates), "")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (26. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [146,147,148]", scans == [146, 147, 148], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = e.get("groom", {}).get("place", "") + " " + e.get("bride", {}).get("place", "")
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = sorted(griblje_rows(ent))
    check("I4 Griblje vrste [1,2,3,12]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        for pl in (e.get("groom", {}).get("place", ""), e.get("bride", {}).get("place", "")):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 6 GRIBLJE [9,15,31,33,34,63]", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c INTRA-GRIBLJE ×2 (№1 h31 × h63 + №2 h15 × h34)",
          allsi.count("GRIBLJE × GRIBLJE") >= 2, str(allsi.count("GRIBLJE × GRIBLJE")))
    check("I4d REHABILITACIJSKA POROKA (№1 — samka h63-1909!)", "REHABILITACIJSKA" in allsi, "")
    check("I4e BETETTO Hofopern-Sänger (№7!)", "HOFOPERN-SÄNGER" in allsi.upper() or "Hofopern-Sänger" in allsi, "")
    check("I4f PER DELEGATIONEM (№7 Rauy!)", "PER DELEGATIONEM" in allsi, "")
    check("I4g ISTA-HIŠA ×3 (№6+№8+№11!)", "ISTA HIŠA" in allsi or "ista-hiša" in allsi.lower(), "")
    check("I4h №12 VDOVEC", "WITWER" in allsi or "vdovec" in allsi.lower(), "")
    check("I4i KORPUS-SINHRONIZACIJA (№12 krst 1912!)", "KORPUS-SINHRONIZACIJA" in allsi, "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1911 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1911,', ts))
    check("I5a parish.ts bloki 1911 = 6", n_04455_1911 == GRIBLJE_BLOCKS, str(n_04455_1911))
    pins = [
        ("31", "5. poročni dokaz h31"), ("31", "KRST V KORPUSU"),
        ("63", "NOVA POROČNA HIŠA"), ("63", "REHABILITACIJSKA"), ("63", "samka"),
        ("15", "KAMBIČ-DINASTIJA"), ("34", "KAMBIČ-DINASTIJA"),
        ("9", "JAKOBČIČ-TROJNA MREŽA"), ("9", "26 LET"),
        ("33", "GENETSKA-GRIBLJE"), ("33", "KORPUS-SINHRONIZACIJA"), ("33", "WITWER"),
    ]
    for hn, pin in pins:
        ms = re.findall(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1911,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = any(m and pin.lower() in m.lower() for m in ms)
        check(f"I5b pin h{hn} 1911 ({pin})", ok, (ms[0][:60] if ms else "BLOK MANJKA"))
    check("I5c P140 sekcija", "P140 razširitev: POROČNA KNJIGA 04455 — polno leto 1911" in ts)
    check("I5d INTRA-GRIBLJE v ts", "GRIBLJE × GRIBLJE" in ts and "h31 × h63" in ts)
    check("I5e BETETTO v ts", "BETETTO" in ts and "Wallergasse" in ts)

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p140 id", "qa-p140-parish-marriage-1911" in qa)
    n670 = qa.count("HOUSE_VITALS.length !== 702")
    check("I6b vitals pini 670", n670 >= 54, str(n670))
    n153 = qa.count('.length !== 185')
    check("I6c bloki pini 158", n153 >= 25, str(n153))
    check("I6d sidra 163 + 1911:6", "poročna sidra ≠ 178" in qa and "h.year === 1911).length !== 6" in qa)
    check("I6e hiše 1911 pin", '"9,15,31,33,34,63"' in qa)
    check("I6f ostanki 664/147/140", "!== 664" not in qa and ".length !== 147" not in qa and "sidra ≠ 140" not in qa, "stare pini!")
    check("I6g p80 hiše 70 (+h63!)", "p80Houses.size !== 75" in qa, "")
    check("I6h PT luknja 13 nespremenjena (h63 v naboru!)", "p80Gap.length !== 13" in qa, "")

    # ---------- I7: duhovniki + dnevi ----------
    priests = [e["priest"] for e in ent]
    rauy = sum(1 for p in priests if "Rauy" in p)
    check("I7 Rauy 13/13 (№7 per delegationem!)", rauy == RAUY_COUNT, str(rauy))
    st = d["stats"]
    check("I7b stats mondays 8", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7c stats sundays 4", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7d stats sameHouse 3 (REKORD!)", st.get("sameHouseCount") == 3, str(st.get("sameHouseCount")))

    # ---------- I8: Parish stats ----------
    check("I8a stats vitals", st.get("vitalsTotal") == VITALS_TOTAL, str(st.get("vitalsTotal")))
    check("I8b stats bloki", st.get("blocks04455") == BLOKI_04455, str(st.get("blocks04455")))
    check("I8c stats sidra", st.get("sidraTotal") == SIDRA_TOTAL, str(st.get("sidraTotal")))
    check("I8d stats entries 13", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    check("I8e stats gribljeBlocks 6", st.get("gribljeBlocks") == GRIBLJE_BLOCKS, str(st.get("gribljeBlocks")))
    check("I8f stats newHouses [63]", st.get("newHouses") == ["63"], str(st.get("newHouses")))
    check("I8g stats gribljeIntra 2 (REKORD!)", st.get("gribljeIntra") == GRIBLJE_INTRA, str(st.get("gribljeIntra")))
    check("I8h stats p80Houses 69 (+h63! — ERA-PIN P140)", st.get("p80Houses") == 69, str(st.get("p80Houses")))
    check("I8i stats unnumbered 0", st.get("unnumbered") == 0, str(st.get("unnumbered")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 14", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 20", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P140" in notes and "1911" in notes and "BETETTO" in notes)
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 7, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P140 bullet", "po P141" in rd)
    check("I10b README 670/153", "670" in rd and "153" in rd)
    check("I10c README P141 lead", "P141" in rd)

    # ---------- I11: P139 dokaz nespremenjen (lekcija P9) ----------
    d139 = json.load(open(DOKAZ_P139))
    check("I11 P139 dokaz 19 vpisov", len(d139["entries"]) == 19, str(len(d139["entries"])))

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
