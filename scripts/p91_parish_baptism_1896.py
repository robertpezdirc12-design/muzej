#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P91 — župnija Podzemelj: krstna knjiga 04105, polno leto 1896 (issue #18).

Razširitev vzorca P79 (1886) → … → P89 (1894) → P90 (1895) na leto 1896:
okvir skeni 85–92 == strani 83–90 (glava »1896« na str. 83 po 1895 row 73;
leto 1896 ima 94 zveznih vrstic — NAJDALJŠE doslej; prelom 1897 na str. 91 =
sken 93 po row 94 — oznake ponastavljene, novela P83 potrjena 9. leto).
NOVELA P89 POTRJENA 3. LETO: stran == sken − 2 za celo leto (sken 73
podvojen, NI citiran). LE OKVIR — prejšnja leta imajo svoje skripte p82–p90.
14 vpisov / 14 hiš — NARE (3. leto po P87/P89); 3 NOVE hiše (9, 14, 45);
h45 = NOVA LUKNJA ŠTEVILKA (16. dokazana v 41–60 — prva nova od P88);
h41 4. dokaz + h46 3. dokaz + h53 3. dokaz. NOVELA babica potrjena 2. leto
(14/14 PRAZNO). NOV duhovnik Fr. Šuvar? dominanten (9/14). Statusi: ½ × 12 +
bajtar × 2 — prvo leto brez ¼. Sidra: h1 Željko × Kure 3. VPIS ISTA zveza
(1888+1892+1896; botra ISTI priimki kot starši vse 3×), h63 oče ISTI 5×
(1887–1896), h30 Šegina × Mihelt ISTA zveza 2. leto, h41 Hušič × Jakobič
4. VPIS ISTA zveze, h15 Jaklič × Brinec 3. VPIS, h36 Križan × Straucelj
2. VPIS, h53 Pendirec? × Hrižan 3. VPIS variante, h31 MENJAVA (Fapič →
Pendirec), h25 KLEPEC NAZAJ, h46 mati menjana/varianta, h26 Jakobič ×
Stubljar na DRUGI hiši (75 → 26 — selitev ali napaka [~]).

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
DOKAZ = "research/issue17/parish-baptism-1896.json"
DOKAZ_P77 = "research/issue17/parish-sample-transcription.json"
DOKAZ_P82 = "research/issue17/parish-baptism-1887.json"
DOKAZ_P83 = "research/issue17/parish-baptism-1888.json"
DOKAZ_P84 = "research/issue17/parish-baptism-1889.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
DOKAZ_P87 = "research/issue17/parish-baptism-1892.json"
DOKAZ_P88 = "research/issue17/parish-baptism-1893.json"
DOKAZ_P89 = "research/issue17/parish-baptism-1894.json"
DOKAZ_P90 = "research/issue17/parish-baptism-1895.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (85, 92)          # skeni 85–92 == strani 83–90 (okvir leta 1896)
FRAME_PAGES = (83, 90)
BREAK_1897 = {"scan": 93, "page": 91}
EXPECTED_ENTRIES = 14
EXPECTED_DISTINCT = 14          # 14 vpisov / 14 hiš — NARE (3. leto)
EXPECTED_CITED = [85, 86, 87, 88, 89, 90, 91, 92]  # sken 73 podvojen ni citiran
EXPECTED_PT_IN_SET = ["1", "9", "14", "15", "25", "26", "30", "31", "36", "63"]
EXPECTED_PT_GAP = ["41", "45", "46", "53"]
PT_GAP_NEW = ["45"]             # h45 = NOVA luknja številka (16. dokazana)
EXPECTED_NEW_HOUSES = ["9", "14", "45"]
EXPECTED_REPEATS = 11           # 14 − 3 nove
EXPECTED_HOUSES_VITALS = 14
EXPECTED_VITALS_TOTAL = 490     # HOUSE_VITALS 179 + 14 (p80 I7 pin); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900); P98: + 12 (1903); P99: + 19 (1904); P101: + 18 (1906); P102: + 15 (1907); P103: + 18 (1908); P104: + 18 (1909); P105: + 20 (1910)
EV_ONLY_TOTAL = 8               # P84: 2 + P85: 3 + P86: 1 + P102: r4 (1) + P103: r84 (1) (P77–P83, P87–P91: 0)
EV_ONLY_HOUSE_STRINGS = {"65 [~]"}  # P85 — edina imenovana EV-only hiša (None × 4)
# sidra/pins P91:
H9_ROW = {"row": 2, "scan": 85, "fatherPin": "Jakobič"}
H14_ROW = {"row": 5, "scan": 85, "fatherPin": "Brinec"}
H31_ROW = {"row": 13, "scan": 86, "fatherPin": "Pendirec"}
H36_ROW = {"row": 18, "scan": 86, "fatherPin": "Križan"}
H1_ROW = {"row": 24, "scan": 87, "fatherPin": "Željko"}
H25_ROW = {"row": 25, "scan": 87, "fatherPin": "Klepec"}
H46_ROW = {"row": 31, "scan": 87, "fatherPin": "Brodarič"}
H26_ROW = {"row": 45, "scan": 88, "fatherPin": "Jakobič"}
H41_ROW = {"row": 46, "scan": 88, "fatherPin": "Hušič"}
H15_ROW = {"row": 50, "scan": 89, "fatherPin": "Jaklič"}
H63_ROW = {"row": 53, "scan": 89, "fatherPin": "Hrižan"}
H45_ROW = {"row": 70, "scan": 90, "fatherPin": "Straus"}
H53_ROW = {"row": 81, "scan": 91, "fatherPin": "Pendirec"}
H30_ROW = {"row": 92, "scan": 92, "fatherPin": "Šegina"}


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
        except Exception:  # noqa: BLE001
            pass
    return sorted(set(urls))


def probe_jpeg(url):
    st, b = http_get(url, UA)
    return {"http": st, "jpeg": bool(b) and b[:2] == b"\xff\xd8", "bytes": len(b) if b else 0}


def pt_house_set():
    d = json.load(open(PT_CHAIN, encoding="utf-8"))
    return {str(r["no"]).strip() for r in d["chain"] if r.get("kind") == "hiša"}


def parish_vitals(signature, year=None):
    src = open(PARISH_TS, encoding="utf-8").read()
    out = []
    pat = r"\{[^{}]*?bookSignature:\s*\"" + signature + r"\"[^{}]*?\}"
    for m in re.finditer(pat, src, re.S):
        block = m.group(0)
        g = lambda k: (re.search(rf'{k}:\s*"([^"]*)"', block) or re.search(rf"{k}:\s*(\d+)", block))  # noqa: E731
        hn = g("houseNo")
        yr = re.search(r"year:\s*(\d+)", block)
        sc = re.search(r"scan:\s*(\d+)", block)
        pg = re.search(r"page:\s*(\d+)", block)
        out.append({
            "houseNo": hn.group(1) if hn else None,
            "year": int(yr.group(1)) if yr else None,
            "scan": int(sc.group(1)) if sc else None,
            "page": int(pg.group(1)) if pg else None,
            "bookSignature": signature,
        })
    if year is not None:
        out = [v for v in out if v["year"] == year]
    return out


def page_of_scan(scan):
    """NOVELA P89 potrjena 3. leto: stran == sken − 2 za celo leto 1896."""
    return scan - 2


def verify():
    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    entries = dokaz["entries"]
    inv = {}

    # I1 — knjiga dostopna + inventar 326
    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    # I3 — citirani skeni ⊆ okvir 85–92 + JPEG probe; sken 73 NI citiran
    cited = sorted({e["scan"] for e in entries})
    inv["I3_cited_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and cited == EXPECTED_CITED and 73 not in cited
    probes = {s: probe_jpeg(urls[s - 1]) for s in cited} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())

    # I4 — okvir: vsi vpisi 1896, stran == sken − 2 (novela P89, 3. leto);
    # prelom 1897 na str. 91 (sken 93); rowsTotal 94 (NAJDALJŠE doslej)
    rows = [e["row"] for e in entries]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1896 for e in entries)
        and all(e["page"] == page_of_scan(e["scan"]) for e in entries)
        and all(FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1] for e in entries)
        and all(FRAME_PAGES[0] <= e["page"] <= FRAME_PAGES[1] for e in entries)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and dokaz["frame"]["break1897"]["scan"] == BREAK_1897["scan"]
        and dokaz["frame"]["break1897"]["page"] == BREAK_1897["page"]
        and dokaz["frame"]["rowsTotal"] == 94
        and dokaz["frame"]["duplicateScan"]["scan"] == 73
        and "NE citiran" in dokaz["frame"]["duplicateScan"]["note"]
        and "94" in dokaz["frame"]["rowsNote"]
    )

    # I5 — števec: 14 vpisov / 14 hiš (NARE — brez ponovitev znotraj leta) /
    # 0 neberljivih; NOVELA babica 2. leto: vseh 14 PRAZNO; r5 brez botre +
    # brez podpisa; r70 botra pod trakom
    houses = {e["houseNo"] for e in entries}
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"] == "Griblje" for e in entries)
        and len(houses) == EXPECTED_DISTINCT
        and len(rows) == len(set(rows))
        and dokaz["stats"]["housesIllegible"] == 0
        and all(e["babica"] and "prazen" in e["babica"] for e in entries)  # NOVELA babica 2. leto
        and dokaz["stats"]["babica"] == 0
        and next(e for e in entries if e["row"] == 5)["botra"].startswith("—")
        and "PRAZEN" in next(e for e in entries if e["row"] == 5)["priest"]
        and "TRAKOM" in next(e for e in entries if e["row"] == 70)["botra"]
    )

    # I6 — PT klasifikacija: 10 v naboru + 4 v luknjah/izven; NOVA LUKNJA
    # ŠTEVILKA 45 (16. dokazana); 3 NOVE hiše (9, 14, 45)
    pts = pt_house_set()
    inset = sorted((h for h in houses if h in pts), key=int)
    gap = sorted((h for h in houses if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGapNew"] == PT_GAP_NEW
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and "16" in dokaz["stats"]["ptGapNote"]
        and "45" in dokaz["stats"]["ptGapNote"]
        # atlas.ts PT_GAP_KNOWN mora vsebovati 45 (runtime projekcija)
        and '"45"' in re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", open(ATLAS_TS, encoding="utf-8").read()).group(0)
    )

    # I7 — sidra (14 vpisov — očetovski pini + kontinuitetne oznake)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    h9 = e_by_row(H9_ROW["row"])
    h14 = e_by_row(H14_ROW["row"])
    h31 = e_by_row(H31_ROW["row"])
    h36 = e_by_row(H36_ROW["row"])
    h1 = e_by_row(H1_ROW["row"])
    h25 = e_by_row(H25_ROW["row"])
    h46 = e_by_row(H46_ROW["row"])
    h26 = e_by_row(H26_ROW["row"])
    h41 = e_by_row(H41_ROW["row"])
    h15 = e_by_row(H15_ROW["row"])
    h63 = e_by_row(H63_ROW["row"])
    h45 = e_by_row(H45_ROW["row"])
    h53 = e_by_row(H53_ROW["row"])
    h30 = e_by_row(H30_ROW["row"])
    inv["I7_anchors"] = (
        h9["houseNo"] == "9" and H9_ROW["fatherPin"] in h9["father"]
        and "NOVA HIŠA" in json.dumps(h9["notes"], ensure_ascii=False)
        and h14["houseNo"] == "14" and H14_ROW["fatherPin"] in h14["father"]
        and "NOVA HIŠA" in json.dumps(h14["notes"], ensure_ascii=False)
        and h31["houseNo"] == "31" and H31_ROW["fatherPin"] in h31["father"]
        and "MENJAVA GOSPODINJSTVA" in json.dumps(h31["notes"], ensure_ascii=False)
        and h36["houseNo"] == "36" and H36_ROW["fatherPin"] in h36["father"]
        and "ISTA ZVEZA" in json.dumps(h36["notes"], ensure_ascii=False)
        and h1["houseNo"] == "1" and H1_ROW["fatherPin"] in h1["father"]
        and "3. VPIS ISTA ZVEZA" in json.dumps(h1["notes"], ensure_ascii=False)
        and h25["houseNo"] == "25" and H25_ROW["fatherPin"] in h25["father"]
        and "KLEPEC NAZAJ" in json.dumps(h25["notes"], ensure_ascii=False)
        and h46["houseNo"] == "46" and H46_ROW["fatherPin"] in h46["father"]
        and "3. DOKAZ LUKNJE" in json.dumps(h46["notes"], ensure_ascii=False)
        and h26["houseNo"] == "26" and H26_ROW["fatherPin"] in h26["father"]
        and "DRUGI hiši" in json.dumps(h26["notes"], ensure_ascii=False)
        and h41["houseNo"] == "41" and H41_ROW["fatherPin"] in h41["father"]
        and "4. VPIS ISTA ZVEZA" in json.dumps(h41["notes"], ensure_ascii=False)
        and h15["houseNo"] == "15" and H15_ROW["fatherPin"] in h15["father"]
        and "3. VPIS ISTA ZVEZA" in json.dumps(h15["notes"], ensure_ascii=False)
        and h63["houseNo"] == "63" and H63_ROW["fatherPin"] in h63["father"]
        and "OČE ISTI VSEH 5×" in json.dumps(h63["notes"], ensure_ascii=False)
        and h45["houseNo"] == "45" and H45_ROW["fatherPin"] in h45["father"]
        and "NOVA LUKNJA ŠTEVILKA" in json.dumps(h45["notes"], ensure_ascii=False)
        and h53["houseNo"] == "53" and H53_ROW["fatherPin"] in h53["father"]
        and "3. DOKAZ LUKNJE" in json.dumps(h53["notes"], ensure_ascii=False)
        and h30["houseNo"] == "30" and H30_ROW["fatherPin"] in h30["father"]
        and "ISTA ZVEZA 2. leto" in json.dumps(h30["notes"], ensure_ascii=False)
    )

    # I8 — čez-letne kontinuitete prek dokazov:
    # h1 (P83 Zeljth + P87 Željko × Kure → P91 ISTA zveza 3. VPIS)
    # h30 (P85 Milek ×2 + P86 Milek + P88 Jakljevič + P90 Šegina × Mihelt → P91 ISTA)
    # h36 (P77 Križan ×2 + P89 Križan × Straucelj → P91 ISTA)
    # h41 (P85 Hrušič? ×2 + P88 Hušič × Jakobič → P91 ISTA 4. VPIS)
    # h46 (P88 Brodarič × Klobučar + P90 Brodarič × Klobučan? → P91 Brodarič 3. VPIS)
    # h53 (P86 Pozdirec × Križan + P89 Pegdirec × Hrižan → P91 Pendirec × Hrižan)
    # h63 (P82 Prižan + P84 Hrigian + P85 Križan + P87 Hrižan → P91 oče ISTI 5×)
    # h15 (P82 Jakšič? + P88 Jaklič × Brinec → P91 3. VPIS)
    # h31 (P89 Fapič × Straus → P91 Pendirec = MENJAVA)
    # h25 (P88 Hrižan × Požek; poroka 04455 1886 Klepec GRIBLJE 25 → P91 Klepec NAZAJ)
    # h26 (P87 h75 Jakobič × Stubljar + P89 h75 ISTA → P91 ISTI priimki na h26)
    # h9/h14/h45 NOVE (brez priora)
    p77 = json.load(open(DOKAZ_P77, encoding="utf-8"))
    p82 = json.load(open(DOKAZ_P82, encoding="utf-8"))
    p83 = json.load(open(DOKAZ_P83, encoding="utf-8"))
    p84 = json.load(open(DOKAZ_P84, encoding="utf-8"))
    p85 = json.load(open(DOKAZ_P85, encoding="utf-8"))
    p86 = json.load(open(DOKAZ_P86, encoding="utf-8"))
    p87 = json.load(open(DOKAZ_P87, encoding="utf-8"))
    p88 = json.load(open(DOKAZ_P88, encoding="utf-8"))
    p89 = json.load(open(DOKAZ_P89, encoding="utf-8"))
    p90 = json.load(open(DOKAZ_P90, encoding="utf-8"))

    def hs(d, h):
        return [e for e in d["entries"] if e.get("houseNo") == h]

    p83_h1 = hs(p83, "1")
    p87_h1 = hs(p87, "1")
    p85_h30 = hs(p85, "30")
    p86_h30 = hs(p86, "30")
    p88_h30 = hs(p88, "30")
    p90_h30 = hs(p90, "30")
    p77_h36 = hs(p77, "36")
    p89_h36 = hs(p89, "36")
    p85_h41 = hs(p85, "41")
    p88_h41 = hs(p88, "41")
    p88_h46 = hs(p88, "46")
    p90_h46 = hs(p90, "46")
    p86_h53 = hs(p86, "53")
    p89_h53 = hs(p89, "53")
    p82_h63 = hs(p82, "63")
    p84_h63 = hs(p84, "63")
    p85_h63 = hs(p85, "63")
    p87_h63 = hs(p87, "63")
    p82_h15 = hs(p82, "15")
    p88_h15 = hs(p88, "15")
    p89_h31 = hs(p89, "31")
    p88_h25 = hs(p88, "25")
    p87_h75 = hs(p87, "75")
    p89_h75 = hs(p89, "75")
    inv["I8_crossyear_continuity"] = (
        # h1 — 3. VPIS ISTA zveza (P83 + P87)
        len(p83_h1) == 1 and "Zeljth" in p83_h1[0]["father"]
        and len(p87_h1) == 1 and "Željko" in p87_h1[0]["father"]
        and "Kure" in p87_h1[0]["mother"]
        and "Željko" in h1["father"] and "Kure" in h1["mother"]
        # h30 — ISTA zveza 2. leto (P85/P86 Milek + P88 Jakljevič + P90 Šegina)
        and len(p85_h30) == 2 and all("Milek" in e["father"] for e in p85_h30)
        and len(p86_h30) == 1 and "Milek" in p86_h30[0]["father"]
        and len(p88_h30) == 1 and "Jakljevič" in p88_h30[0]["father"]
        and len(p90_h30) == 1 and "Šegina" in p90_h30[0]["father"]
        and "Mihelt" in p90_h30[0]["mother"]
        and "Šegina" in h30["father"] and "Mihelt" in h30["mother"]
        # h36 — 2. VPIS Križan zveze (P77 ×2 + P89)
        and len(p77_h36) == 2 and any("Križan" in e["father"] for e in p77_h36)
        and len(p89_h36) == 1 and "Križan" in p89_h36[0]["father"]
        and "Straucelj" in p89_h36[0]["mother"]
        and "Križan" in h36["father"] and "Straucelj" in h36["mother"]
        # h41 — 4. VPIS ISTA zveze (P85 ×2 + P88)
        and len(p85_h41) == 2 and any("Hrušič" in e["father"] or "Hušič" in e["father"] for e in p85_h41)
        and len(p88_h41) == 1 and "Hušič" in p88_h41[0]["father"]
        and "Jakobič" in p88_h41[0]["mother"]
        and "Hušič" in h41["father"] and "Jakobič" in h41["mother"]
        # h46 — 3. VPIS Brodarič; mati menjana/varianta
        and len(p88_h46) == 1 and "Brodarič" in p88_h46[0]["father"]
        and "Klobučar" in p88_h46[0]["mother"]
        and len(p90_h46) == 1 and "Brodarič" in p90_h46[0]["father"]
        and "Brodarič" in h46["father"] and "Kramarič" in h46["mother"]
        # h53 — 3. VPIS variante (P86 + P89)
        and len(p86_h53) == 1 and "Pozdirec" in p86_h53[0]["father"]
        and len(p89_h53) == 1 and "Pegdirec" in p89_h53[0]["father"]
        and "Pendirec" in h53["father"] and "Hrižan" in h53["mother"]
        # h63 — oče ISTI 5× (P82/P84/P85/P87)
        and len(p82_h63) == 1 and ("Prižan" in p82_h63[0]["father"] or "Križan" in p82_h63[0]["father"])
        and len(p84_h63) == 1 and ("Hrigian" in p84_h63[0]["father"] or "Hrižan" in p84_h63[0]["father"])
        and len(p85_h63) == 1 and "Križan" in p85_h63[0]["father"]
        and len(p87_h63) == 1 and "Hrižan" in p87_h63[0]["father"]
        and "Hrižan" in h63["father"]
        # h15 — 3. VPIS (P82 + P88)
        and len(p82_h15) == 1 and "Brinec" in p82_h15[0]["mother"]
        and len(p88_h15) == 1 and "Jaklič" in p88_h15[0]["father"]
        and "Brinec" in p88_h15[0]["mother"]
        and "Jaklič" in h15["father"] and "Brinec" in h15["mother"]
        # h31 — MENJAVA (P89 Fapič × Straus → P91 Pendirec)
        and len(p89_h31) == 1 and "Fapič" in p89_h31[0]["father"]
        and "Straus" in p89_h31[0]["mother"]
        and "Pendirec" in h31["father"] and "Žugelj" in h31["mother"]
        # h25 — KLEPEC NAZAJ (P88 Hrižan × Požek menjava → P91 Klepec)
        and len(p88_h25) == 1 and "Hrižan" in p88_h25[0]["father"]
        and "Požek" in p88_h25[0]["mother"]
        and "Klepec" in h25["father"]
        # h26 — ISTI priimki kot h75 zveza (P87 + P89 na h75; Kurrent variante)
        and len(p87_h75) == 1 and "Jakobčič" in p87_h75[0]["father"]
        and "Sušljar" in p87_h75[0]["mother"]
        and len(p89_h75) == 1 and "Jakobič" in p89_h75[0]["father"]
        and "Stubljar" in p89_h75[0]["mother"]
        and "Jakobič" in h26["father"] and "Stubljar" in h26["mother"]
    )

    # I9 — runtime projekcija: HOUSE_VITALS 1896 == 14 zasidranih
    # (sk. 85–92, stran == sken − 2); skupaj 193; brez »Hraus« v aktivnih whatSi
    vitals_1896 = parish_vitals(BOOK_SIGNATURE, 1896)
    hv_houses = sorted({v["houseNo"] for v in vitals_1896}, key=int)
    src = open(PARISH_TS, encoding="utf-8").read()
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    active_hraus = [
        w for w in re.findall(r"whatSi:\s*\"([^\"]+)\"", src)
        if "Hraus" in w and "re-read" not in w and "prej" not in w
    ]
    inv["I9_runtime_projection"] = (
        len(vitals_1896) == EXPECTED_HOUSES_VITALS
        and hv_houses == sorted(houses, key=int)
        and all(v["scan"] and 85 <= v["scan"] <= 92 and v["page"] == page_of_scan(v["scan"])
                for v in vitals_1896)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
        and not active_hraus
    )

    # I10 — statistika dokaza == neodvisen preracun: 11 ponovitev + 3 nove
    # (9/14/45); kumulativ 193 + 6 EV-only == 199; hiše vitals 70 (67 + 3) —
    # dokaz 71 = 70 + EV-only »65 [~]«
    # klasifikacija v vesolju lastnega leta — poznejši bloki (04105 > 1896)
    # ne smejo spreminjati zgodovinske klasifikacije novih/ponovljenih hiš (h45: 1897 ponovitev)
    vitals_pre97 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913))
    ]
    repeat_houses = [h for h in houses if any(
        v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1896
        or v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE
        for v in vitals_pre97
    )]
    new_houses = sorted(houses - set(repeat_houses), key=int)
    n_entries_total = len(vitals_all)
    n_houses_total = len({v["houseNo"] for v in vitals_all})
    ev_only_houses = set()
    for fn in (DOKAZ_P84, DOKAZ_P85, DOKAZ_P86):
        d = json.load(open(fn, encoding="utf-8"))
        vit_h = {v["houseNo"] for v in vitals_all}
        for e in d["entries"]:
            hn = e.get("houseNo")
            if hn is not None and hn not in vit_h:
                ev_only_houses.add(hn)
    cumulative = dokaz["stats"]["cumulative"]
    # neodvisen preracun duhovnikov: 9 + 4 + 1 prazen == 14
    n_suvar = sum(1 for e in entries if "Šuvar" in e["priest"])
    n_rauq = sum(1 for e in entries if "Rauq" in e["priest"])
    n_praz = sum(1 for e in entries if "PRAZEN" in e["priest"])
    inv["I10_stats_independent"] = (
        len(repeat_houses) == EXPECTED_REPEATS
        and dokaz["stats"].get("repeatHouses", EXPECTED_REPEATS) == EXPECTED_REPEATS
        and new_houses == dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and len(dokaz["stats"]["intraYearRepeats"]) == 0  # NARE
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 498  # kumulativno po P110 (490 + 8)
        and n_houses_total == 85  # P98: 80 vitals; P99: + 3 (h6, h42, h50); P100: + 0 (1905 brez novih); P101: + 1 (h4); P107: + 1 (h86)
        and ev_only_houses == EV_ONLY_HOUSE_STRINGS
        and cumulative["entries"] == 199  # P91 JSON — lastni kumulativ (P92 vrne 217/74 v p92 skripti)
        and cumulative["houses"] == 71  # 70 vitals + 1 EV-only »65 [~]«
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and len(dokaz["entries"]) == 14
        and (n_suvar, n_rauq, n_praz) == (9, 4, 1)
    )

    ok = all(inv.values())
    print("P91 — krstna knjiga 04105, polno leto 1896 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {cited} (sken 73 = podvojen str. 71 — ni citiran)")
    print(f"vpisi {len(entries)} / hiše {len(houses)} (NARE);"
          f" PT {len(inset)}/{len(gap)} (45 NOVA luknja); nove hiše {sorted(new_houses)};"
          f" vitals 1896 = {len(vitals_1896)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vitals = {n_houses_total}; kumulativ {n_entries_total + EV_ONLY_TOTAL}"
          f" vpisov / {n_houses_total + len(ev_only_houses)} hiš")
    return 0 if ok else 1


def e_by_row(entries, row):
    return next(e for e in entries if e["row"] == row)


if __name__ == "__main__":
    sys.exit(verify())
