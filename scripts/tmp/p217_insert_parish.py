#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P217 — vstavi 10-GRIBLJE-blokov (04106, leto 1860) v parish.ts PRED P215-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/muzej-backup/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P215: mrliška PREDZGODOVINA 04106, leto 1862"

E = json.load(open("/tmp/p217/entries_1860.json"))
grib = E["griblje_entries"]
assert len(grib) == 9, f"grib={len(grib)}"

P217_HDR = "  // ——— P217: mrliška PREDZGODOVINA 04106, leto 1860"
if P217_HDR in src:
    i = src.index(P217_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P217-bloke (idempotenca)")

KOM = {
    7: "★★★ KROP-full-row+PAS + ★★★ GRIBLJE-h55-NOVA-HIŠA + ime-DUEL-X-open (Miklavž/Anništ[?]) + starost-TRI-DUEL-X-open (27/87/37!) + Wassersucht[?]",
    13: "★★★ KROP-full-row+PAS + ★★★ GRIBLJE-h6-NOVA-HIŠA + ime-duel (Jakofčič/Jakobčič) + starost-TRI-DUEL-X-open (46/1-J-1-M/14!)",
    23: "★★★ KROP-full-row+PAS + ★★★ GRIBLJE-h13-NOVA-HIŠA + ime-DUEL-X-open (Andrej-Jakošec/Lunbran-Jakobs!) + 59-J-2×-1:1 + Lungenentzündung-Auszehrend",
    24: "★★★ KROP-full-row+PAS-×2 + ★★★ GRIBLJE-h50-NOVA + ime-TRI-GARBLE-X-open (Matija-Petine/Peter-Mautknecht/Rosalia-Pedire — SPOL-X-open!) + hisna-DUEL (50/30) + starost-DUEL (64/68)",
    27: "★★★ KROP-full-row+PAS + ★★★ POŽEK-h58-NIT-1860 (z27-otrok-8-mes! cf.-P211-z90-h58 + P192-h58!) + ★★★ '16.-Mai-1860'-EKSPLICITNA-LETNICA-v-vpisu (KROP!) + ime-DUEL-X-open (Barbara/Bartholomä-Požek/Pöckl!)",
    61: "★★★ KROP-full-row-P216 + ★★★ GRIBLJE-h24 (z61-Inocenz[~Lukas!]-Brenc[~Brinar?]-23J-Okt!) + hisna-24-3×-1:1",
    65: "★★★ KROP-full-row-P216 + ★★★ PEZDIRC-h30[?]-NIT (z65-Mathias[~Martin?]-Pezdirc[?]-34J[~54!]-Nov! — PEZDIRC-MREŽA!) + hisna-DUEL (30/40) + ime-TRI-DUEL-X-open",
    69: "★★★ VALENTIN-×2-h57-1/2 (written-55! REGISTERJSKA-NAPAKA-#69!) + Dez-10/12 + 54-J + priimek-NEBERLJIV-X-open",
    70: "★★★ VALENTIN-×2-h57-2/2 (written-56! #70!) + Dez-10/13 + 37-J + 'Griblje-Prist-57'-'Prist'[?]-X-open + oče-sin-hipoteza",
}

def esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')

def gen_block(e):
    z = e["z"]
    ime = (e.get("ime") or "?").strip()
    stan = (e.get("stan") or "").strip()
    starost = (e.get("starost") or "?").strip()
    mesec = (e.get("mesec") or "").strip()
    smrt = (e.get("smrt") or "").strip()
    pokop = (e.get("pokop") or "").strip()
    bolezen = (e.get("bolezen") or "?").strip()
    kom = KOM.get(z, "")
    mes = mesec.split()[0] if mesec else ""
    mes = {"Februar": "Feber", "Januar": "Jänner", "December": "Dezember", "Junij": "Juni",
           "Martii": "März", "Maii": "Mai", "Julii": "July", "September": "September"}.get(mes, mes)
    smrt_clean = str(smrt).replace(".", "").strip()
    pokop_clean = str(pokop).split()[0].replace(".", "").strip() if pokop else "?"
    what = f"umrl(a) {ime}"
    if stan: what += f", '{stan}'"
    what += f", {starost} ({mes} {smrt_clean}., pokop {pokop_clean}.) — {bolezen};"
    if kom: what += f" + {kom}"
    what += f" + [z{z}]"
    what_en = f"died {ime}"
    if stan: what_en += f", {stan}"
    what_en += f", {starost} ({mes} {smrt_clean}., buried {pokop_clean}.) — {bolezen}; + [see-SI] + [z{z}]"
    return (
        "  {\n"
        f'    houseNo: "{e.get("hisna")}",\n'
        '    bookSignature: "04106",\n'
        "    year: 1860,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {e['pag']},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P217: mrliška PREDZGODOVINA 04106, leto 1860 = 26. leto PREDZGODOVINSKE LINIJE "
    "(s017–s025 == Pag. 12–20, z1–z73 = 73 vpisov — ŠTEVJE-IZ-VRSTIC-19.× (kronološko-z1–z73; "
    "WRITTEN-duplikat-53–59-REGISTERJSKA-NAPAKA-P216!; vrstna-aritmetika 13+13+13+13+14+7; "
    "meseci J7+F7+M6+A2+M7+J6+J8+A10+S4+O6+N5+D5; pag = sken−5; 2×-neodvisna-prenosa-7/7-md5 + s023-carry-P216!) — "
    "9-GRIBLJE-blokov / 8 hiš (h57-×2-VALENTIN!) + ★★★ MEJA-1859/60-s20 ('1860'-rokopisna-glava-KROP-POTRJENA — "
    "VLM-'1800'-misread-KOREKCIJA! = 55.-POTRDITEV-invariante! + restart-z1–z13-BREZ-taila!) + ★★★ MEJA-1860/61-s25 "
    "(WRITTEN-53–59 + vsotna-'60'-REGISTERJSKA-NAPAKA + vsotna-'1861'-marker + '1861'-rokopisna-glava — P216!) + "
    "★★★ VLM-margin-misreadi-KOREKCIJE (s18-'90–101'→'80–91'-+10-tens-duel-KROP! + s22-r1-'23'→'27'-KROP! + "
    "z53-mesec-'avgust-nadaljevanje'-KROP-P216!) + ★★★ z27-'16.-Mai-1860'-EKSPLICITNA-LETNICA-v-vpisu (KROP!) + "
    "★★★ POŽEK-h58-NIT (z27-Barbara[~Bartholomä!]-8-mes!) + ★★★ VALENTIN-×2-h57 (z69+z70-2-dni-oče-sin-hipoteza!) + "
    "★★★ PEZDIRC-MREŽA (z65-h30[?]-34J[~54!] + tail-1859-z73/z81!) + z24-ime-TRI-GARBLE-SPOL-X-open + "
    "otroška-umrljivost-11%-1/9 (NAJNIŽJA!) ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count("year: 1860,")
print(f"vstavljenih blokov 1861: {n} (pričakovano 10)")
