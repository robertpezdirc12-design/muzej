#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P227 — vstavi 22-GRIBLJE-blokov (krstna 04104, leto 1879 = 7/15!) v parish.ts PRED P226-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P226: krstna PREDZGODOVINA 04104, leto 1880"

E = json.load(open("/tmp/p227/entries_1879.json"))
grib = E["griblje_entries"]
assert len(grib) == 22, f"grib={len(grib)}"

P227_HDR = "  // ——— P227: krstna PREDZGODOVINA 04104, leto 1879"
if P227_HDR in src:
    i = src.index(P227_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P227-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}
MESEC_MAP = {"Jänner": "J", "Feber": "F", "Februar": "F", "März": "M", "April": "A", "Mai": "M2", "Juni": "J2", "Juli": "J3", "August": "A2", "September": "S", "October": "O", "November": "N", "December": "D", "Dezember": "D"}

KOM = {
 "z2": "★★★ RESTART-stran (z1=Kloster-h37-8./9.-JÄNNER-NAJPONEJŠI-restart! + VSOTNA-RAZPETA-'1 8'+'79'!) + BRODARIČ-matec-nit + h31 (z91-×2!)",
 "z11": "★★★ h68-nit (P223-GRIBLJE-h68-DVOJČKI-PARALELA!) + oče-garble-honesty",
 "z13": "★★★ KRIŽAN-DVOJNI-botra-nit (×2-v-vrstici!) + ★★★ MODRI-PRIPIS-'†-25.4.1949' (1.-Griblje-1879!)",
 "z20": "★★★ SIMEC-oče-nit (1/3!) + MILEK-matec-nit (1/6!)",
 "z21": "★★★ MODRI-PRIPIS-'†-30.12.1953' + JAKOFČIČ-oče-nit (1/5!) + rojen≠krsten-13/14 + DOVGAN-izmenjava",
 "z22": "★★★ MILEK-DVOJNI-nit (oče+boter!) + ★★★ PEZDIRC-matec-nit (1/5-Griblje!-continuum-7-let!) + h22 (z61-×2!)",
 "z23": "★★★ NEZAKONSKI-GRIBLJE (očetov-stolpec-PRAZEN!-P226-z114-PARALELA!) + PEZDIRC-botra-X-open (Poždire!)",
 "z28": "★★★ JAKOFČIČ-DVOJNI-nit (matec+botra!) + rojen≠krsten-10/13 (3-dnevi!) + h17 (z69-×2!)",
 "z30": "★★★ MODRI-PRIPIS-'†-19.9.1960' + MILEK-boter-nit + Juni-blok-start",
 "z33": "★★★ h49-DUEL-REŠEN-MAX-krop ('4'-odprta-NE-'1'!) + SIMEC-boter-nit + MUSIČ-DVOJNI-garble",
 "z39": "★★★ MODRI-PRIPIS-DOLG-'†-10.5.1962-v-Gribljah-št.65' + KLOBUČAR-matec+botra-X-open + h44 (P226-PARALELA!)",
 "z44": "★★★ JAKOFČIČ-DVOJNI-botra-nit (×2!) + KRIŽAN-matec-nit (4/4!) + h7 (P226-TOTER-PARALELA!)",
 "z49": "★★★ KLOBUČAR-oče-X-open (continuum!) + MILEK-matec + JAKOFČIČ-botra + August-blok-start + DOVGAN",
 "z61": "★★★ h22-×2-REŠEN-MAX-krop (z22!) + DRAGOŠ-matec-X-open (1/2!) + botra-garble-MAX",
 "z63": "★★★ MODRI-PRIPIS-'†-7.5.1945' + HURE-oče-nit (P226-PARALELA!) + KRIŽAN-matec-KOMPLET + MILEK + BRODARIČ + h62",
 "z69": "★★★ h17-×2-REŠEN-MAX-krop ('17'-1+γ-7!-z28!) + KLOBUČAR-oče-X-open + DOVGAN",
 "z74": "★★★ MODRI-PRIPIS-'†-20.1.1939' + BRODARIČ-boter-KOMPLET + KLOBUČAR-botra + h37-PARALELA-z1",
 "z78": "★★★ MILEK-oče-nit (5/6!) + ★★★ PEZDIRC-boter-X-open (Pozdire!) + KLOBUČAR-botra + h63 + Oktober-start",
 "z85": "DRAGOŠ-matec-X-open-KOMPLET + JAKOFČIČ-boter-KOMPLET + SIMEC-botra-KOMPLET + h11-PARALELA + November-start",
 "z91": "★★★ PEZDIRC-matec-nit (3/5!) + ★★★ MODRI-PRIPIS-'†-15.11.1965' + h31-×2 (z2!)",
 "z92": "★★★ TAIL-1879-ZAČETEK ('Jahr 1879'-glava-BREZ-VSOTNE-s-popravo-9čez7!) + MILEK-boter-KOMPLET (6/6!) + HURE-botra-X-open",
 "z95": "★★★ PEZDIRC-oče-nit (4/5!-LEAD-ŽE-VLM!) + ★★★ pripis-'†-15.6.1941' + ★★★ podpis-Franz-DOVGAN (izmenjava!) + TAIL-konec-+Schnörkel!",
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
    what_si = (f"krščena {e['otrok']} ({rojen}./{krsten}. {mesec_si_num}.) — oče {esc(e['ocec'])}, mati {esc(e['matec'])}; "
               f"botra {esc(e['botra'])}; + {kom} + pag-konvencija-sken−6 + [z{z[1:]}]")
    what_en = (f"baptized {e['otrok']} ({mesec_en} {rojen}/{krsten}) — father {esc(e['ocec'])}, mother {esc(e['matec'])}; "
               f"godparents {esc(e['botra'])}; + [see-SI] + [z{z[1:]}]")
    return (
        "  {\n"
        f'    houseNo: "{e["hisna"].split()[0]}",\n'
        '    bookSignature: "04104",\n'
        "    year: 1879,\n"
        f"    scan: {sk},\n"
        f"    page: {pag},\n"
        f'    whatSi: "{what_si}",\n'
        f'    whatEn: "{what_en}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

P227_HEADER = (
    "  // ——— P227: krstna PREDZGODOVINA 04104, leto 1879 = 7/15 — (s106–s119 == gola-svinčna-pag-'sken−6' "
    "(14/14-SEKVENČNO: s106='100'/s107='101'/s108='102'/s109='103'/s110='104'/s111='105'/s112='106'-LEAD-PREDICTION-POTRJENA!"
    "/s113='107'/s114='108'/s115='109'/s116='110'/s117='111'/s118='112'/s119='113'-P226! — 100–113-brez-luknje-v-1879-oknu!; "
    "2×-neodvisna-prenosa-md5-15/15!); ★★★ MEJA-1878/79-s105/s106 (TAIL-1878-z90–z94-Dez-23–30 + VSOTNA-RAZPETA-'1 8'+'79'-"
    "razpeta-čez-obe-strani! + glava-'Jahr 1878'-s-popravo-cifre! + RESTART-z1-NA-DAN-8./9.-JÄNNER-Kloster-h37-Maria-†19.7.1942-MODRI!-"
    "7.-restart-z1-NAJPONEJŠI!-P221-1.1!-P222-1.1!-P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!) = 66.-POTRDITEV-invariante! (65.-P226!); "
    "96-vpisov-DISTINCT — vrstna-aritmetika 2+8+7+7+6+6+7+8+8+9+8+7+8+5 = 96 = P226-LEAD-'1879-=-96-vpisov-BONUS'-1:1-INVARIANTA! "
    "(zap-stolpci-14/14-ČISTO!); ★★★ 22-GRIBLJE / 19-hiš (h31-×2: z2+z91! + h22-×2: z22+z61! + h17-×2: z28+z69!-DUELI-REŠENI-MAX-krop!) "
    "+ ★★★ PEZDIRC-×12-vrstic (z51-DVOJNI! + z67-DVOJNI!-ne-Griblje! + z22/z91-matec + z95-oče-in-Griblje!) — grafija-continuum-7-let! "
    "+ KRIŽAN-×4 (z13-DVOJNI!) + MILEK-×6 (z22-DVOJNI!) + JAKOFČIČ-×5+×3-neG (z28/z44-DVOJNI!) + SIMEC-×3-KOMPLET + BRODARIČ-×3-KOMPLET "
    "+ KLOBUČAR-×5-X-open + HURE-×2 + DRAGOŠ-×2 + ★★★ DVOJČKI-ZWILLINGE-×3-REKORD (z47/48 + z55/56 + z65/66!-vse-z-pisarjevo-"
    "'Zwillinge'-vertikalno-anotacijo + zavitim-oklepajem!-vs-×1-P223-×1-P226!) + ★★★ TODTGEBOREN-garble-×3 (z15/z57/z66!-krsten+botra+"
    "duhovnik-VSI-PRAZNI!-Mißgeburt-P226-PARALELA!-1.-dvojček-todtgeboren!) + ★★★ z23-NEZAKONSKI-GRIBLJE (očetov-stolpec-PRAZEN!) "
    "+ ★★★ MODRI-MATIČARSKI-PRIPISI-×12-REKORD-LINJE (×7-Griblje: z13/z21/z30/z39/z63/z74/z91! + ×5-ne-G!) + ★★★ DUHOVNIŠKA-IZMENJAVA-1879 "
    "('Janičar-coep' ↔ 'Dovgan'-ALTERNIRAJOČE-čez-celo-leto!-Griblje-split-11/22!-vs-1880-čista-menjava-z106!-z60-pripis-'B.Dog'!) "
    "+ z60-POGOJNI-KRST ('sub-conditione-die-27.-Augusti-1879-B.Dog'!) + z32-IMENSKI-POPRAVEK (Anna→prečrtano-Johann→Anna + ✗!) "
    "+ z76-DATUMSKI-PRIPIS ('…-gebären-am-[21~26].-Decemb-1879'!-Z49-PARALELA!) + z42-HEBAMME-Maria-Rom (rojen≠krsten-10/13!) "
    "+ meseci-Griblje: J1+F2+A5+Juni2+Juli2+A2+S3+O1+N2+D2 (März/Mai-×0!) ———\n"
)

blocks = P227_HEADER
for e in grib:
    blocks += gen_block(e)

i = src.index(ANCHOR)
src = src[:i] + blocks + src[i:]
TS.write_text(src, encoding="utf-8")
print(f"vstavljenih-blokov: {len(grib)} (PRED P226-anchor)")
