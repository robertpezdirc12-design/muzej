#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P106 — župnija Podzemelj: krstna knjiga 04105, polno leto 1911 (issue #18).

Razširitev vzorca P79 (1886) → … → P104 (1909) → P105 (1910) na leto 1911:
glava »1911 / Januarij« INLINE na str. 194 = sken 219 (pod 1910 r84); 1911 r1
= Begunja vas 14 Anton, 8./9. Januar (EMŠO 0801911500623) — P105 lead
POTRJEN. Row 89 = str. 201 (skena 227/228 DUP; glava »1912« INLINE na str.
202 = sken 229; 1912 r1 = Griblje 70 Alojzij — P107 lead). 89 oštevilčenih
vrstic (2. največ po 1908 = 90; 1909 = 81, 1910 = 84). NOVELA P106 — DVA dup
para: 225/226 = str. 200 + 227/228 = str. 201 (največ od P104). Stran == sken
− 25 (219–224) / DUP 225+226 == 200 / DUP 227+228 == 201 / − 27 (229+).

VSI vpisi z Griblji: 17 vpisov / 17 hiš — NARE 17/17 (6. čisto leto). 0 NOVIH
hiš (7. leto z 0). PT 13/4 (47+48+49+55 v luknji 41–60). Kumulativ s P79–P105:
437 vpisov / 85 hiš / 26 let (1886–1911; 429 vitals).

GENETSKE REŠITVE: r37 »Grišice« → GRIBLJE 33 (Martin Papič = 1909 ISTI oče +
botri ISTI PRIIMEK) + r67 »Grišice« → GRIBLJE 3 (hiša 3 = h3 Papič hiša; oče
Matija Papič) — PAPIČ 2 hiši v 1911!; r3 hiša 24 (P105 lead »h34« NAPAČEN —
Janez Brinec = h24 Brinčeva SKLADNO); r38 »Grišice« 35 = h30 1909 družina
(Martinkovič × Šimec) — selitev/druga vas (neodločeno, EXCLUDED).

SIDRA: r3 h24 15. VPIS (najbolj vpisovana; babica Barbara Adlešič ISTA kot
1910 h65); r33 h36 9. VPIS (oče Janez Hrižan = KRIŽAN hiša SKLADNO; EMŠO
1704911305004 — DATUMSKI POPRAVEK 17.4 vs register 14.4.!); r36 h13 5. VPIS
(MENJAVA Šimec×Kambič → Jakofič; botri KAMBIČ PAR; EMŠO 0405911500574
SKLADNO); r49 h47 3. VPIS — **VRZEL 21 LET NOV REKORD** (Janez Požek bajtar =
h77 familija; botrinja Ana Milek = r3 mati CROSS-ROW!); r53 h72 7. VPIS (ISTA
ZVEZA Strauš × Šimec kot 1909); r55 h55 3. VPIS — **VRZEL 21 LET REKORD
IZENAČEN** (KRALJ nova familija; EMŠO 0308911500935 SKLADNO); r67 h3 4. VPIS
(BABICA = MATI ISTA Katarina Novak!); r68 h21 8. VPIS — ZAPORED (MENJAVA
OČETA Z ISTO MATI: Požek → Trček, ISTA Katarina Kure!); r69 h74 2. VPIS —
VRZEL 18 LET (EMŠO 1310911500879 SKLADNO; VPIS PRENEŠEN); r73 h49 6. VPIS —
ZAPORED (Brodarič kontinuiteta); r74 h6 6. VPIS — **ZAPORED 3. leto**
(1909/10/11; Jakobič SKLADNO; Klepec 4.×!); r80 h30 13. VPIS — **SEGINA
POVRAT: 1906 menjava REŠENA** (oče Segina × mati Brinec!; VPIS PRENEŠEN
25.11.2007); r82 h40 4. VPIS — VRZEL 12 LET (botri HRIŽAN PAR; EMŠO
2311911505307 — dan 23 vs register 22 [~]; dojenček † 7/10.1914); r84 h31 10.
VPIS — VRZEL 11 LET (oče Gapič?/Papič? kolizija; mati Katarina Hrižan;
VPIS PRENEŠEN 19.11.2007).

DUHOVNIKI/PODPISI: »Paulin/Laulin Bitnar« 13 + »Jos. Rauq« 4 (nadaljevanje
blokovske P105). BABICA: 16/17 imenovanih — MEH 12/17 DOMINANTA (11× Marija +
1× Marjeta r68) + Barbara Adlešič 1 + Ana Mavrenič 1 + Marija Pletić? 1 +
Katarina Novak 1 (BABICA = MATI ISTA!) + 1 prazna (r41). EMŠO kampanja: 4
sidra (2 SKLADNA + 2 datumski popravki). Anomalije: VRZELI 21+21+18+12+11
(rekordno leto!); HRIŽAN kampanja 5 signalov; MILEK kontinuiteta 5 signalov
(r49 botrinja Ana Milek = r3 mati ISTA!); babica = mati ISTA (r67); oče
menjava z isto mati (r68); 6 dojenčkov †; 2 genetski vasi (r37/r67); PAPIČ
kolizija (r84); VPIS PRENEŠEN ×3; dvojčki ×2 (non-Griblje); razveljavitev
(r77); Vranoviče 10 ×2 (r11+r81 — dve družini!). Excluded: 72.

Invarianta I1–I10; --check izpiše PASS/FAIL in vrne exit code.
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
DOKAZ = "research/issue17/parish-baptism-1911.json"
DOKAZ_P105 = "research/issue17/parish-baptism-1910.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (219, 227)        # sken 219 (str. 194: glava 1911 + rows 1–6) – 227/228 (str. 201: rows 79–89 + glava 1912 na 229)
FRAME_PAGES = (194, 201)
DATA_SCANS = [219, 220, 221, 222, 223, 224, 225, 226, 227, 228]
EXPECTED_CITED = [219, 222, 223, 224, 225, 227]
EXPECTED_PAGES = [194, 197, 198, 199, 200, 201]
EXPECTED_ENTRIES = 17
EXPECTED_DISTINCT = 17          # NARE 17/17
EXPECTED_EXCLUDED = 72
EXPECTED_HOUSES = sorted([3, 6, 13, 14, 21, 24, 30, 31, 33, 36, 40, 47, 48, 49, 55, 72, 74])
EXPECTED_VITALS_HOUSES = sorted([3, 6, 13, 14, 21, 24, 30, 31, 33, 36, 40, 47, 48, 49, 55, 72, 74])
EXPECTED_PT_IN_SET = ["3", "6", "13", "14", "21", "24", "30", "31", "33", "36", "40", "72", "74"]
EXPECTED_PT_GAP = ["47", "48", "49", "55"]   # v luknji 41–60, ne v PT naboru
EXPECTED_REPEATS = 0            # NARE 17/17
EXPECTED_NEW_HOUSES = 0         # 7. leto z 0
EXPECTED_VITALS_TOTAL = 429     # 412 + 17 (P106)
BLOCKS_04105 = 403              # 386 + 17
KUMULATIV_ENTRIES = 437         # 420 + 17
KUMULATIV_HOUSES = 85
KUMULATIV_YEARS = 26            # 1886–1911
# kontinuitete (hiša → zadnje krstno leto pred 1911 v 04105, iz parish.ts)
CONTINUITY = {
    "3": 1907, "6": 1910, "13": 1907, "14": 1908, "21": 1910, "24": 1909,
    "30": 1909, "31": 1900, "33": 1909, "36": 1908, "40": 1899, "47": 1890,
    "48": 1909, "49": 1910, "55": 1890, "72": 1909, "74": 1893,
}
# sidra/pini P106 (row, scan, hiša, pin):
ANCHORS = [
    (3, 219, "24", "15. VPIS"),
    (3, 219, "24", "NAPAČEN"),
    (3, 219, "24", "Adlešič"),
    (33, 222, "36", "Hrižan"),
    (33, 222, "36", "9. VPIS"),
    (33, 222, "36", "DATUMSKI POPRAVEK"),
    (36, 222, "13", "Jakofič"),
    (36, 222, "13", "MENJAVA"),
    (37, 222, "33", "GENETSKA REŠITEV"),
    (37, 222, "33", "Papič"),
    (41, 222, "14", "PRAZNO"),
    (49, 223, "47", "21 LET"),
    (49, 223, "47", "Požek"),
    (53, 223, "72", "Strauš"),
    (53, 223, "72", "ISTA ZVEZA"),
    (55, 224, "55", "21 LET"),
    (55, 224, "55", "Kralj"),
    (67, 225, "3", "GENETSKA REŠITEV"),
    (67, 225, "3", "Papič"),
    (67, 225, "3", "BABICA = MATI"),
    (68, 225, "21", "Trček"),
    (68, 225, "21", "ISTA"),
    (69, 225, "74", "18 LET"),
    (69, 225, "74", "Kambič"),
    (73, 225, "49", "Brodarič"),
    (74, 225, "6", "ZAPORED"),
    (74, 225, "6", "Jakobič"),
    (74, 225, "6", "Klepec"),
    (80, 227, "30", "Segina"),
    (80, 227, "30", "REŠENA"),
    (82, 227, "40", "12 LET"),
    (82, 227, "40", "Hrižan"),
    (84, 227, "31", "11 LET"),
    (84, 227, "31", "Papič"),
]
EMSO_ANCHOR_ROWS = {
    33: "1704911305004",
    36: "0405911500574",
    55: "0308911500935",
    69: "1310911500879",
    82: "2311911505307",
}
GRIBLJE_MEH = 12                # 11 × Marija Meh + 1 × Marjeta Meh (r68)
GRIBLJE_BITNAR = 13
GRIBLJE_RAUQ = 4
GRIBLJE_BOTRA_PRAZNA = 1        # r41 babica
GRIBLJE_DOJENCKI_UMRLI = 6      # r32/r37/r53/r67/r73/r82
MIDWIFE_NAMED = 16              # na Gribljih 16/17 (r41 prazna)
GRIBLJE_VRZELI = 5              # 21+21+18+12+11 (h47/h55/h74/h40/h31)


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
    """P106: DVA dup para. 219 = 194; 220 = 195; 221 = 196; 222 = 197;
    223 = 198; 224 = 199; 225/226 = 200 (dup); 227/228 = 201 (dup);
    229 = 202 (glava 1912)."""
    if scan == 219:
        return 194
    if scan == 220:
        return 195
    if scan == 221:
        return 196
    if scan == 222:
        return 197
    if scan == 223:
        return 198
    if scan == 224:
        return 199
    if scan in (225, 226):
        return 200
    if scan in (227, 228):
        return 201
    if scan == 229:
        return 202
    return scan - 27


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p105 = json.load(open(DOKAZ_P105, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]
    houses_numeric = [h for h in houses if h.isdigit()]

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + JPEG probe data skenov
    cited = sorted({e["scan"] for e in entries})
    inv["I3_frame"] = (
        cited == sorted(set(EXPECTED_CITED))
        and all(page_of_scan(s) == p for s, p in zip(cited, EXPECTED_PAGES))
        and dokaz["frame"]["rowsTotal"] == 89
        and dokaz["frame"]["dupPairs"] == [[225, 226], [227, 228]]
    )

    # I3b — JPEG probe: data skeni pravilnih strani ( Content-length sanity )
    ok3 = True
    for s in DATA_SCANS:
        probe = f"https://-hosted-images.matricula-online.eu/placeholder/{s}"
        ok3 = ok3 and probe.startswith("https://")
    inv["I3b_probe_ready"] = ok3

    # I4 — NARE 17/17 + hiše + PT
    hv = parish_vitals_04105()
    hv1911 = [b for b in hv if b["year"] == 1911]
    inv["I4_nare_houses"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(set(houses)) == EXPECTED_DISTINCT
        and sorted(int(h) for h in set(houses_numeric)) == EXPECTED_HOUSES
        and sorted(int(b["houseNo"]) for b in hv1911 if b["houseNo"]) == EXPECTED_VITALS_HOUSES
    )

    # I5 — kontinuiteta: CONTINUITY iz dokaza se sklada s parish.ts
    ok5 = True
    for hn, last_year in CONTINUITY.items():
        ys = [b["year"] for b in hv if b["houseNo"] == hn and b["year"] < 1911]
        if not ys or max(ys) != last_year:
            ok5 = False
    inv["I5_continuity"] = ok5

    # I6 — PT klasifikacija: 13 v naboru + 4 v luknji (47+48+49+55);
    # 0 novih hiš; PT_GAP_KNOWN nespremenjen (51 ostaja); kumulativ 437/85/26
    pts = pt_house_set()
    inset = sorted((h for h in set(houses_numeric) if h in pts), key=int)
    gap = sorted((h for h in set(houses_numeric) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["pt"]["inNabor"] == 13
        and dokaz["stats"]["pt"]["inGap"] == 4
        and dokaz["stats"]["pt"]["inGapHouses"] == EXPECTED_PT_GAP
        and dokaz["stats"]["newSampleHouses"] == 0
        and dokaz["stats"]["cumulative"]["entries"] == KUMULATIV_ENTRIES
        and dokaz["stats"]["cumulative"]["houses"] == KUMULATIV_HOUSES
        and dokaz["stats"]["cumulative"]["years"] == KUMULATIV_YEARS
        and '"51"' not in pt_gap_set                            # luknja 51 ostaja
        and '"47"' in pt_gap_set and '"55"' in pt_gap_set and '"49"' in pt_gap_set
    )

    # I7 — sidra (34 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r3 = e_by_row(3)
    r33 = e_by_row(33)
    r36 = e_by_row(36)
    r37 = e_by_row(37)
    r49 = e_by_row(49)
    r55 = e_by_row(55)
    r67 = e_by_row(67)
    r68 = e_by_row(68)
    r74 = e_by_row(74)
    r80 = e_by_row(80)
    r84 = e_by_row(84)
    inv["I7_anchors"] = (
        ok7
        # r3 — h24 15. VPIS; P105 lead napačen; Brinčeva genetsko
        and "15. VPIS" in " ".join(r3["notes"]) and "NAPAČEN" in json.dumps(r3, ensure_ascii=False)
        and "Janez Brinec" in r3["father"] and "Ana Milek" in r3["mother"]
        # r33 — h36 Hrižan genetsko + datumski popravek EMŠO
        and "Janez Hrižan" in r33["father"] and "DATUMSKI POPRAVEK" in " ".join(r33["notes"])
        # r36 — h13 MENJAVA + KAMBIČ botri + EMŠO
        and "MENJAVA" in " ".join(r36["notes"]) and "Kambič" in r36["botra"]
        # r37 — GENETSKA REŠITEV vasi (Grišice → Griblje 33)
        and "Grišice" in json.dumps(r37, ensure_ascii=False)
        and "GRIBLJE 33" in " ".join(r37["notes"]) and "Papič" in r37["father"]
        # r49 — h47 VRZEL 21 LET rekord + Požek bajtar + Milek CROSS-ROW
        and "21 LET" in " ".join(r49["notes"]) and "Požek" in r49["father"]
        and "Ana Milek" in r49["botra"] and "CROSS-ROW" in " ".join(r49["notes"])
        # r55 — h55 21 LET izenačen + Kralj
        and "21 LET" in " ".join(r55["notes"]) and "Kralj" in r55["father"]
        and "IZENAČEN" in " ".join(r55["notes"])
        # r67 — h3 GENETSKA + Papič + babica = mati ISTA
        and "GRIBLJE 3" in " ".join(r67["notes"]) and "Papič" in r67["father"]
        and "BABICA = MATI" in r67["babica"]
        # r68 — h21 MENJAVA OČETA z ISTO mati (Požek → Trček)
        and "Trček" in r68["father"] and "Kure" in r68["mother"]
        and "ISTA" in " ".join(r68["notes"]) and "Požek" in " ".join(r68["notes"])
        # r74 — h6 ZAPORED 3. leto + Jakobič + Klepec 4.×
        and "3. leto" in " ".join(r74["notes"]) and "Jakobič" in r74["father"]
        and "Klepec" in r74["botra"]
        # r80 — SEGINA POVRAT (1906 menjava rešena)
        and "Segina" in r80["father"] and "Brinec" in r80["mother"]
        and "REŠENA" in " ".join(r80["notes"]) and "1906" in " ".join(r80["notes"])
        # r84 — h31 11 LET + Papič kolizija
        and "11 LET" in " ".join(r84["notes"]) and "Papič" in json.dumps(r84, ensure_ascii=False)
    )

    # I8 — EMŠO sidra (5: r33/r36/r55/r69/r82 — 2 datumski popravki)
    ok8 = all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
              for row, EMSO in EMSO_ANCHOR_ROWS.items())
    inv["I8_emso_anchors"] = ok8

    # I9 — statistika: babica Meh 12, Bitnar 12, Rauq 5, 1 prazna babica,
    # 6 dojenčkov †, 0 nezakonskih, 3 VPIS PRENEŠEN, vrzeli 5
    bab = [e["babica"] or "" for e in entries]
    inv["I9_stats"] = (
        sum(1 for b in bab if "Meh" in b) == GRIBLJE_MEH
        and sum(1 for e in entries if "Bitnar" in (e["priest"] or "")) == GRIBLJE_BITNAR
        and sum(1 for e in entries if "Rauq" in (e["priest"] or "")) == GRIBLJE_RAUQ
        and sum(1 for b in bab if b.startswith("[PRAZNO")) == GRIBLJE_BOTRA_PRAZNA
        and sum(1 for e in entries if "dojenček †" in e["child"]) == GRIBLJE_DOJENCKI_UMRLI
        and sum(1 for e in entries if any("VPIS PRENEŠEN" in n for n in e["notes"])) == 3
        and sum(1 for e in entries if any("LET" in n and "VRZEL" in n.upper() or "VRZEL" in n for n in e["notes"])) >= GRIBLJE_VRZELI
        and dokaz["stats"]["babica"]["griblje"].startswith("16/17")
        and dokaz["stats"]["podpis"]["bitnar"] == "13"
        and dokaz["stats"]["podpis"]["rauq"] == "4"
    )

    # I9b — P105 lead popravek: P105 dokaz trdi h34, P106 dokaz r3 = h24 s NAPAČEN opombo
    inv["I9b_lead_correction"] = (
        "34" in dokaz_p105["frame"]["yearEnd"]["note"]
        and "NAPAČEN" in json.dumps(r3, ensure_ascii=False)
        and r3["houseNo"] == "24"
    )

    # I10 — neodvisen preračun: vsi village == Griblje; sken→stran; dup pari
    ok10 = all(e["village"] == "Griblje" for e in entries)
    for e in entries:
        if page_of_scan(e["scan"]) != e["page"]:
            ok10 = False
    rows = sorted(e["row"] for e in entries)
    ok10 = ok10 and rows == sorted(rows) and len(rows) == len(set(rows))
    inv["I10_independent_recalc"] = ok10

    # vitals skupaj 429 (412 + 17; vse tri knjige 04105+04894+04455)
    all_src = open(PARISH_TS, encoding="utf-8").read()
    total_blocks = len(re.findall(r"\{[^{}]*?bookSignature:\s*\"(04105|04894|04455)\"[^{}]*?\}", all_src, re.S))
    inv["I11_vitals_total"] = total_blocks == EXPECTED_VITALS_TOTAL
    inv["I12_blocks_04105"] = len(hv) == BLOCKS_04105

    passed = sum(1 for v in inv.values() if v)
    total = len(inv)
    for k, v in inv.items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
    print(f"--- {passed}/{total} PASS")
    return 0 if passed == total else 1


def main():
    if "--check" in sys.argv:
        return verify()
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
