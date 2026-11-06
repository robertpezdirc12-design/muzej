#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P210 — vstavi 20-GRIBLJE-blokov (04106, leto 1867) v parish.ts PRED P209-sekcijo."""
import json
from pathlib import Path

TS = Path("/home/z/my-project/muzej-backup/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")
ANCHOR = "  // ——— P209: mrliška PREDZGODOVINA 04106, leto 1868"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1867," not in src, "1867-bloki-že-obstajajo?!"

E = json.load(open("/tmp/p210/entries_1867.json"))
grib = E["griblje_entries"]

KOM = {
    3: "★ h60-nit + starost-DUEL ('6'-vs-'65[?]-let'!) + ime-DUEL-Selho[~Zelho]",
    8: "★ h2-KLEPEC-nit (Anna-87J[~37?]-Asthma — cf. 1871-z62-Anna-Klepec-h2-54J!) + starost-DUEL",
    11: "★ h10-nit (Ana-Perdih-1-J-Pljučnica — cf. 1868-z74-Rom-h10!)",
    15: "★ h44-nit (Barbara-Perneus[~Perne?-Strnčec?]-68-J — ime-TRI-DUELI!-cf. 1867-z45-h44-Strucež!)",
    21: "★ h40-nit (Katarina-Perdih-2-leti — PEZDIR-kontekst!-cf. 1870-z39-h40-Pezić!)",
    26: "★ h74[~71?]-hišna-DUEL (Marko-Brinz[~Brinc]-56-J — BRINEC-grafia!)",
    35: "★ h48-nit (Janez-Vlokušar[~Vukovičar?Wlokučar]-64-J — ime-DUEL!-cf. krstne-h48-1890!)",
    44: "★ h13-JAKOFČIČ-nit (Matthias-66-J-Mai — cf. 1868-z66/z80-h13-×2!)",
    45: "★ h44-×2-#2 (Matija-Strucež-1½-J-Frisen — z15-Perneus-v-isti-hiši!)",
    46: "★ h56-nit (Anna-Šimic-57-J — ŠIMEC-grafia!)",
    47: "★ h38-nit (Josef-Stojmič-9-mes — cf. 1871-z20-h33-Arik-kontekst!)",
    62: "★★★ PEZDINC-GRAFIA-#12 (Maria-Pezdinc-6-mes-h46-Frisen — cf. P200-PEZDINC-×3-1877 + 1869-z61-Pezdir!)",
    78: "★ h68-Urih-nit (Maria-54-J-Nadruha[?]-cf. 1870-z49-h68-Urih-78J!)",
    86: "★ h18-nit (Nicolaus-Simič[~Jimič]-25-J-Ruša[?] — ŠIMEC-grafia!)",
    88: "★ h35-nit (Martin-Hojnic-14-J-Griželzi-Schwindsucht!)",
    93: "★★★ h7-×3-TRIPLE-#1 (Andrej-Potar-1-Monat-Frisen!)",
    95: "★★★ h7-×3-TRIPLE-#2 (Anton-Papic-11-W[?]-Krčavica!)",
    96: "★★★ h7-×3-TRIPLE-#3 (Barbara-Papic-2-Tage-Krčavica — Papic-×2-v-3-dneh!)",
    98: "★ h3-nit (Joannes-Papic-10-Tage-Krčavica — PAPIC-×3-v-9-dneh!-KRČAVICA-epidemija-klaster!)",
    101: "★ h51-nit (Marko-Urih-1½-J — cf. 1870-z63-h51-Afrik!)",
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
    mes_dejansko = {"Februar": "Feber", "Januar": "Jänner", "December": "Dezember", "Junij": "Juni", "Decemb": "Dezember"}.get(mesec.split()[0] if mesec else "", mesec.split()[0] if mesec else "")
    what_si = f"umrl(a) {ime}"
    if stan: what_si += f", '{stan}'"
    what_si += f", {starost} ({mes_dejansko} {smrt}, pokop {pokop}) — {bolezen}"
    if kom: what_si += f"; + {kom}"
    what_si += f" + [z{z}]"
    hn = str(e.get('hisna', '?')).split()[0]
    return f"""  {{
    houseNo: "{hn}",
    bookSignature: "04106",
    year: 1867,
    scan: {e['sken']},
    page: {e['pag']},
    whatSi: "{what_si.replace('"', "'")}",
    whatEn: "died {ime}, {starost} ({mes_dejansko} {smrt}, buried {pokop}) — {bolezen}; + [see-SI] + [z{z}]",
    status: "DOCUMENTED",
  }},
"""

header = """  // ——— P210: mrliška PREDZGODOVINA 04106, leto 1867 = 19. leto PREDZGODOVINSKE LINIJE (s61–s69 == Pag. 56–64, z1–z103 = 103 vpisov — ŠTEVJE-IZ-VRSTIC-12.× (ordinali-1–103-ČISTO — 4.-LETO-ZAPORED-BREZ-luknje/dupa!; ord-stolpec-s61-'1–10'-×3.5 + kontinuiteta-zap-35→36-s63→s64!; vrstna-aritmetika 10+12+13+13+13+13+13+15+1; meseci J18-MAX+F10+M4+A3-MIN+M9+J7+J9+A9+S9+O3+N12+D9(+1-Decemb); pag = sken−5, md5-križna-ta-seja: s64+s65+s66+s67+s68-sveži == P209-disk-1:1 — veriga-P197→…→P210-14.×!) — 20-GRIBLJE-blokov-REKORD-PREDZGODOVINE (2.-največ-po-koleri-38!)-/ 17 hiš (h7-×3-TRIPLE!-h44-×2!) + ★★★ MEJA-1866/67-s61 (restart-'Jänner'-'1867'-VELIKA-LETVICA-KROP-48.-POTRDITEV-invariante — VLM-'1864'-halucinacija-FALSIFICIRANA! s57–s60-1866-kontekst-zap-59–104!) + ★★★ h7-×3-TRIPLE-klaster (z93-Potar + z95/z96-Papic-×2-v-3-dneh — PAPIC-×3-v-9-dneh-z98-h3!-KRČAVICA-epidemija!) + PEZDINC-grafia-#12 (z62-h46!) + JAKOFČIČ-nit-z44 + KLEPEC-nit-z8 + starost-DUELI-×2 (z3-'6-vs-65' + z8-'87-vs-37'!) ———
"""

blocks = "".join(gen_block(e) for e in grib)
src = src.replace(ANCHOR, header + blocks + ANCHOR, 1)
TS.write_text(src, encoding="utf-8")
print(f"OK — 1867-bloki: {len(grib)}")
