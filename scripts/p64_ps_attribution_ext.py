#!/usr/bin/env python3
# P64 — RAZŠIRITEV PER-BLATT ATRIBUCIJE NA VSEH 110 ČEZ-BLATT BASE
# (odprta točka P60/P62 #7 — "razširiti atribucijo na vseh 110 čez-Blatt base";
#  predpogoj izpolnjen: polna pokritost glav listov 135/135 × 2 — P62/P63).
#
# P60 je atributiral 17 ruleCandidate base s pravilom pasu [0.8, 1.25] (moda B).
# P64 razširi atribucijo na preostalih 93 čez-Blatt base z MERJENO hierarhijo
# pravil (deterministično, brez prerazporeditev joina — disciplina P56/P58/P59):
#
#   R1 (pas, P60)    — 17 base: attributedBlatt = pas-instanca [0.8, 1.25]
#                      (bajtno konsistentno s P60 evidence; prednost pred R2).
#   R2a (dominanca)  — base z ≥2 Blatt-i, ki nosijo areaQK > 0: če ima
#                      dominantni Blatt delež Σ areaQK ≥ 0.75 → attributedBlatt.
#   R2b (ena area)   — točno en Blatt nosi vso izmerjeno površino (ostali
#                      Blatt-i brez areaQK) → attributedBlatt = ta Blatt,
#                      flag areaIncomplete (npr. 1605: II 2688 QK vs IV brez).
#   split            — dominantni delež v [0.5, 0.75) → attributedBlatt = null,
#                      alternatives = blattShares (pravi split po Blattih;
#                      kandidati za lastniško odločitev o SPLIT joinu).
#   fragmented       — dominantni delež < 0.5 (MERJENO: 0 primerov).
#
# Konsistenca R1↔R2 (za vseh 17 tudi area-dominanca): 15 soglasij, 2 merjeni
# divergence (930: R1 II vs R2 dom III @ 0.763; 671: R1 I vs R2 dom II @ 0.8844)
# — dokumentirana, R1 ima prednost (bajtna kompatibilnost s P60).
#
# Join v2 (1093 vrstic) ostaja NESPREMENJEN — izpisi ne vsebujejo pozicij;
# površine (Σ areaQK po Blattih) so meritve za atribucijo, ne join polja.
#
# Vhodi (committed):
#   research/issue17/ps-parcels-geo-v2.json     — vrstice v2 (rowsEvidence)
#   research/issue17/ps-blatt-headers.json      — P59 dokaz (pageAttribution,
#                                                 perBlattAmbiguity 110/17)
#   research/issue17/ps-perblatt-attribution.json — P60 dokaz (R1 baze)
# Izhodi:
#   research/issue17/ps-attribution-ext.json    (dokaz)
#   src/data/atlas/ps-attribution-ext.json      (runtime, bajtno projekcija)
#
# Invarianti (FAIL ob padu):
#   I1 vhodni pini: 110 multi-Blatt == P59, 17 ruleCandidate == P59,
#      sha256 runtime vhodov (bhrt efe39f41…, p60rt 28465b3e…, v2 ev ebb8f729…)
#   I2 re-izpeljava instanc == P59 (rows/pages/median Δ<1e-9) za vseh 110
#   I3 R1 == P60: attributedBlatt + inBand (median/pages/rows) bajtno
#   I4 pokritost pravil: R1 17 · R2a 53 · R2b 1 · split 39 · fragmented 0 = 110;
#      atributiranih 71 (Blatt II 42 · III 15 · I 5 · IV 5 · V 4);
#      občutljivost praga: 69/63/58/53/45/24 @ ≥0.6/0.6667/0.7/0.75/0.8/0.9
#   I5 soslednost števci: v3 175/29 (R1 del 19/1; flagged vsebuje 934@p99; v2: 186/30)
#   I6 join nespremanjen (sha256 v2 vhoda; brez lat/lng povsod; areaQK samo
#      v blattShares in rows-detaljah)
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
P60 = os.path.join(ROOT, "research/issue17/ps-perblatt-attribution.json")
BHRT = os.path.join(ROOT, "src/data/atlas/ps-blatt-headers.json")
P60RT = os.path.join(ROOT, "src/data/atlas/ps-perblatt-attribution.json")
OUT_EV = os.path.join(ROOT, "research/issue17/ps-attribution-ext.json")
OUT_RT = os.path.join(ROOT, "src/data/atlas/ps-attribution-ext.json")

RATIO_LO, RATIO_HI = 0.8, 1.25      # P60 pas (moda B)
DOM_THR = 0.75                       # R2a prag dominance
SPLIT_LO = 0.5                       # pod tem = fragmented

PIN_V2_EV_SHA = "af7479e428182f381d3a2537896493d7cf86210fac7027221e22ac2aea218b53"  # P68: v3 dokaz (1079; + join blok)
PIN_BHRT_SHA = "f4c4dedcd6c65d4d1480b4124ae93d00304be2f24f30aa74ca5d0c6ff8c9efe6"  # P68: v3 re-run
PIN_P60RT_SHA = "c42bf221141e46aee0c387506bdf594c24373d41b19420fe2fc8fc2b7047d6e4"  # P68: v3 re-run

EXPECTED_STATUS_DIST = {"R1": 14, "R2a": 47, "R2b": 1, "split": 36, "fragmented": 0}  # P68 v3 (v2: R1 17/R2a 53/R2b 1/split 39)
EXPECTED_ATTR_BLATT = {"II": 35, "I": 2, "III": 16, "IV": 5, "V": 4}  # P68 v3 (v2: II 42/III 15/I 5/IV 5/V 4)
EXPECTED_R2A = {"I": 2, "II": 25, "III": 11, "IV": 5, "V": 4}  # P68 v3 (v2: I 4/II 29/III 11/IV 5/V 4)
EXPECTED_SPLIT_DOM = {"I": 1, "II": 16, "III": 10, "IV": 5, "V": 4}  # P68 v3 (v2: I 1/II 19/III 9/IV 6/V 4)
EXPECTED_SENS = {"0.6": 63, "0.6667": 57, "0.7": 52, "0.75": 47, "0.8": 39, "0.9": 20}  # P68 v3 (v2: 69/63/58/53/45/24)
EXPECTED_SOS = {"ok": 175, "flag": 29}  # P68 v3 (v2: 186/30)
EXPECTED_R1_SOS = {"ok": 19, "flag": 1}  # P68 v3 (v2: 21/2)
EXPECTED_DIVERGE = {"930": ("II", "III")}  # P68 v3 (671 RAZPADLA — II instanca = 1691; P67 part C)


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


def median(vals):
    s = sorted(vals)
    return s[len(s) // 2] if s else None


def main():
    v2 = json.load(open(V2))
    p59 = json.load(open(P59))
    p60 = json.load(open(P60))
    rows = v2["rowsEvidence"]
    page_attr = p59["pageAttribution"]
    multi = p59["perBlattAmbiguity"]["multiBlattBaseList"]
    cands = p59["perBlattAmbiguity"]["ruleCandidateBases"]
    p59_inst = p59["perBlattAmbiguity"]["instances"]

    # ————— I1 vhodni pini —————
    if sha256(V2) != PIN_V2_EV_SHA:
        fail("I1 sha256 v2 vhoda se je spremenil (drift — preveri P58 chain)")
    if sha256(BHRT) != PIN_BHRT_SHA:
        fail("I1 sha256 runtime ps-blatt-headers.json ≠ pin (drift)")
    if sha256(P60RT) != PIN_P60RT_SHA:
        fail("I1 sha256 runtime ps-perblatt-attribution.json ≠ pin (drift)")
    if len(multi) != 98:
        fail(f"I1 multiBlattBaseList {len(multi)} ≠ 98 (v3 P68; v2: 110)")
    if len(cands) != 14:
        fail(f"I1 ruleCandidate {len(cands)} ≠ 14 (v3 P68; v2: 17)")
    if sorted(cands) != sorted(p60["bases"].keys()):
        fail("I1 ruleCandidate ≠ P60 bases ključi")
    p60rt = json.load(open(P60RT))
    if sorted(p60rt["bases"].keys()) != sorted(cands):
        fail("I1 runtime P60 bases ≠ ruleCandidate")

    # ————— vrstice po base + vrstni red per stran (soslednost, P60 metoda) —————
    rows_by_base = defaultdict(list)
    page_order = defaultdict(list)
    for r in rows:
        rows_by_base[r["base"]].append(r)
        page_order[r["page"]].append(r["base"])

    def blatt_stats(b):
        """Per-Blatt: Σ areaQK, vrstice, strani (vrstice brez pageAttribution preskočene)."""
        by_blatt = defaultdict(lambda: {"a": 0.0, "rows": [], "pages": set()})
        for r in rows_by_base[b]:
            bl = page_attr.get(str(r["page"]), {}).get("blatt")
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
            bl = page_attr.get(str(r["page"]), {}).get("blatt")
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

    # ————— obdelava vseh 110 —————
    bases_out = {}
    status_dist = Counter()
    attr_dist = Counter()
    r1_dist = Counter()
    r2a_dist = Counter()
    r2b_dist = Counter()
    split_dom = Counter()
    sens = Counter()
    sos_all = {"ok": 0, "flag": 0}
    sos_flagged = []
    r1_sos = {"ok": 0, "flag": 0}
    divergences = []

    for b in sorted(multi, key=int):
        by_blatt, tot, shares = blatt_stats(b)

        # ————— I2 re-izpeljava instanc == P59 —————
        ref = p59_inst.get(b) or p59_inst.get(str(b))
        if not ref:
            fail(f"I2 P59 nima instanc za {b}")
        ref_map = {i["blatt"]: i for i in ref["instances"]}
        new_map = {bl: {"rows": len(d["rows"]), "pages": sorted(d["pages"]),
                        "medianRatio": median([r["ratio"] for r in d["rows"] if r.get("ratio")])}
                   for bl, d in by_blatt.items()}
        if set(ref_map) != set(new_map):
            fail(f"I2 {b}: blatt množica ≠ P59 ({sorted(new_map)} vs {sorted(ref_map)})")
        for bl, i in new_map.items():
            j = ref_map[bl]
            if i["rows"] != j["rows"] or i["pages"] != j["pages"]:
                fail(f"I2 {b}/{bl}: rows/pages ≠ P59")
            if (i["medianRatio"] is None) != (j["medianRatio"] is None):
                fail(f"I2 {b}/{bl}: median None-asimetrija vs P59")
            if i["medianRatio"] is not None and \
                    abs(i["medianRatio"] - j["medianRatio"]) > 1e-9:
                fail(f"I2 {b}/{bl}: median ≠ P59")

        kultures = sorted({str(r.get("kultur")) for r in rows_by_base[b] if r.get("kultur")})
        owners = sorted({(r.get("owner") or "") for r in rows_by_base[b] if r.get("owner")})
        pages = sorted({r["page"] for r in rows_by_base[b]})
        entry = {
            "status": None, "attributedBlatt": None,
            "blattShares": shares, "rowsTotal": len(rows_by_base[b]),
            "pages": pages, "kultures": kultures, "owners": owners,
            "sosledje": None,
        }

        # ————— pravila —————
        if b in cands:
            # R1 (pas, P60) — I3: bajtno == P60
            in_band = [(bl, i) for bl, i in new_map.items()
                       if i["medianRatio"] and RATIO_LO <= i["medianRatio"] <= RATIO_HI]
            if len(in_band) != 1:
                fail(f"I3 {b}: pas-instanc {len(in_band)} ≠ 1")
            attr_blatt, attr = in_band[0]
            p60b = p60["bases"][b]
            if attr_blatt != p60b["attributedBlatt"]:
                fail(f"I3 {b}: attributedBlatt {attr_blatt} ≠ P60 {p60b['attributedBlatt']}")
            if abs(attr["medianRatio"] - p60b["inBand"]["medianRatio"]) > 1e-9:
                fail(f"I3 {b}: inBand median ≠ P60")
            if attr["pages"] != p60b["inBand"]["pages"]:
                fail(f"I3 {b}: inBand pages ≠ P60")
            entry["status"] = "R1"
            entry["attributedBlatt"] = attr_blatt
            r1_dist[attr_blatt] += 1
            entry["pas"] = {"medianRatio": attr["medianRatio"], "pages": attr["pages"],
                            "rows": p60b["inBand"]["rows"]}
            # konsistenca z R2 (area-dominanca)
            with_area = [s for s in shares if (s["areaQK"] or 0) > 0]
            if tot > 0 and with_area:
                dom = shares[0]
                if dom["blatt"] != attr_blatt:
                    divergences.append({"base": b, "r1": attr_blatt,
                                        "r2Dominant": dom["blatt"], "share": dom["share"]})
            status_dist["R1"] += 1
            o, f, fl = sosled(b, attr_blatt)
            r1_sos["ok"] += o
            r1_sos["flag"] += f
        else:
            with_area = [s for s in shares if (s["areaQK"] or 0) > 0]
            if tot <= 0:
                fail(f"I4 {b}: brez izmerjene površine (NOAREA — ni v pinih)")
            if len(with_area) == 1:
                entry["status"] = "R2b"
                entry["attributedBlatt"] = with_area[0]["blatt"]
                r2b_dist[with_area[0]["blatt"]] += 1
                entry["areaIncomplete"] = True
                entry["arealessBlatts"] = [s["blatt"] for s in shares
                                           if (s["areaQK"] or 0) == 0]
                status_dist["R2b"] += 1
                o, f, fl = sosled(b, entry["attributedBlatt"])
            else:
                dom = shares[0]
                sh = dom["share"]
                for t in (0.6, 0.6667, 0.7, 0.75, 0.8, 0.9):
                    if sh >= t:
                        sens[str(t)] += 1
                if sh >= DOM_THR:
                    entry["status"] = "R2a"
                    entry["attributedBlatt"] = dom["blatt"]
                    status_dist["R2a"] += 1
                    o, f, fl = sosled(b, entry["attributedBlatt"])
                elif sh >= SPLIT_LO:
                    entry["status"] = "split"
                    status_dist["split"] += 1
                    split_dom[dom["blatt"]] += 1
                    o, f, fl = sosled(b, None)
                else:
                    entry["status"] = "fragmented"
                    status_dist["fragmented"] += 1
                    split_dom[dom["blatt"]] += 1
                    o, f, fl = sosled(b, None)

        if entry["attributedBlatt"]:
            attr_dist[entry["attributedBlatt"]] += 1
            if entry["status"] == "R2a":
                r2a_dist[entry["attributedBlatt"]] += 1
        sos_all["ok"] += o
        sos_all["flag"] += f
        sos_flagged += fl
        entry["sosledje"] = {"ok": o, "flag": f, "flaggedRows": fl}
        bases_out[b] = entry

    # ————— I4 pokritost + distribucije —————
    if set(status_dist) - set(EXPECTED_STATUS_DIST) or \
            {k: status_dist[k] for k in EXPECTED_STATUS_DIST} != EXPECTED_STATUS_DIST:
        fail(f"I4 status dist {dict(status_dist)} ≠ {EXPECTED_STATUS_DIST}")
    if dict(attr_dist) != EXPECTED_ATTR_BLATT:
        fail(f"I4 attributedBlattDist {dict(attr_dist)} ≠ {EXPECTED_ATTR_BLATT}")
    if dict(r2a_dist) != EXPECTED_R2A:
        fail(f"I4 R2a dist {dict(r2a_dist)} ≠ {EXPECTED_R2A}")
    if dict(split_dom) != EXPECTED_SPLIT_DOM:
        fail(f"I4 split dominant dist {dict(split_dom)} ≠ {EXPECTED_SPLIT_DOM}")
    if {k: sens[k] for k in EXPECTED_SENS} != EXPECTED_SENS:
        fail(f"I4 občutljivost praga {dict(sens)} ≠ {EXPECTED_SENS}")
    div_map = {d["base"]: (d["r1"], d["r2Dominant"]) for d in divergences}
    if div_map != EXPECTED_DIVERGE:
        fail(f"I4 R1↔R2 divergence {div_map} ≠ {EXPECTED_DIVERGE}")

    # ————— I5 soslednost —————
    if sos_all["ok"] != EXPECTED_SOS["ok"] or sos_all["flag"] != EXPECTED_SOS["flag"]:
        fail(f"I5 soslednost {sos_all} ≠ {EXPECTED_SOS}")
    if r1_sos["ok"] != EXPECTED_R1_SOS["ok"] or r1_sos["flag"] != EXPECTED_R1_SOS["flag"]:
        fail(f"I5 R1 soslednost {r1_sos} ≠ {EXPECTED_R1_SOS}")
    if "934@p99" not in sos_flagged:  # P68 v3: 671@p36 izpadla (671 single-Blatt po renum; P67 part C)
        fail("I5 flaggedRows brez 934@p99")

    # ————— I6: brez geo polj; areaQK samo v blattShares + rows —————
    v2_sha = sha256(V2)

    def assert_no_geo(obj, path="root", in_rows=False, in_shares=False):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ("lat", "lng"):
                    fail(f"I6 geo polje '{k}' @ {path}.{k}")
                if k in ("areaModern", "joch", "klafter", "areaQK") and not (in_rows or in_shares):
                    fail(f"I6 polje '{k}' izven rows/blattShares @ {path}.{k}")
                nr = in_rows or k == "rows"
                ns = in_shares or k == "blattShares"
                assert_no_geo(v, f"{path}.{k}", nr, ns)
        elif isinstance(obj, list):
            for k, v in enumerate(obj):
                assert_no_geo(v, f"{path}[{k}]", in_rows, in_shares)

    n_attr = status_dist["R1"] + status_dist["R2a"] + status_dist["R2b"]

    verdict_si = (
        "P64: RAZŠIRITEV PER-BLATT ATRIBUCIJE NA VSEH 110 ČEZ-BLATT BASE (issue #13) — "
        "odprta točka P60/P62 #7 izpolnjena z merjeno hierarhijo pravil: R1 pas "
        "[0.8, 1.25] (P60, 17 base — bajtno konsistentno) · R2a area-dominanca ≥ 0.75 "
        "(53 base: II 29 · III 11 · IV 5 · I 4 · V 4) · R2b ena sama Blatt s površino "
        "(1: 1605 — II 2688 QK, IV brez areaQK [~]) → skupaj 71/110 atributiranih "
        "(Blatt II 42 · III 15 · I 5 · IV 5 · V 4); 39 base status 'split' "
        "(dominantni delež 0.5–0.75: II 19 · III 9 · IV 6 · V 4 · I 1) z "
        "alternativami po deležih — kandidati za lastniško odločitev o per-Blatt "
        "SPLIT joinu; KONSISTENCA R1↔R2: 15/17 soglasij, 2 merjeni divergence "
        "(930: R1 II vs R2 dom III @ 0.763; 671: R1 I vs R2 dom II @ 0.8844) — "
        "R1 (moda B pas) ima prednost [~]; občutljivost praga 0.75: 24 base @ ≥0.9, "
        "45 @ ≥0.8, 53 @ ≥0.75, 58 @ ≥0.7, 63 @ ≥2/3, 69 @ ≥0.6 (od 92 z izmerjeno "
        "površino); soslednost relevantnih vrstic 186/216 (flag 30 — prečrtane "
        "vrstice [~]; R1 del 21/23 kot P60); join v2 NESPREMENJEN (meritve brez "
        "prerazporeditev — disciplina P56/P58/P59); strojna atribucija ni dokazni vir"
    )
    verdict_en = (
        "P64: PER-BLATT ATTRIBUTION EXTENDED TO ALL 110 CROSS-BLATT BASES (issue #13) — "
        "the P60/P62 open point #7 fulfilled with a measured rule hierarchy: R1 band "
        "[0.8, 1.25] (P60, 17 bases — byte-consistent) · R2a area dominance >= 0.75 "
        "(53 bases: II 29 · III 11 · IV 5 · I 4 · V 4) · R2b a single Blatt holding all "
        "measured area (1: 1605 — II 2688 QK, IV without areaQK [~]) -> 71/110 attributed "
        "in total (Blatt II 42 · III 15 · I 5 · IV 5 · V 4); 39 bases status 'split' "
        "(dominant share 0.5-0.75: II 19 · III 9 · IV 6 · V 4 · I 1) with per-share "
        "alternatives — candidates for the owner decision on the per-Blatt SPLIT join; "
        "R1-vs-R2 CONSISTENCY: 15/17 agreements, 2 measured divergences (930: R1 II vs "
        "R2 dom III @ 0.763; 671: R1 I vs R2 dom II @ 0.8844) — R1 (mode B band) takes "
        "precedence [~]; threshold sensitivity at 0.75: 24 bases @ >=0.9, 45 @ >=0.8, "
        "53 @ >=0.75, 58 @ >=0.7, 63 @ >=2/3, 69 @ >=0.6 (of 92 with measured area); "
        "adjacency of relevant rows 186/216 (30 flags — crossed-out rows [~]; the R1 "
        "part 21/23 as P60); the v2 join UNCHANGED (measurements without reassignments "
        "— P56/P58/P59 discipline); machine attribution is not an evidentiary source"
    )

    ev = {
        "task": "P64 — razširitev per-Blatt atribucije na vseh 110 čez-Blatt base (odprta točka P60/P62 #7)",
        "date": "2026-10-14",
        "principle": ("razširitev atribucije z merjeno hierarhijo pravil (R1 pas > R2a "
                      "dominanca ≥ 0.75 > R2b ena-area > split); MERJENO brez "
                      "prerazporeditev — join v2 nespremanjen (disciplina P56/P58/P59); "
                      "split base ostajajo neatributirane z alternativami (odločitev "
                      "lastnika); konsistenca R1↔R2 dokumentirana (2 divergence)"),
        "inputs": {
            "v2": "research/issue17/ps-parcels-geo-v2.json (rowsEvidence 1093)",
            "p59": "research/issue17/ps-blatt-headers.json (pageAttribution + perBlattAmbiguity 110/17)",
            "p60": "research/issue17/ps-perblatt-attribution.json (R1 baze 17)",
        },
        "rule": {
            "R1": "pas [0.8, 1.25] (P60, moda B) — 17 base, bajtno konsistentno s P60",
            "R2a": f"area-dominanca: dominantni Blatt (Σ areaQK) z deležem ≥ {DOM_THR}",
            "R2b": "točno en Blatt nosi vso izmerjeno površino → attributedBlatt + areaIncomplete flag",
            "split": "dominantni delež v [0.5, 0.75) → attributedBlatt = null + blattShares alternative",
            "fragmented": f"dominantni delež < {SPLIT_LO} (MERJENO: 0 primerov)",
            "soslednost": "kontrola kakovosti per vrstica (sosedi ±1 po vrstnem redu vrstic evidence na isti strani); za atributirane base nad vrsticami atributiranega Blatta, za split nad vsemi",
        },
        "v2Sha256": v2_sha,
        "inputSha256": {"bhrt": sha256(BHRT), "p60rt": sha256(P60RT)},
        "summary": {
            "bases": len(bases_out),
            "attributed": n_attr,
            "statusDist": {k: status_dist[k] for k in ("R1", "R2a", "R2b", "split", "fragmented")},
            "attributedBlattDist": dict(sorted(attr_dist.items())),
            "distByRule": {"R1": dict(sorted(r1_dist.items())),
                           "R2a": dict(sorted(r2a_dist.items())),
                           "R2b": dict(sorted(r2b_dist.items()))},
            "splitDominantDist": dict(sorted(split_dom.items())),
            "thresholdSensitivity": {k: sens[k] for k in sorted(sens)},
            "soslednost": {"ok": sos_all["ok"], "flag": sos_all["flag"],
                           "relevantRows": sos_all["ok"] + sos_all["flag"],
                           "r1Subset": dict(r1_sos),
                           "flaggedRows": sorted(sos_flagged)},
            "r1R2Consistency": {"agree": 17 - len(divergences), "diverge": len(divergences),
                                "divergentBases": divergences},
        },
        "bases": bases_out,
        "invariants": ["I1 vhodni pini (110/17 + sha256)", "I2 instance == P59",
                       "I3 R1 == P60 bajtno", "I4 pokritost pravil + distribucije",
                       "I5 soslednost števci", "I6 join nespremanjen + brez geo polj",
                       "I7 dokaz ⊇ runtime", "I8 determinizem (--check)"],
        "statusLine": (
            f"P64 RAZŠIRITEV ATRIBUCIJE: {n_attr}/110 čez-Blatt base atributiranih "
            f"(R1 pas 17 · R2a dominanca ≥0.75 {status_dist['R2a']} · R2b {status_dist['R2b']}), "
            f"{status_dist['split']} split z alternativami [~]; R1↔R2 soglasje "
            f"{17 - len(divergences)}/17 ({', '.join(sorted(div_map))} [~]); "
            f"Blatt II {attr_dist['II']} · III {attr_dist['III']} · I {attr_dist['I']} · "
            f"IV {attr_dist['IV']} · V {attr_dist['V']}; join v2 nespremanjen"
        ),
        "verdictSi": verdict_si,
        "verdictEn": verdict_en,
        "next": [
            "per-Blatt SPLIT joina za 71 atributiranih base (odločitev lastnika o pozicijah) — 39 split base z alternativami po deležih",
            "razlaga 2 R1↔R2 divergenc (930: moda B pas @ p49 vs III dominanca @ 0.763; 671: moda B pas @ p36 vs II dominanca @ 0.8844) [~]",
            "atribucija 101 single-Blatt več-stranskih base (211 − 110; instanca enotna po Blattu — trivialno, za SPLIT join potrebna lastniška odločitev)",
            "razlaga mode B enote (glave sekcij str. 61–99 — identiteta enote ostaja odprta [~])",
            "lastniki atributiranih instanc ↔ PF protokol (npr. 163 II: Schimey Martho/Stainzldt Wölfl/Schumitsch Matja/Laune Hülfse)",
        ],
    }

    runtime = {
        "version": 1,
        "task": ev["task"],
        "date": ev["date"],
        "generatedBy": "scripts/p64_ps_attribution_ext.py",
        "rule": ev["rule"],
        "summary": ev["summary"],
        "bases": {b: dict(e) for b, e in bases_out.items()},
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

    print(f"OK: base {len(bases_out)}, atributiranih {n_attr} "
          f"(R1 {status_dist['R1']} · R2a {status_dist['R2a']} · R2b {status_dist['R2b']}), "
          f"split {status_dist['split']}, fragmented {status_dist['fragmented']}")
    print(f"OK: attributedBlattDist {dict(sorted(attr_dist.items()))}")
    print(f"OK: R1↔R2 {17 - len(divergences)}/17 soglasij, divergence {div_map}")
    print(f"OK: soslednost {sos_all['ok']}/{sos_all['ok'] + sos_all['flag']} "
          f"(R1 del {r1_sos['ok']}/{r1_sos['ok'] + r1_sos['flag']})")
    print(f"OK: dokaz {OUT_EV}, runtime {OUT_RT}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        h1 = sha256(OUT_EV)
        main()
        if sha256(OUT_EV) != h1:
            fail("I8 determinizem: izhod se je spremenil")
        print("I8 --check: PASS")
    else:
        main()
