# Georeferenca N83 A03/A04/A05 — poskus prek reke Kolpe (P8) — NEGATIVNI izid, dokumentiran

Cilj: georeferencirati preostale grafične liste katastrske občine Griblje
(A03, A04, A05; A01/A02 sta georeferencirani od issue #14) z **deterministično
metodo brez AI** (med blokado VLM-kvote 2026-10-08).

## Kaj DELUJE (validirano)

1. **Moderna Kolpa — centerline iz OpenTopoMap ploščic** (`kolpa-modern-centerline.json`,
   2034 točk, lat 45,49–45,63): z15, 91 ploščic; voda = modra dominanta
   (B−R > 12, B−G > 8); centerline = najdaljši povezan vodni blok (višina > 900 px),
   po vrsticah najdaljši povezan tek, center tega.
   - **VALIDACIJA proti GEOTRUTH sidrom (issue #14):** pri lat cerkve 45,5676 →
     lng **15,29866** = NATANČNO kontrolna točka A02 (»sodobna struga pri latitudi
     cerkve, OSM«); pri 45,5578 → 15,29941 (sidro A01: 15,2994). Ujemanje ≤ ~8 m.
   - opomba: tile.openstreetmap.org s sandboxa vrača VSE ploščice enake
     (6987 B = placeholder!) — zato OpenTopoMap.

2. **Kolpa ~1825 na listih — ekstrakcija** (`fit-river-georef.py`, `extract_river`):
   reka na listu = pas »prazne vode med bregovnima črtama«; po 40-px oknih:
   temnost stolpcev (prag 150), poteči ≥ 40 px med temnima bregovoma
   (breg = stolpec s temnostjo > 0,15), center = središče pasu. Na A02 da
   61 točk, center x 2780–2900 pri y 100–1400 — SKLADNO z znano lego
   (desni krak x≈2827, pas 2765–2890).

## Kaj NE DELA — merjeno na znani resnici (A02)

Podobnostna prileganja (rotacija, merilo, translacija) px→geo prek razdalj do
moderne centerline (robustno soft-L1):

| nastavitev | reka (mediana) | CERKEV px(1995,577) → EŠD 2122 |
|---|---|---|
| brez mej (θ±0,5 rad, s 0,4–2,0) | 11 m | **napaka 1,6 km** (s → 0,4!) |
| realne meje (θ ±5°, s 0,70–1,15) | 21 m | **napaka 916 m** (dN −909 m, s → 0,70) |
| fiksirano s (resnica 0,79) | 40 m | dN ≈ −204 m |
| fiksirani s ∈ {0,70…1,00}, θ=0 | 36–50 m | **s NI razločen** (inlier-mean: 0,84 → 30,5 m BESEDILO 0,79 → 31,5 m!) |

**Diagnoza:** Kolpa na tem odseku je skoraj ravnovesna S–J črta z šibkim
vijuganjem (amplituda ±400 m na 6 km) — vzorec vijug NE razloči merila ne
S–J lege. Vzhodno-zahodna kontrola je močna (dE −9…−33 m), a premalo.

Tudi medlistna ORB/SIFT registracija (P7 metoda) NE DELA za te liste:
- vse pare a01↔a02↔a03↔a04↔a05: NI resničnih ujemanj vsebine
  (a02→a4 »41 inlierjev« = LAŽNO — vsi na robu lista pri y≈0,03, marginalije;
  RMS 57 px);
- edina povezava a03↔a04 (55–88 inlierjev, rotacija ±44°) — a oba lista
  nista zasidrana; ±44° potrjuje, da ima vsak list SVOJO orientacijo snemanja.

## Kaj bi zadoščalo (za nadaljevanje, ko bo mogoče)

1. **VAČ metapodatki** (fizične mere lista / ločljivost skena) → merilo;
   VAČ s sandboxa trenutno timeout.
2. **Ena točkovna sidra na list** (poimenovan zaselek z znano lego — npr.
   napis »Adleschitz« na A04; Kurrent, potreben VLM ali človek) + reka →
   podobnost določena; pričakovana natančnost ±150–300 m [~].
3. **VLM premer listov** (kvota) ali človeške kontrolne točke (QGIS).

## Artefakti

- `tiles/` (60 placeholder OSM — dokaz blokade) + `/tmp` OTM 91 ploščic
- `kolpa-modern-centerline.json` — moderna Kolpa (validirana)
- `otm-water-mask.png` — vodna maska mozaika
- `fit-river-georef.py` — ekstrakcija + prileganje + validacija A02 (reproducibilno)

Status: **A03/A04/A05 georefStatus ostaja TO_COLLECT** — pošteno negativen izid
z dokazano diagnozo; A01/A02 (issue #14) nedotaknjena.

## P9 (2026-10-08, po dvigu VLM kvote) — A04 GEOREFERENCIRAN prek OVINA Kolpe ⭢

P8 je padel na A02, ker je Kolpa pri Gribljah preveč ravna. A04 pa vsebuje
**OVIN pri Adlešičih** (SSE→ESE, moderno (45.534, 15.304)→(45.529, 15.314)) —
odsek, ki razloči tudi smer in (delno) merilo.

### Metoda

1. **VLM ploščični sken** (`scripts/georef-tiles.mjs`, 5×4 mreža + 12 % prekrivanja,
   1,6× povečava): vsi napisi listov A02/A03/A04/A05 z relativnimi pozicijami.
   **Validacija metode na A02** (znana resnica): napis "St. Veith" px(1921,501)
   proti cerkvi px(1995,577) → odmik ~106 px (~84 m) — ploščične pozicije so
   uporabne za groba sidra [~].
2. **Identifikacija k.o. sosedov** (web): Bedenj = **Weidendorf** (Wikipedija),
   Tribuče (45.54515/15.24304), Adlešiči (45.5224/15.3110), Bedenj
   (45.53742/15.27694). Na A04: WEIDENDORF (spodaj levo), ADLESCHITZ
   (površinski, desno), seznam sosedov Grüble/Adleschitz/Zaplje v glavi.
   Na A03: razpršeni napis E-H-C-S-T-U-B-I-R-T = **TRIBUTSCH** (Tribuče).
3. **Sledenje reke na A04** (ploščično, 20 VLM klicev): desna stran + diagonala
   SW + dno → 10-točkovni konsenz (2456,743) → (1537,1947).
4. **Similarity fit** (rotacija/merilo/translacija; soft-L1, multi-start)
   proti **validirani moderni centerline** (KD-drevo, zgoščena na 3 m):

   | parameter | vrednost |
   |---|---|
   | rotacija | **+30,9°** (stabilna +21…+31° v vseh režimih) |
   | merilo | **0,55 m/px** (optimum) |
   | mediana odmika struge | **10 m** (fit), **23 m** (neodvisna točka) |
   | vogali lista | NW 45.52188/15.30202 · NE 45.52860/15.31800 · SW 45.53102/15.29420 · SE 45.53774/15.31018 |

5. **Merilo — analiza dvoumnosti** (P9b): oblika ovinka optimalna pri 0,48–0,55;
   prisiljena območja: s 0,60–0,80 → mediana 19–25 m (rotacija kompenzira).
   Neodvisni določevali: (a) širina narisane struge 120–165 px proti realni
   Kolpi 50–90 m (OTM z16, 1,67 m/px) → s 0,36–0,75; (b) kalibracija
   pretiravanja iz A02 (pas 125 px × 0,79 = 99 m narisano; realno ~60 m →
   faktor ~1,65) → s ≈ 0,45–0,65 [~]; (c) simboli hiš A04 = simboli A02
   (9×13 px) → s ≈ 0,79 [~] (metoda ±30 %, A01 kontrola odpovedala).
   **Sklep: s = 0,55 (objavljeno), poštena negotovost 0,45–0,74** → vogali
   ±250–470 m; vzdolž reke ±100–150 m (sidro).

### Napačne sledi (zavrnjene)

- "widest light band" ekstrakcija po vrsticah: zajame svetla polja med gozdnimi
  pasovi (DP sled skakalna) — zavrnjeno;
- spodnja vrstica ploščic (x 326–1224 pri y 1796–2098): pod fitom 332–625 m od
  Kolpe → ceste/dolina, ne reka;
- zgornji levi kot A04 (231,91): 1047 m od Kolpe → ne reka;
- "Bresnik" ≠ Brinsko selo (zaselek Griblj) — 4 km od fita; identiteta
  odprta [~];
- Overpass API iz sandboxa: ConnectionRefused (dokumentirano).

### A03/A05 (ostajata TO_COLLECT)

- **A03** (~sever-gor): brez reke; naselbinska veriga ~41 stavb NAVPIČNO ob
  vzhodnem robu (x ≈ 87–91 %) — skladno z nadaljevanjem vzdolžnega pasu vasi
  Griblje (Dolnje Griblje?) [~]; TRIBUTSCH = k.o. Tribuče; parc. št. 1800–1845
  ob vzhodnem robu. Ima glavo "III".
- **A05**: brez reke; sklop ~45 stavb (75 %, 28 %) z hišnimi št. (N°9) +
  vrstnimi imeni (Pri Janhovičih, Na Dvagi Žoleg, Šiže Vardianove [~]) —
  verjetno južni konec pasu vasi [~]; razpršene črke A D L E S C… zgoraj desno
  + [Vedalschitz ~] = k.o. Adlešiči; glava "V" (5. list). Simboli nakazujejo
  s ~0,66 m/px [~].
- Manjka eno točkovno sidro z znano modernim lego na vsakem listu.

### Artefakti

- `tiles-vlm/` — a02/a03/a04/a05-labels.json (ploščični skeni),
  a04-tile-river.json, a04-rivertrace.json
- `p9-fit-a04.py`, `p9b-refine.py`, `p9-dp-trace.py` — skripte
- `p9-a04-fit.json`, `p9-a04-fit2.json`, `p9b-a04-refined.json` — fiti
- `scripts/georef-tiles.mjs` — ploščični skener (ponovljiv)
- Muzej: `SHEET_GEOREFS[2]` = georef-a04 (RECONSTRUCTED), src-a04
  GEOREFERENCED, QA test `qa-p9-a04-georef` (21→22)

## P10 (2026-10-08, zvečer) — SEKCIJSKA MREŽA eZKN RAZREŠILA VSE LISTE ⭢

Ključna razkritje: **okvirne oznake listov so kode sekcija mreže 1:2880** (eZKN
pregledovalnik arhivskih načrtov GURS, sloj `GURS/EZKN_LISTI/MapServer/8000`,
uradna geometrija D96/TM). Celice ~1,9 × 1,5 km, kodirane `IX24` + 2 črki
(stolpci a–d po poldnevniku, vrstice e–i po vzporedniku).

### Preslikava listov → celice

| list | okvirna oznaka | celica | uradna geometrija (N, E) |
|---|---|---|---|
| A02 | `O.IX24cƒ` | **VKIX24cf** | 45,5572–45,5710; 15,2730–15,2975 |
| A03 | `O.IX24dɡ` | **VKIX24dg** | 45,5437–45,5575; 15,2485–15,2730 |
| A04 | `O.IX24cg` | **VKIX24cg** | 45,5436–45,5574; 15,2728–15,2973 |
| A05 | `O.IX24ch` | **VKIX24ch** | 45,5299–45,5437; 15,2726–15,2971 |

**VALIDACIJA principa list≈celica:** središče risane vsebine A02 (GEOTRUTH)
se NATANČNO ujema s središčem celice cf (~10 m). Vsebina listov = le k.o.
Griblje: A03 samo vzhodni pas (zahodni rob k.o. ob Tribučah/Bednju), A05
zgornja desna polovica (skrajni jug k.o.), A04 cela celica cg.

### POPRAVEK P9 (umaknjena georeferenca A04)

P9 je list A04 zasidral na ovinu Kolpe pri Adlešičih (rot +30,9°, s 0,55,
mediana 10 m). P10 ugotavlja, da je bila lega **NAPAČNA (~2,5 km)**:

1. **Oznaka lista `O.IX24cg`** (brana 3×: P9 nepomaknjeno + 2× ciljno) = celica
   cg = območje DIREKTNO JUŽNO od A02 — ne odsek Adlešiči;
2. **Stavbna validacija** (222 zaznanih simbolov A04 vs sodobne stavbne
   parcele GURS): P9-lega mediana **636 m** (statistična izključitev),
   celica cg 72 m;
3. **P9 kontrole so bile nedisukriminativne** — ADLESCHITZ in WEIDENDORF
   padejo v k.o. Adlešiči/Bedenj pri OBEH legah (k.o. sta veliki);
4. **P9 sled »reke«** (10 točk, širina 180 px ≈ 130 m pri 0,72 m/px) je
   najverjetneje dolina/cesta — Kolpa teče ~1,2 km vzhodno od vzhodnega roba
   celice cg, IZVEN lista A04. Prileganje oblike ovinka = zavedljiv lokalni
   optimal proste podobnostne preslikave (4 prosti parametri, 10 točk).

### Nove uradne poti (vir 2026-10-08)

- **VAČ** (vac.sjas.gov.si): enota `SI AS 176/N/N83` — k.o. Griblje št. 83,
  prejšnja signatura N083A, zgodovinsko ime **Grüble**, NATANČNO 5 listov
  (N083A01–A05) + spisovno; javno dostopno. Identiteta listov potrjena
  neodvisno (križne korelacije VAČ-predogledov ↔ naši skeni: diagonala).
  JPG tok (fileStream) zahteva prijavo — predogledi javni (520×418).
- **GURS WFS** (ipi.eprostor.gov.si): `wfs-si-gurs-kn` (KATASTRSKE_OBCINE,
  PARCELE…) + `wfs-si-gurs-rpe` (NASELJA…). Preneseno: k.o. GRIBLJE poligon
  (SIFKO 1544), 2117 parcel, 2432 parcel k.o. Adlešiči, 8 naselij.
- **eZKN** (geohub.gov.si/ghapp/ezkn): zapis **N83-1544** (»Stanje 20 —
  Franciscejski kataster ARS«) s povezavo do VAČ; javni DjVu skeni ZKN
  listov (GRIBLJE 1/2/4/K 2–3; dekodirani z libdjvulibre, 300 dpi).
- Zavrnjeno: Mapire/Arcanum (403 s sandboxa), VAC fileStream brez prijave.

### Zgodovinska ugotovitev

1825 k.o. Griblje je segala ~2,4 km DLJE na jug (do ~45,530 — območje
Fučkovcev/Dragošev/Jankovičev) kot današnja k.o. (do 45,5442) — ozemlje je
bilo pozneje priključeno k.o. Adlešiči. A05 dokumentira skrajni jug tedanje
k.o. (Flurnamen: Pri Jankovichti = današnje naselje Jankoviči ✓).

### Artefakti P10

- `gurs/` — k.o. poligoni, parcele (1544/1552), naselja, seznam k.o.
- `ezkn/` — DjVu datoteke (1544_2880_0001–0008, 1552_2880_0015)
- `p10-targeted.json` (tiles-vlm/) — ciljani VLM skeni A03/A05
- `vac-preview-*.jpg` — VAČ predogledi listov (korelacijska matrika)
- skripte: `scripts/tmp/p10-*.mjs|py` (skeni, fiti, validacije)

## P45 (2026-10-12, issue #14) — VALIDACIJA PORAZDELITVE STAVB: vse tri celične umestitve kvantitativno potrjene ⭢

Ruralni listi A03/A04/A05 nimajo točkovnih sidrov vrste cerkev/most/sotočje
(merila dokončanja #14 dopuščajo alternativno pot: vidno opombo o negotovosti
+ posodobljen geotruth.ts). P45 je izvedla tretjo pot — KVANTIFIKACIJO
 obstoječe celične umestitve z neodvisnimi podatki:

### Metoda (scripts/p45-sheet-anchors.py + scripts/p45-verify.py)

1. **KALIBRACIJA na A02** (156 stavb buildings.json = GEOTRUTH resnica):
   - resnična podobnost (z y-zrcaljenjem slika→sever): **merilo 0,805 m/px,
     rotacija +0,02°, mediana ostanka 2,4 m** — celično izračunano merilo
     (0,80) se s resnico ujema < 1 % → zanesljiv prior za sestrobdne liste;
   - izbira detektorja simbolov po F1 na 156 resnicah: **rdeče steblo**
     (R−G>28 ∧ R−B>28, 7–32×7–28 px) F1 0,56, recall@50 0,94 — bistveno
     bolje od temnih lis P10 (F1 0,35; temne lise ločijo tudi črte besedila).
2. **DETEKCIJA** na A03 (maska vzhodni pas x≥78 %), A04 (cel list), A05
   (zgornja desna polovica).
3. **Celična preslikava** (okvir lista ≈ celica eZKN) → statistika bližine
   do sodobnih stavbnih parcel GURS (< 800 m²; k.o. 1544 + 1552 = 1.500).
4. **Fitovi**: prosti (rot/merilo/translacija) in omejeni (merilo = celično
   ±5 %, rotacija = prior ±3°) z nič-testi (zasuki 90/180/270° + 30
   naključnih zamikov ±350 m) — nasičena P10 točkovalnica zamenjana z
   nenasičeno (clip(1−(d−15)/85)).
5. **Križne preverbe oznak** → naselja (point-in-polygon, pyproj D96/TM→WGS84).

### Rezultati (dokaz: p45-sheet-fits.json)

| list | simbolov 1825 | sodobnih v coni | CELIČNA mediana | inlier@30 | sklep |
|---|---|---|---|---|---|
| A03 (dg) | 30 (veriga x 86–93 %) | 51 | **89 m** | 0,067 | veriga = nadaljevanje vasi POTRJENO |
| A04 (cg) | 170 (cel list) | 440 | **69,7 m** | 0,118 | POPRAVEK P10 POTRJEN (P9: 636 m) |
| A05 (ch) | 30 (sklop x 52–86 %) | 535 | **27 m** | 0,60 | sklop Fučkovci/Jankoviči (45,5404/15,2908) |

- **Prosti fitovi ZAVRŽENI** na vseh treh listih: izboljšajo mediano le z
  nafizikalnimi parametri (A03 rot +12°/s 0,60; A04 rot +8,5°/s 0,54;
  A05 rot −16°/s 0,53) — 4 prosti parametri + 30 točk = pretreniranje
  (P9-past prepoznana in izognjena).
- **Omejeni fit**: A05 neodvisno POTRDI celično lego (Δ 64 m, mediana 23 m —
  dva neodvisna vira se strinjata); A04 izboljša mediano na 55 m a premakne
  oznako WEIDENDORF iz k.o. Bedenj → ZAVRNJEN (križna preverba zmaga nad
  15 m izboljšave); A03 slabši od celice (153 m).
- **ODPRTA DVOUMNOST A05** (dokumentirana v geotruth.ts SHEET_TRUTH + QA):
  prosta translacija najde višje ocene na VZ robu celice (0,915 pri
  45,5328/15,2974 — brez naselja, zunaj celice) — gostota sodobnih stavb
  metrike ne loči popolnoma; zavrnjeno na dokazu okvirne kode (3× prebrana),
  razrešitev čaka #12 (paleografija) / #13 (vektorizacija).
- Naselja ( centroids, WGS84): Fučkovci (45,5447/15,2947), Dragoši
  (45,5550/15,2840 — celica cg!), Jankoviči (45,5333/15,2831) — A05 sklop
  pade MED Fučkovce in Jankoviče (obmeje 1825 k.o. Griblje).

### Integracija

- `src/data/atlas/geotruth.ts` — NOV razdelek SHEET_TRUTH (3 zapisi z
  kvantificirano validacijo; tretje merilo dokončanja #14);
- `model.ts` SHEET_GEOREFS A03/A04/A05 — accuracy posodobljene iz
  »±200–400 m« na poštene ocene (±150–250 / ±100–200 / ±100–200 m) z
  P45 dokazi; statusi ostanejo REVIEW;
- `sources.ts` — placement + noteSi/En vseh treh listov dopolnjeni;
- `qa.ts` — novi test `qa-p45-sheet-anchors` (42. → 43. test).

### Artefakti P45

- `p45-sheet-fits.json` — celotni dokaz (kalibracija A02, detekcije, fiti,
  nič-testi, oznake, vogali, alternative A05)
- `scripts/p45-sheet-anchors.py`, `scripts/p45-verify.py` — reproducibilno
