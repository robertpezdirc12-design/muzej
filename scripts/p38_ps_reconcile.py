#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P38 (issue #10) — N083PS: DETERMINISTIČNA SPRAVA strojno prebranega protokola
Grund-Parcellen der Gemeinde Grüble.

Kaj naredi (vse izključno iz committed dokazov research/issue17/ps-raw/):
  1. Klasifikacija vsake vrstice v sekcijo (GRUND_1_2505 / NADALJEVANJE_2506_PLUS /
     WALDUNG / BLATT_X) po eksplicitnih pravilih (spodaj), ki jih je mogoče
     neodvisno preveriti.
  2. Razdvojitev večkulturnih vrstic: ista parcela z več rabami (kultur) →
     en par parcela×raba (določa štetje vrstic po razdvojitvi).
  3. Pokritost glavnega niza 1–2505 proti kontrolni vsoti 102 + 2505 = 2607
     (str. 143, rdeči tuš; po P36 šteje KATEGORIJE, ne maksimum številke).
  4. Kandidati za izgubo vodilne števke (161→61) po konzervativnem
     determinističnem pravilu — NE popravlja podatkov, samo izrecno označi.
  5. Občutljivostna analiza treh pravil branja: pass1-only / pass2-wins / union.

Pravila branja (P38 RULESET v1, committed skozi ta skript):
  - Razpoložljive vrstice: ps-NNN.json (pass-1, 135 strani) in
    ps-NNN-pass2.json (pass-2, 78 strani z okvarjeno soslednostjo).
  - SEKCIJA (per row, v tem vrstnem redu):
      BLATT_X           stran 138 ali 139 (lastno številčenje, PS-structure.json
                        str. 3/4 in audit §17; podatki: 1–20 in 81–100, s hišnimi št.)
      WALDUNG           parcela ≥ 2601 IN hišna št. ni prisotna (str. 133–137:
                        skupna gozdna zemlja brez hišnih št.)
      NADALJEVANJE_2506 parcela ≥ 2506 (s hišnimi št.; nadaljevalni niz prek 2505,
                        vključno s Schmiegärten po auditu §17, str. ~128–130)
      GRUND_1_2505      parcela 1–2505
      NEBEREŽNA         vrstica brez številčne parcele (izrecno šteta, izločena
                        iz prostorskih štetij)
  - Blatt X se IZLOČI iz primerjave s kontrolno vsoto (lastno številčenje,
    ni Grundparzellen niza).
  - P36 osnovna črta: PS-full.json totals (grundSeen 1889, over2505 176,
    grundMissing 616) se pod pravilom pass2-wins + izločitvijo Blatt X
    REPRODUCIRA natanko — to je izračunano in potrjeno v tem skriptu.

Izpiše: research/issue17/ps-reconciliation.json (+ povzetek na stdout).
Vrni izhodna števila v TS konstanto PS_RECONCILIATION_P38 (src/data/atlas/research.ts)
in QA test qa-p38-ps-reconciliation (src/lib/qa.ts) — ročno, s skriptnim izpisom.

Status vseh rezultatov ostaja REVIEW (strojno branje ni dokazni vir) —
pravilo hiše: »ne nadgradi gotovosti brez človeške paleografske potrditve«.
"""

import json
import glob
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "research" / "issue17" / "ps-raw"
OUT = ROOT / "research" / "issue17" / "ps-reconciliation.json"

BLATT_X_PAGES = {138, 139}
CHECKSUM_TARGET = {"bauplatze": 102, "grundparzellen": 2505, "skupaj": 2607}


def load_passes():
    """Vrni (pass1: {stran: vrstice}, pass2: {stran: vrstice})."""
    p1, p2 = {}, {}
    for f in sorted(glob.glob(str(RAW / "ps-*.json"))):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        page = d["page"]
        rows = (d.get("parsed") or {}).get("vrstice") or []
        if "pass2" in Path(f).name:
            p2[page] = rows
        else:
            p1[page] = rows
    return p1, p2


def parcel_int(row):
    v = row.get("parzella")
    if v is None:
        return None
    s = str(v).strip()
    if not re.fullmatch(r"\d+", s):
        return None
    return int(s)


def classify(page, row):
    """Sekcija vrstice po P38 pravilih (glej docstring)."""
    n = parcel_int(row)
    if n is None:
        return "NEBEREŽNA", None
    if page in BLATT_X_PAGES:
        return "BLATT_X", n
    if n >= 2601 and not (row.get("hausNr") or "").strip():
        return "WALDUNG", n
    if n >= 2506:
        return "NADALJEVANJE_2506", n
    return "GRUND_1_2505", n


def read_rule(p1, p2, rule):
    """Izberi vrstice po pravilu: pass1 | pass2wins | union."""
    pages = sorted(set(p1) | set(p2))
    chosen = {}
    for pg in pages:
        if rule == "pass1":
            chosen[pg] = p1.get(pg, [])
        elif rule == "pass2wins":
            chosen[pg] = p2.get(pg, p1.get(pg, []))
        else:  # union
            chosen[pg] = p1.get(pg, []) + p2.get(pg, [])
    return pages, chosen


def compact_ranges(nums):
    """[3,4,5,9] → '3–5, 9' (za človeško berljive sezname)."""
    ns = sorted(set(nums))
    if not ns:
        return ""
    parts, start, prev = [], ns[0], ns[0]
    for n in ns[1:] + [None]:
        if n is not None and n == prev + 1:
            prev = n
            continue
        parts.append(f"{start}–{prev}" if prev > start else f"{start}")
        if n is not None:
            start = prev = n
    return ", ".join(parts)


def ocr_candidates(pages_rows):
    """OCR kandidati znotraj ENE bralne seje: parcela < 100 zunaj Blatt X,
    kjer so VSE ostale parcele strani ≥ 100 (vsaj 3) → domnevna izguba
    vodilne števke (+100). Kandidat mora obstajati znotraj enega branja."""
    out = []
    for pg, rows in sorted(pages_rows.items()):
        if pg in BLATT_X_PAGES:
            continue
        nums = [parcel_int(r) for r in rows]
        nums = [n for n in nums if n is not None]
        others = [n for n in nums if n >= 100]
        for n in sorted(set(n for n in nums if n < 100)):
            if len(set(others)) >= 3 and min(others) - n >= 40:
                out.append(
                    {
                        "page": pg,
                        "parcel": n,
                        "suggestion": n + 100,
                        "evidence": f"str. {pg}: min drugih={min(others)}, max={max(others)}, št. drugih={len(set(others))}",
                    }
                )
    out.sort(key=lambda x: (x["page"], x["parcel"]))
    return out


def analyze(p1, p2, rule):
    pages, chosen = read_rule(p1, p2, rule)
    sec_rows = defaultdict(int)           # sekcija → vrstic
    sec_par = defaultdict(set)            # sekcija → distinct parcele
    sec_pages = defaultdict(set)          # sekcija → strani
    rows_no_parcel = 0
    rows_nonnum_parcel = 0
    # večkulturne vrstice: parcela(sekcija) → množica rab
    cultures = defaultdict(set)
    culture_pages = defaultdict(set)

    for pg in pages:
        for row in chosen[pg]:
            sec, n = classify(pg, row)
            sec_rows[sec] += 1
            if sec != "NEBEREŽNA":
                sec_par[sec].add(n)
                sec_pages[sec].add(pg)
                k = (row.get("kultur") or "").strip()
                if k:
                    cultures[(sec, n)].add(k)
                    culture_pages[(sec, n)].add(pg)
            elif row.get("parzella") is None:
                rows_no_parcel += 1
            else:
                rows_nonnum_parcel += 1

    # 1–2505 pokritost (Blatt X po pravilih ni v GRUND_1_2505 — brez vpliva)
    grund = sec_par["GRUND_1_2505"]
    missing = [n for n in range(1, 2506) if n not in grund]

    # OCR kandidati po sejah: seja-1 = pass-1 (vse strani); seja-2 = pass-2
    # (78 strani) dopolnjena s pass-1 na preostalih. Kandidat obstaja, če
    # ga zazna KATERAKOLI seja — nikoli čez mešanih dveh branj strani.
    s1 = {pg: rows for pg, rows in p1.items()}
    s2 = {pg: p2.get(pg, p1.get(pg, [])) for pg in set(p1) | set(p2)}
    seen, ocr = set(), []
    for cand in ocr_candidates(s1) + ocr_candidates(s2):
        key = (cand["page"], cand["parcel"])
        if key not in seen:
            seen.add(key)
            ocr.append(cand)

    # večkulturne vrstice (isti parcela+sekcija, več rab) — razdvojitev
    multi = {
        f"{sec}#{n}": sorted(ks)
        for (sec, n), ks in cultures.items()
        if len(ks) > 1
    }
    pairs = len(cultures)  # parcela×raba parov (po razdvojitvi)
    rows_total = sum(sec_rows.values())
    pass1_rows_total = sum(len(v) for v in p1.values())

    return {
        "pass1RowsTotal": pass1_rows_total,
        "sections": {
            sec: {
                "rows": sec_rows.get(sec, 0),
                "distinctParcels": len(sec_par.get(sec, set())),
                "pages": sorted(sec_pages.get(sec, set())),
                "range": (
                    [
                        min(sec_par[sec]),
                        max(sec_par[sec]),
                    ]
                    if sec_par.get(sec)
                    else None
                ),
            }
            for sec in [
                "GRUND_1_2505",
                "NADALJEVANJE_2506",
                "WALDUNG",
                "BLATT_X",
                "NEBEREŽNA",
            ]
        },
        "splitting": {
            "rowsBefore": rows_total,
            "parcelCulturePairs": pairs,
            "rowsAfter": pairs + rows_no_parcel + rows_nonnum_parcel,
            "parcelsWithMultipleCultures": len(multi),
            "extraRowsFromMultiCulture": rows_total - pairs - rows_no_parcel - rows_nonnum_parcel,
            "examples": {k: multi[k] for k in sorted(multi)[:10]},
            "rowsWithoutParcel": rows_no_parcel,
            "rowsWithNonNumericParcel": rows_nonnum_parcel,
        },
        "coverage": {
            "grundDistinct": len(grund),
            "grundMissing": len(missing),
            "grundCoveragePct": round(100 * len(grund) / 2505, 1),
            "grundMissingRanges": compact_ranges(missing),
            "nad2506Distinct": len(sec_par.get("NADALJEVANJE_2506", set())),
            "nad2506Range": (
                [
                    min(sec_par.get("NADALJEVANJE_2506", set())),
                    max(sec_par.get("NADALJEVANJE_2506", set())),
                ]
                if sec_par.get("NADALJEVANJE_2506")
                else None
            ),
            "waldungDistinct": len(sec_par.get("WALDUNG", set())),
            "waldungRange": (
                [
                    min(sec_par.get("WALDUNG", set())),
                    max(sec_par.get("WALDUNG", set())),
                ]
                if sec_par.get("WALDUNG")
                else None
            ),
            "blattXDistinct": len(sec_par.get("BLATT_X", set())),
            "blattXRange": (
                [min(sec_par.get("BLATT_X", set())), max(sec_par.get("BLATT_X", set()))]
                if sec_par.get("BLATT_X")
                else None
            ),
        },
        "ocrLeadingDigitCandidates": {
            "count": len(ocr),
            "note": "konzervativno pravilo: parcela < 100 zunaj Blatt X na strani, kjer so vse ostale parcele ≥ 100 (≥ 3) → domnevna izguba vodilne števke; NE popravi podatkov, status ostaja REVIEW",
            "list": ocr,
        },
        "checksumReconciliation": {
            "target": CHECKSUM_TARGET,
            "grundSeenVsTarget": len(grund),
            "grundMissingVsTarget": len(missing),
            "verdictSi": (
                "DELNO USKLAJENO: glavni niz 1–2505 pokrit "
                f"{len(grund)}/2505 ({round(100*len(grund)/2505,1)} %); preostalih "
                f"{len(missing)} parcel = strojno neodčitane/okvarjene vrstice, "
                "kandidati napak OCR in vloge Blatt X še niso spravljene; "
                "povprečje kontrolne vsote (102+2505=2607 kategorij) zahteva "
                "3. prehod dvoumnih strani in primerjavo z rekapitulacijo 140–143"
            ),
            "status": "REVIEW",
            "next": [
                "3. prehod ~15 dvoumnih strani (audit §17, npr. str. 84, 138)",
                "razdvojitev večkulturnih vrstic v spravni model (podatki pripravljeni)",
                "primerjava posameznih parcel z rekapitulacijo str. 140–143 (P5-b)",
                "človeška paleografska potrditev kandidatov za napake OCR",
            ],
        },
    }


def main():
    p1, p2 = load_passes()
    rules = {r: analyze(p1, p2, r) for r in ["pass1", "pass2wins", "union"]}

    # P36 osnovna črta: PS-full.json totals pod pravilom pass2wins
    full = json.loads((ROOT / "research" / "issue17" / "PS-full.json").read_text(encoding="utf-8"))
    t = full["totals"]
    r2 = rules["pass2wins"]["coverage"]
    p36_reproduced = (
        r2["grundDistinct"] == t["grundSeen"]
        and (r2["nad2506Distinct"] + r2["waldungDistinct"]) == len(t["over2505"])
        and r2["grundMissing"] == t["grundMissing"]
        and r2["blattXDistinct"] == t["bauplatzeSeen"]
    )

    report = {
        "series": "PS",
        "source": "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani)",
        "method": "P38 deterministična sprava (ta skript, committed) nad committed "
        "dokazi research/issue17/ps-raw/ (213 VLM branj, P36); brez AI ob delovanju, "
        "brez urejanja surovih podatkov; vsi statusi ostajajo REVIEW",
        "rulebook": {
            "readingPreference": "pass2wins (stran s pass-2 zapisom uporabi pass-2, sicer pass-1); občutljivost za pass1 in union spodaj",
            "sections": [
                "BLATT_X: stran 138 ali 139 (lastno številčenje; PS-structure.json str. 3/4, audit §17)",
                "WALDUNG: parcela ≥ 2601 brez hišne št. (str. 133–137, skupna gozdna zemlja)",
                "NADALJEVANJE_2506: parcela ≥ 2506 s hišno št. (nadaljevalni niz prek 2505, vključno s Schmiegärten)",
                "GRUND_1_2505: parcela 1–2505 (glavni niz do kontrolne vsote)",
                "NEBEREŽNA: vrstica brez številčne parcele (izrecno šteta, izločena iz prostorskih štetij)",
            ],
            "checksum": "102 Bauplätze + 2505 Grundparzellen = 2607 KATEGORIJ (str. 143, rdeči tuš; P36) — ni maksimum številke",
            "blattXExclusion": "Blatt X se izloči iz primerjave s 2607 (lastno številčenje, ni del Grundparzellen niza)",
        },
        "p36Baseline": {
            "psFullTotals": {
                "grundSeen": t["grundSeen"],
                "grundMissing": t["grundMissing"],
                "over2505Count": len(t["over2505"]),
                "bauplatzeSeen": t["bauplatzeSeen"],
            },
            "reproducedUnderPass2wins": p36_reproduced,
            "note": (
                "P36 štetja se pod pravilom pass2wins + izločitvijo Blatt X "
                "REPRODUCIRAJO natanko: grundSeen 1889 = distinct GRUND_1_2505; "
                "over2505 176 = NADALJEVANJE_2506 (95) + WALDUNG (81); "
                "grundMissing 616 = 2505 − 1889; bauplatzeSeen 60 = distinct "
                "BLATT_X — P38 torej razreši tudi poreklo bauplatzeSeen: to je "
                "stevec lastno številčenega odseka Blatt X (str. 138–139), ki "
                "po strukturi protokola nosi stavbna mesta (cilj 102)"
                if p36_reproduced
                else "POZOR: P36 štetij pod pravilom pass2wins NI uspelo reproducirati — preveri rulebook!"
            ),
        },
        "readingRule": "pass2wins",
        **rules["pass2wins"],
        "sensitivity": {
            r: {
                "grundDistinct": rules[r]["coverage"]["grundDistinct"],
                "grundMissing": rules[r]["coverage"]["grundMissing"],
                "nad2506Distinct": rules[r]["coverage"]["nad2506Distinct"],
                "waldungDistinct": rules[r]["coverage"]["waldungDistinct"],
                "ocrCandidates": rules[r]["ocrLeadingDigitCandidates"]["count"],
            }
            for r in ["pass1", "pass2wins", "union"]
        },
        "negativeResults": [
            "večkulturne vrstice pri razdvojitvi NISO šle v aplikacijski model (samo štetja) — strukturna zagata str. 84 (22 vrstic za 8 parcel) ostaja za 3. prehod",
            "zamenjave števk 3↔1 in 8↔5 (audit §17) NISO deterministično zaznavne brez lažnih pozitivov — samo izguba vodilne števke ima kandidatsko pravilo",
            "parcela 680 (str. 5) je očitno okvarjena (hišna št. namesto parcele), a ne ustreza pravilu <100 — ostaja REVIEW brez samodejnega popravka",
            "P36 podatek pagesRead=8/143 v inventarju (qa-p20) označuje STRUKTURNO branje (P20); strojni prepis 135 strani (P36) je dokumentiran ločeno — semantika scopeCheck ni spreminjana",
        ],
        "generatedBy": "scripts/p38_ps_reconcile.py",
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    # povzetek na stdout (za commit sporočilo)
    cov = report["coverage"]
    spl = report["splitting"]
    print("=== P38 SPRAVA (pass2wins) ===")
    print(f"GRUND_1_2505:      vrstice={report['sections']['GRUND_1_2505']['rows']}, distinct={cov['grundDistinct']}, manjka={cov['grundMissing']} ({cov['grundCoveragePct']} % pokritosti)")
    print(f"NADALJEVANJE_2506: distinct={cov['nad2506Distinct']}, obseg={cov['nad2506Range']}")
    print(f"WALDUNG:           distinct={cov['waldungDistinct']}, obseg={cov['waldungRange']}")
    print(f"BLATT_X:           distinct={cov['blattXDistinct']}, obseg={cov['blattXRange']}")
    print(f"razdvojitev: {spl['rowsBefore']} vrstic → {spl['parcelCulturePairs']} parov parcela×raba; parcel z več rabami={spl['parcelsWithMultipleCultures']}, presežek={spl['extraRowsFromMultiCulture']}")
    print(f"OCR kandidati (vodilna števka): {report['ocrLeadingDigitCandidates']['count']}")
    print(f"P36 osnovna črta reproducirana: {p36_reproduced}")
    print(f"občutljivost: {json.dumps(report['sensitivity'], ensure_ascii=False)}")
    print(f"izpis: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
