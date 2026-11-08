#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P42 (issue #10) — N083PS: PRAVILNIK RAB v2 — deterministična razširitev klasifikacije
rab nad P39 model (parcela × raba), brez AI ob delovanju.

Kaj naredi (izključno iz committed dokazov src/data/atlas/ps-landuse.json, P39):
  1. Rekonstruira v1 klasifikacijo iz SUROVIH vrednosti (identičen norm + 12 pravil
     kot scripts/p39_ps_landuse.py) in zavrača (FAIL), če se kogar koli pari razlikuje
     od shranjenega `classes`/`primary` — regresijska kontrola P39.
  2. Priloži 13 novih pravil (vrstni red 13–25, PRVI ZADETEK = primarni razred).
     Vsa v1 pravila ostanejo nespremenjena na nespremenjenih mestih → v2 ⊇ v1
     (vsak pari z v1 primarno jo ohrani; preverjeno izrecno).
  3. Vrednostim brez kulturnega pravila dodeli izrecni termType:
       - TOPONIM   (eksplicitni seznam, pregledan vrednost po vrednost — lokacijska
                    oznaka, NE raba; formant + zaupanje [~]/[?])
       - ARTIFAKT  (številke/registrične besede/opombe o prihodkih v stolpcu rabe)
       - NEKLASIFICIRANO (ostanek, z družinsko analizo za paleografijo)
  4. Izračuna so-odvisnostne dokaze (isti parceli / isti lastnik) za dvoumne
     družine (Lhut, Lohn, Äfling, …) — DOKAZ za prihodnjo paleografijo, ne ugibanj.
  5. Izpiše:
       - research/issue17/ps-landuse-v2.json  (kanonski dokaz)
       - src/data/atlas/ps-landuse-v2.json    (identična runtime kopija)

Invariante (FAIL ob padu):
  - v1 rekonstrukcija == P39 shranjeno (2632 parov)
  - v2 ⊇ v1: nič pari ne izgubi ali spremeni v1 primarno
  - TOPONIM/ARTIFAKT seznami ⊥ vseh pravil (regex in v1 in v2) in med seboj
  - KULTURA + TOPONIM + ARTIFAKT + NEKLASIFICIRANO = 2632 parov
  - družine Lhut/Lohn/Ahn/Äfling ostajajo NEKLASIFICIRANE (pinane)

Vse surove vrednosti ostanejo nedotaknjene; vsi statusi ostajajo REVIEW.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASIS = ROOT / "src" / "data" / "atlas" / "ps-landuse.json"
OUT_EVIDENCE = ROOT / "research" / "issue17" / "ps-landuse-v2.json"
OUT_RUNTIME = ROOT / "src" / "data" / "atlas" / "ps-landuse-v2.json"

# ——— v1 pravila (NESPREMENJENA, vrstni red del pravilnika) ———
V1_RULES = [
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

# ——— v2 priložena pravila (13–25; aplicirajo SAMO na v1 neklasificirane vrednosti) ———
# confidence: "~" = utemeljena interpretacija termina, "?" = spekulativnejša
V2_RULES = [
    ("OBCINA", r"gmde\b|gmand\b|gimand|gemaind", "~",
     "dialektne okrajšave Gemainde (Gmde/Gmand/Gimand) = občinska skupna zemlja; "
     "Gumig Gmde, Lohgimand NNN (= Lohgemainde, skupna lohišča)"),
    ("TRAVNIK", r"maid\b", "~",
     "Maid = Mahd = Mähwiese (kärntensko); družina Haitenmaid (Leinwand/Gründung/Balazig)"),
    ("TRAVNIK", r"gras\b|heu\b|wisen\b|rasen\b", "~",
     "Gras/Heu = travniški pridelek (einheimisches Gras/Heu); wisen = Wiesen; Rasen = travišče"),
    ("VINOGRAD", r"wein", "~",
     "sami 'Wein'/'Weing' = okrajšava za Weingarten (v1 je zahteval weingarten|weinberg — "
     "vrzel: 10 parov vinogradov je bilo nevidnih)"),
    ("VRT", r"gae?rt", "~",
     "umlaut Gärten (→ gaerten) — v1 'gart' jih ni ujel; Findling/Himbeeren/Gebüsch/Einhait und Gärten"),
    ("VRT", r"obst|himbeer|gmias", "~",
     "Obst = sadovnjak, Himbeeren = malinje, Gmias = Gemüse (zelenjava)"),
    ("NJIVA", r"rueben|schlagfeld|stopp\b|achl\b|frucht", "~",
     "Rüben = poljska kultura; Schlagfeld = izsekano polje (Feld); Stopp = Stoppeln (ozimje); "
     "Achl = kärntensko za Acker (deminutiv); Frucht = žito"),
    ("GOZD", r"wald|gebuesch|straeuch|eichhol|laub\b|laubm|lorbeer|baum", "~",
     "sredbesedni -wald (Schlagwald, Lohwald — v1 \\\\bwald jih je zgrešil); Gebüsch/Gesträuch; "
     "Eichhol = hrastov les; Laub/Laubm. = listavec; Lorbeer (sami = drevesa); baum = drevesna opomba "
     "(Schindel baum, baumart)"),
    ("PASTVISCE", r"shut\b|johut\b|weid", "~",
     "-shut (Schingutshut = pašnik k meta farmi Schingut), Johut (= Jochhut?), weid BREZ \\\\b "
     "(Schafweide — v1 \\\\bweid je zgrešil sredbesedno); IZRECNO NE zajame Lhut (družina ostaja neznana)"),
    ("NEROD", r"aehnl?\b|eidn\b|eidau|ehda\b|inoed|aeinod|wist|brache\b", "~",
     "Öhnl/Aehn = osuto; Eidn/Eidau/Ehda = Öden/Ödau (dialektne zapiske ö→ei/e); "
     "Ainöd/Aeinod = Einöde; Wist* = wüst (opustošeno); Brache = osuto"),
    ("TRAVNIK", r"malde\b", "?",
     "Malde = Mahd (kärntensko, Schatz: Wörterbuch); samo 'Ehmalde' 1 par — spekulativno"),
    ("STAVBNO", r"schupf|staidl|grube\b|gutl\b|edl?hop|edhup|hau(ss)?\b|boden\b", "~",
     "Schupfe (v1 schupfn ni ujel schupf./schupfen!); Staidl = Stadel; Grube (Lohgrube = strojna jama, "
     "Steingrube = kamnolom); -gutl = Gütl (kmetija); Ed-/Edl-hop = Öd-/Edelhof; -hauß/-haus; "
     "Boden (Schüttboden = pod — 100 % so-odvisnost s STAVBNO)"),
    ("VODA", r"lachen?\b", "~", "Lache(n) = lokva/mlaka"),
]

RULE_LABELS_SI = {
    "VINOGRAD": "vinograd", "NJIVA": "njiva (Acker)", "TRAVNIK": "travnik (Wiese)",
    "GOZD": "gozd (Wald)", "PASTVISCE": "pašnik (Weide/Hutweide/Trift)",
    "ALM": "planina (Alm/Alpe)", "VRT": "vrt (Garten)", "NEROD": "nerodovoljna (Ödung)",
    "STAVBNO": "stavbna/gospodarska", "VODA": "voda", "OBCINA": "občinska skupna",
    "CESTA": "pot/cesta",
}


def norm(s: str) -> str:
    """Identično P39: male črke, ä→ae, ö→oe, ü→ue, ß→ss."""
    s = s.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    return s


def classes_for(raw: str, rules) -> list:
    n = norm(raw)
    return [cls for cls, _pat in rules if re.search(_pat, n)]


# ——— TOPONIM: eksplicitni seznam (pregledan vrednost po vrednost; P42 dokaz) ———
# (raw, formant, confidence, opomba)
TOPONYM_LIST = [
    ("Löwisch Thal", "thal", "~", "Löwenthal — dolinsko ime"),
    ("Leite", "leite", "~", "Leite = požleb/naklon — mikrolokalna oznaka"),
    ("Schüttgrund", "grund", "~", "'Schütt-Grund' — zemljiško ime (Grund = parcela/tla)"),
    ("Winkel", "winkel", "~", "kot/ogljek — ležajno ime"),
    ("Zehorn", "horn", "~", "horn = gorski vrh — ležajno ime"),
    ("Abhang", "hang", "~", "naklon — terenski opis"),
    ("Ablay", "lay", "~", "lay = skala/plaz (kärntensko) — ležajno ime"),
    ("Ebneist", "eben", "~", "eben = ravnina — terensko ime"),
    ("Ebnerd", "eben", "~", "eben + Erd — 'ravna zemlja'"),
    ("Lbney", "eben", "?", "verjetno Eben(e) — okrnjen zapis"),
    ("Ebene ?", "eben", "~", "izrecno dvomljiv zapis (?), terenski opis"),
    ("Ebnisgutland", "eben", "~", "sestavljeno terensko ime (Eben…-gut-land)"),
    ("Schmieggrat", "grat", "~", "grat = greben — ležajno ime"),
    ("Lipfmaß, Hang in Böschung", "hang", "~", "terenski opis naklona/bočaske"),
    ("Grien", "grien", "~", "Grien = prod/nahaj (kärntensko) — opis tal"),
    ("Lehmo", "lehm", "~", "Lehm = glina — opis tal"),
    ("Lehmg.", "lehm", "~", "Lehm(g) — okrajšan opis tal"),
    ("Lehga", "lehm", "?", "morda Lehm-ga… — okrnjeno"),
    ("Lhga", "lehm", "?", "morda Lehm-ga… — okrnjeno"),
    ("Indrunt Laimen", "lehm", "~", "'in der Grund' + Laimen = glinena tla"),
    ("Indrund Laimen", "lehm", "~", "varianta zapisa"),
    ("Indrult Laimen", "lehm", "~", "varianta zapisa"),
    ("Indrunt Leimen", "lehm", "~", "Leimen = glina"),
    ("Eingemaut Gfrörer und Laimauer", "laim/au", "~", "opis lege: 'eingemauerte Gfrörer- und Laimau' (zmrzovalna kotanja in glinena au)"),
    ("Eingemaut Laimauer", "laim/au", "~", "okrajšana varianta"),
    ("Eingemaut Gfrörer und Lorenz", "laim/au", "~", "varianta (Lorenz/Laimen?)"),
    ("Eingemaut Lorenz", "laim/au", "~", "okrajšana varianta"),
    ("Abtränig Spötlg. Leumuth", "leum/au", "~", "opis lege (Abtränig = odcepek? + Leumaue)"),
    ("Abtränig Leumuth", "leum/au", "~", "okrajšana varianta"),
    ("Abtränig Spötlg.", "abtränig", "~", "okrajšana varianta"),
    ("Gübel", "gübel", "~", "Gübel/Gupf = gričevnat vrh (kärntensko)"),
    ("Gebürg", "gebürg", "~", "Gebürg = Gebirge — terenska oznaka"),
    ("Gruning Grunau", "au", "~", "Grünau — ležajno ime"),
    ("Ehing", "ing", "~", "-ing = prazgodovinsko-srednjeveški naselbinski formant"),
    ("Ehinga", "ing", "~", "varianta zapisa"),
    ("Ebingach", "ach", "~", "-ach/-aach = vodni formant v imenu"),
    ("o. Ried", "ried", "~", "Ried = ledinsko ime (kärntensko)"),
]

# ——— ARTIFAKT: številke/registrične besede/opombe v stolpcu rabe ———
# (raw, razlog, confidence)
ARTIFAKT_LIST = [
    ("81. flur", "številka + flur (poljna regija) — lokacijska oznaka namesto rabe", "~"),
    ("100 Futter", "opomba o prihodkih (Futter = krma/krmna enota)", "?"),
    ("65 Fürtrg.", "opomba o prihodkih (Fürtrg. ≈ Fütterung/Futtertrag)", "?"),
    ("87 Furtreg.", "opomba o prihodkih (Furtreg. ≈ Futtertrag)", "?"),
    ("Furtrage", "opomba o prihodkih (Furtrage ≈ Futterträge)", "?"),
    ("[?] Fürstg.", "neberljiva okrajšava s [?]; morda Fürtrg.", "?"),
    ("Summa", "registrična beseda (vsota) — prišla v stolpec rabe", "~"),
    ("Zahl", "registrična beseda (številka)", "~"),
    ("5k Einträg", "opomba (Einträge = vnosi/pridelki)", "?"),
    ("29 Bäumen", "opomba številu dreves", "~"),
]

# ——— družine za paleografijo (ostajajo NEKLASIFICIRANE — pinano) ———
FAMILIES = [
    {"id": "LHUT-JEDRO", "values": ["Lhut", "Lhup", "Lhupf", "Lhupa", "Lhuta"],
     "hypothesisSi": "morda L+Hut (pašnik) ali Lehen-Hut; tudi Rhut (Rodung) ob zamenjavi R/L v Kurrentu — NE dokazano",
     "confidence": "?"},
    {"id": "LHIZ", "values": ["Lhize", "Lhizl"],
     "hypothesisSi": "ista neznana družina kot Lhut-jedro (Lhizgutl [?] pa v2 STAVBNO prek formanta -gutl = Gütl)",
     "confidence": "?"},
    {"id": "LHOPI-LOHIFA", "values": ["Lhopi", "Lohifa", "Luppa", "Shüfa"],
     "hypothesisSi": "morda ista korenina kot Lhut (t/p/f obrati OCR) — NE dokazano",
     "confidence": "?"},
    {"id": "LOHN-RAUT", "values": ["Lohn", "Lohng", "Lohnraut Gfüttergütl", "Lohnraut Bäurean", "Lohnraut Lönnean"],
     "hypothesisSi": "Lohn/Loh = izsek (Waldschlag) ALBO Loh = strojnica; Raut = Rodung (izsek) — smer GOZD?/NJIVA? — NE dokazano",
     "confidence": "?"},
    {"id": "AHN", "values": ["Ahn"], "hypothesisSi": "morda Ahorn (javor) ali Acker-dialekt — NE dokazano", "confidence": "?"},
    {"id": "AEFLING", "values": ["Äfling"],
     "hypothesisSi": "neznano; so-odvisnost: 12/13 parov na parcelah s TRAVNIK → travniški kontekst, termin ostaja neznan", "confidence": "?"},
    {"id": "ERDAR", "values": ["Erdar", "Eidar", "Achat", "Achm"],
     "hypothesisSi": "morda Erd-/Eid- (Öd?) ali Achm = Acker-Mad — NE dokazano; Erdar 4/4 so-odvisnost GOZD", "confidence": "?"},
    {"id": "GUETEN", "values": ["Güten", "Gütung"],
     "hypothesisSi": "morda 'die Güten' (rodovitna tla) ali Güter (kmetije) — NE dokazano (v1 umlaut gueten zgreši vzorec gut)", "confidence": "?"},
    {"id": "EINHART", "values": ["Einhart mit Gypfel &c.", "Einhart mit Gypf. &c."],
     "hypothesisSi": "morda Einöd-Hart (Hart = gozd/pašnik na trdem terenu) + Gipfel — NE dokazano", "confidence": "?"},
    {"id": "DINGF", "values": ["Dingf"], "hypothesisSi": "morda Dingfeld? — mešana so-odvisnost (TRAVNIK 9/NJIVA 4/ALM 4) — NE dokazano", "confidence": "?"},
    {"id": "LUKIG", "values": ["Lukig"], "hypothesisSi": "morda Luch/Lukig = mokrišče (Loch) — NE dokazano", "confidence": "?"},
    {"id": "LOHGARN", "values": ["Lohgarn"], "hypothesisSi": "Loh + garn? — NE dokazano", "confidence": "?"},
    {"id": "HURGI", "values": ["Hurgi"], "hypothesisSi": "neznano", "confidence": "?"},
    {"id": "WING", "values": ["Wing"], "hypothesisSi": "morda Wingert (vinograd, zahodnoavstrijsko) — v Kärntenu netipično — NE dokazano", "confidence": "?"},
    {"id": "EINSCHLAG-GUELZE", "values": ["Einschlag mit Gülze", "Einschicht mit Poggi u. Bau",
                                          "Einschicht mit Gfretzgen bau", "Gülze", "Gülze mit Gülze"],
     "hypothesisSi": "Einschlag = ograda/obor?; Gülze = Gülte?/krma?; 'Einschlag mit Frucht und Gülze' "
                     "(3 pari) → v2 NJIVA prek formanta Frucht, zato NI v tej družini; ostalo NE dokazano; "
                     "Einschlag~Einschicht = verjetno isti termin (OCR)",
     "confidence": "?"},
    {"id": "SCHINDEL", "values": ["Schindel"],
     "hypothesisSi": "'Schindel baum' (5 parov) → v2 GOZD prek formanta baum; samostojna 'Schindel' ostaja neznan (skodla/les?)", "confidence": "?"},
    {"id": "OSTALI-SAMOSTOJNI", "values": [],  # izpolni skript (vsak v danes neznani vrednosti brez družine)
     "hypothesisSi": "samostojne neznane vrednosti (1–4 pari) — čakajo na paleografijo", "confidence": "?"},
]

KNOWN_FAMILY_VALUES = {v for f in FAMILIES for v in f["values"]}


def main() -> None:
    data = json.loads(BASIS.read_text(encoding="utf-8"))
    parcels = data["parcels"]
    totals39 = data["totals"]

    # ——— 1. para = (parcela, surova raba); v1 rekonstrukcija + regresija ———
    v1_mismatch = 0
    pair_list = []  # (key, section, raw, rows, v1classes, stored_primary)
    for p in parcels:
        seen = set()
        for c in p["cultures"]:
            raw = c["raw"]
            dup = raw in seen
            if not dup:
                seen.add(raw)
                recomputed = classes_for(raw, V1_RULES)
                stored = c.get("classes") or []
                if recomputed != stored:
                    v1_mismatch += 1
                pair_list.append((p["key"], p["section"], raw, c.get("rows", 1),
                                  recomputed, c.get("primary")))
    assert v1_mismatch == 0, f"v1 rekonstrukcija: {v1_mismatch} neskladij s P39 shranjenim"
    assert len(pair_list) == totals39["parcelCulturePairs"] == 2632, "število parov != 2632"

    # v1 statistika po parih (regresija do cultureClasses v P39)
    v1_primary_counts = Counter(prim for *_x, prim in pair_list if prim)
    stored_counts = data["cultureClasses"]["primaryCounts"]
    assert dict(v1_primary_counts) == stored_counts, "v1 primaryCounts se ne ujemajo s P39"

    # ——— 2. priložena pravila: KONČNE dodelitve (first-match-wins) ———
    # Najprej izračunaj v2 razred po vrednosti, potem dodeli par pravilu, ki je
    # prvo ujemanje v skupnem vrstnem redu (v1 1–12 → priložena 13–25).
    all_rules = V1_RULES + [(r[0], r[1]) for r in V2_RULES]

    def v2_for(raw: str):
        """(classes, primary, ruleNo) — first-match-wins nad vsemi pravili."""
        n = norm(raw)
        for i, (cls, pat) in enumerate(all_rules, start=1):
            if re.search(pat, n):
                return cls, i
        return None, None

    appended_claimed = {idx: {"class": cls, "pattern": pat, "confidence": conf,
                              "noteSi": note, "values": {}}
                        for idx, (cls, pat, conf, note) in enumerate(V2_RULES, start=13)}
    for key, section, raw, rows, v1cls, _prim in pair_list:
        if v1cls:
            continue  # v1 pravilo je že odločilo — priložena pravila ne pridejo na vrsto
        cls, rule_no = v2_for(raw)
        if cls and rule_no > 12:
            m = appended_claimed[rule_no]["values"].setdefault(raw, {"pairs": 0, "rows": 0})
            m["pairs"] += 1
            m["rows"] += rows

    appended = []
    for idx in sorted(appended_claimed):
        a = appended_claimed[idx]
        vals = {r: m for r, m in sorted(a["values"].items(), key=lambda kv: (-kv[1]["pairs"], kv[0]))}
        appended.append({
            "no": idx, "class": a["class"], "labelSi": RULE_LABELS_SI[a["class"]],
            "pattern": a["pattern"], "confidence": a["confidence"], "noteSi": a["noteSi"],
            "claimedRaw": vals,
            "pairs": sum(m["pairs"] for m in vals.values()),
            "rows": sum(m["rows"] for m in vals.values()),
        })

    # ——— 3. v2 resolucija po vrednosti ———
    raw_stats = defaultdict(lambda: {"pairs": 0, "rows": 0, "sections": Counter()})
    for key, section, raw, rows, v1cls, prim in pair_list:
        s = raw_stats[raw]
        s["pairs"] += 1
        s["rows"] += rows
        s["sections"][section] += 1

    toponym_map = {raw: (formant, conf, note) for raw, formant, conf, note in TOPONYM_LIST}
    artifakt_map = {raw: (reason, conf) for raw, reason, conf in ARTIFAKT_LIST}

    value_rows = []
    for raw, s in raw_stats.items():
        v1cls = classes_for(raw, V1_RULES)
        v2prim, v2rule = v2_for(raw) if not v1cls else (v1cls[0], None)
        v2cls = ([v2prim] if v2prim else []) if not v1cls else v1cls
        # v2 ⊇ v1 garantirano s strukturo (v1 pravila prej, ista mesta); preveri:
        if v1cls:
            assert v2cls == v1cls, f"v1 primarna se je spremenila: {raw}"
        prim = v2prim
        rule_no = v2rule
        if v2cls:
            term_type = "KULTURA"
            note = None
            conf = "~"
        elif raw in toponym_map:
            term_type = "TOPONIM"
            formant, conf, note = toponym_map[raw]
            assert formant, raw
        elif raw in artifakt_map:
            term_type = "ARTIFAKT"
            note, conf = artifakt_map[raw]
        elif re.fullmatch(r"\d+", raw):
            term_type = "ARTIFAKT"
            note = "številka namesto rabe (Blatt X register / lokacijska št.)"
            conf = "~"
        else:
            term_type = "NEKLASIFICIRANO"
            note = None
            conf = None
        value_rows.append({
            "raw": raw, "norm": norm(raw), "pairs": s["pairs"], "rows": s["rows"],
            "sections": dict(s["sections"].most_common()),
            "v1Classes": v1cls, "v2Classes": v2cls, "v2Primary": prim,
            "v2RuleNo": rule_no, "termType": term_type, "confidence": conf,
            "noteSi": note,
        })

    # ——— 4. invarianta: seznami ⊥ pravila, ⊥ med seboj, obstoj ———
    for raw, *_x in TOPONYM_LIST:
        assert raw in raw_stats, f"TOPONIM vrednost ne obstaja: {raw!r}"
        assert not classes_for(raw, all_rules), f"TOPONIM bi ga ujelo pravilo: {raw!r}"
    for raw, *_x in ARTIFAKT_LIST:
        assert raw in raw_stats, f"ARTIFAKT vrednost ne obstaja: {raw!r}"
        assert not classes_for(raw, all_rules), f"ARTIFAKT bi jo ujelo pravilo: {raw!r}"
        assert raw not in toponym_map, f"ARTIFAKT ∩ TOPONIM: {raw!r}"
    for f in FAMILIES:
        for v in f["values"]:
            assert v in raw_stats, f"družinska vrednost ne obstaja: {v!r}"
            assert not classes_for(v, all_rules), f"družinska vrednost ujeta s pravilom: {v!r}"
            assert v not in toponym_map and v not in artifakt_map, f"družina ∩ seznami: {v!r}"

    # ——— 5. statistika po parih ———
    tt_pairs = Counter()
    tt_rows = Counter()
    v2_primary_counts = Counter()
    new_by_class = Counter()
    for v in value_rows:
        tt_pairs[v["termType"]] += v["pairs"]
        tt_rows[v["termType"]] += v["rows"]
        if v["v2Primary"]:
            v2_primary_counts[v["v2Primary"]] += v["pairs"]
            if not v["v1Classes"]:
                new_by_class[v["v2Primary"]] += v["pairs"]

    assert sum(tt_pairs.values()) == 2632, "vsota termType parov != 2632"
    v1_classified = tt_pairs["KULTURA"] - sum(new_by_class.values())
    assert v1_classified == data["cultureClasses"]["classifiedPairs"] == 1896, "v1 klasificirani pari != 1896"
    appended_claimed_pairs = sum(a["pairs"] for a in appended)
    assert appended_claimed_pairs == sum(new_by_class.values()), (
        f"vsota dodelitev priloženih pravil {appended_claimed_pairs} != novi pari {sum(new_by_class.values())}")

    # družine ostajajo NEKLASIFICIRANE (pinano)
    fam_pairs = {}
    for f in FAMILIES:
        n = sum(raw_stats[v]["pairs"] for v in f["values"])
        fam_pairs[f["id"]] = n
    for fid, n in fam_pairs.items():
        assert n >= 0

    # ——— 6. so-odvisnostni dokazi za dvoumne družine ———
    # (a) isti parcel: primarne rabe drugih rab na parcelah z vrednostjo V
    # (b) isti lastnik: primarne rabe na drugih parcelah skupnega lastnika
    owner_index = defaultdict(set)   # owner -> {parcelKey}
    parcel_prim = {}                 # parcelKey -> Counter(primarne)
    for p in parcels:
        prims = Counter()
        seen = set()
        for c in p["cultures"]:
            if c["raw"] in seen:
                continue
            seen.add(c["raw"])
            if c.get("primary"):
                prims[c["primary"]] += 1
        parcel_prim[p["key"]] = prims
        for o in p.get("owner") or []:
            owner_index[o].add(p["key"])

    def cooccurrence(values):
        co_parcel = Counter()
        co_owner = Counter()
        for p in parcels:
            raws_here = {c["raw"] for c in p["cultures"]}
            if not (set(values) & raws_here):
                continue
            for cls_, n in parcel_prim[p["key"]].items():
                co_parcel[cls_] += n
        for p in parcels:
            raws_here = {c["raw"] for c in p["cultures"]}
            if not (set(values) & raws_here):
                continue
            linked = set()
            for o in p.get("owner") or []:
                linked |= owner_index.get(o, set())
            linked.discard(p["key"])
            for k in linked:
                for cls_, n in parcel_prim[k].items():
                    co_owner[cls_] += n
        return co_parcel, co_owner

    family_evidence = []
    for f in FAMILIES:
        if not f["values"]:
            continue
        co_parcel, co_owner = cooccurrence(f["values"])
        family_evidence.append({
            "id": f["id"], "values": f["values"],
            "pairs": fam_pairs[f["id"]],
            "hypothesisSi": f["hypothesisSi"], "confidence": f["confidence"],
            "verdict": "NEKLASIFICIRANO (čaka paleografijo)",
            "coParcel": dict(co_parcel.most_common(6)),
            "coOwner": dict(co_owner.most_common(6)),
        })

    # samostojne neznane vrednosti (brez družine, brez termType kulture)
    numeric_raws = {r for r in raw_stats if re.fullmatch(r"\d+", r)}
    resolved_or_family = (set(toponym_map) | set(artifakt_map) | numeric_raws
                          | KNOWN_FAMILY_VALUES)
    singles = sorted(
        (raw for raw, s in raw_stats.items()
         if not classes_for(raw, all_rules) and raw not in resolved_or_family),
        key=lambda r: (-raw_stats[r]["pairs"], r),
    )
    singles_table = [{"raw": r, "pairs": raw_stats[r]["pairs"], "rows": raw_stats[r]["rows"]}
                     for r in singles]
    # vsi NEKLASIFICIRANI pari morajo biti pokriti z družinami ali singles
    uncls_pairs_check = sum(raw_stats[r]["pairs"] for r in singles) + sum(
        fam_pairs[f["id"]] for f in FAMILIES)
    assert uncls_pairs_check == tt_pairs["NEKLASIFICIRANO"], (
        f"družine+singles {uncls_pairs_check} != NEKLASIFICIRANO {tt_pairs['NEKLASIFICIRANO']}")

    # ——— 7. izpis ———
    pairs_total = 2632
    stats = {
        "pairsTotal": pairs_total,
        "v1ClassifiedPairs": v1_classified,
        "v2ClassifiedPairs": tt_pairs["KULTURA"],
        "toponymPairs": tt_pairs["TOPONIM"],
        "artifaktPairs": tt_pairs["ARTIFAKT"],
        "unresolvedPairs": tt_pairs["NEKLASIFICIRANO"],
        "classifiedPctV1": round(100 * v1_classified / pairs_total, 1),
        "classifiedPctV2": round(100 * tt_pairs["KULTURA"] / pairs_total, 1),
        "explainedPctV2": round(100 * (pairs_total - tt_pairs["NEKLASIFICIRANO"]) / pairs_total, 1),
        "rowsTotalCulture": totals39["cultureRows"],
        "unresolvedRows": tt_rows["NEKLASIFICIRANO"],
        "primaryCountsV2": dict(v2_primary_counts.most_common()),
        "newPairsByClassV2": dict(new_by_class.most_common()),
    }

    out = {
        "series": "PS",
        "source": "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani)",
        "method": "P42 pravilnik rab v2 — deterministično nad P39 modelom (committed dokaz), "
                  "brez AI ob delovanju; v1 pravila nespremenjena + 13 priloženih pravil; "
                  "izrecna ločitev KULTURA / TOPONIM / ARTIFAKT / NEKLASIFICIRANO; "
                  "surove vrednosti nedotaknjene; vsi statusi ostajajo REVIEW",
        "basis": {"json": "src/data/atlas/ps-landuse.json", "phase": "P39",
                  "generatedBy": data.get("generatedBy"),
                  "generatedAt": data.get("generatedAt")},
        "readingRule": data.get("readingRule"),
        "countScope": "štetje po PARIH parcela×raba (podvojene rabe znotraj parcele enkrat) — kot P39",
        "rulebook": {
            "version": "v2",
            "noteSi": "prvi zadetek v skupnem vrstnem redu (v1 1–12 → priložena 13–25) = primarni "
                      "razred; termType izrecno ločuje: KULTURA (razred), TOPONIM (ležajno ime, "
                      "ni raba), ARTIFAKT (številka/registrična opomba), NEKLASIFICIRANO (neznan "
                      "termin — ni ugibanj); vsi novi vzorci imajo zaupanje [~] ali [?]",
            "noteEn": "first match in combined rule order (v1 1–12 → appended 13–25) = primary "
                      "class; termType distinguishes KULTURA / TOPONIM / ARTIFAKT / NEKLASIFICIRANO; "
                      "no guessing for unknown terms",
            "v1Rules": [{"no": i, "class": c, "pattern": p}
                        for i, (c, p) in enumerate(V1_RULES, start=1)],
            "appendedRules": appended,
        },
        "stats": stats,
        "termTypes": {
            "KULTURA": {"pairs": tt_pairs["KULTURA"]},
            "TOPONIM": {
                "pairs": tt_pairs["TOPONIM"], "rows": tt_rows["TOPONIM"],
                "distinct": len(toponym_map),
                "values": [{"raw": r, "formant": fm, "confidence": cf, "noteSi": nt,
                            "pairs": raw_stats[r]["pairs"], "rows": raw_stats[r]["rows"]}
                           for r, fm, cf, nt in TOPONYM_LIST],
                "noteSi": "ležajna/terenska imena brez kulturnega termina — NI raba; "
                          "za statistiko uporabe se NE štejejo kot kultura",
            },
            "ARTIFAKT": {
                "pairs": tt_pairs["ARTIFAKT"], "rows": tt_rows["ARTIFAKT"],
                "distinct": sum(1 for v in value_rows if v["termType"] == "ARTIFAKT"),
                "values": [{"raw": r, "reason": rs, "confidence": cf,
                            "pairs": raw_stats[r]["pairs"], "rows": raw_stats[r]["rows"]}
                           for r, rs, cf in ARTIFAKT_LIST],
                "numericRaw": sorted([r for r in raw_stats
                                      if re.fullmatch(r"\d+", r)],
                                     key=lambda x: int(x)),
                "noteSi": "številke (Blatt X register/lokacije), registrične besede "
                          "(Summa, Zahl) in opombe o prihodkih (Futter…) — ne rabe",
            },
            "NEKLASIFICIRANO": {
                "pairs": tt_pairs["NEKLASIFICIRANO"], "rows": tt_rows["NEKLASIFICIRANO"],
                "distinct": len(singles) + sum(1 for f in FAMILIES for v in f["values"]),
                "families": family_evidence,
                "singles": singles_table,
            },
        },
        "values": value_rows,
        "v1Regression": {"checkedPairs": pairs_total, "mismatches": 0,
                         "primaryCounts": dict(v1_primary_counts.most_common())},
        "generatedBy": "scripts/p42_ps_rulebook_v2.py",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
    }

    text = json.dumps(out, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    OUT_EVIDENCE.write_text(text, encoding="utf-8")
    OUT_RUNTIME.write_text(text, encoding="utf-8")
    assert OUT_EVIDENCE.read_text(encoding="utf-8") == OUT_RUNTIME.read_text(encoding="utf-8")

    s = stats
    print(f"P42 OK — pari {s['pairsTotal']}: KULTURA {s['v2ClassifiedPairs']} "
          f"({s['classifiedPctV2']} %; v1 {s['classifiedPctV1']} %) · "
          f"TOPONIM {s['toponymPairs']} · ARTIFAKT {s['artifaktPairs']} · "
          f"NEKLASIFICIRANO {s['unresolvedPairs']} ({s['unresolvedRows']} vrstic) · "
          f"pojasnjeno {s['explainedPctV2']} %")
    print("nove rabe po razredih:", s["newPairsByClassV2"])
    print("družine:", {k: v for k, v in fam_pairs.items() if v})


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
