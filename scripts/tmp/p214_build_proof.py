#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P214 — dokaz parish-death-1863-04106.json (64 entries: 7-Griblje + 57-druge!)."""
import json
from collections import defaultdict

TMP = "/tmp/p214"
E = json.load(open(f"{TMP}/entries_1863.json"))
entries = E["entries"]
grib = E["griblje_entries"]

hise = sorted({e.get("hisna") for e in grib}, key=lambda x: int(x))
hise_map = defaultdict(list)
for e in grib:
    hise_map[e.get("hisna")].append(e["z"])

# otroci Griblje 1863: z33 (4J4M) + z38 (1½J) = 2
OTROCI_Z = [33, 38]
otrostenje = f"{len(OTROCI_Z)}/{len(grib)} = {round(100*len(OTROCI_Z)/len(grib))}%"

meseci_g = defaultdict(int)
for e in grib:
    m = str(e.get("mesec", "")).split()[0]
    meseci_g[{"Februar": "F", "März": "M", "Mai": "Mai", "Juni": "Juni", "Juli": "Juli"}.get(m, m)] += 1

proof = {
    "faza": "P214",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1863 = 23/29 (issue #18)",
    "knjiga": "04106 (matricula-online.eu — župnija Podzemelj, mrliška 1857–1885)",
    "okvir": {
        "skeni": "s033–s039 (6 svežih 2×-md5 + s39-carry-iz-P213-md5-križ-1:1!)",
        "pag": "28–34 (pag = sken − 5)",
        "meja_1862_63": "s35 (tail-1862-z55–z60 + VSOTNA-'1|8|6|3'-'1863'-MARKER + RESTART-z1–z8!; '1863'-rokopisna-glava-s35 = 52.-POTRDITEV-invariante — arb_s35_glava-KROP!)",
        "meja_1863_64": "s39-tail (z55–z64 = P213-VLM + z64-ULEDBA-#11-EKSPLICITNI-LETNICI-'31.Dec.1863'-'2.Jän.1864' + vsotna-'1|8|6|4'-'1864'-MARKER!)",
        "vrstna_aritmetika": "8+15+15+16+10 = 64 (ŠTEVJE-IZ-VRSTIC-16.×!)",
    },
    "statistika": {
        "vpisov_1863": len(entries),
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
        {"id": "vsotna-letnica-marker", "opis": "★★★ VSOTNA-VRSTA = LETNICA-MARKER-naslednjega-leta (NOV-INVARIANTA-TIP!): s35-'1|8|6|3'='1863' + s39-'1|8|6|4'='1864' — cifre-razpete-čez-stolpce (zap/Land + ime + Alter + Priester)! KROP-s39_vsota_desno: Alter-'6'+Priester-'4'-1:1! — vsotna-NI-vsota-oseb-MARVEČ-letnica!"},
        {"id": "z64-uledba-eksplicitno", "opis": "★★★ ULEDBA-#11-12.-INSTANCE-EKSPLICITNO: z64-smrt-'31.-Dec-1863' + pokop-'2.-Jänner-1864' — OBE-LETNICI-ZAPISANI-V-VPISU (@6×-KROP-z64_datumi_tight!) — čez-mejo-vpis-z-eksplicitnimi-letnicami!"},
        {"id": "z27-hisna-duel-11-71", "opis": "★★★ HISNA-DUEL-NEREŠEN-HONEST: z27-Griblje KROP-tight-'11' ('ozka-črtica-brez-zanke') — ALTERNATIVA-'71' (γ-7-S-PREČKA! isti-γ-glyph-kot-P213-z44-h71!) — STRAUS-h71-KORELACIJA: 1863-z27-'Joannes-Straus' + 1864-z44-'Anna-Strauž[~Straus?]'-h71!"},
        {"id": "z27-ime-straus", "opis": "★★★ IME-TRI-branja-DUEL: 'Kras'[full-page] / 'Graus'[VIZUALNO-s37] / 'Straus'[KROP-tight] — K/G/S-KURRENT-duel — X-open! — če-STRAUS: mreža-z-P213-z44!"},
        {"id": "z38-ime-rosalia", "opis": "★★★ IME-4-branja-DUEL-X-open: 'infant-Rosalia-v.-Joh.-Broznič[?]'[VIZUALNO-s37-2-vrstično!] + 'infant-Rosalia'[KROP-full-row] + 'Josef-Brozik'[full-page — FALSIFICIRANA-SINTEZA-v-Joh.+] + 'Rojč/Jože'[tight-garble] — Rosalia-INFANS-hči-Joh.-Brozič[~Broznik?/Barak?]"},
        {"id": "z2-ime-kune", "opis": "★★★ IME-4-branja-DUEL-X-open: 'Kune'[full-page+VIZUALNO] / 'Kumre'[tight] / 'Kime'[krop] / 'Kure'[krop] — KURRENT-m/n+u/r-zmeda!"},
        {"id": "z12-unehelich", "opis": "★★★ OPOMBA-'unehelich'-KROP-tight-ANMERKUNG-STOLPEC: z12-Johan-Brinc-h65-NEZAKONSKO! — 1.-eksplicitna-'unehelich'-opomba-v-GRIBLJE-korpusu!"},
        {"id": "z53-außerehelich-formula", "opis": "★★★ FORMULA-DOKAZ-za-P213-z6-garble: z53-s38-'außereheliches-Kind-von-Mathias-Klepec-in-Gübler' — jasen-'außereheliches-Kind-von'-vpis → P213-z6-'?ollganerischb-Kind-von'-hipezoza-PODPRTA (cf. z80/z84-'Mastgutlinstleht-Kind-von')!"},
        {"id": "z54-filak-novorojenček", "opis": "★★★ FILAK-NIT: z54-s38-'Neugebohrenes-Kind-des-Mathias-Filak'-Grem-h33 + z59-s39-'Maria-Filak-5-J'-Grem-h33-ISTO-HIŠO-v-3-tednih! + duel: full-page-'otrok-Anny-in-Mathias'-vs-VIZUALNO-'Kind-des-Mathias-Filak'"},
        {"id": "z61-marentič-doctor", "opis": "★ DOCTOR-HOUSE-NIT: z61-'Magistrats-Amts-Diener-v.-Franz-Marentič-(Doct.)'-Gradac-h60 — ISTA-HIŠA-kot-1862-z57-s35-'Magistr.Amts.Dien.-Doct.-Franz-Marentič'! (Alter+bolezen-PRAZNA-'—')"},
        {"id": "z1-datumi-duel", "opis": "★ z1-1863-restart-datumi-DUEL: VLM-'Jänner-1.'-vs-VIZUALNO-'26.?6.?|3.?' — če-26.-Dec-1862→3.-Jän-1863: ULEDBA-PATTERN-13.-instance-X-open! + stan-'¼-Gütlers-Kind'-VIZUALNO"},
        {"id": "z9-zastava-h9", "opis": "★ z9-'Zastava'-h9 (VIZUALNO-'Zastawa'!; duel-full-page-'Kaslava[?]') — cf. 1864-z1-ŽUNIĆ-Zaštava-h9-ISTO-HIŠO! + starost-duel-74[J-VIZUALNO]-vs-54[full-page]"},
        {"id": "z11-annotacija", "opis": "★ z11-Klošter-h52/32-duel + Anmerkung-annotacija-3-vrstična ('...6.-Feb.-865'?-X-open!) + starost-56[J-VIZUALNO]-vs-36[full-page]"},
    ],
    "hišne_kontinuitete": [
        "★★★ ŠIMEC-h18-NIT-ČEZ-LETA (1863-z26-Georg-Simic-53-J-¼-Güblerssohn → 1864-z34-Peter-ŠIMIC-h18! + 1864-z10-Mathias-h19! — ŠIMEC-2-HIŠI-2-LETI + P200-h18-1877!)",
        "★★★ SIMIC-×2-1863-2-hiši (h18-Georg-53-J + h53-Peter-4-J-4-M — isti-PATTERN-kot-1864-×2-h18/h19!)",
        "★★★ BRINC-h65-NOVA-HIŠA (z12-Johan-43-J-unehelich! — 3.-BRINC-hiša: P212-h23-Anna-60-J + P212-h28-Jernej-28-J + h65!)",
        "★★★ STRAUS-h71-KORELACIJA (1863-z27-'Joannes-Straus'-h11[~71!] → 1864-z44-'Anna-Strauž[~Straus?]'-h71-γ-7 — če-71: isti-γ-glyph-2-leta! X-open!)",
        "★★★ FILAK-Grem-h33-×2-v-3-TEDNIH (z54-novorojenček-Mathias-Filak-Nov-7. + z59-Maria-Filak-5-J-Dez-2.! — cf. FILAK-h34-nit-1864/1865/1866!)",
        "★ DOCTOR-HOUSE-Gradac-h60 (1862-z57 + 1863-z61-Magistrats-Amts-Diener-v.-Dr.-Franz-Marentič!)",
        "★ KRIŽAN-Otok-h20-NIT (1863-z39+z40-Margaretha+Barbara-Križan-1-Mt-Zaugfall-×2! — cf. 1864-z88-Maria-Križan-Otok-h20!)",
        "★ NOVE-HIŠE-1863: h10 (Kune-X-open) + h32 (Ulrich) + h21 (Rosalia-infans) + h53 (Peter-Simic) — korpus-93-X-open!",
    ],
    "crossChecks": [
        "2×-NEODVISNA-PRENOSA-7/7-md5 (s033–s038; s39-carry-iz-/tmp/p213-md5-križ-1:1 — veriga-P213-11.×!)",
        "s35-tail-križ: z55–z60-VLM-1:1-z-P213-pričakovanji + vsotna-'1863'-marker-KROP!",
        "s39-tail-križ: z55–z64-1:1-z-P213-VLM-dokazom (z59-Filak + z61-Marentič + z64-ULEDBA-EXPLICITNI!)",
        "zaporedna-chain-1:1-čez-5-skenov: s35-restart-1–8 → s36-9–23 → s37-24–38 → s38-39–54 → s39-tail-55–64 (ordinali-ČISTO-8.-leto!)",
        "VIZUALNA-verifikacija-skenov-s35–s39 (direktni-vpogled-v-slike: kolone-hišna-x0.21–0.235 + imena + datum + Alter/bolezen-na-desni-strani-razpona!)",
        "KROP-VIZUALNE-ADJUDIKACIJE-×7-skupin (z2-ime+bolezen + z12-hisna+bolezen+opomba + z18-starost + z26-hisna+starost + z27-hisna+ime + z33-hisna+datumi + z38-ime+starost+bolezen!)",
        "arb_s35_glava-'1863'-rokopisna = 52.-POTRDITEV-invariante!",
        "vrstna-aritmetika-8+15+15+16+10 = 64-EXAKT (ordinali-1–64-ČISTO-8.-leto!)",
    ],
    "honesty": [
        "z27-hisna-DUEL-NEREŠEN ('11' vs alternativa-'71' γ-7 — HONEST!)",
        "z27-ime-TRI-branja ('Kras'/'Graus'/'Straus' — X-open!)",
        "z2-ime-4-branja ('Kune'/'Kumre'/'Kime'/'Kure' — X-open!)",
        "z38-ime-4-branja ('Rosalia-infans'/'Josef-Brozik'/'Rojč-Jože' — X-open!)",
        "z38-starost-TRAJNI-DUEL ('1½-J' vs '3-J' — X-open!)",
        "z12-stan-GARBLE ('Pächter-Junggesell[?]' — X-open!)",
        "z11-hisna-DUEL (52-full-page vs 32-krop-zoom — ne-Griblje-HONEST)",
        "z14-hisna-DUEL (54-full vs 31-VIZUALNO) + z19-datumi-DUEL (18./17.? — pokop-pred-smrtjo?!) + z23-hisna-DUEL (54/51)",
        "z64-hisna-DUEL (h14[P213] vs '4'[?VIZUALNO] — Gradac)",
        "z9-starost-DUEL (74-VIZUALNO vs 54-full) + z56-starost-DUEL (27-VIZUALNO vs 25-full) + z48-starost-DUEL (12-VIZUALNO vs 15-full)",
        "z1-datumi-DUEL (VLM-'Jänner-1.' vs VIZUALNO-'26.?6.?|3.?' — ULEDBA-13.-X-open!)",
        "VLM-leta-napake-ignorirane (s34-'410–424'-robna-prefixacija — margin-kontaminacija; ordinali-iz-CHAIN!)",
    ],
    "kaskada": {
        "vitals": "1574 → 1581 (+7 blokov 1863)",
        "04106": "355 → 362",
        "yearset": "+1863 (04106-predzgodovina-23/29!)",
        "meja_1862_63": "s35-restart + vsotna-'1863'-marker + '1863'-rokopisna-glava (52.-POTRDITEV!)",
    },
    "lead": {"P215": "1862 — s33/s34-ŽE-VLM (z24–z54: 31-vrstic-1862!) + s35-tail-z55–z60 (6!) → probe-s029–s033!"},
    "entries_count": len(entries),
    "griblje_count": len(grib),
    "notes": "P214 = 7-skenov-faza (s033–s039; 6-svežih-2×-md5 + s39-carry-P213). MEJA-'1863'-52.-POTRDITEV + NOV-INVARIANTA-TIP: vsotna-vrsta=LETNICA-MARKER ('1|8|6|3' + '1|8|6|4')! + ULEDBA-#11-12.×-EKSPLICITNO (obe-letnici-v-vpisu!) + z53-'außereheliches-Kind-von'-FORMULA-DOKAZ (P213-z6-garble-podprt!) + ŠIMEC-h18-ČEZ-LETA + BRINC-h65-3.-hiša + STRAUS-h71-korelacija-γ-7 + FILAK-Grem-h33-×2. 7-GRIBLJE = NAJMANJ-v-predzgodovini-do-zdaj! (1866:13/1865:13/1864:17/1863:7). KORPUS-93-NESPREMENJEN.",
    "entries": entries,
    "griblje_entries": grib,
    "tail_1862": {"vir": "s35-vrste-1–7 (1862-tail-z55–z60 + vsotna-'1863'-marker — ŽE-VLM-ta-seja! → P215-lead!)",
                  "vrstice_1862_tail": "s35-vrste-1–6 = 1862-z55–z60: Gradac-h5-Schmiedbauer-34J + Krasinec-h9-Križan-27J[~25!] + Gradac-h60-Magistr.Amts-Dien-Doct-Franz-Marentič + Gradac-h60-Podner-1Mt + Boršt-h19-Kožman-82J + Primostek-h13-Tome-68J! + vsotna-'1|8|6|3'-'1863'-MARKER!",
                  "stevilo": 6},
    "meja_1862": "s35: tail-1862 (z55–z60) + vsotna-vrstica-'1|8|6|3' = LETNICA-MARKER-'1863' (NOVI-TIP!) + RESTART-z1 (Gradac-h11-Johana-Marenzič-7-J-'¼-Gütlers-Kind'-Jänner!) — '1863'-rokopisna-glava-s35 = 52.-POTRDITEV!",
}

json.dump(proof, open(f"{TMP}/proof_1863.json", "w"), ensure_ascii=False, indent=1)
import shutil
shutil.copy(f"{TMP}/proof_1863.json", "/home/z/my-project/muzej-backup/research/issue17/parish-death-1863-04106.json")
print(f"dokaz: {proof['entries_count']} entries / {proof['griblje_count']} griblje / {proof['statistika']['griblje_hise']} hiš")
print("otroška:", otrostenje)
print("meseci-griblje:", dict(meseci_g))
