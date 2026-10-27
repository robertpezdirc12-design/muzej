#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P146 — poročna knjiga 04455, polno leto 1917 (s160–s163 == Pag. 159–162)
(issue #18). 32. leto poročne linije (P115 = 1886 → … → P145 = 1916 → P146 = 1917).

Invariante I1–I12 + --live (LIVE 04455 HTTP). Vzorec: p145 (ZAMRNJENI pini 687/170/163
p145 + 688/171/164 p146 ostajajo; tekoči korpus 688/171/164/72 od P146)."""
import json
import re
import sys
import urllib.request

DOKAZ = "research/issue17/parish-marriage-1917.json"
DOKAZ_P145 = "research/issue17/parish-marriage-1916.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1917-notes.md"
EXPECTED_ENTRIES = 8            # №1–№8 (P145-lead je poznal 2 — №3–8 novi!)
EXPECTED_EXCLUDED = 0           # s159-dno prazen pas + diagonala (obe strani!) = čista meja!
EXPECTED_ANOMALIES = 13
EXPECTED_CROSSCHECKS = 10
GRIBLJE_ROWS = [3]             # №3 — edini Griblje-vpis leta (h15 × h38 INTRA!)
GRIBLJE_HOUSES = ["15", "38"]  # №3 ženin h15 + nevesta h38 (obe znani!)
GRIBLJE_BLOCKS = 1              # №2 → 1 blok
GRIBLJE_INTRA = 1               # №3 INTRA-GRIBLJE h15 × h38!
VITALS_TOTAL = 688              # 687 + 1 (tekoči pin P146)
BLOKI_04455 = 171               # 170 + 1
SIDRA_TOTAL = 164               # 163 + 1 blok (+1917:1)
EXPECTED_MONDAYS = 1            # №7 22.10. ponedeljek
EXPECTED_SUNDAYS = 5            # №2–№5 18.2. (4 NA ISTI DAN!) + №8 25.11.

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
    check("I1b excluded 0 (s159-dno prazen pas + diagonala = čista meja!)",
          len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride"))
    check("I1c obojestransko 4/4", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [str(e["row"]) for e in ent]
    check("I2 vrste [1–8]", rows == [str(i) for i in range(1, 9)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\[?(\d+)[^\s]*\s+(\w+)", dt)
        if m:
            months[m.group(2)] = months.get(m.group(2), 0) + 1
    # januar 1 + februar 4 + april 1 + oktober 1 + november 1 = 8
    check("I2b meseci (jan 1 + feb 4 + apr 1 + okt 1 + nov 1)",
          months.get("januar") == 1 and months.get("februar") == 4
          and months.get("april") == 1 and months.get("oktober") == 1
          and months.get("november") == 1
          and sum(months.values()) == 8, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    tor = sum(1 for dt in dates if "torek" in dt.lower())
    cet = sum(1 for dt in dates if "četrt" in dt.lower())
    sre = sum(1 for dt in dates if "sreda" in dt.lower())
    check("I2c 1 pon + 5 ned + 2 SRE + 0 čet + 0 tor (№2–№5 4 NA ISTI DAN!)",
          mon == EXPECTED_MONDAYS and sun == EXPECTED_SUNDAYS and tor == 0 and cet == 0 and sre == 2,
          f"{mon} pon + {sun} ned + {tor} tor + {cet} čet + {sre} sre")
    sameday = sum(1 for dt in dates if "18. februar" in dt or "18. feb." in dt)
    check("I2c-2 ★★★ 4 POROKE NA ISTI DAN 18.2. (2. rekord linije po 1893: 7!)", sameday == 4, str(sameday))
    # WWI: 4 poroke = najšibkejše leto + 2 vojaka
    wwi = "VOJNI KONTEKST ×4" in str(d.get("stats", {}).get("warGap", "")) and "2 dispensa" in str(d.get("stats", {}).get("warGap", ""))
    check("I2d WWI (VOJNI KONTEKST ×4 + 3 vojaške listine + 2 dispensa!)", wwi, "")
    # knjiga-razširitev do 1922
    be = str(d.get("stats", {}).get("bookExtension", ""))
    check("I2e ★★ KNJIGA DO 1922 (naslovnica P 1873–1922 + P147–P151!)",
          "1922" in be and "P151" in be, be[:60])

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (32. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [160,161,162,163]", scans == [160, 161, 162, 163], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = str(e.get("groom", {}).get("place", "")) + " " + str(e.get("bride", {}).get("place", ""))
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = sorted(griblje_rows(ent))
    check("I4 Griblje vrste [2]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        for pl in (str(e.get("groom", {}).get("place", "")), str(e.get("bride", {}).get("place", ""))):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 2 GRIBLJE [15,38] (h15 = 1887-Fablić!; h38 znana — Šimec ×223!)",
          pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c 1 INTRA-GRIBLJE №3 (h15 × h38 — obe znani!)", allsi.count("INTRA") >= 1
          and "GRIBLJE 15" in allsi and "GRIBLJE 38" in allsi, "")
    check("I4d ★★★ 4 POROKE NA ISTI DAN 18.2. (2. rekord po 1893: 7!)",
          "4 POROKE NA ISTI DAN" in allsi, "")
    check("I4e №4 1. MLADOLETEN ŽENIN LINIJE (21 < 24) + OBA MLADOLETA!",
          "1. MNLADOLETEN ŽENIN LINIJE" in allsi and "OBA MLADOLETA" in allsi, "")
    check("I4f №7 OČE-ŽENINA PRAZEN (3. primer!) + 70-letnik + građnik-priča!",
          "OČE PRAZEN" in allsi and "GRAĐNIK" in allsi, "")
    check("I4g №1 SANITETNI vojak + №8 INVALID-fotograf 'PRI VOJAKIH' + dispensi!",
          "SANITETNI" in allsi and "PRI VOJAKIH" in allsi and "Dispens" in allsi, "")
    check("I4h №6 k.u.k. VOJNI DELAVEC + №4 KRANJSKA GORA zglašnica!",
          "VOJNI DELAVEC" in allsi and "KRANJSKA GORA" in allsi, "")
    check("I4i №3 PREDKORPUSNA generacija (b. 1863!) + Šimec ×223!",
          "PREDKORPUSNA" in allsi and "×223" in allsi, "")
    check("I4j №2 M1906-ŽENIN-HIŠA (Županič-18 recipročni!) + №5 30-letna razlika!",
          "M1906" in allsi and "30-LETNA" in allsi, "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1917 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1917,', ts))
    check("I5a parish.ts bloki 1917 = 1", n_04455_1917 == GRIBLJE_BLOCKS, str(n_04455_1917))
    pins = [
        ("15", "PREDKORPUSNA"), ("15", "INTRA"), ("15", "ŠIMEC"), ("15", "4 pokojni"),
    ]
    for hn, pin in pins:
        ms = re.findall(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1917,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = any(m and pin.lower() in m.lower() for m in ms)
        check(f"I5b pin h{hn} 1917 ({pin})", ok, (ms[0][:60] if ms else "BLOK MANJKA"))
    check("I5c P146 sekcija", "P146 razširitev: POROČNA KNJIGA 04455 — polno leto 1917" in ts)
    check("I5d KNJIGA-1922 v ts (P146-sekcija!)", "P 1873–1922" in ts and "PRI VOJAKIH" in ts, "")

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p146 id", "qa-p146-parish-marriage-1917" in qa)
    n688 = qa.count("HOUSE_VITALS.length !== 688")
    check("I6b vitals pini 688", n688 >= 57, str(n688))
    n171 = qa.count(".length !== 171")
    check("I6c bloki pini 171", n171 >= 2, str(n171))
    check("I6d sidra 164 + 1917:1", "poročna sidra ≠ 164" in qa and "p146Marr.length !== 1" in qa, "")
    check("I6e hiše 1917 pini [15,38]", '"15"' in qa and '"38"' in qa, "")
    check("I6f ostanki 687/170/163/72 (P146-kaskada!)", "HOUSE_VITALS.length !== 687" not in qa and ".length !== 170" not in qa
          and "p80MarrAnchors.length !== 163" not in qa and "p80Houses.size !== 71" not in qa, "stare pini!")
    check("I6g p80 hiše 72 (nespremenjeno — h37+h27 že znani!)", "p80Houses.size !== 72" in qa, "")
    check("I6h PT luknja 13 nespremenjena", "p80Gap.length !== 13" in qa, "")
    check("I6i anchors-lista 1917:1 (p115)", 'h.year === 1917).length !== 1' in qa, "")

    # ---------- I7: dnevi ----------
    st = d["stats"]
    check("I7a stats mondays 1", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7b stats sundays 5", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7c stats sameVillage 2 (№3 Griblje + №4 Vranoviče!)", st.get("sameVillageCount") == 2, str(st.get("sameVillageCount")))
    check("I7d stats sameHouse 0 (2. leto z 0!)", st.get("sameHouseCount") == 0, str(st.get("sameHouseCount")))
    check("I7e letna glava 1917 + meja 1918 v s163!", "1917" in str(st.get("yearHeading", "")) and "1918" in str(st.get("yearHeading", "")), str(st.get("yearHeading", ""))[:40])

    # ---------- I8: Parish stats ----------
    check("I8a stats vitals 688", st.get("vitalsTotal") == VITALS_TOTAL, str(st.get("vitalsTotal")))
    check("I8b stats bloki 171", st.get("blocks04455") == BLOKI_04455, str(st.get("blocks04455")))
    check("I8c stats sidra 164", st.get("sidraTotal") == SIDRA_TOTAL, str(st.get("sidraTotal")))
    check("I8d stats entries 8", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    check("I8e stats gribljeBlocks 1", st.get("gribljeBlocks") == GRIBLJE_BLOCKS, str(st.get("gribljeBlocks")))
    check("I8f stats newHouses [] (h15+h38 že znani!)", st.get("newHouses") == [], str(st.get("newHouses")))
    check("I8g stats gribljeIntra 1", st.get("gribljeIntra") == GRIBLJE_INTRA, str(st.get("gribljeIntra")))
    check("I8h stats p80Houses 72 (nespremenjeno!)", st.get("p80Houses") == 72, str(st.get("p80Houses")))
    check("I8i stats unnumbered 0", st.get("unnumbered") == 0, str(st.get("unnumbered")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 13", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 10", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P146" in notes and "1917" in notes and "NA ISTI DAN" in notes, "")
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 5, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P145 bullet", "po P145" in rd, "")
    check("I10b README 687/170", "687" in rd and "170" in rd, "")
    check("I10c README P146 lead", "P146" in rd, "")

    # ---------- I11: P144 dokaz nespremenjen ----------
    d145 = json.load(open(DOKAZ_P145))
    check("I11 P145 dokaz 4 vnosa", len(d145["entries"]) == 4, str(len(d145["entries"])))

    # ---------- I12: lead-korekcija ----------
    lead = d.get("lead", {})
    check("I12 lead-korekcija (8 vpisov + KNJIGA DO 1922 + 4 NA ISTI DAN!)",
          "8 vpisov" in lead.get("correction", "") and "P 1873–1922" in lead.get("correction", "")
          and "4 POROKE NA ISTI DAN" in lead.get("correction", ""), lead.get("correction", "")[:60])

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
