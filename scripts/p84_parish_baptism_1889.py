#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P84 — župnija Podzemelj: krstna knjiga 04105, polno leto 1889 (issue #18).

Razširitev vzorca P79 (1886) → P82 (1887) → P83 (1888) na leto 1889: skeni
35–43 == strani 34–42 (stran == sken − 1) — vsi vpisi z Griblji + dokaz
preloma 1890 (»Leto 1890« na strani 42, row 1). NOVELI P84: ① ŠTEVILČENJE
STR. 40 — duhovnikove oznake vrstic PONOVLJENE 68–8x (napaka), modri
svinčnik popravi z zvezno 81–93 v datumskih celicah (str. 41 nadaljuje
94–106 — neodvisna potrditev); ② RE-READ P83 — »HRAUS/HRAUCELJ« je
STRAUŠ/STRAUCELJ (Kurrent ſt brana kot H; familija JE v vesolju 1825,
P81 0.8571) — P83 podatki popavljeni vidno. Paleografska faza ročna
(skeni v delovnem imeniku, NI v repu); ta skripta je DETERMINISTIČNI
VERIFIKATOR (brez AI ob delovanju): live HTTP preveri knjigo + citirane
skene, dokaz preveri proti PARISH_BOOKS/CHAIN pinom, PT klasifikaciji
(luknja 41–60: 58 NOVA, 59/57 potrditvi), sidrom (h63 Šimec=ATLAS,
row 82 Filak babica, row 89 Dragoš botr, h72 Strauš re-read), re-readu
P83 (brez »Hraus« v očetovskih/materevnih poljih P83 dokaza) in runtime
projekciji (HOUSE_VITALS v src/data/atlas/parish.ts).

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
DOKAZ = "research/issue17/parish-baptism-1889.json"
DOKAZ_P83 = "research/issue17/parish-baptism-1888.json"
PACK_P81 = "research/issue17/parish-name-linkage.json"
PARISH_TS = "src/data/atlas/parish.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (35, 43)          # skeni 35–43 == strani 34–42 (okvir leta 1889)
ENTRY_SCANS = (35, 42)          # vpisi: skeni 35–42 (str. 34–41)
FRAME_PAGES = (34, 42)
BREAK_1890 = {"scan": 43, "page": 42, "row": 1}
EXPECTED_ENTRIES = 19
EXPECTED_DISTINCT = 16          # imenovane hiše (2 neberljive izključene)
ILLEGIBLE_ROWS = (70, 82)       # hišne št. neberljive (row 70 »///«; row 82 prekrita)
EXPECTED_PT_IN_SET = {"2", "3", "8", "26", "32", "33", "35", "63", "64", "65", "69", "72", "83"}
EXPECTED_PT_GAP = {"57", "58", "59"}
PT_GAP_NEW = ["58"]
EXPECTED_HOUSES_VITALS = 17     # 19 vpisov − 2 neberljivi (runtime projekcija)
# sidra/pins P84:
H63_ROW = {"row": 53, "scan": 38, "child": "Barbara", "botraPin": "Janez Šimec"}
R82_FILAK = {"row": 82, "scan": 41, "babicaPin": "Ana Filak"}
R89_DRAGOS = {"row": 89, "scan": 41, "botraPin": "Janez Dragoš", "houseNo": "8"}
H72_STRAUS = {"row": 64, "scan": 39, "fatherPin": "Matija Strauš"}
R33_ILLEGIT = {"row": 33, "houseNo": "59"}


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

    # I3 — citirani skeni ⊆ okvir 35–42 + JPEG probe (str. 34 = sk. 35: rows 1–14,
    # 1 Griblje; str. 42 = sk. 43: prelom 1890 — citirana kot prelom)
    by_name = {u.split("/")[-1]: u for u in urls}
    cited = sorted({e["scan"] for e in entries})
    ok3 = all(ENTRY_SCANS[0] <= n <= ENTRY_SCANS[1] for n in cited) and len(cited) >= 7
    probes = {}
    for n in cited:
        name = f"R%20Podzemelj%201886-1919-{n:04d}.jpg"
        u = by_name.get(name)
        p = probe_jpeg(u) if u else {"http": 0, "jpeg": False, "bytes": 0}
        probes[n] = p
        ok3 = ok3 and p["http"] == 200 and p["jpeg"]
    inv["I3_cited_scans_jpeg"] = ok3

    # I4 — okvir: vsi vpisi 1889, skeni 35–42, stran == sken − 1; prelom 1890
    # (str. 42, row 1) + NOVELA številčenja str. 40 (ponovljene oznake 68–8x,
    # svinčnik 81–93; str. 41 zvezno 94–106) + rowsTotal 106
    ok4 = all(
        e["year"] == 1889 and ENTRY_SCANS[0] <= e["scan"] <= ENTRY_SCANS[1]
        and e["page"] == e["scan"] - 1 and FRAME_PAGES[0] <= e["page"] <= FRAME_PAGES[1]
        for e in entries
    )
    ok4 = ok4 and dokaz["frame"]["scanFrom"] == 35 and dokaz["frame"]["scanTo"] == 43
    ok4 = ok4 and dokaz["frame"]["break1890"]["scan"] == BREAK_1890["scan"]
    ok4 = ok4 and dokaz["frame"]["break1890"]["page"] == BREAK_1890["page"]
    ok4 = ok4 and dokaz["frame"]["break1890"]["row"] == BREAK_1890["row"]
    ok4 = ok4 and dokaz["frame"]["rowsTotal"] == 106
    rn = dokaz["frame"]["rowNumberingNovela"]
    ok4 = ok4 and "68–8x" in rn["page40"] and "81–93" in rn["page40"]
    ok4 = ok4 and "94–106" in rn["page41Confirm"]
    inv["I4_frame_break_numbering"] = ok4

    # I5 — merila issue #18: ≥ 5 hiš; 19 vpisov / 16 imenovanih hiš + 2 neberljivi
    named = [e for e in entries if e["houseNo"] is not None]
    illegible = [e for e in entries if e["houseNo"] is None]
    houses = [e["houseNo"] for e in named]
    inv["I5_houses"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(set(houses)) == EXPECTED_DISTINCT
        and len(illegible) == 2
        and sorted(r["row"] for r in illegible) == sorted(ILLEGIBLE_ROWS)
        and len(set(houses)) >= 5
    )

    # I6 — PT usklajenost (klasifikacija iz verige PT 1825; luknja 41–60: 58 NOVA)
    pt = pt_house_set()
    in_set = sorted({h for h in set(houses) if h in pt}, key=int)
    gap = sorted({h for h in set(houses) if h not in pt}, key=int)
    inv["I6_pt_consistency"] = (
        set(in_set) == EXPECTED_PT_IN_SET and set(gap) == EXPECTED_PT_GAP
        and all(41 <= int(h) <= 60 for h in gap)
        and dokaz["stats"]["ptGapNew"] == PT_GAP_NEW
    )

    # I7 — celovitost polj (houseNo sme biti null LE pri neberljivih vrsticah)
    req = ("row", "year", "month", "born", "village", "scan", "page",
           "child", "father", "mother", "whatSi", "whatEn")
    ok7 = all(all(e.get(k) not in (None, "") for k in req) for e in entries)
    ok7 = ok7 and all(e["village"] == "Griblje" for e in entries)
    ok7 = ok7 and all(
        e["houseNo"] is not None for e in entries if e["row"] not in ILLEGIBLE_ROWS
    )
    ok7 = ok7 and all("Matricula" in dokaz["source"]["book"] or
                      dokaz["source"]["url"].startswith("https://data.matricula")
                      for _ in [0])
    inv["I7_entries_complete"] = ok7

    # I8 — sidra P84: h63 (botr Janez Šimec = ATLAS 1825), row 82 (babica Ana
    # Filak = P81 1.0), row 89 (botr Janez Dragoš = P81 1.0), h72 (re-read Strauš)
    h63 = [e for e in entries if e["houseNo"] == "63" and e["row"] == H63_ROW["row"]
           and e["scan"] == H63_ROW["scan"] and e["child"] == H63_ROW["child"]
           and H63_ROW["botraPin"] in e["botra"]]
    r82 = [e for e in entries if e["row"] == R82_FILAK["row"] and e["scan"] == R82_FILAK["scan"]
           and R82_FILAK["babicaPin"] in e["babica"]]
    r89 = [e for e in entries if e["row"] == R89_DRAGOS["row"] and e["scan"] == R89_DRAGOS["scan"]
           and R89_DRAGOS["botraPin"] in e["botra"] and e["houseNo"] == R89_DRAGOS["houseNo"]]
    h72 = [e for e in entries if e["houseNo"] == "72" and e["row"] == H72_STRAUS["row"]
           and H72_STRAUS["fatherPin"] in e["father"]
           and any("RE-READ" in n for n in e["notes"])]
    ok8 = len(h63) == 1 and len(r82) == 1 and len(r89) == 1 and len(h72) == 1
    inv["I8_anchors_63_82_89_72"] = ok8

    # I9 — križne povezave: ① ATLAS/PT Šimec @63 (P81 pack) ↔ P84 botr row 53;
    # ② RE-READ P83: v P83 dokazu NI več »Hraus« v starševskih poljih, h72 P84
    # nosi RE-READ noto; ③ h64 ×2 (multi-vpisna); ④ nezakonski 1 (row 33, h59);
    # ⑤ ponovitve prek runtime vitals (h2/h8/h26/h63/h65/h83/h69/h72/h35/h57/h59)
    pack = json.load(open(PACK_P81, encoding="utf-8"))
    names = pack["universe1825"]["names"]
    chain63 = [n for n in names if n.get("src") == "chain" and n.get("house") == "63"]
    atlas63 = [n for n in names if n.get("src") == "atlas" and "63" in (n.get("house") or [])]
    ok9 = len(chain63) == 1 and "Šimec" in chain63[0]["name"]
    ok9 = ok9 and len(atlas63) == 1 and "Schimek" in atlas63[0]["name"]
    ok9 = ok9 and "Janez Šimec" in h63[0]["botra"]

    p83 = json.load(open(DOKAZ_P83, encoding="utf-8"))
    p83_parent_fields = []
    for e in p83["entries"]:
        p83_parent_fields += [e.get("father") or "", e.get("mother") or ""]
    # aktivna branja brez re-read pripombe »(P84 RE-READ: prej »Hraus« …)«
    active = [f.split("(P84 RE-READ")[0] for f in p83_parent_fields]
    ok9 = ok9 and not any("Hraus" in f for f in active)
    ok9 = ok9 and any("Strauš" in f for f in active)
    ok9 = ok9 and "reRead" in p83 and p83["reRead"]["by"].startswith("P84")

    h64 = [e for e in entries if e["houseNo"] == "64"]
    ok9 = ok9 and len(h64) == 2 and {e["row"] for e in h64} == {24, 60}

    r33 = [e for e in entries if e["row"] == R33_ILLEGIT["row"]]
    ok9 = ok9 and len(r33) == 1 and r33[0]["houseNo"] == R33_ILLEGIT["houseNo"] \
        and "PRAZEN" in r33[0]["father"] and dokaz["stats"]["illegitimate"] == 1

    vit_89 = parish_vitals("04105", 1889)
    ok9 = ok9 and len(vit_89) == EXPECTED_HOUSES_VITALS
    for hn, yr, sig in (("2", 1887, "04105"), ("8", 1888, "04105"), ("26", 1887, "04105"),
                        ("63", 1887, "04105"), ("65", 1887, "04105"), ("83", 1888, "04105"),
                        ("69", 1888, "04105"), ("72", 1888, "04105"), ("35", 1887, "04105"),
                        ("57", 1888, "04105"), ("59", 1886, "04894")):
        ok9 = ok9 and any(v["houseNo"] == hn and v["year"] == yr
                          for v in parish_vitals(sig, yr))
    inv["I9_cross_links"] = ok9

    # I10 — runtime projekcija: 17 zasidranih vpisov v HOUSE_VITALS (year 1889,
    # houseNo/scan ujemanje); 2 neberljivi izključeni (evidence-only)
    missing = []
    for e in named:
        hit = [v for v in vit_89 if v["houseNo"] == e["houseNo"] and v["scan"] == e["scan"]]
        if not hit:
            missing.append((e["row"], e["houseNo"]))
    inv["I10_runtime_projection"] = not missing and len(vit_89) == EXPECTED_HOUSES_VITALS

    return dokaz, inv, probes, len(urls), in_set, gap, missing


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    dokaz, inv, probes, n_images, in_set, gap, missing = verify()
    all_ok = all(inv.values())
    print(f"P84 --check: {DOKAZ}")
    detail = " ".join(f"{k}={'P' if v else 'F'}" for k, v in inv.items())
    print(f"invarianti: {all_ok} — {detail}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {n_images} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {sorted({e['scan'] for e in dokaz['entries']})}")
    print(f"PT usklajenost: v naboru {in_set} | luknja 41–60 {gap} (NOVA: {PT_GAP_NEW})")
    if missing:
        print(f"manjkajoče projekcije: {missing}")
    if mode == "--check":
        print("P84 --check: PASS" if all_ok else "P84 --check: FAIL")
        sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
