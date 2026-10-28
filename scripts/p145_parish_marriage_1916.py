#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P145 — poročna knjiga 04455, polno leto 1916 (s158 + s159 == Pag. 157–158)
(issue #18). 31. leto poročne linije (P115 = 1886 → … → P144 = 1915 → P145 = 1916).

Invariante I1–I12 + --live (LIVE 04455 HTTP). Vzorec: p144 (ZAMRNJENI pini 686/169/162
p144 + 687/170/163 p145 ostajajo; tekoči korpus 687/170/163/72 od P145)."""
import json
import re
import sys
import urllib.request

DOKAZ = "research/issue17/parish-marriage-1916.json"
DOKAZ_P144 = "research/issue17/parish-marriage-1915.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1916-notes.md"
EXPECTED_ENTRIES = 4            # №1–№4 (P144-lead je poznal 3 — №4 nov!)
EXPECTED_EXCLUDED = 0           # s159-dno prazen pas + diagonala (obe strani!) = čista meja!
EXPECTED_ANOMALIES = 13
EXPECTED_CROSSCHECKS = 10
GRIBLJE_ROWS = [2]             # №2 — edini Griblje-vpis leta (VOJNO LETO — padec 6 → 4!)
GRIBLJE_HOUSES = ["37", "27"]  # №2 ženin h37 + nevesta h27 (Perdinčeva hiša — hišar!)
GRIBLJE_BLOCKS = 1              # №2 → 1 blok
GRIBLJE_INTRA = 1               # №2 INTRA-GRIBLJE h37 × h27!
VITALS_TOTAL = 687              # 686 + 1 (tekoči pin P145)
BLOKI_04455 = 170               # 169 + 1
SIDRA_TOTAL = 163               # 162 + 1 blok (+1916:1)
EXPECTED_MONDAYS = 1            # №4 6.11. ponedeljek
EXPECTED_SUNDAYS = 2            # №2 27.2. + №3 11.6.

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
    check("I2 vrste [1–4]", rows == [str(i) for i in range(1, 5)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\[?(\d+)[^\s]*\s+(\w+)", dt)
        if m:
            months[m.group(2)] = months.get(m.group(2), 0) + 1
    # januar 1 + februar 1 + junij 1 + november 1 = 4
    check("I2b meseci (jan 1 + feb 1 + jun 1 + nov 1)",
          months.get("januar") == 1 and months.get("februar") == 1
          and months.get("junij") == 1 and months.get("november") == 1
          and sum(months.values()) == 4, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    tor = sum(1 for dt in dates if "torek" in dt.lower())
    cet = sum(1 for dt in dates if "četrt" in dt.lower())
    check("I2c 1 pon + 2 ned + 1 ČET №1 (1. ČETRTEK LINIJE! — 3/4 vikendov)",
          mon == EXPECTED_MONDAYS and sun == EXPECTED_SUNDAYS and tor == 0 and cet == 1,
          f"{mon} pon + {sun} ned + {tor} tor + {cet} čet")
    # WWI: 4 poroke = najšibkejše leto + 2 vojaka
    wwi = "NAJŠIBKEJŠE LETO" in str(d.get("stats", {}).get("warGap", "")) and "2 VOJAKA" in str(d.get("stats", {}).get("warGap", ""))
    check("I2d WWI (4 poroke = NAJŠIBKEJŠE LETO linije 1915:6 → 4! + 2 VOJAKA)", wwi, "")
    # meja 1916/1917 v yearHeading
    yh = str(d.get("stats", {}).get("yearHeading", ""))
    check("I2e meja 1916/1917 (s159-dno diagonala + s160 = »1917«!)",
          "1916" in yh and "1917" in yh and "DIAGONALA" in yh, yh[:60])

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (31. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [158,159]", scans == [158, 159], str(scans))

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
    check("I4b hiše 2 GRIBLJE [27,37] (h27 = Perdinčeva — hišar!; h37 = 1825-cenzus 1.0!)",
          pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c 1 INTRA-GRIBLJE №2 (h37 × h27 — obe Griblje!)", allsi.count("INTRA") >= 1
          and "GRIBLJE 27" in allsi and "GRIBLJE 37" in allsi, "")
    check("I4d №2 TROJNA KORPUS-SINHRONIZACIJA (datum 27.2.1916 + r. 7.5.1893 + starša h29!)",
          "27. 2. 1916" in allsi and "7. 5. 1893" in allsi and "Kuhar?/Kuklar?" in allsi, "")
    check("I4e №2 3 POPRAVKE P144-leada (posestnik ≠ vdovec + 26 ≠ 37 + h27 ≠ h34!)",
          "PRAVKA POPRAVKA" in allsi, "")
    check("I4f №3 OČE-ŽENINA PRAZEN (2. primer linije po 1915 №1!)", "OČE PRAZEN" in allsi or "PRAZEN" in allsi, "")
    check("I4g №1 VOJAK 5. ARMADE — SOŠKA FRONTA (Ermächtigungsschein!)",
          "SOŠKA FRONTA" in allsi and "Ermächtigungsschein" in allsi, "")
    check("I4h №2+№4 DVE MLADOLETNI nevesti = REKORD LINIJE (22 + 20!)",
          allsi.count("MLADOLETNA") >= 2, "")
    check("I4i №3+№4 DVOTERNA hiša h4 VRANOVIČE (hišna veriga!)", "DVOTERNA hiša h4" in allsi, "")
    check("I4j №3 ROJ. GORJE (2. Gorenjska-žel. mobilnost po 1915 №6!)", "GORJE" in allsi, "")
    check("I4k №4 OTOVEC [~ 'Otorovec'] + obč. TALIČVRH [~] NEidentificirana!",
          "OTOVEC" in allsi and "TALIČVRH" in allsi, "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1916 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1916,', ts))
    check("I5a parish.ts bloki 1916 = 1", n_04455_1916 == GRIBLJE_BLOCKS, str(n_04455_1916))
    pins = [
        ("37", "TROJNA"), ("37", "MLADOLETNA"), ("37", "INTRA"),
        ("37", "PRAVKA POPRAVKA"), ("37", "PERDINČEVA"),
    ]
    for hn, pin in pins:
        ms = re.findall(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1916,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = any(m and pin.lower() in m.lower() for m in ms)
        check(f"I5b pin h{hn} 1916 ({pin})", ok, (ms[0][:60] if ms else "BLOK MANJKA"))
    check("I5c P145 sekcija", "P145 razširitev: POROČNA KNJIGA 04455 — polno leto 1916" in ts)
    check("I5d SOŠKA FRONTA v ts (P145-sekcija!)", "SOŠKA FRONTA" in ts and "Ermächtigungsschein" in ts, "")

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p145 id", "qa-p145-parish-marriage-1916" in qa)
    n687 = qa.count("HOUSE_VITALS.length !== 714")
    check("I6b vitals pini 687", n687 >= 57, str(n687))
    n170 = qa.count(".length !== 197")
    check("I6c bloki pini 170", n170 >= 2, str(n170))
    check("I6d sidra 163 + 1916:1", "poročna sidra ≠ 187" in qa and "p145Marr.length !== 1" in qa, "")
    check("I6e hiše 1916 pini [37,27]", '"37"' in qa and '"27"' in qa, "")
    check("I6f ostanki 686/169/162/71", "HOUSE_VITALS.length !== 686" not in qa and ".length !== 169" not in qa
          and "p80MarrAnchors.length !== 162" not in qa and "p80Houses.size !== 74" not in qa, "stare pini!")
    check("I6g p80 hiše 72 (nespremenjeno — h37+h27 že znani!)", "p80Houses.size !== 77" in qa, "")
    check("I6h PT luknja 13 nespremenjena", "p80Gap.length !== 13" in qa, "")
    check("I6i anchors-lista 1916:1 (p115)", 'h.year === 1916).length !== 1' in qa, "")

    # ---------- I7: dnevi ----------
    st = d["stats"]
    check("I7a stats mondays 1", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7b stats sundays 2", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7c stats sameVillage 2 (№3+№4 Vranoviče!)", st.get("sameVillageCount") == 2, str(st.get("sameVillageCount")))
    check("I7d stats sameHouse 0 (1. leto z 0 ISTA-HIŠA po 1913!)", st.get("sameHouseCount") == 0, str(st.get("sameHouseCount")))
    check("I7e letna glava 1916 + meja 1917", "1916" in str(st.get("yearHeading", "")) and "1917" in str(st.get("yearHeading", "")), str(st.get("yearHeading", ""))[:40])

    # ---------- I8: Parish stats ----------
    check("I8a stats vitals 687", st.get("vitalsTotal") == VITALS_TOTAL, str(st.get("vitalsTotal")))
    check("I8b stats bloki 170", st.get("blocks04455") == BLOKI_04455, str(st.get("blocks04455")))
    check("I8c stats sidra 163", st.get("sidraTotal") == SIDRA_TOTAL, str(st.get("sidraTotal")))
    check("I8d stats entries 4", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    check("I8e stats gribljeBlocks 1", st.get("gribljeBlocks") == GRIBLJE_BLOCKS, str(st.get("gribljeBlocks")))
    check("I8f stats newHouses [] (h37+h27 že znani!)", st.get("newHouses") == [], str(st.get("newHouses")))
    check("I8g stats gribljeIntra 1", st.get("gribljeIntra") == GRIBLJE_INTRA, str(st.get("gribljeIntra")))
    check("I8h stats p80Houses 72 (nespremenjeno!)", st.get("p80Houses") == 72, str(st.get("p80Houses")))
    check("I8i stats unnumbered 0", st.get("unnumbered") == 0, str(st.get("unnumbered")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 13", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 10", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P145" in notes and "1916" in notes and "SOŠKA" in notes, "")
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 5, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P145 bullet", "po P145" in rd, "")
    check("I10b README 687/170", "687" in rd and "170" in rd, "")
    check("I10c README P146 lead", "P146" in rd, "")

    # ---------- I11: P144 dokaz nespremenjen ----------
    d144 = json.load(open(DOKAZ_P144))
    check("I11 P144 dokaz 6 vnosov", len(d144["entries"]) == 6, str(len(d144["entries"])))

    # ---------- I12: lead-korekcija ----------
    lead = d.get("lead", {})
    check("I12 lead-korekcija (4 vpisov + 3 POPRAVKE + SOŠKA FRONTA!)",
          "4 vpisov" in lead.get("correction", "") and "PRAVKA POPRAVKA" in lead.get("correction", "")
          and "SOŠKA FRONTA" in lead.get("correction", ""), lead.get("correction", "")[:60])

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
