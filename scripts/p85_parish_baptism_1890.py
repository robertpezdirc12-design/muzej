#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P85 — župnija Podzemelj: krstna knjiga 04105, polno leto 1890 (issue #18).

Razširitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) na leto
1890: skeni 43–49 == strani 42–48 (stran == sken − 1) — vsi vpisi z Griblji +
dokaz preloma 1891 (velike cifre »1891.« na strani 48, row 1 po row 86). LE
OKVIR — leta 1887/1888/1889 imajo svoje skripte p82/p83/p84 (vzorec 1886 ∪
1897 + sidri 61/78 ostaja v p80 I7). NOVELA P85: STATUS = ULOMEK — Kurrent
znak pred »zemljak« (P79–P84 brana »ž zemljaf«) je z jasnimi izrezi 1890
ulomek ½ (ali ¼) — 15/24 vpisov; isti znak kot P84 row 3 »¼ zemljišč«.
Paleografska faza ročna (skeni v delovnem imeniku /tmp/p85, NI v repu); ta
skripta je DETERMINISTIČNI VERIFIKATOR (brez AI ob delovanju): live HTTP
preveri knjigo + citirane skene, dokaz preveri proti PARISH_BOOKS/CHAIN
pinom, PT klasifikaciji (luknja 41–60: 41 NOVA z 2 vpisoma, 47/55/58
potrditvi), sidrom (h77 Požek bajtar = P83 h79, h71 Strauš oče = PUA @71,
h63 Križan na Šimec ATLAS sidru, h55 Šimec na luknji), dvojčkom (h30 ×2),
multi-vpisni h41 (dve družini), anomalijama (h24 + h35 == P82 row 93
čez-letno), ponovitvam prek vitals in runtime projekciji (HOUSE_VITALS v
src/data/atlas/parish.ts).

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
DOKAZ = "research/issue17/parish-baptism-1890.json"
DOKAZ_P82 = "research/issue17/parish-baptism-1887.json"
PARISH_TS = "src/data/atlas/parish.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (43, 49)          # skeni 43–49 == strani 42–48 (okvir leta 1890)
ENTRY_SCANS = (43, 49)          # vpisi: skeni 43–49 (str. 42–48; prelom na 49)
FRAME_PAGES = (42, 48)
BREAK_1891 = {"scan": 49, "page": 48, "row": 1}
EXPECTED_ENTRIES = 24
EXPECTED_DISTINCT = 19          # imenovane hiše (3 evidence-only izključene)
ILLEGIBLE_ROWS = (31, 75, 77)   # hišne št. neberljive (r31/r75 prekriti; r77 rez)
EXPECTED_PT_IN_SET = {"7", "11", "15", "24", "27", "30", "31", "32", "35", "38", "63", "69", "71", "77", "90"}
EXPECTED_PT_GAP = {"41", "47", "55", "58"}
PT_GAP_NEW = ["41"]
EXPECTED_HOUSES_VITALS = 21     # 24 vpisov − 3 evidence-only (runtime projekcija)
EXPECTED_VITALS_TOTAL = 193     # HOUSE_VITALS 91 + 21 (p80 I7 pin); P86: + 9 (1891); P87: + 12 (1892); P88: + 17 (1893); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896)
# sidra/pins P85:
H77_ROW = {"row": 47, "scan": 46, "fatherPin": "Jurij Pošek", "status": "bajtar"}
H71_ROW = {"row": 23, "scan": 44, "fatherPin": "Jurij Straus"}
H63_ROW = {"row": 76, "scan": 48, "fatherPin": "Nikolaj Križan"}
H55_ROW = {"row": 66, "scan": 48, "fatherPin": "Nikolaj Šimec"}
H35_ANOMALY = {"row": 85, "scan": 49, "fatherPin": "Marija Hrižan"}
H24_ANOMALY = {"row": 19, "scan": 44, "fatherPin": "Marija Brinec"}
TWIN_HOUSE = "30"               # rows 51+52 — dvojčka (isti sken 46)
MULTI_HOUSE = "41"              # rows 71+72 — dve različni družini (isti sken 48)


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
    """JSON 'files': ['/image/<base64>/', ...] → hosted URL seznam."""
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
    """Izvleči (houseNo, year, scan, page) za vpise dane signature iz parish.ts."""
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

    # I3 — citirani skeni ⊆ okvir 43–49 + JPEG probe (str. 42 = sk. 43: rows 1–12,
    # 1 Griblje; str. 48 = sk. 49: prelom 1891 — citirana kot prelom)
    cited = sorted({e["scan"] for e in entries})
    inv["I3_cited_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and cited == list(range(43, 50))
    probes = {s: probe_jpeg(urls[s - 1]) for s in cited} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())

    # I4 — okvir: vsi vpisi 1890, skeni 43–49, stran == sken − 1; prelom 1891
    rows = [e["row"] for e in entries]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1890 for e in entries)
        and all(e["scan"] - 1 == e["page"] for e in entries)
        and all(FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1] for e in entries)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and dokaz["frame"]["break1891"]["scan"] == BREAK_1891["scan"]
        and dokaz["frame"]["break1891"]["page"] == BREAK_1891["page"]
        and dokaz["frame"]["rowsTotal"] == 86
    )

    # I5 — števec: 24 vpisov / 19 hiš + 3 neberljive (evidence-only po row)
    ev_only = [e for e in entries if e["row"] in ILLEGIBLE_ROWS]
    named = [e for e in entries if e["row"] not in ILLEGIBLE_ROWS]
    houses = {e["houseNo"] for e in named}
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"] == "Griblje" for e in entries)
        and all(e["houseNo"] in (None, "65 [~]") for e in ev_only)
        and len(houses) == EXPECTED_DISTINCT
        and len(ev_only) == len(ILLEGIBLE_ROWS)
        and {e["row"] for e in ev_only} == set(ILLEGIBLE_ROWS)
    )

    # I6 — PT klasifikacija: 15 v naboru + 4 v luknji (41 NOVA, 47/55/58 potrditvi)
    pts = pt_house_set()
    inset = sorted((h for h in houses if h in pts), key=int)
    gap = sorted((h for h in houses if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGapNew"] == PT_GAP_NEW
        and dokaz["stats"]["newSampleHouses"] == ["7", "30", "38", "41", "77", "90"]
    )

    # I7 — sidra (h77 Požek bajtar = P83 h79; h71 Strauš = PUA @71; h63 Križan;
    # h55 Šimec; anomaliji h24 + h35 == P82 row 93)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    h77 = e_by_row(H77_ROW["row"])
    h71 = e_by_row(H71_ROW["row"])
    h63 = e_by_row(H63_ROW["row"])
    h55 = e_by_row(H55_ROW["row"])
    h35 = e_by_row(H35_ANOMALY["row"])
    h24 = e_by_row(H24_ANOMALY["row"])
    inv["I7_anchors"] = (
        h77["houseNo"] == "77"
        and H77_ROW["fatherPin"] in h77["father"]
        and H77_ROW["status"] in h77["father"]
        and "P83" in json.dumps(h77["notes"], ensure_ascii=False)
        and h71["houseNo"] == "71"
        and H71_ROW["fatherPin"] in h71["father"]
        and "PUA" in json.dumps(h71["notes"], ensure_ascii=False)
        and h63["houseNo"] == "63"
        and H63_ROW["fatherPin"] in h63["father"]
        and h55["houseNo"] == "55"
        and H55_ROW["fatherPin"] in h55["father"]
        and h35["houseNo"] == "35"
        and H35_ANOMALY["fatherPin"] in h35["father"]
        and h24["houseNo"] == "24"
        and H24_ANOMALY["fatherPin"] in h24["father"]
        and "P82 row 93" in json.dumps(h35["notes"], ensure_ascii=False)
        and h35["child"].startswith("N. moškega")
    )

    # I8 — dvojčka h30 (rows 51+52, isti sken, isti oče) + multi h41 (rows
    # 71+72, dve družini) + čez-letna anomalija h35 == P82 row 93 (ista hiša,
    # isti par imen: Marija Hrižan × Ana Požek, 1887 IN 1890)
    twins = [e for e in named if e["houseNo"] == TWIN_HOUSE]
    multi = [e for e in named if e["houseNo"] == MULTI_HOUSE]
    p82 = json.load(open(DOKAZ_P82, encoding="utf-8"))
    p82_h35 = [e for e in p82["entries"] if e.get("houseNo") == "35"]
    tw_norm = lambda s: re.sub(r"\s*\(skupna celica[^)]*\)", "", s)  # noqa: E731
    inv["I8_twins_multi_crossyear"] = (
        len(twins) == 2
        and {e["row"] for e in twins} == {51, 52}
        and len({e["scan"] for e in twins}) == 1
        and tw_norm(twins[0]["father"]) == tw_norm(twins[1]["father"])
        and len(multi) == 2
        and {e["row"] for e in multi} == {71, 72}
        and multi[0]["father"] != multi[1]["father"]
        and len(p82_h35) == 1
        and "Marija Hrižan" in p82_h35[0]["father"]
        and "Marija Hrižan" in h35["father"]
        and "Ana Požek" in p82_h35[0]["mother"]
        and "Ana Požek" in h35["mother"]
    )

    # I9 — runtime projekcija: HOUSE_VITALS 1890 == 21 zasidranih (sk. 43–49,
    # page == sken−1); skupaj 112; brez »Hraus« v aktivnih whatSi poljih
    # (re-read pripombe dovoljene — vzorec I9 p84); h41 dva različna očeta
    vitals_1890 = parish_vitals(BOOK_SIGNATURE, 1890)
    hv_houses = sorted((v["houseNo"] for v in vitals_1890), key=int)
    src = open(PARISH_TS, encoding="utf-8").read()
    blocks_41 = re.findall(r"\{[^{}]*?houseNo:\s*\"41\"[^{}]*?\}", src, re.S)
    blocks_41_1890 = [b for b in blocks_41 if "year: 1890" in b]
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    active_hraus = [
        w for w in re.findall(r"whatSi:\s*\"([^\"]+)\"", src)
        if "Hraus" in w and "re-read" not in w and "prej" not in w
    ]
    inv["I9_runtime_projection"] = (
        len(vitals_1890) == EXPECTED_HOUSES_VITALS
        and sorted(set(hv_houses), key=int) == sorted(houses, key=int)
        and all(v["scan"] and 43 <= v["scan"] <= 49 and v["page"] == v["scan"] - 1
                for v in vitals_1890)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
        and len(blocks_41_1890) == 2
        and all("Muc" in b or "Hrušič" in b for b in blocks_41_1890)
        and not active_hraus
    )

    # I10 — statistika dokaza == neodvisen preracun: 13 ponovitev + 6 novih;
    # sampleTotal po konvenciji verige P82–P84 (zasidrani + evidence-only;
    # hišne korekcijske dvojice 52/15 + 75/78 štejeta ločeno)
    # klasifikacija v P85 vesolju — brez P86/P87/P88/P89 razširitev (1891/1892/1893/1894 blokov
    # ne morejo spreminjati zgodovinske new/repeat klasifikacije leta 1890;
    # h30 je 1891 ponovitev, toda za P85 dokaz ostaja nova; h90 je 1892
    # ponovitev, toda za P85 dokaz ostaja nova)
    vitals_pre86 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1891, 1892, 1893, 1894, 1895, 1896))
    ]
    repeat_houses = [h for h in houses if any(
        v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1890
        or v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE
        for v in vitals_pre86
    )]
    new_houses = sorted(houses - set(repeat_houses), key=int)
    n_entries_total = len(vitals_all)
    n_houses_total = len({v["houseNo"] for v in vitals_all})
    ev_only_total = 6  # P84: 2; P85: 3; P86: r52 (1)
    inv["I10_stats_independent"] = (
        len(repeat_houses) == dokaz["stats"]["repeatHouses"] == 13
        and new_houses == dokaz["stats"]["newSampleHouses"]
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + ev_only_total == 199  # kumulativno po P91 (193 + 6)
        and n_houses_total == 70  # P90: 67; P91: + 3 (9, 14, 45)
        and dokaz["stats"]["sampleTotal"] == "117 vpisov / 56 hiš čez tri knjige (04105 + 04894 + 04455) in pet let (1886/1887/1888/1889/1890)"  # zgodovinski P85 dokaz
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 3
    )

    ok = all(inv.values())
    print("P85 — krstna knjiga 04105, polno leto 1890 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {cited}")
    vitals_all_n = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    print(f"vpisi {len(entries)} / hiše {len(houses)} + {len(ev_only)} neberljive;"
          f" PT {len(inset)}/{len(gap)}; vitals 1890 = {len(vitals_1890)};"
          f" vitals vseh treh knjig = {len(vitals_all_n)} (pričakovano {EXPECTED_VITALS_TOTAL})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
