#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P233 — vstavi 17-GRIBLJE-blokov (krstna 04104, leto 1873 = 13/15!) v parish.ts PRED P232-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P232: krstna PREDZGODOVINA 04104, leto 1874"

E = json.load(open("/tmp/p233/entries_1873.json"))
grib = E["griblje_entries"]
assert len(grib) == 17, f"grib={len(grib)}"

P233_HDR = "  // ——— P233: krstna PREDZGODOVINA 04104, leto 1873"
if P233_HDR in src:
    i = src.index(P233_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P233-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}
MESEC_MAP = {"Jänner": "J", "Feber": "F", "Februar": "F", "März": "M", "April": "A", "Mai": "M2", "Juni": "J2", "Juli": "J3", "August": "A2", "September": "S", "October": "O", "November": "N", "December": "D", "Dezember": "D"}

KOM = {
 "z14": "★★★ 1.-GRIBLJE-1873-v-oknu (zap-24-brano-[~14-X-ARITMETIKA-+10-misread!]!) + ŠILAR-oče-nit (2/3!) + matec-DUEL-Catharina/Anna + botra-garble-×2",
 "z18": "ŠILAR-oče-nit (2/3-z14-PARALELA!) + DEBLIČ-matec-nit (1/2-continuum-P232!) + mesec-DUEL-APRIL-2/3 (vs-X-'März'!) + zap-[~18-X-ARITMETIKA!]",
 "z19": "hisna-37/27-DUEL-X-open (h37-×2-POTENCIJA-z-z81!) + oče-garble-3-way-HRIČ/HUMIČ/FLURIČ + URH-botra-garble + DEBLIČ-botra-nit-KOMPLET + rojen≠krsten-3/4 + zap-[~19-X-ARITMETIKA!]",
 "z23": "★★★ JAKOFČIČ-oče-nit + ŠILAR-matec-nit (3/3-KOMPLET!) + MODRI-'+28.12.1941'! + retro-nota-'von-20-April-1873'-X-open + LEGDIRE-garble-boter + zap-[~23-X-ARITMETIKA!]",
 "z28": "★★★ PEZDIRC-oče-garble-nit (1/8-REKORD!-X-'Marius-Pezdirc'!) + mesec-DUEL-MAI-X-open (full-'September'-kronološko-IZKLJUČEN!) + hisna-31/33-DUEL-X-open + X-straddle-r6/r7-dokumentiran",
 "z39": "★★★ PEZDIRC-×2-DVOJNI-garble-nit (matec-Perdisek + boter-Peter-Perdisek!) + BRODARIČ-oče-nit + mesec-JULI-X-potrjen + h49-continuum-P232 + zap-39-pozicijsko",
 "z47": "★★★ JAKOFČIČ-boter-DVOJNI-zakonca-nit (PARALELA-P232-z2-1:1!) + oče-garble-ŠTEFKO + h1 + zap-47-pozicijsko (X-'41'-shift!)",
 "z51": "★★★ PEZDIRC-oče-garble-nit (4/8!-'Ležir'-hipoteza!) + ★★★ h40-DUEL-continuum (z-P232-×2!-h40-×3-v-2-letih!) + ★★★ MODRI-'†12.3.1938' (Q4-križ-1:1!) + DEBLIČ-matec-nit + MILEK-botra-garble + ★★★ zap-51-X-POTRJEN-1:1 (★ANKA!)",
 "z55": "★★★ PEZDIRC-botra-garble-nit (5/8!-'Pedice'!) + vas-DUEL-×2/×1-GRIBLJE-zmaga (PARALELA-P232-z51-1:1!) + oče-garble-3-way + zap-55-X-POTRJEN (★ANKA!)",
 "z56": "★★★ BRODARIČ-matec+botra-DVOJNI-nit (KOMPLET!) + oče-garble-3-way-HAMBIČ/KAMBIČ/BRODARIČ + hisna-74/64-DUEL + ime-DUEL-Mathias-2/3 + zap-56-X-POTRJEN (★ANKA!)",
 "z65": "★★★ BRODARIČ-matec-nit (3/3-KOMPLET!) + DRAGOŠ-botra-nit (1/3!) + oče-garble-JAKOPIČ/GLASPIĆ + h8 + zap-65-X-POTRJEN (★ANKA!)",
 "z68": "★★★ oče-DUEL-NOVAC-vs-MILEK-X-open-★★★ (MILEK-hipoteza!) + ★★★ matec-PRAZNO/prečrtano-NEZAKONSKI?-X-open + BRODARIČ-boter-nit (KOMPLET!) + hisna-22/42-DUEL (PARALELA-P232-z90!) + zap-68-X-POTRJEN (★ANKA!)",
 "z73": "★★★ PEZDIRC-×3-DVOJNI-garble-nit (oče+boter+matec-hipoteza!-X-'Pezdirc'-EKSPPLICITNO!) + ★★★ DRAGOŠ-botra-nit (3/3-KOMPLET!) + datum-DUEL-Oct-3/31 + ★★★ POZICIJSKA-PARALELA-P232-z73 (obe-z73-1:1!) + zap-73-pozicijsko",
 "z81": "★★★ hisna-37/57-DUEL-X-★★★-REŠEN-'37' + ★★★ h37-×2-DELO-DUEL-X-open (vs-z19!) + ★★★ full-r2/r3-MERGE-RAZREŠEN (Carolina-Sušnik-IZLOŽENA!) + LOGAR-oče-garble + KLOBUČAR-botra-nit + rojen≠krsten-27/28 + zap-81-pozicijsko",
 "z92": "★★★ LEAD-'JAKOŠA[?]'-REŠEN-X-'JAKOFČIČ'-★★★ (3/3!) + JAKOFČIČ-oče-nit (3/5!) + ★★★ zap-92-X-POTRJEN-P232-KRIŽ-1:1 + DRAGOŠ-botra-nit",
 "z93": "★★★ LEAD-'MILEK-botra'-DUEL-X-open (Mihelč-vs-Mileh-2-way-MILEK-hipoteza!) + HRIŽAN-matec-garble-nit + oče-garble-GUVEČ/HURE + zap-93-X ✓ P232-KRIŽ",
 "z94": "★★★ LEAD-'h11-Kaspar-KUMIĆ'-DUEL-REŠEN-X-open-×3 (h41-2/2!-Grmič-2/2!-KUMIĆ-hipoteza!) + ime-DUEL-Katharina/Kaspar + DRAGOŠ-matec-nit + SIMEC-boter-nit + JAKOFČIČ-botra-nit (5/5-KOMPLET!) + zap-94-X ✓ P232-KRIŽ",
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
        f'    houseNo: "{e["hisna"].split()[0].split("[")[0]}",\n'
        '    bookSignature: "04104",\n'
        "    year: 1873,\n"
        f"    scan: {sk},\n"
        f"    page: {pag},\n"
        f'    whatSi: "{what_si}",\n'
        f'    whatEn: "{what_en}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

P233_HEADER = (
    "  // ——— P233: krstna PREDZGODOVINA 04104, leto 1873 = 13/15 — (s28–s36 == 9 skenov (MEJA-1872/73-PRED-s28!-glave-9/9-'Jahr 1873'!-s28–s35-1873-teče!-s36-TAIL-zap-88–97-P232-predizkop!-DESCENDING-probe-P232-LEAD-s28–s36!); "
    "★★★ FOLIACIJA-'sken−3'-SEKVENČNO-s28–s36 (25–33!-9/9!-s28='25'-s30='27'-s35='32'-s36='33'!-P232-LEAD-s35='32'-1:1-POTRJENA!-s30='27'-POTRJENA!-formula-CONTINUES-iz-P232!-BREZ-duplikatov-v-oknu!-2-DUPLIKATA-še-vedno-pred-s28-s1–s27!); "
    "★★★ X-ARITMETIČNI-MODEL-zap (9-ANKER-X-POTRJENIH: z51!-z55!-z56!-z65!-z68!-z88!-z92!-z93!-z94!): s28=11–21 (brano-20–30-★★★ +10-SISTEMATIČNI-KURRENT-'1'-'2'-MISREAD!-11-vrstic!) + s29=22–32 (brano-32–42-+10!) + s30=33–40 + s31=41–51 + s32=52–60 + s33=61–68 + s34=69–78 + s35=79–87-P232! + s36=88–97-P232-križ! = 87-vrstic-okna (z11–z97!) + z1–z10-PRED-s28 (Jänner–März!-na-s26/s27!-X-open!) + z98-TAIL-s37-r1-P232! = ★★★ 98-VPISOV-1873 (z1–z98!) — vs-LEAD-'~95'-NADGRADJENO + ★★★ P232-X-open-'TAIL-zap-28[~98/lokalni-restart]'-REŠEN-1:1-'zap-98' (KURRENT-'9'-'2'-misread!-z97+1-ARITMETIKA!); "
    "★★★ MEJA-1872/73 = PRED-s28 (IZVEN-okna!-X-open): restart-z1-Jänner-1873-NA-s26/s27 ('finis-Anni-1872'/'Initium-1873'-kalligrafija-NI-v-oknu-Q4-9/9-negativno!) = 13.-restart-z1-linije (X-open-ARITMETIČNO-dokazan!) | TAIL-1873 = s36-r1–r10-zap-88–97-vsi-November-P232-1:1! + s37-r1-Dez-28/29-Kloster-zap-98!; "
    "★★★ 17-GRIBLJE / 16-hiš (h37-×2-DUEL-X-open-z19-vs-z81!-RAZLIČNI-družini!): z14-h16-ŠILAR-oče!-1.-v-oknu!-zap-[~14-X-ARITMETIKA!] + z18-h34-ŠILAR-oče!-DEBLIČ-matec! + z19-h37/27-DUEL-Maria-HRIČ-garble!-URH-botra!-DEBLIČ-botra! + z23-h13-JAKOFČIČ-oče!-ŠILAR-matec-KOMPLET!-MODRI-†28.12.1941!-retro-nota! + z28-h31/33-DUEL-Johann-PEZDIRC-oče-garble-X-★★★!-mesec-MAI-X-open! + z39-h49-BRODARIČ-oče!-PEZDIRC-×2-matec+boter-garble-★★★! + z47-h1-JAKOFČIČ-botra-DVOJNI-zakonca (PARALELA-P232-z2-1:1!)! + z51-h40-PEZDIRC-oče-garble-hipoteza!-MODRI-†12.3.1938!-h40-DUEL-continuum!-★zap-51-X! + z55-h69-vas-DUEL-GRIBLJE-zmaga!-PEZDIRC-botra-'Pedice'!-★zap-55-X! + z56-h74/64-DUEL-BRODARIČ-matec+botra-DVOJNI!-★zap-56-X! + z65-h8-BRODARIČ-matec!-DRAGOŠ-botra!-★zap-65-X! + z68-h22/42-DUEL-MILEK-vs-NOVAC-DUEL-X-★★★!-matec-PRAZNO/prečrtano-NEZ? + BRODARIČ-boter!-★zap-68-X! + z73-h53-PEZDIRC-×3-DVOJNI-oče+boter+matec-hipoteza-X-'Pezdirc'-EKSPPLICITNO!-DRAGOŠ-botra-KOMPLET!-POZICIJSKA-PARALELA-P232-z73! + z81-h37-X-REŠEN-LOGAR-oče-garble!-KLOBUČAR-botra!-full-MERGE-RAZREŠEN! + z92-h6-JAKOFČIČ-oče-X-★★★ (LEAD-JAKOŠA-REŠEN!)-DRAGOŠ-botra!-★zap-92-X! + z93-h62-HRIŽAN-matec-garble!-MILEK-botra-DUEL-X-open! + z94-h41/11-DUEL-Kaspar-KUMIĆ-DUEL-X-open-×3!-DRAGOŠ-matec!-SIMEC-boter!-JAKOFČIČ-botra-KOMPLET!-★zap-94-X! + "
    "★★★ PEZDIRC-×8-GARBLE-REKORD-PORAST (vs-×7-P232!-X-★★★-×3-eksplicitni!-grafija: Pezdirc/Perdisek/Ležir/Pedice/Pegdire/Bezdirč!) + JAKOFČIČ-×5-REKORD (PARALELA-P232-z2-zakonca-1:1!) + BRODARIČ-×6-REKORD-KOMPLET (oče+matec+botra!) + ŠILAR-×3-KOMPLET-NOVA-NIT + DRAGOŠ-×3-KOMPLET + DEBLIČ-×3 + MILEK-×1-DUEL-X-open + HRIŽAN-×1-garble + KLOBUČAR-×1 + URH-×1-garble + LEGDIRE-×2-garble + SIMEC-×1 + LOGAR-×1-garble + "
    "★★★ NEZAKONSKI-×1-X-open (z68-matec-PRAZNO/prečrtano!-vs-×0-P232!) + ★★★ MODRI-×2-Griblje (†28.12.1941!-†12.3.1938!-razpon-1938–1941!-+ne-G-MODRI-s36-kontrole!) + "
    "★★★ 4-PRAZNI-MESECI-REKORD-IZENAČEN (Jänner/Juni/September/Dezember!-M1+A3+Mai1+Juli3+Aug4+O2+N3 = 17!-vs-P232-BREZ-PRAZNIH!) + ★★★ PENT-duhovnikov-1873-X-open-GARBLE ('Dovgan'!-'Pihlár[?]'!-'Roblek-Kaplan'!-'Bobleh-Kaplan'!-'Dolenc[?]'!-vs-P232-TRI!-REKORD!) + s36-r9-PREČRTANO-ime + rdeči-tički-continuum ———\n"
)

blocks = P233_HEADER
for e in grib:
    blocks += gen_block(e)

i = src.index(ANCHOR)
src = src[:i] + blocks + src[i:]
TS.write_text(src, encoding="utf-8")
print(f"vstavljenih-blokov: {len(grib)} (PRED P232-anchor)")
