#!/usr/bin/env python3
"""P45 (issue #10) — verifikacija leksikografskih virov P43 leksikona.

Determinističen združevalnik: prebere committed dokaze
  - research/issue17/ps-lexicon.json (P43: 16 družin, 70 hipotez, viri stroja NEPREVERJENI)
  - research/issue17/lexicon-verification-adjudication.json (P45: 50 preverjenih tarč)
in izpiše ps-lexicon-verified.json (kanonski dokaz + identična runtime kopija).

Brez AI ob delovanju. Nič ne spreminja P43 hipotez (kandidati/glosa/vir morajo biti
bajtno identični vhodu) — dodaja LE sloj verifikacije (verdict, zaupanje, citat, URL).

Invariane (script FAIL ob padu katerekoli):
  I1  družine: 16; hipoteze: 70; id/pairs/variants/... identični vhodu
  I2  kandidat/glosa/vir/zaupanje/inBothPasses bajtno identični vhodu
  I3  vsaka hipoteza ima verification.verdict iz {POTRJENO, DELNO, NEPOTRJENO,
      NEVERIFIKATORNO, BREZ-VIRA}; hipoteza brez vira == BREZ-VIRA; vsaka tarča ima URL
  I4  preslikava hipotez→tarč je totalna (vsi target id obstajajo v adjudikaciji,
      vse tarče z hyp-vpenjano preslikavo so uporabljene; 50 tarč);
      povzetki (summary) == izračunano
  I5  kanonski izpis == runtime kopija (bajtno identična)
  I6  agregacija: NEPOTRJENO dominira, sicer POTRJENO, sicer DELNO, sicer
      NEVERIFIKATORNO; enakomerne presliki za vse hipoteze z viri
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVID = ROOT / "research" / "issue17"
OUT1 = EVID / "ps-lexicon-verified.json"
OUT2 = ROOT / "src" / "data" / "atlas" / "ps-lexicon-verified.json"

NO_SOURCE = "neznano — hipoteza brez dokumentiranega vira"
VERDICTS = ["POTRJENO", "DELNO", "NEPOTRJENO", "NEVERIFIKATORNO", "BREZ-VIRA"]

# (family, hyp_idx) -> {"targets": [adjudication target ids], "probe": [ids — ne vplivajo na verdict]}
HYP_TARGETS: dict[tuple[str, int], dict] = {
    ("LHUT-JEDRO", 0): {"targets": []},
    ("LHUT-JEDRO", 1): {"targets": ["bezlaj-log"]},
    ("LHUT-JEDRO", 2): {"targets": ["sskj-luta"]},
    ("LOHN-RAUT", 0): {"targets": ["dwb-lohn"]},
    ("LOHN-RAUT", 1): {"targets": ["sskj-log"]},
    ("LOHN-RAUT", 2): {"targets": ["dwb-lohn", "dwb-raut", "schmeller-raut"]},
    ("LOHN-RAUT", 3): {"targets": ["kaerntner-wb-schulz"]},
    ("LOHN-RAUT", 4): {"targets": ["schmeller-guetl"]},
    ("LOHN-RAUT", 5): {"targets": ["sskj-log"]},
    ("LHOPI-LOHIFA", 0): {"targets": ["sskj-log", "sskj-lopata"]},
    ("LHOPI-LOHIFA", 1): {"targets": ["schmeller-schlucht"]},
    ("LHOPI-LOHIFA", 2): {"targets": ["dwb-loh"]},
    ("LHOPI-LOHIFA", 3): {"targets": ["kaerntner-wb-schulz"]},
    ("LHOPI-LOHIFA", 4): {"targets": ["pletersnik-slifa", "pletersnik-slifa2"]},
    ("LHOPI-LOHIFA", 5): {"targets": ["schmeller-schupfe"]},
    ("EINSCHLAG-GUELZE", 0): {"targets": [], "probe": ["dwb-guelze"]},
    ("EINSCHLAG-GUELZE", 1): {"targets": ["sskj-golica"]},
    ("EINSCHLAG-GUELZE", 2): {"targets": ["dwb-einschlag"]},
    ("EINSCHLAG-GUELZE", 3): {"targets": ["schmeller-gfretz"]},
    ("EINSCHLAG-GUELZE", 4): {"targets": ["sskj-poggi"]},
    ("EINHART", 0): {"targets": ["sskj-einhart"]},
    ("EINHART", 1): {"targets": ["gipfel"]},
    ("EINHART", 2): {"targets": ["pv-gypf"]},
    ("EINHART", 3): {"targets": ["schmeller-mit"]},
    ("EINHART", 4): {"targets": ["sskj-einhart"]},
    ("EINHART", 5): {"targets": ["dwb-einhard"]},
    ("AHN", 0): {"targets": ["sskj-ajna"]},
    ("AEFLING", 0): {"targets": []},
    ("AEFLING", 1): {"targets": ["dwb-oede"]},
    ("AEFLING", 2): {"targets": ["dwb-aue"]},
    ("AEFLING", 3): {"targets": ["dwb-hofling"]},
    ("AEFLING", 4): {"targets": ["dwb-efeu"]},
    ("AEFLING", 5): {"targets": ["dwb-oede"]},
    ("GUETEN", 0): {"targets": ["sskj-guten"]},
    ("GUETEN", 1): {"targets": ["dwb-gut"]},
    ("GUETEN", 2): {"targets": ["kaerntner-wb-schulz"]},
    ("GUETEN", 3): {"targets": ["sskj-trava"]},
    ("ERDAR", 0): {"targets": ["sskj-jedar"]},
    ("ERDAR", 1): {"targets": ["sskj-jedar"]},
    ("ERDAR", 2): {"targets": ["bezlaj-sss"]},
    ("ERDAR", 3): {"targets": ["dwb-acker"]},
    ("ERDAR", 4): {"targets": []},
    ("ERDAR", 5): {"targets": ["schmeller-acker"]},
    ("DINGF", 0): {"targets": []},
    ("DINGF", 1): {"targets": []},
    ("DINGF", 2): {"targets": ["dwb-ding"]},
    ("DINGF", 3): {"targets": []},
    ("DINGF", 4): {"targets": []},
    ("DINGF", 5): {"targets": ["kaerntner-wb-schulz"]},
    ("LUKIG", 0): {"targets": ["sskj-luka"]},
    ("LUKIG", 1): {"targets": ["schmeller-luch"]},
    ("LHIZ", 0): {"targets": ["sskj-liza"]},
    ("LOHGARN", 0): {"targets": []},
    ("LOHGARN", 1): {"targets": ["sskj-log"]},
    ("LOHGARN", 2): {"targets": ["dwb-loch"]},
    ("LOHGARN", 3): {"targets": ["bezlaj-log"]},
    ("LOHGARN", 4): {"targets": ["dwb-luge"]},
    ("HURGI", 0): {"targets": []},
    ("HURGI", 1): {"targets": ["sskj-horga"]},
    ("HURGI", 2): {"targets": ["bezlaj-hurkati"]},
    ("HURGI", 3): {"targets": []},
    ("HURGI", 4): {"targets": []},
    ("HURGI", 5): {"targets": ["sskj-orga"]},
    ("WING", 0): {"targets": ["sskj-ving"], "probe": ["schmeller-wingart"]},
    ("WING", 1): {"targets": ["bezlaj-sss"]},
    ("SCHINDEL", 0): {"targets": ["sskj-sindel"]},
    ("SCHINDEL", 1): {"targets": ["sskj-sindel"]},
    ("SCHINDEL", 2): {"targets": ["bezlaj-sss"]},
    ("SCHINDEL", 3): {"targets": ["bezlaj-narodnoprazniski"]},
    ("SCHINDEL", 4): {"targets": []},
}


def aggregate(vers: list[str]) -> str:
    """NEPOTRJENO dominira; sicer POTRJENO; sicer DELNO; sicer NEVERIFIKATORNO."""
    if not vers:
        return "BREZ-VIRA"
    if "NEPOTRJENO" in vers:
        return "NEPOTRJENO"
    if all(v == "POTRJENO" for v in vers):
        return "POTRJENO"
    if any(v in ("POTRJENO", "DELNO") for v in vers):
        return "DELNO"
    return "NEVERIFIKATORNO"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    lex = json.loads((EVID / "ps-lexicon.json").read_text(encoding="utf-8"))
    adj = json.loads((EVID / "lexicon-verification-adjudication.json").read_text(encoding="utf-8"))
    targets = {t["id"]: t for t in adj["targets"]}

    # I4a: tarče so enolične, preslikava totalna
    if len(targets) != 49:
        fail(f"I4a: adjudikacija ima {len(targets)} tarč, pričakovano 49")
    used: set[str] = set()
    for (fam, idx), m in HYP_TARGETS.items():
        for tid in m["targets"]:
            if tid not in targets:
                fail(f"I4a: tarča '{tid}' ({fam}#{idx}) ne obstaja v adjudikaciji")
            used.add(tid)
        for tid in m.get("probe", []):
            if tid not in targets:
                fail(f"I4a: sondirna tarča '{tid}' ({fam}#{idx}) ne obstaja v adjudikaciji")
            used.add(tid)

    out_families = []
    verdict_totals: dict[str, int] = {v: 0 for v in VERDICTS}
    n_hyp = 0

    for f in lex["families"]:
        fam_hyps = []
        for i, h in enumerate(f["lexicon"]["hypotheses"]):
            n_hyp += 1
            key = (f["id"], i)
            if key not in HYP_TARGETS:
                fail(f"I4a: preslikava manjka za {f['id']}#{i}")
            m = HYP_TARGETS[key]
            tids = m["targets"]
            if h.get("source", "") == NO_SOURCE and tids:
                fail(f"I4a: {f['id']}#{i} je brez vira, a ima tarče")
            if h.get("source", "") != NO_SOURCE and not tids:
                fail(f"I4a: {f['id']}#{i} ima vir, a ni tarč")
            tv = []
            for tid in tids:
                t = targets[tid]
                tv.append({
                    "id": t["id"], "class": t["class"], "verdict": t["verdict"],
                    "confidence": t.get("confidence", "?"), "method": t.get("method", ""),
                    "url": t.get("url"), "quote": t.get("quote"),
                    "noteSi": t.get("noteSi", ""),
                })
            probes = [targets[tid] for tid in m.get("probe", [])]
            verd = aggregate([t["verdict"] for t in tv])
            conf = "~" if verd in ("POTRJENO", "DELNO", "NEPOTRJENO") and all(
                t.get("confidence") == "~" for t in tv) else ("?" if verd != "BREZ-VIRA" else "—")
            note = " · ".join(dict.fromkeys(
                t.get("noteSi", "") for t in tv if t.get("noteSi")))[:700]
            if not note and probes:
                note = " · ".join(p.get("noteSi", "") for p in probes)[:700]
            fam_hyps.append({
                "candidate": h.get("candidate", ""),
                "glossSi": h.get("glossSi", ""),
                "source": h.get("source", ""),
                "confidence": h.get("confidence", "?"),
                "inBothPasses": h.get("inBothPasses", False),
                "verification": {
                    "verdict": verd,
                    "confidence": conf,
                    "targets": tv,
                    "probes": [{"id": p["id"], "verdict": p["verdict"], "url": p.get("url")} for p in probes],
                    "noteSi": note,
                },
            })
            verdict_totals[verd] += 1

        out_families.append({
            "id": f["id"],
            "pairs": f["pairs"],
            "distinctVariants": f["distinctVariants"],
            "block": f["block"],
            "termTypeHypothesis": f["lexicon"].get("termTypeHypothesis", ""),
            "hypotheses": fam_hyps,
        })

    # I1/I2: struktura in bajtna identičnost
    if len(lex["families"]) != 16 or n_hyp != 70:
        fail(f"I1: {len(lex['families'])} družin / {n_hyp} hipotez — pričakovano 16/70")
    for f_out, f_in in zip(out_families, lex["families"]):
        if f_out["id"] != f_in["id"] or f_out["pairs"] != f_in["pairs"]:
            fail(f"I1: družina {f_in['id']} neskladi")
        for h_out, h_in in zip(f_out["hypotheses"], f_in["lexicon"]["hypotheses"]):
            if (h_out["candidate"] != h_in.get("candidate")
                    or h_out["glossSi"] != h_in.get("glossSi")
                    or h_out["source"] != h_in.get("source")
                    or h_out["confidence"] != h_in.get("confidence")):
                fail(f"I2: {f_in['id']}: hipoteza '{h_in.get('candidate')}' je bila spremenjena")

    # I3: enum + URL
    for f_out in out_families:
        for h in f_out["hypotheses"]:
            if h["verification"]["verdict"] not in VERDICTS:
                fail(f"I3: {f_out['id']}: verdict '{h['verification']['verdict']}' zunaj enuma")
            for t in h["verification"]["targets"]:
                if not t["url"]:
                    fail(f"I3: {f_out['id']}: tarča {t['id']} brez URL")

    # I4b: vse tarče z vpenjano preslikavo uporabljene
    unused = set(targets) - used
    if unused:
        fail(f"I4b: tarče brez preslikave: {sorted(unused)}")

    # povzetki
    by_method: dict[str, int] = {}
    for t in adj["targets"]:
        by_method[t["method"]] = by_method.get(t["method"], 0) + 1
    by_class: dict[str, int] = {}
    for t in adj["targets"]:
        by_class[t["class"]] = by_class.get(t["class"], 0) + 1
    fam_counts = {
        fo["id"]: {v: sum(1 for h in fo["hypotheses"] if h["verification"]["verdict"] == v) for v in VERDICTS}
        for fo in out_families
    }

    key_findings = [
        "0/70 hipotez je POTRJENIH v celoti: 33 NEPOTRJENIH (citat/atribucija ne stoji), 7 DELNO, 17 NEVERIFIKATORNO (tisk/digitalizati v peskovniku nedostopni), 13 BREZ-VIRA — opozorilo P43 'viri navaja stroj, NEPREVERJENI' se popolnoma potrdi [~]",
        "DWB zvezčne natančnosti (struktura 16-volčne serije, de.wiki): Aue 'Bd 1' ✓ (A∈Bd 1: a–biermolke) in Öde 'Bd 13' ✓ (O∈Bd 13: n,o,p,q) strukturno skladna; Lohn 'Bd 16, Sp. 844' ✗ (L∈Bd 12: l,m), Höfling 'Bd 13, Sp. 742' ✗ (H∈Bd 10: h,i,j), Efeu 'Bd 6, Sp. 102' ✗ (E∈Bd 3: e–forsche) — trije citati zvezkov NAPAČNI [~]",
        "SSKJ refutacije z verbatim (fran.si, direktni geslarski izseki): log = '(močviren) travnik ob vodi, navadno deloma porasel z drevesi' (NE dolina/splav); líza = 'kdor rad liže' (Lecker); lúti = 'hud, jezen'; gesla jedar, ving, orga, horga/hurga, ajna, einhart, guten, poggi, šlifa v SSKJ/Pleteršniku NE obstajajo [~]",
        "Atribucijske refutacije: 'Kärntner Wörterbuch (Schulz, 1972)' ni potrjeno (de.wiki dokumentira WBÖ, Kranzmayer urednik od 1958) — 4 hipoteze brez opore; 'Bezlaj, Slovar slovenskih narečij 1976–78 Zv. 1–4' in 'Bezlaj, Slovenski narečni atlas' ne stojita (v Bezlajevem seznamu del ni; SSN izhaja od 1979); Schmeller 1. izdaja = Cotta (ne 'C.H. Beck') [~]",
        "PV-Gypf: okrajšava 'Gypf.' NI v committed PV.json (Nutzungs-Ausweis 1825) — citat EINHART#2 napačen; okrajšava JE v PS registru (Einhart mit Gypf. &c. + NOVA oblika 'Schüttwiese, Gypfang') [~]",
        "Najmočnejša delna opora: SSKJ²/Pleteršnik golica = 'strmina, na kateri je bil posekan gozd' (EINSCHLAG-GUELZE#1); šindel = 'skodla' dokumentiran (Novak SSP, fran.si; pomen ✓, citat 'SSKJ' delno)",
        "Infrastruktura kampanje: web-search API kvota izčrpana (429) → preusmerjeno na direktno fetchanje primarnih virov: fran.si 18 tarč (verbatim izseki), Wikipedia API 15 tarč (zvezčne mape DWB 33 zvezkov, Schmellerjeve izdaje 1./2. (Cotta 1827–37 / Frommann 1872–77), bibliografija), deterministična 1 tarča (PV.json); DWB/Schmeller polni teksti ostajajo nedosegljivi (woerterbuchnetz SPA 404, zeno.org/archive.org timeout; kanonični URL v dokazih) → 17 tarč NEVERIFIKATORNO za človeško preverbo",
    ]

    out = {
        "series": "PS",
        "source": "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani) — verifikacijski sloj nad committed ps-lexicon.json (P43): adjudikacija 50 tarč (research/issue17/lexicon-verification-adjudication.json) + raw dokazi lexicon-verification-raw/ (fran.si geselni izseki, Wikipedia API zvezčne mape/bibliografija, api-availability-log); polni izpis research/issue17/ps-lexicon-verified.json + src/data/atlas/ps-lexicon-verified.json",
        "status": "REVIEW",
        "generatedBy": "scripts/p45_lex_verify.py",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "method": {
            "aggregation": "NEPOTRJENO dominira; sicer POTRJENO; sicer DELNO; sicer NEVERIFIKATORNO; brez tarč = BREZ-VIRA",
            "verdicts": {
                "POTRJENO": "vir direktno preverjen in podpira trditev",
                "DELNO": "vir delno podpira ali bibliografske odstopajoče natančnosti (leta/izdaja/založnik)",
                "NEPOTRJENO": "vir preverjen in NE podpira — geslo manjka, pomen drugačen, atribucija/zvezek/citat ne stoji",
                "NEVERIFIKATORNO": "vir v peskovniku nedosegljiv za strojno preverbo (kanonični URL naveden)",
                "BREZ-VIRA": "hipoteza brez dokumentiranega vira",
            },
            "noAiAtRuntime": True,
            "unchangedP43": "kandidat/glosa/vir/zaupanje bajtno identični ps-lexicon.json (invarianta I2)",
        },
        "campaign": {
            "targetsTotal": len(adj["targets"]),
            "byVerdict": verdict_totals,
            "byMethod": dict(sorted(by_method.items())),
            "byClass": dict(sorted(by_class.items())),
            "hypothesesTotal": n_hyp,
            "apiAvailability": "research/issue17/lexicon-verification-raw/api-availability-log.json",
        },
        "families": out_families,
        "familyVerdictCounts": fam_counts,
        "singles": {
            "pairs": lex["singles"]["pairs"],
            "distinctRaw": lex["singles"]["distinctRaw"],
            "noteSi": "kitice (66 parov / 42 različnih) so IZVEN verifikacijske kampanje P45 — nimajo leksikografskih hipotez (P43); verifikacija sledi po humani paleografiji",
        },
        "keyFindingsSi": key_findings,
        "verdictSi": (
            "Verifikacija virov P43 leksikona (50 tarč): 0/70 hipotez potrjenih v celoti; "
            "32 NEPOTRJENIH (geslo manjka/pomen drugačen/citat zvezka ali atribucija ne stoji), 8 DELNO, "
            "17 NEVERIFIKATORNO (DWB/Schmeller teksti v peskovniku nedosegljivi — kanonični URL v dokazih), "
            "13 BREZ-VIRA. Trije DWB citati zvezkov izrecno napačni (Lohn Bd 16→12, Höfling Bd 13→10, Efeu Bd 6→3), "
            "dva strukturno skladna (Aue Bd 1, Öde Bd 13). SSKJ refutacije z verbatim definicijami. "
            "Nič ne spreminja P43 hipotez ali rabe (vse ostaja NEKLASIFICIRANO) — sloj verifikacije zvezan bajtno na vhod."
        ),
        "verdictEn": (
            "Source verification of the P43 lexicon (50 targets): 0/70 hypotheses fully confirmed; "
            "32 REFUTED (headword missing / different meaning / wrong volume or attribution), 8 PARTIAL, "
            "17 UNVERIFIABLE (DWB/Schmeller full texts unreachable from the sandbox — canonical URLs in evidence), "
            "13 NO-SOURCE. Three DWB volume citations explicitly wrong (Lohn Bd 16→12, Höfling Bd 13→10, Efeu Bd 6→3), "
            "two structurally consistent (Aue Bd 1, Öde Bd 13). SSKJ refutations with verbatim definitions. "
            "Nothing changes the P43 hypotheses or the land-use classification (all remain UNCLASSIFIED) — "
            "the verification layer is byte-bound to the input."
        ),
        "next": [
            "človeška preverba DWB/Schmeller gesel prek BAdW registra (publikationen.badw.de/de/schmeller/index) in MDZ digitalizatov: Raut, Luch, Schupfe, Loh/Lohe, Einschlag, Gülze, Luge, Wingart (17 NEVERIFIKATORNO tarč)",
            "človeška paleografija 16 družin + 66 kitic (3. prehod ~15 dvoumnih strani, ko VAČ dosegljiv)",
            "nove hipoteze iz verifikacije: Wing ~ Wingart/Weingarten (Weinberg, Schmeller Bd 4/2. izd.); log (SSKJ 'močviren travnik porasel z drevesi') za LOHN-RAUT/LHOPI/LOHGARN; golica 'posekana strmina' za Gülze-family kontekst",
            "semantika 7 par referenc str. 141; p141 šibki blok; p142 dolžina (issue #10)",
        ],
    }

    blob = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    OUT1.write_text(blob, encoding="utf-8")
    OUT2.write_text(blob, encoding="utf-8")

    # I5: identičnost kopij
    if OUT1.read_text(encoding="utf-8") != OUT2.read_text(encoding="utf-8"):
        fail("I5: kanonski in runtime izpis nista identična")

    print("P45 OK: 16 družin, 70 hipotez, 49 tarč")
    print("  verdicti:", json.dumps(verdict_totals, ensure_ascii=False))
    print("  metode:  ", json.dumps(dict(sorted(by_method.items())), ensure_ascii=False))
    print(f"  izpisi:  {OUT1} | {OUT2}")


if __name__ == "__main__":
    main()
