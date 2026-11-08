#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P217 — dokaz parish-death-1860-04106.json (73 entries: 9-Griblje + 64-druge!)."""
import json
from collections import defaultdict

TMP = "/tmp/p217"
E = json.load(open(f"{TMP}/entries_1860.json"))
entries = E["entries"]
grib = E["griblje_entries"]

hise = sorted({e.get("hisna") for e in grib}, key=lambda x: int(x))
hise_map = defaultdict(list)
for e in grib:
    hise_map[e.get("hisna")].append(e["z"])

# otroci Griblje 1860: z27 (8-mes) = 1
OTROCI_Z = [27]
otrostenje = f"{len(OTROCI_Z)}/{len(grib)} = {round(100*len(OTROCI_Z)/len(grib))}%"

meseci_g = defaultdict(int)
for e in grib:
    m = str(e.get("mesec", "")).split()[0]
    meseci_g[{"Januar": "J", "Februar": "F", "Mai": "M", "Maj": "M", "Oktober": "O", "November": "N", "December": "D"}.get(m, m)] += 1

proof = {
    "faza": "P217",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1860 = 26/29 (issue #18)",
    "knjiga": "04106 (matricula-online.eu — župnija Podzemelj, mrliška 1857–1885)",
    "okvir": {
        "skeni": "s017–s025 (6 svežih 2×-md5: s017–s022 + carry-iz-P216-md5-križ-1:1: s023! + P216-VLM-s23/s24 + P215-VLM-s25-tail!)",
        "pag": "12–20 (pag = sken − 5)",
        "meja_1859_60": "s20 ('1860'-rokopisna-glava-KROP-POTRJENA — arb_s20_glava: '1860-je-pravilna...ni-1800'! — VLM-'1800'-misread-KOREKCIJA-dokumentirana! + RESTART-z1–z13-BREZ-taila — tail-1859-še-3-strani-s17–s19!) = 55.-POTRDITEV-invariante!",
        "meja_1860_61": "s25 (tail-WRITTEN-53–59 + vsotna-'60'-REGISTERJSKA-NAPAKA + vsotna-'1861'-marker-4.-instance + '1861'-rokopisna-glava = 54.-POTRDITEV — P216!)",
        "vrstna_aritmetika": "13+13+13+13+14+7 = 73 (kronološko-z1–z73!; WRITTEN-duplikat-53–59-dokumentiran — REGISTERJSKA-NAPAKA-P216!)",
    },
    "statistika": {
        "vpisov_1860": len(entries),
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
        {"id": "vlm-letnica-misread-1800", "opis": "★★★ VLM-LETNICA-MISREAD-KOREKCIJA: s20-glava-'1800'[VLM]→'1860'[KROP-POTRJENA! — arb_s20_glava: 'druga-cifra-ima-gornji-podaljšek-to-je-kurrentsko-6-ne-0'!] = 55.-POTRDITEV-invariante! (cf. s30-'1858'-hallucination-P215!)"},
        {"id": "registerjska-napaka-1860", "opis": "★★★ REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA-1860 (P216-dokazana!): s25-tail-WRITTEN-53–59 + vsotna-'60' — kronološko-#67–#73 (s24-že-53–66!) — ordinali-1860-NI-ČISTO (1.-leto-z-registrsko-napako! — ŠTEVJE-IZ-VRSTIC-še-vedno-EXAKT-73!)"},
        {"id": "vlm-margin-misreadi-1860", "opis": "★★★ VLM-MARGIN-MISREADI-KOREKCIJE: s18-'90–101'→'80–91' (+10-tens-8/9-duel-KROP-s18_zap-'PRAVILNE-SO-80–91'!) + s22-r1-'23'→'27' (KROP-s22_zap-'27-pravilna'!) + z53-mesec-'September'→'avgust-nadaljevanje' (KROP-P216 — September-glava-šele-z54!) — kronološka-veriga-ČISTA!"},
        {"id": "z27-eksplicitna-letnica", "opis": "★★★ z27-'16.-Mai-1860'-EKSPLICITNA-LETNICA-v-vpisu (KROP: smrt-'16.-Mai-1860'!) — sredino-letnika-vpis! (cf. ULEDBA-pattern-'31.-Dec-1863'-'2.-Jän-1864' — ampak-tu-BREZ-meje! — pisarjeva-previdnost-po-REGISTERJSKI-NAPAKI-hipoteza?)"}
        ,
        {"id": "z27-pozek-h58-nit", "opis": "★★★ z27-POŽEK-h58-NIT-1860: Barbara[~Bartholomä!-DUEL-X-open!]-Požek[~Pöckl!]-8-mesecev-Mai-16/18! — cf. P211-z90-h58-POŽEK + P192-h58! (POŽEK-mreža: h58-1860-otrok + h67-1861/1865-Mathias-×2!)"},
        {"id": "z24-ime-tri-garble", "opis": "★★★ z24-IME-TRI-GARBLE-X-open: 'Matija?-Petine?'[VLM]-vs-'Peter-[Mautknecht?]'[KROP-z23-opomba]-vs-'Rosalia-Pedire[~]'[KROP2-opomba] — SPOL-X-open! + hisna-DUEL-50[2×]-vs-30[1×] + starost-DUEL-64[2×]-vs-68[1×]!"},
        {"id": "valentin-×2-h57", "opis": "★★★ VALENTIN-×2-h57-GRIBLJE (z69-written-55-Dez-10/12-54J + z70-written-56-'Prist-57'-Dez-10/13-37J!) — 2-osebi-ista-hiša-v-2-dnih (oče-sin-hipoteza?) + 'Prist[?]'-lokalna-oznaka-X-open!"},
        {"id": "z7-z13-starost-dueli", "opis": "★★★ z7-starost-TRI-DUEL-X-open (27[VLM]-vs-87[KROP]-vs-37[PAS]! — Miklavž[~Anništ?]-Simčič-h55!) + z13-starost-TRI-DUEL-X-open (46-let[VLM]-vs-1-J-1-M[?KROP]-vs-14-J[?PAS]! — Josip-Jakofčič[~Jakobčič]-h6!)"},
        {"id": "pezdirc-mreza-1860", "opis": "★★★ PEZDIRC-MREŽA-1860: z65-'Mathias[~Martin?]-Pezdirc[?]-Griblje-h30[~40!]-34J[~54!]' (X-open-TRI-DUEL-ime!) + TAIL-1859-×2: z73-'Elizabeta-Pardire[~Pezdirceva?]-vs-'Klara-Podire'[KROP]-h20[~10!]-23J' + z81-'Andreas[~Johann!]-Pesdire[~Pestiric!]-Griblje-52-99J[~83!]-TRAJNI-DUEL!' — PEZDIRC-niti-globlje-v-1859/60!"},
        {"id": "tail-1859-45-vrstic", "opis": "TAIL-1859 (kontekst!): s17-z68–z79 (12) + s18-z80–z91 (12 — KROP-'80–91'!) + s19-z92–z112 (11 — VLM-margin-ČISTO!) = 45-vrstic (Sept-16 → Dez-27/29! glava-'1859'-×3!) — GRIBLJE-tail-×6: z73-h20[~10!]-Pardire[?]/Podire[?] + z76-h24[~]-Miklik + z81-h52-Pesdire[?] + z86-h21-Požek-Anastasia-69J + z95-h49-Petek + z100-h65-Brino-Valentin! (1859-NI-bran-v-celoti — P218-LEAD!)"},
    ],
    "hišne_kontinuitete": [
        "★★★ POŽEK-MREŽA-2-HIŠI (h58-1860-z27-Barbara[?]-8-mes + h67-1861-z54-Mathias-2J + h67-1865-z36-Mathias-36J + h58-P211/P192!)",
        "★★★ PEZDIRC-MREŽA-×7-1859–1865 (1859-tail-z73[?]-Pardire + z81[?]-Pesdire-99J[~83!] + 1860-z65-h30[?] + 1861-h42-×3[?] + 1862-z1 + 1864-×2 + 1865-z41!)",
        "★★★ VALENTIN-×2-h57-1860 (z69+z70 — oče-sin-hipoteza!) — h57-NOVA (korpus-99→100-X-open!)",
        "★★★ NOVE-HIŠE-1860: h55 (Simčič) + h6 (Jakofčič) + h13 (Jakošec) + h50 (Petine[?]-X-open) + h58-POŽEK-že-znana + h24 (Brenc) + h30 (Pezdirc[?]) + h57 ×2 (Valentin-×2) — 8-hiš!",
        "★ KRIŽAN-h9-nit (1862-z4 — ni-v-1860!) + KUNE-h10-nit (1862/63 — ni-v-1860!) — Griblje-hiše-1860-VSE-NOVE-ali-X-open!",
    ],
    "crossChecks": [
        "2×-NEODVISNA-PRENOSA-7/7-md5 (s017–s022-fresh + s023-carry-iz-/tmp/p216-md5-križ-1:1 — veriga-P216-14.×!)",
        "zap-chain-1860: s20-restart-1–13 → s21-14–26 → s22-27–39 (KROP-'27'!) → s23-40–52 (KROP-P216-'40–52'!) → s24-53–66 (KROP-P216-1:1!) → s25-tail-WRITTEN-53–59-#67–#73 (KROP-P216-1:1!) — ŠTEVJE-IZ-VRSTIC-19.×!",
        "1859-tail-križ: s17-z68–z79 → s18-z80–z91 (KROP-'PRAVILNE-SO-80–91'! — VLM-+10-korekcija!) → s19-z92–z112 → s20-restart-z1 (kronološko-ČISTO!)",
        "arb_s20_glava-KROP: '1860'-rokopisna-POTRJENA ('ni-1800'!) = 55.-POTRDITEV!",
        "z27-'16.-Mai-1860'-KROP-eksplicitna-letnica + s22_zap-KROP-('16.-Mai-18.'-Griblje-58!)",
        "VIZUALNA-verifikacija-skenov-s17–s25 (direktni-vpogled: pozicije + margini + glave!)",
        "KROP-VIZUALNE-ADJUDIKACIJE-×9-skupin (z7 + z13 + z23 + z24 + z27 + z61 + z65 + z69 + z70-full-row/pas + 2-zap + 1-arb + 2-tail!)",
        "vrstna-aritmetika-13+13+13+13+14+7 = 73-EXAKT (kronološko-z1–z73!)",
    ],
    "honesty": [
        "z7-ime-DUEL (Miklavž/Anništ[?]) + starost-TRI-DUEL (27/87/37!)",
        "z13-ime-duel (Jakofčič/Jakobčič) + starost-TRI-DUEL (46/1-J-1-M/14!) + bolezen-GARBLE",
        "z23-ime-DUEL-X-open (Andrej-Jakošec/Lunbran-Jakobs!) + bolezen-duel",
        "z24-ime-TRI-GARBLE-X-open (Matija-Petine/Peter-Mautknecht/Rosalia-Pedire — SPOL-X-open!) + hisna-DUEL (50/30) + starost-DUEL (64/68)",
        "z27-ime-DUEL-X-open (Barbara/Bartholomä! + Požek/Pöckl!) + bolezen-GARBLE ('Müeman[?]')",
        "z61-ime-DUEL (Inocenz/Lukas + Brenc/Brinar) + starost-DUEL (23/1½[?])",
        "z65-ime-TRI-DUEL-X-open (Mathias/Martin + Pezdirc/Poschirc/Pestirne!) + hisna-DUEL (30/40) + starost-DUEL (34/54)",
        "z69-ime-X-open (Valentin-priimek-NEBERLJIV!)",
        "z70-ime-X-open (Valentin-Struna[?]) + 'Prist[?]'-oznaka-X-open",
        "z73-tail-ime-DUEL (Elizabeta-Pardire/Klara-Podire!) + hisna-DUEL (20/10!)",
        "z81-tail-ime-DUEL (Andreas/Johann + Pesdire/Pestiric!) + starost-TRAJNI-DUEL (99/83!)",
        "VLM-letnica-misread-s20 ('1800'→'1860'-KROP!) + VLM-margin-misreadi (s18-+10 + s22-r1-'23'→'27' + z53-mesec!)",
    ],
    "kaskada": {
        "vitals": "1600 → 1609 (+9 blokov 1860)",
        "04106": "381 → 390",
        "yearset": "+1860 (04106-predzgodovina-26/29!)",
        "meja_1859_60": "s20-'1860'-rokopisna-glava-KROP (55.-POTRDITEV!) + restart-z1–z13",
    },
    "lead": {"P218": "1859 — s17/s18/s19-ŽE-VLM (z68–z112: 45-vrstic-1859-tail! glava-'1859'-×3!) → probe-s011–s017!"},
    "entries_count": len(entries),
    "griblje_count": len(grib),
    "notes": "P217 = 9-skenov-faza (s017–s025; 6-svežih-2×-md5 + s023-carry-P216 + P216-VLM-s23/s24 + P215-VLM-s25-tail!). MEJA-'1860'-55.-POTRDITEV (rokopisna-glava-KROP-'1860'-POTRJENA — VLM-'1800'-misread-korekcija!) + REGISTERJSKA-NAPAKA-1860 (ordinali-NI-ČISTO — 1.-leto! written-53–59-×2!) + VLM-margin-misreadi-korekcije (s18-+10 + s22-'27' + z53-avgust!) + z27-'16.-Mai-1860'-EKSPLICITNO + POŽEK-h58-nit + VALENTIN-×2-h57 + PEZDIRC-niti-1859/60 + z24-ime-TRI-GARBLE-SPOL-X-open. 9-GRIBLJE / 8-hiš (h57 ×2!). KORPUS-99→100-hiš-X-open.",
    "entries": entries,
    "griblje_entries": grib,
    "tail_1859": {"vir": "s17-z68–z79 (12) + s18-z80–z91 (12 — KROP-'80–91'!) + s19-z92–z112 (11!) — 45-vrstic (Sept-16 → Dez-27/29; glava-'1859'-×3!)",
                  "vrstice_1859_tail": "s17-z68–z79 (★ 2-GRIBLJE: z73-h20[~10!]-Elizabeta-Pardire[~Pezdirceva?]-vs-'Klara-Podire'[KROP]-23J + z76-h24[~]-Paulmann-Miklik-24J!) + s18-z80–z91 (★ 2-GRIBLJE: z81-h52-Andreas[~Johann!]-Pesdire[~Pestiric!]-99J[~83!]-TRAJNI-DUEL + z86-h21-Anastasia-Požek-69J!) + s19-z92–z112 (★ 2-GRIBLJE: z95-h49-Jožef-Petek-16J + z100-h65-Valentin-Brino[~]-58J!)",
                  "stevilo": 45},
    "meja_1860": "s20: '1860'-rokopisna-glava-KROP-POTRJENA (55.-POTRDITEV! — VLM-'1800'-misread-korekcija!) + RESTART-z1 (Gradac-h18-Josip-Mihelic-60J-Jän-4/6!) — BREZ-vsotne-vidne-na-s20 (glava+restart-neposredno!)",
}

json.dump(proof, open(f"{TMP}/proof_1860.json", "w"), ensure_ascii=False, indent=1)
import shutil
shutil.copy(f"{TMP}/proof_1860.json", "/home/z/my-project/research/issue17/parish-death-1860-04106.json")
print(f"dokaz: {proof['entries_count']} entries / {proof['griblje_count']} griblje / {proof['statistika']['griblje_hise']} hiš")
print("otroška:", otrostenje)
print("meseci-griblje:", dict(meseci_g))
