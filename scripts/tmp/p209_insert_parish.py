#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P209 — vstavi 13-GRIBLJE-blokov (04106, leto 1868) v parish.ts PRED P208-sekcijo."""
import json
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P208: mrliška PREDZGODOVINA 04106, leto 1869"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1868," not in src, "1868-bloki-že-obstajajo?!"

E = json.load(open("/tmp/p209/entries_1868.json"))
grib = E["griblje_entries"]

KOM = {
    32: "★ h54-×2-#1 (Georg-Timic-48J-Asthma — cf. krstne-h54-1887-P82!)",
    35: "★ h54-×2-#2 (Georg-Lopare-68J-Altersschwäche — 2-smrti-isti-hiši-1868!)",
    36: "★ h50-PERDIRC-nit (otrok-5½J[?]-Frisen — PEZDIR-grafia! cf. 1867-kontekst-PEZDINC-z66!)",
    47: "★ h36-'½-Weibl'-pripis-v-imeni (Martha-Kuzan-16J-Gehirnentzündung!)",
    52: "★ h65-Mililc[?~Milh]-6-Mon (MILIČ-grafia-kontekst!)",
    55: "★ h66[?60]-hišna-DUEL (Maria-Zelko-68J!)",
    56: "★ h26-Brinc[?~Brune]-3½-J-Dürrfall (BRINEC-grafia! mesec-dualni-Aug/Sep-31→1-ULEDBA-vzorec!)",
    61: "★★★ h15-'nožgodanujeleg'-ANOMALIJA (ime-neberljivo + starost-'—' + bolezen-'[—]' — edina-popolnoma-NEBERLJIVA-vrsta-1868!)",
    66: "★ h13-JAKOFČIČ-nit (Anna-63J-Oct → cf. 1869-z17-Georg-62J + 1871-z17!)",
    74: "★ h10-Rom-1½-J (Dec-4./5-Frisen)",
    77: "★ h41-HROVAT-nit (Marko-46J-Dec-13./15 — P208-tail-soglasje-1:1!)",
    78: "★ h35-Hrovćan[?Hrovžan]-57J-Dec-13./15 (ISTI-DATUMI-kot-z77 — 2-smrti-v-ISTEM-dnevu!)",
    80: "★ h13-JAKOFČIČ-×2 (Agnes-19J-Dec-26./28-Posledice[~Brandfleck?] — z66-Anna-v-isti-hiši!)",
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
    year: 1868,
    scan: {e['sken']},
    page: {e['pag']},
    whatSi: "{what_si.replace('"', "'")}",
    whatEn: "died {ime}, {starost} ({mes_dejansko} {smrt}, buried {pokop}) — {bolezen}; + [see-SI] + [z{z}]",
    status: "DOCUMENTED",
  }},
"""

header = """  // ——— P209: mrliška PREDZGODOVINA 04106, leto 1868 = 18. leto PREDZGODOVINSKE LINIJE (s69–s75 == Pag. 64–70, z1–z80 = 80 vpisov — ŠTEVJE-IZ-VRSTIC-11.× (ordinali-1–80-ČISTO — 3.-LETO-ZAPORED-BREZ-luknje/dupa!; ord-stolpci-×3.5: s69-'1–10' + s75-'77–80'-(P208-soglasje!); vrstna-aritmetika 10+13+13+13+14+13+4; meseci J13-MAX+F6+M4+A10+M5+J2+J5+A10(+1-dualni)+S4+O7+N4(+1-dualni)+D8; pag = sken−5, md5-križna-ta-seja: s71+s72+s73+s74-sveži == P208-disk-1:1 — veriga-P197→…→P209-13.×!) — 13 GRIBLJE-blokov / 11 hiš (h54-×2!-h13-×2!) + ★★★ MEJA-1867/68-s69 (1867-tail-×1-zap-103-Primostek-15-Lutblan-80J-ULEDBA-31.Dez→1.Jän + 'vsota'-4-DELNA-'1|8|6|8'-NOVA-FORMA-1.×! + restart-'1.-Jänner-1868'! s64–s68-1867-kontekst-zap-36–102!) + ★★★ h15-'nožgodanujeleg'-ANOMALIJA-z61 (edina-popolnoma-NEBERLJIVA!) + h35/h41-'2-smrti-v-ISTEM-dnevu' (z77/z78-Dec-13./15!) + ULEDBA-vzorec-×2 (z56-Aug/Sep + tail-103!) ———
"""

blocks = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, header + blocks + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
print(f"OK — 1868-bloki: {len(grib)}")
