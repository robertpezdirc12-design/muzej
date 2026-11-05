#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P212 — vstavi 13-GRIBLJE-blokov (04106, leto 1865) v parish.ts PRED P211-sekcijo. IDEMPOTENTEN."""
import json, re
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P211: mrliška PREDZGODOVINA 04106, leto 1866"

E = json.load(open("/tmp/p212/entries_1865.json"))
grib = E["griblje_entries"]
assert len(grib) == 13, f"grib={len(grib)}"

# idempotenca: odstrani prejšnje P212-bloke (če obstajajo)
P212_HDR = "  // ——— P212: mrliška PREDZGODOVINA 04106, leto 1865"
if P212_HDR in src:
    i = src.index(P212_HDR)
    j = src.index(ANCHOR, i)
    src = src[:i] + src[j:]
    print("odstranjene-prejšnje-P212-bloke (idempotenca)")

KOM = {
    1: "★★★ PRVI-VPIS-1865-restart! KRIŽAN-h3-nit (Maria-81-J-Marasmus-senilis — cf. 1867-h3-Papic-×3!) + 2×-MARIA-KRIŽAN-v-1-tednu (z88-tail-Otok-h20-48-J-12.Dez!) + stan-DUEL-3×-branja-HONEST (Abrabannin/Albrechtin/Ablabamin!)",
    8: "★ URIH-grafia (KROP-'Urih,-ne-Urik'!) + stan-DUEL (VLM-'Inoaskanica'-vs-KROP-'G—l—'≈Güblerin) + hisna-68-VLM (krop-pending)",
    9: "★ starost-DUEL-HONEST (KROP-'60'-vs-VLM-'56'!) + BRINC-nit-#1 (cf. z20-h28-Jernej!)",
    11: "★★★ KROP-4-KOREKCIJE-1-VRSTICO (h50-NI-80 'Kurrent-5-s-čopom'! + Redovi-NI-Podgoršek-VLM-halucinacija-FALSIFICIRANA! + ½-Gübler-Kind + Wassersucht-NI-Mrzlica!)",
    13: "★★★ ANOMALIJA-PISAR-MOTA-dokumentirana (pokop-17.-vpisan-PRED-smrt-18.-KROP-POTRJENO-v-zapisu!) + HUSIČ-h37-klaster-#1 (mati-27-J-Schwindsucht — umrla-18.2) + '½-Güblerswirt'",
    17: "★ h18-nit (Marija-Muc-43-J-Lungenentzündung — krop-pending)",
    18: "★★★ HUSIČ-h37-klaster-#2 (otrok-Anna-2-mes — umrla-11.3 — 3-tedni-po-materi! '-Kind'-suffix-potrjuje-isto-hišo!)",
    20: "★★★ BRINC-nit-#2 (Jernej-28-J-h28 — 2-BRINC-v-2-hišah-v-1-mesecu! cf. z9-h23!)",
    24: "★ TYPHUS-rdka (Nicolaus-Ulrich-46-J — cf. 1867-Krčavica-epidemija-Papic-klaster!)",
    36: "★★★ POŽEK-nit-#2 (Mathias-36-J-h67-Abzehrung — cf. P211-z90-h58-Totgeborenes-v.-Mark.-Požek + P192-h58! h67-NOVA-hiša-nit!)",
    50: "★ h32-nit (Michael-Straus-6-dni-Krämpfe — cf. 1866-h34-FILAK-×2-sosednje?)",
    63: "★ h19-nit-GRIBLJE (Anna-Križe-2-J-Abzehrung — RAZLIČNA-vas-od-P211-z34/35-h19-Vranoviče-Žunič!)",
    66: "★★★ TAIL-1865-ZADNJI-GRIBLJE-VPIS + PEZDIRC-h14-KONTINUITETA (Maria-66-J → z41-1866-Mathias-unehelich-Kind-h14! VLM-h11-duel-rešen-KROP-h14!) + stan-DUEL ('Abfaknin/Ablokumin-?-dekla')",
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
    mes_dejansko = {"Februar": "Feber", "Januar": "Jänner", "December": "Dezember", "Junij": "Juni",
                    "Martii": "März", "Maii": "Mai", "Julii": "July"}.get(mesec.split()[0] if mesec else "", mesec.split()[0] if mesec else "")
    what_si = f"umrl(a) {ime}"
    if stan: what_si += f", '{stan}'"
    what_si += f", {starost} ({mes_dejansko} {smrt}, pokop {pokop}) — {bolezen}"
    if kom: what_si += f"; + {kom}"
    if e.get("krop_opomba"): what_si += f"; [KROP: {e['krop_opomba'][:180]}]"
    what_si += f" + [z{z}]"
    hn = str(e.get('hisna', '?')).split()[0]
    return f"""  {{
    houseNo: "{hn}",
    bookSignature: "04106",
    year: 1865,
    scan: {e['sken']},
    page: {e['pag']},
    whatSi: "{what_si.replace('"', "'")}",
    whatEn: "died {ime}, {starost} ({mes_dejansko} {smrt}, buried {pokop}) — {bolezen}; + [see-SI] + [z{z}]",
    status: "DOCUMENTED",
  }},
"""

header = """  // ——— P212: mrliška PREDZGODOVINA 04106, leto 1865 = 21. leto PREDZGODOVINSKE LINIJE (s046–s051 == Pag. 41–46, z1–z66 = 66 vpisov — ŠTEVJE-IZ-VRSTIC-14.× (ordinali-1–66-ČISTO — 6.-LETO-ZAPORED-BREZ-luknje/dupa!; vrstna-aritmetika 7+14+14+14+15+2; meseci J8+F6+M7+A10+M6+J2+J6+A4+S3+O4+N7+D3; pag = sken−5; 2×-neodvisna-prenosa-9/9 + križ-s50-vs-P211-disk-1:1!) — 13-GRIBLJE-blokov / 12 hiš (h37-×2-HUSIČ-klaster!) + ★★★ MEJA-1864/65-s46 (tail-1864-z88–z91-NATAČNO-4-vrstice-KROP! + z91-ULEDBA-#11-30.Dez-1864→1.Jänner-1865-pokop + dvojna-črta + restart-'1865'-VELIKA-LETVICA-KROP-50.-POTRDITEV-invariante!) + ★★★ z74-duel-REŠEN (s45=74–87: '4-ima-zanko-1-je-ozka-črtica'-KROP-cifra-analiza → 1864-kontekst-60–91-ZVEZNA!) + ★★★ z13-ANOMALIJA-PISAR-MOTA (pokop-17-PRED-smrt-18.-KROP-POTRJENO!) + ★★★ HUSIČ-h37-KLASTER (mati-27-J-umrla-18.2 + otrok-2-mes-umrla-11.3 — ½-Güblerswirt + -Kind!) + ★★★ 2×-MARIA-KRIŽAN-v-1-tednu (z88-Otok-48J + z1-Griblje-81J-h3!) + ★★★ BRINC-×2-2-hiši (z9-Anna-h23 + z20-Jernej-h28!) + ★★★ POŽEK-h67-nit + ★★★ PEZDIRC-h14-kontinuiteta-tail (z66-Maria-66J → z41-1866-Mathias!) + otroška-umrljivost-31%-4/13 (NIŽJA-kot-1866-77%!) ———
"""

blocks = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, header + blocks + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
print(f"OK — 1865-bloki: {len(grib)} (vsi-year-1865; h-hiš={len(set(str(e.get('hisna','?')).split()[0] for e in grib))})")
