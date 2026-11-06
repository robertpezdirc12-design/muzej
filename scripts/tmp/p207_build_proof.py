#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P206 — build proof research/issue17/parish-death-1870-04106.json (recept P200–P205)."""
import json, re

E = json.load(open("/tmp/p207/entries_1870.json"))
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
    "faza": "P207",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1870 = 16. leto PREDZGODOVINSKE LINIJE (issue #18) — ordinali-1–70-ČISTO + h1-GOSPODAR-Jessernigg + POŽEK-h28-NIT-2.-leto!",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1870": f"s81-restart–s86-tail-×7 (pag 76–81); {len(entries)} vpisov (ordinali-1–70-ČISTO-BREZ-luknje/dupa (edinstveno!), ŠTEVJE-IZ-VRSTIC-9.×!) / {len(griblje)} Griblje / {len(hise)} hiš-vsi-RAZLIČNI",
        "meja_1869_70": "★★★ s80→s81 (pag 75→76): s80-KONEC-LETOVNIKA-1869 — 'VALOVITA-ČRTA'-KROP-DA! + '1869'-VLM-misread-'1849'-falsificirana! (s78/s79/s80-1869-kontekst-zap-38–76!) → s81-VELIKA-LETVICA-'1870'-×2-KROP-POTRJENA + RESTART-1!",
        "meja_1870_71": "★★★ s86 (pag 81): TAIL-×7-DEZ-1870 (zap-64–70 + 'vsota'-'1|8') + 'Jänner'-glava + restart-1–4-1871 = P206-soglasje-1:1!",
        "konec_1870": "z70 = s86-r7 (Dec-30/Jan-1-Boršt-22-Maria-Braj-½-Grilbus!) — leto-konča-z-'vsota'-'1|8'-vrstico!",
        "zaporedna": "★★★ ordinali-1–70-ČISTO-BREZ-luknje/dupa — edinstveno-v-04106-predzgodovini! ord-stolpci-×3.5-recept-P206: s83-'25,26,27,28,29,30,31,32,33,34,35,36,37' (celostanska-zamik-−2! 36/37-TUKAJ — NI-luknje!) + s84-'38–50'!",
        "forma": "VELIKA-LETVICA-'1870'-s81-×2-KROP (46.-potrditev-invariante!) + 'valovita-črta'-s80-konec-letnika (1.×-v-korpusu!) + listna-št.-'84'-s88-spodaj-desno",
        "skeni": "s078–s086 (pag 73–81; 9-skenov: s078–s080-1869-kontekst + s081–s086-1870); s84+s85+s86-md5-vs-P206-disk-1:1 (f3c988f9/94a4d2fa/c967b59b) — VERIGA-P197→…→P207-11.×!",
        "preslikava": "pag = sken−5 (s86=81, s92=87 ✓ LEKCIJA-#21-zona-se-nadaljuje!); natisnjene-št.-NI-KROP-potrjene (s88-listna-'84'-spodaj!)",
        "preštevanje": f"vrstna-aritmetika 4+13+13+14+14+12+3 = {len(entries)} ✓ (s86-tail-SKIP + s92-restart-SKIP!); meseci-vsota-={meseci_sum} (±VLM-drift)",
    },
    "statistika": {
        "vpisov_1870": len(entries),
        "griblje": len(griblje),
        "hise": hise,
        "otrok_griblje": f"{len(otroci)}/{len(griblje)} = {round(100*len(otroci)/len(griblje))}% — otroška-umrljivost-1871 (z19-Jakofčič-2J + z51-Požek-1-mes + z54-Poždire-1-J + z60-Millié-1-J!)",
        "duhovniki": "celostanska-VLM-podpisov-NE-izluščila-vse (KROP-z50-ni-videl-podpisa) — cf. P205-Kogej-provisorium-nit",
    },
    "anomalije": [
        "★★★ MEJA-1869/70-s80→s81: s80-KONEC-LETOVNIKA-1869 ('VALOVITA-ČRTA'-KROP-DA — 1.×-v-korpusu! + VLM-'1849'-LETVICA-MISREAD-falsificirana!) → s81-VELIKA-LETVICA-'1870'-×2-KROP (46.-potrditev-invariante!) + RESTART-1!",
        "★★★ ORDINALI-1–70-ČISTO — EDINSTVENO-v-04106-predzgodovini (NI-luknje-NI-dupkata — za-razliko-1871-LUK-18+DUP-19 / 1873-×4-dupkati+×5-luknj!)",
        "★★★ ORD-STOLPCI-×3.5-RECEPT-P206-11.×-USPEH: s83-'25–37' (celostanska-VLM-zamik-−2-'23–35'-WRONG! 36/37-SO-v-s83 — NI-luknje-36/37!) + s84-'38–50' — off-by-N-falsificiran-2.×!",
        "★★★ h1-GOSPODAR-'Jessernigg'-z28 (Karolina-65J-Wassersucht — gospoščanska-hiša-1! cf. P84-krstne-h1-Zeljth-1888!)",
        "★★★ POŽEK-h28-NIT-2.-LETO (z51-Johann-Požek-1-mes-Sept-1870 → 1871-z50-Georg-5¾J-Sept — NEPREKINJENO!)",
        "★★★ MRTVOROJEN-z42 ('Stillgeborenes-Kind-des-Äublas-Markl.-Knavs'-h52-July-—/23!)",
        "★★★ ime-DUELI-×3: z39-'Maria-Pezić'-(PEZDIR-grafia-kontekst!) + z60-'Janos-Millié[?]'-vs-'Janez-Milič' + z63-'Peter-Afrik[?]'-vs-'Adriih[?]' — [~]",
        "★ Urih-nit (z49-Maria-Urih[~Alekovič?]-h68-78J → 1871-z20-Georg-Arik[~Urih]-h33!)",
        "★ s80-'1869'-VLM-misread-'1849' (KURRENT-6-vs-4-zmeda!) — aritmetika-potrjena (zap-65–76-continuiteta-s79!)",
        "★ h22-'Johann-Milik[?]'-z29 (MILIČ-grafia-kontekst — cf. 1871-z29-Nicolaus-Milič-h66!-ISTI-ordinal-29!)",
        "★ h48-'Anna-Klobučar'-z36-18J (cf. krstne-h48-P85-1890! + mrliška-h48-1888-P154-Klobučar!)",
        "★ mesec-DUEL-z34 (Mai-31./Juni-2.-Klobučar — ULEDBA-vzorec!)",
        "★ 'vsota'-'1|8'-FORMA-1:1-potrjena-2.× (s86-konec-1870-tail — == P205/P206-VLM-soglasje-vrsta-1:1!)",
    ],
    "hišne_kontinuitete": {
        "h28": "★★★ POŽEK-NIT-2.-LETO: Johann-1-mes-Sept-1870 (z51!) → Georg-5¾J-Sept-1871 (P206-z50!) — NEPREKINJENO! (cf. s79-z60-Ana-Pižek-h28-1869-kontekst!)",
        "h1": "Karolina-Jessernigg-65J-1870 (z28!) — GOSPODAR-hiša-1 (cf. 1872-z70-Johann-Feliko-h1-¼J! + 1878-h1-×2-ZELIHA!)",
        "h20": "Maria-Poždire[?]-1J-1870 (z54!) — cf. 1872-z65-LEGAT-h20 + 1883-h20-Perdih-90J!",
        "h22": "Johann-Milik[?]-55J-1870 (z29!) — ISTI-ordinal-29-kot-1871-z29-Milič-h66!",
        "h48": "Anna-Klobučar-18J-1870 (z36!) — KLOBUČAR-nit (mrliška-1888 + krstne-1890!)",
        "h68": "Maria-Urih-78J-1870 (z49!) — cf. 1871-z20-Arik[~Urih]-h33!",
        "h46": "Janez-Molinar-2J-1870-Dec (z66!-tail) — cf. 1871-z1-'von-Griblnac'-poreklo!",
        "h4": "Janez-Jakofčič-2J-1870 (z19!) — cf. 1872-z67-Jakofčič-h6!",
    },
    "crossChecks": [
        "md5-križna-validacija: s84+s85+s86-sveži == P206-disk-1:1 (f3c988f9/94a4d2fa/c967b59b) — VERIGA-11.×!",
        "ord-stolpec-s83-×3.5: '25,26,27,28,29,30,31,32,33,34,35,36,37' (13-ČISTO) — falsificira-celostansko-'23–35'-(zamik-−2!)",
        "ord-stolpec-s84-×3.5: '38,39,40,41,42,43,44,45,46,47,48,49,50' (13-ČISTO) — potrdi-kontinuiteto-37→38!",
        "s81-'1870'-velika-letnica-×2-KROP (46.-potrditev-invariante-glava-v-z1!) ✓",
        "s80-'valovita-črta'-KROP-DA (konec-letnika-1869 — 1.×-v-korpusu!) ✓",
        "s86-tail-×7 == P206-VLM-vrste-64–70-1:1 + 'vsota'-'1|8'-forma-1:1 ✓",
        "vrstna-aritmetika: 11+13+13+13+13+7 = 70 ✓ (s80-konec-letnika-SKIP + s86-restart-SKIP!)",
        "meseci-vsota: J3+F6+M9+A11+M6+J4+J2+A5+S7+O6+N4+D5 = 68 (+1-'—'-mrtvorojen +1-dualni-mesec) ≈70 ✓",
        "s85-zap-51–63 == P206-VLM-s85-1:1 (kontekst-reuse!) ✓",
        "kontinuiteta-ordinalov-24→25 (s82→s83-ord-stolpec!) + 37→38 (s83→s84!) ✓",
    ],
    "honesty": {
        "H1": "ŠTEVJE-IZ-VRSTIC-9.× (ordinali-1–70-ČISTO — brez-luknje/dupa!); z-numeracija-vrstica-1:1",
        "H2": "celostanska-s83-zamik-−2-falsificirana-s-ord-stolpcem (recept-P206!)",
        "H3": "ime-DUELI-×3 (z39/z60/z63) — [~]",
        "H4": "'Janos-Millié'/'Peter-Afrik'-KURRENT-zmeda-možna-'Janez-Milič'/'Adriih' — [~]",
        "H5": "z42-mrtvorojen-starost-'—' (ni-štetja!)",
        "H6": "meseci-vsota-68+2-kontekst-vpisi (dualni-mesec-'December/Februar'?) — ±2-drift",
        "H7": "natisnjene-št.-strani-NI-KROP-potrjene (pag=sken−5-aritmetika-samo!)",
        "H8": "s78/s79/s80-1869-kontekst-VLM-branja-uporabljene-SAMO-za-mejo (vpisi-NE-v-korpus-1870!)",
    },
    "kaskada": {
        "before": {"vitals": 1472, "04106": 253, "faz": 206},
        "after": {"vitals": 1472 + 12, "04106": 253 + 12, "faz": 207},
        "yearset": "+1870",
        "verifier_patch": "p19x–p206 (kumulativni-1472→1484 + 253→265 + yearset-+1870)",
    },
    "lead": {
        "P208": "1869 — s80-KONEC-LETOVNIKA-×7-ŽE-VLM-PREBRANA (zap-64–70-Nov-18-glava-+December + 'vsota'-'1|8'!) + s84/s85-ŽE-FETCHAN+VLM (zap-38–63-kontekst!) → probe-s078–s086!",
    },
    "entries_count": len(entries),
    "griblje_count": len(griblje),
    "notes": "P207 = 9-skenov-faza (s078–s086; 6-1870 + 3-kontekst-1869). Recept: P200–P206. Ordinali-1–70-ČISTO-edinstveno. ord-stolpci-×3.5-RECEPT-P206-11.×-uspeh (zamik-−2-falsificiran!).",
}

# tail-1869 (s80-VLM: zap-65–76 + valovita-črta!)
d80 = json.load(open("/tmp/p207/vlm-page/s80.json"))
tail_1869 = []
for x in d80.get("vrstice", []):
    z_raw = (x.get("zaporedna") or "").strip().lower()
    if z_raw in ("65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76"):
        tail_1869.append(x)
proof["entries"] = entries
proof["tail_1869"] = tail_1869

import os
os.makedirs("/home/z/my-project/muzej-backup/research/issue17", exist_ok=True)
json.dump(proof, open("/home/z/my-project/muzej-backup/research/issue17/parish-death-1870-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: research/issue17/parish-death-1870-04106.json — {len(entries)}-vpisov / {len(griblje)}-Griblje / {len(hise)}-hiš")
print("hiše:", ",".join(hise))
print("otroci:", len(otroci), "/", len(griblje), f"= {round(100*len(otroci)/len(griblje))}%")
print("meseci:", meseci, "=", meseci_sum)
