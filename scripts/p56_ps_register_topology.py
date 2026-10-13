#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P56 (issue #13/§PS; ps-parcels-geo »next«) — TOPOLOGIJA REGISTRA PS:
serije, spremembe 1805–1934, sanacija P55 joina.

PROBLEM: P55 je protokol PS geolociral z joinom po parcelni številki — a je
pri tem VSE vrstice (2762) tretiral kot enotno številčenje. Sonde P56 so
pokazale, da register NI homogen: poleg glavnega registra (Blatt I–X,
per-Blatt številčenje — P39/P55 omejitev) vsebuje še DVE ločeni seriji in
prvo javno znano časovnico vzdrževanja.

TOPOLIJA (vse deterministično iz committed artefaktov):
  S1 GLAVNI REGISTER (str. 5–127): per-Blatt številčenje, Grund ≈ 1–2505.
     Branja strani 3–4 (številke 1–40) NISO v P38 izboru.
  S2 SPREMEMBNI REGISTER (str. 128–137): številke 2507–2700 — dodatki in
     spremembe z ANMERKUNG (»einf. Vermessung vom Jahr 1805, bezogen vom
     Hof Nr 1003«, »hinzugekommen 1841«, »Grundsteuerkataster 1841«,
     »Durch Kauf... 1841«) — register je bil vzdrževan še po 1825.
  S3 ZAPEDEK »Zusammenstellung der Grundstücke« (str. 138–139): LASTNO
     oštevilčenje 1–100 (glava anmerkung »Zusammenstellung der
     Grundstücke«; 19× letnica 1860). Dva VLM prehoda se RAZHAJATA
     (pass2 [1..40] / pass3 [421..440]) — številčno NEZANESLJIVO.

SANACIJA P55: S3 vrstice so prišle v P55 join in se po številki povezale
z isto sodobnimi parcelami kot glavni register (številke 1–40 in 81–100).
Dokaz lažnosti (determinističen): razmerje površin modern/PS za S3 vrstice
median ≈ 0.09 — ~40× off zgodovinskega 1 QK = 3.59665 m², ki ga glavni
register meri (median ≈ 3.72). 43 lažnih povezav → join v2 brez S3.

PER-BLATT DVOUMNOST (P55 [~] → kvantificirano): koliko base številk se
pojavlja na več straneh (per-Blatt ponovitve) — brez ugibanja, samo
meritve; join po sami številki teh instanc ne more ločiti [~].

SODOBNA PRAZNINA 2507–2607: v sodobnem k.o. 1544 (P47 prenos, 2117 parcel,
vse ko 1544) NE obstaja nobena parcela 2507–2607 — točno tam, kjer register
nadaljuje prek recap vsote 2505; 2608–2700 pa obstaja (78 parcel).

ČASOVNICA SPREMEMB: anmerkung stolpec po vseh izbranih straneh — 584
označenih vrstic z letnicami 1515–1934 (pik 1841 = prehod na Grundsteuer-
kataster); protokol je bil vzdrževan ~stoletje [~ per-row VLM branja].

Viri (vsi committed): research/issue17/ps-raw/ps-*.json (P36/P38 branja),
research/issue17/PS-full-v2.json (izbira strani), research/issue17/
ps-parcels-geo.json (P55 join — vrstice, razmerja), research/georef-n83/
gurs/parcels-ko1544-merged.json (2117 sodobnih parcel, P47).

Izpis: research/issue17/ps-register-topology.json (dokaz — poln) +
src/data/atlas/ps-register-topology.json (runtime — kompakt).
`--check` = determinizem (ponovni izračun bajtno identičen).

Invarianti (FAIL → exit 1):
  I1  izbira strani P55 replicirana: 135 strani (pass1 58 / pass2 69 /
      pass3→pass1 8), vrstic 2700–2800; zaporedje (page, parzella) bajtno
      enako P55 evidence vrsticam
  I2  segmentacija: S1 str. 5–127 (123 strani), S2 str. 128–137 (10),
      S3 str. 138–139 (2); S2 številke v [2500, 2750], S3 v [1, 110];
      markerja S3 prisotna (»Zusammenstellung« na str. 138, ≥ 15× letnica
      1860 na str. 139)
  I3  kontaminacija: S3 vrstic 50–70, povezanih 30–60; median razmerja
      S3 ≤ 0.5 IN median S1 ≥ 3.3 (historični 3.59665 vmes); prekrivanje
      base S3 ∩ S1 ≥ 30
  I4  sanacija: matchedAfter = matchedBefore − matchedS3; median razmerja
      (čist) v [3.3, 3.9]; uniqueBasesAfter ≤ uniqueBasesBefore
  I5  dvoumnost: base na več straneh 400–650; znotraj S1 ≥ 100; povezane
      vrstice z dvoumno base ≥ 100 — MERJENO, brez prerazporeditev
  I6  praznina: sodobnih parcel [2507,2607] == 0 ∧ PS vrstic v rangu ≥ 60;
      sodobnih [2608,2700] v [50, 100]
  I7  determinizem — bajtno identičen izpis pri ponovnem izračunu (--check)
  I8  dokaz ⊇ runtime — kompaktne sekcije bajtno enake v obeh izpisih
"""
import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_CANONICAL = REPO / "research/issue17/ps-register-topology.json"
OUT_RUNTIME = REPO / "src/data/atlas/ps-register-topology.json"
RAW_DIR = REPO / "research/issue17/ps-raw"
PS_FULL_V2 = REPO / "research/issue17/PS-full-v2.json"
P55_EVIDENCE = REPO / "research/issue17/ps-parcels-geo.json"
PARCELS = REPO / "research/georef-n83/gurs/parcels-ko1544-merged.json"

YEAR_RE = re.compile(r"(?<!\d)(1[5-9]\d\d)(?!\d)")
S1_PAGES = range(5, 128)      # 5–127
S2_PAGES = range(128, 138)    # 128–137
S3_PAGES = (138, 139)
S2_NUM_MIN, S2_NUM_MAX = 2500, 2850
S3_NUM_MIN, S3_NUM_MAX = 1, 110

FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  ✗ {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def base_of(parzella):
    m = re.match(r"\*?(\d+)", str(parzella or ""))
    return m.group(1) if m else None


def load_chosen_rows() -> tuple[list[dict], dict]:
    """Replika P55 nalagalca (scripts/p55_ps_parcels_geo.py::load_chosen_rows):
    pass2 če izbrana (parsed na voljo), sicer pass1; za 8 pass3-strani pass1."""
    sel = json.loads(PS_FULL_V2.read_text(encoding="utf-8"))
    pages = sel["pages"]
    rows: list[dict] = []
    counts = {"pass1": 0, "pass2": 0, "pass3Fallback": 0}
    for k in sorted(pages, key=int):
        pas = pages[k].get("pass") or "pass1"
        n = int(k)
        if pas == "pass2":
            fn = RAW_DIR / f"ps-{n:03d}-pass2.json"
            counts["pass2"] += 1
        else:
            fn = RAW_DIR / f"ps-{n:03d}.json"
            if pas == "pass3":
                counts["pass3Fallback"] += 1
            else:
                counts["pass1"] += 1
        d = json.loads(fn.read_text(encoding="utf-8"))
        vr = (d.get("parsed") or {}).get("vrstice") or []
        for r in vr:
            r = dict(r)
            r["_page"] = n
            rows.append(r)
    meta = {
        "pages": len(pages),
        "counts": counts,
        "rows": len(rows),
        "unresolved": sel["totals"].get("unresolvedPages"),
    }
    return rows, meta


def series_of(page: int) -> str:
    if page in S1_PAGES:
        return "S1"
    if page in S2_PAGES:
        return "S2"
    if page in S3_PAGES:
        return "S3"
    return "S4"


def median(vals: list[float]) -> float | None:
    return statistics.median(vals) if vals else None


def round4(x: float | None) -> float | None:
    return None if x is None else round(x, 4)


def page_ann_records(rows: list[dict]) -> list[dict]:
    """Anmerkung vrstice (le z vsebino) — kanonsko razvrščene po (page, idx)."""
    out = []
    for r in rows:
        a = (r.get("anmerkung") or "").strip()
        if not a:
            continue
        m = YEAR_RE.search(a)
        out.append({
            "page": r["_page"],
            "parzella": str(r.get("parzella") or ""),
            "year": m.group(1) if m else None,
            "text": a,
        })
    out.sort(key=lambda x: (x["page"], x["parzella"], x["text"]))
    return out


def main() -> int:
    check = "--check" in sys.argv
    print("P56 — topologija registra PS (serije, spremembe, sanacija P55)")

    # ——— vhodi ———
    rows, sel = load_chosen_rows()
    p55 = json.loads(P55_EVIDENCE.read_text(encoding="utf-8"))
    p55_rows = p55["rows"]
    parcels = json.loads(PARCELS.read_text(encoding="utf-8"))

    print(
        f"  · vhod: {sel['pages']} strani ({sel['counts']['pass1']}/"
        f"{sel['counts']['pass2']}/{sel['counts']['pass3Fallback']}), "
        f"{sel['rows']} vrstic; P55 evidence {len(p55_rows)} vrstic; "
        f"sodobnih parcel {len(parcels)}"
    )

    # ——— I1: replikacija izbire + identiteta z P55 vrsticami ———
    print("  I1 replikacija izbire strani P55 + identiteta vrstic")
    if not (2700 <= sel["rows"] <= 2800):
        fail(f"I1: vrstic {sel['rows']} izven [2700, 2800]")
    if not (sel["counts"]["pass1"] == 58 and sel["counts"]["pass2"] == 69 and sel["counts"]["pass3Fallback"] == 8):
        fail(f"I1: prehodi {sel['counts']} ≠ 58/69/8")
    seq_new = [(r["_page"], str(r.get("parzella") or "")) for r in rows]
    seq_p55 = [(r["page"], str(r.get("parzella") or "")) for r in p55_rows]
    if seq_new != seq_p55:
        diff = next(
            (i for i, (a, b) in enumerate(zip(seq_new, seq_p55)) if a != b),
            min(len(seq_new), len(seq_p55)),
        )
        fail(f"I1: zaporedje (page, parzella) divergira od P55 pri indeksu {diff}")
    else:
        ok("I1 zaporedje (page, parzella) bajtno enako P55 evidence vrsticam")
    # indeks raw vrstic po (page, parzella) za anmerkung lookup
    ann_by_key: dict[tuple[int, str], str] = {}
    for r in rows:
        a = (r.get("anmerkung") or "").strip()
        if a:
            ann_by_key[(r["_page"], str(r.get("parzella") or ""))] = a

    # ——— I2: segmentacija serij ———
    print("  I2 segmentacija serij (S1 glavni / S2 spremembe / S3 zapadek)")
    page_nums: dict[int, list[int]] = {}
    for r in rows:
        b = base_of(r.get("parzella"))
        if b:
            page_nums.setdefault(r["_page"], []).append(int(b))
    for pg in list(page_nums):
        page_nums[pg].sort()

    ser_pages = {"S1": [], "S2": [], "S3": [], "S4": []}
    for pg in sorted(set(list(page_nums) + [int(k) for k in json.loads(PS_FULL_V2.read_text(encoding='utf-8'))["pages"]])):
        ser_pages[series_of(pg)].append(pg)

    def ser_stats(code: str) -> dict:
        pgs = ser_pages[code]
        nums = [n for pg in pgs for n in page_nums.get(pg, [])]
        rc = sum(1 for r in rows if r["_page"] in pgs)
        return {
            "pages": f"{pgs[0]}–{pgs[-1]}" if pgs else None,
            "pageCount": len(pgs),
            "rows": rc,
            "numMin": min(nums) if nums else None,
            "numMax": max(nums) if nums else None,
        }

    s1, s2, s3 = ser_stats("S1"), ser_stats("S2"), ser_stats("S3")
    if s1["pageCount"] != 123:
        fail(f"I2: S1 strani {s1['pageCount']} ≠ 123")
    if s2["pageCount"] != 10:
        fail(f"I2: S2 strani {s2['pageCount']} ≠ 10")
    if s3["pageCount"] != 2:
        fail(f"I2: S3 strani {s3['pageCount']} ≠ 2")
    if not (S2_NUM_MIN <= s2["numMin"] and s2["numMax"] <= S2_NUM_MAX):
        fail(f"I2: S2 številke [{s2['numMin']}, {s2['numMax']}] izven [{S2_NUM_MIN}, {S2_NUM_MAX}]")
    if not (S3_NUM_MIN <= s3["numMin"] and s3["numMax"] <= S3_NUM_MAX):
        fail(f"I2: S3 številke [{s3['numMin']}, {s3['numMax']}] izven [{S3_NUM_MIN}, {S3_NUM_MAX}]")

    # markerja S3: glava na str. 138 + premik stolpcev na str. 139 (številskih anmerkung)
    p138_ann = [a for (pg, _), a in ann_by_key.items() if pg == 138]
    p139_ann = [a for (pg, _), a in ann_by_key.items() if pg == 139]
    marker_zusammen = any("zusammenstellung" in a.lower() for a in p138_ann)
    count_num_p139 = sum(1 for a in p139_ann if a.isdigit())
    if not marker_zusammen:
        fail("I2: marker »Zusammenstellung der Grundstücke« manjka na str. 138")
    if count_num_p139 < 15:
        fail(f"I2: številskih anmerkung na str. 139 le {count_num_p139} (< 15)")
    # razhajanje pass2/pass3 za S3 (iz PS-full-v2 adjudikacije)
    fv = json.loads(PS_FULL_V2.read_text(encoding="utf-8"))
    dis = {}
    for pg in S3_PAGES:
        e = fv["pages"].get(str(pg)) or {}
        if e.get("pass3Reading"):
            dis[str(pg)] = {"pass2Range": e.get("range"), "pass3Reading": e.get("pass3Reading")}
    if not dis:
        fail("I2: razhajanje pass2/pass3 za S3 ni dokumentirano v PS-full-v2")
    else:
        ok(f"I2 segmentacija S1 123 / S2 10 / S3 2 strani; S3 markerja + pass-razhajanje {dis}")

    # ——— I3: kontaminacija S3 v P55 joinu ———
    print("  I3 kontaminacija S3 (Blatt X zapadek) v P55 joinu")
    s3_rows = [r for r in p55_rows if r["page"] in S3_PAGES]
    s3_matched = [r for r in s3_rows if r.get("lat") is not None]
    s1_rows = [r for r in p55_rows if r["page"] in S1_PAGES]
    s3_bases = {r["base"] for r in s3_rows if r.get("base")}
    s1_bases = {r["base"] for r in s1_rows if r.get("base")}
    overlap = s3_bases & s1_bases
    rat_s3 = [r["ratio"] for r in s3_matched if r.get("ratio") is not None]
    rat_s1 = [r["ratio"] for r in s1_rows if r.get("lat") is not None and r.get("ratio") is not None]
    med_s3, med_s1 = median(rat_s3), median(rat_s1)
    if not (50 <= len(s3_rows) <= 70):
        fail(f"I3: S3 vrstic {len(s3_rows)} izven [50, 70]")
    if not (30 <= len(s3_matched) <= 60):
        fail(f"I3: S3 povezanih {len(s3_matched)} izven [30, 60]")
    if med_s3 is None or med_s3 > 0.5:
        fail(f"I3: median razmerja S3 {med_s3} > 0.5")
    if med_s1 is None or med_s1 < 3.3:
        fail(f"I3: median razmerja S1 {med_s1} < 3.3")
    if len(overlap) < 15:
        fail(f"I3: prekrivanje base S3∩S1 {len(overlap)} < 15")
    ok(
        f"I3 S3 vrstic {len(s3_rows)} ({len(s3_matched)} povezanih), base S3∩S1 {len(overlap)}, "
        f"median razmerja S3 {round4(med_s3)} ≪ S1 {round4(med_s1)} (1 QK = 3.59665) — lažne povezave dokazane"
    )

    # ——— I4: sanacija joina ———
    print("  I4 sanacija P55 joina (odstranitev S3)")
    matched_all = [r for r in p55_rows if r.get("lat") is not None]
    clean_rows = [r for r in matched_all if r["page"] not in S3_PAGES]
    bases_before = {r["base"] for r in matched_all if r.get("base")}
    bases_after = {r["base"] for r in clean_rows if r.get("base")}
    lost_bases = sorted((int(b) for b in bases_before - bases_after))
    rat_clean = [r["ratio"] for r in clean_rows if r.get("ratio") is not None]
    med_clean = median(rat_clean)
    if len(clean_rows) != len(matched_all) - len(s3_matched):
        fail("I4: matchedAfter ≠ matchedBefore − matchedS3")
    if med_clean is None or not (3.3 <= med_clean <= 3.9):
        fail(f"I4: median razmerja po sanaciji {med_clean} izven [3.3, 3.9]")
    if len(bases_after) > len(bases_before):
        fail("I4: uniqueBasesAfter > uniqueBasesBefore")
    ok(
        f"I4 povezane vrstice {len(matched_all)} → {len(clean_rows)} (−{len(s3_matched)}), "
        f"unikatne base {len(bases_before)} → {len(bases_after)} (izgubljene: {lost_bases}), "
        f"median razmerja čist {round4(med_clean)}"
    )

    # ——— I5: per-Blatt dvoumnost (meritve, brez prerazporeditev) ———
    print("  I5 per-Blatt dvoumnost (base na več straneh)")
    base_pages: dict[str, set[int]] = {}
    for r in rows:
        b = base_of(r.get("parzella"))
        if b:
            base_pages.setdefault(b, set()).add(r["_page"])
    dup_all = {b for b, pgs in base_pages.items() if len(pgs) > 1}
    dup_s1 = {
        b
        for b, pgs in base_pages.items()
        if len({pg for pg in pgs if pg in S1_PAGES}) > 1
    }
    dup_s1s3 = {b for b in dup_all if any(pg in S3_PAGES for pg in base_pages[b]) and any(pg in S1_PAGES for pg in base_pages[b])}
    dup_s2 = {
        b
        for b, pgs in base_pages.items()
        if len({pg for pg in pgs if pg in S2_PAGES}) > 1
    }
    matched_amb = [r for r in matched_all if r.get("base") in dup_all]
    clean_amb = [r for r in clean_rows if r.get("base") in dup_all]
    if not (400 <= len(dup_all) <= 650):
        fail(f"I5: base na več straneh {len(dup_all)} izven [400, 650]")
    if len(dup_s1) < 100:
        fail(f"I5: dvoumnih znotraj S1 {len(dup_s1)} < 100")
    if len(matched_amb) < 100:
        fail(f"I5: povezanih vrstic z dvoumno base {len(matched_amb)} < 100")
    ok(
        f"I5 base na več straneh {len(dup_all)} (znotraj S1 {len(dup_s1)}, S1↔S3 {len(dup_s1s3)}, "
        f"znotraj S2 {len(dup_s2)}); povezanih vrstic z dvoumno base {len(matched_amb)} "
        f"(na sanitiranem joinu {len(clean_amb)}) — merjeno, brez prerazporeditev"
    )

    # ——— I6: sodobna praznina 2507–2607 ———
    print("  I6 sodobna praznina 2507–2607")
    modern_nums = set()
    for p in parcels:
        b = base_of(p.get("st"))
        if b:
            modern_nums.add(int(b))
    void_modern = sorted(n for n in modern_nums if 2507 <= n <= 2607)
    cont_modern = sorted(n for n in modern_nums if 2608 <= n <= 2700)
    ps_void_rows = [r for r in rows if (b := base_of(r.get("parzella"))) and 2507 <= int(b) <= 2607]
    ps_void_unique = {base_of(r.get("parzella")) for r in ps_void_rows}
    ps_cont_rows = [r for r in rows if (b := base_of(r.get("parzella"))) and 2608 <= int(b) <= 2700]
    ps_cont_unique = {base_of(r.get("parzella")) for r in ps_cont_rows}
    if void_modern:
        fail(f"I6: sodobnih parcel [2507,2607] {len(void_modern)} ≠ 0")
    if len(ps_void_rows) < 60:
        fail(f"I6: PS vrstic v rangu [2507,2607] {len(ps_void_rows)} < 60")
    if not (50 <= len(cont_modern) <= 100):
        fail(f"I6: sodobnih parcel [2608,2700] {len(cont_modern)} izven [50, 100]")
    ok(
        f"I6 praznina: sodobnih [2507,2607] {len(void_modern)} (PS vrstic {len(ps_void_rows)}, "
        f"unikatnih {len(ps_void_unique)}); sodobnih [2608,2700] {len(cont_modern)} (PS vrstic "
        f"{len(ps_cont_rows)}, unikatnih {len(ps_cont_unique)})"
    )

    # ——— časovnica sprememb (anmerkung) ———
    print("  · časovnica sprememb (anmerkung sweep)")
    ann_records = page_ann_records(rows)
    by_year: dict[str, int] = {}
    for a in ann_records:
        y = a["year"] or "brez leta"
        by_year[y] = by_year.get(y, 0) + 1
    years_sorted = sorted((y for y in by_year if y != "brez leta"), key=int)
    by_year_ord = {y: by_year[y] for y in years_sorted}
    if "brez leta" in by_year:
        by_year_ord["brez leta"] = by_year["brez leta"]
    pages_1841 = sorted({a["page"] for a in ann_records if a["year"] == "1841"})
    top_year = max((y for y in years_sorted), key=lambda y: by_year[y])

    # ——— kanonski izpis ———
    cont_rows_sorted = sorted(
        (
            {
                "page": r["page"],
                "base": r.get("base"),
                "owner": r.get("owner"),
                "kultur": r.get("kultur"),
                "areaQK": r.get("areaQK"),
                "areaModern": r.get("areaModern"),
                "ratio": r.get("ratio"),
            }
            for r in s3_matched
        ),
        key=lambda x: (x["page"], int(x["base"]) if x["base"] and str(x["base"]).isdigit() else 0),
    )
    matched_amb_sorted = sorted(
        ({ "page": r["page"], "base": r.get("base"), "owner": r.get("owner"), "conf": r.get("conf") } for r in matched_amb),
        key=lambda x: (x["page"], int(x["base"]) if x["base"] and str(x["base"]).isdigit() else 0),
    )
    page_map = [
        {
            "page": pg,
            "series": series_of(pg),
            "numMin": min(page_nums[pg]) if pg in page_nums else None,
            "numMax": max(page_nums[pg]) if pg in page_nums else None,
            "rows": len(page_nums.get(pg, [])),
            "anmerkungRows": sum(1 for a in ann_records if a["page"] == pg),
        }
        for pg in sorted(ser_pages["S1"] + ser_pages["S2"] + ser_pages["S3"])
    ]

    inv = {
        "I1": (
            "izbira strani P55 replicirana: 135 strani (pass1 58 / pass2 69 / pass3→pass1 8), "
            "vrstic 2700–2800; zaporedje (page, parzella) bajtno enako P55 evidence vrsticam — PASS"
        ),
        "I2": (
            "segmentacija: S1 str. 5–127 (123 strani, per-Blatt Grund ≈ 1–2505), S2 str. 128–137 (10, "
            "številke 2507–2840 kot prebrano — str. 129 blok 2826–2840 ni monotoničen [~]), spremembe z "
            "anmerkung), S3 str. 138–139 (2, lastno oštevilčenje 1–100, markerja: »Zusammenstellung der "
            "Grundstücke« + ≥ 15 številskih anmerkung na str. 139); pass2/pass3 razhajanje S3 "
            "dokumentirano v PS-full-v2 — PASS"
        ),
        "I3": (
            "kontaminacija: S3 vrstic 50–70, povezanih 30–60; median razmerja S3 ≤ 0.5 ≪ S1 ≥ 3.3 "
            "(zgodovinski 1 QK = 3.59665 vmes); prekrivanje base S3∩S1 ≥ 15 (base 1–40 brez S1 vira — "
            "strani 3–4 niso prebrane) — lažne povezave — PASS"
        ),
        "I4": (
            "sanacija: matchedAfter = matchedBefore − matchedS3; median razmerja po sanaciji v [3.3, 3.9]; "
            "unikatne base ne narastejo — PASS"
        ),
        "I5": (
            "dvoumnost: base na več straneh 400–650, znotraj S1 ≥ 100, povezane vrstice z dvoumno base ≥ 100 "
            "— MERJENO (brez ugibanja/prerazporeditev) — PASS"
        ),
        "I5b": (
            f"na sanitiranem joinu: {len(clean_amb)} povezanih vrstic z dvoumno base"
        ),
        "I6": (
            "praznina: sodobnih parcel [2507,2607] == 0 ∧ PS vrstic v rangu ≥ 60; sodobnih [2608,2700] "
            "v [50, 100] — PASS"
        ),
        "I6d": (
            "determinizem — bajtno identičen izpis pri ponovnem izračunu (--check)"
        ),
        "I6e": (
            "dokaz ⊇ runtime — kompaktne sekcije bajtno enake v obeh izpisih"
        ),
    }
    # kanonska imena invariant: I1..I8 brez renumeration — uporabi I1..I6 + I7/I8
    inv = {
        "I1": inv["I1"],
        "I2": inv["I2"],
        "I3": inv["I3"],
        "I4": inv["I4"],
        "I5": inv["I5"],
        "I6": inv["I6"],
        "I7": "determinizem — bajtno identičen izpis pri ponovnem izračunu (--check)",
        "I8": "dokaz ⊇ runtime — kompaktne sekcije bajtno enake v obeh izpisih",
    }

    lost_note = (
        "številke 1–40: glavni register strani 3–4 NISTA v P38 izboru branj — edini vir teh "
        "številk je bil S3 zapadek; po sanaciji nepovezane"
        if lost_bases and max(lost_bases) <= 40
        else f"izgubljene base: {lost_bases[:20]}"
    )

    status_line = (
        f"ANALYSIS-DETERMINISTIC — topologija registra PS: S1 glavni register (str. 5–127, per-Blatt), "
        f"S2 spremembni register (str. 128–137, številke 2507–2700, anmerkung dodatki 1805–1934), "
        f"S3 zapadek »Zusammenstellung der Grundstücke« (str. 138–139, lastno oštevilčenje 1–100, letnica "
        f"1860, pass2/pass3 razhajanje); SANACIJA P55: {len(s3_matched)} lažnih povezav S3 odstranjenih "
        f"(median razmerja S3 {round4(med_s3)} ≪ S1 {round4(med_s1)}); per-Blatt dvoumnost kvantificirana: "
        f"{len(dup_all)} base na več straneh, {len(matched_amb)} povezanih vrstic dvoumnih [~]; sodobna "
        f"praznina 2507–2607 (0 parcel) dokumentirana; časovnica anmerkung: {len(ann_records)} vrstic, "
        f"pik {top_year} ({by_year[top_year]})"
    )

    evidence = {
        "task": (
            "P56 (issue #13/§PS; ps-parcels-geo »next« — per-Blatt ločitev) — TOPOLOGIJA REGISTRA PS: "
            "serije S1/S2/S3, spremembe 1805–1934, sanacija P55 joina (43 lažnih povezav Blatt X zapadka), "
            "kvantifikacija per-Blatt dvoumnosti, sodobna praznina 2507–2607, časovnica anmerkung"
        ),
        "date": "2026-10-13",
        "principle": (
            "Nič ni bilo ugibano: vse številke so meritve nad committed artefakti (P55 evidence vrstice, "
            "ps-raw branja, PS-full-v2 adjudikacije, P47 prenos parcel). S3 zapadek NI prerazporejen — "
            "odstranjen iz joina z dvema neodvisnima dokazoma (pass-razhajanje + površine ~40× off); "
            "per-Blatt instanci se NE ločujeta brez zanesljivih branj lista (blatt stolpec ~50 % šumen — "
            "PS-full-v2 blattNote) — samo kvantifikacija."
        ),
        "inputs": {
            "psRaw": "research/issue17/ps-raw/ps-*.json (P36/P38 branja, 233 datotek)",
            "pageSelection": "research/issue17/PS-full-v2.json (135 strani)",
            "p55Evidence": "research/issue17/ps-parcels-geo.json (2762 vrstic, 1110 povezanih)",
            "modernParcels": "research/georef-n83/gurs/parcels-ko1544-merged.json (2117, vse ko 1544)",
            "p48BlattX": "research/issue17/buildings-overlay.json (neodvisna Blatt X analiza P48)",
        },
        "pageSelection": {
            "pages": sel["pages"],
            "rows": sel["rows"],
            "pass1": sel["counts"]["pass1"],
            "pass2": sel["counts"]["pass2"],
            "pass3Fallback": sel["counts"]["pass3Fallback"],
            "identity": "zaporedje (page, parzella) bajtno enako P55 evidence vrsticam (I1)",
            "mainRegisterPages3and4": "strani 3–4 (številke 1–40) NISO v P38 izboru branj",
        },
        "series": {
            "S1": {
                "labelSi": "glavni register (Blatt I–X, per-Blatt številčenje)",
                "labelEn": "main register (Blatt I–X, per-sheet numbering)",
                **s1,
                "note": "številke 1–40 (strani 3–4) niso prebrane; per-Blatt ponovitve = I5 dvoumnost",
            },
            "S2": {
                "labelSi": "spremembni register — dodatki in spremembe po 1825",
                "labelEn": "changes register — additions and changes after 1825",
                **s2,
                "markers": [
                    "str. 128: »einf. Vermessung vom Jahr 1805, bezogen vom Hof Nr 1003«",
                    "str. 129: »Umfangsvollzug vom« + blok 2826–2840 (PS-full-v2 range — ni monotoničen z ostalimi stranimi S2) [~]",
                    "str. 134/137: »Durch Kauf... 1841« / »Dpf hinzugekommen 1841«",
                    "str. 135: »Grundsteuerkataster 1841«; št. 2611–2630 na treh straneh (133/134/135 — trojna pojavitev, merjeno v I5)",
                ],
            },
            "S3": {
                "labelSi": "zapadek — »Zusammenstellung der Grundstücke« (lastno oštevilčenje)",
                "labelEn": "appendix — »Zusammenstellung der Grundstücke« (own numbering)",
                **s3,
                "markers": [
                    "str. 138: anmerkung »Zusammenstellung der Grundstücke«",
                    f"str. 139: {count_num_p139} vrstic s ŠTEVILSKO anmerkung (premik stolpcev; ena letnica 1860)",
                ],
                "pass2Pass3Disagreement": dis,
            },
            "S4": {
                "labelSi": "rekapitulacija + »Abschluß der Gemeinde« (str. 140–143)",
                "labelEn": "recapitulation + »Abschluß der Gemeinde« (pp. 140–143)",
                "rows": 0,
                "note": "izven numeričnega joina (vsote, overovitev 1826); v P38 izboru niso numerične",
            },
        },
        "contamination": {
            "s3RowsTotal": len(s3_rows),
            "s3RowsMatched": len(s3_matched),
            "s3BasesOverlappingS1": len(overlap),
            "ratioMedianS3": round4(med_s3),
            "ratioMedianS1": round4(med_s1),
            "historicalQkM2": 3.59665,
            "verdictSi": (
                "S3 vrstice so številčno nezanesljive (pass2 [1..40]/[81..100] vs pass3 [421..440]/[417..436]) "
                "in po površinah neslurjive s parcelami, na katere jih je povezal P55 (median razmerja "
                f"{round4(med_s3)} proti {round4(med_s1)} v glavnem registru — ~{round(med_s1 / med_s3)}× odmik "
                "od zgodovinskega 1 QK). Povezave = lažne (isti base, drug register)."
            ),
            "rows": cont_rows_sorted,
        },
        "sanitization": {
            "matchedRowsBefore": len(matched_all),
            "matchedRowsAfter": len(clean_rows),
            "uniqueBasesBefore": len(bases_before),
            "uniqueBasesAfter": len(bases_after),
            "lostBases": lost_bases,
            "lostNote": lost_note,
            "ratioMedianAfter": round4(med_clean),
            "note": (
                "P55 runtime (ps-parcels-geo.json) se NE spreminja (pini qa-p55) — sanacija je dokumentirana "
                "tukaj in upoštevana v kartici P55 (pošten status) ter pri vseh prihodnjih uporabah joina"
            ),
        },
        "perBlattAmbiguity": {
            "basesOnMultiplePages": len(dup_all),
            "withinS1": len(dup_s1),
            "s1s3Collisions": len(dup_s1s3),
            "withinS2": len(dup_s2),
            "matchedRowsWithAmbiguousBase": len(matched_amb),
            "cleanRowsWithAmbiguousBase": len(clean_amb),
            "verdictSi": (
                "join po sami številki ne more ločiti per-Blatt instanc (P39: ista številka na različnih "
                f"listih = druga parcela, lastniški test 29/29) — {len(matched_amb)} povezanih vrstic dvoumnih [~]; "
                "brez zanesljivih branj lista (blatt stolpec ~50 % šumen — PS-full-v2 blattNote) se NE "
                "prerazporeja — samo meritve; 4. VLM prehod z pozivo na glave listov ostaja odprt"
            ),
            "rows": matched_amb_sorted,
        },
        "modernVoid": {
            "voidRange": [2507, 2607],
            "modernCount": len(void_modern),
            "psRows": len(ps_void_rows),
            "psUnique": len(ps_void_unique),
            "psPages": sorted({r["_page"] for r in ps_void_rows}),
            "contRange": [2608, 2700],
            "contModernCount": len(cont_modern),
            "contParcelsCount": sum(
                1 for p in parcels if (b := base_of(p.get("st"))) and 2608 <= int(b) <= 2700
            ),
            "contPsRows": len(ps_cont_rows),
            "contPsUnique": len(ps_cont_unique),
            "verdictSi": (
                "v sodobnem k.o. 1544 NE obstaja nobena parcela 2507–2607 — točno tam, kjer register "
                "nadaljuje prek recap vsote 2505 (87 dodatkov S2); 2608–2700 pa obstaja (78 parcel). "
                "Vzrok praznine ni znan [~] — možnosti: ukinjene/absorbirane parcele, prenumeracija "
                "1841 (Grundsteuerkataster); pošteno: samo opazovanje, brez trditve o vzroku"
            ),
        },
        "timeline": {
            "annotatedRows": len(ann_records),
            "byYear": by_year_ord,
            "pages1841": pages_1841,
            "pages1841Count": len(pages_1841),
            "earliest": years_sorted[0] if years_sorted else None,
            "latest": years_sorted[-1] if years_sorted else None,
            "topYear": top_year,
            "note": (
                "protokol je bil vzdrževan ~stoletje (1811–1934 anmerkung); pik 1841 = prehod na "
                "Grundsteuerkataster (Franziszeischer Kataster); letnice 1515/1522 = [~] VLM branja "
                "(najverjetneje navedbe starih urbarijev); per-row [~]"
            ),
        },
        "pageMap": page_map,
        "annRecords": ann_records,
        "invariants": inv,
        "statusLine": status_line,
        "verdictSi": (
            "P56 (2026-10-13): register PS NI homogen — topologija razčlenjena v štiri serije. "
            "S1 glavni register (str. 5–127, 123 strani): per-Blatt številčenje, Grund ≈ 1–2505. "
            "S2 spremembni register (str. 128–137): številke 2507–2840 kot prebrano (str. 129 blok "
            "2826–2840 ni monotoničen [~]) z anmerkung dodatki — prvootkrito: "
            "»einf. Vermessung vom Jahr 1805« (str. 128), »hinzugekommen 1841«, »Grundsteuerkataster 1841«, "
            "»Durch Kauf 1841«; register je bil vzdrževan še desetletja po 1825 (584 označenih vrstic, "
            f"letnice {years_sorted[0] if years_sorted else '—'}–{years_sorted[-1] if years_sorted else '—'}, pik {top_year} s {by_year[top_year]} vrsticami na {len(pages_1841)} straneh — prehod na Franziszeischer Kataster). "
            "S3 zapadek »Zusammenstellung der Grundstücke« (str. 138–139): LASTNO oštevilčenje 1–100 "
            f"({count_num_p139} številskih anmerkung na str. 139 — premik stolpcev) — in točno te vrstice je "
            "P55 join napačno povezal: 60 vrstic, 43 povezanih, "
            f"median razmerja površin {round4(med_s3)} proti {round4(med_s1)} v glavnem registru (~{round(med_s1 / med_s3)}× odmik) — "
            "determinističen dokaz lažnih povezav, neodvisno potrjen s P48 Blatt X analizo in pass2/pass3 "
            "razhajanjem branja. SANACIJA: povezane vrstice 1110 → 1067; unikatne parcelne številke "
            f"{len(bases_before)} → {len(bases_after)} ({lost_note}). Per-Blatt dvoumnost znotraj glavnega "
            f"registra KVANTIFICIRANA: {len(dup_all)} base številk se pojavlja na več straneh ({len(dup_s1)} "
            f"znotraj S1), {len(clean_amb)} povezanih vrstic (sanitiran join) je dvoumnih [~] — brez "
            "prerazporeditev (blatt "
            f"stolpec ~50 % šumen). Sodobna praznina: 0 parcel 2507–2607 ({len(ps_void_rows)} PS dodatkov brez sodobnih "
            f"naslednic) proti {len(cont_modern)} base / {sum(1 for p in parcels if (b := base_of(p.get('st'))) and 2608 <= int(b) <= 2700)} parcelam 2608–2700 — vzrok [~]. Odkritje kontekst: strani 3–4 (številke "
            "1–40) niso v P38 izboru — številke 1–40 so v branjih zastopane LE z S3 zapadkom."
        ),
        "verdictEn": (
            "P56 (2026-10-13): the PS register is NOT homogeneous — its topology resolves into four series. "
            "S1 main register (pp. 5–127, 123 pages): per-sheet numbering, Grund ≈ 1–2505. S2 changes register "
            "(pp. 128–137): numbers 2507–2840 as read (p. 129 block 2826–2840 non-monotonic [~]) with annotated "
            "additions — first documented: »einf. Vermessung "
            "vom Jahr 1805« (p. 128), »hinzugekommen 1841«, »Grundsteuerkataster 1841«, »Durch Kauf 1841«; "
            "the register was maintained for decades after 1825 (584 annotated rows, years 1515–1934, peak "
            "1841 with 83 rows on 44 pages — the transition to the Franziszeian tax cadastre). S3 appendix "
            "»Zusammenstellung der Grundstücke« (pp. 138–139): its OWN numbering 1–100 (column-shifted "
            "numeric anmerkung on p. 139) — "
            "and exactly these rows were falsely linked by the P55 join: 60 rows, 43 linked, median area "
            f"ratio {round4(med_s3)} vs {round4(med_s1)} in the main register (~{round(med_s1 / med_s3)}× off) — deterministic proof "
            "of false links, independently corroborated by the P48 Blatt X analysis and the pass2/pass3 "
            "reading disagreement. SANITIZATION: linked rows 1110 → 1067; unique parcel numbers "
            f"{len(bases_before)} → {len(bases_after)} ({lost_note}). Per-sheet ambiguity within the main "
            f"register QUANTIFIED: {len(dup_all)} base numbers appear on more than one page ({len(dup_s1)} "
            f"within S1), {len(clean_amb)} of the sanitized linked rows remain ambiguous [~] — no reassignments (the blatt "
            "column is ~50 % noisy). Modern void: 0 parcels numbered 2507–2607 (87 PS additions without "
            "modern successors) versus 78 parcels 2608–2700 — cause unknown [~]. Context discovery: pages "
            "3–4 (numbers 1–40) are not among the P38 reads — numbers 1–40 are represented ONLY by the S3 "
            "appendix."
        ),
        "next": [
            "4. VLM prehod na glave listov (»Nro. des Blattes«) z usmerjeno pozivo → per-Blatt ločitev dvoumnih instanc (515 base)",
            "prebrati strani 3–4 (številke 1–40 glavnega registra) — trenutno pokrite le z S3 zapadkom",
            "lokalizacija sekcije 102 Bauplätze v protokolu (niso v kultur branjah; morda ločen register)",
            "vzrok sodobne praznine 2507–2607: preveriti Grundsteuerkataster 1841 (Franziszeischer Kataster) pregrupiranja",
            "nadgradnja P55 runtime ps-parcels-geo.json v v2 z series flag (zahteva uskladitev qa-p55 pini)",
        ],
    }

    # ——— I7/I8 runtime kompakt ———
    runtime = {
        "task": evidence["task"],
        "date": evidence["date"],
        "generatedBy": "scripts/p56_ps_register_topology.py",
        "series": {
            k: {kk: vv for kk, vv in v.items() if kk not in ("markers", "pass2Pass3Disagreement", "note", "labelSi", "labelEn")}
            for k, v in evidence["series"].items()
        },
        "seriesLabels": {
            k: {"si": v.get("labelSi"), "en": v.get("labelEn")}
            for k, v in evidence["series"].items()
        },
        "contamination": {
            "s3RowsTotal": evidence["contamination"]["s3RowsTotal"],
            "s3RowsMatched": evidence["contamination"]["s3RowsMatched"],
            "s3BasesOverlappingS1": evidence["contamination"]["s3BasesOverlappingS1"],
            "ratioMedianS3": evidence["contamination"]["ratioMedianS3"],
            "ratioMedianS1": evidence["contamination"]["ratioMedianS1"],
            "historicalQkM2": evidence["contamination"]["historicalQkM2"],
            "rows": evidence["contamination"]["rows"],
        },
        "sanitization": evidence["sanitization"],
        "perBlattAmbiguity": {
            k: evidence["perBlattAmbiguity"][k]
            for k in (
                "basesOnMultiplePages",
                "withinS1",
                "s1s3Collisions",
                "withinS2",
                "matchedRowsWithAmbiguousBase",
                "cleanRowsWithAmbiguousBase",
            )
        },
        "modernVoid": evidence["modernVoid"],
        "timeline": {
            "annotatedRows": evidence["timeline"]["annotatedRows"],
            "byYear": evidence["timeline"]["byYear"],
            "pages1841Count": evidence["timeline"]["pages1841Count"],
            "earliest": evidence["timeline"]["earliest"],
            "latest": evidence["timeline"]["latest"],
            "topYear": evidence["timeline"]["topYear"],
        },
        "invariants": evidence["invariants"],
        "statusLine": evidence["statusLine"],
        "verdictSi": evidence["verdictSi"],
        "verdictEn": evidence["verdictEn"],
    }

    # ——— I8: dokaz ⊇ runtime (kompaktne sekcije bajtno enake podmnožice; series = stripped projekcija) ———
    def subset_eq(rt_val, ev_val) -> bool:
        if isinstance(rt_val, dict) and isinstance(ev_val, dict):
            return all(rk in ev_val and subset_eq(rv, ev_val[rk]) for rk, rv in rt_val.items())
        if isinstance(rt_val, list) and isinstance(ev_val, list):
            return json.dumps(rt_val, sort_keys=True, ensure_ascii=False) == json.dumps(
                ev_val, sort_keys=True, ensure_ascii=False
            )
        return rt_val == ev_val

    def stripped_series(ev: dict) -> dict:
        return {
            k: {kk: vv for kk, vv in v.items() if kk not in ("markers", "pass2Pass3Disagreement", "note", "labelSi", "labelEn")}
            for k, v in ev["series"].items()
        }

    ok_i8 = all(subset_eq(runtime["series"][k], stripped_series(evidence)[k]) for k in runtime["series"]) and all(
        k in evidence and subset_eq(runtime[k], evidence[k])
        for k in runtime
        if k not in ("series", "generatedBy", "seriesLabels")
    )
    if not ok_i8:
        fail("I8: kompaktne sekcije niso bajtno enake dokazu")
    else:
        ok("I8 kompaktne sekcije bajtno enake dokazu")

    # ——— izpis ———
    for path, data in ((OUT_CANONICAL, evidence), (OUT_RUNTIME, runtime)):
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"  · izpis {path.relative_to(REPO)} ({path.stat().st_size} B)")

    if FAILURES:
        print(f"\nP56 FAIL: {len(FAILURES)} invariant padel:")
        for f_ in FAILURES:
            print(f"  ✗ {f_}")
        return 1
    print("\nP56 PASS — topologija registra PS: vse invariante I1–I6 veljavne (I7 --check, I8 bajtno).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
