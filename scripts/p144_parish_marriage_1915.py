#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P144 — poročna knjiga 04455, polno leto 1915 (s156 + s157 == Pag. 155–156)
(issue #18). 30. leto poročne linije (P115 = 1886 → … → P144 = 1915).

Invariante I1–I12 + --live (LIVE 04455 HTTP). Vzorec: p143 (ZAMRNJENI pini 681/164/157
p142 + 685/168/161 p143 ostajajo; tekoči korpus 686/169/162/72 od P144)."""
import json
import re
import sys
import urllib.request

DOKAZ = "research/issue17/parish-marriage-1915.json"
DOKAZ_P143 = "research/issue17/parish-marriage-1914.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1915-notes.md"
EXPECTED_ENTRIES = 6            # №1–№6
EXPECTED_EXCLUDED = 0           # s157-dno prazen pas + diagonala = čista meja!
EXPECTED_ANOMALIES = 13
EXPECTED_CROSSCHECKS = 10
GRIBLJE_ROWS = [1]             # №1 — edini Griblje-vpis leta (VOJNO LETO!)
GRIBLJE_HOUSES = ["82"]        # №1 h82 — ISTA-HIŠA!
GRIBLJE_BLOCKS = 1              # №1 h82 → 1 blok
GRIBLJE_INTRA = 1               # №1 INTRA-GRIBLJE ISTA-HIŠA h82 × h82!
VITALS_TOTAL = 686              # 685 + 1 (tekoči pin P144)
BLOKI_04455 = 169               # 168 + 1
SIDRA_TOTAL = 162               # 161 + 1 blok (+1915:1)
EXPECTED_MONDAYS = 1            # + 4 nedelje + 1 torek = 5/6 vikendov
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
    check("I1b excluded 0 (s157-dno prazen pas + diagonala = čista meja!)",
          len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride"))
    check("I1c obojestransko 6/6", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [str(e["row"]) for e in ent]
    check("I2 vrste [1–6]", rows == [str(i) for i in range(1, 7)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\[?(\d+)[^\s]*\s+(\w+)", dt)
        if m:
            months[m.group(2)] = months.get(m.group(2), 0) + 1
    # maj 1 + avgust 1 + september 2 + oktober 1 + november 1 = 6
    check("I2b meseci (maj 1 + avgust 1 + sep 2 + okt 1 + nov 1)",
          months.get("maj") == 1 and months.get("avgust") == 1
          and months.get("september") == 2 and months.get("oktober") == 1 and months.get("november") == 1
          and sum(months.values()) == 6, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    tor = sum(1 for dt in dates if "torek" in dt.lower())
    check("I2c 1 pon + 4 ned + 1 TOR №4 (5/6 vikendov — 3. torek po 1912 №1 + 1914 №7 — VOJAŠKI termin!)",
          mon == EXPECTED_MONDAYS and sun == EXPECTED_SUNDAYS and tor == 1,
          f"{mon} pon + {sun} ned + {tor} tor")
    # BREZ postne vrzeli — 1. leto brez (vojna: 1. poroka šele 2.5. = 4 tedne po veliki noči 4.4.1915!)
    nolent = any("2. maj" in dt for dt in dates) and "NI porok v postu" in str(d.get("stats", {}).get("lentGap", ""))
    check("I2d BREZ postne vrzeli (1. leto po 4-letni seriji 1911–1914 — vojna!)", nolent, "")
    # WWI: 10-mesečna vrzel + 3 vojaki
    wwi = "vojna" in str(d.get("stats", {}).get("warGap", "")).lower() and "3 VOJAKI" in str(d.get("stats", {}).get("warGap", ""))
    check("I2e WWI (10-mesečna vrzel 7.7.1914 → 2.5.1915 + 3 VOJAKI NA DOPUSTU = rekord!)", wwi, "")

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (30. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [156,157]", scans == [156, 157], str(scans))

    # ---------- I4: Griblje ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            pl = str(e.get("groom", {}).get("place", "")) + " " + str(e.get("bride", {}).get("place", ""))
            if re.search(r"GRIBLJE\s+\d+", pl):
                out.append(e["row"])
        return out

    g = sorted(griblje_rows(ent))
    check("I4 Griblje vrste [1]", g == GRIBLJE_ROWS, str(g))
    houses = []
    for e in ent:
        for pl in (str(e.get("groom", {}).get("place", "")), str(e.get("bride", {}).get("place", ""))):
            for m in re.findall(r"GRIBLJE\s+(\d+)", pl):
                houses.append(m)
    houses = sorted(set(houses), key=lambda x: int(x))
    pin_houses = sorted(set(GRIBLJE_HOUSES), key=lambda x: int(x))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b hiše 1 GRIBLJE [82] (vojno leto — edini Griblje-vpis!)", pin_houses == houses, f"dokaz {houses} vs pin {pin_houses}")
    check("I4c 1 INTRA-GRIBLJE ISTA-HIŠA №1 (h82 × h82 — 2. primer po 1914 №4!)",
          allsi.count("INTRA-GRIBLJE") >= 1 and "ISTA-HIŠA h82 × h82" in allsi, "")
    check("I4d №1 PAR-KRSTI 1916+1919 h82 (Ana + Peter — korpus!)", "PAR-KRST" in allsi, "")
    check("I4e №1 DVOTERNA (1887-krst neveste h52 oče PRAZEN + par-krsti h82!)", "DVOTERNA" in allsi, "")
    check("I4f №1 NEVESTA NEZAKONSKA (oče PRAZEN — korpus-exact!)", "NEZAKONSKA" in allsi, "")
    check("I4g №3 CIGANKA — 1. ROMSKA poroka linije!", "CIGANKA" in allsi and "oba cigana" in allsi, "")
    check("I4h 3 VOJAKI NA DOPUSTU (№3+№4+№6 — rekord!)", allsi.count("vojak na dopustu") + allsi.count("VOJAK NA DOPUSTU") >= 3, "")
    check("I4i FELDSUPERIORAT GRAZ (№3 soglasje + №4 Verkündmachtigungsschein!)", "Feldsuperiorat" in allsi or "FELDSUPERIORAT" in allsi or "Verkündmachtigungsschein" in allsi, "")
    check("I4j №3 ISTA-HIŠA Dobravice 48 × 48 (3. primer linije!)", "48 × 48" in allsi, "")
    check("I4k №6 KRANJSKA GORA (najbolj oddaljena oblast!)", "Kranjska Gora" in allsi or "KRANJSKA GORA" in allsi or "Kranj Gora" in allsi, "")

    # ---------- I5: parish.ts ----------
    ts = open(PARISH_TS).read()
    n_04455_1915 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1915,', ts))
    check("I5a parish.ts bloki 1915 = 1", n_04455_1915 == GRIBLJE_BLOCKS, str(n_04455_1915))
    pins = [
        ("82", "ISTA-HIŠA"), ("82", "PAR-KRST"), ("82", "DVOTERNA"), ("82", "NOVA p80-hiša"),
        ("82", "NEZAKONSKA"),
    ]
    for hn, pin in pins:
        ms = re.findall(rf'houseNo:\s*"{hn}",\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1915,.*?whatSi:\s*"([^"]*)"', ts, re.S)
        ok = any(m and pin.lower() in m.lower() for m in ms)
        check(f"I5b pin h{hn} 1915 ({pin})", ok, (ms[0][:60] if ms else "BLOK MANJKA"))
    check("I5c P144 sekcija", "P144 razširitev: POROČNA KNJIGA 04455 — polno leto 1915" in ts)
    check("I5d 3 VOJAKI NA DOPUSTU v ts (P144-sekcija!)", "3 VOJAKI NA DOPUSTU" in ts and ts.count("Verkündmachtigungsschein") >= 1, "")

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p144 id", "qa-p144-parish-marriage-1915" in qa)
    n686 = qa.count("HOUSE_VITALS.length !== 688")
    check("I6b vitals pini 686", n686 >= 57, str(n686))
    n169 = qa.count(".length !== 171")
    check("I6c bloki pini 169", n169 >= 2, str(n169))
    check("I6d sidra 162 + 1915:1", "poročna sidra ≠ 164" in qa and "p144Marr.length !== 1" in qa, "")
    check("I6e hiše 1915 pin", '"82"' in qa, "")
    check("I6f ostanki 686/169/162/71 (P145-kaskada!)", "HOUSE_VITALS.length !== 686" not in qa and ".length !== 169" not in qa
          and "p80MarrAnchors.length !== 162" not in qa and "p80Houses.size !== 71" not in qa, "stare pini!")
    check("I6g p80 hiše 72 (+h82!)", "p80Houses.size !== 72" in qa, "")
    check("I6h PT luknja 13 nespremenjena", "p80Gap.length !== 13" in qa, "")
    check("I6i anchors-lista 1915:1 (p115)", 'h.year === 1915).length !== 1' in qa, "")

    # ---------- I7: dnevi ----------
    st = d["stats"]
    check("I7a stats mondays 1", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7b stats sundays 4", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7c stats sameVillage 2 (№1+№3!)", st.get("sameVillageCount") == 2, str(st.get("sameVillageCount")))
    check("I7d stats sameHouse 2 (№1 h82 + №3 h48 — 2 novi ISTA-HIŠI!)", st.get("sameHouseCount") == 2, str(st.get("sameHouseCount")))
    check("I7e letna glava 1915/1916 (meja s157-dno diagonala!)", "1915" in str(st.get("yearHeading", "")) and "1916" in str(st.get("yearHeading", "")), str(st.get("yearHeading", ""))[:40])

    # ---------- I8: Parish stats ----------
    check("I8a stats vitals 686", st.get("vitalsTotal") == VITALS_TOTAL, str(st.get("vitalsTotal")))
    check("I8b stats bloki 169", st.get("blocks04455") == BLOKI_04455, str(st.get("blocks04455")))
    check("I8c stats sidra 162", st.get("sidraTotal") == SIDRA_TOTAL, str(st.get("sidraTotal")))
    check("I8d stats entries 6", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    check("I8e stats gribljeBlocks 1", st.get("gribljeBlocks") == GRIBLJE_BLOCKS, str(st.get("gribljeBlocks")))
    check("I8f stats newHouses [82]", st.get("newHouses") == ["82"], str(st.get("newHouses")))
    check("I8g stats gribljeIntra 1", st.get("gribljeIntra") == GRIBLJE_INTRA, str(st.get("gribljeIntra")))
    check("I8h stats p80Houses 72 (+h82!)", st.get("p80Houses") == 72, str(st.get("p80Houses")))
    check("I8i stats unnumbered 0", st.get("unnumbered") == 0, str(st.get("unnumbered")))

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 13", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 10", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P144" in notes and "1915" in notes and "CIGANKA" in notes, "")
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 5, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P144 bullet", "po P144" in rd, "")
    check("I10b README 686/169", "686" in rd and "169" in rd, "")
    check("I10c README P145 lead", "P145" in rd, "")

    # ---------- I11: P143 dokaz nespremenjen ----------
    d143 = json.load(open(DOKAZ_P143))
    check("I11 P143 dokaz 7 vnosov", len(d143["entries"]) == 7, str(len(d143["entries"])))

    # ---------- I12: lead-korekcija ----------
    lead = d.get("lead", {})
    check("I12 lead-korekcija (6 vpisov + 1. ROMSKA + 22.8.!)",
          "6 vpisov" in lead.get("correction", "") and "ROMSKA" in lead.get("correction", ""), lead.get("correction", "")[:60])

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
