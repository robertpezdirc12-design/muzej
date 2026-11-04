#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P205 — vstavi 17-GRIBLJE-blokov (04106, leto 1872) v parish.ts PRED P204-sekcijo."""
import json
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P204: mrliška PREDZGODOVINA 04106, leto 1873"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1872," not in src, "1872-bloki-že-obstajajo?!"

E = json.load(open("/tmp/p205/entries_1872.json"))
grib = E["griblje_entries"]

KOM = {
    13: "★★★ PEZDIR-grafia-#11-1872 ('Pecdiac/Kerdise/Perdise'!) + otrok-½-J + h50-NOVA-hiša",
    16: "★ KRIŽAN-korekcija (KROP — VLM-'Vrižan'-ZAVRJEN!) + 66-J + h66-NOVA",
    23: "★★★ h11-NIT-4.-LETO-1872 (otrok-2mes! → 1873-z177-63J → P203-16dni → P202-KUNIĆ-1875 — NEPREKINJENO!) + ime-DUEL",
    26: "★ h44-×2-#1 + 'Prümml-und-Son-Pfarre'[?]",
    28: "★★★ KROP-KOREKCIJA-ime ('Žunec'→'PRIMEJ'!) + otrok-2-DNI-Brechruhr + h44-×2-#2-v-7-dneh!",
    35: "★★★ KROP-KOREKCIJA ('Zaupšek'→'Jakofitsch'!) + otrok-1J + h6-×2-#1",
    36: "★ h5-nit (cf. P202-h5!) + otrok-1½-J + ime-DUEL",
    43: "★ hisna-DUEL (37-vs-38!) + otrok-½-J + Husič-nit",
    65: "★★★ KROP-KOREKCIJA ('Pegdirec'→'LEGAT'!) + otrok-1-TEDEN + h20-nit",
    67: "★ JAKOFČIČ-nit + otrok-8-Mon-Friesen + h6-×2-#2-v-10-dneh!",
    70: "★ otrok-¼-J + h1-nit (ZELIHA-h1-×2-1878!)",
    74: "★ hisna-DUEL (7-vs-3!) + otrok-3½-J",
    78: "★★★ KROP-KOREKCIJA ('Dejak'→'JEGLIČE'!) + 83-J + ★★★ CHOLERA-1872-NASTOP (epidemija-1873-začne-tukaj!) + h42-nit",
    85: "★ NEPOZNAN-ime-'Dutzbandl'-otrok + h62-×2-#1",
    86: "★ KURE-nit + 36-J + h62-×2-#2",
    89: "★ hisna-DUEL (8/9-vs-5!) + otrok-1½-J-Frisen",
    111: "★ h38/24-'Prilozje-in-Griblje'-DVOJNA (P204-s101-tail-1:1!) + 24-J-Nervenfieber",
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
    year: 1872,
    scan: {e['sken']},
    page: {e['pag']},
    whatSi: "{what_si.replace('"', "'")}",
    whatEn: "died {ime}, {starost} ({mes_dejansko} {smrt}, buried {pokop}) — {bolezen}; + [see-SI] + [z{z}]",
    status: "DOCUMENTED",
  }},
"""

header = """  // ——— P205: mrliška PREDZGODOVINA 04106, leto 1872 = 14. leto PREDZGODOVINSKE LINIJE (s92–s101 == Pag. 87–96, z1–z114 = 114 vpisov — ŠTEVJE-IZ-VRSTIC-7.× (ordinali-partial-vidni: s101-'102–110'-jasno; VLM-drift-×n!); vrstna-aritmetika 9+11+13+12+11+11+14+13+12+9; meseci J21-MAX+F1-MIN+M3+A15+M13+J4+J5+A9+S12+O6+N6+D10; pag = sken−5, md5-križna-ta-seja: s100+s101-sveža == P204-disk-1:1 — veriga-P197→…→P205-9.×!) — 17 GRIBLJE-blokov / 14 hiš + ★★★ MEJA-1871/72-s92 (1871-tail-×3 + 'vsota'-vrsica-1.×-v-korpusu + 'Jänner'-glava + restart!) + ★★★ 'finis'-s101-1.× + ★★★ CHOLERA-1872-NASTOP (z78-Jegliče-83J!) + ★★★ KROP-KOREKCIJE-×5 + h11-NIT-4.-leto! ———
"""

blocks = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, header + blocks + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
print(f"OK — 1872-bloki: {len(grib)}")
