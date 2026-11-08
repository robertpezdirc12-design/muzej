#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P229 — vstavi 20-GRIBLJE-blokov (krstna 04104, leto 1877 = 9/15!) v parish.ts PRED P228-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P228: krstna PREDZGODOVINA 04104, leto 1878"

E = json.load(open("/tmp/p229/entries_1877.json"))
grib = E["griblje_entries"]
assert len(grib) == 20, f"grib={len(grib)}"

P229_HDR = "  // ——— P229: krstna PREDZGODOVINA 04104, leto 1877"
if P229_HDR in src:
    i = src.index(P229_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P229-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}
MESEC_MAP = {"Jänner": "J", "Feber": "F", "Februar": "F", "März": "M", "April": "A", "Mai": "M2", "Juni": "J2", "Juli": "J3", "August": "A2", "September": "S", "October": "O", "November": "N", "December": "D", "Dezember": "D"}

KOM = {
 "z8": "★★★ PEZDIRC-DVOJNI-vrstica (oče+botra!) + MILEK-boter + ★★★ MODRI-MATCH-h37-'umrla-21.4.1961-št.37!' + Roggja-DUEL + ★★★ MEJA-1876/77-s78-ENE-STRANI-68.-POTRDITEV-invariante! (Incipit-annus-Domini-1877-KALLIGRAFIJA! + RESTART-z1-9./10.-JÄNNER!-9.-restart!)",
 "z13": "★★★ JAKOFČIČ-oče + ★★★ MODRI-dolg-'†27.1.1963-v-Gribljah'+'o.23/1.1910' + h6-×2 (z56!)",
 "z15": "★★★ JAKOFČIČ-oče + PEZDIRC-boter + HRIŽAN-matec + ★★★ DATUMSKI-DUEL-Feb28→Mar1 (ČEZ-MESEC!-1877-NON-LEAP!)",
 "z22": "★★★ PREČRTANA-VRSTICA-GRIBLJE (veliki-X-črnilo!) + OČE-PREČRTAN-SWAP-'Samuel-Štua' + SIMEC-matec + BRODARIČ-boter + MODRI-'†20.I.1912' + Roggja-DUEL",
 "z25": "★★★ MILEK-oče + PEZDIRC-boter + rojen≠krsten-29/30 + DOVGAN",
 "z34": "★★★ HAMBIČ-oče + BRODARIČ-boter + MILEK-boter + BRINC-matec + Hoggja-DUEL",
 "z56": "★★★ KLOBUČAR-oče + MILEK-matec + JAKOFČIČ-boter + ★★★ črnilo-'†30.4.19?0-v-Gribljah'-X-open + h6-×2 (z13!)",
 "z61": "★★★ SIMEC-boter (2/3!) + DOVGAN + h7 (P228-izjema-nit-continuum-11-let!)",
 "z67": "★★★ DVOJČKI-×1-GRIBLJE (bracket-'Zwillings'-nota!) + PEZDIRC-oče + BRINC-matec + JAKOFČIČ+HAMBIČ-botra + rojen≠krsten-31/1",
 "z68": "★★★ DVOJČKI-×1-GRIBLJE (z67-zaverižani-isti-starši+botra!) + PEZDIRC-oče + h14-×2",
 "z77": "★★★ JAKOFČIČ-matec + KLOBUČAR-boter + rojen≠krsten-5/6 + DOVGAN + h2 + Oktobar-start",
 "z79": "★★★ HRIŽAN-oče + DOVGAN + h35 (z101-h34-RAZLIČNI!)",
 "z84": "★★★ PEZDIRC-oče + DEBLIČ-matec + BRODARIČ+MILEK-botra + rojen≠krsten-22/23 + November-start",
 "z85": "★★★ JAKOFČIČ-DVOJNI-vrstica (oče+matec!) + DRAGOŠ-boter (continuum!) + rojen≠krsten-23/24",
 "z89": "★★★ November-31-DUEL-×1-GRIBLJE (Nov-31-NE-OBSTAJA!→Dec-1!-z90-PARALELA-×2!) + PEZDIRC-oče-X-open + JAKOFČIČ-matec + DEBLIČ+KLOBUČAR-botra",
 "z94": "★★★ BRODARIČ-oče + ★★★ črnilo-'†6.3.1945'-s-križem (P228-z87-†6.4.1945-PARALELA!) + HUSIČ-botra + h49-DUEL (49/40!)",
 "z95": "★★★ BRODARIČ+KLOBUČAR-botra + oče-garble-MAX-'Levac/Lezar'-X-open",
 "z99": "★★★ HRIŽAN-DVOJNI-vrstica (oče+matec!) + SIMEC-boter (3/3-KOMPLET!) + DOVGAN + h3",
 "z101": "★★★ DEBLIČ-matec + oče-garble-MAX + botra-garble-×2-MAX + h34-DUEL (34/84/94!)",
 "z106": "★★★ DEBLIČ-oče + HUSIČ-matec + BRODARIČ-boter (6/6-KOMPLET!) + PEZDIRC-boter (P228-TAIL-1:1-KRIŽ!) + h33",
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
        "    year: 1877,\n"
        f"    scan: {sk},\n"
        f"    page: {pag},\n"
        f'    whatSi: "{what_si}",\n'
        f'    whatEn: "{what_en}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

P229_HEADER = (
    "  // ——— P229: krstna PREDZGODOVINA 04104, leto 1877 = 9/15 — (s78–s92 == gola-svinčna-pag-'sken−5' "
    "(15/15-SEKVENČNO: s78='73'/s79='74'/s80='75'/s81='76'/s82='77'/s83='78'/s84='79'/s85='80'-LEAD-PREDIKCIJA-POTRJENA!"
    "/s86='81'/s87='82'/s88='83'/s89='84'/s90='85'/s91='86'/s92='87'-P228!; 2×-neodvisna-prenosa-md5-15/15!); "
    "★★★ MEJA-1876/77-s78-ENE-STRANI (TAIL-1876-Dobravce-Martin-Dez-24/26-h16 + glava-'Jahr 1876'! + 'Incipit-annus-Domini-1877'-"
    "VELIKA-KALLIGRAFIJA-ČEZ-SREDINO-STRANI-1.-INCIPIT-v-krstni-liniji! + glava-'Jahr 1877-Jänner' + RESTART-z1-NA-DAN-9./10.-JÄNNER-"
    "Zemelj-h20-Catharina-Škatab[?]/Jurejčič[?]-DUEL!-9.-restart-z1!-P221-1.1!-P222-1.1!-P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!-P227-8./9.!-P228-[8↔9]-DUEL!) "
    "= 68.-POTRDITEV-invariante! (67.-P228!); "
    "★★★ 108-VPISOV-DISTINCT — LEAD-KOREKCIJA-9.×-linija (P228-LEAD-'1877-=91'-NAPAČNA!-predpostavka-tail-'z86–z91'!) — "
    "vrstna-aritmetika 5+7+8+9+7+8+9+7+8+8+7+6+7+6+6 = 108 + zap-stolpci-VIDNI-×6-strani-1:1 (s78:1–5!-s79:6–12!-s80:13–20!-s81:21–29!-s82:30–36!-s83:37–44!) "
    "= NOV-REKORD-POTRDITEV-zap-1:1!; "
    "★★★ 20-GRIBLJE / 18-hiš (h6-×2: z13+z56! + h14-×2: z67+z68-DVOJČKI-bracket!-h37-h13-h36-h65-h74-h7-h2-h35-h20-h9-h40-h49-DUEL-h78-h3-h34-DUEL-h33!) "
    "+ ★★★ PEZDIRC-×11-vrstic-continuum-9-let (z8-DVOJNI-Griblje!-×7-Griblje + ×4-ne-Griblje!) — grafija-continuum-9-let: ×4/×4/×6/×4/×9/×14/×12/×17/×11! "
    "+ JAKOFČIČ-×11 (z85-DVOJNI!-z31-TRIJNI-neG!) + MILEK-×5-vse-Griblje-KOMPLET + BRODARIČ-×6-Griblje-KOMPLET (z94-oče!) + KLOBUČAR-×4 + DEBLIČ-×4 + HRIŽAN-×5 (z99-DVOJNI!) "
    "+ SIMEC-×3-KOMPLET + DRAGOŠ-×1 + HURE-×2-neG + HAMBIČ-×4 + "
    "★★★ DVOJČKI-×4-REKORD-LINJE (z28/z29-Prilozje-h30! + z46/z47-Grem-h26! + z67/z68-GRIBLJE-h14-'Zwillings'-nota! + z75/z76-Krasine-h18-†11.3.1939-ink!-vs-×3-P227!) "
    "+ ★★★ TODTGEBOREN-TIP-garble-×3-REKORD (z41-'Nurlygaburišt'-Krasine-h11! + z42-'Tuolynbuns'-Podzemelj-hišna-PRAZNA! + z65-'Nurlygabuništ'-Kloster-h43!-P228-z28-'Nrbžgabumšt'-PARALELA!) "
    "+ ★★★ NEZAKONSKI-×4 (z38-Krasine-h46-dash! + z43-Certovišče-h14! + z44-Vranoviče-h20-X-open!) "
    "+ ★★★ DUHOVNIŠKA-IZMENJAVA-1877 ('Ferdinand-Hoggin/Hoggja/Roggja-coop'-KURRENT-DUEL-podpis-DOMINANTA! ↔ 'Franz-Dovgan'-ALTERNIRAJÖČE!-Griblje-split-HOGGIN-×13/DOVGAN-×7!) "
    "+ ★★★ November-31-DUEL-×2 (z89-GRIBLJE! + z90-Dragoše!-Nov-31-NE-OBSTAJA!) + ★★★ RETRO-VPISI-×2 (z97/z98-Nov-29/30-NA-s91-PO-Dec-28/29!) "
    "+ ★★★ z22-PREČRTANA-VRSTICA-GRIBLJE (veliki-X-črnilo! + OČE-SWAP-'Samuel-Štua'!) + ★★★ z15-DATUMSKI-DUEL-Feb28→Mar1-GRIBLJE! "
    "+ ★★★ MODRI-×9 (z8-MATCH-h37! + z13-†27.1.1963! + z27-TORONTO-KANADA! + z40-dolg-†6.12.1960! + z43-DUEL-1943/1953! + z18-MMK-Otok-1964!) "
    "+ ★★★ črnilo-×2-Griblje (z56-†30.4.19?0! + z94-†6.3.1945-P228-z87-PARALELA!) + HEBAMME-Maria-Rom/Born-×7-continuum! "
    "+ meseci-Griblje: J1+F3+M2+A1+Juli1+A3+O2+N3+D5 (Juni/Sep-×0!) ———\n"
)

blocks = P229_HEADER
for e in grib:
    blocks += gen_block(e)

i = src.index(ANCHOR)
src = src[:i] + blocks + src[i:]
TS.write_text(src, encoding="utf-8")
print(f"vstavljenih-blokov: {len(grib)} (PRED P228-anchor)")
