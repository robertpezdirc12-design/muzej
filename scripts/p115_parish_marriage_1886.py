#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P115 — župnija Podzemelj: poročna knjiga 04455, polno leto 1886 (issue #18).

NOVA linija po zaključku krstne 04105 (P79–P114, 1886–1919)! Okvir P80
POTRJEN 1:1: skeni 61–65 == Pag. 60–64 (Pag. == sken − 1 v 61–66); **24 vpisov**
(razpored 3+5+7+5+4); meja na Pag. 60: vpis 22/1885 (Griblje 13 × 25 = P80
sidro h13) pod ločilnico »1 8 8 6«; glava 1887 na Pag. 65 (s66).

FAZA 2: **24/24 vpisov transkribiranih OBOJESTRANSKO** (starši/priče/
Urkunden/duhovnik). **P80 RE-READ POPRAVKI ×11** (max zoom + 1:1 primerjava
števk): h36→h56 (vpis 4) + h63→h65 (vpis 12; nevesta POŽEK iz GRIBLJ 64 =
NOVA hiša okvira!) + h15→h16 (vpis 17; h15 ostaja sidro 1887!) +
h25→PRILOŽJE 25 (vpis 20; izbrisan zapis pod vasjo!) + priimki: Klepec (11,
ne »Kukec«), Tomec (20, ne »Gomec«), Požek (12, ne »Peršić«), Pegdirec
(4/5/12/1885, ne »Perdinec«/»Podlirec«), Martin KRIŽAN Landwirth Krasinec 9
(23, ne »Marko Perzan, Vinica 9«), Straus (2, ne »Špelcer«).

NOVELE: 6 POROK NA ISTI DAN 15.2. (vpisi 3–8) + DVA SESTRSKA DVOJNA POROKA
(vpis 4+5 Pegdirec ISTEGA DNE z ISTIMI starši; vpis 9+21 Musié sestri, 9
mesecev) + vdove 4+1 (najmlajša 23 »Witwe Schweiger«!) + vpis 19 OBADVA
LEDIGA pri 43/42 (1. policist vzorca; »Podze-meč« = sicerptova pisava
Podzemelj) + MÜNDEL-timeline vpis 23 (mati † 7.9.1886 → hči 34 poročena
21.11. kot varovanka!) + prečrtano ~~Josef~~ vpis 24 (oče Josef Bufala) +
duhovnik franz Dovgan 9 podpisov (vpisi 1–3 + 20–24 + 1885; VPISI 4–19 (16!)
PRAZEN STOLPEC!) + dispensacije ×6 + Eheverlags-Contract vpis 22 + »Krasi-nec«
= prelom besede Krasinec + PEGDIREC-mreža ×7.

Excluded: 5 (sidro 1885 + 4× glava 1887). Skripta
scripts/p115_parish_marriage_1886.py (I1–I10, --check izpiše PASS/FAIL in vrne
exit code; --live omogoči HTTP preverjanje knjige/inventarja).
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES = 192
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1886.json"
DOKAZ_P114 = "research/issue17/parish-baptism-1919.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"

FRAME_SCANS = (61, 65)          # 61 = Pag. 60 (vpisi 1–3 + meja) – 65 = Pag. 64 (vpisi 21–24)
FRAME_PAGES = (60, 64)
EXPECTED_ENTRIES = 24
EXPECTED_EXCLUDED = 5
EXPECTED_ANOMALIES = 15
EXPECTED_CROSSCHECKS = 22
GRIBLJE_ROWS = [2, 4, 11, 12, 17, 23]
GRIBLJE_MARRIAGES = 6
GRIBLJE_HOUSES_TS = "16,25,31,56,60,65,71"
EXPECTED_WIDOWS = 4
EXPECTED_DISPENSATIONS = 6
EXPECTED_SIGNED = 9
EXPECTED_UNSIGNED = 15
EXPECTED_VITALS = 533           # P116: 528 + 5 novih poročnih blokov (h23/h37/h69/h3/h10)
BLOCKS_04455 = 164                # 7 okvir 1886 + sidra (P115) + … + 3 bloki 1895 (P124) + 3 bloki 1896 (P125) + 9 blokov 1897 (P126) + 2 bloka 1900 (P129) + 11 blokov 1903 (P132)
DATE_COUNTS = {"januar": 2, "februar": 10, "marec": 3, "april": 0, "maj": 1,
               "junij": 1, "julij": 0, "avgust": 2, "september": 0, "oktober": 0,
               "november": 5, "december": 0}
# P115 popravki P80 (blok-houseNo → obvezen pin v whatSi)
BLOCK_PINS = [
    ("31", "STRAUS"), ("31", "Papič"), ("31", "franz Dovgan"),
    ("56", "PEGDIREC"), ("56", "SESTRIN+BRAT"), ("56", "BREZ PODPISA"),
    ("60", "KLEPEC"), ("60", "BREZ PODPISA"),
    ("65", "POŽEK"), ("65", "GRIBLJE 64"), ("65", "BREZ PODPISA"),
    ("16", "GRIBLJE 16"), ("16", "h15 še vedno sidro 1887"), ("16", "BREZ PODPISA"),
    ("25", "PRILOŽJE 25"), ("25", "Klepec"), ("25", "TOMEC"),
    ("71", "Martin KRIŽAN"), ("71", "MÜNDEL"), ("71", "Landwirth"),
]
# stara P80 branja = IZTEKLA iz 04455 blokov (natančni fragmenti)
OLD_READINGS = [
    "Dorothea Perdinec", "Perdinec [~], 30, Krasinec 38", "Mathias Kukec",
    "Katharina Peršić", "Marko Perzan [~]", "Martin Pavie", "Gasthausmeister [~]",
    "Vinica 9;", "Vinica 10 rad.", "Maria née Podlirec", "née Stabek",
    "bivališče neveste nečitljivo", "GRIBLJE 63", "GRIBLJE 36 (starši",
]


def http_get(url, headers=None, tries=3):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers or UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except Exception as e:  # noqa: BLE001
            last = e
    raise last


def main() -> int:
    live = "--live" in sys.argv
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    # ---------- I1: dokaz JSON ----------
    try:
        d = json.load(open(DOKAZ))
    except Exception as e:  # noqa: BLE001
        print(f"I1 FAIL: {e}")
        return 1
    check("I1 json obstaja", True, DOKAZ)
    check("I1b entries=24", len(d["entries"]) == EXPECTED_ENTRIES, f"{len(d['entries'])}")
    check("I1c excluded=5", len(d["excluded"]) == EXPECTED_EXCLUDED, f"{len(d['excluded'])}")
    check("I1d anomalije=15", len(d["anomalies"]) == EXPECTED_ANOMALIES, f"{len(d['anomalies'])}")
    check("I1e crossChecks=22", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, f"{len(d['crossChecks'])}")
    # vsi vpisi imajo obojestransko transkripcijo (starši obeh + priče + urkunden + duhovnik)
    bad = [e["row"] for e in d["entries"]
           if not e.get("parentsGroom") or not e.get("parentsBride") or not e.get("witnesses")
           or not e.get("urkunden") or not e.get("priest")]
    check("I1f obojestransko (24/24)", not bad, str(bad) if bad else "vse ✓")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 entries=24", fr.get("entriesTotal") == EXPECTED_ENTRIES, str(fr.get("entriesTotal")))
    check("I2b skeni 61–65", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2c strani 60–64", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))
    rows = [e["row"] for e in d["entries"]]
    check("I2d vrstice 1–24 zapored", rows == list(range(1, 25)), str(rows))
    sc = [e["scan"] for e in d["entries"]]
    check("I2e skeni znotraj 61–65", all(61 <= s <= 65 for s in sc), str(sorted(set(sc))))
    # razpored po straneh 3+5+7+5+4
    per = {}
    for e in d["entries"]:
        per[e["scan"]] = per.get(e["scan"], 0) + 1
    check("I2f razpored 3+5+7+5+4",
          [per.get(s, 0) for s in (61, 62, 63, 64, 65)] == [3, 5, 7, 5, 4], str(per))

    # ---------- I3: Griblje vpisi + nova hiša 64 ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [2,4,11,12,17,23] (vpis 20 → Priložje!)", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 6", d["stats"].get("gribljeMarriages") == GRIBLJE_MARRIAGES, str(d["stats"].get("gribljeMarriages")))
    check("I3b hiš omenjenih = 8 (vključno h64 nevesta!)", d["stats"].get("gribljeHousesMentioned") == 8,
          str(d["stats"].get("gribljeHousesMentioned")))
    e12 = next(e for e in d["entries"] if e["row"] == 12)
    check("I3c vpis 12 = h65 × Požek × h64",
          e12["groom"]["houseNo"] == 65 and "Požek" in e12["bride"]["name"] and e12["bride"]["houseNo"] == 64,
          str(e12["groom"]["houseNo"]) + "/" + e12["bride"]["name"] + "/" + str(e12["bride"]["houseNo"]))
    e20 = next(e for e in d["entries"] if e["row"] == 20)
    check("I3d vpis 20 = PRILOŽJE 25", "PRILOŽJE" in e20["groom"]["village"] and e20["groom"]["houseNo"] == 25,
          e20["groom"]["village"])
    e23 = next(e for e in d["entries"] if e["row"] == 23)
    check("I3e vpis 23 = Martin Križan × Mündel",
          "KRIŽAN" in e23["groom"]["name"].upper() and "MÜNDEL" in e23["bride"]["status"].upper(),
          e23["groom"]["name"] + " × " + e23["bride"]["status"])

    # ---------- I4: datumi + meseči ----------
    mc = d["stats"].get("dateCounts", {})
    bad_m = {k: (v, DATE_COUNTS[k]) for k, v in mc.items() if DATE_COUNTS.get(k) != v}
    check("I4 meseči (vsota 24)", not bad_m and sum(mc.values()) == 24, str(bad_m or sum(mc.values())))
    winter = mc.get("januar", 0) + mc.get("februar", 0) + mc.get("marec", 0)
    check("I4b zimska koncentracija 15 (62.5%)", winter == 15, str(winter))
    e9 = next(e for e in d["entries"] if e["row"] == 9)
    check("I4c vpis 9 ZUNAJ VRSTNEGA REDA (24.1.)", "ZUNAJ VRSTNEGA REDA" in e9["date"], e9["date"])
    feb15 = [e["row"] for e in d["entries"] if e["date"].startswith("15.2.1886")]
    check("I4d 6 porok 15.2. = [3..8]", feb15 == [3, 4, 5, 6, 7, 8], str(feb15))

    # ---------- I5: stats ključne številke ----------
    st = d["stats"]
    check("I5 vdove=4", st.get("widows") == EXPECTED_WIDOWS, str(st.get("widows")))
    check("I5b dispensacije=6", st.get("dispensations") == EXPECTED_DISPENSATIONS, str(st.get("dispensations")))
    check("I5c Dovgan podpisi=9", st.get("priestSigned") == EXPECTED_SIGNED, str(st.get("priestSigned")))
    check("I5d brez podpisa=15", st.get("priestUnsigned") == EXPECTED_UNSIGNED, str(st.get("priestUnsigned")))
    check("I5e vitals=528 (P115 dokaz; P116 533)", st.get("vitals") == 528, str(st.get("vitals")))
    check("I5f bloki 04455=11 (P115 dokaz; P116 +5 → 16)", st.get("blocks04455") == 11, str(st.get("blocks04455")))
    check("I5g popravki P80=8", st.get("p80BlocksCorrected") == 8, str(st.get("p80BlocksCorrected")))

    # ---------- I6: anomalije A1–A15 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A15", ids == [f"A{i}" for i in range(1, 16)], str(ids))
    a2 = next((a for a in d["anomalies"] if a["id"] == "A2"), {})
    check("I6b A2 = sestrski dvojni poroki", "Pegdirec" in a2.get("summary", "") and "Musié" in a2.get("summary", ""))
    a5 = next((a for a in d["anomalies"] if a["id"] == "A5"), {})
    check("I6c A5 = Mündel-timeline", "MÜNDEL" in a5.get("summary", "").upper() and "7.9.1886" in a5.get("summary", ""))
    a12 = next((a for a in d["anomalies"] if a["id"] == "A12"), {})
    check("I6d A12 = P80 popravki ×11", "×11" in a12.get("summary", ""))

    # ---------- I7: crossChecks ----------
    cc_ok = [c for c in d["crossChecks"] if c["verdict"].startswith("✓")]
    check("I7 crossChecks ✓ ≥ 15", len(cc_ok) >= 15, f"{len(cc_ok)}/{len(d['crossChecks'])}")
    cc8 = next((c for c in d["crossChecks"] if c.get("id") == "CC8"), {})
    check("I7b CC8 = Priložje", "PRILOŽJE" in cc8.get("verdict", ""), cc8.get("verdict", "")[:60])

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 94 (P116 +5, P117 +4, P118 +7, P119 +4, P120 +2 + P123 +4 + P124 +3 + P125 +3 + P126 +9 + P127 +9 + P128 +6 + P129 +2! + P131 +4 + P132 +12!)", len(blocks_m) == BLOCKS_04455, str(len(blocks_m)))
    h1886 = sorted((h for h, y, _ in blocks_m if y == "1886"), key=int)
    check("I8b hiše 1886 = [16,25,31,56,60,65,71]", ",".join(h1886) == GRIBLJE_HOUSES_TS, ",".join(h1886))
    anchors = [(h, y, s) for h, y, s in blocks_m if y != "1886"]
    check("I8c sidra 95 (… 1895×5 · 1896×1 · 1897×9 · 1898×9 · 1900×2 · 1902×4 · 1903×12 — P124 +3 + P125 +3 + P126 +9 + P127 +9 + P128 +6 + P129 +2 + P131 +4 + P132 +12!)",
          len(anchors) == 157 and sorted((y for _, y, _ in anchors)) == ["1882", "1885"] + ["1887"] * 7 + ["1888"] * 4 + ["1889"] * 7 + ["1890"] * 4 + ["1891"] * 2 + ["1892"] * 4 + ["1893"] * 5 + ["1894"] * 4 + ["1895"] * 5 + ["1896"] * 1 + ["1897"] * 9 + ["1898"] * 9 + ["1899"] * 6 + ["1900"] * 2 + ["1902"] * 4 + ["1903"] * 12 + ["1904"] * 8 + ["1905"] * 13 + ["1906"] * 5 + ["1907"] * 5 + ["1908"] * 9 + ["1909"] * 8 + ["1910"] * 5 + ["1911"] * 6 + ["1912"] * 5 + ["1913"] * 6
          and any(s == "50" for _, y, s in anchors if y == "1882"),
          str(anchors))
    # pini novih brani
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1886,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin in m.group(4):
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8d pini P115 (20)", not missing, str(missing) if missing else "vse ✓")
    whatsis = [m.group(2) for m in re.finditer(r'bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*\d+,\s*page:\s*\d+,\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S) if int(m.group(1)) <= 1910]  # P140: leto <= 1910 ('GRIBLJE 63' je od 1911 PONOVNO VELJAVNA hiša — №1 nevesta h63!)
    stale = [o for o in OLD_READINGS if any(o in w for w in whatsis)]
    check("I8e stara branja iztekla", not stale, str(stale) if stale else "vse ✓")

    # ---------- I9: qa-p115 ----------
    qa = open(QA_TS).read()
    check("I9 qa-p115", '"qa-p115-parish-marriage-1886"' in qa)
    check("I9b qa-p115 hiše 1886", "16,25,31,56,60,65,71" in qa)
    # vitals 528 regresijska zaščita v qa-p115
    check("I9c vitals 637 zaščita (P129)", "HOUSE_VITALS.length !== 681" in qa[qa.index("const p115Marr"):])

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P115", "P115" in rd and ("124/124" in rd or "po P123" in rd))
    nt = open("research/issue17/parish-marriage-1886-notes.md").read()
    check("I10b notes faza 2", "FAZA 2 — ZAKLJUČENA" in nt and "PRILOŽJE 25" in nt)

    # ---------- live ----------
    if live:
        st_, body = http_get(BOOK_URL)
        check("I11 live knjiga 200", st_ == 200, str(st_))
        m = re.search(r'"files":\s*\[(.*?)\]', body.decode("utf-8", "ignore"), re.S)
        n = len(re.findall(r'/image/', m.group(1))) if m else 0
        check("I11b slike = 192", n == EXPECTED_IMAGES, str(n))

    # ---------- izpis ----------
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    print(f"\n{passed}/{total} PASS")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
