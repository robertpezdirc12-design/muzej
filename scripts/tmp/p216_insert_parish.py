#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P216 — vstavi 10-GRIBLJE-blokov (04106, leto 1861) v parish.ts PRED P215-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P215: mrliška PREDZGODOVINA 04106, leto 1862"

E = json.load(open("/tmp/p216/entries_1861.json"))
grib = E["griblje_entries"]
assert len(grib) == 10, f"grib={len(grib)}"

P216_HDR = "  // ——— P216: mrliška PREDZGODOVINA 04106, leto 1861"
if P216_HDR in src:
    i = src.index(P216_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P216-bloke (idempotenca)")

KOM = {
    7: "★★★ KROP-full-row+PAS + ★★★ ŽELKO-h1-NIT-4.-LETO (1861-[Grozj?]-47J → 1862-z41-Maria-½J → 1864-×2!) + ime-TRI-branja-DUEL-X-open ('Jurkič'/'Franc'/'Šumič'!) + stan-duel-¼/½ + 47-J-KROP+PAS-2:1 + Wassersucht-duel",
    11: "★★★ KROP-full-row+PAS + ★★★ URIH-h68-NOVA-HIŠA (cf. 1865-'URIH-ne-Urik'!) + ime-4-BRANJA-DUEL-X-open ('Marko'/'Mariša'/'Markus'/'Martha' — SPOL-X-open!) + 46-J-3×-1:1 + Lungenentzündung",
    14: "★★★ KROP-full-row+PAS + ★★★ h42-×3-APR-KLASTER-1/3 (družina-HIPEZOZA!) + ime-GARBLE-X-open ('Perdiu[?]'/'Kerdivc[?]'/'Peždinc'!) + starost-TRI-DUEL (45/4½/7½)",
    15: "★★★ KROP-full-row+PAS + ★★★ h42-×3-APR-KLASTER-2/3 + 2-J-3×-1:1 + 'Steckfluß'-KROP+PAS-1:1 + PEZDIRC-družina-hipoteza ('Anžal[?]-¼-Gütlertsohn')",
    17: "★★★ KROP-full-row+PAS + ★★★ h42-×3-APR-KLASTER-3/3 (dojenček-5-tednov!) + ime-GARBLE-4-branja + starš+2-otroci-v-6-dnih",
    30: "★★★ KROP-full-row+PAS + ★★★ MALEŠIČ-h26-NOVA-HIŠA + ime-TRI-branja-1:1 (Mathias-Malesič!) + starost-DUEL (59/54/57) + Abzehrung-TRI-branja-1:1!",
    32: "★★★ KROP-full-row+PAS + ★★★ KLOBUČAR-h48-NOVA-HIŠA + starost-TRAJNI-DUEL-X-open (15/65/1!) + '¼-Güblerkind' + 15-J-otrok + ime-S/H-duel",
    35: "★★★ ŠIMEC-h18-NIT-GLOBLJE (1861-Anna-Goric-1½J-h18 → 1863-z26-Georg-Simic → 1864-z34!) + hisna-DUEL-18/19 + P215-VLM-s29-križ",
    44: "★★★ PEZDIRC-h14-NIT-GLOBLJE (1861-Anna-Hrance[?]-3J-h14 → 1864-z18-Michael + 1865-z41!) + hisna-DUEL-14/44 + cf.-h42-×3-klaster",
    54: "★★★ POŽEK-h67-NIT-ZADNJI-1861-VNOS (Dez-16/18! γ-forma-'67'-vs-'69'-DUEL-KROP-P215!) → 1865-z36-Mathias-36J-ISTO-HIŠA (oče-sin-hipezoza-X-open!) + 2-J-otrok",
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
        "    year: 1861,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {e['pag']},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P216: mrliška PREDZGODOVINA 04106, leto 1861 = 25. leto PREDZGODOVINSKE LINIJE "
    "(s023–s030 == Pag. 18–25, z1–z54 = 54 vpisov — ŠTEVJE-IZ-VRSTIC-18.× (ordinali-1–54-ČISTO — "
    "10.-LETO-ZAPORED-BREZ-luknje/dupa!; vrstna-aritmetika 5+13+14+16+6; meseci J2+F2+M7+A6+M4+J6+J5+A7+S3+O6+N3+D3; "
    "pag = sken−5; 2×-neodvisna-prenosa-8/8-md5 + s029/s030-carry-P215!) — 10-GRIBLJE-blokov / 8 hiš (h42-×3!) + "
    "★★★ MEJA-1860/61-s25 (tail-1860-WRITTEN-53–59 + VSOTNA-'60'-margin-REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA-NOV-TIP! + "
    "VSOTNA-'1|8|...|1'-'1861'-MARKER-4.-INSTANCE + ROKOPISNA-'1861'-GLAVA = 54.-POTRDITEV! + restart-z1–z5!) + "
    "★★★ MEJA-1861/62-s30 (vsotna-'1|8|6|2'-'1862'-MARKER-3.-instance + RESTART-BREZ-rokopisne-glave — P215!) + "
    "★★★ s27=s26-DOUBLE-SCAN-3.-v-knjigi (2×-NEODVISNA-VLM-z6–z18!) + ★★★ VLM-margin-misreadi-KOREKCIJE (s23-'41–53'→'40–52'-+1-pomik! + "
    "z53-1860-mesec-avgust-nadaljevanje! + z20-vas-'Zemelj'! + z18-mesec-'Mai'!) + ★★★ h42-×3-APR-KLASTER (družina-HIPEZOZA — ime-garble!) + "
    "★★★ PEZDIRC-MREŽA-×5-1860–1865 (h30[?]-tail + h42-×3[?] + z1-'von-Griblje[?]'-1862 + h14/h11-1864 + h14-1865!) + "
    "★★★ ŽELKO-h1-nit-4.-LETO + ★★★ ŠIMEC-h18-nit-GLOBLJE + ★★★ POŽEK-h67-nit-ZADNJI-VNOS + URIH-h68/MALEŠIČ-h26/KLOBUČAR-h48-NOVE + "
    "★★★ VALENTIN-×2-h57-1860-tail + otroška-umrljivost-50%-5/10 (NAJVIŠJA-v-predzgodovini!) ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count("year: 1861,")
print(f"vstavljenih blokov 1861: {n} (pričakovano 10)")
