#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P215 — vstavi 9-GRIBLJE-blokov (04106, leto 1862) v parish.ts PRED P214-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P214: mrliška PREDZGODOVINA 04106, leto 1863"

E = json.load(open("/tmp/p215/entries_1862.json"))
grib = E["griblje_entries"]
assert len(grib) == 9, f"grib={len(grib)}"

P215_HDR = "  // ——— P215: mrliška PREDZGODOVINA 04106, leto 1862"
if P215_HDR in src:
    i = src.index(P215_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P215-bloke (idempotenca)")

KOM = {
    4: "★★★ KROP-full-row+PAS (ime-Markus/Mathias-DUEL + stan-'Gutsler[~]'-garble + h9-γ/9-duel-rešen-9!) + ★★★ KRIŽAN-h9-NOVA-HIŠA (soseda-h10-KUNE! cf. 1862-tail-z56-Krasinec-h9-Krijžan!) + 72-J + Marasmus-senilis-KROP+PAS-1:1",
    10: "★★★ KROP-full-row+PAS-×2 (ime-DUEL-X-open: full-'Simon'-vs-krop-'Maria/Vinanz-Ehefrau[?]'!) + ★★★ KUNE-h10-NIT: 1862-'Simon-Kure'-h10-2J → 1863-z2-'Joannes-Kune'-h10 (X-open-4-branja — 'Kure'-5.-branja-PODPORA!) + '¼-Güblerssohn' + Ohnmacht[ucht?]-garble",
    11: "★★★ KROP-full-row+PAS + ★★★ FILAK-h61-1862! (ime-F/T/K-DUEL-rešen-FILAK-via-z14!) + ★★★ KATARINA-FILAK-age-match-1862/1866-X-open (34J→38J-MOŽNO-ISTA-OSEBA — h61-vs-h34!) + h61-1.-instance + Lungenentzündung-1:1",
    14: "★★★ KROP-full-row + ★★★ FILAK-h5-'...Kind-von-ANNA-FILAK' (opomba-garble — unehelich/verwaiset-X-open — FORMULA-cf.-P214-z53!) + ★★★ ANNA-FILAK-nova-oseba — FILAK-mreža-×3-1862 → h34-1864/65/66! + 10-J + h5-duel-krop-'3'",
    17: "★★★ KROP-full-row+PAS + bolezen-DUEL-X-open ('Lungensucht'-vs-'Masern'-'ošpice!'-epidemija-hipoteza?) + h47-NOVA-hiša (duel-'17'-vs-'47'-2×!) + 1½-J + '¼-Gütlerskind' + ime-S/H-duel",
    41: "★★★ KROP-full-row+PAS + ★★★ ŽELKO-h1-NIT-3.-LETO (1862-Maria-½J → 1864-Anna-22J + Peter-1J!) + ime-Ž/Z-duel ('Zeljko'/'Šeljko') + Zuckfall-duel (cf.-1863-z39/z40-'Zaugfall'!) + '¼-Güblerskind'",
    43: "★★★ KROP-full-row+PAS + Typhus-TRI-branja-1:1 (KROP+PAS+FULL — izjemno!) + ★★★ KRIŽAN-h63-NIT-2-LETI (1862-Thomas-Potočar-28J → 1864-z63-Kind-von-Johann-Križan-h63!) + stan-2-vrstični-garble + h63-duel-'68'",
    48: "★★★ KROP-full-row+PAS + ★★★ h61-2.-INSTANCE-v-1-LETU (z11-Filak-März + z48-Okt!) + ★★★ ANOMALIJA-PRAZNI-STOLPCI (starost-'—' + bolezen-'—' — duel-krop-'1-J[?]'!) + ime-J/S-DUEL ('Jerlicar'/'Seliscar') + 'Müllerssohn[?]'-garble",
    50: "★★★ KROP-full-row+PAS + ★★★ h5-2.-INSTANCE-v-1-LETU (z14-Filak-Apr + z50-Okt!) + ime-TRI-branja-DUEL-X-open ('Graucek'/'Strucelj'/'Gartner[?]'-G/S/K-cf.-1863-z27-STRAUS!) + starost-TRAJNI-DUEL ('61-J'-vs-'6-tednov[?]'!) + ½-Gübler + Abzehrung",
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
        "    year: 1862,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {e['pag']},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P215: mrliška PREDZGODOVINA 04106, leto 1862 = 24. leto PREDZGODOVINSKE LINIJE "
    "(s029–s035 == Pag. 24–30, z1–z60 = 60 vpisov — ŠTEVJE-IZ-VRSTIC-17.× (ordinali-1–60-ČISTO — "
    "9.-LETO-ZAPORED-BREZ-luknje/dupa!; vrstna-aritmetika 7+16+16+15+6; meseci J4+F5+M2+A8+M8+J3+J4+A6+S6+O6+N3+D5; "
    "pag = sken−5; 2×-neodvisna-prenosa-7/7-md5 + s033–s035-carry-P214!) — 9-GRIBLJE-blokov / 7 hiš (h5+h61-×2!) + "
    "★★★ MEJA-1861/62-s30 (tail-1861-z49–z54 + VSOTNA-'1|8|6|2'-'1862'-MARKER-3.-INSTANCE + restart-z1–z7! + "
    "NOVA-VARIANTA: BREZ-rokopisne-'1862'-glave — vsotna=EDINI-marker! + KROP-zap-stolpec: '1861'-glava + '49–54' — "
    "VLM-misread-'29–34'-KOREKCIJA!) + ★★★ MEJA-1862/63-s35 (vsotna-'1|8|6|3'-'1863'-MARKER + '1863'-rokopisna-glava = "
    "52.-POTRDITEV-P214!) + ★★★ s32=s33-DOUBLE-SCAN-2.-v-knjigi (2×-NEODVISNA-VLM-z24–z39!) + "
    "★★★ FILAK-MREŽA-×3-1862 (z11-Katharina-h61-F/T/K-DUEL + z14-Nicolaus-h5-'Kind-von-ANNA-FILAK' + ANNA! → h34-1864/65/66!) + "
    "★★★ KUNE-h10-nit (z10-'Simon-Kure' → 1863-z2-'Joannes-Kune' — 'Kure'-5.-branja!) + ★★★ ŽELKO-h1-nit (z41-Maria-½J → 1864!) + "
    "★★★ KRIŽAN-h63-nit-2-LETI (z43-Thomas-Potočar-Typhus-TRI-branja-1:1!) + ★★★ POŽEK-h67-nit-4-LETA (tail-1861-z54-Mathias-2J → 1865-36J!) + "
    "★★★ PEZDIRC-z1-restart ('von-Griblje[?]'!) + z48-prazni-stolpci + z30-pokop-brez-smrti + otroška-umrljivost-33%-3/9 ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count("year: 1862,")
print(f"vstavljenih blokov 1862: {n} (pričakovano 9)")
