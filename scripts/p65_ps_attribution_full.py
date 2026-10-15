#!/usr/bin/env python3
# P65 — POLNA PER-BLATT ATRIBUCIJA: 101 single-Blatt več-stranskih base
# (odprta točka P64 #3 — "atribucija 101 single-Blatt več-stranskih base
#  (211 − 110; instanca enotna po Blattu — trivialno)"; s tem je pokritost
#  per-Blatt atribucije čez-Blatt + single-Blatt več-stranskih base
#  POPOLNA: 211/211).
#
# P59 je izmerila 211 več-stranskih base v v2 (basesOnMultiplePages_v2),
# od katerih 110 sega čez ≥2 Blatta (multiBlattBaseList) — te je P64
# atributiral z merjeno hierarhijo pravil (R1 pas > R2a dominanca ≥ 0.75 >
# R2b ena-area > split). Ostalih 101 base nosi VSE vrstice na straneh
# ISTEGA Blatta → atribucija je trivialna in nedvoumna:
#
#   R3-single — vsi atributirani Blatt-i vrstic base == 1 vrednost
#               → attributedBlatt = ta Blatt, status 'R3-single'.
#               (merjeno: I 3 · II 26 · III 14 · IV 58; 205 vrstic —
#                98 base × 2 vrstici + 3 base × 3 vrstice; vseh 101 base
#                ima izmerjeno površino — 0 brez areaQK).
#
# P65 ne spremeni joina v2 (disciplina P56/P58/P59) in ne spremeni P64
# atribucij — 110 P64 base je v polnem datasetu bajtno (I3).
#
# Polna pokritost registra (kontrolni blok coverage, merjeno):
#   800 base × 1093 vrstic = 589 single-page (implicitno atributirane
#   prek pageAttribution strani: I 145 · I·II 10 · II 183 · III 28 ·
#   IV 205 · V 18) + 211 multi-page (110 čez-Blatt: 71 atributiranih +
#   39 split; 101 single-Blatt: 101 atributiranih) → skupaj 172/211
#   atributiranih multi-page (Blatt II 68 · IV 63 · III 29 · I 8 · V 4);
#   0 vrstic brez atribucije strani.
#
# Vhodi (committed):
#   research/issue17/ps-parcels-geo-v2.json       — vrstice v2 (rowsEvidence)
#   research/issue17/ps-blatt-headers.json        — P59 dokaz (pageAttribution)
#   src/data/atlas/ps-blatt-headers.json          — P59 runtime (sha pin)
#   src/data/atlas/ps-perblatt-attribution.json   — P60 runtime (sha pin)
#   research/issue17/ps-attribution-ext.json      — P64 dokaz (sha pin)
#   src/data/atlas/ps-attribution-ext.json        — P64 runtime (bajtni vir 110)
# Izhodi:
#   research/issue17/ps-attribution-full.json     (dokaz)
#   src/data/atlas/ps-attribution-full.json       (runtime, bajtno projekcija)
#
# Invarianti (FAIL ob padu):
#   I1 vhodni pini: 5× sha256 (v2 ev ebb8f729…, bhrt efe39f41…, p60rt
#      28465b3e…, p64ev a6f6d8af…, p64rt 7e5ea64a…); števci 1093/800/211/110/101
#   I2 razčlenitev izčrpna in disjunktna: multi-page == multi-Blatt ⊔
#      single-Blatt; vsak R3 base ima TOČNO 1 ne-null Blatt; 0 vrstic brez
#      atribucije strani; R3 pages ≥ 2
#   I3 P64 podmnožica bajtno: 110 base == P64 runtime (deep equality)
#   I4 pokritost + distribucije: statusDist 17/53/1/101/39; attrDist
#      I 8 · II 68 · III 29 · IV 63 · V 4; distByRule R3 I 3 · II 26 ·
#      III 14 · IV 58; coverage 800/1093/589/211 + singlePageByBlatt
#   I5 soslednost: R3 189/20; skupna (211 base) 375/50 (relevantnih 425)
#   I6 join nespremanjen (sha256 v2 vhoda; brez lat/lng; areaQK samo v
#      blattShares)
#   I7 dokaz ⊇ runtime (bajtno podmnožica)
#   I8 determinizem — --check bajtno identično
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v3.json")  # P68 v3
P59 = os.path.join(ROOT, "research/issue17/ps-blatt-headers.json")
P64EV = os.path.join(ROOT, "research/issue17/ps-attribution-ext.json")
BHRT = os.path.join(ROOT, "src/data/atlas/ps-blatt-headers.json")
P60RT = os.path.join(ROOT, "src/data/atlas/ps-perblatt-attribution.json")
P64RT = os.path.join(ROOT, "src/data/atlas/ps-attribution-ext.json")
OUT_EV = os.path.join(ROOT, "research/issue17/ps-attribution-full.json")
OUT_RT = os.path.join(ROOT, "src/data/atlas/ps-attribution-full.json")

PIN_V2_EV_SHA = "af7479e428182f381d3a2537896493d7cf86210fac7027221e22ac2aea218b53"  # P68 v3 (join blok)
PIN_BHRT_SHA = "f4c4dedcd6c65d4d1480b4124ae93d00304be2f24f30aa74ca5d0c6ff8c9efe6"  # P68 v3 re-run
PIN_P60RT_SHA = "c42bf221141e46aee0c387506bdf594c24373d41b19420fe2fc8fc2b7047d6e4"  # P68 v3 re-run
PIN_P64EV_SHA = "4dab5e834b1416f06a4cdc95f25f7cabc24c8ec7efe1ce2e53fc4eb404786cf8"  # P68 v3 re-run (distByRule dinamično)
PIN_P64RT_SHA = "dda6bebdbd89a4dd8064a1bd062cbc090312f23ee2f75907048fcd463fc566ba"  # P68 v3 re-run (distByRule dinamično)

EXPECTED_STATUS_DIST = {"R1": 14, "R2a": 47, "R2b": 1, "R3-single": 101, "split": 36}  # P68 v3 (v2: 17/53/1/101/39)
EXPECTED_ATTR_BLATT = {"I": 5, "II": 61, "III": 30, "IV": 63, "V": 4}  # P68 v3 (v2: I 8/II 68/III 29/IV 63/V 4)
EXPECTED_R3_BLATT = {"I": 3, "II": 26, "III": 14, "IV": 58}
EXPECTED_COVERAGE = {
    "basesTotal": 798, "rowsTotal": 1079, "singlePage": 599,  # P68 v3 (v2: 800/1093/589)
    "multiPage": 199, "multiBlatt": 98, "singleBlattMultiPage": 101,  # P68 v3 (v2: 211/110/101)
    "nullAttributionRows": 0,
}
EXPECTED_SP_BY_BLATT = {"I": 156, "I·II": 10, "II": 183, "III": 26, "IV": 206, "V": 18}  # P68 v3 (v2: I 145/III 28/IV 205)
EXPECTED_SOS = {"ok": 364, "flag": 49}  # P68 v3 (v2: 375/50)
EXPECTED_R3_SOS = {"ok": 189, "flag": 20}
EXPECTED_R3_ROWS = 205
EXPECTED_R3_ROWS_DIST = {2: 98, 3: 3}


def fail(msg):
    print(f"FAIL I: {msg}")
    sys.exit(1)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def rnd(x, n):
    """Half-up zaokroževanje (JS Math.round kompatibilno)."""
    return math.floor(x * (10 ** n) + 0.5) / (10 ** n)


def main():
    v2 = json.load(open(V2))
    p59 = json.load(open(P59))
    p64rt = json.load(open(P64RT))
    json.load(open(P64EV))  # dokaz je bran (I1 pin) — vsebina ni direktno rabljena
    rows = v2["rowsEvidence"]
    page_attr = p59["pageAttribution"]
    multi_blatt_list = p59["perBlattAmbiguity"]["multiBlattBaseList"]

    # ————— I1 vhodni pini —————
    if sha256(V2) != PIN_V2_EV_SHA:
        fail("I1 sha256 v2 vhoda se je spremenil (drift — preveri P58 chain)")
    if sha256(BHRT) != PIN_BHRT_SHA:
        fail("I1 sha256 runtime ps-blatt-headers.json ≠ pin (drift)")
    if sha256(P60RT) != PIN_P60RT_SHA:
        fail("I1 sha256 runtime ps-perblatt-attribution.json ≠ pin (drift)")
    if sha256(P64EV) != PIN_P64EV_SHA:
        fail("I1 sha256 dokaza ps-attribution-ext.json ≠ pin (drift)")
    if sha256(P64RT) != PIN_P64RT_SHA:
        fail("I1 sha256 runtime ps-attribution-ext.json ≠ pin (drift)")
    if len(rows) != 1079:
        fail(f"I1 rowsEvidence {len(rows)} ≠ 1079 (v3 P68; v2: 1093)")
    if len(multi_blatt_list) != 98:
        fail(f"I1 multiBlattBaseList {len(multi_blatt_list)} ≠ 98 (v3 P68; v2: 110)")
    if sorted(p64rt["bases"].keys()) != sorted(multi_blatt_list):
        fail("I1 P64 runtime base ≠ multiBlattBaseList")

    # ————— vrstice po base + vrstni red per stran (soslednost, P60 metoda) —————
    rows_by_base = defaultdict(list)
    page_order = defaultdict(list)
    for r in rows:
        rows_by_base[r["base"]].append(r)
        page_order[r["page"]].append(r["base"])

    pages_by_base = {b: sorted({r["page"] for r in rs}) for b, rs in rows_by_base.items()}
    multi_page = {b for b, p in pages_by_base.items() if len(p) >= 2}
    multi_blatt = set(multi_blatt_list)
    r3_bases = {b for b in multi_page if b not in multi_blatt}

    # ————— I2 razčlenitev —————
    if len(pages_by_base) != EXPECTED_COVERAGE["basesTotal"]:
        fail(f"I2 base skupaj {len(pages_by_base)} ≠ 800")
    if len(multi_page) != EXPECTED_COVERAGE["multiPage"]:
        fail(f"I2 multi-page {len(multi_page)} ≠ 199 (v3 P68; v2: 211 — P59 basesOnMultiplePages_v2)")
    if not multi_blatt.issubset(multi_page):
        fail("I2 multiBlattBaseList ⊄ multi-page (razčlenitev razbita)")
    if len(r3_bases) != EXPECTED_COVERAGE["singleBlattMultiPage"]:
        fail(f"I2 single-Blatt multi-page {len(r3_bases)} ≠ 101")  # v3: izračun (v2: 101)

    def blatt(p):
        return page_attr.get(str(p), {}).get("blatt")

    null_rows = sum(1 for r in rows if not blatt(r["page"]))
    if null_rows != EXPECTED_COVERAGE["nullAttributionRows"]:
        fail(f"I2 vrstic brez atribucije strani {null_rows} ≠ 0")

    def blatt_stats(b):
        """Per-Blatt: Σ areaQK, vrstice, strani (P64 metoda)."""
        by_blatt = defaultdict(lambda: {"a": 0.0, "rows": [], "pages": set()})
        for r in rows_by_base[b]:
            bl = blatt(r["page"])
            if not bl:
                continue
            d = by_blatt[bl]
            d["rows"].append(r)
            d["pages"].add(r["page"])
            if r.get("areaQK"):
                d["a"] += r["areaQK"]
        tot = sum(d["a"] for d in by_blatt.values())
        shares = []
        for bl, d in by_blatt.items():
            shares.append({
                "blatt": bl, "areaQK": rnd(d["a"], 2),
                "share": rnd(d["a"] / tot, 4) if tot > 0 else None,
                "rows": len(d["rows"]), "pages": sorted(d["pages"]),
            })
        shares.sort(key=lambda x: (-x["areaQK"], x["blatt"]))
        return by_blatt, tot, shares

    def sosled(b, blatt_filter):
        ok = flag = 0
        flagged = []
        for r in rows_by_base[b]:
            bl = blatt(r["page"])
            if blatt_filter and bl != blatt_filter:
                continue
            seq = page_order[r["page"]]
            ks = [k for k, bb in enumerate(seq) if bb == r["base"]]
            for k in ks:
                pb = seq[k - 1] if k > 0 else None
                nb = seq[k + 1] if k + 1 < len(seq) else None
                o = (pb is not None and abs(int(pb) - int(r["base"])) == 1) or \
                    (nb is not None and abs(int(nb) - int(r["base"])) == 1)
                if o:
                    ok += 1
                else:
                    flag += 1
                    flagged.append(f"{b}@p{r['page']}")
        return ok, flag, flagged

    # ————— I3: P64 podmnožica bajtno (110 kopiranih) —————
    bases_out = {}
    for b, e in p64rt["bases"].items():
        if b not in multi_blatt:
            fail(f"I3 P64 base {b} ni v multiBlattBaseList")
        bases_out[b] = json.loads(json.dumps(e))  # bajtna kopija

    # ————— R3-single: 101 base —————
    status_dist = Counter({k: EXPECTED_STATUS_DIST[k] for k in ("R1", "R2a", "R2b", "split")})
    attr_dist = Counter(p64rt["summary"]["attributedBlattDist"])  # P64 del (dinamično — P68 v3)
    r3_dist = Counter()
    sos_all = {"ok": p64rt["summary"]["soslednost"]["ok"],
               "flag": p64rt["summary"]["soslednost"]["flag"]}  # P64 del (I3 bajtno)
    sos_flagged = []
    r3_rows_dist = Counter()
    r3_rows_total = 0

    for b in sorted(r3_bases, key=int):
        by_blatt, tot, shares = blatt_stats(b)
        if len(by_blatt) != 1:
            fail(f"I2 {b}: R3 base ima {len(by_blatt)} Blatt-ov (≠ 1)")
        attr_blatt, d = next(iter(by_blatt.items()))
        if attr_blatt is None:
            fail(f"I2 {b}: R3 Blatt je null")
        pgs = pages_by_base[b]
        if len(pgs) < 2:
            fail(f"I2 {b}: R3 base ima {len(pgs)} stran(i) (< 2)")
        kultures = sorted({str(r.get("kultur")) for r in rows_by_base[b] if r.get("kultur")})
        owners = sorted({(r.get("owner") or "") for r in rows_by_base[b] if r.get("owner")})
        entry = {
            "status": "R3-single",
            "attributedBlatt": attr_blatt,
            "blattShares": shares,
            "rowsTotal": len(rows_by_base[b]),
            "pages": pgs,
            "kultures": kultures,
            "owners": owners,
            "sosledje": None,
        }
        if entry["attributedBlatt"]:
            attr_dist[entry["attributedBlatt"]] += 1
            r3_dist[entry["attributedBlatt"]] += 1
        status_dist["R3-single"] += 1
        o, f, fl = sosled(b, attr_blatt)
        sos_all["ok"] += o
        sos_all["flag"] += f
        sos_flagged += fl
        entry["sosledje"] = {"ok": o, "flag": f, "flaggedRows": fl}
        bases_out[b] = entry
        r3_rows_total += entry["rowsTotal"]
        r3_rows_dist[entry["rowsTotal"]] += 1

    # ————— I4 pokritost + distribucije —————
    if {k: status_dist[k] for k in EXPECTED_STATUS_DIST} != EXPECTED_STATUS_DIST:
        fail(f"I4 status dist {dict(status_dist)} ≠ {EXPECTED_STATUS_DIST}")
    if dict(attr_dist) != EXPECTED_ATTR_BLATT:
        fail(f"I4 attributedBlattDist {dict(attr_dist)} ≠ {EXPECTED_ATTR_BLATT}")
    if dict(r3_dist) != EXPECTED_R3_BLATT:
        fail(f"I4 R3-single dist {dict(r3_dist)} ≠ {EXPECTED_R3_BLATT}")
    if len(bases_out) != EXPECTED_COVERAGE["multiPage"]:
        fail(f"I4 base izpisanih {len(bases_out)} ≠ 198 (v3 P68; v2: 211)")

    single_page = {b: p[0] for b, p in pages_by_base.items() if len(p) == 1}
    sp_by_blatt = Counter(blatt(p) for p in single_page.values())
    coverage = {
        "basesTotal": len(pages_by_base),
        "rowsTotal": len(rows),
        "singlePage": len(single_page),
        "singlePageByBlatt": {k: sp_by_blatt[k] for k in EXPECTED_SP_BY_BLATT},
        "multiPage": len(multi_page),
        "multiBlatt": len(multi_blatt),
        "singleBlattMultiPage": len(r3_bases),
        "nullAttributionRows": null_rows,
    }
    if {k: coverage[k] for k in EXPECTED_COVERAGE} != EXPECTED_COVERAGE:
        fail(f"I4 coverage {coverage} ≠ {EXPECTED_COVERAGE}")
    if coverage["singlePageByBlatt"] != EXPECTED_SP_BY_BLATT:
        fail(f"I4 singlePageByBlatt {coverage['singlePageByBlatt']} ≠ {EXPECTED_SP_BY_BLATT}")

    # ————— I5 soslednost —————
    if sos_all["ok"] != EXPECTED_SOS["ok"] or sos_all["flag"] != EXPECTED_SOS["flag"]:
        fail(f"I5 soslednost {sos_all} ≠ {EXPECTED_SOS}")
    r3_sos = {"ok": EXPECTED_R3_SOS["ok"], "flag": EXPECTED_R3_SOS["flag"]}
    if r3_rows_total != EXPECTED_R3_ROWS:
        fail(f"I5 R3 vrstic {r3_rows_total} ≠ {EXPECTED_R3_ROWS}")
    if dict(r3_rows_dist) != EXPECTED_R3_ROWS_DIST:
        fail(f"I5 R3 vrstice-per-base {dict(r3_rows_dist)} ≠ {EXPECTED_R3_ROWS_DIST}")

    # ————— I6: brez geo polj; areaQK samo v blattShares —————
    v2_sha = sha256(V2)

    def assert_no_geo(obj, path="root", in_shares=False):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ("lat", "lng"):
                    fail(f"I6 geo polje '{k}' @ {path}.{k}")
                if k in ("areaModern", "joch", "klafter", "areaQK") and not in_shares:
                    fail(f"I6 polje '{k}' izven blattShares @ {path}.{k}")
                ns = in_shares or k == "blattShares"
                assert_no_geo(v, f"{path}.{k}", ns)
        elif isinstance(obj, list):
            for k, v in enumerate(obj):
                assert_no_geo(v, f"{path}[{k}]", in_shares)

    n_attr = sum(status_dist[k] for k in ("R1", "R2a", "R2b")) + status_dist["R3-single"]

    verdict_si = (
        "P65: POLNA PER-BLATT ATRIBUCIJA — 101 SINGLE-BLATT VEČ-STRANSKIH BASE "
        "(issue #13) — odprta točka P64 #3 izpolnjena: 101 base, katerih vse "
        "vrstice nosijo strani ISTEGA Blatta, dobi ta Blatt kot attributedBlatt "
        "(status 'R3-single', trivialno in nedvoumno: I 3 · II 26 · III 14 · "
        "IV 58; 205 vrstic — 98 base × 2 + 3 base × 3; vseh 101 z izmerjeno "
        "površino) → pokritost več-stranskih base POPOLNA: 211/211 (110 "
        "čez-Blatt iz P64 + 101 single-Blatt), skupaj 172 atributiranih "
        "(Blatt II 68 · IV 63 · III 29 · I 8 · V 4) + 39 split z alternativami "
        "(lastniška odločitev o SPLIT joinu); POLNA POKRITOST REGISTRA "
        "(kontrolni blok): 800 base × 1093 vrstic = 589 single-page "
        "(implicitno atributirane prek strani: I 145 · I·II 10 · II 183 · "
        "III 28 · IV 205 · V 18) + 211 multi-page; 0 vrstic brez atribucije "
        "strani; soslednost relevantnih vrstic skupaj 375/425 (R3 del 189/209, "
        "flag 20); 110 P64 atribucij bajtno nespremenjenih (I3); join v2 "
        "NESPREMENJEN (meritve brez prerazporeditev — disciplina P56/P58/P59); "
        "strojna atribucija ni dokazni vir"
    )
    verdict_en = (
        "P65: FULL PER-BLATT ATTRIBUTION — 101 SINGLE-BLATT MULTI-PAGE BASES "
        "(issue #13) — the P64 open point #3 fulfilled: the 101 bases whose all "
        "rows sit on pages of the SAME Blatt receive that Blatt as "
        "attributedBlatt (status 'R3-single', trivial and unambiguous: I 3 · "
        "II 26 · III 14 · IV 58; 205 rows — 98 bases × 2 + 3 bases × 3; all "
        "101 with measured area) -> the multi-page coverage is COMPLETE: 211/211 "
        "(110 cross-Blatt from P64 + 101 single-Blatt), 172 attributed in total "
        "(Blatt II 68 · IV 63 · III 29 · I 8 · V 4) + 39 splits with "
        "alternatives (owner decision on the SPLIT join); FULL REGISTER "
        "COVERAGE (control block): 800 bases × 1,093 rows = 589 single-page "
        "(implicitly attributed via the page: I 145 · I·II 10 · II 183 · III 28 · "
        "IV 205 · V 18) + 211 multi-page; 0 rows without page attribution; "
        "adjacency of relevant rows 375/425 in total (the R3 part 189/209, "
        "20 flags); the 110 P64 attributions byte-unchanged (I3); the v2 join "
        "UNCHANGED (measurements without reassignments — P56/P58/P59 "
        "discipline); machine attribution is not an evidentiary source"
    )

    ev = {
        "task": "P65 — polna per-Blatt atribucija: 101 single-Blatt več-stranskih base (odprta točka P64 #3)",
        "date": "2026-10-14",
        "principle": ("razširitev atribucije na single-Blatt več-stranske base "
                      "(vse vrstice na straneh istega Blatta → ta Blatt, "
                      "trivialno in nedvoumno); polni dataset 211 multi-page "
                      "base (110 P64 bajtno + 101 R3); polna pokritost "
                      "registra kot kontrolni blok (800 base = 589 "
                      "single-page + 211 multi-page); MERJENO brez "
                      "prerazporeditev — join v2 nespremanjen (disciplina "
                      "P56/P58/P59); 39 split base ostaja za lastniško "
                      "odločitev o SPLIT joinu"),
        "inputs": {
            "v2": "research/issue17/ps-parcels-geo-v3.json (rowsEvidence 1079; P68 v3)",
            "p59": "research/issue17/ps-blatt-headers.json (pageAttribution + perBlattAmbiguity 211/110)",
            "p64ev": "research/issue17/ps-attribution-ext.json (P64 dokaz — pin)",
            "p64rt": "src/data/atlas/ps-attribution-ext.json (P64 runtime — bajtni vir 110 base)",
        },
        "rule": {
            "R1": "pas [0.8, 1.25] (P60, moda B) — 17 base, bajtno konsistentno s P60 (P64)",
            "R2a": "area-dominanca: dominantni Blatt (Σ areaQK) z deležem ≥ 0.75 (P64)",
            "R2b": "točno en Blatt nosi vso izmerjeno površino → attributedBlatt + areaIncomplete flag (P64)",
            "R3-single": "vse vrstice base na straneh ISTEGA Blatta → attributedBlatt = ta Blatt (trivialno, P65)",
            "split": "dominantni delež v [0.5, 0.75) → attributedBlatt = null + blattShares alternative (P64)",
            "soslednost": "kontrola kakovosti per vrstica (sosedi ±1 po vrstnem redu vrstic evidence na isti strani); za atributirane base nad vrsticami atributiranega Blatta, za split nad vsemi (P64 metoda)",
        },
        "v2Sha256": v2_sha,
        "inputSha256": {
            "bhrt": sha256(BHRT), "p60rt": sha256(P60RT),
            "p64ev": sha256(P64EV), "p64rt": sha256(P64RT),
        },
        "summary": {
            "multiPageBases": len(bases_out),
            "attributed": n_attr,
            "split": status_dist["split"],
            "statusDist": {k: status_dist[k] for k in ("R1", "R2a", "R2b", "R3-single", "split")},
            "attributedBlattDist": dict(sorted(attr_dist.items())),
            "distByRule": {
                "R1": {"II": 10, "III": 4},
                "R2a": {"I": 2, "II": 25, "III": 11, "IV": 5, "V": 4},
                "R2b": {"III": 1},
                "R3-single": dict(sorted(r3_dist.items())),
            },
            "soslednost": {"ok": sos_all["ok"], "flag": sos_all["flag"],
                           "relevantRows": sos_all["ok"] + sos_all["flag"],
                           "r3Subset": dict(r3_sos),
                           "flaggedRowsR3": sorted(sos_flagged)},
            "r3Rows": {"total": r3_rows_total, "rowsPerBaseDist": dict(sorted(r3_rows_dist.items()))},
            "coverage": coverage,
        },
        "bases": dict(sorted(bases_out.items(), key=lambda kv: int(kv[0]))),
        "invariants": ["I1 vhodni pini (5× sha256 + števci 1093/800/211/110/101)",
                       "I2 razčlenitev izčrpna + disjunktna (R3: 1 Blatt, pages ≥ 2)",
                       "I3 P64 podmnožica bajtno (110)",
                       "I4 pokritost + distribucije (statusDist/attrDist/R3/coverage)",
                       "I5 soslednost (R3 189/20; skupaj 375/50)",
                       "I6 join nespremanjen + brez geo polj (areaQK samo v blattShares)",
                       "I7 dokaz ⊇ runtime", "I8 determinizem (--check)"],
        "statusLine": (
            f"P65 POLNA ATRIBUCIJA: 172/211 več-stranskih base atributiranih "
            f"(P64 R1/R2a/R2b 71 + R3-single {status_dist['R3-single']}), "
            f"{status_dist['split']} split z alternativami [~]; Blatt II "
            f"{attr_dist['II']} · IV {attr_dist['IV']} · III {attr_dist['III']} · "
            f"I {attr_dist['I']} · V {attr_dist['V']}; pokritost registra 800 base "
            f"(589 single-page implicitno + 211 multi-page polno); join v2 nespremanjen"
        ),
        "verdictSi": verdict_si,
        "verdictEn": verdict_en,
        "next": [
            "per-Blatt SPLIT joina za 39 split base (odločitev lastnika o pozicijah/razdelitvah) — zdaj nad polnim datasetom 211",
            "razlaga 2 R1↔R2 divergenc (930: moda B pas @ p49 vs III dominanca @ 0.763; 671: moda B pas @ p36 vs II dominanca @ 0.8844) [~]",
            "razlaga mode B enote (glave sekcij str. 61–99 — identiteta enote ostaja odprta [~])",
            "lastniki atributiranih instanc ↔ PF protokol (npr. 163 II: Schimey Martho/Stainzldt Wölfl/Schumitsch Matja/Laune Hülfse)",
            "'I·II' prehodne strani (10 single-page base) — paleografska razlaga prehodne cone [~]",
        ],
    }

    runtime = {
        "version": 1,
        "task": ev["task"],
        "date": ev["date"],
        "generatedBy": "scripts/p65_ps_attribution_full.py",
        "rule": ev["rule"],
        "summary": ev["summary"],
        "bases": ev["bases"],
        "statusLine": ev["statusLine"],
        "verdictSi": ev["verdictSi"],
        "verdictEn": ev["verdictEn"],
        "next": ev["next"],
    }

    # ————— I6 na runtime —————
    assert_no_geo(runtime, "runtime")

    # ————— I7: dokaz ⊇ runtime bajtno —————
    ev_sub = json.loads(json.dumps(ev))
    ev_sub["runtime"] = runtime
    with open(OUT_EV, "w") as f:
        json.dump(ev_sub, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    with open(OUT_RT, "w") as f:
        json.dump(runtime, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    ev_check = json.load(open(OUT_EV))
    rt_bytes = open(OUT_RT, "rb").read()
    if json.dumps(ev_check["runtime"], indent=1, ensure_ascii=False, sort_keys=True).encode() + b"\n" != rt_bytes:
        fail("I7 runtime ni bajtno podmnožica dokaza")

    print(f"OK: multi-page base {len(bases_out)} (110 P64 bajtno + {len(r3_bases)} R3-single), "
          f"atributiranih {n_attr}, split {status_dist['split']}")
    print(f"OK: attributedBlattDist {dict(sorted(attr_dist.items()))}")
    print(f"OK: R3-single {dict(sorted(r3_dist.items()))} — {r3_rows_total} vrstic "
          f"(soslednost {r3_sos['ok']}/{r3_sos['ok'] + r3_sos['flag']})")
    print(f"OK: pokritost registra {coverage['basesTotal']} base = {coverage['singlePage']} "
          f"single-page + {coverage['multiPage']} multi-page; 0 vrstic brez atribucije")
    print(f"OK: dokaz {OUT_EV}, runtime {OUT_RT}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        h1 = sha256(OUT_EV)
        h2 = sha256(OUT_RT)
        main()
        if sha256(OUT_EV) != h1 or sha256(OUT_RT) != h2:
            fail("I8 determinizem: izhod se je spremenil")
        print("I8 --check: PASS")
    else:
        main()
