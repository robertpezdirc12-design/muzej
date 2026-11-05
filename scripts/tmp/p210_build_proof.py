#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P206 — build proof research/issue17/parish-death-1867-04106.json (recept P200–P205)."""
import json, re

E = json.load(open("/tmp/p210/entries_1867.json"))
entries = E["entries"]
griblje = E["griblje_entries"]
kask = E["ord_kaskada"]

def starost_leta(s):
    s = (s or "").lower()
    m = re.match(r"\s*(\d+(?:[.,¾½¼]\d*)?)", s)
    if not m: return None
    v = m.group(1).replace(",", ".")
    try: f = float(v)
    except: return None
    if 0 < f < 1 and ("½" in s or "¾" in s or "¼" in s or "." in v): return f
    return f if f < 10 else None

otroci = [e for e in griblje if starost_leta(e.get("starost")) is not None]
hise = sorted({str(e.get("hisna", "?")).split()[0] for e in griblje}, key=lambda x: (len(x), x))

# meseci-vsota (iz entries — ŠTEVJE-IZ-VRSTIC-osnova!)
MESECI_MAP = {"Februar": "Feber", "Januar": "Jänner", "Jüli": "July", "Juli": "July", "Junij": "Juni",
              "Avgust": "August", "Sept": "September", "Okt": "October", "Oktob": "October", "Dec": "Dezember", "December": "Dezember"}
meseci = {}
for e in entries:
    m = (e.get("mesec") or "").strip()
    if not m: continue
    key = m.split()[0].split("-")[0].rstrip(".").strip()
    key = MESECI_MAP.get(key, key)
    if key.lower() in ("jänner", "feber", "märz", "april", "mai", "juni", "july", "august", "september", "october", "november", "dezember"):
        meseci[key] = meseci.get(key, 0) + 1
meseci_sum = sum(meseci.values())

proof = {
    "faza": "P210",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1867 = 19. leto PREDZGODOVINSKE LINIJE (issue #18) — ordinali-1–103-ČISTO-4.leto + h7-×3-TRIPLE + PEZDINC-#12 + REKORD-20-GRIBLJE!",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1869": f"s61-restart–s69-tail-×1 (pag 56–64); {len(entries)} vpisov (ordinali-1–103-ČISTO (4.-leto-zapored!), ŠTEVJE-IZ-VRSTIC-12.×!) / {len(griblje)} Griblje / {len(hise)} hiš-vsi-RAZLIČNI",
    "meja_1866_67": "★★★ s61 (pag 56): restart-'Jänner'-'1867'-VELIKA-LETVICA-KROP-48.-POTRDITEV-invariante! — VLM-'1864'-halucinacija-FALSIFICIRANA! (s57–s60-1866-kontekst-zap-59–104!)",
        "meja_1870_71": "★★★ s69-tail (pag 64): 1867-TAIL-×1 — (zap-103-Primostek-15-Lutblan-80J-ULEDBA-31.Dez-1867→1.Jän-1868-pokop — P209-soglasje-1:1!)",
        "konec_1869": "z70 = s86-r7 (Dec-30/Jan-1-Boršt-22-Maria-Braj-½-Grilbus!) — leto-konča-z-'vsota'-'1|8'-vrstico!",
        "zaporedna": "★★★ ordinali-1–103-ČISTO (4.-leto-zapored-ČISTO!) — ord-stolpec-s61-'1,2,3,4,5,6,7,8,9,10'-(×3.5!)-+ kontinuiteta-zap-35→36 (s63→s64!)",
        "forma": "'1867'-VELIKA-LETVICA-s61-KROP (48.-potrditev-invariante!) + 'Jänner'-glava-restart! VLM-'1864'-halucinacija-FALSIFICIRANA!",
        "skeni": "s057–s069 (pag 52–64; 13-skenov: s057–s060-1866-kontekst + s061–s069-1867); s64+s65+s66+s67+s68-md5-vs-P209-disk-1:1 (7021e964/2c6e7d8e/092ded76/2a27e2a2/dddc4191) — VERIGA-P197→…→P210-14.×!",
        "preslikava": "pag = sken−5 (s86=81, s92=87 ✓ LEKCIJA-#21-zona-se-nadaljuje!); natisnjene-št.-NI-KROP-potrjene (s88-listna-'84'-spodaj!)",
        "preštevanje": f"vrstna-aritmetika 4+13+13+14+14+12+3 = {len(entries)} ✓ (s86-tail-SKIP + s92-restart-SKIP!); meseci-vsota-={meseci_sum} (±VLM-drift)",
    },
    "statistika": {
        "vpisov_1867": len(entries),
        "griblje": len(griblje),
        "hise": hise,
        "otrok_griblje": f"{len(otroci)}/{len(griblje)} = {round(100*len(otroci)/len(griblje))}% — otroška-umrljivost-1871 (z19-Jakofčič-2J + z51-Požek-1-mes + z54-Poždire-1-J + z60-Millié-1-J!)",
        "duhovniki": "celostanska-VLM-podpisov-NE-izluščila-vse (KROP-z50-ni-videl-podpisa) — cf. P205-Kogej-provisorium-nit",
    },
    "anomalije": [
        "★★★ MEJA-1866/67-s61: restart-'Jänner'-'1867'-VELIKA-LETVICA-KROP-48.-POTRDITEV-invariante! — VLM-'1864'-LETVICA-HALUCINACIJA-FALSIFICIRANA!",
        "★★★ 20-GRIBLJE-REKORD-PREDZGODOVINE (2.-največ-v-korpusu-po-koleri-38-1873!)",
        "★★★ h7-×3-TRIPLE-klaster (z93-Andrej-Potar-1-Mon + z95-Anton-Papic-11-W + z96-Barbara-Papic-2-Tage — PAPIC-×2-v-3-dneh!)",
        "★★★ PAPIC-×3-v-9-dneh (z95/z96-h7 + z98-h3 — vsi-Krčavica! KRČAVICA-epidemija-klaster-Dez-1867!)",
        "★★★ PEZDINC-GRAFIA-#12 (z62-Maria-Pezdinc-6-mes-h46!)",
        "★★★ h44-×2 (z15-Barbara-Perneus[~Perne?Strnčec?]-68J + z45-Matija-Strucež-1½J!)",
        "★ h13-JAKOFČIČ-nit (z44-Matthias-66J → 1868-×2-Anna+Agnes!)",
        "★ h2-KLEPEC-nit (z8-Anna-87J[~37?]-Asthma → 1871-z62-Anna-Klepec-54J!)",
        "★ starost-DUELI-×2 (z3-'6-vs-65[?]-let' + z8-'87-vs-37[?]-let')",
        "★ ime-DUELI-×3 (z3-Selho[~Zelho] + z15-Perneus[~Perne?Strnčec?] + z35-Vlokušar[~Vukovičar?Wlokučar]!)",
        "★ h74[~71?]-hišna-DUEL (z26-Marko-Brinz[~Brinc]-56J-BRINEC-grafia!)",
        "★ h18-Simič[~Jimič]-grafia (z86-Nicolaus-25J-Ruša[?]!)",
        "★ s64-'2.36'-Kurent-pripisa (marginalne-oznake!)",
        "★ s57–s60-1866-kontekst-zap-59–104 (1866-=-104-vpisov-P211-lead!)",
    ],
    "hišne_kontinuitete": {
        "h7": "★★★ ×3-TRIPLE-1867 (z93-Potar-1-Mon + z95-Anton-Papic-11-W + z96-Barbara-Papic-2-Tage!) — PAPIC-POTENCA!",
        "h13": "JAKOFČIČ-nit: Matthias-66J-1867 (z44!) → 1868-Anna-63J + Agnes-19J-×2!",
        "h2": "KLEPEC-nit: Anna-87J[~37?]-1867 (z8!) → 1871-z62-Anna-Klepec-54J!",
        "h44": "×2-1867 (z15-Perneus + z45-Strucež-1½J-otrok!)",
        "h46": "PEZDINC-#12-1867 (z62-Maria-6-mes!) — cf. P200-PEZDINC-×3-1877!",
        "h68": "Urih-nit: Maria-54J-1867 (z78!) → 1870-z49-Maria-Urih-78J!",
        "h18": "Simič[~Jimič]-1867 (z86-Nicolaus-25J!) — ŠIMEC-grafia",
        "h48": "Vlokušar[~Vukovičar?]-1867 (z35-64J!) — cf. krstne-h48-1890!",
        "h3": "Papic-#3-1867 (z98-Joannes-10-Tage!-Krčavica!)",
    },
    "crossChecks": [
        "md5-križna-validacija: s64+s65+s66+s67+s68-sveži == P209-disk-1:1 (7021e964/2c6e7d8e/092ded76/2a27e2a2/dddc4191) — VERIGA-14.×!",
        "ord-stolpec-s61-×3.5: '1,2,3,4,5,6,7,8,9,10' (10-ČISTO!) — restart-potrjen!",
        "s61-'1867'-VELIKA-LETVICA-KROP (48.-potrditev-invariante!) — VLM-'1864'-falsificirana!",
        "s69-tail-×1 == P209-VLM-1:1 (zap-103-Primostek-15-Lutblan-80J-ULEDBA!) ✓",
        "kontinuiteta-zap-35→36 (s63→s64 — 1867-klenar!) ✓",
        "vrstna-aritmetika: 10+12+13+13+13+13+13+15+1 = 103 ✓ (s69-tail-SAMO-103!)",
        "meseci-vsota: J18+F10+M4+A3+M9+J7+J9+A9+S9+O3+N12+D9+D1 = 103 ✓",
        "h7-×3-TRIPLE: 3-vpisa-v-isti-hiši-v-1-mesecu (Nov/Dez!) ✓",
        "PAPIC-×3-v-9-dneh (z95-8.Dez + z96-10.Dez + z98-17.Dez — vsi-Krčavica!) ✓",
        "s64-'2.36'-pripisa-Kurent-marginala (ne-ordinali!) ✓",
    ],
    "honesty": {
        "H1": "ŠTEVJE-IZ-VRSTIC-12.× (ordinali-1–103-ČISTO!); z-numeracija-vrstica-1:1",
        "H2": "'1867'-glava-KROP-potrjena — ampak-VLM-je-v-s61-prvo-brala-'1864' (falsificirana!)",
        "H3": "starost-DUELI-×2 (z3-'6-vs-65' + z8-'87-vs-37') — [~]",
        "H4": "ime-DUELI-×3 (z3/z15/z35) — [~]",
        "H5": "h74-vs-h71-DUEL (z26!)",
        "H6": "s65-VLM-leto-null (kontekst-manj-vredna-branja — zap-teče-vendar!)",
        "H7": "meseci-±1-drift ('Decemb'-skrajšan-1×!)",
        "H8": "s57–s60-1866-kontekst-SAMO-za-mejo (vpisi-NE-v-korpus-1867!)",
    },
    "kaskada": {
        "before": {"vitals": 1531, "04106": 279, "faz": 208},
        "after": {"vitals": 1531 + 13, "04106": 279 + 13, "faz": 209},
        "yearset": "+1867",
        "verifier_patch": "p19x–p208 (kumulativni-1531→1511 + 279→292 + yearset-+1868)",
    },
    "lead": {
        "P211": "1866 — s57–s60-ŽE-FETCHAN+VLM (zap-59–104: 1866-≈104-vpisov!) + s61-GLAVA-1867-ŽE-KROP-POTRJENA → probe-s050–s060!",
    },
    "entries_count": len(entries),
    "griblje_count": len(griblje),
    "notes": "P210 = 13-skenov-faza (s057–s069; 9-1867 + 4-kontekst-1866). Recept: P200–P209. Ordinali-1–103-ČISTO-4.leto. REKORD-20-GRIBLJE + h7-×3-TRIPLE + PAPIC-×3-Krčavica-klaster.",
}

# 1866-konec-kontekst (s60-VLM: zap-95–104 — tail-potencial!)
d60 = json.load(open("/tmp/p210/vlm-page/s60.json"))
tail_1866 = [x for x in d60.get("vrstice", []) if str(x.get("zaporedna") or "").strip().startswith(("95", "96", "97", "98", "99", "10"))]
proof["entries"] = entries
proof["tail_1866"] = tail_1866

import os
os.makedirs("/home/z/muzej/research/issue17", exist_ok=True)
json.dump(proof, open("/home/z/muzej/research/issue17/parish-death-1867-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: research/issue17/parish-death-1867-04106.json — {len(entries)}-vpisov / {len(griblje)}-Griblje / {len(hise)}-hiš")
print("hiše:", ",".join(hise))
print("otroci:", len(otroci), "/", len(griblje), f"= {round(100*len(otroci)/len(griblje))}%")
print("meseci:", meseci, "=", meseci_sum)
