#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P231 — vstavi 17-GRIBLJE-blokov (krstna 04104, leto 1875 = 11/15!) v parish.ts PRED P230-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P230: krstna PREDZGODOVINA 04104, leto 1876"

E = json.load(open("/tmp/p231/entries_1875.json"))
grib = E["griblje_entries"]
assert len(grib) == 17, f"grib={len(grib)}"

P231_HDR = "  // ——— P231: krstna PREDZGODOVINA 04104, leto 1875"
if P231_HDR in src:
    i = src.index(P231_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P231-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}
MESEC_MAP = {"Jänner": "J", "Feber": "F", "Februar": "F", "März": "M", "April": "A", "Mai": "M2", "Juni": "J2", "Juli": "J3", "August": "A2", "September": "S", "October": "O", "November": "N", "December": "D", "Dezember": "D"}

KOM = {
 "z2": "★★★ MEJA-1874/75-s47-SREDI-PAGI-NOVA-VARIANTA-70.-POTRDITEV (TAIL-1874!-+'Jänner'-PRELIM-+-veliki-cifri-'1'+'8'!-RESTART-z1-9./9.!-11.-restart!) + ★★★ 1.-GRIBLJE-1875 (2.-vpis-leta!) + ★★★ NEZAKONSKI (oče-PRAZNO!-P226-z114-PARALELA!) + ★★★ HRIŽAN-boter-DVOJNI (Nicolaus+Rosa!) + matec-'eg.-paroch.-Lipnik'-nota + DOVGAN-podpis + zap-stolpec-NEZAPISAN (starša-forma!)",
 "z4": "★★★ NEZAKONSKI-×2 (oče-PRAZNO!-+'ledig.'-materina-NOTA!-X4-krop-kolonirano-VIZUALNO!) + ★★★ h48[~18]-DUEL (X1-hisna-zoom!-kolizija-z-z93!) + boter-Urih-nit (z98-oče-PARALELA!) + DOVGAN-podpis",
 "z7": "★★★ MODRI-'umrla-24.5.1948'-dolg-pripis! + rojen≠krsten-24/25 (25/25-DUEL!) + STRUZEL-DVOJNI-nit (oče+botra!-z93-botra-PARALELA!) + HARASINIČ-matec-nit + podpis-'Roggja-Coop'-KURRENT-DUEL",
 "z8": "★★★ MILEK-boter-nit (1/4!) + Jožek-DVOJNI-nit (oče+botra!) + oče-garble-JOŽEK-X-open + matec-garble-KUHAR + DOVGAN-podpis + h28",
 "z14": "★★★ DEBLIČ-matec-garble-DUEL + oče-garble-FELAH/ŠELAH-X-open + ŽELJKO-boter + STRAUS-botra-nit (z4-PARALELA!) + podpis-'Hoggjač-Coop'-KURRENT-DUEL + rojen≠krsten-7/8 + mesec-Feber (full-page-'Dezember'-NAPAČEN!-X1-'Febr'-POTRJEN!)",
 "z15": "★★★ HUSIČ-oče-nit (P230-z53-botra-PARALELA!) + ★★★ HAMBIČ-matec-nit (1/2!-z16-DVOJNI-sosed!) + botra-garble-×2-DUEL (Merh/Urh! + Perdlova/Petek!) + podpis-'Roggja-Coop' + rojen≠krsten-11/12",
 "z16": "★★★ HAMBIČ-oče-nit (2/2-KOMPLET!-z15-SOSEDNJI-VRSTICI!) + ★★★ MILEK-boter-nit (2/4!-X1-potrjen!) + ★★★ MODRI-'†6.3.1946'-+poroka-1925! + h94-NOVA-hiša (vs-h37-DUEL!) + PRODNIK-botra + DOVGAN-podpis",
 "z29": "★★★ PEZDIRC-boter-nit (1/3!-X4-extended-krop-potrjen!) + ★★★ DEBLIČ-oče-nit (2/2!-z14-PARALELA!) + ★★★ BRODARIČ-botra-nit (1/3!) + matec-garble-HEWIČ-X-open + podpis-'Hoggja-Coop'",
 "z36": "★★★ MILEK-oče-nit (3/4!-continuum!) + ★★★ HRIŽAN-matec-nit (1/3!-z57-IME-1:1-PARALELA!) + botra-garble-×2 (Alešič! + Gozel/Rozel!) + DOVGAN-podpis (X4-potrjen!)",
 "z44": "★★★ PEZDIRC-matec-nit (2/3!-X2-potrjen!) + oče-garble-WERBÖSER/VERBIČAR-X-open + botra-garble-×2 + DOVGAN-podpis + rojen≠krsten-22/23 + h64 (vs-h6-DUEL!) + mesec-Mai (row-read-'Juni'-NAPAČEN!-chronologija!)",
 "z51": "★★★ DRAGOŠ-matec-nit (1/3!) + ★★★ ŠKRANC-oče+boter-DVOJNI-nit (X2-potrjen!) + hisna-72/42-DUEL (X2-'72'!) + botra-garble-LAVRINNA-X-open + DOVGAN-podpis + rojen≠krsten-14/15",
 "z57": "★★★ SIMEC-oče-nit (1/2!-X2-LOČILNI-KROP-row-read-halucinacija-ZAVRNJENA!) + ★★★ HRIŽAN-matec-nit (2/3!) + ★★★ DRAGOŠ-boter-nit (2/3!) + ★★★ mesec-DUEL-REŠEN (row-read-'Juni'-NE-mogoče! → JULI!) + datum-DUEL-23-vs-22 + boter-garble-FOLTER-Lavrmann + MODRI-nota-'5.9.1922' + DOVGAN-podpis",
 "z59": "★★★ LOGAR-oče-nit (1/2!-z98-Lozar-ime-DUEL!) + ★★★ HARASINIČ-matec-nit (2/2-KOMPLET!) + ★★★ BRODARIČ-botra-nit (2/3!) + boter-garble-HLOBEC/HLEBEC + DOVGAN-podpis + h57 (row-'r4-DUP'-halucinacija-ZAVRNJENA-s54-7-vrstic!)",
 "z93": "★★★ KLOBUČAR-oče-nit (1/1!) + ★★★ PEZDIRC?-matec-DUEL (X3-'Podirec/Podvec'-h48-kolizija-z-z4!-X-open!) + ★★★ BRODARIČ-boter-nit (3/3-KOMPLET!) + ★★★ STRUZEL-botra-nit (z7-PARALELA!) + ★★★ MODRI-'†28.XI.1940'! + podpis-'Hoggjač-Coop'-KURRENT-DUEL + h48-×2-RAZLIČNI",
 "z98": "★★★ URH-oče-nit (2/2-KOMPLET!-z4-boter-PARALELA!) + ★★★ GOZEK-DVOJNI-nit (matec+botra!-X3-×2!) + ★★★ LOGAR/LOZAR-ime-DUEL (z59-1:1-ime!) + podpis-'Hoggjač-Coop' + h68-NOVA-hiša!",
 "z111": "★★★ JAKOFČIČ-DVOJNI-nit (matec+boter!-X4-potrjen!) + oče-garble-KELČHO/ŠTEFKO-X-open + ★★★ MODRI-'†17.9.1933'! + DOVGAN-podpis + h1-NOVA-hiša (1.-Griblje-h1!)",
 "z3t": "★★★ TAIL-1875-GRIBLJE (s64-r3-P230-1:1-KRIŽ!) + ★★★ DRAGOŠ-matec-nit (3/3-KOMPLET!) + ★★★ JAKOFČIČ-botra-nit + ŠIMEC-boter-nit (2/2!) + oče-garble-LUNIČ/ZUNIČ-X-open + podpis-'Hoggia-Coop'-KURRENT-DUEL + ★★★ TAIL-RESTART-z1–z4-LOKALNI-NOVA-VARIANTA + 'finis-Anni-1875'-KALLIGRAFIJA!",
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
               f"botra {esc(e['botra'])}; + {kom} + pag-konvencija-sken−3 [z{z.replace('z3t','3-tail')[1:]}]")
    what_en = (f"baptized {esc(e['otrok'])} ({mesec_en} {rojen}/{krsten}) — father {esc(e['ocec'])}, mother {esc(e['matec'])}; "
               f"godparents {esc(e['botra'])}; + [see-SI] + [z{z.replace('z3t','3-tail')[1:]}]")
    return (
        "  {\n"
        f'    houseNo: "{e["hisna"].split()[0]}",\n'
        '    bookSignature: "04104",\n'
        "    year: 1875,\n"
        f"    scan: {sk},\n"
        f"    page: {pag},\n"
        f'    whatSi: "{what_si}",\n'
        f'    whatEn: "{what_en}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

P231_HEADER = (
    "  // ——— P231: krstna PREDZGODOVINA 04104, leto 1875 = 11/15 — (s45–s64 == 20 skenov (s45–s47-TAIL-1874 + s47-SREDI-PAGI-MEJA! + "
    "s48–s64-1875!-s60/s61/s62-TROJNI-DUPLIKAT-folio-57!-DESCENDING-probe-P230-LEAD-s57–s64-RAZŠIRJEN-na-s45–s56!); "
    "★★★ FOLIACIJA-NOVO-ODKRITJE-TROJNI-DUPLIKAT-folio-57 (s60=s61=s62-VIZUALNO-1:1-isti-razpon-November-3–20!-3-različnih-md5!-prilepljeni-listi-na-3-položajih!) + "
    "s45–s60-'sken−3'-SEKVENČNO (42–57!-15/15-visoko!) + s63='58'/s64='59'-'sken−5'-P230! — 2-DUPLIKATA-PRED-s45-neznana-lokacija-s1–s44!; "
    "★★★ MEJA-1874/75 = s47-SREDI-PAGI-NOVA-VARIANTA-3.-mejna-varianta-zaporedoma (TAIL-1874-Dez-26–31-×5-vrstic-incl.-GRIBLJE-h22+μh65-MILEK-×2! + "
    "'Jänner'-VELIKA-PRELIM + veliki-cifri-'1'+'8'-VSOTNA-'1[8][7][5]'-razpeto[?]-X-open! + RESTART-z1-NA-DAN-9./9.-JÄNNER-Dobravce-h20-Nicolaus-Rus!-11.-restart! "
    "= 70.-POTRDITEV-invariante!-BREZ-'finis-Anni-1874'-KALLIGRAFIJE-leto-končano-SREDI-PAGI!-glave-'Jahr 1874'-×3/'Jahr 1875'-×14-glava-NI-meja! | "
    "s64-TAIL-1875 + TAIL-RESTART-z1–z4-LOKALNI-NOVA-VARIANTA + 'finis-Anni-1875'-KALLIGRAFIJA-P230!); "
    "★★★ 119-VPISOV (z1–z115-Jan–Nov + TAIL-z1–z4-Dez!-aritmetika 3+9+8+9+9+9+9+7+7+7+7+8+8+7+8+4 = 119!-z100-MILESTONE-s59-r8-TODGEBORENE[?]-garble!) + "
    "zap-stolpec-NEZAPISAN-s47–s63-starša-forma (vs-P230-×6-VIDNI!) + TAIL-1874-zap-72–87-VIDEN-×2-strani (1874-sklenjen-z~92!); "
    "★★★ 17-GRIBLJE / 16-hiš (h48-×2-DUEL-z4-'48[~18]'-NEZ-vs-z93-KLOBUČAR!): z2-h30-NEZ-HRIŽAN-boter-DVOJNI! + z4-h48-NEZ-'ledig.'-NOTA!-Urih-boter! + "
    "z7-h5-STRuzel-DVOJNI!-MODRI-umrla-24.5.1948! + z8-h28-MILEK-boter! + z14-h34-DEBLIČ-matec-DUEL! + z15-h37-HUSIČ-oče!-HAMBIČ-matec! + z16-h94-HAMBIČ-oče!-MILEK-boter!-MODRI-†6.3.1946! + "
    "z29-h33-PEZDIRC-boter!-DEBLIČ-oče!-BRODARIČ-botra! + z36-h29-MILEK-oče!-HRIŽAN-matec! + z44-h64-PEZDIRC-matec! + z51-h72-DRAGOŠ-matec!-ŠKRANC-DVOJNI! + z57-h38-SIMEC-oče!-HRIŽAN-matec!-DRAGOŠ-boter! + "
    "z59-h57-LOGAR-oče!-HARASINIČ-matec!-BRODARIČ-botra! + z93-h48-KLOBUČAR-oče!-BRODARIČ-boter!-STRuzel-botra!-MODRI-†28.11.1940!-PEZDIRC?-matec-DUEL! + z98-h68-URH-oče!-GOZEK-DVOJNI!-LOGAR/LOZAR-DUEL! + "
    "z111-h1-JAKOFČIČ-DVOJNI!-MODRI-†17.9.1933! + z3t-h11-TAIL-DRAGOŠ-matec!-JAKOFČIČ-botra!-ŠIMEC-boter! + ★★★ PEZDIRC-×5-NAJNIŽJA-linije (×3-Griblje!-vs-×17-1876!) + "
    "MILEK-×4 + HRIŽAN-×6 + BRODARIČ-×5 + DRAGOŠ-×3-KOMPLET + JAKOFČIČ-×4 + DEBLIČ-×2 + HAMBIČ-×2-SOSEDNJI + STRUZEL-×3 + URH-×2 + GOZEK-×2-DVOJNI + LOGAR/LOZAR-×2-ime-DUEL + ŠKRANC-×2 + ŠIMEC-×2 + "
    "★★★ NEZAKONSKI-×2-GRIBLJE (oče-PRAZNO-×2!) + ★★★ MODRI-×4-Griblje (†1933/1940/1946/1948!-+poroka-1925!) + ★★★ VIOLET-RETRO-VPIS-z6-datiran-'vom-11.-October-1875'-NOVI-TIP! + "
    "★★★ FEBER-1-PRELIM-BREZ-DATUMA-s48-r9 (veliki-'Feber-1'-prelom-celici-PRAZNI!) + ★★★ z100-MILESTONE-TODGEBORENE[?]-garble (P229-DRUŽINA-PARALELA!) + HEBAMME-Maria-Born[~Rom]-×2 + "
    "★★★ DUHOVNIŠKA-IZMENJAVA-1875 ('Hoggia/Roggja/Hoggin-Coop'-DUEL ↔ Franz-Dovgan!-Griblje-split-DOVGAN-×10/HOGGIA-×7!-vs-P230-7/7!-TAIL-'Rogej-Coop'-×3!) + "
    "meseci-Griblje: J4+F3+M1+A1+Mai1+Juni1+Juli2+O2+N1+D1 (August+September-×0!-2-prazne!) ———\n"
)

blocks = P231_HEADER
for e in grib:
    blocks += gen_block(e)

i = src.index(ANCHOR)
src = src[:i] + blocks + src[i:]
TS.write_text(src, encoding="utf-8")
print(f"vstavljenih-blokov: {len(grib)} (PRED P230-anchor)")
