#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P213 — vstavi 17-GRIBLJE-blokov (04106, leto 1864) v parish.ts PRED P212-sekcijo. IDEMPOTENTEN."""
import json, re
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P212: mrliška PREDZGODOVINA 04106, leto 1865"

E = json.load(open("/tmp/p213/entries_1864.json"))
grib = E["griblje_entries"]
assert len(grib) == 17, f"grib={len(grib)}"

# idempotenca: odstrani prejšnje P213-bloke (če obstajajo)
P213_HDR = "  // ——— P213: mrliška PREDZGODOVINA 04106, leto 1864"
if P213_HDR in src:
    i = src.index(P213_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P213-bloke (idempotenca)")

KOM = {
    6: "★★★ X-open-IME-GARBLE ('?ollganerischb-Kind-von' — ultra-zoom-6×; VLM-2-branja-FALSIFICIRANA!) + FORMULA-hipoteza-≈'uneheliches-Kind-von' (cf. z80/z84-ISTI-formula!) + KRIŽAN-nit (otrok-Johanna-Križana-½-Güblerja!)",
    9: "★ KRIŽAN-nit-#1 (Maria-87-J-NAJSTAREJŠA-1864-h62 — cf. 1865-z1-Maria-Križan-h3 + P212-2×-Maria-Križan!) + stan-GARBLE-HONEST ('¼-Gürlichanderuib'≈¼-Güblerin?)",
    10: "★ ŠIMEC-grafia-#1 (Mathias-65-J-h19 — cf. z34-Peter-ŠIMIC-h18! 2-hiši-1-leto!)",
    12: "★ KLEPEC-nit (Maria-2-J-h2-weiler-Pragovi[~] — ½-Güblerstochter! cf. h45 + Lemež-z14!)",
    13: "★ ime-DUEL-HONEST ('Obrawos[~Obranos?]' — X-open!) + h45-nit (Georg-73-J-Altlöbler[~])",
    18: "★★★ KROP-VIZUALNA-ADJUDIKACIJA-3-FAZNA (hisna-'14'-4-IMA-ZANKO! + ime-PEZDIRC-via-glyph-comparacija-z85! + starost-6-M!) + ★★★ PEZDIRC-h14-NIT-1864 (Michael-6-M → 1865-z41-Mathias-unehelich → 1865-tail-z66-Maria! 3-LETA-GLOBOKO!)",
    27: "★★★ KROP-VIZUAL-'3' (dvoja-izboklina ≠5≠8!) + DRAGOŠ-glyph (Georg-70-J-h3 — cf. P200-DRAGOŠ-h12-nit! h3 = KRIŽAN-h3-nit-1865!)",
    30: "★★★ ŽELKO-nit-#1 (Anna-22-J-½-Witwe-h1 — cf. z35-Peter-ŽELKO-h1! ×2-MAJ-klaster!)",
    31: "★ 'Kitah'-grafia-X-open (Matthias-5-J-h16 — cf. z32-Grem-Michael-Kitah — brata?)",
    33: "★★★ KROP-VIZUAL-FILAK ('-ilak'-rez! duels-'Kitah'/'Šilak'-FALSIFICIRANI!) + ★★★ FILAK-h34-NIT-1864 (→ P211-z48-z80! 3.-leto!)",
    34: "★★★ KROP-VIZUAL-ŠIMIC (haček-Š! duel-'Jinnie'-FALSIFICIRAN!) + ★★★ ŠIMEC-h18-NIT (cf. P200-h18-1877!)",
    35: "★★★ ŽELKO-h1-×2-KLASTER-#2 (Peter-1-J — 13-dni-po-z30-Anna! mati+sin-hipezoza! cf. P212-HUSIČ-h37!)",
    36: "★★★ POŽEK-h67-NIT-1864 (KROP-'Požeh'! duel-'Pogach'-FALSIFICIRAN!) — h67-veriga: 1864-z36-Maria → 1865-z36-Mathias (ISTI-z36!)",
    44: "★★★ KROP-VIZUAL-'71' (γ-7-S-PREČKO! duels-'11[~71?]'-VLM-'7'-FALSIFICIRANA!) + h71-DUEL-KONTINUITETA (P210-z26!) + STRAUS-mreža?-X-open",
    61: "★★★ KROP-VIZUAL-CALIBRACIJA-'5' (z60-'1'/z62-'8'-primerjava! VLM-'3'-×2-FALSIFICIRANA — KURRENT-3/5/8!) + ★ NOVA-hiša-h5-X-open + stan-'¼'-KROP (duel-'½'!)",
    64: "★ KURRENT-J/G/Z-duel ('Zager'-KROP vs 'Gašek'-VLM — X-open!) + h27-nit (Mathias-1-Mt-Krämpfe)",
    85: "★★★ KROP-VIZUAL-×3 (ime-'Anna-Pezdirc'! + hisna-'11'-DVE-OZKI-1 ≠ z18-'14'! + datumi-Dec-2./4.-ČISTO!) + ★★★ ANOMALIJA-NE-KRONOLOŠKI-VNOS-2.-×-leta (po-z84-Dec-11.[~] — cf. P212-z13!) + ★★★ PEZDIRC-h11 (2-hiši-nit!)",
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
        "    year: 1864,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {e['pag']},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P213: mrliška PREDZGODOVINA 04106, leto 1864 = 22. leto PREDZGODOVINSKE LINIJE "
    "(s039–s046 == Pag. 34–41, z1–z91 = 91 vpisov — ŠTEVJE-IZ-VRSTIC-15.× (ordinali-1–91-ČISTO — "
    "7.-LETO-ZAPORED-BREZ-luknje/dupa!; vrstna-aritmetika 2+14+14+14+15+14+14+4; meseci J2+F5+M8+A13+M11+J5+J7+A8+S9+O6+N7+D10; "
    "pag = sken−5; 2×-neodvisna-prenosa-8/8-md5!) — 17-GRIBLJE-blokov / 16 hiš (h1-×2-ŽELKO!) + "
    "★★★ MEJA-1863/64-s39 (tail-1863-z55–z64 + vsotna-vrstica-1-8-6-4 + restart-z1–z2! + '1864'-VELIKA-LETVICA-na-s40-glavi = "
    "51.-POTRDITEV-invariante!) + ★★★ s41-SHIFT-SANACIJA (VLM-zap-+1-pomik — 2.×-po-P158! margin-17–30-KROP-VIZUALNO!) + "
    "★★★ 8-KROP-VIZUALNIH-ADJUDIKACIJ (z18-h14-PEZDIRC + z27-h3-DRAGOŠ-glyph + z33-FILAK + z34-ŠIMIC + z44-h71-γ-7 + "
    "z61-h5-CALIBRACIJA + z85-PEZDIRC-h11 + z85-datumi!) + ★★★ ANOMALIJA-NE-KRONOLOŠKI-VNOS-z85 (2.-×-leta!) + "
    "★★★ PEZDIRC-×2-hiši (h14+h11!) + ŽELKO-h1-×2-MAJ-klaster + FILAK-h34-3.-leto + ŠIMEC-×2-hiši + POŽEK-h67-nit + "
    "KRIŽAN-×2-hiši + otroška-umrljivost-53%-9/17 (VIŠJA-kot-1865-31%!) ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count("year: 1864,")
print(f"vstavljenih blokov 1864: {n} (pričakovano 17)")
