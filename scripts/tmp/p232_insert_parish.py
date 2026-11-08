#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P232 — vstavi 19-GRIBLJE-blokov (krstna 04104, leto 1874 = 12/15!) v parish.ts PRED P231-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P231: krstna PREDZGODOVINA 04104, leto 1875"

E = json.load(open("/tmp/p232/entries_1874.json"))
grib = E["griblje_entries"]
assert len(grib) == 19, f"grib={len(grib)}"

P232_HDR = "  // ——— P232: krstna PREDZGODOVINA 04104, leto 1874"
if P232_HDR in src:
    i = src.index(P232_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P232-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}
MESEC_MAP = {"Jänner": "J", "Feber": "F", "Februar": "F", "März": "M", "April": "A", "Mai": "M2", "Juni": "J2", "Juli": "J3", "August": "A2", "September": "S", "October": "O", "November": "N", "December": "D", "Dezember": "D"}

KOM = {
 "z2": "★★★ MEJA-1873/74-s37-SREDI-PAGI-'Initium-anni-Domini-1874'-KALLIGRAFIJA-NOVA-VARIANTA-71.-POTRDITEV (TAIL-1873-zap-28! + RESTART-z1-1./1.!-12.-restart!) + ★★★ 1.-GRIBLJE-1874 (zap-2-VIDEN!) + ★★★ JAKOFČIČ-boter-DVOJNI-zakonca (Joseph+Anna!) + matec-DUEL-3-way-X-open + NOVI-DUHOVNIK-'Albin-Schwinger-Coop.'",
 "z8": "★★★ MILEK-×2-DVOJNI-nit (matec+botra!) + oče-HLOBUČAR-X-★★★-ločitev (3-way-rešen!) + stan-DUEL-½/¾G + rojen≠krsten-7/8",
 "z10": "★★★ MILEK-boter-nit + hisna-45/25-DUEL-X-★★★-REŠEN-'45'! + oče-garble-BRIME/BRUNE + matec-garble-MARKOVIN/HORVAT + botra-KUHAR-X-rešen",
 "z20": "★★★ STRAUČIČ-oče+boter-DVOJNI-nit + KLOBUČAR-matec+botra-DVOJNI-nit + MESEC-MÄRZ-X2-potrjen (full-'April'-rešen!) + 'Lužana'-nota-X-open",
 "z21": "★★★ SIMEC-oče-nit (continuum!) + MODRI-'†3.2.1933[?]'! + matec-DUEL-JANAPIČ/ZUNIČ + boter-priimek-kot-matec-PARALELA + stan-DUEL-½/¼ + rojen≠krsten-15/16",
 "z23": "★★★ HERBAVEC-×3-DVOJNI-nit (oče+boter+botra-VSE!) + vas-DUEL-REŠEN-X2-'Griblje' (row-halucinacija-ZAVRNJENA!) + matec-garble-LOJDA/LOVE-X-open + h30",
 "z24": "★★★ PEZDIRC-matec-nit (X-★★★-POTRJEN!) + oče-KOBLAR-X-★★★-ločitev (3-way-rešen!) + botra-garble-×2-DUEL + mesec-April-X-potrjen + h48-continuum",
 "z27": "★★★ MESEC-JUNI-X-open (VLM-neberljiv!-kronologija-mora-JUNI/JULY!-vs-full-'August'-NAPAČEN!) + oče-garble-JARREC-X-★★★-NE-Simec (row-halucinacija-ZAVRNJENA!) + botra-garble-×2",
 "z51": "★★★ vas-DUEL-X-open-×2/×1 (Griblje-majoriteta!-botra-MILEK-fit!) + hisna-40-×2-DELO-DUEL + oče-garble-ZGAJDIRE-X-★★★ (PEZDIRC-hipoteza!) + MILEK-botre-nit + BRODARIČ-boter-nit + rojen≠krsten-15/16",
 "z57": "★★★ HRIŽAN-matec-nit (X-'Hrižan'!) + oče-garble-FELK/ZELKO + botra-garble-PILAK + 'Begić/Bizdivec'-DUEL + s43-GLAVA-'1871'-VLM-MISREAD (kronologija-✓!) + duhovnik-'Franz-Dovgan'",
 "z58": "★★★ PEZDIRC-×2-DVOJNI-nit (matec+botra-X-★★★!) + BRODARIČ-oče-nit + matec-X-'Pezdirc' (row-'Bizdivec'-halucinacija-ZAVRNJENA!) + DEBLIČ-botra-nit + duhovnik-'Fabijan-Kragelj[?]-Cap'-NOVI-X-open + rojen≠krsten-4/5",
 "z63": "★★★ JAKOFČIČ-oče+matec-DVOJNI-nit (Jaškofčič-variant!) + boter-KELHO-garble (P231-'Kelčho'-PARALELA!) + botra-DRAGOŠ-nit (KOMPLET!) + h9-NOVA-hiša!",
 "z65": "★★★ PEZDIRC-boter-nit (X-★★★!-+botra-Pezdirc[?]-DVOJNI?) + MODRI-'preseljen[?]-19.3.1882'! + HRIŽAN-matec-nit + oče-DUEL-JAKOFČIČ/JAKOPIČ + h13",
 "z73": "★★★ HRIŽAN-oče-nit (X-★★★-4-way-DUEL-rešen!) + MODRI-'†22.10.1930'-P231-križ! + ★★★ zap-73-VIDEN-1:1-pozicijska-aritmetika! + matec-garble-'MILCH'-X-open (MILEK?) + LEGDIRE-boter-nit + hisna-66/64-X-rešen-'66' + TAIL-1874-P231-PREDIZKOP-1:1!",
 "z76": "★★★ LEGDIRE-oče-nit (KOMPLET-2×-LEGDIRE!-P231-križ!) + hisna-32/52/62-TROJNI-DUEL-X-★★★-REŠEN-'32'! + ★★★ zap-76-VIDEN-1:1! + matec-DUEL-NOVAK/VORALT + TAIL-1874-P231-PREDIZKOP-1:1!",
 "z81": "★★★ HRIŽAN-oče+matec-DVOJNI-nit (Peter+Dorothea!-P231-križ!) + ★★★ zap-81-VIDEN-1:1-aritmetika! + botra-garble-×2 (Kumpar! + Lah!) + h3-P231-PREDIZKOP-1:1!",
 "z82": "★★★ PEZDIRC-oče-nit (X-★★★!) + hisna-40-DELO-DUEL (P231-'h4[~40]'-X-REŠEN-'40'!) + MODRI-'†29.11.1947[?]-vs-1944[?]'-DUEL-X-open! + ★★★ zap-82-VIDEN-1:1! + matec-DUEL-JAKOFČIČ/PAHOVIČ + botra-HLOBUČAR-nit (z8-PARALELA!) + DEBLIČ-botra-continuum!",
 "z90": "★★★ TAIL-1874-GRIBLJE (P231-1:1-KRIŽ!) + PEZDIRC-matec-nit + MILEK-oče+boter-DVOJNI-nit + hisna-22/42-DUEL-X-★★★-REŠEN-'22'! + BRODARIČ-botra-KOMPLET!",
 "z91": "★★★ TAIL-1874-GRIBLJE (P231-1:1-KRIŽ!-μh65!) + PEZDIRC-boter-nit (X-★★★-REŠEN!) + MILEK-oče-nit + HARASINIČ-matec-nit (continuum!) + ime-DUEL-Maria/Franziska-X-REŠEN + botra-garble-PUTLAR/TURK",
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
               f"botra {esc(e['botra'])}; + {kom} + pag-konvencija-sken−3 [z{z[1:]}]")
    what_en = (f"baptized {esc(e['otrok'])} ({mesec_en} {rojen}/{krsten}) — father {esc(e['ocec'])}, mother {esc(e['matec'])}; "
               f"godparents {esc(e['botra'])}; + [see-SI] + [z{z[1:]}]")
    return (
        "  {\n"
        f'    houseNo: "{e["hisna"].split()[0]}",\n'
        '    bookSignature: "04104",\n'
        "    year: 1874,\n"
        f"    scan: {sk},\n"
        f"    page: {pag},\n"
        f'    whatSi: "{what_si}",\n'
        f'    whatEn: "{what_en}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

P232_HEADER = (
    "  // ——— P232: krstna PREDZGODOVINA 04104, leto 1874 = 12/15 — (s37–s47 == 11 skenov (s37-SREDI-PAGI-MEJA-'Initium'!-TAIL-1873-r1! + "
    "s38–s44-1874!-s45–s47-TAIL-1874-P231-predizkop!-DESCENDING-probe-P231-LEAD-s36–s45!); "
    "★★★ FOLIACIJA-'sken−3'-SEKVENČNO-s36–s47 (33–44!-12/12!-s37='34'-s44='41'-s45='42'-s47='44'!-formula-CONTINUES-iz-P231!-BREZ-duplikatov-v-oknu!-2-DUPLIKATA-še-vedno-pred-s36-s1–s35!); "
    "★★★ MEJA-1873/74 = s37-SREDI-PAGI + 'Initium-anni-Domini-1874'-VELIKA-KALLIGRAFIJA-NOVA-VARIANTA-1.-INITIUM-v-liniji (vs-'finis-Anni'-P230!-vs-BREZ-P231!-4.-mejna-varianta-zaporedoma: "
    "P229-ENO!-P230-DVO!-P231-SREDI!-P232-SREDI-z-INITIUM!): s37-r1-TAIL-1873 (zap-28[~98/lokalni-restart-X-open!]-Dez-28/29-Kloster-h69-Amalia-'Franz-Dovgan'!) → "
    "'Initium-anni-Domini-1874'-KALLIGRAFIJA-ČEZ-VRSTO → s37-r2-RESTART-z1-NA-DAN-1./1.-JÄNNER (krst-4.!-Gradac-h31-Maria!-TIE-najzgodnejši-P221-1.1!-P222-1.1!-12.-restart!-'Albin-Schwinger-Coop.'-NOVI-duhovnik!) "
    "= 71.-POTRDITEV-invariante (70.-P231!) | s47-SREDI-PAGI-MEJA-1874/75-P231!; "
    "★★★ 92-VPISOV (z1–z92!-P231-LEAD-'~92'-1:1-POTRJENO!-aritmetika 7+8+9+11+9+9+9+9+8+8+5 = 92!-1874-sklenjen-z92!) + "
    "zap-stolpec-VIDEN-s37 (z1–z7!-restart!-z2-GRIBLJE!)-in-s45/s46 (zap-73–87!-P231-križ!-★★★ POZICIJSKA-ARITMETIKA-4/4-POTRJENA: z73=zap-73!-z76=zap-76!-z81=zap-81!-z82=zap-82!)-NEZAPISAN-s38–s44 (starša-forma!); "
    "★★★ 19-GRIBLJE / 18-hiš (h40-×2-DUEL-z51-vs-z82!-RAZLIČNI-družini!): z2-h12-DRAGOŠ-oče!-JAKOFČIČ-zakonca-botra-DVOJNI! + z8-h46-MILEK-×2-matec+botra!-HLOBUČAR-oče-X-★★★! + z10-h45-MILEK-boter!-BRIME-oče! + "
    "z20-h44-STRAUČIČ-oče+boter-DVOJNI!-KLOBUČAR-matec+botra-DVOJNI! + z21-h18-SIMEC-oče!-MODRI-†3.2.1933! + z23-h30-HERBAVEC-×3-oče+boter+botra! + z24-h48-KOBLAR-oče-X-★★★!-PEZDIRC-matec-X-★★★! + "
    "z27-h39-JARREC-oče-X-★★★!-MESEC-JUNI-X-open! + z51-h40-ZGAJDIRE-oče-X-★★★-PEZDIRC-hipoteza!-vas-DUEL-×2/×1!-MILEK-botra!-BRODARIČ-boter! + z57-h60-FELK-oče!-HRIŽAN-matec! + z58-h49-BRODARIČ-oče!-PEZDIRC-×2-matec+botra-X-★★★!-DEBLIČ-botra! + "
    "z63-h9-NOVA!-JAŠKOFČIČ-oče+matec-DVOJNI!-KELHO-boter-P231-PARALELA!-DRAGOŠ-botra! + z65-h13-PEZDIRC-boter-X-★★★!-HRIŽAN-matec!-MODRI-preseljen-19.3.1882! + z73-h66-HRIŽAN-oče-X-★★★-4-way!-MODRI-†22.10.1930!-zap-73-1:1!-MILCH-matec-X-open!-LEGDIRE-boter! + "
    "z76-h32-LEGDIRE-oče!-TROJNI-hisna-DUEL-X-★★★!-zap-76-1:1! + z81-h3-HRIŽAN-oče+matec-DVOJNI!-zap-81-1:1! + z82-h40-PEZDIRC-oče-X-★★★!-MODRI-†1947!-zap-82-1:1!-HLOBUČAR-botra!-DEBLIČ-botra! + "
    "z90-h22-TAIL-MILEK-oče+boter-DVOJNI!-PEZDIRC-matec!-BRODARIČ-botra! + z91-h65-TAIL-MILEK-oče!-PEZDIRC-boter-X-★★★!-HARASINIČ-matec! + ★★★ PEZDIRC-×7-Griblje-PORAST (vs-×5-P231!-+z51-'Zgajdire'-hipoteza-→×8!) + "
    "MILEK-×7-REKORD-PORAST (vs-×4!) + HRIŽAN-×5 + KLOBUČAR/HLOBUČAR-×4 + JAKOFČIČ-×4 + BRODARIČ-×3-KOMPLET + DEBLIČ-×2 + LEGDIRE-×2 + STRAUČIČ-×2-DVOJNI + HERBAVEC-×3-DVOJNI + DRAGOŠ-×2 + SIMEC-×1 + KOBLAR-×1 + HARASINIČ-×1 + "
    "★★★ NEZAKONSKI-×0-GRIBLJE (1.-liniji!-vs-×2-P231!) + ★★★ MODRI-×4-Griblje (†3.2.1933!-preseljen-19.3.1882!-†22.10.1930!-†29.11.1947!-razpon-1882–1947!) + "
    "GLAVE-'Jahr 1873'-×2 (s36–s37!-s37-nosi-staro-glezvo-vzor-P231-s47!)/'Jahr 1874'-×8 (s38–s45!)-glava-NI-meja-vzorec! + ★★★ BREZ-PRAZNIH-MESECEV-1.-LINIJI (J1+F2+M2+A2+Juni1+Aug1+S3+O1+N4+D2 = 19!-vs-P231-2-prazne!) + ★★★ TRI-duhovnika-1874 ('Albin-Schwinger-Coop'-NOVI!-'Franz-Dovgan'-continuum!-'Fabijan-Kragelj[?]-Cap'-NOVI-X-open!-vs-1875-2-duhovnika!) ———\n"
)

blocks = P232_HEADER
for e in grib:
    blocks += gen_block(e)

i = src.index(ANCHOR)
src = src[:i] + blocks + src[i:]
TS.write_text(src, encoding="utf-8")
print(f"vstavljenih-blokov: {len(grib)} (PRED P231-anchor)")
