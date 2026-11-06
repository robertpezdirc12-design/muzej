#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P220 — vstavi 10-GRIBLJE-blokov (04106, leto 1857 = ZADNJE leto knjige!) v parish.ts PRED P219-sekcijo. IDEMPOTENTEN."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P219: mrliška PREDZGODOVINA 04106, leto 1858"

E = json.load(open("/tmp/p220/entries_1857.json"))
grib = E["griblje_entries"]
assert len(grib) == 10, f"grib={len(grib)}"

P220_HDR = "  // ——— P220: mrliška PREDZGODOVINA 04106, leto 1857"
if P220_HDR in src:
    i = src.index(P220_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P220-bloke (idempotenca)")

KOM = {
    4: "★ 1.-GRIBLJE-vpis-KNJIGE-04106-kadarkoli (z4 = 4.-vpis-knjige!) + h60/66-DUEL (TOMINC-h60-nit-X-open!) + ime-TRI-DUEL (Lazar/Luka/Peter-Pečenko!)",
    5: "★ PRVI-vpis-h64-v-korpusu + priimek-4×-križ (Verbičar!) + 'iz-Griblje'-stan",
    10: "★ PRVI-vpis-h52-v-korpusu (P218-'Posdiac[?]'-h52-99J + Knavs-družina-h52!) + ime-TRI-DUEL (Peskar/Bedric/Petrič!)",
    45: "★ PRVI-vpis-h13-v-korpusu + ime-DRAGOŠ-družina (cf. P193-h3-DRAGOŠ-1864!) + spol-DUEL (Marija-vs-Martin!) + SCARLATINA?-klaster-6/7",
    50: "★★★ h36-KRIŽAN-×2-v-1857 (1/2 — otrok-4J!) + ime-DUEL (Križan-2×-križ-vs-Krajncan!) + PRVI-vpis-h36!",
    56: "★ PRVI-vpis-h31-v-korpusu + hiša-TRI-DUEL (31/51/57!) + ime-3×-križ (Ana-Urih!)",
    58: "★ PRVI-vpis-h48-v-korpusu + honesty-MAX (hiša-TRI-DUEL-48/43/145 + ime-TRI-DUEL-Stamcar/Straus/Maria + starost-DUEL-66/Kind!)",
    61: "★★★ PRVI-vpis-h65-MILEK-hiša-v-korpusu (1858-'Keržan[?]' → 1859-×2 → MILEK-mreža-04894-×9!) + priimek-TRI-garble (Mulik/Mililkh/Gobik!)",
    71: "★ hiša-NEBERLJIVA-3× (edini-primer-1857!) + STAROST-DUEL (14-let-vs-1-mj-1-dan — dojenček-hipoteza!) + NEZAKONSKI-kandidat ('ganz-außerehelich'!) + duhovnik-Verbič-cooperator",
    74: "★★★ TAIL-1857 = ZADNJI-vpis-leta + h36-KRIŽAN-×2 (2/2 — 73J-NAJSTAREJŠI-Griblje-1857!) + 4×-priimek-garble (Križan!) + duhovnik-'J.-Knauš/Kranz[?]' — MOŽEN-ZGODNJI-Knavs-podpis (KOREKCIJA-P219-lead: ŽE-DEC-1857 — X-open!)",
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
    znum = int(str(z).replace("z", ""))
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
        "    year: 1857,\n"
        f"    scan: {e['sken']},\n"
        f"    page: {e['pag']},\n"
        f'    whatSi: "{esc(what)}",\n'
        f'    whatEn: "{esc(what_en)}",\n'
        '    status: "DOCUMENTED",\n'
        "  },\n"
    )

GLAVA = (
    "  // ——— P220: mrliška PREDZGODOVINA 04106, leto 1857 = 29/29 — ZADNJE leto knjige — "
    "PREDZGODOVINSKA LINIJA KONČANA! (s002–s007 == pag sken−1-SVINČNIK-FOLIACIJA-ARHIVARJA "
    "(dokumentirano-3×: s4='3'/s5='4'/s7='6'!) — KONVENCIJSKI-PREHOD: sken−5-NEMOŽEN-za-s1–s5!; "
    "★★★ KNJIGA-04106-SE-ZAČNE-1857: s1-NASLOVNI-LIST-'Tom. III'-'Sterb-Buch'-'Podzemelj' + s2-RAZPRTA-NASLOVNA + "
    "'18 57'-RAZPETA-letnica-glava (rokopisna-nadčrtana!) + restart-z1 — MEJA-1856/57-NE-OBSTAJA!; "
    "73 vpisov-kronološko — ŠTEVJE-IZ-VRSTIC-22.× (WRITTEN-1–31 + 33–74 = 73-ČISTO; "
    "★★★ LUKNJA-32 — pisarski-preskok-3.-instance-po-LUKNJA-92-1859! — s3-ordinali-konča-31 + s3-dno-PRAZNO (3-kropi!) + "
    "s4-začne-33 + seam-Juni-21/22→Juni-21/23-GLADAK — X-open-morda-obrezan!; vrstna-aritmetika 16+15+13+13+14+2; "
    "meseci J4+F8+M5+A5+M7+J3+J6+A18+S8+O0!!+N5+D4 — ★★★ OKTOBER-×0 (z65-Sep-24/26 → z66-Nov-9/11!) — "
    "2-POPRAVKI-PISARJA (s3-'1867'→1857 + s4-z33-'1858'→1857!)) — "
    "★★★ 10-GRIBLJE-blokov / 9 hiš (h36-×2-KRIŽAN: z50-otrok-4J + z74-Marijan-73J-TAIL!; z71-hiša-NEBERLJIVA-3×!) + "
    "★★★ 8-od-10-hiš-dobi-PRVI-vpis-v-korpusu (h13/h31/h36/h48/h52/h60?/h64/h65 — 1857 = 1.-leto-knjige!) + "
    "★★★ SCARLATINA?-klaster-×13–14 ('Rušfieber'-×6–7 + 'Amigdilitis[?]'-×7 — 2.-val-X-open — 1-GRIBLJE-z45!) + "
    "★★★ MEJA-1857/58-s7 (P219 + re-križ-P220-arb_s7_meja-1:1: TAIL-z73–z74 + VSOTNA-'1 8 5 [8]'-P214-TIP-3.-INSTANCE + "
    "restart + NEŠTEVILČENA!) = 59.-POTRDITEV-invariante! + "
    "★★★ z74-duhovnik-'J.-Knauš/Kranz[?]' — MOŽEN-ZGODNJI-Knavs-podpis (KOREKCIJA-P219-lead: ŽE-DEC-1857 — X-open!) + "
    "otroška-umrljivost-30%-3/10 (+z71-duel-→-40%!) — ekstremi-3-tedne-→-73-J — duhovniki: 'Ladergal'-garble-klaster-DOMINANTA "
    "(8-variant!) + Skubic + Verbič-cooperator ———\n"
)

bloki = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, GLAVA + bloki + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
n = src.count("year: 1857,")
print(f"vstavljenih blokov 1857: {n} (pričakovano 10)")
