#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P82 — župnija Podzemelj: krstna knjiga 04105, polno leto 1887 (issue #18).

Razširitev vzorca P79 (1886) na naslednje leto 1887: skeni 16–27 == strani
15–26 (stran == sken − 1) — vsi vpisi z Griblji + dokaz preloma 1888 (velike
cifre »1 8 8 8« na strani 26 po vrstici 106). Paleografska faza ročna (skeni
v delovnem imeniku, NI v repu); ta skripta je DETERMINISTIČNI VERIFIKATOR
(brez AI ob delovanju): live HTTP preveri knjigo + citirane skene, dokaz
preveri proti PARISH_BOOKS/CHAIN pinom, sidru hiše 61 (P79 re-verify),
PT klasifikaciji in runtime projekciji (HOUSE_VITALS v src/data/atlas/parish.ts).

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
DOKAZ = "research/issue17/parish-baptism-1887.json"
PARISH_TS = "src/data/atlas/parish.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (16, 27)
FRAME_PAGES = (15, 26)
BREAK_1888 = {"scan": 27, "page": 26, "row": 107}
EXPECTED_HOUSES = 19
EXPECTED_ENTRIES = 20
EXPECTED_PT_IN_SET = {"2", "15", "17", "21", "24", "26", "27", "31", "34", "35", "61", "62", "63", "65", "66", "78"}
EXPECTED_PT_GAP = {"47", "52", "55"}


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
    raise last  # type: ignore[misc]


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

    # I3 — citirani skeni ⊆ okvir 16–27 + JPEG probe (strani 15, 17, 18, 21
    # prebrane brez Gribljev — zato niso citirane; celoten okvir pinja frame)
    by_name = {u.split("/")[-1]: u for u in urls}
    cited = sorted({e["scan"] for e in entries})
    ok3 = all(FRAME_SCANS[0] <= n <= FRAME_SCANS[1] for n in cited) and len(cited) >= 8
    probes = {}
    for n in cited:
        name = f"R%20Podzemelj%201886-1919-{n:04d}.jpg"
        u = by_name.get(name)
        p = probe_jpeg(u) if u else {"http": 0, "jpeg": False, "bytes": 0}
        probes[n] = p
        ok3 = ok3 and p["http"] == 200 and p["jpeg"]
    inv["I3_cited_scans_jpeg"] = ok3

    # I4 — okvir: vsi vpisi 1887, skeni 16–27, stran == sken − 1
    ok4 = all(
        e["year"] == 1887 and FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1]
        and e["page"] == e["scan"] - 1 and FRAME_PAGES[0] <= e["page"] <= FRAME_PAGES[1]
        for e in entries
    )
    ok4 = ok4 and dokaz["frame"]["scanFrom"] == 16 and dokaz["frame"]["scanTo"] == 27
    b = dokaz["frame"]["break1888"]
    ok4 = ok4 and b.get("scan") == BREAK_1888["scan"] and b.get("page") == BREAK_1888["page"] \
        and b.get("row") == BREAK_1888["row"]  # row 107 = zvezno štetje 106+1 (P83: pisane
        # oznake se pri prelomu leta ponastavijo na 1 — str. 27 = oznaka 3; rowNote v dokazu)
    inv["I4_frame_and_break"] = ok4

    # I5 — merila issue #18: ≥ 5 hiš; pričakovano 20 vpisov / 19 različnih hiš
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
    )

    # I7 — celovitost polj
    req = ("row", "year", "month", "born", "village", "houseNo", "scan", "page",
           "child", "father", "mother", "whatSi", "whatEn")
    ok7 = all(all(e.get(k) not in (None, "") for k in req) for e in entries)
    ok7 = ok7 and all(e["village"] == "Griblje" for e in entries)
    ok7 = ok7 and all(dokaz["source"]["book"].startswith("Matricula") for _ in [0])
    inv["I7_entries_complete"] = ok7

    # I8 — sidro hiše 61 (P79 re-verify): row 28, sken 20, Katarina
    anchor = [e for e in entries if e["houseNo"] == "61" and e["scan"] == 20
              and e["row"] == 28 and e["child"] == "Katarina"]
    inv["I8_anchor_61"] = len(anchor) == 1

    # I9 — križne povezave P79/P80: hiša 61 krst 1887 (P79 sidro, re-verify);
    # hiša 31 mrliška 1886 (04894, Katarina Marh — P80) + 2× krst 1887 (P82)
    vit = parish_vitals("04105")
    vit_death = parish_vitals("04894")
    v61 = [v for v in vit if v["houseNo"] == "61"]
    ok9 = any(v["year"] == 1887 and v["scan"] == 20 for v in v61)
    ok9 = ok9 and any(v["houseNo"] == "31" and v["year"] == 1886 for v in vit_death)
    ok9 = ok9 and len([e for e in entries if e["houseNo"] == "31"]) == 2
    ok9 = ok9 and dokaz["crossLinks"]["house31"].startswith("1886 mrliška")
    inv["I9_cross_links"] = ok9

    # I10 — runtime projekcija: vsi 20 vpisov v HOUSE_VITALS (houseNo/year/scan/page)
    missing = []
    for e in entries:
        hit = [v for v in vit if v["houseNo"] == e["houseNo"] and v["year"] == 1887
               and v["scan"] == e["scan"]]
        if not hit:
            missing.append(e["houseNo"])
    inv["I10_runtime_projection"] = not missing

    return dokaz, inv, probes, len(urls), in_set, gap, missing


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    dokaz, inv, probes, n_images, in_set, gap, missing = verify()
    all_ok = all(inv.values())
    print(f"P82 --check: {DOKAZ}")
    detail = " ".join(f"{k}={'P' if v else 'F'}" for k, v in inv.items())
    print(f"invarianti: {all_ok} — {detail}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {n_images} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {sorted({e['scan'] for e in dokaz['entries']})}")
    print(f"PT usklajenost: v naboru {in_set} | luknja 41–60 {gap}")
    if mode == "--check":
        print("P82 --check: PASS" if all_ok else "P82 --check: FAIL")
        sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
