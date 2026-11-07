#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P224 — vstavi 25-GRIBLJE-blokov (krstna 04104, leto 1882 = 4/15!) v parish.ts PRED P223-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P223: krstna PREDZGODOVINA 04104, leto 1883"

E = json.load(open("/tmp/p224/entries_1882.json"))
grib = E["griblje_entries"]
assert len(grib) == 25, f"grib={len(grib)}"

P224_HDR = "  // ——— P224: krstna PREDZGODOVINA 04104, leto 1882"
if P224_HDR in src:
    i = src.index(P224_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P224-bloke (idempotenca)")

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}

KOM = {
 "z2": "★★★ oče-garble-DUEL (Klarič-vs-Hausser!) + matec-garble-X-open!",
 "z7": "★★★ pripis-MMK-'umrla-7.[~4!].8.1955-v-Bohinju[?]' + Butala-nit!",
 "z10": "★★★ KLOBUČAR-mati-nit (×3-leta: z34-oče + z97-oče!) + oče-TRI-garble-honesty!",
 "z22": "★★★ DRAGOŠ-mati-nit (2/2-pogojno!-z85-X-open!) + SIMEC-botra-nit (2×!) + pripis-MMK-'umrla-29.11.1960'-MNR-št.187!",
 "z23": "★★★ hiša-'73'-VIZUALNO (γ-7!-krop-'43'-ZAVRNJEN!) + PEZDIRC-mati-nit-X-open (Pegdire!) + Feb-28→Mär-2-meja (z24-'März'-VIZUALNO!)",
 "z29": "★★★ hiša-'1' (paralela-P223-z73!) + KRIŽAN-mati-nit-KOREKCIJA (Križan!-page-'Kuržan') + ŽELJKO-×3-nit (P139!)",
 "z31": "★★★ hiša-'28'-VIZUALNO + LAZAR-oče-nit (P220/P222!) + Skarasinič-mati-PARALELA-P222 + BRODARIČ-botra!",
 "z34": "★★★ KLOBUČAR-oče-nit (×3-leta!) + matec-DUEL-X-open (Janer/Mihelčič!)",
 "z43": "★★★ POŽEK-oče-nit (2/2-z105/106-mati!) + pripis-MMK-'†-23/4.[~1!]-1919' + botra-garble-dueli!",
 "z55": "★★★ ZAP-KOREKCIJA (z55-NE-z54!-VIZUALNO-'55'!) + hiša-'65'-VIZUALNO (page-'66'-ZAVRNJENA!) + MILEK-oče-nit (h65!)",
 "z58": "★★★ hiša-'41'-VIZUALNO (krop-'11'-4→1-ZAVRNJEN!) + pripis-MMK-'†-30.4.[~9!]-1937' + garble-honesty-MAX!",
 "z71": "★★★ MESEC-KOREKCIJA (OKTOBER-11/12!-page-'[?Nov]'-'…ember'-failure!) + hiša-'5'-3× + oče-DUEL (Brinc/Primc-P223-paralela!)",
 "z73": "★★★ hiša-'40'-3× + oče-DUEL-X-open (Petir/Perdič-PEZDIRC-variant!) + pag-'151'-DUEL-REŠEN (sken−6!)",
 "z74": "★★★ hiša-'62'-3× + Kure/Hure-DUEL + matec-DUEL-X-open (Brižan-KRIŽAN-variant?) + BRODARIČ-botra!",
 "z85": "★★★ hiša-'58'-VIZUALNO-3× (page-'38'-3/5-ZAVRNJEN!) + DRAGOŠ-mati-nit-X-open (Drugot/DRAGOŠ!)",
 "z87": "★★★ hiša-'16'-3× + Nov-20→21 (z85/z87-zapored!)",
 "z89": "★★★ hiša-'13'-VIZUALNO-3× + PEZDIRC-mati-nit (2×!) + oče-DUEL (Jakofčič/Gabrovec!)",
 "z90": "★★★ hiša-'74'-VIZUALNO (page-'14'-7→1-ZAVRNJEN!) + PEZDIRC-mati+botra-DVOJNI-nit (Perdiuc-×2!-P223-z96-PARALELA!)",
 "z91": "★★★ hiša-'44'-VIZUALNO-3× (page-'11'-4→1-ZAVRNJEN!) + pripis-MMK-'umrl-27.3.1966-MMK-k.50-str.81'-2×! + oče-TRI-garble!",
 "z92": "★★★ hiša-'43'-VIZUALNO-3× (page-'13'-4→1-ZAVRNJEN!) + DEZEMBER-labela-z92-VIZUALNO (carry-over-1882!) + P222-h43-PARALELA!",
 "z95": "★★★ hiša-'35'-3× + pripis-MMK-'umrla-26.[~28!]-6.1971-Ljubljana' + 'Zu-Griblau'-pripis + garble-QUAD-honesty!",
 "z97": "★★★ hiša-'47'-2:1 (krop-'17'-4→1-ZAVRNJEN!) + KLOBUČAR-oče (×3-leta!) + DEZEMBER-carry-over (z96-labela-VIZUALNO!)",
 "z99": "★★★ hiša-'13'-VIZUALNO (h13-×2: z89!) + KRIŽAN-botra-nit (Dorothea-Hrižan-2×!) + P223-LEAD-POTRJEN!",
 "z105": "★★★ DVOJČEK-1/2 (ZWILLINGE-P223-LEAD-POTRJEN!) + POŽEK-mati-nit (2/2-z43-oče!) + Dez-31-×4!",
 "z106": "★★★ DVOJČEK-2/2 (ZWILLINGE-P219/P221/P223-PARALELE!) + h68-×2 + TAIL-1882!",
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
        "    year: 1882,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {pag_int},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P224: krstna PREDZGODOVINA 04104, leto 1882 = 4/15 — (s147–s161 == gola-svinčna-pag-'sken−6' "
    "(9-VIZUALNIH: s148='142'/s153='147'/s157='151'/s159='153'/s160='154'/s161='155'/s162='156'/s163='157'!; "
    "2×-neodvisna-prenosa-md5-17/17!); ★★★ MEJA-1881/82-s147/s148 (TAIL-1881-z83–z89 + 'finis' + "
    "'Anni 1 8 8 1.'-RAZPETA-P214-TIP-4.-instance! + 'Jahr 18|82'-glava + RESTART-z1-NA-DAN-2.-1.-JÄNNER-Dobravce-h27!) "
    "= 63.-POTRDITEV-invariante! (62.-P223!); 106-vpisov-DISTINCT — vrstna-aritmetika "
    "8+9+8+8+7+9+8+7+7+8+8+8+8+3 = 106 = P223-LEAD-'z88–z106-tail'-1:1-INVARIANTA!; "
    "★★★ S160-'NOVEMBER'-MISREAD-KOREKCIJA = DEZEMBER-BLOK-z92–z106 (z96-'DECEMBER'-labela-VIZUALNO! "
    "z103-dan-31!-'…ember'-failure-mode-PARALELA-P223-'Feber'!-Dez-31-×4: z103–z106!) + "
    "★★★ Z71-MESEC-KOREKCIJA (OKTOBER-11/12!-October-labela-z70-carry-over!) + "
    "★★★ FOLIACIJA-TRI-SERIJE (sken−6-1882! + ★LUKNJA-'158'-skok-s163→s164! + sken−5-1883-P223! + "
    "'Pag.'-'sken+13'-1884-P222!) + ★★★ S149-Z16-DUPLIKAT (16-×2→17!-P222-z84-PARALELA!) + "
    "★★★ Z55-ZAP-KOREKCIJA (VIZUALNO-'55'!-page-shift!) + HIŠNE-VIZUALNE-REŠITVE-×6 (z85-58! z90-74! "
    "z91-44! z92-43! z23-73! z97-47!-KURRENT-1↔4/7+3↔5!) — 25-GRIBLJE / 23-hiš (h13-×2: z89+z99! "
    "h68-×2: z105/z106-DVOJČKI-ZWILLINGE!) = TIE-REKORD-P221! + ★★★ POZNEJŠI-PRIPISI-MMK-ERA-×6 "
    "(z7-1955 + z22-1960-MNR! + z43-†1919 + z58-†1937 + z91-†1966-MMK-k.50! + z95-†1971!) + "
    "mreže: PEZDIRC-×4 (z23-mati-X-open! + z89-mati! + z90-mati+botra-DVOJNI!) + DRAGOŠ-×2 (z22-mati! "
    "+ z85-X-open!) + KRIŽAN-×2 (z29-mati-KOREKCIJA! + z99-botra-Dorothea!) + KLOBUČAR-×3 (z10+z34+z97!) + "
    "LAZAR (z31!) + POŽEK-×2 (z43-oče! + z105/z106-mati!) + BRODARIČ-×2 + MILEK (z55!) + SIMEC (z22!) + "
    "ŽELJKO-×3 (z29!-P139!) ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count('year: 1882,\n    scan:')
print(f"vstavljenih blokov 1882-04104: {n} (pričakovano 25)")
