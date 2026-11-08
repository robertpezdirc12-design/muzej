# P134 — Župnija Podzemelj: Poročna knjiga 04455, polno leto 1905 (s125–s129 == Pag. 124–128)

**Status:** SAMPLE-TRANSCRIPTION-M1905 · **Datum:** 2026-10-24 · **20. leto poročne linije** (P115 = 1886 → … → P134 = 1905) · **issue #18**

## Okvir

- **s125–s129 == Pag. 124–128** (Pag. == sken − 1, **20. zaporedna potrditev**; velja 61–128).
- **ROKOPISNA GLAVA »1905.« POTRJENA na s125** (P133-lead) + velike tiskane glave »Traunungs=Buč.« na s126/s127/s128/s129 + **ROKOPISNA GLAVA »1906« na s129** (P135 LEAD — 1906 v1–v4 že videni!).
- **P134-lead KOREKCIJE**: »min 5 vpisov s125–s126« → **17 vpisov s125–s129** (3× podcenjeno); »v2 Griblje 39 Markočič?« → **v2 = Griblje 34 Johann KAMBIČ** + **v4 = Griblje 24 Mathias BRNC** (lead-v2 je bil v resnici v4!).
- **1905 = 17 vpisov OBOJESTRANSKO** = 16. januar + 20. februar ×2 + 27. februar ×2 + 6. marec ×2 + 8. maj + 15. maj ×2 + 22. maj ×2 + 29. maj ×2 + 3. julij + 31. julij + 7. avgust.

## Metoda

- Skeni 127–130: `fetch134.py` (+129–130 za mejo — lekcija 2 skenika naprej!) → `crop_rows_134.py` (34 izrezov: L x 0–1250, R x 1300–W, 2× LANCZOS, ločene L/R y-meje po P131-lekciji).
- Meje vrstic: `detect134.py`/`detect134b.py` (temni pasovi, stolpci 430–560 L + 1900–2100 R) + **ravnila** `ruler134.py` (grid s250–300 vsakih 25px, oznake vsakih 100px) — vizualna kalibracija L: s125 [589/1085/1283/1560], s126 [246/587/880/1300/1556], s127 [246/579/980/1217/1558], s128 [246/513/724/949/1312/1618], s129 [246/599]; R zamik +6…+21px.
- Mikro-zoomi ×3–8: `zoom134.py` (~25) — v1-vas 8×, v2-priče/Befunden, v4-status/hiši/starost 8×, v5-priče, v6-ime/status, v7-vas/status/bride-status, v8-Befunden 4×, v9-občina/Sodja, v10-vas 8×/ime/priimek-L, v11-, v12-hiša 7×/vmet, v14-ime/hiša-korekcija 7×, v16-nevesta ×3, v17-ime 7×/oče 7×.

## Ključne rešitve

1. **★ 11/11 PONEDELJKOV = 100%** — 1. popolno leto linije (P133 13/15, P132 ponedeljkovski vzorec!).
2. **★ RAUY 17/17 = 100%** — 3. popolno leto (P129 8/8, P130 11/11); kariera ≈ 66/72.
3. **★ 3 HIŠE Z 2 BLOKI V ENEM LETU = NOVI REKORD**: h24 (**BRATA BRNC** — v4 Mathias 21 + v12 Johann 24, isti starši!) · h34 (**BRAT-SESTRA KAMBIČ** — v2 ženin Johann + v13 nevesta Maria, isti starši = vzorec P132 h11!) · h1 (2 nevesti Željko v15 Maria + v17 Barbara — ⚠️ 2 različna Nicolaus-očeta!).
4. **★ 3 JURAJEVČIČ-ženińi v 3 tednih maja** (v8 Johann 27 Otok 11 + v9 Johann 28 Kapljiše? 6 + v11 Michael 27 Krasinec 21?).
5. **★ 1. AMERIŠKI DRŽAVLJAN LINIJE** (v8): »Ženin je Ameriški državlan« — konzul ZDA v Trstu, sporočilo 27.3.1905: »da ni denarnega zadržka za ženitev« — NOV dokument-tip (konzularno sporočilo!).
6. **★ 2 DISPENSI 3. KOLENA**: v7 (ordinariat 28.1. № 342) + v9 (ordinariat 9.5. № 1816 — 6 dni pred poroko!) — vzorec 1890 (2 dispensaciji).
7. **★ 1. SCHMIEDMEISTER-ŽENIN × 1. SCHMIEDMEISTERS-WITWE** (v16): Anton Strugar 24 (Črnomelj 158!) × Maria Pabič? 25 (Gradac 27) — obrtniški par (kovač × kovačeva vdova); oče Jakob Strugar **Wagner-Meister** = 2. dokaz P130!
8. **★ VMET nem. k.k. Landesregierung für Krain № 15129** (v12): »dass der Taufname des Brunc richtig Anna lautet« [~] — 1. nemški vmet poročne linije.
9. **★ 6 KONTINUITET**: h18 SIMEC 1897→05 (**8 let + isto ime Mathias!**) · h27 KUČAR/KUKAR 1897→05 (8 let, dve pisavi!) · h44 ŠTRUCELJ 1903→05 · h65 MÜCK/MILEK 1903→05 (dve pisavi!) · h1 ŽELJKO 1899→05 (×2!) · h30 4. dokaz.
10. **4 MENJAVE DRUŽIN**: h24 Brišec?→BRNC ×2 · h30 LEGINA→Grabrijan · h34 FILAK/ŠILAK→KAMBIČ ×2 · h10 KURE→PERDINEC (vzorec h22 STRAUS→MILEK 1904!).
11. **★ v14 KOREKCIJA V VPISU: hiša 34 PREČRTANO → 35** (zoom 7×!) — h35 = **1. poročni dokaz = EDINA nova hiša 1905** (brez korekcije bi h34 imel 3 poroke v letu!).
12. **Formula REŠENA**: »očetovo ustno dovoljenje za ml. nevesto **v navzočnosti zgornjih prič**« (v3 explicitno → v2/v5/v8/v9/v12 rešeni!).
13. **★ v2: 1. SKUPNI STATUS PRIČ** ({ ½ Hübler za OBE priče [~]) + v15: dovoljenje za ml. **ŽENINA** (19!) + polnoletnost ×5 (v1 + v17 ZA OBA!).
14. **NOVE VASI/HIŠE**: Škrilje? 1 [~] · Kapljiše? 4+6 [~] · Gakova? 3 draga Virodina? u Croatien [~ — 2. hrvaški vpis, vas potrjena ×2 v Befunden!] · Metlika 36 (mesto!) · Črnomelj 158 (mesto! najvišja!) · Gradac 27 · Otok 11+20 · Krasinec 21?+22+6 · Dobravice 16 · Zastava 7 · Vranoviče 14 · Priložje 26 · Primostek 8+17 · Cerkvišče 4+9.
15. **NOVI PRIIMKI**: SLOBODNIK (v6 — 'Skobernik?' misread rešen!) · Strugar · Plut · Urbanek (hrvaški) · Kapuršinič? [~] · Pabič? [~] · Šešak · Jötter? [~] · Segna? [~] · Ramuta [~] · Hojrič [~] · Malevič [~] · Marantič? [~] · Vergane? [~] · Grabek? [~] · Štonic? [~] · Zahorič? [~] · Sodja? [~] + **KUKAR 2. dokaz priimka** (P133 v11 mati Anna Kukar [~] → zdaj družina: oče Johann Kukar h27!).
16. **1. pisava »Liubljani« za Laibach** (v4 deželna vlada!) — slovenizacija urada.
17. **statusi**: »¼ gbl.Pofu?« [~] ×2 (v4+v14; cf. P135-lead v4!) · »griblarst.Hofe/Hofsa?« [~] ×4 · »griblarin« ženska forma (v10!) · Besitzerssohn (v6) · Schmied-Meister (v16) · Bauernsohn (v10) · Wagner-Meister (v16 oče).

## Mreže 1905

- **JURAJEVČIČ ×3 ženińi** (v8/v9/v11!) + priči Marcus (v8) · **MILEK ×3** (v1 Muek/Mue + v12 Catharina + v13 mati Anna) · **KLOBUČAR ×2** (v5 mati Agnes + v17 mati Catharina) · **KRIŽAN ×3** (v7 + v14 nevesti + v15 mati) · **HARAŠINIČ ×3** (v10 oče+priča + v17 priča) · **STRAUSS ×3** (v7? status + v11 priča + v14 mati) · **ŽELJKO ×3** (v15 + v17 nevesti + v15 priča Georg) · **POŽEK ×2** (v2 priča + v12 mati) · **DRAGOŠ ×2** (v2 nevesta + v13 priča) · **BRNC ×4** (v2 mati + v4 ×2 + v12 ×2) · **KAMBIČ ×4** (v2 + v13 + starši ×2) · **PERDINEC ×6** (v4 oče+priča + v8 nevesta+oče + v10 mati? + v14 ženin+oče) · **KURE ×3** (v7 ženin+priča + v17 mati) · **GRABRIJAN ×2** (v4 nevesta + v15 priča) · ŽUNIČ (v15) · KLEPEC (v13) · BRODARIČ (v2 + v11 priča) · NOVAK (v7) · MUE/MUEK (v1 ×3 + v9 priča).

## Anomalije (13) + nejasnosti

- A1 lead-korekcije (min 5→17; v2-lead je bil v4!) · A2 v1 vas »Germ 26« [~] · A3 3 hiše z 2 bloki (rekord!) · A4 JURAJEVČIČ 2 Georga? (polbrata?) · A5 v10 oče Harašinič? ≠ hči Moravec · A6 v12 nemški vmet № 15129 »Anna« [~] · A7 v14 korekcija 34→35 · A8 »Pofu?« status ×2 · A9 »Hofe/Hofsa?« ×4 · A10 v2 skupni status prič · A11 h10 KURE→PERDINEC menjava · A12 v11/v12 zglasmnica št: 4 dual-občina isti dan? [~] · A13 2 Nicolaus Željko-očeta (v15/v17).
- NEREŠENO [~]: v1 vas Germ; v7/v9 Kapljiše; v10 Gakova/Virodina identifikacija; v12 vmet-subjekt; status Pofu; v16 Pabič/Babič; v17 Hukav/Kukar pisava.

## Pag. == sken − 1

20. zaporedna potrditev: s125→124 · s126→125 · s127→126 · s128→127 · s129→128 (velja 61–128).

## P135 LEAD

- **poročna 1906**: rokopisna glava »1906« na s129 + **v1–v4 že vidni**: v1 Jän 15 **Djelonia? 1 u Kroatien** (3. hrvaški vpis!) Frana Martinkovič? Beizgerssohn? 31 × Gajiče 35 **Catharina Simec ¼ Mückbrin** 24 · v2 Jän 29 Krasinec 25 **Nicolaus Brodnič? 49 = NAJSTAREJŠI ženin od 1902-Legina 43!** × Krasinec 12? Margaretha Šurbaern? wtw 33 (VDOVA!) · v3 Jän 29 Krasinec 18 Nicolaus Županič 40 × Krasinec 35 Anna Vrdomari? wtw 23 (2. VDOVA — 2 v 2 dneh!) · v4 Febr 12 Ojerm? 23 Nicolaus Perdinec? × Gradac 6 Maria Kreivelin? 24.
- MEJA: preveriti s130 + s131 (lekcija!). Skani 129–130 v .p126tmp.
