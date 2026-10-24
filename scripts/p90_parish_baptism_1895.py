#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P90 — župnija Podzemelj: krstna knjiga 04105, polno leto 1895 (issue #18).

Razširitev vzorca P79 (1886) → P82 (1887) → … → P88 (1893) → P89 (1894) na
leto 1895: okvir skeni 78–84 == strani 76–82 (glava »1895.~« na str. 76 po
1894 row 90; leto 1895 ima 73 zveznih vrstic; prelom 1896 na str. 83 = sken
85 po row 73 — oznake ponastavljene, novela P83 potrjena 8. leto). NOVELA
P89 POTRJENA 2. LETO: stran == sken − 2 za celo leto (sken 73 podvojen, NI
citiran). LE OKVIR — prejšnja leta imajo svoje skripte p82–p89. 15 vpisov /
14 hiš (h24 DVOM 2×: r22 Brime + r48 Toško?/Simec — prva ponovitev hiše
znotraj leta po P87 NARE); 3 NOVE hiše (20, 37, 87) po P89 »0 novih«.
NOVELI VZORCA: babica stolpec na VSEH 15 vrstic PRAZEN (1894: Trotter 11×) —
Trotter žene pa 7× kot BOTRA (vloga prestopila); 4× PRAZNA botra (r53/r54/
r55/r66, september–december). TRIJE duhovniki: Jelenuš 8× + Rauq 3× + NOV
Franc Klunng 2× (od septembra). MATI PODCELICA (X × Y) prvič eksplicitno
dokumentirana — semantika ODPRTA. Sidra: h58 4. VPIS + MATI MENJANA (Dragoš
→ Kambic?), h32 + h72 5. VPIS — NAJDALJŠI zvezi vzorca (1889–1895), h69 oče
ISTI 5×, h30 3. DRUŽINA (2× menjava), h29 MENJAVA (»hiša kuge« → Kuhar? ×
Klobučar), h91 oče MENJAN (Novak → Muc), h46/h24/h12/h65 kontinuitete.

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
DOKAZ = "research/issue17/parish-baptism-1895.json"
DOKAZ_P77 = "research/issue17/parish-sample-transcription.json"
DOKAZ_P82 = "research/issue17/parish-baptism-1887.json"
DOKAZ_P83 = "research/issue17/parish-baptism-1888.json"
DOKAZ_P84 = "research/issue17/parish-baptism-1889.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
DOKAZ_P87 = "research/issue17/parish-baptism-1892.json"
DOKAZ_P88 = "research/issue17/parish-baptism-1893.json"
DOKAZ_P89 = "research/issue17/parish-baptism-1894.json"
PARISH_TS = "src/data/atlas/parish.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (78, 84)          # skeni 78–84 == strani 76–82 (okvir leta 1895)
FRAME_PAGES = (76, 82)
BREAK_1896 = {"scan": 85, "page": 83}
EXPECTED_ENTRIES = 15
EXPECTED_DISTINCT = 14          # 15 vpisov / 14 hiš (h24 2× — DVOM)
EXPECTED_CITED = [79, 80, 82, 83, 84]  # sken 78/81 brez Gribljev; 73 podvojen ni citiran
EXPECTED_PT_IN_SET = {"12", "20", "24", "29", "30", "32", "37", "65", "69", "72", "87", "91"}
EXPECTED_PT_GAP = {"46", "58"}   # obe v PT_GAP_KNOWN: 46 = 2. dokaz (P88+P90); 58 = 4. vpis (P84/P85/P87)
PT_GAP_NEW = []                 # luknja 41–60: h46 ponovitev — brez novih števil
EXPECTED_NEW_HOUSES = ["20", "37", "87"]
EXPECTED_REPEATS = 11           # 14 − 3 nove
EXPECTED_HOUSES_VITALS = 15     # 15 vpisov (h24 2 bloka)
EXPECTED_VITALS_TOTAL = 659  # POSODABLJENO P138: 490 (era P105/106) → 651 (P137) → 659 (P138: + 8 poročnih blokov 1909!)
EV_ONLY_TOTAL = 8               # P84: 2 + P85: 3 + P86: 1 + P102: r4 (1) + P103: r84 (1) (P77–P83, P87–P90: 0)
EV_ONLY_HOUSE_STRINGS = {"65 [~]"}  # P85 r?? — edina EV-only hiša z imenom (None × 4)
# sidra/pins P90:
H58_ROW = {"row": 15, "scan": 79, "fatherPin": "Požek"}
H46_ROW = {"row": 18, "scan": 80, "fatherPin": "Brodarič"}
H87_ROW = {"row": 19, "scan": 80, "fatherPin": "Pegdirec"}
H24A_ROW = {"row": 22, "scan": 80, "fatherPin": "Brime"}
H12_ROW = {"row": 26, "scan": 80, "fatherPin": "Dragoš"}
H30_ROW = {"row": 27, "scan": 80, "fatherPin": "Šegina"}
H20_ROW = {"row": 40, "scan": 82, "fatherPin": "Pezdirec"}
H65_ROW = {"row": 43, "scan": 82, "fatherPin": "Mihelt"}
H32_ROW = {"row": 45, "scan": 82, "fatherPin": "Urh"}
H24B_ROW = {"row": 48, "scan": 82, "fatherPin": "Toško"}
H37_ROW = {"row": 49, "scan": 82, "fatherPin": "Pezdirec"}
H69_ROW = {"row": 53, "scan": 83, "fatherPin": "Brinec"}
H72_ROW = {"row": 54, "scan": 83, "fatherPin": "Straus"}
H91_ROW = {"row": 55, "scan": 83, "fatherPin": "Muc"}
H29_ROW = {"row": 66, "scan": 84, "fatherPin": "Kuhar"}


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
    pat = r"\n  \{[^{]*?bookSignature:\s*\"" + signature + r"\".*?\n  \},"  # P138: strukturno zasidran vzorec (zaviti oklepaji v besedilu ne motijo!)
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
    """NOVELA P89 potrjena 2. leto: stran == sken − 2 za celo leto 1895
    (sken 73 = podvojen sken str. 71, ni citiran)."""
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

    # I3 — citirani skeni ⊆ okvir 78–84 + JPEG probe; sken 73 NI citiran
    # (podvojen sken str. 71 — novela P89); skena 78/81 brez Gribljev
    cited = sorted({e["scan"] for e in entries})
    inv["I3_cited_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and cited == EXPECTED_CITED and 73 not in cited
    probes = {s: probe_jpeg(urls[s - 1]) for s in cited} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())

    # I4 — okvir: vsi vpisi 1895, stran == sken − 2 (novela P89, 2. leto);
    # prelom 1896 na str. 83 (sken 85); rowsTotal 73
    rows = [e["row"] for e in entries]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1895 for e in entries)
        and all(e["page"] == page_of_scan(e["scan"]) for e in entries)
        and all(FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1] for e in entries)
        and all(FRAME_PAGES[0] <= e["page"] <= FRAME_PAGES[1] for e in entries)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and dokaz["frame"]["break1896"]["scan"] == BREAK_1896["scan"]
        and dokaz["frame"]["break1896"]["page"] == BREAK_1896["page"]
        and dokaz["frame"]["rowsTotal"] == 73
        and dokaz["frame"]["duplicateScan"]["scan"] == 73
        and "NE citiran" in dokaz["frame"]["duplicateScan"]["note"]
    )

    # I5 — števec: 15 vpisov / 14 hiš / 0 neberljivih; NOVELI: babica na
    # vseh 15 vrsticah PRAZEN; 4× PRAZNA botra (r53/r54/r55/r66);
    # ena ponovitev hiše znotraj leta (h24: r22 + r48 — DVOM)
    houses = {e["houseNo"] for e in entries}
    empty_botra_rows = sorted(e["row"] for e in entries
                              if not e["botra"] or e["botra"].startswith("—"))
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"] == "Griblje" for e in entries)
        and len(houses) == EXPECTED_DISTINCT
        and len(rows) == len(set(rows))
        and dokaz["stats"]["housesIllegible"] == 0
        and all(e["babica"] and "prazen" in e["babica"] for e in entries)  # NOVELA babica
        and empty_botra_rows == [53, 54, 55, 66]                            # NOVELA botra
        and dokaz["stats"]["babica"] == 0
        and dokaz["stats"]["emptyBotra"] == 4
    )

    # I6 — PT klasifikacija: 9 v naboru + 5 v luknjah/izven (h46 = 2. dokaz
    # v luknji 41–60 — brez novih števil); 3 NOVE hiše (20, 37, 87) po P89
    pts = pt_house_set()
    inset = sorted((h for h in houses if h in pts), key=int)
    gap = sorted((h for h in houses if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGapNew"] == PT_GAP_NEW
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and "3 nove hiše" in dokaz["stats"]["newSampleHousesNote"]
    )

    # I7 — sidra (15 vpisov — očetovski pini + kontinuitetne oznake)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    h58 = e_by_row(H58_ROW["row"])
    h46 = e_by_row(H46_ROW["row"])
    h87 = e_by_row(H87_ROW["row"])
    h24a = e_by_row(H24A_ROW["row"])
    h12 = e_by_row(H12_ROW["row"])
    h30 = e_by_row(H30_ROW["row"])
    h20 = e_by_row(H20_ROW["row"])
    h65 = e_by_row(H65_ROW["row"])
    h32 = e_by_row(H32_ROW["row"])
    h24b = e_by_row(H24B_ROW["row"])
    h37 = e_by_row(H37_ROW["row"])
    h69 = e_by_row(H69_ROW["row"])
    h72 = e_by_row(H72_ROW["row"])
    h91 = e_by_row(H91_ROW["row"])
    h29 = e_by_row(H29_ROW["row"])
    inv["I7_anchors"] = (
        h58["houseNo"] == "58" and H58_ROW["fatherPin"] in h58["father"]
        and "4. VPIS" in json.dumps(h58["notes"], ensure_ascii=False)
        and "MATI MENJANA" in json.dumps(h58["notes"], ensure_ascii=False)
        and h46["houseNo"] == "46" and H46_ROW["fatherPin"] in h46["father"]
        and "2. VPIS" in json.dumps(h46["notes"], ensure_ascii=False)
        and h87["houseNo"] == "87" and H87_ROW["fatherPin"] in h87["father"]
        and "NOVA HIŠA" in json.dumps(h87["notes"], ensure_ascii=False)
        and h24a["houseNo"] == "24" and H24A_ROW["fatherPin"] in h24a["father"]
        and "3. VPIS" in json.dumps(h24a["notes"], ensure_ascii=False)
        and h12["houseNo"] == "12" and H12_ROW["fatherPin"] in h12["father"]
        and "3. VPIS" in json.dumps(h12["notes"], ensure_ascii=False)
        and h30["houseNo"] == "30" and H30_ROW["fatherPin"] in h30["father"]
        and "3. DRUŽINA" in json.dumps(h30["notes"], ensure_ascii=False)
        and h20["houseNo"] == "20" and H20_ROW["fatherPin"] in h20["father"]
        and "NOVA HIŠA" in json.dumps(h20["notes"], ensure_ascii=False)
        and h65["houseNo"] == "65" and H65_ROW["fatherPin"] in h65["father"]
        and "4. VPIS" in json.dumps(h65["notes"], ensure_ascii=False)
        and h32["houseNo"] == "32" and H32_ROW["fatherPin"] in h32["father"]
        and "5. VPIS" in json.dumps(h32["notes"], ensure_ascii=False)
        and "NAJDALJŠA ZVEZA" in json.dumps(h32["notes"], ensure_ascii=False)
        and h24b["houseNo"] == "24" and H24B_ROW["fatherPin"] in h24b["father"]
        and "DVOM" in json.dumps(h24b["notes"], ensure_ascii=False)
        and h37["houseNo"] == "37" and H37_ROW["fatherPin"] in h37["father"]
        and "NOVA HIŠA" in json.dumps(h37["notes"], ensure_ascii=False)
        and h69["houseNo"] == "69" and H69_ROW["fatherPin"] in h69["father"]
        and "5. VPIS" in json.dumps(h69["notes"], ensure_ascii=False)
        and h72["houseNo"] == "72" and H72_ROW["fatherPin"] in h72["father"]
        and "5. VPIS" in json.dumps(h72["notes"], ensure_ascii=False)
        and h91["houseNo"] == "91" and H91_ROW["fatherPin"] in h91["father"]
        and "2. VPIS" in json.dumps(h91["notes"], ensure_ascii=False)
        and h29["houseNo"] == "29" and H29_ROW["fatherPin"] in h29["father"]
        and "MENJAVA GOSPODINJSTVA" in json.dumps(h29["notes"], ensure_ascii=False)
    )

    # I8 — čez-letne kontinuitete prek dokazov:
    # h58 (P84 r3 + P85 r22 + P87 r60 — oče Požek; P90 mati Kambic? = MENJAVA)
    # h46 (P88 r43 Brodarič × Klobučar — ISTA zveza)
    # h24 (P82 r105 + P88 r56 Brinec; P90 r22 3. vpis + r48 DVOM)
    # h12 (P87 r17 Dragos + P89 r4 Dragoš — 3. vpis)
    # h30 (P85/P86 Milek + P88 r50 Jakljevič → P90 Šegina = 3. DRUŽINA)
    # h65 (P82 r72 + P84 r102 + P88 r15 Milek → P90 Mihelt varianta; mati Požek ISTA 2×)
    # h32 (P84 r62 + P85 r67 + P87 r54 Urh — 5. vpis NAJDALJŠA zveza)
    # h72 (P83 r8 + P84 r64 + P86 r6 + P88 r46 Strauš/Straus — 5. vpis)
    # h91 (P88 r31 Novak × Kure → P90 Muc × Kure — mati ISTA, oče MENJAN)
    # h69 (P83 r15 + P84 r28 + P85 r61 + P89 r18 Brinec — oče ISTI 5×)
    # h29 (P83 r85 + P87 r11 Milek × Križan → P90 Kuhar? × Klobučar — MENJAVA)
    # h87 podcelica h63 (P87 r68 Hrižan) + Željko veriga (P83 h1 Zeljth + P89 h60)
    p77 = json.load(open(DOKAZ_P77, encoding="utf-8"))
    p82 = json.load(open(DOKAZ_P82, encoding="utf-8"))
    p83 = json.load(open(DOKAZ_P83, encoding="utf-8"))
    p84 = json.load(open(DOKAZ_P84, encoding="utf-8"))
    p85 = json.load(open(DOKAZ_P85, encoding="utf-8"))
    p86 = json.load(open(DOKAZ_P86, encoding="utf-8"))
    p87 = json.load(open(DOKAZ_P87, encoding="utf-8"))
    p88 = json.load(open(DOKAZ_P88, encoding="utf-8"))
    p89 = json.load(open(DOKAZ_P89, encoding="utf-8"))
    p84_h58 = [e for e in p84["entries"] if e.get("houseNo") == "58"]
    p85_h58 = [e for e in p85["entries"] if e.get("houseNo") == "58"]
    p87_h58 = [e for e in p87["entries"] if e.get("houseNo") == "58"]
    p88_h46 = [e for e in p88["entries"] if e.get("houseNo") == "46"]
    p82_h24 = [e for e in p82["entries"] if e.get("houseNo") == "24"]
    p88_h24 = [e for e in p88["entries"] if e.get("houseNo") == "24"]
    p87_h12 = [e for e in p87["entries"] if e.get("houseNo") == "12"]
    p89_h12 = [e for e in p89["entries"] if e.get("houseNo") == "12"]
    p85_h30 = [e for e in p85["entries"] if e.get("houseNo") == "30"]
    p86_h30 = [e for e in p86["entries"] if e.get("houseNo") == "30"]
    p88_h30 = [e for e in p88["entries"] if e.get("houseNo") == "30"]
    p82_h65 = [e for e in p82["entries"] if e.get("houseNo") == "65"]
    p88_h65 = [e for e in p88["entries"] if e.get("houseNo") == "65"]
    p84_h32 = [e for e in p84["entries"] if e.get("houseNo") == "32"]
    p85_h32 = [e for e in p85["entries"] if e.get("houseNo") == "32"]
    p87_h32 = [e for e in p87["entries"] if e.get("houseNo") == "32"]
    p83_h72 = [e for e in p83["entries"] if e.get("houseNo") == "72"]
    p88_h72 = [e for e in p88["entries"] if e.get("houseNo") == "72"]
    p88_h91 = [e for e in p88["entries"] if e.get("houseNo") == "91"]
    p83_h69 = [e for e in p83["entries"] if e.get("houseNo") == "69"]
    p84_h69 = [e for e in p84["entries"] if e.get("houseNo") == "69"]
    p85_h69 = [e for e in p85["entries"] if e.get("houseNo") == "69"]
    p89_h69 = [e for e in p89["entries"] if e.get("houseNo") == "69"]
    p83_h29 = [e for e in p83["entries"] if e.get("houseNo") == "29"]
    p87_h29 = [e for e in p87["entries"] if e.get("houseNo") == "29"]
    p87_h63 = [e for e in p87["entries"] if e.get("houseNo") == "63"]
    p83_h1 = [e for e in p83["entries"] if e.get("houseNo") == "1"]
    p89_h60 = [e for e in p89["entries"] if e.get("houseNo") == "60"]
    inv["I8_crossyear_continuity"] = (
        # h58 — 4. VPIS; oče ISTI 3. leto; MATI MENJANA (Dragoš → Kambic?)
        len(p84_h58) == 1 and "Požek" in p84_h58[0]["father"]
        and len(p85_h58) == 1 and "Požek" in p85_h58[0]["father"]
        and len(p87_h58) == 1 and "Požek" in p87_h58[0]["father"]
        and "Dragos" in p87_h58[0]["mother"]
        and "Požek" in h58["father"] and "Kambic" in h58["mother"]
        # h46 — ISTA zveza (P88 Brodarič × Klobučar)
        and len(p88_h46) == 1 and "Brodarič" in p88_h46[0]["father"]
        and "Klobučar" in p88_h46[0]["mother"]
        and "Brodarič" in h46["father"] and "Klobuč" in h46["mother"]
        # h24 — 3. vpis Brime zveze (P82 + P88) + DVOM r48
        and len(p82_h24) == 1 and "Brinec" in p82_h24[0]["father"]
        and len(p88_h24) == 1 and "Brinec" in p88_h24[0]["father"]
        and "Brime" in h24a["father"] and "Jakobič" in h24a["mother"]
        and "Toško" in h24b["father"] and "Simec" in h24b["mother"]
        # h12 — 3. vpis (P87 Dragos + P89 Dragoš)
        and len(p87_h12) == 1 and "Dragos" in p87_h12[0]["father"]
        and len(p89_h12) == 1 and "Dragoš" in p89_h12[0]["father"]
        and "Dragoš" in h12["father"]
        # h30 — 3. DRUŽINA (P85 2× Milek + P86 Milek + P88 Jakljevič → P90 Šegina)
        and len(p85_h30) == 2 and all("Milek" in e["father"] for e in p85_h30)
        and len(p86_h30) == 1 and "Milek" in p86_h30[0]["father"]
        and len(p88_h30) == 1 and "Jakljevič" in p88_h30[0]["father"]
        and "Šegina" in h30["father"]
        # h65 — 4. vpis (P82/P88 Milek; P90 Mihelt varianta; mati Požek ISTA)
        and len(p82_h65) == 1 and "Milek" in p82_h65[0]["father"]
        and "Požek" in p82_h65[0]["mother"]
        and len(p88_h65) == 1 and "Milek" in p88_h65[0]["father"]
        and "Mihelt" in h65["father"] and "Požek" in h65["mother"]
        # h32 — 5. vpis NAJDALJŠA zveza (P84/P85/P87 Urh)
        and len(p84_h32) == 1 and "Urh" in p84_h32[0]["father"]
        and len(p85_h32) == 1 and "Urh" in p85_h32[0]["father"]
        and len(p87_h32) == 1 and "Urh" in p87_h32[0]["father"]
        and "Urh" in h32["father"] and "Pegdirec" in h32["mother"]
        # h72 — 5. vpis (P83 + P88 Strauš/Straus)
        and len(p83_h72) == 1 and "Strauš" in p83_h72[0]["father"]
        and len(p88_h72) == 1 and "Strauš" in p88_h72[0]["father"]
        and "Straus" in h72["father"] and "Jakobič" in h72["mother"]
        # h91 — 2. vpis; mati ISTA, oče MENJAN (Novak → Muc)
        and len(p88_h91) == 1 and "Novak" in p88_h91[0]["father"]
        and "Kure" in p88_h91[0]["mother"]
        and "Muc" in h91["father"] and "Kure" in h91["mother"]
        # h69 — 5. vpis; oče ISTI (P83/P84/P85/P89)
        and len(p83_h69) == 1 and "Brinec" in p83_h69[0]["father"]
        and len(p84_h69) == 1 and "Brinec" in p84_h69[0]["father"]
        and len(p85_h69) == 1 and "Brinec" in p85_h69[0]["father"]
        and len(p89_h69) == 1 and "Brinec" in p89_h69[0]["father"]
        and "Brinec" in h69["father"]
        # h29 — MENJAVA (P83/P87 Milek × Križan → P90 Kuhar? × Klobučar)
        and len(p83_h29) == 1 and "Milek" in p83_h29[0]["father"]
        and len(p87_h29) == 1 and "Milek" in p87_h29[0]["father"]
        and "Kuhar" in h29["father"] and "Klobučar" in h29["mother"]
        # h87 podcelica: h63 Hrižan (P87) + Željko veriga (P83 h1 + P89 h60)
        and len(p87_h63) == 1 and "Hrižan" in p87_h63[0]["father"]
        and "Hrižan" in json.dumps(h87["mother"], ensure_ascii=False)
        and "Željko" in json.dumps(h87["mother"], ensure_ascii=False)
        and len(p83_h1) == 1 and "Zeljth" in p83_h1[0]["father"]
        and len(p89_h60) == 1 and "Željko" in p89_h60[0]["father"]
    )

    # I9 — runtime projekcija: HOUSE_VITALS 1895 == 15 blokov (h24 2×),
    # hiše == dokaz; stran == sken − 2; skupaj 179; brez »Hraus« v aktivnih whatSi
    vitals_1895 = parish_vitals(BOOK_SIGNATURE, 1895)
    hv_houses = sorted({v["houseNo"] for v in vitals_1895}, key=int)
    src = open(PARISH_TS, encoding="utf-8").read()
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    active_hraus = [
        w for w in re.findall(r"whatSi:\s*\"([^\"]+)\"", src)
        if "Hraus" in w and "re-read" not in w and "prej" not in w
    ]
    inv["I9_runtime_projection"] = (
        len(vitals_1895) == EXPECTED_HOUSES_VITALS
        and hv_houses == sorted(houses, key=int)
        and all(v["scan"] and 78 <= v["scan"] <= 84 and v["page"] == page_of_scan(v["scan"])
                for v in vitals_1895)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
        and not active_hraus
    )

    # I10 — statistika dokaza == neodvisen preracun: 11 ponovitev + 3 nove
    # (20/37/87); kumulativ 179 + 6 EV-only == 185; hiše vitals 67 (64 + 3) —
    # dokaz 68 = 67 + EV-only »65 [~]« (P85, edina imenovana EV-only hiša)
    # klasifikacija v vesolju lastnega leta — poznejši bloki (04105 > 1895)
    # ne smejo spreminjati zgodovinske klasifikacije novih/ponovljenih hiš (h20: 1897 ponovitev)
    vitals_pre96 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911))
    ]
    repeat_houses = [h for h in houses if any(
        v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1895
        or v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE
        for v in vitals_pre96
    )]
    new_houses = sorted(houses - set(repeat_houses), key=int)
    n_entries_total = len(vitals_all)
    n_houses_total = len({v["houseNo"] for v in vitals_all})
    # EV-only hiše: P84/P85/P86 vnosi brez vitals bloka (4× None + »65 [~]«)
    ev_only_houses = set()
    for fn in (DOKAZ_P84, DOKAZ_P85, DOKAZ_P86):
        d = json.load(open(fn, encoding="utf-8"))
        vit_h = {v["houseNo"] for v in vitals_all}
        for e in d["entries"]:
            hn = e.get("houseNo")
            if hn is not None and hn not in vit_h:
                ev_only_houses.add(hn)
    cumulative = dokaz["stats"]["cumulative"]
    intra = dokaz["stats"]["intraYearRepeats"]
    inv["I10_stats_independent"] = (
        len(repeat_houses) == EXPECTED_REPEATS
        and (dokaz["stats"].get("repeatHouses") or EXPECTED_REPEATS) == EXPECTED_REPEATS  # P90 JSON: repeatHouses null — ključ obstaja, .get vrne None
        and new_houses == dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and len(intra) == 1 and intra[0]["houseNo"] == "24"
        and sorted(intra[0]["rows"]) == [22, 48]
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 667  # POSODABLJENO P138: 659 + 8 (bilo 498 po P110!)
        and n_houses_total == 89  # POSODABLJENO P138 (bilo 85)  # P98: 80 vitals; P99: + 3 (h6, h42, h50); P100: + 0 (1905 brez novih); P101: + 1 (h4); P107: + 1 (h86)
        and ev_only_houses == EV_ONLY_HOUSE_STRINGS
        and cumulative["entries"] == 185
        and cumulative["houses"] == 68  # 67 vitals + 1 EV-only »65 [~]«
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and len(dokaz["entries"]) == 15
        # neodvisen preracun duhovnikov: 9 + 4 + 2 == 15
        and sum(1 for e in entries if "Jele" in e["priest"]) == 9
        and sum(1 for e in entries if "Rauq" in e["priest"]) == 4
        and sum(1 for e in entries if "Klun" in e["priest"]) == 2
    )

    ok = all(inv.values())
    print("P90 — krstna knjiga 04105, polno leto 1895 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {cited} (sken 73 = podvojen str. 71 — ni citiran;"
          f" 78/81 brez Gribljev)")
    print(f"vpisi {len(entries)} / hiše {len(houses)} (h24 DVOM 2×);"
          f" PT {len(inset)}/{len(gap)}; nove hiše {sorted(new_houses)};"
          f" vitals 1895 = {len(vitals_1895)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vitals = {n_houses_total}; kumulativ {n_entries_total + EV_ONLY_TOTAL}"
          f" vpisov / {n_houses_total + len(ev_only_houses)} hiš")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
