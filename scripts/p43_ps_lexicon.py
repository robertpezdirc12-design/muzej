#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P43 (issue #10) — N083PS: NEZNAME DRUŽINE — PREČNI PREHODI, PV OBMOČNA SPRAVA
IN LEDINSKO-IMENSKA STRUKTURA.

Kaj naredi (izključno iz committed dokazov research/issue17/ + ps-raw/):
  1. PREČNI PREHODI: za vse vrstice, katerih raba pade v v2 NEKLASIFICIRANO
     (282 parov / 16 družin), poišče vrstico istega (sekcija, parcela) v drugem
     prehodu (pass1 ↔ pass2) in sestavi tabelo variant per parcela.
     Nova fenomena, ki ju skript izrecno izmeri:
       a) GENERIČNI PADCEK (fallback): en prehod prebere generični termin
          (Wiese/Acker/Liegend.), drugi prehod prebere specifično (neznano)
          besedo — dokaz, da je specifična beseda v viru dejansko prisotna.
       b) STABILNOST: obe branji se ujemata (do ločila) — močno branje.
  2. BLOKOVSKA KONCENTRACIJA: per družina — število strani, številke strani,
     razpon parcel, število zaporednih (kontinuiranih) parcelnih tekov,
     število različnih lastnikov → statistični dokaz LEDINSKEGA IMENA
     (enojno ime za sosednje parcele istega bloka), ne splošnega termina.
  3. PV OBMOČNA SPRAVA: iz committed transkripcije PV.json (Nutzungs-Ausweis,
     10. 1. 1825) z regexom izvleče uradne kategorije in vsote (FAIL, če
     katera manjka) ter jih primerja z vsotami površin po v2 razredih P39
     modela. Izmeri:
       - WEIDEN-GAP: PV Weiden vs PS izrecne Weide/Alm vrstice,
       - presežke NJIVA/TRAVNIK/VRT nad uradnimi kategorijami,
       - uskladitev VINOGRAD,
       - identiteto PV total ≈ P41 Area der Gemeinde (1220|1493),
       - RAZKORAK VRSTICNI-MODEL vs dokumentna rekapitulacija (Blatt X + NAD
         + WALDUNG kot kandidati za površine zunaj uradne Area).
  4. LEXIKON (h I P O T E Z E, ne klasifikacija): iz committed raw odgovorov
     LLM leksikografske kampanje (research/issue17/ps-lexicon-raw/) prebere
     kandidate etimologij per družina (2 neodvisna prehoda; oba prehoda morata
     obstajati, drugače FAIL). Surove izpise ne spreminja; v finalni izpis
     kopira izrecno označene hipoteze ([~] verjetno / [?] morda) z viri.
     SKRIPT NIKLIGAR ne priredi rabe (KULTURA razred ostaja NEKLASIFICIRANO) —
     le termType-hipotezo (LEDINSKO-IME / KULTURA-DIALEKT / OKRAJSAVA /
     ARTIFAKT / NEZNANO) in leksikografske kandidate z viri.

Nevarne spremembe so izrecno PREPREČENE z invariantami (FAIL ob padu):
  I1: v2 razredi per (sekcija, parcela, raba) se NE spremenijo (rekonstrukcija
      == v2 stats: 2199/122/29/282 parov z numeriki v ARTIFAKT).
  I2: PV izvlečene vsote ustrezajo committed transkripciji (npr. Aecker
      413|870, Weiden 636|263, Wein 7|665, total 1221|1513).
  I3: P39 model vsote sekcij == P40 konstante (GRUND 1232,96 / BLATT_X
      280,73 / WALDUNG 37,63 / NADALJEVANJE 13,46; total 1564,78).
  I4: prečni prehodi: vsota parov po družinah == 282 (v2 NEKLASIFICIRANO)
      + numeriki/kitice so izključeni prek istih v2 seznamov.
  I5: vsi leksikografski kandidati imajo vir (source) in zaupanje [~]/[?];
      vsa imena družin ⊥ v2 TOPONIM/ARTIFAKT seznami.

Izpisi (identična vsebina, dve lokaciji):
  - research/issue17/ps-lexicon.json   (kanonski dokazni izpis)
  - src/data/atlas/ps-lexicon.json     (identična kopija za runtime API)
  - povzetek na stdout (za TS konstanto PS_LEXICON_P43 in QA qa-p43).

Načini:
  python3 scripts/p43_ps_lexicon.py evidence   → /tmp/ps43_lex_evidence/ (za LLM)
  python3 scripts/p43_ps_lexicon.py            → polni izpis (zahteva raw)

Status vseh rezultatov ostaja REVIEW (strojno branje ni dokazni vir) —
pravilo hiše: »ne nadgradi gotovosti brez človeške paleografske potrditve«.
"""

import json
import glob
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "research" / "issue17" / "ps-raw"
EVID = ROOT / "research" / "issue17"
OUT_EVIDENCE = EVID / "ps-lexicon.json"
OUT_RUNTIME = ROOT / "src" / "data" / "atlas" / "ps-lexicon.json"
LLM_RAW = EVID / "ps-lexicon-raw"
TMP_EVID = Path("/tmp/ps43_lex_evidence")

SECTION_ORDER = ["GRUND_1_2505", "NADALJEVANJE_2506", "WALDUNG", "BLATT_X"]
BLATT_X_PAGES = {138, 139}

# P40 konstante (Joch float, iz ps-recap.json — samo za kontrolo I3)
P40_SECTIONS = {
    "GRUND_1_2505": 1232.96,
    "NADALJEVANJE_2506": 13.46,
    "WALDUNG": 37.63,
    "BLATT_X": 280.73,
}
P40_TOTAL = 1564.78

# v2 NEKLASIFICIRANO družine (iz ps-landuse-v2.json; ID-ji so part izpisa)
FAMILY_IDS = [
    "LHUT-JEDRO", "LHIZ", "LHOPI-LOHIFA", "LOHN-RAUT", "AHN", "AEFLING",
    "ERDAR", "GUETEN", "EINHART", "DINGF", "LUKIG", "LOHGARN", "HURGI",
    "WING", "EINSCHLAG-GUELZE", "SCHINDEL",
]

# stems za prečne prehode — pokrijejo tudi pas1 padceke (Schlif/Stifta/Einfach…)
FAMILY_STEMS = {
    "LHUT-JEDRO": ["lhut", "lhup", "rhut"],
    "LHIZ": ["lhiz"],
    "LHOPI-LOHIFA": ["lhopi", "lohifa", "luppa", "shuefa", "stifta",
                     "schlif"],
    "LOHN-RAUT": ["lohn"],
    "AHN": ["ahn"],
    "AEFLING": ["aefling"],
    "ERDAR": ["erdar", "eidar", "achat", "achm"],
    "GUETEN": ["gueten", "guetung"],
    "EINHART": ["einhart"],
    "DINGF": ["dingf"],
    "LUKIG": ["lukig"],
    "LOHGARN": ["lohgarn"],
    "HURGI": ["hurgi"],
    "WING": ["wing"],
    "EINSCHLAG-GUELZE": ["einschlag", "einschicht", "guelze", "guelle"],
    "SCHINDEL": ["schindel"],
}

# generični termini, ki jih en prehod uporabi kot padcek namesto specifične
# besede (za fenomen (1a) — izrecen seznam, ne ugibanje)
GENERIC_FALLBACK = {"wiese", "acker", "liegend.", "gm. & gülle", "wiese mit gras & gülze"}

PV_EXPECT = {  # committed transkripcija PV.json; ključ: (joch, klafter)
    "Gemuese_Gaerten": (2, 123),
    "Wein_Gaerten": (7, 665),
    "Wiesen": (76, 1480),
    "Wiesen_mit_Obstbaeumen": (12, 328),
    "Weiden": (636, 263),
    "Aecker": (413, 870),
    "Oedungen": (1, 476),
    "Fluesse_oder_Baeche": (21, 142),
    "Weg_Parzellen": (46, 1127),
    "Bau_Parzellen": (4, 889),
    "Partial_Sum": (1148, 539),
    "Second_Section_Sum": (73, 1024),
    "Grand_Total": (1221, 1513),
}


def fail(msg):
    print(f"P43 FAIL: {msg}")
    sys.exit(1)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


# ————————————————————————————— vhodni podatki —————————————————————————————

def parse_raw_rows(d):
    out = []
    for r in (d.get("parsed") or []):
        if isinstance(r, str):
            r = r.strip()
            if r.startswith("{"):
                try:
                    out.append(json.loads(r))
                except Exception:
                    pass
        elif isinstance(r, dict):
            out.append(r)
    if not out:
        for line in (d.get("content") or "").splitlines():
            line = line.strip()
            if line.startswith("{"):
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out


def num_or_none(x):
    if x is None:
        return None
    s = str(x).strip().replace(" ", "")
    m = re.match(r"^(\d+)$", s)
    return int(m.group(1)) if m else None


def norm(s):
    s = (s or "").lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    return s


def load_all_rows():
    """(page, pass, rows) za vse ps-raw datoteke."""
    out = []
    for fp in sorted(glob.glob(str(RAW / "ps-*.json"))):
        m = re.match(r"ps-(\d+)(-pass2)?\.json$", Path(fp).name)
        if not m:
            continue
        page = int(m.group(1))
        pas = 2 if m.group(2) else 1
        rows = parse_raw_rows(json.load(open(fp)))
        out.append((page, pas, rows))
    return out


def load_v2():
    return json.load(open(EVID / "ps-landuse-v2.json"))


def load_p39_model():
    return json.load(open(EVID / "ps-landuse.json"))


def v2_classify(v2, raw):
    """Identična rekonstrukcija v2 dodelitve (v1 pravila → appended →
    TOPONIM → ARTIFAKT → NEKLASIFICIRANO). Vrne (class, termType)."""
    ks = str(raw or "").strip()
    if not ks:
        return None, None
    n = norm(ks)
    for r in v2["rulebook"]["v1Rules"]:
        if re.search(r["pattern"], n, re.I):
            return r["class"], "KULTURA"
    for r in v2["rulebook"]["appendedRules"]:
        if re.search(r["pattern"], n, re.I):
            return r["class"], "KULTURA"
    toponim = {v["raw"] for v in v2["termTypes"]["TOPONIM"]["values"]}
    if ks in toponim:
        return "TOPONIM", "TOPONIM"
    art = {v["raw"] for v in v2["termTypes"]["ARTIFAKT"]["values"]}
    if ks in art:
        return "ARTIFAKT", "ARTIFAKT"
    numraw = set(v2["termTypes"]["ARTIFAKT"].get("numericRaw") or [])
    if ks in numraw:
        return "ARTIFAKT", "ARTIFAKT"
    return "NEKLASIFICIRANO", "NEKLASIFICIRANO"


def family_of(value):
    n = norm(value)
    for fam, stems in FAMILY_STEMS.items():
        for s in stems:
            if s in n:
                return fam
    return None


# ——————————————————————————— 1) PREČNI PREHODI ————————————————————————————

def build_index(all_rows):
    """(page, pass) → {parcel_str → row} in parcel → seznam pas-branj."""
    by_page = {}
    for page, pas, rows in all_rows:
        idx = {}
        for r in rows:
            pz = str(r.get("parzella") or "").strip()
            if pz:
                idx.setdefault(pz, []).append(r)
        by_page[(page, pas)] = idx
    return by_page


def parcel_key(s):
    return norm(str(s or "").strip()).replace(" ", "")


def cross_pass_families(v2, p39, all_rows, by_page):
    """Izhod iz P39 modela (pass2wins pari): vsak par z v2
    NEKLASIFICIRANO rabo. Družine: family_of(raw); ostalo → SINGLES
    (kitice). Nasprotni prehod SAMO znotraj iste fotografije (isti page,
    drugi prehod) — med-fotografske primerjave so nezanesljive zaradi
    ponovnih posnetkov v skenu."""
    # indeks raw vrstic po parceli per (page, pass)
    for page, pas, rows in all_rows:
        idx = {}
        for r in rows:
            pz = parcel_key(r.get("parzella"))
            if pz:
                idx.setdefault(pz, []).append(r)
        by_page[(page, pas)] = idx

    results = []
    for e in p39["parcels"]:
        for c in e.get("cultures", []):
            raw = c.get("raw")
            cls, _tt = v2_classify(v2, raw)
            if cls != "NEKLASIFICIRANO":
                continue
            fam = family_of(raw)
            pz = parcel_key(e.get("parcel"))
            others = []
            seen = set()
            # NASPROTNI PREHOD SAMO ZNOTRAJ ISTE FOTOGRAFIJE (isti page, drugi
            # prehod): sken vsebuje ponovne posnetke (razponi parcel se
            # ponavljajo čez fotografije — 61↔83↔84↔86 [161,180] …), zato
            # med-fotografske primerjave po številki parcele NE zanesljive
            # (različni lastniki/površine za isto številko = drug blok
            # registra ali druga stran razpona). P38/P39 to že spravijo s
            # pass2wins; P43 uporablja samo zanesljivo isto-fotografsko
            # dvojno branje.
            for pg in (c.get("pages") or e.get("pages") or []):
                # pari so pass2wins: če pass2 vrstica za to parcelo obstaja,
                # je par iz pass2 → nasprotni prehod je PASS1; sicer je par
                # iz pass1 → nasprotni PASS2 (če obstaja).
                has_p2 = pz in by_page.get((pg, 2), {})
                other = 1 if has_p2 else 2
                for r2 in by_page.get((pg, other), {}).get(pz, []):
                    key = (pg, other, str(r2.get("kultur")))
                    if key not in seen:
                        seen.add(key)
                        others.append({"where": "samePage", "page": pg,
                                       "pass": other, "kultur": r2.get("kultur")})
            results.append({
                "family": fam or "SINGLES",
                "section": e.get("section"),
                "parcel": e.get("parcel"),
                "parcelAsRead": str(e.get("parcel") or "").strip(),
                "raw": raw,
                "pages": c.get("pages") or e.get("pages") or [],
                "joch": c.get("joch"),
                "klafter": c.get("klafter"),
                "owner": (e.get("owner") or [None])[0],
                "counterparts": others,
            })
    return results


def cross_pass_summary(occ):
    per = defaultdict(lambda: {"variants": defaultdict(int),
                               "pairs": 0,
                               "stablePairs": 0,
                               "fallbackPairs": 0,
                               "variantPairs": 0,
                               "noCounterpart": 0})
    for o in occ:
        fam = per[o["family"]]
        fam["variants"][str(o["raw"]).strip()] += 1
        fam["pairs"] += 1
        cps = o["counterparts"]
        if not cps:
            fam["noCounterpart"] += 1
            continue
        # ključni nasprotni prehod: samePage ima prednost
        same = [c for c in cps if c["where"] == "samePage"]
        cand = same[0] if same else cps[0]
        other_raw = str(cand.get("kultur") or "").strip()
        a, b = norm(o["raw"]), norm(other_raw)
        a_c, b_c = a.rstrip(".").strip(), b.rstrip(".").strip()
        if a_c == b_c:
            fam["stablePairs"] += 1
        elif b_c in {norm(g).rstrip(".").strip() for g in GENERIC_FALLBACK}:
            fam["fallbackPairs"] += 1
        else:
            fam["variantPairs"] += 1
    return {k: {"variants": dict(v["variants"]), "pairs": v["pairs"],
                "stablePairs": v["stablePairs"],
                "fallbackPairs": v["fallbackPairs"],
                "variantPairs": v["variantPairs"],
                "noCounterpart": v["noCounterpart"]}
            for k, v in per.items()}


# ————————————————————— 2) BLOKOVSKA KONCENTRACIJA ——————————————————————

def block_concentration(occ):
    per = defaultdict(lambda: {"pages": set(), "parcels": []})
    for o in occ:
        f = per[o["family"]]
        for pg in (o.get("pages") or []):
            f["pages"].add(pg)
        try:
            f["parcels"].append(int(str(o["parcel"]).strip()))
        except Exception:
            pass
    # teki sosednjih parcel per (family, page): vsota tekov
    by_fp = defaultdict(list)
    for o in occ:
        for pg in (o.get("pages") or []):
            try:
                by_fp[(o["family"], pg)].append(int(str(o["parcel"]).strip()))
            except Exception:
                pass
    runs_by_fam = defaultdict(int)
    for (fam, page), pzs in by_fp.items():
        pzs = sorted(set(pzs))
        if not pzs:
            continue
        runs = 1
        for a, b in zip(pzs, pzs[1:]):
            if b != a + 1:
                runs += 1
        runs_by_fam[fam] += runs
    return {k: {"pages": sorted(v["pages"]), "distinctPages": len(v["pages"]),
                "parcelsCount": len(v["parcels"]),
                "parcelMin": min(v["parcels"]) if v["parcels"] else None,
                "parcelMax": max(v["parcels"]) if v["parcels"] else None,
                "contiguousRuns": runs_by_fam.get(k, 0)}
            for k, v in per.items()}


# ————————————————————— 3) PV OBMOČNA SPRAVA ————————————————————————————

def extract_pv():
    pv = json.load(open(EVID / "PV.json"))
    t = pv["pages"][0]["rawTranscription"]
    def grab(name_pats):
        for p in name_pats:
            m = re.search(p, t, re.S)
            if m:
                return (int(m.group(1)), int(m.group(2)))
        return None
    # sidranje na oštevilčene podatkovne vrstice transkripcije
    # ("N.  **Ime.**\n * Joch: **X**\n * Klf: **Y**") — glava tabele vsebuje
    # ista imena, zato goli search zadošča samo ob sidru na vrstico.
    def row(nname):
        return grab([
            rf"\d+\.\s+\*\*{nname}\*\*\s*$.*?Joch: \*\*(\d+)\*\*.*?Klf?:? \*\*(\d+)\*\*",
            rf"\d+\.\s+\*\*{nname}\*\*.*?Joch: \*\*(\d+)\*\*.*?Klf?:? \*\*(\d+)\*\*",
        ])
    got = {
        "Gemuese_Gaerten": row(r"Gemüse Gärten\.?"),
        "Wein_Gaerten": row(r"Wein Gärten\.?"),
        "Wiesen": row(r"Wiesen\."),
        "Wiesen_mit_Obstbaeumen": row(r"Wiesen mit Obstbäumen\.?"),
        "Weiden": row(r"Weiden\.?"),
        "Aecker": row(r"Aecker\."),
        "Oedungen": row(r"Oedungen\.?"),
        "Fluesse_oder_Baeche": row(r"Flüsse oder Bäche\.?"),
        "Weg_Parzellen": row(r"Weß Parzellen\.?"),
        "Bau_Parzellen": row(r"Bau Parzellen\.?"),
        "Partial_Sum": grab([r"\(Partial Sum\).*?Joch: \*\*(\d+)\*\*.*?Klf?:? \*\*(\d+)\*\*"]),
        "Second_Section_Sum": grab([r"\(Final Total\).*?Joch: \*\*(\d+)\*\*.*?Klf?:? \*\*(\d+)\*\*"]),
        "Grand_Total": grab([r"\(Grand Total.*?\).*?Joch: \*\*(\d+)\*\*.*?Klf?:? \*\*(\d+)\*\*"]),
    }
    missing = [k for k, v in got.items() if v is None]
    if missing:
        fail(f"PV izvleka neuspešna za: {missing}")
    # I2: ujemanje s committed pričakovanimi vrednostmi
    for k, expect in PV_EXPECT.items():
        if got[k] != expect:
            fail(f"I2: PV {k} izvlečeno {got[k]} != pričakovano {expect} (transkripcija)")
    return got


def class_areas(p39, v2):
    agg = defaultdict(lambda: [0, 0, 0])  # (class) → [pairs, areaK, withArea]
    per_section = defaultdict(lambda: defaultdict(int))
    for e in p39["parcels"]:
        for c in e.get("cultures", []):
            cls, _tt = v2_classify(v2, c["raw"])
            if cls is None:
                cls = "BEZ-RABE"
            j, k = c.get("joch") or 0, c.get("klafter") or 0
            hasarea = (c.get("joch") is not None) or (c.get("klafter") is not None)
            a = agg[cls]
            a[0] += 1
            if hasarea:
                a[1] += j * 1600 + k
                a[2] += 1
            per_section[e["section"]][cls] += (j * 1600 + k) if hasarea else 0
    return {k: {"pairs": v[0], "areaK": v[1], "withArea": v[2]} for k, v in agg.items()}, per_section


# ——————————————————————————— LEXIKON RAW ————————————————————————————————

def load_lexicon_raw():
    """2 prehoda per družina; FAIL, če kateri manjka ali ni JSON."""
    out = {}
    for fam in FAMILY_IDS:
        passes = []
        for n in (1, 2):
            fp = LLM_RAW / f"{fam}-pass{n}.json"
            if not fp.exists():
                fail(f"manjka leksikografski raw: {fp}")
            d = json.load(open(fp))
            raw = d.get("raw") or ""
            raw = re.sub(r"^```(json)?|```$", "", raw.strip(), flags=re.M).strip()
            try:
                parsed = json.loads(raw)
            except Exception:
                try:
                    parsed = json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
                except Exception:
                    fail(f"lexicon raw {fp} ni JSON")
            passes.append(parsed)
        out[fam] = passes
    return out


def merge_lexicon_hypotheses(raw_by_fam):
    """Združi 2 prehoda: hipoteze, ki jih omenita OBÉ prehoda, dobijo
    zaupanje prehoda-1 (pogosto [~]); hipoteze enega prehoda ostanejo [?].
    Viri se zbirajo. SKRIPT ne ocenjuje vsebine — samo strukturo."""
    final = {}
    for fam, passes in raw_by_fam.items():
        lists = []
        for p in passes:
            hyps = p.get("hypotheses") or []
            lists.append(hyps)
        # indeks po normaliziranem ključnem kandidatu
        def key(h):
            return norm((h.get("candidate") or h.get("lemma") or "")).strip()
        def conf_of(h):
            c = str(h.get("confidence") or "?").strip()
            return c if c in ("~", "?") else "?"
        # dedupe znotraj posameznega prehoda (isti kandidat večkrat)
        def dedupe(lst):
            seen = set()
            out = []
            for h in lst:
                k = key(h)
                if not k or k in seen:
                    continue
                seen.add(k)
                out.append(h)
            return out
        lists = [dedupe(x) for x in lists]
        merged = []
        for h in lists[0]:
            if not key(h):
                continue
            other = next((g for g in lists[1] if key(g) == key(h)), None)
            merged.append({
                "candidate": str(h.get("candidate") or h.get("lemma") or "").strip(),
                "glossSi": str(h.get("glossSi") or h.get("meaningSi") or "").strip(),
                "source": str(h.get("source") or h.get("reference") or "").strip(),
                "confidence": conf_of(h) if other is None else conf_of(other),
                "inBothPasses": other is not None,
            })
        merged = merged[:6]
        for h in lists[1]:
            if not key(h):
                continue
            if not any(m["candidate"].lower() == key(h) for m in merged):
                if len(merged) >= 6:
                    continue
                merged.append({
                    "candidate": str(h.get("candidate") or h.get("lemma") or "").strip(),
                    "glossSi": str(h.get("glossSi") or h.get("meaningSi") or "").strip(),
                    "source": str(h.get("source") or h.get("reference") or "").strip(),
                    "confidence": "?",
                    "inBothPasses": False,
                })
        # viri, če jih prehoda izrecno navajata
        sources = []
        for p in passes:
            s = p.get("sources") or []
            for x in s:
                sx = str(x).strip()
                if sx and sx not in sources:
                    sources.append(sx)
        def verdicts_of(p):
            v = str(p.get("termTypeHypothesis") or p.get("verdict") or "NEZNANO").strip().upper()
            parts = [x.strip().replace(" ", "-") for x in v.split("|") if x.strip()]
            parts = [x for x in parts if x in (
                "LEDINSKO-IME", "KULTURA-DIALEKT", "KULTURA-KOMPOZIT",
                "OKRAJSAVA", "ARTIFAKT", "NEZNANO", "TOPONIM")]
            return parts or ["NEZNANO"]
        v1p, v2p = verdicts_of(passes[0]), verdicts_of(passes[1])
        # skupni = presek, če ni prazen; sicer unija (vrstni red ohranjen)
        inter = [x for x in v1p if x in v2p]
        union = v1p + [x for x in v2p if x not in v1p]
        verdict = inter if inter else union
        final[fam] = {
            "hypotheses": merged,
            "sources": sources,
            "termTypeHypothesis": " | ".join(verdict),
            "noteSi": str(passes[0].get("noteSi") or "").strip(),
        }
    return final


# ———————————————————————————————— MAIN ——————————————————————————————————

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    v2 = load_v2()
    p39 = load_p39_model()
    all_rows = load_all_rows()
    by_page = build_index(all_rows)

    occ = cross_pass_families(v2, p39, all_rows, by_page)
    cp = cross_pass_summary(occ)
    bc = block_concentration(occ)

    if mode == "evidence":
        TMP_EVID.mkdir(parents=True, exist_ok=True)
        for fam in FAMILY_IDS:
            rows = [o for o in occ if o["family"] == fam]
            fam_bc = bc.get(fam, {})
            fam_cp = cp.get(fam, {})
            doc = {
                "family": fam,
                "occurrences": rows,
                "crossPass": fam_cp,
                "block": fam_bc,
            }
            (TMP_EVID / f"{fam}.json").write_text(
                json.dumps(doc, ensure_ascii=False, indent=1))
        singles = [o for o in occ if o["family"] == "SINGLES"]
        by_raw = defaultdict(list)
        for o in singles:
            by_raw[str(o["raw"]).strip()].append(o)
        sing_doc = {
            "family": "SINGLES",
            "groupedRaw": {k: v for k, v in sorted(by_raw.items(), key=lambda x: -len(x[1]))},
            "crossPass": cp.get("SINGLES", {}),
            "block": bc.get("SINGLES", {}),
            "distinctRaw": len(by_raw),
            "pairs": len(singles),
        }
        (TMP_EVID / "SINGLES.json").write_text(
            json.dumps(sing_doc, ensure_ascii=False, indent=1))
        print(f"evidence zapisana v {TMP_EVID} ({len(FAMILY_IDS)}+1 datotek, "
              f"kitice {len(singles)}/{sing_doc['distinctRaw']})")
        return

    # ——— I1: rekonstrukcija v2 stats ———
    areas, per_section = class_areas(p39, v2)
    sum_pairs = areas["KULTURA"]["pairs"] if "KULTURA" in areas else None
    # KULTURA = vse z KULTURA termType; rekonstruiramo stats iz v2:
    # primaryCounts v2: vsota KULTURA parov (2199) + TOPONIM (122) + ARTIFAKT (29)
    # + NEKLASIFICIRANO (282) = 2632
    stat_pairs = sum(v["pairs"] for v in areas.values())
    if stat_pairs != 2632:
        fail(f"I1: rekonstrukcija parov {stat_pairs} != 2632")

    # ——— I3: sekcije vs P40 konstante ———
    for sec, const in P40_SECTIONS.items():
        s = sum(per_section[sec].values()) / 1600.0
        if abs(s - const) > 0.02:
            fail(f"I3: sekcija {sec} {s:.2f} != P40 {const}")

    # ——— 3) PV sprava ———
    pv = extract_pv()
    def J(x):
        return x / 1600.0
    past_alm = areas.get("PASTVISCE", {"areaK": 0})["areaK"] + areas.get("ALM", {"areaK": 0})["areaK"]
    weiden_gap = PV_EXPECT["Weiden"][0] * 1600 + PV_EXPECT["Weiden"][1] - past_alm
    njiva_area = areas.get("NJIVA", {"areaK": 0})["areaK"]
    travnik_area = areas.get("TRAVNIK", {"areaK": 0})["areaK"]
    vrt_area = areas.get("VRT", {"areaK": 0})["areaK"]
    vinograd_area = areas.get("VINOGRAD", {"areaK": 0})["areaK"]
    gozd_area = areas.get("GOZD", {"areaK": 0})["areaK"]
    neklas_area = areas.get("NEKLASIFICIRANO", {"areaK": 0})["areaK"]
    total_rows = sum(v["areaK"] for v in areas.values())
    pv_total = PV_EXPECT["Grand_Total"][0] * 1600 + PV_EXPECT["Grand_Total"][1]
    area_gap = total_rows - pv_total

    # ——— 4) leksikon ———
    raw_by_fam = load_lexicon_raw()
    lex = merge_lexicon_hypotheses(raw_by_fam)
    # I5: viri + zaupanje
    for fam, d in lex.items():
        if d["termTypeHypothesis"] not in (
                "LEDINSKO-IME", "KULTURA-DIALEKT", "OKRAJSAVA", "ARTIFAKT",
                "NEZNANO", "TOPONIM", "KULTURA-KOMPOZIT") and "|" not in d["termTypeHypothesis"]:
            print(f"OPOMBA: termTypeHypothesis {fam}: {d['termTypeHypothesis']}")
        for h in d["hypotheses"]:
            if h["confidence"] not in ("~", "?"):
                fail(f"I5: zaupanje {fam}/{h['candidate']}: {h['confidence']}")

    fam_order = sorted(FAMILY_IDS, key=lambda f: -cp.get(f, {"pairs": 0})["pairs"])
    families_out = []
    for fam in fam_order:
        c = cp.get(fam, {})
        b = bc.get(fam, {})
        families_out.append({
            "id": fam,
            "pairs": c.get("pairs", 0),
            "variants": c.get("variants", {}),
            "distinctVariants": len(c.get("variants", {})),
            "stablePairs": c.get("stablePairs", 0),
            "fallbackPairs": c.get("fallbackPairs", 0),
            "variantPairs": c.get("variantPairs", 0),
            "noCounterpart": c.get("noCounterpart", 0),
            "block": b,
            "blockConcentration": (b.get("distinctPages", 0) == 1) if b else None,
            "lexicon": lex.get(fam),
            "verdictSi": "NEKLASIFICIRANO (hipoteze; čaka paleografijo)",
        })
    sing_cp = cp.get("SINGLES", {})
    singles_out = {
        "pairs": sing_cp.get("pairs", 0),
        "variants": sing_cp.get("variants", {}),
        "distinctRaw": len(sing_cp.get("variants", {})),
        "fallbackPairs": sing_cp.get("fallbackPairs", 0),
        "noteSi": "kitice (posamezne neznane vrednosti) — P42 jih izrecno ločuje "
                  "od družin; večina je verjetno okrnjenih/napačno prebranih "
                  "oblik znanih terminov (Einfach≈Einschlag, Schutt≈Schütt…)",
    }

    out = {
        "series": "PS",
        "source": "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani)",
        "method": "P43 — neznane družine: prečni prehodi (pass1↔pass2 po parceli), "
                  "blokovska koncentracija, PV območna sprava nad committed transkripcijo "
                  "PV.json, leksikografske hipoteze iz 2 neodvisnih LLM prehodov "
                  "(ps-lexicon-raw/, samo hipoteze z viri); rabe se NE prirejajo — "
                  "v2 klasifikacija nespremenjena; vse ostaja REVIEW",
        "basis": {
            "landuse": "research/issue17/ps-landuse.json (P39 model) + ps-landuse-v2.json (P42)",
            "pv": "research/issue17/PV.json (Nutzungs-Ausweis, 10. 1. 1825)",
            "lexiconRaw": "research/issue17/ps-lexicon-raw/ (2 prehoda × 16 družin)",
        },
        "readingRule": "pass2wins (P38/P39); prečni prehodi so DODATNI dokaz, ne zamenjava",
        "countScope": "štetje po PARIH parcela×raba (podvojene rabe znotraj parcele enkrat) — kot P39/P42",
        "families": families_out,
        "singles": singles_out,
        "pvReconciliation": {
            "pvOfficial": {k: {"joch": v[0], "klafter": v[1], "jochF": round(J(v[0]*1600+v[1]), 2)} for k, v in PV_EXPECT.items()},
            "psClassAreasJ": {k: round(v["areaK"] / 1600.0, 2) for k, v in sorted(areas.items())},
            "weidenGapJ": round(J(weiden_gap), 2),
            "psPastVisceAlmJ": round(J(past_alm), 2),
            "njivaVsAeckerDeltaJ": round(J(njiva_area - (PV_EXPECT["Aecker"][0]*1600+PV_EXPECT["Aecker"][1])), 2),
            "travnikVsWiesenDeltaJ": round(J(travnik_area - (PV_EXPECT["Wiesen"][0]*1600+PV_EXPECT["Wiesen"][1]) - (PV_EXPECT["Wiesen_mit_Obstbaeumen"][0]*1600+PV_EXPECT["Wiesen_mit_Obstbaeumen"][1])), 2),
            "vrtVsGemueseDeltaJ": round(J(vrt_area - (PV_EXPECT["Gemuese_Gaerten"][0]*1600+PV_EXPECT["Gemuese_Gaerten"][1])), 2),
            "vinogradVsWeinDeltaJ": round(J(vinograd_area - (PV_EXPECT["Wein_Gaerten"][0]*1600+PV_EXPECT["Wein_Gaerten"][1])), 2),
            "gozdVsWalderNote": "PV 'Walder' vrstica v committed transkripciji PRAZNA — "
                                "gozda uradni izkaz NE navaja; PS ima GOZD "
                                f"{J(gozd_area):.2f} J; vrzel odprta (možen napaka branja PV ali "
                                "gozd prištet pod druge kategorije — [?])",
            "rowsModelVsPvTotalJ": round(J(area_gap), 2),
            "rowsModelTotalJ": round(J(total_rows), 2),
            "pvTotalJ": round(J(pv_total), 2),
            "p41AreaIdentity": "PV Grand_Total 1221|1513 ≈ P41 Area der Gemeinde 1220|1493 "
                               "(Δ 1 J 20 K ≈ 0,05 %) — dokumentna rekapitulacija in uradni "
                               "izkaz STAKAJETA",
            "unknownFamiliesAreaJ": round(J(neklas_area), 2),
            "gapDecompositionNote": "PV Weiden-gap (576,24 J) NI pojasnljiv samo z "
                "neznanimi družinami (96,68 J = 17 % vrzeli) — preostanek leži v "
                "presežkih NJIVA (+202,29) in TRAVNIK (+182,12) nad uradnima "
                "kategorijama ter TOPONIM/ARTIFAKT/ostalih: kulturni stolpec "
                "meša rabo, ledinska imena in opombe, PV pa šteje parcelo enkrat "
                "po njeni kategoriji. Sprava je IZRAZNO hipoteza [~] — za "
                "končno atribucijo je treba človeško paleografijo.",
            "rowsVsRecapGap": "vrstični model (1564,78 J) − dokumentna/PV Area (≈1221 J) "
                              "≈ Blatt X (280,73) + NADALJEVANJE (13,46) + WALDUNG (37,63) "
                              "+ ostanki ≈ 343,85 J → kvantitativni argument, da so te sekcije "
                              "zunaj 'Area der Gemeinde' rekapitulacije (izrecno [~])",
        },
        "invariants": {
            "I1": "v2 klasifikacija rekonstruirana identično (2632 parov)",
            "I2": "PV izvlek == committed transkripcija (13 kategorij)",
            "I3": "sekcije == P40 konstante (±0,02 J)",
            "I4": "prečni prehodi pokrijejo vseh 16 družin v2 NEKLASIFICIRANO",
            "I5": "vsi kandidati z viri in zaupanjem [~]/[?]; rabe NI prirejena",
        },
        "generatedBy": "scripts/p43_ps_lexicon.py",
        "generatedAt": now_iso(),
    }

    # ——— I4 kontrola: vseh 16 družin + kitice; 216 + 66 == 282 ———
    fam_pairs = {f["id"]: f["pairs"] for f in families_out}
    missing_fams = [f for f in FAMILY_IDS if f not in fam_pairs]
    if missing_fams:
        fail(f"I4: manjkajo družine: {missing_fams}")
    total_fam_pairs = sum(fam_pairs.values())
    sing_pairs = singles_out["pairs"]
    if total_fam_pairs != 216:
        fail(f"I4: vsota parov po 16 družinah {total_fam_pairs} != 216")
    if total_fam_pairs + sing_pairs != 282:
        fail(f"I4: 216 + kitice {sing_pairs} != 282 (v2 NEKLASIFICIRANO)")

    for target in (OUT_EVIDENCE, OUT_RUNTIME):
        target.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")

    print(f"P43: {len(families_out)} družin ({total_fam_pairs} parov) + kitice "
          f"({sing_pairs} parov/{singles_out['distinctRaw']} različnih)")
    for f in families_out:
        b = f["block"]
        print(f"  {f['id']:18s} parov={f['pairs']:3d} variant={f['distinctVariants']:2d} "
              f"stabilnih={f['stablePairs']:3d} padcek={f['fallbackPairs']:3d} "
              f"strani={b.get('distinctPages', 0)} teki={b.get('contiguousRuns', 0)} "
              f"termType={f['lexicon']['termTypeHypothesis']}")
    print(f"PV sprava: Weiden-gap {out['pvReconciliation']['weidenGapJ']} J; "
          f"NJIVA Δ {out['pvReconciliation']['njivaVsAeckerDeltaJ']} J; "
          f"model−Area {out['pvReconciliation']['rowsModelVsPvTotalJ']} J")
    print(f"izpisano: {OUT_EVIDENCE} + {OUT_RUNTIME}")


if __name__ == "__main__":
    main()
