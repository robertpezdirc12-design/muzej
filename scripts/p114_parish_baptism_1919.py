#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P114 — župnija Podzemelj: krstna knjiga 04105, polno leto 1919 (issue #18).

ZAKLJUČEK krstne linije 1886–1919 (34 let)! Okvir: velika ročna glava
»Anno 1919« VRH str. 263 = s311; str. 263–275 == skeni 311–324; **79 vpisov
(l1–l78 + DUPLA labela »31« — napaka številčenja!)** + **BREZ zaključne
opombe** (vojno leto). s321 = DUP-FOTO s320 (bela listina prepognjena —
razkriti starši l56–l59!). s325 = prazna tiskana stran + **PRILEPEN DOPIS
ŠKOFIJSKEGA ORDINARIATA v Ljubljani (25.6.1919, č. 2908) — popravek Jakoba
Košca (roj. 14.4.1917, NE 1.5.1917; napačen vpis v Metliki!)** = l27
(naknadni vpis »Leto 1917, krčen v Metliki 18.5.1919«). s326 = zadnja
platnica »Podzemelj R 1886–1919«.

VSI vpisi z Griblji: **11 vpisov / 11 hiš — NARE 10/11 + 1 NOVA hiša (h81!)
— čisto leto (P110–P113 ×4) se konča pri 4!** NOVELE 1919: BELA LISTINA =
legitimizacijsko pismo (Bohumil Šponiček, Bahnhof Ljube bei Fiume, 1.8.1915
— otrok Emil krščen 16.7.1915; starša poročena 1907 Zagreb!) + EMŠO
kampanja ~34 žigov = REKORD (27 ✓ datumsko + 6 dvomov + l57 PRAZEN
»EMŠO je:« + l75 12-mestni!) + 4 RAZVELJAVITVE ZAKONA = REKORD (Zagreb
1948 + NM 1982 + l40 + Ljubljana 1958 s priimkom TRILAR!) + 5 DUHOVNIKOV =
REKORD (Cerar župnik + Učak + Lopar + Rogar kaplani + Katanov barban
Metlika!) + 19 VPIS PRENEŠEN = REKORD + PRIIMEK BRINC marg + NEZAKONSKI ×3
+ MRTVOROJEN ×1 (l69, brez imena!) + † 12 (l78 † 30.1.1945 UBITA OD
BOMBARDIRANJA = ZADNJI VPIS KNJIGE!) + tuje države ×8 (Rijeka, Zagreb,
Beograd, AMERIKA!, Ohio, Pag, Graz) + 2 neznani vasi (Okljuka, Trilovje?)
+ KAPLJIŠČE 1. pojav + kumulativ **509 vpisov / 88 hiš / 34 let**
(1886–1919; 528 vitals).

Excluded: 70. Skripta scripts/p114_parish_baptism_1919.py (I1–I12,
--check izpiše PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
knjige/inventarja).
"""
import json
import re
import sys
import base64
import urllib.request
import urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/"
BOOK_SIGNATURE = "04105"
EXPECTED_IMAGES = 326
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-baptism-1919.json"
DOKAZ_P113 = "research/issue17/parish-baptism-1918.json"
PARISH_TS = "src/data/atlas/parish.ts"

FRAME_SCANS = (311, 324)        # 311 = str. 263 (glava 1919 + l1–l6) – 324 = str. 275 (l74–l78, brez zaključne opombe)
FRAME_PAGES = (263, 275)
EXPECTED_ENTRIES = 11
EXPECTED_DISTINCT = 11
EXPECTED_EXCLUDED = 70
EXPECTED_ROWS_TOTAL = 79        # 78 label + dup »31«
EXPECTED_ROWS_1919 = 77         # rojenih 1919 (l27 = 1917!)
EXPECTED_STRUCK = 0
EXPECTED_NUMERIC_HOUSES = sorted([5, 6, 8, 40, 46, 47, 48, 81, 82, 88, 90])
EXPECTED_NEW_HOUSES = 1         # h81!
EXPECTED_VITALS_TOTAL = 528     # 517 + 11 (P114)
BLOCKS_04105 = 502              # 491 + 11
KUMULATIV_ENTRIES = 614         # 603 + 11 (krstna linija 1886–1919, po P113 metodi)
KUMULATIV_HOUSES = 88           # 87 + h81
KUMULATIV_YEARS = 34            # 1886–1919
# kontinuitete (hiša → zadnje krstno leto pred 1919 v 04105, iz parish.ts)
CONTINUITY = {
    "8": 1914, "47": 1913, "88": 1917, "46": 1917,
    "90": 1914, "82": 1916, "48": 1914, "40": 1915,
    "6": 1913, "5": 1917,
}
# dup-novela: stran == sken − 48, RAZEN s321 (dup str. 272!)
PAGE_OF_SCAN = {
    311: 263, 312: 264, 313: 265, 314: 266, 315: 267,
    316: 268, 317: 269, 318: 270, 319: 271, 320: 272,
    321: 272, 322: 273, 323: 274, 324: 275,
}
# sidra/pini P114 (label, scan, hiša, pin-fragment v whatSi):
ANCHORS = [
    (10, 312, "8", "2603919505488"),
    (15, 313, "47", "h47"),
    (26, 315, "88", "1605919505381"),
    (31, 315, "46", "h46"),
    (40, 317, "82", "h82"),
    (44, 318, "48", "3108919505332"),
    (46, 318, "40", "h40"),
    (47, 318, "81", "NOVA HIŠA"),
    (73, 323, "6", "h6"),
    (75, 324, "5", "h5"),
]
# EMŠO datumski sidri (labela, datum rojstva po registru, EMŠO DDMM iz žiga):
EMSO_DATE_CHECKS = [
    (1, "1.1.1919", "0101"), (2, "13.1.1919", "1301"), (5, "5.2.1919", "0502"),
    (6, "20.2.1919", "2002"), (9, "20.3.1919", "2003"), (10, "26.3.1919", "2603"),
    (14, "23.3.1919", "2303"), (16, "10.4.1919", "1004"), (17, "14.4.1919", "1404"),
    (19, "20.4.1919", "2004"), (23, "8.5.1919", "0805"), (26, "16.5.1919", "1605"),
    (28, "30.5.1919", "3005"), (39, "15.8.1919", "1508"), (40, "19.8.1919", "1908"),
    (44, "31.8.1919", "3108"), (47, "9.9.1919", "0909"), (49, "13.9.1919", "1309"),
    (53, "28.9.1919", "2809"), (55, "30.9.1919", "3009"), (56, "30.9.1919", "3009"),
    (58, "6.10.1919", "0610"), (59, "7.10.1919", "0710"), (60, "9.10.1919", "0910"),
    (62, "16.10.1919", "1610"), (64, "29.10.1919", "2910"), (71, "23.11.1919", "2311"),
    (72, "23.11.1919", "2311"), (74, "1.12.1919", "0112"), (76, "22.12.1919", "2212"),
    (77, "23.12.1919", "2312"),
]
MONTH_COUNTS = dict(januar=4, februar=2, marec=8, april=8, maj=6, junij=3,
                    julij=4, avgust=9, september=8, oktober=12, november=8, december=5)


def http_get(url, headers=None, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers or UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except Exception as e:  # noqa: BLE001
            last = e
    raise last


def extract_block_field(ts: str, house_no: str, year: int, field: str):
    """Iz parish.ts poišči blok (houseNo, year 04105) in vrni field (whatSi)."""
    pat = re.compile(
        r'houseNo:\s*"' + re.escape(house_no) + r'",\s*bookSignature:\s*"04105",\s*year:\s*'
        + str(year) + r'.*?' + field + r':\s*"((?:[^"\\]|\\.)*)"', re.S)
    m = pat.search(ts)
    if not m:
        return None
    return m.group(1).encode().decode("unicode_escape")


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
    check("I1b entries=11", len(d["entries"]) == 11, f"{len(d['entries'])}")
    check("I1c excluded=70", len(d["excluded"]) == 70, f"{len(d['excluded'])}")
    check("I1d anomalije=18", len(d["anomalies"]) == 18, f"{len(d['anomalies'])}")
    check("I1e crossChecks=33", len(d["crossChecks"]) == 33, f"{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 rowsTotal=79", fr.get("rowsTotal") == 79, str(fr.get("rowsTotal")))
    check("I2b rows1919Born=77", fr.get("rows1919Born") == 77, str(fr.get("rows1919Born")))
    check("I2c scans 311–324", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2d pages 263–275", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))

    # ---------- I3: Griblje hiše + NARE ----------
    houses = sorted((e["houseNo"] for e in d["entries"] if e["village"] == "Griblje" and e["houseNo"].isdigit()), key=int)
    check("I3 hiše = 11 numeričnih", [int(h) for h in houses] == EXPECTED_NUMERIC_HOUSES, str(houses))
    nare = d["stats"].get("nare")
    check("I3b NARE 10/11", nare == 10, str(nare))
    check("I3c nova hiša h81", d["stats"].get("newHouseNos") == ["81"], str(d["stats"].get("newHouseNos")))

    # ---------- I4: kontinuiteta vs parish.ts (pred 1919) ----------
    ts = open(PARISH_TS).read()
    prior_map = {}
    for m in re.finditer(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04105",\s*year:\s*(\d{4})', ts):
        h, y = m.group(1), int(m.group(2))
        if y < 1919:
            prior_map.setdefault(h, []).append(y)
    bad = []
    for h, exp_prior in CONTINUITY.items():
        got = max(prior_map.get(h, [0]))
        if got != exp_prior:
            bad.append((h, exp_prior, got))
    check("I4 kontinuiteta hiš (10)", not bad, str(bad) if bad else "vse ✓")

    # ---------- I5: EMŠO datumski sidri ----------
    cc = {c["id"]: c for c in d["crossChecks"]}
    solid = [c for c in d["crossChecks"] if c["verdict"].startswith("✓") and "dvom" not in c["verdict"]]
    dvom = [c for c in d["crossChecks"] if "dvom" in c["verdict"] or "PRAZEN" in c["verdict"] or "DVOM" in c["verdict"]]
    check("I5 crossChecks ✓ solid ≥ 20", len(solid) >= 20, f"{len(solid)}")
    check("I5b dvom/prazni ≥ 12", len(dvom) >= 12, f"{len(dvom)}")
    # datumski vzorec DDMM9YY
    bad_emso = []
    for lab, born, d4 in EMSO_DATE_CHECKS:
        row = next((c for c in d["crossChecks"] if c.get("row") == lab), None)
        if not row:
            bad_emso.append((lab, "manjka"))
    check("I5c EMŠO vrstice (31)", not bad_emso, str(bad_emso) if bad_emso else "vse ✓")

    # ---------- I6: mesečna porazdelitev ----------
    mc = d["stats"].get("monthCounts", {})
    bad_m = {k: (v, MONTH_COUNTS[k]) for k, v in mc.items() if MONTH_COUNTS.get(k) != v}
    check("I6 meseči (12, vsota 77)", not bad_m and sum(mc.values()) == 77, str(bad_m or sum(mc.values())))

    # ---------- I7: stats ključne številke ----------
    st = d["stats"]
    check("I7 nezakonski=3", st.get("nezakonski") == 3, str(st.get("nezakonski")))
    check("I7b mrtvorojeni=1", st.get("mrtvorojeni") == 1, str(st.get("mrtvorojeni")))
    check("I7c razveljavitve=4", st.get("razveljavitve") == 4, str(st.get("razveljavitve")))
    check("I7d duhovniki=5", st.get("duhovniki") == 5, str(st.get("duhovniki")))
    check("I7e vpisPrenešen=19", st.get("vpisPrenešen") == 19, str(st.get("vpisPrenešen")))
    check("I7f deadInfants=12", st.get("deadInfants") == 12, str(st.get("deadInfants")))
    check("I7g vitals=528", st.get("vitals") == EXPECTED_VITALS_TOTAL, str(st.get("vitals")))
    check("I7h kumulativ 614/88/34", st.get("cumulative", {}).get("vpisi") == 614
          and st.get("cumulative", {}).get("hise") == 88 and st.get("cumulative", {}).get("leta") == 34,
          str(st.get("cumulative")))

    # ---------- I8: anomalije A1–A18 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I8 anomalije A1–A18", ids == [f"A{i}" for i in range(1, 19)], str(ids))
    a1 = next((a for a in d["anomalies"] if a["id"] == "A1"), {})
    check("I8b A1 = konec knjige", "ZADNJE leto" in a1.get("summary", ""))
    a3 = next((a for a in d["anomalies"] if a["id"] == "A3"), {})
    check("I8c A3 = bela listina Šponiček", "Šponiček" in a3.get("summary", "") and "Fiume" in a3.get("summary", ""))
    a4 = next((a for a in d["anomalies"] if a["id"] == "A4"), {})
    check("I8d A4 = EMŠO REKORD 32 žigov", "32 žigov" in a4.get("summary", ""))

    # ---------- I9: parish.ts bloki + vitals ----------
    blocks_04105 = len(re.findall(r'bookSignature:\s*"04105"', ts))
    check("I9 bloki 04105 ≥ 502", blocks_04105 >= BLOCKS_04105, str(blocks_04105))
    qa_ts = open("src/lib/qa-parish.ts").read()
    n587 = qa_ts.count("HOUSE_VITALS.length !== 659")
    n578x = qa_ts.count("HOUSE_VITALS.length !== 578")
    n569 = qa_ts.count("HOUSE_VITALS.length !== 569")
    n544 = qa_ts.count("HOUSE_VITALS.length !== 544")
    n548x = qa_ts.count("HOUSE_VITALS.length !== 550")
    n537 = qa_ts.count("HOUSE_VITALS.length !== 537")
    n554x = qa_ts.count("HOUSE_VITALS.length !== 554")
    n563x = qa_ts.count("HOUSE_VITALS.length !== 563")
    n566x = qa_ts.count("HOUSE_VITALS.length !== 566")
    n587stale = qa_ts.count("HOUSE_VITALS.length !== 587")
    check("I9b vitals 659 (qa ×46+, brez 587/578/569/566/563/554/550/548/544/537/595 — P131 +4 bloka = 599)", n587 >= 44 and n587stale == 0 and n578x == 0 and n569 == 0 and n566x == 0 and n563x == 0 and n554x == 0 and n548x == 0 and n544 == 0 and n537 == 0, f"587×{n587} 578×{n578x} 569×{n569} 566×{n566x} 563×{n563x} 554×{n554x} 550×{n548x} 544×{n544} 537×{n537}")
    # vsi 11 blokov 1919 prisotni
    y1919 = re.findall(r'bookSignature:\s*"04105",\s*year:\s*1919', ts)
    check("I9c blokov 1919 ≥ 11", len(y1919) >= 11, str(len(y1919)))
    # pin sidra v whatSi
    missing = []
    for lab, scan, hisa, pin in ANCHORS:
        y = 1919
        hs = None
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04105",\s*year:\s*1919,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hisa and int(m.group(2)) == scan and pin in m.group(4):
                found = True
                break
        if not found:
            missing.append((lab, hisa))
    check("I9d sidra (10)", not missing, str(missing) if missing else "vse ✓")

    # ---------- I10: qa-p114 ----------
    qa = open("src/lib/qa-parish.ts").read()
    check("I10 qa-p114", '"qa-p114-parish-baptism-1919"' in qa or "qa-p114" in qa)

    # ---------- I11: README ----------
    rd = open("README.md").read()
    check("I11 README po P114", "P114" in rd and ("115/115" in rd or "po P114" in rd))

    # ---------- I12: live ----------
    if live:
        st_, body = http_get(BOOK_URL)
        check("I12 live knjiga 200", st_ == 200, str(st_))
        m = re.search(r'"files":\s*\[(.*?)\]', body.decode("utf-8", "ignore"), re.S)
        n = len(re.findall(r'/image/', m.group(1))) if m else 0
        check("I12b slike = 326", n == EXPECTED_IMAGES, str(n))

    # ---------- izpis ----------
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    print(f"\n{passed}/{total} PASS")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
