#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P109 — župnija Podzemelj: krstna knjiga 04105, polno leto 1914 (issue #18).

Razširitev vzorca P79 (1886) → … → P107 (1912) → P108 (1913) na leto 1914
(PRVO VOJNO leto!). Okvir: glava »1914« INLINE na str. 218 (pod 1913 r105);
1914 r1 = [vas pod marg.] 17 Terezija 1./1. Januar (EMŠO 01019141505225, VPIS
PRENEŠEN 16.10.2002); row 79 = str. 224 (**r79 PREČRTANA!**); opomba na dnu
str. 224: **»78 konec porodov l. 1914«**; **glava 1915 NI INLINE — je na VRHU
str. 225 = s269** (P110 lead). == tiskane strani 218–224 (78 veljavnih vrstic
+ 1 prečrtana). NOVELA P109 — **ŠEST dup parov skenov — NOV REKORD** (2. leto
zapored): 256/257 + 258/259 + 260/261 + 263/264 + 265/266 + 267/268; enojni
samo s262 = str. 221.

VSI vpisi z Griblji: **12 vpisov / 12 hiš — NARE 12/12 (9. čisto leto!)** +
**0 NOVIH hiš** (prvič po 1912/13 — h86 1912 + h76 1913!). **r29 Griblje 5
NOVA VRSTICA VZORCA** (faza-1 izpustila — nalepka!) + **r54 Griblje 48 DVOM
REŠEN** (»G« skozi prozoren trak!). Kumulativ s P79–P108: **487 vpisov /
87 hiš / 29 let** (1886–1914; 479 vitals).

Sidra: r5 hiša **1** (4.5× — faza-1 »1?/4?« + »Anton« POPRAVLJENO → Ana!);
r21 hiša **11** (OBE dupi 4.5× — faza-1 »pod zavihkom« ZAVRŽENO!); r28 hiša
**44** (»44«; band-dvom »34« ZAVRŽEN); r42 starši **Papič × Krixan** (botra
Lozar ×2 — faza-1 zamenjava!); r45 oče **Ernest Šušteršič, ljudski učitelj**;
r38 oče **šahtar**; r53 babica **Ana Mavrenič** + podpis **Bitnar**; r62
botra **Štrucel + Potter** (faza-1 »Hrovat« POPRAVLJENO); **EMŠO 2210914505196
= r63 (Zemelj 20, 22./22. OKTOBER) — faza-1 pripis r62 POPRAVLJEN**.

DUHOVNIKI/PODPISI: Rauq ~6 + Bitnar ~3 + Polak 1 (r5!) + **»Dostál« 1 (r22 —
NOVI 4. duhovnik!)** + Koziga? 1 [~]. BABICA: 12/12 — **JAKOFČIČ 4/12
DOMINANTA** (2. leto zapored!) + Pleščič 2? + Adlešič 2? + Mavrenič 2 +
Jakobčič 1? + Karevič 1?. EMŠO kampanja: ~20 marginalij; 4 SKLADNA sidra
(r21/r42/r53/r29) + 2 [~].

Anomalije: **r79 PREČRTANA** (vse celice + podpis) + »78 konec porodov l.
1914«; **r78 mrtvorojen** (krsta/botra/podpis PRAZNO — 2. sub divo); **žensko
ime v očetovi koloni ×3** (r29 Štrucel + r39 Križan + r63 Šilah — izenačeno s
P108!); mesečne glave PODOBLJENE na meji strani (September ×2 + November ×2);
**1. SVETOVNA: † 1915/16/17/19 marginalia ×7+** (r10 Jože 30.7.1915 + r16
17.7.1916 + r61 19.1.1916 + r68 12.7.1916 + r69 14.7.1916 + r75 12.1916? +
r50 Bologna 25.3.1919 + r58 vojni invalid Podrečje 25.11.1917); **4/12
Griblje otrok † 1914/15** (33%!); h53 VRZEL 16 LET; h44 + h8 ZAPORED 2. leto.

Excluded: 66 + r79 prečrtana. Skripta scripts/p109_parish_baptism_1914.py
(I1–I12, --check izpiše PASS/FAIL in vrne exit code).
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
DOKAZ = "research/issue17/parish-baptism-1914.json"
DOKAZ_P108 = "research/issue17/parish-baptism-1913.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (256, 268)        # 256/257 = str. 218 (glava 1914 + rows 1–7) – 268 (str. 224: rows 69–79 + konec porodov)
FRAME_PAGES = (218, 224)
EXPECTED_ENTRIES = 12
EXPECTED_DISTINCT = 12          # NARE 12/12 — 9. čisto leto!
EXPECTED_EXCLUDED = 66
EXPECTED_STRUCK = 1             # r79
EXPECTED_HOUSES = sorted([1, 5, 8, 11, 14, 18, 21, 44, 48, 53, 77, 90])
EXPECTED_VITALS_HOUSES = EXPECTED_HOUSES
EXPECTED_PT_IN_SET = ["1", "5", "8", "11", "14", "18", "21", "77", "90"]
EXPECTED_PT_GAP = ["44", "48", "53"]  # v luknji 41–60 (vse dokazane!)
EXPECTED_NEW_HOUSES = 0         # PRVIČ po 1912/13!
EXPECTED_VITALS_TOTAL = 479     # P109 lastno (467 + 12) — dokaz stats.vitals
BLOCKS_04105_P109 = 453         # P109 lastno (441 + 12)
VITALS_TOTAL_NOW = 490          # P110: 479 + 11 (skupno stanje parish.ts)
BLOCKS_04105 = 464              # 453 + 11 (P110)
KUMULATIV_ENTRIES = 487         # 475 + 12 (P109 lastno kumulativno stanje)
KUMULATIV_HOUSES = 87           # + 0
KUMULATIV_YEARS = 29            # 1886–1914
# kontinuitete (hiša → zadnje krstno leto pred 1914 v 04105, iz parish.ts)
CONTINUITY = {
    "1": 1910, "5": 1912, "8": 1913, "11": 1912, "14": 1911, "18": 1912,
    "21": 1911, "44": 1913, "48": 1912, "53": 1898, "77": 1909, "90": 1912,
}
# sidra/pini P109 (row, scan, hiša, pin):
ANCHORS = [
    (5, 257, "1", "Ana"),
    (5, 257, "1", "Štrucel"),
    (5, 257, "1", "POPRAVEK"),
    (13, 259, "14", "Brinec"),
    (13, 259, "14", "POPRAVLJENO"),
    (17, 259, "53", "16 LET"),
    (17, 259, "53", "Perdivec"),
    (21, 261, "11", "1803914505878"),
    (21, 261, "11", "ZAVRŽENO"),
    (28, 261, "44", "ZAVRŽEN"),
    (28, 261, "44", "11.04.2001"),
    (29, 261, "5", "NOVA VRSTICA VZORCA"),
    (29, 261, "5", "Štrucel"),
    (29, 261, "5", "0405914505481"),
    (38, 262, "77", "šahtar"),
    (38, 262, "77", "POPRAVEK"),
    (42, 262, "21", "3006914500518"),
    (42, 262, "21", "Lozar"),
    (45, 264, "90", "učitelj"),
    (45, 264, "90", "Štrucel"),
    (53, 264, "18", "2108914500174"),
    (53, 264, "18", "Brinec"),
    (54, 264, "48", "REŠEN"),
    (54, 264, "48", "12. VPIS"),
    (62, 266, "8", "ZAPORED"),
    (62, 266, "8", "31.7.1915"),
]
EMSO_ANCHOR_ROWS = {
    21: "1803914505878",
    29: "0405914505481",
    42: "3006914500518",
    53: "2108914500174",
}
GRIBLJE_JAKOFCIC = 4            # 4 × babica Marija Jakofčič — DOMINANTA 1914 (2. leto!)
GRIBLJE_BITNAR = 3              # ~3 (r53 jasno + r62 jasno + r54 [~])
GRIBLJE_RAUQ = 5                # jasni: r13/r29/r38/r45 + r17 nalepka
GRIBLJE_POLAK = 1               # r5!
GRIBLJE_DOJENCKI_UMRLI = 4      # r5 Ana 1915 + r21 Jožefa 1914 + r45 Ivanka 1915 + r62 Jožefa 1915 (33%!)
GRIBLJE_VRZELI = 10             # 12 vrstic, vsi imajo VRZEL opombo (h44/h8 ZAPORED)


def http_get(url, headers, tries=4):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read() if hasattr(e, "read") else b""
        except Exception as e:  # noqa: BLE001
            last = e
    raise last  # type: ignore


def decode_inventory(html):
    urls = []
    for m in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', html):
        s = m.group(1)[7:-1]
        try:
            d = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
            if d.startswith("http"):
                urls.append(d)
        except Exception:
            pass
    return sorted(set(urls))


def pt_house_set():
    d = json.load(open(PT_CHAIN, encoding="utf-8"))
    return {str(r["no"]).strip() for r in d["chain"] if r.get("kind") == "hiša"}


def parish_vitals_04105():
    src = open(PARISH_TS, encoding="utf-8").read()
    blocks = re.findall(r"\{[^{}]*?bookSignature:\s*\"" + BOOK_SIGNATURE + r"\"[^{}]*?\}", src, re.S)
    out = []
    for b in blocks:
        hn = re.search(r'houseNo:\s*"([^"]*)"', b)
        yr = re.search(r"year:\s*(\d+)", b)
        out.append({"houseNo": hn.group(1) if hn else None,
                    "year": int(yr.group(1)) if yr else None})
    return out


def page_of_scan(scan):
    """P109: ŠEST dup parov (256/257=218, 258/259=219, 260/261=220, enojni
    262=221, 263/264=222, 265/266=223, 267/268=224)."""
    return {256: 218, 257: 218, 258: 219, 259: 219, 260: 220, 261: 220,
            262: 221, 263: 222, 264: 222, 265: 223, 266: 223,
            267: 224, 268: 224}.get(scan)


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p108 = json.load(open(DOKAZ_P108, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]
    houses_numeric = [h for h in houses if h.isdigit()]

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + stran==sken + ŠEST dup parov + konec porodov
    cited = sorted({e["scan"] for e in entries})
    inv["I3_frame"] = (
        cited == sorted(set(cited)) and set(cited) <= {256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266}
        and all(page_of_scan(s) == p for s, p in ((e["scan"], e["page"]) for e in entries))
        and dokaz["frame"]["rowsTotal"] == 78
        and dokaz["frame"]["rowsStruck"] == 1
        and len(dokaz["frame"]["dupPari"]) == 6
        and dokaz["frame"]["scans"] == [256, 268]
        and dokaz["frame"]["pages"] == [218, 224]
        and "78 konec porodov" in dokaz["frame"]["rowsNote"]
    )

    # I4 — 12 vpisov / 12 hiš (NARE 12/12!) + hiše + vitals hiše
    hv = parish_vitals_04105()
    hv1914 = [b for b in hv if b["year"] == 1914]
    inv["I4_nare_houses"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(set(houses)) == EXPECTED_DISTINCT
        and sorted(int(h) for h in set(houses_numeric)) == EXPECTED_HOUSES
        and sorted(int(b["houseNo"]) for b in hv1914 if b["houseNo"]) == EXPECTED_VITALS_HOUSES
    )

    # I5 — kontinuiteta: CONTINUITY iz dokaza se sklada s parish.ts
    ok5 = True
    for hn, last_year in CONTINUITY.items():
        ys = [b["year"] for b in hv if b["houseNo"] == hn and b["year"] < 1914]
        if not ys or max(ys) != last_year:
            ok5 = False
    inv["I5_continuity"] = ok5

    # I5b — 0 novih hiš: vsaka 1914 hiša ima zgodnejše vpise v 04105
    ok5b = all(
        any(b["houseNo"] == hn and b["year"] < 1914 for b in hv)
        for hn in set(houses_numeric)
    )
    inv["I5b_no_new_houses"] = ok5b and dokaz["stats"]["newSampleHouses"] == 0

    # I6 — PT klasifikacija: 10 v naboru + 2 v luknji (44+48); 0 novih;
    # kumulativ 487/87/29
    pts = pt_house_set()
    inset = sorted((h for h in set(houses_numeric) if h in pts), key=int)
    gap = sorted((h for h in set(houses_numeric) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["pt"] == "9/3 (h44 + h48 + h53 v luknji 41–60 — vse tri dokazane v PT_GAP_KNOWN!)"
        and dokaz["stats"]["newHouseNos"] == []
        and dokaz["stats"]["cumulative"] in ("487 vpisov / 87 hiš / 29 let (1886–1914)", "498 vpisov / 87 hiš / 30 let (1886–1915)")
        and dokaz["stats"]["vitals"] == EXPECTED_VITALS_TOTAL  # P109 lastno
        and all(f'"{x}"' in pt_gap_set for x in ("44", "48", "53"))
    )

    # I7 — sidra (26 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r5 = e_by_row(5)
    r13 = e_by_row(13)
    r17 = e_by_row(17)
    r21 = e_by_row(21)
    r28 = e_by_row(28)
    r29 = e_by_row(29)
    r38 = e_by_row(38)
    r42 = e_by_row(42)
    r45 = e_by_row(45)
    r53 = e_by_row(53)
    r54 = e_by_row(54)
    r62 = e_by_row(62)
    inv["I7_anchors"] = (
        ok7
        # r5 — Ana (ne Anton!) + hiša 1 + boter Štrucel
        and "ANA (ne »Anton«!)" in json.dumps(r5, ensure_ascii=False)
        and "Jožef Štrucel" in r5["botra"]
        # r13 — h14 vrzel 3 (POPRAVLJENO iz 18)
        and "VRZEL 3 LETA" in " ".join(r13["notes"]) and "POPRAVLJENO" in " ".join(r13["notes"])
        # r17 — h53 VRZEL 16 LET + nalepka 2000 = r18
        and "VRZEL 16 LET" in " ".join(r17["notes"]) and "= **r18" in " ".join(r17["notes"])
        # r21 — hiša 11 ZAVRŽENO »pod zavihkom«
        and "ZAVRŽENO" in " ".join(r21["notes"])
        # r28 — hiša 44, band-dvom 34 ZAVRŽEN + nalepka 11.04.2001
        and "ZAVRŽEN" in " ".join(r28["notes"]) and "ZAPORED 2. LETO" in " ".join(r28["notes"])
        # r29 — NOVA VRSTICA + žensko ime
        and "NOVA VRSTICA VZORCA" in " ".join(r29["notes"])
        and r29["father"].startswith("**Marija Štrucel**")
        # r38 — šahtar + Anfons POPRAVEK
        and "ŠAHTAR" in r38["father"] and "Anfons" in r38["child"]
        # r42 — botra Lozar ×2 (faza-1 zamenjava starši/botra!)
        and "Anton Lozar + Barbara Lozar" in r42["botra"]
        and "POPRAVEK" in json.dumps(r42, ensure_ascii=False)
        # r45 — Ernest Šušteršič učitelj
        and "Ernest Šušteršič" in r45["father"] and "učitelj" in r45["father"]
        # r53 — mati Brinec + babica Ana Mavrenič + Bitnar
        and r53["mother"] == "Katarina Brinec" and r53["babica"] == "Ana Mavrenič"
        and "Bitnar" in r53["priest"]
        # r54 — dvom REŠEN (Griblje 48!)
        and "REŠEN" in " ".join(r54["notes"]) and r54["village"] == "Griblje"
        and r54["houseNo"] == "48"
        # r62 — botra Štrucel + Potter (POPRAVLJENO iz Hrovat) + † 31.7.1915
        and "Matija Štrucel + Katarina Potter" in r62["botra"]
        and "31.7.1915" in json.dumps(r62, ensure_ascii=False)
        # EMŠO reassign: r62 brez 2210914505196, r63 (excluded) z njim
        and "NE r62" in json.dumps(r62, ensure_ascii=False)
        and "2210914505196" in json.dumps(next(x for x in excluded if x["row"] == 63), ensure_ascii=False)
    )

    # I8 — EMŠO sidra (4 SKLADNA: r21/r29/r42/r53)
    ok8 = all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
              for row, EMSO in EMSO_ANCHOR_ROWS.items())
    inv["I8_emso_anchors"] = ok8

    # I9 — statistika: babica Jakofčič 4 (DOMINANTA), Bitnar ≥2, Rauq ≥4,
    # Polak 1, 4 dojenčkov/otrok †, vrzeli, dup 6, excluded 66, struck 1
    bab = [e["babica"] or "" for e in entries]
    inv["I9_stats"] = (
        sum(1 for b in bab if "Jakofčič" in b) == GRIBLJE_JAKOFCIC
        and sum(1 for e in entries if "Bitnar" in (e["priest"] or "")) >= 2
        and sum(1 for e in entries if "Rauq" in (e["priest"] or "")) >= 4
        and sum(1 for e in entries if "Polak" in (e["priest"] or "")) == GRIBLJE_POLAK
        and sum(1 for e in entries if any("1915" in n or "1914" in n for n in e["notes"])) >= GRIBLJE_DOJENCKI_UMRLI
        and sum(1 for e in entries if any("VRZEL" in n and "LET" in n for n in e["notes"])) >= 10
        and dokaz["stats"]["babica"].startswith("12/12")
        and dokaz["stats"]["entries"] == 12
        and dokaz["stats"]["distinctHouses"] == 12
        and dokaz["stats"]["intraYearRepeats"] == 0
        and dokaz["excludedCount"] == EXPECTED_EXCLUDED
        and dokaz["frame"]["rowsStruck"] == EXPECTED_STRUCK
    )

    # I9b — P108 lead popravek: P108 trdi 1914 r1 = [vas] 17 Terezija,
    # P109 dokaz r1 (excluded) potrjuje hišo 17 + P108 r5 »Anton« → P109 ANA
    inv["I9b_lead_correction"] = (
        dokaz_p108["frame"]["yearEnd"]["scan"] == 256
        and dokaz["excluded"][0]["row"] == 1
        and dokaz["excluded"][0]["houseNo"] == "17"
        and "POPRAVEK" in json.dumps(e_by_row(5), ensure_ascii=False)
        and e_by_row(5)["child"] == "Ana"
    )

    # I10 — neodvisen preračun: vsi village == Griblje; sken→stran; vrstice
    ok10 = all(e["village"] == "Griblje" for e in entries)
    for e in entries:
        if page_of_scan(e["scan"]) != e["page"]:
            ok10 = False
    rows = sorted(e["row"] for e in entries)
    ok10 = ok10 and rows == sorted(rows) and len(rows) == len(set(rows))
    inv["I10_independent_recalc"] = ok10

    # vitals skupaj 479 (467 + 12; vse tri knjige 04105+04894+04455)
    src_all = open(PARISH_TS, encoding="utf-8").read()
    total_blocks = len(re.findall(r"\{[^{}]*?bookSignature:\s*\"(04105|04894|04455)\"[^{}]*?\}", src_all, re.S))
    inv["I11_vitals_total"] = total_blocks == VITALS_TOTAL_NOW
    inv["I12_blocks_04105"] = len(hv) == BLOCKS_04105

    passed = sum(1 for v in inv.values() if v)
    total = len(inv)
    for k, v in inv.items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
    print(f"--- {passed}/{total} PASS")
    return 0 if passed == total else 1


def main():
    if "--check" in sys.argv:
        sys.exit(verify())
    print(__doc__)


if __name__ == "__main__":
    main()
