#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P89 — župnija Podzemelj: krstna knjiga 04105, polno leto 1894 (issue #18).

Razširitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85
(1890) → P86 (1891) → P87 (1892) → P88 (1893) na leto 1894: okvir skeni 70–78
== strani 69–76 (glava »1894« na str. 69 po 1893 row 83; velike cifre »1895~«
na str. 76 po row 90) — vsi vpisi z Griblji. NOVELA OKVIRA: sken 73 je
PODOVOJEN sken str. 71 (matricula re-scan; prvi v seriji) — stran == sken − 1
velja do skena 72, od skena 74 naprej stran == sken − 2. LE OKVIR — prejšnja
leta imajo svoje skripte p82–p88. Sidra: h2 ŠTIRIKRATNA kontinuiteta (ISTI
starši Hlebec × Jakobič 4×: 1887+1889+1891+1894 — najdaljša zveza vzorca),
h71 ISTA zveza Jurij Strauš × Barbara čez 8 let (P77 1886 r83) — Strauš na
DVEH sosednjih hišah (h71+h72; PUA @71 0.8571), h36 Križan 2. generacija
(tri-virska hiša dobi 4. vir), h31 4. VPIS (oče Papič/Fapič ISTI + mati
Straus ISTA + botra Klobučar), h17 ISTI oče Kralj ¼ + MATER MENJANA (Ana
Jakobič 1887 → Doroteja Firlak? [~]), h57 ISTA botra pa čez 8 let (P77),
h60 + h23 ISTA botra pa 2. leto (P88), h12/h53/h73/h75 ISTA zvezi (2. vpis).
NOVELA: PRVO leto z 0 novih hiš — vseh 14 vpisov na že zasidranih hišah.

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
DOKAZ = "research/issue17/parish-baptism-1894.json"
DOKAZ_P77 = "research/issue17/parish-sample-transcription.json"
DOKAZ_P82 = "research/issue17/parish-baptism-1887.json"
DOKAZ_P83 = "research/issue17/parish-baptism-1888.json"
DOKAZ_P84 = "research/issue17/parish-baptism-1889.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
DOKAZ_P87 = "research/issue17/parish-baptism-1892.json"
DOKAZ_P88 = "research/issue17/parish-baptism-1893.json"
PARISH_TS = "src/data/atlas/parish.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (70, 78)          # skeni 70–78 == strani 69–76 (okvir leta 1894)
FRAME_PAGES = (69, 76)
BREAK_1895 = {"scan": 78, "page": 76}
EXPECTED_ENTRIES = 14
EXPECTED_DISTINCT = 14          # 14 vpisov / 14 hiš (brez ponovitev znotraj leta)
EXPECTED_CITED = [70, 71, 72, 74, 75, 76, 77, 78]  # sken 73 = podvojen str. 71
EXPECTED_PT_IN_SET = {"2", "12", "13", "17", "23", "31", "36", "69", "71", "73", "75"}
EXPECTED_PT_GAP = {"53", "57", "60"}   # vse tri PONOVITVE (53 P86; 57 P79/P77; 60 P80/P88)
PT_GAP_NEW = []                 # brez novih (ostaja 15 dokazanih)
EXPECTED_NEW_HOUSES = []        # NOVELA: prvo leto z 0 novih hiš
EXPECTED_REPEATS = 14
EXPECTED_HOUSES_VITALS = 14     # 14 vpisov, vsi zasidrani (runtime projekcija)
EXPECTED_VITALS_TOTAL = 341     # HOUSE_VITALS 179 + 14 (p80 I7 pin); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900); P98: + 12 (1903); P99: + 19 (1904); P101: + 18 (1906)
EV_ONLY_TOTAL = 6               # P84: 2 + P85: 3 + P86: 1 (P87–P89: 0)
# sidra/pins P89:
H2_ROW = {"row": 11, "scan": 71, "fatherPin": "Hlebec"}
H12_ROW = {"row": 4, "scan": 70, "fatherPin": "Dragoš"}
H53_ROW = {"row": 14, "scan": 71, "fatherPin": "Pegdirec"}
H69_ROW = {"row": 18, "scan": 71, "fatherPin": "Brinec"}
H36_ROW = {"row": 24, "scan": 72, "fatherPin": "Križan"}
H57_ROW = {"row": 44, "scan": 74, "fatherPin": "Pegdirec"}
H73_ROW = {"row": 47, "scan": 75, "fatherPin": "Županič"}
H31_ROW = {"row": 49, "scan": 75, "fatherPin": "Fapič"}
H13_ROW = {"row": 50, "scan": 75, "fatherPin": "Jakljevič"}
H75_ROW = {"row": 64, "scan": 76, "fatherPin": "Jakobič"}
H17_ROW = {"row": 65, "scan": 76, "fatherPin": "Kralj"}
H71_ROW = {"row": 72, "scan": 77, "fatherPin": "Straus"}
H23_ROW = {"row": 88, "scan": 78, "fatherPin": "Brinec"}
H60_ROW = {"row": 90, "scan": 78, "fatherPin": "Željko"}


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
    """NOVELA P89: stran == sken − 1 do skena 72; od skena 74 naprej − 2
    (sken 73 = podvojen sken str. 71)."""
    return scan - 2 if scan >= 74 else scan - 1


def verify():
    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    entries = dokaz["entries"]
    inv = {}

    # I1 — knjiga dostopna + inventar 326
    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    # I3 — citirani skeni ⊆ okvir 70–78 + JPEG probe; sken 73 NI citiran
    # (podvojen sken str. 71 — novela P89); vpisi na 70, 71, 72, 74–78
    cited = sorted({e["scan"] for e in entries})
    inv["I3_cited_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and cited == EXPECTED_CITED and 73 not in cited
    probes = {s: probe_jpeg(urls[s - 1]) for s in cited} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())

    # I4 — okvir: vsi vpisi 1894, stran == sken − 1 (≤72) / sken − 2 (≥74);
    # prelom 1895 na str. 76 (sken 78); rowsTotal 90
    rows = [e["row"] for e in entries]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1894 for e in entries)
        and all(e["page"] == page_of_scan(e["scan"]) for e in entries)
        and all(FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1] for e in entries)
        and all(FRAME_PAGES[0] <= e["page"] <= FRAME_PAGES[1] for e in entries)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and dokaz["frame"]["break1895"]["scan"] == BREAK_1895["scan"]
        and dokaz["frame"]["break1895"]["page"] == BREAK_1895["page"]
        and dokaz["frame"]["rowsTotal"] == 90
        and "73" in dokaz["frame"]["duplicateScan"]["note"]
    )

    # I5 — števec: 14 vpisov / 14 hiš / 0 neberljivih / brez ponovitev znotraj leta
    houses = {e["houseNo"] for e in entries}
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"] == "Griblje" for e in entries)
        and len(houses) == EXPECTED_DISTINCT
        and len(rows) == len(set(rows))
        and dokaz["stats"]["housesIllegible"] == 0
        and sum(1 for e in entries if e["babica"] is None) == 1  # r50 prazna
    )

    # I6 — PT klasifikacija: 13 v naboru + 1 v luknji (53 ponovitev, 0 novih);
    # NOVELA: 0 novih hiš (vseh 14 zasidranih)
    pts = pt_house_set()
    inset = sorted((h for h in houses if h in pts), key=int)
    gap = sorted((h for h in houses if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGapNew"] == PT_GAP_NEW
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and "0 NOVIH" in json.dumps(dokaz["stats"]["newSampleHousesNote"], ensure_ascii=False)
    )

    # I7 — sidra (14 hiš — vsi očetovski pini + kontinuitetne oznake)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    h2 = e_by_row(H2_ROW["row"])
    h12 = e_by_row(H12_ROW["row"])
    h53 = e_by_row(H53_ROW["row"])
    h69 = e_by_row(H69_ROW["row"])
    h36 = e_by_row(H36_ROW["row"])
    h57 = e_by_row(H57_ROW["row"])
    h73 = e_by_row(H73_ROW["row"])
    h31 = e_by_row(H31_ROW["row"])
    h13 = e_by_row(H13_ROW["row"])
    h75 = e_by_row(H75_ROW["row"])
    h17 = e_by_row(H17_ROW["row"])
    h71 = e_by_row(H71_ROW["row"])
    h23 = e_by_row(H23_ROW["row"])
    h60 = e_by_row(H60_ROW["row"])
    inv["I7_anchors"] = (
        h2["houseNo"] == "2" and H2_ROW["fatherPin"] in h2["father"]
        and "4. VPIS" in json.dumps(h2["notes"], ensure_ascii=False)
        and h12["houseNo"] == "12" and H12_ROW["fatherPin"] in h12["father"]
        and h53["houseNo"] == "53" and H53_ROW["fatherPin"] in h53["father"]
        and h69["houseNo"] == "69" and H69_ROW["fatherPin"] in h69["father"]
        and h36["houseNo"] == "36" and H36_ROW["fatherPin"] in h36["father"]
        and "2. GENERACIJA" in json.dumps(h36["notes"], ensure_ascii=False)
        and h57["houseNo"] == "57" and H57_ROW["fatherPin"] in h57["father"]
        and h73["houseNo"] == "73" and H73_ROW["fatherPin"] in h73["father"]
        and h31["houseNo"] == "31" and H31_ROW["fatherPin"] in h31["father"]
        and "4. VPIS" in json.dumps(h31["notes"], ensure_ascii=False)
        and h13["houseNo"] == "13" and H13_ROW["fatherPin"] in h13["father"]
        and h75["houseNo"] == "75" and H75_ROW["fatherPin"] in h75["father"]
        and h17["houseNo"] == "17" and H17_ROW["fatherPin"] in h17["father"]
        and "MATER MENJANA" in json.dumps(h17["notes"], ensure_ascii=False)
        and h71["houseNo"] == "71" and H71_ROW["fatherPin"] in h71["father"]
        and h23["houseNo"] == "23" and H23_ROW["fatherPin"] in h23["father"]
        and h60["houseNo"] == "60" and H60_ROW["fatherPin"] in h60["father"]
    )

    # I8 — čez-letne kontinuitete prek dokazov:
    # h2 (P82 r77 + P84 r75 + P86 r43 — ISTI starši Hlebec × Jakobič vsi štirje)
    # h31 (P82 r67 Papič × Straus + botra Klobučar; P85 r14; P86 r50 — oče varianta + mati ISTA)
    # h53 (P86 r40 Pozdirec × Križan + babica Ana Križan)
    # h73 (P87 r13 Županič × Pozdirec)
    # h75 (P87 r8 Jakobčič × Sušljar + botra Barb. Brinec ISTA)
    # h12 (P87 r17 Dragos × Civlkovič?)
    # h17 (P82 r82 Kralj ¼ × Ana Jakobič — mati menjana)
    # h71 (P77 r83 Jurij Strauš ½ × Barbara Jakopič — ISTA ZVEZA 8 let)
    # h36 (P77 r39 Šimec + r95 Matija Križan × Ana Milavec; h57 P77 r20 ISTA botra pa)
    # h23 (P88 r28 Brinec + botra Jaklič + Pegdirec ISTA pa) + h60 (P88 r1 Željko × Brodarič + ISTA botra pa)
    # h1 Željko (P83 r3 Zeljth) — Željko h60
    p77 = json.load(open(DOKAZ_P77, encoding="utf-8"))
    p82 = json.load(open(DOKAZ_P82, encoding="utf-8"))
    p83 = json.load(open(DOKAZ_P83, encoding="utf-8"))
    p84 = json.load(open(DOKAZ_P84, encoding="utf-8"))
    p85 = json.load(open(DOKAZ_P85, encoding="utf-8"))
    p86 = json.load(open(DOKAZ_P86, encoding="utf-8"))
    p87 = json.load(open(DOKAZ_P87, encoding="utf-8"))
    p88 = json.load(open(DOKAZ_P88, encoding="utf-8"))
    p82_h2 = [e for e in p82["entries"] if e.get("houseNo") == "2"]
    p84_h2 = [e for e in p84["entries"] if e.get("houseNo") == "2"]
    p86_h2 = [e for e in p86["entries"] if e.get("houseNo") == "2"]
    p82_h31 = [e for e in p82["entries"] if e.get("houseNo") == "31"]  # r55 Urh + r67 Papič — 2 vpisa
    p85_h31 = [e for e in p85["entries"] if e.get("houseNo") == "31"]
    p86_h31 = [e for e in p86["entries"] if e.get("houseNo") == "31"]
    p86_h53 = [e for e in p86["entries"] if e.get("houseNo") == "53"]
    p87_h73 = [e for e in p87["entries"] if e.get("houseNo") == "73"]
    p87_h75 = [e for e in p87["entries"] if e.get("houseNo") == "75"]
    p87_h12 = [e for e in p87["entries"] if e.get("houseNo") == "12"]
    p82_h17 = [e for e in p82["entries"] if e.get("houseNo") == "17"]
    p77_h71 = [e for e in p77["entries"] if e.get("houseNo") == "71"]
    p77_h36 = [e for e in p77["entries"] if e.get("houseNo") == "36"]
    p77_h57 = [e for e in p77["entries"] if e.get("houseNo") == "57"]
    p77_h13 = [e for e in p77["entries"] if e.get("houseNo") == "13"]
    p88_h23 = [e for e in p88["entries"] if e.get("houseNo") == "23"]
    p88_h60 = [e for e in p88["entries"] if e.get("houseNo") == "60"]
    p83_h1 = [e for e in p83["entries"] if e.get("houseNo") == "1"]
    inv["I8_crossyear_continuity"] = (
        # h2 — ŠTIRIKRATNA (vsi trije prejšnji + 1894)
        len(p82_h2) == 1 and "Hlebec" in p82_h2[0]["father"] and "Jakobič" in p82_h2[0]["mother"]
        and len(p84_h2) == 1 and "Hlebec" in p84_h2[0]["father"]
        and len(p86_h2) == 1 and "Hlebec" in p86_h2[0]["father"]
        and "Hlebec" in h2["father"] and "Jakobič" in h2["mother"]
        and "4. VPIS" in json.dumps(h2["notes"], ensure_ascii=False)
        # h31 — 4. VPIS (oče varianta P/F/T + mati Straus ISTA + botra Klobučar)
        # P82 h31 ima 2 vpisa (r55 Urh + r67 Papič) — papičeva je r67
        and len(p82_h31) == 2
        and any("Papič" in e["father"] for e in p82_h31)
        and any("Straus" in e["mother"] and "Klobučar" in e["botra"] for e in p82_h31)
        and len(p85_h31) == 1 and "Papič" in p85_h31[0]["father"] and "Straus" in p85_h31[0]["mother"]
        and len(p86_h31) == 1 and "Tepič" in p86_h31[0]["father"] and "Straus" in p86_h31[0]["mother"]
        and "Fapič" in h31["father"] and "Straus" in h31["mother"] and "Klobučar" in h31["botra"]
        # h53 — ISTA zveza (P86 Pozdirec × Križan + babica Ana Križan)
        and len(p86_h53) == 1 and "Pozdirec" in p86_h53[0]["father"] and "Križan" in p86_h53[0]["mother"]
        and "Ana Križan" in p86_h53[0]["babica"]
        and "Pegdirec" in h53["father"] and "Hrižan" in h53["mother"] and "Hrižan" in h53["babica"]
        # h73 — ISTA zveza (P87 Županič × Pozdirec)
        and len(p87_h73) == 1 and "Županič" in p87_h73[0]["father"] and "Pozdirec" in p87_h73[0]["mother"]
        and "Županič" in h73["father"] and "Pegdirec" in h73["mother"]
        # h75 — ISTA zveza + botra Barb. Brinec ISTA (P87 Jakobčič × Sušljar)
        and len(p87_h75) == 1 and "Jakobčič" in p87_h75[0]["father"] and "Sušljar" in p87_h75[0]["mother"]
        and "Brinec" in p87_h75[0]["botra"]
        and "Jakobič" in h75["father"] and "Stubljar" in h75["mother"] and "Brinec" in h75["botra"]
        # h12 — ISTI oče (P87 Dragos)
        and len(p87_h12) == 1 and "Dragos" in p87_h12[0]["father"]
        and "Dragoš" in h12["father"]
        # h17 — ISTI oče Kralj ¼; mati menjana (P82 Ana Jakobič → 1894 Firlak)
        and len(p82_h17) == 1 and "Kralj" in p82_h17[0]["father"] and "Jakobič" in p82_h17[0]["mother"]
        and "Kralj" in h17["father"] and "Firlak" in h17["mother"]
        # h71 — ISTA ZVEZA čez 8 let (P77 r83 Jurij Strauš × Barbara Jakopič)
        and len(p77_h71) == 1 and "Strauš" in p77_h71[0]["father"] and "Jakopič" in p77_h71[0]["mother"]
        and "Straus" in h71["father"] and "Jakobčič" in h71["mother"]
        # h36 — Križan 2. generacija (P77 r95 Matija Križan × Ana Milavec)
        and len(p77_h36) == 2 and any("Križan" in e["father"] for e in p77_h36)
        and "Križan" in h36["father"]
        # h57 — ISTA botra pa (P77 r20: Jurij Brodarič + Marija Strauš)
        and len(p77_h57) == 1 and "Brodarič" in p77_h57[0]["godparents"]
        and "Strauš" in p77_h57[0]["godparents"]
        and "Brodarič" in h57["botra"] and "Straus" in h57["botra"]
        # h13 — P77 r77 Matija Jakopič? (ISTI oče ime+status)
        and len(p77_h13) == 1 and "Matija" in p77_h13[0]["father"]
        and "Jakljevič" in h13["father"]
        # h23 + h60 — ISTA botra pa 2. leto (P88)
        and len(p88_h23) == 1 and "Brinec" in p88_h23[0]["father"]
        and "Jaklič" in p88_h23[0]["botra"] and "Pegdirec" in p88_h23[0]["botra"]
        and "Brinec" in h23["father"] and "Jakljič" in h23["botra"] and "Pegdirec" in h23["botra"]
        and len(p88_h60) == 1 and "Željko" in p88_h60[0]["father"] and "Brodarič" in p88_h60[0]["mother"]
        and "Pegdirec" in p88_h60[0]["botra"] and "Klepec" in p88_h60[0]["botra"]
        and "Željko" in h60["father"] and "Brodarič" in h60["mother"]
        and "Pegdirec" in h60["botra"] and "Klepec" in h60["botra"]
        # Željko h1 (P83) — familija 2 hiši
        and len(p83_h1) == 1 and "Zeljth" in p83_h1[0]["father"]
    )

    # I9 — runtime projekcija: HOUSE_VITALS 1894 == 14 zasidranih
    # (sk. 70–78, stran == sken−1 / sken−2 po noveli); skupaj 164;
    # brez »Hraus« v aktivnih whatSi poljih
    vitals_1894 = parish_vitals(BOOK_SIGNATURE, 1894)
    hv_houses = sorted((v["houseNo"] for v in vitals_1894), key=int)
    src = open(PARISH_TS, encoding="utf-8").read()
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    active_hraus = [
        w for w in re.findall(r"whatSi:\s*\"([^\"]+)\"", src)
        if "Hraus" in w and "re-read" not in w and "prej" not in w
    ]
    inv["I9_runtime_projection"] = (
        len(vitals_1894) == EXPECTED_HOUSES_VITALS
        and sorted(set(hv_houses), key=int) == sorted(houses, key=int)
        and all(v["scan"] and 70 <= v["scan"] <= 78 and v["page"] == page_of_scan(v["scan"])
                for v in vitals_1894)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
        and not active_hraus
    )

    # I10 — statistika dokaza == neodvisen preracun: 14 ponovitev + 0 novih
    # (NOVELA: prvo leto brez novih hiš — vse 14 že v vitals prej);
    # sampleTotal po konvenciji verige P82–P88 (170 = 156 + 14; hiše 65)
    # klasifikacija v vesolju lastnega leta — poznejši bloki (04105 > 1894)
    # ne smejo spreminjati zgodovinske klasifikacije novih/ponovljenih hiš
    vitals_pre95 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1906))
    ]
    repeat_houses = [h for h in houses if any(
        v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1894
        or v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE
        for v in vitals_pre95
    )]
    new_houses = sorted(houses - set(repeat_houses), key=int)
    n_entries_total = len(vitals_all)
    n_houses_total = len({v["houseNo"] for v in vitals_all})
    inv["I10_stats_independent"] = (
        len(repeat_houses) == dokaz["stats"]["repeatHouses"] == EXPECTED_REPEATS
        and new_houses == dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 347  # kumulativno po P101 (341 + 6)
        and n_houses_total == 84  # P98: 80 vitals; P99: + 3 (h6, h42, h50); P100: + 0 (1905 brez novih); P101: + 1 (h4)
        and dokaz["stats"]["sampleTotal"] == "170 vpisov / 65 hiš čez tri knjige (04105 + 04894 + 04455) in DEVET let (1886/1887/1888/1889/1890/1891/1892/1893/1894)"
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and len(dokaz["entries"]) == 14
    )

    ok = all(inv.values())
    print("P89 — krstna knjiga 04105, polno leto 1894 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {cited} (sken 73 = podvojen str. 71 — novela)")
    print(f"vpisi {len(entries)} / hiše {len(houses)}; PT {len(inset)}/{len(gap)};"
          f" nove hiše {sorted(new_houses)}; vitals 1894 = {len(vitals_1894)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vseh treh knjig = {n_houses_total}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
