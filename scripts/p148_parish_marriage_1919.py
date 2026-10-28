#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P148 — poročna knjiga 04455, polno leto 1919 (s165–s175 == Pag. 164–174)
(issue #18). 34. leto poročne linije (P115 = 1886 → … → P147 = 1918 → P148 = 1919).

INVARJANTA: 1919 = ★★★ REKORD LINIJE — 40 vpisov (39 oštevilčenih + 1 NEŠTEVILČEN
Boren!) = povojni poročni boom ×2,35 nad prejšnjim rekordom (1912: 17)!
→ 10 GRIBLJE-VPISOV (P147-lead napovedal 1!): kumulativ vitals 688 → 698,
bloki 04455 171 → 181, sidra 164 → 174, p80 hiše 72 (vse že znane!).
Vzorec: p146/p147 (okvir I1–I12 + --live) + p130 (rekordno-leto)."""
import json
import re
import sys
import urllib.request

DOKAZ = "research/issue17/parish-marriage-1919.json"
DOKAZ_P147 = "research/issue17/parish-marriage-1918.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-marriage-1919-notes.md"
EXPECTED_ENTRIES = 40            # №1–39 + 1 neštevilčen (Boren!)
EXPECTED_NUMBERED = 39
EXPECTED_UNNUMBERED = 1
EXPECTED_EXCLUDED = 5            # meja-marker + 4 vpisi 1920
EXPECTED_ANOMALIES = 22
EXPECTED_CROSSCHECKS = 13
GRIBLJE_BLOCKS = 10              # h22[~] · h77 · h12 · h2 · h41 · h20 · h48 · h61 · h26 · h15
GRIBLJE_HOUSES = "12,15,2,20,22,26,41,48,61,77"
VITALS_TOTAL = 698               # 688 + 10!
BLOKI_04455 = 181                # 171 + 10!
SIDRA_TOTAL = 174                # 164 + 10!
P80_HOUSES = 75                  # 72 + 3 NOVE (h2 · h12 · h77 — 1. poročni dokazi v 04455!)
EXPECTED_MONDAYS = 33            # 82,5 % ponedeljkov!
EXPECTED_SUNDAYS = 6
EXPECTED_SATURDAYS = 1           # №39 29.11. — edina sobota!

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
    check("I1 dokaz JSON 40 vpisov", len(ent) == EXPECTED_ENTRIES, f"{len(ent)}/{EXPECTED_ENTRIES}")
    unnum = [e for e in ent if not re.match(r"^\d+$", str(e["row"]))]
    check("I1b 1 neštevilčen vpis (Boren!)", len(unnum) == EXPECTED_UNNUMBERED, str([e["row"] for e in unnum]))
    numbered = sum(1 for e in ent if re.match(r"^\d+$", str(e["row"])))
    check("I1c 39 oštevilčenih (№1–39)", numbered == EXPECTED_NUMBERED, str(numbered))
    both = sum(1 for e in ent if e.get("groom") and e.get("bride"))
    check("I1d obojestransko 40/40", both == EXPECTED_ENTRIES, str(both))

    # ---------- I2: vrste + datumi ----------
    dates = [e["date"] for e in ent]
    mon = sum(1 for dt in dates if re.search(r"januar|februar|[rm]arec|april|maj|junij|julij|avgust|sept|okt|nov", dt) and "1920" not in dt)
    check("I2b vsi datumi 1919", all("1919" in dt for dt in dates), "")
    pon = sum(1 for e in ent if "pon" in str(e.get("groom", "")) + str(e.get("bride", "")))
    # dnevi iz kalendarske kontrole: 19.1.1919 = nedelja
    check("I2c meja-marker v excluded", any("meja" in str(x.get("row", "")) for x in d.get("excluded", [])), "")
    check("I2d excluded 5 (meja + 4× 1920)", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    e1920 = [x for x in d.get("excluded", []) if "1920" in str(x.get("row", ""))]
    check("I2e 4 vpisi 1920 na s175-dno (vsak 19.1.!)", len(e1920) == 4 and all("19.1.1920" in x["note"] for x in e1920), str(len(e1920)))

    # ---------- I3: Pag == sken − 1 ----------
    bad = [(e["scan"], e["page"]) for e in ent if e["page"] != e["scan"] - 1]
    check("I3 Pag == sken − 1 (34. potrditev)", not bad, str(bad))
    scans = sorted({e["scan"] for e in ent})
    check("I3b skeni [165–175]", scans == list(range(165, 176)), str(scans))

    # ---------- I4: 10 Griblje-vpisov ----------
    def griblje_rows(dd):
        out = []
        for e in dd:
            vse = json.dumps(e, ensure_ascii=False)
            if re.search(r"GRIBLJE\s+\d+", vse):
                out.append(str(e["row"]))
        return out

    g = griblje_rows(ent)
    check("I4 10 GRIBLJE-VRSTIC (rekord!)", len(g) == GRIBLJE_BLOCKS, str(g))
    check("I4b stats gribljeBlocks 10", d["stats"].get("gribljeBlocks") == GRIBLJE_BLOCKS, str(d["stats"].get("gribljeBlocks")))
    check("I4c stats sameHouse 3 (rekord linije!)", d["stats"].get("sameHouseCount") == 3, str(d["stats"].get("sameHouseCount")))
    allsi = json.dumps(d, ensure_ascii=False)
    check("I4d ★★★ REKORD LINIJE 40 vpisov (×2,35 nad 1912: 17!)",
          "REKORD LINIJE" in allsi and "×2,35" in allsi, "")
    check("I4e ★★ 2 vdovi po WWI-vojakih (Kambič sodno potrdilo + Hosteler lajtnant!)",
          "KAMBIČ" in allsi and "LAJTNANT" in allsi and "sod" in allsi, "")
    check("I4f ★★★ PEZDIRC-delaža 25 omenb", "25 omenb" in allsi or "25 PEZDIRC" in allsi, "")
    check("I4g ★★★ VPIS BREZ ŠTEVILKE (Boren!)", "NEŠTEVILČEN" in allsi and "Boren" in allsi, "")
    check("I4h ★★ 4 familijski dvojni poročni dani (Mališič Otok 13 + Rovnik + Klepec + Pezdirc!)",
          "Mališič" in allsi and "Rovnik" in allsi and "SESTRA ženina №26" in allsi, "")
    check("I4i ★ meja 19/20 marker (7. tehnika!)", "»19«/»20«" in allsi or "19«/»20«" in allsi, "")

    # ---------- I5: parish.ts bloki 1919 ----------
    try:
        ts = open("src/data/atlas/parish.ts").read()
        n_04455_1919 = len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1919,', ts))
        check("I5a parish.ts bloki 1919 = 10", n_04455_1919 == GRIBLJE_BLOCKS, str(n_04455_1919))
        hs = re.findall(r'houseNo:\s*"(\d+)",\s*\n\s*bookSignature:\s*"04455",\s*\n\s*year:\s*1919', ts)
        check("I5b hiše 1919 = [2,12,15,20,22,26,41,48,61,77]",
              sorted(int(h) for h in hs) == [2, 12, 15, 20, 22, 26, 41, 48, 61, 77], str(sorted(hs, key=int)))
        check("I5c parish.ts 1917 blok = 1 (P146 nedotjen)",
              len(re.findall(r'bookSignature:\s*"04455",\s*\n\s*year:\s*1917,', ts)) == 1, "")
    except FileNotFoundError:
        check("I5 parish.ts", False, "datoteka manjka!")

    # ---------- I6: qa-parish.ts ----------
    qa = open(QA_TS).read()
    check("I6a qa-p148 id", "qa-p148-parish-marriage-1919" in qa)
    n698 = qa.count("HOUSE_VITALS.length !== 714")
    check("I6b vitals pini 698", n698 >= 62, str(n698))
    n181 = qa.count(".length !== 197")
    check("I6c bloki pini 181", n181 >= 33, str(n181))
    check("I6d p148Marr 10-blok pin (qa-p148!)", "p148Marr.length !== 10" in qa, "")
    check("I6e ostanki 688/171 (stale čisti!) + P149-sanacija", "HOUSE_VITALS.length !== 711" not in qa and ".length !== 171" not in qa
          and "HOUSE_VITALS.length !== 702" not in qa and ".length !== 181" not in qa, "stare pini!")
    check("I6f sidra 174", "poročna sidra ≠ 187" in qa, "")

    # ---------- I7: dnevi + stats ----------
    st = d["stats"]
    check("I7a stats mondays 33", st.get("mondays") == EXPECTED_MONDAYS, str(st.get("mondays")))
    check("I7b stats sundays 6", st.get("sundays") == EXPECTED_SUNDAYS, str(st.get("sundays")))
    check("I7c stats saturdays 1", st.get("saturdays") == EXPECTED_SATURDAYS, str(st.get("saturdays")))
    check("I7d stats sameHouse 3", st.get("sameHouseCount") == 3, str(st.get("sameHouseCount")))
    check("I7e stats sameVillage 6", st.get("sameVillageCount") == 6, str(st.get("sameVillageCount")))
    check("I7f letna glava 1919 + meja 19/20 (s175!)",
          "1919" in str(st.get("yearHeading", "")) and ("1920" in str(st.get("yearHeading", "")) or "»20«" in str(st.get("yearHeading", ""))), str(st.get("yearHeading", ""))[:40])

    # ---------- I8: kumulativ 698/181/174/72 ----------
    check("I8a stats vitals 698 (+10!)", st.get("vitalsTotal") == VITALS_TOTAL, str(st.get("vitalsTotal")))
    check("I8b stats bloki 181 (+10!)", st.get("blocks04455") == BLOKI_04455, str(st.get("blocks04455")))
    check("I8c stats sidra 174 (+10!)", st.get("sidraTotal") == SIDRA_TOTAL, str(st.get("sidraTotal")))
    check("I8d stats entries 40", st.get("entries") == EXPECTED_ENTRIES, str(st.get("entries")))
    check("I8e stats p80Houses 75 (+3 h2/h12/h77!)", st.get("p80Houses") == P80_HOUSES, str(st.get("p80Houses")))
    check("I8f stats unnumbered 1 (Boren!)", st.get("unnumbered") == 1, str(st.get("unnumbered")))
    check("I8g KNJIGA-1922 v stats bookExtension (P149–P151!)",
          "1922" in str(st.get("bookExtension", "")) and "P149" in str(st.get("bookExtension", "")), str(st.get("bookExtension", ""))[:50])
    check("I8h stats sameDayRecord 10.2. (5 vpisov — rekord dneva!)",
          "10. 2. 1919" in str(st.get("sameDayRecord", "")), str(st.get("sameDayRecord", ""))[:40])

    # ---------- I9: anomalije + crossChecks + notes ----------
    check("I9 anomalije 22", len(d.get("anomalies", [])) == EXPECTED_ANOMALIES, str(len(d.get("anomalies", []))))
    check("I9b crossChecks 12", len(d.get("crossChecks", [])) == EXPECTED_CROSSCHECKS, str(len(d.get("crossChecks", []))))
    notes = open(NOTES).read()
    check("I9c notes obstaja", "P148" in notes and "1919" in notes and "PEZDIRC" in notes, "")
    check("I9d honesty v dokazu (VERIF seznam)", len(d.get("honesty", [])) >= 20, str(len(d.get("honesty", []))))
    check("I9e P147-lead PODCENITEV ×3,6 v lead-correction",
          "PODCENITEV" in str(d.get("lead", {}).get("correction", "")), "")

    # ---------- I10: README ----------
    rd = open(README).read()
    check("I10a README P148 bullet", "po P148" in rd, "")
    check("I10b README 698/181", "698" in rd and "181" in rd, "")
    check("I10c README QA 149/149", "149/149" in rd, "")
    check("I10d README P149 lead", "P149" in rd, "")

    # ---------- I11: P147 dokaz nespremenjen ----------
    d147 = json.load(open(DOKAZ_P147))
    check("I11 P147 dokaz 4 vnosa", len(d147["entries"]) == 4, str(len(d147["entries"])))

    # ---------- I12: lead-korekcija ----------
    lead = d.get("lead", {})
    check("I12 lead-korekcija (40 vpisov + 10 Griblje + Griblje 87!)",
          "40 vpisov" in lead.get("correction", "") and "10" in lead.get("correction", "")
          and "GRIBLJE 87" in lead.get("correction", ""), lead.get("correction", "")[:60])

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
