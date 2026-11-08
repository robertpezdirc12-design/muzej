# Georeferenca zemljevida 1812 — dokazna pot (P6 + P7)

Zemljevid: **»Provinces Illyriennes Servie et Bosnie 1812«** (Giraldon, 1812, javna last).
List, ki ga `MAP_1812` v `src/data/atlas/research.ts` citira kot obdobjeni izvirnik
(potrjen tudi v dlib ref. 6EZTJ9C0 / ZRC SAZU 2012).

## P6 — georeferenca prvega skena (Commons 8297 × 6080)

Deterministična metoda (0 AI-klicev):

1. `orig-1812.jpg` — prenos s Commons (Special:FilePath).
2. `ocr-full.tsv` — tesseract PSM 11, cel list (39 s) → 423 besed; izluščene
   kandidatne kontrolne točke.
3. `crops/` + `crops2/` — ciljani izrezi (3×/4×/6×) pričakovanih mest →
   cele besede mestnih oznak.
4. `fit-georef.py` — 15 kontrolnih točk → LSQ **afina** in **kvadratna 2. reda**
   px→WGS84; `affine-{prelim,robust,final}.json`, `fit-compare.json`.
5. `georef-1812.json` — končni rezultat; `griblje-okolis-1812*.jpg` — dokazni
   izrez ± 63 km z oznako (v zbirki MVG-092).

Rezultat P6: merilo 126 × 124 m/px (razmerje 1,024), residuali mediana 10,1 km
(max 25,0), **Griblje px (2499, 2286) ± ~10 km**, pokritje ~11–24°E / 41–48°N.

## P7 — koroboracija na drugem skenu (Internet Archive 7636 × 5936)

Vprašanje: *je rezultat P6 lastnost LISTA ali artefakt skeniranja prve datoteke?*
Odgovor: neodvisen knjižni sken istega lista (IA `dr_provinces-illyriennes…`,
Lapie/Malte-Brun/Chamouin/Giraldon — isti graver; potrditev v `periodOriginals`).

1. `orig-1812-second.jpg` — prenos (Commons mirror IA datoteke).
2. **Slikovna registracija** (`regis-orb.json`): ORB (~30 k značilk/sken) +
   BFMatcher ratio-test + RANSAC afina sken1→sken2 → **4030/4670 inlierjev,
   RMS 3,9 px**; merilo 0,8187/0,8148, rotacija ~0,3°. Oba skena = isti list,
   povezana skoraj-similariteto.
3. **OCR drugega skena**: napovedane lege oznak (iz registracije) → ozki izrezi
   (3–8×, CLAHE/OTSU/erode) → `scan2-labels.json`: **12 oznak** prebranih v
   drugem skenu (5 celih besed: Pest, Nissa, WIDDIN, Raguse, Semlin;
   7 fragmentov: Bel, Prist, Agr, icone, eobern, aye, wor). Nissa (Niš) je
   NOVA točka, ki je ni v modelu prvega skena. `crops5/` — 12 končnih izrezov.
   Laibach/Fiume/Trieste/BanyaLuka v knjižnem skenu NEberljivi (pregibi zvezka).
4. `fit-georef-second.py` — neodvisen 12-točkovni LSQ geo-model drugega skena
   → `georef-1812-second.json`.

### Ključno merilo — sporazumenje o legi Gribelj

| pot | veriga | Griblje px (2. sken) |
|---|---|---|
| **A** | geo → model 1. skena⁻¹ → (2499, 2286) → registracija | **(2513, 2003)** |
| **B** | geo → model 2. skena⁻¹ (neposredno, lastni OCR) | **(2489, 2032)** |

**|A − B| = 37 px = 5,6 km** — znotraj ± 10 km negotovosti P6.
→ Georeferenca NI artefakt skeniranja; lista je res skoraj izotropna
(2. sken: 151 × 152 m/px, razmerje 0,998; 1. sken 1,024 — razlika ~2 %
je znotraj merilne negotovosti modelov).

Drugi sken sam: residuali mediana 9,7 km (max 22,2); **samo cele besede 6,2 km**
— inherentna točnost metode »center napisa« je ~6–10 km, kar pošteno
dokumentira [~] status.

## Reproducibilnost

```
python3 research/georef-1812/fit-georef.py         # P6 (predpogoj: orig-1812.jpg)
python3 research/georef-1812/fit-georef-second.py  # P7 (predpogoj: regis-orb.json, scan2-labels.json)
```

Status vsega: **REVIEW [~]** — kontrolne točke so centri OCR-anih NAPISOV
(ne mestnih pik); mrežne stopinje strojno neberljive (Parisov meridian
nepotrjen); končna potrditev = človeška paleografija ali QGIS georeferenciranje.
