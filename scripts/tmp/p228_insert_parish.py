#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P228 — vstavi 16-GRIBLJE-blokov (krstna 04104, leto 1878 = 8/15!) v parish.ts PRED P227-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P227: krstna PREDZGODOVINA 04104, leto 1879"

E = json.load(open("/tmp/p228/entries_1878.json"))
grib = E["griblje_entries"]
assert len(grib) == 16, f"grib={len(grib)}"

P228_HDR = "  // ——— P228: krstna PREDZGODOVINA 04104, leto 1878"
if P228_HDR in src:
    i = src.index(P228_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P228-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}
MESEC_MAP = {"Jänner": "J", "Feber": "F", "Februar": "F", "März": "M", "April": "A", "Mai": "M2", "Juni": "J2", "Juli": "J3", "August": "A2", "September": "S", "October": "O", "November": "N", "December": "D", "Dezember": "D"}

KOM = {
 "z23": "★★★ PEZDIRC-matec-nit (1/6!) + ★★★ črnilo-pripis-'por. 18/11 1920-† 12.5.1939' + DOVGAN + h73 (z31-h43-RAZLIČNI!)",
 "z24": "★★★ TRETJI-DUHOVNIK-'…binant-Kroggj[?]-coop'-garble (trojna-izmenjava!) + rojen≠krsten-4/5",
 "z27": "★★★ MILEK-oče-nit + DOVGAN + h29",
 "z28": "★★★ TODTGEBOREN-GRIBLJE (garble-'Nrbžgabumšt'≈'nichtlebendgeburt'-X-open!) + botra+duhovnik-PRAZNI! + h11-×2",
 "z29": "★★★ DRAGOŠ-matec + SIMEC-botra + h11-×2 (z28!) + DOVGAN",
 "z30": "★★★ JAKOFČIČ-DVOJNI-botra-nit (×2-v-vrstici!) + rojen≠krsten-28/29 + DOVGAN + h1",
 "z31": "★★★ MODRI-PRIPIS-'† 18.6.1955-št 43'-MATCH-h43! + h43 (z23-h73!) + Mai-start + DOVGAN",
 "z45": "★★★ SIMEC-oče-KOMPLET (2/2!) + ★★★ PEZDIRC-matec-nit (2/6!) + JANIČAR-coop (1/3!) + h55 (z56-h53!)",
 "z46": "★★★ PEZDIRC-DVOJNI-vrstica (oče-X-open + boter!) + ★★★ DATUMSKA-KOREKCIJA ('Juni 30'-prečrtan→'Juli 1'!) + h64-×2-DUEL (z81-identični-glifyi!-64/69-X-open!) + DOVGAN",
 "z52": "★★★ MODRI-PRIPIS-'† 18.3.1959-v-Gribljah-št 18'-MATCH-h18! + DRAGOŠ+KLOBUČAR-boter-X-open + JANIČAR-coop (2/3!)",
 "z53": "★★★ PEZDIRC-matec-nit (3/6!) + BRODARIČ-boter + DOVGAN + h48",
 "z56": "★★★ PEZDIRC-oče+matec-garble-X-open (4/6!) + BRODARIČ+DRAGOŠ-botra-KOMPLET + rojen≠krsten-19/20 + DOVGAN + h53 (z45-h55!)",
 "z64": "★★★ HURE-boter-nit (P227-PARALELA!) + ★★★ črnilo-pripis-dolg-'poročen-27/9-974[?]' + rojen≠krsten-28/29 + DOVGAN + h77",
 "z65": "★★★ NEZAKONSKI-GRIBLJE (očetov-stolpec-PRAZEN!-P227-z23-PARALELA!-×5-linije!) + ★★★ črnilo-pripis-'um 16 Novr 880[?]' + DOVGAN + h6 + Oktobar-start",
 "z69": "★★★ SIMEC-oče-KOMPLET (2/2!) + DRAGOŠ-botra-KOMPLET (3/3!) + ★★★ črnilo-pripis-'† 31.10.1931' + DOVGAN + h38",
 "z81": "★★★ PEZDIRC-DVOJNI-vrstica (matec+boter!-5/6!-JAKOFČIČ-oče!) + h64-×2-DUEL (z46!) + JANIČAR-coop (3/3!) + Dezember-blok + s105-DUPLIKAT-SKEN!",
}

def esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')

def clean_day(d):
    d = str(d or "").strip().rstrip(".")
    d = d.split()[0] if d else "?"
    return d if d else "?"

def gen_block(e):
    z = e["z"]
    sk = e["sken"]
    pag = e["pag"].split()[0]
    m = MESEC_MAP[e["mesec"]]
    mesec_si_num = MESEC_SI[m]
    mesec_en = MESEC_EN[m]
    rojen = clean_day(e["rojen"])
    krsten = clean_day(e["krsten"])
    hisna = esc(e["hisna"])
    kom = esc(KOM[z])
    what_si = (f"krščena {esc(e['otrok'])} ({rojen}./{krsten}. {mesec_si_num}.) — oče {esc(e['ocec'])}, mati {esc(e['matec'])}; "
               f"botra {esc(e['botra'])}; + {kom} + pag-konvencija-sken−5 + [z{z[1:]}]")
    what_en = (f"baptized {esc(e['otrok'])} ({mesec_en} {rojen}/{krsten}) — father {esc(e['ocec'])}, mother {esc(e['matec'])}; "
               f"godparents {esc(e['botra'])}; + [see-SI] + [z{z[1:]}]")
    return (
        "  {\n"
        f'    houseNo: "{e["hisna"].split()[0]}",\n'
        '    bookSignature: "04104",\n'
        "    year: 1878,\n"
        f"    scan: {sk},\n"
        f"    page: {pag},\n"
        f'    whatSi: "{what_si}",\n'
        f'    whatEn: "{what_en}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

P228_HEADER = (
    "  // ——— P228: krstna PREDZGODOVINA 04104, leto 1878 = 8/15 — (s92–s106 == gola-svinčna-pag-'sken−5' "
    "(13/14-SEKVENČNO: s92='87'/s93='88'/s94='89'/s95='90'/s96='91'/s97='92'/s98='93'-LEAD-'93'-NA-s98-NE-s99!"
    "/s99-TEMNA-'34'-ANOMALIA-LUKNJA-'94'!/s100='95'/s101='96'/s102='97'/s103='98'/s104='99' + s105='99'-"
    "DUPLIKAT-SKEN (≡s104-1:1!-LEPLJENEC-1908!)-→ s106='100'-'sken−6'-P227/P226-konvencija = ARTEFAKT-DUPLIKATA-s105-"
    "RAZLAGA-NAJDENA!; 2×-neodvisna-prenosa-md5-15/15!); ★★★ MEJA-1877/78-s92/s93 (TAIL-1877-Dezember + glava-'Jahr 1877'-"
    "BREZ-VSOTNE/velikih-cifer-P225-TIP! + RESTART-z1-NA-DAN-[8↔9]-JÄNNER-DUEL-Geburt-'9'/Taufe-'8'-OBRNJENO-X-open!-"
    "Boginja-vas-h14-Margareth-MODRI-dolg-†6.12.1959!-mesec-'Jänner'-PREČRTAN!-8.-restart-z1-NAJPONEJŠI-SE-ZLOMIL!"
    "-P221-1.1!-P222-1.1!-P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!-P227-8./9.!-P228-[8↔9]-DUEL!) = 67.-POTRDITEV-invariante! (66.-P227!); "
    "94-vpisov-DISTINCT — vrstna-aritmetika 7+6+7+7+6+8+8+7+8+8+7+10+5 = 94 = P227-LEAD-'1878-=-94-vpisov-pričakovano'-1:1-INVARIANTA! "
    "(zap-stolpci-15/15-ČISTO!); ★★★ 16-GRIBLJE / 14-hiš (h11-×2: z28+z29! + h64-×2: z46+z81!-identični-glifyi-64/69-DUEL-X-open!-"
    "z23-h73!-z31-h43!-z45-h55!-z56-h53!-DUELI-RAZREŠENI-Kurrent-7/4-5/3!) "
    "+ ★★★ PEZDIRC-×17-vrstic-NOV-REKORD-LINJE (z46-DVOJNI! + z81-DVOJNI! + ×4-matec-Griblje + ×2-oče-Griblje + ×11-ne-Griblje!) — "
    "grafija-continuum-8-let: ×4/×4/×6/×4/×9/×14/×12/×17! + SIMEC-×3-KOMPLET + DRAGOŠ-×4 (3/3-KOMPLET!) + JAKOFČIČ-×5 "
    "(z30-DVOJNI-botra!) + BRODARIČ-×2 + MILEK-×2 + HURE-×1 (z64!-P227-PARALELA!) + KLOBUČAR-×1-X-open + "
    "★★★ DUHOVNIŠKA-TROJNA-IZMENJAVA-1878 ('…binant-Kroggj[?]-coop'-garble ↔ 'Franz-Dovgan' ↔ 'Franz-Janičar-coop'-3-PODPISA!-"
    "vs-×2-1879/1880!-Kroggj-z1–z26-alternacija-z-Dovganom!-Janičar-vstopi-z35!-Griblje-split-DOVGAN-×10/JANIČAR-×3/KROGGJ-×1/PRAZNA-×1!) "
    "+ ★★★ z28-TODTGEBOREN-GRIBLJE (garble-'Nrbžgabumšt'≈'nichtlebendgeburt'/'Notgeburt'-X-open!-botra+duhovnik-VSI-PRAZNI!-1.-v-GRIBLJI!) "
    "+ ★★★ z65-NEZAKONSKI-GRIBLJE (očetov-stolpec-PRAZEN!-×5-linije!) + ★★★ DVOJČKI-×2 (z17/z18-Krasinec-h43-bracket! + z87/z88-Bajukh-squiggle-+Agnes-Bajukh-PREČRTANA!) "
    "+ ★★★ MODRI-×12+-REKORD (×2-MATCH-hišam: z31-h43! + z52-h18!) + ★★★ ČRNILO-pripisi-×4-Griblje (z23-por-†! + z64-poročen! + z65-um! + z69-†!) "
    "+ ★★★ POPRAVKI-×5 (z87-VAS-'Nicolaus'-✗✗→'Primostek'! + z88-'Gerag[?]'-X-open + z46-DATUMSKA-'Juni-30'→'Juli-1'! + z1-MESEC-PREČRTAN! + z4-OČE-PREČRTAN!) "
    "+ z1-RESTART-DATUMSKI-DUEL (Geburt-'9'/Taufe-'8'-OBRNJENO!) + s105-LEPLJENEC-1908 (Danijel-Barle!-PEČAT!) + HEBAMME-Maria-Rom/Born-×8-continuum! "
    "+ meseci-Griblje: A6+Mai1+Aug1+Juli2+S3+O2+D1 (Jänner/Feber/März-×0!) ———\n"
)

blocks = P228_HEADER
for e in grib:
    blocks += gen_block(e)

i = src.index(ANCHOR)
src = src[:i] + blocks + src[i:]
TS.write_text(src, encoding="utf-8")
print(f"vstavljenih-blokov: {len(grib)} (PRED P227-anchor)")
