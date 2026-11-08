#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P39 (issue #10) — N083PS: RAZDVOJITEV VEČKULTURNIH VRSTIC V SPRAVNI MODEL
(parcela × raba) + deterministična klasifikacija rab.

Kaj naredi (izključno iz committed dokazov research/issue17/ps-raw/, P36):
  1. S P38 pravili (identična klasifikacija sekcij + pravilo branja pass2wins)
     združi ravne vrstice v MODEL PO PARCELAH: vsak (sekcija, parcela) = en
     vnos z razčlenjenimi rabami (kulturami), strani, hišno št., lastniki,
     površino in opombo. Nobena vrstica ni izgubljena: vsote se pokrijejo.
  2. Razdvojitev: večkulturna parcela (več rab) postane en vnos z več
     kulturen — model ohrani število vrstic dokaza per kultura (podvojene
     iste rabe ostajo vidne kot rows > 1, niso tiho spletene).
  3. NEBEREŽNA vrstice (neštevilčna parcela) ostanejo v modelu doslovno
     (frakcijske parcele »76½«, »[?]« …) — zero-loss tudi zanje.
  4. Klasifikacija rab (ZA STATISTIKO; surove vrednosti ostanejo nedotaknjene):
     ekspliciten pravilnik v1 — besedni vzorci nemških katastrskih terminov
     (Acker/Wiese/Wald/Weide/Alm/Garten/Ödung/Bauplatz/…); vse, česar pravila
     ne pokrijejo, je izrecno NEKLASIFICIRANO. Brez AI ob delovanju.
  5. Navzkrižne kontrole s P38 (PS_RECONCILIATION_P38): 2118 = parcele z vsaj
     eno rabo; sekcije 1889/95/81/60 vključno s sirotami.

IZBOLJŠAVE ŠTETJA NASPROTI P38 (nove ugotovitve, P38 konstante ostanejo):
  - P38 "parcelCulturePairs" 2118 so v resnici VNOSI PO PARCELAH z vsaj eno
    rabo; skupaj z 7 sirotami (parcela brez nobene rabe, samo prazna
    kultur-stolpec) je pravih vnosov 2125, model skupaj 2134 (2125 + 9
    NEBEREŽNA), ne 2127.
  - pravih različnih parov parcela×raba je 2632 (P38 številka je bila vnosov);
    49 vrstic ponovi rabo znotraj svoje parcele (rows > 1) — ohranjene.
  - 70 vrstic je numeričnih brez kulture: 63 na parcelah, ki imajo tudi rabo
    (prevzete v model), 7 na sirotah (izrecni vnosi brez rabe).

Izpiše:
  - research/issue17/ps-landuse.json   (kanonski dokazni izpis — POLNI model)
  - src/data/atlas/ps-landuse.json     (identična kopija za runtime import API)
  - povzetek na stdout (za TS konstanto PS_LANDUSE_P39 in QA qa-p39).

Status vseh rezultatov ostaja REVIEW (strojno branje ni dokazni vir) —
pravilo hiše: »ne nadgradi gotovosti brez človeške paleografske potrditve«.
"""

import json
import glob
import re
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "research" / "issue17" / "ps-raw"
OUT_EVIDENCE = ROOT / "research" / "issue17" / "ps-landuse.json"
OUT_RUNTIME = ROOT / "src" / "data" / "atlas" / "ps-landuse.json"

BLATT_X_PAGES = {138, 139}
SECTION_ORDER = ["GRUND_1_2505", "NADALJEVANJE_2506", "WALDUNG", "BLATT_X"]

# ——— P39 pravilnik klasifikacije rab (v1, determinističen, brez AI) ———
# Vrstni red je del pravilnika: prvi zadetek = primarni razred.
# Vzorci se uporabijo nad normalizirano vrednostjo (male črke, ä→ae, ö→oe,
# ü→ue, ß→ss). Surova vrednost v modelu ostane vedno nedotaknjena.
CULTURE_RULES = [
    ("VINOGRAD", "weingarten|weinberg"),
    ("NJIVA", r"\backer\w*|\baecke\w*"),
    ("TRAVNIK", r"wies|\bwey\b"),
    ("GOZD", r"\bwald\w*"),
    ("PASTVISCE", r"\bweid\w*|\bhut\w*|\btrift\w*"),
    ("ALM", r"\balm\w*|\balp\w*"),
    ("VRT", r"gart"),
    ("NEROD", r"\boed\w*"),
    ("STAVBNO", r"bauplatz|hof\w*|stadel|stadl|schupfn|purgstall|muehl|muhl|\bhaus\w*|anger\w*"),
    ("VODA", r"\bteich\w*|\bfluss\w*|\bbach\w*|lokva"),
    ("OBCINA", r"gemeinde"),
    ("CESTA", r"\bweg\w*|steig\w*"),
]

RULE_LABELS_SI = {
    "VINOGRAD": "vinograd",
    "NJIVA": "njiva (Acker)",
    "TRAVNIK": "travnik (Wiese)",
    "GOZD": "gozd (Wald)",
    "PASTVISCE": "pašnik (Weide/Hutweide/Trift)",
    "ALM": "planina (Alm/Alpe)",
    "VRT": "vrt (Garten, Schmiegärten)",
    "NEROD": "nerodovoljna zemlja (Ödung)",
    "STAVBNO": "stavbna/gospodarska (Bauplatz, Hof, Stadl, Mühle …)",
    "VODA": "voda (Teich, Fluss, Bach, lokva)",
    "OBCINA": "občinska skupna zemlja (Gemeinde)",
    "CESTA": "pot/cesta (Weg, Steig)",
}


def norm(s: str) -> str:
    s = s.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    return s


def classes_of(raw: str):
    n = norm(raw)
    return [cls for cls, pat in CULTURE_RULES if re.search(pat, n)]


def load_passes():
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
    """Identično pravilom P38 (scripts/p38_ps_reconcile.py)."""
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


def to_int(v):
    if v is None:
        return None
    s = str(v).strip()
    return int(s) if re.fullmatch(r"\d+", s) else None


def build_model(p1, p2):
    pages = sorted(set(p1) | set(p2))
    entries = {}  # (sec, n) → vnos
    neberezna = []
    rows_before = 0

    for pg in pages:
        for idx, row in enumerate(p2.get(pg, p1.get(pg, [])), start=1):
            rows_before += 1
            sec, n = classify(pg, row)
            k = (row.get("kultur") or "").strip()
            if sec == "NEBEREŽNA":
                neberezna.append(
                    {
                        "key": f"NEBEREŽNA#p{pg}r{idx}",
                        "section": "NEBEREŽNA",
                        "page": pg,
                        "row": idx,
                        "parcelAsRead": str(row.get("parzella") or "").strip(),
                        "kultur": k,
                        "hausNr": (row.get("hausNr") or "").strip() or None,
                        "owner": (row.get("name") or "").strip() or None,
                        "joch": to_int(row.get("joch")),
                        "klafter": to_int(row.get("klafter")),
                        "note": (row.get("anmerkung") or "").strip() or None,
                    }
                )
                continue
            e = entries.setdefault(
                (sec, n),
                {
                    "key": f"{sec}#{n}",
                    "section": sec,
                    "parcel": n,
                    "pages": set(),
                    "blatt": None,
                    "hausNr": [],
                    "owner": [],
                    "rows": 0,
                    "note": None,
                    "cultures": {},  # raw → podatek
                    "cultureOrder": [],
                },
            )
            e["pages"].add(pg)
            e["rows"] += 1
            b = (row.get("blatt") or "").strip()
            if b and e["blatt"] is None:
                e["blatt"] = b
            hn = (row.get("hausNr") or "").strip()
            if hn and hn not in e["hausNr"]:
                e["hausNr"].append(hn)
            nm = (row.get("name") or "").strip()
            if nm and nm not in e["owner"]:
                e["owner"].append(nm)
            an = (row.get("anmerkung") or "").strip()
            if an and e["note"] is None:
                e["note"] = an
            if k:
                if k not in e["cultures"]:
                    e["cultures"][k] = {"rows": 0, "pages": set(), "joch": None, "klafter": None}
                    e["cultureOrder"].append(k)
                c = e["cultures"][k]
                c["rows"] += 1
                c["pages"].add(pg)
                if c["joch"] is None:
                    c["joch"] = to_int(row.get("joch"))
                if c["klafter"] is None:
                    c["klafter"] = to_int(row.get("klafter"))

    return entries, neberezna, rows_before


def finalize(entries):
    out = []
    for (sec, n), e in entries.items():
        cs = []
        for raw in e["cultureOrder"]:
            c = e["cultures"][raw]
            cls = classes_of(raw)
            cs.append(
                {
                    "raw": raw,
                    "classes": cls,
                    "primary": cls[0] if cls else None,
                    "rows": c["rows"],
                    "pages": sorted(c["pages"]),
                    "joch": c["joch"],
                    "klafter": c["klafter"],
                }
            )
        out.append(
            {
                "key": e["key"],
                "section": e["section"],
                "parcel": e["parcel"],
                "pages": sorted(e["pages"]),
                "blatt": e["blatt"],
                "hausNr": e["hausNr"],
                "owner": e["owner"],
                "rows": e["rows"],
                "cultures": cs,
                "note": e["note"],
            }
        )
    out.sort(key=lambda x: (SECTION_ORDER.index(x["section"]), x["parcel"]))
    return out


def main():
    p1, p2 = load_passes()
    entries, neberezna, rows_before = build_model(p1, p2)
    parcels = finalize(entries)

    parcel_entries = len(parcels)
    with_culture = sum(1 for e in parcels if e["cultures"])
    empty_culture = parcel_entries - with_culture
    culture_rows = sum(c["rows"] for e in parcels for c in e["cultures"])
    empty_culture_rows = sum(e["rows"] for e in parcels) - culture_rows
    parcel_culture_pairs = sum(len(e["cultures"]) for e in parcels)
    multi_culture = sum(1 for e in parcels if len(e["cultures"]) > 1)
    duplicate_culture_rows = culture_rows - parcel_culture_pairs
    model_entries = parcel_entries + len(neberezna)

    # ——— klasifikacija rab (nad vrsticami rab parcel) ———
    cls_counts = Counter()
    cls_multi = 0
    uncls = Counter()
    for e in parcels:
        for c in e["cultures"]:
            if c["primary"]:
                cls_counts[c["primary"]] += 1
                if len(c["classes"]) > 1:
                    cls_multi += 1
            else:
                uncls[c["raw"]] += 1
    classified = sum(cls_counts.values())

    # ——— navzkrižna kontrola s P38 (konstante PS_RECONCILIATION_P38) ———
    rec = json.loads((ROOT / "research" / "issue17" / "ps-reconciliation.json").read_text(encoding="utf-8"))
    sec_distinct = {
        sec: sum(1 for e in parcels if e["section"] == sec) for sec in SECTION_ORDER
    }
    p38_sections = rec["sections"]
    cross_ok = (
        with_culture == rec["splitting"]["parcelCulturePairs"]
        and sec_distinct["GRUND_1_2505"] == p38_sections["GRUND_1_2505"]["distinctParcels"]
        and sec_distinct["NADALJEVANJE_2506"] == p38_sections["NADALJEVANJE_2506"]["distinctParcels"]
        and sec_distinct["WALDUNG"] == p38_sections["WALDUNG"]["distinctParcels"]
        and sec_distinct["BLATT_X"] == p38_sections["BLATT_X"]["distinctParcels"]
        and rows_before == rec["splitting"]["rowsBefore"]
        and len(neberezna) == p38_sections["NEBEREŽNA"]["rows"]
    )
    if not cross_ok:
        raise SystemExit("NAVZKRIŽNA KONTROLA S P38 NI USPELA — preveri pravila!")

    # celovitost (zero-loss): vsaka vrstica upoštevana
    accounted = culture_rows + empty_culture_rows + len(neberezna) == rows_before
    if not accounted:
        raise SystemExit("ZERO-LOSS NI POLN: vrstice niso vse upoštevane!")

    top_raw = Counter()
    for e in parcels:
        for c in e["cultures"]:
            top_raw[c["raw"]] += c["rows"]

    report = {
        "series": "PS",
        "source": "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani)",
        "method": "P39 razdvojitev večkulturnih vrstic v spravni model (parcela × raba), "
        "deterministično iz committed dokazov research/issue17/ps-raw/ (213 VLM branj, P36) "
        "s P38 pravili (pass2wins, sekcije); klasifikacija rab po eksplicitnem pravilniku v1 "
        "(brez AI ob delovanju); surove vrednosti nedotaknjene; vsi statusi ostajajo REVIEW",
        "readingRule": "pass2wins",
        "sectionRulebook": rec["rulebook"]["sections"],
        "cultureRulebook": {
            "version": "v1",
            "noteSi": "klasifikacija ZA STATISTIKO — surove rabe v modelu ostanejo nedotaknjene; "
            "prvi zadetek v vrstnem redu = primarni razred; vse, česar pravila ne pokrijejo, "
            "je izrecno NEKLASIFICIRANO (ni ugibanj)",
            "noteEn": "classification FOR STATISTICS ONLY — raw cultures in the model stay untouched; "
            "first match in rule order = primary class; anything the rules do not cover is "
            "explicitly UNCLASSIFIED (no guessing)",
            "rules": [
                {"class": cls, "labelSi": RULE_LABELS_SI[cls], "pattern": pat}
                for cls, pat in CULTURE_RULES
            ],
        },
        "totals": {
            "rowsBefore": rows_before,
            "parcelEntries": parcel_entries,
            "parcelEntriesWithCulture": with_culture,
            "parcelEntriesEmptyCulture": empty_culture,
            "emptyCultureRows": empty_culture_rows,
            "cultureRows": culture_rows,
            "duplicateCultureRows": duplicate_culture_rows,
            "parcelCulturePairs": parcel_culture_pairs,
            "parcelsWithMultipleCultures": multi_culture,
            "nebereznaRows": len(neberezna),
            "modelEntries": model_entries,
        },
        "sections": {
            sec: {"parcelEntries": sec_distinct[sec], "range": rec["sections"][sec]["range"]}
            for sec in SECTION_ORDER
        },
        "cultureClasses": {
            "scope": "štetje po PARIH parcela×raba (parcelCulturePairs) — podvojene rabe znotraj parcele se štejejo enkrat; topCulturesRaw pa po VRSTICAH",
            "classifiedPairs": classified,
            "classifiedPct": round(100 * classified / parcel_culture_pairs, 1) if parcel_culture_pairs else 0.0,
            "primaryCounts": dict(cls_counts.most_common()),
            "multiClassPairs": cls_multi,
            "unclassified": {
                "count": sum(uncls.values()),
                "distinctRaw": len(uncls),
                "top": [{"raw": v, "count": n} for v, n in uncls.most_common(20)],
            },
        },
        "topCulturesRaw": [{"raw": v, "count": n} for v, n in top_raw.most_common(20)],
        "p38CrossCheck": {
            "pairs38": rec["splitting"]["parcelCulturePairs"],
            "rowsAfter38": rec["splitting"]["rowsAfter"],
            "entriesWithCultureMatch38": with_culture == rec["splitting"]["parcelCulturePairs"],
            "sectionsMatch38": True,
            "noteSi": "P38 »parcelCulturePairs« 2118 = vnosi po parcelah z vsaj eno rabo "
            "(sekcije 1889+95+81+60 vključno s sirotami = 2125); P39 pojasni semantiko in "
            "dopolni model: + 7 sirot (70 vrstic brez kulture, pri P38 pod »extra«), "
            "pravih parov parcela×raba 2632, podvojenih rab znotraj parcele 49",
            "noteEn": "P38's »parcelCulturePairs« 2,118 = parcel-level entries with at least one "
            "culture (sections 1,889+95+81+60 including orphans = 2,125); P39 clarifies the "
            "semantics and completes the model: + 7 orphans (70 cultureless rows, subsumed "
            "under »extra« in P38), true parcel×culture pairs 2,632, 49 duplicate-culture rows",
        },
        "parcels": parcels,
        "neberezna": neberezna,
        "generatedBy": "scripts/p39_ps_landuse.py",
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    payload = json.dumps(report, ensure_ascii=False, indent=1) + "\n"
    OUT_EVIDENCE.write_text(payload, encoding="utf-8")
    OUT_RUNTIME.write_text(payload, encoding="utf-8")

    # ——— povzetek za stdout (TS konstanta + commit sporočilo) ———
    t = report["totals"]
    print("=== P39 MODEL RABE TAL (pass2wins) ===")
    print(f"vrstice pred: {t['rowsBefore']}")
    print(f"vnosi po parcelah: {t['parcelEntries']} (z rabo {t['parcelEntriesWithCulture']}, sirote {t['parcelEntriesEmptyCulture']})")
    print(f"model skupaj: {t['modelEntries']} (vnosi {t['parcelEntries']} + NEBEREŽNA {t['nebereznaRows']})")
    print(f"vrstice rab: {t['cultureRows']} → parov parcela×raba: {t['parcelCulturePairs']} (podvojenih rab: {t['duplicateCultureRows']})")
    print(f"parcel z več rabami: {t['parcelsWithMultipleCultures']}")
    print(f"sekcije: {json.dumps(sec_distinct, ensure_ascii=False)}")
    print(f"klasifikacija (po parih): {classified}/{parcel_culture_pairs} ({round(100*classified/parcel_culture_pairs,1)} %); mešanih {cls_multi}; neklasificiranih {sum(uncls.values())} ({len(uncls)} surovih vrednosti)")
    print("primarni razredi:", json.dumps(dict(cls_counts.most_common()), ensure_ascii=False))
    print(f"P38 navzkrižna kontrola: OK (2118/2125/2760/9/1889/95/81/60)")
    print(f"zero-loss: {accounted}")
    print(f"izpisa: {OUT_EVIDENCE.relative_to(ROOT)} + {OUT_RUNTIME.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
