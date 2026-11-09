#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P235 — vstavi 17-GRIBLJE-blokov (krstna 04104, leto 1871 = 15/15 — LINIJA KOMPLETNA!) v parish.ts PRED P234-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P234: krstna PREDZGODOVINA 04104, leto 1872"

E = json.load(open("/tmp/p235/entries_1871.json"))
grib = E["griblje_entries"]
assert len(grib) == 17, f"grib={len(grib)}"

P235_HDR = "  // ——— P235: krstna PREDZGODOVINA 04104, leto 1871"
if P235_HDR in src:
    i = src.index(P235_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P235-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}
MESEC_MAP = {"Jänner": "J", "Feber": "F", "Februar": "F", "März": "M", "April": "A", "Mai": "M2", "Juni": "J2", "Juli": "J3", "July": "J3", "August": "A2", "September": "S", "October": "O", "November": "N", "December": "D", "Dezember": "D"}

KOM = {
 "z13": "★★★ 1.-GRIBLJE-1871 = z13 (Februar!-Jänner-×0-GRIBLJE!-vs-1872-1.-vpis-leta-GRIBLJE-z1!-VZOREC-PREKINJEN!) + BRINE-matec-nit (1/2!) + BRODARIČ-botra-garble + duhovnik-Weisel-Cap.-obdobje (z1–z13!)",
 "z16": "★★★ BRINE-oče-nit (2/2-KOMPLET-z13!) + ★★★ MILIČ-matec-'Mihelik'-hipoteza (1/5-MILIČ-nit!-MILEK?-X-open-PARALELA-P234-'Milhoeluc'!) + duhovnik-JAKOB?-zamenjava (z14–z19!-DUHOVNIŠKA-MEJA-z13/z14!)",
 "z18": "HRIŽAN-matec-nit (1/9!-Križan-continuum!) + h60 (PARALELA-1874-z57-h60!-×2-v-3-letih!) + oče-garble-SCHELKO",
 "z25": "★★★ vrstica-ZELO-BLEDA (X-open-×4-polja!) + h5 + duhovnik-DOTTO.-EKSPPLICITEN (z20–z41!) + KLAR-matec-garble-PARALELA-z34",
 "z34": "★★★ PEZDIRC-boter-nit-'Peter-Pezdirc' (1/8!-EKSPPLICITNO!-'Peter'-×3-linije-z34/z40/z81!) + KLAR-oče-garble + STRUČELJ-botra (1st!)",
 "z35": "★★★ †-pripis-'geboren-1885?-+1939?'-X-open-NEBERLJIV (anomalija!) + TOMC-DVOJNI-oče+botra-nit (KOMPLET!) + h4",
 "z44": "★★★ h69-CONTINUUM (z44-1871!-+z97-1872!-+z55-1873!-×3-v-3-letih-RAZLIČNI-družini!) + rojen≠krsten-8/9 + BRINE-botra-garble (3rd!) + duhovnik-FERŠLAN-Pfr.-obdobje (z42–z52!)",
 "z46": "★★★ DRAGOŠ-DVOJNI-oče+matec-nit (1/6+2/6!-Griblje-h12!) + ★★★ JAKOFČIČ-DVOJNI-boter+botra-nit (1/7+2/7!) + duhovnik-D.-FERŠLAN-Pfr.-EKSPPLICITEN + h12-CONTINUUM-z59-1872-PEZDIRC (×2-v-2-letih-RAZLIČNI!)",
 "z69": "★★★ SAKOFČIČ-×3-TROJNI-block (matec+boter+botra!-JAKOFČIČ-garble-'S'-for-'J'!) + h1 (PARALELA-1873-z47-h1!-×2-v-2-letih!) + DVOJČKI-stran (s10!)",
 "z80": "★★★ KLOBUČAR-oče-nit-EKSPPLICITEN (1/5!-X-zoom-POTRJEN!) + ★★★ matec-'Pez-Jure'-PEZDIRC?-hipoteza-X-OPEN (DUEL-'Požek-Jure'!) + BRODARIČ-boter-nit + STRUČELJ-botra (2nd!) + zap-80-X-POTRJEN",
 "z81": "★★★ PEZDIRC-oče-EKSPPLICITEN-'Peter-Pezdirc-in-Griblach' (2/8!-X-ZOOM-1:1-POTRJEN!-h28-PETER-PEZDIRC-družina!-PETER-×3!) + ★★★ hisna-28/20-DUEL-X-open (KURRENT-2/8!) + ★★★ DEBLIČ?-matec-garble-'Dehlič' (X-open-continuum-P234-'Deblin'!) + MILIČ-botra-nit (2/5!) + KLOBUČAR-botra-nit (2/5!) + zap-81-X-'1'-črtica",
 "z83": "★★★ h28-×2-DELO-DUEL (z81-Pezdirc!-vs-z83-Požek!-RAZLIČNI!-3.-LETO-VZOREC-h30-h37-h28!) + ★★★ POŽEK-oče-nit (matec-z80-'PožJure'-continuum-1:1-OJAČANA!) + MILIČ-botra-nit (3/5!-2×-ISTI-botra!) + HRIŽAN-botra-garble (2/9!)",
 "z91": "★★★ KRSTEN-PRAZNO-'—' + BREZ-BOTER + BREZ-PODPISA (X-★★★-X-open: totgeboren?/nepisan!-vs-z30-totgeboren!) + MILIČ-oče-nit (4/5!) + KLOBUČAN-matec-garble (3/5!) + h65",
 "z92": "★★★ skupni-PODPIS-92/93-'Wilhelm-Wenzel?-Coop.' (X-★★★-WEISEL/WENZEL/WESSELY-garble-continuum!) + DRAGOŠ-matec+botra-nit (3/6+4/6!) + STRUČELJ-botra (3rd!) + h72",
 "z96": "★★★ MILIČ-oče-nit-KOMPLET (5/5!-MILIČ-×5-oseb-1871-REKORD!-MILEK?-X-open!) + matec-garble-TRNIČAN (DUEL-'Frižan'!) + botra-garble-ŠTLER-continuum + h26[?]",
 "z98": "★★★ TAIL-VERIGA-z98 (X-★★★-'98'-1:1-POTRJEN!-GRIBLJE-v-TAIL!) + JAKOFČIČ-garble-'Sakotovič'-oče (6/7!-SAK-continuum!) + DRAGOŠ-botra-nit (5/6!) + h6 (PARALELA-1872-z63!) + duhovnik-DANIEL-WESSELY-cop.-EKSPPLICITEN (WEISEL/WESSELY-garble-X-open!)",
 "z103": "★★★ TAIL-1871 = z108 (z103-pred-tail-GRIBLJE!-Dez-22!) + KUKE-DVOJNI-oče+botra-nit (KOMPLET!-'Kuke/Kukej'!) + ŠKALA-matec-continuum + duhovnik-'Po-ista-roka'-garble (continuum-z98!)",
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
        "    year: 1871,\n"
        f"    scan: {sk},\n"
        f"    page: {pag},\n"
        f'    whatSi: "{what_si}",\n'
        f'    whatEn: "{what_en}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

P235_HEADER = (
    "  // ——— P235: krstna PREDZGODOVINA 04104, leto 1871 = 15/15 — LINIJA KOMPLETNA! — (s3–s13 == 11 skenov ODPRTJE-KNJIGE (s1-vezava-0-vrstic!-s2-naslovna-'Tauf-Buch.'-0-vrstic!-arhivski-nalepek-'PODZEMELJ-R-1871-1885'!-s3–s13-'Jahr 1871'-11/11-glave!-s14-ŽE-1872-P234!-DESCENDING-probe-P234-LEAD-s9–s13-NADGRAJENO-s3–s13!-2×-md5-14/14!); "
    "★★★ FOLIACIJA-'sken−3'-KOMPLETNA-FORMULA-KNJIGE-s3–s14 (s3='1'!-s4='1'-★★★ DUPLIKAT!-s5='2'-...-s13='10'!-s14='11'-P234!-12/12!-SKOK-NA-DUPLIKATU-s4→s5-'1'→'2'-PARALELA-s29→s30-P234!-2-DUPLIKATA-KNJIGE: s3=s4-fol-1 + s28=s29-fol-25-P234!); "
    "★★★ 108-VPISOV-ARITMETIČNI-MODEL (z1–z108!-SEKVENČNO-1:1-10/10-strani!): s3=1–8 (8!-z1-RESTART-13.-restart!-ODPRTJE-ZVEZKA!) + [s4=DUPLIKAT-s3-fol-1!] + s5=9–19 (11!-z9-POST-DUPLIKAT-X!) + s6=20–30 + s7=31–41 (z37/z38-PREČRTANI!) + s8=42–52 + s9=53–64 + s10=65–74 (z72/z73-DVOJČKI-ZWILLINGE!) + s11=75–86 (z80/z81/z83-X!) + s12=87–96 (z91-KRSTEN-PRAZNO!) + s13=97–108 (TAIL-VERIGA-3/3!-z108-TAIL-Dez-31!) = ★★★ 116-vrstic-−-8-DUPLIKAT = 108-DISTINCT-VPISOV — vs-LEAD-'~90–110'-POTRJENO-1:1; "
    "★★★ MEJA-1870/71 = ZAČETEK-KNJIGE (s2/s3!-EDINSTVENO-LINIJE!): s1 = vezava + s2 = tiskana-naslovna-'Tauf-Buch.' (+ arhivski-nalepek-'PODZEMELJ-R-1871-1885'-★★★ KNJIGA = 15-LET-LINIJA-1:1!) + s3-r1 = z1-RESTART-Jänner-3-KRASINEC-h27 (13.-restart!-1.-vpis-leta = KRASINEC-NOT-GRIBLJE!-VZOREC-PREKINJEN!) | MEJA-1871/72 = s13/s14-PAGE-BOUNDARY (P234-1:1!-re-use!): s13-TAIL-z108-Dez-31-Otok (TAIL-VERIGA-3/3-X!-BREZ-'finis'-kalligrafije-Q4-5/5!-plain-PARALELA-1872!) + s14-r1 = z1-GRIBLJE (12.-restart-P234-SUPER!); "
    "★★★ DUPLIKAT-s3 = s4-RESITEV (P234-'1-DUPLIKAT-s1–s13'-UGE-REŠENA-1:1!-fol-1-2×-SKENIRAN!-s3-r1 = s4-r1-'Jänner-3'-1:1-obe!-X-K2-'1'-+ vlepljeni-list-s4!-★★★ 2-DUPLIKATA-KNJIGE-KOMPLETNA-REŠITEV: s3=s4-fol-1 + s28=s29-fol-25!-108-TOTAL-1871-INTAKTEN-1:1!) + "
    "★★★ 17-GRIBLJE / 16-hiš (h28-×2-DUEL-z81-Pezdirc!-vs-z83-Požek!-RAZLIČNI!-3.-LETO-VZOREC-h30-h37-h28!-+ X-hisna-z81-28/20!): z13-h24-1.-GRIBLJE-1871-Februar! + z16-h23-BRINE-KOMPLET-MILIČ-'Mihelik'-hipoteza! + z18-h60-HRIŽAN-matec! + z25-h5-ZELO-BLEDA-DOTTO! + z34-h46-PEZDIRC-boter-'Peter'! + z35-h4-TOMC-DVOJNI-†-pripis! + z44-h69-CONTINUUM-×3! + z46-h12-DRAGOŠ-DVOJNI-oče+matec!-JAKOFČIČ-DVOJNI-boter!-FERŠLAN! + z69-h1-SAKOFČIČ-×3-TROJNI-garble! + z80-h48-KLOBUČAR-oče-X!-'Pez-Jure'-hipoteza! + z81-h28-★★★-'Peter-Pezdirc'-EKSPPLICITNO-X-ZOOM-1:1!-hisna-28/20-DUEL!-DEBLIČ?-'Dehlič'! + z83-h28-★★★-DUEL-POŽEK-oče!-MILIČ-botra-2×! + z91-h65-KRSTEN-PRAZNO-BREZ-botra!-MILIČ-oče! + z92-h72-PODPIS-Wenzel?-WEISEL-continuum!-DRAGOŠ-matec+botra! + z96-h26[?]-MILIČ-KOMPLET-×5! + z98-h6-TAIL-VERIGA-X!-SAKOTOMIČ-garble!-WESSELY-cop.! + z103-h10-pred-tail!-KUKE-DVOJNI! + "
    "★★★ PEZDIRC-×8-'Peter'-×3-linije (z81-oče-X-POTRJEN!-z34-z40-boter!-z32-matec+botra!-z84-matec+boter!-z88-garble!-z80-'Pez-Jure'-hipoteza!-vs-×5-1872!-×8-1873!) + ★★★ MILIČ-×5-oseb-REKORD (z16-'Mihelik'-matec-hipoteza!-z81-z83-boter-2×-ISTI!-z91-z96-oče!-MILEK?-X-open-continuum!) + ★★★ JAKOFČIČ-×11-ish-REKORD-LINIJE (×7-eksplicitni!-SAKOFČIČ-×4-garble-'S'-for-'J'!-z69-TROJNI!-z98!-vs-×5-1873!) + ★★★ HRIŽAN-×9-oseb-REKORD (Križan/Križanič/Krlžan/Kricžan-continuum!) + ★★★ KLOBUČAR-×5 ('Klobučan'-garble!-z80-oče-X!) + ★★★ BRODARIČ-×5 + ★★★ DRAGOŠ-×6-oseb (z46-DVOJNI-oče+matec!-'Dragaš'-z92!-vs-×3-1872/1873!) + ŠKALA-KUKE-TOMC-BRINE-STRUCHELJ-POŽEK-niti + "
    "★★★ DUHOVNIKI-1871-EKSTRAHIRANI-1:1 (1872-X-open-LEKCIJA-UPOŠTEVANA!): Wilhelm-Weisel-'D.H.-Cap.'-z1–z13 + Jakob?-z14–z19 (MEJA-z13/z14!) + Dotto.-z20–z41 (ekspliciten-z25!) + D.-Feršlan-'Pfr.'-z42–z52 (ekspliciten-z46!) + Daniel?-z53–z64-X-open + neberljivi-paraf-s11 + Wilhelm-Wenzel?-Coop.-z92/93 (skupni-podpis!) + Daniel-Wessely-'cop.'-z98 (ekspliciten!) + 'Po-ista-roka'-z103 — ≥4-eksplicitnih-imen + ★★★ WEISEL/WENZEL/WESSELY-garble-continuum-ista-oseba?-X-open! + "
    "★★★ z72/z73-DVOJČKI-'Zwillinge'-pripis-X-POTRJEN (Boršt-h20!-Georg+Catharina!-1.-DVOJČKI-linije!) + ★★★ z37/z38-PREČRTANI-DVOJNI (Krasinec-h12-Harasinič!-April-22!-vijugasta-črta!-mrtvorojeni?-X-open!-vs-P234-1-prečrtana!) + z30-TOTGEBOREN-Dragoše (krsten-'—'!) + z91-KRSTEN-PRAZNO-BREZ-botra-BREZ-podpisa (Griblje-h65-MILIČ!-X-open!) + ★★★ NEZAKONSKI-×1 (z29-oče-PRAZNO!-Gradac-h49!-PARALELA-1873!) + ★★★ MODRI-×3-arhivski-pripisi ('umrl-20.12.1957'-★★★ 1957-NAJNOVEJŠI-LINIJE!-'1940'-'1953'!-razpon-1940–1957!-vs-×4-1872!) + "
    "★★★ JÄNNER-×0-+ JUNI-×0-GRIBLJE (2-prazna-meseca-1871!-vs-1872-Sep!-vs-1873-4!-vs-1874-BREZ!) + h69-×3-CONTINUUM-v-3-letih (RAZLIČNI!) + h12-CONTINUUM (z46-DRAGOŠ-1871→z59-PEZDIRC-1872!) + h24-×2 (z13-1871→z47-1872!) + h1-×2 (z69-1871→z47-1873!) + h60-×2 (z18-1871→z57-1874!) + rdeči-tički-continuum-'Lamim'-noty-'E-125.2.1933'-z42 ———\n"
)

blocks = P235_HEADER
for e in grib:
    blocks += gen_block(e)

i = src.index(ANCHOR)
src = src[:i] + blocks + src[i:]
TS.write_text(src, encoding="utf-8")
print(f"vstavljenih-blokov: {len(grib)} (PRED P234-anchor)")
