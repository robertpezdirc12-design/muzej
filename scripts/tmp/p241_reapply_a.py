#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p241_reapply_a — obnovi P241 v src/data/atlas/parish.ts (6 novih blokov + merge-obogatitev P80-sidra h36)."""
import sys

PATH = '/home/z/my-project/src/data/atlas/parish.ts'
with open(PATH, encoding='utf-8') as f:
    text = f.read()

ANCHOR_P239 = '  // ——— P239: poročna PREDZGOVINA 04455, leto 1884 = 2/13'
# najdi vrstico-sidro (ASCII-varno)
anchor = None
for line in text.split('\n'):
    if 'P239: poročna PREDZGOVINA 04455, leto 1884' in line and line.strip().startswith('//'):
        anchor = line
        break
if anchor is None or text.count(anchor) != 1:
    print('ABORT: anchor P239'); sys.exit(1)

SECTION = '''  // ——— P241: poročna PREDZGOVINA 04455, leto 1882 = 4/13 — (s45–s50; 26-vpisov-leta-1882 (števje-iz-zap-stolpca 1.–26., BREZ-preskokov!-4.-leto-zapored!-kontrast-1885-vpis-3-PRESKOČEN!); ★★★ RESTART-1882 = s45 (VELIKA-GLAVA-'1882'-PRED-VRSTICO-zap.-št.-1-NE-V-GLAVI-STRANI!-NOVA-4.-MEJNA-VARIANTA!-p12-ultra-zoom-1:1!-cf.-1883-'1-8-8-3.'-razporejeno + 1884/1885-glava-vrhnja!); ★★★ MEJA-1881/82 = s44→s45-glava (tail-1881-NI-na-s45-top-p12-1:1!-1881-se-zaključi-na-s44!); ★★★ MEJA-1882/83 = s50-MID (tail-1882-vpisi-24–26-novembra-19./26./26.!-P240-1:1!); številčenje: s45=1–4 · s46=5–8 · s47=9–12 · s48=13–17 · s49=18–23 · s50-tail=24–26 (nodat-trakovi-×5-1:1-BREZ-preskokov!) — 6-NOVIH-GRIBLJE-blokov + 1-MERGE-z-P80-sidrom-h36 (P238-h13-MERGE-vzorec!-P240-napoved-IZPOLNJENA!): h35-NEVESTA + h38-×-h12-POLNI×2! + h56-NEVESTA-VDOVA + h13-×-h52-POLNI×2! + h8-NEVESTA + h1-×-h10-POLNI×2! + h36-TAIL-MERGE! + ★★★★★ h1 = NAJNIŽJA-HIŠA-S-POROČNIM-BLOKOM-KADARKOLI (preglasi-h2-P240!-h1-aktivna-04894-1889/1890/1904!-poročna-OUTRUNA-mrliško-tudi-na-h1-ZA-7-LET!) + PEZDIRC-×5-vpisov (v9-OBA-Georg-×-Margaretha-PEZDIRC! + v15-Maria + v16-Michael + v18-Anna + v21-Anna-[~]!) = PEZDIRC-CONTINUUM-04104-×131→04455-v-4.-letu! + BRINC/BRINEC-mreža-v13 + DRAGOŠ-nit-v8 + Jakopič-križ-v15×v16 + duhovnik-Franz-Dovgan-[~garble]-dominanta + v18-'Georg/Jurij-Dragon-[~]'-duel + foliacija-s45-'93/94'-[~X-OPEN]-ne-ujema-s-'pag-=-sken−1'! ———
  {
    houseNo: "35",
    bookSignature: "04455",
    year: 1882,
    scan: 45,
    page: 44,
    whatSi: "poroka 1. Februar 1882 [~21.-Jänner-DUEL-2:2-branja!] (vpis 1 = RESTART-1882!) — ženin Anton TASIE [~Tasič-DUEL], lediger-Bauernsohn [~Gömblerssohn-DUEL], 24 let, Mokrine 1 [~Hrasine/Krasinec-DUEL-3-branja!] × nevesta Anna CVET [~Cvec-DUEL], lediga-Vinarski-Dienstbotin [~], 19 let, GRIBLJE 35 (ultra-zoom-števke-'35'-1:1-p01!-vs-'33/36'-dueli-desno!) — GRIBLJE-BLOK-NEVESTA + ★★★ RESTART-1882 = s45 (VELIKA-GLAVA-'1882'-PRED-VRSTICO-1-NE-V-GLAVI-STRANI!-NOVA-4.-MEJNA-VARIANTA-p12-1:1!-cf.-1883-razporejeno-+ 1884/1885-vrhnja!) + MEJA-1881/82 = s44→s45-glava (tail-1881-NI-na-s45-top!-p12-1:1!) + datum-DUEL-'1.-Februar'-(levo_cel-+ p12-2-branja!)-vs-'21.-Jänner'-(pass-1-+ p01!-2:2!) + priče-Matthias-[~Katabon/Katarbon]-×-Johann-[~] + spričevalo-občine-12.-februar-[~desno-1-read]",
    whatEn: "marriage Feb 1, 1882 [~Jan-21-DUEL-2:2-readings!] (entry 1 = THE 1882 RESTART!) — groom Anton TASIE [~], lediger-Bauernsohn [~], 24 y., Mokrine 1 [~3-reading-DUEL!] × bride Anna CVET [~], lediga-Vinarski-Dienstbotin [~], 19 y., GRIBLJE 35 (ultra-zoom-digits-'35'-1:1-p01!-vs-'33/36'-duels!) — THE GRIBLJE-BRIDE-BLOCK + ★★★ THE 1882 RESTART = s45 (the-BIG-'1882'-HEADING-BEFORE-row-1-NOT-in-the-page-head!-a-NEW-4th-BOUNDARY-VARIANT-p12-1:1!) + the-1881/82-boundary = s44→s45-heading (NO-1881-tail-on-s45-top!-p12-1:1!) + date-DUEL-'Feb-1'-(2-readings!)-vs-'Jan-21'-(2-readings!-2:2!) + witnesses-Matthias-[~]-×-Johann-[~]",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "38",
    bookSignature: "04455",
    year: 1882,
    scan: 46,
    page: 45,
    whatSi: "poroka 15. Februar 1882 [~16.-februar-spričevalo-DUEL!] (vpis 8) — ženin Johan PAZEŠ [~Pazek/Gozek/Bozðe-DUEL-4-branja!-p03-krop-misaligned-RAZREŠEN-na-polovicah!], ½-Güblner-Knecht, 24 let, GRIBLJE 38 (s46_levo-'jasno-38'-1:1!-×2-branja!) × nevesta Anna DRAGOS [~Dragoš], ½-Güblnerin-Tochter, 23 let [~], GRIBLJE 12 [~1-branje-pass-1!-p03-'½'-MISREAD-RAZREŠEN-kot-STATUS-ne-hiša!] — POLNI-GRIBLJE-BLOK ×2! + ★★★ DRAGOŠ-nit (starši-neveste-Johann-DRAGOS-×-Anna-DRAGOS-obé-isti-priimek-[~!]— cf.-P239-v16-mati-Dorothea-roj.-DRAGOŠ-P236-nit!-+ P231-z51-h72-DRAGOŠ-matec!-+ 1882-v3-ženin-Josef-DRAGOŠ-Krasinec!) + spričevalo-občine-Griblje-od-16.-febr.-1882-[~datum-DUEL] + v5–v8-datumi-12./15./15./15.-Februar (desno-spričevala-12./8./2./16.-februar-[~!]— 4-spričevala-PRED-poroko!)",
    whatEn: "marriage Feb 15, 1882 [~Feb-16-certificate-DUEL!] (entry 8) — groom Johan PAZEŠ [~4-reading-DUEL!-p03-crop-misaligned-RESOLVED-via-halves!], ½-Güblner-Knecht, 24 y., GRIBLJE 38 (s46_levo-'clearly-38'-1:1!-×2-readings!) × bride Anna DRAGOS [~Dragoš], ½-Güblnerin-Tochter, 23 y. [~], GRIBLJE 12 [~1-reading-pass-1!-p03-'½'-MISREAD-RESOLVED-as-STATUS-not-house!] — THE FULL-GRIBLJE-BLOCK ×2! + ★★★ THE DRAGOŠ-thread (the-bride's-parents-Johann-DRAGOS-×-Anna-DRAGOS-both-the-same-surname-[~!]— cf.-P239-v16-the-mother-Dorothea-née-DRAGOŠ-P236-thread!-+ P231-z51-h72-DRAGOŠ-mother!-+ 1882-v3-groom-Josef-DRAGOŠ-Krasinec!) + the-Griblje-certificate-of-Feb-16-1882-[~date-DUEL]",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "56",
    bookSignature: "04455",
    year: 1882,
    scan: 48,
    page: 47,
    whatSi: "poroka 19. Februar 1882 (vpis 13; levo-'13.-Febr.'-datum-DUEL!) — ženin Ivan HUDIČ [~Hrovič-DUEL!], gütlер [~], 36 let [~56-DUEL-1-branje!], Dolence 24 × nevesta Katharina BRINC, vdova [vdh.-roj.-Grunc-[~]-1-branje!], 48 let (ULTRA-ZOOM-2×-1:1-p06!), GRIBLJE 56 (ultra-zoom-'jasno-56-NE-50'-1:1!) — GRIBLJE-BLOK-NEVESTA-VDOVA + ★★★ BRINC/BRINEC-MREŽA (oče-neveste-Ivan-Brinc-×-mati-Maria-roj.-Grunc-[~]! + priči-Peter-BRINEC-×-Georg-BRINEC-[~Brinc-DUEL]!— cf.-P238-BRINC/BRINEC-×2-bloki-+ usnjarska-veja-×14!) + duhovnik-pripis-'Comm.-ad-valid.-Missam'-[~Dvorjan/Dorgam-garble]-1.×-te-vrste-v-predzgodovini! + starost-ženina-36-vs-56-DUEL (p06-'36'-vs-levo_cel-'56.-[~]'!)",
    whatEn: "marriage Feb 19, 1882 (entry 13; the-left-'13.-Febr.'-date-DUEL!) — groom Ivan HUDIČ [~Hrovič-DUEL!], gütlер [~], 36 y. [~56-DUEL!] , Dolence 24 × bride Katharina BRINC, a-widow [née-Grunc-[~]-1-reading!], 48 y. (ULTRA-ZOOM-2×-1:1-p06!), GRIBLJE 56 (ultra-zoom-'clearly-56-NOT-50'-1:1!) — THE-GRIBLJE-BRIDE-WIDOW-BLOCK + ★★★ THE BRINC/BRINEC-network (the-bride's-father-Ivan-Brinc-×-mother-Maria-née-Grunc-[~]! + witnesses-Peter-BRINEC-×-Georg-BRINEC-[~Brinc-DUEL]!— cf.-P238-BRINC/BRINEC-×2-blocks-+ the-tannery-line-×14!) + the-priest-annotation-'Comm.-ad-valid.-Missam'-1st-of-this-kind-in-the-prehistory! + the-groom's-age-36-vs-56-DUEL",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "13",
    bookSignature: "04455",
    year: 1882,
    scan: 48,
    page: 47,
    whatSi: "poroka 19. Februar 1882 (vpis 15) — ženin Matthias JAKOPIČ [~Jakobitsch-DUEL], ledig, 25 let, GRIBLJE 13 (×3-branja-1:1!-p07-krop-horizontałно-raztegnjen-MISREAD-'8'-RAZREŠEN-na-polovicah!) × nevesta Maria PEZDIRC [~Pegdirc-DUEL-2.-črka-e/z!], ledige-Dienstmagd, 31 let [~], GRIBLJE 52 [~2-branja-pass-1-+ desno!] (starši-neveste-Ivan-PEZDIRC-[~]-×-[~Krambič]-kmetje!) — POLNI-GRIBLJE-BLOK ×2! + ★★★ PEZDIRC-NEVESTA (continuum-×131→04455-se-širi-v-4.-letu!) + ★★★ h13-CONTINUUM-3-poročna-vpisa-v-predzgodovini (1882-v15-JAKOPIČ!-+ 1883-v5-RADOVIČ-P240!-+ 1885-v22-P80-sidro-'née-PEGDIREC'!) + ★★★ Jakopič-križ-v15×v16 (ženin-v15-JAKOPIČ + nevesta-v16-Anna-JAKOPIČ-[~sorodstvo-X-OPEN!]) ———",
    whatEn: "marriage Feb 19, 1882 (entry 15) — groom Matthias JAKOPIČ [~Jakobitsch-DUEL], ledig, 25 y., GRIBLJE 13 (×3-readings-1:1!-p07-crop-horizontally-stretched-MISREAD-'8'-RESOLVED-via-halves!) × bride Maria PEZDIRC [~Pegdirc-DUEL-the-2nd-letter-e/z!], ledige-Dienstmagd, 31 y. [~], GRIBLJE 52 [~2-readings!] (the-bride's-parents-Ivan-PEZDIRC-[~]-×-[~Krambič]-farmers!) — THE-FULL-GRIBLJE-BLOCK ×2! + ★★★ THE-PEZDIRC-BRIDE (the-continuum-×131→04455-spreads-into-the-4th-year!) + ★★★ THE-h13-CONTINUUM-3-marriage-entries-in-the-prehistory (1882-v15-JAKOPIČ!-+ 1883-v5-RADOVIČ-P240!-+ 1885-v22-the-P80-anchor-'née-PEGDIREC'!) + ★★★ THE-Jakopič-cross-v15×v16 (the-v15-groom-JAKOPIČ-+ the-v16-bride-Anna-JAKOPIČ-[~kinship-X-OPEN!])",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "8",
    bookSignature: "04455",
    year: 1882,
    scan: 48,
    page: 47,
    whatSi: "poroka 14. Mai 1882 (vpis 16) — ženin Michael PEZDIRC [~Pegdirc-DUEL-ultra-zoom!], ½-Gütler, 42 let, Prusi-nec.-3 [~pripis-'nec.'-1.×-te-vrste!] (oče-Georg-PEZDIRC-Gütler-¥-pokojni-[~1-branje!]!) × nevesta Anna JAKOPIČ, ledige-½-Güblerin, 16 let (ULTRA-ZOOM-2×-1:1-p08!-NAJMLAJŠA-NEVESTA-1882!), GRIBLJE 8 (ultra-zoom-številka-'8'-1:1-p08!) — GRIBLJE-BLOK-NEVESTA + ★★★ PEZDIRC-ŽENIN-#2-v-1882 (oče-tudi-PEZDIRC!-očetov-¥-pripis-1.×!) + ★★★ Jakopič-križ (v15-ženin-Matthias-JAKOPIČ + v16-nevesta-Anna-JAKOPIČ-2-Jakopiča-v-2-zaporednih-vpisih-[~brat/sestra-X-OPEN!] + nevesta-v15-Maria-PEZDIRC-h52!-križ-Pezdirc↔Jakopič!) + priče-Michael-[~Kruth]-×-Georg-[~Hrovatin]-×-Martin-[~] + duhovnik-Franz-Dergan-[~Dovgan-garble]-Cooperator!",
    whatEn: "marriage May 14, 1882 (entry 16) — groom Michael PEZDIRC [~Pegdirc-DUEL-ultra-zoom!], ½-Gütler, 42 y., Prusi-nec.-3 [~the-'nec.'-annotation-1st-of-this-kind!] (the-father-Georg-PEZDIRC-a-Gütler-¥-deceased-[~1-reading!]!) × bride Anna JAKOPIČ, ledige-½-Güblerin, 16 y. (ULTRA-ZOOM-2×-1:1-p08!-THE-YOUNGEST-BRIDE-OF-1882!), GRIBLJE 8 (ultra-zoom-the-digit-'8'-1:1-p08!) — THE-GRIBLJE-BRIDE-BLOCK + ★★★ THE-PEZDIRC-GROOM-#2-in-1882 (the-father-also-PEZDIRC!-the-father's-¥-annotation-1st!) + ★★★ THE-Jakopič-cross (the-v15-groom-Matthias-JAKOPIČ-+ the-v16-bride-Anna-JAKOPIČ-2-Jakopičs-in-2-consecutive-entries-[~siblings-X-OPEN!] + the-v15-bride-Maria-PEZDIRC-h52!-the-Pezdirc↔Jakopič-cross!) + witnesses-Michael-[~]-×-Georg-[~]-×-Martin-[~] + the-priest-Franz-Dergan-[~Dovgan-garble]-Cooperator!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "1",
    bookSignature: "04455",
    year: 1882,
    scan: 49,
    page: 48,
    whatSi: "poroka 12. November 1882 (vpis 23) — ženin Nicolaus LESIRO [~Lesko/Geširo/Heßiro-DUEL-4-branja!], ¼-Höfling, 50 let, GRIBLJE 1 (s49_levo-'Haus-Nr.-1'-1:1!-×2-branja!) × nevesta Katharina ŠKRCE [~Škerce-DUEL], Leinannin [~Leinweber-nit-cf.-P80-h13-'Leinweber'!], 30 let, GRIBLJE 10 [~1-branje-pass-1!] — POLNI-GRIBLJE-BLOK ×2! + ★★★★★ h1 = NAJNIŽJA-HIŠA-S-POROČNIM-BLOKOM-KADARKOLI (preglasi-h2-P240-za-1-stopnjo!-h1-AKTIVNA-v-04894-mrliški-1889/1890/1904-'NAJNIŽJA-hiša-3-mrliških-vpisov'!— poročna-zdaj-OUTRUNA-mrliško-tudi-na-h1-ZA-7-LET!-1882-vs-1889!) + priči-Georg-[~Šeško]-×-Nikola-[~Švec] + LESKO-križ (v10-priča-'Johann-Lesko-[~]'-s47!-×2-v-letu!) ———",
    whatEn: "marriage Nov 12, 1882 (entry 23) — groom Nicolaus LESIRO [~Lesko/Geširo/Heßiro-DUEL-4-readings!], ¼-Höfling, 50 y., GRIBLJE 1 (s49_levo-'Haus-Nr.-1'-1:1!-×2-readings!) × bride Katharina ŠKRCE [~Škerce-DUEL], Leinannin [~the-Leinweber-thread-cf.-the-P80-h13-'Leinweber'!], 30 y., GRIBLJE 10 [~1-reading-pass-1!] — THE-FULL-GRIBLJE-BLOCK ×2! + ★★★★★ h1 = THE-LOWEST-HOUSE-WITH-A-MARRIAGE-BLOCK-EVER (it-supersedes-the-h2-P240-by-1-step!-h1-is-ACTIVE-in-the-04894-death-register-1889/1890/1904-'THE-LOWEST-house-3-death-entries'!— the-marriage-book-now-OUTRUNS-the-death-book-also-at-h1-BY-7-YEARS!-1882-vs-1889!) + witnesses-Georg-[~]-×-Nikola-[~] + THE-LESKO-cross (the-v10-witness-'Johann-Lesko-[~]'-s47!-×2-in-the-year!)",
    status: "DOCUMENTED" as const,
  },

'''

text = text.replace(anchor, SECTION + anchor, 1)
print('A1) 6-novih-blokov + komentar sekcije vstavljen')

# A2) merge-obogatitev P80-sidra h36-1882
OLD_SI = 'whatSi: "poroka (26. 11. 1882, vpis 26) — ženin Mathias Križan [~], Leinweber [~], 24, GRIBLJE 36 × Anna Matuschea [~], 18; = oče krsta hiše 36 (Dec 1886: oče Matija Križan, mati Ana roj. Milavec) — križni dokaz družine Križan na hiši 36"'
NEW_SI = 'whatSi: "poroka 26. November 1882 (vpis 26 = TAIL-1882!-P241-MERGE-z-P80-sidrom-1:1!-P238-h13-MERGE-vzorec!) — ženin Mathias HRIZAN/Križan [~DVOJNA-PRIIMKA-DUEL!-cf.-1884-v7-Hrizan?-\'Griblje-2?\'-X-OPEN!], Leinweber [~Leinweber-nit-cf.-P241-v23-nevesta-\'Leinannin\'-h10!], 24 let, GRIBLJE 36 × nevesta Anna Matuschea [~], 18 let; ★★★ h36-PREDISTOPNA-NIT-P240-IZPOLNJENA-1:1! (P240-lead-→-P241-MERGE!) + h36-continuum (1884-v18-nevesta-Anna-KRIZAN-h36-P239! + krstna-h36-križ-Dec-1886-oče-Matija-Križan-×-mati-Ana-roj.-Milavec-1:1-IZ-TEGA-VPISA!) + MEJA-1882/83 = s50-MID (tail-24–26-novembra-19./26./26.!-P240-1:1!-nato-VELIKA-glava-\'1-8-8-3.\'-razporejena-črez-stolpce!) + page-44-P80-ere-[=sken−6?]-vs-P238/239/240-pravilo-\'pag-=-sken−1\'-(s50→49)-[~X-OPEN!]"'
if text.count(OLD_SI) != 1:
    print('ABORT: OLD_SI:', text.count(OLD_SI)); sys.exit(1)
text = text.replace(OLD_SI, NEW_SI)

i = text.find(NEW_SI)
s = text.find('whatEn: "marriage (Nov 26, 1882, entry 26)', i)
e = text.find('",\n', s)
OLD_EN = text[s:e + 3]
NEW_EN = 'whatEn: "marriage Nov 26, 1882 (entry 26 = THE-1882-TAIL!-the-P241-MERGE-with-the-P80-anchor-1:1!-the-P238-h13-MERGE-pattern!) — groom Mathias HRIZAN/Križan [~the-double-surname-DUEL!-cf.-the-1884-v7-Hrizan?-\'Griblje-2?\'-X-OPEN!], a-linen-weaver [~the-Leinweber-thread-cf.-the-P241-v23-bride-\'Leinannin\'-h10!], 24 y., GRIBLJE 36 × bride Anna Matuschea [~], 18 y.; ★★★ THE-h36-PRE-STOP-THREAD-FROM-P240-FULFILLED-1:1! (the-P240-lead-→-the-P241-MERGE!) + the-h36-continuum (1884-v18-the-bride-Anna-KRIZAN-h36-P239! + the-baptism-h36-cross-Dec-1886-the-father-Matija-Križan-×-the-mother-Ana-née-Milavec-1:1-FROM-THIS-ENTRY!) + THE-1882/83-BOUNDARY = s50-MID (the-tail-24–26-of-November-19/26/26.!-P240-1:1!-then-the-BIG-\'1-8-8-3.\'-heading-spread-across-the-columns!) + the-page-44-P80-era-[=sken−6?]-vs-the-P238/239/240-rule-\'pag-=-sken−1\'-(s50→49)-[~X-OPEN!]",\n'
if not OLD_EN.endswith('",\n'):
    print('ABORT: OLD_EN'); sys.exit(1)
text = text.replace(OLD_EN, NEW_EN, 1)
print('A2) P80-sidro h36 obogateno (MERGE)')

with open(PATH, 'w', encoding='utf-8', newline='') as f:
    f.write(text)
print('ZAPISANO:', PATH)
