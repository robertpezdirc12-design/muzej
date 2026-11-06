#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P206 — vstavi 11-GRIBLJE-blokov (04106, leto 1871) v parish.ts PRED P205-sekcijo."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P205: mrliška PREDZGODOVINA 04106, leto 1872"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1871," not in src, "1871-bloki-že-obstajajo?!"

E = json.load(open("/tmp/p206/entries_1871.json"))
grib = E["griblje_entries"]

KOM = {
    5: "★★★ h11-NIT-5.-LETO-1871 (Plut-13J-Gehirnentzündung → 1872-z23-otrok-2mes → 1873-63J → 1874-16dni → 1875-KUNIĆ — NEPREKINJENO! h11-nit-RAZŠIRJENA-NAZAJ)",
    17: "★★★ ime-DUEL (VLM-'Maria-Jančarič' vs KROP-'Anton-Grüblner-Tonis[?]'!) + starost-'110 J'[?] (KURRENT-zmeda!)",
    20: "★★★ ordinala-20-potrjena (ord-stolpec-cele-s88-×3.5: 19,19,20–30!) + hišna-DUEL (33-vs-62/65-KROP!) + ime-DUEL (Arik-vs-Urih!)",
    29: "★★★ stan-'Ablasser'-(odpustitelj!) + hišna-DUEL (66-vs-65-KROP-×2!) + 65½-J (KROP!) + dup-19-kontekst",
    32: "★ h72-nit (→1874-mrtvorojen-Mai + 1874-Malensič-72J!) + stan-'Urbler'[?]",
    50: "★★★ KROP-POPOLNO-SOGLASJE (5¾-J-vs-'5let[~5½]'!) + '¼-Griblerjev-sohn' + h28-nit (Požek-1870-s85-h28!)",
    61: "★ VLM-'None/None'-starost+bolezen-n/v (iz-izreza) — celostanska-negotovost",
    62: "★ h2-nit (→1873-Hlebec + 1874!)",
    67: "★ h8-nit (1871-Lakovčič-85J-Dec!)",
}

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
    mes_dejansko = {"Februar": "Feber", "Januar": "Jänner", "December": "Dezember", "Junij": "Juni"}.get(mesec.split()[0] if mesec else "", mesec.split()[0] if mesec else "")
    what_si = f"umrl(a) {ime}"
    if stan: what_si += f", '{stan}'"
    what_si += f", {starost} ({mes_dejansko} {smrt}, pokop {pokop}) — {bolezen}"
    if kom: what_si += f"; + {kom}"
    what_si += f" + [z{z}]"
    return f"""  {{
    houseNo: "{e.get('hisna', '?')}",
    bookSignature: "04106",
    year: 1871,
    scan: {e['sken']},
    page: {e['pag']},
    whatSi: "{what_si.replace('"', "'")}",
    whatEn: "died {ime}, {starost} ({mes_dejansko} {smrt}, buried {pokop}) — {bolezen}; + [see-SI] + [z{z}]",
    status: "DOCUMENTED",
  }},
"""

header = """  // ——— P206: mrliška PREDZGODOVINA 04106, leto 1871 = 15. leto PREDZGODOVINSKE LINIJE (s86–s92 == Pag. 81–87, z1–z73 = 73 vpisov — ŠTEVJE-IZ-VRSTIC-8.× (ordinali-1–73: LUK-18-pisarski-preskok (s87-zap-17 → s88-zap-19!) + DUP-19-×2-s88 (r1-Drugoše-Kumin + r2-Primostek-Klavec!) — ord-stolpec-cele-s88-×3.5: 19,19,20,21,…,30!); vrstna-aritmetika 4+13+13+14+14+12+3; meseci J7+F4+M4+A8+M9+J5+A5+S8+O9+N4+D10; pag = sken−5, md5-križna-ta-seja: s92-sveža == P205-disk-1:1 — veriga-P197→…→P206-10.×!) — 11 GRIBLJE-blokov / 11 hiš (vsi-različni!) + ★★★ MEJA-1870/71-s86 (1870-tail-×7-zap-64–70 + 'vsota'-'1|8'-2.×-v-korpusu + 'Jänner'-glava + restart! — s84/s85-1870-kontekst-'1876'-glava-MISREAD!) + ★★★ MEJA-1871/72-s92 ('December-1871'-glava-KROP-1:1-P205-soglasje!) + ★★★ h11-NIT-5.-LETO-1871 (z5-Plut-13J!) + ★★★ ime-DUEL-z17 ('Maria-Jančarič'-vs-'Anton-Grüblner-Tonis'!) + ★★★ stan-'ABlasser'-z29 (odpustitelj!) + ★★★ KROP-POPOLNO-SOGLASJE-z50 (5¾-J!) + ordinala-DUEL-z20-Arik-20-! ———
"""

blocks = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, header + blocks + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
print(f"OK — 1871-bloki: {len(grib)}")
