#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P230 — vstavi 14-GRIBLJE-blokov (krstna 04104, leto 1876 = 10/15!) v parish.ts PRED P229-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P229: krstna PREDZGODOVINA 04104, leto 1877"

E = json.load(open("/tmp/p230/entries_1876.json"))
grib = E["griblje_entries"]
assert len(grib) == 14, f"grib={len(grib)}"

P230_HDR = "  // ——— P230: krstna PREDZGODOVINA 04104, leto 1876"
if P230_HDR in src:
    i = src.index(P230_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P230-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}
MESEC_MAP = {"Jänner": "J", "Feber": "F", "Februar": "F", "März": "M", "April": "A", "Mai": "M2", "Juni": "J2", "Juli": "J3", "August": "A2", "September": "S", "October": "O", "November": "N", "December": "D", "Dezember": "D", "August[?]-DUEL": "A2"}

KOM = {
 "z22": "★★★ PEZDIRC-oče-garble-X-open + DEBLIČ-boter + KLOBUČAR-botra + ★★★ MEJA-1875/76-s64/s65-DVO-STRANSKA-69.-POTRDITEV (finis-Anni-1875-KALLIGRAFIJA!-RESTART-z1-5./5.-JÄNNER!-10.-restart!) + Hoggia-DUEL + zap-22-VIDEN",
 "z26": "★★★ SIMEC-oče + JAKOFČIČ-matec + BRODARIČ-boter + KLOBUČAR-botra + rojen≠krsten-12/13 + Roggja-DUEL + zap-26-VIDEN",
 "z28": "★★★ PEZDIRC-oče (P229-z84-h20-1:1-PARALELA!) + DEBLIČ-matec + MILEK-boter + BRODARIČ-botra + rojen≠krsten-1/2 + h20-×2-continuum + zap-28-VIDEN",
 "z32": "★★★ HRIŽAN-boter + oče-garble-Šelah-X-open + NEMANIČ-matec + rojen≠krsten-19/20 + h16-continuum + zap-32-VIDEN",
 "z43": "★★★ HRIŽAN-matec + ★★★ HURE-boter (P228-×1-PARALELA!) + ★★★ 'als-Amtsvormund'-botra-NOTA-NOVI-TIP + oče-garble-JETTER + h7-+'až7'-nota + zap-43-VIDEN",
 "z46": "★★★ MUC-oče (P229-z1-PARALELA!) + matec-garble-Jaklič + botra-garble-×2 + DOVGAN + zap-46-VIDEN + h15-continuum",
 "z53": "★★★ MILEK-oče + ★★★ PEZDIRC-matec + BRODARIČ-boter + HUSIČ-botra + ★★★ MESEC-DUEL-X-open ('August[?]-4/4'-vs-'Juli-27/27'!) + ★★★ MODRI-†7.10.1931-črnilo-floret",
 "z85": "★★★ PEZDIRC-DVOJNI-vrstica (oče+boter!) + ★★★ DRAGOŠ-boter + matec-garble-Šerdič + Hoggia-DUEL + September-blok",
 "z86": "★★★ MODRI-'umrl-23.12.1953-n-občin-št.10' + MILEK-boter + BRODARIČ-boter + KRIŽAN-matec + oče-garble-KURE-X-open + DOVGAN + h62-nova-hiša",
 "z88": "★★★ BRINC-oče (P229-z67/z68-matec-PARALELA!) + ★★★ MODRI-†9.12.1935-črnilo + rojen≠krsten-18/19 + oče-garble + botra-garble-×2 + DOVGAN + h25-nova-hiša",
 "z92": "★★★ JAKOFČIČ-oče + BRODARIČ-matec + ★★★ DRAGOŠ-boter (2/2-KOMPLET!) + KLOBUČAR-boter + Hoggia-DUEL + October-blok + h8-continuum",
 "z96": "★★★ SIMEC-oče (2/2-KOMPLET!) + ★★★ PEZDIRC-DVOJNI-vrstica (matec+botra!) + botra-garble-Škranc + DOVGAN + November-blok + h55-continuum",
 "z98": "★★★ KLOBUČAR-DVOJNI-vrstica (matec+botra!) + oče-garble-Hruzelj + botra-garble + Roggja-DUEL + h44-nova-hiša",
 "z94": "★★★ PEZDIRC-matec (7/7-KOMPLET-GRIBLJE!) + ŽUPANIČ-oče+botra-DVOJNI + ★★★ zap-'94'-MODRA + ★★★ MODRI-dolg-'umrl-18.9.1961-v-Suhorju[?]'+por-1914[?] + DOVGAN + h31 + Dezember-blok",
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
        "    year: 1876,\n"
        f"    scan: {sk},\n"
        f"    page: {pag},\n"
        f'    whatSi: "{what_si}",\n'
        f'    whatEn: "{what_en}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

P230_HEADER = (
    "  // ——— P230: krstna PREDZGODOVINA 04104, leto 1876 = 10/15 — (s64–s78 == gola-svinčna-pag-'sken−5' "
    "(15/15-SEKVENČNO: s64='59'-NARISE!/s65='60'-NARISE!/s66='61'/s67='62'/s68='63'/s69='64'/s70='65'/s71='66'-NARISE!"
    "/s72='67'/s73='68'/s74='69'/s75='70'/s76='71'/s77='72'/s78='73'-P229!-3×-VIZUALNO-NARISE!; SKUPNA-SERIJA-59–158-continuum!; 2×-neodvisna-prenosa-md5-15/15!); "
    "★★★ MEJA-1875/76-s64/s65-DVO-STRANSKA-NOVA-VARIANTA (TAIL-1875-×4-vrstic-incl.-GRIBLJE-h11-Anna-Dez-26/26! + glava-'Jahr 1875'! + "
    "'finis-Anni-1875'-VELIKA-KALLIGRAFIJA-'finis'-LEVO-'An-ni-1-8-75'-DESNO-PARALELA-'Incipit-annus-Domini-1877'! | glava-'Jahr 1876'-BREZ-INCIPIT! + "
    "RESTART-z1-NA-DAN-5./5.-JÄNNER-Aloshor[?]-h24-Agnes-Hampauhar[?]/Schweiger!-10.-restart-z1!-P221-1.1!-P222-1.1!-P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!-P227-8./9.!-P228-[8↔9]-DUEL!-P229-9./10.!-P230-5./5.!) "
    "= 69.-POTRDITEV-invariante! (68.-P229!); "
    "★★★ 100-VPISOV-DISTINCT (z1–z100!) — vrstna-aritmetika 7+7+7+8+9+8+8+7+8+8+7+7+8+1 = 100 + zap-stolpci-VIDNI-×6-strani-1:1 "
    "(s65:1–7!-s66:8–14!-s67:15–21!-s68:22–29!-s69:30–38!-s70:39–46!-P229-×6-PARALELA!) + s77-zap-'94'-MODRA! + s78-r1-zap-'100'-X-open!; "
    "★★★ 14-GRIBLJE / 14-hiš-BREZ-DUPLIKATOV (h7-h8-h15-h16-h20-h22-h25-h31-h39-h40-h44-h53-h55-h62!) "
    "+ ★★★ PEZDIRC-×17-vrstic-TIE-REKORD-P228-continuum-10-let (×4/×4/×6/×4/×9/×14/×12/×17/×11/×17!-×2-DVOJNI-GRIBLJE-h53-oče+boter!-h55-matec+botra!-×6-Griblje-vrstic-8-oseb + ×11-ne-Griblje!) "
    "+ JAKOFČIČ-×8 + MILEK-×5 + BRODARIČ-×7 + KLOBUČAR-×5 (z98-DVOJNI!) + HRIŽAN-×6 + SIMEC-×3-KOMPLET + DEBLIČ-×3 + DRAGOŠ-×2-KOMPLET + MUC-×4 + ŽUPANIČ-×2-DVOJNI + HURE-×1 + "
    "★★★ DVOJČKI-×4-dogodki-REKORD-NOVI-VARIANTI (2-BRACE-'Zwillinge': s71-Peter+Michael-Krasine-h25! + s73-Petrus+Maria-Certoviše-h26! + 2-SHARED-ROW: s71-r6-Nicolaus+Martin-'Gri-moršk'! + s69-r9-Anna+Katharina-Goriče-zap-38-ISTI!) "
    "+ ★★★ NEZAKONSKI-×6-REKORD (s66-r6-Krasine-h34! + s72-r3-Zemelj! + s72-r7-Certoviše! + s77-r7-Grem! + s74-r2-Boginja-vas! + s72-r6-'Griže'-WOLFGR!) "
    "+ ★★★ WOLFGR-ANOMALIJA-DRUŽINA-×3-NOVA ('Wolfgrabiff[?]'-s69-r1! + 'Wolfgr-Annišl[?]'-s70-r1! + 'Wolfgr-Daisl[?]'-s72-r6-RETRO!-VSI-botra+duhovnik-PRAZNA!-samo-hebamme!-P229-TODTGEBOREN-GARBLE-DRUŽINA-PARALELA!) "
    "+ ★★★ MODRI-×11-linij-REKORD (Griblje-×4-†: h22-†7.10.1931! + h62-umrl-23.12.1953! + h25-†9.12.1935! + h31-umrl-18.9.1961! + ne-G-×7: CHICAGO-1970! + MMK-Metlika-1962! + MMK-Novo-mesto-1963! + umrl-18.8.1946! + umrl-5.1.1950! + umrla-9.10.1956! + umrla-20.3.1957!) "
    "+ ★★★ 'als-Amtsvormund'-botra-NOTA-NOVI-TIP (z43!) + ★★★ RETRO-VPISI-×2 (s72-r6! + s64-TAIL-r4!) + ★★★ zap-'94'-MODRA (z94-h31!) + HEBAMME-Maria-Rom-×9-continuum + RED-tički-continuum "
    "+ ★★★ DUHOVNIŠKA-IZMENJAVA-1876 ('Hoggia/Roggja/Hoggin-Coop'-KURRENT-DUEL ↔ Franz-Dovgan!-Griblje-split-7/7-POPOLNOM-IZENAČEN-vs-P229-13/7!) "
    "+ meseci-Griblje: M1+A2+Mai1+Juli2+A[?]1+S3+O1+N2+D1 (Jänner/Feber/Juni-×0!) ———\n"
)

blocks = P230_HEADER
for e in grib:
    blocks += gen_block(e)

i = src.index(ANCHOR)
src = src[:i] + blocks + src[i:]
TS.write_text(src, encoding="utf-8")
print(f"vstavljenih-blokov: {len(grib)} (PRED P229-anchor)")
