#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P213 — dokaz parish-death-1864-04106.json (91 entries: 17-Griblje + 74-druge!)."""
import json

TMP = "/tmp/p213"
E = json.load(open(f"{TMP}/entries_1864.json"))
entries = E["entries"]
grib = E["griblje_entries"]

hise = sorted({e.get("hisna") for e in grib}, key=lambda x: int(x))
hise_d = {}
for e in grib:
    hisena_d.setdefault(e.get("hisna"), []).append(e["z"]) if False else None
from collections import defaultdict
hise_map = defaultdict(list)
for e in grib:
    hise_map[e.get("hisna")].append(e["z"])

otroci = [e for e in grib if any(u in str(e.get("starost", "")) for u in ("mesec", "Mt.", "M.", "tedn", "dn", "uri", "Tage", "Woche")) or str(e.get("starost", "")).startswith(("1 J", "2 J", "5 let"))]
# preštej otroke ročno po z: 6(Kind),12(2J),18(6M),31(5J),35(1J),36(6M),44(1J),61(1½Mt),64(1Mt) = 9
OTROCI_Z = [6, 12, 18, 31, 35, 36, 44, 61, 64]
otrostenje = f"{len(OTROCI_Z)}/{len(grib)} = {round(100*len(OTROCI_Z)/len(grib))}%"

meseci_g = defaultdict(int)
for e in grib:
    m = str(e.get("mesec", "")).split()[0]
    meseci_g[{"Februar": "F", "März": "M", "April": "A", "Mai": "Mai", "Juni": "Juni",
              "September": "S", "December": "D"}.get(m, m)] += 1

proof = {
    "faza": "P213",
    "tema": "MRLIŠKA PREDZGODOVINA 04106 — leto 1864 = 22/29 (issue #18)",
    "knjiga": "04106 (matricula-online.eu — župnija Podzemelj, mrliška 1857–1885)",
    "okvir": {
        "skeni": "s039–s046 (8 skenov svežih; 2×-NEODVISNA-PRENOSA-md5-8/8!)",
        "pag": "34–41 (pag = sken − 5)",
        "meja_1863_64": "s39 (tail-1863-z55–z64 + VSHOTNA-VRSTICA-'1-8-6-4' + RESTART-z1–z2!; rokopisna-'1863'-glava-na-s39 + '1864'-VELIKA-LETVICA-na-s40-glavi = 51.-POTRDITEV-invariante! — arb_s39_glava + arb_s40_glava-KROP!)",
        "meja_1864_65": "s46-tail (z88–z91 = P212-KROP-dokaz-1:1! + ULEDBA-#11-z91-30.Dez→1.Jän-1865!)",
        "vrstna_aritmetika": "2+14+14+14+15+14+14+4 = 91 (ŠTEVJE-IZ-VRSTIC-15.×!)",
    },
    "statistika": {
        "vpisov_1864": len(entries),
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
        {"id": "s41-shift", "opis": "★★★ VLM-ZAP-STOLPEC-+1-POMIK-RAZKRIT (s41): fresh-VLM-prebral-18–31, KROP-stripi + VIZUALNI-dokaz (s41_zap_top: margin-17-18-19-20-21-22-23!) → margin-N == fresh-row(N-16); s41 = z17–z30-ČISTO (KURRENT-ŠTEVILKE-nad-vrstico-lekcija-P158!)"},
        {"id": "z85-nekronološki-vnos", "opis": "★★★ ANOMALIJA-PISAR-2.-×-LETA: z85 (Dec 2./4.-KROP-VIZUALNO-ČISTO!) vpisan-PO-z84 (Dec 11.[~]/13.[~]) — NE-kronološki-vnos (cf. P212-z13-pokop-pred-smrtjo!) — fizični-vrstni-red ≠ kronološki!"},
        {"id": "z6-garble", "opis": "★★★ X-open-IME-GARBLE-z6: '?ollganerischb-Kind-von-Johann-Križan-(½-Gübler)' (ultra-zoom-6×; VLM-'Malijschehibsb'/'Wolfgang-Khür'-FALSIFICIRANI) — FORMULA-hipezoza ≈'uneheliches/außereheliches-Kind-von' (cf. z80-'Mastgutlinstleht-Kind-von-Peter-Požen' + z84-ISTI!)"},
        {"id": "z89-dual-krop", "opis": "★ z89-DUAL-KROP-DUEL (tail): P212-KROP-'Johann-Topič-Lavtinar[?]' vs svež-KROP-2026-'Johanna-Soprič[~]-Kerssnbraid.-hči' — neskladna-2×-max-zoom-branja-HONEST; starost-KOREKCIJA-V-ZAPISU-potrjena-v-obe-seji!"},
        {"id": "z61-h3-vs-h5", "opis": "★★★ KURRENT-3/5/8-ZMEDA-DUEL: z61-hisna VLM-'3'-×2-FALSIFICIRANA → KROP-VISUAL-CALIBRACIJA-'5' (s44_hisna_cal@5×: z60-'1' + z61-'5'-kapa + z62/z63-'8'!)"},
        {"id": "z44-h71", "opis": "★★★ KURRENT-γ-7-DUEL: z44-hisna VLM-'11[~71?]'+KROP-VLM-'7'-FALSIFICIRANA → KROP-VIZUAL-'71' (γ-7-S-PREČKO + ozka-1!) — h71-DUEL-KONTINUITETA-z-P210-z26-'h74[~71?]'!"},
        {"id": "z18-h14", "opis": "★★★ KURRENT-1/4-DUEL: z18-hisna VLM-'11'+KROP-VLM-'11'-FALSIFICIRANA → KROP-VIZUAL-'14' (4-IMA-ZANKO!) → PEZDIRC-h14-NIT-1864!"},
        {"id": "z18-ime-glyph", "opis": "★★★ IME-Glyph-COMPARACIJA: z18-'Feydrie'[KROP]/'Poždrie'[VLM] → PEZDIRC via identična-glyph-veriga-z-z85-'Anna-Pezdirc' (P-cap-e-z-d-r-c!)"},
        {"id": "z33-filak", "opis": "★★★ IME-DUEL: z33-'Kitah'[VLM]/'Šilak'[KROP-VLM]-obe-FALSIFICIRANI → KROP-VIZUAL-'-ilak' → FILAK (h34-nit-3.-leto!)"},
        {"id": "z34-Šimic", "opis": "★★★ IME-DUEL: z34-'Jinnie/Zinnig'[VLM] → KROP-VIZUAL-'Peter-Šimic' (haček-Š!) — ŠIMEC-h18-nit-1864 (cf. z10-h19!)"},
        {"id": "z91-uledba", "opis": "★★★ ULEDBA-#11-10.INSTANCE: z91-smrt-30.Dez-1864 → pokop-1.Jänner-1865 (KLOŠTER-kaplan! čez-mejo-vpis!)"},
        {"id": "z1-pokop-duel", "opis": "★ z1-pokop-DUEL ('14.[~4.?]' — KURRENT-4/9; z1 = Georg-Žunić-Zastava[?]-79-J)"},
    ],
    "hišne_kontinuitete": [
        "★★★ PEZDIRC-NIT-×2-hiši-1864 (h14-Michael-6-M + h11-Anna-14-let!) — h14-veriga: 1864-z18 → 1865-z41-Mathias-unehelich → 1865-tail-z66-Maria-66J (3-LETA!)",
        "★★★ ŽELKO-h1-×2-MAJ-KLASTER (z30-Anna-22-J-½-Witwe-4.5. + z35-Peter-1-J-17.5. — 13-DNI! mati+sin-hipezoza! cf. P212-HUSIČ-h37!)",
        "★★★ FILAK-h34-NIT-1864 (z33-Mathias-63-J → P211-z48-Katarina-6½-J + z80-Josip-1-J!)",
        "★★★ ŠIMEC-NIT-×2-hiši (h18-Peter-60-J + h19-Mathias-65-J! cf. P200-h18-ŠIMEC-NIT-1877)",
        "★★★ POŽEK-h67-NIT (z36-Maria-6-M → 1865-z36-Mathias-36-J-ISTI-z36-ČUDEN-SOVPAD! → h58-P192?)",
        "★★★ KRIŽAN-NIT-×2-hiši (h62-Maria-87-J-NAJSTAREJŠA-1864 + h63-Kind-von-Johann-Križan!) — cf. 1865-z1-h3 + Otok-z88!",
        "★★★ DRAGOŠ-glyph-z27-h3 (Georg-70-J — cf. P200-DRAGOŠ-h12-nit! h3 = KRIŽAN-h3-1865-z1!)",
        "★ KLEPEC-×2 (h2-Maria-2-J + h45-Georg-Obrawos[?]-73-J + Lemež-z14!)",
        "★ NOVA-hiša-h5 (z61-Johannes-Hruscel[?] — korpus-93 X-open!) + h71 (z44 — X-open-P210-duel!)",
    ],
    "crossChecks": [
        "2×-NEODVISNA-PRENOSA-8/8-md5 (s039–s046; strežnik-determinističen — veriga-P212-10.×!)",
        "sveža-s46-tail-križ-vs-P212-dokaz: 3/4-EXAKT (z88-z90-z91-1:1!; z89-DUAL-KROP-duel-HONEST)",
        "s41-zap-KROP-stripi: s41_zap_bot-'23–30'-VLM-✓ + s41_zap_top-VIZUALNO-'17–23' + s40_zap-'3–9'+'10–16' + s42_zap_top-'31–32' = CHAIN-3–44-BREZ-LUKNJE!",
        "sveža-s42/s43/s44/s45-margins == P212-lead-chain-31–91-1:1 (z74-duel-REŠEN-potrjen!)",
        "KROP-VIZUALNE-ADJUDIKACIJE-×8 (z18-h14 + z27-h3 + z44-h71 + z61-h5 + z85-h11/datumi + z33-Filak + z34-Šimic + z18-Pezdirc!)",
        "arb_s39_glava-'1863' + arb_s40_glava-'1864' = 51.-POTRDITEV-invariante!",
        "vrstna-aritmetika-2+14+14+14+15+14+14+4 = 91-EXAKT (ordinali-1–91-ČISTO-7.-leto!)",
    ],
    "honesty": [
        "z6-ime-GARBLE-X-open ('?ollganerischb' — 3-branja-neskladna; formula-hipezoza-dokumentirana!)",
        "z9-stan-GARBLE ('¼-Gürlichanderuib'/'güblasbonil' — ≈¼-Güblerin? X-open!)",
        "z17-hisna-DUEL (VLM-'11' vs KROP-vizual-'14'? — ne-Griblje-HONEST)",
        "z25-mesec-KONTEKST-ZAPUŠČANJE ('—' → April-deduced!)",
        "z31/z32-'Kitah'-2×-X-open (brata? garble? — HONEST)",
        "z45-datum-'Juli-27.[~]' (5-tednov-luknja-po-z44-Juni-22 — HONEST-as-read)",
        "z84-datum-DUEL (VLM-'11.[~]/13.[~]' vs KROP-vizual-'14.[~]/15.[~]' — ne-Griblje)",
        "z89-DUAL-KROP-DUEL (P212-vs-2026-KROP-neskladna!)",
        "z13/z33/z34-stan-'Altabler[?]-garble' (≈Ablöser? — HONEST)",
        "VLM-leta-napake-ignorirane (s42-'1861'-hallucinacija — letnica-iz-KROP-glav!)",
    ],
    "kaskada": {
        "vitals": "1557 → 1574 (+17 blokov 1864)",
        "04106": "338 → 355",
        "yearset": "+1864 (04106-predzgodovina-22/29!)",
        "meja_1863_64": "s39-restart + vsotna-vrstica-1-8-6-4 + '1864'-glava-s40 (51.-POTRDITEV!)",
    },
    "lead": {"P214": "1863 — s39-tail-ŽE-VLM (z55–z64: 10-vrstic-1863-tail + vsotna!) → probe-s033–s039!"},
    "entries_count": len(entries),
    "griblje_count": len(grib),
    "notes": "P213 = 8-skenov-faza (s039–s046; 7-1864 + s39-meja + s46-tail-reuse-P212). MEJA-'1864'-51.-POTRDITEV + s41-SHIFT-SANACIJA (2.×-po-P158!) + 8-KROP-VIZUALNIH-ADJUDIKACIJ (hišne-številke-×4 + imena-×4!) + ANOMALIJA-ne-kronološki-vnos-z85 + PEZDIRC-×2-hiši + ŽELKO-h1-×2 + otroška-53% (VIŠJA-kot-1865!). KORPUS-93-NESPREMENJEN (X-open-h5/h71!)",
    "entries": entries,
    "griblje_entries": grib,
    "tail_1863": {"vir": "s39-vrstice-1–10 (1863-z55–z64 — ŽE-PREBRANO-ta-seja! → P214-lead!)",
                  "vrstice_1863_tail": [e for e in entries if e.get("sken") == 39][:0] or "v-P214! (s39-vrstice-1–10 = 1863-z55–z64: Prilozje-32-Kuštarić-19J + Zemelj-22-Taklić-49J + Prilozje-41-Takleci-29J + Dobravce-27-Engel-30J + Grem-33-Filak-5J + Certovše-23-Stubler-2J + Gradac-60-Mavretič[?]-? + Certovše-1-Stubler-2J + Giriče-35-Hozinić[?]-71J + Gradac-14-Marentič-7-dni!)",
                  "stevilo": 10},
    "meja_1863": "s39: tail-1863 (z55–z64) + vsotna-vrstica (1-8-6-4) + RESTART-z1 (Georg-Žunić-Zastava[?]-h9-79-J-Jan-2./14.[~4.?]) + z2 (Peter-Štipanić[?]-Gradac-h6-61-J) — '1864'-VELIKA-LETVICA-na-s40 = 51.-POTRDITEV!",
}

json.dump(proof, open(f"{TMP}/proof_1864.json", "w"), ensure_ascii=False, indent=1)
# tudi v research/
import shutil
shutil.copy(f"{TMP}/proof_1864.json", "/home/z/my-project/muzej-backup/research/issue17/parish-death-1864-04106.json")
print(f"dokaz: {proof['entries_count']} entries / {proof['griblje_count']} griblje / {proof['statistika']['griblje_hise']} hiš")
print("otroška:", otrostenje)
print("meseci-griblje:", dict(meseci_g))
