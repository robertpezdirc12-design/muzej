#!/usr/bin/env python3
# P60 — PER-BLATT ATRIBUCIJA ruleCandidate base (odprta točka P59 #2).
#
# P59 je MERIL per-Blatt instancе 211 dvoumnih base v2 in označil 17
# ruleCandidate: baza z TOČNO eno instanco z median razmerjem v pasu
# [0.8, 1.25]. P60 to pravilo IZVEDE kot atribucijo — merjeno, brez
# prerazporeditev joina (disciplina P56/P58/P59):
#   * vsaka od 17 base dobi attributedBlatt (pas-instanca) + celotno
#     strukturo instanc (median, strani, kulture, lastniki),
#   * soslednost = kontrola kakovosti per vrstica (sosedi ±1 po vrstnem
#     redu vrstic evidence na isti strani),
#   * strukturna meritev: strani pas-instanc nosijo 100 % več-stranske
#     base (re-listing; Kultur-Tabellen interpretacija [~]),
#   * unit-semantics opomba: pas [0.8, 1.25] ujema modo B (ratio ≈ 1),
#     ne modo A (≈ 3.597 = 1 QK → m²) — absolutna korespondenca ostaja
#     ODPRTO vprašanje (faktor ~3.6 med modama).
# Join v2 (1093 vrstic) ostaje NESPREMENJEN — izpisi ne vsebujejo pozicij
# ali površin (I4 po gradnji).
#
# Vhodi (committed):
#   research/issue17/ps-parcels-geo-v2.json  — vrstice v2 (rowsEvidence)
#   research/issue17/ps-blatt-headers.json   — P59 dokaz (pageAttribution,
#                                              instances, ruleCandidateBases)
# Izhodi:
#   research/issue17/ps-perblatt-attribution.json (dokaz)
#   src/data/atlas/ps-perblatt-attribution.json   (runtime, bajtno projekcija)
#
# Invarianti (FAIL ob padu):
#   I1 ruleCandidate == P59 pin (17 base, enak seznam)
#   I2 re-izpeljava instanc == P59 instances (blatt/strani/median, Δ<1e-9)
#   I3 vsaka base ima TOČNO eno pas-instanco → attributedBlatt
#   I4 join nespremenjen (sha256 v2 vhoda; izpisi brez lat/lng/area polj)
#   I5 soslednost izračunana za vse pas-vrstice (števec pinan)
#   I6 determinizem — --check bajtno identično
#   I7 dokaz ⊇ runtime (bajtno podmnožica)
import hashlib
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = os.path.join(ROOT, "research/issue17/ps-parcels-geo-v2.json")
P59 = os.path.join(ROOT, "research/issue17/ps-blatt-headers.json")
OUT_EV = os.path.join(ROOT, "research/issue17/ps-perblatt-attribution.json")
OUT_RT = os.path.join(ROOT, "src/data/atlas/ps-perblatt-attribution.json")

RATIO_LO, RATIO_HI = 0.8, 1.25
# referenca 1 QK = 3.59665 m² (P57); moda A pas okoli konverzije
QK_REF = 3.59665
MODA_A = (3.3, 4.3)
# strani pas-instanc (izhajajo iz podatkov; pinned v I5-struktura)
EXPECTED_ATTR_PAGES = {61, 83, 84, 85, 86, 87, 99, 36, 49, 94}
EXPECTED_ATTR_BLATT = {"I": 1, "II": 12, "III": 4}
EXPECTED_ADJ = {"ok": 21, "flag": 2}


def fail(msg):
    print(f"FAIL I: {msg}")
    sys.exit(1)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def median(vals):
    s = sorted(vals)
    return s[len(s) // 2] if s else None


def main():
    v2 = json.load(open(V2))
    p59 = json.load(open(P59))
    rows = v2["rowsEvidence"]
    page_attr = p59["pageAttribution"]
    cands = p59["perBlattAmbiguity"]["ruleCandidateBases"]
    p59_inst = p59["perBlattAmbiguity"]["instances"]

    # ————— vrstice po base + vrstni red per stran (soslednost) —————
    rows_by_base = defaultdict(list)
    page_order = defaultdict(list)  # page -> [base,...] v vrstnem redu evidence
    for r in rows:
        rows_by_base[r["base"]].append(r)
        page_order[r["page"]].append(r["base"])

    # ————— I1 ruleCandidate == P59 pin —————
    p59_cands = p59["perBlattAmbiguity"]["ruleCandidateBases"]
    if cands != p59_cands:
        fail(f"I1 ruleCandidate seznam ≠ P59 pin: {cands} vs {p59_cands}")
    if len(cands) != 17:
        fail(f"I1 ruleCandidate {len(cands)} ≠ 17")

    bases_out = {}
    attr_pages = set()
    attr_blatt_dist = defaultdict(int)
    adj_ok = adj_flag = 0

    for b in cands:
        # ————— instance iz vrstic × pageAttribution —————
        by_blatt = defaultdict(list)
        for r in rows_by_base[b]:
            bl = page_attr.get(str(r["page"]), {}).get("blatt")
            if bl:
                by_blatt[bl].append(r)
        insts = []
        for bl in sorted(by_blatt):
            rr = by_blatt[bl]
            med = median([r["ratio"] for r in rr if r.get("ratio")])
            insts.append({
                "blatt": bl,
                "rows": len(rr),
                "pages": sorted({r["page"] for r in rr}),
                "medianRatio": med,
                "kultures": sorted({str(r.get("kultur")) for r in rr if r.get("kultur")}),
                "owners": sorted({(r.get("owner") or "") for r in rr if r.get("owner")}),
            })

        # ————— I2 re-izpeljava == P59 instances —————
        ref = p59_inst.get(b) or p59_inst.get(str(b)) or p59_inst.get(int(b) if b.isdigit() else b)
        if not ref:
            fail(f"I2 P59 nima instanc za {b}")
        ref_map = {i["blatt"]: i for i in ref["instances"]}
        new_map = {i["blatt"]: i for i in insts}
        if set(ref_map) != set(new_map):
            fail(f"I2 {b}: blatt množica ≠ P59 ({sorted(new_map)} vs {sorted(ref_map)})")
        for bl, i in new_map.items():
            j = ref_map[bl]
            if i["rows"] != j["rows"] or i["pages"] != j["pages"]:
                fail(f"I2 {b}/{bl}: rows/pages ≠ P59")
            if i["medianRatio"] is None or j["medianRatio"] is None or \
                    abs(i["medianRatio"] - j["medianRatio"]) > 1e-9:
                fail(f"I2 {b}/{bl}: median ≠ P59")

        # ————— I3 točno ena pas-instanca —————
        in_band = [i for i in insts if i["medianRatio"] and RATIO_LO <= i["medianRatio"] <= RATIO_HI]
        if len(in_band) != 1:
            fail(f"I3 {b}: pas-instanc {len(in_band)} ≠ 1")
        attr = in_band[0]
        attr_blatt_dist[attr["blatt"]] += 1
        attr_pages.update(attr["pages"])

        # ————— pas-vrstice: detalj + soslednost —————
        detail = []
        for r in rows_by_base[b]:
            bl = page_attr.get(str(r["page"]), {}).get("blatt")
            if bl != attr["blatt"]:
                continue
            seq = page_order[r["page"]]
            same = [k for k, bb in enumerate(seq) if bb == r["base"]]
            for k in same:
                pb = seq[k - 1] if k > 0 else None
                nb = seq[k + 1] if k + 1 < len(seq) else None
                adj_ok_row = (pb is not None and abs(int(pb) - int(r["base"])) == 1) or \
                             (nb is not None and abs(int(nb) - int(r["base"])) == 1)
                if adj_ok_row:
                    adj_ok += 1
                else:
                    adj_flag += 1
                detail.append({
                "page": r["page"], "parzella": r["parzella"],
                "kultur": r.get("kultur"),
                "owner": r.get("owner"),
                "joch": r.get("joch"), "klafter": r.get("klafter"),
                "areaQK": r.get("areaQK"), "areaModern": r.get("areaModern"),
                "ratio": r.get("ratio"),
                "sosledje": {"prev": int(pb) if pb is not None else None,
                             "next": int(nb) if nb is not None else None,
                             "ok": adj_ok_row},
            })

        out_insts = [i for i in insts if i["blatt"] != attr["blatt"]]
        bases_out[b] = {
            "attributedBlatt": attr["blatt"],
            "inBand": {"medianRatio": attr["medianRatio"], "pages": attr["pages"],
                       "rows": len(detail)},
            "outInstances": [{"blatt": i["blatt"], "medianRatio": i["medianRatio"],
                              "pages": i["pages"]} for i in out_insts],
            "kulturProfile": attr["kultures"],
            "rows": detail,
        }

    # ————— struktura: pas-strani + re-listing delež —————
    base_pages = defaultdict(set)
    for r in rows:
        base_pages[r["base"]].add(r["page"])
    attr_page_stats = {}
    for p in sorted(attr_pages):
        prows = [r for r in rows if r["page"] == p]
        pbases = list(dict.fromkeys(r["base"] for r in prows))
        multi = [b for b in pbases if len(base_pages[b]) > 1]
        attr_page_stats[str(p)] = {
            "blatt": page_attr[str(p)]["blatt"],
            "rows": len(prows), "bases": len(pbases),
            "multiPageBases": len(multi),
            "multiPageShare": round(len(multi) / len(pbases), 4) if pbases else None,
            "kultures": sorted({str(r.get("kultur")) for r in prows if r.get("kultur")}),
        }
    relist_100 = [p for p, s in attr_page_stats.items() if s["multiPageShare"] == 1.0]

    # ————— unit semantics: moda A vs moda B (globalno, merjeno) —————
    ratios = [r["ratio"] for r in rows if r.get("ratio")]
    moda_a = [x for x in ratios if MODA_A[0] <= x <= MODA_A[1]]
    moda_b = [x for x in ratios if RATIO_LO <= x <= RATIO_HI]

    # ————— I4 join nespremenjen: sha v2 vhoda + izpisi brez pozicij/površin —————
    v2_sha = sha256(V2)

    def assert_no_geo(obj, path="root"):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ("lat", "lng", "areaModern", "areaQK", "joch", "klafter"):
                    # dovoljeno SAMO v per-vrstičnih pas-detaljah (kopija vhodnih vrednosti,
                    # ne nova pozicija joina) — teh ni na višjih nivojih
                    if not path.endswith(".rows"):
                        fail(f"I4 geo polje '{k}' izven rows @ {path}")
                assert_no_geo(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for k, v in enumerate(obj):
                assert_no_geo(v, f"{path}[{k}]")

    # ————— I5 števci —————
    n_rows = sum(len(v["rows"]) for v in bases_out.values())
    if adj_ok + adj_flag != n_rows:
        fail(f"I5 soslednost vrstic {adj_ok + adj_flag} ≠ pas-vrstice {n_rows}")
    if dict(attr_blatt_dist) != EXPECTED_ATTR_BLATT:
        fail(f"I5 atribucije {dict(attr_blatt_dist)} ≠ {EXPECTED_ATTR_BLATT}")
    if {"ok": adj_ok, "flag": adj_flag} != EXPECTED_ADJ:
        fail(f"I5 soslednost {adj_ok}/{adj_flag} ≠ {EXPECTED_ADJ}")
    if attr_pages != EXPECTED_ATTR_PAGES:
        fail(f"I5 pas-strani {sorted(attr_pages)} ≠ {sorted(EXPECTED_ATTR_PAGES)}")

    verdict_si = (
        "Per-Blatt atribucija 17 ruleCandidate base IZVEDENA (merjeno): vsaka dobi "
        "instanco v pasu [0.8, 1.25] — II 12 · I 1 · III 4 (23 vrstic); soslednost 21/23 "
        "(671/934 [~] = prečrtane vrstice v registru). Strani pas-instanc (61, 83–87, 99, "
        "36, 49, 94) nosijo 100 % več-stranskih base — Kultur-Tabellen re-listing [~]. "
        "OPOMBA: pas ujema modo B (ratio ≈ 1), ne konverzije 1 QK = 3.59665 m² (moda A) "
        "— absolutna korespondenca ostaja odprta; join v2 NESPREMENJEN."
    )
    verdict_en = (
        "Per-Blatt attribution of the 17 ruleCandidate bases EXECUTED (measured): each gets "
        "the instance within band [0.8, 1.25] — II 12 · I 1 · III 4 (23 rows); adjacency 21/23 "
        "(671/934 [~] = crossed-out rows in the register). Attribute pages (61, 83-87, 99, "
        "36, 49, 94) carry 100% multi-page bases — Kultur-Tabellen re-listing [~]. "
        "NOTE: the band matches mode B (ratio ~ 1), not the 1 QK = 3.59665 m2 conversion "
        "(mode A) — absolute correspondence remains open; the v2 join UNCHANGED."
    )

    ev = {
        "task": "P60 — per-Blatt atribucija ruleCandidate base v2 (izvedba P59 pravila pasu [0.8, 1.25])",
        "date": "2026-10-14",
        "principle": ("izvedba P59 ruleCandidate pravila kot atribucije; MERJENO brez prerazporeditev — "
                      "join v2 nespremenjen (disciplina P56/P58/P59); soslednost = kontrola kakovosti; "
                      "unit-semantics moda B vs moda A dokumentirano kot odprto"),
        "inputs": {
            "v2": "research/issue17/ps-parcels-geo-v2.json (rowsEvidence 1093, sha256 spodaj)",
            "p59": "research/issue17/ps-blatt-headers.json (pageAttribution + instances + ruleCandidateBases)",
        },
        "rule": {
            "band": f"[{RATIO_LO}, {RATIO_HI}] (raw ratio = areaModern / areaQK)",
            "definition": "baza s TOČNO eno instanco (Blatt) z median razmerjem v pasu → attributedBlatt",
            "origin": "P59 evidence perBlattAmbiguity.ruleCandidateNote (MERJENO); P60 izvedba z soslednostjo",
        },
        "v2Sha256": v2_sha,
        "summary": {
            "bases": len(bases_out),
            "rows": n_rows,
            "attributedBlattDist": dict(sorted(attr_blatt_dist.items())),
            "soslednost": {"ok": adj_ok, "flag": adj_flag,
                           "flaggedRows": [f"{b}@p{d['page']}" for b, v in sorted(bases_out.items())
                                           for d in v["rows"] if not d["sosledje"]["ok"]]},
            "attrPages": sorted(attr_pages),
            "relist100Pages": sorted(int(p) for p in relist_100),
        },
        "bases": bases_out,
        "attrPageStats": attr_page_stats,
        "unitSemantics": {
            "qkReference": QK_REF,
            "modaA": {"band": list(MODA_A), "count": len(moda_a),
                      "note": "ratio ≈ 3.597 — prava konverzija QK → m² (1 QK = 3.59665 m²)"},
            "modaB": {"band": [RATIO_LO, RATIO_HI], "count": len(moda_b),
                      "note": "ratio ≈ 1 — areaModern ≈ areaQK po ŠTEVILKI; pas pravila P59/P60 ujema to modo"},
            "factor": round(QK_REF / 1.0, 5),
            "status": "ODPRTO — absolutna korespondenca pas-instanc ni dokazana; "
                      "atribucija = relativa (najboljše ujemanje med instancami) [~]",
        },
        "invariants": ["I1 ruleCandidate == P59", "I2 instance == P59", "I3 ena pas-instanca",
                       "I4 join nespremenjen + brez geo polj izven rows", "I5 soslednost števci",
                       "I6 determinizem", "I7 dokaz ⊇ runtime"],
        "statusLine": (f"P60 PER-BLATT ATRIBUCIJA: {len(bases_out)} ruleCandidate atributiranih "
                       f"(II {attr_blatt_dist['II']} · I {attr_blatt_dist['I']} · III {attr_blatt_dist['III']}), "
                       f"{n_rows} vrstic, soslednost {adj_ok}/{n_rows} [~]; re-listing 100 % na pas-straneh "
                       f"{sorted(int(p) for p in relist_100)}; join v2 nespremenjen"),
        "verdictSi": verdict_si,
        "verdictEn": verdict_en,
        "next": [
            "razrešiti unit-semantics mode B (ratio ≈ 1): kolonialna merska enota ali delna površina [~]",
            "razširiti atribucijo na vseh 106 čez-Blatt base (potrebno P59 pokritost 133–136 + 138–139 dokončati)",
            "razlaga strani 61/83–87/99 kot Kultur-Tabellen: navzkrižje s Kultur stolpcem polnih branj P38",
            "per-Blatt SPLIT joina za atributirane base (zahteva pini + odločitev lastnika o pozicijah)",
            "povezati lastnike pas-instanc (npr. 163 II: Schimey Martho/Stainzldt Wölfl/Schumitsch Matja/Laune Hülfse) s PF protokolom",
        ],
    }

    runtime = {
        "version": 1,
        "task": ev["task"],
        "date": ev["date"],
        "generatedBy": "scripts/p60_ps_perblatt_attribution.py",
        "rule": ev["rule"],
        "summary": ev["summary"],
        "bases": {b: {"attributedBlatt": v["attributedBlatt"],
                      "inBand": v["inBand"],
                      "outInstances": v["outInstances"],
                      "kulturProfile": v["kulturProfile"],
                      "rows": [{"page": d["page"], "parzella": d["parzella"],
                                "kultur": d["kultur"], "owner": d["owner"],
                                "ratio": d["ratio"],
                                "sosledje": d["sosledje"]} for d in v["rows"]]}
                  for b, v in bases_out.items()},
        "attrPageStats": ev["attrPageStats"],
        "unitSemantics": ev["unitSemantics"],
        "statusLine": ev["statusLine"],
        "verdictSi": ev["verdictSi"],
        "verdictEn": ev["verdictEn"],
    }

    # ————— I4: brez geo polj izven rows —————
    assert_no_geo(runtime, "runtime")
    for b, v in bases_out.items():
        for d in v["rows"]:
            for g in ("lat", "lng"):
                if g in d:
                    fail(f"I4 geo polje {g} v pas-vrstici {b}")

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

    print(f"OK: base {len(bases_out)}, pas-vrstice {n_rows}, atribucije {dict(sorted(attr_blatt_dist.items()))}")
    print(f"OK: soslednost {adj_ok}/{n_rows} (flag {adj_flag}), pas-strani {sorted(attr_pages)}")
    print(f"OK: moda A {len(moda_a)} ({MODA_A}), moda B {len(moda_b)} ({RATIO_LO}-{RATIO_HI})")
    print(f"OK: dokaz {OUT_EV}, runtime {OUT_RT}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        h1 = sha256(OUT_EV)
        main()
        if sha256(OUT_EV) != h1:
            fail("I6 determinizem: izhod se je spremenil")
        print("I6 --check: PASS")
    else:
        main()
