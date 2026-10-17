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
| Skrivnosti (samo za rezervo) | `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` kot šifrirane GitHub Actions skrivnosti; obnovitev skrivnosti prek REST API-ja (`PUT /repos/…/actions/secrets/{ime}` — vrednost šifrirana z libsodium sealed box, PyNaCl; tako je P78 saniral `GITLAB_TOKEN`) |
| Zdravje žetona | `token-health.yml` preverja žetona dnevno (06:12 UTC): avtentikacija + obseg ekipe; ob napaki komentira na issue #6. ⚠ **P78 (15. 10. 2026): watchdog trenutno MRTV — GitHub Actions blokiran na nivoju računa (billing; anotacija check-run); dokler ne bo sanirano, velja ročni audit `p78_tokens_production_audit.py --check` |

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
  (razpršena zidanica — vinice/hambi na zahodnih pobočjih) — nadgradnja P16
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
- **globinska povezava** `?atlas=hiša-75` (hiša št. 73 — demonstracijska veriga do MVG-010).

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
  posodobljeni; SHEET_GEOREFS in join v2 nespremenjeni.

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
  SHEET_GEOREFS in join v2 nespremenjeni.
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
  join v2 in SHEET_GEOREFS nespremenjeni.
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
  join v2 in SHEET_GEOREFS nespremenjeni.
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
  join v2 in SHEET_GEOREFS nespremenjeni.
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
  nespremenjeni.
- **v3 sanacija številčenja + sistemski pregled pass1 slojev (P68/P69, issue #13)** — P68 je IZVEDEL 17 preslikav P67 specifikacije (p78 160x→150x, p93 160x→190x, p87 661–680→1681–1700; 0 kolizij; re-join: 14 vrstic izpada, p93 3× re-claim 1903/1904/1905) → v3 = 1079 vrstic / 798 base / 199 multi-page / 98 cross-Blatt, join ključi sanirani, registrska branja nespremenjena, veriga re-run P59–P67 s posodobljenimi pini; P69 je nato z OČESNO forenziko (22 strani p73–93 + p99; 4× široki izrezi + 7×–8× zoomi + kontinuiteta + karta + P56 annRecords zamiki + hišne številke + površinska razmerja) razrešil odprto točko P68 #3: stari P38 pass1 sloji = sistematski digitalni artefakti (p74 1121–40 je pravzaprap 1421–40 4→1, p79 1821–42 = 1521–40 5→8, p80/p81 16xx = 15xx 5→6, p82 1681–1700 = 1581–1600 s 16 izgubljenimi vrsticami, p88 721–740 = 601–620 +120, p89/p90 19xx = 9xx fantom-1, p92 990–1008 = 981–1000 +9, p99 921–40 = 1921–40 −1000 zrcalno) — **77 renum preslikav (0 kolizij) + 98 rejoin kandidatov = spec P70**; 5 lokalnih sekcij (p83/p84/p86 161–180 ×3, p85 641–660, p88 601–620; 56 vrstic) = dokazane lažne fuzije na Blatt I poligone (hiše p85 r641 Hi16 vs p35 Hi68; Σ ratio 161 = 235.65×) — exclude/per-Blatt = lastniška odločitev;
  `scripts/p69_ps_pass1_layers.py` (I1–I6, `--check` bajtno PASS) + dokaz `research/issue17/ps-pass1-layers.json` + API `/api/atlas/ps-pass1-layers` + kartica P69; QA 71 → **72/72**; join v3 nespremenjen (spec čaka izvedbo).
- **izvedba P69 specifikacije — v4 sanacija (P70, issue #13)** — P70 je IZVEDEL P69 specifikacijo kot mehanski izvod (deterministično, brez AI ob delovanju): **77 renum preslikav** (bajtno po P69 renumSpec; konec lažnih fuzij cone p73–93/p99: p74 1121–1140→1421–1440 4→1, p76 1161–1180→1461–1480, p79 182x→152x 5→8, p80/p81 16xx→15xx 5→6, p89/p90 19xx→9xx fantom-1 — 9 dolgi ascender ≠ vodilna 1, p92 990–1008→981–999 +9, p99 921–940→1921–1940 Blatt III zrcalno; parzella ostaja originalno branje) **+ 95 rejoin vrstic** iz starih P38 slojev po P55 metodi (sloji po P69: pass1-pravilen p74/82/89/90/91, P38 izbira sicer; 3 kandidati p80 1541–1543 brez vira [~] — p1 odrez blok 62–81) **+ 29 preslikanih izpada** (base brez PF poligona); **33 fuzij isti-Blatt dokumentiranih** (register vsebuje 921–1000 v dveh blokih: p49–52 »glavni tek« + p89–92 »stolpec« — SPLIT join = lastniška odločitev); v4 = **1145 vrstic / 878 base / 215 multi-page / 79 cross-Blatt**; površine median 3.8843 ≈ 1 Wiener QK 3.59665 m² (Δ +8.0 %, kontrola 4.2701); soslednost 654 parov / 52.0 m / 27.6×; zaupanje 188/797/160; **56 sekijskih vrstic (p83–86, p88) nespremenjenih** — exclude ali per-Blatt instance = lastniška odločitev; veriga P59–P67 skript --check PASS (P69 klasifikacija zamrznjena na v3 dokaz);
  `scripts/p70_ps_v4_rejoin.py` (I1–I9, `--check` bajtno PASS) + dokaz `research/issue17/ps-parcels-geo-v4.json` + runtime `src/data/atlas/ps-parcels-geo.json` (version 4) + API `/api/atlas/ps-parcels-geo` + kartica P70; QA 72 → **73/73**; v3 arhiviran (research/issue17/ps-parcels-geo-v3.json).
- **korekcije v4 — sekcije exclude + p93 reverzija (P71, issue #13)** — C1: 56 sekijskih vrstic (p83–86, p88) EXCLUDE iz joina (P69 dokazane lažne fuzije; lastniška odločitev; 0 poligonov ostane praznih) + C2: P68 renum p93 160x→190x OVRŽEN z notranjo glifno forenziko (r9=1609/r19=1619: 6 ≠ 9; kontrole p98/p92) + annRecords anotatorja (1601–1619) + pageMap — 15 vrstic base := parzella, PF 1603/1604/1605 dobijo prve vrstice, 12 izpadlih; **v5 = 1077 vrstic / 879 base / 184 multi / 48 cross**; area median 3.9052 (Δ +8.58 %); soslednost 652/51.8/25.5×; forenzika research/issue17/p93-forensics/; veriga P59–P67 PASS, P69 zamrznjen, P70 dokaz bajtno;
  `scripts/p71_ps_v5_sections_p93.py` (I1–I8, `--check` bajtno PASS) + dokaz `research/issue17/ps-parcels-geo-v5.json` + runtime `src/data/atlas/ps-parcels-geo.json` (version 5) + kartica P71; QA 73 → **74/74**; v4 arhiviran (research/issue17/ps-parcels-geo-v4.json).
- **dvojnosti registra — 135 isti-Blatt dual base (P72, issue #13)** — odločitveni paket za isti-Blatt SPLIT joina (P70 »SPLIT = LASTNIKA« razširjen na cel register; razširitev P66 cross-Blatt vzorca; NE odloča namesto lastnika — MERI in DOKAZUJE; **v5 join nespremenjen**): base z vrsticami na ≥ 2 straneh ISTEGA Blatta z DISJUNKTNIMI lastniki med straneh — **135 base × 274 vrstic** (2 tri-zapisni; + 2 nearDual 2080/2081 izključeni); stranski pari delijo iste številčne razpone po P56 pageMap (p23/p24 = 401–420 obe, p51/p91 = 961–980 obe, p103/p118 = 2001–2020 obe …) z odmiki po blokih konsistentnimi (**40 × 44 · 15 × 49 · 5 × 29 · 1 × 13**) = **dvojni zapis iste serije v dveh blokih registra**; hišne številke različne 130/135; Σ areaQK blok A 128 125 / blok B 145 057 QK; **P70 33 kolizij = podmnožica** + 11 starih p51×p91 (v2 era) + 91 dozdaj neopaženih; opcija A (drop drugi blok po C1 vzorcu): 137 vrstic izpada, 0 base brez vrstic, rows 1077 → 939, multi 50, cross 48 nespr.; opcija B (per-page instance) zahteva georef Blattnih kart [~]; opcija C (re-renum) neodločljiva; **odločitev LASTNIKA**;
  `scripts/p72_ps_dual_pack.py` (I1–I9, `--check` bajtno PASS) + dokaz `research/issue17/ps-dual-occurrence-pack.json` + runtime `src/data/atlas/ps-dual-occurrence-pack.json` + kartica P72; QA 74 → **75/75**; v5 runtime join NESPREMENJEN (sha256 pin I9).
- **isti-Blatt SPLIT opcija A — v6 (P73, issue #13)** — izvedba C3 iz P72 dual pack (lastniško soglasje 2026-10-15; P70 »SPLIT = LASTNIKA« razširjen na cel register): za **135 dual base** (lastniki med straneh disjunktni 135/135; P70 33 kolizij = podmnožica: p89 × 15, p90 × 10, p92 × 8) so vrstice drugega bloka izpadle iz joina — **drop 137 kombinacij = 138 vrstic** (keep = min stran »glavni tek«; vrstice ostanejo v registru brez geometrije) — **v6 = 939 vrstic (34.0 %) / 879 base / multi 184 → 50 / cross 48**; serije S1 847 / S2 66 / BI 26; zaupanje 174/629/136; dvoumnost 50/100 (135 True→False po P55 metodi); area median **3.8941** (Δ +8.27 %, kontrola 4.5766); soslednost 652/51.8/25.5× nespremenjena; nearDual 2080/2081 ostanejo; 0 base brez vrstic; v5 arhiviran (v5Delta + v6Delta = nasledstvo);
  `scripts/p73_ps_v6_split_a.py` (I1–I8, `--check` bajtno PASS) + dokaz `research/issue17/ps-parcels-geo-v6.json` + runtime `src/data/atlas/ps-parcels-geo.json` (version 6) + kartica P73; QA 75 → **76/76** (nova qa-p73-v6-split: celoven neodvisen preracun + nil-claim).
- **cross-Blatt dvojnosti registra — 48 čez-Blatt base (P74, issue #13)** — odločitveni paket za cross-Blatt SPLIT joina (odprta točka P73 ①; P66 vzorec re-izpeljan iz v6 univerzuma; NE odloča namesto lastnika — MERI in DOKAZUJE; **v6 join nespremenjen**): 48 base z vrsticami na ≥ 2 RAZLIČNIH **sosednjih** Blattih — **48 base × 96 vrstic, točno 1 vrstica per Blatt 48/48**; pari **I·II 13 · II·III 16 · III·IV 1 · IV·V 18** (sosednji 48, skoki 0); **lastniki med Blatti DISJUNKTNI 48/48** (0 prekrivanj; P66 v v3: 36/36) — jedro paketa; pageMap prekrivanja razponov 48/48 (p11 I 161–183 / p61 II 161–180; p64 II 1821–1840 / p94 III 1821–1841; p110 IV 2141–2160 / p125 V 2141–2160) = dokaz ponovitve numeracije per Blatt; hišne številke **42 različne · 2 isti (161, 174) · 4 brez** (2611–2616); Σ areaQK per Blatt I 1874 / II 11364 / III 18300 / IV 13257 / V 13118 QK; pasovi [0.50,0.60) 8 · [0.60,0.70) 5 · [0.70,0.75) 8 · **≥0.75 27** (P66 kriterij <0.75 bi pokril samo 21); **opcija A1** (keep dominant Blatt): drop 48, rows 939 → 891, multi 2, cross 0, ambRows 4; **opcija A2** (keep min Blatt) enaki števci, različen keep pri 29 — izbira pravila **LASTNIŠKA**; evolucija P66 → v6: **17/36 ostaja · 19 odhaja** (C1 5 · C3 13 · C2 1) · **31 novih**;
  `scripts/p74_ps_cross_blatt_pack.py` (I1–I9, `--check` bajtno PASS) + dokaz `research/issue17/ps-cross-blatt-pack.json` + runtime `src/data/atlas/ps-cross-blatt-pack.json` + kartica P74; QA 76 → **77/77** (nova qa-p74-cross-blatt: celoven neodvisen preracun cross seta × P59 × P66 pack); v6 runtime join NESPREMENJEN (sha256 pin I9).
- **cross-Blatt SPLIT opcija A1 → v7 (P75, issue #13)** — izvedba C4 iz P74 odločitvenega paketa (lastniška odločitev 2026-10-15; opcija A1 = privzeta pot — **keep DOMINANT Blatt po Σ areaQK; ties 0**; vzorec P72→P73): za **48 cross base** (vrstice na ≥ 2 sosednjih Blattih; lastniki med Blatti disjunktni 48/48; ista številka pod dvema Blattoma = 2 realni parceli) je vrstica ne-dominantnega Blatta izpadla iz joina — **drop 48 kombinacij = 48 vrstic** — **v7 = 891 vrstic (32.3 %) / 879 base / multi 50 → 2 / cross 48 → 0** (NIL-CLAIM kontrola: cross set na v7 == prazno); dvoumnost 100 → 4 (48 True→False po P55 metodi); zaupanje 172/588/131 (0 sprememb); serije S1 803 / S2 62 / BI 26; area median **3.8102** (Δ **+5.94 %**, kontrola 4.1435; 871 parov); soslednost 652/51.8/25.5× nespremenjena; 0 base brez vrstic; opcija A2 bi pri **29 base** obdržala drugo vrstico; opcija B (per-Blatt instance + razdelitev geometrije) zahteva georef Blattnih kart [~]; vrstice ostanejo v registru brez geometrije (removedRows 48); ohranjene vrstice bajtno == v6 (P9); v6 arhiviran (v5Delta + v6Delta + v7Delta = nasledstvo 1145 → 1077 → 939 → 891);
  `scripts/p75_ps_v7_cross_split_a1.py` (I1–I8, `--check` bajtno PASS; veriga p60–p74 PASS) + dokaz `research/issue17/ps-parcels-geo-v7.json` + runtime `src/data/atlas/ps-parcels-geo.json` (version 7) + kartica P75; QA 77 → **78/78** (nova qa-p75-cross-split: celoven neodvisen preracun + nil-claim + nasledstvo 939 − 48 = 891 + area/sosledje preracun; produkcija veja izmerjena iz v7 runtime).
- **lokalne sekcije — per-Blatt instance odločitveni paket (P76, issue #13)** — odprta točka P70 ①/P71 C1 (vzorec P72/P74 — paket MERI, NE odloča; **v7 join nespremenjen**): **56 sekcij vrstic** (p83 13 · p84 12 · p85 14 · p86 14 · p88 3; vse **Blatt II** po P59) × **31 base** — identitetno **DISJUNKTNE od counterpartov** (lastniki **0/0** — sekcija×counterpar IN sekcija×sekcija; hišne številke **0 isti / 31 različni**) — dokazano na celotni množici, ne samo na P69 vzorcu; **counterpar v v7 31/31** (Blatt I 23: p10 1 · p11 5 · p35 14 · p40 3 / Blatt II 8: p61 8; lat/lng 31/31); evolucija C4 **13/31 cross** (8 obdržalo II, 5 I) / **18 single**; P56 pageMap ponovitev bandov **5/5** (p83 161–181 ⊆ p11 161–183 + p61 161–180; p85 641–660 == p35; p88 721–740 == p40); P60 moda B **8 base = 12/56 vrstic** z band identiteto, 44 [~] brez (PF protokol = manjkajoči vir); v3 forenzika: geoShared 56/56, ratio absurdni >4.3: **20 (max 134.6786)**, Σ areaQK **38517 QK**; opcije: **A** status quo 891/2/0/4 · **B1** vse 56 → 947/33/23/91 — **KRŠI C4 NIL-CLAIM z base-ključem (23 cross)** → obvezen **per-instanca ključ (base, stran)**: 0/2/4 · **B2** samo P60 band 12 → 903/10/6/24 (+ instance 0/2/4; 44 ostane [~]) · **B3** georef [~] neizvedljivo — **izbira LASTNIŠKA**;
  `scripts/p76_ps_sections_perblatt_pack.py` (I1–I9, `--check` bajtno PASS) + dokaz `research/issue17/ps-sections-perblatt-pack.json` + runtime `src/data/atlas/ps-sections-perblatt-pack.json` + kartica P76; QA 78 → **79/79** (nova qa-p76-sections-perblatt: celoven neodvisen preracun iz P69 sectionClass × v7 runtime × P59 × P60 × pack runtime; opcije re-izpeljane + instance ključ; repo dodaja dokaz == runtime bajtno + P56 dokaz pageMap == pini); v7 runtime join NESPREMENJEN (sha256 pin I9, 4bb40370…).
- **PF protokol — VAČ inventarna forenzika, dokazani negativ (P77, issue #13)** — odprta točka P76 ② (vir identitete pas-instanc; MERI, NE odloča; **v7 join nespremenjen**): VAČ je bil posodobljen 2026-10-14 (verzija 2.21_5.5) — iskalni API pokvarjen (`fieldSearch` 0 zadetkov za vse kriterije, `details` interna napaka), **edini delujoč API = tektonika** (`archivePlanSearchAjax`) + `pdfPageImage`; besedilni sprehod po tektoniki (root → 000 UPRAVA → 070 → 071 → **SI AS 176 (23253)** → N Novomeška kresija (226589) → **N83 Griblje (227663)**): natanko **12 enot** (grafični A01–A05 + spisovni PG/PR/PS/PT/PUA/PV/PZ; 373413–373419) == številu v README; **mapiranje `docid = uodid − 331635`** verificirano 7/7 JPEG probe; sosedski uodid prostor (373411, 373420–373424) 0/6 JPEG — ni skrite enote; **DOKAZANI NEGATIV (I6): med 12 enotami NI dodatnega protokola (PF/Parzellen-Führer/Stavbni protokol)** — edini protokol-slični vir = PT Seznam stavbnih parcel (373416), ŽE v repu (105 vrstic); **implikacija: vir identitete pas-instanc NI na VAČ → fizični arhiv (SI AS 176 ali SI AS 52 Finančna direkcija) ali drugi fond — operativna lastniška akcija; P76 opcije B1/B2 ostajata edini izvedljivi poti brez PF protokola, izbira LASTNIŠKA**;
  `scripts/p77_pf_vac_inventory.py` (I1–I8, `--check` bajtno PASS) + dokaz `research/issue17/pf-vac-inventory.json` (PROVEN-NEGATIVE-INVENTORY); QA ostaja **79/79** (VAČ = zunanji omrežni vir — ne sme biti produkcija QA kontrola, P53/P57/P58 lekcija; dokaz ponovljiv s `--check`); v7 runtime join NESPREMENJEN (sha256 4bb40370…).
- **produkcija & žetoni — operativni zdravstveni audit (P78, issue #6)** — edina NE-lastniška odprta točka po P77 (③ žetoni; MERI in SANIRA, kjer API to dopušča; **v7 join nespremenjen**): **produkcija ZDRAVA in AKTUALNA** — `GET /` HTTP 200 (704 548 B == post-P77 deploy), `/api/qa` ok True **79/79** (79 testov; `qa-p76-sections-perblatt` True), `/api/atlas/ps-parcels-geo` **v7/891**; **zrcala bajtno identična** (`git ls-remote`: GitLab = GitHub = lokalni HEAD; GitHub REST `GET /commits/main` 404 neavtentificirano — repozitorij zaseben, ls-remote z žetonom iz remote URL); **GitLab PAT #3 AVTORITATIVNO aktiven** (`/personal_access_tokens/self`: id 28471532, `dsfsd`, active, rok **2026-11-14**, scopes ⊇ api + write_repository + read_repository + self_rotate) — rok 2026-11-09 v naslovu issue #6 se nanaša na STARI žeton; **DISCOVERY — GitHub Actions blokiran na nivoju računa (billing)**: vsi jobi NE STARTAJO (failure v ~2 s, `steps: []`, `runner_id: 0`, logi `BlobNotFound`; kontrola z dispatchem tudi po sanaciji skrivnosti — enak podpis na sync.yml IN token-health.yml) — check-run anotacija (avtoritativno GitHub): *"The job was not started because recent account payments have failed or your spending limit needs to be increased. Please check the 'Billing & plans' section in your settings"*; zadetki: **sync.yml** (dvosmerna sinhronizacija — mreža varnosti; zadnji uspeh 2026-10-11T06:23Z), **token-health.yml** (dnevni watchdog — ZATO NI OPOZORIL 10-13/14/15 ob izteku VERCEL_TOKEN!) in **deploy.yml** (rezervni deploy; zadnji uspeh 2026-10-11; potekel žeton 2026-10-14 = dodaten razlog) — **SANACIJA P78: skrivnost GITLAB_TOKEN** (držala neveljaven PAT #2, updated 2026-10-13) zamenjana z aktualnim PAT #3 (libsodium sealed box prek PyNaCl; `PUT /repos/…/actions/secrets/GITLAB_TOKEN` HTTP 204, updated 2026-10-15T20:51:08Z) — nujno tudi samo po sebi (stari PAT bi padel ob auth, takoj ko bi Actions začel teči); **OSTAJA LASTNIŠKA AKCIJA: Billing & plans** (plačilna metoda / spending limit — API brez admin:billing scope ne more) + nov VERCEL_TOKEN (vercel.com/account/tokens; Vercel API ne ustvarja žetonov) — primarni deploy (Vercel GitHub App) NEODVISEN od obeh in DELA;
  `scripts/p78_tokens_production_audit.py` (I1–I9, `--check` bajtno PASS; live probe: Vercel `/`, `/api/qa`, geo; GitLab PAT/project z WAF-retry; zrcala ls-remote; Actions check-run anotacija; brez mutacij) + dokaz `research/issue17/tokens-production-audit.json` (OPERATIONAL-AUDIT; sanacija + časovnica + vpliv per workflow + 3 lastniške akcije po prioriteti); QA ostaja **79/79** (operativni audit ni produkcija vsebine); veriga `p60–p67 + p70–p78 --check` bajtno PASS; tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).
- **župnija Podzemelj — vzorčni prepis matričnih vpisov z gribeljskimi hišnimi št. (P79, issue #18)** — prvi napredek na človeški/paleografski liniji od P39 (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online** (prosto dostopen, brez avtentikacije; krstna knjiga **04105 1886–1919**, Nadškofijski arhiv Ljubljana; slike prek base64-kodiranih URL-jev v JSON `files`); **VZOREC = polno leto 1886** (skeni 2–15 == tiskane strani 1–14: vsi vpisi z Griblji v letu; prebranih 95 vrstic, od tega 12 Griblje) **+ sidro 1887** (verifikacija obstoječega zapisa hiše 61) — **15 vpisov / 13 različnih hiš** (8 [~] · 11 · 13 · 16 · 36×2 · 39 · 54 · 56 · 57 · 61 · 71 · 75 · 94) — **NAD merili issue #18 (vzorec 5 hiš)**; vsak vpis: signatura + leto + stran/skan + hišna št. + otrok + starši (Kurrent branje z [~] negotovostjo; hišne številke preverjene z 2× izrezi); **PT usklajenost = DOKAZ ŠTEVILČNE EVOLUCIJE**: PT 1825 nabor = 84 hiš **1–40 + 61–99** z polovičkami (LUKNJA 41–60) → 10/13 vpisov v naboru (8, 11, 13, 16, 36, 39, 61, 71, 75, 94), 3/13 (**54, 56, 57**) v luknji 41–60 — številčenje se je med 1825 in 1886 razširilo/preštevilčilo (številčna usklajenost ≠ identiteta stavbe — za to bi bila potrebna povezava prek lastniških imen, opozorilo PUA/PT iz issue #18 ostaja); hiša 36: 2 vpisa v 1886 (row 39 brez očeta — mati Barbara Šimec; row 95 oče Matija Križan — dve družini pod eno št. [~]); poznejši modri pripisi 20. st. (npr. hiša 39: umrl 18.9.1961 v Gribljah št. 39 — potrjuje št.) dokumentirani ločeno od osnovnega vpisa; **sidro: hiša 61 (sken 20, stran 19, vrstica 28) ponovno prebrana in POTRJENA** (sken/leto/hiša/ime == parish.ts; oče: obe branji dokumentirani — »Miha P.—« obstoječe / »Miko Jože H.?« ponovno [~]);
  `scripts/p79_parish_sample.py` (I1–I8, `--check` PASS; live: knjiga HTTP 200, inventar **326 slik** iz base64 dekodiranja, citirani skeni 10/10 JPEG 200) + dokaz `research/issue17/parish-sample-transcription.json` (SAMPLE-TRANSCRIPTION) + `parish.ts` HOUSE_VITALS 2 → 15 (vsi DOCUMENTED, s stranmi) + QA 79 → **80/80** (nova qa-p79-parish-sample: celovit runtime preracun iz HOUSE_VITALS × PARISH_BOOKS + pini PT klasifikacije — okvir/sidro/PT/usklajenost, dve obliki repo/produkcija po P53/P57/P58); kartica NI dodana (paleografski dokaz raziskovalne linije — strojno berljiv prek dokaza, vzorec P77); veriga `p60–p67 + p70–p79 --check` PASS; tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).

- **župnija Podzemelj — vzorec razširjen na mrliško (04894) in poročno (04455) knjigo (P80, issue #18)** — P79 nextSteps (isti vzorec kriterijev: okvir 1886 + sidra; MERI, NE odloča; **v7 join nespremenjen**): vira **Matricula Online**, mrliška **04894 1886–1924** (256 skenov) in poročna **04455 1873–1922** (192 skenov) — že v PARISH_BOOKS (issue #6); **mrliški okvir 1886**: skeni 2–6 == strani 1–5 (46 vrstic; **stran == sken − 1**; leto 1887 se začne na strani 5 pri prelomu »Januarj 1887« — zadnji gribeljski vpis 1886 Katarina vdova Podec hiša 69 (11. 12.), prvi 1887 Matija Šproch hiša 44, 1. 1.) — **13 vpisov / 11 hiš** (5 · 13 · 15 · 16 · 29×3 · 31 · 59 · 69 · 71 · 74 · 88) + sidro 1887 (sken 6: hiša 44 prvi vpis leta + hiša 36 Ana Šimec neza., povezava z materjo Barbaro Šimec); **poročni okvir 1886**: skeni 61–65 == Pag. 60–64 (vpisi 1–24; **Pag. == sken − 1 v zveznem razponu 61–66** — ročno številčenje ni zvezno skozi knjigo: sken 50 == Pag. 44) — **7 vpisov / 10 hiš** (31 · 36 · 60 · 63 · 15 · 25 · 71) + sidra (Nov 1885 sk. 61: hiša 13 ženin Janez Jakobič, starši == pari krsta hiše 13; Nov 1882 sk. 50 Pag. 44: hiša 36 Mathias Križan = oče krsta Dec 1886; 1887 sk. 66: hiša 71 Mathias Straus + hiša 15/29 Johann Šambie × Maria Brinec); **križne povezave treh virov: hiše 13 · 36 · 71 dokumentirane v VSEH treh knjigah** (krstna + mrliška + poročna — 13 = Jakopič/Podlirc; 36 = Šimec/Križan; 71 = Strauš v vseh treh); **dokaz epidemije — hiša 29**: trije otroci (Janez 8, Katarina 9, Ana 11 — Mileh [~]) umrli v 4 dneh (10.–13. 10. 1886) z istim vzrokom »Kolera i. morbas« [~]; **P80 RE-READ KOREKCIJA P79**: hiša 56 mati = **»Dora roj. Perdinec«** (ne »Podžire«) — dokaz: poročna sk. 62 vpis 4/1886 Johann Šimec × Dorothea Perdinec = isti par kot krst Nov 1886; števk forenzika: hiša **59** (ne 39) — izrez Kurrent števk 3 vs 5; **PT klasifikacija vzorca 25 hiš: 19 v naboru + 6 v luknji 41–60** (44, 54, 56, 57, 59, 60 — 59/60 NOVA dokaza luknje);
  `scripts/p80_parish_md_books.py` (**I1–I10**, `--check` PASS; live: knjigi HTTP 200, inventarja **256 + 192 slik**, citirani skeni 13/13 JPEG 200) + dokaz `research/issue17/parish-md-transcription.json` (SAMPLE-TRANSCRIPTION-EXTENDED) + `parish.ts` HOUSE_VITALS 15 → **41** + **qa.ts → qa-parish.ts izvleček** (telo runQA preseglo prag TS control flow analysis; kontrole bajtno enake) + QA 80 → **81/81** (nova qa-p80-parish-md-books; dve obliki repo/produkcija) + `atlas.ts` checkIntegrity sanitacija (PT luknja hiše 41–60 ZAKONITO izven ATLAS_HOUSES — dokaz evolucije, ne regresija); kartica NI dodana (vzorec P77/P79); veriga `p60–p67 + p70–p80 --check` PASS; tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).

- **župnija Podzemelj — povezava lastniških imen 1825 (PT/PUA) ↔ matrični priimki 1886 (P81, issue #18)** — P80 nextSteps: test ali številčna usklajenost vzorca s PT/PUA nosi tudi IMENSKO kontinuiteto (MERI, NE odloča; **v7 join nespremenjen**): **vesolje 1825 = 232 imen** v treh slojih — **PT 84 hišnih lastnikov** (chain-full-pt-ps.json [pin]) + **PUA 101 vrstic** str. 3–49 (bundle) + **ATLAS 26 lastnikov** str. A–B (bundle) × **vzorec 25 hiš P79/P80** (19 v naboru PT, 6 v luknji 41–60) z 40 različnimi priimki; **metoda deterministična, brez AI ob delovanju**: normalizacija pass1 (de-diacritika) + pass2 (nem. Kurrent **sch→s**), Levenshtein razmerje, **prag priče ≥ 0.72** (P43 W-most), kratki priimki < 5 znakov le natančna enakost, **stoplist krstnih imen** (Gregor itn. — brez nje bi priimek Gregorič lažno ujel krstno ime Gregor 0.75) + uredniški žetoni; **REZULTATI**: ① **isto-hišna kontinuiteta vs PT 1825: 0/19 (NIL-CLAIM)** — vsaka hiša z PT lastnikom ima 1886 drugačen priimek ② isto-hišne ujeme po PUA lastnem številčenju [~]: **2** — hiša 36 Križan ↔ Krischan @36 (0.8333) in hiša 71 Straus ↔ Strauß Niklo @71 (0.8571) — PUA ≠ PT številčenje: usklajenost dveh sistemov, NE istovetnost ③ **cenzus priimkov: 10/38 eligible (26.32 %) ima pričo 1825** — Dragoš, Filak, Stubler, Šimec (najtrajnejša: PUA 5 zapisov + ATLAS 5 → 1886 hiše 36/39/56/88), Šimer [~], Strauš/Straus, Brinec [~] (PUA @43 — št. v luknji!), Filatk [~], Križan — preživetje na ravni PRIIMKA, ne hiše (17 brez priče; Meh/Muc izključena po dolžinskem pravilu) ④ near-miss pas [0.55, 0.72): 11 priimkov (Gilatk, Mileh/Milavec ~ Milleg, Stupanič ~ Stepanitsch, Šilah ~ Fillah …) ⑤ luknja 41–60: PUA ohranja 16 vrstic, 0 isto-številnih ujem ≥ 0.72 (najbližje @56 Schumetz vs Šimec 0.667 [~]) ⑥ tri-virske hiše 13/36/71: **0/3 imenskih ujem z 1825**; **IMPLIKACIJA za issue #18: imenska raven POTRJUJE opozorilo — številčna usklajenost ≠ identiteta stavbe ≠ identiteta družine**; most = per-hišne kronološke verige (poln prepis = lastniška prioriteta);
  `scripts/p81_parish_name_linkage.py` (**I1–I10**, `--check` PASS; trojni determinizem Python ↔ TS ↔ QA) + dokaz `research/issue17/parish-name-linkage.json` (**NAME-LINKAGE-PACK**) + runtime `src/data/atlas/parish-name-linkage.json` (bajtna projekcija) + `src/lib/name-matcher.ts` (zrcalna TS izvedba — vsaka sprememba zrcaljena v Python, I5) + QA 81 → **82/82** (nova qa-p81-parish-name-linkage: celoven neodvisen preracun isto-hiša PT/ATLAS/PUA + cenzus + PUA 41–60 + 57 sidr src==parish proti bundled parish.ts; preostala 4 sidra — 1 p80 + 3 p79 — verificirana le v repo skripti; dve obliki repo/produkcija); kartica NI dodana (vzorec P77–P80); veriga `p60–p67 + p70–p81 --check` PASS; tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).

- **župnija Podzemelj — krstna knjiga 04105, polno leto 1887 (P82, issue #18)** — P81 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919** (326 skenov); **okvir 1887: skeni 16–27 == strani 15–26** (stran == sken − 1; glava »Leto 18_87« na str. 15; **leto 1888 se začne na str. 26 po row 106 z velikimi ciframi »1 8 8 8«**) — **VSI vpisi z Griblji: 20 vpisov / 19 različnih hiš** (2, 15, 17, 21, 24, 26 [~], 27, 31×2, 34, 35, 47, 52→04→15 [~], 55, 61, 62, 63, 65, 66, 78) — skupaj s P79/P80 vzorec **59 vpisov / 42 hiš čez tri knjige in dve leti**; **NOVI PT LUKNJI 47 in 55** (+ 52 izvirno row 78 — **trojna korekcija 52 → 04 → 15** [~]): luknja 41–60 v krstnih vpisih zdaj **9 dokazanih števil** (54/56/57 + 44/59/60 + 47/52/55); **P79 RE-READ KOREKCIJA: hiša »75« = 78** (P79 sidro je ista vrstica kot row 26; izrez Kurrent: dve zaprti zanki = 8 — vzorec forenzike P80 3-vs-5); **P79 SIDRO hiša 61 re-verificirano** (row 28: oče zdaj »Miko Požek« [~], prej »Miha P.—«/»Miko Jože H.?« — oba branji ohranjena); **NEZAKONSKI vpisi 2** (row 78 hiša 52 mati Marija Muc [~]; row 80 hiša 55 mati Ana Smič [~] — očeta stolpca PRAZNA) + **ANOMALIJA row 93** (hiša 35: žensko ime v očetovem stolpcu, dve interpretaciji [~]); **križna povezava dveh knjig: hiša 31** (mrliška 1886 Katarina Marh — P80 + krstna 1887 ×2) — edina multi-vpisna hiša; priimki čez leta: **Šimec 1886: 36/39/56/88 → 1887: 34 (NOVA hiša)**, Straus, Filak, Stubler, Požek; **troi duhovniki 1887** (Griebel [~] 14×, Dovgan, »Jos. Povmij« [~] 4× — nov podpis) + **babica Marija Brinec 9×**;
  `scripts/p82_parish_baptism_1887.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1887.json` (SAMPLE-TRANSCRIPTION-1887) + `parish.ts` HOUSE_VITALS 41 → **59** (19 novih + posodobljeni 61 + re-read 75→78) + QA 82 → **83/83** (nova qa-p82-parish-baptism-1887: celoven neodvisen preracun okvir/PT 16/3/sidro/nezakonski/trojna korekcija/anomalija/multi/križna povezava; dve obliki repo/produkcija) + qa-p79/qa-p80 ožje opredeljena (P82 scoping; pin 75 → 78) + atlas.ts PT_GAP_KNOWN + 47/52/55 + p81 pack REGENERIRAN (CURATED 75 → 78; statistika nespremenjena) + p80 skripta I7 P82 scoping; kartica NI dodana (vzorec P77–P81); veriga `p60–p67 + p70–p82 --check` PASS; tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).

- **župnija Podzemelj — krstna knjiga 04105, polno leto 1888 (P83, issue #18)** — P82 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1888: skeni 27–35 == strani 26–34** (stran == sken − 1; vpisi na skenih 28–34; **prelom 1889 »1 8 8 9« na str. 34 row 1** — prvi vpis 1889 = 3./3. 1., Gradac 8; leto 1888 ima 92 pisanih vrstic); **NOVELA P83: PISANE OZNAKE VRSTIC SE PRI PRELOMU LETA PONASTAVIJO NA 1** (str. 27 = oznaka 3 — dokaz; P82 »row 107« = zvezno štetje 106+1, pisana oznaka prve 1888 vrstice pod raztrganino [~]; narativi p82/qa-p82 usklajeni) — **VSI vpisi z Griblji: 15 vpisov / 15 različnih hiš** (1, 8, 13, 21, 24, 29, 44, 56, 57, 69, 72, 78 [~], 79, 83, 85) — skupaj s P79/P80/P82 vzorec **74 vpisov / 45 hiš čez tri knjige in tri leta**; **NOVE hiše 5** (1, 72, 79, 83, 85); **PT klasifikacija 12/3 — luknja 41–60: 44/56/57 VSE POTRDITVE, 0 novih števil** (skupaj 11 dokazanih čez tri knjige); **SIDRA**: hiša 13 (row 53: oče Matija **Jakobič** [~] × Marija Perdinec [~] — **TRI-VIRSKA hiša: 1885 poročna sidro + 1886 krst + 1886 mrliška + 1888 krst; Jakobič/Jakopič čez leta = PRVA per-hišna imenska veriga** — najmočnejši kandidat za 1825→1886→1888 most), hiša 78 (row 24: oče Mihail **Poxan** [~] **OSKRBAR** — 1886/1887 Jakobič → 1888 oskrbar = **socio-ekonomska motnja gospodinjstva**), hiša 29 (row 85: oče Peter **Milek** [~] — hiša epidemije 1886 Mileh ×3 → isti rod); **NOVA familija po 1825: POŽEK** (h79 oče bajtar + h21 nezakonska mati + botra — NI v vesolju 1825); **P84 RE-READ: »HRAUS/HRAUCELJ« = STRAUŠ/STRAUCELJ — JE v vesolju 1825** (Kurrent ſt brana kot H; trditev odpada — glej P84); nasprotje: **KRIŽAN 6 prič 1888 SE povezuje s 1825** (Krišan Gregor, Krischan @36 — P81 0.8333); **NEZAKONSKI 3/15** (h24 mati Barbara Melith [~]; h56 mati Ana Šimec [~] — Šimec ZNOVA na 56; h21 mati Marija Požek [~] — priimek ist kot 1887 hišni oče); **ANOMALIJE**: otrok »Kaxmarp« [~] (morda Kasimir), »Musca« [~], »Alex« [~] z nasprotjem spola (kolone moški [~] proti marginaliji »Umrla« [~]), **dvodelni priimek »Radovič Mrgaič« [~]** (vzporednica 1825 »Šture Majzel«); duhovniki Grieblj [~] 12× + Povmij [~] 1×; babica Brinec 10×;
  `scripts/p83_parish_baptism_1888.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1888.json` (SAMPLE-TRANSCRIPTION-1888) + `parish.ts` HOUSE_VITALS 59 → **74** (15 novih) + QA 83 → **84/84** (nova qa-p83-parish-baptism-1888: celoven neodvisen preracun okvir/PT 12/3/sidra/nezakonski/veriga hiše 13; dve obliki repo/produkcija) + p80 skripta I7 P83 scoping (vitals 74) + p82 skripta I4 tolerantna break1888 + P82 dokaz rowNote (ponastavitev oznak); atlas.ts NESPREMENJEN (PT_GAP_KNOWN že 44/56/57); kartica NI dodana (vzorec P77–P82); veriga `p60–p67 + p70–p83 --check` PASS; tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).

- **župnija Podzemelj — krstna knjiga 04105, polno leto 1889 (P84, issue #18)** — P83 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1889: skeni 35–43 == strani 34–42** (stran == sken − 1; vpisi na skenih 35–42; **prelom 1890 »Leto 1890« na str. 42 row 1** — oznake se ponastavijo na 1, novela P83 potrjena 2. leto; leto 1889 ima 106 zveznih vrstic); **NOVELI P84**: ① **številčenje str. 40 — duhovnikove oznake PONOVLJENE 68–8x** (napaka), modri svinčnik popravi zvezno 81–93 v datumskih celicah (str. 41 zvezno 94–106 — neodvisna potrditev); ② **RE-READ P83: »HRAUS/HRAUCELJ« = STRAUŠ/STRAUCELJ** — v isti p83 vrstici babica jasno »Neža Straucelj«; Kurrent ſt (S+t) brana kot H; familija **JE v vesolju 1825** (P81 0.8571 Strauß) — P83 »dve novi familiji« → ENA nova (Požek); h72 oče 1888 = 1889 isti **Matija Strauš**; h57 botra 1888 = 1889 ista **Marija Straucelj** — **VSI vpisi z Griblji: 19 vpisov / 16 imenovanih hiš + 2 neberljivi** (row 70 »///«, row 82 prekrita — evidence-only; HOUSE_VITALS 17 zasidranih): 58, 33, 3 [~], 64 ×2 (**multi-vpisna**), 35, 69, 59 [~], 63, 57, 32, 72, 2, 8 [~], 83 [~], 65, 26 [~] — skupaj s P79/P80/P82/P83 vzorec **93 vpisov / 50 hiš čez tri knjige in štiri leta**; **PT klasifikacija 13/3 — luknja 41–60: 58 NOVA** (row 3; dve zaprti zanki = 8 — vzorec forenzike P82) **+ 59/57 POTRDITVI** (skupaj 12 dokazanih čez tri knjige); **SIDRA**: hiša 63 (row 53: botr **Janez Šimec** [~] — **ATLAS 1825 Šimec @63 + PT lastnik »Šimec Ripane« @63 → NEPOSREDNA 1825↔1889 imenska + hišna povezava**), row 82 (babica **Ana Filak** [~] — P81 1.0 priča), row 89 = h8 (botr **Janez Dragoš** [~] — P81 1.0; mati Marija Urh [~] ISTA kot 1888), h72 (re-read veriga Strauš 1888+1889); **Šimec najtrajnejša**: 3 pojavi (mati row 70 »samka« + botr h63 + botra h2); priimki z 1825 pričo: Dragoš 2× (1.0), Strauš/Straucelj 6× (0.8571), Šimec 3× (1.0), Brinec 9× (0.8333 [~]), Filak 1× (1.0), Hrižan/Križan [~] 4× (0.8333 — **babica z naslovom hiše: »Ana Hrižan, Griblje št. 63«**), Jakobič 4× (veriga h13), Milek 2× (near-miss); **NEZAKONSKI 1/19** (h59 [~] mati Katarina Podirec »a samka?«) + **ANOMALIJA row 70** (mati »samka hči« × oče »šefur« — dve gospodinjstvi; otrok »Ožbolt?« [~]); duhovniki Griebel [~] 7× + Povmij [~] 8×; babice Brinec 7× + Ana Hrižan [~] 4×;
  `scripts/p84_parish_baptism_1889.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1889.json` (SAMPLE-TRANSCRIPTION-1889) + `parish.ts` HOUSE_VITALS 74 → **91** (17 zasidranih + 3 re-read popravki P83 z zgodovino) + QA 84 → **85/85** (nova qa-p84-parish-baptism-1889: celoven neodvisen preracun okvir/PT 13/3/sidra/multi/nezakonski/ponovitve; dve obliki repo/produkcija) + qa-p83 narativi (re-read novela) + atlas.ts PT_GAP_KNOWN + **58** + p80 skripta I7 P84 scoping (vitals 91) + P83 dokaz RE-READ blok (provenienca); kartica NI dodana (vzorec P77–P83); veriga `p60–p67 + p70–p84 --check` PASS; tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).

- **župnija Podzemelj — krstna knjiga 04105, polno leto 1890 (P85, issue #18)** — P84 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1890: skeni 43–49 == strani 42–48** (stran == sken − 1; vpisi na skenih 43–49; **prelom 1891 velike cifre »1891.« na str. 48 row 1 po row 86** — oznake se ponastavijo na 1, novela P83 potrjena 3. leto; leto 1890 ima 86 zveznih vrstic; glave mesecev se ponavljajo — Marec 2×, April 2×, Junij 2×); **NOVELA P85: STATUS = ULOMEK** — Kurrent znak pred »zemljak« (P79–P84 brana »ž zemljaf«) je z jasnimi izrezi 1890 **ulomek ½ (ali ¼)** — 15/24 vpisov (isti znak kot P84 row 3 »¼ zemljišč«); socio-ekonomski profil: malokmetje + bajtarja 2 (r47, r71) + **čevljar** (prvi obrtnik v vzorcu) + **učitelj** (šolska hiša 90) + mežnar iz Adlešič — **VSI vpisi z Griblji: 24 vpisov / 19 imenovanih hiš + 3 neberljive** (2 prekriti z modrimi pripisi, 1 rez strani — evidence-only; HOUSE_VITALS 21 zasidranih): 27, 31, 47, 24, 58, 71, 38, 15, 77, 30 ×2 (**DVOJČKA — prvi v vzorcu**: Janez †2/6/93 + Marija †19/6/90), 7, 69, 55, 32, 11, 41 ×2 (**multi-vpisna — dve različni družini**, 3. primer po h36/h64), 63, 90, 35 — skupaj s P79–P84 vzorec **117 vpisov / 56 hiš čez tri knjige in pet let**; **PT klasifikacija 15/4 — luknja 41–60: 41 NOVA** (rows 71+72; prvi dokaz 41!) **+ 47/55/58 POTRDITVI** (skupaj 13 dokazanih); **SIDRA**: h77 (oče **Jurij Pošek/Požek BAJTAR = P83 sidro h79 oče 1888** + botra **Barbara Požek = P83 h79 botra** — Požek veriga 79→77, 3. leto familije), h71 (oče **Jurij Straus** — tri-virska P80 + PUA Strauß Niklo @71, P81 0.8571 — 1890 živ oče), h63 (oče **Nikolaj Križan** — prvi KRIŽAN hišni oče v vzorcu; na P84 Šimec ATLAS sidru — 4. gospodinjstvo), h55 (oče **Nikolaj Šimec** — Šimec zdaj tudi na luknji 55, 6. hiša najtrajnejše familije); **ČEZ-LETNA POTRDITEV ANOMALIJE: r85 (h35) == P82 row 93** — očetov stolpec »Marija Hrižan ½ zemljak« × mati »Ana Požek« na ISTI hiši 1887 IN 1890 + otrok brez imena (»N. moškega spola«); + r19 (h24) anomalija »Marija Brinec ½ zemljak«; priimki z 1825 pričo v 1890: **Strauš 7×** (0.8571), **Šimec 4×** (1.0), **Križan/Hrižan 6×** (0.8333 [~]), Dragoš 2× (1.0), Brinec 3× + babica 11× (4. leto), Filak 1× (1.0), Požek 7×, Pendirec 9×, Klobučar 4×, Urh 2×, Milek 2×; duhovniki **Jos. Rauq [~] 19** (isti tip pisave kot P84 »Griebel/Povmij« [~]) + **C. g. Jurcan Šašelj, župr v D. Lazič [~] 1** (obiskni — edini popolnoma berljiv podpis) + Jos. G— 1; RE-READ P84 okvir: oče r6 = **»Janez Stubhar«** [~] (P84 »Kukhar« — Kurrent St/K);
  `scripts/p85_parish_baptism_1890.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1890.json` (SAMPLE-TRANSCRIPTION-1890) + `parish.ts` HOUSE_VITALS 91 → **112** (21 zasidranih) + QA 85 → **86/86** (nova qa-p85-parish-baptism-1890: celoven neodvisen preracun okvir/PT 15/4/sidra/dvojčka/multi/anomaliji/ponovitve; dve obliki repo/produkcija) + atlas.ts PT_GAP_KNOWN + **41** + p80 skripta I7 P85 scoping (vitals 112); kartica NI dodana (vzorec P77–P84); veriga `p60–p67 + p70–p85 --check` PASS; tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).


- **župnija Podzemelj — krstna knjiga 04105, polno leto 1891 (P86, issue #18)** — P85 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1891: skeni 49–56 == strani 48–55** (stran == sken − 1; leto se začne na str. 48 row 1 po 1890 rows 78–86; vpisi na skenih 50–54; **glava »Leto 1892« na str. 55 row 1** — oznake se ponastavijo na 1, novela P83 potrjena 4. leto; leto 1891 ima 75 zveznih vrstic; glave mesecev se ponavljajo — Avgust 2×, November 2×); **NOVELA (novela P85 potrjena 2. leto): VSI 9 zasidranih statusov = ¼ ulomek** (zemljak 5, gemžgah 4 — brez bajtarjev/obrtnikov na Gribljih, kontrast 1890) — **VSI vpisi z Griblji: 10 vpisov / 9 imenovanih hiš + 1 neberljiva** (r52 prekrita z modrimi pripisi — evidence-only; HOUSE_VITALS 9 zasidranih): 72, 30, 62, 61, 53, 2, 31, 5, 28 — **NOVE hiše 2 (28, 53)** + 1 neberljiva, **ponovitve 7** (h2 ×3 leta; h30 kontinuiteta; h31 ×4; **h5 ČEZ KNJIGE** — mrliška 04894 1886: umrla Barbara Brinec 2 leti → Torec 1891 = menjava gospodinjstva; h61 1887+1897+1891; h62 1887; h72 1888) — skupaj s P79–P85 vzorec **127 vpisov / 58 hiš čez tri knjige in šest let**; **PT klasifikacija 8/1 — luknja 41–60: 53 NOVA** (r40; forenzika izrez 4x: jasno 53 — prvi prebir »33« [~], Kurrent 3/5; **14. dokazana številka**); **SIDRA**: h72 (oče **Matija Straus [~] = ISTI očet kot P83 1888** — re-read Hraus→Strauš; **mati MENJANA: Husič [~] → Jakobič [~]**; tri-virska P80 + PUA @71 0.8571; botra Straucelj), h30 (oče **Janez Milek [~] = P85 dvojčka rows 51+52 — POPOLNA DVOLETNA KONTINUITETA: isti starši + ISTA botra** Matija Milek + Katarina Križan; Milek = P81 near-miss), h61 (oče **Nikolaj Pošek/Požek [~] = P82 SIDRO 1887 Miko Požek — ISTA OSEBA po 4 letih; mati MENJANA: 1887 Bara Filak → 1891 Ana Dragos [~ Dragoš] — PRVI dokaz menjave gospodinjstva na zasidrani hiši**; 3 krstni vpisi 1887+1897+1891; edini vpis brez botre/podpisa), h53 (oče Janez Pozdirec [~] × mati Marija Križan [~]), h2 (oče Peter Hlebec [~] — **TROJNA KONTINUITETA P82 1887 + P84 1889 + 1891, ISTI starši ×3**), h31 (mati **Marjeta Straus [~] — ISTA OSEBA 1887 Margaretha + 1890 + 1891, 3 vpise čez 5 let**; oče Papič [~] → Tepič [~] Kurrent P/T; botra Klobučar 4. leto), h5 (vsi **TOREC** — ponovitev čez knjige; modro ime »Terezija?« [~] vs tmavo »Jožefa«), h28 (oče **Jurij Požek [~] — POŽEK VERIGA h79 1888 → h77 1890 → h28 1891, 3. hiša familije v 4 letih**; mati Milkovič [~] = Milek varianta); **DVE menjavi matere na zasidranih hišah** (h61 + h72 — druga žena / ponovna poroka / re-read [~], MERI); **ŠIMEC 0× — prvo leto brez najtrajnejše familije** (1886: 4 hiše, 1887: 1, 1888: 1, 1889: 3, 1890: 6); priimki z 1825 pričo v 1891: **Križan/Hrižan 8×** (0.8333 [~] — najmočnejše leto), Milek/Milkovič 4×, Straus/Straucelj 3+1 [~] (0.8571), Požek/Pošek 2× (4. leto), Dragoš 1× (1.0), Urh 1× [~] (1.0), Jakobič 2×; babice: Ana Hrižan 4× (vrnitev po 1889) + Brinec 2× (6./7. leto) + Marjeta Fojter 2× (nova); duhovniki **Jos. Rauq [~] 7** + Jos. R— 1 + prazna 1; **NOV podpis St. Češarek [~] od r68** (menjava sredi decembra 1891, 0× na Gribljih);
  `scripts/p86_parish_baptism_1891.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1891.json` (SAMPLE-TRANSCRIPTION-1891) + `parish.ts` HOUSE_VITALS 112 → **121** (9 zasidranih) + QA 86 → **87/87** (nova qa-p86-parish-baptism-1891: celoven neodvisen preracun okvir/PT 8/1/sidra h72–h28/kontinuiteta h30 prek 1890 blokov/trojna kontinuiteta h2/menjava matere h61 prek 1887 bloka/ponovitve vključno h5 04894/NOVE hiše/vitals 121; dve obliki repo/produkcija) + atlas.ts PT_GAP_KNOWN + **53** + p80 skripta I7 P86 scoping (vitals 121) + p85 skripta I10 kumulativno (127; klasifikacija v pre-P86 vesolju); kartica NI dodana (vzorec P77–P85); veriga `p60–p67 + p70–p86 --check` PASS; tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).

- **župnija Podzemelj — krstna knjiga 04105, polno leto 1892 (P87, issue #18)** — P86 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1892: skeni 56–63 == strani 55–62** (stran == sken − 1; glava »Leto 1892« na str. 55 row 1 po 1891 rows 65–75; vpisi na skenih 56, 57, 60, 61, 62 — 58/59 brez Gribljev; **velike cifre »1893~« na str. 62 po row 82** — oznake se ponastavijo na 1, novela P83 potrjena **5. leto**; leto 1892 ima 82 zveznih vrstic; glave mesecev se ponavljajo — Avgust 2×, November 2×); **NOVELA (novela P85 potrjena 3. leto): vsi statusi ulomki ali poklici** — ½ zemljak 5 + ¼ zemljak 4 + **bajtar 2** (vrnitev po 1891: 0) + **učitelj 1** — **VSI vpisi z Griblji: 12 vpisov / 12 hiš — NARE** (prvo leto brez ponovitev znotraj leta; 0 neberljivih; HOUSE_VITALS 12 zasidranih): 75, 29, 73, 12, 27, 1, 32, 58, 90, 63, 61, 24 — **NOVE hiše 3 (12, 73, 75)** + ponovitve 9 — skupaj s P79–P86 vzorec **139 vpisov / 61 hiš čez tri knjige in sedem let**; **PT klasifikacija 11/1 — luknja 41–60: 58 že dokazana (P84/P85), brez novih** (ostaja 14 dokazanih); 0 nezakonskih; r70 h61 edini vpis brez botre + brez podpisa (**isti vzorec kot 1891 r39 na ISTI hiši**); **SIDRA**: h58 (oče **Janez Požek [~] × mati Ana Dragos [~] — POŽEK × DRAGOS 3. LETO** 1889+1890+1892, najdaljša zasidrana zveza familije; forenzika izrez: jasno **58**, prvi prebir 53 [~] Kurrent 3/5), h61 (oče **Nikolaj Požek [~] ½ × mati Ana Dragos [~] — KONTINUITETA SIDRA 2. LETO**: P86 1891 ISTA zveza + ISTI vzorec brez botre/podpisa; **status ¼→½ [~] — menjava statusa na zasidrani hiši**; P82 sidro 1887 + 1897 + 1891 + 1892), h63 (oče **Nikolaj Hrižan [~] — ISTI OČE ime+priimek 4×**: 1887 Prižan [Križan] + 1889 Hrigian? [nezakonska] + 1890 Križan ½ + 1892 Hrižan — najmočnejši čez-letni očetovski pin, P85 SIDRO potrjeno), h29 (oče **Peter Milek [~] × mati Ana Križan [~] — ISTA ZVEZA 1888+1892** »hiša epidemije«; mrliška 04894 1886: trije Mileh otroci v koleri), h1 (oče **Nikolaj Željko [~] × mati Katarina Kure [~] — ISTA ZVEZA 1888+1892** (P83 »Zeljth« re-read); **najnižja hišna številka v vzorcu**), h32 (oče **Matija Urh [~] — ISTI OČE 3×** 1889+1890+1892; Urh veriga 1887–1892, 6 let; PUA urh 1.0), h90 (**ŠOLSKA HIŠA**: učitelj **Franc Kopitac [~] × Marija Schweizer [~] — ISTA UČITELJSKA DRUŽINA 1890+1892**; botra Janez Barle **nadučitelj** — prvi v vzorcu), h24 (oče **Martin Jurajevič [~] bajtar — MENJAVA GOSPODINJSTVA**: Brinec 1887 + anomalija 1890 → Jurajevič 1892, 4. vpis; forenzika 4x: kraj jasno Griblje, modri pripisi so mrliški), h27 (oče **Marko Pozdirec [~] bajtar — MENJAVA GOSPODINJSTVA**: oče 1887 Kukar = 1890 Stubhar ISTI (re-read) → 1892 Pozdirec); **ŠIMEC 0× — 2. leto zapored** (1886: 4, 1887: 1, 1888: 1, 1889: 3, 1890: 6, 1891: 0, 1892: 0); babice: **Marija Brinec 4×** (8.–10. leto) + Ana Križan 3× + Marjeta Trotter 2× (nova) + Ana Krajnovec 1×; duhovnika **SOČASNO aktivna 1892**: Fr./St. Češarek [~] 8 (Jan–Sep) + **Jos. Rauq [~] 3 (Feb!, Okt–Dec)** — menjava P86 decembra 1891 **NI dokončna**; r13 podpis celo ime »Franc Češarek« [~];
  `scripts/p87_parish_baptism_1892.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1892.json` (SAMPLE-TRANSCRIPTION-1892) + `parish.ts` HOUSE_VITALS 121 → **133** (12 zasidranih) + QA 87 → **88/88** (nova qa-p87-parish-baptism-1892: celoven neodvisen preracun okvir/PT 11/1/sidra h58–h27/kontinuitete 14 pinov vključno h63 1889 Hrigian + h24 1887 Brinec/1890 ANOMALIJA/NOVE hiše/vitals 133; dve obliki repo/produkcija) + qa-p86 vitals pin 133 + qa-p85 h90 dovoli 1892 blok (P87 kontinuiteta) + atlas.ts PT_GAP_KNOWN komentar (58 ponovitev, brez novih) + p80 skripta I7 P87 scoping (vitals 133) + p85/p86 skripti I10 kumulativno (139; hiše 60); kartica NI dodana (vzorec P77–P87); veriga `p60–p67 + p70–p87 --check` PASS (25 skript); tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).

- **župnija Podzemelj — krstna knjiga 04105, polno leto 1893 (P88, issue #18)** — P87 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1893: skeni 63–70 == strani 62–69** (stran == sken − 1; glava »1893~« na str. 62 po 1892 row 82; vpisi na skenih 63–68; **velike cifre »1894« na str. 69 po row 83** — oznake se ponastavijo na 1, novela P83 potrjena **6. leto**; leto 1893 ima 83 zveznih vrstic) — **VSI vpisi z Griblji: 17 vpisov / 16 hiš — h27 DVOJČICI** (Antonija †13/9.93 + Ivana; vertikalni pripis »dvojčice«; vsi starševski stolpci r34 »isto«; 2. dvojčki v vzorcu po P85 h30, prvi z eksplicitnim pripisom): 60, 65, 41, 70, 23, 91, 27 ×2, 15, 46, 72, 30, 24, 74, 21, 25, 32 — **NOVE hiše 4 (23, 46, 70, 91)** + ponovitve 12 (h60 nova krstna — poroka 04455 1886 Maria Bohor GRIBLJE 60) — skupaj s P79–P87 vzorec **156 vpisov / 65 hiš čez tri knjige in OSEM LET**; **PT klasifikacija 13/3 — luknja 41–60: 46 NOVA (15. dokazana številka!)**; 41 že dokazana (P85; 3. vpis), 60 že dokazana (P80 poroka; prvi krstni vpis); 0 nezakonskih; r50 brez babice (edini); r34 ditto; **SIDRA**: h72 (oče **Matija Strauš [~] — SIDRO 3. VPIS: ISTI oče 3× čez 6 let** 1888+1891+1893; mati 1891+1893 ISTA Jakobič; botra Straucelj ISTA 2×; tri-virska P80 + PUA @71 0.8571 — **najmočnejša veriga vzorca**), h65 (oče **Matija Milek [~] — ISTI 3×** 1887+1889+1893; Milek = P81 near-miss), h27 (oče **Janez Stukar/Stubhar [~] = 1887 Kukar + 1890 Stubhar ISTI**; ISTA mati Katarina Klobučar — 3.+4. vpis; forenzika 5x: jasno 27, prvi prebir 24 [~]), h21 (oče **Janez Požek [~] ISTI 1887+1893; MATI MENJANA: 1887 Brinec → 1893 Ana Šimec** — 3. dokazana menjava matere po h61/h72; **ŠIMEC NAZAJ NA GRIBLJIH** — mati + botra Janez Šimec prvič od 1890), h24 (oče **Matija Brinec [~] × Barbara Jakobčič [~] — ISTA ZVEZA kot 1887**; **5. VPIS**; gospodinjstvi Brinec ↔ Jurajevič se izmenjujeta 1887→1892→1893), h30 (oče **Peter Jakljevič [~] × Marija Kralj [~] — MENJAVA GOSPODINJSTVA** Milek → Jakljevič; babica PRAZNA; podpis obiskni G. Ambrož? m.p.), h41 (oče **Matija Hušič? [~] × Neža Jakobič [~] — ISTA ZVEZA kot 1890**; 3. vpis na luknji), h15 (oče **Janez Jaklič [~] × Marija Brinec [~] — ISTA ZVEZA kot 1887** Jakšič × Brinec), h60 (**NOVA krstna** — oče **Nikolaj Željko [~] = h1 oče — ŽELJKO 2. HIŠA**: h1 → h60), h91 (**NOVA** — botra **Nikolaj Željko + Katarina Kure** = h1 starši priimki — **Željko signal 3 hiš**: h1, h60, h91), h74 (mrliška 04894 1886 **Hambeč [~]** → **Kambič? [~]** — čez knjige varianta), h25 (poroka 04455 1886 Klepec → 1893 **Matija Hrižan × Ana Požek** — menjava gospodinjstva; 2. Hrižan oče), h32 (oče **Matija Meh/Mrh? [~] — MERI**: ISTA mati Pegdirec + ISTA botra Hrižan/Strauš kot 1892 Urh — isti oče z novo brano priimko ali drug mož); **ŽELJKO VERIGA 3 hiš**; babice: **Trotter 9×** (nova dominanta) + Ana Hrižan 3× + Barbara Adlešič 2× + Ana Križan 1× + Ana Klepec 1× + prazna 1; DUHOVNIKI: **Jos. Rauq [~] 14 (Jan–Avg) + NOV Janez Jelovšek? [~] 2 (od septembra)** + G. Ambrož? m.p. 1 (obiskni);
  `scripts/p88_parish_baptism_1893.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1893.json` (SAMPLE-TRANSCRIPTION-1893) + `parish.ts` HOUSE_VITALS 133 → **150** (17 zasidranih) + QA 88 → **89/89** (nova qa-p88-parish-baptism-1893: celoven neodvisen preracun okvir/PT 13/3/sidra h72–h91/kontinuitete 14 pinov + h60 04455 + h41 any-blok/NOVE hiše/vitals 150; dve obliki repo/produkcija) + qa-p86/p87 vitals pini 150 + qa-p85 h30/h41 dovolita 1893 blok (P88 kontinuiteta) + atlas.ts PT_GAP_KNOWN + **46** (15. dokazana!) + p80 skripta I7 P88 scoping (vitals 150) + p85 skripta I10 kumulativno (156; vesolje brez 1891/1892/1893 blokov) + p86/p87 skripti I10 kumulativno (156; hiše 64); kartica NI dodana (vzorec P77–P88); veriga `p60–p67 + p70–p88 --check` PASS (26 skript); tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).

- **župnija Podzemelj — krstna knjiga 04105, polno leto 1894 (P89, issue #18)** — P88 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1894: skeni 70–78 == strani 69–76** (**NOVELA OKVIRA: sken 73 je PODOVOJEN sken str. 71** — matricula re-scan, prvi v seriji; stran == sken − 1 velja do skena 72, od skena 74 naprej **− 2**; glava »1894« na str. 69 po 1893 row 83; vpisi na skenih 70, 71, 72, 74–78; **velike cifre »1895~« na str. 76 po row 90** — oznake se ponastavijo na 1, novela P83 potrjena **7. leto**; leto 1894 ima **90 zveznih vrstic** — najdaljše doslej) — **VSI vpisi z Griblji: 14 vpisov / 14 hiš** (drugo leto brez ponovitev znotraj leta po P87 NARE): 12, 2, 53, 69, 36, 57, 73, 31, 13, 75, 17, 71, 23, 60 — **NOVELA VZORCA: 0 NOVIH hiš** (vseh 14 že zasidranih — **vzorec se ZASIČA**; 65 hiš naprej) — skupaj s P79–P88 vzorec **170 vpisov / 65 hiš čez tri knjige in DEVET LET**; **NOVELA (novela P85 potrjena 5. leto): vsi statusi ulomki** — ½ zemljak 8 + ¼ zemljak 6 (brez bajtarjev/obrtnikov); **PT klasifikacija 11/3** — luknja 41–60: **53 + 57 + 60 vse tri PONOVITVE, brez novih** (ostaja 15 dokazanih); 0 nezakonskih; r50 brez babice (druga po P88); **SIDRA**: h2 (Peter Hlebec [~] ¼ × Ana Jakobič [~] — **ŠTIRIKRATNA KONTINUETETA: ISTI starši vseh 4× 1887+1889+1891+1894 — najdaljša zasidrana zveza vzorca**; moder pripis: mati † 1965 Novo mesto), h71 (Jurij Straus? [~] ¼ × Barbara Jakobčič? [~] — **ISTA ZVEZA čez 8 let**: P77 1886 r83 »Jurij Strauš ½ × Barbara Jakopič«; status ½→¼; **STRAUŠ na DVEH sosednjih hišah h71+h72** — **PUA @71 0.8571 dobi krstno oporo**), h36 (Janez Križan? [~] ¼ × Katarina Straucelj? [~] — 3. krstni vpis + **4. VIR tri-virske hiše: KRIŽAN 2. GENERACIJA** — Matija 1882/1886 → Janez 1894, mogoč sin [~]), h31 (Martin Fapič? [~] ½ × Marjeta Straus? [~] — **4. VPIS 1887+1890+1891+1894**: oče Papič/Fapič/Tepič ISTI + mati ISTA vseh 4× + botra **Marko Klobučar ISTI** — najbolj popolna trojica), h17 (Janez Kralj? [~] ¼ — **ISTI oče ISTA frakcija** kot P82 1887; **MATER MENJANA: Ana Jakobič → Doroteja Firlak? [~] — 5. dokazana** po h61/h72/h21), h57 (Peter Pegdirec? [~] × Marija Županc? [~] — 2. vpis čez 8 let; **ISTA BOTRA PA čez 8 let**: Jurij Brodarič? + Marija Strauš? = P77 r20), h60 (Nikolaj Željko [~] ¼ × Marija Brodarič [~] — **h60 2. VPIS ISTA zveza + ISTA BOTRA PA 2. leto** (P88 r1); status ½→¼; **ŽELJKO VERIGA 4 signali**: h1 + h60 + h91 botra + h25 botra), h23 (Matija Brinec [~] ½ — **ISTI oče + ISTA BOTRA PA 2. leto** (P88 r28); mati Debič?/Žehlič? varianti), h12 (Janez Dragoš [~] ½ — ISTI oče kot P87, 2. vpis), h53 (Janez Pegdirec? [~] × Marija Hrižan? [~] — ISTA zveza kot P86 Pozdirec × Križan + babica ISTA), h73 (Nikolaj Županič? [~] × Katarina Pozdirec/Pegdirec? [~] — ISTA zveza kot P87), h75 (Janez Jakobič? [~] × Marija Stubljar? [~] — ISTA zveza kot P87 Jakobčič × Sušljar; **botra Barb. Brinec ISTA 2. leto**), h13 (Matija Jakljevič? [~] ½ — ISTI oče ime+status kot P77 »Jakopič? ½«; tri-virska; **babica PRAZNA**), h69 (Janez Brinec [~] × Ana Kure [~] — **NOV krstni vpis čez knjige**: mrliška 04894 1886; botra **Katarina Požek? — Požek 7. leto**); **Pegdirec/Pozdirec 7/14 vpisov** (najgostejša botrska familija 1894); menjave statusov h71/h60 (½→¼); DUHOVNIKI: **Jan Jelenu—? [~] 11** (verjetno ISTI kot P88 »Jelovšek?« — varianti istega podpisa [~]) + **Jos. Rauq? 3** (Feb/Sep/Dec — izmenjava NI čista); babice: **Trotter 11×** (2. leto dominanta; »Jotter«; »Margan.« = Margareta) + Ana Hrižan 2× + prazna 1;
  `scripts/p89_parish_baptism_1894.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1894.json` (SAMPLE-TRANSCRIPTION-1894) + `parish.ts` HOUSE_VITALS 150 → **164** (14 zasidranih) + QA 89 → **90/90** (nova qa-p89-parish-baptism-1894: celoven neodvisen preracun okvir z novelo podvojenega skena/PT 11/3/sidra h2–h60/NOVELA 0 novih hiš (vsaka mora imeti prejšnje zasidranje)/kontinuitete 19 pinov/vitals 164; dve obliki repo/produkcija) + qa-p86 h53 dovoli 1894 blok + qa-p87 h12/h73/h75 dovolijo 1894 bloke + qa-p88 h23 dovoli 1894 blok + qa-p86/p87/p88 vitals pini 164 + atlas.ts PT_GAP_KNOWN komentar (P89: brez novih) + p80 skripta I7 P89 scoping (vitals 164) + p85 skripta I10 kumulativno (170; vesolje brez 1891/1892/1893/1894 blokov) + p86/p87/p88 skripti I10 kumulativno (170; hiše 64; vsak z lastnim vesoljem pre87/pre88/pre89); kartica NI dodana (vzorec P77–P89); veriga `p60–p67 + p70–p89 --check` PASS (27 skript); tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…).
- **župnija Podzemelj — krstna knjiga 04105, polno leto 1895 (P90, issue #18)** — P89 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1895: skeni 78–84 == strani 76–82** (**NOVELA P89 POTRJENA 2. LETO: stran == sken − 2 ZA CELO LETO**; sken 73 podvojen, NI citiran; glava »1895.~« na str. 76 po 1894 row 90; **prelom 1896 na str. 83 = sken 85 po row 73** — oznake se ponastavijo na 1, novela P83 potrjena **8. leto**; leto 1895 ima **73 zveznih vrstic**) — **VSI vpisi z Griblji: 15 vpisov / 14 hiš** (**h24 DVOM 2× — prva ponovitev hiše znotraj leta po P87 NARE**: r22 Brime × Jakobič + r48 Toško? × Simec, forenzika vztraja 24, alternative 21/27 [~]): 58, 46, 87, 24 ×2, 12, 30, 20, 65, 32, 37, 69, 72, 91, 29 — **3 NOVE hiše (20, 37, 87)** po P89 »0 novih« + 11 ponovitev — skupaj s P79–P89 vzorec **185 vpisov / 68 hiš čez tri knjige in DESET LET**; **NOVELI VZORCA: ① babica stolpec na VSEH 15 vrsticah PRAZEN** (1894: Trotter 11×!) — **Trotter žene pa 7× kot BOTRA — vloga prestopila**; ② **4× PRAZNA botra** (sep–dec cluster); novela P85 potrjena 6. leto (½ 10 + ¼ 2 + bajtar 1); **PT klasifikacija 12/2** — luknja 41–60: **h46 2. dokaz (P88+P90) + h58 4. vpis, brez novih** (ostaja 15 dokazanih; 20/30/37/87/91 vse v naboru PT); 0 nezakonskih na Gribljih (2 izven: Primostek + Krasinec); **MATI PODCELICA (X × Y) prvič eksplicitno dokumentirana** — semantika ODPRTA; **SIDRA**: h58 (Janez Požek [~] ISTI 3. leto zapored — **4. VPIS; MATI MENJANA: Ana Dragoš → Katarina Kambic? [~]** — mrliška 04894 bi dokazala), **h32 + h72 — 5. VPIS, NAJDALJŠI zvezi vzorca (1889–1895)** (Urh × Pegdirec ISTA 5×; Straus × Jakobič ISTA 5×), h69 (**oče Brinec ISTI vseh 5×**; mati 5. različno branje [~]), h30 (**3. DRUŽINA — 2× menjava gospodinjstva: Milek → Jakljevič → Šegina** — najbolj nestabilna hiša), h29 (**MENJAVA — »hiša kuge« popolnoma prekinjena**: Milek × Križan → Kuhar? × Klobučar), h91 (**oče MENJAN: Novak → Muc**; mati Kure ISTA; »mlinar in kovač?«), h46 (2. VPIS ISTA zveza — 2. dokaz luknje), h24 (3. VPIS ISTA zveza + r48 DVOM), h12 (3. VPIS; mati 3. branje [~]), h65 (4. VPIS; mati Požek ISTA 2×), **h87 NOVA (PEGDIREC PRVIČ STARŠI; podcelica Hrižan × Željko)**, h20 NOVA (podcelica blizu para h65), h37 NOVA (**ANOMALIJA: isti oče kot h20, druga žena! [~]**); **ŽELJKO VERIGA 6 signalov** (h1 + h60 + h91/h87/h66 podcelice + h25 botra); DUHOVNIKI (**TRIJE hkrati**): Jelenuš/Jelez? **9×** + Rauq **4×** (apr–sep) + **NOV Franc Klunng? 2× od septembra**; babice **0 zabeleženih** (NOVELA);
  `scripts/p90_parish_baptism_1895.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1895.json` (SAMPLE-TRANSCRIPTION-1895) + `parish.ts` HOUSE_VITALS 164 → **179** (15 zasidranih) + QA 90 → **91/91** (nova qa-p90-parish-baptism-1895: celoven neodvisen preracun okvir z novelo (stran == sken − 2 za celo leto)/NOVELA babica 15 praznih/PT 12/2/sidra h58–h29 + DVOM/NOVE hiše 20/37/87 brez priora/kontinuitete 26 pinov/vitals 179; dve obliki repo/produkcija) + qa-p85 h30 dovoli 1895 blok + qa-p87 h12 dovoli 1895 blok + qa-p88 h46/h91 dovolita 1895 bloka + qa-p86/p87/p88/p89 vitals pini 164 → 179 + p80 skripta I7 P90 scoping (vitals 179) + p85/p86/p87/p88 skripti I10 kumulativno (185; hiše 67; vesolja brez 1895 blokov); kartica NI dodana (vzorec P77–P90); veriga `p60–p67 + p70–p90 --check` PASS (28 skript); tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…). Lekcije: PT iz osnutka (9/5) neustrezen → veriga ujela, dokaz popravljen na 12/2; duhovniki 8+3+2 → 9+4+2 (neodvisen preracun).
- **župnija Podzemelj — krstna knjiga 04105, polno leto 1896 (P91, issue #18)** — P90 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1896: skeni 85–92 == strani 83–90** (**NOVELA P89 POTRJENA 3. LETO: stran == sken − 2 ZA CELO LETO**; sken 73 podvojen, NI citiran; glava »1896« na str. 83 po 1895 row 73; **leto 1896 ima 94 zveznih vrstic — NAJDALJŠE doslej** (1894: 90); **prelom 1897 na str. 91 = sken 93 po row 94** — novela P83 potrjena **9. leto**) — **VSI vpisi z Griblji: 14 vpisov / 14 hiš — NARE (3. leto)** po P87 1892/P89 1894: 9, 14, 31, 36, 1, 25, 46, 26, 41, 15, 63, 45, 53, 30 — **3 NOVE hiše (9, 14, 45)** + 11 ponovitev — skupaj s P79–P90 vzorec **199 vpisov / 71 hiš čez tri knjige in ENAJST LET**; **NOVA LUKNJA ŠTEVILKA: h45 — 16. dokazana v 41–60, prva nova od P88** (PT_GAP_KNOWN +45) + **h41 4. dokaz + h46 3. dokaz + h53 3. dokaz** — luknja zdaj 16 dokazanih; **NOVELA babica POTRJENA 2. LETO: 14/14 PRAZNO** (Trotter žene 0× — izginejo tudi kot botre); statusi: **½ zemljak 12 + bajtar 2 — prvo leto brez ¼** (novela P85, 7. leto); DUHOVNIKI: **NOV Fr. Šuvar? 9×** (dominanta Jan–Jun) + Rauq 4× (Feb/Sep/Okt/Dec) + r5 brez podpisa (3. primer) — **P90 trojica se krči** (Klunng in Jelenuš izginejo); **KURRENT FORENZIKA 4 popravki**: r25 26→**25** (referenčna primerjava Gradac 25!), r31 16→**46**, r92 25→**30** (starša Šegina × Mihelt = h30 1895 potrdita), r13 37?→**31**; **MATI PODCELICA izgine**; dojenčijska umrljivost († ×3 + r5 krsta prazna); **SIDRA**: h1 (Nikolaj Željko [~] ½ × Katarina Kure — **3. VPIS ISTA ZVEZA 1888+1892+1896 — 8 let; botra ISTI priimki kot starši vse 3× — začarani krog familije; ŽELJKO VERIGA 8 signalov**), h63 (**OČE ISTI VSEH 5×** 1887–1896 — najbolj konstanten oče), h30 (Šegina × Mihelt — **ISTA ZVEZA 2. LETO — 3. družina se je UNESLA**), h41 (Hušič × Jakobič — **4. VPIS ISTA ZVEZE**), h15 (Jaklič × Brinec — **3. VPIS**), h36 (Križan × Straucelj — **2. VPIS**; tri-virska dobi 5.+6. vir), h53 (Pendirec? × Hrižan — **3. VPIS VARIANTE** 1891+1894+1896), h46 (Brodarič 3. VPIS + **MATI MENJANA**: Klobučar → Kramarič?), h31 (**MENJAVA**: Fapič × Straus → Pendirec bajtar × Žugelj), h25 (**KLEPEC NAZAJ** — vrnitev originalne familije 10 let po poroki 04455), h26 (**ANOMALIJA: ISTI priimki kot h75 zveza — 3. vpis na DRUGI hiši** 75→26: selitev ali napaka [~]), h9/h14 NOVE (h14: **neimenovan otrok** + krsta PRAZNA + brez botre/podpisa — najbolj fragmentaren vpis), h45 NOVA (Martin Straus? bajtar — **Straus signal 3. hiša**; botra POD TRAKOM [?]);
  `scripts/p91_parish_baptism_1896.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1896.json` (SAMPLE-TRANSCRIPTION-1896) + `parish.ts` HOUSE_VITALS 179 → **193** (14 zasidranih) + QA 91 → **92/92** (nova qa-p91-parish-baptism-1896: celoven neodvisen preracun okvir z novelo (94 vrstic — najdaljše)/NOVELA babica 14 praznih/NOVA LUKNJA 45 pin/PT 10/4/sidra h9–h30/NOVE hiše 9/14/45 brez priora/kontinuitete 25 pinov/vitals 193; dve obliki repo/produkcija) + **atlas.ts PT_GAP_KNOWN + 45** + qa-p85 h30/h41 dovolita 1896 bloka + qa-p86 h53 dovoli 1896 blok + qa-p88 h46 dovoli 1896 blok + qa-p86/p87/p88/p89/p90 vitals pini 179 → 193 + p80 skripta I7 P91 scoping (vitals 193) + p85/p86/p87/p88/p89/p90 skripti I10 kumulativno (199; hiše 70; vesolja brez 1896 blokov); kartica NI dodana (vzorec P77–P91); veriga `p60–p67 + p70–p91 --check` PASS (29 skript); tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…). Lekcije: Kurrent 5/6 referenčna primerjava (r25 25 ≠ 26 — skladno s Klepec h25); Python vstavljanje pustilo `]` namesto `];` — p81 regex ujela;

- **župnija Podzemelj — krstna knjiga 04105, polno leto 1897 (P92, issue #18)** — §68 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1897: skeni 93–101 == strani 91–98** (**NOVELA P92: SKEN 97 = PODVOJEN** — duplikat s96 = str. 94, **2. znani duplikat po skenu 73**; **NOVELA P89 (stran == sken − 2) velja samo do skena 96, od skena 98 stran == sken − 3 — premik offseta je ARTEFAKT DUPLIKATA, ne nova številčenja**; glava »Leto 1897« na str. 91 po 1896 row 94; **leto 1897 ima 85 vrstic**; **prelom 1898 na str. 98 = sken 101 row 86** — novela P83 potrjena **10. leto**) — **VSI vpisi z Griblji: 19 vpisov / 18 hiš — NARE (4. leto)** po P87/P89/P91: 12, 32, 10, 24, 37, 54, 60, 2, 43, 23, 46, 31, 16, 40, 20, 31, 61, 65, 45 — **h31 2 VPISA V ENEM LETU** (r51 Sapič? × Straus + r64 Straus? × Jakobič — **STRAUS KOMPLEKS**: 1894 Fapič?×Straus → 1896 Pendirec?×Žugelj menjava → 1897 obe nazaj!) — **3 NOVE hiše (10, 40, 43)** + 15 ponovitev — skupaj s P79–P91 vzorec **217 vpisov / 74 hiš čez tri knjige in DVANAEST LET** (211 vitals; **h61 sidro ZDRUŽENO s P79-era placeholderjem — ČEZ-FAZNA POTRDITEV**: izvirna prepis hiše 61 je opazila »Anton, oče Miha P.—« pri strani 49 po stari predpostavki, P92 5x forenzika dopolni Janez Muc bajtar × Ana Kure, stran 97 po noveli); **NOVA LUKNJA ŠTEVILKA: h43 — 17. dokazana v 41–60** (PT_GAP_KNOWN +43; številka NA RAZPOKI [~]) + **h54 2. dokaz + h60 4. dokaz** — luknja zdaj 17 dokazanih; **PRVI NEZAKONSKI VPIS OD P90: r31 Florijan — OČE PRAZEN, mati Katarina Pozdirec SAMA MATI ¼ zemljatva** (novela P85, 8. leto); **NOVELA babica POTRJENA 3. LETO: 19/19 PRAZNO** (Trotter žene 0× 3. leto); **DOJENČIJSKA UMRLJIVOST 7/19 — NAJVIŠJE doslej** (P91: 4/14): † r12 (24/1.98?), r15 (5/9.97?), r25 (17/9.97?), r28 (16/2.98?), r29 (7/6.97), r38 (3/9.99?), r59 (3/9.98?); DUHOVNIKI: **Šuvar (1896 dominant) IZGINE — Klun 11× + Rauq 8× — MEŠANO LETO** (preplet skozi vse mesece); statusi: **½ × 16 + bajtar × 2 + ¼ × 1** (sama mati); **KURRENT FORENZIKA 6 POPRAVKOV**: ① h23/h24 (r21 jasno 24 + r38 jasno 23 — **DVE RAZLIČNI Brinec hiši**, prvi prebir »oba 23« napačen) ② s93 r11 »Grablje?« → jasno **GRISICE** (druga vas — izključena; isto št. 2 kot Griblje r29!) ③ s99 r65/66 »Griblje 11?« → jasno **OTOK** (izključena) ④ s98 r53 »Griblje 10?« → jasno **16** ⑤ row številke s99 **59/62/64** (Kurrent 5/6 — kontinuiteta s98 51–58 → s99 59) ⑥ h45 mati = **Barbara Spudič** (5x — **POPRAVEK P91 prebira »Doroteja?«**); **MATIČAR PRIPISI 20. st. 6 vpisov** (najgostejše doslej: r41 † 1931, r52 poroka 1919 + † 1981, r62 † 1980, r64 poroka 1934, r79 zakonca † 1979 + EHS ČG, r80 † 1989 + EHS ČG); **SIDRA**: h45 (Straus bajtar × Spudič — **2. VPIS ISTA ZVEZA 1896+1897 + POPRAVEK matere**), h46 (Brodarič **4. VPIS** + **mati 3. VARIANTA**: Klobučar 1893/95 → Kramarič? 1896 → Harašimovič? 1897 [~]; botra Željko = veriga), h31 (Straus kompleks 2 vpisa), h60 (Željko × Brodarič ISTA zveza — **4. dokaz luknje**), h61 (Muc bajtar × Kure; **botra Nikolaj Željko + Katarina Kure = h1 PAR KOT BOTRA** — ŽELJKO VERIGA 10 signalov, začarani krog kot P91 h1), h24/h23 (dve Brinec hiši — 8. pin h24), **h63 IZGINE** (oče konstanten 5× 1887–96 — konec serije; botra Hrižan 3× v letu po izgini), h2 5. pin, h12 4. pin, h65 5. pin;
  `scripts/p92_parish_baptism_1897.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1897.json` (SAMPLE-TRANSCRIPTION-1897) + `parish.ts` HOUSE_VITALS 193 → **211** (18 novih + sidro h61 združeno) + QA 92 → **93/93** (nova qa-p92-parish-baptism-1897: celoven neodvisen preracun okvir z novelo podvojenega skena (piecewise page_of_scan)/NOVELA babica 19 praznih/NOVA LUKNJA 43 pin/PT 13/5/sidra 19/NOVE hiše 10/40/43 brez priora/kontinuitete 35 pinov (scan-pini)/vitals 211; dve obliki repo/produkcija) + **atlas.ts PT_GAP_KNOWN + 43** + qa-p79/p80 filtri scoperani na originalni P79 vzorec (1897 samo h61) + qa-p87 h12 / qa-p88 h23+h46 / qa-p90 h20+h37 / qa-p91 h45 dovolijo 1897 bloke + qa-p86/p87/p88/p89/p90/p91 vitals pini 193 → 211 + p80 skripta I7 P92 scoping (vitals 211) + p85/p86/p87/p88/p89/p90/p91 skripti I10 kumulativno (217; hiše 73; vesolja brez 1897 blokov); kartica NI dodana (vzorec P77–P92); veriga `p60–p67 + p70–p92 --check` PASS (30 skript); tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…). Lekcije: podvojen sken premakne stran==sken−2 → −3 (artefakt, ne novela številčenja); h61 P79-era placeholder združen z P92 forenziko (čez-fazna potrditev, ne duplikat);


- **župnija Podzemelj — krstna knjiga 04105, polno leto 1898 (P93, issue #18)** — §69 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1898: skeni 101–109 == strani 98–106** (**NOVELA P92 POTRJENA: stran == sken − 3 ZA CELO LETO** — brez novih duplikatov; **sken 105 = str. 102 brez Griblje vrstic** — pregledan, ni citiran; glava »1898.« na str. 98 po 1897 row 85; **leto 1898 ima 96 vrstic**; **prelom 1899 na str. 106 = sken 109 row 97→1** — novela P83 potrjena **11. leto**; **1899 row 1 = Griblje 12 Marija — novo leto se začne z Griblji!**) — **VSI vpisi z Griblji: 12 vpisov / 12 hiš — NARE (5. leto)** po P87/P89/P91/P92: 40, 69, 89, 18, 32, 36, 33, 48, 63, 52, 53, 90 — **3 NOVE hiše (18, 48, 89)** + 9 ponovitev — skupaj s P79–P92 vzorec **229 vpisov / 77 hiš čez tri knjige in TRINAJST LET** (223 vitals); **NOVA LUKNJA ŠTEVILKA: h48 — 18. dokazana v 41–60** (PT_GAP_KNOWN +48; forenzika 6x: jasno 48, ne 40 — **dvojna zanka = 8**) + **h52 PRVI TRDNI PIN** (1887 [~] po trojni korekciji 52→04→15) — luknja zdaj 18 dokazanih; **VRNITEV h63: oče Nikolaj Hrižan ISTI 6×** (1887–1898 brez 1897; **P92 »konec serije« POPRAVLJEN**; dojenček Jožef † 6/6.1900); **NAJGOSTEJŠE GIBANJE GOSPODINJSTEV (4 rotacije v enem letu)**: h69 MENJAVA Brinec (5 vpisov 1888–95) → **Nikolaj Straus × Marija Jakobšič** (Straus na 4. hiši; otrok † 6.1.1983 »v Gribljah«), h33 MENJAVA Brinec → **Dehlič × Rožek** (stari Brinec zdaj BOTRA), **SELISTEV Berkopne × Klobučar h40 → h48** (ISTA zveza), h40 MENJAVA → **Anton Brodarič × Marija Milek** (= h46 oče 1893–97; **očetovo ime PREČRTANO v izvirniku**); **ŠOLSKA HIŠA h90: TRETJI UČITELJ** — Kopitar (1890+1892) → **Alojzij Vetročnik UČITELJ × Leopolda Schmelzer** (nemški priimek); botr učitelj **Ivan Vrhovec** — tretja učiteljska generacija; **0 nezakonskih** med Griblji (r29 Obveca = druga vas); **NOVELA babica POTRJENA 4. LETO: 12/12 PRAZNO**; **DOJENČIJSKA UMRLJIVOST 1/12** (+ r37 [~]) — najnižja po P92 7/19; DUHOVNIKI: **Rauq 8× + Šturm 3× + 1 neberljiv — Klun (11× 1897) IZGINE**; statusi: ½ × 10 + ¼ × 2 + učitelj × 2; **KURRENT FORENZIKA 6 POPRAVKOV**: ① s101 r5 »Griblje 39?« → jasno **GRIŠINIČE 33** (izključena) ② s107 r76 »Griblje?« → jasno **ŠRIGLJE?** (izključena) ③ s102 r20 **LEVI DEL UNIČEN** (desni: Jurij Straus × Marija Jakofin — verjetno Griblje [~], NEŠTET) ④ s107 r72 »40?« → jasno **48** (6x) ⑤ s106 r63 »56?« → jasno **36** (5x) ⑥ s103 r22 »2?« → jasno **69** + r30 »81/31?« → jasno **89** (Kurrent 9 z dolgim repom); priimki: **Hrigar = Hrižan/Križan cluster**, **Podrinc = Pendirec cluster**, **Urk = Urh cluster** [~]; **MATIČAR PRIPISI v 9/12 vpisov** (najgostejša pokritost: EMŠO blok 1982–83, † 1951–1983, poroke 1921–1929); **SIDRA**: h63 VRNITEV (oče 6×), h69/h33 menjavi, h48 selitev + NOVA LUKNJA, h90 tretji učitelj, h53 **4. VPIS ISTA ZVEZA** + botra **Ana Kure** (h1 familija), h36 **3. VPIS ISTA ZVEZA** (tri-virska hiša 7.+8. vir), h32 8. pin (Urk varianta), h89+h18 NOVI (Šimec 5. hiša; oče Matija Šimec = r89 botra — ista oseba oče + botra), h52 prvi trdni pin; **ŽELJKO VERIGA 2 nova signala — skupaj 12**;

  `scripts/p93_parish_baptism_1898.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1898.json` (SAMPLE-TRANSCRIPTION-1898) + `parish.ts` HOUSE_VITALS 211 → **223** (12 novih 1898 blokov) + QA 93 → **94/94** (nova qa-p93-parish-baptism-1898: celoven neodvisen preracun okvir − 3 za celo leto/brez duplikatov/NOVELA babica 12 praznih/NOVA LUKNJA 48 pin + SELITEV/VRNITEV h63 + OČE ISTI 6× + † 1900/h52 TRDNI pin/sidra 12/PT 9/3/NOVE hiše 18/48/89 brez priora/kontinuitete 22 pinov (scan-pini)/vitals 223) + **atlas.ts PT_GAP_KNOWN + 48** + qa-p85 h90 / qa-p86 h53 / qa-p92 h40 dovolijo 1898 bloke (allow mehanizem) + qa-p85–p92 vitals pini 211 → 223 + **POPRAVI ZASTARELIH SKRIPT (regresije po P92)**: p80 I7 (PT_GAP_HOUSES +43/45/46/48 + scoping 38 hiš/9 luknj + vitals 223), p85–p92 filtri vesolja lastnega leta (poznejši bloki 1897/1898 ne spreminjajo zgodovinske klasifikacije novih hiš: p85 +1897/98, p86 +1897/98, p87 +1897/98, p88 +1897/98, p89 +1895–98, p90 +1896–98 + None-varna repeatHouses, p91 +1897/98 + kumulativ POPRAVLJEN 199/71, p92 +1898) — vseh 14 skript p80–p93 `--check` PASS (exit 0); kartica NI dodana (vzorec P77–P93); tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…). Lekcije: klasifikacija »nove hiše« je zgodovinska — poznejši bloki ne smejo spreminjati preteklih let (filtri vesolja); prečrtano očetovo ime brez zamenjave = dokumentiraj, ne ugani;


- **župnija Podzemelj — krstna knjiga 04105, polno leto 1899 (P94, issue #18)** — §70 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1899: skeni 109 row 97 – 118 row 104 == strani 106–115** (**NOVELA P92 POTRJENA: stran == sken − 3 ZA CELO LETO** — brez novih duplikatov; **sken 118 = str. 115 samo okvir** — ni citiran za vpise; **1899 r1 = Griblje 12 Marija** na str. 106 — novo leto se začne z Griblji; **leto 1899 ima 104 vrstic**; **prelom 1900 NA SREDINI str. 115 = sken 118 row 105 — PRVIČ V VZORCU se novo leto NE začne na novi strani**; 1900 row 1 = Krasinec — **prvič z drugo vasjo**; novela P83 potrjena **12. leto**) — **VSI vpisi z Griblji: 15 vpisov / 15 hiš — NARE (6. leto)** po P87/P89/P91/P92/P93 — in **PRVO LETO BREZ znotraj-letnih ponovitev** (vsaka hiša 1×): 12, 46, 27, 60, 59, 22, 41, 21, 40, 1, 30, 75, 57, 49, 34 — **2 NOVI hiši (22, 49)** + 13 ponovitev — skupaj s P79–P93 vzorec **244 vpisov / 79 hiš čez tri knjige in ŠTIRNAJST LET** (238 vitals); **NOVA ŠTEVILKA h22** (v PT naboru 1825 — prvi matrični dokaz; **Nikolaj Milek × Marija Klepec NOVA ZVEZA** — mati [~ ista oseba kot botra h60 Marija Klepac: botra 13.3. + mati 20.3. v 1 tednu]) + **NOVA LUKNJA ŠTEVILKA: h49 — 19. dokazana v 41–60** (PT_GAP_KNOWN +49; forenzika 8x: jasno 49; **Nikolaj Brodarič × Marjeta Milek NOVA ZVEZA** — Brodarič = botra h48 1898 → oče h49 1899; dojenčnica **† 24/6.1900**) — luknja zdaj **42/50/51**; **h60 TRDNI PIN: 4. VPIS ISTA ZVEZA Željko × Brodarič (1893+1894+1897+1899) + 3. ISTA BOTRA PARA Pendirec × Klepac (1893+1894+1899)** — hišna pod modrim pripisom: kanalna forenzika (temen »…o 6o«) + STRUKTURNA POTRDITEV; **ŽELJKO VERIGA 13.+14. signal** (oče h60 + botra h57); **SEGINA VERIGA 3 signali v enem letu** (oče h1 + botra h49 + botra h34); **h40 TRETJA DRUŽINA V TRIH LETIH** (najgostejša rotacija: Berkopne 1897 → Brodarič 1898 [~] → **Martin Straus bajtar × Barbara Spudič** — **STRAUS × SPUDIČ = POTRDITEV poročnega lead-a 04455**); **MENJAVE GOSPODINJSTEV**: h1 **Željko (1888–96) → Segina** (SEGINA VERIGA h70 1893 → h30 1895 → h1 1899 — 3 hiše / 6 let; kraj »Griblja« varianta, smrtna opomba POTRJUJE Griblje † 31.3.1975), h30 **4. DRUŽINA v 9 letih** (Milek → Jakljevič → Šegina → **Janez Županič** — ŽUPANIČ CLUSTER 3 signali), h34 **2. DRUŽINA** (Šimec 1887 → **Nikolaj Šilak? × Katarina Klobučar**), h57 **OČE MENJAVA** Peter Pezdirec → **Miha Pozdirec** (brata? sin?); h46 **5. VPIS ISTA ZVEZA** (4. varianta matere Škaradinič? — potrjena pri Krasinec 32); h27 **6. VPIS** (oče 2. branje **Knekar?** vs Stukar/Stubhar 1893; botra h21 Janez Knekar = KRIŽNI SKLIC); h41 4. / h21 2. / h75 3. VPIS ISTA ZVEZA; h12 mati MENJAVA [~] (Straus 1897 → Cvitkovič 1899); 0 nezakonskih; **NOVELA babica POTRJENA 5. LETO: 15/15 PRAZNO/poškodovano**; **DOJENČIJSKA UMRLJIVOST 3/15** (r1 † 25/6.99 [~], r26 † 2/[5-6].99 [~], r94 † 24/6.00); DUHOVNIKI: **Šturm 6× + Rauq 4× + Klun 2× VRNITEV + 3 neberljivih**; statusi: ½ zemljak × 14 + **bajtar × 1** (r43 Straus); **KURRENT FORENZIKA**: r13 hišna pod pripisom (kanalna + strukturna — **60 TRDNO**), r89 **datum UNIČEN** (raztrgan rob — ~november po sosedi), r71 datum popravek (»23« + »2« nad — verjetno 2.10.), r94 jasno 49 (ne 34 — dvojna forenzika z r100), r61 kraj »Griblja« varianta (smrt † 31.3.1975 v Gribljah potrjuje), **r25 NEŠTET** (matičar ČRNO nadpisal kraj+hišno), r27 Berkoviše + r93 »Germ« izključeni; matičar pripisi 20./21. st. v večini vpisov († 1964/1965/1969/1975/1984, poroke 1921/1926/1930, EMŠO blok);

  `scripts/p94_parish_baptism_1899.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1899.json` (SAMPLE-TRANSCRIPTION-1899) + `parish.ts` HOUSE_VITALS 223 → **238** (15 novih 1899 blokov) + QA 94 → **95/95** (nova qa-p94-parish-baptism-1899: celoven neodvisen preracun okvir − 3 za celo leto/brez duplikatov/prelom 1900 NA SREDINI strani/NOVELA babica 15/NOVA LUKNJA 49 + 19. dokazana/h60 TRDNI PIN + 4. VPIS + 3. BOTRA PARA/h40 STRAUS × SPUDIČ + TRETJA DRUŽINA + bajtar/sidra 13/PT 9/6/NOVI hiši 22+49 brez priora/kontinuitete 27 pinov/vitals 238) + **atlas.ts PT_GAP_KNOWN + 49** + qa-p85 h30+h41 / qa-p87 h12+h75 / qa-p88 h46 / qa-p92 h40 dovolijo 1899 bloke (allow mehanizem) + qa-p86–p93 vitals pini 223 → 238 + **POPRAVI ZASTARELIH SKRIPT (regresije po P93)**: p80 I7 (vitals 238), p85–p92 filtri vesolja + 1899 (p85–p91 nabori, p92 filter (1898, 1899)), p85–p93 vitals 238 + kumulativ 244 + hiše 78 — vseh 15 skript p80–p94 `--check` PASS (exit 0); kartica NI dodana (vzorec P77–P94); tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…). Lekcije: novo leto se lahko začne NA SREDINI strani (1900 — prazne vrstice + glava); »novo« hišo v PT naboru (h22) loči od »nove luknje« (h49); nezakonska mati na hiši (h59 1889 Podirec) pomeni, da je 1899 oče PRVI imenovani;

- **župnija Podzemelj — krstna knjiga 04105, polno leto 1900 (P95, issue #18)** — §71 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1900: skeni 118 row 105 (SREDINA str. 115, P94 dokazano) – 124 row 77 == strani 115–121** (**NOVELA P92 POTRJENA: stran == sken − 3 ZA CELO LETO** — brez novih duplikatov; **sken 122 = str. 119 starševska stran** — citiran v dokazu za starše r45/r46, brez data vpisov; sken 125 = str. 122 = **glava 1901**, samo okvir; **1900 r1 = Krasinec Matija — PRVIČ se novo leto začne z DRUGO VASJO**; **leto 1900 ima 77 vrstic**; sken 121 = **DVA podatkovna panela** (r33–44 levo + r45–56 desno), sken 122 = 2 starševska panela; **r51–56 FIZIČNO RAZTRGANE** — podatki izgubljeni, starši znani) — **VSI vpisi z Griblji: 16 vpisov / 16 hiš — NARE (7. leto)** po P87/P89/P91/P92/P93/P94 — in **2. LETO BREZ znotraj-letnih ponovitev**: 1, 67, 10, 32, 65, 20, 14, 90, 23, 9, 54, 16, 58, 31, 25, 45 — **1 NOVA hiša (67)** + 15 ponovitev — skupaj s P79–P94 vzorec **260 vpisov / 80 hiš čez tri knjige in PETNAEST LET** (254 vitals); **NOVA HIŠA h67** (prvi matrični dokaz; v PT naboru 1825 — ATLAS_HOUSES 61–99 blok; **80. hiša vzorca**; **Nikolaj Straus gumbar × Marija Jakopič — STRAUS gumbar mreža**; EMŠO matičarja 1002900505074 ujema z vrstico!); **SCOPING POPRAVKI**: r5→r3 + r8→r6 (margini str. 115 raztrgani — BREZ ANOMALIJE; hipoteza o 2 nenumeriranih vrsticah ZAVRŽENA), r27→r28…r30→r31 (izpuščen r27 Otok 8), **4 IZPUŠČENE vrstice najdene** (r45 h16, r46 h58, r59 h31, r63 h25 — celostranski pregled), **scopingov r49 »Griblje 51 NOVA LUKNJA« ZAVRŽEN** (Primostek 5!) — **luknja 42/50/51 NESPREMENJENA** (19 dokazanih v 41–60); **PT 13/3** (45/54/58 — vsi že dokazani; 58 NI v PT verigi); **NOVELA babica: stolpec PRVIČ IZPOLNJEN po 15 letih** (Fottre/Foča 7× + Hrižan 1×; 1886–99 prazen!); **DUHOVNIKI: Šturm 0× — PRVIČ V VZORCU** (Rauq 9× + Perg 4× + Klunček 2× — nov duhovnik + 1 neberljiv); **h1 ŽELJKO VRNITEV** (1888–96 Željko × Kure → 1899 Segina → 1900 **Jurij Željko × Barbara Kure** — Jurij = **BOTER h1 1888 → OČE 1900**; ŽELJKO signal 15); **h31 6. PIN ISTA ZVEZA Papič × Straus (1887–1900 — najdaljša zaporedna zveza vzorca; 11. vpis)**; **h45 3. PIN ISTA ZVEZA Straus × Spudič (1896+1897+1900) — 04455 POROČNI LEAD krstno 3× POTRJEN**; **h90 ŠOLSKA HIŠA 4. PIN** (ISTA učiteljska družina Vetročnik × Schmelzer — hči **Leopoldina po materi Leopoldi**; Kopitar 1890–92 → Vetročnik 1898–1900; **KONFLIKT DATUMA**: vrstica »40 jun« vs EMŠO 2405900505109 = 24.05. — MERI: EMŠO avtoritativno); **h23 4. PIN ISTA ZVEZA Brinec × Dehlič** — **P88 1893 »Debič?« REŠENO** z 1900 forenziko; **h14 2. VPIS — 1896 (P91) oče MERI dvom REŠUJE P91**; **h58 5. PIN + PRVA MENJAVA ŽENE** (Dragoš → **Katarina Kranbič**); h32 **8. PIN** (1893 »Meh/Mrh?« POTRJENO z 1900 »Meh« — KURRENT U/M); h65 **6. VPIS ISTI OČE** Milek (1887–1900) + 5. varianta matere (Tožek?); h20 **3. PIN** Pendirec × Klepec; **MENJAVE GOSPODINJSTEV**: h10 (→ **Grabrijan × Pozdirec** — scoping »Gmajrjan?« POPRAVLJENO), h9 (→ **Muc × Kure** — Kure = h1 rodbina; svinčnik »Štumer?«), h16 (→ **Novak × Šilak** — ŠILAK križni sklic 1886 mrliška), h25 (→ **Brinec × Segina** — SEGINA signal 4); **h54 starši RAZTRGANI** (sken 122 levo odtrgan — edina izguba staršev 1900); r19 dnevi raztrgani + mati IME PREČRTANO; pripis »Umrla 14.3.1954« r30/r31 dvomna (MERI po položaju črte); **DOJENČIJSKA UMRLJIVOST 5/16** (r3 † 1907, r23 † 2/6.00, r45 † 7/11.02, r46 † 8/5.03, r69 † 9/2.03); **EMŠO blok 3× ujema** (r6/r28/r31); matičar pripisi 13/16 vpisov;

  `scripts/p95_parish_baptism_1900.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1900.json` (SAMPLE-TRANSCRIPTION-1900) + `parish.ts` HOUSE_VITALS 238 → **254** (16 novih 1900 blokov) + QA 95 → **96/96** (nova qa-p95-parish-baptism-1900: celoven neodvisen preracun okvir − 3 za celo leto/sken 122 starševska stran/NOVELA babica 6+8/NOVA HIŠA 67 + 80. hiša + gumbar/h1 ŽELJKO VRNITEV + BOTER h1 1888/h31 6. PIN + najdaljša zveza/h45 3. PIN + 04455/h90 ŠOLSKA HIŠA 4. PIN + Leopoldina/h23 4. PIN + REŠENO/h58 5. PIN + MENJAVA ŽENE/sidra 16/PT 13/3/NOVA hiša 67 brez priora/kontinuitete 28 pinov/vitals 254) + **atlas.ts PT_GAP_KNOWN NESPREMENJEN** (P95: brez novih — h51 ZAVRŽEN; luknja 42/50/51 ostaja) + qa-p85 h90 / qa-p88 h23 / qa-p90 h20 / qa-p91 h9+h14+h45 / qa-p92 h10 dovolijo 1900 bloke (allow mehanizem) + qa-p86–p94 vitals pini 238 → 254 + **POPRAVI ZASTARELIH SKRIPT (regresije po P94)**: p80 I7 (vitals 254), p85–p92 filtri vesolja + 1900 (nabori), p85–p94 vitals 254 + kumulativ 260 + hiše 79 — vseh 16 skript p80–p95 `--check` PASS (exit 0); kartica NI dodana (vzorec P77–P95); tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…). Lekcije: novo leto se lahko začne z DRUGO VASJO (1900 r1 = Krasinec) in celo NA SREDINI strani (P94); fizčno raztrgane vrstice (r51–56) se sicer izključijo, a starši na starševski strani ostanejo berljivi; h58 NI v PT verigi — PT_GAP_KNOWN že vsebuje 58 (opomba: scopingov »NOVA LUKNJA« lead lahko napačno vas — Primostek 5);

- **župnija Podzemelj — krstna knjiga 04105, polno leto 1901 (P96, issue #18)** — §71 nextSteps ①: širitev vzorca po letih (MERI, NE odloča; **v7 join nespremenjen**): vir **Matricula Online**, krstna **04105 1886–1919**; **okvir 1901: glava »1901.« sredina str. 122 (sken 125, P95 dokazano) – row 87 str. 129 (sken 135; glava »1902« na dnu iste strani) == strani 122–129 (87 vrstic)**; **NOVELA P96 — TRIJE podvojeni skeni** (127/128, 129/130, 133/134): sken 128 = str. 124 z matičarskima nalepkama **PREPOGNJENIMA** → **r32/r33 REŠENI** (Juni 1/2 Primostek 2 Anton EMŠO 01.06.1901 + Gradac 32?/33? Jožef EMŠO 01.06.1901; nalepki 1989 = † Zagreb/Črnomelj); **stran == sken − 3 (125–127) / − 4 (129–130) / − 5 (131–132) / − 6 (135)**; **NOVELA formata: od str. 125 celo-spread fotografije** (leva podatkovna + desna roditelja/boter/babica/podpis — poravnava po y-pasovih); **NOVELA mesecev: r65–r69 NOVEMBER** (EMŠO r66 08.11.1901 + r68 16.11.1901) — December od r70; **r36 »Jurij«? = JUNI** (sekvence r39 July 10 vsiljuje) — **VSI vpisi z Griblji: 10 vpisov / 9 hiš**: 12, 12, 7, 54, 2, 17, 65, 24, 19, 44 — **h12 ×2 = PRVA PONOVITEV znotraj leta po 1893** (NARE 1894–1900 prekinjeno po 8 letih; r1 Gregor Juvan? × Barbura Cvetkovič vs r36 **Matija Straus × Marija Jakobič** — več-družinska hiša/menjava; pripis † 17/6.02 dojenček) — **1 NOVA hiša (19) + 8 ponovitev** — skupaj s P79–P95 vzorec **270 vpisov / 81 hiš čez tri knjige in ŠESTNAJST LET** (264 vitals); **NOVA HIŠA h19** (prvi matrični dokaz; v PT naboru 1825; **81. hiša vzorca**; oče **Nikolaj Hriče? bajtar** — najemnik kmeta); **h24 pripis »Umrła 11.10.1946 griblje št 24« SAMOPOTRJUJE hišo** (9. VPIS); **h7 EMŠO 2107901505598 = 21.07.1901 sidro** (Jakob Toter = rodbina babice Marjeta Toter!) + **h65 EMŠO 1110901503024 = 11.10.1901 sidro** (7. VPIS isti oče Milek 1887–1900); **PT 7/2** (h44 3. VPIS + h54 4. VPIS v luknji — oba že v PT_GAP_KNOWN; **luknja 42/50/51 NESPREMENJENA**, 19 dokazanih); **DUHOVNIKI: Kulbinek? 7×** (= P95 »Klunček?« — isti podpis, boljše branje na spread formatu) + Rauq 2× + **NOV podpis Fran. Dostál** (češko; tudi ne-Griblje r63/r67/r70/r71/r80/r83); **NOVELA babica 2. leto izpolnjeno: Toter 6×** (oče r48 = njena rodbina!) + Mavrefič + Mikl + Tolar? + Tome — **10/10 imenovanih**; **DOJENČIJSKA UMRLJIVOST 2/10** (r36 † 17/6.02, r52 † 17/3.03); **EXCLUDED: r35** (Griblje [~], hiša pod trakom + rob odtrgan — odprt lead: konflikt h24 r65, dva dojenčka Jun+Nov iste matere?) + **r47** (nalepka 26.01.1989 — starši Jurij Straus × Barbura Jakobič, MOŽEN Griblje, hiša nedokazljiva; za str. 125 NI dup skena z odprtimi nalepkami);

  `scripts/p96_parish_baptism_1901.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1901.json` (SAMPLE-TRANSCRIPTION-1901) + `parish.ts` HOUSE_VITALS 254 → **264** (10 novih 1901 blokov) + QA 96 → **97/97** (nova qa-p96-parish-baptism-1901: celoven neodvisen preracun trije dup pari + stran == sken − 3/− 4/− 5/− 6/NOVELA formata spread/NOVELA mesecev November/NOVA HIŠA 19 + 81. hiša + bajtar/h12 ×2 PRVA ponovitev po 1893/EMŠO sidri r48 + r59/babica 10/10 + Toter 6×/duhovniki Kulbinek? 7× + Rauq 2× + Dostál 1×/PT 7/2/NOVA hiša 19 brez priora/kontinuitete 8 pinov/vitals 264) + **atlas.ts PT_GAP_KNOWN NESPREMENJEN** (44/54 že vsebovani; luknja 42/50/51 ostaja) + qa-p85 h7 / qa-p87 h12 dovolita 1901 bloka (allow mehanizem) + qa-p86–p95 vitals pini 254 → 264 + **POPRAVI ZASTARELIH SKRIPT (regresije po P95)**: p80 I7 (vitals 264), p85–p92 filtri vesolja + 1901 (nabori), p93 vitals 264 + kumulativ 270 + hiše 80, p94/p95 filtri vesolja izključujejo 1901 (zgodovinske klasifikacije zamrznjene) — vseh 17 skript p80–p96 `--check` PASS (exit 0); kartica NI dodana (vzorec P77–P96); tsc 0 / lint 0; v7 runtime join NESPREMENJEN (sha256 4bb40370…). Lekcije: matičarske nalepke (1989) pokrijejo izvorno vrstico — podvojeni skeni z PREPOGNJENIMI nalepkami jih rešijo (127/128); format spread (od 1901) omogoča starše/botro na istem listu — poravnava po y-pasovih; znotraj-letna ponovitev (h12 ×2) po 8 letih NARE pomeni več-družinsko hišo (dva para staršev); prvotne QA napake: whatSi mora vsebovati literal »babica Ime Priimek« (ne samo sklanjeno) in NOVA-hiša allow liste zahtevajo + leto bloka;


  `scripts/p97_parish_baptism_1902.py` (**I1–I10**, `--check` PASS) + dokaz `research/issue17/parish-baptism-1902.json` (SAMPLE-TRANSCRIPTION-1902) + `parish.ts` HOUSE_VITALS 264 → **276** (12 novih 1902 blokov) + QA 97 → **98/98** (nova qa-p97-parish-baptism-1902: celoven neodvisen preracun dva dup para + stran == sken − 6/− 7/− 8/NOVELA formata NOVA TISKANA/NARE 0 ponovitev/PRVO LETO brez novih hiš/SEGINA VRNITEV h30 + STRAUS×SPUDIČ h16/ŽELJKO signali 16+17/babica 12/12 + Toter 9×/duhovniki Dostál 8× + Stanislav 5× + Rauq 4× + Kulbinek 0×/kontinuitete 12 pinov/vitals 276) + **atlas.ts PT_GAP_KNOWN NESPREMENJEN** (58 že vsebovan; luknja 42/50/51 ostaja) + qa-p85 h30+h77 / qa-p88 h91 / qa-p90 h87 / qa-p91 h14 / qa-p94 h22 dovolijo 1902 bloke (allow mehanizem) + qa-p86–p96 vitals pini 264 → 276 + **POPRAVI ZASTARELIH SKRIPT (regresije po P96)**: p80 (vitals 276), p85–p92 filtri vesolja + 1902 (nabori), p93 vitals 276 + kumulativ 282, p94/p95/p96 filtri izključujejo 1902 (zgodovinske klasifikacije zamrznjene) — vseh 18 skript p80–p97 `--check` PASS (exit 0); kartica NI dodana (vzorec P77–P97); tsc 0 / lint 0; v7 runtime join NESPREMENJEN. Lekcije: 1902 = NOVA TISKANA knjiga (vse kolone na eni strani; predtisk »Leto 18|02« — konec spread-formata); PRVO LETO brez novih hiš (h3/h87 že dokazani) — NARE 8. leto; KURRENT variante istega očeta (1895 Pegdirec? = 1902 Perdinec?) NE menjava družine — preveri zadnji vpis hiše pred interpretacijo menjave; peskovnik reset med fazo — dvorogi push po vsaki fazi reši vsa dela (repo obnovljen iz zrcala b5a25d7, artefakti rekonstruirani);

## Zadnje stanje raziskave (po P97 · 2026-10-17)

- **Runtime join**: `src/data/atlas/ps-parcels-geo.json` — **version 7**:
  **891 vrstic (32.3 %) / 879 base / multi 2 / cross 0 / ambRows 4**;
  soslednost 652 parov / 51.8 m / 25.5×; area median 3.8102 ≈ 1 Wiener QK
  3.59665 m² (Δ +5.94 %); zaupanje 172/588/131.
- **Nasledstvo verzij**: v1 1110 → v2 1093 → v3 1079 → v4 1145 → v5 1077 →
  v6 939 → **v7 891** — vsaka arhivirana v `research/issue17/` z delta
  dokazom (`v5Delta`/`v6Delta`/`v7Delta`); ohranjene vrstice med verzijami
  bajtno nespremenjene (lekcija P9).
- **QA**: **98/98** — repo veja (dokazi v `research/`) + produkcija (brez
  `research/`, izmerjeno iz runtime datotek); prek `GET /api/qa` na
  produkciji. Veriga skript `p60–p67 + p70–p97 --check` bajtno PASS (p68 zamrznjen po C2;
  p80–p97 = 18 župnijskih skript --check PASS). Matrične kontrole župnije (qa-p79/qa-p80/qa-p81/
  qa-p82/qa-p83/qa-p84/qa-p85/qa-p86/qa-p87/qa-p88/qa-p89/qa-p90/qa-p91/qa-p92/qa-p93/qa-p94/qa-p95/qa-p96/qa-p97) v ločenem modulu `src/lib/qa-parish.ts` (P80: runQA telo
  preseglo prag TS control flow analysis).
- **Kartice**: P40–P76 vidne v zavihku *Prepisi Kurrent* v muzejskem UI;
  vsaka vezana na API endpoint + dokaz + skripto. P77–P97 brez kartic
  (inventarni/operativni/paleografski/imenski dokazi raziskovalne linije — strojno
  berljivi prek dokazov).
- **Zrcaljenje**: GitLab `markec-group1/muzej` = **vir resnice**;
  GitHub `robertpezdirc12-design/muzej` = zrcalo, ki sproži Vercel deploy.
  Vsak push gre najprej na GitLab, nato na GitHub (obe z lastnikovo
  identiteto Robert Pezdirc — past avtorstva spodaj).
- **Odpri lastniških odločitve (P77+)**:
  ① opcija lokalnih sekcij iz P76 paketa — **A** status quo (v7, trenutna) /
  **B1** vse 56 vrstic (obvezen per-instanca ključ (base, stran)) /
  **B2** samo P60 band 12 / **B3** georef Blattnih kart [~];
  ② PF protokol kot vir identitete pas-instanc — **P77 DOKAZANI NEGATIV:
  NI na VAČ** (12 enot k.o. N83; dokaz `research/issue17/pf-vac-inventory.json`)
  → potreben fizični arhiv (SI AS 176 ali SI AS 52) ali drugi fond;
  ③ žetoni — **P78 AUDIT (issue #6)**: GitLab PAT #3 aktiven, rok
  **2026-11-14** (avtoritativno prek `/personal_access_tokens/self`; rok
  2026-11-09 v naslovu issue #6 = stari žeton); VERCEL_TOKEN potekel
  2026-10-14 (samo rezervni deploy; primarni GitHub App deploy dela,
  produkcija aktualna); skrivnost `GITLAB_TOKEN` v Actions sanirana (P78,
  sealed box); **GitHub Actions blokiran na nivoju računa (billing —
  avtoritativna anotacija check-run)**: sync.yml (mreža varnosti),
  token-health.yml (watchdog) in deploy.yml (rezerva) mrtvi do lastniške
  sanacije *Billing & plans*; do takrat velja ročni audit
  `p78_tokens_production_audit.py --check`.

## Varnost

Žeton `VERCEL_TOKEN` je shranjen izključno kot šifrirana GitHub Actions
skrivnost in ni v repozitoriju. Datoteki `.gitignore` in `.vercelignore`
preprečujeta prenos `.env*` in lokalnih datotek pri deployu.

