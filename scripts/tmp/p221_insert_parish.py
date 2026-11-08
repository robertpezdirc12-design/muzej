#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P221 — vstavi 25-GRIBLJE-blokov (krstna 04104, leto 1885 = 1/15 NOVA LINIJA!) v parish.ts PRED P79-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P79 vzorec: polno leto 1886 (vsi Griblje vpisi, strani 1–14) ———"

E = json.load(open("/tmp/p221/entries_1885.json"))
grib = E["griblje_entries"]
assert len(grib) == 25, f"grib={len(grib)}"

P221_HDR = "  // ——— P221: krstna PREDZGODOVINA 04104, leto 1885"
if P221_HDR in src:
    i = src.index(P221_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P221-bloke (idempotenca)")

KOM = {
    1: "★★★ RESTART-z1 = 1.-vpis-1885-NA-DAN-1.-1.! + pripis-'†-7.9.1887' = KRIŽ-z-mrliško-04106-X-open! + ŽELKO-številka-h21-nit",
    5: "★ pripis-'gest.-12.[?]1888' = KRIŽ-04106-X-open! + POŽEK-botra-nit! + hiša-[?]-(~10-krop-X-open!)",
    14: "★★★ page-'h6'-MISREAD-KOREKCIJA (61-2:1!) — h61-URIH-hiša + oče-POŽEK + mati-FILAK + botri-PEZDIRC-×2 = 4-MREŽE-V-1-VRSTICI!",
    15: "★ h11-nit-potrjena (trak-'41'-MISREAD!)",
    20: "★ h63-nit (P220-z74-KRIŽAN-h63-1857-TAIL! — h63-2-obdobji!)",
    26: "★ ordinal-DUEL-KOREKCIJA (27→z26!) + hiša-TRI-DUEL (49/17/1[8?]!)",
    28: "★ page-'28-dup'-MISREAD-KOREKCIJA (EN-vpis!) — h28-nit",
    30: "★ page-'h45'-MISREAD-KOREKCIJA (42-2:1!) + 'Intabvre'-intabuliran-status-X-open!",
    33: "★★★ h1-nit (1/2!) + ŽELKO-mreža (oče-Miklo + botri-Želko-×2!)",
    37: "★ h55-nit (1/2!) + SIMIC-oče + ordinal-'97'-krop-MISREAD-KOREKCIJA (37!)",
    47: "★★★ page-'h33'-MISREAD-KOREKCIJA (53-2:1!) — PEZDIRC-grafija-oče!",
    48: "★★★ page-'h33'-MISREAD-KOREKCIJA (35-2:1!) — h33-×2-HIPOTEZA-MRTVA! + botra-URH!",
    56: "★ h16-nit + ordinal-'36'-krop-MISREAD-KOREKCIJA (56!)",
    57: "★ ordinal-TRI-DUEL (57/58/59! — zap-pozicija!) + datum-kronološki-preskok (Aug-2-vs-Jul-31/3-X-open!)",
    59: "★★★ honesty-MAX-1885 (hiša-QUAD-DUEL-27/47/37/21 + ime-TRI-DUEL-Marko/Maria/Martin/Martha!)",
    62: "★ page-'h19'-MISREAD-KOREKCIJA (17-2:1!) — oče-Hval-¼-Gärtler",
    63: "★★★ mati-DRAGOŠ-nit (P193/P220!) + botra-PEZDIRC-nit!",
    64: "★ h9-nit (3×-križ!)",
    68: "★ h55-nit (2/2 — h55-×2!) + SIMIC-oče (z37-X-open-ista-družina!)",
    78: "★ hiša-TRI-DUEL (17/29/9/99!) + ordinal-'98'-krop-MISREAD-KOREKCIJA (78!)",
    82: "★ h2-nit — oče-HLEBEC (P219-KLEPEC/HLEBEC-nit-2-obdobji!)",
    85: "★★★ mati-PEZDIRC-nit (Katharina-roj.-Pegdirec!) + page-'39-ep-91'-MISREAD-KOREKCIJA (23-2:1!)",
    100: "★★★ page-'Škrilje'-MISREAD-KOREKCIJA (r7-krop-'Gribile-h1'-1:1!) — h1-×2 (2/2!) — BREZ-te-korekcije-bi-korpus-izgubil-1-GRIBLJE!",
    104: "★★★ TAIL-1885 = ZADNJI-VPIS-KNJIGE-04104 + ordinal-POPRAVEK-PISARJA ('103'-prečr→104!) + botra-KRIŽAN-nit!",
}

MESEC_SI = {"J": "1", "F": "2", "M": "3", "A": "4", "M2": "5", "J2": "6", "J3": "7", "A2": "8", "S": "9", "O": "10", "N": "11", "D": "12"}
MESEC_EN = {"J": "Jan", "F": "Feb", "M": "Mar", "A": "Apr", "M2": "May", "J2": "Jun", "J3": "Jul", "A2": "Aug", "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"}


def esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def clean_day(d):
    d = str(d or "").strip().rstrip(".")
    d = d.split()[0] if d else "?"
    return d if d else "?"


def gen_block(e):
    z = e["z"]
    znum = int(str(z).replace("z", ""))
    ime = (e.get("ime") or e.get("otrok") or "?").strip()
    ocec = (e.get("ocec") or "").strip()
    matec = (e.get("matec") or "").strip()
    botra = (e.get("botra") or "").strip()
    mesec = (e.get("mesec") or "").strip()
    rojen = clean_day(e.get("rojen"))
    krsten = clean_day(e.get("krsten"))
    kom = KOM.get(znum, "")
    mm = mesec.split()[0] if mesec else ""
    mm = mm.strip("[]()~? ")
    mnum = MESEC_SI.get(mm, "")
    men = MESEC_EN.get(mm, mm or "?")
    mpart = f"{mnum}." if mnum else "[?]"
    what = f"krščena {ime} ({rojen}./{krsten}. {mpart})"
    if ocec: what += f" — oče {ocec}"
    if matec: what += f", mati {matec}"
    if botra: what += f"; botra {botra}"
    if kom: what += f"; + {kom}"
    what += f" + [z{z}]"
    what_en = f"baptized {ime} ({men} {rojen}/{krsten})"
    if ocec: what_en += f" — father {ocec}"
    if matec: what_en += f", mother {matec}"
    if botra: what_en += f"; godparents {botra}"
    what_en += "; + [see-SI]" + f" + [z{z}]"
    hisna = str(e.get("hisna") or "[?]")
    return (
        "  {\n"
        f'    houseNo: "{esc(hisna)}",\n'
        '    bookSignature: "04104",\n'
        "    year: 1885,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {e['pag']},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P221: krstna PREDZGODOVINA 04104, leto 1885 = 1/15 — NOVA LINIJA (mrliška-04106-KONČANA-29/29-P220!) — "
    "(s185–s199 == pag sken+13-FOLIO-SVINČNIK-ARHIVARJA (razprti-dvostranski-list = 1-folio! — potrjeno-5×-natančno: "
    "s185='198'/s190='203'/s193='206'/s196='209'/s199='212'! + tens-MISREADI-dokumentirani!; 2×-neodvisna-prenosa-md5-15/15!); "
    "★★★ MEJA-1884/85-s186 (TAIL-1884-z111[prečr]-Gradac-68 + z112[prečr]-GRIBLJE-h43 + VSOTNA-razpete-'1/8/8/5'-P214-TIP + "
    "restart-z1-NA-DAN-1.-1.-GRIBLJE-h21!) = 60.-POTRDITEV-invariante! + 1884 = 112-vpisov!; "
    "104-vpisov-kronološko — ŠTEVJE-IZ-VRSTIC-1.×-za-krstno-linijo (z1–z104; vrstna-aritmetika 4+8+8+8+9+9+8+8+8+7+8+8+9+2; "
    "meseci J11+F3+M9+A6+M5-9+J6-11+J7-7+A8-10+S7+O9+N3+D16) — "
    "★★★ DVOJČKI-GRADAC-×2-2-VRSTICI (z92-Anton-umrl-'Na-umrla' + z93-Jožef-živ — Dez-14/14! — page-VLM-SPOJIL-KOREKCIJA! — "
    "PARALELA-P219-DVOJČKI-SIMIC!) + ★★★ z101-NEIDENTIFICIRANA-VRSTICA (page-VLM-ZAMUJENA! — DOKAZ: POPRAVEK-PISARJA-s199-"
    "'102'→103 + '103'→104! + t4-fragment-'Janez-Tomaž-½-gem.' + robni-svinčnik-100/101/102!) + ★★★ POPRAVEK-PISARJA-s199-×2 + "
    "z102-IME-POPRAVEK (Katharina→Marija!) + ★★★ NASLOVNA-SREDI-LETNIKA-s190 (paralela-mrliška-s9+s10! + glava-'18 85'-page-"
    "'1886'-MISREAD-KOREKCIJA!) — "
    "★★★ 25-GRIBLJE = NOV-REKORD-PREDZGODOVINE/KORPUSA (prej-23-P218-1859!) / 20-hiš + 3-[?]-dueli (h1-×2-ŽELKO + h55-×2-SIMIC!; "
    "z59-honesty-MAX-QUAD-DUEL-hiša+TRI-DUEL-ime!) + ★★★ page-VLM-hišne-MISREAD-KOREKCIJE-×7 (h6→61! h45→42! h33→53+h33→35 "
    "(h33-×2-HIPOTEZA-MRTVA!) h19→17! h39-ep91→23! 'Škrilje'→GRIBLJE-h1 (z100!)! h37-'97'→37!) + "
    "★★★ POZNEJŠI-PRIPISI-KRIŽ-z-mrliško-04106 (z1-†7.9.1887 + z5-†12.[?]1888 + 1884-tail-†25.9.1885/†28.12.1887! — "
    "NOVA-VERIFIKACIJSKA-DIMENZIJA!) + mreže: PEZDIRC-×4 (z47-oče + z85-mati + z63/z14-botri!) + POŽEK + ŽELKO + SIMIC-×2 + "
    "URIH + FILAK + DRAGOŠ + HLEBEC + KRIŽAN-botra-TAIL ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count('year: 1885,\n    scan:')
print(f"vstavljenih blokov 1885-04104: {n} (pričakovano 25)")
