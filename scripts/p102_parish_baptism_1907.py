#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P102 — župnija Podzemelj: krstna knjiga 04105, polno leto 1907 (issue #18).

Razširitev vzorca P79 (1886) → … → P99 (1904) → P100 (1905) → P101 (1906) na
leto 1907: okvir glava »1907« POD r87 na str. 165 = skeni 178/179 (dup par že
P101; 1907 r1 = Dobravice 27 Ivanka, 5./5. Januar, podpis Anton Dostál —
P101 lead POTRJEN) – row 90 na str. 172 (sken 188; glava »1908« na str. 173
= sken 189; 1908 r1 = Krasinec 58 August — P103 lead). 90 oštevilčenih
vrstic. NOVELA P102 — DVA nova dup para: 180/181 = str. 166 (rows 9–20) +
183/184 = str. 168 (rows 33–44). Stran == sken − 16 (184–189) / − 15
(181–183) / − 14 (179–180). VSI vpisi z Griblji: 16 vpisov / 14 hiš +
1 neberljiva (r4 — strglek + modri pripisi) — NARE PRELOM: h10 ×2 (r85+r86
dvojčka, oba † december 1907; 1. intra-letna ponovitev po 1905 h12×2; 1906
je bil 18/18). 0 NOVIH hiš (tretje leto zapored … po P101 h4). PT 12/2
(48+49 v luknji 41–60 — ponovitve; luknja 41–60 ostaja samo h51). Kumulativ
s P79–P101: 363 vpisov / 85 hiš / DVAINDVAJSET let (1886–1907).
Sidra: r4 ŽELJKO×KURE krog (hiša neberljivo; EMŠO sidro); r11 h11 4. VPIS
ISTA familija (Žumič — 1905 »Žume/Žunič«); r48 h3 3. VPIS ISTA (Papič —
Kurrent P/T »Tapič«); r52 h7 4. VPIS ISTA (JAKOB TOTER kot hišni oče!);
r53 h12 11. VPIS — Dragoš×Cvitkovič POVRAT po 1901/05 Štraus/Šimec
interludu (več-družinska h12); r60 h5 4. VPIS ISTA (Štrucelj×Meh) + NOV
KAPLAN Gregor Pecar (prvi podpis 17./18. 9.); r61 h18 3. VPIS — MENJAVA
Šimec → Peter Brinec × Ana Butala; r64 h48 3. VPIS — MENJAVA Pezdirec →
Janez Kure bajtar; r67 h6 3. VPIS — MENJAVA Jakobič → Kapucina?×Moravec;
r69 h49 3. VPIS — Brodarič (mati Milek/Miheč [MERI]) + dojenček † 17.11.;
r73 h27 9. VPIS — Pozdirec 2. leto + ISTA botra (Željko+Hrižan) 2. leto
(hiša »8y« = Kurrent »27«!); r76 h13 6. VPIS — VRZEL 13 LET + MENJAVA
Jakopič → ŠIMEC×KAMBIČ (SELITEV h18→h13!); r80 h83 4. VPIS — ISTA Željko
družina kot 1903 (luknja 1890–1902); r85+r86 h10 ×2 — BRINEC POVRAT
(1897 familija) + dvojčka † (19.12. + 25.12. božič); r88 h62 2. VPIS —
VRZEL 16 LET (2. najdaljša vzorca) + Kure×Požek.
DUHOVNIKI NOVELA (na Gribljih 16/16): NOV KAPLAN Gregor Pecar 10 (prvi
podpis r60 = 17./18. 9. 1907; paralelni Rauq Sep–Nov!) + Jos. Rauq 5 +
P. Janez Kmetij? 1 (januar, branje negotovo). BABICA NOVELA: MIH 0× —
prvič od 1902? (dominantna 1904–06); Vötter 0× → Šotter 7 + Toter 1
(ISTA Marjeta — dve črkovanji v istem dvojčkem paru r85/r86!); celo leto
vsi imenovani. EMŠO kampanja: 6 sidr na Gribljih (r4/r52/r53/r60/r64/r73)
— VSI SKLADNI. Anomalije: 4 para dvojčkov (r2/r3, r33/r34, r35/r36,
r54/r55 non-Griblje + r85/r86 h10 NARE); 3 dojenčki † na Gribljih; r61
pripisno neskladje († 1941 + poroka 1950?); r30 dvoje imen; kraj
forenzika: r5 = Zemelj, r58 = Grišiče (dva revidirana prva branja);
matični vpisi 20. stol. (r52 2007, r71/r72 2001); duhovniški pripis na
krstni vrstici (r9 nalepka: »otok umrl 17.8.1985 … duhovnik«). Excluded: 6.

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
DOKAZ = "research/issue17/parish-baptism-1907.json"
DOKAZ_P101 = "research/issue17/parish-baptism-1906.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (178, 188)        # skeni 178/179 (str. 165: glava 1907 + rows 1–8) – 188 (str. 172: rows 81–90)
FRAME_PAGES = (165, 172)
DATA_SCANS = [178, 180, 182, 183, 185, 186, 187, 188]
EXPECTED_CITED = [178, 180, 182, 183, 185, 186, 187, 188]
EXPECTED_PAGES = [165, 166, 167, 168, 169, 170, 171, 172]
EXPECTED_ENTRIES = 16
EXPECTED_DISTINCT = 14          # 14 berljivih hiš (+1 neberljiva r4)
EXPECTED_EXCLUDED = 6           # r5 Zemelj, r9 nalepka, r43 mrtvorojena, r44 strglek, r58 Grišiče, r90 Otok
EXPECTED_HOUSES = sorted({3, 5, 6, 7, 10, 11, 12, 13, 18, 27, 48, 49, 62, 83})
EXPECTED_VITALS_HOUSES = sorted([3, 5, 6, 7, 10, 10, 11, 12, 13, 18, 27, 48, 49, 62, 83])
EXPECTED_PT_IN_SET = ["3", "5", "6", "7", "10", "11", "12", "13", "18", "27", "62", "83"]
EXPECTED_PT_GAP = ["48", "49"]  # ponovitve že dokazanih (48 P99?, 49 P92) — luknja 41–60 ostaja samo h51
EXPECTED_REPEATS = 1            # NARE PRELOM — h10 ×2
EXPECTED_NEW_HOUSES = 0         # tretje leto z 0 novih (po P101 h4; P100 0, P101 1)
EXPECTED_VITALS_TOTAL = 429     # HOUSE_VITALS 341 + 15 (P102: krstna 1907; r4 neberljiva brez bloka)
BLOCKS_04105 = 403              # 315 + 15
KUMULATIV_ENTRIES = 363         # 347 + 16
KUMULATIV_HOUSES = 85
KUMULATIV_YEARS = 22            # 1886–1907
# kontinuitete (hiša → zadnje krstno leto pred 1907 v 04105, iz parish.ts)
CONTINUITY = {
    "3": 1902, "5": 1905, "6": 1905, "7": 1905, "10": 1900, "11": 1905,
    "12": 1905, "13": 1894, "18": 1906, "27": 1906, "48": 1905, "49": 1906,
    "62": 1891, "83": 1903,
}
# sidra/pini P102 (row, scan, hiša, pin):
ANCHORS = [
    (4, 178, "?", "NEBERLJIVO"),
    (4, 178, "?", "EMŠO"),
    (4, 178, "?", "Željko"),
    (11, 180, "11", "Žumič"),
    (48, 185, "3", "Papič"),
    (52, 185, "7", "Toter"),
    (53, 185, "12", "Dragoš"),
    (53, 185, "12", "POVRAT"),
    (60, 186, "5", "Štrucel"),
    (60, 186, "5", "Pecar"),
    (61, 186, "18", "Brinec"),
    (61, 186, "18", "MENJAVA DRUŽINE"),
    (64, 186, "48", "Kure"),
    (67, 186, "6", "MENJAVA DRUŽINE"),
    (69, 187, "49", "Brodarič"),
    (73, 187, "27", "Pozdirec"),
    (73, 187, "27", "ISTA BOTRA"),
    (76, 187, "13", "Šimec"),
    (76, 187, "13", "SELITEV"),
    (80, 187, "83", "Željko"),
    (85, 188, "10", "NARE PRELOM"),
    (85, 188, "10", "Brinec"),
    (86, 188, "10", "DVOJČEK"),
    (88, 188, "62", "VRZEL 16 LET"),
]
EMSO_ANCHOR_ROWS = {
    4: "1101907505283",
    52: "2708907505219",
    53: "2708907500520",
    60: "1709907505092",
    64: "0910907500078",
    73: "0511907305286",
}
GRIBLJE_TOTER = 1               # r85 »Toter« (r86 = Šotter — ISTA Marjeta)
GRIBLJE_MIH = 0                 # NOVELA: MIH 0× — prvič od 1902?
GRIBLJE_VOTTER = 0              # NOVELA: Vötter 0× → Šotter 7
MIDWIFE_NAMED = 16              # na Gribljih 16/16
MIDWIFE_EMPTY = 0


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
    """NOVELA P102: DVA nova dup para (+ 178/179 že P101).
    skeni 178/179 = str. 165 (dup par); 180/181 = str. 166 (dup par);
    182 = str. 167; 183/184 = str. 168 (dup par); stran == sken − 15
    (181–183); stran == sken − 16 (184+); 179/180 == sken − 14."""
    if scan in (178, 179):
        return 165
    if scan in (180, 181):
        return 166
    if scan == 182:
        return 167
    if scan in (183, 184):
        return 168
    if scan <= 183:
        return scan - 15
    return scan - 16


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p101 = json.load(open(DOKAZ_P101, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]
    houses_numeric = [h for h in houses if h != "?"]

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + JPEG probe data skenov
    inv["I3_data_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in dokaz["source"]["scans"])
    probes = {}
    for s in DATA_SCANS:
        if s <= len(urls):
            try:
                st2, img = http_get(urls[s - 1], UA)
                probes[s] = st2 == 200 and img[:2] == b"\xff\xd8"
            except Exception:  # noqa: BLE001
                probes[s] = False
    inv["I3_jpeg_probes"] = all(probes.get(s, False) for s in DATA_SCANS)
    inv["I3_cited_scans"] = dokaz["source"]["scans"] == EXPECTED_CITED

    # I4 — okvir leta: glava 1907 POD r87 str. 165 = skeni 178/179 (P101 dokazano)
    # … row 90 (sken 188, str. 172); glava 1908 str. 173 = sken 189; 90 vrstic;
    # TRI dup para; page_of_scan konsistenten
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        fr["yearStart"]["scan"] == 178 and fr["yearStart"]["page"] == 165
        and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 188 and fr["yearEnd"]["page"] == 172
        and fr["yearEnd"]["row"] == 90
        and fr["rowsTotal"] == 90
        and fr["duplicateScans"]["count"] == 3
        and {(p["scans"][0], p["scans"][1], p["page"]) for p in fr["duplicateScans"]["pairs"]}
        == {(178, 179, 165), (180, 181, 166), (183, 184, 168)}
    ) and all(page_of_scan(s) == p for s, p in zip(dokaz["source"]["scans"], dokaz["source"]["pages"]))
    inv["I4_glava_notes"] = (
        "POTRJEN" in fr["yearStart"]["note"]
        and "1908" in fr["yearEnd"]["note"]
        and fr["duplicateScans"]["count"] == 3
        and "P103 lead" in fr["glava1908"]["note"]
    )

    # I5 — štetja: 16 vpisov / 14 hiš + 1 neberljiva; 6 excluded; NARE PRELOM
    # (h10 ×2); 0 novih hiš; babica 16/16 + Toter 1 + Mih 0 + Vötter 0;
    # EMŠO sidri r4/r52/r53/r60/r64/r73
    houses_written = sorted({int(h) for h in dokaz["stats"]["housesWritten"]})
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(excluded) == EXPECTED_EXCLUDED
        and len(set(houses_numeric)) == EXPECTED_DISTINCT
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 1
        and houses_written == EXPECTED_HOUSES
        and dokaz["stats"]["intraYearRepeats"] == EXPECTED_REPEATS
        and "NARE PRELOM" in dokaz["stats"]["intraYearRepeatsNote"]
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["babica"]["griblje"].startswith("16/16")
        and sum(1 for e in entries if "Toter" in e["babica"]) == GRIBLJE_TOTER
        and sum(1 for e in entries if "Mih" in e["babica"]) == GRIBLJE_MIH
        and sum(1 for e in entries if "Vötter" in e["babica"]) == GRIBLJE_VOTTER
        and sum(1 for e in entries if "Šotter" in e["babica"]) == 7
        and all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
                for row, EMSO in EMSO_ANCHOR_ROWS.items())
    )

    # I6 — PT klasifikacija: 12 v naboru + 2 v luknji (48/49 = ponovitve);
    # 0 novih hiš; PT_GAP_KNOWN nespremenjen (ostaja samo 51);
    # kumulativ 363/85/22
    pts = pt_house_set()
    inset = sorted((h for h in set(houses_numeric) if h in pts), key=int)
    gap = sorted((h for h in set(houses_numeric) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["pt"]["inNabor"] == 12
        and dokaz["stats"]["pt"]["inGap"] == 2
        and dokaz["stats"]["pt"]["inGapHouses"] == EXPECTED_PT_GAP
        and dokaz["stats"]["newSampleHouses"] == 0
        and dokaz["stats"]["cumulative"]["entries"] == KUMULATIV_ENTRIES
        and dokaz["stats"]["cumulative"]["houses"] == KUMULATIV_HOUSES
        and dokaz["stats"]["cumulative"]["years"] == KUMULATIV_YEARS
        and '"51"' not in pt_gap_set                            # luknja 51 ostaja
        and '"48"' in pt_gap_set and '"49"' in pt_gap_set       # ponovitve že dokazanih
    )

    # I7 — sidra (24 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r4 = e_by_row(4)
    r61 = e_by_row(61)
    r73 = e_by_row(73)
    r76 = e_by_row(76)
    r85 = e_by_row(85)
    r86 = e_by_row(86)
    inv["I7_anchors"] = (
        ok7
        # r4 — hiša neberljivo + ŽELJKO×KURE krog + EMŠO sidro
        and r4["child"] == "Marija" and "Željko" in r4["father"]
        and "Barbara Kure" in r4["mother"] and "NEBERLJIVO" in " ".join(r4["notes"])
        # r61 — h18 menjava Šimec → Peter Brinec × Ana Butala
        and r61["child"] == "Alojzij" and "Peter Brinec" in r61["father"]
        and "Butala" in r61["mother"] and "MENJAVA DRUŽINE" in " ".join(r61["notes"])
        # r73 — h27 9. VPIS Pozdirec 2. leto + ISTA botra + hiša Kurrent 27
        and r73["child"] == "Helena" and "Pozdirec" in r73["father"]
        and "Žugelj" in r73["mother"] and "ISTA BOTRA" in " ".join(r73["notes"])
        # r76 — h13 selitev Šimec×Kambič h18→h13 + vrzel 13 let
        and r76["child"] == "Marija" and "Šimec" in r76["father"]
        and "Kambič" in r76["mother"] and "SELITEV" in " ".join(r76["notes"])
        and "13 LET" in " ".join(r76["notes"])
        # r85/r86 — h10 ×2 NARE PRELOM dvojčka †
        and r85["child"] == "Jožef" and r86["child"] == "Anton"
        and "Janez Brinec" in r85["father"] and "Janez Brinec" in r86["father"]
        and "NARE PRELOM" in " ".join(r85["notes"])
        and "25.12.1907" in " ".join(r85["notes"])
        and "19/12" in " ".join(r86["notes"])
        and "DVOJČEK" in " ".join(r86["notes"])
    )

    # I8 — kontinuitete: vsaka hiša ima pravilen zadnji prior-leto v parish.ts
    vitals = parish_vitals_04105()
    prior = {}
    for v in vitals:
        h, y = v["houseNo"], v["year"]
        if h in CONTINUITY and y is not None and y < 1907:
            if h not in prior or y > prior[h]:
                prior[h] = y
    inv["I8_continuity"] = all(prior.get(h) == y for h, y in CONTINUITY.items())

    # I9 — vitals projekcija: 04105 blokov 330 (315 + 15); 1907 bloki == 15
    # (16 vpisov − 1 neberljiva); SKUPNI HOUSE_VITALS (vse 3 knjige) == 356
    blocks_1907 = [v for v in vitals if v["year"] == 1907]
    all_src = open(PARISH_TS, encoding="utf-8").read()
    total_blocks = len(re.findall(r"\{[^{}]*?bookSignature:\s*\"(04105|04894|04455)\"[^{}]*?\}", all_src, re.S))
    inv["I9_vitals_projection"] = (
        len(vitals) == BLOCKS_04105
        and len(blocks_1907) == EXPECTED_ENTRIES - 1
        and sorted(int(v["houseNo"]) for v in blocks_1907) == EXPECTED_VITALS_HOUSES
        and total_blocks == EXPECTED_VITALS_TOTAL
    )

    # I10 — neodvisen preracun: vsi village == Griblje; sken→stran konsistenten
    # z vnosnim scan/page; P101 kumulativ == 347/85 (veriga)
    ok10 = all(e["village"] == "Griblje" for e in entries)
    ok10 = ok10 and all(
        e["page"] == page_of_scan(e["scan"]) for e in entries)
    ok10 = ok10 and all(
        any(e["scan"] == s for s in dokaz["source"]["scans"]) for e in entries)
    cum_p101 = dokaz_p101["stats"]["cumulative"]
    ok10 = ok10 and cum_p101["entries"] == 347 and cum_p101["houses"] == 85
    inv["I10_independent_recalc"] = ok10

    return inv


def main():
    inv = verify()
    failed = [k for k, v in inv.items() if not v]
    for k, v in inv.items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
    if failed:
        print(f"\n{len(failed)} FAILED: {', '.join(failed)}")
        sys.exit(1)
    print("\nALL INVARIANTS PASS (I1–I10)")


if __name__ == "__main__":
    main()
