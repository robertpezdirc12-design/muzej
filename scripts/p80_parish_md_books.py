#!/usr/bin/env python3
# P80 — ŽUPNIJA Podzemelj: RAZŠIRITEV vzorčnega prepisa na mrliško (04894)
# in poročno (04455) knjigo (issue #18, vzorec P79).
#
# Naslednja faza P79 nextSteps: "razširitev vzorca: poročne in mrliške knjige
# za rojstva/poroke/smrti istih hiš". Merila dokončanja (isti vzorec kot P79):
# okvir 1886 v obeh knjigah + sidra čez leta; vsak vpis s signaturo, letom,
# stranjo/skanom, hišno št.
#
# Ta skripta je DETERMINISTIČNI VERIFIKATOR prepisa (paleografsko branje
# skenov je ročna faza — skripta ne more in ne sme "ponovno brati" Kurrenta;
# meri DOSTOPNOST virov, strukturo vzorca in usklajenost s PT):
#   1. mrliška knjiga 04894 na Matricula Online (HTTP 200) + inventar 256 slik
#   2. poročna knjiga 04455 na Matricula Online (HTTP 200) + inventar 192 slik
#   3. citirani mrliški skeni (2,3,4,5,6) ⊆ inventar + live probe (JPEG ff-d8)
#   4. citirani poročni skeni (50,61,62,63,64,65,66) ⊆ inventar + live probe
#   5. okvir mrliške 1886: skeni 2–6, stran == sken − 1 (13 vpisov) + sidro
#      1887 (sken 6, 2 vpisa)
#   6. okvir poročne 1886: skeni 61–65, Pag. == sken − 1 (7 vpisov) + sidra
#      (1882 sk.50 Pag.44 · 1885 sk.61 · 1887 sk.66 ×2)
#   7. obdobja knjig == PARISH_BOOKS (04894 death 1886–1924; 04455 marriage
#      1873–1922 — branje iz parish.ts)
#   8. PT usklajenost: 25 različnih hiš celotnega vzorca (krstna+mrliška+
#      poročna): 19 v naboru PT (1–40 + 61–99; branje chain-full-pt-ps.json)
#      + 6 v luknji 41–60 (44, 54, 56, 57, 59, 60)
#   9. križne povezave treh virov: hiše 13, 36, 71 prisotne v VSEH treh
#      knjigah (krstna 04105 + mrliška 04894 + poročna 04455)
#  10. P80 re-read: hiša 56 (krstna) = "roj. Perdinec", brez starrega branja
#      "roj. Podžire" (poročna sk. 62 vpis 4/1886 = isti par)
#
# Izhod: transkripcijski dokaz research/issue17/parish-md-transcription.json
#        (ročna faza — NIKOLI ne prepisan s strani skripte); skripta izpiše
#        invarianti in exit 0/1. --check == verify (live probe, brez mutacij).
#
# Status: SAMPLE-TRANSCRIPTION-EXTENDED (mrliška 1886: 13 vpisov / 11 hiš +
#         sidro 1887 ×2; poročna 1886: 7 vpisov / 10 hiš + 4 sidra; skupaj
#         s krstno 41 vpisov / 25 različnih hiš).

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOKAZ = os.path.join(REPO, "research", "issue17", "parish-md-transcription.json")
DOKAZ_P79 = os.path.join(REPO, "research", "issue17", "parish-sample-transcription.json")
PT_CHAIN = os.path.join(REPO, "research", "issue13", "chain-full-pt-ps.json")
PARISH_TS = os.path.join(REPO, "src", "data", "atlas", "parish.ts")

DEATH_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
MARR_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# --- pričakovano stanje (invarianti) ---
EXPECTED_DEATH_IMAGES = 256
EXPECTED_MARR_IMAGES = 192
DEATH_FRAME_SCANS = (2, 6)  # skeni 2–6 == strani 1–5 == leto 1886
MARR_FRAME_SCANS = (61, 65)  # skeni 61–65 == Pag. 60–64 == leto 1886
DEATH_1886_ENTRIES = 13
DEATH_1887_ANCHORS = 2
MARR_1886_ENTRIES = 7
MARR_ANCHORS = {"1882": 1, "1885": 1, "1887": 2}
PT_GAP_HOUSES = {"43", "44", "45", "46", "47", "48", "52", "53", "54", "55", "56", "57", "58", "59", "60", "42"}  # P82: + 47, 52 (row 78 izvirno), 55; P85: + 41 (izven vzorca); P86: + 53; P88: + 46; P91: + 45; P92: + 43; P93: + 48; P123: + 42 (CERNIČ-hiša — krstni dokazi izven vzorca!)
TRI_SOURCE_HOUSES = {"13", "36", "71"}


def http_get(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
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


def base64_pad_decode(s):
    import base64
    return base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")


def decode_inventory(html):
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


def probe_jpeg(url):
    st, b = http_get(url)
    return {"http": st, "jpeg": bool(b) and b[:2] == b"\xff\xd8", "bytes": len(b) if b else 0}


def pt_house_set():
    d = json.load(open(PT_CHAIN, encoding="utf-8"))
    return {str(r["no"]).strip() for r in d["chain"] if r.get("kind") == "hiša"}


def parse_house_vitals():
    """Preprost parsnik HOUSE_VITALS iz parish.ts (brez TS runtime)."""
    src = open(PARISH_TS, encoding="utf-8").read()
    m = re.search(r"export const HOUSE_VITALS[^=]*=\s*\[(.*?)\n\];", src, re.S)
    body = m.group(1)
    vitals = []
    for obj in re.finditer(r"\{(.*?)\}", body, re.S):
        o = obj.group(1)
        def pick(key):
            mm = re.search(key + r':\s*"((?:[^"\\]|\\.)*)"', o)
            return mm.group(1) if mm else None
        def pickn(key):
            mm = re.search(key + r':\s*(\d+)', o)
            return int(mm.group(1)) if mm else None
        vitals.append({
            "houseNo": pick("houseNo"),
            "bookSignature": pick("bookSignature"),
            "year": pickn("year"),
            "scan": pickn("scan"),
            "page": pickn("page"),
            "whatSi": (pick("whatSi") or "").replace("\\\"", '"').replace("\\\\", "\\"),
            "whatEn": (pick("whatEn") or "").replace("\\\"", '"').replace("\\\\", "\\"),
            "status": pick("status"),
        })
    return [v for v in vitals if v["houseNo"]]


def verify():
    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    entries = dokaz["entries"]
    p79 = json.load(open(DOKAZ_P79, encoding="utf-8"))
    vitals = parse_house_vitals()
    inv = {}

    # I1 — mrliška knjiga dostopna + inventar
    st, body = http_get(DEATH_URL)
    inv["I1_death_book_200_inv256"] = (st == 200 and len(decode_inventory(body.decode("utf-8", "replace"))) == EXPECTED_DEATH_IMAGES) if st == 200 else False
    death_urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []

    # I2 — poročna knjiga dostopna + inventar
    st, body = http_get(MARR_URL)
    inv["I2_marriage_book_200_inv192"] = (st == 200 and len(decode_inventory(body.decode("utf-8", "replace"))) == EXPECTED_MARR_IMAGES) if st == 200 else False
    marr_urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []

    # I3 — citirani mrliški skeni live (2,3,4,5,6)
    death_scans = sorted({int(e["scan"]) for e in entries if e["bookSignature"] == "04894"})
    probes = []
    ok_all = True
    for n in death_scans:
        p = probe_jpeg(death_urls[n - 1]) if len(death_urls) >= n else {"http": 0, "jpeg": False, "bytes": 0}
        probes.append({"scan": n, **p})
        ok_all = ok_all and p["http"] == 200 and p["jpeg"]
    inv["I3_death_scans_live"] = ok_all and len(death_scans) == 5

    # I4 — citirani poročni skeni live (50,61,62,63,64,65,66)
    marr_scans = sorted({int(e["scan"]) for e in entries if e["bookSignature"] == "04455"})
    probes_m = []
    ok_all = True
    for n in marr_scans:
        p = probe_jpeg(marr_urls[n - 1]) if len(marr_urls) >= n else {"http": 0, "jpeg": False, "bytes": 0}
        probes_m.append({"scan": n, **p})
        ok_all = ok_all and p["http"] == 200 and p["jpeg"]
    inv["I4_marriage_scans_live"] = ok_all and len(marr_scans) == 7

    # I5 — okviri in sidra iz dokaza (mrliška 1886 = 13; poročna 1886 = 7)
    d1886 = [e for e in entries if e["bookSignature"] == "04894" and int(e["year"]) == 1886]
    d1887 = [e for e in entries if e["bookSignature"] == "04894" and int(e["year"]) == 1887]
    m1886 = [e for e in entries if e["bookSignature"] == "04455" and int(e["year"]) == 1886]
    manch = {}
    for e in entries:
        if e["bookSignature"] == "04455" and int(e["year"]) != 1886:
            manch[str(e["year"])] = manch.get(str(e["year"]), 0) + 1
    frame_ok = (
        len(d1886) == DEATH_1886_ENTRIES
        and all(DEATH_FRAME_SCANS[0] <= int(e["scan"]) <= DEATH_FRAME_SCANS[1] and int(e["page"]) == int(e["scan"]) - 1 for e in d1886)
        and len(d1887) == DEATH_1887_ANCHORS and all(int(e["scan"]) == 6 for e in d1887)
        and len(m1886) == MARR_1886_ENTRIES
        and all(MARR_FRAME_SCANS[0] <= int(e["scan"]) <= MARR_FRAME_SCANS[1] and int(e["page"]) == int(e["scan"]) - 1 for e in m1886)
        and manch == MARR_ANCHORS
        and all(int(e["scan"]) == 50 for e in entries if e["bookSignature"] == "04455" and int(e["year"]) == 1882)
    )
    inv["I5_frames_anchors"] = frame_ok

    # I6 — obdobja knjig == parish.ts (PARISH_BOOKS)
    ts = open(PARISH_TS, encoding="utf-8").read()
    bd = re.search(r'signature:\s*"04894",\s*type:\s*"death",\s*from:\s*(\d+),\s*to:\s*(\d+)', ts)
    bm = re.search(r'signature:\s*"04455",\s*type:\s*"marriage",\s*from:\s*(\d+),\s*to:\s*(\d+)', ts)
    inv["I6_book_periods"] = bool(
        bd and bm
        and bd.group(1) == "1886" and bd.group(2) == "1924"
        and bm.group(1) == "1873" and bm.group(2) == "1922"
        and all(1886 <= int(e["year"]) <= 1924 for e in entries if e["bookSignature"] == "04894")
        and all(1873 <= int(e["year"]) <= 1922 for e in entries if e["bookSignature"] == "04455")
    )

    # I7 — PT usklajenost celotnega P79/P80 vzorca (krstna+mrliška+poročna ==
    # parish.ts); P82: vzorec omejen na 04105 1886 ∪ 1897 ∪ sidri 61/78
    # (1887 okvir ima svojo skripto p82); P83: 1888 okvir ima svojo skripto
    # p83; P84: 1889 okvir ima svojo skripto p84; P85: 1890 okvir ima svojo
    # skripto p85; P86: 1891 okvir ima svojo skripto p86; P87: 1892 okvir
    # ima svojo skripto p87; P88: 1893 okvir ima svojo skripto p88;
    # P89: 1894 okvir ima svojo skripto p89;
    # HOUSE_VITALS skupaj 193 (179 + 14 zasidranih celotnega okvira 1896)
    sample = [
        v for v in vitals
        if v["bookSignature"] in ("04894", "04455")
        or (v["bookSignature"] == "04105"
            and (v["year"] == 1886 or v["year"] == 1897
                 or (v["year"] == 1887 and v["houseNo"] in ("61", "78"))))
    ]
    houses = {v["houseNo"] for v in sample}
    pts = pt_house_set()
    gap = sorted(houses & PT_GAP_HOUSES, key=int)
    inset = sorted(houses - PT_GAP_HOUSES, key=lambda x: int(float(x)))
    inv["I7_pt_consistency"] = (
        houses == (set(inset) | set(gap))
        and len(gap) == 12  # P92 scoping: 1897 bloki vnesejo 43/45/46/54/60 — 6 → 9; P119: h53 NOVI dokaz v luknji 41–60 → 9 → 10; P122/P123: h58 (Požek v16!) + h42 (CERNIČ-hiša) NOVA dokaza v luknji → 10 → 12
        and all((float(h) <= 40 or float(h) >= 61) or ("½" in h) for h in inset)
        and all(41 <= float(h) <= 60 for h in gap)
        and all(h in houses for h in (v["houseNo"] for v in sample))
        and len(vitals) == 563  # P121: 554; P122: +5 blokov 1893 (h26/h58/h62/h69/h74) + P123: +4 bloki 1894 (h9/h11/h27/h42) → 563
        and len(houses) == 53  # P121: 47; P122+P123: +6 NOVIH hiš v vzorcu (9, 26, 27, 42, 58, 62 — h69/h74 že prek mrliške!) → 53
        and set(inset) <= pts
    )

    # I8 — križne povezave treh virov (hiše 13, 36, 71 v vseh treh knjigah)
    tri = {
        h: all(any(v["houseNo"] == h and v["bookSignature"] == s for v in vitals) for s in ("04105", "04894", "04455"))
        for h in TRI_SOURCE_HOUSES
    }
    inv["I8_tri_source_links"] = all(tri.values())

    # I9 — P80 re-read hiša 56: "roj. Perdinec", brez "roj. Podžire"
    h56 = next((v for v in vitals if v["houseNo"] == "56" and v["bookSignature"] == "04105"), None)
    inv["I9_reread_house56_perdinec"] = bool(
        h56 and "roj. Perdinec" in h56["whatSi"] and not re.search(r"roj\.\s*Podžire", h56["whatSi"])
        and any(e.get("reRead") for e in entries if e["bookSignature"] == "04455" and e.get("houseNo") == "36")
    )

    # celovitost: vsak vpis ima polja + status DOCUMENTED
    fields_ok = all(
        e.get("houseNo") and e.get("bookSignature") and e.get("year") and e.get("scan")
        and e.get("page") is not None and e.get("whatSi") and e.get("whatEn") and e.get("status") == "DOCUMENTED"
        for e in entries
    )
    inv["I10_fields_complete"] = fields_ok and len(entries) == 26 and len(p79["entries"]) == 14

    print("=== P80 verifikacija (mrliška 04894 + poročna 04455) ===")
    for k in sorted(inv):
        print(f"  {k}: {'PASS' if inv[k] else 'FAIL'}")
    ok = all(inv.values())
    print(f"SKUPAJ: {'PASS' if ok else 'FAIL'}")
    return ok, inv, probes, probes_m


def issue():
    """Izdaja dokaza (brez live probe — tista gre v verify; dokaz je determinističen)."""
    raise SystemExit("dokaz je izdan ročno (paleografska faza) — skripta NE izdaja dokaza")


if __name__ == "__main__":
    if "--check" in sys.argv or "verify" in sys.argv:
        ok, inv, p1, p2 = verify()
        sys.exit(0 if ok else 1)
    else:
        issue()
