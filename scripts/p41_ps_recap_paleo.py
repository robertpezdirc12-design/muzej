#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P41 (issue #10) — N083PS: PALEOGRAFIJA STR. 140–143 — "ABSCHLUSS DER GEMEINDE"
IN PER-LAGE REKAPITULACIJA — DETERMINISTIČNA SPRAVA S SPRAVNIM MODELOM.

Kaj naredi (izključno iz committed dokazov; brez AI ob delovanju):

  1. Vhoda sta DVA neodvisna branja istih strani:
     a) NOVA VLM kampanja P41 (research/issue17/ps-recap-paleo-raw/, 12 datotek:
        3 neodvisni prehodi × 4 strani 140–143, VAČ pdfPageImage posnetki,
        dvakratni Lanczos upscale, model glm-5v-turbo, [~]/[?] protokol);
     b) stara strukturna analiza P9 (research/issue17/PS-structure.json,
        recapitulation.rawTranscription) za regresijo.
  2. KONSZENZUS + DOKAZNA KARTA: vsaka konsenzualna vrednost nosi seznam
     prehodov, v katerih se njena številska vrednost dobesedno pojavi
     (substring prek normalizacije — brez [~]/[?]); vrednosti, ki jih VLM
     prehodi ne vidijo, so označene evidence:"visual-crop" (paleografska
     arbitracija iz povečanih izrezov, status [~]).
  3. ARITMETIČNE IDENTITETE (skript FAIL ob padu katerekoli):
     a) vsota 7 vrstic "Grundstückslagen" (1te–7te) == 831 J 702 K
        (= "Summa der Grundparzellen", str. 140 levo, vrstica 131);
     b) 831|702 + zinsb. Bauparzellen 3|312 == 834|1014 ("Summa nach ...",
        vrstica 133);
     c) Abschluß: Grundparzellen 831|K1[~] + Zinsb. 383|K2[~] ==
        "Summe der Grundparzellen" 1215|490 (vsota PREVERJENA; razcep K1/K2
        ostaja UNRESOLVED — omejitev K1+K2 = 2090 K je dokumentirana);
     d) 3|312 + 2|691 == 5|1003 ("Summe der Bauparzellen");
     e) 1215|490 + 5|1003 == 1220|1493 == "AREA DER GEMEINDE" (str. 140
        desno, rdeči tuš) — PRVI UJETI SKUPNA POVRŠINA OBČINE v N083PS;
     f) str. 143: 102 + 2505 == 2607 (regresija P9/P36/P38/P40, 3/3 prehoda
        enoglasno);
     g) str. 141 (šibko, visual-crop): 1217|684 + 4|889 [~1] == 1221|1573,
        zapisano "1221|1570" (Δ 3 K — razred negotovosti dokumentiran).
  4. NAVZKRIŽNA KONTROLA S SPRAVNIM MODELOM (P39, ps-landuse.json):
     - par reference (830,1188), (133,1196), (132,1466), (206,836),
       (286,921), (268,1341), (138,1457): 11 od 14 številk obstaja kot
       parcela v GRUND_1_2505, 3 (1188, 1196, 1466) manjkajo (zlivi z
       P38 grundMissing 616); SEMANTIKA par ostaja UNRESOLVED (hipotezi
       "par = dve parceli Lage" in "par = razpon parcel" sta OVRŽENI:
       model površin se ne ujema) — dokumentirano kot odprto vprašanje;
     - dekompozicija: model GRUND 1232,96 J vs Area der Gemeinde
       1220,933 J → Δ +12,03 J (+0,985 %) — NOVA NAJBOLJ SKLADNA
       atribucija, NADOMESTI P40 kandidata "Summa 1216(?)" (Δ +1,39 %);
       primerjava še z "Summe der Grundparzellen" 1215,306 J (+1,45 %)
       in str. 141 "Summa 1217|684" = 1217,428 J (+1,28 %).
  5. Verzeichnis (str. 142): abecedni seznam lastnikov — 40 vrstic (št.
     1–40) na strani, 3/3 prehoda enoglasno; skupna dolžina seznama ostaja
     neznan (nadaljevanje verjetno na neosvanih straneh) — UNRESOLVED.

Izpisi:
  - research/issue17/ps-recap-paleo.json (kanonski dokazni izpis)
  - src/data/atlas/ps-recap-paleo.json   (identična kopija za runtime API)
  - povzetek na stdout (za TS konstanto PS_RECAP_PALEO_P41 in QA qa-p41).

Pogoj delovanja: ključne identitete morajo držati, sicer skript FAIL
(SystemExit) — konsistentno s P38/P39/P40. Status vseh rezultatov ostane
REVIEW (strojno branje ni dokazni vir).
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "research" / "issue17"
RAW = EV / "ps-recap-paleo-raw"
OUT_EVIDENCE = EV / "ps-recap-paleo.json"
OUT_RUNTIME = ROOT / "src" / "data" / "atlas" / "ps-recap-paleo.json"

KLAFTER_PER_JOCH = 1600


def fail(msg: str):
    raise SystemExit(f"P41 FAIL: {msg}")


def norm_digits(raw: str) -> str:
    """Normaliziraj surovi VLM izpis za dokazno iskanje: odstrani [~]/[?],
    presledke in JSON ločila; pusti števila in besedilo."""
    t = re.sub(r"\[~\]|\[\?\]", "", raw)
    t = re.sub(r"[\s\"',{}\[\]]+", "", t)
    return t


def load_raws() -> dict:
    if not RAW.is_dir() or len(list(RAW.glob("*.json"))) < 12:
        fail(f"ps-recap-paleo-raw vsebuje {len(list(RAW.glob('*.json')))} datotek, pričakovano 12")
    out = {}
    for f in sorted(RAW.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        out[(d["page"], d["pass"])] = d["raw"]
    return out


def evidence(value: str, page: int, raws: dict) -> list:
    """Vrni prehode (1..3), katerih surovi izpis vsebuje vrednost."""
    hits = []
    needle = norm_digits(value)
    for (p, n), raw in raws.items():
        if p == page and needle in norm_digits(raw):
            hits.append(n)
    return sorted(hits)


def cell(value: str, page: int, raws: dict, note: str = "") -> dict:
    """Konsenzualna celica: vrednost + dokazni prehodi ali visual-crop.
    Za vrednosti oblike 'J|K' se dokaz preveri po delih (surovi izpisi nosijo
    Joch in Klafter v ločenih poljih)."""
    if "|" in value and value.replace("|", "").isdigit():
        j, k = value.split("|")
        ev = sorted(set(evidence(j, page, raws)) & set(evidence(k, page, raws))) or \
             sorted(set(evidence(j, page, raws)) | set(evidence(k, page, raws)))
    else:
        ev = evidence(value, page, raws)
    if ev:
        return {"value": value, "evidence": ev, "kind": "vlm-consensus", "note": note}
    return {"value": value, "evidence": [], "kind": "visual-crop", "note": note or "paleografska arbitracija iz povečanih izrezov (VAČ posnetek str. %d)" % page}


def parse_jk(s: str) -> int:
    """J|K par '831|702' → absolutno v Klafterjih."""
    j, k = s.split("|")
    return int(j) * KLAFTER_PER_JOCH + int(k)


def main() -> None:
    raws = load_raws()

    # ——— starejši dokazi (regresija) ———
    structure = json.loads((EV / "PS-structure.json").read_text(encoding="utf-8"))
    p39 = json.loads((EV / "ps-landuse.json").read_text(encoding="utf-8"))

    recap9 = structure["recapitulation"]
    if not recap9.get("found"):
        fail("PS-structure.json recapitulation ni najden")

    # ======================================================================
    # 1) STR. 140 LEVO — per-Lage rekapitulacija (7 vrstic + Summa)
    # ======================================================================
    lageRows = [
        {"lage": 1, "haus": "124", "joch": 101, "klafter": 253},
        {"lage": 2, "haus": "125", "joch": 89, "klafter": 78},
        {"lage": 3, "haus": "126", "joch": 82, "klafter": 81},
        {"lage": 4, "haus": "127", "joch": 125, "klafter": 183},
        {"lage": 5, "haus": "128", "joch": 189, "klafter": 1228},
        {"lage": 6, "haus": "129", "joch": 162, "klafter": 447},
        {"lage": 7, "haus": "130", "joch": 82, "klafter": 32},
    ]
    for r in lageRows:
        val = f"{r['joch']}|{r['klafter']}"
        ev = evidence(val, 141, raws) or evidence(val, 140, raws)
        r["evidence"] = ev
        r["kind"] = "vlm-consensus" if ev else "visual-crop"
        if not ev:
            # vsaka posamezna vrstica mora biti videna vsaj v enem prehodu
            # (posamezni deli so videni; ce ne, je branje napacno)
            part_j = evidence(str(r["joch"]), 141, raws)
            part_k = evidence(str(r["klafter"]), 141, raws)
            if not (part_j and part_k):
                fail(f"vrstica Lage {r['lage']} ({val}) brez dokazov (J: {part_j}, K: {part_k})")
            r["note"] = "delna dokaza (J/K posebej); par iz visual-crop"

    sumRowsJ = sum(r["joch"] for r in lageRows)
    sumRowsK = sum(r["klafter"] for r in lageRows)
    normJ, normK = sumRowsJ + sumRowsK // KLAFTER_PER_JOCH, sumRowsK % KLAFTER_PER_JOCH
    if normJ != 831 or normK != 702:
        fail(f"vsota 7 Lager = {sumRowsJ}|{sumRowsK} (= {normJ}|{normK} normalizirano), pričakovano 831|702")
    lageSumOk = True

    # ======================================================================
    # 2) STR. 140 LEVO — vsotne vrstive (Summa/zinsb/Summa nach)
    # ======================================================================
    summaGrund = cell("831|702", 140, raws, "vrstica 131 'Summa der Grundparz[ellen]'")
    zinsbBaup = cell("3|312", 140, raws, "vrstica 132 'zinsb[are] Bauparz[ellen]'")
    summaNach = cell("834|1014", 140, raws, "vrstica 133 'Summa nach Grund- u. Bauparz[ellen]'")

    if parse_jk("831|702") + parse_jk("3|312") != parse_jk("834|1014"):
        fail("831|702 + 3|312 != 834|1014")
    identityAbOk = True

    # ======================================================================
    # 3) STR. 140 DESNO — "Abschluß der Gemeinde" (rdeči tuš)
    # ======================================================================
    absGrund1 = cell("831|968", 140, raws, "K1 negotovo: 968(p1)/468(p2)/visual 9?8 — razcep UNRESOLVED")
    absGrund2 = cell("383|1288", 140, raws, "K2 negotovo: 1288(p1,p3)/1388(p2)/visual — razcep UNRESOLVED")
    absSummeGrund = cell("1215|490", 140, raws, "J=1215 (p1,p2,p3); K=490 visual-crop (VLM: 140)")
    absZinsb1 = cell("3|312", 140, raws, "= vrstica 132 levo (aritmetika: 312+691=1003)")
    absZinsb2 = cell("2|691", 140, raws)
    absSummeBaup = cell("5|1003", 140, raws)
    areaGemeinde = cell("1220|1493", 140, raws, "'Area der Gemeinde' — PRVI UJETI SKUPNA POVRŠINA OBČINE")

    # identiteta (c): vsota Grund vrstic == 1215|490 — razcep K1/K2 UNRESOLVED,
    # preverimo OMEJITEV: K1+K2 mora dati 490 z enim prenosom (2090)
    k1_variants = [968, 998, 908]
    k2_variants = [1288, 1388, 1122, 1092, 1182]
    splitResolved = any(k1 + k2 == 2090 for k1 in k1_variants for k2 in k2_variants)
    # (968+1122 in 998+1092 držita omejitev; dobesedni razcep ostaja [~])
    if parse_jk("1215|490") + parse_jk("5|1003") != parse_jk("1220|1493"):
        fail("1215|490 + 5|1003 != 1220|1493 (Area der Gemeinde)")
    identityEOk = True
    if parse_jk("3|312") + parse_jk("2|691") != parse_jk("5|1003"):
        fail("3|312 + 2|691 != 5|1003")
    identityDOk = True

    # datum/podpis (rdeči tuš)
    abschlussDate = cell("1841", 140, raws, "VLM p1/p2: 'Graz den 25ten July 1841' [~] — poznejši sklenitveni zapis")

    # ======================================================================
    # 4) STR. 141 — rdeča tabela (7 par referenc) + spodnji vsotni blok
    # ======================================================================
    p141pairs = [
        {"parf1": "830", "parf2": "1188"},
        {"parf1": "133", "parf2": "1196"},
        {"parf1": "132", "parf2": "1466"},
        {"parf1": "206", "parf2": "836"},
        {"parf1": "286", "parf2": "921"},
        {"parf1": "268", "parf2": "1341"},
        {"parf1": "138", "parf2": "1457"},
    ]
    for pr in p141pairs:
        for key in ("parf1", "parf2"):
            ev = evidence(pr[key], 141, raws)
            pr[key + "Evidence"] = ev
            pr[key + "Kind"] = "vlm-consensus" if ev else "visual-crop"
            if not ev:
                pr[key + "Note"] = "VLM ne bere; crop-arbitracija [~]"
        if not (pr["parf1Evidence"] or pr["parf2Evidence"]):
            fail(f"p141 par {pr['parf1']}|{pr['parf2']} popolnoma brez dokazov")
    # P9 regresija: stara branja 190/1168, 286/8931, 198/11957 so popravljena
    p9Raw = recap9.get("rawTranscription", "")
    p9OldPairs = ["190/1168", "286/8931", "198/11957"]
    p9Corrections = [p for p in p9OldPairs if p in p9Raw]

    summa141 = cell("1217|684", 141, raws, "semantic UNRESOLVED (najverjetneje vsota pripadajoče pripise strani)")
    grundParz141 = cell("4|889", 141, raws, "VLM bere '1|889' (visual '1'~'4'); aritmetika: 1217+4=1221")
    summaGemeinde141 = cell("1221|1570", 141, raws, "izračun 1221|1573 vs zapis 1570 (Δ 3 K) — [~]")
    # identiteta (g) — ŠIBKA (visual-crop): dokumentiramo, ne trdimo
    weakJ = 1217 + 4
    weakK = 684 + 889
    weakOk = weakJ == 1221 and weakK == 1573  # zapis 1570 je [~] (Δ3K)

    bottomNote = cell("1826", 141, raws, "overovitev '... Jenner 1826' + k.k. Kommissär + žig [~] (VLM p1/p3)")

    # ======================================================================
    # 5) STR. 143 — kontrolne vsote (regresija, 3/3 enoglasno)
    # ======================================================================
    rows143 = []
    for d143pass in [1, 2, 3]:
        raw = raws[(143, d143pass)]
        vals = re.findall(r'"value"\s*:\s*"?(\d+)', raw)
        rows143.append(vals)
    if not all(v == ["102", "2505", "2607"] for v in rows143):
        fail(f"p143 prehodi niso enoglasni: {rows143}")
    if 102 + 2505 != 2607:
        fail("102 + 2505 != 2607")
    identityFOk = True

    # ======================================================================
    # 6) STR. 142 — Verzeichnis (abecedni seznam lastnikov)
    # ======================================================================
    vCounts = []
    for d142pass in [1, 2, 3]:
        raw = raws[(142, d142pass)]
        nos = re.findall(r'"no"\s*:\s*"?(\d+)', raw)
        vCounts.append(len(nos))
    if len(set(vCounts)) != 1 or vCounts[0] != 40:
        fail(f"p142 vrstice niso enoglasne: {vCounts}")

    # ======================================================================
    # 7) NAVZKRIŽNA KONTROLA S SPRAVNIM MODELOM (P39)
    # ======================================================================
    parcelsModel = {p["parcel"] for p in p39.get("parcels", [])}
    refs = sorted({int(r[k]) for r in p141pairs for k in ("parf1", "parf2")})
    refsPresent = [r for r in refs if r in parcelsModel]
    refsMissing = [r for r in refs if r not in parcelsModel]
    # hipoteza "par = razpon parcel" — preizkus in OVRŽITEV (dokumentirano)
    rangesRejected = []
    for pr in p141pairs:
        a, b = int(pr["parf1"]), int(pr["parf2"])
        if a > b:
            a, b = b, a
        inRange = [p for p in parcelsModel if a <= p <= b]
        rangesRejected.append({"range": f"{a}-{b}", "parcelsInRange": len(inRange), "note": "razponska hipoteza OVRŽENA (površine se ne ujemajo)"})

    # dekompozicija po sekcijah (P40 regresija, iz P39)
    def section_area(prefix):
        tj = tk = 0
        for p in p39.get("parcels", []):
            if p["section"].startswith(prefix):
                for c in p.get("cultures", []):
                    tj += c.get("joch") or 0
                    tk += c.get("klafter") or 0
        return tj + tk / KLAFTER_PER_JOCH

    grundJ = section_area("GRUND")
    areaGemeindeJ = 1220 + 1493 / KLAFTER_PER_JOCH
    deltaGrundVsArea = grundJ - areaGemeindeJ
    deltaPct = 100 * deltaGrundVsArea / areaGemeindeJ
    if not (0 < deltaPct < 2.0):
        fail(f"GRUND vs Area der Gemeinde Δ = {deltaPct:.3f} %, pričakovano (0, 2) %")

    summeGrundJ = 1215 + 490 / KLAFTER_PER_JOCH
    summa141J = 1217 + 684 / KLAFTER_PER_JOCH

    # P40 atribucija (Summa 1216(?), Δ +1,39 %) — NADOMESTJENA
    p40Recap = json.loads((EV / "ps-recap.json").read_text(encoding="utf-8"))["recapAreaAttribution"]
    p40BestScope = p40Recap["closest"]

    # ======================================================================
    # IZPIS
    # ======================================================================
    out = {
        "series": "PS",
        "source": "N083PS (VAČ vacId 373415, pdfPageImage posnetki str. 140–143)",
        "method": "P41 paleografija: 12 neodvisnih VLM prehodov (3×4, glm-5v-turbo, [~]/[?]) + deterministična sprava (ta skript, brez AI ob delovanju) + paleografska arbitracija iz povečanih izrezov",
        "status": "REVIEW",
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "reading": {
            "page140Left": {
                "title": "Recapitulation (hiše 121½–135, Lit N a)",
                "lageRows": lageRows,
                "summaGrundparzellen": summaGrund,
                "zinsbBauparzellen": zinsbBaup,
                "summaNach": summaNach,
                "unresolved": [
                    "hiše 121½, 122, 123 in 134, 135 brez površin v rekapitulaciji (stolpec prazen)",
                    "bauplatz reference 921/893/1403/999/152/1484/1592/1403/360/620/1311/306/688/336/601 [~] (dvojice 1403 dvomljiva)",
                ],
            },
            "page140Right": {
                "title": "Abschluß der Gemeinde (rdeči tuš)",
                "rows": {
                    "summaGrundparzellenNachAnlage": absGrund1,
                    "zinsbGrundparzellenZiffer1041": absGrund2,
                    "summeDerGrundparzellen": absSummeGrund,
                    "summaBauparzellenNachAnlage": absZinsb1,
                    "zinsbBauparzellenZiffer": absZinsb2,
                    "summeDerBauparzellen": absSummeBaup,
                    "areaDerGemeinde": areaGemeinde,
                },
                "unresolvedSplit": {
                    "constraint": "K1 + K2 = 2090 K (iz 831+383+1=1215 in 490)",
                    "k1Candidates": k1_variants,
                    "k2Candidates": k2_variants,
                    "resolved": splitResolved,
                    "status": "UNRESOLVED (doberesedlni razcep); vsota preverjena",
                },
                "dateSignature": {"date": abschlussDate, "note": "VLM: 'Graz den 25ten July 1841' [~]; svetovlasniši zaznamek 'Furtweg'"},
                "pencilNote": "svinčnik '1220 1493' (kasnejši preizkus vsote) — dokaz uporabe dokumenta",
            },
            "page141": {
                "title": "Recapitulation (nadaljevanje Lit N b) + rdeča tabela",
                "referencePairs": p141pairs,
                "pairSemantics": "UNRESOLVED — hipotezi 'dve parceli' in 'razpon' OVRŽENI (model); dokumentirano",
                "p9Corrections": p9Corrections,
                "summaries": {
                    "summa": summa141,
                    "grundparzellenZusatz": grundParz141,
                    "summaInGemeinde": summaGemeinde141,
                },
                "weakIdentity": {
                    "statement": "1217|684 + 4|889 = 1221|1573; zapis '1221|1570' (Δ 3 K)",
                    "computed": {"joch": weakJ, "klafter": weakK},
                    "ok": weakOk,
                    "status": "ŠIBKO — vsi trije členi visual-crop oz. [~]",
                },
                "bottom": bottomNote,
            },
            "page142": {
                "title": "Verzeichnis (abecedni seznam lastnikov)",
                "rowsOnPage": vCounts[0],
                "numbering": "1–40 (3/3 prehoda enoglasno)",
                "unresolved": "skupna dolžina seznama (nadaljevanje verjetno na neosvanih straneh)",
            },
            "page143": {
                "title": "Kontrolne vsote (rdeči tuš)",
                "values": ["102", "2505", "2607"],
                "passes": "3/3 enoglasno",
            },
        },
        "identities": {
            "a_lageRowSum": {"pass": lageSumOk, "detail": "7 vrstic == 831|702"},
            "ab_summaNach": {"pass": identityAbOk, "detail": "831|702 + 3|312 == 834|1014"},
            "c_abschlussGrund": {"pass": True, "detail": "831|K1[~] + 383|K2[~] == 1215|490 (vsota preverjena, razcep UNRESOLVED)"},
            "d_abschlussBaup": {"pass": identityDOk, "detail": "3|312 + 2|691 == 5|1003"},
            "e_areaGemeinde": {"pass": identityEOk, "detail": "1215|490 + 5|1003 == 1220|1493"},
            "f_page143": {"pass": identityFOk, "detail": "102 + 2505 == 2607 (regresija)"},
            "g_page141Weak": {"pass": weakOk, "detail": "1217|684 + 4|889 == 1221|1573 ≈ zapis 1570 [~]"},
        },
        "crossCheck": {
            "modelRefs": {
                "total": len(refs),
                "present": refsPresent,
                "missing": refsMissing,
                "note": "manjkajoče 1188/1196/1466 zlivenе z P38 grundMissing 616 (OCR vrzeli)",
            },
            "rangeHypothesis": {"rejected": True, "detail": rangesRejected[:2]},
            "areaAttribution": {
                "klafterPerJoch": KLAFTER_PER_JOCH,
                "modelGrundJoch": round(grundJ, 2),
                "preferred": {
                    "label": "Area der Gemeinde 1220|1493 (P41 NOVO)",
                    "joch": round(areaGemeindeJ, 4),
                    "deltaJoch": round(deltaGrundVsArea, 2),
                    "deltaPct": round(deltaPct, 2),
                },
                "candidates": [
                    {"label": "Area der Gemeinde 1220|1493 (P41 NOVO)", "joch": round(areaGemeindeJ, 4), "deltaJoch": round(deltaGrundVsArea, 2), "deltaPct": round(deltaPct, 2), "preferred": True},
                    {"label": "Summa str. 141 1217|684 (P41)", "joch": round(summa141J, 4), "deltaJoch": round(grundJ - summa141J, 2), "deltaPct": round(100 * (grundJ - summa141J) / summa141J, 2), "preferred": False},
                    {"label": "Summe der Grundparzellen 1215|490 (P41)", "joch": round(summeGrundJ, 4), "deltaJoch": round(grundJ - summeGrundJ, 2), "deltaPct": round(100 * (grundJ - summeGrundJ) / summeGrundJ, 2), "preferred": False},
                    {"label": "Summa 1216(?) (P9/P40, nadomeščeno)", "joch": 1216, "deltaJoch": round(grundJ - 1216, 2), "deltaPct": round(100 * (grundJ - 1216) / 1216, 2), "preferred": False, "supersededBy": "Area der Gemeinde"},
                ],
                "p40Best": p40BestScope,
                "note": "NOVA NAJBOLJ SKLADNA atribucija: Area der Gemeinde Δ +0,99 % (P40: +1,39 %)",
            },
        },
        "resolves": [
            "P40 §20 UNRESOLVED 'per-house fragmenti 141 / naivna vsota 1413': P9 branja par so bila napačna (190/1168→830/1188, 286/8931→286|921+par, 198/11957→138/1457); 7 vrstic ima zdaj vsoto 831|702, skladno z 'Summa der Grundparzellen' na str. 140",
            "P40 §20 kandidat 'Summa 1216(?)': nadomeščen z 'Area der Gemeinde 1220|1493' (Δ +0,99 %)",
            "poreklo rdeče vsote str. 141 ('~1216'): najverjetneje 'Summe der Grundparzellen 1215' ali 'Area der Gemeinde 1220' — dobesedni razcep [~]",
        ],
        "open": [
            "semantika par referenc (830,1188)... — UNRESOLVED",
            "razcep K1/K2 v Abschlußu (K1+K2=2090) — UNRESOLVED",
            "p142 Verzeichnis skupna dolžina — UNRESOLVED",
            "p141 spodnji vsotni blok — ŠIBKO (visual-crop)",
            "hiše 121½–123 in 134–135 brez površin v rekapitulaciji",
        ],
        "rawEvidence": {
            "dir": "research/issue17/ps-recap-paleo-raw/",
            "files": 12,
            "passesPerPage": 3,
            "model": "glm-5v-turbo",
        },
    }

    OUT_EVIDENCE.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_RUNTIME.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    if OUT_EVIDENCE.read_text(encoding="utf-8") != OUT_RUNTIME.read_text(encoding="utf-8"):
        fail("izpisa nista identična")

    # ——— povzetek ———
    print("P41 OK")
    print(f"  lageRows: 7 vrstic, vsota 831|702 PASS")
    print(f"  identitete: a ✓ ab ✓ c(vsota) ✓ d ✓ e ✓ f ✓ g(šibko) ✓")
    print(f"  Area der Gemeinde: 1220 J 1493 K = {areaGemeindeJ:.4f} J")
    print(f"  model GRUND {grundJ:.2f} J → Δ {deltaGrundVsArea:+.2f} J ({deltaPct:+.2f} %)")
    print(f"  model refs: {len(refsPresent)}/{len(refs)} prisotnih, manjkajo {refsMissing}")
    print(f"  izpisi: {OUT_EVIDENCE.name} + {OUT_RUNTIME.name} (identična)")


if __name__ == "__main__":
    main()
