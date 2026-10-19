#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P100 — župnija Podzemelj: krstna knjiga 04105, polno leto 1905 (issue #18).

Razširitev vzorca P79 (1886) → … → P97 (1902) → P98 (1903) → P99 (1904) na
leto 1905: okvir glava »1905« na str. 150 POD r90 (sken 160, P99 dokazano;
1905 r1 = Gradac 45 Antonija, 2./7. Januar) – row 87 na str. 157 (sken 169;
glava »1906« na str. 158 = sken 170/171 — 1906 r1 = »Gorn?« 34 Jožef, P101
lead). 87 oštevilčenih vrstic. NOVELA P100 — DVA podvojena para skenov v
okviru leta: 164/165 (str. 154, rows 40–51) + 168/169 (str. 157, rows 76–87)
+ dup par 170/171 (str. 158) = ŽE leto 1906. Stran == sken − 10 (160–164) /
− 11 (165–168) / − 12 (169–170) / − 13 (171+) — premik offseta za vsak dup
par (vzorec P97 −6/−7/−8, P98 −8/−9, P99 −9/−10). Format = spread (levo
data, desno Roditelja/Botra/Babica; naslov razporejen čez obe strani).
16 vpisov / 15 hiš — NARE PRELOM (h12 ×2: r4 Neža + r15 Ana — 2. intra-letna
ponovitev po 1901!); 0 NOVIH hiš (vse 15 že dokumentirane); h42 (NOVA 1904)
se ponovi že 1905 — MENJAVA DRUŽINE (Štraus → Perdinec/Pezdirec). LETO
VELIKIH VRZELI: h39 18 let (1886→1905 — najdaljša v vzorcu!), h11 15 let
(1890→1905), h1 4 leta (1900→1905). Sidra: r4 h12 RAZVELJAVITEV ZAKONA
(sodišče Novo mesto 23.5.1949 — 1. gribeljska!) + 9. VPIS; r49 h6 2. VPIS
ZAPORED (isti starša + ISTA botra Željko+Klepec kot 1904) + vijolični
pripis »Po odloči Okrajnega sodišča v Črnomelju« + EMŠO neskladje spola
(ženski znak, ime Janez); r69 h58 8. VPIS — ISTI PAR Požek × Kambič (P98
rešitev tretjič!); r66 h25 5. VPIS — Brinec × Šegina (3. dokumentacija);
r50 h7 3. VPIS — Jakob Toter × Katarina Jakobšič (1901 par); r62 h22 4.
VPIS — Nikolaj Milek (1904 oče) + botra Ana Požek; r82 h66 3. VPIS (2.
zapored; † 1944). Duhovniki (celo leto 87): Hengsfeld 54 dominant + Ravq 26
+ Dostál 1 [~ r43] + neberljivo 5 (odrezani); na Gribljih: Ravq 7 + Hengsfeld
8 + odrezan 1 (r15). Babica (celo leto): 78 imenovanih / 5 praznih (r30,
r37, r44, r46, r79 »—«) / 3 neberljive (r1–r3 odrezani, r72 ditto); na
Gribljih 16/16: Toter 12 + Mih 3 + Kambič [~] 1. EMŠO kampanja 1982–84
(Šimonič Mira/Nuša): 17 sidr. Anomalije: r8 Gradac VSTAVLJEN vpis 2007 (2.
primer po P99 r19); r85 Gradac žandar Wachtmeister (2. po 1903 Morvet);
r76/r79/r84 »Hudorovac samska ciganka« nezakonski + legitimizacija 1915;
r71/r72 dvojčka (ditto); r73 razveza Zagreb. Excluded: 4 (r2 pripis pokrije,
r3 + r27 odrezani, r40 nalepka). Excluded: 4.

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
DOKAZ = "research/issue17/parish-baptism-1905.json"
DOKAZ_P99 = "research/issue17/parish-baptism-1904.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (160, 170)        # skeni 160 (str. 150: r90 1904 + glava 1905 + rows 1–3) – 170 (str. 158: glava 1906 + rows 1–5 1906)
FRAME_PAGES = (150, 158)
EXPECTED_ENTRIES = 16
EXPECTED_DISTINCT = 15          # 16 vpisov / 15 hiš (h12 ×2 — NARE prelom)
EXPECTED_EXCLUDED = 4           # r2 pripis, r3 + r27 odrezani, r40 nalepka
EXPECTED_CITED = [160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170]
EXPECTED_PAGES = [150, 151, 152, 153, 154, 154, 155, 156, 157, 157, 158]
DATA_SCANS = [160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170]
EXPECTED_HOUSES = sorted({1, 5, 6, 7, 11, 12, 22, 23, 25, 34, 39, 42, 48, 58, 66})
EXPECTED_PT_IN_SET = ["1", "5", "6", "7", "11", "12", "22", "23", "25", "34", "39", "66"]
EXPECTED_PT_GAP = ["42", "48", "58"]  # ponovitve že dokazanih (42 P99, 48 P93, 58 P84) — vse v luknji 41–60
EXPECTED_REPEATS = 15           # 16 vpisov − 1 intra-letni ponovitev (h12)
EXPECTED_NEW_HOUSES = 0         # TRETJIKRAT v vzorcu 0 novih (po 1903–1904 mešano)
EXPECTED_VITALS_TOTAL = 490     # HOUSE_VITALS 307 + 16 (P100: krstna 1905); P101: + 18 (1906); P102: + 15 (1907)
KUMULATIV_ENTRIES = 329         # 313 + 16
KUMULATIV_HOUSES = 84
KUMULATIV_YEARS = 20            # 1886–1905
BLOCKS_04105 = 441              # 386 + 17 (P106: krstna 1911)
# kontinuitete (hiša → zadnje krstno leto pred 1905 v 04105, iz parish.ts)
CONTINUITY = {
    "1": 1900, "5": 1903, "6": 1904, "7": 1901, "11": 1890, "12": 1903,
    "22": 1904, "23": 1903, "25": 1902, "34": 1903, "39": 1886, "42": 1904,
    "48": 1898, "58": 1903, "66": 1904,
}
# sidra/pini P100 (row, scan, hiša, pin):
ANCHORS = [
    (4, 161, "12", "RAZVELJAVITEV ZAKONA"),
    (4, 161, "12", "9. VPIS"),
    (14, 161, "5", "Štrucelj"),
    (15, 161, "12", "NARE"),
    (19, 162, "34", "SEGINA signal"),
    (28, 163, "39", "VRZEL 18 LET"),
    (29, 163, "42", "MENJAVA DRUŽINE"),
    (31, 163, "11", "VRZEL 15 LET"),
    (42, 164, "23", "Brinec"),
    (49, 164, "6", "2. VPIS ZAPORED"),
    (50, 164, "7", "Jakob Toter"),
    (57, 166, "48", "Berkovec"),
    (62, 166, "22", "Milek"),
    (65, 167, "1", "ŽELJKO signal"),
    (66, 167, "25", "Šegina"),
    (69, 167, "58", "Požek"),
    (82, 168, "66", "Hrižan"),
]
GRIBLJE_TOTER = 12
GRIBLJE_MIH = 3
MIDWIFE_NAMED = 78              # celo leto (87 vrstic)
MIDWIFE_EMPTY = 5               # r30 + r37 + r44 + r46 + r79 (»—«)
EMSO_ANCHOR_ROW = 4             # h12 Neža — 1201905505202
EMSO_ANCHOR_ROW_2 = 19          # h34 Ana — 0103905505058


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
    """NOVELA P100: DVA podvojena para v okviru leta (+ en 170/171 = 1906).
    stran == sken − 10 (160–164); skeni 164/165 = str. 154 (dup par);
    stran == sken − 11 (165–168); skeni 168/169 = str. 157 (dup par);
    stran == sken − 12 (169–170); skeni 170/171 = str. 158 (dup par, 1906);
    stran == sken − 13 (171+)."""
    if scan in (164, 165):
        return 154
    if scan in (168, 169):
        return 157
    if scan in (170, 171):
        return 158
    if scan <= 164:
        return scan - 10
    if scan <= 168:
        return scan - 11
    if scan <= 170:
        return scan - 12
    return scan - 13


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p99 = json.load(open(DOKAZ_P99, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]

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

    # I4 — okvir leta: glava 1905 POD r90 na str. 150 (sken 160, P99 dokazano)
    # … row 87 (sken 169, str. 157); glava 1906 na str. 158 (sken 170/171);
    # 87 vrstic; DVA dup para; page_of_scan konsistenten
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        fr["yearStart"]["scan"] == 160 and fr["yearStart"]["page"] == 150
        and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 169 and fr["yearEnd"]["page"] == 157
        and fr["yearEnd"]["row"] == 87
        and fr["rowsTotal"] == 87
        and fr["duplicateScans"]["pairs"] == [{"scans": [164, 165], "page": 154},
                                              {"scans": [168, 169], "page": 157}]
        or fr["duplicateScans"]["count"] == 2
    ) and all(page_of_scan(s) == p for s, p in zip(dokaz["source"]["scans"], dokaz["source"]["pages"]))
    inv["I4_glava_notes"] = (
        "POD r90" in fr["yearStart"]["note"]
        and "Gradac 45" in fr["yearStart"]["note"]
        and "1906" in fr["yearEnd"]["note"]
        and fr["duplicateScans"]["count"] == 2
    )

    # I5 — štetja: 16 vpisov / 15 hiš; 4 excluded; NARE PRELOM (h12 ×2);
    # 0 novih hiš; babica celo leto 78/5 + Toter 12× na Gribljih; EMŠO sidri
    houses_written = sorted({int(h) for h in dokaz["stats"]["housesWritten"]})
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(excluded) == EXPECTED_EXCLUDED
        and len(set(houses)) == EXPECTED_DISTINCT
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and houses_written == EXPECTED_HOUSES
        and dokaz["stats"]["intraYearRepeats"] == 1
        and "NARE" in dokaz["stats"]["intraYearRepeatsNote"]
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["midwifeNamed"] == MIDWIFE_NAMED
        and dokaz["stats"]["midwifeEmpty"] == MIDWIFE_EMPTY
        and sum(1 for e in entries if "Toter" in e["babica"]) == GRIBLJE_TOTER
        and sum(1 for e in entries if "Mih" in e["babica"]) == GRIBLJE_MIH
        and EMSO_ANCHOR_ROW_EMSO in json.dumps(e_by_row(EMSO_ANCHOR_ROW), ensure_ascii=False)
        and EMSO_ANCHOR_ROW_2_EMSO in json.dumps(e_by_row(EMSO_ANCHOR_ROW_2), ensure_ascii=False)
    )

    # I6 — PT klasifikacija: 13 v naboru + 2 v luknji (42/48 = ponovitvi);
    # 0 novih hiš; PT_GAP_KNOWN nespremenjen (ostaja samo 51); kumulativ 329/84/20
    pts = pt_house_set()
    inset = sorted((h for h in set(houses) if h in pts), key=int)
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    pt_gap_line = re.search(r"PT_GAP_KNOWN[^\n]*", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGap"] == EXPECTED_PT_GAP
        and dokaz["stats"]["ptInNabor"] == 12
        and dokaz["stats"]["newSampleHouses"] == 0
        and dokaz["stats"]["cumulative"]["entries"] == KUMULATIV_ENTRIES
        and dokaz["stats"]["cumulative"]["houses"] == KUMULATIV_HOUSES
        and dokaz["stats"]["cumulative"]["years"] == KUMULATIV_YEARS
        and '"51"' not in pt_gap_set                            # luknja 51 ostaja
        and '"42"' in pt_gap_set and '"48"' in pt_gap_set       # ponovitvi že dokazanih
    )

    # I7 — sidra (17 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r4 = e_by_row(4)
    r49 = e_by_row(49)
    r69 = e_by_row(69)
    inv["I7_anchors"] = (
        ok7
        # r4 — h12 9. VPIS + razveljavitev zakona (Novo mesto 23.5.1949)
        and r4["child"] == "Neža" and "Janez Dragoš" in r4["father"]
        and "23.5.1949" in " ".join(r4["notes"])
        # r49 — h6 2. VPIS ZAPORED + ista botra Željko+Klepec + vijolični pripis
        and r49["child"] == "Janez" and "Nikolaj Željko" in r49["botra"]
        and "Marija Klepec" in r49["botra"]
        and "Okrajnega sodišča" in " ".join(r49["notes"])
        # r69 — h58 8. VPIS — Požek × Kambič (P98 rešitev 3×)
        and r69["child"] == "Matija" and "Janez Požek" in r69["father"]
        and "Katarina Kambič" in r69["mother"]
    )

    # I8 — kontinuitete: vsaka hiša ima pravilen zadnji prior-leto v parish.ts
    vitals = parish_vitals_04105()
    prior = {}
    for v in vitals:
        h, y = v["houseNo"], v["year"]
        if h in CONTINUITY and y is not None and y < 1905:
            if h not in prior or y > prior[h]:
                prior[h] = y
    inv["I8_continuity"] = all(prior.get(h) == y for h, y in CONTINUITY.items())

    # I9 — vitals projekcija: 04105 blokov 297 (281 + 16); 1905 bloki == 16;
    # SKUPNI HOUSE_VITALS (vse 3 knjige) == 323 (307 + 16)
    blocks_1905 = [v for v in vitals if v["year"] == 1905]
    all_src = open(PARISH_TS, encoding="utf-8").read()
    total_blocks = len(re.findall(r"\{[^{}]*?bookSignature:\s*\"(04105|04894|04455)\"[^{}]*?\}", all_src, re.S))
    inv["I9_vitals_projection"] = (
        len(vitals) == BLOCKS_04105
        and len(blocks_1905) == EXPECTED_ENTRIES
        and sorted(int(v["houseNo"]) for v in blocks_1905) == sorted(EXPECTED_HOUSES + [12])
        and sum(1 for v in vitals if v["houseNo"] == "12" and v["year"] == 1905) == 2
        and total_blocks == EXPECTED_VITALS_TOTAL
    )

    # I10 — neodvisen preracun: vsi village == Griblje; sken→stran konsistenten
    # z vnosnim scan/page; P99 kumulativ == 313/84 (veriga)
    ok10 = all(e["village"] == "Griblje" for e in entries)
    ok10 = ok10 and all(
        e["page"] == page_of_scan(e["scan"]) for e in entries)
    ok10 = ok10 and all(
        any(e["scan"] == s for s in dokaz["source"]["scans"]) for e in entries)
    cum_p99 = dokaz_p99["stats"]["cumulative"]
    ok10 = ok10 and cum_p99["entries"] == 313 and cum_p99["houses"] == 84
    inv["I10_independent_recalc"] = ok10

    return inv


EMSO_ANCHOR_ROW_EMSO = "1201905505202"
EMSO_ANCHOR_ROW_2_EMSO = "0103905505058"


def main():
    inv = verify()
    failed = [k for k, v in inv.items() if not v]
    for k in sorted(inv):
        print(f"{'PASS' if inv[k] else 'FAIL'}  {k}")
    if failed:
        print(f"\n{len(failed)} FAILED: {', '.join(failed)}")
        return 1
    print("\nP100 parish-baptism-1905: ALL INVARIANTS PASS (I1–I10)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
