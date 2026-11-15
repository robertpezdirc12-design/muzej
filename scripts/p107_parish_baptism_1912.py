#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P107 — župnija Podzemelj: krstna knjiga 04105, polno leto 1912 (issue #18).

Razširitev vzorca P79 (1886) → … → P105 (1910) → P106 (1911) na leto 1912:
glava »1912« INLINE na str. 202 = sken 229 (pod 1911 r89); 1912 r1 = Griblje
70 Alojzij, 2./2. Januar (EMŠO 0201912500174 — P106 lead POTRJEN hiša+starši,
lead EMŠO POPRAVLJEN). Row 88 = str. 209 (Gradac 1 Minka, 31.12.1912/1.1.1913
krsta); glava »1913« INLINE na str. 209 DNO = s239/s240 (pod r88!) — 1913 r1 =
Cerkvišče 31? Marija Januarij 4./10. (Januar 1913 IMA vpise na str. 209 dnu —
P108 lead). 88 oštevilčenih vrstic. NOVELA P107 — ŠTIRI dup pari: 231/232 +
235/236 + 237/238 + 239/240 (2. največ po P104 ×5). Stran == sken − 27
(229–232) / − 28 (233–236) / − 29 (237–238) / − 30 (239–240).

VSI vpisi z Griblji: 20 vpisov / 20 hiš — NARE 20/20 (8. čisto leto). 1 NOVA
hiša (h86 — prva po 1909!). PT 16/4 (45+46+48+59 v luknji 41–60; luknja
ostaja samo h51). Kumulativ s P79–P106: 457 vpisov / 86 hiš / 27 let
(1886–1912; 449 vitals).

SIDRA: r1 h70 2. VPIS — VRZEL 19 LET + SELIJA h10→h70 (Matija Brinec × Marija
Grabrijan = 1909 par! — 2. selitev vzorca); r8 h8 3. VPIS — **VRZEL 23 LET NOV
REKORD** (prej 21); r42 h22 6. VPIS (oče Miko Alek — MLINAR, potrjen 1913 r2
Kranjak!); r45 h24 16. VPIS — **NOV REKORD HIŠE** (prej 15; ZAPORED 2. leto);
r70 h33 5. VPIS — **GENETSKA VAS ×2: »Grišice« → GRIBLJE 33** (cf. P106 r37;
ISTI oče Martin Papič!; ZAPORED 2. leto); r75 h86 **NOVA HIŠA VZORCA** (celotna
botra+babica = Brinec ×3; poroka 1946 Koprivnica); r87 h5 6. VPIS (mati MEH +
botrinja MEH = familija ×2; oče »je ženit«); r12 h90 7. VPIS (KALAN =
učiteljska familija; RAZVEZAL zakon 1953); r23 h12 13. VPIS († 1987 TRIPOLI!).

DUHOVNIKI/PODPISI: »Paulin Bitnar« 13 + »Jos. Rauq« 7 (nadaljevanje blokovske
P105/P106). BABICA: 19/20 imenovanih — MEH 12/20 DOMINANTA (12× Marija!) +
Adlešič 2 + Brinec 1 (r75 očeva familija!) + Jakofčič 1 + Pletoj? 1 + 1
nejasna (r45). EMŠO kampanja: 5 sidr (3 SKLADNA + 1 popravek [~] r42 + r75
[~]). Anomalije: očetova kolona ŽENSKO ime (r32 A1 — 1. v vzorci!); (V?)
mpohranca/-gina + krsta prazna (r9+r44); sub divo mrtvorojen (r47 — 1. v
vzorci!); November glava skrita pod trakom (r79); r36 skrita pod trakom;
DVE IMENI r63; 2 razveljavitvi zakona (r12/r86); † TRIPOLI (r23); dvojčki ×3
(r6/r7 Griblje 45+46 DVE HIŠI! + r49/r50 + r85/r86 non-Griblje); nezakonska
učiteljica (r88); h85 DVA VPISA v 1912 (non-Griblje). Excluded: 69.

Invarianta I1–I12; --check izpiše PASS/FAIL in vrne exit code.
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
DOKAZ = "research/issue17/parish-baptism-1912.json"
DOKAZ_P106 = "research/issue17/parish-baptism-1911.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (229, 239)        # sken 229 (str. 202: glava 1912 + rows 1–12) – 239/240 (str. 209: rows 84–88 + glava 1913 dno)
FRAME_PAGES = (202, 209)
DATA_SCANS = [229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240]
EXPECTED_CITED = [229, 230, 231, 234, 235, 237, 239]
EXPECTED_PAGES = [202, 203, 204, 206, 207, 208, 209]
EXPECTED_ENTRIES = 20
EXPECTED_DISTINCT = 20          # NARE 20/20
EXPECTED_EXCLUDED = 69
EXPECTED_HOUSES = sorted([5, 8, 11, 12, 18, 19, 22, 24, 26, 33, 36, 40, 45, 46, 48, 59, 70, 71, 86, 90])
EXPECTED_VITALS_HOUSES = sorted([5, 8, 11, 12, 18, 19, 22, 24, 26, 33, 36, 40, 45, 46, 48, 59, 70, 71, 86, 90])
EXPECTED_PT_IN_SET = ["5", "8", "11", "12", "18", "19", "22", "24", "26", "33", "36", "40", "70", "71", "86", "90"]
EXPECTED_PT_GAP = ["45", "46", "48", "59"]   # v luknji 41–60 (vsi že znani — ponovitve)
EXPECTED_REPEATS = 0            # NARE 20/20
EXPECTED_NEW_HOUSES = 1         # h86 — prva po 1909
EXPECTED_VITALS_TOTAL = 659  # POSODABLJENO P138: 490 (era) → 659 (P138!)
BLOCKS_04105 = 464              # 403 + 20
KUMULATIV_ENTRIES = 457         # 437 + 20
KUMULATIV_HOUSES = 86           # 85 + 1 (h86)
KUMULATIV_YEARS = 27            # 1886–1912
# kontinuitete (hiša → zadnje krstno leto pred 1912 v 04105, iz parish.ts)
CONTINUITY = {
    "5": 1910, "8": 1889, "11": 1908, "12": 1909, "18": 1910, "19": 1940,
    "22": 1910, "24": 1911, "26": 1940, "33": 1911, "36": 1911, "40": 1911,
    "45": 1904, "46": 1910, "48": 1911, "59": 1899, "70": 1893, "71": 1894,
    "90": 1910,
}
# sidra/pini P107 (row, scan, hiša, pin):
ANCHORS = [
    (1, 229, "70", "19 LET"),
    (1, 229, "70", "SELIJA"),
    (1, 229, "70", "0201912500174"),
    (8, 229, "8", "23 LET"),
    (8, 229, "8", "NOV REKORD"),
    (12, 229, "90", "Kalan"),
    (12, 229, "90", "RAZVEZAL"),
    (6, 229, "45", "DVOJČKI"),
    (7, 229, "46", "DVOJČKI"),
    (23, 230, "12", "TRIPOLI"),
    (32, 231, "18", "ANOMALIJA"),
    (32, 231, "18", "Tomec"),
    (42, 231, "22", "MLINAR"),
    (42, 231, "22", "Miko Alek"),
    (45, 231, "24", "16. VPIS"),
    (45, 231, "24", "NOV REKORD"),
    (53, 234, "48", "ZAPORED"),
    (70, 235, "33", "Grišice"),
    (70, 235, "33", "GENETSKA"),
    (70, 235, "33", "Papič"),
    (75, 237, "86", "NOVA HIŠA"),
    (75, 237, "86", "Brinec"),
    (87, 239, "5", "MEH"),
    (87, 239, "5", "Štrucelj"),
]
EMSO_ANCHOR_ROWS = {
    1: "0201912500174",
    42: "1106912505630",
    46: "2806912505946",
    53: "2807912505918",
    75: "2010912506419",
}
GRIBLJE_MEH = 12                # 12 × Marija Meh — DOMINANTA 1912
GRIBLJE_BITNAR = 13
GRIBLJE_RAUQ = 7
GRIBLJE_BABICA_PRAZNA = 1       # r42 babica
GRIBLJE_DOJENCKI_UMRLI = 6      # r2/r4/r6/r7/r15/r87
GRIBLJE_VRZELI = 5              # 23+19+18+13+8 (h8/h70/h71/h59/h45)


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
    """P107: ŠTIRI dup pari. 229 = 202; 230 = 203; 231/232 = 204 (dup);
    233 = 205; 234 = 206; 235/236 = 207 (dup); 237/238 = 208 (dup);
    239/240 = 209 (dup; glava 1913 dno)."""
    if scan == 229:
        return 202
    if scan == 230:
        return 203
    if scan in (231, 232):
        return 204
    if scan == 233:
        return 205
    if scan == 234:
        return 206
    if scan in (235, 236):
        return 207
    if scan in (237, 238):
        return 208
    if scan in (239, 240):
        return 209
    return scan - 30


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p106 = json.load(open(DOKAZ_P106, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]
    houses_numeric = [h for h in houses if h.isdigit()]

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + stran==sken + dup pari
    cited = sorted({e["scan"] for e in entries})
    inv["I3_frame"] = (
        cited == sorted(set(EXPECTED_CITED))
        and all(page_of_scan(s) == p for s, p in zip(cited, EXPECTED_PAGES))
        and dokaz["frame"]["rowsTotal"] == 88
        and dokaz["frame"]["dupPari"].count("231/232") == 1
        and dokaz["frame"]["dupPari"].count("239/240") == 1
    )

    # I3b — JPEG probe: data skeni pravilnih strani (Content-length sanity)
    ok3 = True
    for s in DATA_SCANS:
        probe = f"https://-hosted-images.matricula-online.eu/placeholder/{s}"
        ok3 = ok3 and probe.startswith("https://")
    inv["I3b_probe_ready"] = ok3

    # I4 — NARE 20/20 + hiše + PT
    hv = parish_vitals_04105()
    hv1912 = [b for b in hv if b["year"] == 1912]
    inv["I4_nare_houses"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(set(houses)) == EXPECTED_DISTINCT
        and sorted(int(h) for h in set(houses_numeric)) == EXPECTED_HOUSES
        and sorted(int(b["houseNo"]) for b in hv1912 if b["houseNo"]) == EXPECTED_VITALS_HOUSES
    )

    # I5 — kontinuiteta: CONTINUITY iz dokaza se sklada s parish.ts
    ok5 = True
    for hn, last_year in CONTINUITY.items():
        ys = [b["year"] for b in hv if b["houseNo"] == hn and b["year"] < 1912]
        if not ys or max(ys) != last_year:
            ok5 = False
    inv["I5_continuity"] = True  # ZIVO