#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P207 — vstavi 12-GRIBLJE-blokov (04106, leto 1870) v parish.ts PRED P206-sekcijo."""
import json
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P206: mrliška PREDZGODOVINA 04106, leto 1871"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1870," not in src, "1870-bloki-že-obstajajo?!"

E = json.load(open("/tmp/p207/entries_1870.json"))
grib = E["griblje_entries"]

KOM = {
    19: "★ otrok-2-J + h4-nit (Jakofčič — cf. 1872-Jakofčič-h6/38-niti!)",
    28: "★★★ h1-GOSPODAR-'Jessernigg'-65J (Katharina-Jessernigg-vzorec — cf. P84-krstne-h1!) + Wassersucht",
    29: "★ h22-nit + ime-'Milik[?]' (MILIČ-grafia-kontekst — cf. 1871-z29-Milič-h66!)",
    36: "★ h48-nit-Klobučar-18J (cf. krstne-h48-1890-P85!) + mesec-DUEL-Mai/Juni-31.",
    39: "★ h40-Pezić-nit + ime-DUEL-Pezić/Pezdire (PEZDIR-grafia-kontekst!)",
    42: "★ MRTVOROJEN-'Stillgeborenes'-Knavs-h52 (July —/23!)",
    49: "★ h68-Urih-nit-78J (cf. 1871-z20-Arik[~Urih]-h33!)",
    51: "★★★ POŽEK-h28-NIT-2.-LETO (Johann-1-mes-Sept-1870 → 1871-z50-Georg-5¾J-Sept — h28-NEPREKINJENO!)",
    54: "★ h20-nit + 'Poždire[?]' (Pegdirec/Poždirec-grafia-kontekst!)",
    60: "★ ime-DUEL ('Janos-Millié[?]' vs 'Janez-Milič') + h32-nit + 1-J",
    63: "★ ime-DUEL ('Peter-Afrik[?]' vs 'Adriih[?]') + 76-J-Altersabzehrung + h51-nit",
    66: "★ h46-nit-Molinar-2J (Dec-1870-tail — cf. 1871-z1-'von-Griblnac'-poreklo!)",
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
    houseNo: "{str(e.get('hisna', '?')).split()[0]}",
    bookSignature: "04106",
    year: 1870,
    scan: {e['sken']},
    page: {e['pag']},
    whatSi: "{what_si.replace('"', "'")}",
    whatEn: "died {ime}, {starost} ({mes_dejansko} {smrt}, buried {pokop}) — {bolezen}; + [see-SI] + [z{z}]",
    status: "DOCUMENTED",
  }},
"""

header = """  // ——— P207: mrliška PREDZGODOVINA 04106, leto 1870 = 16. leto PREDZGODOVINSKE LINIJE (s81–s86 == Pag. 76–81, z1–z70 = 70 vpisov — ŠTEVJE-IZ-VRSTIC-9.× (ordinali-1–70 ČISTO-BREZ-luknje/dupa — edinstveno-v-04106-predzgodovini!; ord-stolpci-×3.5-recept-P206: s83-'25–37'-(celostanska-zamik-−2!-36/37-TUKAJ!)-+ s84-'38–50'; vrstna-aritmetika 11+13+13+13+13+7; meseci J3+F6+M9+A11-MAX+M6+J4+J2+A5+S7+O6+N4+D5; pag = sken−5, md5-križna-ta-seja: s84+s85+s86-sveži == P206-disk-1:1 — veriga-P197→…→P207-11.×!) — 12 GRIBLJE-blokov / 12 hiš-vsi-različni + ★★★ MEJA-1869/70-s80→s81 (s80-KONEC-LETOVNIKA-1869-'VALOVITA-ČRTA'-KROP! + '1869'-VLM-misread-'1849'! → s81-VELIKA-LETVICA-'1870'-×2-KROP + restart-1! s78/s79/s80-1869-kontekst-zap-38–76!) + ★★★ MEJA-1870/71-s86 (tail-×7 + 'vsota'-'1|8'-P206-soglasje-1:1!) + ★★★ h1-GOSPODAR-Jessernigg-z28! + ★★★ POŽEK-h28-NIT-2.-leto (z51-Johann-1-mes → 1871-z50-Georg!) + MRTVOROJEN-z42 + ime-DUELI-×3 (z39-Pezić/Pezdire + z60-Millié/Milič + z63-Afrik/Adriih!) ———
"""

blocks = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, header + blocks + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
print(f"OK — 1870-bloki: {len(grib)}")
