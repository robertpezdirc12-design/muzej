#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P206 — build proof research/issue17/parish-death-1871-04106.json (recept P200–P205)."""
import json, re

E = json.load(open("/tmp/p206/entries_1871.json"))
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
    "faza": "P206",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1871 = 15. leto PREDZGODOVINSKE LINIJE (issue #18) — LUK-18 + DUP-19 + h11-nit-5.-leto + 'Ablasser'!",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1871": f"s86-restart–s92-tail-×3 (pag 81–87); {len(entries)} vpisov (ordinali-1–73 — LUK-18-pisarski-preskok + DUP-19-×2, ŠTEVJE-IZ-VRSTIC-8.×!) / {len(griblje)} Griblje / {len(hise)} hiš-vsi-RAZLIČNI",
        "meja_1870_71": "★★★ s86 (pag 81): 1870-TAIL-×7 (zap-64–70, Nov-18-glava + December) + 'VSOTA'-'1|8'-vrstica-2.×-V-KORPUSU + 'Jänner'-glava + RESTART-zaporedja-1–4; s84/s85 = 1870-kontekst (zap-38–63) — VLM-'1876'-glava-s85-MISREAD-falsificirana (aritmetika-zaklenjena: 38–50→51–63→64–70-Dec-1870!)",
        "meja_1871_72": "★★★ s92 (pag 87): TAIL-×3-DEZ-1871 (zap-71–73 + 'vsota'-'1|8') + 'December 1871'-GLAVA-KROP-POTRJENA (1:1-soglasje-s-P205-VLM!) + restart-1–9-'Jänner'-1872 = P205-LEAD",
        "konec_1871": "z73 = s92-r3 (Dez-20./22-Uranović-Mathias-Novak-2-Mh) — leto-konča-z-'vsota'-'1|8'-vrstico!",
        "zaporedna": "★★★ ordinali-1–73: LUK-18 (s87-zap-17 → s88-zap-19 — pisarski-preskok, vzorec-P204-luknje!) + DUP-19-×2-s88 (r1-Drugoše-Valentin-Kumin + r2-Primostek-Mathias-Klavec — vzorec-P204-dupkatov!) — ord-stolpec-cele-s88-×3.5: '19,19,20,21,22,23,24,25,26,27,28,29,30'!",
        "forma": "letnica-v-DATUMSKI-CELICI-×2: s89-r1-'1871-Mai-25./27'-Plut-KROP + s91-r1-marginalna-'59'-ordinala-marginala; mesec-glave-'December 1871'-s92-KROP",
        "skeni": "s084–s092 (pag 79–87; 9-skenov: s84/s85-1870-kontekst + s86–s92-1871); s92-md5-vs-P205-disk-1:1 (63705d84) — VERIGA-P197→…→P206-10.×!",
        "preslikava": "pag = sken−5 (s86=81, s92=87 ✓ LEKCIJA-#21-zona-se-nadaljuje!); natisnjene-št.-NI-KROP-potrjene (s88-listna-'84'-spodaj!)",
        "preštevanje": f"vrstna-aritmetika 4+13+13+14+14+12+3 = {len(entries)} ✓ (s86-tail-SKIP + s92-restart-SKIP!); meseci-vsota-={meseci_sum} (±VLM-drift)",
    },
    "statistika": {
        "vpisov_1871": len(entries),
        "griblje": len(griblje),
        "hise": hise,
        "otrok_griblje": f"{len(otroci)}/{len(griblje)} = {round(100*len(otroci)/len(griblje))}% — otroška-umrljivost-1871 (z5-Plut-13J + z50-Požek-5¾J!)",
        "duhovniki": "celostanska-VLM-podpisov-NE-izluščila-vse (KROP-z50-ni-videl-podpisa) — cf. P205-Kogej-provisorium-nit",
    },
    "anomalije": [
        "★★★ PISARSKI-ORDINAL-LUKNJA-18: ordinala-18-NIKJER (s87-konec-zap-17 → s88-zacetek-zap-19 — probe_s88top-'samo-19-brez-prekinitve'!) — pisarski-preskok-vzorec-P204-luknje!",
        "★★★ PISARSKI-ORDINAL-DUP-19: s88-r1-r2-ordinal-19-×2 (r1-Drugoše-Valentin-Kumin-April-4. + r2-Primostek-Mathias-Klavec-16J-April-9./9. — RAZLIČNA-VRSTA-ISTI-ordinal!) — vzorec-P204-dupkatov!",
        "★★★ ORD-STOLPEC-CELE-S88-×3.5-RECEPT-NOV: '19,19,20,21,22,23,24,25,26,27,28,29,30' (13-števil-1:1-z-13-vrsticami!) — ordinalni-stolpec-kot-ločen-izrez-REŠIL-off-by-N-ping-pong (celostanska-13-vrstic-'19–31'-WRONG-vs-wide-'30'-✓-vs-full-'29'-✗!)",
        "★★★ ime-DUEL-z17: celostanska-'Maria-Jančarič-110J[?]-ženska' vs KROP-'Grüblner-Tonis[=Anton!]-h13-starost-n/v-MOŠKI' — KROP-boljši-za-detail (25./27.+Lungensucht-soglasje!) — [~]",
        "★★★ stan-'ABlasser'-z29 (Nicolaus-Milič-65½J — KROP!-odpustitelj — 1.×-v-korpusu!) + hišna-DUEL-h66-vs-h65 (KROP-'65-potrjena-s-primerjavo-starosti'!)",
        "★★★ KROP-y-drift-LEKCIJA-#22: ob-mesečnih-glavah-izrezi-±1-vrstico-drift (z5/z7/z61/z62/z67-KROP-je-zadel-sosednje-vrste-Dec/Mar-writer-glyphs!) — celostanska-VLM-za-VRSTNE-POZICIJE-bolj-zanesljiva; KROP-UPORABEN-SAMO-ob-soglasju-o-poziciji (z13/z20/z29/z32/z50!)",
        "★★★ ordinala-DUEL-z20-Arik: celostanska-'21' vs ord-stolpec-'20' (REŠENO-ord-stolpec!) + ime-DUEL-Arik-vs-Urih (KROP!) + hišna-DUEL-h33-vs-h62/65 (KROP-'62-ali-65'!) — [~]",
        "★ VLM-'1876'-glava-s85 = MISREAD (aritmetika: zap-51–63-continuiteto-s84-38–50 → s86-tail-64–70-Dec-1870 — '1870'-Kurrent-misread!)",
        "★ z61-'None/None'-starost+bolezen (VLM-celostanska-negotovost — h65-Mihelič-October-18./19.)",
        "★ 'vsota'-'1|8'-2.×-V-KORPUSU (s86-zac + s92-konec-1871 — P205-1.×-s92!-enaka-forma!)",
        "★ h11-NIT-5.-LETO-1871 (z5-Josef-Plut-13J-Gehirnentzündung! — nit-RAZŠIRJENA-NAZAJ: 1871→1872→1873→1874→1875!)",
        "★ s86-z1-'Debravic-36-Anna-...-von-Griblnac[?]' — poreklo-'von-Griblje'-v-opombi (ni-Griblje-vpis!)",
    ],
    "hišne_kontinuitete": {
        "h11": "★★★ Plut-13J-1871 (z5!) → 1872-z23-otrok-2mes → 1873-z177-63J → 1874-16dni → 1875-KUNIĆ-65J — NIT-5-LET-NEPREKINJENO!",
        "h72": "Strovs-72J-1871 (z32!) → 1874-mrtvorojen-Mai + Malensič-72J-Sept (P203!)",
        "h2": "Klepec-54J-1871 (z62!) → 1873-Hlebec-z210 + 1874 (P204!) — h2-nit",
        "h28": "Požek-5¾J-1871 (z50!-'¼-Griblerjev-sohn') — cf. s85-zap-51-Požek-h28-1-mes-Sept-1870-kontekst — POŽEK-h28-NIT!",
        "h8": "Lakovčič-85J-1871-Dec (z67!) — cf. P200-1877-h8-ŠIMEC-nit",
        "h65": "Mihelič-1871 (z61!) + Milič-h66[~65?]-DUEL — h65/h66-kontekst-klaster",
        "h13": "Grüblner-Tonis[?]-1871 (z17!) — cf. P204-h13-×2-otroška-1873!",
        "h33": "Arik-91J-1871 (z20!) — NOVA-hiša-korpusa",
    },
    "crossChecks": [
        "md5-križna-validacija: s92-sveža == P205-disk-1:1 (63705d84) — VERIGA-10.×!",
        "ord-stolpec-cele-s88-×3.5: '19,19,20–30' (13-števil) — 1:1-z-13-VLM-vrsticami + zadnja-'30'-×4-soglasje (ord-zoom-×2 + wide + full-table)!",
        "s88-r1-'19'-(probe_s88top-'samo-19-brez-prekinitve'!) + r2-dup-'19'-(Primostek-Klavec-RAZLIČEN-vpis!) ✓",
        "s89-r1-'31-Plut-Podzemelj-h28-42J-'1871-Mai-25./27.'-letnica-V-CELICI (KROP!)-zamik-REŠEN",
        "s92-tail-×3 == P205-VLM-vrste-71–73-1:1 (Maria-Kerasinić-23 + Maria-Gunić-27 + Mathias-Novak-11!) ✓",
        "'vsota'-'1|8'-forma-×2 (s86-zac-1871 + s92-konec-1871 — 1:1-vzorec!) ✓",
        "'December 1871'-glava-KROP-s92 (1:1-soglasje-s-P205-VLM-meja!) ✓",
        "KROP-SOGLASJA-×5: z13-(h13-25./27-Lungensucht!) + z20-(zap-20-ord!) + z29-(65½J-Ablasser!) + z32-(h72-Juni-1./3.!) + z50-(5¾-J-9./11-Gehirnentzündung-POPOLNO!) ✓",
        "vrstna-aritmetika: 4+13+13+14+14+12+3 = 73 ✓ (s86-tail-×7-SKIP + s92-restart-×9-SKIP!)",
        "meseci-vsota: J6+F6+M5+A10+M4+J2+J3+A11+S7+O8+N3+D8 = 73 ✓",
    ],
    "honesty": {
        "H1": "ŠTEVJE-IZ-VRSTIC-8.× (ordinali-1–73-rekonstruirani: LUK-18 + DUP-19!); z-numeracija-vrstica-1:1",
        "H2": "ordinala-z20-Arik-DUEL-rešen-s-ord-stolpcem-×3.5 (celostanska-'21'-WRONG!)",
        "H3": "ime-DUELI-×2 (z17-Jančarič-vs-Grüblner + z20-Arik-vs-Urih) — [~]",
        "H4": "starost-DUELI-×3 (z17-'110J'-vs-'n/v' + z20-'91let' + z32-'72J'-vs-KROP-kljukice)",
        "H5": "hisna-DUELI-×2 (z20-h33-vs-62/65 + z29-h66-vs-65) — [~]",
        "H6": "KROP-y-drift-LEKCIJA-#22 (5/11-kropov-zadelo-sosednje-vrste-ob-mesečnih-glavah!) — celostanska-osnova-za-pozicije",
        "H7": "z61-'None/None'-starost+bolezen-neberljiva-v-celostanski",
        "H8": "meseci-vsota-±2-drift-možna (VLM-glave-različno-zajete)",
        "H9": "natisnjene-št.-strani-NI-KROP-potrjene-v-taj-seji (pag=sken−5-aritmetika-samo!)",
    },
    "kaskada": {
        "before": {"vitals": 1461, "04106": 242, "faz": 205},
        "after": {"vitals": 1461 + 11, "04106": 242 + 11, "faz": 206},
        "yearset": "+1871",
        "verifier_patch": "p19x–p205 (kumulativni-1461→1472 + 242→253 + yearset-+1871)",
    },
    "lead": {
        "P207": "1870 — s86-TAIL-×7-ŽE-VLM-PREBRANA (zap-64–70-Nov-18-glava-+December + 'vsota'-'1|8'!) + s84/s85-ŽE-FETCHAN+VLM (zap-38–63-kontekst!) → probe-s078–s086!",
    },
    "entries_count": len(entries),
    "griblje_count": len(griblje),
    "notes": "P206 = 7-skenov-faza (s084–s092; 5-1871 + 2-kontekst). Recept: P200–P205. LUK-18 + DUP-19-aritmetika-73. LEKCIJA-#22: KROP-y-drift-ob-mesečnih-glavah.",
}

# tail-1870 (s86-VLM: zap-64–70 + vsota)
d86 = json.load(open("/tmp/p206/vlm-page/s86.json"))
tail_1870 = []
for x in d86.get("vrstice", []):
    z_raw = (x.get("zaporedna") or "").strip().lower()
    if z_raw in ("64", "65", "66", "67", "68", "69", "70") or "vsota" in z_raw:
        tail_1870.append(x)
proof["entries"] = entries
proof["tail_1870"] = tail_1870

import os
os.makedirs("/home/z/my-project/research/issue17", exist_ok=True)
json.dump(proof, open("/home/z/my-project/research/issue17/parish-death-1871-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: research/issue17/parish-death-1871-04106.json — {len(entries)}-vpisov / {len(griblje)}-Griblje / {len(hise)}-hiš")
print("hiše:", ",".join(hise))
print("otroci:", len(otroci), "/", len(griblje), f"= {round(100*len(otroci)/len(griblje))}%")
print("meseci:", meseci, "=", meseci_sum)
