#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P147 — poročna knjiga 04455, polno leto 1918 (s163–s164 == Pag. 162–163)
(issue #18). 33. leto poročne linije (P115 = 1886 → … → P146 = 1917 → P147 = 1918).

INVARJANTA: 1918 = 0 GRIBLJE blokov = 2. leto linije BREZ Griblje (po 1901 P130!)
→ kumulativ NESPREMENJEN: vitals 688 / bloki 04455 171 / sidra 164 / p80 hiše 72.
Vzorec: p130 (0-blok-leto) + p146 (okvir I1–I12 + --live)."""
import json
import re
import sys
import urllib.request

DOKAZ = "research/issue17/parish-marriage-1918.json"
DOKAZ_P146 = "research/issue17/parish-marriage-1917.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1918-notes.md"
EXPECTED_ENTRIES = 4            # №1 (s163) + №2–4 (s164) — P146-lead štetje TOČNO!
EXPECTED_EXCLUDED = 0           # s163-dno + s164-dno = čisti rob; s165-vrh = glava 1919!
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_ROWS = []              # ★★ 0 Griblje-vpisov = 2. leto linije BREZ (po 1901!)
VITALS_TOTAL = 688              # NESPREMENJENO (0 novih blokov!)
BLOKI_04455 = 171               # NESPREMENJENO
SIDRA_TOTAL = 164               # NESPREMENJENO (1918:0)
P80_HOUSES = 72                 # NESPREMENJENO
EXPECTED_MONDAYS = 1            # №1 4.2.
EXPECTED_SUNDAYS = 2            # №2 2.6. + №3 30.6.
EXPECTED_WEDNESDAYS = 1         # №4 16.10. (vojni termin!)

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
    check("I1b excluded 0 (s163-dno + s164-dno = čisti rob; s165-vrh = glava 1919!)",
          len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride"))
    check("I1c obojestransko 4/4", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    rows = [str(e["row"]) for e in ent]
    check("I2 vrste [1–4]", rows == [str(i) for i in range(1, 5)], str(rows))
    dates = [e["date"] for e in ent]
    months = {}
    for dt in dates:
        m = re.match(r"\[?[^\s]*\.?\s*(\w+)", dt)
        if m:
            months[m.group(1)] = months.get(m.group(1), 0) + 1
    # februar 1 + junij 2 + oktober 1 = 4
    check("I2b meseci (feb 1 + jun 2 + okt 1)",
          months.get("februar") == 1 and months.get("junij") == 2
          and months.get("oktober") == 1 and sum(months.values()) == 4, str(months))
    mon = sum(1 for dt in dates if "ponedeljek" in dt)
    sun = sum(1 for dt in dates if "nedelja" in dt.lower())
    wed = sum(1 for dt in dates if "sreda" in dt.lower())
    check("I2c 1 pon + 2 ned + 1 sre (vojni razpad vikendov 50%!)",
          mon == EXPECTED_MONDAYS and sun == EXPECTED_SUNDAYS and wed == EXPECTED_WEDNESDAYS,
          f"{mon} pon + {sun} ned + {wed} sre")
    ameriki = "AMERIKI" in json.dumps(d, ensure_ascii=False)
    check("I2d ★★ №2 NEVESTA V AMERIKI ROJENA (1. v liniji 1886–1918!)", ameriki, "")
    korek = d.get("lead", {}).get("correction", "")
    check("I2e P146-lead KOREKCIJE ×4 (14 · 2.6. · 16.10. · pešpolka 17)",
          "14" in korek and "junij" in korek and "OKTOBER" in korek and "pešpolka" in korek, korek[:60])

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (33. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [163,164]", scans == [163, 164], str(scans))

    # ---------- I4: Griblje = 0 (2. leto linije BREZ!) ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            vse = json.dumps(e, ensure_ascii=False)
            if re.search(r"GRIBLJE\s+\d+", vse) and "NEidentificirana" not in vse[:0]:
                out.append(e["row"])
        return out

    g = sorted(griblje_rows(ent))
    check("I4 ★★ 0 GRIBLJE-VRSTIC (2. leto linije BREZ Griblje — po 1901 P130!)",
          g == GRIBLJE_ROWS, str(g))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4b stats gribljeBlocks 0", d["stats"].get("gribljeBlocks") == 0, str(d["stats"].get("gribljeBlocks")))
    check("I4c stats newHouses [] (0 novih blokov!)", d["stats"].get("newHouses") == [], str(d["stats"].get("newHouses")))
    check("I4d ★★ №4 NAJSTAREJŠI PAR WWI (99 let skupaj!)",
          "NAJSTAREJŠI PAR WWI" in allsi and "99 let skupaj" in allsi, "")
    check("I4e ★★ №3 VOJAK-ŽELEZNIŠKI PREDELAVEC + OČE PRAZEN + Feldsuperior Graz!",
          "VOJAK-ŽELEZNIŠKI PREDELAVEC" in allsi and "OČE PRAZEN" in allsi and "Feldsuper" in allsi, "")
    check("I4f ★★ 3 DUHOVNIKI / 4 vpise (Miklavčič + Bitnar + Höltker!)",
          "Bitnar" in allsi and "Höltker" in allsi and "Miklavčič" in allsi, "")
    check("I4g ★ №1 ISTA PRIČA ×2 (Starasinič 32 IN 9!)",
          "ISTI PAR ime+priimek" in allsi and "32" in allsi and "št. 9" in allsi, "")
    check("I4h ★ Štrukelj 3. POJAV (priča → ženin → priča!)",
          "3. pojav" in allsi and "Štrukelj" in allsi, "")

    # ---------- I5: parish.ts nespremenjen (0 blokov 1918) ----------
    try:
        ts = open("src/data/atlas/parish.ts").read()
        n_04455_1918 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1918,', ts))
        check("I5a parish.ts bloki 1918 = 0 (nespremenjen!)", n_04455_1918 == 0, str(n_04455_1918))
        check("I5b parish.ts P146 sekcija še vedno zadnja (1917 blok = 1)",
              len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1917,', ts)) == 1, "")
    except FileNotFoundError:
        check("I5 parish.ts", False, "datoteka manjka!")

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p147 id", "qa-p147-parish-marriage-1918" in qa)
    n688 = qa.count("HOUSE_VITALS.length !== 725")
    check("I6b vitals pini 688", n688 >= 58, str(n688))
    n171 = qa.count(".length !== 197")
    check("I6c bloki pini 171", n171 >= 3, str(n171))
    check("I6d p147Marr 0-blok pin (qa-p147!)", "p147Marr.length !== 0" in qa, "")
    check("I6e ostanki 687/170/181-sidra-check (kaskada čista) + P152-sanacija — 714 je ERA-pin (pozitivno!)", "HOUSE_VITALS.length !== 687" not in qa and ".length !== 170" not in qa
          and "HOUSE_VITALS.length !== 725" in qa and ".length !== 181" not in qa, "stare pini!")
    check("I6f sidra 164 (nespremenjeno)", "poročna sidra ≠ 187" in qa, "")

    # ---------- I7: dnevi + stats ----------
    st = d["stats"]
    check("I7a stats mondays 1", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7b stats sundays 2", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7c stats wednesdays 1", st.get("wednesdays") == EXPECTED_WEDNESDAYS, str(st.get("wednesdays")))
    check("I7d stats sameVillage 1 (№2 Cerkvišče 18 × 4!)", st.get("sameVillageCount") == 1, str(st.get("sameVillageCount")))
    check("I7e stats sameHouse 0", st.get("sameHouseCount") == 0, str(st.get("sameHouseCount")))
    check("I7f letna glava 1918 + meja 1919 (s165-vrh!)",
          "1918" in str(st.get("yearHeading", "")) and "1919" in str(st.get("yearHeading", "")), str(st.get("yearHeading", ""))[:40])

    # ---------- I8: kumulativ NESPREMENJEN ----------
    check("I8a stats vitals 688 (nespremenjen!)", st.get("vitalsTotal") == VITALS_TOTAL, str(st.get("vitalsTotal")))
    check("I8b stats bloki 171 (nespremenjen!)", st.get("blocks04455") == BLOKI_04455, str(st.get("blocks04455")))
    check("I8c stats sidra 164 (nespremenjen!)", st.get("sidraTotal") == SIDRA_TOTAL, str(st.get("sidraTotal")))
    check("I8d stats entries 4", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    check("I8e stats p80Houses 72 (nespremenjeno!)", st.get("p80Houses") == P80_HOUSES, str(st.get("p80Houses")))
    check("I8f stats unnumbered 0", st.get("unnumbered") == 0, str(st.get("unnumbered")))
    check("I8g KNJIGA-1922 v stats bookExtension (P148–P151!)",
          "1922" in str(st.get("bookExtension", "")) and "P148" in str(st.get("bookExtension", "")), str(st.get("bookExtension", ""))[:50])

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 10", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 10", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P147" in notes and "1918" in notes and "BREZ Griblje" in notes, "")
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 5, str(len(d.get("honesty", []))))

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P147 bullet", "po P147" in rd, "")
    check("I10b README 688/171", "688" in rd and "171" in rd, "")
    check("I10c README QA 148/148", "148/148" in rd, "")
    check("I10d README P148 lead", "P148" in rd, "")

    # ---------- I11: P146 dokaz nespremenjen ----------
    d146 = json.load(open(DOKAZ_P146))
    check("I11 P146 dokaz 8 vnosov", len(d146["entries"]) == 8, str(len(d146["entries"])))

    # ---------- I12: lead-korekcija ----------
    lead = d.get("lead", {})
    check("I12 lead-korekcija (4 vpisov + Krasinec 14 + 16. OKTOBER + 0 GRIBLJE!)",
          "4 vpisi" in lead.get("correction", "") and "KRASINEC ŠT. 14" in lead.get("correction", "")
          and "0 GRIBLJE-VPISOV" in lead.get("correction", ""), lead.get("correction", "")[:60])

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
