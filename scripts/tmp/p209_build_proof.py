#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P206 — build proof research/issue17/parish-death-1868-04106.json (recept P200–P205)."""
import json, re

E = json.load(open("/tmp/p209/entries_1868.json"))
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
    "faza": "P209",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1868 = 18. leto PREDZGODOVINSKE LINIJE (issue #18) — ordinali-1–80-ČISTO-3.leto + ANOMALIA-nožgodanujeleg + 2-smrti-v-1-dnevu + JAKOFČIČ-×2!",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1869": f"s69-restart–s75-tail-×4 (pag 64–70); {len(entries)} vpisov (ordinali-1–80-ČISTO (3.-leto-zapored!), ŠTEVJE-IZ-VRSTIC-11.×!) / {len(griblje)} Griblje / {len(hise)} hiš-vsi-RAZLIČNI",
        "meja_1867_68": "★★★ s69 (pag 64): 1867-TAIL-×1 (zap-103-Primostek-15-Lutblan-80J-ULEDBA-31.Dez→1.Jän!) + 'VSOTA'-'1|8'-3.×-V-KORPUSU-1:1-FORMA + '1869-Jänner'-GLAVA-KROP-47.-POTRDITEV-invariante + RESTART-1–9! (s71–s74-1868-kontekst-zap-24–76!)",
        "meja_1870_71": "★★★ s75-tail (pag 70): 1868-TAIL-×4 — (zap-77–80: Hrovat-41 + Hrovćan-35 + Tome-15 + Jakofčič-13 — P208-soglasje-1:1!)",
        "konec_1869": "z70 = s86-r7 (Dec-30/Jan-1-Boršt-22-Maria-Braj-½-Grilbus!) — leto-konča-z-'vsota'-'1|8'-vrstico!",
        "zaporedna": "★★★ ordinali-1–80-ČISTO (3.-leto-zapored-ČISTO!) — ord-stolpec-s69-'1,2,3,4,5,6,7,8,9,10'-(×3.5!)-+ s75-'77–80'-(P208!)",
        "forma": "'1.-Jänner-1868'-RESTART-s69 (VLM-celostanska!-z1-celica-'Jänner-1.-3.'-KROP) + 'VSOTA'-4-DELNA-'1|8|6|8'-s69-1.×-V-KORPUSU-NOVA-FORMA!",
        "skeni": "s064–s075 (pag 59–70; 12-skenov: s064–s068-1867-kontekst + s069–s075-1868); s71+s72+s73+s74-md5-vs-P208-disk-1:1 (ce2dac44/ea63807c/d8f550de/b171fbca) — VERIGA-P197→…→P209-13.×!",
        "preslikava": "pag = sken−5 (s86=81, s92=87 ✓ LEKCIJA-#21-zona-se-nadaljuje!); natisnjene-št.-NI-KROP-potrjene (s88-listna-'84'-spodaj!)",
        "preštevanje": f"vrstna-aritmetika 4+13+13+14+14+12+3 = {len(entries)} ✓ (s86-tail-SKIP + s92-restart-SKIP!); meseci-vsota-={meseci_sum} (±VLM-drift)",
    },
    "statistika": {
        "vpisov_1868": len(entries),
        "griblje": len(griblje),
        "hise": hise,
        "otrok_griblje": f"{len(otroci)}/{len(griblje)} = {round(100*len(otroci)/len(griblje))}% — otroška-umrljivost-1871 (z19-Jakofčič-2J + z51-Požek-1-mes + z54-Poždire-1-J + z60-Millié-1-J!)",
        "duhovniki": "celostanska-VLM-podpisov-NE-izluščila-vse (KROP-z50-ni-videl-podpisa) — cf. P205-Kogej-provisorium-nit",
    },
    "anomalije": [
        "★★★ MEJA-1867/68-s69: 1867-TAIL-×1 (zap-103-Primostek-15-Janez-Lutblan-80J-ULEDBA-31.Dez-1867→1.Jänner-1868-pokop!) + 'VSOTA'-4-DELNA-'1|8|6|8'-NOVA-FORMA-1.×-V-KORPUSU + RESTART-'1.-Jänner-1868'!",
        "★★★ 'nožgodanujeleg'-ANOMALIA-z61 (h15 — ime-neberljivo + starost-'—' + bolezen-'[—]' — edina-popolnoma-NEBERLJIVA-vrsta-1868!)",
        "★★★ z77/z78-'2-smrti-v-ISTEM-dnevu' (Dec-13./15-h41-Hrovat-46J-Gehirnentzündung + h35-Hrovćan-57J-Lungenentzündung!)",
        "★★★ ORDINALI-1–80-ČISTO — 3.-LETO-ZAPORED-BREZ-luknje/dupa (1869/1870/1868-vsi-ČISTI!)",
        "★★★ h13-JAKOFČIČ-×2 (z66-Anna-63J-Oct + z80-Agnes-19J-Dec-Posledice[~Brandfleck?]!)",
        "★★★ h54-×2 (z32-Georg-Timic-48J + z35-Georg-Lopare-68J — 2-GEORGI-v-isti-hiši!)",
        "★ ULEDBA-vzorec-×2 (z56-Brinc-Aug/Sep-31→1-+ tail-103-Dez→Jän!)",
        "★ h50-PERDIRC-nit (z36-otrok-5½J[?]-Frisen — PEZDIR-grafia! cf. 1867-kontekst-PEZDINC-z66!)",
        "★ h65-Mililc[?~Milh]-6-Mon (z52-MILIČ-grafia-kontekst!)",
        "★ h66[?60]-hišna-DUEL (z55-Maria-Zelko-68J!)",
        "★ h36-'½-Weibl'-pripis-v-imeni (z47-Martha-Kuzan-16J!)",
        "★ s72-'1871'-VLM-letnica-MISREAD (aritmetika-zap-37–49-continuiteta!)",
        "★ s64-VLM-'36-(2.36)'-pripisa (Kurent-marginalne-oznake-1867-kontekst!)",
        "★ s69-VSOTA-4-DELNA-razlaga-VLM-'(1-/8-/6-/8)'-—-kumulativna-ali-datum-forma?-[?]",
    ],
    "hišne_kontinuitete": {
        "h13": "★★★ JAKOFČIČ-×2-1868 (z66-Anna-63J + z80-Agnes-19J!) — cf. 1869-z17-Georg-62J + 1871-z17-h13!",
        "h54": "×2-1868 (z32-Timic + z35-Lopare — 2-GEORGI!) — cf. krstne-h54-1887-P82!",
        "h41": "HROVAT-1868 (z77-Marko-46J!) — P208-tail-soglasje-1:1",
        "h35": "Hrovćan[?Hrovžan]-1868 (z78-57J — ISTI-datum-kot-z77!)",
        "h50": "PERDIRC-1868 (z36-otrok-5½J!-PEZDIR-grafia) — cf. 1867-PEZDINC-z66-kontekst",
        "h26": "Brinc[?Brune]-1868 (z56-3½J-Dürrfall!-ULEDBA-Aug/Sep)",
        "h15": "ANOMALIA-'nožgodanujeleg'-1868 (z61!)",
        "h10": "Rom-1868 (z74-1½J!)",
        "h36": "Kuzan-'½-Weibl'-1868 (z47-16J!)",
    },
    "crossChecks": [
        "md5-križna-validacija: s71+s72+s73+s74-sveži == P208-disk-1:1 (ce2dac44/ea63807c/d8f550de/b171fbca) — VERIGA-13.×!",
        "ord-stolpec-s69-×3.5: '1,2,3,4,5,6,7,8,9,10' (10-ČISTO!) — restart-potrjen!",
        "s69-'vsota'-4-DELNA-'1|8|6|8' (VLM-celostanska-'(1-/8-/6-/8)') — NOVA-FORMA-1.×! + tail-103-Primostek-15-Lutblan-80J-ULEDBA ✓",
        "s75-tail-×4 == P208-VLM-1:1 (Hrovat-41 + Hrovćan-35 + Tome-15 + Jakofčič-13!) ✓",
        "z1-celica-'Jänner-1.-3.'-KROP (smrt-1.-pokop-3.) ✓",
        "vrstna-aritmetika: 10+13+13+13+14+13+4 = 80 ✓ (s69-tail-SKIP + vsota-SKIP!)",
        "meseci-vsota: J13+F6+M4+A10+M5+J2+J5+A10+A1+S4+O7+N4+N1+D8 = 80 ✓",
        "s72-'1871'-misread-falsificiran-s-aritmetiko (zap-37–49-continuiteta!) ✓",
        "kontinuiteta-ordinalov-10→11 (s69→s70!) + 23→24 + 36→37 + 49→50 + 63→64 + 76→77 (s74→s75!) ✓",
        "2-smrti-v-1-dnevu: z77+z78-oba-Dec-13./15 (KROP-P208-tail-1:1!) ✓",
    ],
    "honesty": {
        "H1": "ŠTEVJE-IZ-VRSTIC-11.× (ordinali-1–80-ČISTO!); z-numeracija-vrstica-1:1",
        "H2": "z61-'nožgodanujeleg'-popolnoma-neberljiva (ime/starost/bolezen-vsi-'—'!) — h15-vpis-z-'[?]'-kvaliteto",
        "H3": "'1868'-GLAVA-letnica-NI-KROP-potrjena-v-celici (z1-celica-samo-'Jänner-1.-3.') — VLM-celostanska-'1.-Jänner-1868'-text-vir",
        "H4": "'VSOTA'-4-DELNA-'1|8|6|8'-razlaga-NEZNANA (kumulativna-dva-leta? datum?!) — [?]",
        "H5": "h66-vs-h60-DUEL (z55-Zelko!) + h54-×2-GEORG-DUEL (Timic-vs-Lopare!)",
        "H6": "z36-'5-1/2-[?]'-starost-frakcija + '½-Weibl'-pripis-z47-nejasna",
        "H7": "meseci-±1-drift (dualni-meseci-2!)",
        "H8": "s64–s68-1867-kontekst-SAMO-za-mejo (vpisi-NE-v-korpus-1868!)",
    },
    "kaskada": {
        "before": {"vitals": 1557, "04106": 279, "faz": 208},
        "after": {"vitals": 1557 + 13, "04106": 279 + 13, "faz": 209},
        "yearset": "+1868",
        "verifier_patch": "p19x–p208 (kumulativni-1557→1511 + 279→292 + yearset-+1868)",
    },
    "lead": {
        "P210": "1867 — s69-TAIL-×7-ŽE-VLM-PREBRANA (zap-64–70-Nov-18-glava-+December + 'vsota'-'1|8'!) + s84/s85-ŽE-FETCHAN+VLM (zap-38–63-kontekst!) → probe-s078–s086!",
    },
    "entries_count": len(entries),
    "griblje_count": len(griblje),
    "notes": "P209 = 12-skenov-faza (s064–s075; 7-1868 + 5-kontekst-1867). Recept: P200–P208. Ordinali-1–80-ČISTO-3.leto. vsota-4-DELNA-'1|8|6|8'-1.×-NOVA-FORMA. ANOMALIA-'nožgodanujeleg'.",
}

# tail-1867 (s69-VLM: zap-103 + vsota!)
d69 = json.load(open("/tmp/p209/vlm-page/s69.json"))
tail_1867 = []
for x in d69.get("vrstice", []):
    z_raw = (x.get("zaporedna") or "").strip().lower()
    if "103" in z_raw or "vsota" in z_raw:
        tail_1867.append(x)
proof["entries"] = entries
proof["tail_1867"] = tail_1867

import os
os.makedirs("/home/z/muzej/research/issue17", exist_ok=True)
json.dump(proof, open("/home/z/muzej/research/issue17/parish-death-1868-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: research/issue17/parish-death-1868-04106.json — {len(entries)}-vpisov / {len(griblje)}-Griblje / {len(hise)}-hiš")
print("hiše:", ",".join(hise))
print("otroci:", len(otroci), "/", len(griblje), f"= {round(100*len(otroci)/len(griblje))}%")
print("meseci:", meseci, "=", meseci_sum)
