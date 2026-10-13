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

## Varnost

Žeton `VERCEL_TOKEN` je shranjen izključno kot šifrirana GitHub Actions
skrivnost in ni v repozitoriju. Datoteki `.gitignore` in `.vercelignore`
preprečujeta prenos `.env*` in lokalnih datotek pri deployu.
