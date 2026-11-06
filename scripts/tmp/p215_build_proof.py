#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P215 — dokaz parish-death-1862-04106.json (60 entries: 9-Griblje + 51-druge!)."""
import json
from collections import defaultdict

TMP = "/tmp/p215"
E = json.load(open(f"{TMP}/entries_1862.json"))
entries = E["entries"]
grib = E["griblje_entries"]

hise = sorted({e.get("hisna") for e in grib}, key=lambda x: int(x))
hise_map = defaultdict(list)
for e in grib:
    hise_map[e.get("hisna")].append(e["z"])

# otroci Griblje 1862: z10 (2J) + z17 (1½J) + z41 (½J) = 3
OTROCI_Z = [10, 17, 41]
otrostenje = f"{len(OTROCI_Z)}/{len(grib)} = {round(100*len(OTROCI_Z)/len(grib))}%"

meseci_g = defaultdict(int)
for e in grib:
    m = str(e.get("mesec", "")).split()[0]
    meseci_g[{"Januar": "J", "März": "M", "April": "A", "September": "S", "October": "O"}.get(m, m)] += 1

proof = {
    "faza": "P215",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1862 = 24/29 (issue #18)",
    "knjiga": "04106 (matricula-online.eu — župnija Podzemelj, mrliška 1857–1885)",
    "okvir": {
        "skeni": "s029–s035 (4 sveža 2×-md5: s029–s032 + 3 carry-iz-P214-md5-križ-1:1: s033–s035!)",
        "pag": "24–30 (pag = sken − 5)",
        "meja_1861_62": "s30 (tail-1861-z49–z54 + VSOTNA-'1|8|6|2'-'1862'-MARKER-3.-INSTANCE + RESTART-z1–z7!; NOVA-VARIANTA: BREZ-rokopisne-'1862'-glave — vsotna=EDINI-letnica-marker (cf. s35-'1863'-glava+vsota-OBOJE!); KROP-zap-stolpec: '1861'-glava-bledo + '49–54'-jasno — VLM-misread-'29–34'-KOREKCIJA!)",
        "meja_1862_63": "s35 (tail-1862-z55–z60 + vsotna-'1|8|6|3'-'1863'-MARKER + RESTART-z1–z8 + '1863'-rokopisna-glava = 52.-POTRDITEV — P214!)",
        "vrstna_aritmetika": "7+16+16+15+6 = 60 (ŠTEVJE-IZ-VRSTIC-17.×!)",
    },
    "statistika": {
        "vpisov_1862": len(entries),
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
        {"id": "vsotna-letnica-marker-3-instance", "opis": "★★★ VSOTNA-VRSTA = LETNICA-MARKER-3.-INSTANCE: s30-'1|8|6|2'='1862' (KROP-levo-'1|8' + KROP-desno-'6|2' — 2-izreza-1:1!) + ★★★ NOVA-VARIANTA: s30-RESTART-BREZ-rokopisne-'1862'-glave (arb_s30_glava-KROP: 'rokopisna-letnica-NE-vidna') — vsotna=EDINI-marker! (cf. s35-'1863' + s39-'1864'-markeri!)",
         "s30_zap_stolpec": "s30-zap-stolpec-KROP: glava-'1861'-bledo-nad-November + številke-'49–54'-jasne (50/52/53/54-eksplicitno!) — VLM-misread-'29–34'-DOKUMENTIRAN-KOREKCIJA (Kurrent-2/5-margin-duel!)"},
        {"id": "s32-s33-double-scan", "opis": "★★★ s32 = s33 DOUBLE-SCAN (2.-v-knjigi: cf.-s53/s54-P211!) — ISTA-registrska-stran-2-foto-seji! 2×-NEODVISNA-VLM-branja-z24–z39 (s32-sveža-ČISTEJŠA + s33-P214-obscured!) — duel-rešitve: z28-vas-'Otok-2'[s32]-vs-'zakrito'[s33] + z29-starost-'74-J'[s32]-vs-'51-J'[s33] + z31-'13-J'-vs-'43-J' + z38-'Dančar'-vs-'Mancar' + z39-vas-'Begunja-vas'[s32]-vs-'Boginja-vas'[s33]!"},
        {"id": "filak-mreza-1862", "opis": "★★★ FILAK-MREŽA-×3-v-1862: z11-Katharina-Filak-h61-34J (DUEL-'Kolak'-full-vs-'Tilak'-vizualno-vs-'Filak'-KROP — F/T/K-rešen-z-z14-korelacijo!) + z14-Nicolaus-Filak-h5-10J-'...Kind-von-ANNA-Filak' (opomba-2-vrstično-garble — unehelich/verwaiset-X-open!) + ANNA-FILAK (mati-opomba!) → FILAK-h34-1864/65/66 (P213-z33-Mathias-63J + P211-z48-Katarina + z80-Josip!) + ★★★ KATARINA-FILAK-age-match: 1862-34J → 1866-38J-MOŽNO-ISTA-OSEBA (h61-vs-h34-sprememba-možna — HIPEZOZA-X-open!)"},
        {"id": "kune-h10-nit", "opis": "★★★ KUNE-h10-NIT: z10-1862-'Simon-Kure'-h10-2J ('¼-Güblerssohn') → 1863-z2-'Joannes-Kune'-h10-34J (X-open-4-branja-'Kumre/Kime/Kure') — 1862-'Kure'-reading-PODPORA-za-Kune (5.-branja!) + ime-DUEL-X-open: full-'Simon'-vs-krop-'Maria/Vinanz-Ehefrau[?]'!"},
        {"id": "z1-pezdirc-restart", "opis": "★★★ z1-RESTART-1862-PEZDIRC-NIT: Andreas-Pezdirc-36J-'¼-Güblerssohn'-Podzemelj-h10-'von-Griblje[?]-KROP' — Lungenentzündung-Jän-6/8 — cf. 1864-z18-Michael-Pezdirc-h14-¼-Güblers-Kind + 1864-z85-Anna-Pezdirc-h11 + 1865-z41-Mathias-Pezdirc-unehelich-h14! (PEZDIRC-mreža-globlje-v-1862!)"},
        {"id": "z48-prazni-stolpci", "opis": "★★★ z48-ANOMALIJA-PRAZNI-STOLPCI: starost-'—' + bolezen-'—' (Mathias-Jerlicar[~Seliscar?-J/S-duel]-h61-'Müllerssohn[?]'-2-vrstični-garble!) — duel-krop-starost-'1-J[?]' — cf. doctor-house-pattern ('—'-obrazec!) + ★★★ h61-2.-INSTANCE-v-1-LETU (z11-März + z48-Okt!)"},
        {"id": "z30-pokop-brez-smrti", "opis": "★★★ z30-ANOMALIJA: pokop-'26.'-BREZ-smrti-datuma ('—') + ime-garble-'Mrtvogrobnik[~Mörtvogrobnik=grobar?/Mrtvorojenček?]-David[?]-Joh.-Marxin[?]'-X-open (Gradac-h9; s32-ČISTEJŠA-foto-vs-s33-obscured!)"},
        {"id": "z43-typhus-tri-branja", "opis": "★★★ z43-Typhus-TRI-branja-1:1 (KROP+PAS+FULL — izjemno-skladje!) — Thomas-Potočar-h63-28J + ★★★ KRIŽAN-h63-NIT-2-LETI: 1862-z43-Thomas-Potočar → 1864-z63-'?ollganerischb'-Kind-von-Johann-Križan-h63! + h63-duel-krop-'68'-vs-'63'-2×"},
        {"id": "z41-zuckfall-duel", "opis": "★★★ z41-ŽELKO-h1-NIT-3.-LETO-GLOBOKO: Maria-Zeljko[~Šeljko-Ž/Z-duel]-½J-'¼-Güblerskind'-Griblje-h1 → 1864-z30-Anna-22J + z35-Peter-1J (h1-×2!) + bolezen-'Zuckfall[~Kaßfall/Unfall-duel]' — cf.-1863-z39/z40-KRIŽAN-'Zaugfall≈Zuckfall'-×2!"},
        {"id": "z17-bolezen-duel", "opis": "★★★ z17-bolezen-DUEL-X-open: 'Lungensucht'[KROP]-vs-'Masern'[PAS-'ošpice!'] — MEASLES-EPIDEMIJA-HIPOTEZA? (Anna-Skobucar[~Hlobucar-S/H-duel]-h47-1½J-'¼-Gütlerskind') + h47-NOVA-hiša (duel-krop-'17'-vs-'47'-2×)"},
        {"id": "z50-starost-duel", "opis": "★★★ z50-TRAJNI-DUEL-X-open: starost-'61-J[?]-vs-6-tednov[?]-vs-1[?]' (Joseph-Graucek[TRI-branja-DUEL: 'Strucelj'-KROP-vs-'Gartner[?]'-full-vs-'Štraucelj'-vizualno — G/S/K-cf.-1863-z27-STRAUS-K/G/S!]-h5-½-Gübler-Abzehrung) + ★★★ h5-2.-INSTANCE-v-1-LETU (z14-Apr + z50-Okt!)"},
        {"id": "z54-pozek-tail-1861", "opis": "★★★ TAIL-1861-GRIBLJE: z54-Mathias-POŽEK-h67-2J-Krämpfe-Dez-16/18 (h69[full-VLM]-vs-h67[KROP-γ-forma!]-duel!) — ★★★ POŽEK-h67-NIT-4-LETA-GLOBOKO: 1861-z54-Mathias-2J → 1865-P212-z36-Mathias-36J-ISTO-HIŠA-h67 (oče-sin-hipezoza-X-open!) + TAIL-GRIBLJE-×2-s29: z35-Anna-Goric[~]-h18[~19]-1½J + z44-Anna-Hrance[?]-h14[~44]-3J (h18=ŠIMEC! + h14=PEZDIRC! — niti-globlje!)"},
    ],
    "hišne_kontinuitete": [
        "★★★ FILAK-MREŽA-×3-1862 (h61-Katharina-34J + h5-Nicolaus-10J-'Kind-von-Anna' + ANNA!) → h34-1864/65/66 (Mathias-63J + Katarina + Josip!) — KATARINA-age-match-1862/1866-X-open!",
        "★★★ KUNE-h10-NIT (1862-z10-'Simon-Kure'-2J → 1863-z2-'Joannes-Kune'-34J — 5.-branja-'Kure'-podpora-X-open-duelu!)",
        "★★★ ŽELKO-h1-NIT (1862-z41-Maria-½J → 1864-z30-Anna-22J + z35-Peter-1J — 3.-leto-globoko!)",
        "★★★ KRIŽAN-h63-NIT (1862-z43-Thomas-Potočar-28J-Typhus → 1864-z63-Kind-von-Johann-Križan!) + KRIŽAN-h9-NOVA (z4-Markus/Mathias-72J-Marasmus-senilis — soseda-h10-KUNE!)",
        "★★★ POŽEK-h67-NIT-4-LETA (1861-tail-z54-Mathias-2J → 1865-z36-Mathias-36J-ISTO-HIŠA — oče-sin-X-open!)",
        "★★★ PEZDIRC-MREŽA (1862-z1-Andreas-36J-Podzemelj-h10-'von-Griblje[?]' → 1864-z18/z85 + 1865-z41!)",
        "★ DOCTOR-HOUSE-Gradac-h60 (1862-tail-z57-Magistr.Amts-Dien-Doct-Franz-Marentič → 1863-z61!)",
        "★ TAIL-1861-GRIBLJE-h14/h18-niti (z35-Anna-Goric-h18[ŠIMEC!] + z44-Anna-Hrance-h14[PEZDIRC!])",
        "★★★ NOVE-HIŠE-1862: h9 (Križan) + h47 (Skobucar) + h63 (Potočar/Križan-nit) + h61 (Filak) + h5-2× (Filak/Graucek) — korpus-93→98-GRIBLJE-hiš-X-open!",
    ],
    "crossChecks": [
        "2×-NEODVISNA-PRENOSA-7/7-md5 (s029–s032-fresh + s033–s035-carry-iz-/tmp/p214-md5-križ-1:1 — veriga-P214-12.×!)",
        "s32-vs-s33-double-scan-križ: z24–z39-2×-NEODVISNA-VLM (16/16-vrstic-ordinali-1:1! — duel-neskladja-dokumentirana: z28/z29/z31/z38/z39!)",
        "zaporedna-chain-1:1-čez-5-skenov: s30-restart-1–7 → s31-8–23 → s32/s33-24–39 → s34-40–54 (robna-'410–424'-prefixacija-ignorirana!) → s35-tail-55–60 (ordinali-ČISTO-9.-leto!)",
        "s30-zap-stolpec-KROP: glava-'1861' + '49–54'-POTRJENO ('VLM-misread-29–34'-korekcija-dokumentirana!)",
        "vsotna-'1|8|6|2'-KROP-×2 (levo-'1|8' + desno-'6|2') — 3.-instance-invariante-1:1!",
        "VIZUALNA-verifikacija-skenov-s29–s35 (direktni-vpogled: pozicije-vrstic + margin-številke + vsotna-glava!)",
        "KROP-VIZUALNE-ADJUDIKACIJE-×11-skupin (z1-PEZDIRC + z4 + z10 + z11 + z14 + z17 + z41 + z43 + z48 + z50-full-row/pas-×2 + z54-tail + z30-s32-anomalija!)",
        "vrstna-aritmetika-7+16+16+15+6 = 60-EXAKT (ordinali-1–60-ČISTO-9.-leto!)",
    ],
    "honesty": [
        "z10-ime-DUEL-X-open ('Simon'-full-vs-'Maria/Vinanz-Ehefrau'-krop!) + stan-DUEL ('¼-Güblerssohn'-vs-'Ehefrau?')",
        "z11-ime-F/T/K-DUEL ('Kolak'/'Tilak'/'Filak' — rešen-FILAK-via-z14 — X-open-honest-dokumentirano!) + starost-duel-34/37",
        "z14-opomba-GARBLE ('...Kind-von-Anna-Filak' — unehelich/verwaiset-X-open!) + bolezen-GARBLE (Zufallfluß[?]/Zopfkrankheit[?]) + h5-duel-krop-'3'",
        "z17-bolezen-DUEL ('Lungensucht'-vs-'Masern' — X-open!) + h47-duel (47/17)",
        "z41-ime-Ž/Z-duel ('Zeljko'/'Šeljko') + bolezen-duel (Zuckfall/Kaßfall/Unfall)",
        "z43-stan-2-vrstični-GARBLE (Ehemann-von-Agnes[?]/Amts...) + h63-duel (63/68)",
        "z48-ime-DUEL-J/S ('Jerlicar'/'Seliscar') + 'Müllerssohn[?]'-garble + starost-duel ('—'/'1-J[?]')",
        "z50-ime-TRI-branja-DUEL ('Graucek'/'Strucelj'/'Gartner[?]') + starost-TRAJNI-DUEL (61-J/6-tednov/1) + mesec-duel-krop-'Xbr'",
        "z4-ime-DUEL ('Markus'-krop-vs-'Mathias'-full) + stan-GARBLE ('Gutsler[~]') + h9-γ/9-duel",
        "z1-stan-'von-Griblje[?]'-KROP-dodatelj (X-open!) + z54-h69-vs-h67-DUEL + z30-ime-GARBLE-'Mrtvogrobnik[?]'",
        "s30-vsotna-cifra-2-DUEL ('8'-hipezoza-via-chain-vs-'2/9'-VLM-morda — KROP-'1|8'-levo-'6|2'-desno-chain-zaključek-'1862'!)",
        "VLM-leta-napaka-s30 ('tail-1857-novo-leto-1858'-NAPAČNO — vsotna-KROP-'1862'-KOREKCIJA!) + VLM-zap-misread-s30-tail ('29–34'→'49–54')",
    ],
    "kaskada": {
        "vitals": "1581 → 1590 (+9 blokov 1862)",
        "04106": "362 → 371",
        "yearset": "+1862 (04106-predzgodovina-24/29!)",
        "meja_1861_62": "s30-tail-z49–z54 + vsotna-'1862'-marker (BREZ-rokopisne-glave — NOVA-VARIANTA!) + restart-z1-PEZDIRC",
    },
    "lead": {"P216": "1861 — s29-ŽE-VLM (z33–z48: 16-vrstic-1861! glava-'1861'!) + s30-tail-z49–z54 (6! z54-GRIBLJE-Požek-h67!) → probe-s023–s029!"},
    "entries_count": len(entries),
    "griblje_count": len(grib),
    "notes": "P215 = 7-skenov-faza (s029–s035; 4-sveža-2×-md5 + 3-carry-P214). MEJA-'1862'-3.-instance-vsotna-letnica-marker + NOVA-VARIANTA (BREZ-rokopisne-glave!) + s32=s33-DOUBLE-SCAN-2.-v-knjigi (2×-VLM-z24–z39!) + KROP-zap-stolpec-DOKAZ ('1861'-glava + '49–54' — VLM-misread-korekcija!) + ★★★ FILAK-MREŽA-×3 (Katharina-h61 + Nicolaus-h5-'Kind-von-Anna' + Anna!) + KUNE-h10-nit ('Kure'-5.-branja!) + ŽELKO-h1-nit + KRIŽAN-h63-nit + POŽEK-h67-tail-1861-nit + PEZDIRC-z1-restart + z48-prazni-stolpci + z30-pokop-brez-smrti + z43-Typhus-TRI-branja-1:1. 9-GRIBLJE / 7-hiš (h5+h61-×2!). KORPUS-93→98-hiš-X-open.",
    "entries": entries,
    "griblje_entries": grib,
    "tail_1861": {"vir": "s29-vrste-1–16 (1861-z33–z48 + glava-'1861'!) + s30-vrste-1–6 (1861-tail-z49–z54 — KROP-zap-DOKAZ!)",
                  "vrstice_1861_tail": "s29-z33–z48: 16-vrstic (★ 2-GRIBLJE: z35-Anna-Goric-h18[~19!]-1½J-Aug-15/17 + z44-Anna-Hrance[?]-h14[~44!]-3J-Okt-10/12!) + s30-z49–z54: 6-vrstic (★ z54-GRIBLJE: Mathias-POŽEK-h67[~69!]-2J-Krämpfe-Dez-16/18 — POŽEK-nit!)",
                  "stevilo": 22},
    "meja_1862": "s30: tail-1861 (z49–z54) + vsotna-vrstica-'1|8|6|2' = LETNICA-MARKER-'1862' (3.-instance!) + RESTART-z1 (Andreas-PEZDIRC-36J-Podzemelj-h10-'von-Griblje[?]'-Jänner-6/8!) — BREZ-rokopisne-'1862'-glave (NOVA-VARIANTA — vsotna=edini-marker!)",
}

json.dump(proof, open(f"{TMP}/proof_1862.json", "w"), ensure_ascii=False, indent=1)
import shutil
shutil.copy(f"{TMP}/proof_1862.json", "/home/z/my-project/research/issue17/parish-death-1862-04106.json")
print(f"dokaz: {proof['entries_count']} entries / {proof['griblje_count']} griblje / {proof['statistika']['griblje_hise']} hiš")
print("otroška:", otrostenje)
print("meseci-griblje:", dict(meseci_g))
