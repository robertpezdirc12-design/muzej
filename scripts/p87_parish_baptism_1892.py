#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P87 — župnija Podzemelj: krstna knjiga 04105, polno leto 1892 (issue #18).

Razširitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85
(1890) → P86 (1891) na leto 1892: okvir skeni 56–63 == strani 55–62 (stran
== sken − 1; leto se začne na str. 55 row 1 po 1891 rows 65–75; velike cifre
»1893~« na str. 62 po row 82) — vsi vpisi z Griblji. LE OKVIR — prejšnja
leta imajo svoje skripte p82/p83/p84/p85/p86. Sidra: h58 Požek × Dragos
(3. leto — 1889+1890+1892), h61 Požek × Dragos (P86 kontinuiteta 2. leto,
isti vzorec brez botre/podpisa), h63 Križan/Hrižan (oče ISTI 3× — P85 sidro),
h1 Željko × Kure (ISTA zveza 1888+1892), h32 Urh (ISTI oče 1890+1892),
h90 učitelj Kopitar × Schweiger (ISTA družina 1890+1892), h24 4. FAMILIJA,
h27 3. FAMILIJA, nove hiše 12/73/75.

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
DOKAZ = "research/issue17/parish-baptism-1892.json"
DOKAZ_P83 = "research/issue17/parish-baptism-1888.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
PARISH_TS = "src/data/atlas/parish.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (56, 63)          # skeni 56–63 == strani 55–62 (okvir leta 1892)
FRAME_PAGES = (55, 62)
BREAK_1893 = {"scan": 63, "page": 62}
EXPECTED_ENTRIES = 12
EXPECTED_DISTINCT = 12          # 12 vpisov / 12 hiš — NARE (0 neberljivih)
ILLEGIBLE_ROWS = ()             # 1892 brez evidence-only
EXPECTED_PT_IN_SET = {"1", "12", "24", "27", "29", "32", "61", "63", "73", "75", "90"}
EXPECTED_PT_GAP = {"58"}
PT_GAP_NEW = []                 # 58 že dokazana (P84/P85) — brez novih
EXPECTED_NEW_HOUSES = ["12", "73", "75"]
EXPECTED_REPEATS = 9
EXPECTED_HOUSES_VITALS = 12     # 12 vpisov, vsi zasidrani (runtime projekcija)
EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 121 + 12 (p80 I7 pin); P88: + 17 (1893); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900)
EV_ONLY_TOTAL = 6               # P84: 2 + P85: 3 + P86: 1 (P87: 0)
# sidra/pins P87:
H58_ROW = {"row": 60, "scan": 61, "fatherPin": "Požek"}
H61_ROW = {"row": 70, "scan": 61, "fatherPin": "Požek"}
H63_ROW = {"row": 68, "scan": 61, "fatherPin": "Hrižan"}
H1_ROW = {"row": 50, "scan": 60, "fatherPin": "Željko"}
H32_ROW = {"row": 54, "scan": 60, "fatherPin": "Urh"}
H90_ROW = {"row": 64, "scan": 61, "fatherPin": "Kopitac"}
H24_ROW = {"row": 80, "scan": 62, "fatherPin": "Jurajevič"}
H27_ROW = {"row": 20, "scan": 57, "fatherPin": "Pozdirec"}


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


def verify():
    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    entries = dokaz["entries"]
    inv = {}

    # I1 — knjiga dostopna + inventar 326
    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    # I3 — citirani skeni ⊆ okvir 56–63 + JPEG probe (sken 63 = str. 62:
    # prelom 1893; vpisi na skenih 56, 57, 60, 61, 62 — 58/59 brez Gribljev)
    cited = sorted({e["scan"] for e in entries})
    inv["I3_cited_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and cited == [56, 57, 60, 61, 62]
    probes = {s: probe_jpeg(urls[s - 1]) for s in cited} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())

    # I4 — okvir: vsi vpisi 1892, skeni 56–62, stran == sken − 1; prelom 1893
    rows = [e["row"] for e in entries]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1892 for e in entries)
        and all(e["scan"] - 1 == e["page"] for e in entries)
        and all(FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1] for e in entries)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and dokaz["frame"]["break1893"]["scan"] == BREAK_1893["scan"]
        and dokaz["frame"]["break1893"]["page"] == BREAK_1893["page"]
        and dokaz["frame"]["rowsTotal"] == 82
    )

    # I5 — števec: 12 vpisov / 12 hiš / 0 neberljivih — NARE
    ev_only = [e for e in entries if e["row"] in ILLEGIBLE_ROWS]
    named = [e for e in entries if e["row"] not in ILLEGIBLE_ROWS]
    houses = {e["houseNo"] for e in named}
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"] == "Griblje" for e in entries)
        and len(houses) == EXPECTED_DISTINCT
        and len(ev_only) == 0
        and dokaz["stats"]["housesIllegible"] == 0
    )

    # I6 — PT klasifikacija: 11 v naboru + 1 v luknji (58 — že dokazana P84/P85;
    # brez NOVIH luknjanih številk); nove hiše 12/73/75
    pts = pt_house_set()
    inset = sorted((h for h in houses if h in pts), key=int)
    gap = sorted((h for h in houses if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGapNew"] == PT_GAP_NEW
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
    )

    # I7 — sidra (h58 Požek × Dragos 3. leto; h61 Požek = P86 kontinuiteta;
    # h63 Hrižan = P85 sidro; h1 Željko 1888+1892; h32 Urh; h90 šolska;
    # h24 4. FAMILIJA; h27 3. FAMILIJA)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    h58 = e_by_row(H58_ROW["row"])
    h61 = e_by_row(H61_ROW["row"])
    h63 = e_by_row(H63_ROW["row"])
    h1 = e_by_row(H1_ROW["row"])
    h32 = e_by_row(H32_ROW["row"])
    h90 = e_by_row(H90_ROW["row"])
    h24 = e_by_row(H24_ROW["row"])
    h27 = e_by_row(H27_ROW["row"])
    inv["I7_anchors"] = (
        h58["houseNo"] == "58"
        and H58_ROW["fatherPin"] in h58["father"]
        and "1889" in json.dumps(h58["notes"], ensure_ascii=False)
        and h61["houseNo"] == "61"
        and H61_ROW["fatherPin"] in h61["father"]
        and "P86" in json.dumps(h61["notes"], ensure_ascii=False)
        and h63["houseNo"] == "63"
        and H63_ROW["fatherPin"] in h63["father"]
        and "1890" in json.dumps(h63["notes"], ensure_ascii=False)
        and h1["houseNo"] == "1"
        and H1_ROW["fatherPin"] in h1["father"]
        and "1888" in json.dumps(h1["notes"], ensure_ascii=False)
        and h32["houseNo"] == "32"
        and H32_ROW["fatherPin"] in h32["father"]
        and "1890" in json.dumps(h32["notes"], ensure_ascii=False)
        and h90["houseNo"] == "90"
        and H90_ROW["fatherPin"] in h90["father"]
        and "ŠOLSKA" in json.dumps(h90["notes"], ensure_ascii=False)
        and h24["houseNo"] == "24"
        and H24_ROW["fatherPin"] in h24["father"]
        and "MENJAVA GOSPODINJSTVA" in json.dumps(h24["notes"], ensure_ascii=False)
        and h27["houseNo"] == "27"
        and H27_ROW["fatherPin"] in h27["father"]
        and "MENJAVA GOSPODINJSTVA" in json.dumps(h27["notes"], ensure_ascii=False)
    )

    # I8 — čez-letne kontinuitete prek dokazov: h58 (P85 1890 Požek × Dragoš);
    # h61 (P86 1891 Požek × Dragos — ISTI vzorec brez botre/podpisa); h63
    # (P85 1890 Križan + P84 1889 Hrigian?); h32 (P85 1890 Urh + P84 1889);
    # h1 (P83 1888 Zeljth × Kure); h29 (P83 1888 Milek × Križan); h90
    # (P85 1890 Kopitar × Schweiger); h24 (P85 1890 anomalija Brinec);
    # h27 (P82 1887 Kukar)
    p83 = json.load(open(DOKAZ_P83, encoding="utf-8"))
    p84 = json.load(open("research/issue17/parish-baptism-1889.json", encoding="utf-8"))
    p85 = json.load(open(DOKAZ_P85, encoding="utf-8"))
    p86 = json.load(open(DOKAZ_P86, encoding="utf-8"))
    p85_h58 = [e for e in p85["entries"] if e.get("houseNo") == "58"]
    p86_h61 = [e for e in p86["entries"] if e.get("houseNo") == "61"]
    p85_h63 = [e for e in p85["entries"] if e.get("houseNo") == "63"]
    p84_h63 = [e for e in p84["entries"] if e.get("houseNo") == "63"]
    p85_h32 = [e for e in p85["entries"] if e.get("houseNo") == "32"]
    p84_h32 = [e for e in p84["entries"] if e.get("houseNo") == "32"]
    p83_h1 = [e for e in p83["entries"] if e.get("houseNo") == "1"]
    p83_h29 = [e for e in p83["entries"] if e.get("houseNo") == "29"]
    p85_h90 = [e for e in p85["entries"] if e.get("houseNo") == "90"]
    p85_h24 = [e for e in p85["entries"] if e.get("houseNo") == "24"]
    p82 = json.load(open("research/issue17/parish-baptism-1887.json", encoding="utf-8"))
    p82_h27 = [e for e in p82["entries"] if e.get("houseNo") == "27"]
    inv["I8_crossyear_continuity"] = (
        len(p85_h58) == 1
        and "Požek" in p85_h58[0]["father"]
        and "Dragoš" in p85_h58[0]["mother"]
        and "Požek" in h58["father"]
        and "Dragos" in h58["mother"]
        and len(p86_h61) == 1
        and "Požek" in p86_h61[0]["father"]
        and "Dragos" in p86_h61[0]["mother"]
        and p86_h61[0]["botra"] in (None, "—")
        and p86_h61[0]["priest"] in (None, "—")
        and h61["botra"] is None
        and h61["priest"] is None
        and "Požek" in h61["father"]
        and "Dragos" in h61["mother"]
        and len(p85_h63) == 1
        and "Križan" in p85_h63[0]["father"]
        and len(p84_h63) == 1
        and ("Hrigian" in p84_h63[0]["father"] or "Hrižan" in p84_h63[0]["father"])
        and ("Hrižan" in h63["father"] or "Križan" in h63["father"])
        and len(p85_h32) == 1
        and "Urh" in p85_h32[0]["father"]
        and len(p84_h32) == 1
        and "Urh" in p84_h32[0]["father"]
        and "Urh" in h32["father"]
        and len(p83_h1) == 1
        and "Zeljth" in p83_h1[0]["father"]
        and "Kure" in p83_h1[0]["mother"]
        and "Željko" in h1["father"]
        and "Kure" in h1["mother"]
        and len(p83_h29) == 1
        and "Milek" in p83_h29[0]["father"]
        and "Križan" in p83_h29[0]["mother"]
        and "Milek" in next(e for e in entries if e["row"] == 11)["father"]
        and "Križan" in next(e for e in entries if e["row"] == 11)["mother"]
        and len(p85_h90) == 1
        and "Kopitar" in p85_h90[0]["father"]
        and ("Kopitac" in h90["father"] or "Kopitar" in h90["father"])
        and len(p85_h24) == 1
        and "ANOMALIJA" in p85_h24[0]["father"]
        and "Brinec" in p85_h24[0]["father"]
        and len(p82_h27) == 1
        and "Kukar" in p82_h27[0]["father"]
    )

    # I9 — runtime projekcija: HOUSE_VITALS 1892 == 12 zasidranih (sk. 56–62,
    # page == sken−1); skupaj 133; brez »Hraus« v aktivnih whatSi poljih
    vitals_1892 = parish_vitals(BOOK_SIGNATURE, 1892)
    hv_houses = sorted((v["houseNo"] for v in vitals_1892), key=int)
    src = open(PARISH_TS, encoding="utf-8").read()
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    active_hraus = [
        w for w in re.findall(r"whatSi:\s*\"([^\"]+)\"", src)
        if "Hraus" in w and "re-read" not in w and "prej" not in w
    ]
    inv["I9_runtime_projection"] = (
        len(vitals_1892) == EXPECTED_HOUSES_VITALS
        and sorted(set(hv_houses), key=int) == sorted(houses, key=int)
        and all(v["scan"] and 56 <= v["scan"] <= 62 and v["page"] == v["scan"] - 1
                for v in vitals_1892)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
        and not active_hraus
    )

    # I10 — statistika dokaza == neodvisen preracun: 9 ponovitev + 3 novi
    # (12, 73, 75); sampleTotal po konvenciji verige P82–P86 (zasidrani +
    # evidence-only); edina imenovana evidence-only ostaja P85 »65 [~]«;
    # klasifikacija v P87 vesolju — brez P88/P89 razširitev (1893/1894 blokov
    # ne morejo spreminjati zgodovinske klasifikacije leta 1892 — h12/h73/h75
    # so 1894 ponovitve, toda za P87 dokaz ostajajo nove)
    vitals_pre88 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900))
    ]
    repeat_houses = [h for h in houses if any(
        v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1892
        or v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE
        for v in vitals_pre88
    )]
    new_houses = sorted(houses - set(repeat_houses), key=int)
    n_entries_total = len(vitals_all)
    n_houses_total = len({v["houseNo"] for v in vitals_all})
    p85_ev_named = [e["houseNo"] for e in p85["entries"]
                    if e.get("houseNo") is not None and e.get("row") in (31, 75, 77)]
    inv["I10_stats_independent"] = (
        len(repeat_houses) == dokaz["stats"]["repeatHouses"] == EXPECTED_REPEATS
        and new_houses == dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 260  # kumulativno po P95 (254 + 6)
        and n_houses_total == 79  # P94: 78; P95: + 1 (67)
        and p85_ev_named == ["65 [~]"]
        and dokaz["stats"]["sampleTotal"] == "139 vpisov / 61 hiš čez tri knjige (04105 + 04894 + 04455) in sedem let (1886/1887/1888/1889/1890/1891/1892)"
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
    )

    ok = all(inv.values())
    print("P87 — krstna knjiga 04105, polno leto 1892 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {cited}")
    print(f"vpisi {len(entries)} / hiše {len(houses)} + {len(ev_only)} neberljive;"
          f" PT {len(inset)}/{len(gap)}; vitals 1892 = {len(vitals_1892)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
