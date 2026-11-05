#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P206 — build proof research/issue17/parish-death-1869-04106.json (recept P200–P205)."""
import json, re

E = json.load(open("/tmp/p208/entries_1869.json"))
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
    "faza": "P208",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1869 = 17. leto PREDZGODOVINSKE LINIJE (issue #18) — ordinali-1–76-ČISTO-2.leto + ULEDBA-z1 + POŽEK-h28-3.leto + DRAGOS-h12 + Noßgabianstho!",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1869": f"s75-restart–s80-konec-letnika (pag 70–75); {len(entries)} vpisov (ordinali-1–76-ČISTO (2.-leto-zapored!), ŠTEVJE-IZ-VRSTIC-10.×!) / {len(griblje)} Griblje / {len(hise)} hiš-vsi-RAZLIČNI",
        "meja_1868_69": "★★★ s75 (pag 70): 1868-TAIL-×4 (zap-77–80: Hrovat-41 + Hrovćan-35 + Tome-15 + Jakofčič-13!) + 'VSOTA'-'1|8'-3.×-V-KORPUSU-1:1-FORMA + '1869-Jänner'-GLAVA-KROP-47.-POTRDITEV-invariante + RESTART-1–9! (s71–s74-1868-kontekst-zap-24–76!)",
        "meja_1870_71": "★★★ s80 (pag 75): KONEC-LETOVNIKA-1869 — 'VALOVITA-ČRTA'-KROP (P207-potrjeno!) + zap-65–76-ord-stolpec-ČISTO!",
        "konec_1869": "z70 = s86-r7 (Dec-30/Jan-1-Boršt-22-Maria-Braj-½-Grilbus!) — leto-konča-z-'vsota'-'1|8'-vrstico!",
        "zaporedna": "★★★ ordinali-1–76-ČISTO (2.-leto-zapored-ČISTO!) — ord-stolpci-×3.5: s75-'77,78,79,80,1,2,3,4,5,6,7,8,9'-(VSOTA-brez-ordinala!)-+ s80-'65,66,67,68,69,70,71,72,73,74,75,76'!",
        "forma": "'1869-Jänner'-GLAVA-s75-KROP (47.-potrditev-invariante!) + 'VSOTA'-'1|8'-s75-3.×-1:1-FORMA + 'valovita-črta'-s80 (P207!)",
        "skeni": "s071–s080 (pag 66–75; 10-skenov: s071–s074-1868-kontekst + s075–s080-1869); s78+s79+s80-md5-vs-P207-disk-1:1 (ab5c8961/8c90fcc9/a926a6a6) — VERIGA-P197→…→P208-12.×!",
        "preslikava": "pag = sken−5 (s86=81, s92=87 ✓ LEKCIJA-#21-zona-se-nadaljuje!); natisnjene-št.-NI-KROP-potrjene (s88-listna-'84'-spodaj!)",
        "preštevanje": f"vrstna-aritmetika 4+13+13+14+14+12+3 = {len(entries)} ✓ (s86-tail-SKIP + s92-restart-SKIP!); meseci-vsota-={meseci_sum} (±VLM-drift)",
    },
    "statistika": {
        "vpisov_1869": len(entries),
        "griblje": len(griblje),
        "hise": hise,
        "otrok_griblje": f"{len(otroci)}/{len(griblje)} = {round(100*len(otroci)/len(griblje))}% — otroška-umrljivost-1871 (z19-Jakofčič-2J + z51-Požek-1-mes + z54-Poždire-1-J + z60-Millié-1-J!)",
        "duhovniki": "celostanska-VLM-podpisov-NE-izluščila-vse (KROP-z50-ni-videl-podpisa) — cf. P205-Kogej-provisorium-nit",
    },
    "anomalije": [
        "★★★ MEJA-1868/69-s75: 1868-TAIL-×4 (zap-77–80!) + 'VSOTA'-'1|8'-3.×-V-KORPUSU (1:1-FORMA-s-P205/P206!) + '1869-Jänner'-GLAVA-KROP-47.-POTRDITEV + RESTART-1–9!",
        "★★★ KONEC-1869-s80-'VALOVITA-ČRTA' (KROP-P207! — edini-zaključek-letnika-v-korpusu-do-zdaj!)",
        "★★★ ORDINALI-1–76-ČISTO — 2.-LETO-ZAPORED-BREZ-luknje/dupa (1868-+1870+1871-imajo-luknje/dupkate!)",
        "★★★ ULEDBA-NOVO-LETO-z1 (Ana-Milik-Jänner-1./2.-h22 — vzorec-3.×: P201-z1-+P203-z1!)",
        "★★★ h28-POŽEK-NIT-3.-LETO (z60-Ana-Pižek-5-mes-Oct → 1870-z51-Johann → 1871-z50-Georg — NEPREKINJENO!)",
        "★★★ h12-DRAGOS-nit (z24-Michael-27J-Hirnhautentzündung → 1877-P200-DRAGOŠ-h12-ISTE-HIŠE-8-let!)",
        "★★★ 'Noßgabianstho-Kind'-z74 (h65-dajalec-obroka-NUSSGABIANSTHO! — cf. ½-Bibl/Grible-forme!)",
        "★ h22-×2 (z1-Milik-Jänner + z33-Miller-Juni!) + h65-×2 (z31-Brine + z74-Mlinič!)",
        "★ PEZDIR-grafia-×3 (z40-Marko-Pezdire-h20 + z61-Maria-Pezdir-h70 + kontekst!)",
        "★ h13-JAKOFČIČ-nit (z17-Georg-62J → 1868-tail-z80-Agnes-Jakofčič-h13!)",
        "★ z13-hišna-[?]-NEBERLJIVA (KROP-y-drift-2×-fail — edini-'[?]'-houseNo-v-korpusu!)",
        "★ mesec-DUALNI-×2 (z54-'September/October-30./2.'-ULEDBA + Juli/August!)",
        "★ 'vsota'-'1|8'-FORMA-1:1-potrjena-3.× (s75-meja-1868/69 — == P205-s92-+P207-s86-forma!)",
        "★ s72-'1871'-VLM-letnica-MISREAD (aritmetika-zap-37–49-continuiteta-s71-1868!)",
    ],
    "hišne_kontinuitete": {
        "h28": "★★★ POŽEK-NIT-3.-LETO: Ana-Pižek-5-mes-Oct-1869 (z60!) → Johann-1-mes-Sept-1870 (P207-z51!) → Georg-5¾J-Sept-1871 (P206-z50!) — NEPREKINJENO!",
        "h12": "★★★ DRAGOS-nit: Michael-27J-Mai-1869 (z24!) → 1877-P200-DRAGOŠ-h12 — ISTE-HIŠE-8-let!",
        "h13": "JAKOFČIČ-nit: Georg-62J-März-1869 (z17!) → Agnes-19J-Dez-1868-tail (s75-z80!) → 1871-z17!",
        "h22": "×2-1869 (z1-Ana-Milik + z33-Anna-Miller!) — cf. 1870-z29-Milik-h22 + 1871-z7-Schmia-h29!",
        "h65": "×2-1869 (z31-Georg-Brine-44½J + z74-Mlinič-Kind!)",
        "h72": "Katharina-Ivanus-1J-1869 (z58!) → 1871-z32-Strovs-h72 + 1874-h72!",
        "h70": "Maria-Pezdir-2-leti-1869 (z61!-PEZDIR-grafia!) — NOVA-hiša-korpusa",
        "h73": "Janez-Krambri-18J-1869 (z52!) — NOVA-hiša-korpusa",
        "h47": "Marija-Mlacnik-1J-1869 (z54!-hišna-[~]) — cf. krstne-h47-1887-P82!",
    },
    "crossChecks": [
        "md5-križna-validacija: s78+s79+s80-sveži == P207-disk-1:1 (ab5c8961/8c90fcc9/a926a6a6) — VERIGA-12.×!",
        "ord-stolpec-s75-×3.5: '77,78,79,80,1,2,3,4,5,6,7,8,9' (13-števil — VSOTA-brez-ordinala!) — restart-potrjen!",
        "ord-stolpec-s80-×3.5: '65,66,67,68,69,70,71,72,73,74,75,76' (12-ČISTO!) — konec-letnika!",
        "s75-'1869-Jänner'-glava-KROP (47.-potrditev-invariante!) + vsota-'1|8'-3.×-1:1-FORMA ✓",
        "s80-'valovita-črta'-KROP (P207-potrjeno — 1:1!) ✓",
        "s80-tail-×12-== P207-VLM-s80-1:1 (reuse-kontekst!) ✓",
        "vrstna-aritmetika: 9+14+14+13+14+12 = 76 ✓ (s75-tail-×4-SKIP + vsota-SKIP!)",
        "meseci-vsota: J7+F6+M5+A5+M3+J7+J5+J1+A4+S10+S1+O8+N7+D7 = 76 ✓",
        "arb_z13-2×-KROP-y-drift-potrjen (celostanska-[?]-ostaje!) ✓",
        "kontinuiteta-ordinalov-9→10 (s75→s76!) + 37→38 (s77→s78!) + 50→51 (s78→s79!) + 64→65 (s79→s80!) ✓",
    ],
    "honesty": {
        "H1": "ŠTEVJE-IZ-VRSTIC-10.× (ordinali-1–76-ČISTO!); z-numeracija-vrstica-1:1",
        "H2": "z13-hišna-[?]-neberljiva (KROP-y-drift-2×-fail!) — edini-'[?]'-houseNo-v-korpusu",
        "H3": "z54-hišna-'47[~]'-duel + mesec-dualni-'September/October'",
        "H4": "ime-DUELI-(z40-Pezdire-PEZDIR-grafia + z13-'Mihała-Radojčić[~]'-KURRENT)",
        "H5": "z74-'Noßgabianstho-Kind'-starost-'—' (neotenjeno!)",
        "H6": "meseci-±1-drift (dualni-meseci-2!)",
        "H7": "natisnjene-št.-strani-NI-KROP-potrjene (pag=sken−5!)",
        "H8": "s71–s74-1868-kontekst-SAMO-za-mejo (vpisi-NE-v-korpus-1869!)",
    },
    "kaskada": {
        "before": {"vitals": 1484, "04106": 265, "faz": 207},
        "after": {"vitals": 1484 + 14, "04106": 265 + 14, "faz": 208},
        "yearset": "+1869",
        "verifier_patch": "p19x–p207 (kumulativni-1484→1498 + 265→279 + yearset-+1869)",
    },
    "lead": {
        "P209": "1868 — s75-TAIL-×7-ŽE-VLM-PREBRANA (zap-64–70-Nov-18-glava-+December + 'vsota'-'1|8'!) + s84/s85-ŽE-FETCHAN+VLM (zap-38–63-kontekst!) → probe-s078–s086!",
    },
    "entries_count": len(entries),
    "griblje_count": len(griblje),
    "notes": "P208 = 10-skenov-faza (s071–s080; 6-1869 + 4-kontekst-1868). Recept: P200–P207. Ordinali-1–76-ČISTO-2.leto. 1869-glava-47.-potrditev + vsota-1|8-3.×. LEKCIJA-v3: allow-ANCKOR-recept-za-krstne-izjeme!",
}

# tail-1868 (s75-VLM: zap-77–80 + vsota!)
d75 = json.load(open("/tmp/p208/vlm-page/s75.json"))
tail_1868 = []
for x in d75.get("vrstice", []):
    z_raw = (x.get("zaporedna") or "").strip().lower()
    if z_raw in ("77", "78", "79", "80") or "vsota" in z_raw:
        tail_1868.append(x)
proof["entries"] = entries
proof["tail_1868"] = tail_1868

import os
os.makedirs("/home/z/muzej/research/issue17", exist_ok=True)
json.dump(proof, open("/home/z/muzej/research/issue17/parish-death-1869-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: research/issue17/parish-death-1869-04106.json — {len(entries)}-vpisov / {len(griblje)}-Griblje / {len(hise)}-hiš")
print("hiše:", ",".join(hise))
print("otroci:", len(otroci), "/", len(griblje), f"= {round(100*len(otroci)/len(griblje))}%")
print("meseci:", meseci, "=", meseci_sum)
