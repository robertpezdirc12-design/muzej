#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P214 — vstavi 7-GRIBLJE-blokov (04106, leto 1863) v parish.ts PRED P213-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P213: mrliška PREDZGODOVINA 04106, leto 1864"

E = json.load(open("/tmp/p214/entries_1863.json"))
grib = E["griblje_entries"]
assert len(grib) == 7, f"grib={len(grib)}"

P214_HDR = "  // ——— P214: mrliška PREDZGODOVINA 04106, leto 1863"
if P214_HDR in src:
    i = src.index(P214_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P214-bloke (idempotenca)")

KOM = {
    2: "★★★ KROP-VIZUALNI-ADJUDIKACIJI-×2 (ime-'Kune'-4-branja-X-open-HONEST: 'Kumre'/'Kime'/'Kure' — KURRENT-m/n+u/r! + bolezen-'Gehirnentzündung'-POTRJENA — duel-'Gichtschmerzen'-FALSIFICIRAN!) + h10-NOVA-hiša-X-open",
    12: "★★★ KROP-×3 (hisna-'65'-KROP+VIZUALNO — duel-full-page-'68'-FALSIFICIRAN! + bolezen-'Lungenentzündung+Magenkrampf'-2-vrstično + opomba-'unehelich'-ANMERKUNG!) + ★★★ BRINC-h65-NOVA-HIŠA (3.-BRINC-hiša: cf. 1865-h23-Anna + 1865-h28-Jernej!) + UNEHELICH-1.-v-GRIBLJE-korpusu!",
    18: "★★★ h32-TRIJSKOTRJENA (full-page + KROP + VIZUALNO-s36!) + starost-'65J'-VIZUALNO (duel-'68'-FALSIFICIRAN!) + ULRICH-nova (cf. 1864-z6-'Ulrich'?-X-open)",
    26: "★★★ KROP-h18 + VIZUALNO (2×-neodvisno!) + starost-'53J'-VIZUALNO + stan-'¼-Güblerssohn'-VIZUALNO + ★★★ ŠIMEC-h18-NIT-ČEZ-LETA (1863-z26-Georg-Simic → 1864-z34-Peter-ŠIMIC-h18-ISTO-HIŠO! + h19! 2-HIŠI-2-LETI!)",
    27: "★★★ HISNA-DUEL-HONEST ('11'-KROP-tight-'ozka-črtica' — ALTERNATIVA-'71'-γ-7-S-PREČKA! cf. 1864-z44-h71!) + ★★★ STRAUS-mreža-X-open (1863-'Joannes-Straus'-TRI-branja-K/G/S! + 1864-'Anna-Strauž'-h71 — POPOLNA-γ-7-KORELACIJA-2-LETI!)",
    33: "★★ h53-2× (KROP + VIZUALNO!) + datumi-'13.|15.'-VIZUALNO + ★ SIMIC-×2-1863-2-hiši (h18+h53 — PATTERN-cf.-1864-×2-h18/h19!)",
    38: "★★★ IME-DUEL-X-open-HONEST ('Rosalia-infans'-'hči-Joh.-Brozič[~Broznik?/Barak?]' — 4-branja: VIZUALNO-'infant-Rosalia-2-vrstično' + 'Josef-Brozik'-FALSIFICIRANA-sinteza + 'Rojč/Jože'-garble!) + starost-TRAJNI-duel ('1½-J'/'3-J') + h21-NOVA-hiša-X-open + bolezen-'Dreinsucht'(dizenterija!)",
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
        "    year: 1863,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {e['pag']},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P214: mrliška PREDZGODOVINA 04106, leto 1863 = 23. leto PREDZGODOVINSKE LINIJE "
    "(s033–s039 == Pag. 28–34, z1–z64 = 64 vpisov — ŠTEVJE-IZ-VRSTIC-16.× (ordinali-1–64-ČISTO — "
    "8.-LETO-ZAPORED-BREZ-luknje/dupa!; vrstna-aritmetika 8+15+15+16+10; meseci J9+F6+M8+A2+M6+J6+J11+A2+S1+O1+N5+D7; "
    "pag = sken−5; 2×-neodvisna-prenosa-7/7-md5 + s39-carry-P213!) — 7-GRIBLJE-blokov / 7 hiš (NAJMANJ-v-predzgodovini!) + "
    "★★★ MEJA-1862/63-s35 (tail-1862-z55–z60 + VSOTNA-'1|8|6|3'-'1863'-MARKER + restart-z1–z8! + '1863'-rokopisna-glava = "
    "52.-POTRDITEV-invariante!) + ★★★ MEJA-1863/64-s39-tail (z64-ULEDBA-#11-12.×-EKSPLICITNI-LETNICI-'31.Dec.1863'-'2.Jän.1864'! + "
    "VSOTNA-'1|8|6|4'-'1864'-MARKER!) + ★★★ NOV-INVARIANTA-TIP: VSOTNA-VRSTA = LETNICA-MARKER-naslednjega-leta (cifre-razpete-čez-stolpce!) + "
    "★★★ 7-KROP-VIZUALNIH-ADJUDIKACIJSKIH-SKUPIN (z2-Kune-4-branja + z12-h65/bolezen/'unehelich'-opomba + z18-h32/65J + z26-h18-ŠIMEC-nit + "
    "z27-h11[~71!]-STRAUS + z33-h53 + z38-Rosalia-infans-4-branja!) + ★★★ ŠIMEC-h18-NIT-ČEZ-LETA (1863-z26 → 1864-z34-ISTO-HIŠA!) + "
    "★★★ BRINC-h65-NOVA (3.-hiša!) + ★★★ STRAUS-h71-korelacija-γ-7-2-LETI + ★★★ FILAK-Grem-h33-×2-v-3-tednih + "
    "z53-'außereheliches-Kind-von'-FORMULA-DOKAZ-P213-z6! + otroška-umrljivost-29%-2/7 (NAJNIŽJA-do-zdaj!) ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count("year: 1863,")
print(f"vstavljenih blokov 1863: {n} (pričakovano 7)")
