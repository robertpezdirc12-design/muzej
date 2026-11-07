#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P223 — vstavi 19-GRIBLJE-blokov (krstna 04104, leto 1883 = 3/15!) v parish.ts PRED P222-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P222: krstna PREDZGODOVINA 04104, leto 1884"

E = json.load(open("/tmp/p223/entries_1883.json"))
grib = E["griblje_entries"]
assert len(grib) == 19, f"grib={len(grib)}"

P223_HDR = "  // ——— P223: krstna PREDZGODOVINA 04104, leto 1883"
if P223_HDR in src:
    i = src.index(P223_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P223-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}

KOM = {
 "z5": "★★★ MESEC-KOREKCIJA (carry-over-'Jänner' — page-'Feber'-sklepanje-ZAVRNJENO!) + pripis-MMK-'umrla-18.12.1962'-X-open!",
 "z7": "★★★ PEZDIRC-grafija-oče (Perdiče!) + BRODARIČ-botra-nit!",
 "z17": "★★★ STRUCELJ-×2-nit (mati+botra!) + SIMEC-botra + pripis-garble-X-open!",
 "z22": "★★★ SIMEC-oče-nit + BRODARIČ-botra + pripis-MMK-'umrla-6.1.1940-90-let'!",
 "z25": "★★★ MÄRZ-LABEL-KOREKCIJA (z24-'März'-hi — page-'Mai'-MISREAD!) + DRAGOŠ-botra-nit + KLOBUČAR!",
 "z28": "★★★ MÄRZ-KOREKCIJA + BRODARIČ-botra-nit + hisna-'35'-X-open!",
 "z32": "★★★ PEZDIRC-mati-nit (Perdče!) + ZUPANIČ + pripis-MMK-'umrla-1957'-KOREKCIJA (page-'poročena'-MISREAD!)",
 "z43": "★★★ hiša-DUEL-REŠEN (17!-'42'-preliv-iz-'1942'-ZAVRNJEN!) + SIMEC-botra + pripisa-MMK ('poročen-1919'+'H-1942')!",
 "z52": "★★★ PEZDIRC-oče+mati-DVOJNI-nit (Peršinc+Perdine!) + hisna-'55-vs-65'-DUEL-X-open!",
 "z58": "★★★ HLEBEC-botra-nit + pripis-MMK-'umrla-8.10.[1959/1960]'-garble-X-open!",
 "z59": "★★★ MILEK-MIHELČ-botri-nit + pripis-MMK-'Mrt.-10.7.1985-št.57'-KOREKCIJA (page-'1965'-MISREAD!)!",
 "z61": "★★★ hiša-DUEL-REŠEN (90-2:1-vs-'70'-γ/9!) + garble-gostota-honesty!",
 "z73": "★★★ hiša-'1'-VIZUALNO (prva-1883!) + LESKO-×3-nit + mati-Kure-nit!",
 "z76": "★★★ hiša-KOREKCIJA (56!-vs-page-'51'-1/6!) + ime-TRI-garble-honesty + PEZDIRC-botra (Pozdire!)",
 "z78": "★ hiša-'37'-2:1 (γ-forma!-'sy'-ZAVRNJEN — paralela-P222-z1!)",
 "z88": "★★★ hiša-'25'-VIZUALNO + h25-×2 (2/2!) + P222-LEAD-POTRJEN (Borre!)",
 "z94": "★★★ DRAGOŠ-mati-nit (2/2!) + pripis-MMK-'Cop.-1910-Pilteburg[?]'-X-open!",
 "z96": "★★★ hiša-DUEL-REŠEN (63!-2:1-vs-'18') + PEZDIRC-mati+botra-DVOJNI-nit (Peddire-×2!)",
 "z97": "★★★ KRIŽAN-×2-nit (mati+botra!) + hiša-'29'-VIZUALNO!",
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
    # pag: int (garble-pripis → kom!)
    import re as _re
    _pm = _re.match(r"(\\d+)", str(e.get("pag") or ""))
    pag_int = int(_pm.group(1)) if _pm else 0
    _pgarb = str(e.get("pag") or "")
    if "[" in _pgarb and kom:
        kom += " + pag-garble-" + _pgarb.split("[", 1)[1].rstrip("]")
    hisna_raw = str(e.get("hisna") or "[?]")
    hisna = hisna_raw.split(" ")[0].strip("[],")
    if hisna.startswith("[") or hisna == "" or "DUEL" in hisna_raw:
        hisna = "[?]"
    mm = mesec.split("/")[0].split()[0] if mesec else ""
    mm = mm.strip("[]()~? ").split("-")[0]
    mnum = MESEC_SI.get(mm, "")
    men = MESEC_EN.get(mm, mm or "?")
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
        "    year: 1883,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {pag_int},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P223: krstna PREDZGODOVINA 04104, leto 1883 = 3/15 — (s161–s173 == gola-svinčna-pag-'sken−5' "
    "(s165='160'/s169='164'/s173='168'-VIZUALNO! s161='155[~156?]'-5/6-garble!; 2×-neodvisna-prenosa-md5-15/15!); "
    "★★★ MEJA-1882/83-s161 (TAIL-1882-z104–z106-Dez-31×3 + z105/z106-DVOJČKI-GRIBLJE-h68-ZWILLINGE-bracket-P224-LEAD! + "
    "'Initium-annos-Domini' + VSOTNA-razpeta-'1 8 8 3.' + restart-z1-NA-DAN-4.-1.-JÄNNER-Gradac!) = 62.-POTRDITEV-invariante! "
    "(61.-P222!); 99-vpisov-DISTINCT — vrstna-aritmetika 6+9+8+8+9+9+9+8+8+8+8+8+1 = 99 = P222-LEAD-1:1-INVARIANTA! — "
    "ČISTA-linija-brez-pisarjevih-anomalij!; ★★★ MESEC-CARRY-OVER-VZOREC (labela-samo-z1! — z2–z6-VSI-JÄNNER!) + "
    "★★★ MÄRZ-LABEL-MISREAD-KOREKCIJA (z24-'März'-hi — page-'Mai' → April-sandwich-anomalija-RAZREŠENA!) + "
    "★★★ DVOJNI-FOLIACIJSKI-SERIJI (gola-'sken−5'-1883-okno VS-'Pag.'-'sken+13'-1884-okno — menjava-tiskane-forme! — "
    "P222-'s173=186'-KOREKCIJA-'168'!) — 19-GRIBLJE / 18-hiš (h25-×2: z32+z88!) + z99-TAIL-IZLOČEN (vas-hi-'Obrijuh'-17!) + "
    "hišni-DUELI-REŠENI-×5 (z43-'42'-preliv! z61-90! z76-56! z78-37! z96-63!) + ★★★ POZNEJŠI-PRIPISI-MMK-ERA-×8 "
    "(z5-1962 + z22-1940 + z32-1957-KOREKCIJA + z43-1919/1942 + z52-1965 + z58-1959/60 + z59-1985-KOREKCIJA + z94-1910!) + "
    "mreže: PEZDIRC-grafija-×6 (z7-oče + z32-mati + z52-oče+mati + z76-botra + z96-mati+botra!) + BRODARIČ-×4 + DRAGOŠ-×2 + "
    "SIMEC-×3 + KRIŽAN-×2 + STRUCELJ-×2 + LESKO-×3 + MIHELČ-MILEK-×2 + HLEBEC + KLOBUČAR + ZUPANIČ-×2 + Kure-×2 ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count('year: 1883,\n    scan:')
print(f"vstavljenih blokov 1883-04104: {n} (pričakovano 19)")
