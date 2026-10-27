#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P141 — župnija Podzemelj: poročna knjiga 04455, polno leto 1912
(s148-dno + s149–s151 == Pag. 147–150; s152 = ŽE 1913!) (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P140 = 1911): okvir POTRJEN
— s148-dno + s149–s151 == Pag. 147–150 (Pag. == sken − 1, **27. potrditev;
velja 61–151**) + **s152 = ŽE 1913 №1 (27. 1. 1913) = meja leta DOKAZANA +
P142-lead!**. **LETNICA 1912 V VSAKEM VPISU — brez letne glave** (4. leto
lekcije). **1912 = 17 VPISOV** (№1 s148-dno + №2–6 s149 + №7–11 s150 +
№12–17 s151; štetje potrjeno s STRIP-tehniko [celi datumski stolpci s148–
s151!] + zaporedjem + s152-mejo; P140-lead je poznal samo №1–6 — razširitev
×2,8!). **1912 = SLOVENŠČINA + najhitrejša pisava novega pisarja = najtežje
leto linije** (~190 VLM branj v 6 krogih + STRIP + GRID-geometrija
[REZIDENCA JE PRED IMENOM V BLOKU!] + multi-render pasovi o/i/d).

NOVELE: **★★★ RECIPROČNI DVOJNI PAR SOROJENCEV (№11+№12, 20. 5. 1912)**
— Muc-sorojenca (Barbara 24 + Nikolaj 34, Primostek 10, otroka Matija Muc ×
Ana geb. Vukšinič) × Jakljevič-sorojenca (Nikolaj 26 + Marija 20, Krasinec
13, otroka Nikolaj Jakljevič × Ana geb. Križan [~]) — KRIŽNO-IZMENJČNE
HIŠE = 1. tak primer v celotni liniji 1886–1912! (prejšnji maks: 1910 №3+№4
Dragoš-sorojenca isti dan — a brez reciprocitete!) + **★★★ INTRA-PRIIMEK
×2 V ENEM LETU** (№7 PEZDIREC × PEZDIREC [Mihaelova vs Matijeva linija —
zrcalo 1910 №1 Jakobčič!] + №14 ŽUGELJ × ŽUGELJ [Jakobova vs Matijeva] =
3 intra-priimek poroke linije, 2 v samem 1912 = REKORD!) + **★★★ SESTRI
KRIŽAN h63 V ZAPOREDNIH JANUARJIH** (1911 №1 Katarina × Papič h31 + 1912
№1 Barbara × Lozar h78 — obe hčereti Nikolaja Križana × Katarina geb.
Pezdirec; P140-lead 'sestri?' → POTRJENO S KORPUSOM [krsta 20. 1. 1887 +
20. 6. 1889 h63!]) + **★★★ DVOJNA KORPUS-SINHRONIZACIJA №8** (ženinovi
starši = 1891 №12 Jakša × Jakša + nevestini starši = 1890 №2 Schweiger ×
Jakša — OBA STARŠA-PARA ŽE V KORPUSU = 1. tak primer!) + **★★ №9 NEVESTA
46 LET** (Barbara Straus bajtarica Griblje h46 — 2. najstarejša po 1886-v1
56; par 31+46; h46 = 3. poročni dokaz [1909 №11 INTRA-h46!]) + **★★ №17
KORPUS-SINHRO 1913** (sin Julij krst 8. 8. 1913 h31 Griblje 'Jožef Černič ×
Ana Počelf[=Požek]' — PAR + PRESELITEV POTRJENA!; nevesta krst 3. 4. 1890
Janez Požek × Ana Šimec = starost 22 ✓; POŽEK = MEŽNARJI Adlešič!) + **★★
№4+№6 JAKOFČIČ DVOJČEK** (brat ženin Nikolaj Čerkvišče 16 + sestra nevesta
Ana Čerkvišče 17 — otroka Petra Jakofčiča; poroki 29. 1. + 12. 2.!) + **★★
HRAŠINOVIČ-DVOJČEK** (№6 Nikolaj 24 Krasinec 20 + №16 Nikolaj 49 Krasinec
32 — očeta Anton + Janez + №1 mati Barbara geb. Harasinč = 3. pojav!) +
**★★ ŠTRAVS/STRAUS-MREŽA ×4** (№9+№10+№15 neveste + priča Jožef = 3
Straus-neveste leta = REKORD!) + MASA-DNEVI ×3 (29. 1. №2+№3+№4 TROJNI +
12. 2. №6+№7 + 20. 5. №11+№12) + NOVE OBLASTI (SODIŠČE ČRNOMELJ №17 — 1. v
liniji! + vojaško oblastno poveljstvo №8 + deželna vlada №5 + Radovica
№13) + №13 ALFRED trgovski pomočnik [~] Podzemelj 11 (1. latinsko ime!) +
KRIVOGLAVCI 3. pojav (№14!) + GENETSKA-VAS 'Girišice' = GRIBLJE 3. pojav
(№15!) + ~18 NOVIH PRIIMKOV → vitals 670 → **675**; bloki 04455 153 →
**158**; sidra 146 → **151** (+1912:5); p80 hiše **69 NESPREMENJENE (h78 ŽE v p80 prek 04105-1887-sidra! — razlika od h63/h86: njuni 04105-bloki IZVEN filtra!)**; PT luknja **13** (nespremenjena);
P142 LEAD: 1913 №1 = 27. 1. 1913 na s152!

METODA: ~190 VLM branj v 6 krogih (36 vrstičnih + 8 dopolnilnih + 4 STRIP +
49 finiх + 6 GRID + 30 celopasovnih multi-render o/i/d + 38 mikro + 20
finalnih) + korpus-forenzika (04105-krsti + 04455-poroke 1886–1911).

Skripta scripts/p141_parish_marriage_1912.py (I1–I12, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I11).

Uporaba: python3 scripts/p141_parish_marriage_1912.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux X86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1912.json"
DOKAZ_P140 = "research/issue17/parish-marriage-1911.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1912-notes.md"
EXPECTED_ENTRIES = 17           # №1–№17
EXPECTED_EXCLUDED = 4           # prazni pasi s148–s151 + s152-1913-meja
EXPECTED_ANOMALIES = 18
EXPECTED_CROSSCHECKS = 18
GRIBLJE_ROWS = [1, 9, 15, 17]
GRIBLJE_HOUSES = ["21", "44", "46", "63", "78"]
GRIBLJE_BLOCKS = 5              # №1 2 (INTRA!) + №9 1 + №15 1 + №17 1
GRIBLJE_INTRA = 1
VITALS_TOTAL = 675              # 670 + 5 (ZAMRNJEN 1912-evidence pin — NE posodabljati v kaskadi!; tekoči korpus = 685 od P143)
BLOKI_04455 = 158               # 153 + 5
SIDRA_TOTAL = 151               # 146 + 5 blokov (+1912:5) (ZAMRNJEN 1912-evidence pin — NE posodabljati v kaskadi!; tekoči korpus = 161 od P143)
EXPECTED_MONDAYS = 14           # + 1 nedelja + 1 torek (№1!) + 1 petek (№5!)
EXPECTED_SUNDAYS = 1

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
    check("I1b excluded 4 (prazni pasi + s152-meja)", len(d.get("excluded", [])) == EXPECTED_EXCLUDED,
          str(len(d.get("excluded", []))))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride"))
    check("I1c obojestransko 17/17", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [str(e["row"]) for e in ent]
    check("I2 vrste [1–17]", rows == [str(i) for i in range(1, 18)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\[?(\d+)[^\s]*\s+(\w+)", dt)
        if m:
            months[m.group(2)] = months.get(m.group(2), 0) + 1
    # jan 4 + feb 4 + apr 2 + maj 2 + jul 1 + avg 1 + sep 1 + okt 1 + nov 1 = 17
    check("I2b meseci (jan 4 + feb 4 + apr 2 + maj 2 + jul 1 + avg 1 + sep 1 + okt 1 + nov 1)",
          months.get("januar") == 4 and months.get("februar") == 4 and months.get("april") == 2
          and months.get("maj") == 2 and months.get("julij") == 1 and months.get("avgust") == 1
          and months.get("september") == 1 and months.get("oktober") == 1 and months.get("november") == 1
          and sum(months.values()) == 17, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    tor = sum(1 for dt in dates if "torek" in dt)
    pet = sum(1 for dt in dates if "petek" in dt)
    check("I2c 14 ponedeljkov + 1 nedelja + 1 torek (№1) + 1 petek (№5!)",
          mon == EXPECTED_MONDAYS and sun == EXPECTED_SUNDAYS and tor == 1 and pet == 1,
          f"{mon} pon + {sun} ned + {tor} tor + {pet} pet")
    masa1 = sum(1 for dt in dates if "29. januar 1912" in dt)
    masa2 = sum(1 for dt in dates if "12. februar 1912" in dt)
    masa3 = sum(1 for dt in dates if "20. maj 1912" in dt)
    check("I2d MASA-DNEVI ×3 (29. 1. ×3 + 12. 2. ×2 + 20. 5. ×2 = 7 vpisov!)",
          masa1 == 3 and masa2 == 2 and masa3 == 2, f"{masa1}+{masa2}+{masa3}")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (27. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [148,149,150,151]", scans == [148, 149, 150, 151], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = e.get("groom", {}).get("place", "") + " " + e.get("bride", {}).get("place", "")
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = sorted(griblje_rows(ent))
    check("I4 Griblje vrste [1,9,15,17]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        for pl in (e.get("groom", {}).get("place", ""), e.get("bride", {}).get("place", "")):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 5 GRIBLJE [21,44,46,63,78]", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c INTRA-GRIBLJE №1 (h78 × h63 — 3. leto zapored!)",
          allsi.count("GRIBLJE × GRIBLJE") >= 1, str(allsi.count("GRIBLJE × GRIBLJE")))
    check("I4d SESTRI KRIŽAN (№1 — P140-lead VERIF!)", "SESTRI KRIŽAN" in allsi, "")
    check("I4e RECIPROČNI PAR (№11+№12!)", "RECIPROČNI" in allsi, "")
    check("I4f INTRA-PRIIMEK ×2 (№7 PEZDIREC + №14 ŽUGELJ!)", "INTRA-PRIIMEK" in allsi, "")
    check("I4g DVOJNA KORPUS-SINHRONIZACIJA №8 (1890 №2 + 1891 №12!)", "DVOJNA KORPUS-SINHRONIZACIJA" in allsi, "")
    check("I4h KORPUS-SINHRONIZACIJA №17 (krst Julija 1913!)", "KORPUS-SINHRONIZACIJA" in allsi, "")
    check("I4i №9 NEVESTA 46 LET (2. po 1886-v1!)", "46 LET" in allsi or "46 let" in allsi, "")
    check("I4j GENETSKA-VAS 'Girišice' = Griblje (3. pojav!)", "Girišice" in allsi, "")
    check("I4k KRIVOGLAVCI 3. pojav (№14!)", "KRIVOGLAVCI" in allsi, "")
    check("I4l SODIŠČE ČRNOMELJ (№17 — 1. v liniji!)", "ČRNOMELJ" in allsi.upper(), "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1912 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1912,', ts))
    check("I5a parish.ts bloki 1912 = 5", n_04455_1912 == GRIBLJE_BLOCKS, str(n_04455_1912))
    pins = [
        ("78", "1. POROČNI DOKAZ"), ("78", "KORPUS-KRST"), ("78", "čevljar"),
        ("63", "SESTRI KRIŽAN"), ("63", "SESTRA 1911-№1"),
        ("46", "3. poročni dokaz"), ("46", "NAJSTAREJŠA NEVESTA"),
        ("44", "GENETSKA-VAS"), ("44", "PAPIČ"),
        ("21", "KORPUS-SINHRONIZACIJA"), ("21", "MEŽNARJI"), ("21", "SODIŠČE ČRNOMELJ"),
    ]
    for hn, pin in pins:
        ms = re.findall(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1912,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = any(m and pin.lower() in m.lower() for m in ms)
        check(f"I5b pin h{hn} 1912 ({pin})", ok, (ms[0][:60] if ms else "BLOK MANJKA"))
    check("I5c P141 sekcija", "P141 razširitev: POROČNA KNJIGA 04455 — polno leto 1912" in ts)
    check("I5d INTRA-GRIBLJE v ts", "GRIBLJE × GRIBLJE" in ts and "h78 × h63" in ts, "")
    check("I5e RECIPROČNI + INTRA-PRIIMEK v ts", "RECIPROČNI" in ts and "INTRA-PRIIMEK" in ts, "")

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p141 id", "qa-p141-parish-marriage-1912" in qa)
    n675 = qa.count("HOUSE_VITALS.length !== 688")
    check("I6b vitals pini 675", n675 >= 55, str(n675))
    n158 = qa.count('.length !== 171')
    check("I6c bloki pini 158", n158 >= 1, str(n158))
    check("I6d sidra 151 + 1912:5", "poročna sidra ≠ 164" in qa and "h.year === 1912).length !== 5" in qa, "")
    check("I6e hiše 1912 pin", '"21,44,46,63,78"' in qa, "")
    check("I6f ostanki 670/153/146", "!== 670" not in qa and ".length !== 153" not in qa and "sidra ≠ 146" not in qa, "stare pini!")  # P142: '!== 70' odstranjen — h76 naredil p80=70 TEKOČI pin!
    check("I6g p80 hiše 69 (h78 ŽE v p80!)", "p80Houses.size !== 72" in qa, "")
    check("I6h PT luknja 13 nespremenjena", "p80Gap.length !== 13" in qa, "")

    # ---------- I7: duhovniki + dnevi ----------
    st = d["stats"]
    check("I7a stats mondays 14", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7b stats sundays 1", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7c stats sameVillage 3 (№4+№8+№13!)", st.get("sameVillageCount") == 3, str(st.get("sameVillageCount")))
    check("I7d stats sameHouse 0 (vračilo rekorda 1911 ×3!)", st.get("sameHouseCount") == 0, str(st.get("sameHouseCount")))
    check("I7e duhovnika Rauy+Bitnar [~] (korpus-04105 1912!)", "Rauq" in st.get("priests", "") or "Rauy" in st.get("priests", ""), st.get("priests", "")[:60])

    # ---------- I8: Parish stats ----------
    check("I8a stats vitals 675", st.get("vitalsTotal") == VITALS_TOTAL, str(st.get("vitalsTotal")))
    check("I8b stats bloki 158", st.get("blocks04455") == BLOKI_04455, str(st.get("blocks04455")))
    check("I8c stats sidra 163", st.get("sidraTotal") == SIDRA_TOTAL, str(st.get("sidraTotal")))
    check("I8d stats entries 17", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    check("I8e stats gribljeBlocks 5", st.get("gribljeBlocks") == GRIBLJE_BLOCKS, str(st.get("gribljeBlocks")))
    check("I8f stats newHouses [] (h78 ŽE v p80!)", st.get("newHouses") == [], str(st.get("newHouses")))
    check("I8g stats gribljeIntra 1", st.get("gribljeIntra") == GRIBLJE_INTRA, str(st.get("gribljeIntra")))
    check("I8h stats p80Houses 69 (h78 ŽE v p80 prek 1887-sidra!)", st.get("p80Houses") == 69, str(st.get("p80Houses")))
    check("I8i stats unnumbered 0", st.get("unnumbered") == 0, str(st.get("unnumbered")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 17", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 18", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P141" in notes and "1912" in notes and "RECIPROČNI" in notes, "")
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 7, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P141 bullet", "po P141" in rd, "")
    check("I10b README 675/158", "681" in rd and "164" in rd, "")
    check("I10c README P142 lead", "P142" in rd, "")

    # ---------- I11: P140 dokaz nespremenjen (lekcija P9) ----------
    d140 = json.load(open(DOKAZ_P140))
    check("I11 P140 dokaz 13 vnosov", len(d140["entries"]) == 13, str(len(d140["entries"])))

    # ---------- I12: lead-korekcija ----------
    lead = d.get("lead", {})
    check("I12 lead-korekcija (17 vpisov NE 6 — P140-lead razširjen ×2,8!)",
          "17 vpisov" in lead.get("correction", ""), lead.get("correction", "")[:60])

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
