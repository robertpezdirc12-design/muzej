# Muzej vasi Griblje — digitalni muzej vasi ob Kolpi

Večjezični digitalni muzej resnične vasi v Beli krajini (občina Črnomelj, Slovenija).
Zbirka: **114 zapisov** s trajnimi muzejskimi številkami (MVG-001 → MVG-114), **601 dokazljivih virov**,
lestvica zanesljivosti, odprti podatki in časovnica od prve omembe vasi leta **1468**.

## Značilnosti

- **Muzejski register** — celotna zbirka z iskanjem, filtri po zbirkah (Kraji, Kolpa, Narava,
  Delo in obrt, Šege in tradicija, Vojna in meja) in po stopnji zanesljivosti
- **Zapis eksponata** — status dokaza, "Kaj vemo" / "Kako vemo", življenje predmeta
  (črta umetnine po vzoru Art Tracks), viri, zgodovinske trditve, citat, postaja sprehoda
  in sorodni zapisi
- **Časovnica** — zapisi po obdobjih od 1468 do danes
- **Zgodbe in načela** — kuratorska besedila; **Dogodki** — kronika živih dogodkov
- **Dvojezičnost** — slovenščina / angleščina prek moje povezave `?exponat=<slug>`
- **Temni način** — spoštuje sistemsko nastavitev
- **Odprti podatki** — `/api/exhibits`, `/api/events`, `/api/opendata` (JSON, CC BY-SA 4.0)

## Tehnologija

- [Next.js 16](https://nextjs.org) (App Router, Turbopack) + TypeScript
- Tailwind CSS 4 + shadcn/ui komponente + Lucide ikone
- Framer Motion animacije
- Pisave: Fraunces (razstavna) + Geist Sans / Mono
- Podatki: statični JSON v `src/data/museum/` (brez zunanje baze)

## Zagon

```bash
bun install
bun run dev        # http://localhost:3000
```

## Struktura podatkov

| Datoteka | Vsebina |
|---|---|
| `src/data/museum/exhibits.json` | 114 zapisov (naslovi, povzetki, zgodbe, viri, koordinate) |
| `src/data/museum/events.json` | 11 dogodkov |
| `src/data/museum/meta.json` | metapodatki muzeja, lestvica zanesljivosti, 6 zgodb |
| `src/data/museum/extra.json` | postaje življenja, trditve, sorodni zapisi, postaje sprehoda |
| `public/images/authentic/` | 103 fotografije z navedbami avtorjev: 101 citira 106 zapisov zbirke (5 si deli dveh zapisov), 2 uporablja Atlas 1812 |

## Licenca

- Vsebina zbirke: **CC BY-SA 4.0**
- Zemljevidski podatki: © OpenStreetMap prispevali
- Slike: licenca posamezne slike je navedena v zapisu (Wikimedia Commons in javni viri)

## Provenanca

Spletišje je bilo obnovljeno iz zadnjega delujočega produkcjskega deploymenta
(2026-10-06 11:32 UTC) po incidentu z neavtoriziranim dostopom do GitHub računa.
Vsa vsebina, besedila, viri in slike izhajajo iz izvirne zbirke.

## Povezava GitHub → Vercel

Produkcija teče na Vercelu: **https://griblje-museum.vercel.app**

| Plast | Stanje |
|---|---|
| Repozitorij | `robertpezdirc12-design/muzej` (zasebni, veja `main`) — vsebina identična produkciji |
| Primarni deploy | ✅ **Vercel GitHub App** (povezana 10. 10. 2026 prek Settings → Git; `productionBranch=main`) — vsak push na `main` samodejno zgradi produkcijo na strani Vercel, **brez žetona `VERCEL_TOKEN`** |
| Rezervni deploy | `.github/workflows/deploy.yml` — samo ročni (`workflow_dispatch`, zavihek Actions → *Deploy na Vercel (rocni rezervni)* → Run workflow). Namen: padec git integracije, preizkus žetona ob rotaciji. Push-sprožilec je namenoma odstranjen (dvojni deploy bi na Hobby čakal v vrsti) |
| Skrivnosti (samo za rezervo) | `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` kot šifrirane GitHub Actions skrivnosti; obnovitev žetona: `scripts/renew_vercel_token.py` (libsodium) |
| Zdravje žetona | `token-health.yml` preverja žeton dnevno (06:12 UTC): avtentikacija + obseg ekipe; ob napaki komentira na issue #6 |

**Kako preveriti uspešno objavo:** GitHub status commita (kontekst *Vercel*) mora po pushu
preiti v `success` (*Deployment has completed*). Kadar vidite `failure`
(*Deployment was blocked*), gre za zavrnjeno gradnjo — najpogostejši vzrok je past
avtorstva spodaj. Neodvisna kontrola: `GET /api/qa` na produkciji
(HTTP 200 = vsi testi zeleni) in Vercel dashboard.

> **⚠️ Past pri commitih (Hobby + zaseben repo):** Vercel na Hobby načrtu za
> zasebne repozitorije zahteva, da je **avtor deployanega commita lastnik ekipe**
> (dokumentacija: *troubleshoot-project-collaboration*). Peskovniški
> `Z User <z@container>` povzroči `BLOCKED (TEAM_ACCESS_REQUIRED)` —
> **potrjeno z incidentom 10. 10. 2026** (commit `396a709`, deploy `dpl_3r4DBvP…`:
> GitHub status *failure — Deployment was blocked*; naslednji commit z lastnikovo
> identiteto se je uspešno uveljavil). Pred vsakim commitom v novi seji:
> `git config user.name "Robert Pezdirc" && git config user.email "robert.pezdirc12@gmail.com"`

### Ročni deployment (iz klona repozitorija, rezerva)

```bash
git clone https://github.com/robertpezdirc12-design/muzej.git
cd muzej
npx --yes vercel@latest deploy --prod --yes \
  --token="$VERCEL_TOKEN" \
  --project=griblje-museum \
  --scope=robertpezdirc12-designs-projects
```

#
## ATLAS 1825 (GitLab issue #2)

Zgodovinska katastrska slika vasi (franciscejski kataster, k.o. Griblje št. 83 / Grüble):

- **arhivski viri** — Arhiv RS, fond SI AS 176/N/N83, 12 enot javno dostopnih prek
  [VAČ](https://vac.sjas.gov.si) (listi A01–A05, skica, opis meje, seznam parcel,
  stavbni protokol 1825, abecedni lastniki, raba, cenilni elaborat) — izračunani
  inventar stanja: `/api/atlas` → `inventory` (issue #4);
- **georeferencirana lista** A01 in A02 kot slikovni prekrivki nad OSM (Leaflet),
  prosojnost 0–100 %, cerkev sv. Vida kot kontrolna točka (VERIFIED);
  A03–A05 so umesčene približno po sekcijski mreži eZKN (GRID_APPROX, ±200–400 m);
- **register hiš 1–98** (80 prebranih zapisov, status REVIEW — Kurrent rokopis),
  lastniki (navzkrižno PT × PUA), parcelni sklici;
- **vektorizacija** 156 objektov ~1825 iz lista A02 (RECONSTRUCTED);
- **dokazni vmesnik**: vir → trditev → dokaz → povezave (N083PT str. + VAČ povezave);
- **pokritost + negativni rezultati** — raziskovalna provenienca vključno s statusi
  VERIFIED/DOCUMENTED/REVIEW/RECONSTRUCTED/APPROXIMATE/TO_COLLECT/NOT_FOUND;
- **strojni prepis PS + sprava (P36–P45)** — 135 strani, 2743 vrstic; deterministična
  sprava: glavni niz 1889/2505 (75,4 %), Waldung 81, nadaljevalni niz 95 (do 2840),
  Blatt X 60 = register stavbnih mest; razdvojitev v model parcela×raba: 2134 vnosov,
  2632 parov, 430 parcel z več rabami, 7 sirot, klasifikacija rab (pravilnik v2,
  83,5 % parov — 12 nespremenjenih v1 pravil + 13 priloženih, izrecna ločitev
  TOPONIM/ARTIFAKT/NEKLASIFICIRANO, 16 neznanih družin z so-odvisnostnimi dokazi);
  rekapitulacija str. 140–143 spravljena s modelom: 102 + 2505 = 2607
  (rdeči tuš) == kontrolna vsota sprave, Blatt X 60/102 (vrzel 42); paleografija
  str. 140–143 (12 VLM prehodov + izrezi): **"Area der Gemeinde" 1220 Joch 1493
  Klafter** (rdeči tuš) — prvič ujeta skupna površina občine, aritmetično zvezana
  (1215|490 + 5|1003 = 1220|1493), 7 Grundstückslagen (hiše 124–130) vsota 831|702
  == "Summa der Grundparzellen"; model GRUND Δ +0,99 % (izboljšava P40 +1,39 %);
  dokaz `research/issue17/ps-reconciliation.json`
  + `research/issue17/ps-landuse.json` + `research/issue17/ps-recap.json`
  + `research/issue17/ps-recap-paleo.json` + `research/issue17/ps-landuse-v2.json`
  + `research/issue17/ps-lexicon.json` + `research/issue17/ps-k1k2.json`
  + `scripts/p38_ps_reconcile.py` + `scripts/p39_ps_landuse.py` + `scripts/p40_ps_recap.py`
  + `scripts/p41_ps_recap_paleo.py` + `scripts/p42_ps_rulebook_v2.py`
  + `scripts/p43_ps_lexicon.py` + `scripts/p44_ps_k1k2.py`; razcep K1/K2 (P44)
  RAZREŠEN [~]: paralelnost "nach Anlage" (desna vrstica 4 == leva 132; Joch 831 == 831)
  → K1 = 702, K2 = 2090 − 702 = 1388 == direktno branje pass2 — celoten Abschluß
  zaprt (831|702 + 383|1388 = 1215|490; + 5|1003 = 1220|1493); verifikacija
  leksikografskih virov (P45): 49 tarč, 0/70 hipotez potrjenih v celoti (33
  NEPOTRJENIH, 7 DELNO, 17 NEVERIFIKATORNO, 13 BREZ-VIRA) — trije DWB citati
  zvezkov napačni (Lohn Bd 16→12, Höfling Bd 13→10, Efeu Bd 6→3), SSKJ
  refutacije z verbatim definicijami, atribucije (Kärntner WB "Schulz 1972",
  Bezlaj SSN/SLA) zavrnjene; dokaz `research/issue17/ps-lexicon-verified.json`
  + `scripts/p45_lex_verify.py`;
- **neatline georeferenciranje sekcij dg/cg/ch (P46, issue #14)** — narisana
  neatline franciscejske sekcije = meja sekcije eZKN 1:2880; uradna geometrija
  celic (GURS) znana → preslikava px ↔ WGS84 brez prostih parametrov; princip
  kalibriran na A02 (GEOTRUTH, EŠD 2122): residuala 9,3 in 13,2 m; A04 in A05
  zasidrani 4/4 strani (merilo 0.7727–0.7765 m/px, medosna konsistenca 0,5 %,
  afina RMS 0,1 m), A03 delno (S/E detektirana, N/W preko skupnega merila) —
  **±40–50 m namesto ±200–400 m**; ne-regresija 7/7 P10 kontrolnih napisov
  (Bresnik/Fučkovci/Jankovichti 33–34 m); SHEET_GEOREFS namerno nespremenjen —
  predlog nadgradnje čaka človeško potrditev črt (lekcija P9); dokaz
  `research/issue17/neatline-georef.json` + `scripts/p46_neatline_georef.py`;
- **GURS parcel overlay (P47, issue #14)** — neodvisna validacija neatline
  afin z zunanjim virom: sodobne parcele (GURS eZKN WFS; KO 1544 + KO 1552,
  EPSG:3794 → WGS84) preslikane prek P46 afin pasti na narisane črte 1825 z
  mediano residuala **5.6–9.8 m** (p90 ≤ 13.7 m; kontrola metode na A02 pod
  GEOTRUTH: 9.8 m); pokritost črnila 0.44–0.55 nad kontrolami-zamiki (0.19–0.47),
  pri poravnavi strmi (0.71–0.86); land-use dokaz: 394/559 parcel na A05 = 
  skupna paša **WAIDENDORF** v 1825 (EMPTY stratum); 16 dokaznih izrezov za
  človeško potrditev črt (`research/issue17/neatline-crops/`); SHEET_GEOREFS
  še naprej namerno nespremenjen (lekcija P9); dokaz
  `research/issue17/gurs-overlay.json` + `scripts/p47_gurs_overlay.py` +
  `scripts/p47_fetch_ko1552.sh`;
- **stavbni overlay (P48, issue #14)** — most PUA↔PT↔PS↔GURS: sodobni stavbni
  tlorisi (GURS eZKN WFS `SI.GURS.KN:STAVBE`, OBRIS_GEOM; KO 1544 401 + KO 1552
  južni bbox 313) preslikani prek GEOTRUTH mej A02 / P46 afin pasti na narisane
  stavbne simbole 1825 — **A02: 149/154 stavb on-symbol** (cov@best mediana 1.0),
  mediana residuala **9.8 m** (p90 13.7 m) — stavbna raven potrjuje parcelno
  (P47: 9.8 m); **A05 Fučkovci 26/95, residual 10.1 m**; A04/cg 0 on-symbol
  (sodobne stavbe na paši WEIDENDORF so novejše); kontinuiteta A02: 37 parov
  tloris↔stavba (36 strong), **136/156 tlorisov 1825 brez naslednika**
  (razpršena zidanica — vinice/hambi na zahodnih pobočjih) — nadgradja P16
  present.json; **Blatt X (str. 138–139): direktna referenca na register 1825
  REFRIRANA** (0/37 identičnih površin; površine vrstic mediana 6.3 J vs
  dvorišča 0.28 J) — kvantitativna poprava P42 interpretacije; 12 dokaznih
  izrezov (`research/issue17/buildings-crops/`); SHEET_GEOREFS in dokazi
  P40–P47 nespremenjeni; dokaz `research/issue17/buildings-overlay.json` +
  `scripts/p48_buildings_overlay.py` + `scripts/p48_fetch_stavbe.sh`;
- **Fučkovci 1825 (P49, issue #14)** — delna vektorizacija A05: celtna
  vektorizacija tlorisov NI izvedljiva (rožnati fill siva ~169 < 195,
  zasičenost maske 40.3 % v vasi — izmerjeno); namesto tega tri neodvisna
  dokazna sloja: **modern-anchored 26 mest** (25 v sklopu, residual 9.8 m,
  WGS84 v izpisu), **striktna detekcija temnih jeder** (53; 7 koreliranih,
  19 neujemanih v sklopu — triaža: 2 stavbi + 4 nejasni GONE-kandidati [~]),
  **obseg sklopa** (lupina 36 336 m², masa črnila 257 571 px); ocena stavb
  [27, 44] — P10 ~45 znotraj mej, brez protislovja; ohranjenost ≥ 0.806 [~];
  9 izrezov (`research/issue17/fucukovci-crops/`); dokaz
  `research/issue17/fucukovci-1825.json` + `scripts/p49_fucukovci1825.py`;
- **Georef zapora A03–A05 (P50, issue #14)** — aktivacija P46 neatline afin v
  SHEET_GEOREFS na 5 neodvisnih plasti dokazov (neatline kalibriran na A02
  9,3/13,2 m; parcele P47 9,8/5,6/9,3 m; stavbe P48 149/154 + 26; sidro P49
  43,2 px; napisi 7/7): **GRID_APPROX ±200–400 m → NEATLINE ±40/50 m** (A03
  PARTIAL 2/4 strani; A04/A05 4/4), premik mej le 17,4/16,9/18,0 m
  (konvergencija mreže), merilo 0,7746 m/px; **5/5 listov serije
  georeferenciranih**; vizualni pregled izrezov priporočen [~]; dokaz
  `research/issue17/georef-closure.json` + `scripts/p50_georef_closure.py`;
- **Leaflet overlay A03–A05 (P51, issue #14)** — listi A03/A04/A05 kot
  slikovne prekrivke na atlasu: ovoj skena NEODVISNO preračunan iz P46 afine
  (== P50 boundsImageNWSE ≤ 5e-6° — ni ročno prepisanih koordinat);
  MERJENA SUBTELNOST pošteno dokumentirana: Leaflet ne podpira rotiranih
  prekrivk — odmik vogalov osne postavitve ≤ 19,3/20,0/20,0 m (dva vogala
  točna), del ±40/50 m negotovosti lista; skew ≤ 0,5708°; stikala privzeto
  IZKLOPLJENA, črtkani neatline okvirji s statusom, skupna prosojnost; dokaz
  `research/issue17/leaflet-overlay.json` + `scripts/p51_leaflet_overlay.py`;
- **Rekonstrukcija GitHub↔GitLab (P52, issue #17 — sync dolg)** — združitev dveh
  vzporednih linij (merge-base P37): GitHub linija (11.10.) je prispevala 3. prehod
  PS (233 VLM branj, PS-full-v2.json 2974 vrstic, odkritje Blatt I–X), strukturno
  rekonstrukcijo (33 segmentov, 29/29 dokaz), prvo celotno verigo PT→PUA→PS
  (chain-full-pt-ps.json), PZ tabele cenilnih razredov (71/71 strani,
  PZ_CLASS_TABLE_1825, 76 VLM klicev) in validacijo porazdelitve stavb A03–A05
  (SHEET_TRUTH — zgodovinski neodvisni dokaz; runtime georef od P50 neatline);
  GitLab linija P38–P51 ostaja avtoritativna za georef in spravo. QA 52 → **57**
  testov (5 GitHub-unique testov adaptiranih na spojeno stanje).
- **globa povezava** `?atlas=hiša-75` (hiša št. 73 — demonstracijska veriga do MVG-010).

API (statični, brez runtime AI):

- `GET /api/atlas` — celoten podatkovni model (JSON, provenienca vključena);
- `GET /api/atlas/geojson` — prostorski sloji (GeoJSON, CRS84);
- `GET /api/atlas/integrity` — test povezav hiša ↔ parcela ↔ lastnik ↔ vir (9 preverjanj);
- `GET /api/atlas/ps-landuse` — spravni model rabe tal PS 1825 (parcela×raba, P39);
- `GET /api/atlas/ps-recap` — rekapitulacija str. 140–143 vs spravni model (P40);
- `GET /api/atlas/ps-recap-paleo` — paleografija str. 140–143: Abschluß der Gemeinde (P41);
- `GET /api/atlas/ps-landuse-v2` — pravilnik rab v2: 83,5 % parov, TOPONIM/ARTIFAKT ločitev,
  16 neznanih družin z dokazi (P42);
- `GET /api/atlas/ps-lexicon` — neznane družine: prečni prehodi (DINGF 10/10 stabilna,
  padci Wiese/Acker→specifično), PV območna sprava (Weiden-gap 576,24 J; Area ≈ P41),
  leksikografske hipoteze z nepreverjenimi viri (P43);
- `GET /api/atlas/ps-k1k2` — razcep K1/K2 v Abschlußu RAZREŠEN [~]: paralelnost
  "nach Anlage" → K1 = 702, K2 = 1388 == branje pass2; Abschluß popolnoma zaprt (P44);
- `GET /api/atlas/ps-lexicon-verified` — verifikacija leksikografskih virov P43:
  49 tarč, 0/70 potrjenih (33 NEPOTRJENO, 7 DELNO, 17 NEVERIFIKATORNO, 13 BREZ-VIRA);
  DWB zvezčne natančnosti, SSKJ verbatim refutacije, atribucijske zavrnitve (P45);
- `GET /api/atlas/neatline-georef` — neatline georeferenciranje A03–A05: princip
  "neatline = meja sekcije eZKN" kalibriran na A02 (9,3/13,2 m); A04/A05 zasidrani
  ±40 m, A03 delno ±50 m (iz ±200–400 m); 7/7 P10 validacij; predlog nadgradnje (P46).
- `GET /api/atlas/gurs-overlay` — neodvisna validacija neatline afin prek sodobnih
  parcel (GURS eZKN WFS, KO 1544 + KO 1552): mediana residuala 5.6–9.8 m, p90 ≤ 13.7 m;
  strata DRAWN/EMPTY (WAIDENDORF skupna paša 1825); 16 dokaznih izrezov; status ANALYSIS
  — človeška potrditev črt še pred nado (P47).
- `GET /api/atlas/buildings-overlay` — stavbni overlay: sodobni stavbni tlorisi
  (GURS eZKN WFS) ↔ stavbna mesta 1825; A02 149/154 on-symbol (residual 9.9 m),
  A05 Fučkovci 26/95 (10.1 m); kontinuiteta 37 parov, 136/156 tlorisov brez
  naslednika; Blatt X: direktna referenca REFRIRANA (0/37); 12 izrezov; status
  ANALYSIS-DETERMINISTIC (P48).
- `GET /api/atlas/fucukovci-1825` — Fučkovci 1825: modern-anchored mesta (26,
  25 v sklopu, residual 9.8 m) + striktna temna jedra (53, triaža) + obseg
  sklopa (lupina 36 336 m²); ocena [27, 44] vs P10 ~45; 9 izrezov; status
  ANALYSIS-DETERMINISTIC (P49).
- `GET /api/atlas/georef-closure` — georef zapora A03–A05 (P50): aktivacija
  P46 neatline afin v SHEET_GEOREFS — 5 neodvisnih plasti (L0 kalibracija A02
  9,3/13,2 m; L1 parcele 9,8/5,6/9,3 m; L2 stavbe 149/154 + 26; L3 sidro
  43,2 px; L4 napisi 7/7); GRID_APPROX ±200–400 m → NEATLINE ±40/50 m;
  premik mej le 17,4/16,9/18,0 m; 5/5 listov georeferenciranih;
  status ACTIVATED-DETERMINISTIC.
- `GET /api/atlas/leaflet-overlay` — Leaflet overlay A03–A05 (P51): ovoji
  skena neodvisno preračunani iz P46 afine (== P50 boundsImageNWSE ≤ 5e-6°),
  odmiki osne postavitve ≤ 20 m (dva vogala točna — Leaflet brez rotacij),
  skew ≤ 0,5708°, PIL dims + sha256 slik; UI stikala privzeto izklopljena;
  status UI-ACTIVATED-DETERMINISTIC.
- **present.json na uradnih GURS obriseh (P54, issue #12 nadgradnja)** — P16
  »Kaj je izginilo?« nadgrajeno z OSM posnetka (15/26/115, pokrival le jedro
  vasi) na **uradne GURS eZKN obrise** (380 stavb v oknu A02 + sodobna vas,
  vse KO 1544 — popolna pokritost z zahodnimi pobočji razpršene zidanice);
  pravila P16 nespremenjena, **kalibrirana z replajo na starih podatkih
  (156/156)**; rezultat **18 obstaja · 21 negotovih · 117 ni jih več**
  (7 tlorisov spremenilo status); d zapisana za vseh 156 (do 1541.2 m);
  P48 navzkrižje: cf 154 == modernEvaluated, pari ≤ 25 px 37 == pairs;
  arhiv P16 `research/issue17/present-osm-p16.json`; dokaz
  `research/issue17/present-gurs.json` + `scripts/p54_present_gurs.py`;
  QA 57 → **58**; SHEET_GEOREFS in dokazi P40–P53 nespremenjeni.

- **geolokacija Grundparzellen (P55, issue #13)** — protokol PS
  »Der Grund-Parcellen der Gemeinde GRÜBLE« (2505 + 102 = 2607) prvič
  GEOLOCIRAN: **1110 vrstic (40.2 %) povezanih s sodobnimi parcelami
  k.o. 1544 po ohranjeni parcelni številki** (delitve po 1825 = base +
  pripona, 241 skupin); vztrajnost oštevilčenja 1825→2026 dokazana z
  dvema neodvisnima testoma — (A) površine: median modern/QK **3.6984 ≈
  1 Wiener QK 3.59665 m²** (Δ +2.83 %; premešana kontrola 3.9731, pas
  ±10 % 16.9 % vs 4.0 %), (B) prostorska soslednost: **590 zaporednih
  parov 51.8 m narazen** (naključno 1436.9 m — 27.8×; 89.3 % ≤ 150 m);
  zaupanje vrstic STRONG 171 / MEDIUM 775 / WEAK 164, per-parcelno [~];
  odkritje sekcije »Furkofze« (Fučkovci): 2 vrstici, parceli 2159/2160,
  lastnik Van Wawech Mihó — prvi imenovani Fučkovci v arhivu; dokaz
  `research/issue17/ps-parcels-geo.json` + runtime
  `src/data/atlas/ps-parcels-geo.json` (`/api/atlas/ps-parcels-geo`) +
  `scripts/p55_ps_parcels_geo.py`; QA 58 → **59**; SHEET_GEOREFS in
  dokazi P40–P54 nespremenjeni.

- **topologija registra PS (P56, issue #13)** — register NI homogen:
  **S1** glavni register (str. 5–127, per-Blatt številčenje, 41–2500),
  **S2** spremembni register (str. 128–137, št. 2507–2840 kot prebrano;
  dodatki z anmerkung — »einf. Vermessung vom Jahr 1805, bezogen vom Hof
  Nr 1003«, »Grundsteuerkataster 1841« — register vzdrževan do 1934:
  584 označenih vrstic, pik 1841 s 83 vrsticami na 44 straneh),
  **S3** zapadek »Zusammenstellung der Grundstücke« (str. 138–139, LASTNO
  oštevilčenje 1–100; pass2/pass3 razhajanje [1..40] vs [421..440]),
  **S4** rekapitulacija; **SANACIJA P55**: 43 S3 vrstic lažno povezanih
  (median razmerja površin 0.0892 ≪ 3.7188 — ~42× od 1 Wiener QK
  3.59665 m²; + P48 Blatt X koroboracija) — sanitiran join **1110 → 1067
  vrstic, 800 → 774 base** (št. 1–40: str. 3–4 niso v P38 izboru branj);
  per-Blatt dvoumnost MERJENO (brez prerazporeditev): **515 base na več
  straneh** (475 znotraj S1), 512 vrstic dvoumnih [~]; sodobna praznina
  **0 parcel 2507–2607** (87 PS dodatkov brez naslednic) proti 53 base /
  78 parcelam 2608–2700; P55 runtime nespremenjen (pini qa-p55);
  dokaz `research/issue17/ps-register-topology.json` + runtime
  `src/data/atlas/ps-register-topology.json`
  (`/api/atlas/ps-register-topology`) + `scripts/p56_ps_register_topology.py`;
  QA 59 → **60**; SHEET_GEOREFS in dokazi P40–P55 nespremenjeni.

- **začetek registra PS (P57, issue #13)** — strani 3–4 (številke 1–40, Blatt I),
  ki jih P38/P56 izbora nista vključili, ZDAJ prebrane s **štirimi neodvisnimi
  plastmi** (polna stran ×3, kolone Haus Nro. ×3 iz 3× izrezov — polnostransko
  branje je mešalo dvomestne številke s črkami, izrezi površin ×3 z LCS
  poravnavo, tarčne celice 6× za 10 spornih vrednosti z odločanjem) in
  deterministično adjudicirane; **veriga Blatt I 1–60 zaprta** (committed
  ps-005 začne 41); join po mehaniki P55 **obnovi 26/26 izgubljenih base P56**
  (edini vir teh številk je bil zapadek str. 138–139): 25 s pari površin —
  median modern/QK **3.7594 ≈ 1 Wiener QK 3.59665 m²** (Δ +4.53 %; kontrola
  seed 42 = 3.2098, 2.4× dlje od konstante; pas ±10 % 16 % vs 6.2 %) + številka 1
  (celica površine prazna); **soslednost** 19 parov median **81.2 m** (kontrola
  seed 7: median 263 m, MIN 126 m > opaženi — Monte-Carlo 100 %); zaupanje
  **STRONG 3 / MEDIUM 14 / WEAK 9**; **14 upokojenih številk** (12, 14, 24, 25,
  27–30, 32, 34, 37–40 — brez sodobne naslednice, konsolidacija [~]); r1/r28
  prazni; Fürtrag vsotni vrsti delno berljivi [~]; P55/P56 runtime nespremenjena
  (pini qa-p55/p56); dokaz `research/issue17/ps-register-start.json` + runtime
  `src/data/atlas/ps-register-start.json` (`/api/atlas/ps-register-start`) +
  `scripts/p57_ps_register_start.py`; QA 60 → **61**; SHEET_GEOREFS in dokazi
  P40–P56 nespremenjeni.

- **sanacija produkcije PS-PARCELS-GEO (P58, issue #13, v2)** — v1 produkcija
  (1110 vrstic) je vsebovala **43 lažnih povezav S3** (zapadek str. 138–139), ki
  jih je P56 dokazal (površine ~42× od 1 QK + pass-razhajanje): P58 jih je
  odstranil iz runtime-a (**nabor bajtno enak P56 kontaminacijskemu seznamu**) in
  **dodal 26 Blatt I vrstic** iz primarnega vira P57 (točno vseh 26 lostBases) →
  **1093 vrstic / 800 pozicioniranih števil**; vsaka vrstica zdaj nosi serijo
  (BI/S1/S2) in per-Blatt dvoumnost (**211 base / 495 vrstic** [~]); KLJUČNA
  LASTNOST: pozicije so per base, zato je **soslednost bajtno enaka v1**
  (590 parov / 51.8 m / 27.8×) in S1/S2 zaupanje nespremenjeno
  (**STRONG 174 / MEDIUM 759 / WEAK 160**); **površinski median čist 3.7709**
  (Δ +4.85 % — v1 3.6984 je bil umetno snizan; skladno z neodvisnima merjenjema
  P56 3.7394 in P57 3.7594); v1 dokaz arhiviran nespremenjen + v2Delta zgodovina;
  dokaz `research/issue17/ps-parcels-geo-v2.json` + runtime v2
  `src/data/atlas/ps-parcels-geo.json` (`/api/atlas/ps-parcels-geo`) +
  `scripts/p58_ps_parcels_geo_v2.py` (`--check` bajtno); QA 61 → **62**
  (qa-p55 prepisan na v2 + novi qa-p58: v1 arhiv + delta == P56 + dve obliki
  po P53/P57 lekciji); SHEET_GEOREFS in dokazi P40–P57 nespremenjeni.

- **glave listov registra PS (P59, issue #13)** — stolpec **»Nro. des Blattes«**
  prvič zanesljivo prebran: levi izrez vseh 135 strani (5–139) × 2 neodvisna VLM
  prehoda + **25 arbitraž agent-oči** na 3× izrezih (stari P38 blatt stolpec
  potrjeno šumen — p12 ditto prebrano kot 20× 'I'); STRUKTURA: **Blatt I =
  parcele 1–800** (str. 3–40; prehodna cona 721–800 s popravki I→II [~]),
  **Blatt II se začne pri 801** (str. 43–92; p72 = Blatt III 1281–1302 vmes;
  cona 1100–1640 prepletena z lokalnimi sekcijami 161–180/601–620/921–960; p101
  z ulomki 196½); **per-Blatt ločitev 211 dvoumnih base v2 MERJENA**: 106 čez
  ≥2 Blatta (P39: ista številka pod različnima Blattoma = druga parcela),
  **17 ruleCandidate** (edina instanca v pasu razmerij [0.8, 1.25] — npr. 163:
  Blatt I @ 7.0 vs Blatt II @ 0.981 ≈ 1 QK) — kandidati za P60; **join v2
  NESPREMENJEN** (meritve brez prerazporeditev); pokritost S1 123/123 × 2, S2
  6/10, S3 0/2 (VLM kvota 429 — odprto); dokaz
  `research/issue17/ps-blatt-headers.json` + runtime
  `src/data/atlas/ps-blatt-headers.json` (`/api/atlas/ps-blatt-headers`) +
  `scripts/p59_ps_blatt_headers.py` (I1–I9, `--check` bajtno); QA 62 → **63**;
  SHEET_GEOREFS in dokazi P40–P58 nespremenjeni.

- **per-Blatt atribucija ruleCandidate (P60, issue #13)** — P59 pravilo pasu
  [0.8, 1.25] **IZVEDENO**: vsaka od 17 ruleCandidate base dobi instanco v
  pasu kot attributedBlatt (**II 12 · I 1 · III 4**, 23 vrstic; npr. 163 →
  Blatt II @ 0.9813 — 4 kulture na 61/83/84/86 — vs Blatt I @ 7.0 @ p11);
  **soslednost-kontrola 21/23** (671/934 [~] — prečrtane vrstice);
  **strukturni prinos**: pas-strani (36, 49, 61, 83–87, 94, 99) nosijo 100 %
  več-stranskih base — **Kultur-Tabellen re-listing** [~]; unit-semantics
  opomba: pas ujema modo B (ratio ≈ 1, n=62), ne modo A (≈ 3.59665 = 1 QK →
  m², n=226) — absolutna korespondenca ODPRTA, atribucija = relativa [~];
  **join v2 NESPREMENJEN** (izpisi brez pozicij/površin, sha256 pinan); dokaz
  `research/issue17/ps-perblatt-attribution.json` + runtime
  `src/data/atlas/ps-perblatt-attribution.json`
  (`/api/atlas/ps-perblatt-attribution`) +
  `scripts/p60_ps_perblatt_attribution.py` (I1–I7, `--check` bajtno);
  QA 63 → **64**; SHEET_GEOREFS in dokazi P40–P59 nespremenjeni.

- **unit-semantics moda B (P61, issue #13)** — odprta točka P60 #1
  ("kolonialna enota ali delna površina?") **MERJENO RAZREŠENA s
  preusmeritvijo**: moda B (ratio ≈ 1, n=62, 42 strani, Blatt II 32 · IV 15 ·
  III 9 · I 5; bloki 3/9) ni napaka ujeme in ni delna površina (samo 2 base z
  ≥2 B vrsticami) — je **dosledna drugačna registracijska konvencija**
  (številka ≈ sodobna meritev v m²); **permutacijska kontrola** na GURS
  parcelah KO 1544 (2117 parcel, deterministične FNV-1a točke bajtno enake
  Python/TS, radija 50/100 m, pas ±25 %): moda A real @50 0.9248 vs perm
  0.1637 (ujeta = prava parcela), moda B real @50 0.2903 vs perm 0.1774 →
  **H1 napačni številčni join ZAVRŽEN**; identiteta enote ODPRTA [~];
  pas pravilo P59/P60 = moda B — atribucija relativa smiselna; **join v2
  NESPREMENJEN**; dokaz `research/issue17/ps-unit-semantics.json` + runtime
  `src/data/atlas/ps-unit-semantics.json` (gursCompact za produkcijo
  preracun) (`/api/atlas/ps-unit-semantics`) +
  `scripts/p61_ps_unit_semantics.py` (I1–I9, `--check` bajtno);
  QA 64 → **65**; SHEET_GEOREFS in dokazi P40–P60 nespremenjeni.

- **glave listov PS — polna pokritost (P62, issue #13)** — odprta točka
  P59/P61 ("13 manjkajočih branj ob kvoti 429") **IZPOLNJENA**: kvota
  premagana, vseh 13 VLM branj dopolnjenih (133–136, 138–139 × 2 prehoda +
  p137 pass2) → pokritost **135/135 strani × 2 neodvisna prehoda**; arbitraža
  oči == VLM 100 % na vseh 7 novih straneh (p133 = V s korekcijo 'IV.V',
  p134 = IV + korekcije II.IV/III.IV, p135 = IV/III/II, p136/137 = II,
  p138 neberljivo [?], p139 = 'Nro. des Hauses.' → P58 open #6); **konec
  registra (p133–137) nosi eksplicitne korekcijske cone IV→V/II** (rdeči
  tuš); čez-Blatt base **106 → 110**, 211 multi-page in **17 ruleCandidate
  nespremenjeni** → P60 atribucije bajtno identične; moda B blattDist
  **null 5 → IV +4 / II +1** (II 32 · IV 15); veriga re-run P59→P60→P61
  (`--check` bajtno PASS vsi); QA pine posodobljeni (65/65);
  dokaz+runtime `ps-blatt-headers.json` + `ps-unit-semantics.json`
  posodobljeni; SHEET_GEOREFS in join v2 nespremanjeni.

## Varnost

Žeton `VERCEL_TOKEN` je shranjen izključno kot šifrirana GitHub Actions
skrivnost in ni v repozitoriju. Datoteki `.gitignore` in `.vercelignore`
preprečujeta prenos `.env*` in lokalnih datotek pri deployu.

- **zaključne strani registra PS — Blatt IIb (P63, issue #13)** — rep
  registra (138–139) paleografsko zaključen s 3 neodvisnimi prehodi (VLM 2×
  + agent-oči na izrezih 4×–5×; 2-od-3 konsenz, 42 flagov [~]): **p139 =
  Blatt IIb** (pod-list NOV v strukturi) s parcelami 41–60 (duplikat Blatt I
  številk) + lastninske kolone — Haus Nº rdeče, **'Vor und Zuname' =
  številke 62–80 (ne imena)**; desna stran = kultura rekapitulacija 81–100 /
  Classe 101–120; **KOREKCIJA: prejšnja očesna razlaga 'Nro. des Hauses.' =
  očesna napaka** (glava je 'Nro. des Blattes.') — **P58 open #6 ZAPRT**;
  p138 = izbrisana leva tabela + 'Zusammenstellung der Grundstücke' (Wiese
  1–20); vsote 82|81, 125|183, Fürtrag 189|1228, 162|1447 (enote odprte
  [~]); veriga re-run P59→P60→P61 (`--check` bajtno PASS; I8 pin
  efe39f41…); `scripts/p63_ps_tail_pages.py` (I1–I10, `--check` bajtno) +
  API `/api/atlas/ps-tail-pages` + kartica P63; QA 65 → **66/66**;
  SHEET_GEOREFS in join v2 nespremanjeni.
- **razširitev per-Blatt atribucije na 110 čez-Blatt base (P64, issue #13)** —
  odprta točka P60/P62 #7 z merjeno hierarhijo pravil (deterministično, brez
  AI ob delovanju): **R1** pas [0.8, 1.25] = P60 (17 base, bajtno) · **R2a**
  area-dominanca ≥ 0.75 (53: II 29 · III 11 · IV 5 · I 4 · V 4) · **R2b**
  ena-Blatt-s-površino (1: 1605 — II 2688 QK, IV brez areaQK [~]) → **71/110
  atributiranih** (Blatt II 42 · III 15 · I 5 · IV 5 · V 4); **39 split**
  (delež 0.5–0.75: II 19 · III 9 · IV 6 · V 4 · I 1) z alternativami po
  deležih — za lastniško odločitev o per-Blatt SPLIT joinu; konsistenca
  R1↔R2 15/17 (2 merjeni divergence: 930, 671 [~]); občutljivost praga 0.75
  (24 @ ≥0.9 … 69 @ ≥0.6 od 92); soslednost 186/216 (R1 21/23 kot P60);
  `scripts/p64_ps_attribution_ext.py` (I1–I8, `--check` bajtno PASS; sha
  pini vhodov po lekciji P9) + dokaz `research/issue17/ps-attribution-ext.json`
  + API `/api/atlas/ps-attribution-ext` + kartica P64; QA 66 → **67/67**;
  join v2 in SHEET_GEOREFS nespremanjeni.
- **polna per-Blatt atribucija — 101 single-Blatt več-stranskih base (P65,
  issue #13)** — odprta točka P64 #3 izpolnjena (deterministično, brez AI ob
  delovanju): 101 base, katerih vse vrstice nosijo strani ISTEGA Blatta, dobi
  ta Blatt kot attributedBlatt (status **R3-single** — trivialno in nedvoumno:
  I 3 · II 26 · III 14 · IV 58; 205 vrstic — 98 × 2 + 3 × 3; vse z izmerjeno
  površino) → **pokritost več-stranskih base POPOLNA: 211/211** (110 čez-Blatt
  iz P64 bajtno + 101), skupaj **172 atributiranih** (Blatt II 68 · IV 63 ·
  III 29 · I 8 · V 4) + 39 split z alternativami — za lastniško odločitev o
  per-Blatt SPLIT joinu; **polna pokritost registra**: 800 base × 1093 vrstic
  = 589 single-page (implicitno prek strani: I 145 · I·II 10 · II 183 · III 28
  · IV 205 · V 18) + 211 multi-page; 0 vrstic brez atribucije; soslednost
  375/425 (R3 189/209); `scripts/p65_ps_attribution_full.py` (I1–I8, `--check`
  bajtno PASS; 5× sha pini vhodov po lekciji P9) + dokaz
  `research/issue17/ps-attribution-full.json` + API
  `/api/atlas/ps-attribution-full` + kartica P65; QA 67 → **68/68**;
  join v2 in SHEET_GEOREFS nespremanjeni.
- **split decision pack — 39 split base (P66, issue #13)** — priprava za
  lastniško odločitev o per-Blatt SPLIT joinu (odprta točka P64 #8;
  deterministično, brez AI ob delovanju; NE odloča namesto lastnika —
  MERI in DOKAZUJE dejstva): 39 base × 2 deleža, 93 vrstic (25 × 2 +
  13 × 3 + 1 × 4); Blatt pari I·II 7 · II·III 21 · II·IV 2 · IV·V 9
  (sosednji 37, skok 2: 1603/1604 — isti kulturi); **lastniki per Blatt
  DISJUNKTNI 39/39** (2–3 edinstvenih: 25/13/1) — močan dokaz, da je
  ista številka pod različnima Blattoma 2 RAZLIČNI realni parceli;
  dominantni deleži [0.50,0.60) 23 · [0.60,0.70) 11 · [0.70,0.75) 5;
  kulture 92 z razčlenitvijo per Blatt; **GEO 39/39: ena geometrija
  joina v2 na vseh vrsticah** (na nivoju številke — SPLIT bi zahteval
  2 geometriji); areaSuspect 0; sosledje split del 82/93 (flag 11 —
  5 base); `scripts/p66_ps_split_pack.py` (I1–I8, `--check` bajtno
  PASS; 3× sha pini vhodov po lekciji P9) + dokaz
  `research/issue17/ps-split-pack.json` + API
  `/api/atlas/ps-split-pack` + kartica P66; QA 68 → **69/69**;
  join v2 in SHEET_GEOREFS nespremanjeni.
- **forenzični paket anomalij — skok II·IV, flagi, disjunktnost (P67, issue #13)** — štiri merjena
  dela nad odprtimi točkami P66/P64/P65 (deterministično, brez AI ob delovanju; v2 NESPREMENJEN):
  **(A) skok II·IV = artifakt DVOJNE Kurrent zamenjave** — p78 (Wüstung Pod Grabino) prave
  1501–1520 (strip 2× bajtno, vrstice 5–14 rdeče prečrtane, kontinuiteta 1461→1520, karta:
  1461–1500 ima 12 poligonov / 1121–1200 PRAZNO), p93 prave 1901–1920 (karta: blok 1901–1907 =
  TOČNO 7 prečrtanih poligonov; P38 napaki 9→0 in 9→6), p87 prave 1681–1700 (pass1 661–680 =
  izguba vodilne 1 + 8→6; 11 vrstic z LAŽNO geometrijo == p36) → 1603/1604/1605/661/671 = lažne
  fuzije: skok IZGINE, čez-Blatt primera RAZPADETA; renumerifikacija 17 preslikav (0 kolizij) =
  P68; projekcija base 802, multi-page 208; **(B) 5 sosledje flagov = artefakt obsega joina** —
  manjkajoči sosedje obstajajo v registru (P38 z imeni), brez poligonov v karti; 1820/2140 na
  prejšnjih straneh (meja strani); 11/11 razloženih; **(C) R1↔R2: 671 RAZREŠENA** (II instanca
  @p87 = 1691), 930 [~] z merjenim dokazom; **(D) univerzalna disjunktnost lastnikov per Blatt
  110/110** čez-Blatt base (39 split == P66 bajtno, 71 atributiranih 71/71) — per-Blatt številčenje:
  ista številka pod različnima Blattoma = 2 RAZLIČNI realni parceli;
  `scripts/p67_ps_anomaly_forensics.py` (I1–I8, `--check` bajtno PASS; 28× sha pini vhodov po
  lekciji P9) + dokaz `research/issue17/ps-anomaly-forensics.json` + API
  `/api/atlas/ps-anomaly-forensics` + kartica P67; QA 69 → **70/70**; join v2 in SHEET_GEOREFS
  nespremanjeni.
- **v3 sanacija številčenja + sistemski pregled pass1 slojev (P68/P69, issue #13)** — P68 je IZVEDEL 17 preslikav P67 specifikacije (p78 160x→150x, p93 160x→190x, p87 661–680→1681–1700; 0 kolizij; re-join: 14 vrstic izpada, p93 3× re-claim 1903/1904/1905) → v3 = 1079 vrstic / 798 base / 199 multi-page / 98 cross-Blatt, join ključi sanirani, registrska branja nespremenjena, veriga re-run P59–P67 s posodobljenimi pini; P69 je nato z OČESNO forenziko (22 strani p73–93 + p99; 4× široki izrezi + 7×–8× zoomi + kontinuiteta + karta + P56 annRecords zamiki + hišne številke + površinska razmerja) razrešil odprto točko P68 #3: stari P38 pass1 sloji = sistematski digitalni artefakti (p74 1121–40 je pravzaprap 1421–40 4→1, p79 1821–42 = 1521–40 5→8, p80/p81 16xx = 15xx 5→6, p82 1681–1700 = 1581–1600 s 16 izgubljenimi vrsticami, p88 721–740 = 601–620 +120, p89/p90 19xx = 9xx fantom-1, p92 990–1008 = 981–1000 +9, p99 921–40 = 1921–40 −1000 zrcalno) — **77 renum preslikav (0 kolizij) + 98 rejoin kandidatov = spec P70**; 5 lokalnih sekcij (p83/p84/p86 161–180 ×3, p85 641–660, p88 601–620; 56 vrstic) = dokazane lažne fuzije na Blatt I poligone (hiše p85 r641 Hi16 vs p35 Hi68; Σ ratio 161 = 235.65×) — exclude/per-Blatt = lastniška odločitev;
  `scripts/p69_ps_pass1_layers.py` (I1–I6, `--check` bajtno PASS) + dokaz `research/issue17/ps-pass1-layers.json` + API `/api/atlas/ps-pass1-layers` + kartica P69; QA 71 → **72/72**; join v3 nespremanjen (spec čaka izvedbo).
- **izvedba P69 specifikacije — v4 sanacija (P70, issue #13)** — P70 je IZVEDEL P69 specifikacijo kot mehanski izvod (deterministično, brez AI ob delovanju): **77 renum preslikav** (bajtno po P69 renumSpec; konec lažnih fuzij cone p73–93/p99: p74 1121–1140→1421–1440 4→1, p76 1161–1180→1461–1480, p79 182x→152x 5→8, p80/p81 16xx→15xx 5→6, p89/p90 19xx→9xx fantom-1 — 9 dolgi ascender ≠ vodilna 1, p92 990–1008→981–999 +9, p99 921–940→1921–1940 Blatt III zrcalno; parzella ostaja originalno branje) **+ 95 rejoin vrstic** iz starih P38 slojev po P55 metodi (sloji po P69: pass1-pravilen p74/82/89/90/91, P38 izbira sicer; 3 kandidati p80 1541–1543 brez vira [~] — p1 odrez blok 62–81) **+ 29 preslikanih izpada** (base brez PF poligona); **33 fuzij isti-Blatt dokumentiranih** (register vsebuje 921–1000 v dveh blokih: p49–52 »glavni tek« + p89–92 »stolpec« — SPLIT join = lastniška odločitev); v4 = **1145 vrstic / 878 base / 215 multi-page / 79 cross-Blatt**; površine median 3.8843 ≈ 1 Wiener QK 3.59665 m² (Δ +8.0 %, kontrola 4.2701); soslednost 654 parov / 52.0 m / 27.6×; zaupanje 188/797/160; **56 sekijskih vrstic (p83–86, p88) nespremenjenih** — exclude ali per-Blatt instance = lastniška odločitev; veriga P59–P67 skript --check PASS (P69 klasifikacija zamrznjena na v3 dokaz);
- **korekcije v4 — sekcije exclude + p93 reverzija (P71, issue #13)** — C1: 56 sekijskih vrstic (p83–86, p88) EXCLUDE iz joina (P69 dokazane lažne fuzije; lastniška odločitev; 0 poligonov ostane praznih) + C2: P68 renum p93 160x→190x OVRŽEN z notranjo glifno forenziko (r9=1609/r19=1619: 6 ≠ 9; kontrole p98/p92) + annRecords anotatorja (1601–1619) + pageMap — 15 vrstic base := parzella, PF 1603/1604/1605 dobijo prve vrstice, 12 izpadlih; **v5 = 1077 vrstic / 879 base / 184 multi / 48 cross**; area median 3.9052 (Δ +8.58 %); soslednost 652/51.8/25.5×; forenzika research/issue17/p93-forensics/; skripta p71_ps_v5_sections_p93.py --check PASS; veriga P59–P67 PASS, P69 zamrznjen, P70 dokaz bajtno;
- **dvojnosti registra — 135 isti-Blatt dual base (P72, issue #13)** — odločitveni paket za isti-Blatt SPLIT joina (P70 »SPLIT = LASTNIKA« razširjen na cel register; razširitev P66 cross-Blatt vzorca; NE odloča namesto lastnika — MERI in DOKAZUJE; **v5 join nespremanjen**): base z vrsticami na ≥ 2 straneh ISTEGA Blatta z DISJUNKTNIMI lastniki med straneh — **135 base × 274 vrstic** (2 tri-zapisni; + 2 nearDual 2080/2081 izključeni); stranski pari delijo iste številčne razpone po P56 pageMap (p23/p24 = 401–420 obe, p51/p91 = 961–980 obe, p103/p118 = 2001–2020 obe …) z odmiki po blokih konsistentnimi (**40 × 44 · 15 × 49 · 5 × 29 · 1 × 13**) = **dvojni zapis iste serije v dveh blokih registra**; hišne številke različne 130/135; Σ areaQK blok A 128 125 / blok B 145 057 QK; **P70 33 kolizij = podmnožica** + 11 starih p51×p91 (v2 era) + 91 dozdaj neopaženih; opcija A (drop drugi blok po C1 vzorcu): 137 vrstic izpada, 0 base brez vrstic, rows 1077 → 939, multi 50, cross 48 nespr.; opcija B (per-page instance) zahteva georef Blattnih kart [~]; opcija C (re-renum) neodločljiva; **odločitev LASTNIKA**;
  `scripts/p72_ps_dual_pack.py` (I1–I9, `--check` bajtno PASS) + dokaz `research/issue17/ps-dual-occurrence-pack.json` + runtime `src/data/atlas/ps-dual-occurrence-pack.json` + kartica P72; QA 74 → **75/75**; v5 runtime join NESPREMENJEN (sha256 pin I9).
- **isti-Blatt SPLIT opcija A — v6 (P73, issue #13)** — izvedba C3 iz P72 dual pack (lastniško soglasje 2026-10-15; P70 »SPLIT = LASTNIKA« razširjen na cel register): za **135 dual base** (lastniki med straneh disjunktni 135/135; P70 33 kolizij = podmnožica: p89 × 15, p90 × 10, p92 × 8) so vrstice drugega bloka izpadle iz joina — **drop 137 kombinacij = 138 vrstic** (keep = min stran »glavni tek«; vrstice ostanejo v registru brez geometrije) — **v6 = 939 vrstic (34.0 %) / 879 base / multi 184 → 50 / cross 48**; serije S1 847 / S2 66 / BI 26; zaupanje 174/629/136; dvoumnost 50/100 (135 True→False po P55 metodi); area median **3.8941** (Δ +8.27 %, kontrola 4.5766); soslednost 652/51.8/25.5× nespremenjena; nearDual 2080/2081 ostanejo; 0 base brez vrstic; v5 arhiviran (v5Delta + v6Delta = nasledstvo);
  `scripts/p73_ps_v6_split_a.py` (I1–I8, `--check` bajtno PASS) + dokaz `research/issue17/ps-parcels-geo-v6.json` + runtime `src/data/atlas/ps-parcels-geo.json` (version 6) + kartica P73; QA 75 → **76/76** (nova qa-p73-v6-split: celoven neodvisen preracun + nil-claim).
- **cross-Blatt dvojnosti registra — 48 čez-Blatt base (P74, issue #13)** — odločitveni paket za cross-Blatt SPLIT joina (odprta točka P73 ①; P66 vzorec re-izpeljan iz v6 univerzuma; NE odloča namesto lastnika — MERI in DOKAZUJE; **v6 join nespremanjen**): 48 base z vrsticami na ≥ 2 RAZLIČNIH **sosednjih** Blattih — **48 base × 96 vrstic, točno 1 vrstica per Blatt 48/48**; pari **I·II 13 · II·III 16 · III·IV 1 · IV·V 18** (sosednji 48, skoki 0); **lastniki med Blatti DISJUNKTNI 48/48** (0 prekrivanj; P66 v v3: 36/36) — jedro paketa; pageMap prekrivanja razponov 48/48 (p11 I 161–183 / p61 II 161–180; p64 II 1821–1840 / p94 III 1821–1841; p110 IV 2141–2160 / p125 V 2141–2160) = dokaz ponovitve numeracije per Blatt; hišne številke **42 različne · 2 isti (161, 174) · 4 brez** (2611–2616); Σ areaQK per Blatt I 1874 / II 11364 / III 18300 / IV 13257 / V 13118 QK; pasovi [0.50,0.60) 8 · [0.60,0.70) 5 · [0.70,0.75) 8 · **≥0.75 27** (P66 kriterij <0.75 bi pokril samo 21); **opcija A1** (keep dominant Blatt): drop 48, rows 939 → 891, multi 2, cross 0, ambRows 4; **opcija A2** (keep min Blatt) enaki števci, različen keep pri 29 — izbira pravila **LASTNIŠKA**; evolucija P66 → v6: **17/36 ostaja · 19 odhaja** (C1 5 · C3 13 · C2 1) · **31 novih**;
  `scripts/p74_ps_cross_blatt_pack.py` (I1–I9, `--check` bajtno PASS) + dokaz `research/issue17/ps-cross-blatt-pack.json` + runtime `src/data/atlas/ps-cross-blatt-pack.json` + kartica P74; QA 76 → **77/77** (nova qa-p74-cross-blatt: celoven neodvisen preracun cross seta × P59 × P66 pack); v6 runtime join NESPREMENJEN (sha256 pin I9).
- **cross-Blatt SPLIT opcija A1 → v7 (P75, issue #13)** — izvedba C4 iz P74 odločitvenega paketa (lastniška odločitev 2026-10-15; opcija A1 = privzeta pot — **keep DOMINANT Blatt po Σ areaQK; ties 0**; vzorec P72→P73): za **48 cross base** (vrstice na ≥ 2 sosednjih Blattih; lastniki med Blatti disjunktni 48/48; ista številka pod dvema Blattoma = 2 realni parceli) je vrstica ne-dominantnega Blatta izpadla iz joina — **drop 48 kombinacij = 48 vrstic** — **v7 = 891 vrstic (32.3 %) / 879 base / multi 50 → 2 / cross 48 → 0** (NIL-CLAIM kontrola: cross set na v7 == prazno); dvoumnost 100 → 4 (48 True→False po P55 metodi); zaupanje 172/588/131 (0 sprememb); serije S1 803 / S2 62 / BI 26; area median **3.8102** (Δ **+5.94 %**, kontrola 4.1435; 871 parov); soslednost 652/51.8/25.5× nespremenjena; 0 base brez vrstic; opcija A2 bi pri **29 base** obdržala drugo vrstico; opcija B (per-Blatt instance + razdelitev geometrije) zahteva georef Blattnih kart [~]; vrstice ostanejo v registru brez geometrije (removedRows 48); ohranjene vrstice bajtno == v6 (P9); v6 arhiviran (v5Delta + v6Delta + v7Delta = nasledstvo 1145 → 1077 → 939 → 891);
  `scripts/p75_ps_v7_cross_split_a1.py` (I1–I8, `--check` bajtno PASS; veriga p60–p74 PASS) + dokaz `research/issue17/ps-parcels-geo-v7.json` + runtime `src/data/atlas/ps-parcels-geo.json` (version 7) + kartica P75; QA 77 → **78/78** (nova qa-p75-cross-split: celoven neodvisen preracun + nil-claim + nasledstvo 939 − 48 = 891 + area/sosledje preracun; produkcija veja izmerjena iz v7 runtime).
  `scripts/p70_ps_v4_rejoin.py` (I1–I9, `--check` bajtno PASS) + dokaz `research/issue17/ps-parcels-geo-v4.json` + runtime `src/data/atlas/ps-parcels-geo.json` (version 4) + API `/api/atlas/ps-parcels-geo` + kartica P70; QA 72 → **73/73**; v3 arhiviran (research/issue17/ps-parcels-geo-v3.json).
