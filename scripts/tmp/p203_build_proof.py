#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P203 — build proof research/issue17/parish-death-1874-04106.json (recept P200-P202)."""
import json

E = json.load(open("/tmp/p203/entries_1874.json"))
entries = E["entries"]
tail_1873 = E["tail_1873"]
griblje = [e for e in entries if e["vas"] and "gribl" in str(e["vas"]).lower()]

OTROŠKE = ["2", "6", "13", "15", "37", "39", "40", "46", "81", "85"]  # jasni-otroci <10-let (h11-16dni + h24-9J + h69-½J + h64-8½T + h72-mrtvorojen + h86-1½J + h39-1J + h57-1J + h19-[?76J-NE!]... — ročno: z2,z6,z15,z37,z39,z46,z81 jasni; z40/z13/z85 mejni?
OTROŠKE = ["2", "6", "15", "37", "39", "46", "81"]  # 7 jasni (<10 J): Lunič-16dni + Brime-9J + Brinc-½J + Vebčar-8½T + Krajnc-mrtvorojen + Tilak-1J + Logar-1J
otroci = [e for e in griblje if e["zap"] in OTROŠKE]

proof = {
    "faza": "P203",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1874 = 12. leto PREDZGODOVINSKE LINIJE (issue #18)",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1874": "s119-glava–s127-z10 (pag 114–121!); 94 vpisov (z1–z94, ŠTEVJE-IZ-VRSTIC-5.× — ordinali-ZMEDANI: s119-'3'-marginal + s127-'14.'/'29.'-VLM-claimi-[?]!) / 21 Griblje / 18 hiš (h64-×2 + h69-×2 + h72-×2!) / Mai-19-MAX + August-1-MIN",
        "meja_1873_74": "★★★ s119 (pag 114): TAIL-10-DEZ-1873-nad (margine-201–212-KROP! 3-GRIBLJE: h23-Brinec + h2-Hlebec + h26-Brumc-31-Dec-smrt/pokop-1-Jan-ULEDBA!) + VELIKA-'18 74. Jänner'-GLAVA (split-forma '18'/'74.'/'Jänner' — medvrstično-raztegnjeno! NO-'Incipit-annus-Domini'-frazo — VLM-halucinacija-FALSIFICIRANA!) + restart-[?]",
        "meja_1874_75": "s127 (P202-REUSE-1:1-MD5): TAIL-10-NOV/DEZ-1874-nad (z85-z94!) + 'Jänner 1875'-glava-v-z11-celici (42.-POTRDITEV-P202!) — POPOLNA-SOGLASJA-Z-P202 (Krič-h19 + Miler-h29-POPRAVEK-hišnih-št.-None→19/29!)",
        "konec_1874": "z94 = s127-r10 (Dez-Certovišče-Zahlič[?]) — leto-konča-z-DEZEMBERJEM (pokop-čez-mejo: r11-Plam-31-Dec-1874-smrt→2-Jan-1875-pokop = P202-z1-ULEDBA!)",
        "zaporedna": "ordinali-ZMEDANI-1874 (s119-marginal-'3' + s127-'14.'/'29.'-[?]) → ŠTEVJE-IZ-VRSTIC-5.× (recept!); ordinali-V-DECEMBERJU-1873-VIDLJIVI (201–212!)",
        "forma": "★★★ GLAVE-V-DATUMSKI-CELICAH-×2-ta-seja: 45.-POTRDITEV-s122-z1-'1874.'-Mai + 46.-POTRDITEV-s125-z1-'1874.'-September (VLM-'Jänner'-×13-FALSIFICIRAN → KROP-'9.'-numerično-OKTOBER-NI! '9.'-mesec = September!) + s119-VELIKA-'18 74. Jänner'-meja-glava + meseci-numerično-'9.'-forma (nov-format-1874!)",
        "skeni": "s118–s127 (pag 113–121); s127+s126-md5-križna-validacija-ta-seja: sveži == P202-disk-1:1 (3a304bd8/64665c40) — VERIGA-P197→…→P203-7.×!",
        "preslikava": "★★★ LEKCIJA-#21: NATISNJENE-ŠT.-STRANI-PREVERJENE-×7: s118=113, s121=116, s122=117 (sken−5!), s123=118-DUPLIKAT!, s124=118, s125=119, s126=120, s127=121 (sken−6!) — duplikat-s123-PREMIKAMapping!",
        "preštevanje": "vrstna-aritmetika 3+11+16+15+14+13+12+10 = 94 ✓ (s123-duplikat-IZPUŠČEN!); meseci J4+F5+M4+A10+M19+J11+J5+A1+S17+O3+N11+D4 = 94 ✓",
    },
    "statistika": {
        "vpisov_1874": 94,
        "griblje": len(griblje),
        "hise": sorted({str(e["hisna"]).split()[0] for e in griblje}, key=lambda x: int(x)),
        "otrok_griblje": f"{len(otroci)}/21 jasna = {round(100*len(otroci)/21)}% (z2-Lunič-16dni + z6-Brime-9J + z15-Brinc-½J + z37-Vebčar-8½T + z39-Krajnc-MRTVOROJEN + z46-Tilak-1J + z81-Logar-1J!) + z13-Brime-62J/z40-Johann-1½J/z85-Krič-76J-ne-otroci",
        "duhovniki": "★★★ KOGEJ-'provisorium'-PODPIS-1874 (z69-KRIŽAN-KROP-'p.-undenard-Kogej'!) + DOVGAN-nit (z81-'Franc-Dougan' + s127-'Franz-Dovgan'-×2!) + 'provisorium-Hoggin-Corp.'-×3 (s127!) + Albin-Schranger-coop-[?]-s120-kontekst",
    },
    "anomalije": [
        "★★★ LEKCIJA-#21-DOUBLE-SCAN-2.×: s123 == s124 (pag-118-×2! natisnjena-št.-strani-'118'-NA-OBOH! hamming-15/256 + KROP-r1/r2-1:1-'Griblje-39-Mathias-Tilak'-'Gradec-75'!) — preslikava-pag-PREMIK: sken−5-pre-duplikata → sken−6-post!",
        "★★★ VLM-'Jänner'-s125-FALSIFIKACIJA-×13 (celotna-stran!): KROP-'9.'-numerično-mesec = SEPTEMBER + '1874.'-glava-v-z1-celici (46.-POTRDITEV!) — lekcija-#20: numerični-meseci-1874!",
        "★★★ VLM-'1877'-s122-FALSIFIKACIJA: KROP-'1874.'-glif-za-glifom ('4'-z-zanko-NE-'7'-γ!) — 45.-POTRDITEV (Mai-blok-opener-'1874.'-v-celici!)",
        "★★★ 'Incipit-annus-Domini-1874'-VLM-halucinacija-FALSIFICIRANA (KROP: samo-'18 74. Jänner'-split-glava!)",
        "★★★ VLM-IZPUST?—s120-Anna-MARC/Mušič-r2-Feber-4/6-Primostek-h7 (KROP-s120-levo-potrjena-vrstica! VLM-jo-je-prebral-kot-'Marc'-ne-'Mušič' — grafia!)",
        "★★★ h83→h33-POPRAVEK (z69-KRIŽAN: KROP-'33.'-glif-za-glifom-'ne-5-ne-8-ne-9'!) + h8→h57-POPRAVEK (z81-LOGAR: KROP-'57.'-glavni-stolpec + MODRA-TINTA-'12'-annotacija-kasneje — anomalija!) + h34→h39 (z46-TILAK: KROP-slika-'39.'!)",
        "★★★ BRIME-×2-v-5-TEDNIH (z6-h24-Maria-9J-Feber-21/23 + z13-h28-Maria-62J-März-28/29! 2-MARIJE-BRIME-2-hiši!)",
        "★★★ MRTVOROJEN-z39-h72 (Todtgeborenes-des-[Marcus-Krajnc?-VLM-vs-Anton-Janec?-KROP!]-Mai-26/27 — 2-OTROKA-h72-1874: + z71-Malenšič-72J! h72-NIT!)",
        "★★★ BRUNE-z51-h69-starost-NESOGLASJE (KROP-'69'-vs-VLM-'56¾ J'! + KROP-datumi-28/30-vs-VLM-23/30!) + h69-×2-1874 (z15-Brinc-½J-April!)",
        "★ z2-LUNIČ-h11-16-DNI (h11 = KUNIĆ-hiša-1875-z71! KUNIĆ/h11-NIT-1-LETO-PRED!)",
        "★ z61-SABLER-h21-priimek-PREČRTAN-KORIGIRAN (KROP-k125: 'Johann-Hau…[?]-prečrtan' + VLM-'črtano-Hauß-nad-ime'!)",
        "★ z88-MILER-h29-'Abb.'-grafia [?opat/vdovec] + z85-KRIČ-h19-'nšl.' — 2-STAROSTNIKA-Nov-Griblje (76J + 71J!)",
        "★ DOVGAN-DOMINANTA-NADALJEVANJE (s124-Dovgan-×3-izpisov + s127-×2 + z81-'Dougan'!)",
        "★ ULEDBA-tail (1873-h26-Brumc-31-Dec→1-Jan + 1874-z94→P202-z1-Plam-31-Dec→2-Jan!)",
    ],
    "hišne_kontinuitete": {
        "h11": "KUNIĆ-hiša (z2-LUNIČ-16dni-Jän-1874 → 1875-z71-KUNIĆ-65J! ime-Katharina-×2!)",
        "h57": "P200-NIT-RAZŠIRJENA-NAZAJ (z81-LOGAR-1J-Nov-1874 → 1877-h57! 3-leta!)",
        "h6": "P200-NIT-RAZŠIRJENA-NAZAJ (z67-JABLOVIČ-25J-Sept-1874 → 1877-h6!)",
        "h72": "×2-1874 (z39-MRTVOROJEN-Mai + z71-MALENŠIČ-72J-Sept!) — NOVA-hiša-korpusa (P202-z40-BRAUŠ-1875-tudi!)",
        "h69": "×2-1874 (z15-BRINC-½J-April + z51-BRUNE-Nov) → P202-h69-×2-KONTINUITETA (1875-HUSIC!)",
        "h64": "×2-1874 (z37-VEBČAR-Mai + z75-JAVORNIK-Sept!) — cf. P201-h64-Kerbica-1876!",
        "h19": "NOVA-hiša (z85-KRIČ-76J-Nov!) + h29-NOVA (z88-MILER-71J-Nov!)",
        "h33": "NOVA-hiša (z69-KRIŽAN-60J-Sept-Wassersucht! — KROP-POPRAVEK-h83→h33!)",
        "h39": "NOVA-hiša (z46-TILAK-1J-Juni-Halborn! — '½-Gabrielsova'-stan!)",
        "h24/h28": "BRIME-×2-v-5-tednih (z6-9J + z13-62J!)",
    },
    "crossChecks": [
        "md5-križna-validacija: s127+s126-sveži == P202-disk-1:1 — VERIGA-7.×!",
        "vrstna-aritmetika: 3+11+16+15+14+13+12+10 = 94 ✓ (s123-IZPUŠČEN!)",
        "meseci-vsota: 4+5+4+10+19+11+5+1+17+3+11+4 = 94 ✓",
        "s127-tail-P202-1:1: Krič-Nov-24/26 + Merac-26/28 + Pegan + Miler-28/30 + Fazilič + Abelavin-Nov30/Dez + Sober + Premer + Jurajec + Zahlič == P202-tail_1874-točno ✓ (+ hišni-POPRAVKI-19/29!)",
        "s123==s124-DVOSCAN: hamming-15/256 + KROP-r1/r2-'Tilak'-'Gradec-75'-1:1 + natisnjena-'118'-×2 ✓",
        "natisnjene-št.-strani-×7: s118=113 + s121=116 + s122=117 + s123/124=118 + s125=119 + s126=120 + s127=121 ✓",
        "s122-'1874.'-KROP-glif-za-glifom ('4'-z-zanko!) ✓",
        "s125-'9.'-numerični-mesec + '1874.'-glava-v-celici (KROP-×2!) ✓",
        "h33/h57/h39-KROP-POPRAVKI-glif-za-glifom-×3 ✓",
        "P202-tail-hišni-POPRAVKI: Krič-None→19 + Miler-None→29 (KROP-slike!) ✓",
    ],
    "honesty": {
        "H1": "ordinali-1874-ZMEDANI → zap-REKONSTRUIRAN (ŠTEVJE-IZ-VRSTIC-5.×); margine-201–212-vidne-samo-v-December-1873-tailu!",
        "H2": "s119-tail-10-vs-margine-do-212 (VLM-struktura-13-vrstic; ±2-drift-mogoče!) — P204-LEAD-flag",
        "H3": "z51-BRUNE-starost-NESOGLASJE (KROP-'69'-vs-VLM-'56¾') + datumi (28/30-vs-23/30) — [~]",
        "H4": "z39-oče-NESOGLASJE (VLM-'Marcus-Krajnc'-vs-KROP-'Anton-Janec') — [?]",
        "H5": "z40-h86[?]-Johann-[?] — hišna-št.-dvom",
        "H6": "z74-z77-h36/h64/h38[~] — hišne-št.-VLM-dvomi (ne-KROP-ane!)",
        "H7": "z61-Sabler-priimek-prečrtan-korigiran — [?]",
        "H8": "z85/z88-h19/h29 — KROP-slike-jasni, ampak-P202-tail-je-prebral-None — [~]",
        "H9": "s122-'Oktober-27'-KROP-crop-misread (stran-je-Mai/Juni!) — datum-obdržan-VLM-Mai-26/27-[~]",
        "H10": "modra-tinta-'12'-annotacija-z81 — kasnejši-dodatek-[?]",
        "H11": "s118 (1873-kontekst-Avg/Sept) ni-v-celoti-analiziran — P204-LEAD",
        "H12": "meseci-per-vrstico = VLM-labeli + FORCE-KROP-popravki (s125-×13 + s120-r11!) — vsota-94-robu-stabilna!",
        "H13": "otroška-umrljivost-7/21-jasna (33%) — mejni-z40-1½J-[?]-z85-76J-ne!",
        "H14": "z37-'8½-(tednov?)-[~]' — enota-dvom",
        "H15": "s123-duplikat: matricula-inventory-vsebuje-pag-118-×2 — pag-117-NI-izgubljen (s122=117!)",
        "H16": "tail_1873-×10: dokumentirane-kot-P204-LEAD",
    },
    "kaskada": {
        "vitals": "1385 → 1406 (+21-blokov-04106-1874!)",
        "04106": "166 → 187 (10×-1875 + 20×-1876 + 8×-1877 + 23×-1878 + 9×-1879 + 13×-1880 + 19×-1881 + 16×-1882 + 11×-1883 + 21×-1884 + 16×-1885 + 21×-1874!)",
        "04894": "520-NESPREMENJENO", "p80": "94-NESPREMENJENO", "korpus": "93-NESPREMENJEN",
        "pt_luknja": "18-REGENERIRANA (187/1406!)", "yearset": "+ 1874 ({1874,...,1885})",
    },
    "lead": {
        "P204": "mrliška 04106, leto 1873 (13/29!) — SIDRA: s119-TAIL-×10-DEZ-1873 (margine-201–212! 3-GRIBLJE: h23-Brinec + h2-Hlebec + h26-Brumc!) + s118-ŽE-FETCHAN+VLM (Avg/Sept-1873-kontekst!) → probe: s110–s119; P204-začetek = išče-nazaj",
        "krstna": "04104-1871–1885-čaka (vzporedno!)", "poročna": "04455-začetek-čaka",
    },
    "entries": entries,
    "tail_1873": tail_1873,
    "notes": [
        "P203-recept = P200-P202-recept + LEKCIJA-#21 (natisnjene-št.-strani-preverjene-×7 + duplikat-s123-skip!).",
        "md5-verige: P197→…→P203 (s127/s126-sveža == P202-disk-1:1 — 7.×!).",
        "VLM-falsifikacije-1874-×3 (s125-'Jänner'-×13 + s122-'1877' + 'Incipit'-halucinacija) — KROP-rešene-×3!",
        "KROP-POPRAVKI-hišnih-št.-×5: h33 (ne-h83!) + h57 (ne-h8!) + h39 (ne-h34!) + h19 + h29!",
    ],
}

out = "/home/z/my-project/research/issue17/parish-death-1874-04106.json"
json.dump(proof, open(out, "w"), ensure_ascii=False, indent=1)
print(f"OK → {out} | entries: {len(entries)} | griblje: {len(griblje)} | otroci: {len(otroci)}/21 | hiše: {proof['statistika']['hise']}")
