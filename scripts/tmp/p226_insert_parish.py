#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P226 — vstavi 22-GRIBLJE-blokov (krstna 04104, leto 1880 = 6/15!) v parish.ts PRED P225-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P225: krstna PREDZGODOVINA 04104, leto 1881"

E = json.load(open("/tmp/p226/entries_1880.json"))
grib = E["griblje_entries"]
assert len(grib) == 22, f"grib={len(grib)}"

P226_HDR = "  // ——— P226: krstna PREDZGODOVINA 04104, leto 1880"
if P226_HDR in src:
    i = src.index(P226_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P226-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}
MESEC_MAP = {"Jänner": "J", "Feber": "F", "Februar": "F", "März": "M", "April": "A", "Mai": "M2", "Juni": "J2", "Juli": "J3", "August": "A2", "September": "S", "October": "O", "November": "N", "Dezember": "D"}

KOM = {
 "z10": "★★★ oče-garble-MAX (Alebee/AHebee!) + KLOBUČAR-boter-nit-X-open (continuum!) + JAKOFČIČ-matec-nit (1/6!) + Feb-6/7",
 "z11": "★★★ JAKOFČIČ-DVOJNI-nit (oče+matec-isti-priimek!-P225-z28-PARALELA!) + pripis-MMK-'†-21.8.1935' + DRAGOŠ + ŽELKO-botra",
 "z14": "★★★ SIMEC-oče-nit (×3-leta!) + JAKOFČIČ-matec + BRODARIČ-boter-nit + botra-×3",
 "z26": "★★★ MODRI-MATIČARSKI-PRIPIS-'umrla-25.5.1969' + JAKOFČIČ-oče + KRIŽAN-matec-nit + hiša-'13' (P222/P224-×2!)",
 "z31": "★★★ ŽELKO-DVOJNI-nit (oče+botra!) + KRIŽAN-DVOJNI-nit (matec+boter!) — DVE-DVOJNI-MREŽI-v-vrstici!",
 "z35": "★★★ PEZDIRC-DVOJNI-nit (oče-Joannes + matec-Perdiče!-P225-z55-PARALELA!) + BRODARIČ + DRAGOŠ-botra",
 "z36": "KRIŽAN-oče-nit + boter-DUEL-garble (Pevlho/Pozlho!) + Mär-31-TAIL",
 "z46": "★★★ MODRI-PRIPIS-'umrla-23.5.1957' + MILEK-boter-nit + BRODARIČ-botra-nit + Mai-labela-z46-VIZUALNO + h27 (z54-×2!)",
 "z51": "★★★ SIMEC-boter-nit (2/3!) + oče-garble (Periže!) + hiša-'19 [~]'",
 "z54": "★★★ h27-×2-REŠEN (z46!-oba-'27'-VIZUALNO!) + JAKOFČIČ-botra-nit + matec-Hrumbič-PARALELA-z46",
 "z58": "★★★ TOTER-garble-oče (P225-z30-PARALELA!) + SIMEC-boter-nit (3/3-KOMPLET!) + botra-DUPLIKAT-matec-priimek + Mai-29/30",
 "z61": "BRODARIČ-botra-nit (4/4-KOMPLET!) + QUAD-garble-honesty-MAX + hiša-'21' (P221-z1-PARALELA!)",
 "z65": "JAKOFČIČ-matec-nit (5/6!) + h24-×2-REŠEN (z72!) + hiša-'24' (P225-z71-PARALELA!)",
 "z69": "★★★ KRIŽAN-DVOJNI-nit (matec+botra!-P225-z81-PARALELA!) + PEZDIRC-oče-X-open (Pediče!) + hiša-'42' (P225-z81!)",
 "z72": "★★★ MILEK-botra-nit (3/4!) + HRIŽAN-matec-nit + h24-×2-REŠEN (z65!) + pag-'123'-VIZUALNO",
 "z88": "HURE-oče-nit + SEP-blok + botra-pripis-garble (Mögniglein!) + hiša-'10'",
 "z89": "★★★ pripis-MMK-'†-13.9.1940' + LASIE~LAZAR-grafija-X-open (P220/P222-nit!) + QUAD-garble-honesty-MAX",
 "z95": "PENT-garble-honesty-MAX (Timec!-Mihelk!-Žunič!-Jakopeič!-Levim!) + Okt-15/16 + 'October'-labela-VIZUALNO (VLM-'December'-REŠEN!)",
 "z99": "★★★ PEZDIRC-DVOJNI-nit (botra+boter!-P225-z55-PARALELA!) + oče-DUEL-garble (Dešlič/Deflič!) + matec-Husič-PARALELA-z54",
 "z101": "★★★ MILEK-oče-nit + KRIŽAN-matec-nit + boter-DUEL (Adleveč/Adamič!) + hiša-'29' (P223-z97!) + duhovnik-DUEL",
 "z104": "★★★ KRIŽAN-matec-nit (9/9-REKORD!) + POŽEK-oče-X-open (Pozelj/Pozek!) + hiša-'44 [~]' + NOV-blok",
 "z114": "★★★ NEZAKONSKI-vzorec (očetov-stolpec-PRAZEN!-7.-nezakonski-1880!) + DEZ-1/2 + HRIŽAN-botra-nit + matec-DVOJNI-garble-MAX",
}

def esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')

def clean_day(d):
    d = str(d or "").strip().rstrip(".")
    d = d.split()[0] if d else "?"
    return d if d else "?"

def gen_block(e):
    z = e["z"]
    ime = (e.get("otrok") or "?").strip()
    ocec = (e.get("ocec") or "").strip()
    matec = (e.get("matec") or "").strip()
    botra = (e.get("botra") or "").strip()
    mesec = (e.get("mesec") or "").strip()
    rojen = clean_day(e.get("rojen"))
    krsten = clean_day(e.get("krsten"))
    kom = KOM.get(z, "")
    import re as _re
    pag_raw = str(e.get("pag") or "")
    _pm = _re.match(r"(\d+)", pag_raw)
    pag_int = int(_pm.group(1)) if _pm else 0
    if "[" in pag_raw and kom:
        kom += " + pag-konvencija-sken−6"
    hisna_raw = str(e.get("hisna") or "[?]")
    hisna = hisna_raw.split(" ")[0].strip("[],")
    if hisna.startswith("[") or hisna == "":
        hisna = "[?]"
    mm = MESEC_MAP.get(mesec, "")
    mnum = MESEC_SI.get(mm, "")
    men = MESEC_EN.get(mm, mesec or "?")
    mpart = f"{mnum}." if mnum else "[?]"
    what = f"krščena {ime} ({rojen}./{krsten}. {mpart})"
    if ocec: what += f" — oče {ocec}"
    if matec: what += f", mati {matec}"
    if botra: what += f"; botra {botra}"
    if kom: what += f"; + {kom}"
    what += f" + [{z}]"
    what_en = f"baptized {ime} ({men} {rojen}/{krsten})"
    if ocec: what_en += f" — father {ocec}"
    if matec: what_en += f", mother {matec}"
    if botra: what_en += f"; godparents {botra}"
    what_en += "; + [see-SI]" + f" + [{z}]"
    return (
        "  {\n"
        f'    houseNo: "{esc(hisna)}",\n'
        '    bookSignature: "04104",\n'
        "    year: 1880,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {pag_int},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P226: krstna PREDZGODOVINA 04104, leto 1880 = 6/15 — (s119–s135 == gola-svinčna-pag-'sken−6' "
    "(17/17-SEKVENČNO: s119='113'/s120='114'/s121='115'/s122='116'/s123='117'/s124='118'/s125='119'/s126='120'/"
    "s127='121'/s128='122'/s129='123'-VLM-'129'-misread-9↔3-REŠEN!/s130='124'/s131='125'/s132='126'-VLM-VIZUALNO!/"
    "s133='127'-VLM-'124'-misread-4↔7-REŠEN!/s134='128'/s135='129'! — 113–129-brez-luknje-v-1880-oknu!; "
    "2×-neodvisna-prenosa-md5-17/17!); ★★★ MEJA-1879/80-s119/s120 (TAIL-1879-z92–z96-Dez-17–30 + Schnörkel + "
    "'Jahr 1879'-BREZ-VSOTNE! + velike-cifre-'1/8/8/0'-P214-TIP + 'Jahr 1880'-glava + RESTART-z1-NA-DAN-3.-1.-"
    "JÄNNER-Dobravce-h11-Martin!-5.-restart-z1!) = 65.-POTRDITEV-invariante! (64.-P225!); 122-vpisov-DISTINCT — "
    "vrstna-aritmetika 8+9+9+8+7+9+7+6+7+8+7+8+8+7+7+7 = 122 = P225-LEAD-'1880-=-122'-1:1-INVARIANTA! "
    "(zap-stolpci-16/16-ČISTO!); ★★★ 22-GRIBLJE / 20-hiš (h27-×2 + h24-×2-DUELI-REŠENI-1:1!) + ★★★ "
    "PEZDIRC-×14-NOV-REKORD-LINJE (z35-oče+matec-DVOJNI! + z99-botra+boter-DVOJNI! + ×10-ne-Griblje!) — "
    "grafija-continuum-6-let! + KRIŽAN-×9 (2-DVOJNI-vrstici: z31!-z69!) + JAKOFČIČ-×10-skupaj (z11-DVOJNI!) + "
    "MILEK-×4 + SIMEC-×3 + BRODARIČ-×4 + ŽELKO-×4 (z31-DVOJNI!) + DRAGOŠ-×2 + HRIŽAN-×2 + TOTER-garble (z58!-"
    "P225-PARALELA!) + LASIE~LAZAR-X-open (z89!) + POŽEK-X-open (z104!) + KLOBUČAR-X-open (z10!) + HURE (z88!) + "
    "★★★ DVOJČKI-Boršt-h20-z5/z6 (ne-Griblje!-isti-starši-Rovačič!-pisarjev-oklepaj!-P223-GRIBLJE-h68-PARALELA!) + "
    "★★★ Mißgeburt-'Mößgelauffer'-×2 (z76/z77!-Stillgeburt-brez-boter!) + ★★★ z110-KRSTEN-DAN-PRAZEN + BOTRA-PRAZNA + "
    "★★★ NEZAKONSKI-×7-REKORD (očetov-stolpec-PRAZEN!-z30/z56/z59/z79/z85/z100 + z114-GRIBLJE!) + ★★★ "
    "MODRI-MATIČARSKI-PRIPISI-×9-REKORD (1963–1990!-z21/z26/z46/z55/z56/z68/z70/z83/z91!) + pripisi-MMK-†-×7 "
    "(z11-†1935! + z89-†1940! + z42/z45/z25/z105/z112!) + Z49-datumski-popravek ('den-17.-Juli-1880-zuzschreiben'!) + "
    "Z100-imenski-popravek (Alois→Alojzija + att.!-P221-PARALELA!) + z79-JULI-VLM-misread-REŠEN (krop!-'…ember/Juni'-failure-continuum!) + "
    "z15-FEB-20-SANDWICH (VLM-'29'-9↔0-ZAVRNJEN-po-kronologiji!-prestupno-leto-brez-Feb-29!) + "
    "DUHOVNIŠKA-MENJAVA (Janičar-coep→Dovgan-okoli-z106! + z101-tretji-podpis!) + meseci-Griblje: "
    "F3+M4+Mai3+J2+Juli2+S2+O3+N1+D1 (Jänner/April/August-×0!-Feb-prestupno!) ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count('year: 1880,\n    scan:')
print(f"vstavljenih blokov 1880-04104: {n} (pričakovano 22)")
