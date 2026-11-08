#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P204 — vstavi 38-GRIBLJE-blokov (04106, leto 1873 — KOLERA!) v parish.ts
PRED P203-sekcijo (newest-first vzorec). 212 vpisov / 38 Griblje / 30 hiš (REKORD!)."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")

ANCHOR = "  // ——— P203: mrliška PREDZGODOVINA 04106, leto 1874"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1873," not in src, "1873-bloki-že-obstajajo?!"

E = json.load(open("/tmp/p204/entries_1873.json"))
entries = E["entries"]
grib = E["griblje_entries"]

# per-z-komentarji (iz-merge-MANUAL + dokaz!)
KOM = {
    2: "★★★ 1.-GRIBLJE-1873 + '1873.'-GLAVA-V-Z1-CELICI (41.-POTRDITEV-invariante!) + 'Incipit annus Domini'-ročno-glava + restart-1–12! + vijol.-dopisek-'Zgajnar'-poznejša-tinta! + h55-NOVA-hiša-korpusa",
    3: "★ 2.-Griblje-Jän + h30-nit (cf. P199-h30-×2-1878 + P202-'Krič-None→h19'!)",
    5: "★ 3.-Griblje-Jän (17½-J-KROP! VLM-'44'?) + FRISEN-bolezen",
    6: "★ otrok-3½-TEDNOV + Gurkenkrämpfe[~Hirnhauten?] — JÄN-KLUSTER-×6-Griblje-s102!",
    8: "★★★ h65-×2-KLASTER-#1 + DVOJNI-ime-v-vrstici ('Jurbya-baumann + Mathias-Milthin-Mary.')!",
    9: "★★★ h65-×2-#2 (Margaretha-Küllik-½-Gäblerin-32½J-Kindbettfieber!) — h65-1:1-KROP-×2!",
    19: "★ ime-DUEL (Frupar-vs-Krekar-KROP) + s103==s104-DOUBLE-SCAN-3.×-korpus (pag-98-×2!)",
    30: "★★★ KROP-KOREKCIJA-ime-#1 ('Mariund-Jakočič'→'Marcus-Jakofčič'!) + otrok-10-DNI + h13-×2-KLASTER",
    31: "★ h13-×2-#2 + ime-DUEL (Halak-vs-Cilik) + starost-DUEL (28J-vs-1J) + 'Im-Kindbett-verblutet'!",
    37: "★ ime-DUEL (Jakl-vs-Krik) + starost-4-(ne-40!) + h51-nit",
    40: "★ Anton-Brodarić-h49-74-TAGEN-Schwindsucht + s106-'1873. Jüni'-GLAVA-V-Z37-CELICI-DUPKAT-ordinal!",
    45: "★ ime-DUEL (Mikl-vs-Mihik) + starost-DUEL (4J-vs-1J) + h57-NOVA-hiša-korpusa (→ P200-h57-NIT-1877!)",
    49: "★ Johan-Hrižan-h8[~3?]-14-TAGEN-Ohnmacht + HRIZAN-grafia-nit (→ z80!) + h8-nit (cf. P200-z39-Jakofčič-1877!)",
    55: "★★★ PEZDIRC-NIT-1873-#1 (Georg-h41-36J-Magenkrampf! cf. P199-×3-1878 + P202-'Peglinc-Bezdira'-h59!)",
    56: "★ Maria-Pohler-h5-29J-Schlagfluß + h5-nit (→ P202-h5-1875!)",
    61: "★ Kath.-Marvina[?]-h10-32J + h10-nit (cf. P199-z9-Kure-h10 + P197-h10-×2!)",
    63: "★★★ PEZDIRC-NIT-1873-#2 (Katharina-h40-1J! → P199-h40-×2!) + otrok",
    76: "★★★ Griblje-DVOJNOST ('Krasinec-mimo-Griblje'-h58-Marcus-Dozeth-apl.-Ružar-MOŠKI-KROP!) + VLM-'Mariana-Pojkl'-FALSIFICIRANA + Cholera!",
    79: "★ ime/starost-DUEL (Golobič-2½J-vs-Jakopič-47J-Typhus!) + h43-nit (→ z169-h43!)",
    80: "★ Maria-Hrižan-h63-starost-DUEL (45J-vs-18J) + HRIZAN-grafia-nit-#2 + Cholera",
    87: "★ ime-DUEL (Ložež-vs-Zajec) + h28-×2-KLASTER + Cholera",
    88: "★ h28-×2-#2 (Maria-Ložež-2J-otrok! bratje/otroci-×2-v-3-dneh!) + Cholera",
    105: "★ Maria-Husic-h37-37J-Cholera (KROP-potrjen!) + h37-nit (cf. P196-h37-×2!)",
    112: "★★★ KROP-KOREKCIJA-starost-#2 ('55J'→'5¾-J'!) + otrok-KOLERA + h33-nit",
    115: "★ ime-KOREKCIJA (Brune→BRIME!) + starost-DUEL (5J-vs-51J) + h24-BRIME-NIT (→ P203-z6-h24-9J-1874!)",
    116: "★ Peter-Brumi-h24-39J-Cholera (Sept-tail-s111→s112-prelom!) + h24-×2-1873/74!",
    134: "★ Maria-Milek-h22-33J-Cholera (Sept-26/27)",
    137: "★ Mathias-Hubler-[~Kubler?]-h30-¼-J-otrok-Cholera + h30-×2-1873!",
    140: "★ Marcus-Hure/Kure-h10-otrok-[1-?J] + mesec-DUEL (Okt-vs-Nov) + h10-×2-1873!",
    168: "★ Mathias-Husič-h60[~69?]-Cholera + hisna-DUEL-Kurent-9-0",
    169: "★ Nicolaus-Brotja-h43-62J-Cholera (KROP-'Studir'?) + h43-×2-1873!",
    171: "★ Katharina-Toller-h7-1J-otrok-Cholera + h7-NOVA-hiša-korpusa",
    172: "★ Dorothea-Brinc-h34[~74?]-60J-Cholera + BRINC-nit (cf. P203-h69-Brinc-½J!) + hisna-DUEL",
    177: "★★★ LUNIČ-h11-NIT-3.-LETO (→ P203-h11-16dni-1874 → P202-h11-KUNIĆ-1875!) + hisna-KOREKCIJA-h11! + Cholera",
    193: "★ Mathias-Kumerič-h94[~74?]-otrok-3mes-3ted-Krči + h94-NOVA-hiša-korpusa (max!)",
    208: "★★★ P203-TAIL-1:1 (z5-tail!) + KROP-vizualno-'Brime' + h23 + Altersschwäche — 1.-od-9-DEZ-TAIL-1873!",
    210: "★★★ P203-TAIL-1:1 (z7!) + Johann-Hlebec-h2-64J-Asthma — h2-nit (cf. P200-'Hrible'-Tomc-klaster!)",
    211: "★★★ P203-TAIL-1:1 (z8!) + Maria-Brume-h16-52J-Kindbettfieber + ULEDBA-31-Dez→1-Jän! + 'December 1873'-GLAVA-V-Z204-CELICI (43.-POTRDITEV!)",
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
    duh = (e.get("duhovnik") or "").strip()
    kom = KOM.get(z, "")
    verb = "umrla" if any(w in ime.lower() for w in ("maria", "anna", "kath", "barbara", "marg", "dorot", "antonka", "theresia")) else "umrl"
    # mesec-normalizacija za-okvir
    mm = {"Februar": "Feber", "Januar": "Jänner", "December": "Dezember", "Junij": "Juni", "Jüli": "July"}.get(mesec.split()[0] if mesec else "", mesec.split()[0] if mesec else "")
    mes_dejansko = mm if mm else (e.get("ord_opomba", "")[:0])
    what_si = f"{verb} {ime}"
    if stan: what_si += f", '{stan}'"
    what_si += f", {starost} ({mes_dejansko} {smrt}, pokop {pokop}) — {bolezen}"
    if duh: what_si += f"; duhovnik-[{duh}]"
    if kom: what_si += f"; + {kom}"
    what_si += f" + [z{z}]"
    what_en = f"{ 'died' if verb == 'umrla' else 'died' } {ime}"
    if stan: what_en += f", '{stan}'"
    what_en += f", {starost} ({mm} {smrt}, buried {pokop}) — {bolezen}"
    if duh: what_en += f"; priest-[{duh}]"
    if kom: what_en += f"; + [see-SI]"
    what_en += f" + [z{z}]"
    return f"""  {{
    houseNo: "{e.get('hisna', '?')}",
    bookSignature: "04106",
    year: 1873,
    scan: {e['sken']},
    page: {e['pag']},
    whatSi: "{what_si.replace('"', "'")}",
    whatEn: "{what_en.replace('"', "'")}",
    status: "DOCUMENTED",
  }},
"""

header = """  // ——— P204: mrliška PREDZGODOVINA 04106, leto 1873 = 13. leto PREDZGODOVINSKE LINIJE — ★★★ KOLERA-LETO (cholera epidermica)! (s102–s118 + s119-tail-9 == Pag. 97–114, z1–z212 = 212 vpisov — NAJVEČJE-leto-korpusa (2.3×-P203!) — ŠTEVJE-IZ-VRSTIC-6.× (ordinali-VIDNI-ampak-Kurent-zmedani: pisarski-DUPKATI-×4 (24/37/61/153-ob-mejah!) + LUKNJE-×5 (67 + 141–144!) → neto-−1!); vrstna-aritmetika 12+12+14+12+13+13+13+13+12+12+13+13+12+12+13+14+9; meseci J8+F9+M7+A13+M1+J6+J8+A73-MAX-KOLERA+S41+O13+N12+D9; pag = sken−5 (LEKCIJA-#21!), md5-križna-ta-seja: s118+s119-sveža == P203-disk-1:1 + s110/s111-2. krog — veriga-P197→…→P204-8.×!) — 38 GRIBLJE-blokov / 30 hiš (REKORD!) ———
"""

blocks = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, header + blocks + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
print(f"OK — 1873-bloki vstavljeni: {len(grib)}")
print("year-1873-blokov:", src.count("year: 1873,"))
