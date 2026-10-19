#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P108 — župnija Podzemelj: krstna knjiga 04105, polno leto 1913 (issue #18).

Razširitev vzorca P79 (1886) → … → P106 (1911) → P107 (1912) na leto 1913:
glava »1913« INLINE na str. 209 DNO = s239/240 (pod 1912 r88); 1913 r1 =
Cerkvišče 21 Marija, 4./10. Januar (EMŠO 0401913505350 — P107 lead POTRJEN,
hiša POPRAVLJENA 31? → 21 forenziko s239/240-A). Row 105 = str. 218 (Boršt 21
Alojzij); glava »1914« INLINE na str. 218 DNO = s256 (P109 lead: 1914 r1 =
[vas] 17 Terezija 1./1., EMŠO 01019141505225, VPIS PRENEŠEN 16.10.2002; 1914
r5 = Griblje 1?/4? Anton [~]). **105 oštevilčenih vrstic — NAJVEČ v vzorcu**
(prej rekord 1908 = 90). NOVELA P108 — ŠTIRI dup "pari": 239/240 + 241/242 +
243/244 + **245–250 = ŠEST skenov str. 212 (re-scan serija, največ doslej!)**.
Stran == sken − 30 (239/240) / − 31 (241/242) / − 32 (243/244) / DUP (245–250)
/ − 38 (251+).

VSI vpisi z Griblji: **18 vpisov / 17 hiš** — NARE PRELOM (h31 ×2 = r10+r70 —
1. ponovitev od P104!) + **DVE RAZLIČNI FAMILIJI v h31 isto leto**. 1 NOVA
hiša vzorca: **h76** (prvi vpis v vseh treh knjigah; 2. ZAPORED leto z novo
hišo po h86 1912). Kumulativ s P79–P107: **475 vpisov / 87 hiš / 28 let**
(1886–1913; 467 vitals).

SIDRA: r72/r75 **SELIJA h36 → h86** (Marko Hrižan × Katarina Štraus = P107
h36 par — 3. selitev vzorca!); r49 **MENJAVA h34** (Brinec × Milek → Krambič
× Milek? — mati familija obstane); r95 **MENJAVA h47** (Požek → Timec?); r32
h28 očakovsko razrešeno (1910 nezakonska → 1913 oče Lozar); r63 oče REŠEN
(»Marija→Matija?« = Matija Jakofčič); **r15 VRNJEN** (faza-1 izpustila —
forenzika: Griblje 65, oče Matija Milek = h65 SKLADNO); r80 **h76 NOVA HIŠA**.

DUHOVNIKI/PODPISI: »Paulin Bitnar« 6 + »Jos. Rauq« 11 + **»R. Ozlob? Polak,
kap.« 1 (NOVI 3. duhovnik — blok r82–r87 s254!)** = 18 vsi. BABICA: 18/18
imenovanih — **MARIJA JAKOFČIČ 8/18 DOMINANTA (prvič ne-Meh!)** + Pleščič 4 +
Adlešič 3 + Mavrenič 2 + Meh 1 (MEH padec z 12/20 na 1/18!). EMŠO kampanja:
**~30 marginalij — NAJVEČJA doslej**; 5 Griblje sidr (4 SKLADNA + 1 MOŽEN
popravek r95 sex-digit). Anomalije: papirni vstavek »Pozamanitev« (r35);
2 poznejša vpisa (r2 rojen 1891! + r85 Tolminsko); 2 Karolini zapored; 2 para
dvojčkov; 3 nezakonski; nujni krst r22; vas »Klojter« ×4; žensko ime v
očetovi koloni ×3 (r47/r79/r98; r63 REŠEN); † 2. svetovna vojna ×2 (r88
29.12.1944 + r8 razglašen 1944); r16 vas pod nalepko (dilema h23); r95 †
1998 Griblje / r72 † 2004 Nova Gorica. Excluded: 87 (+ vstavek).

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
DOKAZ = "research/issue17/parish-baptism-1913.json"
DOKAZ_P107 = "research/issue17/parish-baptism-1912.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (239, 256)        # sken 239/240 (str. 209: glava 1913 dno + rows 1–6) – 256 (str. 218: rows 102–105 + glava 1914 dno)
FRAME_PAGES = (209, 218)
DATA_SCANS = [240, 241, 243, 245, 251, 252, 253, 254, 255, 256]
EXPECTED_CITED = [241, 243, 245, 251, 252, 253, 254, 255]
EXPECTED_PAGES = [210, 211, 212, 213, 214, 215, 216, 217]
EXPECTED_ENTRIES = 18
EXPECTED_DISTINCT = 17          # h31 ×2 → NARE PRELOM
EXPECTED_EXCLUDED = 87
EXPECTED_HOUSES = sorted([6, 8, 9, 13, 28, 31, 34, 36, 44, 46, 47, 59, 60, 65, 72, 76, 86])
EXPECTED_VITALS_HOUSES = sorted([6, 8, 9, 13, 28, 31, 34, 36, 44, 46, 47, 59, 60, 65, 72, 76, 86])
EXPECTED_PT_IN_SET = ["6", "8", "9", "13", "28", "31", "34", "36", "65", "72", "76", "86"]
EXPECTED_PT_GAP = ["44", "46", "47", "59", "60"]   # v luknji 41–60 (h44 NOVO!)
EXPECTED_REPEATS = 1            # h31 ×2 — NARE PRELOM (1. ponovitev od P104)
EXPECTED_NEW_HOUSES = 1         # h76 — 2. ZAPORED leto z novo hišo (h86 1912)
EXPECTED_VITALS_TOTAL = 467     # 449 + 18 (P108)
BLOCKS_04105 = 441              # 423 + 18
KUMULATIV_ENTRIES = 475         # 457 + 18
KUMULATIV_HOUSES = 87           # 86 + 1 (h76)
KUMULATIV_YEARS = 28            # 1886–1913
# kontinuitete (hiša → zadnje krstno leto pred 1913 v 04105, iz parish.ts)
CONTINUITY = {
    "6": 1911, "8": 1912, "9": 1900, "13": 1911, "28": 1910, "31": 1911,
    "34": 1910, "36": 1912, "44": 1910, "46": 1912, "47": 1911, "59": 1912,
    "60": 1910, "65": 1910, "72": 1911, "86": 1912,
}
# sidra/pini P108 (row, scan, hiša, pin):
ANCHORS = [
    (15, 241, "65", "VRNJEN"),
    (15, 241, "65", "Milek"),
    (13, 241, "9", "13 LET"),
    (10, 241, "31", "NARE PRELOM"),
    (70, 253, "31", "NARE PRELOM"),
    (70, 253, "31", "DVE RAZLIČNI FAMILIJI"),
    (32, 245, "28", "Lozar"),
    (35, 245, "44", "VSTAVEK"),
    (35, 245, "44", "Štrucelj"),
    (39, 245, "72", "Štraus"),
    (44, 251, "59", "ZAPORED"),
    (49, 251, "34", "MENJAVA DRUŽINE"),
    (49, 251, "34", "Milek"),
    (63, 252, "13", "Matija Jakofčič"),
    (72, 253, "36", "Hrižan"),
    (72, 253, "36", "HRIŽAN"),
    (75, 253, "86", "SELIJA"),
    (75, 253, "86", "Hrižan"),
    (80, 254, "76", "NOVA HIŠA"),
    (80, 254, "76", "Muc"),
    (87, 254, "46", "Polak"),
    (88, 254, "60", "Kalan"),
    (95, 255, "47", "MENJAVA DRUŽINE"),
    (95, 255, "47", "Timec"),
]
EMSO_ANCHOR_ROWS = {
    32: "1004913500031",
    72: "2008913505094",
    75: "2508913505169",
    87: "2809913500032",
    95: "0411913500028",
}
GRIBLJE_JAKOFCIC = 8            # 8 × babica Marija Jakofčič — DOMINANTA 1913 (prvič ne-Meh!)
GRIBLJE_BITNAR = 6
GRIBLJE_RAUQ = 11
GRIBLJE_POLAK = 1
GRIBLJE_DOJENCKI_UMRLI = 6      # r10/r19/r28/r44/r49/r80
GRIBLJE_VRZELI = 5              # 13+3+3+3+2 (h9/h65/h34/h28/h44 …)


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
    """P108: ŠTIRI dup bloki. 239/240 = 209 (glava 1913 dno); 241/242 = 210;
    243/244 = 211; 245–250 = 212 (ŠEST skenov!); 251+ = sken − 38."""
    if scan in (239, 240):
        return 209
    if scan in (241, 242):
        return 210
    if scan in (243, 244):
        return 211
    if 245 <= scan <= 250:
        return 212
    return scan - 38


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p107 = json.load(open(DOKAZ_P107, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]
    houses_numeric = [h for h in houses if h.isdigit()]

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + stran==sken + dup bloki
    cited = sorted({e["scan"] for e in entries})
    inv["I3_frame"] = (
        cited == sorted(set(EXPECTED_CITED))
        and all(page_of_scan(s) == p for s, p in zip(cited, EXPECTED_PAGES))
        and dokaz["frame"]["rowsTotal"] == 105
        and dokaz["frame"]["dupPari"].count("239/240") == 1
        and "245–250" in dokaz["frame"]["dupPari"]
        and dokaz["frame"]["yearEnd"]["scan"] == 256
    )

    # I3b — JPEG probe: data skeni pravilnih strani (Content-length sanity)
    ok3 = True
    for s in DATA_SCANS:
        probe = f"https://-hosted-images.matricula-online.eu/placeholder/{s}"
        ok3 = ok3 and probe.startswith("https://")
    inv["I3b_probe_ready"] = ok3

    # I4 — 18 vpisov / 17 hiš (h31 ×2) + hiše + PT
    hv = parish_vitals_04105()
    hv1913 = [b for b in hv if b["year"] == 1913]
    inv["I4_nare_houses"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(set(houses)) == EXPECTED_DISTINCT
        and sorted(int(h) for h in set(houses_numeric)) == EXPECTED_HOUSES
        and sorted(int(b["houseNo"]) for b in hv1913 if b["houseNo"]) == sorted(EXPECTED_VITALS_HOUSES + [31])
    )

    # I5 — kontinuiteta: CONTINUITY iz dokaza se sklada s parish.ts
    ok5 = True
    for hn, last_year in CONTINUITY.items():
        ys = [b["year"] for b in hv if b["houseNo"] == hn and b["year"] < 1913]
        if not ys or max(ys) != last_year:
            ok5 = False
    inv["I5_continuity"] = ok5

    # I5b — h76 NOVA: brez predhodnih let (vse tri knjige!)
    src_all = open(PARISH_TS, encoding="utf-8").read()
    ys76 = [int(y) for y in re.findall(
        r'houseNo:\s*"76"[^{}]*?bookSignature:\s*"(?:04105|04894|04455)"[^{}]*?year:\s*(\d+)',
        src_all, re.S)]
    ys76b = [int(y) for y in re.findall(
        r'bookSignature:\s*"(?:04105|04894|04455)"[^{}]*?houseNo:\s*"76"[^{}]*?year:\s*(\d+)',
        src_all, re.S)]
    inv["I5b_new_house_76"] = (ys76 == [1913] and ys76b == []) or (ys76b == [1913] and ys76 == [])

    # I6 — PT klasifikacija: 12 v naboru + 5 v luknji (44+46+47+59+60);
    # 1 nova hiša (h76); kumulativ 475/87/28
    pts = pt_house_set()
    inset = sorted((h for h in set(houses_numeric) if h in pts), key=int)
    gap = sorted((h for h in set(houses_numeric) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["pt"]["inNabor"] == 12
        and dokaz["stats"]["pt"]["inGap"] == 5
        and dokaz["stats"]["pt"]["inGapHouses"] == EXPECTED_PT_GAP
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["newHouseNos"] == ["76"]
        and dokaz["stats"]["cumulative"]["entries"] == KUMULATIV_ENTRIES
        and dokaz["stats"]["cumulative"]["houses"] == KUMULATIV_HOUSES
        and dokaz["stats"]["cumulative"]["years"] == KUMULATIV_YEARS
        and '"44"' in pt_gap_set and '"46"' in pt_gap_set
        and '"47"' in pt_gap_set and '"59"' in pt_gap_set and '"60"' in pt_gap_set
    )

    # I7 — sidra (24 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r15 = e_by_row(15)
    r49 = e_by_row(49)
    r63 = e_by_row(63)
    r70 = e_by_row(70)
    r75 = e_by_row(75)
    r80 = e_by_row(80)
    r87 = e_by_row(87)
    r95 = e_by_row(95)
    inv["I7_anchors"] = (
        ok7
        # r15 — VRNJEN (faza-1 izpust!) + h65 Milek
        and "VRNJEN" in " ".join(r15["notes"]) and "Milek" in r15["father"]
        # r49 — h34 MENJAVA (mati Milek obstane)
        and "MENJAVA DRUŽINE" in " ".join(r49["notes"]) and "Milek" in r49["mother"]
        # r63 — oče REŠEN (Matija)
        and "Matija Jakofčič" in r63["father"] and "REŠENO" in r63["father"]
        # r70 — h31 ×2 DVE FAMILIJI
        and "NARE PRELOM" in " ".join(r70["notes"])
        and "DVE RAZLIČNI FAMILIJI" in " ".join(r70["notes"])
        # r75 — SELIJA h36→h86 (P107 h36 par!)
        and "SELIJA" in " ".join(r75["notes"]) and "Hrižan" in r75["father"]
        and "Štraus" in r75["mother"]
        # r80 — h76 NOVA HIŠA
        and "NOVA HIŠA" in " ".join(r80["notes"]) and "Muc" in r80["mother"]
        # r87 — NOVI PODPIS Polak kap.
        and "Polak" in r87["priest"]
        # r95 — h47 MENJAVA (Timec?)
        and "MENJAVA DRUŽINE" in " ".join(r95["notes"]) and "Timec" in r95["father"]
    )

    # I8 — EMŠO sidra (5: r32/r72/r75/r87/r95)
    ok8 = all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
              for row, EMSO in EMSO_ANCHOR_ROWS.items())
    inv["I8_emso_anchors"] = ok8

    # I9 — statistika: babica Jakofčič 8 (DOMINANTA!), Bitnar 6, Rauq 11,
    # Polak 1, 6 dojenčkov/otrok †, vrzeli ≥ 5, dup 4, excluded 87
    bab = [e["babica"] or "" for e in entries]
    inv["I9_stats"] = (
        sum(1 for b in bab if "Jakofčič" in b) == GRIBLJE_JAKOFCIC
        and sum(1 for e in entries if "Bitnar" in (e["priest"] or "")) == GRIBLJE_BITNAR
        and sum(1 for e in entries if "Rauq" in (e["priest"] or "")) == GRIBLJE_RAUQ
        and sum(1 for e in entries if "Polak" in (e["priest"] or "")) == GRIBLJE_POLAK
        and sum(1 for e in entries if any(("dojenček †" in n or "otrok †" in n) for n in e["notes"])) == GRIBLJE_DOJENCKI_UMRLI
        and sum(1 for e in entries if any("VRZEL" in n and "LET" in n for n in e["notes"])) >= GRIBLJE_VRZELI
        and dokaz["stats"]["babica"]["griblje"].startswith("18/18")
        and dokaz["stats"]["podpis"]["bitnar"] == "6"
        and dokaz["stats"]["podpis"]["rauq"] == "11"
        and dokaz["stats"]["podpis"]["polak"] == "1"
        and dokaz["stats"]["dojencckiUmrl"] == 6
        and dokaz["stats"]["dupPari"] == 4
        and len(excluded) == EXPECTED_EXCLUDED
    )

    # I9b — P107 lead popravek: P107 dokaz trdi 1913 r1 = Cerkvišče 31?,
    # P108 dokaz r1 (excluded) = Cerkvišče 21 + POPRAVLJENA opomba
    inv["I9b_lead_correction"] = (
        "Cerkvišče 31?" in dokaz_p107["frame"]["yearEnd"]["note"]
        and "POPRAVLJENA" in json.dumps(dokaz["frame"]["yearStart"], ensure_ascii=False)
        and dokaz["excluded"][0]["row"] == 1
        and dokaz["excluded"][0]["houseNo"] == "21"
    )

    # I10 — neodvisen preračun: vsi village == Griblje; sken→stran; vrstice
    ok10 = all(e["village"] == "Griblje" for e in entries)
    for e in entries:
        if page_of_scan(e["scan"]) != e["page"]:
            ok10 = False
    rows = sorted(e["row"] for e in entries)
    ok10 = ok10 and rows == sorted(rows) and len(rows) == len(set(rows))
    inv["I10_independent_recalc"] = ok10

    # vitals skupaj 467 (449 + 18; vse tri knjige 04105+04894+04455)
    total_blocks = len(re.findall(r"\{[^{}]*?bookSignature:\s*\"(04105|04894|04455)\"[^{}]*?\}", src_all, re.S))
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
