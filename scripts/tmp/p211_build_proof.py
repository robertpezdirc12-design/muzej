#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P211 — build proof research/issue17/parish-death-1866-04106.json (recept P200–P210)."""
import json, re, os

E = json.load(open("/tmp/p211/entries_1866.json"))
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
    "faza": "P211",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1866 = 20. leto PREDZGODOVINSKE LINIJE (issue #18) — ordinali-1–104-ČISTO-5.leto + DOUBLE-SCAN-4.× + DVOJČKA-Totgeborenes + ULEDBA-#10 + HUESTIČ-h41-kontinuiteta! — SANDBOX-RESET-REGENERACIJA (re-recept iz-GitLab-restavracije-P210!)",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1866": f"s51-restart–s60-konec-zap-104 (pag 46–55); {len(entries)} vpisov (ordinali-1–104-ČISTO (5.-leto-zapored!), ŠTEVJE-IZ-VRSTIC-13.×!) / {len(griblje)} Griblje / {len(hise)} hiš (h34-×2-FILAK!)",
        "meja_1865_66": "★★★ s51 (pag 46): tail-1865 (z65-Zemelj-h13-Anna-Berkovec-60J + z66-Griblje-h14-Maria-Pezdirc-66J-KROP!) + PREČRTANA-PRAZNA-VRSTA-67 (Schlangenlinien!-SKIP!) + restart-'Jänner'-'1866'-VELIKA-LETVICA-KROP-49.-POTRDITEV-invariante!",
        "meja_1866_67": "★★★ s60-konec-zap-104 → s61-restart-'1867' (P210-že-obdelano!)",
        "zaporedna": "★★★ ordinali-1–104-ČISTO-BREZ-luknje/dupa — 5.-LETO-ZAPORED! (kontinuiteta-zap: s51-z1→s60-z104; vrstna-aritmetika 8+12+13+12+13+13+11+12+10)",
        "forma": "'1866'-VELIKA-LETVICA-s51-KROP (49.-potrditev-invariante!) + 'Jänner'-glava-restart!",
        "skeni": "s050–s060 (pag 45–55; 11-skenov: s50-1865-kontekst-zap-50–64 + s51–s60-1866); SANDBOX-RESET: /tmp-diski-izgubljeni → 2×-NEODVISNA-PRENOSA-vsak-sken-md5-samoskladnost-11/11! (veriga-P197→…→P210-14.× + vsebinska-križ-s60↔P210-tail-zap-95–104-10/10!)",
        "preslikava": "pag = sken−5 (s51=46 … s60=55)",
        "preštevanje": f"vrstna-aritmetika 8+12+13+12+13+13+11+12+10 = {len(entries)} ✓ (s51-tail+prečrtana-SKIP + s54-DOUBLE-SCAN-SKIP!); meseci-vsota = {meseci_sum}",
    },
    "statistika": {
        "vpisov_1866": len(entries),
        "griblje": len(griblje),
        "hise": hise,
        "otrok_griblje": f"{len(otroci)}/{len(griblje)} = {round(100*len(otroci)/len(griblje))}% — otroška-umrljivost-1866-EXSTREMNA (z41-19d? + z48-6½J + z50-5-mes + z58-4-mes + z64-2J + z78-3½-t + z79-9-dni + z80-1-t + z90-Totgeborenes + z98-Missgeborenes = 10-otrok/2-odrasla/1-duel!)",
        "meseci": meseci,
        "duhovniki": "celostanska-VLM-podpisov-delno ('ditti'-×8 + 'D.-Teržan[~]'-×7 + N.N.-×7)",
    },
    "anomalije": [
        "★★★ DOUBLE-SCAN-4.×: s53==s54 (md5-RAZLIČNA-450719B/470425B — vsebina-1:1: zap-21–33-enako, vas-13/13, imena-13/13, smrti-13/13!) → s54-SKIP (cf. P204-s103==s104!)",
        "★★★ MEJA-1865/66-s51: tail-1865-z65/z66 (KROP-glava!) + PREČRTANA-PRAZNA-VRSTA-67-Schlangenlinien-SKIP + restart-'1866'-VELIKA-LETVICA-KROP-49.-POTRDITEV!",
        "★★★ DVOJČKA-MRTVOROJENA-z34/z35 (s55): 'Totgeborenes Kind v. Josef Žunič'-×2, Vranoviče-h19, April-22./23. (VLM-'Posmrhlanski/Turškorojeni'-halucinaciji-FALSIFICIRANI-KROP!)",
        "★★★ ULEDBA-#10-9.INSTANCE-z58: smrt-29-JUNI → pokop-1-JULI (KROP-'Juli-1'-ČISTO!) — cf. P209-z103 + P203/P202!",
        "★★★ z22-HUESTIČ-h41-KONTINUITETA: Maria-Hušić[~Huestič/Kusić?]-22-J-¼-güblerštofa-h41 — 1903-poroka-Maria-HUESTIČ-GRIBLJE-41-½-griblarštofa + oče-Matthias-¼-griblar! (hiša-DUEL-11-vs-41-rešen-izrezom; prejšnja-seja-'Kusić'-FALSIFICIRANA-s-kontinuiteto!)",
        "★★★ z41-PEZDIRC-h14-KONTINUITETA: Mathias-unehelich-Kind-¼-gübler[?]-h14 — z66-tail-1865-Maria-Pezdirc-h14! + starost-DUEL-HONEST ('19-dni[?]'VLM / '1½-let[?]'KROP / '1-leto'-stara-seja)",
        "★★★ z90-FALSIFIKACIJA-2-OSEBI: 'Totgeborenes[~Taubgebarend?] Kind v. Mark. POŽEK'-h58 (KROP-4.2×!) — POŽEK-h58-kontinuiteta (P192-h58-POŽEK-×2!) — VLM-'Laufgrabend-žival' + KROP-'Laurentius-Ažić+še-Marjeta'-obe-FALSIFICIRANI!",
        "★★★ z98-FALSIFIKACIJA-'Anton': 'Missgeborenes Kind d. Janez PEZDIRC'-h53 (KROP-4.2×!) — P210-tail-'Missgeburt-Anton-dešk'-halucinacija!",
        "★★★ h34-FILAK-×2 (z48-Katarina-6½-J-Juni + z80-Josip[~Filip]-1-teden-September!)",
        "★★★ KLOBUČAR-×2-v-4-dneh (z78-h47-3½-t + z79-h48-9-dni — 2-hiši!)",
        "★ otroška-umrljivost-1866: 10/13-GRIBLJE = 77% (10-otrok!) — MAX-predzgodovine!",
        "★ ½/¼-GÜBLER-leksikon (z22-¼-güblerštofa + z41-unehelich-¼-gübler + z58-½-güblerštocha + z99-½-griblarštofa — cf. 1903-'griblarštofa'-grafia!)",
        "★ hiša-DUELI-×2-rešena-KROP (z22-11→41 + z41-11?→14!)",
        "★ s50-1865-kontekst-zap-50–64 (15-vrstic — P212-lead!)",
    ],
    "hišne_kontinuitete": {
        "h41": "★★★ HUESTIČ-nit: Maria-Hušić[~Huestič]-22J-¼-güblerštofa-1866 (z22!) → 1903-Maria-HUESTIČ-h41-½-griblarštofa (37-let-globoko!) + h41-krstni-vzorec-1890-P85!",
        "h14": "★★★ PEZDIRC-nit: z66-tail-Maria-Pezdirc-66J-1865 + z41-Mathias-unehelich-Kind-1866!",
        "h34": "★★★ FILAK-×2-1866 (z48-Katarina-6½J-Marbmil + z80-Josip-1-t-Frisen!)",
        "h58": "★★★ POŽEK-nit: z90-Totgeborenes-Kind-v.-Mark.-Požek-1866 — cf. P192-h58-POŽEK-×2-1885!",
        "h53": "PEZDIRC-nit-#2: z98-Missgeborenes-Kind-d.-Janez-Pezdirc-1866!",
        "h1": "z58-Maria-Želko-½-güblerštocha-1866 — cf. P192-h1-MUC-bajtar!",
        "h3": "z50-Štefan-Štrucelj-5-mes-1866 — cf. 1867-z98-h3-Papic!",
        "h13": "z64-Jura-Zakotnik-2J-1866 — cf. h13-JAKOFČIČ-nit-1867!",
        "h47/h48": "KLOBUČAR-×2-v-4-dneh (2-hiši!)",
    },
    "crossChecks": [
        "SANDBOX-RESET-REGENERACIJA: 2×-neodvisna-prenosa-vsak-sken-md5-1:1-11/11 (strežnik-determinističen!) — veriga-P211-2×-samoskladnost-11.×!",
        "vsebinska-križ: svež-s60-VLM ↔ P210-dokaz-tail_1866-zap-95–104 = 10/10-zap-EXAKT + vrstna-identiteta-10/10 (ortografska-varianca-samo!)",
        "DOUBLE-SCAN-4.×-dokaz: s53-vs-s54 po-imenih-13/13-enako + po-smrtih-13/13-enako (ortografska-varianca: Krizan/Križan, Novak-Nuević/Hušić, Klopec/Klepec!) — s54-SKIP ✓",
        "'1866'-VELIKA-LETVICA-KROP-s51 (49.-potrditev-invariante!) ✓",
        "tail-1865-KROP: z65-Zemelj-h13-Anna-Berkovec-60J + z66-Griblje-h14-Maria-Pezdirc-66J (december!) ✓",
        "vrstna-aritmetika: 8+12+13+12+13+13+11+12+10 = 104 ✓ (s51-tail+prečrtana-SKIP!)",
        f"meseci-vsota: J8+F5+M7+A12+M10+J13+J9+A7+S7+O7+N11+D4 = {meseci_sum}-normirano (+Martii-3 + '31.'-anomalia-1 = 104!) ✓",
        "Griblje-13/12-hiš (h34-×2) == prejšnja-seja-1:1 (RE-GENERACIJA-POTRJENA!) ✓",
        "z22-h41: KROP-izrez-'4-z-zanko+1'-ČISTO + VLM-B-h41 + HUESTIČ-1903-h41-TRIPLI-DOKAZ ✓",
        "z41-h14: KROP-tight-4×-'14'-ČISTO + Pezdirc-z66-tail-h14-kontinuiteta ✓",
        "z58-'Juli 1'-KROP-ČISTO (ULEDBA!) ✓",
        "z90-'Taubgebarend(?) Kind v. Mark. Požek'-KROP-4.2× (2-OSEBI-FALSIF!) ✓",
        "z98-'Missgeborenes Kind d. Janez Pezdarc'-KROP-4.2× ('Anton'-FALSIF!) ✓",
    ],
    "honesty": {
        "H1": "ŠTEVJE-IZ-VRSTIC-13.× (ordinali-1–104-ČISTO!); z-numeracija-vrstica-1:1",
        "H2": "SANDBOX-RESET: /tmp-diski-P197–P210-izgubljeni → križna-validacija-rekonstruirana-kot-2×-prenoza + vsebinska-križ-vs-P210-dokaz (namesto-disk-md5!)",
        "H3": "z41-starost-DUEL-ne-rešen ('19'-ČISTO-ampak-enota-nečitljiva: dni?/1½-let?) — [~]",
        "H4": "z22-priimek-DUEL (Hušić-izrez+kontinuiteta-VS-prejšnja-seja-'Kusić') — zapis-Hušić[~Huestič/Kusić?]",
        "H5": "z90-'Taubgebarend'vs'Totgeborenes'-glyf-DUEL — [~]",
        "H6": "s53-VLM-leto-'1864'-halucinacija (glava-ni-v-izrezu — kontinuiteta-z52-potrjuje-1866!)",
        "H7": "meseci-±1-drift ('Februar'×5 + 'Martii'×3 + '31.'×1-anomalia!)",
        "H8": "z58-starost-VLM-'4-mesce' + z99-hiša-duel-24-vs-27 (ne-Griblje!)",
        "H9": "z19-h19-[?] — prvi-GRIBLJE-h19-dokaz (potrditev-čiaka-v-mlajših-letih!)",
    },
    "kaskada": {
        "before": {"vitals": 1531, "04106": 312, "faz": 210},
        "after": {"vitals": 1531 + 13, "04106": 312 + 13, "faz": 211},
        "yearset": "+1866",
        "verifier_patch": "p19x–p211 (kumulativni-1531→1544 + 312→325 + yearset-+1866)",
    },
    "lead": {
        "P212": E.get("leadP212", "1865 — s50-ŽE-FETCHAN+VLM (zap-50–64) + s51-TAIL-ŽE-KROP → probe-s042–s050!"),
    },
    "entries_count": len(entries),
    "griblje_count": len(griblje),
    "notes": "P211 = 11-skenov-faza (s050–s060; 10-1866 + 1-kontekst-1865). SANDBOX-RESET-REGENERACIJA: repo-re-kloniran-@P203 → GitLab-restavracija-1:1-P210 → re-recept-1:1 (104/13-EXAKT == prejšnja-seja!). DOUBLE-SCAN-4.× + DVOJČKA + ULEDBA-#10 + HUESTIČ/PEZDIRC/POŽEK-kontinuitete.",
}

# tail_1865 (s51-KROP) + s50-1865-kontekst
kglava = json.load(open("/tmp/p211/krop-reads/arb_s51_glava.json"))
proof["entries"] = entries
proof["griblje_entries"] = griblje
proof["tail_1865"] = {"vir": "s51-KROP-glava (pag 46)", "vrstice": kglava.get("tail_vrstice", []),
                       "precrtana": kglava.get("precrtana_vrsta"), "restart": kglava.get("restart_vrsta1"),
                       "velika_letnica": kglava.get("velika_letnica")}
d50 = json.load(open("/tmp/p211/vlm-page/s50.json"))
proof["kontekst_1865_s50"] = {"zap": "50–64", "vrstic": len(d50.get("vrstice", [])), "vrstice": d50.get("vrstice", [])}

os.makedirs("/home/z/my-project/research/issue17", exist_ok=True)
json.dump(proof, open("/home/z/my-project/research/issue17/parish-death-1866-04106.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: research/issue17/parish-death-1866-04106.json — {len(entries)}-vpisov / {len(griblje)}-Griblje / {len(hise)}-hiš")
print("hiše:", ",".join(hise))
print("otroci:", len(otroci), "/", len(griblje), f"= {round(100*len(otroci)/len(griblje))}%")
print("meseci:", meseci, "=", meseci_sum)
