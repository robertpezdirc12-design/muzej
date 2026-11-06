#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P208 — vstavi 14-GRIBLJE-blokov (04106, leto 1869) v parish.ts PRED P207-sekcijo."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/muzej-backup/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P207: mrliška PREDZGODOVINA 04106, leto 1870"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1869," not in src, "1869-bloki-že-obstajajo?!"

E = json.load(open("/tmp/p208/entries_1869.json"))
grib = E["griblje_entries"]

KOM = {
    1: "★★★ ULEDBA-NOVO-LETO (Jänner-1./2.! — vzorec-3.×: P201-z1 + P203-z1!) + '1869-Jänner'-glava-KROP-47.-POTRDITEV-invariante! + h22-×2-#1 + ime-'Milik' (MILIČ-grafia)",
    13: "★ hišna-[?]-NEBERLJIVA (KROP-y-drift-2×-fail — celostanska-[?]!) + 'bey 60 J'",
    17: "★ h13-JAKOFČIČ-nit (→ 1868-tail-z80-Agnes-Jakofčič-h13! + 1871-z17-h13!)",
    24: "★★★ h12-DRAGOS-nit (Michael-27J-Hirnhautentzündung — → 1877-P200-DRAGOŠ-h12 — ISTE-HIŠE-8-let!)",
    31: "★ h65-×2-#1 + '44½-let'-frakcija + Brine (BRINEC-grafia)",
    33: "★ h22-×2-#2 (Milik-Jänner + Miller-Juni — 2-vpisa-isto-hišo!) + ime-'Miller'[?]",
    36: "★ h49-BRODARIČ-nit (otrok-3-J-Friesen — cf. mrliška-1888-h49? — BRODARIČ-vzorec)",
    40: "★ h20-PEZDIRE-nit (PEZDIR-grafia! — cf. 1870-z39-Pezić-h40 + 1870-z54-Poždire-h20!)",
    52: "★ h73-nit (Janez-Krambri-18J — NOVA-hiša-korpusa!)",
    54: "★ h47[~]-hišna-DUEL + mesec-DUEL-'September/October-30./2.' (ULEDBA-vzorec!) + Reisfieber[?]",
    58: "★ h72-nit (Katharina-Ivanus-1J — → 1871-z32-Strovs-h72 + 1874-h72!)",
    60: "★★★ h28-POŽEK-NIT-3.-LETO (Ana-Pižek-5-mes-Oct-1869 → 1870-z51-Johann → 1871-z50-Georg — NEPREKINJENO-3-LETA!)",
    61: "★ h70-nit + PEZDIR-grafia-'Maria-Pezdir' + Gichtfieber",
    74: "★ h65-×2-#2 + 'Noßgabianstho-Kind' (NUSSGABIANSTHO-dajalec-obroka! cf. ½-Bibl/Grible-forme!) + Mlinič + neotenjeno",
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
    hn = str(e.get('hisna', '?')).split()[0]
    return f"""  {{
    houseNo: "{hn}",
    bookSignature: "04106",
    year: 1869,
    scan: {e['sken']},
    page: {e['pag']},
    whatSi: "{what_si.replace('"', "'")}",
    whatEn: "died {ime}, {starost} ({mes_dejansko} {smrt}, buried {pokop}) — {bolezen}; + [see-SI] + [z{z}]",
    status: "DOCUMENTED",
  }},
"""

header = """  // ——— P208: mrliška PREDZGODOVINA 04106, leto 1869 = 17. leto PREDZGODOVINSKE LINIJE (s75–s80 == Pag. 70–75, z1–z76 = 76 vpisov — ŠTEVJE-IZ-VRSTIC-10.× (ordinali-1–76-ČISTO-BREZ-luknje/dupa — 2.-LETO-ZAPORED-ČISTO!; ord-stolpci-×3.5: s75-'77,78,79,80→1–9' + s80-'65–76'; vrstna-aritmetika 9+14+14+13+14+12; meseci J7+F6+M5+A5+M3+J7+J5(+1-dualni)+A4+S10-MAX(+1-ULEDBA)+O8+N7+D7; pag = sken−5, md5-križna-ta-seja: s78+s79+s80-sveži == P207-disk-1:1 — veriga-P197→…→P208-12.×!) — 14 GRIBLJE-blokov / 13-14 hiš (h22-×2!-h65-×2!-+1-[?]) + ★★★ MEJA-1868/69-s75 (1868-tail-×4-zap-77–80 + 'vsota'-'1|8'-3.×-V-KORPUSU-1:1-FORMA! + '1869-Jänner'-glava-KROP-47.-POTRDITEV-invariante + RESTART-1–9! s71–s74-1868-kontekst-zap-24–76!) + KONEC-1869-s80-'VALOVITA-ČRTA' (P207-potrjeno!) + ★★★ ULEDBA-NOVO-LETO-z1 (Jänner-1./2.-Milik!) + ★★★ h28-POŽEK-NIT-3.-LETO (z60-Ana-Pižek → 1870-Johann → 1871-Georg!) + ★★★ h12-DRAGOS-nit (→ 1877-DRAGOŠ-ISTE-HIŠE!) + h65-×2-'Noßgabianstho'-z74 + PEZDIR-grafia-×3 (z40-z61-+1870!) ———
"""

blocks = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, header + blocks + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
print(f"OK — 1869-bloki: {len(grib)}")
