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
