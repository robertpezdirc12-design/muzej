# P125 — Poročna knjiga 04455: dopolnitev 1895 (s97) + polno leto 1896 (s98–s101)

**Datum:** 2026 (faza 1 + faza 2) · **Scani:** 97–103 · **Pag. = sken − 1 (11. potrditev, velja v 61–100)**

---

## FAZA 1 — OKVIR

- Fetch `p125_fetch.py`: skeni **97–103** (97 že pričakovan kot P124 lead) → LANDSCAPE ~2510–2598×1800.
- **s97 = Pag. 96 = NADALJEVANJE 1895**: tiskana podglava brez leta + **3 zadnji vpisi 1895 (v17–v19)** — P124 je transkribiral 16 (feb–sept); 1895 ima v resnici **19 vpisov** (okt 29 + nov 10 + nov 28)! → stats.linesage: 1895:19.
- **s98 = Pag. 97 = GLAVA 1896**: rokopisno »**1896.**« (zoom cal/s98_year) + tiskana podglava tabele (Bräutigam/Braut) + v1–v4.
- s99 = Pag. 98 (v5–v9) · s100 = Pag. 99 (v10–v14) · **s101 = Pag. 100 (v15 + rokopisna glava »1897« + v1/1897!)**.
- **s103 = Pag. 102: VELIKA TISKANA GLAVA »Traunungs=« + v11/1897 (Mai 31)** — P126 lead že orisan: *Griblje 40 Nikolaus Perdinec ½ Griblar 22 × Griblje 39 Maria Simic [~] 17*.
- Kalibracija meja: `detect_lines_125*.py` (4 pragi) + `cal125*.py` + `halves125.py` + `ruler125.py` + `strips125.py` + `verify125*.py` (7 skript; 36 row-crops L/R ×2 LANCZOS).

## FAZA 2 — TRANSKRIPTCIJA (18/18 OBOJESTRANSKO)

- `crop_rows_125.py` (36 L/R) + `zoom_125.py` (~77 zoomov) + `zoom125b.py` (24 presisnih) + ročni re-zoomi (~110 slik skupaj).
- MERI konvencija; [~] za nejasna branja; Befunde-delež; priče z oklepaji »}« = skupni stand.

## NOVELE 1895-ext (v17–v19)

1. **★ P124 POPOLNJEN: 1895 = 19 vpisov** (16 + 3) — okt/nov poroke; duhovnik Jos. Rauy (3/3).
2. **★ v17 = GRIBLJE × GRIBLJE** (h24 Brinsec × h14 Perdinec) + **DISPENS №2906** (3. st. krvno; Ordinariat Laibach 7/10.) + občina Griblje **št:4 = kontinuiteta** (P124 št:1-3 maj → št:4 okt!).
3. **★ h14-1895 CROSS-LINK**: v17 par (Johann Brinsec × Maria Perdinec) = **ISTI PAR** kot krstna 04105 s85 h14 (1896): oče Janez Brinec × mati Marija Pendirec — ženin oženj v nevestino hišo (vzorec h56-1886 P80!).
4. **★ v18 = 2. REKORD-PAR LINIJE**: 59 + 50 = **109 SKUPAJ** (P123 v5: 112!) + ženin 59 = 2. najstarejši (za 64); Gradac št:22 → kontinuiteta 21→22→23 (P124→P125)!
5. **★ v19 = VORMUNDSCHAFT za 49-letnega ženina** (skrbništvo 5 dni pred poroko!) + Kauf-Brief [~] + oče = ženin (Georg Marvin ×2).

## NOVELE 1896 (v1–v15)

1. **★ ⅓ GRIBLAR = NOV ULOMEK** (5. del; P121: ¼/½/¾): v6 Kolih (oče+sin) + v10 Jakofčič (oče+sin) = 4 osebe! + **1 GRIBLAR** (cel gospodar, v2 Marenfič).
2. **★ 1. NEZAKONSKI ŽENIN POROČNE LINIJE** (v14: starši = [—] + »ledige Magd«; cf. P96 nezakonski krsti).
3. **★ 3. DUHOVNIK LINIJE** (v12: **Franz Herms, coop.**) — edina prekinitev Rauy-monopola (17/18; 4. leto zapored).
4. **★ 2. ŽANDAR LINIJE** (v4: Eduard (Hubert [~]) Röthl, **GENDARM**, 24) + **k.k. Beamte oče** (1.!) + rojen **Rudolfswert** (Novo mesto) + dokumenti **Gottschee/Adelsberg/Laibach** + pravni termin **»Indifferenz«** + ime neveste »Hanna Elisabeth« vs »Anna (Victoria)« (anomalija!).
5. **★ ŽAKANJE = HRVAŠKA** (v11: ženin iz Brod b. Žakanje + **slovensko** »otlični list župnega urada v Zakanjah«) — 3. hrvaška povezava (P120 → P124 → P125); 2. slovenskojezični Befunde-blok (P121 v9 → v11).
6. **★ »hoc« = hic commorans REŠEN** (7×: v5/v7/v8/v9/v11/v14/v15 — status-dodatek »bivajoča tu«).
7. **★ »mütterl. fürwellig«** (v7) — 1. MATICA daje privoljenje (P124: väterl. ×4); formula »in Ungarn« ×4 = ISTI ŠTEVEC kot P124!
8. **★ GROSSJÄHRIGKEIT za ŽENINA** (v3: 22 — prvič za mladoletnega ženina!) + za nevesto (v15: 21); »Klagsbefähigung zustehend« (pravno).
9. **★ DISPENS №293** (v3: 3. st. krvno — ISTA formulacija kot v17-1895!) → 2 dispensacije P125.
10. **★ MUC 3. dokaz** (v1: oče Nicolaus Muc ½ Griblar = P121 v12 ISTA oseba! + nevesta Maria Muc); PERDINEC ×11; KLEPEC ×4; ZUGELJ ×3; JAKOFČIČ ×4 (P124 priča ×2!); STRAOS ×4; Marasinič ×3; JAKŠA ×3; Kralj ×3; Butala ×4.
11. **★ Boginja vas 2×** (v8 št:15 + v13 št:43) + Otokje[~] 2× (32 + 48) + Möttling = Metlika (3. leto dokaza: v3/v8/v9).
12. **★ Občinsko številčenje 3 kontinuitete**: Griblje 1-3→4 · Gradac 21→22→23 · Podzemelj 4→6+8→4[~]→10→11→121[~].
13. Neveste z »1 Griblaršdojft.« (v2) + »¼ Griblaršbe Tojfter« (v11) + »½ Griblarin« (v12) + »Laipfleršdojft.« (v7 — LAIPFLER 5. leto!) — raznovrstnost statusov.
14. Rekord-pari: v18-1895 109 (2.) · v11 54+47 = 101 (3.) — za P123 112 (1.).
15. Taglöhner ×2 (v13/v14) + Besitzer ×2 (v12) + Bauer (v5) + Insessor (v12 priča) + **Tischlermeister** (v14 priča — 1. obrtniški mojster!).

## GEOGRAFIJA (nove vasi/občine linije)

Desinec · Zastava · Dobravec[~] · Grinostek[~] · Kapljišče[~] · Stranska vas b. Semič · Ribnik b. Kočevje · Brusnice (občina) · Apedar[~] · Dobr?melj[~] · Boginja vas · Otokje[~] · Drašiče · Cerkoviče[~] (cf. P96 Cerkvišče!) · Mavrle · Dobliče · Stopiče[~] · Petrova vas · Lomelj[~] · Kloster[~] · Žakanje (HR) · Rudolfswert (rojstvo) · Gottschee · Adelsberg · Laibach.

## EXCLUDED

0.

## NEXT

**P126 LEAD: poročna 1897** — glava + v1 že na s101; s103 = velika tiskana glava + v11 (GRIBLJE poroka: h40 × h39!); skeni 102+ še prenesti.
