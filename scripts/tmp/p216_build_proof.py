#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P216 — dokaz parish-death-1861-04106.json (54 entries: 10-Griblje + 44-druge!)."""
import json
from collections import defaultdict

TMP = "/tmp/p216"
E = json.load(open(f"{TMP}/entries_1861.json"))
entries = E["entries"]
grib = E["griblje_entries"]

hise = sorted({e.get("hisna") for e in grib}, key=lambda x: int(x))
hise_map = defaultdict(list)
for e in grib:
    hise_map[e.get("hisna")].append(e["z"])

# otroci Griblje 1861: z15 (2J) + z17 (5t) + z35 (1½J) + z44 (3J) + z54 (2J) = 5
OTROCI_Z = [15, 17, 35, 44, 54]
otrostenje = f"{len(OTROCI_Z)}/{len(grib)} = {round(100*len(OTROCI_Z)/len(grib))}%"

meseci_g = defaultdict(int)
for e in grib:
    m = str(e.get("mesec", "")).split()[0]
    meseci_g[{"August": "A", "April": "A", "März": "M", "Juli": "J", "Oktober": "O", "Dezember": "D"}.get(m, m)] += 1

proof = {
    "faza": "P216",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1861 = 25/29 (issue #18)",
    "knjiga": "04106 (matricula-online.eu — župnija Podzemelj, mrliška 1857–1885)",
    "okvir": {
        "skeni": "s023–s030 (6 svežih 2×-md5: s023–s028 + 2 carry-iz-P215-md5-križ-1:1: s029/s030!)",
        "pag": "18–25 (pag = sken − 5)",
        "meja_1860_61": "s25 (tail-1860-WRITTEN-53–59 + vsotna-margin-'60' — REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA! + VSOTNA-'1|8'-letnica-marker-4.-INSTANCE + ROKOPISNA-'1861'-GLAVA = 54.-POTRDITEV! + RESTART-z1–z5!)",
        "meja_1861_62": "s30 (tail-1861-z49–z54 + vsotna-'1|8|6|2'-'1862'-MARKER-3.-instance + RESTART-z1–z7-BREZ-rokopisne-glave — P215!)",
        "vrstna_aritmetika": "5+13+14+16+6 = 54 (ŠTEVJE-IZ-VRSTIC-18.×!)",
    },
    "statistika": {
        "vpisov_1861": len(entries),
        "griblje_vpisov": len(grib),
        "griblje_hise": len(hise_map),
        "griblje_hise_seznam": hise,
        "griblje_hise_ponovitve": {k: v for k, v in hise_map.items() if len(v) > 1},
        "meseci_griblje": dict(meseci_g),
        "meseci_vsi": E["statistika"]["meseci"],
        "otroška_umrljivost": otrostenje,
        "otroci_z": OTROCI_Z,
    },
    "anomalije": [
        {"id": "registerjska-stevilcenjska-napaka-1860", "opis": "★★★ NOV-TIP-ANOMALIJE: REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA-1860! s25-tail-WRITTEN-53–59 + vsotna-margin-'60' (KROP-s25_zap_tight-1:1!) — prejšnja-stran-s24-že-ima-53–66 (KROP-s24_zap-1:1!)! Kronološko-tail = #67–#73 — duhovnik-pisal-53–59! (1.-takšna-napaka-v-knjigi!)"},
        {"id": "vsotna-letnica-marker-4-instance", "opis": "★★★ VSOTNA-VRSTA = LETNICA-MARKER-4.-INSTANCE: s25-'1|8|...|1'='1861' (KROP-levo-'1|8'!) + ROKOPISNA-'1861'-GLAVA-pod-njo (arb_s25_glava-KROP: 'jasno-berljiva'!) — OBOJE-cf.-s35-pattern! = 54.-POTRDITEV-invariante! (cf. s30-'1862' + s35-'1863' + s39-'1864'!)"},
        {"id": "vlm-margin-misreadi-1860", "opis": "★★★ VLM-MARGIN-MISREADI-1860-KOREKCIJE: s23-'41–53'[VLM]→'40–52'[KROP — +1-pomik!] + s24-'53–66'[VLM-ČISTO-KROP-1:1!] + s25-tail-'53–59'[VLM-ČISTO-KROP-1:1! + vsotna-'60'!] + z53-1860-mesec-'September'[VLM]→'avgust-nadaljevanje'[KROP — September-glava-šele-pri-z54!] — datum-anomalija-rešena-kronološko-ČISTO!"},
        {"id": "s27-s26-double-scan", "opis": "★★★ s27 = s26 DOUBLE-SCAN (3.-v-knjigi: cf.-s53/s54-P211 + s32=s33-P215!) — 2×-NEODVISNA-VLM-branja-z6–z18 (s26-PRIMARY-čista + s27-delno-obscured!) — duel-rešitve: z6-vas-'Ohljuka'[s26]-vs-'Griblje[?]'[s27!] + z11-ime-'Marko'[s26]-vs-'Mariša/Marša'[s27]!"},
        {"id": "z20-vas-korekcija", "opis": "★★★ z20-VAS-KOREKCIJA: VLM-'Griblje'-NAPAČNO → KROP-'Zemelj' (Z-forma-jasna-vs-G-forma-komparacija-z61/z65-tail!) — Johanna-Muc-Zemelj-h24-2J (MUC-nit-cf.-1862-×4!) — GRIBLJE-ŠTEVJE-BREZ-tega-vpisa!"},
        {"id": "z18-mesec-korekcija", "opis": "★★★ z18-MESEC-KOREKCIJA: VLM-'April-1/3'-×2-NAPAČNO → KROP-'1.-Mai-3.'-jasno! — kronološka-veriga-ČISTA (Apr-23/24→Mai-1/3→Mai-4!) — ne-anomalija-več! (cf. P213-z85-pravi-out-of-order!)"},
        {"id": "h42-klaster-druzina", "opis": "★★★ h42-×3-APR-KLASTER (z14+z15+z17: Apr-19/21 + 20/21 + 23/24 — 6-dnih!) — PERDIU/PEZDIRC[?]-družina-HIPEZOZA (ime-GARBLE-X-open: 'Perdiu[?]'-vs-'Kerdivc[?]'-'Peždinc'-vizualno! starš+2-otroci-2J+5-tednov-v-6-dnih!) — cf.-HUSIČ-h37-1865 + ŽELKO-h1-1864!"},
        {"id": "pezdirc-mreza-1860-1865", "opis": "★★★ PEZDIRC-MREŽA-×5-ČEZ-6-LET: 1860-tail-z65-'Mathias[~Martin?]-Pezdirc[?]-Griblje-h30[~40!]-34J[~54!]' (X-open!) + 1861-h42-×3 (ime-garble-'Peždinc[?]'!) + 1862-z1-Andreas-'von-Griblje[?]'-Podzemelj-h10 + 1864-z18-Michael-h14 + 1864-z85-Anna-h11 + 1865-z41-Mathias-unehelich-h14!"},
        {"id": "valentin-×2-h57-1860-tail", "opis": "★★★ VALENTIN-×2-h57-GRIBLJE-1860-tail (written-55 + 56!): Dez-10/12-Valentin-54J + Dez-10/13-'Griblje-Prist-57'-Valentin-Struna[?]-37J — 2-osebi-ista-hiša-v-2-dnih (oče-sin-hipezoza?) + 'Prist[?]-lokalna-oznaka-X-open!'"},
        {"id": "z11-ime-4-branja", "opis": "★★★ z11-IME-4-BRANJA-DUEL-X-open: 'Marko'[s26-VLM]-vs-'Mariša/Marša'[s27-VLM]-vs-'Markus'[vizualno]-vs-'Martha[~Utrich]'[KROP] — SPOL-X-open! (Kurrent-M-zmeda!) — URIH-priimek-ČISTO-4×! — URIH-h68-NOVA (cf. P212-'URIH-ne-Urik'-1865!)"},
        {"id": "z32-starost-trajni-duel", "opis": "★★★ z32-TRAJNI-DUEL-X-open: starost-'15-J'[VLM+vizualno]-vs-'65-J'[KROP-PAS]-vs-'1-J'[KROP-grib]! (Katharina-Klobučar[~Hlobučar]-h48-NOVA-'¼-Güblerkind')"},
        {"id": "z54-pozek-nit", "opis": "★★★ z54-POŽEK-h67-NIT-ZADNJI-1861-VNOS: Mathias-Požek-2J-Krämpfe-Dez-16/18-h67[~69-VLM-DUEL!-γ-forma-KROP!] → 1865-P212-z36-Mathias-36J-ISTO-HIŠA-h67 (oče-sin-hipezoza-X-open!) + h67-9.-hiša-1861!"},
    ],
    "hišne_kontinuitete": [
        "★★★ ŽELKO-h1-NIT-4.-LETO (1861-z7-[Grozj?-TRI-branja-DUEL!]-47J-Wassersucht → 1862-z41-Maria-½J → 1864-z30/z35-×2!)",
        "★★★ ŠIMEC-h18-NIT-GLOBLJE (1861-z35-Anna-Goric-1½J → 1863-z26-Georg-Simic-h18 → 1864-z34-Peter!) + hisna-duel-18/19",
        "★★★ PEZDIRC-h14-NIT (1861-z44-Anna-Hrance[?]-3J → 1864-z18-Michael + 1865-z41!) + hisna-duel-14/44",
        "★★★ POŽEK-h67-NIT-4-LETA (1861-z54-Mathias-2J → 1865-z36-Mathias-36J!)",
        "★★★ URIH-h68-NOVA (z11-Markus[?]-46J — cf. P212-1865-URIH!) + MALEŠIČ-h26-NOVA (z30-Mathias-59J-Abzehrung-3×!) + KLOBUČAR-h48-NOVA (z32-Katharina-15J[?]-TRAJNI-DUEL!)",
        "★★★ h42-×3-APR-KLASTER (družina-hipoteza!) — NOVA-HIŠA-h42 (korpus-98→99-X-open!)",
        "★★★ KUNE-h10-nit-soseda (h9-KRIŽAN-1862-ni-v-1861 — h1/h42/h67-že-znane!)",
        "★ TAIL-1860-GRIBLJE-×4 (z61-Inocenz[~Lukas!]-Brenc-h24-23J + z65-Mathias[?]-Pezdirc[?]-h30[~40!]-34J[~54!] + Valentin-×2-h57-written-55/56!)",
    ],
    "crossChecks": [
        "2×-NEODVISNA-PRENOSA-8/8-md5 (s023–s028-fresh + s029/s030-carry-iz-/tmp/p215-md5-križ-1:1 — veriga-P215-13.×!)",
        "s27-vs-s26-double-scan-križ: z6–z18-2×-NEODVISNA-VLM (13/13-vrstic-ordinali-1:1! — duel-neskladja-dokumentirana: z6-vas + z11-ime!)",
        "zaporedna-chain-1:1-čez-5-skenov-1861: s25-restart-1–5 → s26/s27-6–18 → s28-19–32 → s29-33–48 → s30-tail-49–54 (ordinali-ČISTO-10.-leto!)",
        "zap-DOKAZI-×3-KROP (s23-'40–52' + s24-'53–66' + s25-'53–59'+'60' — REGISTERJSKA-NAPAKA-DOKAZANA-1:1! + s23-VLM-misread-+1-pomik-korekcija!)",
        "vsotna-'1|8'-KROP + rokopisna-'1861'-glava-KROP (54.-POTRDITEV-invariante — OBOJE!)",
        "z53-1860-mesec-DOKAZ (KROP-s24: avgust-nadaljevanje-brez-glave — September-šele-z54! — datum-kronologija-ČISTA!)",
        "VIZUALNA-verifikacija-skenov-s23–s30 (direktni-vpogled: pozicije + margini + G-forma-komparacija-z61/z65-vs-z20!)",
        "KROP-VIZUALNE-ADJUDIKACIJE-×13-skupin (z1 + z7 + z11 + z14 + z15 + z17 + z18 + z20 + z30 + z32 + z54 + z61 + z65-full-row/pas + 3-zap-stolpci + 2-arb!)",
        "vrstna-aritmetika-5+13+14+16+6 = 54-EXAKT (ordinali-1–54-ČISTO-10.-leto!)",
    ],
    "honesty": [
        "z7-ime-TRI-branja-DUEL-X-open ('Jurkič'/'Franc'/'Šumič-Gunkiè'!) + stan-duel-¼/½ + datum-duel-13/15 + bolezen-duel-Wassersucht/Magenkrank[?]",
        "z11-ime-4-BRANJA-DUEL-X-open (Marko/Mariša/Markus/Martha — SPOL-X-open!) + bolezen-duel-Lungenentzündung/Lungensucht",
        "z14-ime-GARBLE-X-open (Perdiu[?]/Kerdivc[?]/Peždinc!) + starost-TRI-DUEL (45/4½/7½) + stan-garble",
        "z15-ime-DUEL (Anžal/Miklav[?] + priimek-garble!) + bolezen-'Steckfluß[?]'",
        "z17-ime-GARBLE (Marija[?]-4-branja!) + bolezen-GARBLE ('Vifal'šfn[?]')",
        "z18-starost-TRI-DUEL (42/12/1½) + bolezen-'Zopfkrämpfe[?]'",
        "z20-vas-KOREKCIJA (VLM-napaka!) + starost-DUEL (2-J/48-J[?]/2-Tage[?]!) + ime-duel-Johanna-Muc[?]",
        "z30-starost-DUEL (59/54/57) + stan-duel-Ablöser/Ackerer[?]",
        "z32-starost-TRAJNI-DUEL (15/65/1!) + bolezen-duel-Abzehrung/Bräbsfloss[?]",
        "z35-hisna-DUEL (18/19!) + ime-garble-Goric/Goričan[?]",
        "z44-hisna-DUEL (14/44!) + ime-garble-Hrance[?]",
        "z54-hisna-DUEL (67/69!) + starost-duel-2-J/2-J-1-M[?] + bolezen-garble-Gnaifan/Kreuzfluß",
        "z1-restart-DUELI (hisna-34/54/56 + starost-25/65 + ime-Kampšar/Stampehar/Stumpehar!)",
        "z61-ime-DUEL (Inocenz/Lukas + Brenc/Brinar!) + starost-DUEL (23/1½[?]) + datum-duel-10/11",
        "z65-ime-DUEL-X-open (Mathias/Martin + Pezdirc[?]/Poschirc/Pestirne!) + hisna-DUEL (30/40!) + starost-DUEL (34/54!) + bolezen-2-vrstični-GARBLE",
        "VLM-margin-misreadi-dokumentirani (s23-+1-pomik + s24-čisto + s25-tail-čisto + z53-mesec!)",
    ],
    "kaskada": {
        "vitals": "1590 → 1600 (+7 blokov 1861)",
        "04106": "371 → 381",
        "yearset": "+1861 (04106-predzgodovina-25/29!)",
        "meja_1860_61": "s25-tail-WRITTEN-53–59 + vsotna-'60'-REGISTERJSKA-NAPAKA + vsotna-'1861'-marker + '1861'-rokopisna-glava (54.-POTRDITEV!) + restart-z1",
    },
    "lead": {"P217": "1860 — s23/s24/s25-tail-ŽE-VLM (z40–z66 + WRITTEN-53–59: 34-vrstic-1860! glava-'1860'-×2-KROP!) → probe-s017–s023!"},
    "entries_count": len(entries),
    "griblje_count": len(grib),
    "notes": "P216 = 8-skenov-faza (s023–s030; 6-svežih-2×-md5 + 2-carry-P215). MEJA-'1861'-54.-POTRDITEV (vsotna-'1|8'-marker + rokopisna-'1861'-glava-OBOJE!) + ★★★ NOV-TIP: REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA (s25-tail-written-53–59-'60'-vs-s24-53–66 — kronološko-#67–#73!) + s27=s26-DOUBLE-SCAN-3.-v-knjigi + VLM-margin-misreadi-korekcije (s23-+1 + z53-mesec-avgust!) + z20-vas-korekcija (Zemelj!) + z18-mesec-korekcija (Mai!) + h42-×3-APR-KLASTER (družina!) + PEZDIRC-mreža-×5-1860–1865 + VALENTIN-×2-h57-tail + ŽELKO-h1-nit-4.-leto + ŠIMEC-h18-nit + POŽEK-h67-nit + URIH-h68/MALEŠIČ-h26/KLOBUČAR-h48-NOVE. 10-GRIBLJE / 8-hiš (h42 ×3!). KORPUS-98→99-hiš-X-open.",
    "entries": entries,
    "griblje_entries": grib,
    "tail_1860": {"vir": "s23-z40–z52 (13, 0-GRIBLJE!) + s24-z53–z66 (14, 2-GRIBLJE: z61-h24 + z65-h30[PEZDIRC?]) + s25-tail-WRITTEN-53–59 (7, 2-GRIBLJE: Valentin-×2-h57!) — KROP-zap-×3-DOKAZI!",
                  "vrstice_1860_tail": "s23-z40–z52 (July-20→Aug-18/19; 0-GRIBLJE!) + s24-z53–z66 (Aug-27→Nov-13/15; ★ z61-Inocenz-Brenc-h24-23J + z65-Mathias[?]-Pezdirc[?]-h30[~40!]-34J[~54!]!) + s25-tail-WRITTEN-53–59 (Nov-20→Dez-29; ★★ Valentin-×2-h57-54J+37J-Dez-10/12+10/13!) — REGISTERJSKA-NAPAKA: written-53–59 = kronološko-#67–#73!",
                  "stevilo": 34},
    "meja_1861": "s25: tail-1860 (WRITTEN-53–59 + vsotna-'60'-NAPAKA!) + vsotna-'1|8|...|1' = LETNICA-MARKER-'1861' (4.-instance!) + ROKOPISNA-'1861'-GLAVA (54.-POTRDITEV!) + RESTART-z1 (Gradac-h54[~56!]-Jožef-Stampehar[~Kampšar!]-25[~65!]J-Jän-21/23!)",
}

json.dump(proof, open(f"{TMP}/proof_1861.json", "w"), ensure_ascii=False, indent=1)
import shutil
shutil.copy(f"{TMP}/proof_1861.json", "/home/z/my-project/research/issue17/parish-death-1861-04106.json")
print(f"dokaz: {proof['entries_count']} entries / {proof['griblje_count']} griblje / {proof['statistika']['griblje_hise']} hiš")
print("otroška:", otrostenje)
print("meseci-griblje:", dict(meseci_g))
