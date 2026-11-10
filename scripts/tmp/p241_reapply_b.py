#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p241_reapply_b — obnovi P241 v src/data/atlas/parish-marriage-early.ts (glava + izvozi + docstringi)."""
import sys

PATH = '/home/z/my-project/src/data/atlas/parish-marriage-early.ts'
with open(PATH, encoding='utf-8') as f:
    text = f.read()

# B1) glava
OLD_H = '// P240: leto 1883 = 3/13 (s50–s52, 12 vpisov, RESTART = s50-dno, 2 Griblje bloka h13+h2, h2 = 1.-poročni-04455-blok!).'
NEW_H = OLD_H + '\n// P241: leto 1882 = 4/13 (s45–s50, 26 vpisov, RESTART = s45-glava-PRED-vrstico-1!, 7 Griblje blokov, h1 = najnižja-hiša-KADARKOLI!, PEZDIRC ×5!).'
if text.count(OLD_H) != 1:
    print('ABORT: glava:', text.count(OLD_H)); sys.exit(1)
text = text.replace(OLD_H, NEW_H)
print('B1) glava posodobljena')

# B2) izvozi (za MARRIAGE_1883_VILLAGE_DUELS)
ANCHOR = None
for line in text.split('\n'):
    if 'MARRIAGE_1883_VILLAGE_DUELS' in line and line.strip().startswith('export'):
        ANCHOR = line
        break
if ANCHOR is None:
    print('ABORT: anchor DUELS'); sys.exit(1)
# anchor = začetek export const MARRIAGE_1883_VILLAGE_DUELS = [ ... ] as const; — poišči celoten blok
i = text.find(ANCHOR)
j = text.find('] as const;', i)
if j < 0:
    print('ABORT: konec DUELS'); sys.exit(1)
j += len('] as const;')
BLOCK = '''

// ——— P241: leto 1882 = 4/13 — s45–s50, 26 vpisov, RESTART = s45 (glava-PRED-vrstico-1!) ———

/** Bloki P241 (leto 1882) iz korpusa — izpeljano 1:1 (h35-nevesta · h38×h12 · h56-nevesta-vdova · h13×h52 · h8-nevesta · h1×h10 · h36-MERGE-z-P80-sidrom-1:1!). */
export const MARRIAGE_1882_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1882,
);

/** Št. Griblje porok 1882 v korpusu (meritev: 7 = 6-NOVIH + 1-MERGE-z-P80-sidrom-h36! — 3 POLNA ×2 (h38×h12 · h13×h52 · h1×h10!) + 4 Griblje-neveste/ženina; 2 X-OPEN-duela NISTA bloka). */
export const MARRIAGE_1882_GRIBLJE = MARRIAGE_1882_BLOCKS.length;

/** Hiše poročne linije 1882 (merjeni vrstni-red blokov: 35, 38, 56, 13, 8, 1, 36 [h36 = MERGE-z-P80-sidrom — na-koncu-arraya!]). */
export const MARRIAGE_1882_HOUSES = MARRIAGE_1882_BLOCKS.map((h) => h.houseNo);

/** Vsi vpisi leta 1882 (meritev: 26 številčenih — zap 1.–26., BREZ preskokov — 4. leto zapored!). Korpus: 6-NOVIH-blokov (+1-MERGE-z-P80-sidrom-h36!) — P238-h13-MERGE-vzorec! */
export const MARRIAGE_1882_TOTAL = 26;

/** X-open kandidati 1882 (v14-'Gradac/Griblje-2/Lette-40'-3-vasni-duel! + v17-'Nemiška-vas-9-vs-Griblje-8?'-Mličar/Mlinar-duel!) — NE-bloki! */
export const MARRIAGE_1882_XOPEN = [
  "v14 [~X-OPEN]",
  "v17 [~X-OPEN]",
] as const;

/** Meje leta 1882: restart = s45 (VELIKA-glava-'1882'-PRED-vrstico-1 — NOVA-4.-mejna-varianta!) · meja-1881/82 = s44→s45 · meja-1882/83 = s50-MID (P240-1:1!). */
export const MARRIAGE_1882_MEJA = {
  restartSi:
    "restart-vpis-1 = 1. Februar 1882 [~21.-Jänner-DUEL-2:2!] (s45, VELIKA-GLAVA-'1882'-PRED-VRSTICO-1-NE-V-GLAVI-STRANI!-NOVA-4.-MEJNA-VARIANTA!-ženin-Anton-TASIE!)",
  restartEn:
    "restart-entry-1 = Feb 1, 1882 [~Jan-21-DUEL-2:2!] (s45, the-BIG-'1882'-HEADING-BEFORE-row-1-NOT-in-the-page-head!-a-NEW-4th-BOUNDARY-VARIANT!-groom-Anton-TASIE!)",
  tailSi: "tail-vpis-26 = 26. November 1882 (s50-MID — Mathias-HRIZAN-GRIBLJE-36!-restart-1883-na-isti-strani-P240-1:1!)",
  tailEn: "tail-entry-26 = Nov 26, 1882 (s50-MID — Mathias-HRIZAN-GRIBLJE-36!-the-1883-restart-on-the-same-page-P240-1:1!)",
  boundarySi:
    "meja-1881/82 = s44→s45-glava (tail-1881-NI-na-s45-top!-1881-se-zaključi-na-s44!-p12-1:1!) · meja-1882/83 = s50-MID (P240-1:1!)",
  boundaryEn:
    "the-1881/82-boundary = s44→s45-heading (NO-1881-tail-on-s45-top!-1881-ends-on-s44!-p12-1:1!) · the-1882/83-boundary = s50-MID (P240-1:1!)",
} as const;

/** Številčenje strani 1882 (s45=1–4 · s46=5–8 · s47=9–12 · s48=13–17 · s49=18–23 · s50-tail=24–26) — nodat-trakovi-×5-1:1 → 26-VPISOV-BREZ-PRESKOKOV (4.-leto-zapored!-kontrast-1885-vpis-3-PRESKOČEN!). */
export const MARRIAGE_1882_NUMBERING =
  "s45 = restart-1–4 · s46 = 5–8 · s47 = 9–12 · s48 = 13–17 · s49 = 18–23 (nodat-trakovi-×5-1:1!) · s50-tail = 24–26 (P240-1:1!) — 26-VPISOV-BREZ-PRESKOKOV-4.-LETO-ZAPORED";

/** PEZDIRC-nit 1882: ×5-VPISOV (v9-Georg-ŽENIN-×-Margaretha-NEVESTA-OBA-PEZDIRC!-+ starši-oče-Georg-PEZDIRC-×-mati-Anna-roj.-Tomc-+ priča-Georg-PEZDIRC! + v15-nevesta-Maria-h52 + v16-ženin-Michael-Prusi-3-(oče-tudi-PEZDIRC!)-+ v18-nevesta-Anna-Otok-1-(priči-Matthias-×-Anton-PEZDIRC!)-+ v21-nevesta-Anna-[~Krupšiše-4]) = PEZDIRC-CONTINUUM-04104-×131→04455-v-4.-letu-predzgodovine! */
export const PEZDIRC_1882_NIT =
  "×5-vpisov (v9-OBA-Georg-×-Margaretha-PEZDIRC!-+ starši-PEZDIRC-×2-+ priča-PEZDIRC! + v15-Maria-h52 + v16-Michael-Prusi-3 + v18-Anna-Otok-1 + v21-Anna-[~]) + priče/starši-dodatno-×4 = continuum-04104-×131→04455-v-4.-letu!";

/** ★★★★★ h1-REKORD: vpis-23 = 1.-POROČNI-BLOK-NA-h1-KADARKOLI (najnižja-hiša!-preglasi-h2-P240-za-1-stopnjo!-h1-aktivna-v-04894-mrliški-1889/1890/1904!— poročna-zdaj-OUTRUNA-mrliško-tudi-na-h1-ZA-7-LET!-1882-vs-1889!). */
export const H1_1882_REKORD =
  "vpis-23-Nicolaus-LESIRO-GRIBLJE-1 = 1.-poročni-blok-na-h1-KADARKOLI! (najnižja-hiša!-preglasi-h2-P240!-h1-aktivna-04894-1889/1890/1904!-poročna-OUTRUNA-mrliško-tudi-na-h1-ZA-7-LET!)";

/** Duhovnik 1882: Franz-Dovgan-[~garble-dominanta]-×-v18-'Georg/Jurij-Dragon-[~]'-duel-1-read = DRUGI-duhovnik-kandidat-[~X-OPEN!]. */
export const PRIEST_1882 =
  "Franz Dovgan [~Dorgan/Dergan/Dorgam/Dorgun/Dvorjan-garble] — dominanta + v18-'Georg/Jurij-Dragon-[~]'-(p09-1-read!)- = DRUGI-DUHOVNIK-KANDIDAT-[~1-read-X-OPEN!]";

/** Foliacija-s45-branje-'93/94'-[~X-OPEN!]: pass-1-pageNote-je-prebrala-'Strani-93/94' — NE-ujema-s-pravilom-'Pag-=-sken−1'-(s45-→-Pag-44!)-P238/239/240-pravilo-je-bilo-preverjeno-samo-za-s56–s66! */
export const FOLIACIJA_1882_XOPEN =
  "s45-pass-1-branje-'Strani-93/94'-[~1-read!] vs pravilo-'Pag-=-sken−1'-(s45→Pag-44)-[~X-OPEN!]-P238/239/240-pravilo-preverjeno-samo-s56–s66-P240-sami-'[~predvidoma-NI-ločeno-preverjeno]'!";

/** BRINC/BRINEC-mreža 1882 (vpis-13: nevesta-Katharina-BRINC-vdova-h56 + oče-Ivan-Brinc + mati-Maria-roj.-Grunc-[~] + priči-Peter-×-Georg-BRINEC!). */
export const BRINC_1882_NIT =
  "v13-NEVESTA-Katharina-BRINC-vdova-48-let-h56! + oče-Ivan-Brinc + mati-Maria-roj.-Grunc-[~] + priči-Peter-×-Georg-BRINEC-[~Brinc-DUEL] = cf.-P238-BRINC/BRINEC-×2-bloki-+ usnjarska-veja!";

/** Vas-dueli 1882 (v14-'Gradac-5-vs-Griblje-2-vs-Lette-40'-3-branja! + v17-'Nemiška-vas-9-vs-Griblje-8?'-Mličar/Mlinar! + v21-'Krupšiše-4-[~]' + v2-'Mokre/Mohr-[~]'). */
export const MARRIAGE_1882_VILLAGE_DUELS = [
  "v14 »Gradac 5 vs Griblje 2 vs Lette 40« 3-branja [~X-OPEN]",
  "v17 »Nemiška vas 9 vs Griblje 8?« Mličar/Mlinar [~]",
  "v21 »Krupšiše 4« [~]",
  "v2 »Mokre 24 vs Mohr« [~]",
] as const;'''

text = text[:j] + BLOCK + text[j:]
print('B2) izvozi vstavljeni')

with open(PATH, 'w', encoding='utf-8', newline='') as f:
    f.write(text)
print('ZAPISANO:', PATH)
