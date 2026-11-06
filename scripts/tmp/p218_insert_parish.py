#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P218 — vstavi 23-GRIBLJE-blokov (04106, leto 1859) v parish.ts PRED P215-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/muzej-backup/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P215: mrliška PREDZGODOVINA 04106, leto 1862"

E = json.load(open("/tmp/p218/entries_1859.json"))
grib = E["griblje_entries"]
assert len(grib) == 23, f"grib={len(grib)}"

P218_HDR = "  // ——— P218: mrliška PREDZGODOVINA 04106, leto 1859"
if P218_HDR in src:
    i = src.index(P218_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P218-bloke (idempotenca)")

KOM = {
    6: "★★★ z5+z6-PARIČ-FRAISEN-klaster-×2-ISTA-DATA (Jän-27/29 — Marija-Vranoviče-h15-10-tednov!) + ★ h69-NIT (P155-1889-Brinec-16-DNI!) + NOV-DUHOVNIK-'Joh.-Knavs'-podpis",
    9: "★★ h21-NIT-1/2 (z9-Pirczl-80J + z86-Požekh-69J!) + bolezen-GARBLE-X-open (Gallensteine[?])",
    16: "★ h37-DUEL-NIT (37[2×]-vs-17[KROP-row]-3/7-KURRENT!) + ime-TRI-GARBLE-X-open + h37 = P212-1865-HUSIČ-hiša",
    19: "★ h39-NIT-1/2 (z19-Stähler-10-mj + z52-Simic-54J!) + RUDOLFINA-×3-v-1-mesecu",
    24: "★★★ GENICKSTARRE-EPIDEMIJA-1/4 + ★ h65-NIT-1/2 (z24-Graes-2-tedna + z97-Brince-58J — h65 = P155-1889-MILEK-hiša!)",
    25: "★★★ GENICKSTARRE-EPIDEMIJA-2/4 + ★ h57-NIT (→ 1860-VALENTIN-×2-h57!) + ime-DUEL (Keržan/Križan!)",
    31: "★★★ GENICKSTARRE-EPIDEMIJA-3/4 + ★ h5-NIT-1/2 (→ P215-1862-FILAK-h5!) + unverehelicher-Knabe",
    32: "★★★ GENICKSTARRE-EPIDEMIJA-4/4 (ODRASLA-40J!) + ★ h19-NIT-1/2 (KRIŽIČ/HRIČ-2-branji!) + 'von-Griblce[?]'",
    34: "★ h26-NIT (→ 1861-MALEŠIČ-h26!) + ISTA-DATA-kot-z35 (Mai-28/30!) + 80-J-DUEL-z9",
    35: "★★ h58-NIT-1-LETO-PRED-POŽEKOM (→ 1860-z27-Barbara-Požek-8-mes!) + starost-PRAZNA ('—')",
    46: "★ h52-NIT-1/2 (z46-Peterle + z81-Posdiac!) + stan-GARBLE-X-open",
    52: "★ h39-NIT-2/2 + ★ ŠIMEC-grafia (Simic→Šimec-INNEC-lekcija-P200!)",
    53: "★ h5-NIT-2/2 (z31 + z53!) + NOV-VZROK-'Blenmorrea[~]' (Blennorrhoe?)",
    57: "★ h19-NIT-2/2 (z32 + z57!) + MARKTSFREIBN[?Marbmil]-×2-paralela (z65!)",
    61: "★ h33-NIT (→ 1863-FILAK-Grem-h33!) + ★ 1. VOJAK-stan-predzgodovine (Lediknant!) + '44-let-10-mj.'-format",
    64: "★ h74-NOVA-HIŠA-korpusa (76J!) + BRENC-nit (1860-h24-Brenc!)",
    65: "★ h29-NOVA-HIŠA-korpusa (5J!) + MARKTSFREIBN[?Marbmil]-×2 (z57!)",
    73: "★★ TAIL-P217-KOREKCIJA-1 (z73-1:1! + ime-DUEL-Klara[KROP-2×!]-vs-Elena[VLM-fresh]! — Podire/Pardire/Pezdire-TRI!) + ★ h20-NIT (P217-'h20[~10!]'→h20-1:1!) + Sep-30→Okt-1-prelom",
    76: "★★ TAIL-P217-KOREKCIJA-2 (z76-1:1! + ime-TRI-DUEL: Marlfannina[?KROP]/Katharina[VLM]/Paulmann[P217]! — Milich/Mihle/Miklik!) + ★ h24-NIT (→ 1860-Brenc-h24!) + podpis-DUEL ('J.-Halo[?]'!)",
    81: "★★★ TAIL-P217-TRAJNI-DUEL-3 (z81-99-J[VLM+KROP-2×!]-vs-83[P217]!-X-open!) + PEZDIRC-MREŽA ('Posdiac/Pesdire'≈Pezdirc!) + ★ h52-NIT-2/2 + NAJSTAREJŠI-1859 (99J!)",
    86: "★★ TAIL-P217-KOREKCIJA-4 (z86-1:1! + ime-DUEL-Anastasia[P217+KROP-glyph!]-vs-Katharina[VLM]! — Požekh[~Poček]-1:1!) + ★ h21-NIT-2/2 + POŽEK-MREŽA-2-hiši (h21 + h58!) + Joh.-Knavs",
    94: "★★★ TAIL-P217-KOREKCIJA-MAKS (z94: 'z95-Jožef-Petek-16J'-FALSIFICIRAN — margin-95→94! + ime-TRI (Josmat[?]/Josip/Jožef!) + starost-16-J→14-DNI-2:1! + vzrok-'Naussumsfinkrahn[?]'!) + ★ h49-NIT + NAJMLAJŠI-1859 (14-DNI!)",
    97: "★★★ TAIL-P217-KOREKCIJA-5 (z97: 'z100-Valentin-Brino'→margin-97! + ime-TRI-DUEL-X-open: ⅄onalfur[?]/Valentin/Ana! — Brince/Brino/'Kruška-Bina'!) + ★ h65-NIT-2/2 (P155-1889-MILEK-hiša!) + Joh.-Knavs",
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
        "    year: 1859,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {e['pag']},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P218: mrliška PREDZGODOVINA 04106, leto 1859 = 27. leto PREDZGODOVINSKE LINIJE "
    "(s011–s019 == Pag. 6–13, 103 vpisov — ŠTEVJE-IZ-VRSTIC-20.× (kronološko; written-1–91-ČISTO + "
    "93–103 = 102 + 1-NEŠTEVILČENA-s15-r12-Jalkič — 2-NOVI-TIPA-ANOMALIJ: NEŠTEVILČENA + ★★★ LUKNJA-92 "
    "(s18-91→s19-93!); vrstna-aritmetika 7+12+14+11+12(+1!)+12+12+12+11; meseci J6+F7+M7+A8+M7+J7+J6+A19+S8+O9+N7+D12; "
    "pag = sken−5; SANDBOX-RESET-REGENERACIJA: 2×-neodvisna-prenosa-md5-9/9 + vsebinska-križ-tail-vs-P217!) — "
    "★★★ 23-GRIBLJE-blokov = NOV-REKORD-PREDZGODOVINE (prej-20-1867!) / 16 hiš (6-×2: h5/h19/h21/h39/h52/h65!) + "
    "★★★ MEJA-1858/59-s11 (NASLOVNI-LIST-'Sterb-Buch.'-DEEL-2-NOVI-TISKANI-STOLPCI! + '1858'-tail-glava-KROP + "
    "tail-54–57 + VSOTNA-'1 8 [5 9]'-RAZPETE-MARKER-P214-TIP-2.-INSTANCE (1-8-KROP + 5-rob!) + restart-z1–z7-BREZ-Ločne-glave!) "
    "= 56.-POTRDITEV-invariante! + ★★★ MEJA-1859/60-s20 (P217!) + ★★★ s19 = NASLOVNI-LIST-PONOVLJEN + Dec-1859-nadaljevanje-93–103! + "
    "★★★ P217-TAIL-MISREADI-KOREKCIJE (z95→z94 + z100→z97-MARGINALI + z94-'Petek-16J'-FALSIFICIRAN→'Josmat[?]-Padierž-14-DNI'! + "
    "z97-'Valentin-Brino'→'⅄onalfur[?]-Brince'! + z73-KLARA-potrjena + z76/z86-ime-dueli!) + "
    "★★★ GENICKSTARRE-EPIDEMIJA-×4 (z24+z25+z31+z32 — Apr-16→Mai-21! NOV-VZROK!) + "
    "★★★ NOV-DUHOVNIK-'Joh.-Knavs' (podpisi-×7+! Knavs-družina-h52-X-open!) + "
    "★★★ z5+z6-PARIČ-FRAISEN-klaster-×2-Jän-27/29 + z81-99J[~83!]-TRAJNI-DUEL + otroška-umrljivost-35%-8/23 "
    "(ekstremi-14-DNI→99J!) ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count("year: 1859,")
print(f"vstavljenih blokov 1859: {n} (pričakovano 23)")
