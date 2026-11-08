#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P152 — SINTEZA poročne linije 04455 (1886–1922) = kuratorsko zaprtje knjige
(issue #18). 37. faza ZAPORED — 1. sintezna (NI novih branj!). Kompilacija 37
letnih dokazov (P115–P151) + preracun runtime-korpusa parish.ts: 592 evidence
vpisov · 195 linija-blokov + 2 pred-linijska (1882+1885) = 197 · zero-leta
1901+1918 · dobe: predvojna 442/15,79 · WWI 29/5,8 (kolaps!) · boom 121/30,25
(1919 rekord 40!) · max/min 40/4 · kalendarna (44 zabeleženih): PON 21 NED 13
SOB 0! · metrična razlika 127-vs-195 DOKUMENTIRANA · 1906 intra-datotečno
neskladje (6-vs-5-vs-kumulativ+5 — avtoritativno 5!). Vzorec: p146–p151
(I1–I12 + --live)."""
import json
import re
import sys
import urllib.request

DOKAZ = "research/issue17/parish-marriage-synthesis.json"
NOTES = "research/issue17/parish-marriage-synthesis-notes.md"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
README = "README.md"
YEARS = list(range(1886, 1923))

# ---- PINI (izračun P152; sinteza NE spreminja korpusa!) ----
EXPECTED_ENTRIES_TOTAL = 592
EXPECTED_AVG = 16.0
BLOCKS_TOTAL = 197
BLOCKS_LINE = 195
BLOCKS_PRE_LINE = 2
PRE_LINE_YEARS = [(1882, 1), (1885, 1)]
ZERO_BLOCK_YEARS = [1901, 1918]
VITALS = 714
ANCHORS = 190
HOUSES80 = 77
MAX_YEAR, MAX_ENTRIES = 1919, 40
MIN_ENTRIES = 4                      # 1916 + 1918!
MIN_YEARS = [1916, 1918]
ERA_PREWAR = (442, 162)              # 1886–1913 (28 let; avg 15,79)
ERA_WWI = (29, 7)                    # 1914–1918 (5 let; avg 5,8!)
ERA_BOOM = (121, 26)                 # 1919–1922 (4 leta; avg 30,25!)
DOW_RECORDED = {"PONEDELJEK": 21, "NEDELJA": 13, "SREDA": 4, "PETEK": 3, "TOREK": 2, "ČETRTEK": 1}
DOW_UNRECORDED = 548
STATS_METRIC_GRIBLJE = 127           # zgodnja metrika — DOKUMENTIRANA razlika!
GRIBLJE_BLOCK_KEY_YEARS = 23         # leta z gribljeBlocks*-ključi
ANOMALY_1906 = (6, 5)                # stats.gribljeBlocks=6 vs gribljeBlocksNew=5

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def main():
    live = "--live" in sys.argv

    # ---------- I1: dokaz-sinteza ----------
    d = json.load(open(DOKAZ))
    py = d["perYear"]
    check("I1 dokaz-sinteza 37 let", len(py) == 37, str(len(py)))
    check("I1a perYear leta 1886–1922 zapored", [p["year"] for p in py] == YEARS, "")
    etot = sum(p["entries"] for p in py)
    check("I1b evidence-vpisi 592", etot == EXPECTED_ENTRIES_TOTAL, str(etot))
    check("I1c avg 16,0", abs(sum(p["entries"] for p in py) / 37 - EXPECTED_AVG) < 0.01, "")
    btot = sum(p["blocks"] for p in py)
    check("I1d linija-bloki 195", btot == BLOCKS_LINE, str(btot))

    # ---------- I2: letna tabela (37 pinov!) ----------
    pinned = {1886: 24, 1887: 21, 1888: 20, 1889: 10, 1890: 16, 1891: 18, 1892: 15,
              1893: 20, 1894: 15, 1895: 16, 1896: 18, 1897: 18, 1898: 27, 1899: 9,
              1900: 8, 1901: 11, 1902: 6, 1903: 20, 1904: 15, 1905: 17, 1906: 12,
              1907: 12, 1908: 17, 1909: 15, 1910: 19, 1911: 13, 1912: 17, 1913: 13,
              1914: 7, 1915: 6, 1916: 4, 1917: 8, 1918: 4, 1919: 40, 1920: 37,
              1921: 31, 1922: 13}
    bad = [(p["year"], p["entries"], pinned[p["year"]]) for p in py if p["entries"] != pinned[p["year"]]]
    check("I2 letna tabela vpisov 37/37 pini", not bad, str(bad))
    badb = [(p["year"], p["blocks"], BPIN[p["year"]]) for p in py if p["blocks"] != BPIN[p["year"]]]
    check("I2b letna tabela blokov 37/37 pini", not badb, str(badb))

    # ---------- I3: ekstremi + zero-leta ----------
    mx = max(py, key=lambda p: p["entries"])
    check("I3a max 1919:40 (rekord!)", (mx["year"], mx["entries"]) == (MAX_YEAR, MAX_ENTRIES), f"{mx['year']}:{mx['entries']}")
    mins = sorted(p["year"] for p in py if p["entries"] == MIN_ENTRIES)
    check("I3b min 4 = [1916, 1918] (WWI-dno!)", mins == MIN_YEARS, str(mins))
    zb = sorted(p["year"] for p in py if p["blocks"] == 0)
    check("I3c zero-blok-leta [1901, 1918]", zb == ZERO_BLOCK_YEARS, str(zb))

    # ---------- I4: dobe ----------
    prew = [p for p in py if p["year"] <= 1913]
    wwi = [p for p in py if 1914 <= p["year"] <= 1918]
    boom = [p for p in py if p["year"] >= 1919]
    check("I4a predvojna 442 vpisov / 162 blokov",
          (sum(p["entries"] for p in prew), sum(p["blocks"] for p in prew)) == ERA_PREWAR, "")
    check("I4b WWI-kolaps 29 vpisov / 7 blokov (avg 5,8 = 37 %!)",
          (sum(p["entries"] for p in wwi), sum(p["blocks"] for p in wwi)) == ERA_WWI, "")
    check("I4c boom 121 vpisov / 26 blokov (avg 30,25!)",
          (sum(p["entries"] for p in boom), sum(p["blocks"] for p in boom)) == ERA_BOOM, "")

    # ---------- I5: kalendarna + metrike ----------
    cal = d["calendar"]["dayOfWeekRecorded"]
    check("I5a kalendarna PON 21 + NED 13 + SOB 0/44",
          cal.get("PONEDELJEK") == DOW_RECORDED["PONEDELJEK"] and cal.get("NEDELJA") == DOW_RECORDED["NEDELJA"]
          and cal.get("SOBOTA", 0) == 0, json.dumps(cal, ensure_ascii=False))
    check("I5b nezapisanih 548", d["calendar"]["dayOfWeekUnrecorded"] == DOW_UNRECORDED,
          str(d["calendar"]["dayOfWeekUnrecorded"]))
    check("I5c metrična razlika 127-vs-195 dokumentirana",
          d["totals"]["gribljeMarriagesStatsMetric"] == STATS_METRIC_GRIBLJE
          and "RAZLIKA METRIK" in d["totals"]["metricNote"], "")
    check("I5d metricsLegend 4 vrstice", len(d.get("metricsLegend", [])) == 4, "")

    # ---------- I6: pred-linijska bloka + korpuse-pini ----------
    pl = [(x["year"], x["blocks"]) for x in d["line"]["preLineBlocks"]]
    check("I6a pred-linija [(1882,1),(1885,1)]", pl == PRE_LINE_YEARS, str(pl))
    check("I6b korpuse-pini 714/197/190/77",
          d["totals"]["vitals"] == VITALS and d["totals"]["blocks04455Total"] == BLOCKS_TOTAL
          and d["totals"]["anchors"] == ANCHORS and d["totals"]["houses80"] == HOUSES80,
          "714/197/190/77")
    check("I6c naslovnica P-1873-1922", "1873–1922" in d["line"]["bookLabel"], "")

    # ---------- I7: 1906 anomala + honesty ----------
    hon = " ".join(d.get("honesty", []))
    check("I7a 1906-neskladje (6-vs-5-vs-kumulativ+5 — avtoritativno 5!)",
          f"{ANOMALY_1906[0]}" in hon and f"{ANOMALY_1906[1]}" in hon and "avtoritativno 5" in hon, "")
    check("I7b honesty ≥8", len(d.get("honesty", [])) >= 8, str(len(d.get("honesty", []))))
    check("I7c NI novih branj (MERI!)",
          any("NI novih paleografskih branj" in h for h in d.get("honesty", [])), "")
    check("I7d curatorial ≥8 zaključkov", len(d.get("curatorial", [])) >= 8, str(len(d.get("curatorial", []))))

    # ---------- I8: pomeri dokaze — gribljeBlocks*-ključi (23 let) ----------
    mism, present = [], 0
    for y in YEARS:
        dd = json.load(open(f"research/issue17/parish-marriage-{y}.json"))
        st = dd.get("stats", {})
        g = None
        for k in ("gribljeBlocks", "gribljeBlocksNew", "gribljeEntries"):
            if k in st:
                g = st[k]
                break
        if g is None:
            continue
        if isinstance(g, str):
            mm = re.findall(r"\d+", g)
            g = int(mm[0]) if mm else 0
        present += 1
        pin = dict(BPIN).get(y, 0)
        if int(g) != pin and y != 1906:      # 1906 = dokumentirana anomala (6 vs 5)!
            mism.append((y, g, pin))
    check("I8a 23 let z blok-ključi", present == GRIBLJE_BLOCK_KEY_YEARS, str(present))
    check("I8b ujemanja (brez 1906-anomale!)", not mism, str(mism))

    # ---------- I9: qa-parish qa-p152 ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I9a qa-p152-parish-marriage-synthesis (153. kontrola!)",
          "qa-p152-parish-marriage-synthesis" in qa, "")
    check("I9b qa-p152 pini 714/197/190/77",
          all(s in qa for s in ("!== 714", "!== 197", "!== 190", "!== 77")), "")
    check("I9c qa-p152 zero-leta 1901+1918", "1901" in qa and "1918" in qa, "")

    # ---------- I10: README + notes ----------
    rd = open(README, encoding="utf-8").read()
    check("I10a README po P152", "po P152" in rd, "")
    check("I10b README sinteza 592", "592" in rd, "")
    check("I10c README QA 153/153", "153/153" in rd, "")
    nt = open(NOTES, encoding="utf-8").read()
    check("I10d notes P152 obstajajo", "P152" in nt and "SYNTHESIS-M04455" in nt, "")

    # ---------- I11: kontinuiteta P115 + P151 ----------
    d1886 = json.load(open("research/issue17/parish-marriage-1886.json"))
    check("I11a P115-1886 kontinuiteta (24 vpisov!)", len(d1886["entries"]) == 24, "")
    d1922 = json.load(open("research/issue17/parish-marriage-1922.json"))
    check("I11b P151-1922 kontinuiteta (13 vpisov — KONEC!)", len(d1922["entries"]) == 13, "")
    check("I11c sinteza-vrsta SYNTHESIS-M04455", d["type"] == "SYNTHESIS-M04455", "")
    check("I11d openQuestions: odločitev uporabnika",
          any("odločitev uporabnika" in q for q in d.get("openQuestions", [])), "")

    # ---------- I12: veriga — p151 skripta + p151-dokaz pini ----------
    p151 = open("scripts/p151_parish_marriage_1922.py", encoding="utf-8").read()
    check("I12a p151 vitals-pin 714", "VITALS_TOTAL = 714" in p151, "")
    check("I12b p151 bloki-pin 197", "BLOKI_04455 = 197" in p151, "")
    p115 = open("scripts/p115_parish_marriage_1886.py", encoding="utf-8").read()
    check("I12c p115 anchors-pin 190 (kaskada)", "len(anchors) == 190" in p115, "")

    # ---------- L1–L2: live ----------
    if live:
        st_, body = http_get(BOOK_URL)
        check("L1 knjiga 04455 HTTP 200", st_ == 200, str(st_))
        check("L2 sinteza-neodvisnost: knjiga še vedno 'P 1873–1922' v notes/README",
              "1873–1922" in open(NOTES, encoding="utf-8").read(), "")

    # ---------- izpis ----------
    npass = sum(1 for _, ok, _ in results if ok)
    for name, ok, det in results:
        print(("PASS  " if ok else "FAIL  ") + name + (("  " + det) if det and not ok else ""))
    print(f"\nP152 --check{' --live' if live else ''}: {'PASS' if npass == len(results) else 'FAIL'}"
          f" — {npass}/{len(results)} — SINTEZA LINIJE 1886–1922 (37 let · 592 vpisov ·"
          f" 195+2 blokov · dobe 15,79/5,8/30,25 · max 1919:40 · min 4 [1916+1918] ·"
          f" zero-leta 1901+1918 · PON 21/44! · metrična razlika 127-vs-195 dokumentirana!)")
    sys.exit(0 if npass == len(results) else 1)


# bloki-po-letu pini (parish.ts runtime, P152 preracun)
BPIN = {1886: 7, 1887: 7, 1888: 4, 1889: 7, 1890: 4, 1891: 2, 1892: 4, 1893: 5,
        1894: 4, 1895: 5, 1896: 1, 1897: 9, 1898: 9, 1899: 6, 1900: 2, 1901: 0,
        1902: 4, 1903: 12, 1904: 8, 1905: 13, 1906: 5, 1907: 5, 1908: 9, 1909: 8,
        1910: 5, 1911: 6, 1912: 5, 1913: 6, 1914: 4, 1915: 1, 1916: 1, 1917: 1,
        1918: 0, 1919: 10, 1920: 4, 1921: 9, 1922: 3}

if __name__ == "__main__":
    main()
