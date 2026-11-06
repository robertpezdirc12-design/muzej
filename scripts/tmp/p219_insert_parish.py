#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P219 — vstavi 10-GRIBLJE-blokov (04106, leto 1858) v parish.ts PRED P218-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P218: mrliška PREDZGODOVINA 04106, leto 1859"

E = json.load(open("/tmp/p219/entries_1858.json"))
grib = E["griblje_entries"]
assert len(grib) == 10, f"grib={len(grib)}"

P219_HDR = "  // ——— P219: mrliška PREDZGODOVINA 04106, leto 1858"
if P219_HDR in src:
    i = src.index(P219_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P219-bloke (idempotenca)")

KOM = {
    15: "★ h49-NIT-1/2 (z15-'Radine[?]'-19J + 1859-z94-Padierž-14-DNI — BRODARIČ-hiša-2-obdobji!) + GAUFIGALBRANN[?]-nit-1/4 + hisna-DUEL-3× (49[glif]/19[page]/44[krop-VLM]!)",
    16: "★★★ DVOJČEK-1/2 (ZWILLINGE-h19! Ana-Simic-2-dni!) + GAUFIGALBRANN[?]-nit-2/4 + h19-DRAMA-nit (1858-×3 → 1859-×2-Križič/Hrič!)",
    17: "★★★ DVOJČEK-2/2 ('zwilling-Genickfand-kind'-2-vrstica! Mannier[?]-½-dni[?]) + GAUFIGALBRANN-nit-3/4 + PRE-EHO-1859-GENICKSTARRE-EPIDEMIJE!",
    27: "★ h19-DRAMA-3/3 (dvojčka + Kurič-7-mj — 3-otroške-smrti-h19-v-1858!) + FRAISEN-nit (→ 1859-Jän-PARIČ-klaster-×2-P218!) + ime-TRI-DUEL-X-open (Kurič/Kreite/Krix/Petrič!)",
    37: "★ h60-TOMINC-nit (1858-Jakob-60J → 1881-Katharina-TOMINC-Müllerjeva-vdova!) + Joh.-Knavs-1:1",
    39: "★★★ NOV-DUHOVNIK-DUEL ('J.-Auber[?]/Huber[?]-P.'-4×-zoom — vs-Knavs-dominanta + Šinkovec[?]page-garble!) + h65-MILEK-hiša + ime-TRI-DUEL (Keržan/Kerzmann/Deželak!)",
    42: "★ h3-KRIŽAN-nit-1/3 (1858-Kind → 1865-Maria → 1882-Dorothea-VRIŽAN + 04894-KRIŽAN-×4!) + starost-'0'-duel + ime-TRI-DUEL (Križan/Horvat/Vozan!)",
    47: "★ h2-KLEPEC/HLEBEC-nit (1858-otrok-8-tednov → 1864/67/71-Klepec-×3 → 1880/81!) + Knavs-grafija-'Khubiz'",
    51: "★ h44-ŠTRUCELJ-nit-1/3 (1858-18J → 1867-Strucež-1½J → 1873-Barbara + 04894/04455/04105-Štrucelj-mreža!) + ime-spol-DUEL (Anna[2×viz!]-vs-Anton[page]!)",
    52: "★★★ PEZDIRC-MREŽA-NAJGLABLJE: 'Padire'-h50-1858 → 1868-Perdirc → 1872-Kerdise-PEZDIR → 1924-PERDIRC-POSESTNIK — 4-GENERACIJSKA-GRAFIJA-LINIJA-×4-V-ISTI-HIŠI! + ime/spol-duel (Maria/Martin) + starost-duel (68[?])",
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
    znum = int(str(z).replace("z", "").split("-")[0]) if str(z).startswith("z") else None
    kom = KOM.get(znum, "")
    mes = mesec.split()[0] if mesec else ""
    mes = {"Februar": "Feber", "Januar": "Jänner", "December": "Dezember", "Junij": "Juni"}.get(mes, mes)
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
        "    year: 1858,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {e['sken'] - 5},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P219: mrliška PREDZGODOVINA 04106, leto 1858 = 28. leto PREDZGODOVINSKE LINIJE "
    "(s007–s011 == sken−5-konvencija; 58 vpisov-kronološko — ŠTEVJE-IZ-VRSTIC-21.× (WRITTEN-1–57-ČISTO-BREZ-luknij — "
    "ČISTA-ORDINALNA-LINIJA-2.-leto-zapored! + 1-NEŠTEVILČENA-s7-zadnja (Jan-29/31 — levi-stolpec-PRAZEN-KROP-2.× — "
    "2.-instance-po-P218-s15-Jalkič!); vrstna-aritmetika 11+1(NEŠTEVILČENA!)+14+14+14+4; meseci J12+F8+M6+A6+M5+J4+J6+A2+S4+O2+N1+D2; "
    "pag = sken−5-KORPUS-KONVENCIJA — svinčnik-foliacija-arhivarja = sken−1 (s7='6'...s11='10')-dokumentirana!; "
    "SANDBOX-RESET: 2×-neodvisna-prenosa-md5-8/8!) — "
    "★★★ 10-GRIBLJE-blokov / 8 hiš (h19-×3-TRIPLE — edina-×3-v-predzgodovini!) + "
    "★★★ MEJA-1857/58-s7 (NASLOVNI-LIST-RAZPRTA + TAIL-1857-z73–z74 (Gradac + ★ GRIBLJE-h36-'Križan/Krisan[?]'-73J!) + VSOTNA-'1 8 [5 8]'-RAZPETE-MARKER-P214-TIP-3.-INSTANCE + "
    "rokopisna-'Jänner-1858'-glava + restart-z1–z11 + ★ NEŠTEVILČENA!) = 57.-POTRDITEV-invariante! + "
    "★★★ MEJA-1858/59-s11 (P218! re-križ-1:1!) = 58.-POTRDITEV! + "
    "★★★ NASLOVNA-LISTA-s9+s10-SREDI-1858 (quiri-prelom! page-VLM-s10-ujel-LE-4/14-'30–33'-MISREAD → KROP-zap-POTRJENO-40–53-ČISTO-glif-viz-1:1!) + "
    "★★★ DVOJČKI-SIMIC-h19 (z16-2-dni + z17-'zwilling-Genickfand-kind'-½-dni[?] — ZWILLINGE!) + "
    "★★★ GAUFIGALBRANN[?]-KLASTER-×4 (z15/z16/z17 + z27-Fraisin — Feb-Apr!) + "
    "★★★ PEZDIRC-MREŽA-NAJGLABLJE-'Padire'-h50 (1858 → 1868-Perdirc → 1872-Kerdise → 1924-PERDIRC — 4-GENERACIJE-V-ISTI-HIŠI!) + "
    "★★★ NOV-DUHOVNIK-DUEL-'J.-Auber[?]/Huber[?]-P.' (z39! vs-Knavs-dominanta — KOREKCIJA-P218: Knavs-ŽE-Feb-1858! grafije-'Khubiz/Knavo/Knaff') + "
    "otroška-umrljivost-50%-5/10 (ekstremi-0[?]-→-68-J[?]-dueli!) ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count("year: 1858,")
print(f"vstavljenih blokov 1858: {n} (pričakovano 10)")
