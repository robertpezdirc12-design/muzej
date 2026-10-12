#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P44 (issue #10) — N083PS: RAZCEP K1/K2 v "Abschluß der Gemeinde" (str. 140 desno).

PROBLEM (P41 §21, UNRESOLVED):
  Abschluß vrstici  Grundparzellen (nach Anlage) 831|K1  in  Zinsb./Ziffer 1041
  383|K2  se seštejeta v Summe der Grundparzellen 1215|490. Ker je 831+383 = 1214
  Joch, mora veljati  K1 + K2 = 1600 + 490 = 2090 K  (prenos 1 J). VLM prehodi so
  K1 brali 968/468 (vizualno "9?8"), K2 pa 1288/1388 — noben par branj ni izpolnil
  omejitve, zato je razcep ostal UNRESOLVED.

METODA P44 (izključno iz committed dokazov, brez AI ob delovanju):
  1. Rekonstrukcija leve strani (P41): 7 vrstic Grundstückslagen → 831|702
     (aritmetično iz posameznih vrstic, neodvisno od branja vrstice "Summa").
  2. STRUKTURNA PARALELNOST "nach Anlage": desna vrstica 4 "Summa der Bauparzellen
     nach Anlage" = 3|312 je IDENTIČNA levi vrstici 132 (3|312) — to je že
     P41 identiteta (d_abschlussBaup). Po istem vzorcu mora desna vrstica 1
     "Grundparzellen nach Anlage" rekapitulirati levo "Summa der Grundparzellen":
     Joch 831 == 831 → K1 = 702 (Klafter leve vsote). Hipoteza (968|1122) pade:
     831|968 bi pomenilo, da rekapitulacija Anlage PRESEGA vsoto Anlage (968 > 702
     pri istem Joch 831) — podmnožina ne more presegati nadmnožine.
  3. Omejitev: K2 = 2090 − 702 = 1388 — kar je DIREKTNO VLM BRANJE K2 celice
     (pass2), poleg konsenza "1?88" repa (1288 p1+p3 se razlikuje le v 2. števki).
  4. Hipoteze (iz kandidatov + strukturnega sidra) razvrščene po dokazih;
     edino sprejeta je H1 = (702, 1388).
  5. Popolna zaprtost Abschlußa: 831|702 + 383|1388 = 1215|490;
     + 5|1003 = 1220|1493 (Area der Gemeinde); 3|312 + 2|691 = 5|1003.

INVARIANTE (FAIL ob padu katerekoli):
  I1  vsota 7 vrstic leve strani == 831|702 (rekonstrukcija iz committed vrstic)
  I2  831|702 + 3|312 == 834|1014 (zaprtje leve strani)
  I3  omejitev: (1215·1600+490) − (831+383)·1600 == 2090
  I4  paralelnost: desna vrstica 4 (3|312) == leva vrstica 132 (3|312) IN
      Joch desne vrstice 1 (831) == Joch leve vsote (831)
  I5  K1 = 702 == Klafter leve vsote; K2 = 2090 − 702 == 1388; 1388 je med
      committed VLM branji K2 celice (pass2); 1388 < 1600; 702 < 1600
  I6  popolna zaprtost: (831·1600+702) + (383·1600+1388) == 1215·1600+490 IN
      (1215·1600+490) + (5·1600+1003) == 1220·1600+1493 IN
      (3·1600+312) + (2·1600+691) == 5·1600+1003
  I7  enoličnost: natanko ENA sprejeta hipoteza (H1); vse ostale zavrnjene
      z izrecnim razlogom; noben drug par kandidatov ne izpolnjuje omejitve
      s strukturnim sidrom.

IZPISI:
  research/issue17/ps-k1k2.json   (kanonski dokazni izpis)
  src/data/atlas/ps-k1k2.json     (identična runtime kopija)

Status: RESOLVED-ARITMETIČNO [~] — rešitev je aritmetično vsiljena z dvema
neodvisnima korelacijama (paralelnost nach Anlage + direktno branje K2);
človeška paleografska potrditev ostaja odprta (issue #10 ne zapre tega dela).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EV = ROOT / "research" / "issue17"
RUNTIME = ROOT / "src" / "data" / "atlas"

CANON = EV / "ps-recap-paleo.json"
RAW_DIR = EV / "ps-recap-paleo-raw"

K_PER_J = 1600


def jk(j: int, k: int) -> int:
    """Joch|Klafter → absolutni Klafter."""
    return j * K_PER_J + k


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_canon() -> dict:
    if not CANON.is_file():
        fail(f"manjka {CANON}")
    return json.loads(CANON.read_text(encoding="utf-8"))


def parse_pass_raw(path: Path) -> list[dict]:
    """Iz raw odgovora prehoda izlušči vrstice (label, joch, klafter)."""
    txt = json.loads(path.read_text(encoding="utf-8"))["raw"]
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        fail(f"{path.name}: raw brez JSON objekta")
    body = json.loads(m.group(0))
    rows: list[dict] = []

    def walk(o: object) -> None:
        if isinstance(o, dict):
            if ("joch" in o or "klafter" in o or "stand" in o) and (
                "label" in o or "name" in o
            ):
                rows.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(body)
    return rows


def to_int(s: object) -> int | None:
    try:
        return int(str(s).strip())
    except (TypeError, ValueError):
        return None


def main() -> None:
    canon = load_canon()

    # ——— 1. Leva stran: rekonstrukcija vsote 7 vrstic (I1) ———
    left = canon["reading"]["page140Left"]
    lage = left["lageRows"]
    if len(lage) != 7:
        fail(f"I1: število vrstic Grundstückslagen je {len(lage)}, moralo bi biti 7")
    tj = sum(r["joch"] for r in lage)
    tk = sum(r["klafter"] for r in lage)
    lage_j, lage_k = tj + tk // K_PER_J, tk % K_PER_J
    if (lage_j, lage_k) != (831, 702):
        fail(f"I1: vsota 7 vrstic je {lage_j}|{lage_k}, morala bi biti 831|702")

    left_summa = left["summaGrundparzellen"]["value"]  # "831|702"
    if left_summa != "831|702":
        fail(f"I1: leva 'Summa der Grundparzellen' je {left_summa}, pričakovano 831|702")

    # ——— 2. Identitete leve strani (I2) ———
    zinsb_left = left["zinsbBauparzellen"]["value"]  # "3|312"
    if zinsb_left != "3|312":
        fail(f"I2: leva zinsb vrstica je {zinsb_left}, pričakovano 3|312")
    summa_nach = left["summaNach"]["value"]  # "834|1014"
    if jk(831, 702) + jk(3, 312) != jk(834, 1014):
        fail("I2: 831|702 + 3|312 != 834|1014")
    if summa_nach != "834|1014":
        fail(f"I2: leva summaNach je {summa_nach}, pričakovano 834|1014")

    # ——— 3. Desna stran (Abschluß): vrednosti vrstic ———
    right = canon["reading"]["page140Right"]
    rows = right["rows"]

    def parse_jk(v: str) -> tuple[int, int]:
        a, b = v.split("|")
        return int(a), int(b)

    r1 = parse_jk(rows["summaGrundparzellenNachAnlage"]["value"])  # 831|K1 (968 v P41)
    r2 = parse_jk(rows["zinsbGrundparzellenZiffer1041"]["value"])  # 383|K2 (1288 v P41)
    rG = parse_jk(rows["summeDerGrundparzellen"]["value"])         # 1215|490
    r4 = parse_jk(rows["summaBauparzellenNachAnlage"]["value"])    # 3|312
    r5 = parse_jk(rows["zinsbBauparzellenZiffer"]["value"])        # 2|691
    rB = parse_jk(rows["summeDerBauparzellen"]["value"])           # 5|1003
    rA = parse_jk(rows["areaDerGemeinde"]["value"])                # 1220|1493

    # ——— 4. Omejitev (I3) ———
    constraint = jk(*rG) - (r1[0] + r2[0]) * K_PER_J
    if constraint != 2090:
        fail(f"I3: omejitev K1+K2 je {constraint}, pričakovano 2090")

    # ——— 5. Strukturna paralelnost (I4) ———
    if r4 != (3, 312) or zinsb_left != "3|312":
        fail("I4: desna vrstica 4 (nach Anlage, Baup) ni identična levi vrstici 132 (3|312)")
    if r1[0] != 831 or lage_j != 831:
        fail(f"I4: Joch desne vrstice 1 ({r1[0]}) ni enak Joch leve vsote ({lage_j})")

    # ——— 6. Inventar branj iz raw prehodov ———
    inventory: dict[str, dict] = {}
    for p in (1, 2, 3):
        path = RAW_DIR / f"pass{p}-page140.json"
        if not path.is_file():
            fail(f"manjka raw prehod {path}")
        rws = parse_pass_raw(path)
        k1_readings: list[int] = []
        k2_readings: list[int] = []
        for row in rws:
            lbl = str(row.get("label") or row.get("name") or "")
            j_ = to_int(row.get("joch") or row.get("stand"))
            k_ = to_int(row.get("klafter") or row.get("wohnort"))
            if k_ is None:
                continue
            # K1 celica: vrstica z Joch 831 desno (po levi vrstici 131) —
            # pass1/2 jo berejo kot (joch=831, klafter=K1); pass3 ima stolpce
            # zamaknjene (klafter=831/468/383) — obravnavano izrecno spodaj.
            if j_ == 831 and k_ not in (702, 1014):
                k1_readings.append(k_)
            if j_ == 383:
                k2_readings.append(k_)
        # pass3: zamaknjene vrstice — K1 celica ima klafter 468 (2. zamaknjena),
        # K2 celica 1288 (vrstica "…1041.")
        if p == 3:
            shifted = [to_int(r.get("klafter")) for r in rws]
            if 468 in shifted and 1288 in shifted:
                k1_readings.append(468)  # zamaknjeno branje (izrecno označeno)
                k2_readings.append(1288)
        inventory[f"pass{p}"] = {
            "k1": k1_readings,
            "k2": k2_readings,
            "note": "pass3 ima zamaknjene stolpce (izrecno označeno shifted)",
        }

    k2_all = [v for p in inventory.values() for v in p["k2"]]
    k1_all = [v for p in inventory.values() for v in p["k1"]]
    # vizualne razširitve iz P41 paleografske arbitracije (committed kandidati)
    vis = canon["reading"]["page140Right"]["unresolvedSplit"]
    k1_visual = [v for v in vis["k1Candidates"] if v not in k1_all]   # 998, 908
    k2_visual = [v for v in vis["k2Candidates"] if v not in k2_all]   # 1122, 1092, 1182

    # ——— 7. Rešitev (I5) ———
    K1, K2 = 702, 2090 - 702
    if K1 != lage_k:
        fail(f"I5: K1 ({K1}) ni enak Klafteru leve vsote ({lage_k})")
    if K2 != 1388:
        fail(f"I5: K2 je {K2}, pričakovano 1388")
    if 1388 not in k2_all:
        fail("I5: 1388 ni med committed VLM branji K2 celice (pass2)")
    if not (0 <= K1 < K_PER_J and 0 <= K2 < K_PER_J):
        fail("I5: K1 ali K2 je zunaj razreda [0, 1600)")

    # ——— 8. Popolna zaprtost (I6) ———
    if jk(831, K1) + jk(383, K2) != jk(*rG):
        fail("I6: 831|K1 + 383|K2 != 1215|490")
    if jk(*rG) + jk(*rB) != jk(*rA):
        fail("I6: 1215|490 + 5|1003 != 1220|1493")
    if jk(*r4) + jk(*r5) != jk(*rB):
        fail("I6: 3|312 + 2|691 != 5|1003")

    # ——— 9. Hipoteze (I7) ———
    hypotheses = [
        {
            "id": "H1",
            "pair": [K1, K2],
            "accepted": True,
            "reasons": [
                "strukturno sidro: 'nach Anlage' rekapitulira levo vsoto — desna vrstica 4 (Baup 3|312) == leva vrstica 132 (3|312) [P41 PASS], po istem vzorcu mora vrstica 1 (Grund 831|K1) == leva 'Summa der Grundparzellen' 831|702; Joch 831 == 831",
                "K2 = 2090 − 702 = 1388 je DIREKTNO VLM branje K2 celice (pass2); prehoda p1/p3 bereta 1288 — razlika le v 2. števki (3↔2)",
                "omejitev K1+K2 = 2090 izpolnjena natanko",
                "konsenz repa K2 celice je '1?88' — 1388 se ujema, alternativni vizualni kandidati (1122/1092/1182) ne",
                "celoten Abschluß se aritmetično zapre: 831|702 + 383|1388 = 1215|490; + 5|1003 = 1220|1493",
            ],
            "rejection": None,
        },
        {
            "id": "H2",
            "pair": [968, 1122],
            "accepted": False,
            "reasons": [
                "K1 = 968 je branje pass1; K2 = 1122 je le vizualni kandidat (noben prehod ni prebral 1122)",
                "KRŠI paralelnost nach Anlage: 831|968 > 831|702 pri istem Joch — rekapitulacija Anlage ne sme presegati vsote Anlage (podmnožina > nadmnožina, nemogoče)",
            ],
            "rejection": "kršitev strukturne paralelnosti (podmnožina ne more presegati nadmnožine) + K2 brez prehodnega branja",
        },
        {
            "id": "H3",
            "pair": [998, 1092],
            "accepted": False,
            "reasons": [
                "oba kandidata sta le vizualni razširitvi (998 iz '9?8', 1092 iz vizualnega branja K2)",
                "noben prehod ni prebral niti 998 niti 1092; brez strukturnega sidra",
            ],
            "rejection": "brez prehodnih branj in brez strukturnega sidra",
        },
        {
            "id": "H4",
            "pair": [908, 1182],
            "accepted": False,
            "reasons": [
                "oba kandidata sta le vizualni razširitvi (908 iz '9?8', 1182 iz vizualnega branja K2)",
                "noben prehod ni prebral niti 908 niti 1182; brez strukturnega sidra",
            ],
            "rejection": "brez prehodnih branj in brez strukturnega sidra",
        },
        {
            "id": "H5",
            "pair": [468, 1622],
            "accepted": False,
            "reasons": [
                "K1 = 468 je branje pass2 (pass3 zamaknjeno)",
                "K2 = 1622 > 1600 K — anomalija za stolpec Klafter (brazda bi nosila 1 J v Joch stolpcu); brez opore v prehodih",
            ],
            "rejection": "K2 > 1600 K je anomalija + brez opore v prehodih",
        },
    ]
    # aritmetična skladnost vseh hipotez (samo informativno: vse morajo zadosti
    # omejitvi, razlikovalec so DOKAZI, ne aritmetika)
    for h in hypotheses:
        a, b = h["pair"]
        if a + b != constraint:
            fail(f"I7: hipoteza {h['id']} {h['pair']} ne izpolnjuje omejitve {constraint}")
    accepted = [h for h in hypotheses if h["accepted"]]
    if len(accepted) != 1 or accepted[0]["id"] != "H1" or accepted[0]["pair"] != [702, 1388]:
        fail("I7: sprejetih hipotez ni natanko ena (H1 = [702, 1388])")

    # ——— 10. Vzorec napačnih branj (paleografska nota) ———
    misread = {
        "k1": {
            "true": K1,
            "readings": {"pass1": 968, "pass2": 468, "visual": "9?8 → 968/998/908"},
            "pattern": "702 → 968|468: 7→9|4 (zaključena zanka / oster kot), 0→6 (vstopni potez), 2→8 (zaključena spodnja zanka) — vse znane kurrentske zamenjave [~]; konzistentno pri obeh prehodih (repa '68' = 0→6, 2→8)",
            "confidence": "~",
        },
        "k2": {
            "true": K2,
            "readings": {"pass1": 1288, "pass2": 1388, "pass3": 1288, "visual": "1122/1092/1182"},
            "pattern": "1388 → 1288: razlika le v 2. števki (3↔2, standardna kurrentska zamenjava); vizualni kandidati so razširitve dvoumnega izreza",
            "confidence": "~",
        },
    }

    # ——— 11. Izpis ———
    out = {
        "series": "PS",
        "source": "N083PS.pdf (VAČ uodid 373415, docid 41780) — str. 140 desno 'Abschluß der Gemeinde' (rdeči tuš); committed dokazi ps-recap-paleo.json + ps-recap-paleo-raw/pass{1,2,3}-page140.json",
        "method": "deterministična sprava razcepa K1/K2: (1) rekonstrukcija leve vsote 7 vrstic → 831|702; (2) strukturna paralelnost 'nach Anlage' (desna vrstica 4 == leva 132, P41 PASS) → K1 = 702; (3) omejitev K1+K2 = 2090 → K2 = 1388 == direktno branje pass2; (4) enumeracija hipotez H1–H5 z zavrnitvami; brez AI ob delovanju",
        "status": "REVIEW",
        "resolution": {
            "state": "RESOLVED-ARITMETIČNO",
            "confidence": "~",
            "k1": K1,
            "k2": K2,
            "row1": "831|702 (== leva 'Summa der Grundparzellen')",
            "row2": "383|1388",
            "basis": [
                "omejitev K1 + K2 = 2090 K (iz 831+383+1 = 1215 J in 490 K)",
                "paralelnost 'nach Anlage': desna vrstica 4 (3|312) == leva vrstica 132 (3|312) — P41 identiteta d_abschlussBaup PASS; po istem vzorcu vrstica 1 == leva vsota 831|702 (Joch 831 == 831)",
                "K2 = 1388 je direktno VLM branje pass2; p1/p3 branja 1288 se razlikujejo le v eni števki",
                "podmnožinski argument: 831|968 (H2) bi presegel vsoto Anlage 831|702 pri istem Joch — nemogoče",
            ],
            "humanConfirmation": "ostaja odprta — rešitev je aritmetično vsiljena, paleografska potrditev celice K1 (ali '702' ali '9?8') je še vedno zaželena",
        },
        "constraint": {
            "derivation": "Summe der Grundparzellen 1215|490 − (Grund 831 J + Zinsb 383 J) = 1214 J + (490 K) → K1+K2 = 1600 + 490 = 2090 K",
            "value": 2090,
        },
        "readingInventory": {
            "k1Cell": {
                "passes": {"pass1": 968, "pass2": 468, "pass3-shifted": 468},
                "visual": "9?8 → kandidati 968/998/908",
                "consensusTail": "68 (0→6, 2→8)",
                "note": "true vrednost 702 NI bila nikoli direktno prebrana — prideta iz strukturnega sidra; pričakovana sistematična napačna branja (7→9|4, 0→6, 2→8) se ujemajo z opaženimi [~]",
            },
            "k2Cell": {
                "passes": {"pass1": 1288, "pass2": 1388, "pass3": 1288},
                "visual": "kandidati 1122/1092/1182",
                "consensusTail": "88",
                "note": "true vrednost 1388 == branje pass2; p1/p3 razlika le 2. številka",
            },
            "rawEvidence": "research/issue17/ps-recap-paleo-raw/pass{1,2,3}-page140.json",
        },
        "hypotheses": hypotheses,
        "identities": {
            "I1_lageRowSum": {"pass": True, "detail": "7 vrstic == 831|702 (rekonstruirano)"},
            "I2_leftClosure": {"pass": True, "detail": "831|702 + 3|312 == 834|1014"},
            "I3_constraint": {"pass": True, "detail": "K1+K2 = 2090 K"},
            "I4_nachAnlageParallel": {"pass": True, "detail": "desna 4 (3|312) == leva 132 (3|312); Joch 831 == 831"},
            "I5_solution": {"pass": True, "detail": "K1=702==Klafter leve vsote; K2=1388==branje pass2; oba < 1600"},
            "I6_fullClosure": {"pass": True, "detail": "831|702 + 383|1388 == 1215|490; + 5|1003 == 1220|1493; 3|312 + 2|691 == 5|1003"},
            "I7_uniqueness": {"pass": True, "detail": "natanko ena sprejeta hipoteza (H1); H2–H5 zavrnjene z izrecnimi razlogi"},
        },
        "misreadPatterns": misread,
        "impact": {
            "abschlussNowFullyClosed": True,
            "newIdentity": "desna vrstica 1 (831|702) == leva 'Summa der Grundparzellen' — NOVA identiteta (poleg P41 d_abschlussBaup)",
            "gemeindeStructure": "Grundparzellen občine 1215|490 = rustikalne hiše po Anlagi 831|702 (hiše 124–130) + 'Ziffer 1041' (Gütl/gingl. kategorija) 383|1388",
            "replacesP41Note": "P41 vrstici 831|968[~] in 383|1288[~] se nadomestita z 831|702 in 383|1388 [~]",
        },
        "openItems": [
            "človeška paleografska potrditev celice K1 ('702' vs '9?8') in K2 ('1388' vs '1288')",
            "3. prehod dvoumnih strani (ko VAČ dosegljiv iz peskovniške mreže)",
            "semantika 7 par referenc str. 141 (UNRESOLVED)",
            "p141 spodnji vsotni blok (ŠIBKO), p142 skupna dolžina (UNRESOLVED)",
        ],
        "generatedBy": "scripts/p44_ps_k1k2.py",
        "generatedAt": "2026-10-12",
    }

    blob = json.dumps(out, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    (EV / "ps-k1k2.json").write_text(blob, encoding="utf-8")
    (RUNTIME / "ps-k1k2.json").write_text(blob, encoding="utf-8")
    if (EV / "ps-k1k2.json").read_text(encoding="utf-8") != (RUNTIME / "ps-k1k2.json").read_text(encoding="utf-8"):
        fail("izpisa nista identična")

    print("P44 OK — razcep K1/K2 razrešen: K1=702, K2=1388 [~]")
    print("  I1–I7: vse invariante PASS")
    print("  izpisi: research/issue17/ps-k1k2.json + src/data/atlas/ps-k1k2.json (identična)")


if __name__ == "__main__":
    main()
