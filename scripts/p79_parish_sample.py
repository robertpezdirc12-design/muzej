#!/usr/bin/env python3
# P79 — ŽUPNIJA Podzemelj: vzorčni prepis matričnih vpisov z gribeljskimi
# hišnimi št. (issue #18, vzorec P77).
#
# Odprta točka issue #18: "prepis matričnih vpisov za ostale hiše
# (rojstva/poroke/smrti po hišnih številkah — vsebina je prosto dostopna na
# matricula-online.eu)"; do P79 je bil prepisan samo hiša 61 (HOUSE_VITALS 1
# par). Merila dokončanja: vzorčni prepis (npr. 5 hiš) — vsak vpis s
# signaturo, letom, stranjo/skanom; usklajeno s hišnimi št. iz PT.
#
# Ta skripta je DETERMINISTIČNI VERIFIKATOR prepisa (paleografsko branje
# skenov je ročna faza — dokumentirana v transkripcijskem dokazu; skripta
# ne more in ne sme "ponovno brati" Kurrenta — meri DOSTOPNOST vira,
# strukturo vzorca in usklajenost s PT):
#   1. GET knjige 04105 na Matricula Online (HTTP 200)
#   2. dekodiranje inventarja slik: JSON "files": ["/image/<base64>/"] →
#      hosted URL (R%20Podzemelj%201886-1919-NNNN.jpg) — pričakovano 326
#   3. citirani skeni (2,4,6,7,9,12,13,14,15,20) ⊆ inventar + live probe
#      (HTTP 200 + JPEG magija ff-d8)
#   4. invarianti vzorca iz transkripcijskega dokaza:
#      I4 ≥ 5 različnih hiš (merila issue #18), I5 okvir (1886 ⊆ skeni
#      2–15; sidro 1887 = sken 20; stran = sken − 1), I6 PT usklajenost
#      (10/13 v naboru PT 1–40+61–99; 54/56/57 v luknji 41–60 — branje
#      research/issue13/chain-full-pt-ps.json), I7 celovitost polj,
#      I8 sidro hiša 61 (sken 20, vrstica 28, Katarina) == parish.ts
#
# Izhod: transkripcijski dokaz research/issue17/parish-sample-transcription.json
#        (ročna faza — NIKOLI ne prepisan s strani skripte); skripta izpiše
#        invarianti in exit 0/1. --check == verify (live probe, brez mutacij).
#
# Status: SAMPLE-TRANSCRIPTION (polno leto 1886 + sidro 1887; 14 vpisov,
#         13 različnih hiš; nad merili issue #18 — 5 hiš).

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOKAZ = os.path.join(REPO, "research", "issue17", "parish-sample-transcription.json")
PT_CHAIN = os.path.join(REPO, "research", "issue13", "chain-full-pt-ps.json")

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/"
BOOK_SIGNATURE = "04105"
EXPECTED_IMAGES = 326
CITED_SCANS = sorted({int(e["scan"]) for e in json.load(open(DOKAZ, encoding="utf-8"))["entries"]})
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# --- pričakovano stanje (invarianti I1–I8) ---
EXPECTED_PT_IN_SET = {"8", "16", "11", "36", "94", "39", "13", "71", "75", "61"}
EXPECTED_PT_GAP = {"54", "57", "56"}
FRAME_1886_SCANS = (2, 15)  # skeni 2–15 == strani 1–14 == leto 1886
ANCHOR_1887_SCAN = 20


def http_get(url, headers, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            last = (e.code, e.read()[:200])
            if e.code in (403, 429, 500, 502, 503, 504):
                time.sleep(4 * (i + 1))
                continue
            return last
        except Exception as e:
            last = (0, str(e)[:200].encode())
            time.sleep(4 * (i + 1))
    return last


def decode_inventory(html):
    """JSON 'files': ['/image/<base64>/', ...] → hosted URL seznam."""
    raws = re.findall(r"/image/(aHR0cDovL2hvc3RlZC1pbWFnZXM[A-Za-z0-9%+/=]+?)/", html)
    urls = []
    for r in raws:
        try:
            d = base64_pad_decode(r)
            if "hosted-images" in d:
                urls.append(d)
        except Exception:
            pass
    return sorted(set(urls))


def base64_pad_decode(s):
    import base64
    return base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")


def probe_jpeg(url):
    st, b = http_get(url, UA)
    return {"http": st, "jpeg": bool(b) and b[:2] == b"\xff\xd8", "bytes": len(b) if b else 0}


def pt_house_set():
    d = json.load(open(PT_CHAIN, encoding="utf-8"))
    return {str(r["no"]).strip() for r in d["chain"] if r.get("kind") == "hiša"}


def verify():
    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    entries = dokaz["entries"]
    inv = {}

    # I1 — knjiga dostopna
    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    html = body.decode("utf-8", "replace") if st == 200 else ""

    # I2 — inventar slik
    urls = decode_inventory(html) if html else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    # I3 — citirani skeni ⊆ inventar + JPEG probe
    by_name = {u.split("/")[-1]: u for u in urls}
    probes = {}
    ok3 = bool(urls)
    for n in CITED_SCANS:
        name = f"R%20Podzemelj%201886-1919-{n:04d}.jpg"
        u = by_name.get(name)
        if not u:
            ok3 = False
            probes[n] = {"http": 0, "jpeg": False, "bytes": 0, "missing": True}
            continue
        p = probe_jpeg(u)
        probes[n] = p
        ok3 = ok3 and p["http"] == 200 and p["jpeg"]
    inv["I3_cited_scans_jpeg"] = ok3

    # I4 — merila issue #18: ≥ 5 različnih hiš
    houses = [e["houseNo"] for e in entries]
    inv["I4_houses_ge_5"] = len(set(houses)) >= 5

    # I5 — okvir: 1886 ⊆ skeni 2–15; sidro 1887 == sken 20; stran == sken − 1
    ok5 = True
    for e in entries:
        if e["year"] == 1886:
            ok5 = ok5 and FRAME_1886_SCANS[0] <= e["scan"] <= FRAME_1886_SCANS[1]
        elif e["year"] == 1887:
            ok5 = ok5 and e["scan"] == ANCHOR_1887_SCAN
        else:
            ok5 = False
        ok5 = ok5 and e["page"] == e["scan"] - 1
    inv["I5_frame_and_pages"] = ok5

    # I6 — PT usklajenost (klasifikacija iz verige PT 1825)
    pt = pt_house_set()
    in_set = sorted({h for h in houses if h in pt}, key=int)
    gap = sorted({h for h in houses if h not in pt}, key=int)
    inv["I6_pt_consistency"] = (set(in_set) == EXPECTED_PT_IN_SET
                                and set(gap) == EXPECTED_PT_GAP)

    # I7 — celovitost polj (signatura/leto/sken/stran/vas/hiša/otrok/starši)
    req = ("row", "year", "month", "born", "baptized", "village", "houseNo",
           "scan", "page", "child", "father", "mother", "whatSi", "whatEn")
    ok7 = all(all(e.get(k) not in (None, "") for k in req) for e in entries)
    ok7 = ok7 and all(e["village"] == "Griblje" for e in entries)
    ok7 = ok7 and all(dokaz["source"]["bookSignature"] == BOOK_SIGNATURE
                      for _ in [0])
    inv["I7_entries_complete"] = ok7

    # I8 — sidro hiša 61 (verifikacija obstoječega zapisa parish.ts)
    anchor = [e for e in entries
              if e["year"] == 1887 and e["scan"] == 20
              and e["houseNo"] == "61" and e["child"] == "Katarina"]
    inv["I8_anchor_61"] = len(anchor) == 1 and anchor[0]["row"] == 28

    return dokaz, inv, probes, len(urls), in_set, gap


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode not in ("--check", "verify"):
        print("uporaba: p79_parish_sample.py [--check|verify]")
        sys.exit(2)
    dokaz, inv, probes, nurls, in_set, gap = verify()
    print(f"P79 {mode}: {DOKAZ}")
    print(f"invarianti: {all(inv.values())} — " +
          " ".join(f"{k}={'P' if v else 'F'}" for k, v in inv.items()))
    print(f"knjiga {BOOK_SIGNATURE}: slike {nurls} (pričakovano "
          f"{EXPECTED_IMAGES}); citirani skeni {CITED_SCANS}")
    print(f"PT usklajenost: v naboru {in_set} | luknja 41–60 {gap}")
    for n, p in sorted(probes.items()):
        print(f"  sken {n:04d}: HTTP {p['http']} jpeg={p['jpeg']}")
    sys.exit(0 if all(inv.values()) else 1)


if __name__ == "__main__":
    main()
