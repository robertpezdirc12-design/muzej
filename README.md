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

## Varnost

Žeton `VERCEL_TOKEN` je shranjen izključno kot šifrirana GitHub Actions
skrivnost in ni v repozitoriju. Datoteki `.gitignore` in `.vercelignore`
preprečujeta prenos `.env*` in lokalnih datotek pri deployu.
