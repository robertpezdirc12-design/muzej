#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P83 — župnija Podzemelj: krstna knjiga 04105, polno leto 1888 (issue #18).

Razširitev vzorca P79 (1886) → P82 (1887) na leto 1888: skeni 27–35 == strani
26–34 (stran == sken − 1) — vsi vpisi z Griblji + dokaz preloma 1889 (»1 8 8 9«
na strani 34, row 1). NOVO POGlavJE P83: pisane oznake vrstic se pri prelomu
leta ponastavijo na 1 (str. 27 se začne z oznako 3; P82 »row 107« = zvezno
štetje 106+1). Paleografska faza ročna (skeni v delovnem imeniku, NI v repu);
ta skripta je DETERMINISTIČNI VERIFIKATOR (brez AI ob delovanju): live HTTP
preveri knjigo + citirane skene, dokaz preveri proti PARISH_BOOKS/CHAIN pinom,
PT klasifikaciji (luknja 41–60: potrjitve 44/56/57), sidrom (h13 veriga,
h78 oskrbar, h29 Milek) in runtime projekciji (HOUSE_VITALS v
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
DOKAZ = "research/issue17/parish-baptism-1888.json"
PARISH_TS = "src/data/atlas/parish.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (27, 35)          # skeni 27–35 == strani 26–34 (okvir leta 1888)
ENTRY_SCANS = (28, 34)          # vpisi: skeni 28–34 (str. 27–33)
FRAME_PAGES = (26, 34)
BREAK_1889 = {"scan": 35, "page": 34, "row": 1}
EXPECTED_HOUSES = 15
EXPECTED_ENTRIES = 15
EXPECTED_PT_IN_SET = {"1", "8", "13", "21", "24", "29", "69", "72", "78", "79", "83", "85"}
EXPECTED_PT_GAP = {"44", "56", "57"}
# sidra/pins P83:
H13_ROW = {"row": 53, "scan": 31, "child": "Barbara", "fatherPin": "Jakobič"}
H78_OSKRBAR_ROW = {"row": 24, "scan": 29, "pin": "oskrbar"}
H29_MILEK_ROW = {"row": 85, "scan": 34, "fatherPin": "Milek", "epidemija": "1886"}
ROW_RESTART = {"page27FirstRow": 3, "break1889Row": 1}
ILLEGIT_HOUSES = ("24", "56", "21")


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


def parish_vitals(signature):
    """Izvleči (houseNo, year, scan, page) za vse vpise dane signature iz parish.ts."""
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
        })
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

    # I3 — citirani skeni ⊆ okvir 27–35 + JPEG probe (str. 26 = sk. 27: rows 1–2
    # Gradac, brez Gribljev; str. 34 = sk. 35: prelom 1889 — citirana kot prelom)
    by_name = {u.split("/")[-1]: u for u in urls}
    cited = sorted({e["scan"] for e in entries})
    ok3 = all(ENTRY_SCANS[0] <= n <= ENTRY_SCANS[1] for n in cited) and len(cited) >= 6
    probes = {}
    for n in cited:
        name = f"R%20Podzemelj%201886-1919-{n:04d}.jpg"
        u = by_name.get(name)
        p = probe_jpeg(u) if u else {"http": 0, "jpeg": False, "bytes": 0}
        probes[n] = p
        ok3 = ok3 and p["http"] == 200 and p["jpeg"]
    inv["I3_cited_scans_jpeg"] = ok3

    # I4 — okvir: vsi vpisi 1888, skeni 28–34, stran == sken − 1; prelom 1889
    # (str. 34, row 1) + PONASTAVITEV ŠTEVILČENJA (str. 27 = oznaka 3)
    ok4 = all(
        e["year"] == 1888 and ENTRY_SCANS[0] <= e["scan"] <= ENTRY_SCANS[1]
        and e["page"] == e["scan"] - 1 and FRAME_PAGES[0] <= e["page"] <= FRAME_PAGES[1]
        for e in entries
    )
    ok4 = ok4 and dokaz["frame"]["scanFrom"] == 27 and dokaz["frame"]["scanTo"] == 35
    ok4 = ok4 and dokaz["frame"]["break1889"]["scan"] == BREAK_1889["scan"]
    ok4 = ok4 and dokaz["frame"]["break1889"]["page"] == BREAK_1889["page"]
    ok4 = ok4 and dokaz["frame"]["break1889"]["row"] == BREAK_1889["row"]
    ok4 = ok4 and dokaz["frame"]["rowsTotal"] == 92
    rr = dokaz["frame"]["rowRestart1888"]
    ok4 = ok4 and "str. 27" in rr["proof"] and "106+1" in rr["p82ReRead"]
    inv["I4_frame_break_restart"] = ok4

    # I5 — merila issue #18: ≥ 5 hiš; pričakovano 15 vpisov / 15 različnih hiš
    houses = [e["houseNo"] for e in entries]
    inv["I5_houses"] = len(set(houses)) == EXPECTED_HOUSES and len(entries) == EXPECTED_ENTRIES
    inv["I5_houses"] = inv["I5_houses"] and len(set(houses)) >= 5

    # I6 — PT usklajenost (klasifikacija iz verige PT 1825; luknja 41–60)
    pt = pt_house_set()
    in_set = sorted({h for h in set(houses) if h in pt}, key=int)
    gap = sorted({h for h in set(houses) if h not in pt}, key=int)
    inv["I6_pt_consistency"] = (
        set(in_set) == EXPECTED_PT_IN_SET and set(gap) == EXPECTED_PT_GAP
        and all(41 <= int(h) <= 60 for h in gap)
        and dokaz["stats"]["ptGapNew"] == []
    )

    # I7 — celovitost polj
    req = ("row", "year", "month", "born", "village", "houseNo", "scan", "page",
           "child", "father", "mother", "whatSi", "whatEn")
    ok7 = all(all(e.get(k) not in (None, "") for k in req) for e in entries)
    ok7 = ok7 and all(e["village"] == "Griblje" for e in entries)
    ok7 = ok7 and all("Matricula" in dokaz["source"]["book"] or
                      dokaz["source"]["url"].startswith("https://data.matricula")
                      for _ in [0])
    inv["I7_entries_complete"] = ok7

    # I8 — sidra P83: hiša 13 (prva per-hišna imenska veriga, row 53),
    # hiša 78 OSKRBAR (row 24), hiša 29 Milek (row 85, hiša epidemije 1886)
    h13 = [e for e in entries if e["houseNo"] == "13" and e["row"] == H13_ROW["row"]
           and e["scan"] == H13_ROW["scan"] and e["child"] == H13_ROW["child"]
           and H13_ROW["fatherPin"] in e["father"]]
    h78 = [e for e in entries if e["houseNo"] == "78" and e["row"] == H78_OSKRBAR_ROW["row"]
           and H78_OSKRBAR_ROW["pin"] in e["father"]]
    h29 = [e for e in entries if e["houseNo"] == "29" and e["row"] == H29_MILEK_ROW["row"]
           and H29_MILEK_ROW["fatherPin"] in e["father"]]
    ok8 = len(h13) == 1 and len(h78) == 1 and len(h29) == 1
    ok8 = ok8 and any("epidemij" in n for e in entries if e["houseNo"] == "29" for n in e["notes"])
    inv["I8_anchors_13_78_29"] = ok8

    # I9 — križne povezave: h13 v treh knjigah (04105/04894/04455) + h29 mrliška
    # 1886 (04894) + h78 krst 1887 (P79 sidro == P82 row 26, sk. 20) + nezakonski 3
    vit = parish_vitals("04105")
    vit_death = parish_vitals("04894")
    vit_marr = parish_vitals("04455")
    ok9 = any(v["houseNo"] == "13" and v["year"] == 1886 for v in vit)
    ok9 = ok9 and any(v["houseNo"] == "13" and v["year"] == 1886 for v in vit_death)
    ok9 = ok9 and any(v["houseNo"] == "13" and v["year"] == 1885 for v in vit_marr)
    ok9 = ok9 and any(v["houseNo"] == "29" and v["year"] == 1886 for v in vit_death)
    ok9 = ok9 and any(v["houseNo"] == "78" and v["year"] == 1887 and v["scan"] == 20 for v in vit)
    ok9 = ok9 and any(v["houseNo"] == "78" and v["year"] == 1888 for v in vit)
    ok9 = ok9 and dokaz["stats"]["illegitimate"] == 3
    ok9 = ok9 and sorted({e["houseNo"] for e in entries if "PRAZEN" in e["father"]}) == sorted(ILLEGIT_HOUSES)
    inv["I9_cross_links"] = ok9

    # I10 — runtime projekcija: vsi 15 vpisov v HOUSE_VITALS (houseNo/year/scan)
    missing = []
    for e in entries:
        hit = [v for v in vit if v["houseNo"] == e["houseNo"] and v["year"] == 1888
               and v["scan"] == e["scan"]]
        if not hit:
            missing.append(e["houseNo"])
    inv["I10_runtime_projection"] = not missing

    return dokaz, inv, probes, len(urls), in_set, gap, missing


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    dokaz, inv, probes, n_images, in_set, gap, missing = verify()
    all_ok = all(inv.values())
    print(f"P83 --check: {DOKAZ}")
    detail = " ".join(f"{k}={'P' if v else 'F'}" for k, v in inv.items())
    print(f"invarianti: {all_ok} — {detail}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {n_images} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {sorted({e['scan'] for e in dokaz['entries']})}")
    print(f"PT usklajenost: v naboru {in_set} | luknja 41–60 {gap}")
    if mode == "--check":
        print("P83 --check: PASS" if all_ok else "P83 --check: FAIL")
        sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
