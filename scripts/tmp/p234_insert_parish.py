#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P234 — vstavi 17-GRIBLJE-blokov (krstna 04104, leto 1872 = 14/15!) v parish.ts PRED P233-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P233: krstna PREDZGODOVINA 04104, leto 1873"

E = json.load(open("/tmp/p234/entries_1872.json"))
grib = E["griblje_entries"]
assert len(grib) == 17, f"grib={len(grib)}"

P234_HDR = "  // ——— P234: krstna PREDZGODOVINA 04104, leto 1872"
if P234_HDR in src:
    i = src.index(P234_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P234-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}
MESEC_MAP = {"Jänner": "J", "Feber": "F", "Februar": "F", "März": "M", "April": "A", "Mai": "M2", "Juni": "J2", "Juli": "J3", "August": "A2", "September": "S", "October": "O", "November": "N", "December": "D", "Dezember": "D"}

KOM = {
 "z1": "★★★ 1.-VPIS-leta-1872 = GRIBLJE-h11!-RESTART-z1-12.-restart (PARALELA-P223-'krst-4.1'!) + MEJA-1871/72 = s13/s14-PAGE-BOUNDARY-X-open + DRAGOŠ-matec-nit (1/3!)",
 "z14": "h30-nit (1/2-DUEL-z103-Simic!-★★★ h30-×2-RAZLIČNI-družini-PARALELA-1873-h37-×2!) + oče-garble-PETEK + zap-14-pozicijsko (X-'16'-DUEL!)",
 "z27": "★★★ HRIŽAN-DVOJNI-oče+matec-nit (2/5!-+botra-3/5!) + ŠIMEC-boter-nit (1/3!) + mesec-GARBAGE-ROW (celost-'November'-KRONOLOŠKO-IZKLJUČEN!-X-'ne-November'!-kronološki-model-April-X-open!)",
 "z34": "★★★ HLOBUČAR-DVOJNI-matec+botra-nit (1/3+2/3!-z103-boter-KOMPLET!) + oče-DUEL-Mathias-vs-X-'Martin' + KRAUP-×2 + rojen≠krsten-27/28",
 "z36": "DRAGOŠ-boter-nit (2/3!) + oče-garble-LUKET + h9 + zap-36-X-pozicijsko",
 "z38": "★★★ MODRI-'poročena-18.II.1919-†16.3.[?]' (1.-MODRI-1872!) + ★★★ DRAGOŠ-botra-nit (3/3-KOMPLET-PARALELA-P233-×3!) + ŠIMEC-oče-nit (2/3!) + oče-X-straddle-Šimec/Vržan",
 "z47": "h24 + oče-garble-PRINC + matec-DUEL-Ivanc/Ivanis + botra-garble-LOŽEK + zap-47/48-DUEL-X-open + mesec-Mai-29-kronologija",
 "z59": "★★★ PEZDIRC-oče-garble-nit-'Pegdic' (1/5!-continuum-1873-'Pegdire'!) + ★★★ MESEC-'Jänner'-PRIMING-HALUCINACIJA-RAZREŠENA (4-kronološka-dokaza-JUNI/July!) + matec-NOVAK-nit (PARALELA-P233-z68!) + KLOBUČAR-boter-nit + HRIŽAN-botra-nit (4/5!)",
 "z61": "★★★ DEBLIČ-oče-garble-nit-'Deblin'-X-★★★ (vs-'Doblič'/'Pehlič'-3-way!) + ★★★ MODRI-pripis-neberljiv (2.-MODRI!) + BRODARIČ-boter-nit-continuum + h33-continuum-P233-z28",
 "z63": "★★★ PEZDIRC-×2-DVOJNI-matec+boter-nit (2/5+3/5!-EKSPPLICITNI-'Pezdirc'-2×!-PARALELA-P233-z39-1:1!) + hisna-6/61-DUEL-X-open + oče-garble-VERBIČ/DERBIČ",
 "z74": "★★★ h40-CONTINUUM (z74-1872!-+z51-1873!-+z51/z82-1874!-×4-v-3-letih!) + ★★★ PEZDIRC-oče-garble-'Lezdirc'-'Ležir'-hipoteza (4/5!-PARALELA-P233-z51-'Peter-Ležir'-1:1!) + JAKOFČIČ-matec-nit (1/2!) + ŠIMEC-boter-nit (3/3-KOMPLET!) + KLOBUČAR-botra-nit (2/2!) + rojen≠krsten-3/4 + MODRI-neberljiv (3.-MODRI!)",
 "z92": "★★★ MILEK-botra-garble-X-open-'Milhoeluc' (PARALELA-P233-z93-1:1!) + matec-LOŽEK-nit-continuum + h68 + oče-garble-POTOK",
 "z97": "h69-continuum-P233-z55 (×2-v-2-letih!) + oče-garble-BORIN + rojen≠krsten-9/10 + 'November'-prelom-nota",
 "z99": "★★★ PEZDIRC-botra-garble-nit-'Peghirc' (5/5-KOMPLET-1872!-vs-×8-1873!) + oče-garble-FOSTER/LINDER + h7",
 "z103": "★★★ h30-×2-DELO-DUEL (vs-z14-Petek!-★★★ + r7-PREČRTANA-KOPIJA-TE-VRSTICE-X-★★★-POTRJENA!) + ★★★ JAKOFČIČ-matec-nit (2/2-KOMPLET!) + HLOBUČAR-boter-nit (3/3-KOMPLET!) + SIMEC-oče-garble + roj-21/22-DUEL + hisna-30/39-DUEL-X-open + BRODARIČ/BRODNIK-botra-DUEL",
 "z112": "★★★ HRIŽAN-oče-garble-'Kribžan' (5/5-KOMPLET!) + matec-garble-MIHELIČ (MILEK?-X-open!) + MODRI-'smrtka-dne-8.I[?]' (4.-MODRI!) + 'Morija'-črtan-nota + rojen≠krsten-26/27",
 "z115": "★★★ TAIL-1872 = z115 (1.-TAIL-GRIBLJE-linije!-ZADNJI-VPIS-1872!-Dez-29!-TAIL-VERIGA-'110–115'-6/6!-vs-'116'-MISREAD!-s25-r7-PRAZNA!-115-VPISOV!) + MIHELIČ-oče-MILEK?-X-open + HRIŽAN-matec ('Kribžan'!) + MEJA-1872/73 = s25/s26-PAGE-BOUNDARY (restart-z1-s26-r1-SUPER-POTRJEN!-13.-restart!)",
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
    mm = e["mesec"].split()[0].rstrip("[]")
    m = MESEC_MAP.get(mm, "J")
    mesec_si_num = MESEC_SI[m]
    mesec_en = MESEC_EN[m]
    rojen = clean_day(e["rojen"])
    krsten = clean_day(e["krsten"])
    hisna = esc(e["hisna"])
    kom = esc(KOM[z])
    what_si = (f"krščena {esc(e['otrok'])} ({rojen}./{krsten}. {mesec_si_num}.) — oče {esc(e['ocec'])}, mati {esc(e['matec'])}; "
               f"botra {esc(e['botra'])}; + {kom} + pag-konvencija-sken−3 [z{z[1:]}]")
    what_en = (f"baptized {esc(e['otrok'])} ({mesec_en} {rojen}/{krsten}) — father {esc(e['ocec'])}, mother {esc(e['matec'])}; "
               f"godparents {esc(e['botra'])}; + [see-SI] + [z{z[1:]}]")
    return (
        "  {\n"
        f'    houseNo: "{e["hisna"].split()[0].split("[")[0]}",\n'
        '    bookSignature: "04104",\n'
        "    year: 1872,\n"
        f"    scan: {sk},\n"
        f"    page: {pag},\n"
        f'    whatSi: "{what_si}",\n'
        f'    whatEn: "{what_en}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

P234_HEADER = (
    "  // ——— P234: krstna PREDZGODOVINA 04104, leto 1872 = 14/15 — (s14–s25 == 12 skenov (MEJA-1871/72 = s13/s14-PAGE-BOUNDARY!-glave-12/12-'Jahr 1872'!-s14–s25-1872-teče!-s26-ŽE-1873-z1-P233-kontekst!-DESCENDING-probe-P233-LEAD-s19–s28-NADGRAJENO-s14–s25!-2×-md5-16/16!); "
    "★★★ FOLIACIJA-'sken−3'-SEKVENČNO-s14–s25 (11–22!-12/12-visoko!-s14='11'-s19='16'-s25='22'-s28='25'-P233!-formula-CONTINUES-iz-P233!-BREZ-duplikatov-v-oknu!-★★★ DUPLIKAT-s28=s29-ILE-okna (fol-25-2×-skeniran!-P233-'2-DUPLIKATA'-DELOVNO-RAZREŠENA!)); "
    "★★★ 115-VPISOV-ARITMETIČNI-MODEL (z1–z115!-TAIL-VERIGA-6/6-visoko!): s14=1–11 (11!-z1-X-RESTART!) + s15=12–21 + s16=22–30 (meseci-GARBAGE!) + s17=31–40 (X-34/36/38!) + s18=41–50 (X-50-KONTROLA!) + s19=51–59 (JUNI-kronologija!-vs-'Jänner'-PRIMING-halucinacija!) + s20=60–68 + s21=69–79 (h40!) + s22=80–89 (BREZ-Griblje!) + s23=90–99 + s24=100–109 (10-distinct-+1-PREČRTANA-KOPIJA-r7-X-★★★!) + s25=110–115 (TAIL-VERIGA!-z115-TAIL-GRIBLJE-Dez-29!) = ★★★ 116-vrstic-−-1-prečrtana-=-115-DISTINCT-VPISOV — vs-LEAD-'~85–95'-NADGRADJENO; "
    "★★★ MEJA-1871/72 = s13/s14-PAGE-BOUNDARY (1.-PAGE-BOUNDARY-linije!): restart-z1-NA-s14-r1-Jänner-5-GRIBLJE-h11 (X-SUPER-'1'-POTRJEN!-12.-restart-PARALELA-P223-'krst-4.1'!-1.-vpis-leta = GRIBLJE!) | MEJA-1872/73 = s25/s26-PAGE-BOUNDARY (P233-ARITMETIČNA-NAPoved-1:1!): s25-TAIL-z115 + s26-r1 = z1-Jänner-3 (restart-13.-restart-S26R1-SUPER-'1'-VISOKO!-P233-X-open-RESOLVED!-BREZ-'finis-Anni-1872'-kalligrafije-Q4-negativno!); "
    "★★★ DUPLIKAT-s28 = s29-RESITEV (fol-25-2×-skeniran!-P233-'z11–z21'-fantom-NIKOLI-ne-obstajal!-z1–z21-VSE-na-s26/s27!-★★★ 98-TOTAL-1873-INTAKTEN-1:1!-'2-DUPLIKATA'-P233-UGE-DELOVNO-RAZREŠENA!) + "
    "★★★ 17-GRIBLJE / 16-hiš (h30-×2-DUEL-z14-Petek!-vs-z103-Simic!-RAZLIČNI!-+ r7-PREČRTANA-KOPIJA!-ISENAČEN-z-1873-×17!-PARALELA-h37-×2!): z1-h11-1.-VPIS-leta!-DRAGOŠ-matec! + z14-h30-Petek! + z27-h3-HRIŽAN-DVOJNI!-mesec-GARBAGE-ROW! + z34-h44-KRAUP-HLOBUČAR-DVOJNI! + z36-h9-DRAGOŠ-boter! + z38-h38-ŠIMEC-oče-DRAGOŠ-botra-KOMPLET!-MODRI-1919! + z47-h24-PRINC!-zap-47/48-DUEL! + z59-h12-PEZDIRC-'Pegdic'!-'Jänner'-PRIMING-halucinacija-RAZREŠENA-JUNI! + z61-h33-DEBLIČ-'Deblin'-X!-BRODARIČ-boter! + z63-h6/61-DUEL-PEZDIRC-×2-DVOJNI-EKSPPLICITNO! + z74-h40-★★★-CONTINUUM-×4-v-3-letih!-PEZDIRC-'Lezdirc/Ležir'-PARALELA-P233!-JAKOFČIČ-matec!-ŠIMEC-KLOBUČAR-botra! + z92-h68-MILEK-'Milhoeluc'-PARALELA! + z97-h69-continuum! + z99-h7-PEZDIRC-'Peghirc'-5/5! + z103-h30/39-DUEL-JAKOFČIČ-matec-KOMPLET!-HLOBUČAR-boter-KOMPLET!-r7-PREČRTANA! + z112-h66-HRIŽAN-'Kribžan'!-MODRI-'smrtka-8.I'! + z115-h29-★★★-TAIL-1872!-MEJA-s25/s26! + "
    "★★★ PEZDIRC-×5-GARBLE-continuum (z59-'Pegdic'!-z63-Anna+Michael-'Pezdirc'-×2-EKSPPLICITNO-DVOJNI!-z74-'Lezdirc'-'Ležir'-hipoteza!-z99-'Peghirc'!-vs-×8-1873!) + DEBLIČ-×1-'Deblin'-X + JAKOFČIČ-×2-KOMPLET (z74-z103!) + ★★★ DRAGOŠ-×3-KOMPLET-1:1-PARALELA-P233 (matec+boter+botra!) + ★★★ HRIŽAN-×5-oseb-KOMPLET (z27-DVOJNI!-Kribžan/Križan-garble!) + ★★★ HLOBUČAR-×3-KOMPLET (z34-DVOJNI!-z103!) + ★★★ ŠIMEC-×3-KOMPLET (z27-z38-z74!-+Simic-z103-garble!) + KLOBUČAR-×2 + BRODARIČ-×2-garble + LOŽEK-×2 + MILEK-×1-'Milhoeluc'-garble-PARALELA + MIHELIČ-×2-MILEK?-X-open + "
    "★★★ NEZAKONSKI-×0-GRIBLJE (vs-×1-1873!) + ★★★ MODRI-×4-Griblje-1872 ('poročena-18.II.1919-†16.3.'!-2-neberljivih!-'smrtka-8.I'!-razpon-1919!) + "
    "★★★ SEPTEMBER-×0-GRIBLJE-1872 (1.-prazen-mesec-leta!-vs-1873-4-prazni!-vs-1874-BREZ!) + s24-r7-PREČRTANA-KOPIJA-X-★★★-'Morija'-črtan-nota-z112-'November'-prelom-nota-z97 + rdeči-tički-continuum ———\n"
)

blocks = P234_HEADER
for e in grib:
    blocks += gen_block(e)

i = src.index(ANCHOR)
src = src[:i] + blocks + src[i:]
TS.write_text(src, encoding="utf-8")
print(f"vstavljenih-blokov: {len(grib)} (PRED P233-anchor)")
