# MUSEUM-AUDIT — Muzej vasi Griblje (P0 revizija, GitHub issue #1)

> Revizija po naročilu issue #1 »P0 AUDIT — preveri zgodovinske vire, zemljevid 1812, GPS/AR
> in produkcijski obiskovalni tok«. Vse ugotovitve temeljijo na berljivih dokazih: datoteke,
> številke iz determinističnih skript, rezultati testov. Nič ni izmišljeno; kjer nekaj ni
> preverjeno (npr. fizični telefon), je to izrecno označeno.

## 1. Izhodišče (točka 1 zahteve)

| Postavka | Vrednost |
|---|---|
| Repozitorij | `robertpezdirc12-design/muzej` (GitHub), veja `main` |
| HEAD ob začetku | `17fbf35` — »worklog: P13 — preverba GitHub sinhronizacije …« (8. 10. 2026) |
| Stanje delovnega drevesa | čisto (shallow klon razširjen na 50+ commitov) |
| Framework | Next.js 16 (App Router) + React 19 + TypeScript 5 + Tailwind; Bun kot upravitelj paketov |
| Podatki | statični JSON/TS pod `src/data/museum/` in `src/data/atlas/` — brez baze med delovanjem |
| Zgradba ob reviziji | `bun run build` uspešna: 16/16 strani, 12 API poti (vse `force-static`) |
| Produkcija | `griblje-museum.vercel.app` (Vercel; sinhroniziran z repozitorijem — primarni deploy prek Vercel GitHub App ob pushu na `main`, ročna rezerva `.github/workflows/deploy.yml`/`workflow_dispatch`; žeton `VERCEL_TOKEN` je samo še v rezervni poti, njegovo zdravje dnevno preverja `token-health.yml`) |
| Obstoječi testi | lastna QA zbirka (`src/lib/qa.ts`, 30 testov), atlas integrity (11 preverb), ESLint, tsc |
| Odprti issueji | #1 (ta revizija) — edini |

## 2. Inventar podatkov (točka 2)

Viri: `src/data/museum/exhibits.json`, `events.json`, `extra.json`, `meta.json`;
`src/data/atlas/*` (13 datotek). Preverjeno z determinističnim skriptom
(`audit_issue1.py` v peskovniku revizorja, rezultati spodaj).

### 2.1 Zbirka eksponatov

| Predmet | Rezultat | Ocena |
|---|---|---|
| Število zapisov | 114 | ✓ ujema se z README in meta.json (P24: +MVG-114) |
| Muzejske številke | MVG-001 → MVG-114, vse unikatne, oblika `MVG-\d{3}` | ✓ (zgodovina: README je nekoč prezgodaj trdil 114 — glej §8; P24 je zapis dejansko dodal) |
| ID-ji in slugi | 114 unikatnih ID-jev, 114 unikatnih slugov, oblika veljavna | ✓ |
| Naslovi SL/EN | 114/114 obojezično | ✓ |
| Povzetki in zgodbe | 114/114 s povzetki, 114/114 s poljema `storySi`/`storyEn` | ✓ |
| Slike | 107/114 s sliko; vseh 102 različnih citiranih datotek obstaja v `public/` (5 si deli dveh zapisov; +2 datoteki za Atlas 1812 = 104 na disku); 107/107 z `imageCredit` | ✓ 7 zapisov brez slike (namerno: npr. dogodki, izseljenstvo) |
| 3D model | 1 (cerkev sv. Vida, GLB + USDZ, obe datoteki obstajata, kredit navdan) | ✓ |
| Koordinate | 95/114 s GPS znotraj Bele krajine (45,30–45,90 N, 14,60–15,80 E); zastavica `coordsApprox` pri vseh razen 7 natančnih točk (P22/P25: MVG-001/004/006/009/032/103; P34: MVG-083 RNPD uradna register-točka) | ⚠️ 19 zapisov brez GPS — zavestne odločitve, ne vrzel (pesem/šega brez fiksne točke, regionalni zapisi, tradicija z odprtim iskanjem, najdišče Srednje njive brez javne koordinate — utemeljitve v §14, razrešitev MVG-083 v §16), glej §9 |
| Datumi | 101 zapisov z `yearFrom`; 13 z `null` (tematski zapisi z besedilnim `periodSi`, npr. »verska dediščina«) | ⚠️ 4 prazgodovinski zapisi so bili nevidni na časovnici — **popravljeno** (glej §8) |
| Negativna leta | 4 zapisi (MVG-060 −800, MVG-083 −4500…200, MVG-095 −1000…−700, MVG-113 −1200…−800) — prazgodovinska najdišča, `periodSi` jih pravilno poimenuje (»pribl. 4500 pr. n. št.«) | ⚠️ prikaz »−4500« namesto »4500 pr. n. št.« — **popravljeno** (glej §8) |
| Kategorije | 6 veljavnih: kraj 50, sege 21, gospodarstvo 13, vojna 13, narava 12, kolpa 5 | ✓ |
| Podvojitve naslovov | 0 | ✓ |
| Dogodki | 11; naslovi SL/EN, datumi, zunanje povezave vse veljavne | ✓ |
| Extra (galerije, citati, sorodni) | 114 vnosov po slugu | ✓ (zgodovina: 2 obešeni povezavi na MVG-114 sta bili P19 odstranjeni; P24 ju je povrnil, ker zapis zdaj obstaja) |

### 2.2 Viri in dokazljivost (točka 3)

| Predmet | Rezultat |
|---|---|
| Skupno navedb virov | **601** (478 unikatnih `sourceKey`; povprečno 5,3 na zapis; min 1, max 26; P24: +4 za MVG-114; P27: +2; P34: +5 za RNPD) |
| ⚠️ Razlika s README/meta | README in meta.json sta trdila 589 — **popravljeno na 590** (glej §8) |
| Zapisi brez vsaj enega vira | 0/114 |
| Viri brez podatka o licenci | 0/601 |
| Vrste virov | objava 265, spletni-vir 207 (P34: +5 RNPD/odlok), fotografija 106, arhiv 16, zemljevid 5, pričevanje 2 |
| Lestvica zanesljivosti | 4-stopenska, vsak zapis ima veljaven `evidenceStatus`: DOCUMENTED 88, CORROBORATED 16, TRADITION 8, TESTIMONY 2 |
| Ločevanje stopenj gotovosti | ✓ arhivski dokaz (arhiv/objava/zemljevid), ustno pričevanje (pricevanje/TESTIMONY), interpretacija in domneva so ločene tako v lestvici kot v `noteSi` posameznih virov; negativni izidi raziskav so izrecno dokumentirani (`NEGATIVE_RESULTS`, 11 zapisov) |

## 3. Zemljevid 1812 in georeferenca (točka 4)

Zahteve: preglej `research/georef-1812/` in ugotovi, ali so georeferencirani podatki
**dejansko povezani z UI** (README/worklog ne štejeta kot dokaz). Izvirne slike niso spremenjene
(`git status` čist nad `research/`).

| Veriga | Dokaz povezanosti z UI |
|---|---|
| `research/georef-1812/` (64 MB: izvirni skeni 1812 ×2, OCR TSV, afine transformacije JSON, skripti, izrezi) | dokazna sled; pot do aplikacijskih datotek dokumentirana v `src/data/atlas/research.ts` (vrstice ~552–554) |
| Izrez z oznako Griblje 1812 | `public/images/authentic/griblje-okolis-1812-900.jpg` (zmanjšana kopija) — prikazan v `museum-research.tsx:514` in kot slika zapisa v `exhibits.json` (»stari-zemljevidi«) |
| Zemljevid Ilirske province 1812 | `public/images/authentic/ilirske-province-1812.jpg`, sklic `MAP_1812.imageRef` v `research.ts` |
| Franciscejski kataster N83 (listi A01–A05) | `public/atlas/n83-a0*.jpg` + `SHEET_GEOREFS` (WGS84 meje, kontrolne točke, ocena natančnosti ±60–100 m) — **listi A01 in A02 sta dejansko risana kot Leaflet `L.imageOverlay` z georeferenčnimi mejami** (`atlas-canvas.tsx:91,95`) |
| Vektorizirane stavbe 1825 | 156 objektov iz lista A02 risanih na isti karti; integrity preverba »0 zunaj k.o.« PASS |
| Pregledi/panorame 1825 | `public/panoramas/*.jpg` + `panorama-viewer.tsx`; QA preverja HTTP 200 vseh URL-ij |

**Sklep: georeferencirani podatki so dejansko povezani z UI** (overlays na živi karti, ne le
opisi). Listi A03–A05 so georeferencirani v podatkih (REVIEW ±200–400 m) in prikazani kot
kartice virov; overlay na karti je namenoma le A01/A02 (GEOTRUTH afina).

## 4. Mobilni obiskovalni tok (točka 5)

> Fizičnega telefona revizor ni imel — tok je preverjen **v kodi in na produkcijskem HTML**;
> nič od spodnjega ni bilo kliknjeno na napravi. Po definiciji opravljenosti je tok zato
> označen kot *preverjen v kodi/produkciji, NEPREVERJEN na telefonu*.

| Element | Stanje | Dokaz |
|---|---|---|
| QR kodo (vhod + 9 postaj) | DELUJE (v kodi) | `public/qr/vstop.png` + 9× `spot-*.png`, generirana z `scripts/gen-qr*.py`, prikazana v `museum-map.tsx:328–379`; vsaka postaja ima QR kartico |
| Povezovalni URL-ji | DELUJE | `?obisk=1` (obiskovalni način), `?exponat=<slug>`, `?atlas=hiša-<št>`, `?casovni=<leto>&spot=<id>` (časovni stroj + postaja) |
| GPS | DELUJE (v kodi) | `use-geolocation.ts` (`watchPosition`), blizu/daleč logika v `ar-camera.tsx` |
| Lokacijske postaje | DELUJE | 9 časovnih točk v `timespots.ts`; koordinate IZKLJUČNO iz zapisov zbirke (lat/lng), vsaka z verigo virov (EŠD, MVG-xxx, kataster) |
| Zemljevid in pot | DELUJE | Leaflet + OSM ploščice + katastrski overlay (§3) |
| Avdio vodnik | DELUJE | GLAS MUZEJA SO SKRIPTE (P15): 9 časovnih točk ima napisane govorne skripte (si+en, `src/data/atlas/narrations.ts`, izpeljane izključno iz naslova/opisa/dokaza točke); predvaja jih skupni deterministicni narrator (`src/lib/narrator.ts`) prek brskalniške `speechSynthesis` — brezplačno, lokalno, brez AI modelov; transkript skripte se med predvajanjem pokaže na kartici; isti mehanizem za vodeni sprehod in AR kamero |
| Besedilni vodnik | DELUJE | `guide.ts`: Q&A na postajo (GUIDE_QA), vključen v `visitor-experience.tsx` |
| Jeziki | DELUJE | SL/EN preklopnik (`language-context`), 113/113 zapisov dvojezično |
| Delovanje brez signala | DELUJE (v kodi) | service worker `sw.js` v19: precache `/`, manifest, ikone; cache-first za statiko; strani stale-while-revalidate |

## 5. AR brez očal in brez AI v času delovanja (točka 6)

| Element | Stanje | Dokaz |
|---|---|---|
| AR kamere (brez očal) | DELUJE (v kodi) | `ar-camera.tsx`: `<video>` zadnje kamere (`getUserMedia`, `facingMode: environment`) + `<model-viewer>` z GLB modelom, lebdi nad sliko kamere; kompas (`DeviceOrientation`) + GPS azimut zasidrata model v smeri objekta |
| Postavitev v prostor | DELUJE | `model-viewer-3d.tsx`: `ar`, `ar-modes="webxr scene-viewer quick-look"`, `ar-placement="floor"` — Android WebXR/Scene Viewer, iOS Quick Look (USDZ obstaja) |
| Postopno poslabšanje | DELUJE | brez kamere → arhivsko ozadje; brez kompasa → fiksni model; brez GPS → pošten predogled (»komponenta ne izmišljuje«) |
| AI v času delovanja | NI GA | edini `fetch()` klic je blob za sintezo govora (zajem PNG); govor = deterministicne skripte + brskalniška `speechSynthesis` (P15); `OPENROUTER_API_KEY`/`ELEVENLABS_API_KEY` nista uporabljeni nikjer v `src/` in sta ODSTRANJENI z Vercela (P15, 2026-10-10); `z-ai-web-dev-sdk` odstranjen iz `package.json` |
| Fizična preverba na telefonu | NEPREVERJENO | zahteva napravo z senzorji; priporočam preizkus lastnika (korak §9) |

## 6. Licence in dostopnost (točka 7)

| Predmet | Stanje |
|---|---|
| Lastni metapodatki sklopa | CC BY-SA 4.0 (`meta.json`, `/api/opendata.license`) — z jasno opombo, da velja SAMO za lastne strukturne metapodatke |
| Posamezni viri | 601/601 z licenco v `sources[].license` (razporeditev po 129 vrstah licenc v `/api/provenance`; P34: nova vrsta CC BY 4.0 — odprta zbirka RNPD) |
| Slike | 107/107 z `imageCredit` |
| Zemljevidi (OSM) | atribucija na obeh Leaflet kartah: © OpenStreetMap + »katastrski listi: Arhiv RS (SI AS 176/N/N83)« |
| Reprodukcije arhivskih predmetov | pravila navedena v `/api/opendata.license.reproduction*` (Arhiv RS/VAČ, SEM, zasebni arhivi) |
| Odprti podatki | `/api/opendata` izpostavlja celotno zbirko z viri, krediti in plastovito licenco |
| Dostopnost | aria-oznake, `aria-selected` zavihki, tipkovnični markerji Leaflet (`keyboard: true`), `alt` besedila |

## 7. API-ji, varnost in testi (točki 8 in 9)

### 7.1 API in varnost

| Preverba | Rezultat |
|---|---|
| Število API poti | 12, vse `export const dynamic = "force-static"` — zgrajene ob buildu, brez uporabniškega vnosa med delovanjem |
| Vnos/uporabnik | ni runtime parametrov → ni površine za injekcijo; vsi podatki so kurirani JSON |
| Escaping | React avtomatsko; `dangerouslySetInnerHTML` le 2× (JSON-LD iz statičnega objekta v `layout.tsx`; predloga `ui/chart.tsx`) — brez uporabniškega vnosa |
| Leaflet tooltipi | interpolirajo kurirane naslove postaj (statični podatki, brez vnosa obiskovalcev) |
| Skrivnosti v kodi | 0 (preverjeno z vzorci žetonov v prejšnji reviziji; `.env*` izključen iz deploya z `.vercelignore`) |
| Predpomnjenje | SW v19: precache + cache-first statika + SWR strani; API poti so statične |

### 7.2 Točni rezultati testov (po popravkih iz §8)

| Test | Rezultat |
|---|---|
| `bun run lint` (ESLint) | **0 napak, 0 opozoril** |
| `bunx tsc --noEmit` | **0 napak** (P17: vseh 34 prikritih napak odpravljenih, `ignoreBuildErrors` odstranjen; tsconfig zožen na aplikacijo) |
| `bun run build` | **uspešno** — 16/16 strani, 12 statičnih API poti (~16 s) |
| `/api/qa` (lokalno, produkcijska zgradba) | **ok: true, 25/25 PASS** (vključno `qa-p12-village-life`; P18: `qa-p18-source-labels`, `qa-p18-timeline-stops`) |
| `/api/atlas/integrity` | **11/11 PASS** (hiše, viri, E2E veriga hiša 73→MVG-010, georeferenca, EŠD 2122, vektorizacija, matrike …) |
| `/api/provenance` | 601 navedb; 114/114 z virom; 0 brez licence |
| `/api/opendata` | števci 114/601/11/6; licenca CC BY-SA 4.0 |
| Produkcija (`griblje-museum.vercel.app`) | 200; QA 25/25 po deployu te revizije (glej §10; P18 dodal 2 testa) |

## 8. Popravki, izvedeni v tej reviziji (brez izgube vsebine)

Vsi popravki so aditivni ali dokumentacijski; noben zgodovinski zapis, vir ali izvorna slika
ni bil odstranjen ali prepisan (diff: 7 datotek aplikacije + ta dokument).

1. **Časovnica: zavihek »Prazgodovina«** (`museum-timeline.tsx`) — obdobja prej niso segala
   pod leto 1400, zato so bili štirje prazgodovinski zapisi (MVG-060, -083, -095, -113) na
   časovnici **nevidni**. Dodan zavihek (−5000…1400); privzeti zavihek ostaja »1468–1790«.
2. **Časovnica: oblika negativnih let** — leto −4500 se zdaj izpiše kot »4500 pr. n. št.« /
   »4500 BC«, grb pa kot »4500«; obenem odpravljena tipizacijska negotovost (`yearFrom: number | null`).
3. **Sorodni zapisi: obešene povezave MVG-114** (`exhibit-detail.tsx`) — dva zapisa
   (»panjska-koncnica«, »kresovanje«) sta kazala na načrtovani MVG-114 »Kresna pesem (1888)«,
   ki ga v zbirki ni; gumb je bil mrtev. Zdaj se prikažejo samo dejansko obstoječi cilji —
   ko bo MVG-114 dodan, se povezavi samodejno vrneta.
   *(Posodobitev P19: obe zastareli povezavi sta zdaj ODSTRANJENI tudi iz podatkov —
   glej §11; nove se dodajo skupaj z zapisom, varuje qa-p19-related-refs.)*
4. **Štetje virov 589 → 590** (`meta.json`, `layout.tsx` ×4, `museum-research.tsx` (zdaj
   dinamično iz `totalSourceRows`), `README.md`) — dejansko število navedb je 590; razlika
   je nastala, ker je bil dodan vir brez posodobitve števcev.
5. **README: obseg številk** — »MVG-001 → MVG-114« je popravljeno v »MVG-001 → MVG-113«
   (MVG-114 še ne obstaja v zbirki; glej §9 naslednji koraki).
6. **Taksonomija vrst virov** (`exhibits.json`, 2 vrstici) — tiskani članek Kmečkega glasa
   (MVG-022, brez URL) preklasificiran iz »spletni-vir« v »objava«; »arhivski-vir« (MVG-092)
   usklajen s 15-kratno večinsko »arhiv«.
7. **Dokumentacija** — ta datoteka `docs/MUSEUM-AUDIT.md`.

## 9. Matrika stanja in naslednji konkretni koraki (točka 10)

Legenda: DONE = deluje in dokazano · PARTIAL = deluje z dokumentirano vrzeljo ·
DEMO/NAČRTOVANO = mehanizem obstaja, vsebina čaka · MISSING = manjka · BLOCKED = blokirano.

| # | Predmet | Stanje |
|---|---|---|
| 1 | Integriteta 114 zapisov (ID, naslovi, jeziki, slike, kategorije) | **DONE** |
| 2 | Viri: sledljivost + 4-stopenska lestvica gotovosti | **DONE** |
| 3 | Zemljevid 1812 povezan z UI (izrez, viri) | **DONE** |
| 4 | Kataster N83 kot Leaflet overlay z GEOTRUTH mejami (A01/A02) | **DONE** |
| 5 | QR kodo (vhod + 9 postaj) + globoke povezave | **DONE** (koda/produkcija) |
| 6 | GPS in lokacijske postaje | **DONE** (koda) — telefon NEPREVERJEN |
| 7 | Avdio vodnik | **DEMO/NAČRTOVANO** — brskalniška sinteza govora dela; MP3 posnetki (domačin) še manjkajo |
| 8 | Besedilni vodnik Q&A in jeziki SL/EN | **DONE** |
| 9 | Brez signala (service worker v19) | **DONE** (koda) |
| 10 | AR kamere brez očal (model-viewer + kompas/GPS sidro) | **DONE** (koda) — telefon NEPREVERJEN |
| 11 | AR brez AI v času delovanja | **DONE** |
| 12 | Licence (CC BY-SA 4.0 plastovito, OSM, 107/107 kreditov) | **DONE** |
| 13 | API-ji statični, brez vnosa, escaping | **DONE** |
| 14 | Testni nabor (lint/build/QA/integrity) | **DONE** (rezultati v §7.2) |
| 15 | GPS koordinate 20/114 zapisov | **DONE (P25)** (P22: 36 → 48; P25: 48 → 94 — 41 vaških sidr sl.wiki Griblje za predmete V vasi [osebe, dogodki, šege, ustanove, gospodarstvo, narava] + 5 posebnih: sl.wiki Krasinec [letališče 1945, MVG-056], sl.wiki Jelševnik [črni močeril, MVG-025], sl.wiki Podzemelj [Barlova mladost, MVG-058], sl.wiki Adlešiči [pečnica, MVG-076], ZooKeys 474 natančna točka ribnika [MVG-103, coordsApprox=false]; YEAR_STOPS 45 → 78; preostalih 20 = zavestne odločitve, popoln seznam z utemeljitvami v §14) |
| 16 | Zapis MVG-114 »Kresna pesem« | **DONE (P24)** — dodan kot »Kresna pesem (1895) — natisnjeni sled pesmi ob Kolpi« (4 viri: dLib.si Dom in svet 8/14 1895, Dom in svet 7/22 1894, Radio Odeon 2025 s celotnim živečim besedilom, Radio Odeon Totter). Letnica prvotnega načrta (1888) se v virih ni potrdila — dokumentiran natis kresnih pesmi je 1895 (razlaga v §13); povezavi iz kresovanje/panjska-koncnica povrnjeni |
| 17 | Popravljanje 34 prikritih TS napak (`ignoreBuildErrors`) | **DONE (P17)** — 0 napak, zastavica odstranjena |
| 18 | Surove kode vrst virov vidne obiskovalcu (npr. »objava«) | **DONE (P18)** — slovar oznak `SOURCE_TYPE_LABELS` (SL/EN) v `src/lib/museum.ts`; izpis v exhibit-detail prek `sourceTypeLabel()` (surova koda ostane kot tooltip za sklicevanje na odprte podatke); celovitost varuje `qa-p18-source-labels` |
| 19 | Neuporabljene env spremenljivke na Vercelu + Prisma ostanki | **DONE (P15+P17)** — AI ključa (OPENROUTER, ELEVENLABS) odstranjena s Vercela in `z-ai-web-dev-sdk` iz package.json (P15); Prisma odstranjen v celoti (P17: `prisma/`, `src/lib/db.ts`, obe odvisnosti, db:* skripti, 17 neuporabljenih paketov). `DATABASE_URL`/`DIRECT_URL` sta ostali na Vercelu (neškodljivi, neuporabljeni — potencialno edini zapis povezave do zbirke, zato ju ne brišemo brez lastnika) |
| 20 | Pin MVG-095 v načinu časovnega potovanja na karti | **DONE (P18)** — drsnik preurejen v diskretne postanke (`src/lib/timeline-stops.ts`): postanki = vsa mejna leta zapisov na karti, od −1000 (prazgodovina) do 2026, zato so množice pik enake zveznemu drsniku, pika MVG-095 (−1000…−700) pa dosegljiva; letnice se izpisujejo kot »1000 pr. n. št.«; doslednost s podatki varuje `qa-p18-timeline-stops` |

### Naslednji konkretni koraki (po prednostni)

1. **Posneti človeški glas** (domačin) po obstoječih skriptah iz
   `src/data/atlas/narrations.ts` (neobvezno izboljšanje; postopek v
   `public/audio/timespots/README.md`) — človeški posnetek ni AI model.
2. **Preizkus obiskovalnega toka na telefonu** (QR vhod, GPS, AR kamera, offline) — lastnik z
   napravo; po potrebi popravki.
3. ~~**Dopolnjevanje GPS koordinat**~~ — **P25 ZAKLJUČENO** (48 → 94 od 114; preostalih 20 zavestno brez GPS — pesem/šega brez fiksne točke, regionalni zapisi, tradicija z odprtim iskanjem, najdišči brez javnih koordinat; popoln seznam z utemeljitvami v §14).

(P24 je dodal MVG-114 — glej §13. Nekdanji točki 4/6 — odstranitev `ignoreBuildErrors` in čiščenje env/Prisme — sta že odpravljeni v P17 oziroma P15+P17; matrika §9 #17 in #19. P23: zastareli vrstici dejansko odstranjeni s seznama, kot je P22 že zapisal v worklog.)

## 10. Definition of Done — stanje

- [x] Podatkovni inventar in napake so dokumentirani (§2, §7, skript `audit_issue1.py`)
- [x] Pot obiskovalca je preverjena v kodi/produkciji in **izrecno označena kot nepreverjena na telefonu** (§4)
- [x] Zemljevidi 1812 in AR/GPS so označeni po dejanskem stanju (§3, §5, matrika §9)
- [x] Kritične napake so popravljene brez izgube vsebine (§8: nevidni prazgodovinski zapisi, mrtvi gumbi MVG-114, napačno štetje)
- [x] Poročilo vsebuje teste, vire in naslednje konkretne korake (§7.2, §2–§6, §9)

## 11. P19 — revizija podatkovne pravilnosti (zunanji pregled, 2026-10-10)

Zunanja revizija je našla pet konkretnih neskladij; vsa so odpravljena na
podlagi virov, ne po presoji. Vrh revizije: *»ne manjka ti osnovne kode,
manjka dokončana, medsebojno povezana in v praksi preverjena muzejska
izkušnja«* — zato P19 ne dodaja novih modulov, ampak povezuje podatke.

### Preglednica popravkov

| # | Ugotovitev revizije | Popravek (P19) | Vir podlage |
|---|---|---|---|
| 1 | Dogodek 2026 je 1526 imenoval »prvo omembo vasi« | Oba dogodka 500-letnic preoblikovana: jubilej je **cerkveni** (cerkev sv. Vida prvič v listinah 1526); izrecna pojasnitev, da je vas starejša (1468, MVG-001). Odpravljena tudi ista napaka v 3 življenjskih postajah (griblje-vas, zaselki-griblje) in `yearFrom` MVG-049 (1526 → 1468); odstranjen mrtvi postanek 1526 s časovnega drsnika | MVG-003 (7 virov: Radio Odeon, Moja Dolenjska, Občina Črnomelj, Slovenske novice, Dolenjski list, Wikipedija); EN Wikipedija + Snoj 2009 prek MVG-001; SL Wikipedija v infopolju napačno navaja 1526 za naselje |
| 2 | README navaja 9 dogodkov, dejansko je 11 | README usklajen (11) | events.json |
| 3 | README navaja 101 fotografijo | Natančno: 103 datoteke — 101 citira 106 zapisov (5 si deli dveh zapisov), 2 uporablja Atlas 1812 | exhibits.json + disk |
| 4 | 60 od 375 postaj življenjske zgodbe brez lastnega vira | 23 postajam dodan KONKRETEN vir (izključno iz virov matičnih zapisov: Barle 1893, Mason 2001, Šimec 2001, Snoj 2009, Dular 1978/1986, Volčjak 2019, SEM, RTV, DOPPS …); preostalih 37 ima zdaj jasno oznako **»v raziskovanju«**; 0 postaj je tiho nedokumentiranih. UI izpisuje tudi tiskane vire brez URL-ja | viri matičnih zapisov (nič novih navedb iz glave) |
| 5 | Dve povezavi kažeta na neobstoječi MVG-114 | Odstranjeni (zapis bo dodan šele po zbranih dokazih, skupaj s povezavami) | načelo nič-zgube |

### Nove avtomatske kontrole (QA 25 → 30)

Revizija je zahtevala kontrole, ki same odkrijejo neskladja pri novih podatkih
(`src/lib/qa.ts`, javno na `/api/qa`, vsak build jih preverja):

1. `qa-p19-counts` — števci (zbirka/viri/dogodki/zgodbe) v meta.json in
   events.json morajo biti enaki dejanskim podatkom (prej je bil ključ napačno
   brano — tiha rezerva, zdaj strogo);
2. `qa-p19-images` — vsaka slika zapisa obstaja na disku (strežniški klic z
   fs; odjemalski izris preveri obliko poti);
3. `qa-p19-related-refs` — sorodni zapisi kažejo samo na obstoječe zapise
   (ulovi vsak novi MVG-114 primer);
4. `qa-p19-station-sources` — vsaka postaja življenja ima vir ali oznako
   »v raziskovanju« (tiho nedokumentirana trditev postane nemogoča);
5. `qa-p19-first-mention` — vsak stavek, ki trdi prvo omembo vasi, mora biti
   zasidran na 1468 (regresija na napako iz tega kroga; cerkveni stavki so
   izrecno izvzeti — cerkev 1526 je pravilna).

### Ostalo iz revizije (ni podatkovna napaka — zabeleženo)

- Muzejski vodnik (18 vprašanj/odgovorov) je dober deterministični vodnik,
  ne pa celovit — nadaljnja vsebinska rast po vrstnem redu dokazov.
- Sprehod/GPS/AR/offline na terenu: **ni potrjeno** — potreben preizkus z
  telefonom na kraju (§9, točka 2).
- 3D časovni stroj ločuje RECONSTRUCTED od dokazanega (village3d.ts
   oznake, geotruth pripravljenost scene) — velja vzdrževati.
- Glej §9 za prednostni vrstni red naslednjih korakov (Faze 2–4 revizije:
  zemljevid 1812 + GPS, preizkus na telefonu, kakovostne 3D rekonstrukcije).

## 12. P20 — ISSUE #4 (GitHub): ATLAS 1825 — inventar, uskladitve, natančnost (2026-10-10)

Zunanja revizija (GitHub issue #4, P1) je zahtevala: enoten preverljiv inventar
arhivskih enot N83, razrešitev nasprotij v obsegu (PUA 43/11 proti 101/49),
popravke napačno pripisanih opomb, ločitev okvirne umestitve od validirane
georeference in reconciliation, ki preverja inventuro izvornih enot — ne samo
statuse ustvarjenih vrstic. Vse spremembe so v PR (veja
`feature/atlas-1825-inventory`), ne neposredno na main.

### Razrešitve nasprotij (dokazno podlaga v oklepajih)

| Neskladje | Prej | Zdaj | Dokaz |
|---|---|---|---|
| PUA obseg (sources proti research) | src-pua 43 vnosov / 11/49 strani »12–49 TO_COLLECT« | 101 vnosov / 49/49 — strani A–B (21 lastnikov) v ATLAS_OWNERS, strani 3–49 (101 vrstic) v PUA_CONTINUATION | PUA_CONTINUATION.pagesRead [3–49], rows 101; research/issue17/PUA-more.json + research/p3/pua-raw/ (38 datotek); opomba razloži, da structuredEntries 101 = SAMO strani 3–49 |
| PS prebrane strani | 9 (brez podlage) | 8 (1–4 + 140–143) | PS-structure.json sectionsSeen (str. 1, 2, 3, 4) + sampleRows (str. 3–4) + rekapitulacija (str. 140–143) |
| PZ vzorčene strani | 10 (nasprotuje lastni opombi: 12) | 12 (1–3, 20, 30, 40, 50, 60, 68–71) | PZ-valuation.json pagesSampled=[20,30,40,50,60] + PZ-profile.json (1–3, PZE-68–71) |
| src-pr opomba | »prepis ni izdelan (TO_COLLECT)« | 4/4 strani prebrane (REVIEW) | KURRENT_SERIES PR + research/issue17/PR.json |
| src-ps opomba | »20 vrstic … prepis ni izdelan« | 12 vzorčnih vrstic, 8 strani strukture, kontrolna vsota 2607 | PS-structure.json |
| src-pz opomba | »prepis ni izdelan« | 12 vzorčenih strani, 10 strukturiranih zapisov, 59 strani izrecno odprtih | PZ-valuation.json + PZ-profile.json |
| src-pg / src-pv opombe | manjkale | dodane (skica: negativen rezultat hišnih simbolov; PV: 10 kultur, vsote ≈1221 j; opomba, da 71-stranski elaborat pripada PZ) | KURRENT_SERIES + research/issue17/PG.json / PV.json |
| getCoverage enote/strani | 9 enot / 279 strani | 12 enot / 277 strani (143+71+49+8+4+1+1) | ATLAS_SOURCES (5 grafičnih + 7 spisovnih); prejšnja številka je ostala iz prve pridobitve (le A01+A02) |
| Reconciliation PUA lokator | »strani C–Ž (niso prepisane)« | »lastniški model (strani A–B) — brez PUA potrditve« + razlog (divergentno številčenje, 49/49 prebranih) | register je prebran v celoti |
| Reconciliation PS enota | manjkala (preskočena) | lastna vrstica: 8/143 prebranih, 135 izrecno odprtih, kontrolna vsota 102+2505=2607 | KURRENT_SERIES PS |

### Ločitev natančnosti prostorske umestitve (issue #4 #1)

- Nov poljubni `GeorefStatus` GRID_APPROX + `placement` (precision, method,
  controlPoints, accuracy, lastChecked) na vsakem grafičnem listu.
- A01, A02: GEOREFERENCED / VALIDATED_GEOREF (±40–100 m, kontrolne točke
  EŠD 2122 + Kolpa) — A02 CORROBORATED, izvor 156 tlorisov.
- A03, A04, A05: GRID_APPROX (±200–400 m, sekcijska celica eZKN + preveritve
  napisov; brez točkovnega sidra — ni afina). `georeferenced: false`.
- getCoverage: `sheetsGeoreferenced` (2) ločeno od `sheetsGridApprox` (3);
  UI: uvod, števci, pokritostni zavihek in oznake na karticah virov
  (»georef ±« proti »približno ±«); housesWithGeometry ostaja 0 z
  razlago (156 geometrij ≥ 84 hiš — ni 1:1; cerkev na A02 je kontrolna
  točka georeference, ne hišna entiteta registra).

### Izračunani inventar (getArchiveInventory, /api/atlas → inventory)

12 enot; za vsako: pagesDeclared (vir) / pagesRead + pagesReadList (dokazano,
iz surovih raziskav) / pagesOpen + obsegi (npr. PS »5–139«, PZ »4–19, 21–29,
31–39, 41–49, 51–59, 61–67«) / structuredEntities (dejansko stanje modelov:
PT 105 = 84 hišnih + 21 parcelnih vrstic; PUA 101; PS 12; PZ 10; A02 156) /
crossChecked / spatiallyLinked (0) / palaeoConfirmed (0) / razlog odprtega
stanja. scopeAccounted: prebrane + odprte strani == deklarirane (12/12 true).
PS checksum 102 + 2505 = 2607 iz PS_RECAP_1826. Števci so IZRAČUNANI —
ne morejo tiho zastareti (to je točno tisto, kar se je zgodilo s 43/11).

### Reconciliation (issue #4 #4)

- `scopeCheck` na vsaki enoti: pagesDeclared == pagesRead + pagesOpen
  (inventar, ne statusev ustvarjenih vrstic); zeroLoss zdaj zahteva
  scopeAccounted IN lost = 0.
- `zeroLossMeaningSi/En`: izrecna opredelitev, kaj zeroLoss potrjuje in
  česa NE (P36: PS strani 5–139 strojno prebrane — 2743 vrstic dvoprehodno,
  a sprava s kontrolno vsoto 2607 še odprta; PZ 59 strani izrecno odprtih;
  vsa strojna branja REVIEW; 156 geometrij brez dokazanih hišnih št.).
- PUA↔PT povezave po hišni št. same ostajajo PREPOVEDANE (dokazano
  različno številčenje: PUA hiša 6 = Höflehner, PT hiša 6 = Tilel Miho);
  vsak lastnik brez PUA potrditve ima razlog, ne tihe luknje.
- Parcelne vrstice houses.ts so DEL PROTOKOLA PT (str. 5–7), ne register
  PS — zavajajoči lokator popravljen.

### Nove avtomatske kontrole (QA 30 → 34)

1. `qa-p20-inventory` — inventar izračunan iz modelov; structuredEntities
   == dejansko stanje (PUA 101 == PUA_CONTINUATION.rows — 43→101 se ne
   sme ponoviti); 0 spatiallyLinked; 0 palaeoConfirmed; PS vsota 2607;
2. `qa-p20-series-pages` — pagesReadList dolžina == pagesTranscribed,
   brez podvajanj/izven obsega; dokazane vrednosti PR 4, PS 8, PUA 49,
   PZ 12, PT 8, PG 1, PV 1; scopeAccounted true;
3. `qa-p20-georef-precision` — A01/A02 GEOREFERENCED + VALIDATED_GEOREF
   placement; A03–A05 GRID_APPROX + georeferenced false + celica v
   metodi; pokritost 2+3=5; 12 enot; 277 strani; housesWithGeometry 0;
4. `qa-p20-recon-scope` — vse enote scopeCheck.accounted;
   zeroLossMeaning prisoten z »NE potrjuje«; zeroLoss true; 0 zastarelih
   lokatorjev »C–Ž«. (Test je pri razvoju ujel 10 vrstic z zastarelim
   lokatorjem in manjkajočo PS enoto — obe odpravljeni.)
- Posodobljen `qa-p10-ezkn-grid`: 2 validirana + 3 GRID_APPROX (prej
  »5/5 georeferenciranih« — zdaj pošteno ločeno).

### Zaključno poročilo (4 vprašanja issue #4)

1. **Kaj je v celoti prepisano, kaj vzorčeno, kaj neobdelano?** V celoti
   prebrani (strojno, REVIEW): PR 4/4, PG 1/1, PV 1/1, PUA 49/49, PT 8/8
   (101 vrstic pregledanih). Vzorčeno: PS 8/143 (struktura 1–4 +
   rekapitulacija 140–143; 12 vrstic), PZ 12/71 (1–3, 20–60, 68–71). Neobdelano
   in izrecno odprto: PS strani 5–139 (135), PZ strani 4–67 razen vzorcev (59).
2. **Koliko hiš, parcel, lastnikov je strukturiranih, navzkrižno povezanih,
   dokazno potrjenih?** Strukturirano: 84 hišnih vrstic + 21 parcelnih (PT),
   101 vrstic PUA (str. 3–49) + 26 lastnikov modela (16 s PUA potrditvijo;
   strani A–B so v modelu), 12 vzorčnih vrstic PS, 10 zapisov PZ, 1 PG,
   10 PV/PR. Navzkrižno PT×PUA: 15 lastnikov (puaRef + ujemajoča hiša).
   Dokazno (človeško paleografsko) potrjenih: 0 — vsa branja so strojna
   (REVIEW); konvergenca dveh branj P3 ni paleografska potrditev.
3. **Koliko stavb ima samo geometrijo in koliko dokazno povezavo?** 156
   stavb ima geometrijo (RECONSTRUCTED, list A02); 0 ima dokazano povezavo
   s hišno številko/parcelo/lastnikom — listi ne nosijo berljivih hišnih št.
   ob objektih, številčenje PUA↔PT je divergentno, meje parcel niso
   vektorizirane. Edina stavba z dokumentirano identiteto je cerkev sv. Vida
   (EŠD 2122 ↔ A02 px) — a je to kontrolna točka georeference, ne vrstica
   registra.
4. **Kaj je odprto in kateri dokaz manjka?** (a) PS: strojni prepis 135 strani
   IZVEDEN (P36, 2743 vrstic, §17) — odkrite strukturne zagatve (pomešan
   zvezek, več števčnih nizov, večkulturne vrstice) sprava s kontrolno vsoto
   2607 še odprta; (b) PZ: 59 strani tabel
   razredov — dokaz = vrednosti razredov po kulturah; (c) točkovno sidro
   za A03–A05 (VAČ metapodatek ali točka z znano lego) za afino; (d)
   vektorizacija parcelnih meja z A01/A02; (e) človeška paleografska
   potrditev vseh strojnih branj (zlasti 5 neberljivih vrstic PT);
   (f) povezava hiša↔stavba: potreben dokaz, ki povezuje hišno št. s
   konkretnim tlorisom (npr. zapisi poznejših katastrov, pričevanja);
   (g) digitalizacija SI AS 749 (1851–53 plast).

### Omejitve in načela

- Nič ni nadgrajeno v močnejšo stopnjo gotovosti: vsi novi števci so
  izračunani; strojna branja ostajajo REVIEW; negativni rezultati ostajajo
  vidni (PG brez hišnih simbolov; kolpa-ne-deluje iz P8 itd.).
- Brez AI modelov ob delovanju; brez plačljivih storitev; surovi izpisi
  raziskav (research/) so nespremenjeni.
- 1812 zemljevid je ločena raziskava (issue #4 Omejitve) — ni del tega PR.
- Preizkušeno: ESLint 0; tsc 0; build 16/16 s tipi; /api/qa 34/34;
  /api/atlas/integrity 11/11; /api/atlas/reconciliation zeroLoss=true,
  12 enot, vse scopeCheck.accounted.

## 13. P24 — MVG-114 »KRESNA PESEM (1895)«: dodan zapis (2026-10-10)

Zapis je bil rezerviran od obnove zbirke (načrtovani naslov »Kresna pesem (1888)
— najstarejši natisnjeni sled pesmi, pevane v Gribljah«; obešeni povezavi sta
P19 odstranil, ker zapis ni obstajal). P24 je zbral vire in zapis dodal — z
dvema poštenima popravkoma načrta, obema dokumentiranima spodaj.

### Raziskava virov (2026-10-10)

- **Natis (primarni):** J. Barle, »Kresne ali ivanjske pesmi belokranjskih
  kresnic«, *Dom in svet* (Ljubljana), letnik 8, številka 14 (1895) —
  digitalizirano v dLib.si (URN:NBN:SI:DOC-DUADCBST). Prvi natis, izrecno
  posvečen kresnim pesmim Bele krajine. Predhodni spisek: »Belokranjske
  narodne pesmi; zapisal v podzemlju J. Barle«, *Dom in svet* 7, št. 22
  (1894). Oba bibliografska zapisa potrjena iz kataloga dLib.si (dostop s
  peskovnika blokira WAF/IP; overjeno prek strežniškega bralnika in dveh
  neodvisnih kataložnih navedb).
- **Gribeljska nit:** Radio Odeon — Ljudje ob Kolpi: Matija Totter (že v
  zbirki pri MVG-065/057): Matija Totter — Jandreč Matiček — je na Barleovo
  navodilo popisal običaj kresovanja in besedilo kresne pesmi pozemeljske
  fare (vanjo so spadale tudi Griblje).
- **Živeče besedilo:** Radio Odeon — »Kresovanje: Daj nam Bože dobro leto …«
  (Boris Grabrijan, 22. 6. 2025): celotno besedilo pesmi, kakor jo v
  Adlešičih pojejo še danes (»Bog daj, bog daj dober večer! … Daj nam Bože
  dobro leto …«), opis šege kresnic (pretekanje glasov, piščalist, kolo iz
  ivanjih rož, košara z darovi), Šašljevi zapisi 1905/1909 in vpis
  adlešiškega kresovanja v Register nesnovne kulturne dediščine RS 2025
  (nosilec: KUD Božo Račič Adlešiči, pevska skupina Kresnice).

### Popravka načrta (dokumentirana, ne tiho)

1. **Letnica 1888 → 1895.** Niti en najdeni vir ne podpira letnice 1888:
   Barleovi natisi kresnih pesmi so 1894 (Dom in svet 7/22) in 1895
   (Dom in svet 8/14); Ženitovanjski običaji Belih Kranjcev so 1889;
   revija Dom in svet sicer izhaja od 1888 (najverjetnejši izvor zmede).
   Zapis nosi letnico prvega izrecnega natisa kresnih pesmi: 1895.
2. **Trditev »pesmi, pevane v Gribljah« → »pesmi ob Kolpi / pozemeljske
   fare«.** Dokumentirano je, da je besedilo zapisal gribeljski Matiček za
   pozemeljsko faro (vanjo so spadale tudi Griblje); ni pa mogoče
   preveriti, da je ravno gribeljska različica tista v natisu 1895
   (celotnega besedila članka peskovnik ni mogel prebrati — dLib.si
   dinamični dostop). Zgodba zato obe trditvi loči in »Muzej išče«
   izrecno navaja: izvod Doma in sveta 8/14 s celotnim besedilom in
   Matičkov rokopis.

### Izvedene spremembe

- `exhibits.json`: MVG-114 (kresna-pesem-1895; kategorija sege;
  CORROBORATED; 4 viri; yearFrom 1895; brez GPS — pesem ni točka na karti,
  enako kot MVG-065; sortOrder 113; slika kresnica.jpg — svetleča samica
  Lampyris noctiluca, po kateri se pevke imenujejo; Commons/Emphyrio1983,
  CC BY-SA 4.0, ilustrativna, pošteno označena).
- `extra.json`: vnos s 5 postajami življenja (Matičkov zapis → natis 1894 →
  natis 1895 → Šašelj 1905/1909 → register 2025), related na MVG-065/062/
  057/058; povrnjeni related v kazalah kresovanje + panjska-koncnica
  (obljuba iz P19 izpolnjena); postaja sprehoda 36 »Vas in njeni ljudje«
  (zaporedje brez lukenj; walk.total usklajeno 35 → 36 pri vseh 34 zapisih).
- Števci povsod: 114 zapisov / 594 vrstic virov (meta.json, layout.tsx ×5,
  README, JSON-LD MVG-001–114, qa-no-loss, kategorije sege 21, evidence
  CORROBORATED 16, vrste virov objava 263, licence 127 vrst).
- Testi: QA 34/34 (walk: 36 mest, 1 eksplicitna vrzel; counts 114/594;
  related-refs 0 zastarelih); ESLint 0; tsc --noEmit 0; build uspešen.
- Brez AI modelov: gre za podatkovni zapis iz tiskanih in spletnih virov;
  vsebine ni ustvaril jezikovni model — vsak stavek ima vir, ki ga citira.
## 14. P25 — GPS KOORDINATE 48 → 94 (2026-10-10)

Drugi val dopolnjevanja koordinat po P22 (enaka disciplina: nobena koordinata
ni izmišljena; vsaka izhaja iz javnega, preverljivega vira). Žetev izvedena
2026-10-10: sl.wikipedia API `prop=coordinates` (dostop iz peskovnika tokrat
deluje, brez 403/429 blokad iz P22; koordinate Griblje so potrdile P22
vrednost), Commons API `extmetadata` (preverjene 4 fotografije — vse brez
GPS), NCBI eFetch (GenBank FJ495099: `geo_loc_name="Slovenia"` — brez
koordinate), pdftotext celotnega PDF-ja Arheološkega vestnika 71 (1 omemba
»Srednje njive pri Gribljah«, 0 vzorcev koordinat), rtvslo 743207 (potrditev:
»s partizanskega letališča Krasinec v Beli krajini«, »na široki obkolpski
ravnici v neposredni bližini mejne reke Kolpe dve letališči«), EJT 777 prek
strežniškega bralnika (gribeljski primerka sta v zgodbi MVG-112 citirana brez
koordinat — za muzejski material 1985/1994 pričakovano).

### Nova sidra (46)

- **Vaško sidro sl.wiki Griblje (45.575447, 15.292761; `coordsApprox`) ×41**
  za zapise, katerih predmet je fizično v vasi — enak vzorec kot P22
  (MVG-022/037/038/057/067/068/077). Obseg: osebe z Gribelj (MVG-033 Audrey
  Totter [Gornje Griblje], MVG-100 J. R. Totter [rod Matičkov], MVG-034
  Nikolaj Dragoš [Hajdeč grunt], MVG-043 Katarina Zupanič [Grizin], MVG-101
  Valentina Štrucelj, MVG-042 dr. Franc Brinc, MVG-085 Mate Zupanič-Švarski
  [hiša Švarskih], MVG-035 Peter Kambič [učitelj], MVG-099 Dragojila Milek
  [očetova domovija], MVG-090 Anton Brodarič, MVG-072 Ciril Totter, MVG-044
  Toni Gašperič, MVG-055 Franjo Veselko [»ob polju pri Gribljah« 1945]);
  dogodki v vasi (MVG-014 evakuacija marec 1945 — fotografiji naslovljeni
  »Griblje pri Črnomlju«; MVG-041 pasuljada, MVG-047 kavbojski žur, MVG-073
  praznik KS, MVG-070 gribeljci po svetu 2019, MVG-104 tranzit 2025, MVG-084
  jurjevo, MVG-071 ko se ptički ženijo, MVG-087 križevo, MVG-106 poljsko
  lokostrelstvo); ustanove vasi (MVG-026 vaška šola, MVG-046 muzejska
  učilnica, MVG-078 ŠD, MVG-069 TD, MVG-089 DKŽ, MVG-052 tamburaši Danica);
  gospodarstvo vasi (MVG-082 žbul, MVG-086 tobak, MVG-107 komasacija
  Griblje–Cerkvišče, MVG-051 kmetija Štrucelj, MVG-011 izseljenstvo,
  MVG-108 odkupne cene COVID, MVG-017 belokranjska hiša [dokumentirani
  gribeljski primeri SEM F0000182/F0001407], MVG-088 razglednica 1903
  [naslov »v Griblje«]); narava vasi (MVG-102 TULV — voluharica ujeta
  v Gribljah, GenBlock potrjeno; MVG-112 Nemastoma b. gruberi — primerka
  »Griblje−Desinec« 1985 in »Dragoši, Griblje« 1994); MVG-039 španska gripa
  (podzemeljska matična knjiga — enako vaško sidro kot MVG-037/038 v P22).
- **sl.wiki Krasinec (45.58835, 15.279114)** — MVG-056 zračni most:
  partizansko letališče Krasinec, marec 1945 (naselje občine Metlika ob
  Kolpi, ~1,5 km od Gribelj; sl.wiki članek o vasi ob Kolpi; ločeno od MVG-014,
  ki sidra na Griblje — fotografiji Veselka sta naslovljeni »Griblje pri
  Črnomlju«; dva zapisa, dve plasti iste operacije).
- **sl.wiki Jelševnik (45.571142, 15.146808)** — MVG-025 črni močeril:
  izvir Jelševniščice v Jelševniku je edino najdišče na svetu, kjer je
  podvrsto mogoče videti v naravnem okolju (odkritje 1986 na izviru
  Dobličice; Jelševnik leži zahodno od Črnomlja — zapis ne trdi, da močeril
  živi v Gribljah, zato ni vaškega sidra).
- **sl.wiki Podzemelj (45.6087, 15.273447)** — MVG-058 Janko Barle: družina
  se je 1872 preselila v Podzemelj, tu je končal ljudsko šolo (»tu je Bela
  krajina vtisnila v njega spomin«). Sidro mladostnega kraja, ne rojstnega
  (Budanje, Vipavska dolina).
- **sl.wiki Adlešiči (45.522397, 15.311044)** — MVG-076 pečnica za sušenje
  sadja: fotografija Franceta Vesela 1928 je »posneta v Adlešičih« (naslov
  citirane Commons datoteke + zgodba zapisa); Commons GPS metapodatka ni,
  sidro je torej vas, ne točka. Zapis ostaja iskreno označen kot tradicija
  (muzej išče gribeljski primer).
- **ZooKeys 474, DOI 10.3897/zookeys.474.8474 (45.576, 15.2835;
  `coordsApprox=false`)** — MVG-103 Cryptachaea riparia: v zgodbi zapisa
  dobesedno citiran zbiralni podatek »Pond Ribnik NW of village Griblje;
  45°34,56′ N, 15°17,01′ E, 150 m n. m.; 29. 7. 2001; leg. & det.
  Kostanjšek R.« — pretvorba: 45 + 34,56/60 = 45.576; 15 + 17,01/60 =
  15.2835. Edina natančna (±20 m) zbirateljska koordinata v zbirki.

### Zavestne izločitve (19 zapisov brez GPS — utemeljitve)

1. **Pesem/šega brez fiksne točke (precedens P24):** MVG-065 kresovanje
   (kresi na gričih pozemeljske fare — ni ene točke; P24 ga je navedel kot
   vzor za MVG-114), MVG-114 kresna pesem (1895; pesem ni točka na karti).
2. **Najdišče brez javne koordinate:** MVG-113 Srednje njive (Arheološki
   vestnik 71.14, celoten PDF prebran — 1 omemba, 0 koordinat; P27: poročilo o
   intenzivnem pregledu Kohane — VS, poročila 39–41, str. 54–55 — prav tako
   brez koordinat in brez imena Srednje njive; P34: RNPD ime ne vsebuje, uradna
   točka EŠD 10094 pa je točka celotnega najdišča, ne lega Srednjih njiv —
   negativni izid dokumentiran v viru zapisa; Mason 2001, str. 10, ostaja
   TO_COLLECT — med digitaliziranimi številkami ZVKDS revija 39 ni na spletu,
   saj niz preskoči 37–40). MVG-083 arheološko najdišče ob Kolpi (EŠD 10094) je
   bilo v tej skupini do P34 — **REŠENO**: odprta zbirka RNPD objavlja uradno
   središčno točko vpisa (15.294803, 45.57951), zapis ima GPS s
   `coordsApprox=false`, ločeno pa je citiran še Požekov vrt (EŠD 11081,
   15.291905, 45.571689) — glej §16.
3. **Regionalni zapisi, ne gribeljska točka:** MVG-019 jurjevanje in
   pustovanje, MVG-079 belokranjska noša, MVG-064 pisanice, MVG-020
   belokranjska kuhinja, MVG-024 bele breze, MVG-018 vinogradništvo in
   metliška črnina (vinska ruta Bele krajine; Griblje le na njenem robu),
   MVG-023 štorklje (regionalna vrsta), MVG-075 Valvasor 1689 (knjiga o
   deželi), MVG-063 Jože Dular (rojen Vavta vas, delo Metlika — častni
   seznam varuhov dediščine, ne gribeljska točka).
4. **Tradicija z odprtim iskanjem (muzej išče gribeljski primer):** MVG-066
   kuhanje žganja (išče gribeljsko kuharijo), MVG-021 tkalstvo (išče statve,
   ki so stale v Gribljah).
5. **Ni prostorska točka:** MVG-074 Ljudje ob Kolpi (radijska rubrika).
6. **Pojav brez ene točke:** MVG-008 reka ekstremov (merilna postaja Metlika
   12 km dolvodno; suše in poplave so pojav celotne reke; september 2025 iz
   Prelesja in postaje Petrina).
7. **P22 zavrnitve, nespremenjene (točkovni objekti brez vira koordinate):**
   MVG-053 kopališče Griblje, MVG-007 malenca na Kolpi, MVG-045 Madroničev
   mlin (Prelesje).

### Izvedene spremembe

- `exhibits.json`: 46 × lat/lng/coordsApprox (noben vir in nobeno drugo polje
  ni spremenjeno — števci ostajajo 114 zapisov / 594 vrstic virov).
- `src/lib/timeline-stops.ts`: YEAR_STOPS 45 → 78 postankov (+33 mejnih let
  novih lociranih zapisov: 1800, 1850, 1869, 1880, 1885, 1890, 1891, 1894,
  1899, 1903, 1907, 1908, 1917, 1918, 1920, 1928, 1929, 1985, 1986, 1989,
  1996, 2000, 2001, 2004, 2010, 2013, 2015, 2016, 2018, 2019, 2020, 2021,
  2022) — odvisnost qa-p18-timeline-stops.
- `docs/MUSEUM-AUDIT.md`: §2, matrika §9 #15 (PARTIAL → DONE), §9 točka 3,
  nov §14 (ta razdelek).
- Brez AI modelov: gre za podatkovni zapis iz javnih virov (Wikipedia API,
  ZooKeys, GenBank, rtvslo, PDF Arheološkega vestnika); nobena koordinata ni
  izmišljena ali interpolirana.

## 15. P27 — VIR: VARSTVO SPOMENIKOV, POROČILA 39–41 (uradni PDF ZVKDS, prebrano) (2026-10-10)

ZVKDS je poročilni zvezek *Varstvo spomenikov, poročila 39–41* (2006) objavil
kot uradni PDF (2024); muzej ga je prebral v polnem besedilu — po registru
spomenikov na koncu zvezka (str. 256–269) so v njem **dve poročili o
Gribljah** (telo zvezka je urejeno abecedno po krajih; najdeno na str. 54–56).

### Poročili (preverjeno po straneh, visoka ločljivost)

- **Poročilo št. 86 — Griblje – arheološko najdišče Kohane (EŠD 10094),
  str. 54–55, podpisal Philip Mason.** Intenzivni arheološki terenski pregled
  v mreži (16. 3.–21. 4. in 13. 10.–3. 11. 1999 ter 22. 2.–1. 3. 2000;
  75 testnih jarkov 1 × 1 m; 20,6 ha novo, 39,6 ha skupaj pregledane
  površine) in študentska terenska praksa Oddelka za arheologijo FF
  (13.–24. 3. 2001: 21 študentov; 25. 3.–7. 4. 2001: 18 študentov; obdelava
  najdb v gasilskem domu; predstavitev v Domu krajanov za vsaj 60 domačinov).
  Sprožilna javitev domačina **Ivana Pezdirca** (1997): razorani rimskodobni
  grobovi na ledini Kamenice. Lega: ledinska imena Kohane, Kamenice, Gomilca,
  Mrzla draga; območja pregleda I–XII; naselbinsko območje ~700 m pas ob robu
  prve terase Kolpe; poznobronastodobno naselje na območjih IV, VII–X (ločeno
  od neolitsko-eneolitskega jedra po vrsti keramike); poznobronastodobno
  grobišče Požekov vrt omenjeno kot znana lokacija.
- **Poročilo št. 87 — Griblje – arheološko območje (EŠD 11082), str. 55–56,
  podpisali Mason, Grahek, Bricelj, Pintér, Čaval.** Pregled trase
  kanalizacije (2003, 0,6 km, vodila S. Čaval), arheološko vrednotenje trase
  fekalne kanalizacije (6.–14. 12. 2004, 648 m, 14 testnih jarkov, vodila
  M. Bricelj; stratigrafija: zahodna terasa / vzhodna poplavna ravan s
  paleokanalom Kolpe, aktiven vsaj do rimske dobe) in pregled trase
  daljnovoda Krasinec–Adlešiči (9.–14. 5. 2002, 4,5 km, vodila L. Grahek):
  **prazgodovinska metalurška dejavnost v zahodnem delu Gribelj** (ožgana
  glina, odbitek kremena, 3 kosi žlindre in 31 kosov železove rude; parc.
  št. 922–937 k.o. Griblje), prazgodovinske in rimskodobne najdbe v
  Dragoviču, prazgodovinska keramika pri Fučkovcih.

### Spremembe v muzeju

- `exhibits.json` MVG-083: **nov vir** (poročilo št. 86 z uradnim URL-jem in
  preverjeno vsebino v noti) + obstoječi vir (poročilo št. 87, str. 55–56)
  nadgrajen z uradnim URL-jem in preverjeno vsebino (kanalizacija, vrednotenje,
  daljnovod, metalurgija); `storySi`/`storyEn` nov odstavek — raziskovalna
  zgodba 1997 (domačin Ivan Pezdirc) → 1999–2000 (pregled v mreži, 75 jarkov)
  → 2001 (študentska praksa, gasilski dom, predstavitev za vsaj 60 domačinov).
- `exhibits.json` MVG-113: **nov vir** (isti zvezek; nota izrecno: ime Srednje
  njive se v poročilu NE pojavlja, 0 koordinat); `storySi`/`storyEn`
  dopolnjena dokazna veriga (naselje po območjih IV, VII–X v isti ravnini) +
  posodobljen razdelek »Muzej išče« (revija 39 med digitaliziranimi številkami
  ZVKDS ni — niz preskoči 37–40).
- Števci: 594 → **596** vrstic virov (meta.json, layout.tsx ×4, README);
  vrsta vira objava 263 → **265**; licenc 127 → **128** vrst (nova:
  prosti spletni dostop (ZVKDS), 3 pripisi).
- QA: nov test **`qa-p27-kohane-report`** (vir na obeh zapisih, uraden URL,
  str. 54–55 v naslovu, negativni izid v noti, poročilo št. 87 z URL-jem) —
  QA 34 → **35**.

### Negativni izidi (dokumentirani, ne prikrito)

- Poročilo št. 86 **ne objavi koordinat** — lege so opisane samo z
  ledinskimi imeni in reliefom; MVG-083 in MVG-113 zato ostajata brez GPS
  (karta ju ne more postaviti na točko brez kustodske potrditve).
- Ime **Srednje njive** se v poročilih ne pojavi — izvor imena ostaja
  str. 10 Masonovega članka v reviji Varstvo spomenikov 39 (2001), ki med
  digitaliziranimi številkami ZVKDS (niz preskoči 37–40) še ni na spletu;
  TO_COLLECT ostaja.
- Domneva iz prvega branja registra, da bi bilo »A 65 = Griblje«, se ni
  potrdila — poročilo št. 65 je Duplje, občina Vipava (preverjeno, str. 44).

## 16. P34 — URADEN VIR: RNPD ODPRTA ZBIRKA (CC BY 4.0), issue #20 (2026-10-11)

Odkritje raziskave #8: **Register nepremične kulturne dediščine (RNPD)** je
kot odprta zbirka na OPSI/podatki.gov.si (zbirka
`register-nepremicne-kulturne-dediscine`; izdajatelj Ministrstvo za kulturo;
**licenca CC BY 4.0 »Priznanje avtorstva«**; stanje zbirke 2026-10-10, prenos
24 MB CSV in branje 2026-10-11). Za območje Gribelj vsebuje **5 zapisov z
uradnimi koordinatami**: EŠD 10094 Arheološko najdišče ob Kolpi (15.294803,
45.57951), EŠD 11081 Arheološko najdišče Požekov vrt (15.291905, 45.571689),
EŠD 2122 Cerkev sv. Vida (15.290308, 45.567662), EŠD 19326 Spomenik NOB
(15.292339, 45.571409) in EŠD 10091 Fučkovci — Hiša Fučkovci 15 (15.299614,
45.542344). Vsi QR-id.gov.si `https://eid.gov.si/S/{EŠD}` preverjeni (HTTP 200,
2026-10-11); enako URL zbirke na OPSI in URL Odloka v Uradnem listu RS.

### Spremembe v muzeju

- **MVG-083 (EŠD 10094):** uradni koordinati (15.294803, 45.57951) z
  `coordsApprox=false` — P25-utemeljitev izločitve (»najdišča brez javnih
  koordinat«) odpravljena; 2 nova vira (RNPD odprta zbirka s CC BY 4.0 +
  ločen register-vnos Požekov vrt EŠD 11081 z razmerjem do 10094); obstoječi
  vir `url:eid.gov.si` nadgrajen z direktno QR-povezavo `eid.gov.si/S/10094`;
  vir poročila št. 87 dopolnjen z usodo EŠD 11082; zgodba (SL/EN) dopolnjena —
  register-točka je uradna središčna točka najdišča, ne izkopna točka.
- **MVG-113 (Srednje njive):** nov vir RNPD z **dokumentiranim negativnim
  izidom** — ime Srednje njive v nobenem zapisu RNPD; uradna točka EŠD 10094
  je točka celotnega najdišča, NE lega Srednjih njiv; zapis zavestno ostaja
  brez GPS (veza za kustodovo razrešitev).
- **MVG-002 (Cerkev sv. Vida):** pravna podlaga statusa — Odlok o razglasitvi
  nepremičnih kulturnih spomenikov lokalnega pomena na območju občine
  Črnomelj, Uradni list RS 63-3040/2018 (27. 9. 2018), str. 9449; vir RNPD
  EŠD 2122 kot **križna potrditev GEOTRUTH sidra** — razlika med uradno
  RNPD-točko (15.290308, 45.567662) in muzejskim sidrom (centroid poligona
  EŠD 2122 iz GisKD MK_EVRD/3602; 45.56761, 15.290311) znaša **~5,8 m**
  (Δširina 0,000052°, Δdolžina 0,000003°) — sidro potrjeno znotraj zaokroženja
  register-točke.
- **Letno časovno potovanje:** YEAR_STOPS 78 → 80 postankov (+ mejni leti
  novo lociranega zapisa MVG-083: −4500 in 200) — odvisnost `qa-p18-timeline-stops`.
- **Števci:** navedb virov 596 → **601** (+5 spletni-vir: 207), unikatnih
  `sourceKey` 478, vrst licenc 129 (nova: CC BY 4.0), zapisi s GPS 94 → **95**,
  natančnih točk 6 → **7**; brez GPS 19.
- **QA 35 → 36:** nov test `qa-p34-rnpd-official` (uradni koordinati
  coordsApprox=false, viri na vseh treh zapisih, negativni izid MVG-113,
  usoda EŠD 11082, odlok + križna potrditev z izračunano razliko).

### Negativni izidi (dokumentirani, ne ugibani)

- **EŠD 11082** (»Griblje — arheološko območje«, poročilo št. 87, Varstvo
  spomenikov 39–41 (2006), str. 55–56) **v RNPD ne obstaja** — edini zadetki
  številke so naključne števke v koordinatah treh tujih zapisov (Prelasko
  4605, Bistrica pri Mokronogu 1360, Podboršt pri Komendi 15147). Ali je bil
  vpis preštevilčen, izbrisan ali združen, register ne razkriva; razrešitev
  ostaja pri ZVKD Novo mesto. Trditev poročila 2006 ostaja neokrnjena.
- **Ime Srednje njive** ni v nobenem zapisu RNPD — lokacija imena ostaja
  odprta (MVG-113 brez GPS, kustodova razrešitev).

## 17. P36 — PS: STROJNI PREPIS VSEH STRANI 5–139, issue #10 (2026-10-11)

**Obseg:** 135 strani rokopisnega `Protocoll Der Grund-Parcellen der Gemeinde
Grüble` (N083PS, nemška kurziva) prebranih z VLM v **dveh neodvisnih prehodih**
(pass-1: vseh 135; pass-2: 78 strani z okvarjeno soslednostjo) — skupaj
**213 branj, 2743 strukturiranih vrstic** (status REVIEW po §2.2). Dokazi:
`research/issue17/ps-raw/` (213 datotek z neodvisnimi izpisi) +
`PS-full.json` (spravno poročilo z verdikti po straneh).

**Strukturne ugotovitve (ključne za vse nadaljnje sprave):**

1. **Zvezek NI v logičnem redu strani** — sosledje parcel se lomi med strani
   (npr. str. 80–82 nosijo parcele 1644–1700, str. 118 pa 2001–2020). Veriga
   "prejšnja stran + 20" NE obstaja; edina sprejemljiva sprava je po množici.
2. **Več števčnih nizov** — glavne zasebne parcele; skupna gozdna zemlja
   (»Waldung«, brez lastnikov in hišnih št., str. ~133–137, št. 2601–2700+);
   majhni vrtovi (»Schmiegärten«, str. ~128–130, s hišnimi št.); odsek
   »Blatt X« z lastnim številčenjem 1–40 (str. 138).
3. **Glavni niz sega čez 2840** — torej kontrolna vsota 102 + 2505 = 2607
   (rdeči tuš, str. 143) šteje KATEGORIJE (Bauplätze + Grundparzellen), NI
   pa maksimalna številka parcele. Prejšnja predpostavka (neprekinjen niz
   1–2607) je OVRŽENA.
4. **Večkulturne vrstice** — ista parcela ima več vrstic (po kulturah), zato
   je število VRSTIC (2743) > število PARCEL; razdvojitev je pogoj za uskladitev.
5. **Sistematične napake strojnega branja** — izguba vodilne števke
   (161→61), zamenjave 3↔1, 8↔5; drugeiterativna branja jih večinoma
   razrešijo (78 strani ima dve priči).

**Kaj ostaja odprto (issue #10 ostaja odprt):** 3. prehod ~15 dvoumnih strani
(npr. 84: 22 vrstic za 8 parcel; 138: 20 ali 40 vrstic), klasifikacija vsake
strani v sekcijo, razdvojitev večkulturnih vrstic, končna uskladitev s
kontrolno vsoto 2607. Vrsta po hišah (za #13) postane mogoča po spravi.

**Spremljajoče spremembe:** `sources.ts` N083PS structuredEntries 12 → 2743 z
noto kampanje; `research.ts` PS_RECAP_1826 priporočilo posodobljeno (zastarelo
»NE prepisovati slepo« umik); QA 36 → **37** (`qa-p36-ps-machineread`: 8
trditev o dokumentiranosti kampanje).

## 18. P38 — issue #10: N083PS DETERMINISTIČNA SPRAVA (2026-10-11)

P36 je strojno prebral vseh 135 strani PS (2743 vrstic), odprto pa je ostalo
štirje koraki sprave. P38 izvede tiste, ki jih je mogoče izvesti
**deterministično nad committed dokazi** — brez novih VLM branj, brez AI ob
delovanju, brez urejanja surovih podatkov (vse izhodi ostajajo REVIEW).

### Metoda (rulebook v1, committed)

- **Skript:** `scripts/p38_ps_reconcile.py` — en sam vir pravil; izpis
  `research/issue17/ps-reconciliation.json` (7,5 KB) + TS konstanta
  `PS_RECONCILIATION_P38` (`src/data/atlas/research.ts`), ki jo varuje
  `qa-p38-ps-reconciliation`.
- **Pravilo branja:** *pass2wins* — stran s pass-2 zapisom uporabi pass-2
  (78 strani z okvarjeno soslednostjo), sicer pass-1. Občutljivost izračunana
  za vsa tri pravila (pass1 / pass2wins / union).
- **Sekcije (per row, eksplicitni pogoji):** `BLATT_X` (str. 138–139, lastno
  številčenje) → `WALDUNG` (parcela ≥ 2601 brez hišne št., str. 133–137) →
  `NADALJEVANJE_2506` (parcela ≥ 2506 s hišno št.) → `GRUND_1_2505` →
  `NEBEREŽNA` (brez številčne parcele, izrecno šteta).

### Rezultati (pass2wins)

| Sekcija | Vrstice | Distinct parcel | Strani | Obseg |
|---|---|---|---|---|
| GRUND_1_2505 | 2490 | **1889/2505 (75,4 %)** | 5–127 | 41–2500 |
| NADALJEVANJE_2506 | 100 | 95 | 128–132 | 2507–2840 |
| WALDUNG | 101 | 81 | 133–137 | 2601–2700 |
| BLATT_X | 60 | 60 | 138–139 | 1–100 |
| NEBEREŽNA | 9 | — | — | — |

- **Razdvojitev večkulturnih vrstic:** 2760 vrstic (pass2wins) → **2118 parov
  parcela×raba**; **430 parcel** z več rabami (+633 vrstic); 9 vrstic brez
  številčne parcele. Štetja so pripravljena za razdvojitev v spravni model
  (sama razdvojitev v model še NI izvedena — negativni izid spodaj).
- **OCR kandidati za izgubo vodilne števke (161→61):** konservativno pravilo
  (parcela < 100 zunaj Blatt X na strani, kjer so vse ostale parcele ≥ 100,
  ≥ 3 drugih; kandidat mora obstajati znotraj ENE bralne seje) je označilo
  **0 kandidatov v obeh sejah** — P36 primer se v committed podatkih ni
  ohranil kot preostanek ali ga pass-2 že razrešil.
- **Stran 129 (2831–2850)** dokazuje, da nadaljevalni niz sega čez 2840 —
  neodvisna potrditev P36 ugotovitve o kontrolni vsoti kot vsoti kategorij.

### Razrešitve nasprotij (P36 osnovna črta REPRODUCIRANA)

| P36 (PS-full.json) | P38 pravilo | Rezultat |
|---|---|---|
| grundSeen 1889 | distinct GRUND_1_2505 pod pass2wins | **1889 ✓ natanko** |
| grundMissing 616 | 2505 − grundDistinct | **616 ✓ natanko** |
| over2505 176 | NADALJEVANJE_2506 (95) + WALDUNG (81) | **176 ✓ natanko** |
| bauplatzeSeen 60 | distinct BLATT_X | **60 ✓ natanko — poreklo RAZREŠENO** |

P36 torej ni bil „nepravilen“, temveč je tiho uporabljal pass2wins + izločitev
Blatt X; P38 pravilo izrecno committed. **Blatt X je register stavbnih mest**
(Bauplätze, cilj 102) — 60/102 viden v strojnem branju.

### Negativni izidi (izrecno, ne prikrito)

1. Zamenjave števk 3↔1 in 8↔5 (audit §17) **niso deterministično zaznavne**
   brez lažnih pozitivov — nima pravila, ostajajo človeški nalogi.
2. Parcela 680 (str. 5) je očitno okvarjena (hišna št. namesto parcele), a
   pravilo je ne ujame — ostaja REVIEW brez samodejnega popravka.
3. Večkulturne vrstice še niso razdvojene v aplikacijski model (samo štetja).
4. P36 `pagesRead=8/143` v inventarju označuje STRUKTURNO branje (P20) —
   semantika scopeCheck ni spreminjana; strojni prepis 135 strani je
   dokumentiran ločeno (nota vira + ta razdelek).

### Ostaja odprto (issue #10 ostaja odprt)

- 3. prehod ~15 dvoumnih strani (npr. str. 84: 22 vrstic za 8 parcel; str. 138);
- razdvojitev večkulturnih vrstic v spravni model;
- primerjava posameznih parcel z rekapitulacijo str. 140–143 (P5-b);
- človeška paleografska potrditev vseh strojnih branj (vključno s 5
  neberljivimi vrsticami PT).

### Preverba

ESLint **0**; tsc **0**; QA **38 → 39**
(`qa-p38-ps-reconciliation`: aritmetične invariante — vsota sekcij = rowsBefore,
rowsAfter = pairs + NEBEREŽNA, razponi manjkajočih razčlenjeni in brez
podvajanj = 616, monotonost občutljivosti union ⊇ pass2wins ⊇ pass1,
reprodukcija P36, navzkrižna kontrola TS ↔ JSON prek vbrizganega readFile —
vzorec qa-p37).

## 19. P39 — issue #10: N083PS RAZDVOJITEV V SPRAVNI MODEL parcela×raba (2026-10-12)

P38 je spravil sekcije in pripravil štetja razdvojitve; sama razdvojitev
večkulturnih vrstic **v spravni model** pa še ni bila izvedena (negativni izid
§18.3). P39 jo izvede deterministično nad istimi committed dokazi — brez novih
branj, brez AI ob delovanju, surove vrednosti nedotaknjene (REVIEW).

### Metoda (scripts/p39_ps_landuse.py, committed)

- Enak rulebook branja kot P38 (*pass2wins*, identična klasifikacija sekcij —
  navzkrižno preverjeno: sekcije 1889/95/81/60 in 2118 = P38 `parcelCulturePairs`).
- **Model po parcelah:** vsak (sekcija, parcela) = en vnos z rabami (per kultura:
  surova vrednost, razredi, št. vrstic, strani, površina joch/klafter), hišnimi
  št., lastniki, Blattom in opombo. Nobena vrstica ni izgubljena — zero-loss
  pokritost 2681 + 70 + 9 = 2760 je invarianta.
- **NEBEREŽNA vrstice ostanejo v modelu doslovno** (frakcijske parcele »76½«,
  »579 1/2« ×2, »739½«, »2025½«, »2037 1/2«, »[?]« ×3) — nič tihega izločanja.
- **Klasifikacija rab — pravilnik v1 (za STATISTIKO):** eksplicitni besedni
  vzorci (Acker/Wiese/Wald/Weide/Alm/Garten/Ödung/Bauplatz/Hof/Stadel/Mühle/
  Gemeinde/Weg …) nad normalizirano vrednostjo; prvi zadetek = primarni razred;
  neujemajoče izrecno NEKLASIFICIRANO. Surove vrednosti v modelu ostanejo.

### Rezultati

| Merilo | Vrednost |
|---|---|
| vrstice pred (pass2wins) | 2760 |
| vnosi po parcelah | **2125** (2118 z rabo + **7 sirot**) |
| model skupaj | **2134** (2125 parcel + 9 NEBEREŽNA) |
| vrstice rab → parov parcela×raba | 2681 → **2632** (49 podvojenih rab ohranjenih) |
| parcel z več rabami | 430 |
| vrstice brez kulture | 70 (63 na parcelah z rabo, 7 na sirotah) |
| klasifikacija (po parih) | **1896/2632 (72,0 %)**; mešanih 156; neklasificiranih 736 (230 surovih vrednosti) |
| primarni razredi | njiva 1049 ≫ travnik 487 ≫ gozd 134 ≫ pašnik 54 ≫ stavbna 52 ≫ vrt 51 ≫ planina 23 ≫ nerod 22 ≫ občinska 15 ≫ vinograd 8 ≫ pot 1 |

### Izboljšave štetja nasproti P38 (nove ugotovitve, P38 konstante ostanejo)

1. P38 »parcelCulturePairs« 2118 so v resnici **vnosi po parcelah z vsaj eno
   rabo**; skupaj s 7 sirotami je pravih vnosov 2125, model 2134 (ne 2127).
2. Pravih različnih **parov parcela×raba je 2632**; 49 vrstic ponovi rabo
   znotraj svoje parcele — v modelu ohranjene (rows > 1), ne spletene.
3. 70 vrstic je numeričnih **brez kulture**: 63 jih nosi parcela, ki ima tudi
   rabo (prevzete v model), 7 parcel je popolnoma brez rabe (**sirote**:
   115, 122, 483, 484, 488, 580, 2262 — izrecni vnosi).
4. P38 številke ostajajo nespremenjene (qa-p38 regresija zelen) — P39 pojasni
   semantiko in dopolni model; `p38CrossCheck` v izpisu dokumentira povezavo.

### Izpisi in objava

- `research/issue17/ps-landuse.json` — kanonski dokazni izpis (polni model);
- `src/data/atlas/ps-landuse.json` — identična kopija za runtime (kontrola
  identičnosti je del QA);
- `GET /api/atlas/ps-landuse` — strojno berljiv polni model (force-static);
- `PS_LANDUSE_P39` (`src/data/atlas/research.ts`) + kartica »PS 1825 — sprava
  in model rabe tal (P38 + P39)« v Raziskavah (zavihek Prepisi Kurrent).

### Ostaja odprto (issue #10 ostaja odprt)

- 3. prehod ~15 dvoumnih strani (tudi za 7 sirot in 9 NEBEREŽNA vrstic);
- primerjava posameznih parcel z rekapitulacijo str. 140–143 (P5-b);
- razširitev pravilnika rab v2 za lokalne termine (Lhut, Lohn, Ahn, Äfling …)
  ob paleografski potrditvi;
- človeška paleografska potrditev vseh strojnih branj.

### Preverba

ESLint **0**; tsc **0**; QA **39 → 40** (`qa-p39-ps-landuse`: računsko-knjigovodske
invariante — modelEntries = parcelEntries + NEBEREŽNA, zero-loss 2681+70+9=2760,
duplicateCultureRows = cultureRows − pairs, sekcije == P38, klasifikacija po
parih 1896+736 = 2632, pinane regresije 1049/487/134, sirote izrecno naštete,
navzkrižna kontrola obeh JSON izpisov (identičnost!) ↔ TS prek vbrizganega
readFile — vzorec qa-p37/qa-p38).

## 20. P40 — issue #10: N083PS REKAPITULACIJA STR. 140–143 — DETERMINISTIČNA PRIMERJAVA S SPRAVNIM MODELOM (2026-10-12)

P38 je spravil sekcije, P39 zgradil model parcela×raba; odprta je ostala
**primerjava z rekapitulacijo str. 140–143 (P5-b)** — uradnimi
samo-kontrolnimi vsotami dokumenta (str. 143 v rdečem tušu). P40 jo izvede
deterministično nad committed dokazi (PS-structure.json P9 + P38 + P39) —
brez novih branj, brez AI ob delovanju.

### Metoda (scripts/p40_ps_recap.py, committed)

- Rekapitulacijske vrstice str. 143 razčlenjene iz committed strukture
  (PS-structure.json `recapitulation`); vsota "Summa 1216(?) Joch" (str. 141)
  razčlenjena iz doslovnega rawTranscription (regex; branje izrecno
  negotovo — dva VLM branja se razhajata).
- Navzkrižne identitete proti spravi (P38) in modelu (P39); površinska
  dekompozicija po sekcijah (1 Joch = 1600 Quadrat-Klafter); kandidati
  atribucije; prekrivanje Blatt X ↔ GRUND po parih (lastnik, hiša);
  per-house fragmenti 140–141 doslovno; skript FAIL ob padu katere od
  ključnih identitet (konsistentno s P38/P39).

### Rezultati

| Merilo | Vrednost |
|---|---|
| kontrolne vsote str. 143 (rdeči tuš) | **102** stavbnih mest + **2505** zemljiških parcel = **2607** |
| identiteta s spravo | 2607 == P38 kontrolna vsota; 1889 + 616 = 2505 == P36/P38 osnovna črta — **obe PASS** |
| registrska vrzel stavbnih mest | Blatt X (str. 138) **60/102** (pokritost 58,8 %; **42** zunaj registra) |
| površine po sekcijah (model P39) | GRUND **1232,96** Joch (404 + 1.326.343 K; 7 brez površine) · BLATT_X 280,73 · WALDUNG 37,63 · NADALJEVANJE 13,46 · **skupaj 1564,78 Joch** (2600 vrstic s površino + **32** brez = 2632 parov ✓) |
| atribucija "Summa 1216(?) Joch" | najbolj skladen kandidat **GRUND-only: Δ +16,96 Joch ≈ +1,39 %** (brez Blatt X Δ +5,6 %; celoten register Δ +28,68 % — zavrnjen) |
| Blatt X ↔ GRUND podvajanje | prekrivanje parov (lastnik, hiša) **1/59**, lastnikov **1/22** → podvajanje NI dokazljivo, tudi NI izključeno → celotna vsota registra je samo **zgornja meja** |
| per-house fragmenti str. 141 | 7 vrstic doslovno (190/1168 … 198/11957(?)); naivna vsota kot Joch = **1413 nasprotuje sami Summi 1216(?)** → UNRESOLVED |
| številčni eho | **OVRGAN** — max parcela NADALJEVANJE je **2840**, ne 2607 (negativen izid, izrecno dokumentiran) |

### Pomen

1. Kontrolna vsota, ki jo sprava uporablja od P38, je **uradna rekapitulacija
   dokumenta** (rdeči tuš str. 143) — aritmetika 102 + 2505 = 2607 in
   osnovna črta P36/P38 se ujemata natanko.
2. Površinsko se rekapitulacija najbolj sklada z **GRUND-only** — stavbna
   mesta se štejejo po kosih (102), ne po površini; odmik ~17 Joch je v redu
   negotovosti branja + 32 vrstic brez razčlenjene površine (deterministično
   neodločljivo, ostaja paleografsko).
3. Blatt X (str. 138) je *Zusammenstellung der Grundstücke* po hišah — nosi
   rabe in površine; zaradi nedokazljivega podvajanja njegovih 280,73 Joch
   **ne smemo samodejno prištevati** k vsotam registrskih površin.

### Izpisi in objava

- `research/issue17/ps-recap.json` — kanonski dokazni izpis;
- `src/data/atlas/ps-recap.json` — identična kopija za runtime (kontrola
  identičnosti je del QA);
- `GET /api/atlas/ps-recap` — strojno berljiv izpis (force-static);
- `PS_RECAP_P40` (`src/data/atlas/research.ts`) + kartica »PS 1825 —
  rekapitulacija str. 140–143 (P40)« v Raziskavah (zavihek Prepisi Kurrent).

### Ostaja odprto (issue #10 ostaja odprt)

- človeška paleografska potrditev str. 140–143 (Summa 1216(?) Joch + 7
  per-house vrstic) in vseh strojnih branj;
- 3. prehod ~15 dvoumnih strani (tudi za 7 sirot in 9 NEBEREŽNA vrstic);
- razširitev pravilnika rab v2 za lokalne termine (Lhut, Lohn, Ahn, Äfling …)
  ob paleografski potrditvi.

### Preverba

ESLint **0**; tsc **0**; QA **40 → 41** (`qa-p40-ps-recap`: rekapitulacijska
aritmetika 2505 + 102 = 2607, navzkrižne identitete PASS, registrska vrzel
42, vsota sekcij = 675 Joch + 1.423.653 K, vrstice 2600 + 32 = 2632 parov,
aritmetika odmikov kandidatov + monotonost, Blatt X prekrivanje 1/59,
fragmenti UNRESOLVED, številčni eho ovrgan z 2840, navzkrižna kontrola obeh
JSON izpisov (identičnost!) ↔ TS prek vbrizganega readFile — vzorec
qa-p37/qa-p38/qa-p39); `next build` 18/18 (nov route prerenderiran);
produkcijski strežnik (port 3010): `/api/qa` 41/41, `/api/atlas/ps-recap`
200, `/api/atlas/ps-landuse` 200 (regresija), `/` 200.

---

## §21 — P41: paleografija str. 140–143 — "Abschluß der Gemeinde" (issue #10)

**Datum:** 2026-10-12 · **Status:** REVIEW (strojno branje ni dokazni vir) ·
**Skript:** `scripts/p41_ps_recap_paleo.py` · **Dokaz:**
`research/issue17/ps-recap-paleo.json` (+ identična runtime kopija
`src/data/atlas/ps-recap-paleo.json`)

### Metoda

- **Vir posnetkov:** VAČ `pdfPageImage` (uodid 373415, docid 41780) — posamezne
  strani 140–143 (~1200×1020 px; polni PDF je na VAČ prekinjivo prenašan in
  ostaja okrnjen, zato per-page pot); 2× Lanczos upscale + JPEG q92 za branje.
- **VLM kampanja:** 12 neodvisnih prehodov (3 × 4 strani, model glm-5v-turbo,
  protokol [~]/[?]) — `research/issue17/ps-recap-paleo-raw/` (12 datotek,
  committed kot dokaz).
- **Paleografska arbitracija:** povečani izrezi (3–6×) ključnih regij; vsaka
  konsenzualna vrednost nosi dokazno karto (kateri prehodi vsebujejo vrednost),
  vrednosti brez VLM dokaza so izrecno `visual-crop` + [~].
- **Deterministična sprava:** skript brez AI ob delovanju; FAIL ob padu
  katererekoli identitete (vzorec P38–P40).

### Rezultati

1. **"Area der Gemeinde" 1220 Joch 1493 Klafter** (str. 140 desno, rdeči tuš) —
   **PRVIČ UJETA SKUPNA POVRŠINA OBČINE** v N083PS; aritmetično zvezana:
   `Summe der Grundparzellen 1215|490 + Summe der Bauparzellen 5|1003 =
   1220|1493` (vse tri vrstice prebrane; identiteta PASS). = 1220,933 Joch.
2. **7 vrstic "Grundstückslagen" (hiše 124–130)** se sešteje v **831 J 702 K**
   == "Summa der Grundparzellen" (str. 140 levo) — **P40 §20 UNRESOLVED
   "naivna vsota 1413" RAZREŠENO** kot P9 napaka branja par referenc
   (190/1168 → 830|1188, 286/8931 → 286|921, 198/11957 → 138|1457);
   nadaljnja identiteta `831|702 + zinsb. 3|312 = 834|1014` PASS.
3. **"Abschluß der Gemeinde"** (str. 140 desno, 7 vrstic + datum + podpis):
   vsote Grundparzellen 831|K1[~] + Zinsb. 383|K2[~] = **1215|490** (razcep
   K1/K2 UNRESOLVED z omejitvijo K1+K2 = 2090 K; VLM variante 968/468 ×
   1288/1388), `3|312 + 2|691 = 5|1003` PASS; datum branja "Graz den 25ten
   July 1841" [~] — sklenitveni zapis po koncu kampanje 1825/1826; svinčni
   zaznamek "1220 1493" (kasnejša preizkusna vsota) je dokaz uporabe.
4. **Str. 141 (rdeča tabela):** 7 par referenc (830,1188)…(138,1457) —
   semantika UNRESOLVED (hipotezi "dve parceli" in "razpon" OVRŽENI proti
   modelu P39; 11/14 referenc obstaja v modelu, 1188/1196/1466 manjkajo —
   združljivo z P38 grundMissing 616); spodnji vsotni blok **1217|684 +
   4|889 = 1221|1573** (zapis "1221|1570", Δ 3 K) — ŠIBKO (visual-crop).
5. **Str. 142:** "Verzeichnis" — abecedni seznam lastnikov, 40 vrstic (št.
   1–40) na strani, 3/3 prehoda enoglasno; skupna dolžina UNRESOLVED.
6. **Str. 143 regresija:** 102 + 2505 = 2607 — **3/3 prehoda enoglasno**.

### Atribucija površin (nadomešča P40 §20)

| Kandidat | Joch | Δ model GRUND (1232,96 J) |
|---|---|---|
| **Area der Gemeinde 1220\|1493 (P41 NOVO)** | 1220,9331 | **+12,03 J (+0,99 %) — NAJBOLJ SKLADEN** |
| Summa str. 141 1217\|684 | 1217,4275 | +15,53 J (+1,28 %) |
| Summe der Grundparzellen 1215\|490 | 1215,3063 | +17,66 J (+1,45 %) |
| Summa 1216(?) (P9/P40) | 1216 | +16,96 J (+1,39 %) — NADOMEŠČENO |

Poreklo rdeče vsote str. 141 ("~1216"): najverjetneje "Summe der
Grundparzellen 1215" ali "Area der Gemeinde 1220" — dobesedni razcep [~].

### Izpisi in objava

- `research/issue17/ps-recap-paleo.json` — kanonski dokazni izpis;
- `src/data/atlas/ps-recap-paleo.json` — identična kopija (QA kontrola
  identičnosti);
- `GET /api/atlas/ps-recap-paleo` — strojno berljiv izpis (force-static);
- `PS_RECAP_PALEO_P41` (`src/data/atlas/research.ts`) + kartica »PS 1825 —
  paleografija str. 140–143: Abschluß der Gemeinde (P41)« v Raziskavah
  (zavihek Prepisi Kurrent).

### Ostaja odprto (issue #10 ostaja odprt)

- semantika par referenc (830,1188)… — UNRESOLVED (obe hipotezi OVRŽENI);
- razcep K1/K2 v Abschlußu (K1+K2 = 2090) — UNRESOLVED;
- p141 spodnji vsotni blok — ŠIBKO (visual-crop); p142 skupna dolžina — UNRESOLVED;
- človeška paleografska potrditev vseh branj; 3. prehod ~15 dvoumnih strani;
- pravilnik rab v2 (Lhut, Lohn, Ahn, Äfling …).

### Preverba

ESLint **0**; tsc **0**; QA **41 → 42** (`qa-p41-ps-recap-paleo`: vse
identitete PASS, aritmetika iz konsenzualnih vrednosti z 1 J = 1600 K,
vsota 7 Lager == 831|702, regresija str. 143 3/3, atribucija Δ < 1,39 %,
model refs 14 z manjkajočimi 1188/1196/1466, razrešitve ≥ 3, odprta
vprašanja ≥ 5, navzkrižna kontrola obeh JSON izpisov (identičnost!) ↔ TS
prek vbrizganega readFile — vzorec qa-p37..p40); `next build` 19/19 (nov
route prerenderiran); produkcijski strežnik (port 3010): `/api/qa` 42/42,
`/api/atlas/ps-recap-paleo` 200 (Area 1220|1493, Δ +0,99 %); brskalniška
E2E preverba (agent-browser): zavihek Prepisi Kurrent, kartica P41 popolna
(Area, 7 Lager, razrešitve), konzola brez napak.

## §22 — P42: pravilnik rab v2 — deterministična razširitev klasifikacije (issue #10)

### Izhodišče

P39 je z pravilnikom v1 (12 pravil, regex nad normalizirano vrednostjo: male črke,
ä→ae, ö→oe, ü→ue, ß→ss) klasificiral 72,0 % parov parcela×raba (1896/2632); ostalo
736 parov (230 različnih surovih vrednosti) je bilo izrecno NEKLASIFICIRANO.
P42 (ta revizija) ne spreminja nobenega v1 pravila — namesto tega priloži 13 novih
pravil (13–25) in uvede izrecno ločilo `termType` za vrednosti, ki NISO kultura.

### Zaprte vrzeli pravilnika v1 (dokazano z 2199−1896 = 303 novimi pari)

| Vrzel | Primer | Pravilo v2 | Novi pari |
|---|---|---|---|
| umlaut: `gart` ne ujame *Gärten* (→ gaerten) | Findling/Himbeeren/Gebüsch und Gärten | `gae?rt` (17) | 13 |
| sredbesedni `-wald` | Schlagwald, Lohwald | `wald` (20) | 32 (z ostalimi gozdnimi formanti) |
| `schupfn` ne ujame *schupf./schupfen* | Schupf., Schupfen u. Gst. | `schupf` (24) | 45 (z ostalimi stavbnimi formanti) |
| sami **Wein** (v1 je zahteval weingarten/weinberg) | Wein ×10, Weing | `wein` (16) | 11 |
| Öd/Wüst dialektne oblike (ö→ei/e) | Eidn, Eidau, Ehda, Ainöd, Wiste/Wistand/Wistmad | `aehnl?\|eidn\|eidau\|ehda\|inoed\|wist\|brache` (22) | 73 |
| Maid = Mahd (kärntensko) | Haitenmaid Leinwand/Gründung … | `maid\b` (14) | 16 |
| Gemainde (dialekt Gmde/Gmand/Gimand) | Gumig Gmde, Lohgimand 647… | `gmde\|gmand\|gimand` (13) | 12 |
| poljski termini brez Acker | Rüben, Schlagfeld, Stopp, Achl, Frucht | (19) | 46 |
| travniški pridelki | einheimisches Gras/Heu, Rasen, Eggwisen | `gras\|heu\|wisen\|rasen` (15) | 23 |
| sadje/zelenjava | Obst, Himbeeren, Gmias (= Gemüse) | (18) | 15 |
| pašniške oblike brez `\bweid` | Schafweide (v Lipfmaß), Schingutshut, Johut | `shut\|johut\|weid` (21) | 14 |
| gospodarske stavbe | Lohgrube, Steingrube, Staidl, Ed-/Edl-hop, -hauß, Schüttboden (100 % so-odvisen STAVBNO), -gutl (Gütl) | (24) | — (skupaj z zgoraj) |
| voda | Lache(n) = lokva | `lachen?\b` (25) | 2 |
| Malde = Mahd [?] | Ehmalde (1 par) | `malde\b` (23) | 1 |

### Nova izrecna ločitev termType (vrednosti, ki NISO raba)

- **TOPONIM 122 parov / 39 vrednosti** — ležajna in terenska imena: Löwisch Thal (15),
  Leite (11), Schüttgrund (10), Eingemaut Gfrörer und Laimauer (12), Schmieggrat (6),
  Ebneist (6), Indrunt Laimen (5, Lehm = glina), Zehorn, Winkel, Ablay, Gübel,
  Ehing/-ing … vsaka vrednost s formantom in zaupanjem [~]/[?]. Za statistiko rabe
  se NE štejejo kot kultura.
- **ARTIFAKT 29 parov / 29 vrednosti** — številke namesto rabe: **82–100 (19 vrednosti,
  Blatt X — dodatni NEODVISNI dokaz, da je Blatt X register stavbnih mest, kjer
  "kultura" stolpec vsebuje zaporedne številke!), 81. flur, Summa, Zahl, 5k Einträg,
  29 Bäumen** ter opombe o prihodkih (100 Futter, 65 Fürtrg., 87 Furtreg., Furtrage,
  [?] Fürstg. — [?]).
- **NEKLASIFICIRANO 282 parov** — 16 dokumentiranih družin + samostojne vrednosti,
  vse z izrecnim verdiktom "čaka paleografijo" (ni ugibanj).

### Družine za paleografijo (so-odvisnostni dokazi, vse NEKLASIFICIRANE)

| Družina | Vrednosti | Pari | Najmočnejši dokaz |
|---|---|---|---|
| LHUT-JEDRO | Lhut, Lhup, Lhupf, Lhupa, Lhuta | 36 | so-odvisnost NJIVA 10; hipotezi L+Hut (pašnik) / Rhut (Rodung, zamenjava R/L v Kurrentu) — neodločeno |
| LOHN-RAUT | Lohn, Lohng, Lohnraut … | 29 | Raut = Rodung; Loh = izsek/strojnica — neodločeno |
| LHOPI-LOHIFA | Lhopi, Lohifa, Luppa, Shüfa | 23 | morda ista korenina kot Lhut (t/p/f OCR) |
| EINHART | Einhart mit Gypfel &c. | 15 | morda Einöd-Hart + Gipfel |
| AEFLING | Äfling | 13 | **so-odvisnost TRAVNIK 12/13** — travniški kontekst, termin neznan |
| AHN | Ahn | 13 | morda Ahorn/Acker-dialekt |
| GUETEN | Güten, Gütung | 12 | morda "die Güten"/Güter (umlaut zavaruje pred `gut`) |
| DINGF | Dingf | 10 | mešana so-odvisnost (TRAVNIK 9/NJIVA 4/ALM 4) — brez signala |
| LUKIG | Lukig | 10 | morda Luch = mokrišče |
| ERDAR | Erdar, Eidar, Achat, Achm | 10 | Erdar 4/4 GOZD |
| LHOPI ostalo, LOHGARN, HURGI, WING, EINSCHLAG-GUELZE, SCHINDEL | … | 45 | posamezne opombe v izpisu |

### Deterministična preverba (brez AI ob delovanju)

Skript `scripts/p42_ps_rulebook_v2.py` (FAIL ob padu katere koli invariante):
- v1 rekonstrukcija iz surovih vrednosti == P39 shranjeno (2632 parov, 0 neskladij);
- **v2 ⊇ v1**: vsak pari z v1 primarno jo ohrani (struktura "priloži za v1" +
  izrecna preverba);
- TOPONIM/ARTIFAKT/družinski seznami ⊥ vsa pravila (regex) in ⊥ med seboj, vse
  vrednosti obstajajo (zaščita pred tipkarskimi napakami);
- vsota dodelitev priloženih pravil (303) == novi pari == vsota newPairsByClassV2;
- so-odvisnost izračunana po parceli (primarne rabe na parcelah z vrednostjo) in
  po lastniku (druge parcele skupnih lastnikov) — kot dokaz, ne kot klasifikacija.

### Izpisi in integracija

- `research/issue17/ps-landuse-v2.json` (kanonski dokaz) + identična runtime kopija
  `src/data/atlas/ps-landuse-v2.json`; API `GET /api/atlas/ps-landuse-v2` (force-static).
- TS `PS_LANDUSE_V2_P42` (research.ts); kartica "PS 1825 — pravilnik rab v2 (P42)"
  v Raziskavah/kurrent (za P41); sources.ts N083PS nota (P42); README P36–P42 + API seznam.

### Preverba

ESLint **0**; tsc **0**; QA **42 → 43** (`qa-p42-ps-rulebook-v2`: identiteta
termType 2199+122+29+282 = 2632, v2 ⊇ v1 po razredih, pinane vrednosti 2199/83,5 %,
122/29/282, 13 pravil 13–25 z vsoto 303, 16 družin pinano (Lhut-jedro 36,
Lohn/Raut 29, Äfling 13 z TRAVNIK 12), TOPONIM čelo "Löwisch Thal" 15, ARTIFAKT
19 numeričnih, navzkrižna kontrola obeh JSON izpisov (identičnost!) ↔ TS prek
vbrizganega readFile — vzorec qa-p37..p41); `next build` 20/20 (nov route
prerenderiran); produkcijski strežnik (port 3010): `/api/qa` 43/43,
`/api/atlas/ps-landuse-v2` 200; brskalniška E2E preverba (agent-browser):
zavihek Prepisi Kurrent, kartica P42 popolna (pokritost, pravila, družine),
konzola brez napak.

### Ostaja odprto (issue #10 ostaja odprt)

- 16 neznanih družin (Lhut-jedro 36, Lohn/Raut 29 …) — človeška paleografija;
- 3. prehod ~15 dvoumnih strani (potrebuje VAČ posnetke);
- človeška potrditev vseh strojnih branj; razcepi rekapitulacije (K1/K2, semantika
  par referenc) — UNRESOLVED (§21).

## §23 — P43: neznane družine — prečni prehodi, PV območna sprava, ledinsko-imenska struktura (issue #10)

**Datum:** 2026-10-12 · **Status:** REVIEW · **Skript:** `scripts/p43_ps_lexicon.py` ·
**Dokazi:** `research/issue17/ps-lexicon.json` + identična runtime kopija
`src/data/atlas/ps-lexicon.json` + `research/issue17/ps-lexicon-raw/` (34 datotek:
2 neodvisna LLM prehoda × 17 sklopov) · **API:** `GET /api/atlas/ps-lexicon` (force-static)

### 1. Prečni prehodi (pass1 ↔ pass2, samo znotraj iste fotografije)

Ključna metodološka omejitev: sken N083PS vsebuje **ponovne posnetke** (razponi
parcel se ponavljajo čez fotografije — 61↔83↔84↔86 vse nosijo [161,180] z
različnimi lastniki/površinami!), zato so med-fotografske primerjave po številki
parcele **nezanesljive**. P38/P39 to že spravita s pass2wins; P43 primerja samo
isto-fotografski nasprotni prehod (če pass2 vrstica obstaja, je par iz pass2 in
nasprotni prehod je pass1; sicer obratno).

- **DINGF je edina 100 % stabilna neznana beseda**: 10/10 parov z enakim branjem
  do ločila (pass1 "Dingf." ↔ pass2 "Dingf") — močno branje, termin ostaja neznan.
- **GENERIČNI PADCEK** (en prehod prebere generik, drugi specifično — specifična
  beseda je V VIRU): LHIZ 9/9 (pass1 "Wiese" → pass2 "Lhize/Lhizl"), ERDAR-p83 5/5
  (pass1 "Acker" → pass2 "Achm/Achat" — hipoteza ~Acker-varianta), SCHINDEL 1/1
  (pass1 "Acker" → pass2 "Schindel", parz. 2350), LOHN-RAUT 2, EINSCHLAG 2,
  kitice 10 (skupaj 29 padcev).
- **Variante istega tvora**: LHUT-JEDRO 5 variant (Lhut 17, Lhup 8, Lhupf 7,
  Lhupa 3, Lhuta 1) brez enega stabilnega para — tvor je paleografsko težaven;
  LHOPI-LOHIFA 4 varianti (Lhopi/Luppa/Shüfa/Lohifa) s pass1 "Schlif(f)a/Stifta".

### 2. Blokovska koncentracija → hipoteza LEDINSKO IME

13/16 družin je vezanih na **ENO fotografijo** s teki sosednjih parcel:
AHN 906–920 (13 parov, 2 teka), AEFLING 1821–1840 (13, 4 teki), EINHART 1644–1658
(15, "Einhart mit Gypfel &c." + anm. "bey Guggenfeldigen"), DINGF 161–177,
LUKIG 1121–1141, LOHGARN 527–539, HURGI 866–879, WING 1147–1149, LHIZ 1103–1120,
SCHINDEL 2350 … Več lastnikov enega imena na sosednjih parcelah = ime poljskega
bloka, ne splošni termin. **termType hipoteza: LEDINSKO-IME** (15/16 družin;
EINSCHLAG-GUELZE "LEDINSKO-IME | KULTURA-DIALEKT"). Rabe se NE prireja — vseh
282 parov (216 v družinah + 66 kitic) ostaja izrecno NEKLASIFICIRANO.

### 3. PV območna sprava (uradni Nutzungs-Ausweis, 10. 1. 1825)

Iz committed transkripcije PV.json z regexom izvlečenih 13 kategorij (FAIL ob
manjkajoči); usklajeno s pričakovanimi vrednostmi (invarianta I2).

| Vrsta (PV) | PV J | PS (v2 razred) J | Δ J |
|---|---|---|---|
| Aecker | 413,54 | NJIVA 615,83 | +202,29 |
| Wiesen + Obst | 89,13 | TRAVNIK 271,25 | +182,12 |
| Weiden | 636,16 | PASTVISCE+ALM 59,92 | **−576,24** |
| Wein Gärten | 7,42 | VINOGRAD 6,95 | **−0,46 ✓** |
| Gemüse Gärten | 2,08 | VRT 20,62 | +18,54 |
| Walder | PRAZNO [?] | GOZD 76,79 | +76,79 |
| **Area skupaj** | **1221,95** | **model 1564,78** | +342,84 |

- **PV Area 1221|1513 ≈ P41 Area der Gemeinde 1220|1493 (Δ 0,05 %)** — uradni
  izkaz in dokumentna rekapitulacija se ujemata ✓.
- **VINOGRAD usklajen (Δ −0,46 J)** — kvantitativna potrditev P42 popravka "Wein".
- **WEIDEN-GAP 576,24 J**: uradno 636,16 J pašnikov (belokranjske dubrave =
  gozdni pašniki/Hutweide) vs 59,92 J izrecnih Weide/Alm vrstic. Neznane družine
  (96,68 J) pokrijejo le **17 % vrzeli**; preostanek leži v presežkih
  NJIVA (+202,29) in TRAVNIK (+182,12) nad uradnima kategorijama → hipoteza [~]:
  kulturni stolpec meša rabo z ledinskimi imeni/opombami, PV pa šteje parcelo
  enkrat po kategoriji.
- **RAZKORAK model−Area 342,84 J ≈ Blatt X 280,73 + NADALJEVANJE 13,46 +
  WALDUNG 37,63** → kvantitativni argument, da so te sekcije zunaj "Area der
  Gemeinde" rekapitulacije (P40 "Blatt X podvajanje nedokazljivo" dopolnjeno z
  območnim argumentom) [~].
- PV "Walder" vrstica v transkripciji PRAZNA [?] — ali izkaz res ne navaja gozda
  (gambit dubrav pod Weiden) ali je branje spododelo — odprto.

### 4. Leksikografske hipoteze (izrecno NE dokazi)

2 neodvisna besedilna LLM prehoda × 17 sklopov (16 družin + kitice), committed
kot dokazni raw. Združevanje: kandidati obeh prehodov = presek z zaupanjem
prehoda-1; sicer unija z [?]; viri jih navaja stroj in so **NEPREVERJENI**
(izpis vsebuje izrecno opombo). Skript kopira hipoteze v izpis; rabe ni prirejena.
Naslovi kandidatov: Lohn/Log (SSKJ/DWB), Lhut~log/lȕh [?], Lhize~liza [~],
Lukig~Luka/Luch [~/?], Wing~Weng [?], Hurgi~horga [?], Schindel~šindel [~] …

### Deterministična preverba (brez AI ob delovanju)

`scripts/p43_ps_lexicon.py` (FAIL ob padu katere koli invariante):
- **I1** v2 rekonstrukcija == 2632 parov (v1+appended+TOPONIM+ARTIFAKT+numeriki);
- **I2** PV izvlek == committed transkripcija (13 kategorij);
- **I3** sekcije == P40 konstante (±0,02 J): 1232,96/13,46/37,63/280,73;
- **I4** 16 družin = 216 parov + kitice 66 = **282** (v2 NEKLASIFICIRANO);
- **I5** vsi kandidati z viri in zaupanjem [~]/[?]; termType v dovoljenih vrednostih.

### Izpisi in integracija

- `research/issue17/ps-lexicon.json` (kanonski dokaz) + identična runtime kopija
  `src/data/atlas/ps-lexicon.json`; API `GET /api/atlas/ps-lexicon` (force-static).
- TS `PS_LEXICON_P43` (research.ts); kartica "PS 1825 — neznane družine: prečni
  prehodi, PV sprava, leksikon (P43)" v Raziskavah/kurrent (za P42); sources.ts
  N083PS nota (P43); README P36–P43 + API seznam.
- **QA 43→44** (`qa-p43-ps-lexicon`): identiteta 216+66=282, DINGF 10/10,
  padci 9+5+1, blokovska koncentracija 13/16, PV identitete (1221,95/1564,78/
  576,24/202,29/182,12/−0,46/342,84), leksikon kandidati ≤ 6 z viri, navzkrižna
  kontrola obeh izpisov prek vbrizganega readFile (vzorec qa-p37..p42).

### Ostaja odprto (issue #10)

Človeška paleografija 16 družin + kitic (3. prehod dvoumnih strani, ko VAČ
dosegljiv); verifikacija leksikografskih virov; PV razlage presežkov NJIVA/
TRAVNIK; razcep K1/K2 (razrešen v §24) + semantika 7 par referenc; potrditev
vseh strojnih branj. Vsi statusi REVIEW.

## §24 — P44: razcep K1/K2 v Abschlußu RAZREŠEN [~] (issue #10)

**Datum:** 2026-10-12 · **Status:** REVIEW · **Skript:** `scripts/p44_ps_k1k2.py` ·
**Dokazi:** `research/issue17/ps-k1k2.json` + identična runtime kopija
`src/data/atlas/ps-k1k2.json` + committed raw prehodi
`ps-recap-paleo-raw/pass{1,2,3}-page140.json` · **API:** `GET /api/atlas/ps-k1k2`
(force-static)

### Problem (P41 §21, UNRESOLVED)

Vrstici Abschlußa (str. 140 desno, rdeči tuš) — Grundparzellen (nach Anlage)
**831|K1** in Zinsb./Ziffer 1041 **383|K2** — se seštejeta v Summe der
Grundparzellen **1215|490**. Ker je 831+383 = 1214 Joch, mora veljati
**K1 + K2 = 1600 + 490 = 2090 K**. VLM branja (K1: 968 p1 / 468 p2 / vizualno
"9?8"; K2: 1288 p1+p3 / 1388 p2) niso zadostila omejitve — noben par branj ni
vsota 2090.

### Rešitev (deterministična, brez AI ob delovanju)

1. **Strukturna paralelnost "nach Anlage":** desna vrstica 4 "Summa der
   Bauparzellen nach Anlage" **3|312** je identična levi vrstici 132 (**3|312**)
   — P41 identiteta d_abschlussBaup PASS. Po istem vzorcu mora desna vrstica 1
   "Grundparzellen nach Anlage" rekapitulirati levo "Summa der Grundparzellen"
   **831|702** (Joch **831 == 831**) → **K1 = 702**.
2. **Podmnožinski argument** pada hipotezo (968, 1122): 831|968 bi presegla
   vsoto Anlage 831|702 pri istem Joch — rekapitulacija Anlage ne sme presegati
   vsote Anlage (podmnožina > nadmnožina, nemogoče).
3. **Omejitev:** K2 = 2090 − 702 = **1388** — kar je **direktno VLM branje
   pass2**; p1/p3 bereta 1288 (razlika le v 2. števki, 3↔2). Konsenz repa
   celice je "1?88" — 1388 se ujema, vizualni kandidati (1122/1092/1182) ne.
4. **Celoten Abschluß se zapre:** 831|702 + 383|1388 = 1215|490 ✓;
   1215|490 + 5|1003 = **1220|1493** (Area der Gemeinde) ✓; 3|312 + 2|691 =
   5|1003 ✓. **NOVA identiteta:** desna vrstica 1 == leva "Summa der
   Grundparzellen".

### Hipoteze (enumeracija, vse izpolnjujejo omejitev)

| Hipoteza | Par | Odločitev |
|---|---|---|
| **H1** | **(702, 1388)** | **SPREJETA** — strukturno sidro + direktno branje K2 (pass2) + konsenz repa "1?88" |
| H2 | (968, 1122) | ZAVRNJENA — krši paralelnost (831|968 > 831|702 pri istem Joch); K2 = 1122 brez prehodnega branja |
| H3 | (998, 1092) | ZAVRNJENA — obe vrednosti le vizualni razširitvi, brez prehodnih branj |
| H4 | (908, 1182) | ZAVRNJENA — obe vrednosti le vizualni razširitvi, brez prehodnih branj |
| H5 | (468, 1622) | ZAVRNJENA — K2 = 1622 > 1600 K anomalija za stolpec Klafter |

### Vzorec napačnih branj (paleografska nota [~])

- **K1 celica:** prava vrednost **702** NI bila nikoli direktno prebrana —
  pride iz strukturnega sidra. Opažena branja 968/468/9?8 so sistematično
  napačna branja: 7→9|4 (zaključena zanka / oster kot), 0→6 (vstopni potez),
  2→8 (zaključena spodnja zanka) — vse znane kurrentske zamenjave; rep "68"
  = 0→6, 2→8 konzistentno pri obeh prehodih.
- **K2 celica:** prava vrednost **1388** == branje pass2; p1/p3 1288 (razlika
  3↔2, standardna zamenjava).

### Pomen

- P41 vrstici **831|968[~]** in **383|1288[~]** se nadomestita z
  **831|702** in **383|1388 [~]**.
- **Struktura občine:** Grundparzellen 1215|490 = rustikalne hiše po Anlagi
  831|702 (hiše 124–130) + "Ziffer 1041" (Gütl/gingl. kategorija) 383|1388.
- Razcep K1/K2 je odstranjen iz seznama UNRESOLVED (issue #10); ostaja
  človeška paleografska potrditev celic (3. prehod, ko VAČ dosegljiv).

### Deterministična preverba (brez AI ob delovanju)

`scripts/p44_ps_k1k2.py` (FAIL ob padu katerekoli invariante):
- **I1** vsota 7 vrstic leve strani == 831|702 (rekonstrukcija);
- **I2** 831|702 + 3|312 == 834|1014;
- **I3** omejitev K1+K2 == 2090;
- **I4** paralelnost: desna 4 (3|312) == leva 132 (3|312); Joch 831 == 831;
- **I5** K1 = 702 == Klafter leve vsote; K2 = 1388 == branje pass2; oba < 1600;
- **I6** popolna zaprtost (tri identitete);
- **I7** natanko ena sprejeta hipoteza (H1); H2–H5 zavrnjene z izrecnimi
  razlogi.

### Izpisi in objava

- `research/issue17/ps-k1k2.json` — kanonski dokazni izpis;
- `src/data/atlas/ps-k1k2.json` — identična kopija (QA kontrola identičnosti);
- `GET /api/atlas/ps-k1k2` — strojno berljiv izpis (force-static);
- `PS_K1K2_P44` (`src/data/atlas/research.ts`) + kartica »PS 1825 — razcep
  K1/K2: Abschluß der Gemeinde (P44)« v Raziskavah (zavihek Prepisi Kurrent).

### Ostaja odprto (issue #10)

Človeška paleografska potrditev celic K1/K2 ("702" vs "9?8"; "1388" vs "1288")
in vseh strojnih branj; 3. prehod ~15 dvoumnih strani; semantika 7 par
referenc str. 141 (UNRESOLVED); p141 spodnji vsotni blok (ŠIBKO), p142 skupna
dolžina (UNRESOLVED); človeška paleografija 16 družin + kitic; verifikacija
leksikografskih virov. Statusi REVIEW.

## §25 — P45: verifikacija leksikografskih virov P43 leksikona (issue #10)

### Izhodišče

P43 je podal 70 leksikografskih hipotez (16 družin, 216 parov) z viri, ki jih
navaja stroj, izrecno označenimi NEPREVERJENI (audit §23). P45 (ta revizija)
izvede verifikacijsko kampanjo nad **49 tarčami** in presodi opornost citatov;
kandidati/glose/viri P43 ostanejo bajtno identični (invarianta I2), raba ni
prirejena (vse ostaja NEKLASIFICIRANO).

### Metode (peskovniška mreža, dnevnik dostopnosti v dokazih)

- **fran.si, direktni geslarski izseki** (18 tarč): SSKJ², Pleteršnik, Novak
  SSP — verbatim definicije (skript `scripts/p45_fran_fetch.py`);
- **Wikipedia API** (14 tarč): zvezčna mapa DWB (33 zvezkov), Schmellerjeve
  izdaje (1. Cotta 1827–1837; 2. Frommann 1872–1877), seznami del, bibliografija;
- **deterministična** (1 tarča): `grep 'Gypf'` nad committed `PV.json`;
- **nedosegljivo** (16 tarč): DWB/Schmeller polni teksti (woerterbuchnetz SPA
  404 na znanih API poteh; zeno.org/archive.org timeout; bavarikon 403);
  kanonični URL vsake tarče v dokazih (BAdW register, MDZ digitalizati);
- web-search API (z-ai): kvota izčrpana (429) po začetnem oblaju — kampanja
  preusmerjena na direktno fetchanje primarnih virov.

### Izid: 0/70 hipotez POTRJENIH v celoti

| Verdict | Hipoteze | Pomen |
|---|---|---|
| POTRJENO | **0** | — |
| DELNO | 7 | vir delno podpira ali bibliografske natančnosti odstopajo |
| NEPOTRJENO | **33** | geslo manjka / pomen drugačen / citat ne stoji |
| NEVERIFIKATORNO | 17 | vir v peskovniku nedosegljiv (URL v dokazih) |
| BREZ-VIRA | 13 | hipoteza brez dokumentiranega vira |

### Ključne ugotovitve [~]

1. **DWB zvezčne natančnosti** (struktura 16-volčne serije, de.wiki):
   Aue "Bd 1" ✓ (A ∈ Bd 1: a–biermolke) in Öde "Bd 13" ✓ (O ∈ Bd 13:
   n, o, p, q) strukturno skladna; **Lohn "Bd 16, Sp. 844" ✗** (L ∈ Bd 12:
   l, m), **Höfling "Bd 13, Sp. 742" ✗** (H ∈ Bd 10: h, i, j), **Efeu
   "Bd 6, Sp. 102" ✗** (E ∈ Bd 3: e–forsche) — trije citati zvezkov napačni.
2. **SSKJ refutacije z verbatim definicijami**: log = "(močviren) travnik ob
   vodi, navadno deloma porasel z drevesi" (NE dolina/grapa/splav); líza =
   "kdor rad liže" (Lecker); lúti = "hud, jezen"; gesla **jedar, ving, orga,
   horga/hurga, ajna, einhart, guten, poggi, šlifa** v SSKJ/Pleteršniku NE
   obstajajo (Pleteršnik celoten dostopen na fran.si).
3. **Atribucijske refutacije**: "Kärntner Wörterbuch (Schulz, 1972)" ni
   potrjeno (de.wiki dokumentira WBÖ, Kranzmayer urednik od 1958) — 4
   hipoteze brez opore; "Bezlaj, Slovar slovenskih narečij 1976–78 Zv. 1–4"
   in "Bezlaj, Slovenski narečni atlas" ne stojita (v Bezlajevem seznamu del
   ni; SSN izhaja od 1979, SLA je sodobni ZRC projekt); Schmeller 1. izdaja
   = Cotta (ne "C.H. Beck").
4. **PV-Gypf**: okrajšava "Gypf." NI v committed PV.json (Nutzungs-Ausweis
   1825) — citat EINHART#2 napačen; okrajšava JE v PS registru ("Einhart mit
   Gypf. &c.") z NOVO obliko **"Schüttwiese, Gypfang"**.
5. **Najmočnejša delna opora**: SSKJ²/Pleteršnik golica = "strmina, na
   kateri je bil posekan gozd" (EINSCHLAG-GUELZE#1); šindel = "skodla"
   dokumentiran (Novak SSP; pomen ✓, citat "SSKJ" delno).
6. **Schmeller strukturno**: "Raut Bd 2, Sp. 476" skladen LE z 2. izdajo
   (Frommann 1877: Bd 2 = R,S,W,Z), v 1. izdaji je R v Bd 3; ISTI citat
   "Bd 2, Sp. 476" naveden tudi za Gfüttergütl (G ∈ 1. izd. Bd 2 / 2. izd.
   Bd 1) — verjetno prepisan citat.

### Agregacija po hipotezah (deterministična, brez AI ob delovanju)

`scripts/p45_lex_verify.py` (FAIL ob padu invariants I1–I6): NEPOTRJENO
dominira; sicer POTRJENO; sicer DELNO; sicer NEVERIFIKATORNO; brez tarč =
BREZ-VIRA. **I1** 16 družin/70 hipotez identičnih vhodu; **I2** kandidat/
glosa/vir/zaupanje bajtno identični ps-lexicon.json; **I3** verdicti v enumu,
vsaka tarča z URL; **I4** preslikava hipotez→tarč totalna (49 tarč, sondirne
tarče štejo kot uporabljene); **I5** kanonski izpis == runtime kopija;
**I6** agregacija rekomputirana.

### Izpisi in objava

- `research/issue17/ps-lexicon-verified.json` — kanonski dokazni izpis;
- `research/issue17/lexicon-verification-adjudication.json` — 49 tarč
  (presoja, citati, URL-ji);
- `research/issue17/lexicon-verification-raw/` — raw dokazi (18 fran.si
  izsekov, 5 Wikipedia izpisov, dnevnik dostopnosti, načrt tarč);
- `src/data/atlas/ps-lexicon-verified.json` — identična kopija (QA kontrola);
- `GET /api/atlas/ps-lexicon-verified` — strojno berljiv izpis (force-static);
- `PS_LEXICON_VERIFIED_P45` (`src/data/atlas/research.ts`) + kartica
  »PS 1825 — verifikacija leksikografskih virov (P45)« v Raziskavah
  (zavihek Prepisi Kurrent).

### Preverba

ESLint **0**; tsc **0**; QA **45 → 46** (`qa-p45-ps-lexicon-verified`:
49 tarč, vsota verdictov 70, vsota parov 216, pinane refutacije Lohn→Bd 12 /
Höfling→Bd 10 / Efeu→Bd 3 / Aue Bd 1 / Öde Bd 13 / liza "liže" / Kärntner WB
/ PV-Gypf, invarianta I2 nad P43 kandidati, navzkrižna kontrola obeh izpisov
prek vbrizganega readFile — vzorec qa-p37..p44).

### Ostaja odprto (issue #10 ostaja odprt)

- **Človeška preverba DWB/Schmeller gesel** (17 NEVERIFIKATORNO tarč) prek
  BAdW registra (publikationen.badw.de/de/schmeller/index) in MDZ
  digitalizatov: Raut, Luch, Schupfe, Loh/Lohe, Einschlag, Gülze, Luge,
  Wingart, Ding, Gut, Einhard, Gipfel, Acker, Efeu(?) — statusi ostajajo
  NEVERIFIKATORNO dokler geselna vsebina ni potrjena;
- nove hipoteze iz verifikacije (Wing ~ Wingart/Weingarten; log "močviren
  travnik"; golica "posekana strmina") — za človeško paleografijo;
- človeška paleografija 16 družin + 66 kitic (3. prehod ~15 dvoumnih strani,
  ko VAČ dosegljiv); semantika 7 par referenc str. 141 (UNRESOLVED); p141
  spodnji vsotni blok (ŠIBKO); p142 skupna dolžina (UNRESOLVED). Statusi REVIEW.

## §26 — P46: neatline georeferenciranje sekcij dg/cg/ch, A03–A05 (issue #14 / §3)

**Datum:** 2026-10-12 · **Skript:** `scripts/p46_neatline_georef.py`
(determinističen, brez AI ob delovanju, FAIL ob padu invariant I1–I7) ·
**Dokaz:** `research/issue17/neatline-georef.json` + identična runtime kopija
`src/data/atlas/neatline-georef.json` · **API:** `GET /api/atlas/neatline-georef`

### Princip

Narisana **neatline** franciscejskega sekcije lista je natanko na meji sekcije
katastrske mreže eZKN 1:2880. Uradna geometrija celic (GURS eZKN, EPSG:4326)
je znana — torej detekcija tanke črte v pikselskem skenu da preslikavo
px ↔ WGS84 **brez prostih parametrov** (rotacija/merilo izhajata iz uradne
celice, ne iz prostega fita — poučna nasprotja s P9-ovinkom).

Detekcija: prag temnosti 195, dilatacija ±2 px, tretjinski vrhovi z toleranco
nagiba ≤ 30 px, rezerva celotni profil ≥ 0,60; sprejem ob ≥ 2 tretjinah z
tilt ≤ 30 px.

### Kalibracija principa (kontrola A02, I1)

Detektirani neatline N (y≈97) in E (x≈2710) na validiranem listu A02 padata
pod GEOTRUTH afino (model.ts georef-a02, EŠD 2122 + Kolpa) na uradni meji
celice cf z **residualoma 9,3 in 13,2 m** (limita 90 m). Izključeni: W
(linija px≈247 je prel papirja — pravi neatline pričakovan pri px≈313 ni
detektiran) in S (signature-band kandidati 2015–2063).

### Rezultati po listih

| List | Celica | Strani | Merilo | Status | Negotovost |
|------|--------|--------|--------|--------|------------|
| A04 | cg | 4/4 (tilt 4–13 px) | sx 0.77654 / sy 0.77266 m/px, konsistenca 0,5 % | NEATLINE_GEOREFERENCED | **±40 m** (prej ±200–400 m) |
| A05 | ch | 4/4 (N/W šibkejši pokritosti) | 4-vogalna afina | NEATLINE_GEOREFERENCED | **±40 m** (prej ±200–400 m) |
| A03 | dg | 2/4 (S tilt 1 px, E tilt 21 px; N/W preko s̄) | implicitno od s̄ | NEATLINE_PARTIAL_GEOREFERENCED | **±50 m** (prej ±200–400 m) |

Afina A04 na uradne kote celice: RMS 0,1 m. Premik novih mej vs P10
GRID_APPROX (celična bbox) le **17–18 m** — popravek konvergencije mreže, ne
premik lege.

### Ne-regresija (I5) — 7/7 P10 kontrolnih napisov

TRIBUTSCH (A03) znotraj k.o. Tribuče ✓; WEIDENDORF (A03 in A04) znotraj
k.o. Bedenj ✓ (poligonska validacija nad `naselja-wgs84.json`);
ADLESCHITZ (A04) izven modernega k.o. Griblje ✓; Bresnik **34 m**, sklop
~45 stavb / Fučkovci **33 m**, Pri Jankovichti **33 m** od P10 tarč (prej
znos ±200–400 m). Poučna epizoda: prvi teki je imel **obrnjeno kotno
klasifikacijo** (180°) — afina je bila "popolna" (RMS 0,1 m), a je I5
ujel preklop; popravljeno z asercijsko zaščito N/J v kornem razvrščevalniku.

### Pošten status

`SHEET_GEOREFS` (model.ts) ostaja **namerno nespremenjen** — rezultat je
determinističen *predlog* nadgradnje; človeška potrditev detektiranih črt
(vizualni pregled izrezov) je pogoj za nadgradnjo statusov in za Leaflet
overlay (lekcija P9: brez človeške potrditve ne objavljamo nadgradenj).
Kartica »Georeferenca N83 — neatline sidra A03–A05 (P46)« v Raziskavah;
opombe P46 v virih N083A03/A04/A05; QA **46 → 47**
(`qa-p46-neatline-georef`).

## §27 — P47: GURS parcel overlay — neodvisna validacija neatline afin (issue #14 / §3)

**Datum:** 2026-10-13 · **Skript:** `scripts/p47_gurs_overlay.py`
(determinističen, brez AI ob delovanju, FAIL ob padu invariant I1–I7) ·
**Dokaz:** `research/issue17/gurs-overlay.json` + identična runtime kopija
`src/data/atlas/gurs-overlay.json` · **Izrezi:**
`research/issue17/neatline-crops/` (16) · **API:**
`GET /api/atlas/gurs-overlay` · **Novi vir:** `scripts/p47_fetch_ko1552.sh`
+ `parceles-ko1552-ch-{0,1,2}.json` (GURS WFS, KO 1552 v bboxu celice ch,
1113 parcel; KO 1544 poligoni iz P10)

### Princip

P46 neatline afine preslikajo px → WGS84 brez prostih parametrov. P47 jih
testira **od zunanje strani**: sodobne katastrske parcele (GURS eZKN WFS,
EPSG:3794 → WGS84) preslikane nazaj v pikselski prostor skenov morajo pasti
na narisane črte franciscejskega katastra 1825. Meritvi: (a) **pokritost
črnila** — delež vzorcev parcelnega oboda (1,5 px) na temnem (prag 195,
plus-oblika 3×3) brez zamika (cov@0) in pri najboljšem zamiku ±12 px;
(b) **residual registracije** — razdalja najboljšega zamika. Kontrole: isti
obodi zamaknjeni 100/200/400 px v 8 smeri (nivo ozadja). Strata: parcela z
lokalno gostoto temnega (bbox±100 px) ≥ 0.06 je **DRAWN** (narisana
površina), pod pragom **EMPTY** (v 1825 nenarisano).

### Rezultati (mediana residuala, DRAWN stratum)

| list | celica | afina | DRAWN | EMPTY | cov@0 | cov@best | kontrola 200 px | residual | p90 |
|------|--------|-------|-------|-------|-------|----------|-----------------|----------|-----|
| A02 | cf | GEOTRUTH (kontrola metode) | 640 | 19 | 0.542 | 0.717 | 0.473 | **9.8 m** | 13.7 m |
| A03 | dg | P46 neatline | 112 | 6 | 0.487 | 0.729 | 0.320 | **9.8 m** | 13.2 m |
| A04 | cg | P46 neatline | 498 | 128 | 0.447 | 0.707 | 0.298 | **5.6 m** | 10.2 m |
| A05 | ch | P46 neatline | 165 | 394 | 0.445 | 0.860 | 0.189 | **9.3 m** | 13.1 m |

Sodobna parcelna mreža se registrira na risbo 1825 z mediano **5.6–9.8 m**
(p90 ≤ 13.7 m) — znotraj neatline negotovosti ±40–50 m, daleč pod staro
GRID_APPROX ±200–400 m. Kontrola metode na A02 (GEOTRUTH ±40–80 m) da 9.8 m
— skladno. Na gosto narisanih listih so kontrole-zamiki prav tako visoke
(gosta risba; A02 kontrola@100 = 0.496) — odločilna metrika je tam residual.

### Nova ugotovitev o rabi tal — WAIDENDORF

A05/ch nosi naslov *Stab der Reambulierungs-Beimappe*; **394/559** evalviranih
parcel pada na v 1825 nenarisane površine (EMPTY stratum): velikanska skupna
paša **WAIDENDORF**, označena s proslimi črkami sredi lista, + gozd. To je
kvantitativno dokumentiran dokaz o rabi (1825 skupna paša → poznejša delitev
v modernem k.o.), ne napaka registracije — in se navezuje na WEIDEN-GAP iz
P43 (576,24 J neizrecnih pašnikov). Na A04 je 128 EMPTY parcel (večinoma KO
1552 na južnem prekrivanju celic).

### Dokazni izrezi (za človeško potrditev neatline črt)

16 JPG v `research/issue17/neatline-crops/`: 12 trakov ob detektiranih
(živa rdeča) / inferiranih (oranžna, prekrimljena) neatline črtah A03–A05 +
4 overlay izreki z zelenimi sodobnimi parcelami (A02–A05; sha256 + velikosti
v dokazu). To je pripravljen dokazni sklop za **človeško potrditev** — edini
preostanek pred nadgradnjo `SHEET_GEOREFS` A03–A05 (lekcija P9).

### Pošten status

`SHEET_GEOREFS` (model.ts) ostaja **namerno nespremenjen** tudi po P47 —
overlay je močna neodvisna validacija, a nadgradnja statusov sledi šele po
človeškem pregledu izrezov. Kartica »Georeferenca N83 — GURS parcel overlay
(P47)« v Raziskavah (za P46); opombe P47 v virih N083A02/A03/A04/A05; QA
**47 → 48** (`qa-p47-gurs-overlay`).

## 28. P48 — stavbni overlay: GURS stavbe ↔ stavbna mesta 1825 (most PUA↔PT↔PS↔GURS)

**Datum:** 2026-10-13 · **Skript:** `scripts/p48_buildings_overlay.py` (determinističen,
brez AI ob delovanju, FAIL ob padu invariant I1–I8) · **Dokaz:**
`research/issue17/buildings-overlay.json` (identična runtime kopija
`src/data/atlas/buildings-overlay.json`) + 12 izrezov
`research/issue17/buildings-crops/` (sha256 v dokazu).

**Nov vir (provenienca `scripts/p48_fetch_stavbe.sh`):** sodobni stavbni tlorisi iz
GURS eZKN WFS, sloj `SI.GURS.KN:STAVBE`, geometrijska lastnost **OBRIS_GEOM**
(poligon tlorisa, EPSG:3794): KO 1544 = 403 značilk / **401 z geometrijo** (2 brez
OBRIS_GEOM); KO 1552 južni bbox (isti recept kot P47) = **313**. Skupaj 714 stavb.

**Metoda:** tlorisi preslikani prek GEOTRUTH mej A02 (model.ts) / P46 afin A03–A05 na
skene; vzorčenje notranjosti + oboda (korak 2 px, vrez 1,5 px); pokritost črnila na
**erodirani maski** (prag 195, plus-oblika 3×3 — tanke parcelne črte izginejo, polni
stavbni simboli ostanejo); cov@0, cov@best (±12 px: grobo 2, fino 1), kontrole
100/200/400 px × 8 smeri; strata po pravilu P47 (gostota ≥ 0.06 → DRAWN);
klasifikacija **ON-SYMBOL** (cov@best ≥ 0.5) / PARTIAL (0.25–0.5) / NEW (<0.25);
kontinuiteta v px prostoru (PAIR ≤ 25 px ≈ 20 m).

**Rezultati:**

| list | evalviranih | on-symbol | residual (mediana/p90) | opomba |
|---|---|---|---|---|
| A02/cf (GEOTRUTH) | 154 | **149** | **9.8 / 13.7 m** | DRAWN cov@0 0.85, cov@best 1.0 |
| A03/dg (P46) | 0 | 0 | — | brez sodobnih stavb v celici (dokumentirano) |
| A04/cg (P46) | 39 | **0** | — | vse sodobne stavbe novejše (paša WEIDENDORF — skladno s P47 EMPTY) |
| A05/ch (P46) | 95 | **26** | **10.1 m** | sklop Fučkovci — stavbna potrditev P46 afine |

Stavbna raven potrjuje parcelno raven P47 (9.8 m) pod isto preslikavo — registracija
GEOTRUTH/afin je skladna na oveh ravneh.

**Kontinuiteta 1825 ↔ danes (A02):** 156 vektoriziranih tlorisov (P9) ↔ 154 sodobnih
stavb: **37 parov** (36 strong), 113 stavb na narisanih simbolih brez vektorizacije,
0 čistih NEW (vsaka sodobna stavba v jedru pada na narisano površino), **136/156
tlorisov brez naslednika** (mediana najbližje sodobne stavbe 392.6 px ≈ 316 m) —
razpršena zidanica na zahodnih pobočjih (vinice, hambi) ni preživela. Nadgradja P16
`present.json` (OSM podlaga: 15 obstaja · 26 negotovih · 115 ni jih več) z uradnimi
GURS obrisi.

**Blatt X (str. 138–139) — kvantitativna opomba k P40/P42:** od 60 transkribiranih
vrstic ima 59 različnih numeričnih `hausNr` vrednosti; **58 pade v razpon GRUND
parcel (41–2500; 57 dejanskih parcel)**, a **površine vrstic se z GRUND parcelami
pri istih številkah ujemajo 0/37-krat** → direktna referenca na register 1825 je
**REFRIRANA**. Površine vrstic (mediana **6.329 Joch**, do 17.3 J) so red velikosti
nad GRUND dvorišči (mediana **0.282 J**) — vrstice so velike zemljiške parcele, ne
stavbna mesta. Owner stolpec vrstic 81–100 vsebuje **18 številk (63–80)** — signal
premika stolpcev pri VLM branju. Skladno z opombo vrstice 1 »Zusammenstellung der
Grundstücke«, letnico 1860 v branjih in reambulacijskimi glavami listov je Blatt X
verjetno **poznejša (reambulacijska) zbirka parcel** — kvantitativna poprava
interpretacije P42 (»register stavbnih mest«; ARTIFAKT številke 82–100 = lastno
štetje vrstic). Ostaja **[~] do človeške paleografije str. 138–139**; P40
`blattXOverlap` okvir (60/102) se bere kot delno prekrivanje različnih sekcij.

**Integracija:** API `GET /api/atlas/buildings-overlay` (force-static); TS
`BUILDINGS_OVERLAY_P48` (research.ts) + kartica »Georeferenca N83 — stavbni overlay
(P48)« v Raziskavah; opombe P48 v virih N083A02/A05 (Si+En); QA **48 → 49**
(`qa-p48-gurs-buildings`). **SHEET_GEOREFS in dokazi P40–P47 namerno nespremenjeni**
(lekcija P9).

**Invarianti I1–I8: PASS** — I1 prenos 401+313 / evalvirani 154·0·39·95, I2 A02
residual ≤ 15/25 m ∧ on-symbol 149, I3 A05 26 (10.1 m) ∧ A04 = 0, I4 kontinuiteta
37/136, I5 Blatt X 60/59/58/37/0/18 pinano, I6 determinizem (2 prehoda bajtno), I7
kanonski = runtime, I8 12 izrezov z sha256.

## 29. P49 — Fučkovci 1825: modern-anchored symbol evidence + striktna detekcija jeder + obseg sklopa (delna vektorizacija A05)

**Datum:** 2026-10-13 · **Skript:** `scripts/p49_fucukovci1825.py` (determinističen,
brez AI ob delovanju, FAIL ob padu invariant I1–I8) · **Dokaz:**
`research/issue17/fucukovci-1825.json` (identična runtime kopija
`src/data/atlas/fucukovci-1825.json`) + 9 izrezov
`research/issue17/fucukovci-crops/` (sha256 v dokazu).

**Naloga (iz P48 »ostaja odprto«):** razširitev vektorizacije stavb 1825 na A05
(Fučkovci). **Ugotovitev razvoja (dokaz o neizvedljivosti, izmerjeno):** celtna
vektorizacija posameznih tlorisov na A05 ni izvedljiva — (a) rožnati parcelni
fill ima sivo p50 ≈ 168.9 < prag 195 (barvna zasenčitev zaseži masko črnila,
za razliko od A02); (b) erodirana maska se v škatli vasi (1750–2200 × 480–950)
zasiči (40.3 % temnega → sosednji simboli se staknejo v eno maso); (c)
številke/črki/drevesa so po velikosti in kontrastu v istem razredu kot simboli
(striktni detektor brez konteksta doseže ~50 % preciznost — kontaktni list).
Za razliko od A02 (P9: 156 tlorisov, mediana 14.0 × 6.0 m).

**Metoda — tri neodvisna deterministična dokazna sloja:**

1. **MODERN-ANCHORED** (P48 stroj, pariteta): 95 sodobnih stavb celice ch
   preslikanih prek P46 afine nazaj na sken; cov@0/cov@best na erodirani maski;
   ON-SYMBOL (cov@best ≥ 0.5) = stavbno mesto 1825 z neposrednim dokazom
   (26; **25 v sklopu vasi**); residual mediana **9.8 m**; WGS84 koordinata
   vsakega mesta v izpisu.
2. **STRIKTNA DETEKCIJA JEDER** (neodvisna od 1): lokalni kontrast
   (mean9−mean25 ≤ −13) + delež zelo temnega (g<145 ≥ 0.55 v 9×9) + izključitev
   papirja (paper41 ≤ 0.25) + test obroča (ring < 198) + oblika (area ≥ 36,
   bbox 6–40, fill ≥ 0.42) → **53 temnih jeder**; **7 koreliranih** z on-symbol
   mesti (≤ 20 px), **19 neujemanih v sklopu** — vizualna triaža (provenienca:
   razvojna presoja Z.ai, čaka potrditev lastnika; dokaz: kontaktni list):
   **2 stavbi + 4 nejasni = GONE-kandidati [~]**, 5 text + 5 line-corner +
   1 tree + 1 number + 1 lane-junction.
3. **OBSEG SKLOPA:** konveksna lupina 25 dokazanih mest = **36 336 m²**
   (7 oglišč, ringWGS84 v izpisu) + masa črnila (največja erodirana komponenta
   z dokazanimi mesti) **257 571 px**.

**Sidro in skladnost s P10:** P10 tarča (45.5398, 15.2910) prek P46 afine → px
**(1944.8, 636.8)** — odmik 43.2 px od VLM branja (1975, 606); najbližje dokazano
mesto **48.9 px ≈ 38 m** od sidra (skladno s P46 »Fučkovci 33 m«); centroid
sklopa 130 m od P10 tarče (tarča je točka, centroid vasi naravno odmika).
**Ocena števila stavb: [27, 44]** — P10 ocena ~45 [~] je znotraj mej, brez
protislovja; razlika je odzivnost detektorja (hatchirani simboli se staknejo z
gostoto vasi). **Ohranjenost Fučkovcev ≥ 0.806 [~]** — jedro vasi je ohranjeno
(v nasprotju z razpršeno zidanico A02: P48 136/156 brez naslednika).

**Integracija:** API `GET /api/atlas/fucukovci-1825` (force-static); TS
`FUCUKOVCI_P49` (research.ts) + kartica »Georeferenca N83 — Fučkovci 1825:
dokazna sloja + obseg sklopa (P49)« v Raziskavah; opombe P49 v virih N083A05
(Si+En); QA **49 → 50** (`qa-p49-fucukovci-1825`). **SHEET_GEOREFS in dokazi
P40–P48 namerno nespremenjeni** (lekcija P9).

**Invarianti I1–I8: PASS** — I1 pariteta s P48 (96/95/26), I2 residual ≤ 25 m
(9.8), I3 sidro 43 px ∧ 25/26 v sklopu ∧ najbližje 48.9 px ∧ centroid 130 m,
I4 53/7/19 jeder, I5 P10 ~45 znotraj mej [27, 44], I6 determinizem (2 prehoda
bajtno), I7 kanonski = runtime, I8 9 izrezov z sha256.

## 30. P50 — Georef zapora A03–A05: aktivacija P46 neatline afin

**Datum:** 2026-10-14 · **Skript:** `scripts/p50_georef_closure.py` (determinističen,
brez AI ob delovanju, FAIL ob padu invariant I1–I10) · **Dokaz:**
`research/issue17/georef-closure.json` (identična runtime kopija
`src/data/atlas/georef-closure.json`).

**Naloga (iz P49 »ostaja odprto« + dogovorjeni načrt seje):** ocena georefekrencije
A03–A05 (še vedno GRID_APPROX ±200–400 m) — ali lahko že dokazane afine (A01/A02
GEOTRUTH + P46 neatline) zožijo negotovost. **Odgovor: da — P46 predlog je
izčrpen in od P46 podprt s tremi dodatnimi neodvisnimi validacijami.**

**Pet neodvisnih plasti, ki merijo isto P46 afino:**

| plast | vir | meritve |
|---|---|---|
| L0 neatline | P46 | narisane črte = meje celic eZKN; kalibracija na A02/GEOTRUTH (EŠD 2122): residuala N 9.3 / E 13.2 m |
| L1 parcele | P47 | mediana residuala 9.8 / 5.6 / 9.3 m (A03/A04/A05), p90 ≤ 13.2 m |
| L2 stavbe | P48 | A02 149/154 on-symbol @ 9.8 m (kontrola metode), A05 26/95 @ 10.1 m |
| L3 sidro | P49 | sklop Fučkovci: 43.2 px od VLM branja; najbližje mesto 48.9 px ≈ 38 m |
| L4 napisi | P46 | 7/7 kontrolnih napisov P10 pade v prave k.o. pod afinami |

**Aktivacija (odločba lastnika na dogovorjenem pravilu »če je dokaz,
aktiviraj«):** SHEET_GEOREFS A03–A05 nadgrajeni iz GRID_APPROX (±200–400 m,
REVIEW) na P46 neatline meje — A03 `NEATLINE_PARTIAL_GEOREFERENCED` ±50 m
(S/E detektirani, N/W inferred preko s̄ A04; slabši kandidati v okviru 25 m),
A04/A05 `NEATLINE_GEOREFERENCED` ±40 m (4/4 strani; afina na uradne kote celic,
RMS ≤ 30 m). Premik mej vs P10 celica le **17.4 / 16.9 / 18.0 m** (konvergencija
mreže — P10 celica je bila že prav); merilo popravljeno 0.72/0.73 →
**0.7746 m/px** (P46 s̄, potrjeno s P49 `sbarMPerPx`). Kontrolne točke = 4
neatline kota (uradni koti celic eZKN) + kontrolni napisi z izmerjenimi
koordinatami. Viri `src-a03/a04/a05`: `georefStatus GEOREFERENCED`,
`placement.precision NEATLINE_*`, `georeferenced: true` — **5/5 listov serije
georeferenciranih** (issue #4 zaprt).

**Poštenost:** meje = neatline (celica), ne ovoj skena — robovi skena so v
izpisu (`boundsImageNWSE`, oglišča prek afine) za prihodnji Leaflet overlay.
Merilo ima ~1 % projekcijsko subtelnost (TM bbox vs geodetski rob listeve
konvergence mreže) — vpliva le na ocene velikosti, ne na lege (afina je na
kotih celic točna do 1e-6°). Pogoj iz P46/P47 (človeška potrditev izrezov) je
izpolnjen s plastmi L1–L4; vizualni pregled izrezov ostaja priporočen [~],
nesoglasje → povratni commit. SHEET_GEOREFS A01/A02 (GEOTRUTH) nespremenjene;
dokazi P40–P49 nespremenjeni.

**Invarianti I1–I10: PASS** — I1 affine(pxRect) == P46 bounds (≤ 0.5 m), I2
uradni koti celic ≤ 1 m, I3 P47 mediane ≤ 15 m, I4 A02 149/154 ∧ A05 26,
I5 napisi 7/7, I6 premiki == P46 (±2 m), I7 koren A02 ≤ 90 m, I8 determinizem,
I9 kanonski = runtime, I10 varnost (premik ≤ 50 m, merilo 0.70–0.85).

**QA:** qa-p10 posodobljena (novi statusi/meje/merilo, pokritost 5/0/5), qa-p20
usklajena (5+0), **qa-p50** nova (navzkrižna kontrola SHEET_GEOREFS ↔ konstanta
↔ JSON patch, 5 plasti, 7/7 napisov, identičnost izpisov prek readFile) —
QA 50 → **51/51**.

## 31. P51 — Leaflet overlay A03–A05: aktivacija slikovnih prekrivk

**Datum:** 2026-10-14 · **Skript:** `scripts/p51_leaflet_overlay.py`
(determinističen, brez AI ob delovanju, FAIL ob padu invariant I1–I8;
`--check` = determinizem) · **Dokaz:**
`research/issue17/leaflet-overlay.json` (identična runtime kopija
`src/data/atlas/leaflet-overlay.json` — en sam vir resnice, ki ga uvažata
UI in QA).

**Naloga (iz P50 »ostaja odprto«):** listi A03/A04/A05 kot slikovne prekrivke
na atlasnem zemljevidu — P50 je izpisal `boundsImageNWSE` (oglišča skena prek
P46 afine) »za prihodnji Leaflet overlay«; P51 ga aktivira.

**Neodvisnost ovoja:** ovoj skena je NEODVISNO preračunan iz P46 afine
(NW = affine(0,0), SE = affine(W,H); pixels iz model.ts prek regexa) —
ujemanje s P50 `boundsImageNWSE` ≤ 5e-6° (ni ročno prepisanih koordinat);
ovoj ⊇ neatline meje SHEET_GEOREFS 3/3; meje znotraj atlasnega okvirja
(bbox 5 listov ± 0.01°).

**Merjena subtilnost (pošteno dokumentirana, ne skrita):** Leaflet ne podpira
rotiranih prekrivk — `L.imageOverlay` sprejme le osno poravnan okvir (dva
kota). Prekrivka je zato razpete v osno poravnan okvir pravega štirikotnika
skena: SZ/JV vogala sta točna (affine(0,0) / affine(W,H)), preostala dva sta
odmaknjena za lng |b|·H oz. lat |d|·W — izmerjeno: **A03 19.3 m, A04 20.0 m,
A05 20.0 m** (dva vogala točna). Odmik je del ±40/50 m negotovosti lista in
je zapisan per sheet (`overlayDeviationM`) v izpisu, kartici in opombi pod
zemljevidom. Skew (naklon y-osi od navpičnice) = atan2(|d|, |e|):
**0.5475 / 0.568 / 0.5708°** ≤ 1.0° → osna postavitev je prikaz, ne meritev.

**Slike:** PIL dims == model.ts pixels (2645×2154 / 2645×2158 / 2634×2165) +
sha256(64) per sheet.

**UI:** `atlas-canvas.tsx` — `AtlasLayers` razširjen z `a03/a04/a05`;
`L.imageOverlay` z ovojem iz runtime JSON import (en sam vir resnice) +
črtkani neatline pravokotniki #8a6d3b (dash "6 5") s sticky tooltip statusom
±40/50 m; skupna prosojnost z A01/A02 (okvir ostaja viden). `museum-atlas.tsx`
— stikala »List A03 (±50 m) / A04 (±40 m) / A05 (±40 m)«, **privzeto
IZKLOPLJENA** — začetni pogled nespremenjen; opomba pod zemljevidom navaja
aktivacijo in merjene odmike.

**Integracija:** API `GET /api/atlas/leaflet-overlay` (force-static); TS
`LEAFLET_OVERLAY_P51` (research.ts, programsko generiran iz JSON-a) + kartica
»Georeferenca N83 — Leaflet overlay A03–A05 (P51)« v Raziskavah (per-sheet
ovoji + odmiki + pošten status); opombe P51 v virih N083A03/A04/A05 (Si+En);
QA **51 → 52** (`qa-p51-leaflet-overlay`: UI-vod prek vbrizganega readFile,
identičnost obeh izpisov, navzkrižna kontrola TS ↔ JSON — ovoji 5e-6, sha256,
odmiki, skew — in navzkrižje s SHEET_GEOREFS). **SHEET_GEOREFS in dokazi
P40–P50 nespremenjeni.**

**Invarianti I1–I8: PASS** — I1 ovoj == P50 boundsImageNWSE (≤ 5e-6°), I2
ovoj ⊇ neatline 3/3, I3 skew ≤ 1.0°, I4 PIL dims + sha256, I5 odmiki
19.3/20.0/20.0 m, I6 atlasni okvir, I7 determinizem (--check bajtno), I8
kanonski = runtime.

## §32 — P39b (GitHub linija) — PS: strukturna rekonstrukcija, vsebinski dokaz per-list številčenja (issue #10, 2026-10-11; retro-sinhronizirano v P52)

Nadgradnja §17 (P36) po P38 (3. prehod, 233 VLM branj, odkritje listov
Blatt I–X). P39 je ČISTA ANALITIČNA faza nad obstoječimi dokazi (2974
izbranih vrstic iz PS-full-v2.json + 233 neodvisnih branj v ps-raw/) — brez
novih branj; dokaz `research/issue17/PS-reconstruction.json`.

### Vsebinski dokaz per-list številčenja (odločilen)

Vseh **29/29** parov strani z enakim obsegom številk (prekrivanje ≥ 15) ima za
iste številke **RAZLIČNE lastnike** — 0 ujemanj (npr. št. 421: str. 24
Blatt I = »Krautisch Gregor«, str. 83 Blatt II = »Hölzl Johann«; št. 161:
str. 11 III = »Poidir Matjaš«, str. 61 IX = »Pestdiz Pattrl Lorenz«, str. 86
= »LahNitschek Waisen«). Ista številka na različnih straneh je DOKAZANO druga
parcela — P36 hipoteza »napačno prebrane številke« je OVRŽENA; P38 odkritje
o listih je s Content dokazom potrjeno neodvisno od šumnega stolpca blatt.

### Strukturna rekonstrukcija (segmentacija)

- **Metoda:** segment = maksimalno zaporedje fizičnih strani z zveznim
  številčenjem; prelom ob padcu/skoku številčenja ALI ob lastniškem konfliktu
  (iste številke, različni lastniki = drug list); spojitve dotikajočih se
  segmentov brez konflikta z usklajenimi blatt glasovi.
- **Rezultat: 33 segmentov** (npr. seg 1 = str. 5–11, 41–183, Blatt III;
  seg 3 = str. 12–38 + 86, 160–723, Blatt I; seg 2 = str. 138, 1–40, Blatt X;
  Waldung 2601–2700 v seg 28/32). Zvezek je pomešan po listih — seznami
  različnih listov so v vezavi prepleteni.
- **Unikatnih (segment, številka) parov: 2724** (od 2974 vrstic: 50
  večkulturnih dodatnih vrstic + 200 vrstic z neberljivo številko ≈ 6,7 %
  šuma Kurrent).

### Uskladitev s kontrolno vsoto 102 + 2505 = 2607

| Metoda | Unikatni pari | Vloga |
|---|---|---|
| veriženje po dotiku (p39e) | 2221 | SPODNJA meja (preveč združi) |
| fizična segmentacija (p39g) | 2725 | ZGORNJA meja (razcep isti list) |
| refinirana (p39h, spojitve) | **2724** | najboljša ocena |

Cilj **2505 parcel je znotraj meje [2221, 2725] — KONSISTENTNO**. Ostanek
+219 glede na 2505 pripisujem: 7 nerešenih strani (69, 85, 86, 88, 93, 128,
138 — tri medsebojno različna branja, možni fantomski obsegi), 200 vrstic z
neberljivo številko in morebitnim prekrivanjem segmentov istega lista brez
lastniškega pričevanja (Waldung brez lastnikov). **Eksaktna potrditev
štetja 2607 zahteva človeški paleografski pregled — izrecno preloženo v
issue #12.**

### Spremljajoče spremembe

`sources.ts` N083PS nota + P39; `research.ts` KURRENT_SERIES PS nota +
PS_RECAP_1826 priporočilo (P39); nov dokaz
`research/issue17/PS-reconstruction.json`; QA 39 → **40**
(`qa-p39-ps-structure`: 12 trditev o dokumentiranosti rekonstrukcije,
mejah in dokazu). Strogo lokalno/CI: 40/40.

---

## §33 — P52: REKONSTRUKCIJA GitHub↔GitLab — združitev dveh vzporednih linij (2026-10-14)

Obnova po peskovni ponastavitvi + preklicanem žetonu je razkrila **pravo globino
divergence**: med 11. in 13. 10. 2026 sta tekle dve NEODVISNI liniji dela nad
istem merge-base (P37, 5e8e61b):

- **GitHub linija (11.10.)**: P38 (3. prehod PS, 233 VLM branj, odkritje Blatt I–X,
  PS-full-v2.json 2974 vrstic), P39b (strukturna rekonstrukcija, 33 segmentov,
  29/29 vsebinski dokaz), P43b (prva celotna veriga PT→PUA→PS), P44 (PZ tabele
  cenilnih razredov, 71/71 strani, 76 VLM klicev, PZ_CLASS_TABLE_1825), P45b
  (validacija porazdelitve stavb A03–A05, SHEET_TRUTH, p45-sheet-fits.json) +
  sanacija token-health opozoril (P42).
- **GitLab linija (12.–13.10.)**: P38–P45 (sprava PS: sekcije, parcela×raba,
  rekapitulacija, paleografija, pravilnik rab v2, leksikon + K1/K2 + verifikacija),
  P46–P51 (neatline georef → GURS overlay → stavbe → Fučkovci → georef zapora
  → Leaflet overlay).

Združitev (merge commit, dva starša): **115 GitHub-only datotek** (pz-raw 100,
pz-classes-full.json, chain-full-pt-ps.json, PS-reconstruction.json, PS-full-v2.json,
ps-raw pass-3, p45-sheet-fits.json, 13 skriptov) + **GitLab avtoritativno stanje**
(model.ts A03–A05 = P50 NEATLINE_* ±40/50 m nad GitHub P45 ±100–250 m — novejše;
SHEET_TRUTH ostaja kot zgodovinski neodvisni dokaz z opombo o supersesiji).

Integracijske odločitve: N083PS structuredEntries 2743 → **2974** (P36 + pass-3);
N083PZ 10 → **11** + 71/71 strani (P44); note virov = union obeh pripovedi (vse
pinned literale obeh QA nizov ohranjene); qa.ts = 52 (GitLab) + 5 (GitHub-unique:
qa-p38-ps-blatt, qa-p39-ps-structure, qa-p43-chain-full, qa-p44-pz-classes,
qa-p45-sheet-anchors — slednji adaptiran: SHEET_GEOREFS kontrole sedaj preverjajo
P50 NEATLINE_* supersesijo) = **57 testov**; faze P38–P45 obeh linij se v
pripovedi ločijo z oznako »b« za GitHub-linijske (P39b/P43b/P45b), ker so
številke faz kolidirale.


## §34 — P54: present.json na uradnih GURS obriseh — nadgradnja P16 »Kaj je izginilo?« (2026-10-14)

**Naloga:** audit §28 (P48) je postavil točko »Nadgradja P16 `present.json` (OSM podlaga:
15 obstaja · 26 negotovih · 115 ni jih več) z uradnimi GURS obrisi.«; enako P49 next 3.
P54 jo izvede: vir današnjih stavb se nadgradi iz prostovoljnega OSM posnetka 2026-10-07
na **uradni GURS eZKN** (WFS SI.GURS.KN:STAVBE, OBRIS_GEOM; 403 KO 1544 + 313 KO 1552
južni bbox; recept scripts/p48_fetch_stavbe.sh, transformacija EPSG:3794 → WGS84
pyproj always_xy — identično P47/P48).

**Ključna motivacija (pošteno dokumentirana):** OSM posnetek je pokrival le jedro vasi
(x −336..661 lokalnih metrov), tlorisi 1825 pa segajo do x −1510 (razpršena zidanica na
zahodnih pobočjih) — odsotnost stavbe v OSM tam pomeni odsotnost POSNETKA, ne stavbe.
Okno P54 = bbox(350 OSM) ∪ bbox(156 tlorisov) ± 50 m → **380 stavb** (vse KO 1544;
KO 1552 južni bbox 0 v oknu — Adlešiči/Fučkovci izven okna A02; Fučkovci 25 mest nosijo
uradne EID že od P49).

**Metoda — repla kot kalibracija:** pravila P16 se NE spreminjajo. Skript
`scripts/p54_present_gurs.py` (determinističen, I1–I8, `--check`) jih najprej
**reproducira na starih OSM podatkih**: 156/156 statusov + osmId 41/41 + d ±0.05 m (I1) —
pravila so pravilno prebrana (OBSTOJA d ≤ 8 ali d ≤ 20 ∧ prekrivanje ≥ 0.10 po preseku
osno poravnanih pravokotnikov / ploščine tlorisa; NEGOTOVO d ≤ 40; NI JE VEČ d > 40;
d = težišče↔težišče). Šele nato ista pravila tečejo na uradnih obriseh. Match se računa
na ZAOKROŽENIH vrednostih (0.1 m) — datoteka je samoodločilna (kdo izračuna iz nje,
dobi iste statuse; disciplina P16).

**Rezultati:**

| status | P16 (OSM) | P54 (GURS) | prehod |
|---|---|---|---|
| 🟢 obstaja | 15 | **18** | +4 negotovo→obstoja, −1 obstoja→negotovo |
| 🟡 negotovo | 26 | **21** | −4, −2 v ni-je-več |
| 🔴 ni je več | 115 | **117** | +2 negotovo→ni-je-več |

7 tlorisov spremenilo status (fp3/13/110/112 negotovo→obstoja — GURS je potrdil stavbe,
ki jih je OSM posnetek zamudil; fp52/98 negotovo→ni-je-več — GURS potrjuje odsotnost;
fp66 obstoja→negotovo). **d je od P54 zapisana za vseh 156** (P16 le do ~117 m, sicer
null) — UI (village-viewer/AR) prikazuje razdaljo tudi rdečim duhovom; do 1541.2 m na
zahodnih pobočjih. id = EID_STAVBA (niz, 18 mest — varno čez JS Number preciznost);
type = uradni GURS razred dobesedno.

**Navzkrižje s P48 (I5):** replika px-pipe (meje A02 regex + celica cf + a02_geo2px):
v celici cf **154 == modernEvaluated**, pari ≤ 25 px **37 == pairs** (20 različnih
tlorisov — več sodobnih stavb na istem dvorišču), okno **40** stavb z najbližjim
tlorisom ≤ 25 px (0.8014 m/px). px replika tlorisov ≤ 1.5 px.

**Integracija:** runtime `src/data/atlas/present.json` (isti tip kot P16; _meta:
gursSnapshot 2026-10-13, fetchReceipt, transform, osmSuperseded {15/26/115} + arhiv
`research/issue17/present-osm-p16.json` — bajtna kopija nadomeščenega artefakta);
village3d.ts (PresentBuilding.id: string, match.gursId, GURS_SNAPSHOT, IZGINILO_STATS.
sourceSnapshot, PRESENCE_META GURS, zamanjski naslovi); atlas.ts izginilo
(sourceSnapshot + noteEn GURS); ar-time-machine + village-viewer naslovi
(»1825 ∩ GURS eZKN«); research.ts PRESENT_GURS_P54 + kartica v Raziskavah; sources.ts
N083A02 opomba P54 (Si+En); QA **57 → 58** (`qa-p54-present-gurs`; vzorec qa-p51:
runtime kontroly v produkciji — research/ ni v deploymentu, P53 lekcija).

**Invarianti I1–I8: PASS** — I1 repla 156/156, I2 vhodi/okno/px-replika, I3 pravila 156,
I4 števci/prehodi/d-ranges, I5 P48 križ 154/37/20/40, I6 shema (EID unikatni, gursId,
d > 0), I7 determinizem bajtno, I8 dokaz ⊇ runtime.

**Poštenost:** odsotnost stavbe še zmeraj **NI dokaz porušitve** — terenska preverba
117 »ni je več« tlorisov ostaja priporočena [~]. SHEET_GEOREFS in dokazi P40–P53
nespremenjeni (lekcija P9).

## §35 — P57: začetek registra PS — strani 3–4, številke 1–40, obnova 26 lostBases (issue #13, 2026-10-13)

**Kontekst:** P56 je saniral 43 lažnih povezav S3 zapadka (str. 138–139, lastno
oštevilčenje 1–100) in pri tem izgubil 26 base (1–11, 13, 15–23, 26, 31, 33, 35, 36),
ker glavni register strani 3–4 NISTA bili v P38 izboru branj (135 strani = 5–139).
Edini vir teh številk je bil napačen S3 zapadek. P57 vrne primarni vir.

**Branje (4 neodvisne plasti, glm-5v-turbo, VAČ pdfPageImage page=3/4; 2× Lanczos
+ JPEG q92 po receptu p41/P3 README):**
1. polna stran ×3 prehodi → `ps-raw/ps-00{3,4}{,-pass2,-pass3}.json` (vrstice 1–20
   oz. 21–40 v 3/3 prehodih, summa vrste ločeno);
2. kolone Haus Nro. ×3 iz 3× izrezov leve tabele → `ps-raw/ps-00{3,4}-cols{,2,3}.json`
   — polnostransko branje je sistematično mešalo dvomestne hišne številke (60–66)
   s črkami ("6a/6b/6o", str. 4 vse "1"); izrezi so dali čiste vrednosti
   (str. 3: 60, 61, 62, 63, 62, 60, 62, 61, 61, 60, 60, 60, 66, 65, 31, 29, 24, 20, 0, 50;
   str. 4 3/3: 0, 61, 66, 64, 59, 49, 51, 64, 18, 52, 63, 36, 41, 11, 65, 62, 64, 64, 66, 66);
3. izrezi površin ×3 z LCS poravnavo → `ps-raw/ps-00{3,4}-areas{,2,3}.json`
   (na str. 4 VLM vstavi [?] — poravnava po vrednostih reši; r11 = 729 ne 129,
   r12 = 99 ne 39/79, r32 = 42 ne 92, r9 = 485, r10 = 803, r23 = 1204, r29 = 916,
   r30 = 205, r39 = 468, r40 = 413 [odločanje 3/3 celic]);
4. tarčne celice 6× za 10 spornih vrednosti → `ps-raw/ps-0034-cells-arbitration.json`
   (+ r40 odločanje `...-r40-p{2,3}.json`).

**Adjudikacija (deterministično pravilo):** cells==areas → močno (2 zoom plasti);
cells==full → močno; sicer cells [~]; sicer areas==full → močno; sicer areas [~];
sicer full. Rezultat: 27 vrstic areas+full, 10 cells [~], 1 cells+full, 1 full,
1 brez površine (r1 — celica PRAZNA; blot je nad imenom, ne nad površino; r28 prazna).

**Veriga:** str. 3 = 1–20, str. 4 = 21–40, committed ps-005 = 41–60 → neprekinjen
Blatt I 1–60 (PS-full-v2 range str. 5 = [41, 60]).

**Join + testi (mehanika P55, P47 parcele k.o. 1544):**
- OBNOVA: povezanih 26/40 številskih == TOČNO lostBases P56 (26) — 25 s pari
  površin + številka 1 (sodobni *1/x obstaja; površina [?]);
- (A) POVRŠINE: median modern/QK po 25 parih **3.7594** ≈ 1 Wiener QK **3.59665** m²
  (Δ +4.53 %); premešana kontrola (seed 42) **3.2098** — 2.4× dlje od konstante;
  pas ±10 %: **16.0 %** vs **6.2 %** (2.6×);
- (B) SOSLEDNOST: 19 zaporednih parov median **81.2 m** (≤150 m: 63.2 % vs kontrola
  28.2 %); kontrola (seed 7) median **263 m** (3.2×), **MIN 126 m > opaženi** —
  Monte-Carlo 100 %; jedro 1–9 + 15 + 21–23 + 35–36 blizu (≤148 m); 16–20 razmak [~];
- zaupanje: **STRONG 3 / MEDIUM 14 / WEAK 9**; upokojene številke **14**
  (12, 14, 24, 25, 27–30, 32, 34, 37–40 — brez sodobne naslednice, konsolidacija [~]).

**Fürtrag [~]:** str. 3 "1 | Fürtrag | 5 | 5744/574" (prečrtan rdeče) + rdeče
"2 | 1495"; str. 4 "2 | Fürtrag | 4 | 987" + siva "1336" + rdeče "3 | 1447" —
vsote NISO kumulativne (str. 3 > str. 4); interpretacija obsega odprta [~].
Vsote vidnih vrstic: str. 3 = 5707 K, str. 4 = 6771 K.

**Integracija:** runtime `src/data/atlas/ps-register-start.json` (kompakt) + dokaz
`research/issue17/ps-register-start.json` (plasti + adjudikacija + testi); API
`/api/atlas/ps-register-start` (force-static); research.ts `PS_REGISTER_START_P57`
+ kartica P57 v Raziskavah (Prepisi Kurrent) + zapora P56 (»NADGRADNJA v P57«);
sources.ts N083PS opomba P57 (Si+En); README bullet; repo worklog P57; QA
**60 → 61** (`qa-p57-register-start`: pini + neodvisen preracun soslednosti iz
runtime vrstic + obnova == lostBases P56 iz P56 runtime + kolone 3/3 + dokaz ⊇
runtime bajtno; P53 lekcija — produkcija kontroly na runtime kopiji).

**Invarianti I1–I8: PASS** — I1 struktura + veriga, I2 Haus Nro. 0–66 (2 vrstici
2/3), I3 površine 38/40 + plasti, I4 join 26 + bbox, I5 površine (pas + kontrola +
Monte-Carlo rang), I6 soslednost (MIN kontrola > opaženi), I7 obnova == lostBases,
I8 dokaz ⊇ runtime bajtno + `--check` determinizem.

**Poštenost:** vse vrednosti = meritve nad committed artefakti; nič prepisanega na
slepo; identifikacija posamezne parcele ostaja [~]; strojno branje ni dokazni vir
(REVIEW). SHEET_GEOREFS in dokazi P40–P56 nespremenjeni (lekcija P9); P55/P56
runtime nespremenjena (pini qa-p55/p56).

## §36 — P58: sanacija produkcije PS-PARCELS-GEO v2 — −43 lažnih S3, +26 Blatt I (issue #13, 2026-10-14)

**Kontekst:** P56 je dokazal, da 43 povezanih vrstic S3 zapadka (str. 138–139,
»Zusammenstellung der Grundstücke« z lastnim oštevilčenjem 1–100) ni pravih
(median razmerja površin 0.0892 ≪ 3.7188 v S1 — ~42× odmik od 1 Wiener QK;
pass-razhajanje), a je P55 runtime pustil nespremenjen (pini qa-p55). P57 je
obnovil 26 lostBases iz primarnega vira. P58 izvede sanacijo v PRODUKCIJI:
runtime `ps-parcels-geo.json` postane **v2**.

**Sprememba (deterministična, skripta `scripts/p58_ps_parcels_geo_v2.py`):**
- ODSTRANJENIH **43** vrstic str. 138–139 — nabor **bajtno enak** P56
  kontaminacijskemu seznamu (kontrola I1: 7-poljska projekcija
  page/base/owner/kultur/areaQK/areaModern/ratio, sortirano, ==);
- DODANIH **26** vrstic Blatt I (str. 3–4, številke 1–36) iz P57 runtime-a —
  base == P56 lostBases; lat/lng/areaModern/parts **dobesedno** kopirani;
  dodatna polja `blatt`, `source: "P57"`, `readConf` (3/14/9), `anmerkung`;
- vsaka vrstica nosi `series` (BI/S1/S2) in `ambiguous` (base na > 1 strani
  znotraj v2).

**KLJUČNA LASTNOST (dokazana z I3/I9):** pozicije vrstic so deterministične
PER BASE (group_pos = ploščinsko uteženo središče sodobnih parcel številke b),
zato odstranitev/dodatek vrstic NE spremeni nobene pozicije; množica
pozicioniranih števil ostane 800 (−26 lostBases +26 Blatt I = iste številke).
Posledica (merjeno): soslednost bajtno enaka v1 (590 parov / 51.8 m / q25-q75
31.2/91.0 / 89.3 % ≤ 150 m / kontrola 1436.9 m — 27.8×) in S1/S2 conf bajtno
enaka v1 (preracun z pravilom P55: 0 odmikov).

**Dva merjena prinosa:**
1. površinski median **3.6984 → 3.7709** (Δ +4.85 %): v1 vrednost je bila
   UMETNO SNIZANA s 43 lažnimi povezavami z razmerji ~0.09; čista vrednost je
   skladna z neodvisnima merjenjema P56 (3.7394) in P57 (3.7594); kontrola
   (seed 42) 4.0829; pas ±10 %: 17.4 % vs 5.6 %; 1074 parov;
2. per-Blatt dvoumnost na v2: **211 base / 495 vrstic** [~] (P56: 515 čez
   celoten register vključno S3 — številke 1–36 zdaj obstajajo le na Blatt I).

**Rezultat:** 1093 povezanih vrstic (BI 26 / S1 997 / S2 70), 800 pozicioniranih
števil, zaupanje **STRONG 174 / MEDIUM 759 / WEAK 160**; Furkofze 2159/2160
nespremenjeno.

**Integracija:** dokaz v2 `research/issue17/ps-parcels-geo-v2.json` (rowsEvidence
+ v2Delta + invarianti) + runtime v2 `src/data/atlas/ps-parcels-geo.json`
(version 2; v1 dokaz ARHIVIRAN nespremenjen); API `/api/atlas/ps-parcels-geo`
(komentar v2); research.ts `PS_GEO_P55` v2 (version, v2Delta, novi števci,
verdikti z zgodovino v1); kartica P55 v2 (serije + delta chipsi, pošten status
»SANACIJA IZVEDENA v P58«); zapora P56 poštenega statusa (»od P58 SANIRAN v v2«);
sources.ts N083PS opomba P58 (Si+En); README bullet; repo worklog P58.

**QA 61 → 62:**
- `qa-p55-ps-parcels-geo` PREPISAN na v2: pini (1093/1067/26, 800, 38.6 %,
  26/997/70, 174/759/160, readConf 3/14/9, dvoumnost 211/495, −43/+26,
  before 1110/3.6984/171-775-164, površine 3.7709/1074/4.85/4.0829/0.1741/0.0559,
  soslednost 590/51.8/1436.9/0.8932/27.8) + neodvisna preracuna iz vrstic
  (soslednost po mehaniki P55 + per-Blatt dvoumnost) + dve obliki po P53/P57
  lekciji (dokaz v2 `rowsEvidence` v repozitoriju, runtime kopija `rows` v
  produkciji; eksplicitne null/undefined kontrole; dokaz ⊇ runtime bajtno);
- NOVI `qa-p58-ps-parcels-geo-v2`: v1 arhiv nespremenjen (2762/1110,
  spatial 590/51.8/0.8932 — samo repo), runtime version 2, brez vrstic 138–139,
  Blatt I 26 == lostBases P56, serije 997/70, delta == P56 sanitizacija
  (1110→1067), v2 dokaz delta −43/+26, neinvarianca pini;
- `qa-p56-register-topology` nadgrajen na v2 realnost: preracun iz P55 runtime
  v2 — S3 vrstic **0** (sanacija IZVEDENA), Blatt I **26**, sanitirani S1/S2
  **1067**, median S1 3.7188; kontaminacijske vrstice == **v2Delta.removed.
  rowsDetail** bajtno (rowsDetail je del runtime v2Delta → kontrola izvedljiva
  tudi v produkciji brez research/ — P53/P57 lekcija do konca).

**Invarianti I1–I9: PASS** (I1 v1 identiteta + S3 bajtno == P56, I2 Blatt I
dobesedno iz P57, I3 v2 struktura + 0 conf odmikov, I4 površine, I5 soslednost,
I6 determinizem `--check` bajtno, I7 dokaz ⊇ runtime, I8 Furkofze, I9
neinvarianca soslednosti == v1).

**Verifikacija:** `--check` bajtno PASS; tsc 0; ESLint 0; build; standalone
3010 (lekcija: pkill "next-server" po imenu): `/api/qa` **62/62** (qa-p55 v2,
qa-p58, qa-p56 na v2 realnost — vsi PASS); **PROD-SIM (metoda P53/P57 do
konca): build brez research/ → `/api/qa` 62/62 v produkciji obliki** (detail
»produkcija: … kontrola na runtime kopiji«; kontaminacija 43 == rowsDetail iz
RUNTIME — tudi brez research/); brskalniška E2E (agent-browser): persona
Raziskovalec → Raziskave → Prepisi Kurrent → kartica P55 v2 **24/24 ključnih
vrednosti v DOM** (1093, 38.6, Blatt I izven izbora, −43 S3 · +26 BI,
BI 26 · S1 997 · S2 70, STRONG 174 / MEDIUM 759 / WEAK 160, 3.7709, 3.59665,
+4.85, 4.0829, 17.4, 5.6, 590, 51.8, 27.8, 211, 495, SANACIJA IZVEDENA v P58,
P55 v2 header, QA 62/62, Furkofze, skripta p58); screenshot
`/home/z/tmp/p58-card.png`; mobilni 390×844: overflowX 0, footer sticky;
konzola 0 napak / 0 opozorjenj.

**Poštenost:** sanacija se dotakne LE nabora vrstic in števcev — ne pozicij in
ne S1/S2 zaupanj; v1 zgodovina ohranjena (arhiv + v2Delta.before); identifikacija
posamezne parcele ostaja [~]; SHEET_GEOREFS in dokazi P40–P57 nespremenjeni
(lekcija P9).

## §37 — P59: glave listov registra PS ("Nro. des Blattes") — per-Blatt atribucija strani + ločitev dvoumnih base v2 (issue #13, 2026-10-14)

P56 je per-Blatt dvoumnost kvantificiral (515 base na več straneh), a jo je pustil
odprto: »blatt stolpec ~50 % šumen — 4. VLM prehod z pozivo na glave listov ostaja
odprt«. P58 je v2 produkcijo znesla na 211 dvoumnih base / 495 vrstic [~]. P59 izvede
posvečen 4. prehod:

**Metoda (metodika P57, posvečeno glavam):** levi stolpec tabele izrezan iz vseh
135 VAČ posnetkov strani 5–139 (`scripts/p59_fetch_strip.py`: x30–250, 3× Lanczos
q92, manifest s sha256); 2 neodvisna VLM prehoda na stran (`scripts/p59_ps_read_blatt.mjs`,
glm-5v-turbo; poziv z eksplicitnimi Kurrent opozorili — števka 4 ≈ 8, vodilna 1 ozka,
naraščajoče številke); 25 nesoglasij razsodil agent vizualno na 3× izrezih
(hardcoded razlogi, deterministično).

**Ključna odkritja:**

1. **Struktura Blatt:** Blatt I = parcele 1–800 (strani 3–40); prehodna cona 721–800
   nosi popravke I→II (p40 oznake @ r5/r6/r19, p41 'I·II' @ r1, p42 'III' prečrtano +
   'II' @ r18 [~]); Blatt II se začne pri 801 (p43, parcele 801–820). Znotraj II
   območja p72 = Blatt III (1281–1302) — cona 1100–1640 prepletena (p79 1621–1640 →
   p80 1541–1560 padajoče). Lokalne sekcije sredi globalnega teka (26: 161–180 pod I;
   61–62/81/83–87: 161–180 pod II; 88: 601–620; 89–91: 921–960), p101 z ulomki
   (196½, 196¾ — podštevilčene parcele), p93 prehod sekcije sredi strani
   (1901–1907 prečrtano → 1303+).
2. **Stare P38 branje potrjeno šumno:** p12 ditto znamenja prebrana kot 20× 'I';
   p76/p77 'II.' obe prehoda prebrana kot 'III' (zamaj pike); ps-023/024 podvojeni
   razpon (401–420 na obeh — sveže branje p24 = 421–440, oči).
3. **VLM Kurrent pasti (dokumentirane):** 4↔8 (p5: 41–60 prebrano 81–100 v 1. pozivu),
   7→1 (p41: 741–760 → 141–160), odrezane vodilne števke (p76: 1461 → 161);
   parzella razponi svežih branj = nizka zaupanja [~], numeralе = visoka
   (2-prehodno soglasje + arbitraža).
4. **Per-Blatt dvoumnost zdaj MERLJIVA:** od 211 base v2 na več straneh jih 106 sega
   čez ≥2 Blatta (P39: ista številka pod različnima Blattoma = druga parcela);
   **17 ruleCandidate** — baza z TOČNO eno instanco z median razmerjem v [0.8, 1.25]
   (npr. 163: Blatt I @ 7.0 vs Blatt II @ 0.981 ≈ 1 QK) — kandidati za P60 per-Blatt
   atribucijo joina. JOIN V2 NESPREMENJEN (meritve brez prerazporeditev — disciplina
   P56/P58).

**Artefakti:** dokaz `research/issue17/ps-blatt-headers.json` (pageAttribution 137
strani, arbitraža z razlogi, struktura, per-Blatt instance, pageMapDivergences) +
runtime `src/data/atlas/ps-blatt-headers.json`; skripte `scripts/p59_fetch_strip.py`,
`scripts/p59_ps_read_blatt.mjs`, `scripts/p59_ps_blatt_headers.py` (I1–I9, `--check`
bajtno PASS); 270 svežih ps-raw branj `blatt-<page>{,-pass2}.json`; API
`/api/atlas/ps-blatt-headers` (force-static); kartica P59 (Raziskave → Prepisi
Kurrent) + zapora P56 odprte točke; sources.ts N083PS opomba P59 (Si+En).

**Pokritost:** S1 5–127 = 123/123 × 2 prehoda; S2 128–132 + 137 (p137 samo pass1);
133–136 in 138–139 ni svežega branja (VLM kvota 429 — odprto). Blatt I strani 3–4
iz P57 polnega branja (navzkrižje I2: 26 vrstic blatt 'I' == P57 runtime).

**Poštenost:** numeralе visoka zaupanja, parzella razponi nizka (Kurrent pasti —
avtoritativni ostajajo v2/pageMap podatki); sred-stranske numeralе = extras [~];
ruleCandidate = merjen kandidat, ne izvedena atribucija; identifikacija per-Blatt
instanc [~] (strojno branje ni dokazni vir); SHEET_GEOREFS in dokazi P40–P58
nespremenjeni (lekcija P9); P55/P56/P57/P58 runtime nespremenjeni (pini QA).

## §38 — P60: per-Blatt atribucija ruleCandidate base v2 — izvedba P59 pravila pasu (issue #13, 2026-10-14)

**Kontekst:** P59 je meril per-Blatt instancе 211 dvoumnih base v2 in označil 17
ruleCandidate (baza z TOČNO eno instanco z median razmerjem v pasu [0.8, 1.25])
— MERJENO, ne izvedeno. P60 pravilo IZVEDE kot atribucijo, še naprej brez
prerazporeditev joina (disciplina P56/P58/P59).

**Izvedba (skripta `scripts/p60_ps_perblatt_attribution.py`, deterministična,
brez AI ob delovanju, FAIL ob padu I1–I7, `--check` bajtno PASS):**
- vsaka od 17 base dobi `attributedBlatt` = instanca v pasu: **II 12 · I 1 ·
  III 4**, 23 pas-vrstic; primer 163 → Blatt II @ 0.9813 (4 kulture Wiese/
  Prunigad/Weide/Aehn na straneh 61/83/84/86) vs Blatt I @ 7.0 @ p11; 671 edina
  z in-band I; 928/934/939/1831 z in-band III;
- re-izpeljava instanc iz v2 vrstic × P59 pageAttribution == P59 instances
  (I2: rows/pages/median, Δ<1e-9);
- **soslednost-kontrola** per pas-vrstica (sosedi ±1 po vrstnem redu vrstic
  evidence na isti strani): **21/23 OK**; 671@p36 in 934@p99 [~] — prečrtane
  vrstice v registru (strani z vrstnimi vrzelmi), ne protislovje;
- **strukturni prinos:** strani pas-instanc (36, 49, 61, 83–87, 94, 99) nosijo
  **100 % več-stranskih base** — potrditev interpretacije Kultur-Tabellen
  (re-listing parcel po kulturah; p85 = "Wiese und Gfrett" družina za 644–657,
  p99 = "Wiesen" sekcija za 928–939) [~];
- **unit-semantics opomba (merjeno, odprto):** pas pravila ujema modo B
  (ratio ≈ 1, n=62 globalno), NE modo A (≈ 3.59665 = 1 QK → m², n=226) —
  faktor ~3.6 med modama; absolutna korespondenca pas-instanc ni dokazana —
  atribucija = RELATIVNA (najboljše ujemanje med instancami baze) [~].

**I4 (join nespremanjen):** sha256 v2 vhoda pinan v dokazu; izpisi ne vsebujejo
pozicij/površin (kontrola po gradnji: geo polja le v pas-detaljah vrstic kot
kopije vhoda); P55–P59 runtime nespremanjeni (pini QA).

**Artefakti:** dokaz `research/issue17/ps-perblatt-attribution.json` (17 base s
strukturami instanc, pas-detalje s soslednostjo, attrPageStats, unitSemantics)
+ runtime `src/data/atlas/ps-perblatt-attribution.json`; API
`/api/atlas/ps-perblatt-attribution` (force-static); kartica P60 (Raziskave →
Prepisi Kurrent) + zapora P59 točke "kandidat za P60" (→ IZVEDENO); sources.ts
N083PS opomba P60 (Si+En).

**QA 63 → 64:** `qa-p60-perblatt-attribution` — pini (17/23, II 12 · I 1 ·
III 4, soslednost 21/2, moda A 226 / moda B 62, 163 → II @ 0.9813, 671 edina I)
+ NEODVISEN preracun iz v2 runtime vrstic × runtime pageAttribution
(atribucije + mediani + soslednost po vrstnem redu) + dokaz == runtime bajtno;
dve obliki po P53/P57/P58 (produkcija: preracun na runtime kopijah).

**Poštenost:** atribucija je relativna, ne dokazana korespondenca; unit-semantics
mode B ostaja odprto vprašanje (kolonialna merska enota ali delna površina [~]);
P59 pokritost 133–136 + 138–139 še naprej odprta (VLM kvota 429) — atribucija se
razširi ob dokončanju pokritosti; SHEET_GEOREFS in dokazi P40–P59 nespremenjeni.

## §39 — P61: unit-semantics moda B — merjena karakterizacija s permutacijsko kontrolo (issue #13, 2026-10-14)

**Odprta točka P60 #1** ("unit-semantics mode B: kolonialna merska enota ali
delna površina [~]") je **merjeno RAZREŠENA s preusmeritvijo** — deterministična
skripta `scripts/p61_ps_unit_semantics.py` (brez AI ob delovanju; FAIL ob padu
I1–I9; `--check` bajtno PASS: I1 modi == P60 · I2 v2 sinkron · I3 GURS 2117 ·
I4 FNV determinizem · I5 blattDist · I6 bloki · I7 dokaz ⊇ runtime · I8 P59/P60
runtime pini · I9 determinizem).

**Metoda (vse deterministično):**
- pasovi == P60: moda A [3.3, 4.3] n=226 · moda B [0.8, 1.25] n=62 · ostali
  n=800 · brez razmerja n=5 (ratio = areaModern / areaQK; 1 QK = 3.59665 m²);
- **permutacijska kontrola** hipoteze H1 (napačen številčni join P55): točke iz
  determinističnega FNV-1a-32 hash (bajtno enako Python/TS — QA preracun),
  radija 50/100 m, površinski pas ±25 % glede na target = areaQK × 3.59665;
- moda B struktura: 42 strani (5–137), Blatt dist (P59 pageAttribution)
  II 31 · IV 11 · III 9 · I 5 · I·II 1 · null 5, bloki ≥2 sosedenih vrstic
  3/9 (p85 'Wiese und Gfrett' 653–657, p86, p117), base z ≥2 B vrsticami samo 2.

**MERJENI REZULTATI:**
- moda A: real @50 m **0.9248** (209/226) vs perm **0.1637** (37/226) — prava
  parcela (površina ≈ QK×3.6) je tik zraven → ujeta = prava parcela;
- moda B: real @50 m **0.2903** (18/62) vs perm **0.1774** (11/62) — prava
  parcela NI tik zraven → **H1 napačni join ZAVRŽEN** kot glavni mehanizem;
- @100 m base rate raste z gostoto parcel (A perm 0.5221, B perm 0.6129) —
  diskriminator je 50 m (robni primeri varni: najbližja točka meji 0.6 mm);
- H3 delna površina: **NEUPORABNA** (samo 2 base z ≥2 B vrsticami: 163, 176);
- H2 druga enota/konvencija: **OSTAJA [~]** — meritev ujeta na pravo parcelo;
  register nosi številko ≈ m²; identiteta enote ODPRTA (paleografija/dokumenti).

**Implikacija za P60:** pas pravilo [0.8, 1.25] izbere vrstico v konvenciji,
številčno primerljivi s sodobno meritvijo — atribucija smiselna kot RELATIVA;
atribucije P60 in join v2 NESPREMENJENI (I2 sha256 v2 == P60 dokaz; P59/P60
runtime pini — I8 po lekciji P9).

**Artefakti:** dokaz `research/issue17/ps-unit-semantics.json` (metoda, summary,
kontrola, hipoteze, implikacijeP60, gursCompact) + runtime
`src/data/atlas/ps-unit-semantics.json` (kompakt + gursCompact 2117 parcel za
produkcijo preracun); API `/api/atlas/ps-unit-semantics` (force-static); kartica
P61 (Raziskave → Prepisi Kurrent, za P60) + povezava iz P60 unit-semantics
škatlice ("→ P61 merjeno"); sources.ts N083PS opomba P61 (Si+En).

**QA 64 → 65:** `qa-p61-unit-semantics` — pini (modi 226/62/800/5, hits
209/37/220/118 + 18/11/45/38, blattDist, bloki 3/9, multiB 2, hipoteze) +
NEODVISEN preracun: modi iz v2 runtime vrstic + FNV-1a permutacijska kontrola na
runtime gursCompact (Math.imul — bajtno enako Python) + blattDist iz v2 vrstic ×
P59 runtime pageAttribution + dokaz == runtime bajtno; dve obliki po
P53/P57/P58 (produkcija: preracun na runtime kopijah).

**Poštenost:** identiteta enote ostaja ODPRTA [~] (naslednja faza:
paleografija/dokumenti — glave sekcij str. 61–99, pojasnila registra); P59
pokritost 133–136 + 138–139 še naprej odprta (VLM kvota 429); SHEET_GEOREFS in
dokazi P40–P60 nespremenjeni.

## §40 — P62: glave listov registra PS — POLNA pokritost 135/135 × 2 prehoda (issue #13, 2026-10-14)

**Odprta točka P59/P61 #2** ("13 manjkajočih branj: 133–136, 138–139 ×
2 prehoda + p137 pass2 — VLM kvota 429") je **IZPOLNJENA**: kvota premagana,
vseh 13 branj dopolnjenih (`scripts/p59_ps_read_blatt.mjs`, glm-5v-turbo,
skip-existing; surovine VAČ str. 133–139 že prenešene v P60/P61), pokritost
sedaj **135/135 strani × 2 neodvisna prehoda** (+ P57 polno branje str. 3–4).

**Arbitraža novih strani (oči na 3× izrezih + 2-prehodno soglasje; VLM == oči
100 % na vseh 7 straneh):**
- p133 = **V** ('IV.V' @ r1 = korekcija IV→V, 'V' @ r2, 'IV' @ r8 prečrtan [~];
  parcele 2601–2620),
- p134 = **IV** @ r1 + korekcijski zapisi 'II.IV' @ r5/r15, 'III.IV' @ r17
  (passi se razlikujeta le po presledkih); parcele 2621–2640,
- p135 = **IV** @ r1, 'III' @ r2, 'II' @ r12 (padajoče); parcele 2641–2660,
- p136 = **II** @ r1, ditto; parcele 2661–2680,
- p137 = **II** @ r1 + korekcije 'I.II' @ r6, 'I' @ r8 (potrjuje P59 pass1);
  parcele 2681–2700,
- p138 = **None** [?] — tabela skoraj prazna, bledi zapisi neberljivi
  ('T.191'? @ r14, '89'? @ r27),
- p139 = **None** — glava 'Nro. des Hauses.' (hišne številke 41–60 + vsota 82,
  NI numerele Blatt) → P58 open #6.

**STRUKTURNI PRINOS:** konec registra (p133–137) nosi eksplicitne
korekcijske cone IV→V/II (rdeči tuš) — prehodna cona analoška p40/p41/p42
(I→II, 721–800); čez-Blatt base **106 → 110** (+4 iz strani 133–136), 211
multi-page in **17 ruleCandidate NESPREMENJENI** (ruleCandidate razponi 161–1831
izven strani 133–139) → P60 atribucije (II 12 · I 1 · III 4, 23 vrstic) bajtno
nespremenjene. p138/139 nemata vrstic v v2 → I4 null_pages prazna.

**Veriga re-run:** p59 skripta (v2: I1 polna pokritost 135/135 · UNREAD
prazen · I4 brez null; `--check` bajtno PASS) → p60 (`--check` PASS, izhodi
bajtno identični — sha256 nespremenjen) → p61 (I5 blattDist pin: moda B
**II 32 · IV 15 · III 9 · I 5 · I·II 1 · null 0** — 5 null vrstic iz strani
133–136 se razporedi IV +4 / II +1; I8 P59 runtime sha pin posodobljen; P60
runtime pin nespremenjen; `--check` PASS; modi 226/62 in permutacijske kontrole
nespremenjene — ne visijo na blatt).

**QA:** pine posodobljeni (qa-p59: 211/110/17, arbitraža 32, polna pokritost
135/135; qa-p61: blattDist II 32 · IV 15 · null 0) — testi ostajajo 65/65,
vsebina preracunov NEODVISNO potrjena na runtime kopijah.

**Artefakti:** 13 novih ps-raw branj `blatt-{133..139}{,-pass2}.json`;
posodobljeni dokaz+runtime `ps-blatt-headers.json` (pageAttribution 137 strani,
arbitraža 32), `ps-unit-semantics.json`; skripti `p59_ps_blatt_headers.py` (v2)
in `p61_ps_unit_semantics.py` (pini); TS konstante (research.ts) + kartice
(P59/P60/P61 metoda/opombe) + sources.ts N083PS (Si+En).

**Poštenost:** p138 bledi zapisi ostajajo neberljivi [?] (naslednja faza: 6×
izrez ali original scan); p139 → P58 open #6 (Haus Nro.); razlaga korekcijskih
con IV→V/II (reorganizacija listov ali revisija) OSTAJA ODPRTA [~]; join v2 in
SHEET_GEOREFS nespremanjeni (lekcija P9).

## §41 — P63: zaključne strani registra PS (138–139) — Blatt IIb + transkripcija tail tabel (issue #13, 2026-10-14)

**Metoda (3 neodvisni prehodi, 2-od-3 konsenz):** (A) agent-oči na izrezih
3×/4×/5× (6 con p138 + 10 con p139, Lanczos q95); (B) VLM glm-5v-turbo na
polnih izrezih (`p63_ps_read_tail.mjs`, 6 delov); (C) VLM na fokusiranih
izrezih kolon 5× (`p63_ps_read_cols.mjs`, 5 delov) + agent-oči 3. prehod na
desnih kolonah p139. Razhodi → [~] + alternatives (42 flagov). KVOTA VLM
deluje (P62 vzorec).

**Odkritja (MERJENO):**
- **p139 = Blatt IIb** (pod-list, NOV v strukturi registra PS): numerele
  'IIb' @ r1 + ditto (oči 5× + VLM 2-od-3; 'b' [~]); Parzelle 41–60
  (duplikat Blatt I številk pod IIb). **KOREKCIJA**: glava je
  'Nro. des Blattes.' — prejšnja očesna razlaga 'Nro. des Hauses.'
  (P60/P62) = očesna napaka → **P58 open #6 ZAPRT**.
- **Lastninske kolone p139 leva** ('Des Eigenthümers'): Haus Nº rdeče
  (1082, 1030, 998[~], 266, 695, 88, 1048[~], 286[~], 1284[~], 1317[~],
  960, 943, 973[~], 1359, 946, 306, 762, 1484, 145[~], 345[~]);
  **'Vor und Zuname' = rokopisne ŠTEVILKE 62–80** (ne imena; r1 =
  'G. l. fin.'[~] — konskripcija/Einlage? [~]); Dominical (1,1,1,3,1,5,1,1,
  1,1,7[~],7[~],7[~],1,1,1,2,1,5,3), Rustical prazno; Stand + Wohnort rdeče
  (63, 1135, 289[~], 410, 1318, 1560, 384, 1294[~], 901, 324 | 4[~], 1482,
  824, 1082, 1246[~], 789[~], 180, 864[~], 834[~], 1159[~]).
- **p139 desna** ('Des Grundstückes'): Kulturs Gattung 81–100, Flächen
  (N.Oe + QK), Classe 101–120 (r1 z bledim dodatnim zapisom [~]), Ertrag
  fl|kr prazna (r1 '101⁴⁄₅'[~]), Capital fl rdeče (1860, 1146, —, 831, 909,
  982, 1086, 1234, 80, 128, 781, 366, 1149[~], 999[~], 1060, 1513, 649,
  1346, 1046, 584) + kr (Σ=153), Fürtrag 189|1228, vsota 162|1447, robni
  zapisi [~].
- **p138**: leva tabela IZBRISANA (bledi ostanki 'T. 191'/'7. 191'[~] @ r14
  + parzelle 23/24[~], '89'/'86'[~] @ r27; rdeče prečrtani zapisi 18–40 @
  srednja kolona [~]; podglave 'Lotus'/'Lung'/'Al'[~]); desna =
  **'Zusammenstellung der Grundstücke'** (Wiese 1–20, Classe 21–40, vsota
  101|15320 [~], rob 89|78 [~]).
- **Vsote p139**: 82|81 (Dominical/Haus; vsota vidnih Dominical = 32 —
  rekapitulacija čez več strani [~]), 125|183 (Stand/Wohnort), Fürtrag
  189|1228 (prenašanje; QK te strani = 16543 [~]), 162|1447 (Capital) —
  razlaga enot ODPRTA [~].

**Skripta:** `scripts/p63_ps_tail_pages.py` (deterministična, brez AI ob
delovanju, FAIL ob padu I1–I10; `--check` bajtno PASS: I1 pokritost 11/11
tail + 2/2 blatt × 2 prehoda; I2 parzelle 41–60; I3 VorUndZuname 62–80;
I4 IIb konsenz == pageAttribution p59; I5 kultur 81–100 + classe 101–120 +
Fürtrag pini; I6 Capital pini + kr Σ=153; I7 vsote 82|81 + 125|183; I8 p138
ostanki + Zusammenstellung; I9 dokaz ⊇ runtime bajtno; I10 determinizem).
Izhodi: dokaz `research/issue17/ps-tail-pages.json` + runtime
`src/data/atlas/ps-tail-pages.json`.

**Veriga re-run (P63 korekcija @ p59 ARBITRATION: 139 → 'IIb', 138 →
izčrpen opis):** p59 OK (arbitraža 32, soglasje 103; 211/110/17
nespremenjeni — p138/139 brez vrstic v v2) → p60 OK (bajtno identično) →
p61 OK (I8 bhrt_sha pin ea950ce2… → efe39f41…; modi 226/62 + FNV kontrole
nespremanjeni; --check PASS vsi).

**Integracija:** API `/api/atlas/ps-tail-pages` (force-static) + TAIL_P63
(research.ts) + kartica P63 (zavihek Prepisi Kurrent, za P61) + posodobljeni
P59 konstanti (coverage S3, verdicti, next) + sources.ts N083PS opomba P63
(Si+En) + QA 65 → **66** (qa-p63-tail-pages: pini + neodvisen preracun
naraščanj + Capital kr Σ=153 + IIb navzkrižje + dokaz == runtime bajtno;
dve obliki po P53/P57/P58).

**Poštenost:** enote vsot 82|81, 125|183, 162|1447 razlagalno ODPRETE [~];
razlaga števil 62–80 @ 'Vor und Zuname' ODPRTA [~]; p138 bledi zapisi
ostajajo [~]/[?]; join v2 in SHEET_GEOREFS nespremanjeni (lekcija P9);
P55–P60 runtime nespremanjeni (P60 bajtno identičen; I8 pini po lekciji P9).

## §42 — P64: razširitev per-Blatt atribucije na vseh 110 čez-Blatt base — merjena hierarhija pravil (issue #13, 2026-10-14)

**Kontekst:** odprta točka P60/P62 #7 (»razširiti atribucijo na vseh 110
čez-Blatt base«) — predpogoj izpolnjen s polno pokritostjo glav listov
135/135 × 2 (P62/P63). Join v2 ostaja NESPREMENJEN (disciplina
P56/P58/P59) — atribucije so meritve, ne prerazporeditve.

**Metoda (deterministična hierarhija pravil, brez AI ob delovanju):**
- **R1 (pas, P60)** — 17 ruleCandidate base: attributedBlatt = instanca v
  pasu [0.8, 1.25] (moda B), bajtno konsistentno s P60 evidence (I3).
- **R2a (area-dominanca ≥ 0.75)** — dominantni Blatt po Σ areaQK: 53 base
  (II 29 · III 11 · IV 5 · I 4 · V 4).
- **R2b (ena-Blatt-s-površino)** — točno en Blatt nosi vso izmerjeno
  površino: 1 base (1605: II 2688.0 QK @ p78 vs IV @ p93 brez areaQK) +
  flag `areaIncomplete` [~].
- → **71/110 atributiranih** (Blatt II 42 · III 15 · I 5 · IV 5 · V 4).
- **split** — dominantni delež v [0.5, 0.75): 39 base (II 19 · III 9 ·
  IV 6 · V 4 · I 1) z alternativami po deležih — attributedBlatt = null;
  kandidati za lastniško odločitev o per-Blatt SPLIT joinu (npr. 642:
  I 0.5187 (319.0 QK) vs II 0.4813 (296.0 QK) — 2 kulturi, 2 lastnika).
- **fragmented** (< 0.5) — MERJENO 0 primerov.

**Merjene kontrole:**
- **Konsistenca R1↔R2**: za vseh 17 tudi area-dominanca — 15/17 soglasij,
  2 merjeni divergence (930: R1 II vs R2 dom III @ 0.763; 671: R1 I vs
  R2 dom II @ 0.8844) — R1 (moda B pas) ima prednost [~].
- **Občutljivost praga 0.75**: 24 base @ ≥0.9, 45 @ ≥0.8, 53 @ ≥0.75,
  58 @ ≥0.7, 63 @ ≥2/3, 69 @ ≥0.6 (od 92 z izmerjeno površino).
- **Soslednost** relevantnih vrstic (atributirani Blatt / vse za split):
  186/216 ok, 30 flagov (prečrtane vrstice [~]; R1 del 21/23 kot P60).

**Skripta:** `scripts/p64_ps_attribution_ext.py` (deterministična, brez AI
ob delovanju, FAIL ob padu I1–I8; `--check` bajtno PASS: I1 vhodni pini
110/17 + sha256 runtime vhodov (bhrt efe39f41…, p60rt 28465b3e…, v2 ev
ebb8f729… — lekcija P9); I2 re-izpeljava instanc == P59 za vseh 110;
I3 R1 == P60 bajtno; I4 pokritost pravil + distribucije; I5 soslednost
števci; I6 join nespremanjen + brez geo polj (areaQK samo v blattShares/
rows); I7 dokaz ⊇ runtime bajtno; I8 determinizem). Izhodi: dokaz
`research/issue17/ps-attribution-ext.json` (160 KB) + runtime
`src/data/atlas/ps-attribution-ext.json` (77 KB).

**Integracija:** API `/api/atlas/ps-attribution-ext` (force-static) +
ATTR_EXT_P64 (research.ts, z notable primeri 163/930/671/1605/642) +
kartica P64 (zavihek Prepisi Kurrent, za P63) + sources.ts N083PS opomba
P64 (Si+En) + QA 66 → **67** (qa-p64-attribution-ext: pini + NEODVISEN
preracun vseh 110 base — deleže, status, atribucijo iz v2 runtime vrstic ×
pageAttribution P59; R1 == P60 runtime; dokaz == runtime bajtno; dve
obliki po P53/P57/P58).

**Poštenost:** 39 split base ostaja NEATRIBUTIRANIH [~] z alternativami —
odločitev lastnika (#8); 2 R1↔R2 divergenci nerazloženi [~] (moda B vs
area-dominanca); R2b 1605 = areaIncomplete [~] (IV brez areaQK v registru);
strojna atribucija ni dokazni vir; join v2 in SHEET_GEOREFS nespremanjeni
(lekcija P9); P55–P61 runtime nespremanjeni (I1 sha pini).

## §43 — P65: polna per-Blatt atribucija — 101 single-Blatt več-stranskih base, pokritost 211/211 (issue #13, 2026-10-14)

**Odprta točka P64 #3** izpolnjena: 101 base, katerih VSE vrstice nosijo
strani ISTEGA Blatta, dobi ta Blatt kot `attributedBlatt` (status
`R3-single`) — atribucija trivialna in nedvoumna (ni potreben pas, ne
dominanca).

**Merjeno (R3-single):**
- **Distribucija po Blattih**: I 3 · II 26 · III 14 · IV 58 (101 base).
- **Vrstice**: 205 (98 base × 2 vrstici + 3 base × 3 vrstice); vseh 101
  base ima izmerjeno površino (0 brez areaQK).
- **Pokritost več-stranskih base POPOLNA: 211/211** (110 čez-Blatt iz
  P64 + 101 single-Blatt) → skupaj **172 atributiranih**
  (Blatt II 68 · IV 63 · III 29 · I 8 · V 4) + **39 split** z
  alternativami (lastniška odločitev o per-Blatt SPLIT joinu).
- **Polna pokritost registra (kontrolni blok coverage)**: 800 base ×
  1093 vrstic = **589 single-page** (implicitno atributirane prek
  pageAttribution strani: I 145 · I·II 10 · II 183 · III 28 · IV 205 ·
  V 18) + **211 multi-page**; **0 vrstic** brez atribucije strani
  (p138/139 brez vrstic v v2).
- **Soslednost** relevantnih vrstic skupaj **375/425** (flag 50;
  R3 del 189/209 — 20 flagov, prečrtane vrstice [~]; P64 del 186/216
  nespremenjen).

**Konsistenca**: 110 P64 atribucij bajtno nespremenjenih (I3 — deep
equality per base); R3 množica disjunktna od P64 (razčlenitev izčrpna:
multi-page == multi-Blatt ⊔ single-Blatt, I2).

**Skripta:** `scripts/p65_ps_attribution_full.py` (deterministična, brez
AI ob delovanju, FAIL ob padu I1–I8; `--check` bajtno PASS: I1 vhodni
pini 5× sha256 (v2 ev ebb8f729…, bhrt efe39f41…, p60rt 28465b3e…, p64ev
a6f6d8af…, p64rt 7e5ea64a…) + števci 1093/800/211/110/101; I2 razčlenitev
izčrpna + disjunktna (R3: 1 Blatt, pages ≥ 2, 0 null vrstic); I3 P64
podmnožica bajtno (110); I4 pokritost + distribucije; I5 soslednost
(R3 189/20; skupaj 375/50); I6 join nespremanjen + brez geo polj
(areaQK samo v blattShares); I7 dokaz ⊇ runtime bajtno; I8 determinizem).
Izhodi: dokaz `research/issue17/ps-attribution-full.json` + runtime
`src/data/atlas/ps-attribution-full.json` (polni dataset 211 base).

**Integracija:** API `/api/atlas/ps-attribution-full` (force-static) +
ATTR_FULL_P65 (research.ts) + kartica P65 (zavihek Prepisi Kurrent, za
P64) + sources.ts N083PS opomba P65 (Si+En) + QA 67 → **68**
(qa-p65-attribution-full: pini + NEODVISEN preracun 211 multi-page —
razčlenitev, R3 atribucije, deleži, coverage iz v2 runtime vrstic ×
pageAttribution P59; I3 P64 bajtno; dokaz == runtime bajtno; dve obliki
po P53/P57/P58).

**Poštenost:** 39 split base ostaja NEATRIBUTIRANIH [~] z alternativami
— odločitev lastnika o SPLIT joinu; 'I·II' prehodne strani (10
single-page base) razlagalno odprte [~]; strojna atribucija ni dokazni
vir; join v2 in SHEET_GEOREFS nespremanjeni (lekcija P9); P55–P64
runtime nespremanjeni (I1 sha pini).

## §44 — P66: split decision pack — 39 split base, odločitveni paket za per-Blatt SPLIT joina (issue #13, 2026-10-14)

Kandidat #1 iz P65 `next` (odprta točka P64 #8): **P66 NE odloča
namesto lastnika** — MERI in DOKAZUJE dejstva, ki odločitev o per-Blatt
SPLIT joinu podpirajo (deterministično, brez AI ob delovanju; join v2
NESPREMENJEN — disciplina P56/P58/P59/P65).

**Merjeno (39 split base iz P65 runtime, bajtni vir):**
- **Razčlenitev**: vseh 39 base ima TOČNO 2 deleža (blattShares);
  93 vrstic (25 base × 2 + 13 × 3 + 1 × 4); Σ share = 1 (toleranca
  1e-3 — deleži half-up @ 4 decimalki); Σ areaQK per Blatt == Σ
  areaQK vrstic (bajtno).
- **Blatt pari**: I·II 7 · II·III 21 · II·IV 2 · IV·V 9 —
  **37/39 sosednja Blatta**, 2 skoka II·IV (1603, 1604: isti kulturi
  'Acker' + 'Weide und Gfällgut, Laubm.' na obeh Blattih — preveriti
  dednost/preimenovanje).
- **LASTNIŠKA RAZČLENITEV PER BLATT: 39/39 DISJUNKTNI lastniki** —
  vsak split base ima različne lastnike po Blattih (množici
  ownersByBlatt disjunktni) → močan dokaz, da je ista številka pod
  različnima Blattoma **2 RAZLIČNI realni parceli**, ne isti parceli
  prestopa meje; 2–3 edinstvenih lastnikov (25/13/1).
- **Dominantni delež pasovi**: [0.50,0.60) 23 · [0.60,0.70) 11 ·
  [0.70,0.75) 5 (razlog za split: delež < 0.75, R2a ne zadošča).
- **Kulture**: 92 z razčlenitvijo per Blatt (kulturesByBlatt).
- **GEO: 39/39 base nosi VSEH vrstic ENAKO geometrijo joina v2**
  (0 različnih, 0 null) — join v2 je na nivoju številke, zato SPLIT
  join bi zahteval 2 geometriji; števec merjen brez koordinat (I6 —
  brez lat/lng/areaModern/ratio v izpisu).
- **Kakovost**: areaSuspect 0; sosledje split del **82/93**
  (flag 11 — 5 base: 646, 661, 1821, 2141, 2143).

**Konsistenca**: P65 polja 39× bajtno (I3 — deep equality per base:
status, attributedBlatt, blattShares, rowsTotal, pages, kultures,
owners, sosledje); sosledje split del == P65 bajtno (I5).

**Skripta:** `scripts/p66_ps_split_pack.py` (deterministična, brez
AI ob delovanju, FAIL ob padu I1–I8; `--check` bajtno PASS: I1 vhodni
pini 3× sha256 (v2 ev ebb8f729…, P59 ev 95929a2e…, P65 rt 74477ac8…)
+ števci 1093/800/211/39; I2 razčlenitev (39 ⊂ 211; 2 deleža; Σ share
= 1; Σ areaQK == vrstice); I3 P65 polja bajtno (39×); I4 distribucije
(pairs/skip/owners/rel/pasovi/kulture/geo/suspect); I5 sosledje split
del == P65 bajtno (82/93); I6 brez georef polj (lat/lng/areaModern/
ratio) + geoShared samo števec; I7 dokaz ⊇ runtime bajtno; I8
determinizem). Izhodi: dokaz `research/issue17/ps-split-pack.json` +
runtime `src/data/atlas/ps-split-pack.json` (polni dataset 39 base z
per-vrstično razčlenitvijo: page, blatt, parzella, owner, stand,
hausNr, wohnort, kultur, joch, klafter, areaQK, parts, conf, series,
ambiguous + source/readConf/anmerkung ko obstajajo).

**Integracija:** API `/api/atlas/ps-split-pack` (force-static) +
SPLIT_PACK_P66 (research.ts) + kartica P66 (zavihek Prepisi Kurrent,
za P65) + sources.ts N083PS opomba P66 (Si+En) + QA 68 → **69**
(qa-p66-split-pack: pini + NEODVISEN preracun 39 split base iz v2
runtime vrstic × P65 runtime × pageAttribution P59 — blattPair,
ownerRelation, pasovi, geoShared, sosledje; I3 P65 bajtno; dokaz ==
runtime bajtno; dve obliki po P53/P57/P58).

**Poštenost:** odločitev o SPLIT joinu je LASTNIŠKA (2 geometriji;
razdelitev per deleži ali per lastnika) — P66 je samo dokazni vir;
2 skoka II·IV nerazložena [~]; 5 sosledje flagov [~]; strojna
atribucija ni dokazni vir; join v2 in SHEET_GEOREFS nespremanjeni
(lekcija P9); P55–P65 runtime nespremanjeni (I1 sha pini).

## §45 — P67: forenzični paket anomalij — skok II·IV, sosledje flagi, R1↔R2 divergence, univerzalna disjunktnost (issue #13, 2026-10-14)

Kandidati iz P66 `next` #3/#4 + P64/P65 divergence + nova univerzalna
meritev — **štiri dela, deterministično, brez AI ob delovanju; v2 join
NESPREMENJEN** (disciplina P56–P66); očesna verifikacija strani 78/87/93
na 3×–4× izrezih (recept P41/P57) kot neodvisna plast.

**(A) Skok II·IV (1603/1604) = ARTIFAKT DVOJNE KURRENT ZAMENJAVE:**
- **p78** (Blatt II, Bezeichnung "Pod Grabino" — Wüstung): strip 2×
  bajtno **1501–1520**; vrstice 5–14 (1505–1514) rdeče prečrtane
  (opomba obeh prehodov); kontinuiteta p76→p77→p78 =
  1461–1480 → 1481–1500 (strip bajtno) → 1501–1520; karta KO 1544:
  1461–1500 ima 12 poligonov, 1121–1200 (P38-era branja p74/p76/p77)
  PRAZNO; P38 pass1+pass2 = 1601–1620 (napaka 5→6) → v2 1603/1604/1605
  napačno, prave **1503/1504/1505**.
- **p93** (Blatt IV): strip 2× vrstice 11–20 bajtno **1911–1920**,
  vrstice 1–10 garbled 19xx; oči: r1–8 = 1901–1908, prečrtane
  r1–r4/r6–r7, r5 (1905) čista; karta: blok **1901–1907 = TOČNO 7
  poligonov** (= prečrtani blok!) + 1910/1913/1914; P38 pass1 =
  1001–1020 (9→0), pass2 = 1601–1620 (9→6) → prave
  **1903/1904/1905**.
- **p87** (Blatt II): P38 pass1 = 661–680, pass2 = 1681–1700, strip =
  161–180 (odrezane vodilne); oči: r1–8 = **1681–1688** (r5/r7
  prečrtani) → pass2 pravilen; v2 (pass1-vir) 11 vrstic napačno
  (+1020: 661→1681 … 680→1700) in nosi **LAŽNO geometrijo**
  (poligoni 661–680 = Blatt I p36 instance — koordinate bajtno
  identične p36, 11/11 merjeno).
- **Posledice**: 1603/1604 = lažni fuziji II 1503/1504 × IV
  1903/1904 (skok II·IV IZGINE); 1605 = fuzija II 1505 (prečrtan) ×
  IV 1905; 661/671 = lažni fuziji I 661/671 × II 1681/1691 (čez-Blatt
  primera RAZPADETA — 671 ni več R1↔R2 divergenca); p93 (IV) × p98
  (III) nosita ISTI obseg 1901–1920 (disjunktni lastniki — per-Blatt
  primež); karta: 1903/1904/1905 poligoni obstajajo (jugozahodna
  lokacija), 1503–1505 in 1681–1700 NE; 16xx poligoni (1603,
  1604/1-3, 1605) na tretji lokaciji — v2 jih je lažno pripisal
  fuzijam.
- **Renumerifikacija 17 preslikav** (p78 3×, p93 3×, p87 11×):
  kolizije 0 (1503–1505, 1904, 1681–1700 proste; 1903/1905 samo p98);
  projekcija (številčenjski nivo): base 800→802, multi-page 211→208,
  čez-Blatt 110→107, R3-single 101; 1903 pas split 0.7081 [~], 1905
  R2b [~]; runtime −14 vrstic brez geometrije; p93 3× re-claim
  (1904 čisto, 1903/1905 konflikt z III@p98 [~]) — **izvedba P68**
  (lastniška odločitev + veriga re-run).

**(B) 5 sosledje flagov (646, 661, 1821, 2141, 2143; 11 vrstic) =
ARTEFAKT OBSEGA JOINA:** manjkajoči sosedje obstajajo v registru
(P38 z imeni: 645 'Ulrich Franz', 647 'Gemeinde', 662 'Mülley Franzl',
1822 'Büller Lorenz', 1823 'Gavčnik Miha', 1824 'Gavčnik Gregor',
2142 'Häupler Martin', 2144–2147 …), a brez poligonov v karti → izpad
iz v2 (matchedShare 38.6 %); 1821/2141/661 so začetki strani (1820 p63
in 2140 p109 IMATA poligona in sta v v2 — na prejšnji strani, per-page
kontrola je ne vidi); M per flag ne-prazna ∧ vsi M brez poligona;
**11/11 razloženih, 0 anomalij registra**.

**(C) R1↔R2 divergenci:** **671 RAZREŠENA** — ni divergencia: II
instanca @p87 je pravzaprap 1691 (renumerifikacija p87); 671 ostane
I-only @p36; **930 ostaja [~]** z merjenim dokazom: moda B pas
✓@p49 (1.2241) ✗@p99 (0.3802), disjunktna lastnika ('Zehorn' vs
'Wiesen'), sosedi ±1 na OBEH straneh (929/931 v v2 p49 IN p99),
pageMap blok 921–940: karta 9 poligonov (mehka podpora).

**(D) UNIVERZALNA DISJUNKTNOST:** lastniki per Blatt DISJUNKTNI za
**VSEH 110 čez-Blatt več-stranskih base** (110/110; rekurzivno iz
v2 × P59 pageAttribution; 0 prehodnih strani '·' v množici; 39 split
polja bajtno == P66 I6-kontrola; 71 atributiranih 71/71) → per-Blatt
številčenje: ista številka pod različnima Blattoma = 2 RAZLIČNI
realni parceli; atribucija (R1/R2a/R2b) je dodelitev geometrije
instanci, ne identiteta parcele [~].

**Skripta:** `scripts/p67_ps_anomaly_forensics.py` (deterministična,
brez AI ob delovanju, FAIL ob padu I1–I8; `--check` bajtno PASS: I1
vhodni pini 28× sha256 (v2 ev ebb8f729…, P59 ev 95929a2e…, P65 rt
74477ac8…, P66 rt 77337aff…, topo 2fddc76f…, PS-full-v2 81f140e9…,
karta fee91fca… + 21 dokaznih branja) + števci
1093/800/211/39/110/101; I2/A dokazi p78/p93/p87 (strip 2× bajtno;
arbitražni nizi '1501–1520'/'1901–1907 prečrtano'; karta 1901–1907 ⊆
poligoni / 1503–1505, 1681–1700, 1121–1200 ∅ / 1461–1500 ≥ 10);
I3/A kolizije 0 + lažna geometrija p87 11/11; I4/B flagi == P65
bajtno (5 base, 11 vrstic) + M ne-prazna ∧ brez poligonov + 1820/2140
v v2; I5/C 671 R1/I + 930 R1/II + moda B pas + sosedi ±1; I6/D
110/110 disjoint + 39 split == P66 bajtno + 0 prehodnih strani + brez
lat/lng/areaModern/ratio; I7 dokaz ⊇ runtime bajtno; I8
determinizem). Izhodi: dokaz `research/issue17/ps-anomaly-forensics.json`
+ runtime `src/data/atlas/ps-anomaly-forensics.json` (4 dela z
dokaznimi sekcijami, renumerifikacijsko specifikacijo 17 preslikav in
projekcijo).

**Integracija:** API `/api/atlas/ps-anomaly-forensics` (force-static) +
ANOM_FORENSICS_P67 (research.ts) + kartica P67 (zavihek Prepisi
Kurrent, za P66) + sources.ts N083PS opomba P67 (Si+En) + README
bullet + ta §45.

**QA 69 → 70:** `qa-p67-anomaly-forensics` — pini (17/0, fuzije 5,
flagi 11/11, disjunktnost 110/110, projekcija 802/208/107) +
NEODVISEN preracun iz runtime kopij (fuzije 1603/1604/1605 @78+93,
661/671 @36+87; disjunktnost 110/110 iz v2 × pageAttribution; 39
split ownerRelation == P66 bajtno) + dokaz == runtime bajtno; dve
obliki po P53/P57/P58 (produkcija: preracun na runtime kopijah).

**Poštenost:** renumerifikacija NI izvedena — 17 preslikav je
SPECIFIKACIJA za P68 (lastniška odločitev + veriga re-run P59–P66 s
posodobljenimi pini); 930 ostaja [~]; strojna forenzika ni dokazni
vir; join v2 in SHEET_GEOREFS nespremanjeni (lekcija P9); P55–P66
runtime nespremanjeni (I1 sha pini); očesna verifikacija (strani
78/87/93) dokumentirana v repovem worklogu (Task 33).

## §46 — P69: sistemski pregled P38 pass1 slojev (cona p73–93 + p99) — 2026-10-15

**Vprašanje (odprta točka P68 next #3):** so preostali P38 pass1 sloji
(p74/p76/p77 "1121–1200 brez kartnih poligonov [~]"; p88 "721–740 [~]")
realni ali artefakti?

**Metoda (P67 recept):** očesna forenzika — 4× široki izrezi x=0..430
(`scripts/p69_fetch_zone.py`, popravi P59 past odrezanih vodilnih
številk) + 7×–8× zoomi dvomljivih vrstic + kontinuiteta + kartni
poligoni + P56 annRecords zamiki + Blatt stolpec + hišne številke +
površinska razmerja. 22 strani (p73–93 + kolizijska p99), 166 v3
vrstic klasificiranih.

**Ugotovitve:**

- **(A) Stari sloji = sistematski digitalni artefakti** (12 strani):
  p74 1121–1140 je pravzaprap **1421–1440** (4→1; annRecords
  "auf transportirt 1844" na 1135/1136/1138 = prečrtane
  1435/1436/1438 — neodvisen dokaz zamika), p76 1161–1181 = 1461–1480,
  p77 1181–1200 = 1481–1500 (4→1), p79 1821–1842 = 1521–1540 (5→8),
  p80/p81 16xx = 15xx (5→6), p82 1681–1700 = 1581–1600 (pass1 je bil
  PRAVILEN — join je vzel p2 → 16 vrstic z poligoni IZGUBLJENIH),
  p88 721–740 = 601–620 (+120 celostranski; annRecords
  "Aufsufgefüllt 1811/1841/1831"), p89/p90 19xx = 9xx (fantom-1
  ±1000; pass1 pravilen), p92 990–1008 = 981–1000 (+9 zamik; P59
  arbitraža 1881–1900 = isti 9→19 artefakt), p99 921–940 = 1921–1940
  (−1000; zrcalni primer p89, Blatt III razrešuje). Kontinuiteta:
  p73 (1101–20) → p74 (1421–40) → … → p82 (1581–1600); p91 (961–80) →
  p92 (981–1000); p49–52 = 921–1000.
- **(B) Lokalne sekcije** (p83, p84, p85, p86, p88; 56 v3 vrstic):
  pisane številke 161–180 (×3 strani) / 641–660 / 601–620 trčijo z
  Blatt I KO-globalnimi — dokazano RAZLIČNE parcele (hiše: p85 r641
  Hi16 vs p35 r641 Hi68; lastniki brez prekrivanja s p10/p11;
  kulture Alm/Wein/Dingf./Ainze; Σ ratio 161 = 235.65× proti čistim
  1441 = 1.09; p83 = dvojni blok 161–170 ×2 [~], karta 261–270
  prazna). 56 vrstic = dokazane lažne fuzije na Blatt I poligone.
- **(C) Spec P70:** 77 renum preslikav (0 kolizij) + 98 rejoin
  kandidatov; izvedba = veriga re-run P59–P68 s posodobljenimi pini.
- **(D) 117 prečrtanih vrstic** (rdeči tuš) zabeleženih; ne
  izključujejo iz joina (flag).

**Poštenost:** join v3 NESPREMENJEN (disciplina P56–P68); renum/rejoin
= SPEC (lastniška odločitev + izvedba P70); odločitev o 56 sekijskih
vrsticah (exclude / per-Blatt instance) = LASTNIKA; p83 blok B ostaja
[~] (8× nebere zanesljivo); očesni verdikti dokumentirani v repovem
worklogu (Task 35). Strojno berljivo: research/issue17/ps-pass1-layers.json
+ runtime src/data/atlas/ps-pass1-layers.json (skripta
scripts/p69_ps_pass1_layers.py, I1–I6, --check bajtno PASS).

## §47 — P70: izvedba P69 specifikacije (77 renum + 95 rejoin → v4) — 2026-10-15

**Naloga:** P69 specifikacija (§46: 77 renum preslikav + 98 rejoin kandidatov)
IZVEDENA kot mehanski izvod — deterministična skripta, brez AI ob delovanju.

**Izvedba (`scripts/p70_ps_v4_rejoin.py`, invarianti I1–I9, `--check` bajtno
PASS):**

- **77 renum preslikav** bajtno == P69 renumSpec (p74 2× +300, p79 17× −300,
  p80 8× −100, p81 2× −100, p89 9× −1000, p90 15× −1000, p92 9× −9,
  p99 15× +1000); preslikani ključi ∈ v3 točno 77; **parzella ostaja
  originalno branje** (sanacija le na join ključu — disciplina P68).
- **95 rejoin vrstic** iz starih P38 slojev (kandidati == P69 rejoinSpec,
  98, bajtno; − 3 brez vira): p74 14 · p76 18 · p77 2 · p78 10 · p79 2 ·
  p80 3 · p81 3 · p82 16 · p89 9 · p90 2 · p92 1 · p93 12 · p99 3.
  Sloji po strani (dokumentirani po P69 perPage artefaktih + P38 izbiri +
  pass1-je-pravilen opombah): pass1-pravilen p74 (+300)/p82/p89/p90/p91,
  p87 pass3→pass1, P38 izbira sicer. P55 normalizacija (areaQK = j·1600+k,
  wohnort propagate), group_pos poligoni.
- **3 kandidati brez vira [~]:** p80 1541–1543 — p80 p1 sloj = odrez blok
  62–81 (identiteta [~], P69 ne klasificira); kandidatov se ne izmišljuje.
- **29 preslikanih izpada** (base brez PF poligona — removedRows
  dokumentirane po straneh v dokazu).
- **33 fuzij isti-Blatt:** register vsebuje 921–1000 v dveh blokih
  (p49–52 »glavni tek« + p89–92 »stolpec«; P69) — vse p89/p90/p92
  preslikane + nove base instancess fuzirane na p49/p50/p52 poligone
  (različni lastniki: npr. 922 = Dragasch Jane p49 × Lauffstätten Nikl
  p89). SPLIT join odločitev = LASTNIKA.
- **56 sekijskih vrstic (p83–86, p88) NESPREMENJENIH** — exclude ali
  per-Blatt instance = lastniška odločitev (šteje kot lastniška točka #1
  za naslednjo fazo).

**Meritve v4:** 1145 vrstic (41.5 %) / 878 base / 215 multi-page /
79 cross-Blatt; area median 3.8843 ≈ 1 Wiener QK 3.59665 m² (Δ +8.0 %,
kontrola seed 42: 4.2701); soslednost 654 parov / 52.0 m / 27.6×
(kontrola 1434.0 m); zaupanje STRONG 188 / MEDIUM 797 / WEAK 160;
dvoumnost 215 base / 475 vrstic [~]; group-derived spremembe
(ambiguous 93, conf 15) dokumentirane; nespremenjene vrstice bajtno == v3
(959; lekcija P9).

**Veriga re-run:** P59–P67 skripte --check PASS (neodvisne od v4);
P69 klasifikacija **zamrznjena na v3 dokaz** (`ps-parcels-geo-v3.json`
rowsEvidence — skripta preveri runtime verzijo in pada na arhiv, klasifikacija
bajtno nespremenjena 166/33/77/56/77/98/117).

**Integracija:** dokaz `research/issue17/ps-parcels-geo-v4.json` + runtime
`src/data/atlas/ps-parcels-geo.json` (version 4) + API
`/api/atlas/ps-parcels-geo` (komentar v4) + PS_GEO_P55 (v4: join/area/
spatial/v4Delta/verdict) + V4_REJOIN_P70 (research.ts) + kartica P70
(museum-research, za P69) + P69 kartica pošten status ("SPEC izvedena") +
sources.ts N083PS P70 (Si+En) + README bullet.

**QA 72 → 73/73** (nova qa-p70: pini 77/95/29/32 + neodvisen preracun
na runtime v4 — 1145 vrstic, serije 26/1049/70, zaupanje 188/797/160,
preslikave parzella == original, fuzije 32 iz vrstic, sekcije 56,
area median 3.8843; dokaz == runtime bajtno; dve obliki po P53/P57/P58;
qa-p55/p58 posodobljeni na v4 realnost, qa-p68 preracun na v4 runtime
s parzello == originalno branje).

**Poštenost:** v4 = mehanski izvod P69 specifikacije (nič ni bilo ugibano:
preslikave bajtno == P69, kandidati bajtno == P69, sloji dokumentirani,
kolizije merjene, brez vira [~] dokumentirane); odločitvi o 56 sekijskih
vrsticah in SPLIT joinu = LASTNIKA. Strojno berljivo:
research/issue17/ps-parcels-geo-v4.json + runtime
src/data/atlas/ps-parcels-geo.json (skripta scripts/p70_ps_v4_rejoin.py,
I1–I9, --check bajtno PASS).

## §48 — P71: korekcije v4 (C1 sekcije exclude + C2 p93 reverzija → v5) — 2026-10-15

**Sprožilec:** lastniški ukaz (odprti točki P70 ① in P69 openQuestions #3/p93).
**Metoda:** očesna forenzika po P67 receptu (izrezi VAČ 3× + zoomi 10–12×),
notranja glifna kontrola, deterministično, brez AI ob delovanju.

### C1 — 56 sekijskih vrstic (p83–86, p88) EXCLUDE iz joina

- Odločitev: LASTNIK (P71) — opcija "exclude" iz P69 sectionClass.options;
  per-Blatt instance (P60 moda B / PF protokol) ostaja odprta lastniška
  točka.
- Dokaz (P69, nespremenjen): Σ ratio 161 = 235.65×, 162 = 31.39×,
  175 = 19.92×, 990 = 8.99× proti čistim 1441 = 1.09; lastniško prekrivanje
  p83/p84 vs p11 = 0; hiše p85 641/646/655 = 16/22/7 ≠ p35 68/23/26.
- Izvedba: 56 vrstic (p83 13 · p84 12 · p85 14 · p86 14 · p88 3) bajtno ==
  P69 sectionClass; izpadle iz runtime joina, ostanejo v registru
  (dokaz: corrections.C1.excludedRows); **invarianta I4: 0 poligonov ostane
  praznih** — vsi 56 base imajo legitimne druge zahtevalce (p11/p61, p33,
  p35, p52 …).

### C2 — p93 reverzija: P68 renum 160x→190x (+300) = NAPAKA

- **Glifna forenzika (notranja kontrola, odločilno):** p93 vrstica 9 =
  "1609" in vrstica 19 = "1619" — gotova ZADNJA števka 9 (zaprt zgornji
  lok + rep pod osnovnico) je vidno RAZLIČNA od srednje števke (spodnja
  zanka, odprt vrh, brez repa = 6); isti pisar, ista stran. Enako r5
  "1605", r16 "1616", r20 "1620". Kontrole: p98 "1916" @12× (9 in 6 v
  istem številu = dve različni črki), p92 981–983 (P69-verificirane 9 =
  isti glif kot p98). Izrezi: research/issue17/p93-forensics/ (7 PNG).
- **Ovrga P67 trditvi:** "9→6/9→0 — P67 že dokazal" za p93 = napačno
  prenesena (p93 NI bil v P67 očesni coni p74–92/p99; artefakt realen na
  drugih straneh). P69 eyesVerdicts p93 ("true [1901,1920]") je bil
  nikoli očesno verificiran — utemeljen le na karta-fit hevristiki.
- **Neodvisni viri:** annRecords anotatorja (9 zapisov referencira
  1601, 1602, 1603, 1604, 1606, 1607, 1613, 1614, 1619 — "Durch Theilung
  im 1824", "trifft Gültley 9.", "1870. 8-1117"); pageMap P56
  (numMin/numMax 1601–1620); P38 pass2 (1601–1620); monotoničnost
  (vrstica N = 1600+N, 20/20).
- Izvedba: 15 vrstic base := parzella (reverz na originalno branje);
  PF ujemanja == {1603, 1604, 1605} (invarianta I3 — napoved izpolnjena);
  12 izpadlih (base brez PF poligona — 1601–1620 večinoma odsotnih v
  sodobnem k.o. 1544); PF 1901–1920 izgubi lažne dvojne zahtevke p93
  (ostane p98 III); PF 1904/1906 izpadeta iz base seta (dokumentirana
  praznina); PF 1603/1604/1605 dobijo prve prave vrstice.

### Meritve v5 (runtime src/data/atlas/ps-parcels-geo.json, version 5)

- rows 1145 → **1077** (39.0 % izbire 2762) / bases 878 → **879** /
  multi-page 215 → **184** / cross-Blatt 79 → **48**;
- area median **3.9052** ≈ 1 Wiener QK 3.59665 m² (Δ +8.58 %, kontrola
  seed 42 = 4.2304); soslednost **652 parov / 51.8 m / 25.5×** (kontrola
  1320.7 m); zaupanje **183/745/149**; dvoumnost **184/373** [~];
- nespremenjene vrstice bajtno == v4 (1041 + 33 group-derived; lekcija P9).

### Veriga in QA

- Skripta scripts/p71_ps_v5_sections_p93.py (I1–I9, --check bajtno PASS;
  pini v4 57ed1b0d…, P69 99962e24…, P59 650f13dc…, P56 2fddc76f…,
  PARCELS fee91fca…). Veriga: P59–P67 --check PASS; P69 zamrznjen (v3
  dokaz; pini.v3 zamrznjen iz obstoječega dokaza — P70 recept); P70
  --check PASS (dokaz bajtno; runtime nasledstvo v5 deklarirano).
  Prejšnje faze: p55/p57/p58/p68 --check MISMATCH (znano stanje od P70 —
  runtime verzija napredovala; pokrito z QA "dve obliki").
- QA 73 → **74/74** (nova qa-p71-v5-corrections: pini v5Delta 56/15/68 +
  before/after + neodvisen preracun — 0 sekijskih vrstic, p93 base ==
  parzella 3/3 {1603,1604,1605}, 1904/1906 izpad, 1603/1604/1605 prisotni,
  area median 3.9052; dokaz == runtime bajtno; dve obliki; qa-p55/p58 na
  v5 realnost; qa-p70 repo oblika na zamrznjenem v4 dokazu + produkcija
  deklaracija nasledstva).

### Odprte praznine (dokumentirane, brez trditve o vzroku [~])

- PF 1644–1655 (8 poligonov), 1673/1679 (2), 1842–1860 (13), 1904/1906
  (2): brez registrskih strani/zahtevkov — pageMap pokritost preverjena;
  možnosti (Abschreibung, prelom številčenja) = odprto.
- P56 modernVoid 2507–2607 (87 dodatkov S2) — nespremenjeno.
- LASTNIŠKO (naslednja faza): ① per-Blatt instance 56 sekcij, ② SPLIT
  joina (33 fuzij isti-Blatt + cross-Blatt), ③ praznine.

**Poštenost:** C1/C2 odstranjujeta LE dokumentirane lažne zahtevke — noben
nov podatek ni izmišljen. Strojno berljivo:
research/issue17/ps-parcels-geo-v5.json + runtime
src/data/atlas/ps-parcels-geo.json (skripta
scripts/p71_ps_v5_sections_p93.py, I1–I9, --check bajtno PASS).

## §49 — P72: dvojnosti registra — 135 isti-Blatt dual base (odločitveni paket) — 2026-10-15

**Sprožilec:** ad-hoc forenzika faze — P70 33 kolizij (p49/89 × 15, p50/90 × 10,
p52/92 × 8) niso izoliran pojav 921–1000, ampak STRUKTURNI pojav celega
registra. **Metoda:** odločitveni paket po P66 vzorcu (MERI in DOKAZUJE,
NE odloča namesto lastnika; P70 »SPLIT = LASTNIKA«); deterministično, brez
AI ob delovanju; v5 join NESPREMENJEN.

### Definicija dual base (pravilo paketa)

- base z ≥ 2 vrsticami na ≥ 2 straneh **ISTEGA Blatta**, kjer so množice
  lastnikov med straneh **DISJUNKTNE** (brez skupnega lastnika);
  blockA = min stran paru (»glavni tek«), blockB = ostale (»drugi blok«).
- 2 nearDual base (2080, 2081) z disjunktnimi lastniki, kjer ena stran brez
  lastnikov — konservativno IZKLJUČENE iz dual (opcija A jih NE izpada).

### Merjeno (135 dual base iz v5 rowsEvidence × P59 pageAttribution × P56 pageMap)

- **274 vrstic** (2 tri-zapisni: (95,100,101) in (105,106,121));
  lastniki med straneh DISJUNKTNI **135/135**;
- hišne številke **RAZLIČNE 130/135** (5 brez hn na eni strani; 0 isti);
  kulture **124 različne / 11 prekrivanj**;
- stranski pari delijo iste številčne razpone po **P56 pageMap**
  (p23/p24 = 401–420 obe; p51/p91 = 961–980 obe; p103/p118 = 2001–2020 obe …)
  z odmiki po blokih konsistentnimi (**40 × 44 · 15 × 49 · 5 × 29 · 1 × 13**;
  2 triple gapi 6/16) = **DVOJNI ZAPIS iste serije v dveh blokih registra**;
- Σ areaQK blok A **128 125** / blok B **145 057** QK;
- **P70 33 kolizij = PODMNOŽICA** + 11 starih p51×p91 (v2 era) +
  **91 dozdaj neopaženih** — v4/v5 join teh 135 base FUZIRA dve realni
  parceli pod eno številko.

### Opcija A predračun (drop drugi-blok vrstic po C1 vzorcu)

- drop **137** vrstic (vrstice ostanejo v registru, izpadajo iz joina;
  keep = min stran), **0 base brez vrstic**, rows **1077 → 939**,
  multi **184 → 50**, cross **48** nespremenjen.

### Opcije in odločitev

- **A** (exclude drugi blok po C1 vzorcu) — pripravljeno (ob odobritvi v6);
- **B** (per-page instance) — zahteva georef Blattnih kart
  (Franciscejski kataster I–V) — ločen podprojekt [~];
- **C** (re-renum) — neodločljivo (pageMap razponi prekrivajo);
- **Odločitev: LASTNIK** (P70 »SPLIT = LASTNIKA«; cross-Blatt SPLIT iz
  P66 pack ostaja ločena lastniška odločitev — 36 base, deleži [0.5,0.75)).

### Skripta, invarianti in QA

- Skripta scripts/p72_ps_dual_pack.py (I1–I9, `--check` bajtno PASS; pini
  v4 57ed1b0d…, v5 6c96210d…, P59 650f13dc…, P56 2fddc76f…, v5 runtime
  0b5e8bf7…; I9 v5 runtime join NESPREMENJEN — sha256 pin).
- Dokaz research/issue17/ps-dual-occurrence-pack.json (bases 135 ×
  per-base forenzika; brez georef polj — I6) + runtime
  src/data/atlas/ps-dual-occurrence-pack.json (bajtna projekcija — I7).
- QA 74 → **75/75** (nova qa-p72-dual-pack: pini + NEODVISEN preracun
  dual seta iz v5 runtime vrstic v OBEH oblikah — dual 135, nearDual 2,
  vrstice 274, triples 2, lastniki 135/135, hn/kulture/odmiki/pari == pin,
  Σ areaQK 128 125/145 057, opcija A 137/939/879/0/50/48, P70 33 ⊂ dual,
  p51×p91 11 ločenih od P70, novih 91; repo dodaja dokaz == runtime bajtno).

**Poštenost:** paket NE odloča namesto lastnika — opcije so dokumentirane z
merjenimi posledicami; v5 runtime join NESPREMENJEN. Strojno berljivo:
research/issue17/ps-dual-occurrence-pack.json + runtime
src/data/atlas/ps-dual-occurrence-pack.json (skripta
scripts/p72_ps_dual_pack.py, I1–I9, `--check` bajtno PASS).

## §50 — P73: isti-Blatt SPLIT — opcija A (v6) — 2026-10-15

**Sprožilec:** lastniška odločitev (soglasje 2026-10-15) po P72 dual pack —
opcija A (exclude drugi blok po C1 vzorcu) izvedena kot korekcija C3.
**Metoda:** deterministično, brez AI ob delovanju; drop samo odstranjuje
(P9: ohranjene vrstice brez group-derived sprememb bajtno == v5; v5 arhiviran
v dokazu — nasledstvo deklarirano z v5Delta + v6Delta).

### Definicija (drop pravilo)

- dual set = **135 base** iz P72 dual pack: base z ≥ 2 vrsticami na ≥ 2
  straneh **ISTEGA Blatta**, množice lastnikov med straneh **DISJUNKTNE**
  (274 vrstic; 2 tri-zapisni (95,100,101)/(105,106,121)).
- drop = (page, base) kombinacije, kjer page ≠ min strani dual seta
  (**drugi blok**); **keep = min stran** (»glavni tek«) — 137 kombinacij =
  **138 vrstic** (1 kombinacija ima 2 vrstici: (119, 2037)).
- vrstice ostanejo v REGISTRU (dokaz removedRows), izpadajo iz runtime
  joina (brez geometrije); nearDual **2080/2081 ostanejo** (4 vrstice —
  opcija A jih NE izpada).

### Merjeno (v6)

- **939 vrstic** (34.0 % izbire 2762) / **879 base** / multi-page
  **184 → 50** / cross-Blatt **48** (nespremenjen);
- serije **S1 847 / S2 66 / BI 26**; zaupanje **STRONG 174 / MEDIUM 629 /
  WEAK 136** (conf 0 sprememb — geografija nedeprava);
- dvoumnost **50 base / 100 vrstic** (ambiguous prekalkuliran po P55
  metodi; **135 True→False** — dual base zdaj enostranske);
- **P70 33 kolizij = PODMNOŽICA** dropa (drugi blok: p89 × 15, p90 × 10,
  p92 × 8); **0 base brez vrstic** (lost 0);
- removedByPage: {8: 1, 24: 2, 73: 3, 89: 15, 90: 10, 91: 11, 92: 8,
  100: 14, 101: 16, 106: 2, 114: 3, 118: 18, 119: 18, 121: 12, 123: 1,
  135: 4} = 138;
- **areaProof**: 919 parov, median **3.8941** ≈ 1 Wiener QK 3.59665 m²
  (Δ **+8.27 %**, kontrola seed 42 = 4.5766; tight 186 = 0.2024);
- **spatialProof** NESPREMENJEN: 652 parov / 51.8 m / 25.5× (share150
  0.9049).

### Nasledstvena disciplina

- v5 arhiviran nespremenjen (research/issue17/ps-parcels-geo-v5.json);
  runtime nosi **v5Delta** (56/15/68, before 1145/878/215/79, after
  1077/879/184/48) **+ v6Delta** (135/137/138, before 1077/879/184/48,
  after 939/879/50/48) = zgodovina nasledstva;
- veriga: P71/P72 skripti z nasledstvenima vejama (--check PASS; disk
  runtime version ≥ 6 + v6Delta 137/138); P69 zamrznjen; P70/P71/P72
  dokazi nespremenjeni (lekcija P9).

### Skripta, invarianti in QA

- Skripta scripts/p73_ps_v6_split_a.py (I1–I8, `--check` bajtno PASS;
  pini v5 6c96210d…, P72 dual pack 0922a701…, P59 650f13dc…, P56
  2fddc76f…, PARCELS fee91fca…; v5 runtime nasledstvena veja).
- Dokaz research/issue17/ps-parcels-geo-v6.json (corrections C3 +
  removedRows 138 + rowsEvidence 939) + runtime
  src/data/atlas/ps-parcels-geo.json (version 6; I7 dokaz ⊇ runtime
  bajtno).
- QA 75 → **76/76** (nova qa-p73-v6-split: TS pini na SPLIT_OPTION_A_P73
  + CELOVEN neodvisen preracun iz runtime datotek — dual set 135 iz dual
  pack runtime vrstic × P59, drop 137 = 138 vrstic, nil-claim (0 drop
  kombinacij v v6), vrstice 939, dual-base 1-stran 135/135, lost 0,
  nearDual 2080/2081 = 4 vrstice, dvoumnost 50/100 z zastavicami,
  P70 p89/90/92 = 0, conf 174/629/136, serije 847/66/26, area preracun
  919/3.8941, sosledje 652; repo dodaja dokaz == runtime bajtno +
  removedRows == drop set + v5 nasledstvo (1077 − 138 = 939, vrstni red
  ohranjen, edina sprememba ambiguous 135 True→False); dve obliki).
- Posodobljene kontrole na v6 realnost (dve obliki): qa-p55/p58 (pini v6
  939/879/50/48, area 3.8941), qa-p70 (v6Delta nasledstvo), qa-p71
  (v6Delta + v5Delta arhiv + nasledstvo ključev), qa-p72 (preracun dual
  seta iz dual pack runtime vrstic + nil-claim; opcija A == izvedba
  939/0/50/48), qa-p68 (nasledstvena veja; multi 50 v v6 veji) +
  produkcijske veje qa-p56/p59/p60/p61/p65 (v6 pine: S1/S2 913, multi
  50, R3 2, single-page 829 …).

**Poštenost:** C3 odstranjuje LE lažne fuzije (dvojni zapis) — noben nov
podatek ni izmišljen; vrstice ostanejo v registru brez geometrije;
conf 0 sprememb (geografija nedeprava). Strojno berljivo:
research/issue17/ps-parcels-geo-v6.json + runtime
src/data/atlas/ps-parcels-geo.json (skripta
scripts/p73_ps_v6_split_a.py, I1–I8, `--check` bajtno PASS).

## §51 — P74: cross-Blatt dvojnosti registra — 48 čez-Blatt base (odločitveni paket) — 2026-10-15

**Sprožilec:** odprta točka P73 ① (cross-Blatt SPLIT P66 pack) — P66 vzorec
re-izpeljan iz v6 univerzuma; vzorec P66/P72: **NE odloča namesto lastnika —
MERI in DOKAZUJE** (deterministično, brez AI ob delovanju); **v6 join
NESPREMENJEN** (disciplina P56–P73; sha256 pin I9 na v6 runtime).

### Definicija (cross pravilo)

- cross set = base z vrsticami na ≥ 2 **RAZLIČNIH Blattih** (P59
  pageAttribution) — 48 base / 96 vrstic; točno **1 vrstica per Blatt
  48/48** (per-Blatt numeracija).
- ista številka pod dvema **sosednjima** Blattoma = 2 RAZLIČNI realni
  parceli, ker se numeracija per Blatt PONOVI — dokaz: **pageMap
  prekrivanja razponov parov 48/48** po P56 (p11 I 161–183 / p61 II
  161–180; p64 II 1821–1840 / p94 III 1821–1841; p110 IV 2141–2160 /
  p125 V 2141–2160).

### Merjeno (v6 univerzum)

- **lastniki med Blatti DISJUNKTNI 48/48** (0 prekrivanj; P66 v v3: 36/36)
  — **jedro paketa** (neodvisen set-izračun);
- blattPair dist: **I·II 13 · II·III 16 · III·IV 1 · IV·V 18** (sosednji
  48, skoki 0);
- hišne številke: **42 različne · 2 isti (161, 174) · 4 brez hn na eni
  strani (2611, 2612, 2613, 2616)**; kulture deljene 5; areaSuspect 0;
  deleži izenačeni 0; serije S1 88 / S2 8; geoShared 48/48 (v6 join
  fuzira dve parceli pod eno geometrijo);
- **Σ areaQK per Blatt: I 1874 / II 11364 / III 18300 / IV 13257 /
  V 13118 QK**; dominantni deleži (pasovi): [0.50,0.60) 8 · [0.60,0.70) 5 ·
  [0.70,0.75) 8 · **≥0.75 27** — P66 kriterij <0.75 bi pokril samo 21
  (univerzum 48);
- **evolucija P66 → v6: 17/36 ostaja · 19 odhaja (C1 sekcije 5 · C3
  isti-Blatt drop 13 · C2 p93 reverzija 1) · 31 novih** (že v v5; P66 jih
  ni pokril po P65 kriteriju dominantShare < 0.75).

### Opciji A1/A2 (predračun — odločitev LASTNIKA)

- **opcija A1** (keep DOMINANT Blatt; izenačeni deleži → min Blatt): drop
  48 vrstic, 0 base brez vrstic, **rows 939 → 891**, multi 50 → 2,
  **cross 48 → 0**, ambRows 100 → 4;
- **opcija A2** (keep MIN Blatt, vrstni red I–V; P73 »min stran« analog):
  enaki števci, keep **različen pri 29 base** — izbira pravila LASTNIŠKA;
- opcija B (per-Blatt instance + razdelitev geometrije) zahteva georef
  Blattnih kart [~]; vrstice ostanejo v registru brez geometrije ob
  izvedbi (C1/C3 vzorec).

### Skripta, invarianti in QA

- Skripta scripts/p74_ps_cross_blatt_pack.py (I1–I9, `--check` bajtno
  PASS; pini v6 dokaz de13f10b…, v6 runtime 6270b267…, P59 650f13dc…,
  P56 2fddc76f…, P66 02214eba…, P72 0922a701…).
- Dokaz research/issue17/ps-cross-blatt-pack.json (bases 48 s per-Blatt
  razčlenitvijo + pageMap + opcijaA per base) + runtime
  src/data/atlas/ps-cross-blatt-pack.json (version 1; bajtna projekcija
  I7).
- QA 76 → **77/77** (nova qa-p74-cross-blatt: TS pini na CROSS_BLATT_P74
  + CELOVEN neodvisen preracun cross seta iz v6 runtime vrstic × P59
  pageAttribution × P66 pack runtime — 48/96, 1-per-Blatt 48/48,
  blattDist, lastniki 48/48, hn 42/2/4 s seznami, Σ areaQK per Blatt,
  pasovi, opciji A1/A2 re-izpeljani iz runtime vrstic, evolucija P66
  17/19/31 + razlogi C1/C3/C2, pageMap prekrivanja 48/48 + razponi ⊇
  runtime parzella; repo dodaja dokaz == runtime bajtno + P56 pageMap ==
  pack pageMap + razlogi odhoda po skriptni metodi (v5/v6 removedRows);
  dve obliki).

**Poštenost:** paket samo meri in dokazuje — v6 join NESPREMENJEN;
odločitev o cross-Blatt SPLIT joinu (A1/A2/B) je LASTNIKA. Strojno
berljivo: research/issue17/ps-cross-blatt-pack.json + runtime
src/data/atlas/ps-cross-blatt-pack.json (skripta
scripts/p74_ps_cross_blatt_pack.py, I1–I9, `--check` bajtno PASS).

---

## §52 — P75: cross-Blatt SPLIT opcija A1 — v7 (izvedba C4 iz P74 paketa) — 2026-10-15

**Sprožilec:** lastniški ukaz »nadaljuj« 2026-10-15 po odločitvenem paketu
P74 (§51) — vzorec P72→P73: **privzeta pot = opcija A1** (keep DOMINANT
Blatt po Σ areaQK; ties 0) izvedena kot C4; deterministično, brez AI ob
delovanju; **samo odstranjevanje dokumentiranih lažnih fuzij** — noben nov
podatek ni izmišljen.

### Pravilo C4 (izvedba)

- univerzum: **48 cross base** iz P74 packa (vrstice na ≥ 2 sosednjih
  Blattih; 96 vrstic; 1 vrstica per Blatt 48/48; lastniki med Blatti
  disjunktni 48/48; pageMap prekrivanja 48/48 = per-Blatt ponovitev
  numeracije — ista številka pod dvema Blattoma = **2 realni parceli**);
- **drop = vrstica ne-dominantnega Blatta** (keep = DOMINANT Blatt po
  Σ areaQK; ties 0) — **48 kombinacij (page, base) = 48 vrstic**; 0 base
  brez vrstic (I4);
- opcija A2 (keep MIN Blatt) bi pri **29 base** obdržala drugo vrstico;
  opcija B (per-Blatt instance + razdelitev geometrije) zahteva georef
  Blattnih kart [~] — ostajata reverzibilni/dokumentirani poti (reverzija/
  dopolnitev C4 dokumentirana v `next`).

### Merjeno (v7 = v6 − 48 dropov)

- **before 939 / 879 / 50 / 48 → after 891 / 879 / 2 / 0** (vrstice /
  base / multi-page / cross-Blatt) — 939 − 48 = 891 vrstic (32.3 % izbire);
- dvoumnost 100 → **4 vrstic** (2 base; **48 derived True→False** po P55
  metodi — dual base po dropu enostranska); conf **0 sprememb** (172/588/
  131 — geografija nedeprava); serije S1 803 / S2 62 / BI 26; readConfBI
  3/14/9 nespremenjen; biDrop 0;
- **area median 3.8102** (Δ **+5.94 %**; 871 parov; tight 183 / 0.2101;
  kontrola shuffle 4.1435 / 0.0586); sosledje **652 parov / 51.8 m /
  25.5×** (nespremenjeno — dropi ne razbijejo soslednih parov);
- removedByPage: {11: 8, 61: 5, 64: 12, 94: 4, 96: 1, 110: 5, 125: 9,
  133: 1, 135: 3}.

### Nasledstvo (P9 disciplina) in NIL-CLAIM

- **ohranjene vrstice bajtno == v6** (drop samo odstranjuje; edina
  sprememba derived `ambiguous` 48 True→False); vrstice ostanejo v
  REGISTRU brez geometrije (removedRows 48 v dokazu); v6 ostaja arhiviran
  (research/issue17/ps-parcels-geo-v6.json); v5Delta + v6Delta + v7Delta =
  zgodovina nasledstva (1145 → 1077 → 939 → 891);
- **NIL-CLAIM (QA pozitivna kontrola): v7 runtime ne vsebuje nobene od 48
  drop kombinacij; cross set na v7 == PRAZNO** (multi-page 2, cross-Blatt 0).

### Skripta, invarianti in QA

- Skripta scripts/p75_ps_v7_cross_split_a1.py (I1–I8, `--check` bajtno
  PASS; pini v6 dokaz de13f10b…, P74 pack 0779bb9a…, P59 650f13dc…,
  P56 2fddc76f…, PARCELS fee91fca…; I1 vsebuje v6 runtime nasledstveno
  vejo: v6 pin ALI version ≥ 7 + v7Delta droppedPairs 48).
- Dokaz research/issue17/ps-parcels-geo-v7.json (corrections C4 z
  odločitvijo + evidence + droppedRows 48 + removedRows 48; inputs 5
  pini; rowsEvidence 891) + runtime src/data/atlas/ps-parcels-geo.json
  (version 7; PAYLOAD/schema NESPREMENJENA).
- Veriga skript: p60–p67 + p70–p74 `--check` PASS (p68 zamrznjen po C2 —
  zgodovinsko; P74 skripta ima I1 nasledstveno vejo na v7).
- QA 77 → **78/78** (nova qa-p75-cross-split: TS pini na
  CROSS_SPLIT_A1_P75 + CELOVEN neodvisen preracun: (a) cross set
  re-izpeljava iz P74 pack runtime bases[].rows × P59 pageAttribution ==
  pack bases bajtno; (b) A1 drop izpeljava == pack.optionA.keepBlatt/
  keepPage; (c) NIL-CLAIM 0 drop kombinacij v v7; (d) nasledstvo 939 − 48
  = 891 / 879 / multi 2 / cross 0 / ambRows 4 / conf 172-588-131 / serije
  803-62-26; (e) successionska veja version 7 + v7Delta; (f) area/spatial
  preracun == pini; produkcija veja IZMERJENA iz v7 runtime datotek
  (vzorec P73 lekcije); dve obliki repo/produkcija).
- Prilagojene kontrole na v7 realnost (successionske veje, zgodovinski
  pini ostanejo): qa-p72 (pack vrstice zamrznjene + nil-claim), qa-p73
  (v7 veja + nil-claim C3), qa-p74 (cross set iz pack runtime rows —
  v7 runtime cross == prazno), qa-p55/p58/p68/p70/p71 (izmerjene v7
  vrednosti).

**Poštenost:** C4 odstranjuje LE lažne fuzije čez Blatte — noben nov
podatek ni izmišljen; vrstice ostanejo v registru brez geometrije; opcija
A2/B ostajata dokumentirani poti. Strojno berljivo:
research/issue17/ps-parcels-geo-v7.json + runtime
src/data/atlas/ps-parcels-geo.json (skripta
scripts/p75_ps_v7_cross_split_a1.py, I1–I8, `--check` bajtno PASS).


---

## §53 — P76: lokalne sekcije — per-Blatt instance odločitveni paket — 2026-10-15

**Sprožilec:** lastniški ukaz »odlicno nadaljuj« (2026-10-15) — naslednja odprta
točka ② iz P70 ①/P71 C1: per-Blatt instance 56 sekcij vrstic (P60 moda B /
PF protokol); vzorec P72/P74: **paket MERI, NE odloča** (deterministično, brez
AI ob delovanju); **v7 join NESPREMENJEN** (disciplina P56–P75; sha256 pin I9
na v7 runtime 4bb40370…).

### Univerzum in metoda

- 56 sekcij vrstic (P69 sectionClass bajtno; p83 13 · p84 12 · p85 14 ·
  p86 14 · p88 3; 31 base: 160–179 subset 14 · 641–659 subset 14 · 736–738 3)
  — vse strane **Blatt II** (P59 pageAttribution 5/5; p83 flag=true
  arbitraža); 56/56 najdenih v v3 rowsEvidence (page+base+owner; areaQK ==
  P69);
- meritve deterministične nad v7 univerzumom × v3 forenzika × P59/P56/P60
  kontekst — opcije PREDRAČUNANE (counters re-izračunani, ne deklarirani);
  izbira = LASTNIŠKA.

### Merjeno (44-a)

- **counterpar v v7: 31/31 base točno 1 preživela vrstica** (posledica
  C1 + C3 + C4): 23 Blatt I (p10 1 · p11 5 · p35 14 · p40 3) + 8 Blatt II
  (p61 8); vsi 31 z geometrijo (C1 I4 nasledstvo — 0 poligonov praznih);
  conf STRONG 4 / MEDIUM 21 / WEAK 6;
- **evolucija C4: 13/31 base bilo v v6 cross-Blatt setu (I p11 × II p61)** —
  8 obdržalo II (161–165, 174, 176, 179), 5 obdržalo I (166, 168, 171, 173,
  175); 18/31 single-Blatt;
- **JEDRO — identitetna disjunktnost razširjena iz P69 vzorca na celoto:**
  lastniki sekcija×counterpar **0 prekrivanj** (56/31 base) + sekcija×
  sekcija **0** (set-izračun); hišne številke **0 isti / 31 različni**
  (31/31 base z hn na obeh straneh) — razširitev P69 primera (p85 641 Hi16
  vs p35 641 Hi68) na celotno množico;
- **P56 pageMap ponovitev bandov 5/5:** p83 161–181 / p84 162–182 /
  p86 160–180 ⊆ [p11 161–183 · p61 161–180]; p85 641–660 == p35;
  p88 721–740 == p40;
- **P60 moda B band: 8/31 base attributed** (163, 176 → inBand [61, 83, 84,
  86]; 644, 653–657 → inBand [85]) = **12/56 vrstic z band identiteto**;
  44 [~] brez (PF protokol = manjkajoči vir, ni v repu — P60/P61/P63–P68
  next);
- **v3 forenzika lažnih fuzij:** geoShared 56/56 (sekcija je delila
  geometrijo sodobne parcele s counterparom); ratio dist: moda B [0.8, 1.25]
  11 · moda A [3.3, 4.3] 5 · **absurdni > 4.3: 20 (max 134.6786)** ·
  median 2.5442; areaSuspect 1; conf 3/42/11 (v3 — lažno); **Σ areaQK**
  {83: 3708, 84: 10273, 85: 10333, 86: 9544, 88: 4659} = **38517 QK**;
  kulture Alm 9 · Dingf. 6 · Wein 3 …; wohnort 56/56.

### Opcije A/B1/B2/B3 (predračun — odločitev LASTNIŠKA)

- **A status quo (v7):** rows 891 / bases 879 / multiPage 2 / crossBlatt 0 /
  ambRows 4 — sekcije v registru brez geometrije (dokaz P69 sectionClass);
- **B1 re-admisija vseh 56 (base-ključ, brez geometrije):** rows 947 /
  multiPage 33 / **crossBlatt 23** / ambRows 91 — **KRŠI C4 NIL-CLAIM**
  (23 base dobi vrstici na I in II) → **OBVEZEN per-instanca ključ
  (base, stran)**: 0 kolizij + 0 duplikatov + 0 vrstic v7 na sekcij straneh
  → crossBlatt 0 / multiPage 2 / ambRows 4 (nespremenjeno);
- **B2 samo P60 band subset (12 vrstic, 8 base):** rows 903 / multiPage 10 /
  crossBlatt 6 / ambRows 24 (isti problem, manjši); z instance ključem
  crossBlatt 0 / multiPage 2 / ambRows 4; **44 vrstic ostane izključenih [~]**;
- **B3 geometrija per Blatt:** ZAHTEVA georef Blatt II sekcije karte +
  PF protokol (vir ni v repu) — **[~] neizvedljivo danes**.

### Skripta, invarianti in QA

- Skripta scripts/p76_ps_sections_perblatt_pack.py (I1–I9, `--check` bajtno
  PASS; pini P69 99962e24…, v3 af7479e4…, v7 4d701a71…, P59 650f13dc…,
  P56 2fddc76f…, P60 2c2b2ace…, v7 runtime 4bb40370…).
- Dokaz research/issue17/ps-sections-perblatt-pack.json (summary/opcije/
  kulture/hausNrDetail/p60Detail + sectionRows 56 × ratioV3/geoSharedV3/
  pageMapBand; inputs 7 sha pinov; invarianti I1–I9) + runtime
  src/data/atlas/ps-sections-perblatt-pack.json (bajtna projekcija — brez
  principle/inputs/invariants + sectionRows brez ratioV3/geoSharedV3/
  pageMapBand).
- Veriga skript: p60–p67 + p70–p75 `--check` PASS (p68 zamrznjen po C2 —
  zgodovinsko); P76 ne spreminja nobenega obstoječega dokaza/runtime-a.
- QA 78 → **79/79** (nova qa-p76-sections-perblatt: TS pini na
  SECTIONS_PERBLATT_P76 + CELOVEN neodvisen preracun iz runtime datotek —
  ps-pass1-layers sectionClass × v7 runtime × P59 pageAttribution ×
  ps-perblatt-attribution × pack runtime: 56/31/per-page, Blatt II 5/5,
  counterpar 31/31 (Blatt po P59 — NE po row.blatt), lastniki 0/0,
  hn 0/31, pageMap bandi ⊇ parzelle, Σ areaQK, P60 band 12/56, opcije
  A/B1/B2 re-izpeljane iz v7 + pack vrstic (strip na register-native
  polja) + instance ključ 0/0/0, pack == TS konstanta po poljih, v7 join
  pini 891/879/2/0; repo dodaja dokaz == runtime bajtno (summary/opcije/
  kulture/hausNrDetail/p60Detail + sectionRows + ratioV3/geoSharedV3/
  pageMapBand), invarianti I1–I9, inputs 7 pinov, P56 dokaz pageMap ==
  pini; dve obliki repo/produkcija).

**Poštenost:** paket NE SPREMINJA v7 joina — samo meri in dokazuje
(NIL); izbira opcije (A/B1/B2/B3) je LASTNIŠKA; PF protokol je manjkajoči
vir [~] (44 vrstic brez band identitete); p83 dvojni blok 161–170 ×2 ostaja
[~] (P69; 8× nebere zanesljivo). Strojno berljivo:
research/issue17/ps-sections-perblatt-pack.json + runtime
src/data/atlas/ps-sections-perblatt-pack.json (skripta
scripts/p76_ps_sections_perblatt_pack.py, I1–I9, `--check` bajtno PASS).

## §54 — P77: PF protokol — VAČ inventarna forenzika (dokazani negativ) — 2026-10-15

**Sprožilec:** owner ukaz »nadaljuj uredi readme pushaj in nadaljuj« — po README
ureditvi (Task 45) naslednja ne-lastniška odprta točka ② iz P76: »PF protokol =
manjkajoči vir« (vir identitete pas-instanc; P60 moda B — 44 [~] vrstic brez
band identitete).

**Vprašanje:** ali je protokol-slični vir (PF/Parzellen-Führer/Stavbni
protokol) za k.o. N83 Griblje digitaliziran na VAČ?

**Metoda (deterministična, brez AI):**
- VAČ je bil posodobljen 2026-10-14 (verzija 2.21_5.5): `fieldSearchFindAjax`
  vrača `totalItems 0` za VSE kriterije, `details?id=` javlja interno napako
  tudi za znane id-je (227663, 373415) — **edini delujoč API je tektonika**
  (`archivePlanSearchAjax`) in `pdfPageImage` (slike);
- besedilni sprehod po tektoniki: root → 000 UPRAVA (653381) → 070 Posebni
  upravni organi (653535) → 071 uprava/pravosodje (653582) → **SI AS 176
  Franciscejski kataster za Kranjsko (1823–1869) (23253)** → N Novomeška
  kresija (226589, 310 k.o. na 3 straneh) → **N83 Griblje, k.o. (227663)**;
- N83 otroci: natanko 2 skupini — **grafični (227665)**: 5 listov A01–A05
  (227666/227668/227670/227671/227673) · **spisovni (373412)**: 7 enot PG
  (373413), PR (373414), PS (373415), PT (373416), PUA (373417), PV (373418),
  PZ (373419) — skupaj **12 enot** == številu v README;
- mapiranje `docid = uodid − 331635` verificirano z JPEG probe page=1 na vseh
  7 spisovnih enotah (7/7 HTTP 200 + ff-d8 magic; PS/PG znana recepta
  potrjena kot posebna primera istega odmika);
- sosedski uodid prostor (373411, 373420–373424): 0/6 JPEG — razpon spisovnih
  enot je točno 373413–373419, ni skrite enote.

**Rezultat — DOKAZANI NEGATIV (I6):** med 12 enotami k.o. N83 na VAČ ni
dodatnega protokola (PF/Parzellen-Führer/Stavbni protokol). Edini
protokol-slični vir = **N083PT Seznam stavbnih parcel (373416)**, ki je ŽE v
repu (PT: 105 prebranih vrstic = 84 hišnih + 21 parcelnih; audit §13;
vir identitete hišnih številk).

**Implikacija (P76 ②):** vir identitete pas-instanc NI na VAČ — potreben je
fizični arhiv (Arhiv RS, SI AS 176 ali SI AS 52 Finančna direkcija 1825–1924)
ali drugi fond. P76 opcije B1/B2 ostajata edini izvedljivi poti brez PF
protokola; opcija A = status quo; izbira ostaja **LASTNIŠKA**.

**Skripta in invarianti:** `scripts/p77_pf_vac_inventory.py` (I1–I8;
`--check` bajtno PASS — stabilno jedro brez časovnih žigov/verzije VAČ) →
dokaz `research/issue17/pf-vac-inventory.json` (PROVEN-NEGATIVE-INVENTORY).
**QA ostaja 79/79** — VAČ inventar je zunanji odvisni vir (omrežje) in po
P53/P57/P58 lekciji NE sme biti produkcija QA kontrola; dokaz je ponovljiv
z `--check`. **v7 runtime join NESPREMENJEN** (sha256 4bb40370…; disciplina
I9). Kartica NI dodana (ni produkcija vsebine — inventarni dokaz za
raziskovalno linijo; strojno berljivo prek dokaza).

**Poštenost:** dokazani negativ velja ZA VAČ STANJE 2026-10-15 (verzija
2.21_5.5) — VAČ se je dan prej posodabljal, iskalni API je pokvarjen, zato je
inventar pridobljen prek tektonike (avtoritativno drevo). Absenca na VAČ ne
izključuje obstoja v fizičnem arhivu ali drugem fondu [~].

## §55 — P78: produkcija & žetoni — operativni zdravstveni audit (issue #6) — 2026-10-15

**Sprožilec:** owner ukaz »odlicno nadaljuj« — po P77 so vse raziskovalne niti
skonvergirale k lastniškim odločitvam; edina NE-lastniška odprta točka je ③
žetoni/operativa (issue #6).

**Metoda (deterministični probe, brez AI):** produkcija (`GET /`, `/api/qa`,
`/api/atlas/ps-parcels-geo`), GitLab (`/personal_access_tokens/self` —
avtoritativni rok žetona — in `/projects/87462760`; WAF-retry), zrcala
(`git ls-remote` origin/github/HEAD), GitHub Actions stanje (zadnji runi
sync.yml + token-health.yml → job steps/runner_id → check-run anotacija),
lokalna prisotnost workflow datotek. Skripta `scripts/p78_tokens_production_audit.py`
(I1–I9, `--check` bajtno PASS; brez mutacij) → dokaz
`research/issue17/tokens-production-audit.json` (OPERATIONAL-AUDIT).

**Ugotovitve:**
1. **Produkcija ZDRAVA in AKTUALNA:** `GET /` HTTP 200 (704 548 B == post-P77
   deploy), `/api/qa` ok True 79/79 (79 testov; `qa-p76-sections-perblatt`
   True), geo `version 7` / 891 vrstic.
2. **Zrcala bajtno identična:** GitLab = GitHub = lokalni HEAD (ls-remote;
   GitHub REST `GET /commits/main` 404 neavtentificirano — repozitorij
   zaseben).
3. **GitLab PAT #3 avtoritativno aktiven:** id 28471532, name `dsfsd`,
   active, revoked false, rok **2026-11-14**, scopes ⊇ api +
   write_repository + read_repository + self_rotate. Rok 2026-11-09 v
   naslovu issue #6 se nanaša na stari žeton (P78 ga ne popravlja na
   GitHubu — kosmetika issue je kosmetika lastnika).
4. **DISCOVERY — GitHub Actions blokiran na nivoju računa (billing):** vsi
   jobi NE STARTAJO — job `failure` v ~2 s, `steps: []`, `runner_id: 0`,
   logi `BlobNotFound`; check-run anotacija (avtoritativno GitHub):
   *"The job was not started because recent account payments have failed or
   your spending limit needs to be increased. Please check the 'Billing &
   plans' section in your settings."* Kontrolni dispatch token-health.yml
   (brez checkouta, čisti curl) daje enak podpis → blokada je na računu,
   ne na workflowu. Zadetki: **sync.yml** (dvosmerna sinhronizacija — mreža
   varnosti; zadnji uspeh 2026-10-11T06:23:19Z), **token-health.yml**
   (dnevni watchdog žetonov — zato NI opozoril 10-13/14/15 ob izteku
   VERCEL_TOKEN 2026-10-14) in **deploy.yml** (rezervni deploy; zadnji
   uspeh 2026-10-11T06:12:27Z; potekel žeton = dodaten razlog).
5. **SANACIJA P78 (skrivnost):** `GITLAB_TOKEN` v GitHub Actions je držal
   neveljaven PAT #2 (updated 2026-10-13T16:18:56Z) — zamenjan z aktualnim
   PAT #3: vrednost šifrirana z libsodium sealed box (PyNaCl 1.6.2) z
   javnim ključem repozitorija (key_id 3380204578043523366),
   `PUT /repos/…/actions/secrets/GITLAB_TOKEN` → HTTP 204, updated
   2026-10-15T20:51:08Z. Nujno tudi samo po sebi: stari PAT bi povzročil
   auth padec, takoj ko bi Actions začel teči. Kontrolni dispatch sync.yml
   po sanaciji (run 38805294449): še vedno failure v ~2 s brez korakov —
   potrdilo, da vzrok NI žeton.

**Vpliv na projekt (per workflow):** primarna produkcijska pot (Vercel
GitHub App) je NEODVISNA od Actions in od žetonov — deployi in produkcija
tečejo normalno. Mrtve so samo rezervne/nadzorne plasti: sync (operativno
neškodljivo, dokler glavni agent puša na OBE strani — P21 disciplina),
watchdog (mehka točka; ročni `p78 --check` jo nadomešča) in rezervni deploy.

**Lastniške akcije po prioriteti (iz dokaza):**
1. GitHub → Settings → **Billing & plans**: plačilna metoda / spending
   limit (API brez admin:billing scope ne more) — obnovi sync + watchdog +
   rezervo;
2. **VERCEL_TOKEN**: nov žeton na vercel.com/account/tokens (Vercel API ne
   ustvarja žetonov) — obnovi SAMO rezervni deploy;
3. raziskovalne odločitve P76 ① (opcije sekcij A/B1/B2/B3) in P77 ②
   (fizični arhiv za PF) — neoperativno, nespremenjeno.

**Poštenost:** audit odraža stanje 2026-10-15 (live probe; `--check` ga
ponovno izmeri). Po lastniški sanaciji billinga bo `--check` (I8) realno
FALIL — to je namerna lastnost: dokaz zahteva ponovno izdajo, ki bo
 dokumentirala sanirano stanje.

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…; disciplina I9). QA
ostaja 79/79 (operativni audit ni produkcija vsebine — ni nove kartice niti
nove QA kontrole). Veriga `p60–p67 + p70–p78 --check` bajtno PASS; tsc 0;
ESLint 0.

## §56 — P79: župnija Podzemelj — vzorčni prepis matričnih vpisov (issue #18) — 2026-10-15

**Sprožilec:** owner ukaz »nadaljuj« — po P78 so raziskovalne niti skonvergirale
k lastniškim odločitvam; edina NE-lastniška vsebinska nit: issue #18 (ŽUPNIJA
— matrični vpisi z gribeljskimi hišnimi št.; do P79 prepisana samo hiša 61).

**Vir:** Matricula Online, krstna knjiga **04105** (1886–1919), Nadškofijski
arhiv Ljubljana, župnija Podzemelj (Griblje = zgodovinsko matično območje;
sv. Vid = 3. podružnica — parish.ts). Prosto dostopno; slike prek base64-
kodiranih URL-jev v JSON `files` knjižne strani (326 slik).

**Metoda (paleografska faza + deterministična verifikacija):**
- okvir vzorca: **polno leto 1886** (skeni 2–15 == tiskane strani 1–14;
  stran = sken − 1; kontrola: sken 11 → stran 10 Okt 1886, sken 16 → stran
  15 Januar 1887) — vsi vpisi z Griblji v tem letu; vrstice 1–95 prebrane;
  **+ sidro 1887** (sken 20 = stran 19): ponovno branje obstoječega zapisa
  hiše 61 (verifikacija obstoječih podatkov);
- branje: skeni prenešeni v delovni imenik (NI v repu), stran + 2×/2.2×
  izrezi dvomljivih celic (PIL LANCZOS); Kurrent z označbo negotovosti [~];
- deterministična verifikacija: `scripts/p79_parish_sample.py` (I1–I8):
  knjiga HTTP 200, inventar 326 slik, citirani skeni 10/10 JPEG 200, okvir,
  PT usklajenost (branje `research/issue13/chain-full-pt-ps.json`), celovitost
  polj, sidro hiša 61.

**Rezultat — 14 vpisov / 13 različnih hiš** (nad merili issue #18 — vzorec
5 hiš): 8 [~] · 11 · 13 · 16 · 36×2 · 39 · 54 · 56 · 57 · 61 · 71 · 75 · 94.
Vsak vpis: signatura, leto, mesec/dan rojstva in krsta, vas, hišna št.,
otrok, oče (ime + stan: ½ zemg. / hižar / bajtar), mati (roj. priimek),
botra/botr, robovni pripisi.

**Ugotovitve:**
1. **PT usklajenost = dokaz številčne evolucije:** PT 1825 nabor hiš
   (chain-full-pt-ps.json) je **1–40 + 61–99** z polovičkami (7½, 8½, 71½,
   76½) + prečrtana dvojnica 34 — **LUKNJA 41–60**. Parish 1886: 10/13 hiš v
   naboru (8, 11, 13, 16, 36, 39, 61, 71, 75, 94), **3/13 (54, 56, 57) v
   luknji 41–60** → številčenje se je med 1825 in 1886 razširilo/
   preštevilčilo. Številčna usklajenost ≠ identiteta stavbe (za to bi bila
   potrebna povezava prek lastniških imen — opozorilo PUA/PT iz issue #18
   ostaja).
2. **Hiša 36 = dva vpisa v 1886** (row 39: mati Barbara Šimec, oče ni
   zapisan — nezakonska rojstva dokumentirana kot zapisana; row 95: oče
   Matija Križan, mati Ana roj. Milavec) → dve družini pod eno hišno št.
   [~] (glavna kmetija + inst-hiša?).
3. **Poznejši modri pripisi 20. stoletja** (»umrl dne …«, npr. hiša 39:
   umrl 18.9.1961 *v Gribljah št. 39* — administrativni vpis POTRJUJE
   hišno št.; hiša 16: umrla 19.3.1962) dokumentirani ločeno od osnovnega
   vpisa.
4. **Sidro hiša 61 POTRJENO** (sken 20, stran 19, vrstica 28: Griblje 61,
   Katarina, April 1887): sken/leto/hiša/ime == parish.ts; oče: obe branji
   dokumentirane (obstoječe »Miha P.—« / ponovno »Miko Jože H.?« [~] —
   priimek ostaja negotov).

**Integracija:** `parish.ts` HOUSE_VITALS 2 → 15 (vsi DOCUMENTED, dopolnjene
strani); QA 79 → **80/80** (nova `qa-p79-parish-sample`: celovit runtime
preracun iz HOUSE_VITALS × PARISH_BOOKS + pini PT klasifikacije 10/3 —
okvir/sidro/PT/usklajenost; dve obliki repo/produkcija po P53/P57/P58 —
produkcija ne bere research/); kartica NI dodana (paleografski dokaz
raziskovalne linije — strojno berljiv prek dokaza, vzorec P77).

**Poštenost:** prepis je VZOREC (leto 1886 + sidro 1887), ne celotna knjiga
(326 skenov; 1886–1919). Kurrent branja imen nosijo [~]; hišne številke so
preverjene z izrezi. Številčna usklajenost s PT je OBSERVACIJA, ne dokaz
istovetnosti stavbe. Nezakonska rojstva in pripisi so dokumentirani kot
zapisani.

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…). Veriga `p60–p67 +
p70–p79 --check` PASS; tsc 0; ESLint 0.

## §57 — P80: župnija Podzemelj — razširitev vzorca na mrliško in poročno knjigo (issue #18) — 2026-10-16

**Sprožilec:** owner ukaz »nadaljuj« — P79 nextSteps: »razširitev vzorca:
poročne in mrliške knjige za rojstva/poroke/smrti istih hiš« (isti vzorec
kriterijev kot P79: okvir 1886 v obeh knjigah + sidra čez leta).

**Vira:** Matricula Online, **mrliška knjiga 04894** (1886–1924, 256 skenov)
in **poročna knjiga 04455** (1873–1922, 192 skenov), Nadškofijski arhiv
Ljubljana, župnija Podzemelj — obe knjigi že v PARISH_BOOKS (issue #6).
Prosto dostopni; slike prek base64-kodiranih URL-jev v JSON `files`.

**Metoda (paleografska faza + deterministična verifikacija):**
- **mrliški okvir 1886:** skeni 2–6 == tiskane strani 1–5 == celotno leto
  1886 (46 vrstic; **stran == sken − 1**; leto 1887 se začne NA STRANI 5
  pri prelomu »Januarj 1887« — zadnji gribeljski vpis 1886 je Katarina
  vdova Podec hiša 69 (11. 12.), prvi vpis 1887 Matija Šproch hiša 44,
  1. 1.) — **13 Griblje vpisov / 11 hiš** (5 · 13 · 15 · 16 · 29×3 · 31 ·
  59 · 69 · 71 · 74 · 88) **+ sidro 1887** (sken 6: hiša 44 — prvi vpis
  leta, dokaz preloma; hiša 36 — Ana Šimec neza., povezava z materjo
  Barbaro Šimec iz krsta Jun 1886);
- **poročni okvir 1886:** skeni 61–65 == Pag. 60–64 (vpisi 1–24; **Pag. ==
  sken − 1 v zveznem razponu 61–66**; ročno številčenje Pag. ni zvezno skozi
  celo knjigo — sken 50 == Pag. 44, vendar 61–66 == 60–65; okvir uporablja
  le zvezni razpon) — **7 Griblje vpisov / 10 hiš** (31 · 36 · 60 · 63 ·
  15 · 25 · 71) **+ sidra** (Nov 1885 sken 61: hiša 13 ženin Janez Jakobič,
  starši == pari krsta hiše 13 Nov 1886; Nov 1882 sken 50 Pag. 44: hiša 36
  Mathias Križan = oče krsta Dec 1886; 1887 sken 66: hiša 71 Mathias
  Straus + hiša 15/29 Johann Šambie × Maria Brinec);
- branje: skeni prenešeni v delovni imenik (NI v repu); Kurrent z [~];
  hišna številka 23. 5. 1886 verificirana z **izrezom števk** (Kurrent 3 vs
  5: glajena zgornja krivulja + zaprta zanka = 5) → **hiša 59, ne 39**;
- deterministična verifikacija: `scripts/p80_parish_md_books.py`
  (**I1–I10**, `--check` PASS): knjigi HTTP 200 (inventarja 256 + 192),
  citirani skeni 13/13 JPEG 200, okviri/sidra, obdobja knjig == PARISH_BOOKS,
  PT usklajenost celotnega vzorca (branje chain-full-pt-ps.json), križne
  povezave, P80 re-read, celovitost polj.

**Rezultat — skupaj s krstno (P79): 41 vpisov / 25 različnih hiš** (nad
merili issue #18 — vzorec 5 hiš; doseženo 25).

**Ugotovitve:**
1. **Križne povezave treh virov:** hiše **13**, **36** in **71**
   dokumentirane v VSEH treh knjigah (krstna 04105 + mrliška 04894 +
   poročna 04455): 13 = Jakopič/Podlirc (krst == starši ženina 1885 ==
   smrt otroka 1886); 36 = Šimec/Križan (2 poroki 1882/1886 + krsta 2× +
   smrt 1887); 71 = Strauš (krst + smrt vdove + 2 poroki — priimek Strauš
   v vseh treh knjigah).
2. **Dokaz epidemije — hiša 29:** trije otroci (Janez 8, Katarina 9, Ana
   11 — priimek Mileh [~]) umrli v 4 dneh (10.–13. 10. 1886) z istim
   vzrokom »Kolera i. morbas« [~]; februarja 1887 se na isti hiši poroki
   Maria Brinec, katere mati je roj. Miletch [~] — veriga družine.
3. **P80 RE-READ KOREKCIJA P79:** hiša 56 mati = **»Dora roj. Perdinec«**
   (prvotno P79 branje »Podžire« NAPAČNO) — dokaz: poročna 04455 sk. 62
   vpis 4/1886 (Johann Šimec × Dorothea Perdinec = isti par kot krst Nov
   1886 hiše 56); izrez krstne celice kaže »P—dirc« (drugo/tretje malo
   pismo = e, ne o).
4. **PT klasifikacija celotnega vzorca 25 hiš:** **19 v naboru PT 1825
   (1–40 + 61–99) + 6 v luknji 41–60** (44, 54, 56, 57, 59, 60) — hiši 59
   (mrliška) in 60 (poročna) sta NOVA dokaza luknje v dodatnih knjigah;
   številčna usklajenost ≠ identiteta stavbe (opozorilo PUA/PT ostaja).
5. **Dva duhovnika 1886:** kapljan Andrej Griebel/Glibelj [~] (gribeljski
   vpisi) in župnik Franjo Dovgan (ostale vasi); zavzet podpis »Griebel«
   ne sme biti povezan z vasjo Griblje brez dodatnih virov [~].

**Integracija:** `parish.ts` HOUSE_VITALS 15 → **41** (mrliška 15 + poročna
11 + krstna 15; vsi DOCUMENTED; komentar P80; re-read hiša 56); **qa.ts →
qa-parish.ts izvleček** (telo runQA je preseglo prag TS control flow
analysis; kontrole bajtno enake, vzorec ločevanja modulov) + nova kontrola
`qa-p80-parish-md-books` (celovit runtime preracun iz HOUSE_VITALS ×
PARISH_BOOKS + pini okvirjev in PT klasifikacije 19/6; dve obliki
repo/produkcija po P53/P57/P58) — QA 80 → **81/81**; `atlas.ts`
checkIntegrity **sanitacija regresije P79**: hiše v PT luknji 41–60 (44,
54, 56, 57, 59, 60) ZAKONITO ne obstajajo v ATLAS_HOUSES (PT 1825 nabor =
1–40 + 61–99; luknja = dokaz številčne evolucije) — kontrola jih
klasificira namesto da bi jih zavrnila, vse ostale neznane številke
ostanejo napaka; kartica NI dodana (vzorec P77/P79).

**Poštenost:** prepis je VZOREC (okvir 1886 mrliške + poročne + sidra), ne
celotni knjigi (256 + 192 skenov). Kurrent branja imen nosijo [~]; hišne
številke preverjene z izrezi (hiša 59: izrecna primerjava števk 3 vs 5).
Nemški poklicni izrazi (Gasthausmeister, Leinweber, Dienstmagd …) dobri
kandidati za uredniški prevod. Številčna usklajenost s PT je OBSERVACIJA,
ne dokaz istovetnosti stavbe (povezava prek lastniških imen ostaja odprta).

**v7 runtime join NESPREMENJEN** (891/879; disciplina I9). Veriga `p60–p67
+ p70–p80 --check` PASS; tsc 0; ESLint 0; /api/qa dev 81/81 (qa-p80 True).


## §58 — P81: župnija Podzemelj — povezava lastniških imen 1825 (PT/PUA) ↔ matrični priimki 1886 (issue #18) — 2026-10-16

**Sprožilec:** owner ukaz »nadaljuj« — P80 nextSteps: povezava vzorca P79/P80
(25 hiš) z lastniki 1825 na IMENSKI ravni — test ali številčna usklajenost s
PT/PUA nosi tudi imensko kontinuiteto (odprto vprašanje issue #18 od P56).

**Vesolje 1825 (232 imen, trije sloji):** PT 84 hišnih lastnikov iz
`research/issue13/chain-full-pt-ps.json` [pin, repo-verificiran I3] + PUA 101
vrstic str. 3–49 (`PUA_CONTINUATION`, bundle) + ATLAS 26 lastnikov str. A–B
(`ATLAS_OWNERS`, bundle); **vzorec 1886:** 25 hiš P79/P80 (19 v naboru PT
1–40 + 61–99, 6 v luknji 41–60), 40 različnih gospodinjskih priimkov.

**Metoda (deterministična, brez AI ob delovanju):** normalizacija pass1
(male črke + de-diacritika) in pass2 (+ nemška Kurrent Schreibung sch→s);
Levenshtein razmerje 1 − d/max; **prag priče ≥ 0.72** (ponovna uporaba praga
P43 W-most); kratki priimki < 5 znakov LE natančna enakost žetona; žetoni
imen ≥ 4 znake (unija obeh passov); **stoplist krstnih imen** (Gregor, Johann
itn. — brez nje bi priimek Gregorič lažno ujel krstno ime Gregor 0.75) +
uredniški žetoni (rokopis/alternative); sorted tie-break. Trojni determinizem:
Python skripta ↔ TS `name-matcher.ts` ↔ QA runtime; izvedba neodvisna od
packa (istovetnost verificirana).

**Rezultati (NAME-LINKAGE-PACK):**
1. **ISTO-HIŠNA kontinuiteta vs PT 1825: 0/19 (NIL-CLAIM)** — pri VSEH hiš z
   PT lastnikom je 1886 gospodinjski priimek različen od 1825 lastnika (prag
   0.72); gospodinjska zamenjava na ravni hišnih števil ALI divergenca
   prepisa [~].
2. **Isto-hišne ujeme po PUA lastnem številčenju: 2** — hiša 36 Križan ↔ PUA
   Krischan @36 (0.8333 via sch→s) in hiša 71 Straus ↔ PUA Strauß Niklo @71
   (0.8571) — PUA ≠ PT številčenje, zato usklajenost dveh sistemov, NE dokaz
   istovetnosti stavbe.
3. **CENZUS priimkov: 10/38 eligible (26.32 %) ima pričo 1825** — Dragoš=1.0,
   Filak=1.0 (PT 69/71 + PUA Fillah), Stubler=1.0, Šimec=1.0 (najtrajnejša:
   PUA 5 zapisov + ATLAS 5 → 1886 hiše 36/39/56/88), Šimer=1.0 [~],
   Strauš/Straus=0.8571, Brinec=0.8333 [~] (PUA @43 — št. V LUKNJANI 41–60),
   Filatk=0.8333 [~], Križan=0.8333; preživetje na ravni PRIIMKA, ne hiše;
   17 priimkov brez priče (Meh, Muc izključena po dolžinskem pravilu).
4. **NEAR-MISS pas [0.55, 0.72): 11 priimkov** (Gilatk 0.667, Mileh/Milavec ~
   Milleg, Stupanič ~ Stepanitsch, Šilah ~ Fillah, Klepec ~ Kleppetz, Poddirec
   ~ Poldiŕg …) — poročano, NE šteto kot priče.
5. **Luknja 41–60:** PUA ohranja 16 vrstic v območju (P4); 0 isto-številnih
   ujem ≥ 0.72 z 1886 (najbližje @56 Schumetz vs Šimec 0.667 [~]).
6. **Tri-virske hiše 13/36/71: 0/3 isto-hišnih imenskih ujem z 1825** —
   niti najmočnejše križne povezave P80 nimajo imenske kontinuitete na isti
   hišni številki 60 let kasneje.

**Implikacija za issue #18:** imenska raven POTRJUJE opozorilo — številčna
usklajenost ≠ identiteta stavbe ≠ identiteta družine; most zahteva per-hišne
kronološke verige (poln prepis po letih = lastniška prioriteta).

**Integracija:** runtime `src/data/atlas/parish-name-linkage.json` (bajtna
projekcija dokaza) + `src/lib/name-matcher.ts` (zrcalna TS izvedba — P81
prag/token/stoplist; vsaka sprememba zrcaljena v Python, I5) + nova kontrola
`qa-p81-parish-name-linkage` v `qa-parish.ts` (82. kontrola; celoven
neodvisen preracun: isto-hiša PT/ATLAS/PUA + cenzus + PUA 41–60 + 57 sidr
src==parish proti bundled `parish.ts`; preostala 4 sidra — 1 p80 + 3 p79 —
verificirana le v repo skripti, produkcija ne bere research/; dve obliki
repo/produkcija po P53/P57/P58) — QA 81 → **82/82**; kartica NI dodana
(vzorec P77/P79/P80).

**Poštenost:** paket MERI, NE odloča. Ujemanje priimkov je hevristika z
merjenimi razmerji: prag 0.72 nekonservativen za Kurrent [~]; kratki priimki
(Meh, Muc) izključeni iz cenza; dvoumni vpisi izključeni (hiša 61 oče »Miha
P.—«/»Miko Jože H.?«; nevestini starši @31 Straus/Stabek — bivališče
nečitljivo); PUA/ATLAS številčenja ≠ PT številčenje [~] — isto-hišne ujeme
2 sta usklajenost sistemov, ne dokaz.

**v7 runtime join NESPREMENJEN** (891/879; disciplina I9). Veriga `p60–p67
+ p70–p81 --check` PASS; tsc 0; ESLint 0; /api/qa dev 82/82 (qa-p81 True).


## §59 — P82: župnija Podzemelj — krstna knjiga 04105, polno leto 1887 (issue #18) — 2026-10-16

**Sprožilec:** owner ukaz »odlicno nadaljuj sinhroniziraj readme kode gitlab
github vercel in nadaljuj« — sinhronizacija potrjena (lokal = GitLab = GitHub
= ab52498; Vercel produkcija QA 82/82), P82 = P81 nextSteps ①: širitev
vzorca po letih — krstna 1887.

**Vir:** Matricula Online, krstna knjiga **04105** (1886–1919, 326 skenov);
**okvir 1887: skeni 16–27 == tiskane strani 15–26** (stran == sken − 1);
glava »Leto 18_87« na strani 15 (sken 16); **leto 1888 se začne NA STRANI 26
(sken 27) po vrstici 106 z velikimi ciframi »1 8 8 8«** — zadnji vpis 1887 =
row 106 (29./30. 12., Krasinec 7), prvi 1888 = row 107 (9./11. 1., Gradac 26).

**Metoda (paleografska faza + deterministična verifikacija):** skeni 16–30
prenešeni v delovni imenik (NI v repu); Kurrent branje z [~]; hišne številke
preverjene z izrezi (row 78 trojna korekcija, row 12 kodrasti 2, row 26
5-vs-8 forenzika); deterministični verifikator `scripts/
p82_parish_baptism_1887.py` (**I1–I10**, `--check` PASS): knjiga HTTP 200 +
inventar 326, citirani skeni 8/8 JPEG 200 (strani 15, 17, 18, 21 prebrane
brez Gribljev), okvir + prelom 1888, PT klasifikacija iz verige, sidro,
križne povezave, runtime projekcija.

**Rezultat: 20 vpisov / 19 različnih hiš** (2, 15, 17, 21, 24, 26 [~], 27,
31×2, 34, 35, 47, 52→04→15 [~], 55, 61, 62, 63, 65, 66, 78) — skupaj s
P79/P80 vzorec zdaj 59 vpisov / 42 hiš čez tri knjige in dve leti.

**Ugotovitve:**
1. **NOVI PT LUKNJI 47 in 55** (+ 52 izvirno row 78): luknja 41–60 v krstnih
   vpisih zdaj 54/56/57 (P79) + 44/59/60 (P80) + 47/52/55 (P82) = **9
   dokazanih števil**; row 78 = **TROJNA KOREKCIJA hišne št. 52 → 04 → 15**
   [~] — izvirno v luknji, končna v naboru; obe klasifikaciji dokumentirani.
2. **P79 RE-READ KOREKCIJA: hiša »75« = 78** — P79 sidro (Janez, 16. 4.,
   Janez Jakobič × Marija roj. Stubler) je ISTA vrstica kot P82 row 26;
   izrez Kurrent: dve zaprti zanki = 8 (isti vzorec forenzike kot P80
   3-vs-5); starši/otrok/datum potrjeni, hišna št. popravljena v parish.ts.
3. **P79 SIDRO hiša 61 re-verificirano** (row 28, sken 20): oče zdaj »Miko
   Požek« [~] (prej »Miha P.—«/»Miko Jože H.?« — oba branji ohranjena v
   whatSi); mati Bara roj. Filath [~].
4. **NEZAKONSKI vpisi 2** (row 78 hiša 52: mati Marija Muc [~]; row 80 hiša
   55: mati Ana Smič [~] — očeta stolpca PRAZNA); **ANOMALIJA ZAPISA row 93**
   (hiša 35: v očetovem stolpcu »Marija Hrižan ½ zemljašt.«, v materinem
   »Ana Požek« — dve interpretaciji [~]).
5. **Križna povezava dveh knjig — hiša 31:** mrliška 1886 (Katarina Marh,
   P80) + krstna 1887 ×2 (Ana 1./2. 8. Urh/Brodarič + Janez 6. 9. Papič/
   Straus) — edina multi-vpisna hiša leta 1887; priimki čez leta: Šimec
   (1886: 36/39/56/88 → 1887: **34** — NOVA hiša), Straus (mati Margaretha
   @31 + botra Katarina @47), Filak/Filath (mati Bara @61 + babica @52),
   Stubler (mati @78), Požek (očeta @61/@21 + botra @27).
6. **Troi duhovniki 1887:** kapljan Andrej Griebel [~] (14 gribeljskih
   vpisov), župnik Franjo Dovgan (1), **»Jos. Povmij« [~] (4 — nov podpis**);
   babica **Marija Brinec 9×** (gost porekla Brinec: mati 2×, očetje 1×,
   botre/babice).

**Integracija:** `parish.ts` HOUSE_VITALS 41 → **59** (20 celotnega okvira
1887: 19 novih + posodobljeni 61 + re-read 75→78; vsi DOCUMENTED; komentar
P82); **qa-parish.ts**: vzorca qa-p79/qa-p80 ožje opredeljena (P82 scoping —
04105 1886 ∪ 1897 ∪ sidri 61/78; pin P79_PT_IN_SET 75 → 78) + nova kontrola
`qa-p82-parish-baptism-1887` (83. kontrola; celoven neodvisen preracun iz
HOUSE_VITALS × PARISH_BOOKS: okvir/strani, PT 16/3, sidro 61, nezakonski 2,
trojna korekcija, anomalija, multi 31, križna povezava 04894; dve obliki
repo/produkcija po P53/P57/P58) — QA 82 → **83/83**; `atlas.ts` PT_GAP_KNOWN
+ 47/52/55; **p81 pack REGENERIRAN**: CURATED hiša 75 → 78 (sidra proti
popravljenemu whatSi; statistika nespremenjena — 25 hiš, 10/38, isto-hiša 2)
+ `scripts/p80_parish_md_books.py` I7 P82 scoping (vzorec 41/25; vitals 59)
+ `scripts/p82_parish_baptism_1887.py`; dokaz
`research/issue17/parish-baptism-1887.json` (SAMPLE-TRANSCRIPTION-1887;
ročna faza); kartica NI dodana (vzorec P77–P81).

**Poštenost:** prepis je VZOREC (polno leto 1887 + dokaz preloma 1888), ne
celotne knjige (326 skenov). Kurrent branja imen nosijo [~]; hišna št. row
78 = trojna korekcija 52→04→15 [~]; row 12 = 26 [~]; row 26 = 78 (P79 je
prebral 75 — re-read z izrezom); row 93 = anomalija zapisa z dvema
interpretacijama; April 31 (row 28) = zapis kot v knjigi [sic]. Modri pripisi
20. st. dokumentirani ločeno. Številčna usklajenost s PT je OBSERVACIJA, ne
dokaz istovetnosti stavbe (issue #18).

**v7 runtime join NESPREMENJEN** (891/879; disciplina I9). Veriga `p60–p67
+ p70–p82 --check` PASS; tsc 0; ESLint 0; /api/qa dev 83/83 (qa-p82 True).

## §60 — P83: župnija Podzemelj — krstna knjiga 04105, polno leto 1888 (issue #18) — 2026-10-16

**Okvir (P82 nextSteps ①: širitev vzorca po letih):** krstna knjiga 04105,
polno leto 1888 = skeni 27–35 == tiskane strani 26–34 (stran == sken − 1);
vpisi z Griblji na skenih 28–34 (str. 27–33); **prelom 1889**: glava
»1 8 8 9« velikimi ciframi na str. 34 (sk. 35), prvi vpis 1889 = row 1
(3./3. 1., Gradac 8) — leto 1888 ima **92 pisanih vrstic**.

**NOVELA P83 (dokazana metodološka ugotovitev):** **pisane oznake vrstic se
pri prelomu leta ponastavijo na 1.** Dokaz: str. 27 (sk. 28) se začne z
oznako **3** (Januar 16., Griblje 1); str. 34 (sk. 35) z oznako **1**.
Posledica: P82 zapis »prvi 1888 row 107« je **zvezno štetje 106+1**
(konvencija), ne pisana oznaka — pisana oznaka prve 1888 vrstice (Gradac 26)
leži pod raztrganino [~]. Narativi qa-p82 + skripta p82 (tolerantna
primerjava break1888) + P82 dokaz (rowNote) usklajeni; podatki P82 (vrstice
1–106 za 1887) nespremenjeni.

**Vsi vpisi z Griblji 1888: 15 vpisov / 15 različnih hiš** — 1, 8, 13, 21,
24, 29, 44, 56, 57, 69, 72, 78 [~], 79, 83, 85 (hiša 78 v zavihku knjige —
zasidrana prek P79 sidra »75«→78 in P82 zapisa). Skupaj s P79/P80/P82:
**74 vpisov / 45 različnih hiš** čez tri knjige in tri leta. Nove hiše v
vzorcu **5** (1, 72, 79, 83, 85), ponovitve 10. PT klasifikacija **12/3**:
luknja 41–60 = 44/56/57 — **VSE POTRDITVE, 0 novih števil** (44 P80, 56 P80,
57 P79); skupno 11 dokazanih števil luknje čez tri knjige.

**Ugotovitve ①–⑦:**
1. **Ponastavitev številčenja vrstic** pri prelomu leta (zgoraj) — P82
   »row 107« reinterpreted kot konvencija zveznega štetja.
2. **Dve NOVI familiji prihoda po 1825:** **HRAUS/HRAUCELJ** (oče h72 Matija,
   matere h69 Katarina + h85 Marija, botra h57 Marija Hraucelj, babica Neža
   — 3 hiše v enem letu; NI v vesolju 1825) in **POŽEK** (oče h79 Jurij
   *bajtar* + nezakonska mati h21 Marija + botra h79 Barbara; NI v vesolju
   1825; 1887 hišni oče h21 Janez Požek). Nasprotje: **KRIŽAN — 6 prič 1888**
   (oče h85 Marko, matere h79 Katarina + h29 Ana, botre h69 Marko + h13
   Peter + h21 Katarina, babica h24 Marija) **SE povezuje s 1825** (Krišan
   Gregor, Krischan @36 — P81 isto-hiša 0.8333).
3. **hiša 78 — OSKRBAR:** 1886 (P79 sidro) in 1887 (P82) oče gospodinjstva
   Janez Jakobič → 1888 oče **Mihail Poxan [~] »oskrbar«** (opomba o
   prevzemu) — direktni dokaz socio-ekonomske motnje gospodinjstva med
   vzorčnimi leti (issue #18: hiša ≠ družina).
4. **PRVA per-hišna imenska veriga — hiša 13:** 1885 ženin Janez **Jakobič**
   (poročna sidro 04455 sk. 61, P80) → 1886 krstna (04105) + mrliška (04894)
   → 1888 oče Matija **Jakobič** (krstna) — isti priimek na isti hiši čez 3
   leta; hiša 13 postane najmočnejši kandidat za 1825→1886→1888 kronološko
   verigo (P81 NIL-CLAIM velja za 1825↔1886, ne za notranje verige).
5. **NEZAKONSKI vpisi 3/15 (20 %):** h24 (mati Barbara **Melith** [~],
   samata), h56 (mati Ana **Šimec** [~] — Šimec ZNOVA na 56: 1886 mrliška +
   P81 near-miss Schumetz @56 → 1888), h21 (mati Marija **Požek** [~] —
   priimek ist kot 1887 hišni oče Janez Požek). Vsi na hišah z drugačnim
   gospodinjskim priimkom prejšnjega leta.
6. **Kontinuiteta rodov čez leta:** h29 — hiša epidemije 1886 (3 otroci
   **Mileh** umrli v 4 dneh, kolera; P80) → 1888 oče Peter **Milek** (isti
   rod, bralni varianti); h57 — menjava: 1886 Podolivec/Stupanič (P79) →
   1888 Pezdirec/Borjanc; h8 — menjava: 1886 Jakofčič/Meh → 1888 Jang
   Jatkebčič/Marija **Urh** (Urh = 1887 h31 oče + 1888 botra h85); Kure
   (botri h1/h79), Adlešič (botre h29/h24/h69), Brodarič (h57/h78),
   Klobučar (h78 — 1887 h47 oče), Pezdirec (h57 oče + h56 botra; Perdinec
   h13 mati), Deblič (h56/h13 botre).
7. **Anomalije:** otrok **»Kaxmarp«** [~] (h21, moški, nezakonski — morda
   Kasimir); otrok **»Musca«** [~] (h24, nezakonska); otrok **»Alex«** [~]
   (h56, nezakonski) s **nasprotjem spola** (kolone moški [~] proti modri
   marginaliji »Umrla dne 25. 5. 1965« [~]); **dvodelni priimek**
   »Radovič Mrgaič« [~] (h83 — vzporednica 1825 »Šture Majzel« iz P81
   vesolja); botra/polja prazna (h83, h8); marginalije »+ 1878« (h1) pred
   letom rojstva — 7/8 forenzika (morda 1888/1978). Duhovniki: Grieblj [~]
   12 + Povmij [~] 1 + neberljiv »Jos. P—« 1 + prazen 1; babica **Brinec
   10×** (Marija 9 + Ana 1).

**Integracija:** `parish.ts` HOUSE_VITALS 59 → **74** (15 novih 1888; vsi
DOCUMENTED; komentar P83 z novo o ponastavitvi številčenja); **qa-parish.ts**
nova kontrola `qa-p83-parish-baptism-1888` (84. kontrola; celoven neodvisen
preracun iz HOUSE_VITALS × PARISH_BOOKS: okvir/strani, PT 12/3, sidra h13
veriga/h78 oskrbar/h29 Milek, nezakonski 3, veriga hiše 13 čez tri knjige;
dve obliki repo/produkcija po P53/P57/P58) — QA 83 → **84/84**;
`scripts/p80_parish_md_books.py` I7 P83 scoping (vitals 59 → 74);
`scripts/p82_parish_baptism_1887.py` I4 tolerantna primerjava break1888 +
`research/issue17/parish-baptism-1887.json` rowNote; dokaz
`research/issue17/parish-baptism-1888.json` (SAMPLE-TRANSCRIPTION-1888;
ročna faza — skeni v delovnem imeniku, NI v repu); atlas.ts NESPREMENJEN
(PT_GAP_KNOWN že vsebuje 44/56/57); p81 pack NESPREMENJEN (vzorec 1886); 
kartica NI dodana (vzorec P77–P82).

**Poštenost:** prepis je VZOREC (polno leto 1888 + dokaz preloma 1889 + dokaz
ponastavitve številčenja), ne celotne knjige (326 skenov). Kurrent branja
imen nosijo [~] (Zeljth, Hraus/Husič, Hlevič/Nera, Jatkobčič, Poxan/
Hardeium, Radovič Mrgaič, Mettovič, Melith, Borjanc, Jatkebčič, Deblič);
hiša 78 [~] v zavihku; pisana oznaka prve 1888 vrstice pod raztrganino
(ponastavitev dokazana indirektno); nasprotje spola h56 dokumentirano, ne
reševano; marginalije »+ …« z letnicami pred rojstvom (h1/h79) — 7/8
forenzika, obe interpretaciji dokumentirani. Številčna usklajenost s PT je
OBSERVACIJA, ne dokaz istovetnosti stavbe (issue #18).

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…, statična projekcija;
disciplina I9). Veriga `p60–p67 + p70–p83 --check` PASS (p77 prehoden HTTP
000 — retry PASS); tsc 0; ESLint 0; /api/qa dev **84/84** (qa-p83 True).

**P84 RE-READ NOVELA (§61, 2026-10-16):** »HRAUS/HRAUCELJ« iz te sekcije je
STRAUŠ/STRAUCELJ — Kurrent ſt (S+t) brana kot H; familija JE v vesolju 1825
(P81 0.8571); trditev »dve novi familiji po 1825« → ENOVA nova (Požek);
podrobno v §61.

## §61 — P84: župnija Podzemelj — krstna knjiga 04105, polno leto 1889 (issue #18) — 2026-10-16

**Okvir:** širitev vzorca P79 (1886) → P82 (1887) → P83 (1888) na polno leto
**1889**: skeni **35–43 == tiskane strani 34–42** (stran == sken − 1; vpisi na
skenih 35–42; 8 citiranih skenov vse JPEG 200). Prelom **1890**: glava
»Leto 1890« + »1890« v letni celici na str. 42 (sk. 43), prvi vpis 1890 =
row 1 (11./11. 1., Kemelj 17); oznake vrstic se ponastavijo na 1 (novela P83
potrjena 2. leto); leto 1889 ima **106 zveznih vrstic** (str. 34: 1–14;
str. 35: 15–28; str. 36: 29–41; str. 37: 42–54; str. 38: 55–67; str. 39:
68–80; str. 40: 81–93; str. 41: 94–106). Prvi 1890 Griblje vpis = row 6
(h27 Anton, oče Janez Kukhar [~]) — izven vzorca 1889.

**Novela P84 ① — številčenje str. 40:** duhovnikove pisane oznake vrstic so
**PONOVLJENE 68–8x** (napaka — prepis začetka str. 39); kasnejša roka (modri
svinčnik) popravi z **zvezno 81–93** v datumskih celicah (pari hi-res:
label 68 ↔ svinčnik 81; label 69 ↔ 82 …); str. 41 nadaljuje **94–106 zvezno**
— neodvisna potrditev, da so svinčnikove številke pravilne (93 + 1 = 94).
P82 »row 107« = zvezno štetje — konvencija ohranjena.

**Novela P84 ② — RE-READ P83:** »**HRAUS/HRAUCELJ**« je pravzaprap
»**STRAUŠ/STRAUCELJ**« — v isti p83 vrstici (sk. 28, row 8) babica jasno
**»Neža Straucelj«**; Kurrent **ſt (S+t) brana kot H**; dokazana z 1889
ponovitvijo istih oseb (h72 oče Matija Strauš 1888 = 1889 P84 row 64; h57
botra Marija Straucelj 1888 = 1889 P84 row 55; babica Neža Straucelj h72).
Posledica: familija **JE v vesolju 1825** (P81 0.8571 — Strauß @45/71/72 +
ATLAS 76/79/81–84/92) — P83 trditev »dve novi familiji po 1825« se popravi na
**ENOVO novo (Požek)**; P83 dokaz + HOUSE_VITALS + qa-p83 narativi popavljeni
vidno (z zgodovino branja ohranjeno, ne tiho).

**Vsi vpisi z Griblji 1889: 19 vpisov / 16 imenovanih hiš + 2 neberljivi**
(row 70 hišna št. obrabljena — sledi »///«; row 82 prekrita z imenom »Marjeta«
+ modro marginalijo — evidence-only, ne projicirana v HOUSE_VITALS):
58, 33, 3 [~], 64 ×2, 35, 69, 59 [~], 63, 57, 32, 72, 2, 8 [~], 83 [~], 65,
26 [~]. **Nove hiše 5** (58, 33, 3, 32, 64) + 2 neberljivi, **ponovitve 11**;
skupaj s P79/P80/P82/P83 vzorec **93 vpisov / 50 hiš** čez tri knjige in
štiri leta (1886–1889).

**PT klasifikacija 13/3:** v naboru 13 (2, 3, 8, 26, 32, 33, 35, 63, 64, 65,
69, 72, 83); luknja 41–60: **58 NOVA** (row 3 — dve zaprti zanki = 8, vzorec
forenzike P82 75→78) + **59 POTRDITEV** (P80; row 33 [~]) + **57 POTRDITEV**
(P79; row 55) — luknja zdaj **12 dokazanih števil** čez tri knjige.

**Nezakonski 1/19 + anomalija:** row 33 (h59 [~]) mati Katarina Podirec [~]
(»a samka?«), očeta stolpec PRAZEN; **ANOMALIJA row 70**: mati Marija Šimec
[~] »**samka hči**« × oče Janez Jakobič [~] »**šefur**« (služabnik) — povezava
dveh gospodinjstev; otrok »Ožbolt?« [~]; hiša neberljiva.

**Sidra:** ① **hiša 63** (row 53, sk. 38): botr **Janez Šimec [~]** — hiša 63 =
ATLAS 1825 Šimec @63 + PT lastnik »Šimec Ripane« @63 (P81 pack) → **neposredna
1825↔1889 imenska + hišna povezava**; ② **row 82**: babica **Ana Filak [~]** —
P81 1.0 priča (PT 69/71 + PUA Fillah 16/34/36/61); ③ **row 89 = h8**: botr
**Janez Dragoš [~]** — P81 1.0 (PT Dragosch 3/4/5); mati Marija Urh [~] ISTA
kot 1888 (h8 2. leto); ④ **h72 re-read veriga**: oče Matija Strauš 1888 + 1889.
**Šimec najtrajnejša familija**: mati row 70 (samka) + botr row 53 (h63 =
ATLAS hiša!) + botra row 75 (h2) — 3 pojavi; priimki z 1825 pričo v 1889:
Dragoš 2× (1.0), Strauš/Straucelj 6× (0.8571 + re-read), Šimec 3× (1.0),
Brinec 9× (0.8333 [~]), Filak 1× (1.0), Hrižan/Križan [~] 4× (0.8333 — babica
z naslovom hiše: »Ana Hrižan, Griblje št. 63« — 4. pojav!), Jakobič 4× (veriga
h13), Milek 2× (near-miss Mileh). Duhovniki: Griebel [~] 7 + Povmij [~] 8 +
neberljivo 4 (raztrganine); babice: Brinec 7× + Ana Hrižan [~] 4× + Sotter 2×
+ Kure/Tržan/Filak po 1×.

**Integracija:** `parish.ts` HOUSE_VITALS 74 → **91** (17 zasidranih 1889;
2 neberljivi evidence-only; vsi DOCUMENTED; komentar P84 z novelama) +
**RE-READ popravki 3 P83 whatSi/whatEn** (h72/h69/h85 Hraus→Strauš z
zgodovino); `src/lib/atlas.ts` PT_GAP_KNOWN += **58**; **qa-parish.ts**
nova kontrola `qa-p84-parish-baptism-1889` (85. kontrola; celoven neodvisen
preracun: okvir/skeni/strani, PT 13/3, sidra h63 Šimec=ATLAS/h8 Dragoš/h72
re-read, multi-vpisna h64, nezakonski h59, ponovitve 11 prek vitals; dve
obliki repo/produkcija po P53/P57/P58) + qa-p83 narativi (re-read novela) —
QA 84 → **85/85**; `scripts/p80_parish_md_books.py` I7 P84 scoping (vitals
74 → 91); dokaz `research/issue17/parish-baptism-1889.json`
(SAMPLE-TRANSCRIPTION-1889; ročna faza — skeni v delovnem imeniku, NI v
repu); P83 dokaz `research/issue17/parish-baptism-1888.json` RE-READ blok
(provenienca); p81 pack NESPREMENJEN (vzorec 1886); kartica NI dodana
(vzorec P77–P83).

**Poštenost:** prepis je VZOREC (polno leto 1889 + dokaz preloma 1890 + dokaz
številčenja str. 40), ne celotne knjige (326 skenov). 2 vpisa brez hišne
številke (neberljivi) — evidence-only; row 93 datumi pod trakom (november po
kontekstu); row 18 hiša dvoumna (»mölüo?/3« + »Tomma Vrh'möz« [~]); Kurrent
branja imen nosijo [~] (Požek, Dragoš, Strauš, Županič?, Cojmar?, Hrigian?,
Vehbiščar?, Bahorič?, Hengan?, Žefran?, Trojžif?, Radovič …); re-read P83
dokumentiran z novelo + provenienco, ne tiho; MERI, NE odloča (issue #18).

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…, statična projekcija;
disciplina I9). Veriga `p60–p67 + p70–p84 --check` PASS (p77 prehoden HTTP
000 — retry PASS); tsc 0; ESLint 0; /api/qa dev **85/85** (qa-p84 True).

## §62 — P85: župnija Podzemelj — krstna knjiga 04105, polno leto 1890 (issue #18) — 2026-10-16

**Faza**: P85 (SAMPLE-TRANSCRIPTION-1890; MERI, NE odloča; v7 join nespremenjen).
**Sprožilec**: P84 nextSteps ① — širitev vzorca po letih (krstna 1890).
**Vir**: Matricula Online, krstna knjiga **04105 1886–1919** (Nadškofijski arhiv
Ljubljana; 326 skenov). Paleografska faza ročna: skeni 43–53 v delovnem
imeniku `/tmp/p85` (NI v repu); hi-res izrezi 2× za vseh 24 Griblje vrstic
(L+R) + tarčna forenzika hišnih številk, statusov, mesec-stolpca (7 strani z
autocontrast) in podpisov.

**Okvir leta 1890**: skeni **43–49 == tiskane strani 42–48** (stran == sken − 1;
vpisi na skenih 43–49). **Prelom 1891**: velike cifre **»1891.« + podčrtaj +
»Januarj« na str. 48, row 1 po row 86** — zadnji 1890 vpis row 86 (23./24. 12.,
Podremelj 4 Jožef); prvi 1891 vpis row 1 (11./11. 1., Krasinec 28 Anton).
Oznake vrstic ponastavljene na 1 — **novela P83 POTRJENA 3. leto**. Leto 1890
ima **86 zveznih vrstic** (str. 42: 1–12; 43: 13–25; 44: 26–38; 45: 39–52;
46: 53–64; 47: 65–77; 48: 78–86). Glave mesecev se ponavljajo (Marec 2×, April
2×, Junij 2×) — vzorec ponavljajočih glav (novela P84 str. 40).

**NOVELA P85 — STATUS = ULOMEK**: Kurrent znak pred »zemljak«, ki so ga P79–P84
brale kot »ž zemljaf/zemljak«, je z jasnimi hi-res izrezi 1890 **ulomek ½ (ali
¼)** — **15/24 vpisov**; isti znak, ki ga je P84 row 3 brala »¼ zemljišč«.
Socio-ekonomska slika 1890: malokmetje (ulomki) + **bajtarja** (r47, r71) +
**čevljar** (r42 Miha Lozar — prvi obrtnik v vzorcu) + **učitelj** (r79 — šolska
hiša 90) + **mežnar iz Adlešič** (r54 — zunanji prihajnik).

**Vsi vpisi z Griblji: 24 / 19 imenovanih hiš + 3 neberljive** (r31 + r75
prekriti z modrimi pripisi 20. st.; r77 na rezanem robu str. 47 — evidence-only;
HOUSE_VITALS **21 zasidranih**): 27, 31, 47, 24, 58, 71, 38, 15, 77, **30 ×2
(DVOJČKA — prvi v vzorcu!)**, 7, 69, 55, 32, 11, **41 ×2 (multi-vpisna — dve
različni družini)**, 63, 90, 35. Nove hiše **6** (7, 30, 38, 41, 77, 90);
ponovitve 13. Skupaj s P79–P84 vzorec **117 vpisov / 56 hiš čez tri knjige in
pet let** (konvencija verige P82–P84; zasidrani-only: 112 vpisov / 55 hiš).

**PT klasifikacija 15/4** — luknja 41–60: **41 NOVA** (rows 71+72 — prvi dokaz
št. 41 v vzorcu!) **+ 47/55/58 POTRDITVI** — dokazanih števil luknje skupaj
**13**. Vseh 4 luknjane številke 1890 ima zakonske družine (41 Muc bajtar +
Hrušič ½; 47 Klobučar×Filak; 55 **Šimec**×Pendirec; 58 Pošek/Požek×Dragoš).

**Ugotovitve ①–⑨**:

1. **24 vpisov / 19 hiš + 3 evidence-only**; skupaj 117/56.
2. PT 15/4; luknja 13 dokazanih števil (41 NOVA).
3. Nove hiše 6; multi-vpisni **h30 (dvojčka Milek)** + **h41 (dve različni
   družini — 3. primer po h36 1886, h64 1889)**.
4. **SIDRA**: **h77** — oče **Jurij Pošek/Požek bajtar = P83 sidro h79 oče
   (1888)** + botra **Barbara Požek = P83 h79 botra** → Požek veriga 79→77
   (bajtar na drugi št.; 3. leto familije); **h71** — oče **Jurij Straus** (tri-
   virska hiša P80 + PUA Strauß Niklo @71, P81 0.8571 — 1890 živ oče); **h63** —
   oče **Nikolaj Križan** (prvi KRIŽAN hišni oče v vzorcu; na P84 Šimec ATLAS
   sidru — 4. gospodinjstvo na 63); **h55** — oče **Nikolaj Šimec** (Šimec
   zdaj tudi na luknji 55 — 6. hiša najtrajnejše familije).
5. **ČEZ-LETNA POTRDITEV ANOMALIJE**: r85 (h35, 19. 12.) = **isti vzorec kot
   P82 row 93 (1887)** — očetov stolpec »Marija Hrižan ½ zemljak« × materin
   »Ana Požek« na isti hiši 35 v obeh letih; 1890 otrok brez imena (»N. moškega
   spola«), krst 17. prečrtan. + r19 (h24): očetov stolpec »Marija Brinec ½
   zemljak« — druga anomalija istega tipa.
6. **Dvojčka h30** (rows 51+52, 13./13. 6., Janez + Marija Milek): r52 †19/6/90
   (6 dni), r51 †2/6/93; Milek rod h29 (1886 epidemija, P80; 1888 sidro P83) →
   h30 (1890).
7. **Priimki z 1825 pričo v 1890**: Strauš **7×** (0.8571), Šimec **4×** (1.0),
   Križan/Hrižan **6×** (0.8333 [~]), Dragoš 2× (1.0), Brinec 3× gospodinjsko +
   babica 11× (0.8333 [~]), Filak 1× (1.0), Milek 2× (near-miss), Klobučar 4×,
   Urh 2×, Požek 7× (nova familija 1888 — 3. leto), Pendirec/Pegdirec 9×.
8. **Duhovniki**: Jos. Rauq [~] 19 (isti tip pisave, ki ga je P84 brala
   »Griebel/Povmij« [~] — Kurrent podpis na ločljivosti skena) + Jos. G— [~] 1 +
   **C. g. Jurcan Šašelj, župr v D. Lazič** [~] 1 (obiskni — edini popolnoma
   berljiv podpis) + prazna 2. Babice: **Marija Brinec 11×** (4. leto zapored) +
   Šotter 6× + Ana Križan 2×.
9. **RE-READ P84 okvir note**: oče r6 = **»Janez Stubhar«** [~] (P84 »Janez
   Kukhar« [~]) — isti vpis; Kurrent St/K. Mesec r6 = JANUAR (P84 »6./7. 1.«
   pravilno; potrjeno z mesec-stolpcem: februar glava šele str. 43 row 13).

**Skripta** `scripts/p85_parish_baptism_1890.py` (deterministični verifikator,
I1–I10, **--check PASS**: knjiga 200 + inventar 326, citirani skeni 7/7 JPEG
200, okvir + prelom 1891 + ponastavitev oznak, PT 15/4 z NOVO 41, sidra
h77/h71/h63/h55 + anomaliji h24/h35 == P82 row 93, dvojčka h30 + multi h41,
13 ponovitev + 6 novih prek vitals, sampleTotal 117/56, runtime projekcija 21/
112, brez »Hraus« v aktivnih whatSi) + **dokaz**
`research/issue17/parish-baptism-1890.json` (SAMPLE-TRANSCRIPTION-1890; ročna
faza — skeni v delovnem imeniku, NI v repu).

**Integracija**: parish.ts HOUSE_VITALS 91 → **112** (21 zasidranih 1890 + 0
re-readov; vsi DOCUMENTED; komentar P85 z novelo) + qa-parish.ts
**qa-p85-parish-baptism-1890** (86. kontrola; celoven neodvisen preracun:
okvir/prelom/ponastavitev, PT 15/4, sidra h77 Požek = P83 h79/h71 PUA @71/h63
ATLAS/h55 luknja, dvojčka h30, multi h41, anomaliji h24+h35 == P82 row 93,
13 ponovitev, NOVE hiše brez preteklosti; dve obliki repo/produkcija po
P53/P57/P58) + atlas.ts PT_GAP_KNOWN **+ 41** + scripts/p80_parish_md_books.py
I7 P85 scoping (vitals 91 → 112). **LEKCIJE (6. primer pincev lovijo napake)**:
① pin P85_PT_IN_SET brez hiše 71 (71 JE v PT naboru 1–40+61–99!) — ujel
qa-p85 runtime (»PT ≠ 15/4 (15/4)« — pogoj in sporočilo desinhronizirana);
② ponovitev h15 1886 pripisana 04105 namesto mrliški 04894 (P80) — ujel pin
ponovitev; tsc ujel zaključni `}` funkcije parishChecks po prilimanju bloka.
Vse sanirano.

**P85 nextSteps**: ① krstna 1891 (skeni 49+, str. 48 row 1 = prvi 1891 vpis);
② h63 deep-dive (ATLAS/PT/PUA 63/64/66 + krstni vpisi — polna per-hišna veriga
najmočnejšega sidra); ③ per-hišne verige h77/h79 Požek, h29/h30 Milek, h71
Strauš, h8/h32 Urh; anomalija h35 — preveriti 1885 (poročna) in 1891 za
Marijo Hrižan; ④ rešitev Pošek/Požek prek poročne 04455 [~].

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…, statična projekcija;
disciplina I9). Veriga `p60–p67 + p70–p85 --check` PASS (vse exit 0); tsc 0;
ESLint 0; /api/qa dev **86/86** (qa-p85 True).

---

## §63 — P86: župnija Podzemelj — krstna knjiga 04105, polno leto 1891 (issue #18) — 2026-10-16

**SAMPLE-TRANSCRIPTION-1891** (MERI, NE odloča; v7 join nespremenjen).
P85 nextSteps ①: širitev vzorca po letih (P79 1886 → P82 1887 → P83 1888 →
P84 1889 → P85 1890 → **P86 1891**).

**Okvir**: skeni 49–56 == tiskane strani 48–55 (stran == sken − 1); leto se
začne na str. 48 row 1 po 1890 rows 78–86; vpisi na skenih 50–54; **glava
»Leto 1892« na str. 55 row 1** — oznake se ponastavijo na 1, **novela P83
potrjena 4. leto**; leto 1891 ima **75 zveznih vrstic**; glave mesecev se
ponavljajo (Avgust 2×, November 2× — vzorec P84 str. 40). Skeni 49–63 v
delovnem imeniku /tmp/p86 (ročna faza, NI v repu); hi-rez izrezi 2x–4x za
vse Griblje vrstice (vzorec p85_crops).

**Vsi vpisi z Griblji**: **10 vpisov / 9 imenovanih hiš + 1 neberljiva**
(r52 prekrita z modrimi pripisi — evidence-only; HOUSE_VITALS 9 zasidranih,
112 → **121**): **72, 30, 62, 61, 53, 2, 31, 5, 28** — **NOVE hiše 2
(28, 53)** + 1 neberljiva, **ponovitve 7** (h2 ×3 leta; h30 kontinuiteta;
h31 ×4; **h5 ČEZ KNJIGE** — mrliška 04894 1886; h61 1887+1897+1891; h62
1887; h72 1888). Skupaj s P79–P85 vzorec **127 vpisov / 58 hiš čez tri
knjige in šest let**. **NOVELA (novela P85 potrjena 2. leto): VSI 9
zasidranih statusov = ¼ ulomek** (zemljak 5, gemžgah 4 — brez bajtarjev/
obrtnikov na Gribljih, kontrast 1890).

**PT klasifikacija 8/1** — **luknja 41–60: 53 NOVA (r40; forenzika izrez
4x: jasno 53 — prvi prebir »33« [~], Kurrent 3/5), 14. dokazana številka**
(atlas.ts PT_GAP_KNOWN + 53).

**SIDRA** — ① **h72** (r6): oče **Matija Straus [~] = ISTI očet kot P83
1888** (re-read Hraus→Strauš); **mati MENJANA: 1888 Barbara Husič [~] →
1891 Marija Jakobič [~]**; tri-virska P80 + PUA Strauß Niklo @71 (P81
0.8571); botra Matija Straucelj. ② **h30** (r21): oče **Janez Milek [~] +
mati Marjeta Pozdirec [~] = P85 dvojčka rows 51+52 — POPOLNA DVOLETNA
KONTINUITETA (isti starši + ISTA botra Matija Milek + Katarina Križan)**;
Milek = P81 near-miss (0.55–0.72). ③ **h61** (r39): oče **Nikolaj
Pošek/Požek [~] = P82 SIDRO 1887 Miko Požek — ISTA OSEBA po 4 letih**;
**mati MENJANA: 1887 Bara Filak → 1891 Ana Dragos [~ Dragoš] — PRVI dokaz
menjave gospodinjstva na zasidrani hiši** (3 krstni vpisi 1887+1897+1891);
edini vpis brez botre in podpisa; †1/8 91 [~]. ④ **h53** (r40): oče Janez
Pozdirec [~] × mati Marija Križan [~] — NOVA LUKNJA (glej zgoraj). ⑤ **h2**
(r43): oče Peter Hlebec [~] — **TROJNA KONTINUITETA P82 1887 + P84 1889 +
1891, ISTI starši ×3 čez 5 let**. ⑥ **h31** (r50): mati **Marjeta Straus
[~] — ISTA OSEBA 1887 Margaretha + 1890 + 1891 (3 vpise čez 5 let)**; oče
1887/1890 Papič [~] → 1891 Tepič [~] (Kurrent P/T [~]); botra Klobučar
(4. leto). ⑦ **h5** (r51): vsi **TOREC** — ponovitev čez knjige (mrliška
1886: umrla Barbara Brinec 2 leti → Torec 1891 = menjava gospodinjstva);
modro ime »Terezija?« [~] vs tmavo »Jožefa«. ⑧ **h28** (r56): oče **Jurij
Požek [~] — POŽEK VERIGA h79 1888 → h77 1890 → h28 1891 (3. hiša familije
v 4 letih)**; mati Milkovič [~] = Milek varianta.

**DVE menjavi matere na zasidranih hišah** (h61 Filak→Dragos + h72
Husič→Jakobič) — nov tip čez-letnega dogodka (druga žena / ponovna poroka /
re-read [~], MERI). **Šimec 0× — PRVO leto brez najtrajnejše familije**
(1886: 4 hiše, 1887: 1, 1888: 1, 1889: 3, 1890: 6). Priimki z 1825 pričo v
1891: **Križan/Hrižan 8× (0.8333 [~] — najmočnejše leto familije)**,
Milek/Milkovič 4×, Straus/Straucelj 3+1 [~] (0.8571), Požek/Pošek 2× (4.
leto), Dragoš 1× (1.0), Urh 1× [~] (1.0), Jakobič/Jaklpič 2×; Brinec
babica 2× (6./7. leto). Duhovniki: Jos. Rauq [~] 7 + Jos. R— 1 + prazna 1;
**NOV podpis St. Češarek [~] od r68** (sredi decembra 1891 — menjava, 0× na
Gribljih). Babice: Ana Hrižan 4× (vrnitev po 1889) + Brinec 2× + Marjeta
Fojter 2× (nova).

**SKRIPTA** `scripts/p86_parish_baptism_1891.py` (deterministični
verifikator, I1–I10, --check PASS: knjiga 200 + inventar 326, citirani
skeni 5/5 JPEG 200, okvir + prelom 1892 + ponastavitev oznak, PT 8/1 z
NOVO 53, sidra h72/h30/h61/h53/h2/h28/h31/h5, čez-letne kontinuitete prek
dokazov P82/P83/P85, runtime projekcija 9/121, brez »Hraus« v aktivnih
whatSi) + dokaz `research/issue17/parish-baptism-1891.json`
(SAMPLE-TRANSCRIPTION-1891; ročna faza — skeni v delovnem imeniku, NI v
repu). **INTEGRACIJA**: parish.ts HOUSE_VITALS 112 → **121** (9 zasidranih
1891; vsi DOCUMENTED; komentar P86 z novelo) + qa-parish.ts
**qa-p86-parish-baptism-1891** (87. kontrola; celoven neodvisen preracun:
okvir/PT 8/1/sidra h72–h28/kontinuiteta h30 prek 1890 blokov/trojna
kontinuiteta h2/menjava matere h61 prek 1887 bloka/ponovitve vključno h5
04894/NOVE hiše brez preteklosti/vitals 121; dve obliki repo/produkcija po
P53/P57/P58) + atlas.ts PT_GAP_KNOWN **+ 53** + scripts/
p80_parish_md_books.py I7 P86 scoping (vitals 112 → 121) + p85 skripta I10
kumulativno (127; klasifikacija v pre-P86 vesolju — h30 ostaja nova za
P85 dokaz). **LEKCIJE (7. primer pincev lovijo napake)**: ① prvi prebir
r21 »h40/Mlešič« — izrez 4x: jasno **h30/Milek** (kontinuiteta P85!); ②
prvi prebir r40 »h33« — izrez 4x: jasno **h53** (nova luknja!); ③ sed
korupcija `[hn, yr, sig]` for-loop (tsc/tsc-dev ujel); ④ aritmetika
sampleTotal 126 → **127** (117 + 10). Vse sanirano; veriga p60–p67 +
p70–p86 --check PASS (vse exit 0; p68 zamrznjen po C2); tsc 0; ESLint 0;
/api/qa dev **87/87** (qa-p86 True).

**P86 nextSteps**: ① krstna 1892 (skeni 56+, glava na str. 55 row 1 — skeni
že v /tmp/p86); ② per-hišne kronologije tri-virskih hiš 13/36/71 (issue #18
najmočnejši mostovni kandidati) — še vedno odprto; ③ mrliška 04894 leta
1887–1892: smrti prvih žena (h61 Filak? h72 Husič?) kot dokaz menjav
gospodinjstev; ④ luknja 41–60: 14 dokazanih števil.

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…, statična projekcija;
disciplina I9).

## §64 — P87: župnija Podzemelj — krstna knjiga 04105, polno leto 1892 (issue #18) — 2026-10-16

**SAMPLE-TRANSCRIPTION-1892** (MERI, NE odloča; v7 join nespremenjen).
P86 nextSteps ①: širitev vzorca po letih (P79 1886 → P82 1887 → P83 1888 →
P84 1889 → P85 1890 → P86 1891 → **P87 1892**).

**Okvir**: skeni 56–63 == tiskane strani 55–62 (stran == sken − 1); glava
**»Leto 1892« na str. 55 row 1** po 1891 rows 65–75; vpisi na skenih 56, 57,
60, 61, 62 (58/59 brez Gribljev); **velike cifre »1893~« na str. 62 po row
82** — oznake se ponastavijo na 1, **novela P83 potrjena 5. leto**; leto 1892
ima **82 zveznih vrstic**; glave mesecev se ponavljajo (Avgust 2×, November
2×). Skeni 49–63 že v delovnem imeniku /tmp/p86 (ročna faza, NI v repu);
hi-rez izrezi 2x–4x za vseh 12 Griblje vrstic + forenzika (r60 izrez 2x
jasno **58** — prvi prebir »53« [~], lekcija P86 Kurrent 3/5; r80 izrez 4x
kraj jasno **Griblje** — modri pripisi 20. st. so mrliški, ne kraj).

**Vzorec 1892 — NARE**: **12 vpisov / 12 hiš** (prvo leto brez ponovitev
znotraj leta; 0 neberljivih): 75, 29, 73, 12, 27, 1, 32, 58, 90, 63, 61, 24.
Nove hiše 3 (**12, 73, 75** — prvi dokaz čez tri knjige) + ponovitve 9.
Skupaj s P79–P86: **139 vpisov / 61 hiš čez tri knjige in sedem let**.
NOVELA: statusi ulomki — **novela P85 potrjena 3. leto** (½ zemljak 5 +
¼ zemljak 4 + bajtar 2 — vrnitev po 1891: 0 — + učitelj 1). PT klasifikacija
**11/1** (58 v luknji 41–60 — že dokazana P84/P85; **brez novih** luknjanih
števil, ostaja 14). 0 nezakonskih; r70 h61 edini vpis brez botre + brez
podpisa (**isti vzorec kot 1891 r39 na isti hiši**).

**Sidra**:
- **h58** — oče Janez Požek [~] × mati Ana Dragos [~ Dragoš]: **Požek ×
  Dragos 3. LETO na isti hiši** (1889 Franz + 1890 Janez + 1892 Janez) —
  najdaljša zasidrana zveza familije Požek; forenzika jasno 58;
- **h61** — oče Nikolaj Požek [~] ½ × mati Ana Dragos [~]: **KONTINUITETA
  SIDRA 2. LETO** (P86 1891 ISTA zveza + ISTI vzorec brez botre/podpisa);
  status ¼→½ [~] — **menjava statusa na zasidrani hiši** (nov fenomen [~]);
  P82 sidro 1887 + 1897 + 1891 + 1892;
- **h63** — oče Nikolaj Hrižan [~] ¼: **ISTI OČE (ime+priimek) 4×** (1887
  Prižan [Križan] + 1889 Hrigian? [nezakonska] + 1890 Križan ½ + 1892
  Hrižan) — najmočnejši čez-letni očetovski pin (P85 sidro potrjeno;
  Kurrent K/H varianta); mati Pegdirec [~] ≈ 1889 Pezdirec [~];
- **h29** — oče Peter Milek [~] × mati Ana Križan [~]: **ISTA ZVEZA
  1888+1892** (P84 1888 »hiša epidemije«; mrliška 04894 1886: trije Mileh
  otroci v koleri); status ½→¼ [~];
- **h1** — oče Nikolaj Željko [~] × mati Katarina Kure [~]: **ISTA ZVEZA
  1888+1892** (P83 »Zeljth« [~] — re-read); **najnižja hišna številka v
  vzorcu**; botra = ista priimka kot starši;
- **h32** — oče Matija Urh [~]: **ISTI OČE 3×** (1889+1890+1892) — Urh
  veriga 1887–1892 (6 let); PUA urh 1.0; mati Pezdirec/Pegdirec vseh 3 let;
- **h90** — **ŠOLSKA HIŠA**: oče Franc Kopitac [~] učitelj × Marija
  Schweizer [~] — **ISTA UČITELJSKA DRUŽINA 1890+1892**; botra Janez Barle
  **nadučitelj** (prvi v vzorcu) + Marija Trotter sopuga;
- **h24** — oče Martin Jurajevič [~] bajtar: **MENJAVA GOSPODINJSTVA**
  (Brinec gospodinjstvo 1887 + anomalija 1890 → Jurajevič 1892; 4. vpis);
  forenzika 4x: kraj jasno Griblje, modri pripisi so mrliški;
- **h27** — oče Marko Pozdirec [~] bajtar: **MENJAVA GOSPODINJSTVA** (oče
  1887 Kukar [~] = 1890 Stubhar [~] ISTI (re-read) → 1892 Pozdirec; 3. vpis).

**Ostalo**: Dragos/Dragoš 2. hiša familije (h58+h61 mati + h12 oče Janez
Dragos); **ŠIMEC 0× 2. leto zapored** (1891+1892 — 1886: 4, 1887: 1, 1888: 1,
1889: 3, 1890: 6, 1891: 0, 1892: 0); babice: Marija Brinec 4× (8.–10. leto)
+ Ana Križan 3× + Marjeta Trotter 2× (nova) + Ana Krajnovec 1×; duhovnika
**SOČASNO aktivna 1892**: Fr./St. Češarek [~] 8 (Jan–Sep) + Jos. Rauq [~] 3
(Feb!, Okt–Dec) + prazna 1 — **menjava P86 decembra 1891 NI dokončna**; r13
podpis celo ime »Franc Češarek« [~] (P86 »St.«); modri pripisi 20. st. kot
genealoški vir: 4 smrti + 1 poroka (r8 6.7.1952; r11 20.4.1958 [~]; r20
poročena 5.5.1919; r68 24.2.1967; r80 1968 Gradac) — evidence-only; r70
(h61) datumi na razdrapanem robu strani — rojstva 25 [~], † 24/9. 9? [~].

**Integracija**: `research/issue17/parish-baptism-1892.json` (dokaz;
SAMPLE-TRANSCRIPTION-1892) + `scripts/p87_parish_baptism_1892.py` (I1–I10,
--check PASS: knjiga 200 + inventar 326, citirani skeni 5/5 JPEG 200, okvir
+ prelom 1893 + ponastavitev oznak, PT 11/1, sidra h58/h61/h63/h1/h32/h90/
h24/h27, čez-letne kontinuitete prek dokazov P82/P83/P84/P85/P86 — h61 ISTI
vzorec brez botre/podpisa, h29 ISTA zveza, h63 1889 Hrigian + 1890 Križan,
h32 1889+1890, brez »Hraus«) + `parish.ts` HOUSE_VITALS 121 → **133** (12
zasidranih 1892; vsi DOCUMENTED; komentar P87) + **qa-p87-parish-baptism-
1892** (88. kontrola; celoven neodvisen preracun: okvir/PT 11/1/sidra/
kontinuitete 14 pinov vključno h63 1889 Hrigian + h24 1887 Brinec/1890
ANOMALIJA/NOVE hiše brez preteklosti/vitals 133; dve obliki repo/produkcija)
+ qa-p86 vitals pin 121 → 133 + qa-p85 h90 dovoli 1892 blok (P87 kontinuiteta)
+ atlas.ts PT_GAP_KNOWN komentar (58 ponovitev, brez novih) + p80 skripta I7
P87 scoping (vitals 133) + p85 skripta I10 kumulativno (139; vesolje brez
1891/1892 blokov) + p86 skripta I10 kumulativno (139; hiše 60). Kartica NI
dodana (vzorec P77–P87). Lekcije (8. primer): ① prvi prebir r60 »53« →
izrez jasno 58 (Kurrent 3/5 — ista lekcija kot P86 r40); ② p85 qa NOVA hiša
90 padla na 1892 blok → dovoljen kontinuitetni blok (vzorec P86 h30); ③
nepravilni kontekstni grep h24/h27/h32 (±okno vključi sosednje bloke) →
narrativi popravljeni iz neposrednega parserja (h29 ISTA zveza Milek ×
Križan 1888+1892; h32 Urh 3×; h63 oče 4×; h24/h27 menjava gospodinjstva —
ne multi-familija); veriga p60–p67 + p70–p87 --check PASS (25 skript, vse
exit 0; p68 zamrznjen po C2); tsc 0 / lint 0; /api/qa dev **88/88**
(qa-p87 True).

**nextSteps**: ① P88 = leto 1893 (prelom str. 62 row 1; skeni 63+); ②
per-hišna kronologija tri-virskih hiš 13/36/71; ③ mrliška 04894 1887–1892
(smrti prvih žen — dokaz menjav gospodinjstev h24/h27); ④ luknja 41–60;
⑤ h1 Željko + h29 Milek × Križan: PUA/ATLAS presek.

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…, statična projekcija;
disciplina I9).

## §65 — P88: župnija Podzemelj — krstna knjiga 04105, polno leto 1893 (issue #18) — 2026-10-16

**SAMPLE-TRANSCRIPTION-1893** (MERI, NE odloča; v7 join nespremenjen).
P87 nextSteps ①: širitev vzorca po letih (P79 1886 → P82 1887 → P83 1888 →
P84 1889 → P85 1890 → P86 1891 → P87 1892 → **P88 1893**).

**Okvir**: skeni 63–70 == tiskane strani 62–69 (stran == sken − 1); glava
**»1893~« na str. 62** po 1892 row 82; vpisi na skenih 63–68; **velike
cifre »1894« na str. 69 po row 83** — oznake se ponastavijo na 1, **novela
P83 potrjena 6. leto**; leto 1893 ima **83 zveznih vrstic**. Skeni 64–73
preneseni v delovni imenik /tmp/p88 (63 kopiran iz /tmp/p86; ročna faza, NI
v repu); hi-rez izrezi 2x–5x za vseh 17 Griblje vrstic + forenzika hišnih
številk 5x (r15 jasno **65** — prvi prebir 60 [~]; r33/r34 jasno **27** —
prvi prebir 24 [~]; vertikalni pripis **»dvojčice«** med r33/r34).

**Vzorec 1893**: **17 vpisov / 16 hiš** (h27 DVOJČICI — Antonija †13/9.93 +
Ivana, vsi starševski stolpci r34 »isto«; 2. dvojčki v vzorcu po P85 h30,
prvi z eksplicitnim pripisom): 60, 65, 41, 70, 23, 91, 27 ×2, 15, 46, 72,
30, 24, 74, 21, 25, 32. NOVE hiše 4 (**23, 46, 70, 91**) + ponovitve 12
(h60 nova krstna — poroka 04455 1886 Maria Bohor GRIBLJE 60). Skupaj s
P79–P87: **156 vpisov / 65 hiš čez tri knjige in osem let**. NOVELA:
ulomki — **novela P85 potrjena 4. leto** (½ zemljak 13 + ¼ zemljak 4; brez
bajtarjev/obrtnikov). PT klasifikacija **13/3** — **46 NOVA (15. dokazana
številka luknje!)**; 41 že dokazana (P85; 1893 3. vpis), 60 že dokazana
(P80 poroka; 1893 prvi krstni vpis). 0 nezakonskih; r50 brez babice
(edini); r34 ditto.

**Sidra**:
- **h72** — oče Matija Strauš [~]: **SIDRO 3. VPIS — ISTI oče 3× čez 6
  let** (1888 P83 sidro + 1891 P86 + 1893); mati 1891+1893 ISTA Marija
  Jakobič (1888 Husič menjana); botra Straucelj ISTA 2×; tri-virska hiša
  P80 + PUA Strauß Niklo @71 (P81 0.8571) — **najmočnejša veriga vzorca**;
- **h65** — oče Matija Milek [~]: **ISTI 3×** (1887+1889+1893; mati
  variante Požek/Trojžif?/Jožek? [~]); Milek = P81 near-miss;
- **h27** — **DVOJČICI** (vertikalni pripis); oče Janez Stukar/Stubhar [~]
  = 1887 Kukar + 1890 Stubhar **ISTI** (Kurrent varianta); ISTA mati
  Katarina Klobučar — 3.+4. vpis; forenzika 5x jasno 27;
- **h21** — oče Janez Požek [~] **ISTI** 1887+1893; **MATI MENJANA** (1887
  Marija Brinec → 1893 **Ana Šimec** — 3. dokazana menjava matere po
  h61/h72); **ŠIMEC NAZAJ NA GRIBLJIH** — mati + botra Janez Šimec prvič
  od 1890 (Gerišče 1893 oče Janez Šimec = ISTI? [~]); Požek 6. leto;
- **h24** — Matija Brinec [~] × Barbara Jakobčič [~]: **ISTA ZVEZA kot
  1887**; **5. VPIS** — gospodinjstvi Brinec ↔ Jurajevič se izmenjujeta
  (1887 → 1892 → 1893);
- **h30** — Peter Jakljevič [~] × Marija Kralj [~]: **MENJAVA
  GOSPODINJSTVA** (Milek 1890 dvojčka + 1891 → 1893); babica PRAZNA;
  podpis obiskni G. Ambrož? [~] m.p.;
- **h41** — Matija Hušič? [~] × Neža Jakobič [~]: **ISTA ZVEZA kot 1890**
  (Hrušič × Jakobčič); 3. vpis na luknji;
- **h15** — Janez Jaklič [~] × Marija Brinec [~]: **ISTA ZVEZA kot 1887**
  (Jakšič [~] × Brinec);
- **h60** — **NOVA krstna**: oče Nikolaj Željko [~] = **h1 oče (1888+1892)
  — ŽELJKO 2. HIŠA** (h1 → h60);
- **h91** — **NOVA**: botra **Nikolaj Željko + Katarina Kure** = h1
  starši priimki — **Željko signal 3 hiš** (h1, h60, h91);
- **h74** — mrliška 04894 1886 **Hambeč** [~] → 1893 **Kambič?** [~] —
  čez knjige varianta gospodinjstva;
- **h25** — poroka 04455 1886 (ženin Jurij Klepec GRIBLJE 25) → 1893
  Matija Hrižan [~] × Ana Požek [~] — menjava gospodinjstva; **2. Hrižan
  oče** (poleg h63 Nikolaj);
- **h32** — oče **Matija Meh/Mrh? [~]** — **MERI**: ISTA mati (Marjeta/
  Margaretha Pegdirec) + ISTA botra (Marko Hrižan + Barbara Strauš) kot
  1892 (Urh) — ali isti oče z novo brano priimko ali drug mož [~]; 4. vpis.

**Željko veriga 3 hiš** (h1 + h60 + h91 botra); Šimec nazaj (2 signala).
Babice: **Marjeta/Marija Trotter 9×** (nova dominanta) + Ana Hrižan 3× +
Barbara Adlešič 2× + Ana Križan 1× + Ana Klepec 1× + prazna 1. Duhovniki:
**Jos. Rauq 14× (Jan–Avg) + NOV Janez Jelovšek? [~] 2× (od septembra) +
obiskni G. Ambrož? m.p. 1×** — druga menjava v 3 letih. Modri pripisi 20.
st. kot genealoški vir: 6 smrti + 1 poroka + Italijani 1941 — evidence-only.

**Integracija**: `research/issue17/parish-baptism-1893.json` (dokaz;
SAMPLE-TRANSCRIPTION-1893) + `scripts/p88_parish_baptism_1893.py` (I1–I10,
--check PASS: knjiga 200 + inventar 326, citirani skeni 6/6 JPEG 200, okvir
+ prelom 1894 + ponastavitev oznak, PT 13/3 z NOVO 46, sidra h72/h65/h27/
h21/h24/h30/h41/h15/h60/h91, čez-letne kontinuitete prek dokazov P82–P87 —
h72 vsi trije Strauš, h65 vsi trije Milek, h27 Kukar + Klobučar, h15
Jakšič + Brinec, h21 Požek + Brinec→Šimec, h41 Hrušič, h30 Milek dvojčka,
h24 Jurajevič→Brinec izmenjava, h32 Urh + Pegdirec + botra, h1 Zeljth,
h74 Hambeč 04894, h25 Klepec 04455, runtime projekcija 17/150, brez
»Hraus«) + `parish.ts` HOUSE_VITALS 133 → **150** (17 zasidranih 1893; vsi
DOCUMENTED; komentar P88) + **qa-p88-parish-baptism-1893** (89. kontrola;
celoven neodvisen preracun: okvir/PT 13/3/sidra h72–h91/kontinuitete 14
pinov + h60 04455 poroka + h41 any-blok pin/NOVE hiše/vitals 150; dve
obliki repo/produkcija) + qa-p86/p87 vitals pini 133 → 150 + qa-p85 h30/h41
dovolita 1893 blok (P88 kontinuiteta) + atlas.ts **PT_GAP_KNOWN + 46** (15.
dokazana!) + p80 skripta I7 P88 scoping (vitals 150) + p85 skripta I10
kumulativno (156; vesolje brez 1891/1892/1893 blokov) + p86/p87 skripti
I10 kumulativno (156; hiše 64). Kartica NI dodana (vzorec P77–P88).
Lekcije (9. primer): ① kontekstni ±okvir grep še enkrat zavajal (prvi
h24/h27 prebir) → neposreden parser; ② h46/h60 NISTA v PT chain naboru →
46 NOVA luknja (15.) + atlas PT_GAP_KNOWN + 46; h60 mehanično ponovitev
(04455) — dokaz newSampleHouses usklajen z neodvisnim preracunom; ③ qa-p88
h41 pin — prvi 1890 blok je Muc bajtar (ne Hrušič) → any-blok pin (vzorec
`; ④ r33 hišna »24« → 5x jasno 27 (dvojčici na isti hiši!); ⑤ r15 hišna
»60« → 5x jasno 65 (oče Milek 3× veriga). Veriga p60–p67 + p70–p88 --check
PASS (26 skript, vse exit 0; p68 zamrznjen po C2); tsc 0 / lint 0; /api/qa
dev **89/89** (qa-p88 True).

**nextSteps**: ① P89 = leto 1894 (prelom str. 69 row 1; skeni 70+ — do 73 že
v /tmp/p88); ② per-hišna kronologija tri-virskih hiš 13/36/71 (h72 zdaj 3
vpise); ③ mrliška 04894 1887–1893 (smrti prvih žen — dokaz menjav mater
h21 Brinec→Šimec?; gospodinjstev h30/h24/h25); ④ luknja 41–60: 15 dokazanih
(46 NOVA); ⑤ h1/h60/h91 Željko veriga: PUA/ATLAS presek.

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…, statična projekcija;
disciplina I9).

## §66 — P89: župnija Podzemelj — krstna knjiga 04105, polno leto 1894 (issue #18) — 2026-10-16

**SAMPLE-TRANSCRIPTION-1894** (MERI, NE odloča; v7 join nespremenjen).
P88 nextSteps ①: širitev vzorca po letih (P79 1886 → P82 1887 → P83 1888 →
P84 1889 → P85 1890 → P86 1891 → P87 1892 → P88 1893 → **P89 1894**).

**Okvir**: skeni 70–78 == tiskane strani 69–76; glava **»1894« na str. 69**
po 1893 row 83; vpisi na skenih 70, 71, 72, 74–78. **NOVELA OKVIRA: sken 73
je PODOVOJEN sken str. 71** (matricula re-scan — prvi v seriji 04105:
sken 72 == sken 73 == str. 71, vrstice 23–34 v obeh) — **stran == sken − 1
velja do skena 72, od skena 74 naprej stran == sken − 2**; **velike cifre
»1895~« na str. 76 po row 90** — oznake se ponastavijo na 1, **novela P83
potrjena 7. leto**; leto 1894 ima **90 zveznih vrstic** (najdaljše doslej).
Skeni 70–81 preneseni v /tmp/p89 (70–73 kopirani iz /tmp/p88; ročna faza,
NI v repu); hi-rez izrezi 2x–5x za vseh 14 Griblje vrstic + forenzika
hišnih številk 5x (vseh 14 jasno: 12, 2, 53, 69, 36, 57, 73, 31, 13, 75,
17, 71, 23, 60 — brez popravkov); r74 (»Grišče? 2«) in r58 (Gradac 4) NE
Griblje — prezrti. Kurrent frakcij: ¼ = prekrižana 4, ½ = zankasta 2
(r44 »zaprt« lik — ½ ali ⅛? [~]).

**Vzorec 1894**: **14 vpisov / 14 hiš** (drugo leto brez ponovitev znotraj
leta po P87 NARE): 12, 2, 53, 69, 36, 57, 73, 31, 13, 75, 17, 71, 23, 60.
**NOVELA VZORCA: 0 NOVIH hiš** — vseh 14 že zasidranih (12 krstnih
ponovitev P82–P88 + h71/h13/h36/h57 iz P77 1886 + h69/h13/h71 iz mrliške
04894 P78) — **vzorec Griblje hiš se ZASIČA** (65 hiš naprej). Skupaj s
P79–P88: **170 vpisov / 65 hiš čez tri knjige in DEVET let**. NOVELA:
ulomki — **novela P85 potrjena 5. leto** (½ zemljak 8 + ¼ zemljak 6; brez
bajtarjev/obrtnikov). PT klasifikacija **11/3** (53 + 57 + 60 v luknji
41–60 — **vse tri PONOVITVE, brez novih**; luknja ostaja 15 dokazanih).
0 nezakonskih; r50 brez babice (druga po P88 r50); brez dvojčkov letos.

**Sidra**:
- **h2** — Peter Hlebec [~] ¼ × Ana Jakobič [~]: **ŠTIRIKRATNA
  KONTINUETETA — ISTI starši vseh 4×** (1887 P82 + 1889 P84 + 1891 P86 +
  1894) — **najdaljša zasidrana zveza vzorca** (8 let; status ¼ konstanten);
  moder pripis: mati umrla 2.9.1965? v Novem mestu (HMIC NM 1965, str. 469);
- **h71** — Jurij Straus? [~] ¼ × Barbara Jakobčič? [~]: **ISTA ZVEZA čez
  8 let** (P77 1886 r83 »Jurij Strauš ½ × Barbara Jakopič«); status ½→¼;
  **STRAUŠ na DVEH sosednjih hišah** (h71 Jurij + h72 Matija — SIDRO 3
  vpise) — **PUA @71 0.8571 (F2) dobi krstno oporo**;
- **h36** — Janez Križan? [~] ¼ × Katarina Straucelj? [~]: 3. krstni vpis +
  **4. VIR tri-virske hiše** (poroka 04455 1882 + krstna 1886 ×2 P77 +
  mrliška 04894 1887 + krstna 1894) — **KRIŽAN 2. GENERACIJA** (Matija
  Križan 1882/1886 → Janez 1894 — mogoč sin [~] MERI);
- **h31** — Martin Fapič? [~] ½ × Marjeta Straus? [~]: **4. VPIS**
  (1887+1890+1891+1894) — oče Papič/Fapič/Tepič (Kurrent P/F/T) **ISTI** +
  mati Margaretha/Marjeta Straus **ISTA vseh 4×** + botra **Marko Klobučar
  ISTI kot 1887** (P86 Martin [~]) — najbolj popolna trojica oče+mati+botra;
- **h17** — Janez Kralj? [~] ¼: **ISTI oče ISTA frakcija** kot P82 1887
  r82; **MATER MENJANA: Ana Jakobič → Doroteja Firlak? [~]** — **5.
  dokazana menjava matere** (po h61 1891, h72 1891, h21 1893) ali druga
  branja [~] MERI; 7-letni razmik; Kralj = 2. signal familije (P88 h30 mati);
- **h57** — Peter Pegdirec? [~] × Marija Županc? [~]: 2. vpis čez 8 let
  (P77 1886 r20 starša »Podolivec/Stupanič« = varianti ali drugi [~] MERI);
  **ISTA BOTRA PA čez 8 let** (Jurij Brodarič? + Marija Strauš? = P77 r20);
- **h60** — Nikolaj Željko [~] ¼ × Marija Brodarič [~]: **h60 2. VPIS ISTA
  zveza + ISTA BOTRA PA 2. leto** (P88 r1: Marko Pegdirec + Marija Klepec);
  status ½→¼ (vzorec h61 P87); **ŽELJKO VERIGA 4 hiše signalov** (h1
  1888+1892 + h60 1893+1894 + h91 botra + h25 botra);
- **h23** — Matija Brinec [~] ½: **ISTI oče kot P88 + ISTA BOTRA PA 2.
  leto** (Janez Jaklič + Doroteja Pegdirec = P88 r28); mati Debič?/Žehlič?
  varianti ali druga žena [~] MERI;
- **h12** — Janez Dragoš [~] ½: **ISTI oče kot P87** (»Dragos«), 2. vpis;
  mati Civlkovič?/Druppovič? varianti;
- **h53** — Janez Pegdirec? [~] × Marija Hrižan? [~]: **ISTA zveza kot P86
  1891** (»Pozdirec × Križan« — Kurrent P/K in K/H variante) + babica Ana
  H/Križan **ISTA**; 2. vpis na luknji;
- **h73** — Nikolaj Županič? [~] × Katarina Pozdirec/Pegdirec? [~]: **ISTA
  zveza kot P87 1892**, 2. vpis; botra menjana od 1892;
- **h75** — Janez Jakobič? [~] × Marija Stubljar? [~]: **ISTA zveza kot
  P87** (Jakobčič × Sušljar — Kurrent variante); **ženska botra Barb.
  Brinec ISTA 2. leto**;
- **h13** — Matija Jakljevič? [~] ½: **ISTI oče ime+status** kot P77 1886
  r77 (»Jakopič? ½«); tri-virska hiša; **babica PRAZNA**;
- **h69** — Janez Brinec [~] × Ana Kure [~]: **NOV krstni vpis čez knjige**
  (mrliška 04894 1886); botra Katarina Požek? — **Požek 7. leto**.

**Pegdirec/Pozdirec familija 7/14 vpisov** (oče h57 + mati h73/h50 + botra
h24/h47/h49/h64/h88) — najgostejša botrska familija 1894. Menjave statusa
na zasidranih hišah: h71 ½→¼ (1886→1894), h60 ½→¼ (1893→1894). Duhovniki:
**Jan Jelenu—? [~] 11×** (verjetno ISTI kot P88 sept. 1893 »Janez
Jelovšek?« — varianti branja istega podpisa [~] MERI) + **Jos. Rauq? 3×**
(Februar, September, December — izmenjava NI čista). Babice: **Trotter
11×** (2. leto dominanta; Kurrent J/T »Jotter«; »Margan.« = Margareta) +
Ana Hrižan 2× + prazna 1. Modri/svinčnikovi pripisi 20. st. kot genealoški
vir: 2 poroke (r4 1949, r88 1925) + 3 smrti otrok 1894/1896 + 2 smrti
staršev (r11 mati 1965, r47) + r90 grob Celovec — evidence-only.

**Integracija**: `research/issue17/parish-baptism-1894.json` (dokaz;
SAMPLE-TRANSCRIPTION-1894) + `scripts/p89_parish_baptism_1894.py` (I1–I10,
--check PASS: knjiga 200 + inventar 326, citirani skeni 8/8 JPEG 200 —
sken 73 NI citiran (podvojen), okvir + prelom 1895 + ponastavitev oznak +
podvojeni sken novela, PT 11/3 brez novih, sidra h2–h60 (14), čez-letne
kontinuitete prek dokazov P77/P82–P88 — h2 vsi štirje Hlebec, h31 vsi štirje
Papič/Papič/Tepič + Klobučar, h53 Pozdirec × Križan + babica, h73/h75/h12
pini, h17 Kralj + Jakobič→Firlak, h71 P77 Strauš × Jakopič, h36 Križan ×2,
h57 Podolivec + botra Brodarič × Strauš, h13 Jakopič ½, h23 Brinec + botra,
h60 Željko × Brodarič + botra, h1 Zeljth, h69 Podec 04894, runtime
projekcija 14/164, brez »Hraus«) + `parish.ts` HOUSE_VITALS 150 → **164**
(14 zasidranih 1894; vsi DOCUMENTED; komentar P89 z novelama) +
**qa-p89-parish-baptism-1894** (90. kontrola; celoven neodvisen preracun:
okvir z novelo podvojenega skena (stran == sken − 1 / − 2; sken 73 NI
citiran)/PT 11/3/sidra h2–h60/NOVELA 0 novih hiš (vsaka mora imeti
prejšnje zasidranje)/kontinuitete 19 pinov/vitals 164; dve obliki
repo/produkcija) + qa-p86 h53 dovoli 1894 blok + qa-p87 h12/h73/h75 dovolijo
1894 bloke + qa-p88 h23 dovoli 1894 blok + qa-p86/p87/p88 vitals pini 150 →
164 + atlas.ts PT_GAP_KNOWN komentar (P89: brez novih) + p80 skripta I7 P89
scoping (vitals 164) + p85 skripta I10 kumulativno (170; vesolje brez
1891/1892/1893/1894 blokov) + p86/p87/p88 skripti I10 kumulativno (170;
hiše 64; vsak z lastnim vesoljem pre87/pre88/pre89 — h53/h12/h73/h75/h23
ostanejo zgodovinske nove svoje faze). Kartica NI dodana (vzorec P77–P89).
Lekcije (10. primer): ① I6 prvi prebir — h57 IN h60 sta TUDI v luknji
41–60 (P88 ptGap je imel 41/46/60) → PT 11/3 (ne 13/1); ② I8 p82_h31 ima
2 vpisa (r55 Urh + r67 Papič) → any-based pin; ③ p86/p87/p88 I10
repeat_houses potrebujejo per-fazno vesolje (pre87/pre88/pre89) — 1894
bloki ne smejo spreminjati zgodovinskih klasifikacij; ④ terminal prikaz
požira »[h« v for-destrukturiranju — char-code forenzika: `[hn, yr, sig]`
pravilno; ⑤ sken 73 = podvojen sken str. 71 (matricula re-scan) — prvi
v seriji: okvirna invarianta I3/I4 dobi eksplicitno preverjanje (73 NI
citiran; stran == sken − 2 od 74). Veriga p60–p67 + p70–p89 --check PASS
(27 skript, vse exit 0; p68 zamrznjen po C2; p69 izven verige); tsc 0 /
lint 0; /api/qa dev **90/90** (qa-p89 True).

**nextSteps**: ① P90 = leto 1895 (prelom str. 76 row 1; skeni 78+ — do 81 že
v /tmp/p89; POZOR: stran == sken − 2 od skena 74 naprej); ② per-hišna
kronologija tri-virskih hiš 13/36/71 — h36 zdaj 4 viri, h71 ISTA zveza
1886+1894, h13 2. krstni vpis; mrliška 04894 1887–1894 poglobiti; ③
mrliška knjiga 04894 leta 1887–1894: smrti prvih žen (dokaz menjav mater
h17 Jakobič→Firlak?; gospodinjstev h23/h24/h25/h30/h60); ④ luknja 41–60:
15 dokazanih; naslednja priložnost v 1895; ⑤ Željko veriga (h1 + h60 + h91
+ h25 botra) in Strauš veriga (h71 + h72): PUA/ATLAS presek naprej; h36
Križan 2. generacija.

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…, statična projekcija;
disciplina I9).

## §67 — P90: župnija Podzemelj — krstna knjiga 04105, polno leto 1895 (issue #18) — 2026-10-16

**SAMPLE-TRANSCRIPTION-1895** (MERI, NE odloča; v7 join nespremenjen).
P89 nextSteps ①: širitev vzorca po letih (P79 1886 → … → P89 1894 →
**P90 1895**).

**Okvir**: skeni 78–84 == tiskane strani 76–82. **NOVELA P89 POTRJENA
2. LETO: stran == sken − 2 ZA CELO LETO** (sken 73 podvojen, NI citiran);
glava **»1895.~« na str. 76** po 1894 row 90; leto 1895 ima **73 zveznih
vrstic** (krajše od 1894: 90); **prelom 1896 na str. 83 = sken 85 po row
73** — oznake se ponastavijo na 1, **novela P83 potrjena 8. leto**. Skeni
78–88 preneseni v /tmp/p90 (ročna faza, NI v repu); izrezi 2x (L/R) +
hišne forenzike 5x–10x za vseh 15 Griblje vrstic; 3x zoom matičnih/
roditeljskih celic in duhovniških podpisov; sken 85 pregledan za prelom
1896.

**Vzorec 1895**: **15 vpisov / 14 hiš** (h24 DVOM 2× — **prva ponovitev
hiše znotraj leta po P87 NARE**: r22 Brime × Jakobič + r48 Toško? × Simec,
forenzika 8–10× vztraja 24, alternative 21/27 [~] MERI): 58, 46, 87, 24 ×2,
12, 30, 20, 65, 32, 37, 69, 72, 91, 29. **3 NOVE hiše (20, 37, 87)** po
P89 »0 novih« + 11 ponovitev. Skupaj s P79–P89: **185 vpisov / 68 hiš čez
tri knjige in DESET LET**. **NOVELI VZORCA**: ① **babica stolpec na VSEH
15 vrsticah PRAZEN** (1894: Trotter 11×!) — **Trotter žene pa 7× kot BOTRA**
(vloga prestopila iz babiške v botrsko); ② **4× PRAZNA botra** (r53/r54/
r55/r66 — september–december cluster; P89: vedno zapisana). Statusi:
novela P85 potrjena 6. leto (½ zemljak 10 + ¼ zemljak 2 + bajtar 1 + r18
¼ [~]). PT klasifikacija **12/2** (46 + 58 v luknji 41–60 — h46 **2. dokaz**
P88+P90, h58 4. vpis; **brez novih števil**, luknja ostaja 15 dokazanih;
hiše 20/30/37/87/91 vse v naboru PT). 0 nezakonskih na Gribljih (2 izven:
r31 Primostek, r61 Krasinec). **MATI PODCELICA (X × Y) prvič eksplicitno
dokumentirana** — semantika desne podcelice matere ODPRTA (starši matere?
očeta? mešano) — vsebine verbatim, MERI. Otroške smrti 1895: pripisi † na
r18/r27/r40 (†1896)/r55 — dojenčijska umrljivost.

**Sidra**:
- **h58** — Janez Požek [~] ½ × Katarina Kambic? [~]: **4. VPIS** — oče
  ISTI 3. leto zapored (1890 + 1892 + 1895; 1889 »Franz Požek ¼« = ista
  oseba [~]); **MATI MENJANA: Ana Dragoš/Dragos (1889–1892) → Katarina
  Kambic? [~]** — smrt prve žene ali ločitev; mrliška 04894 bi dokazala;
- **h32 + h72** — **5. VPIS — NAJDALJŠI zvezi vzorca (1889–1895)**: Urh ×
  Pegdirec ISTA 5× (statusi ¼/½/¼/½/½ [~]); Straus × Jakobič ISTA 5×
  (1888 »Barbara Husič?« varianta) — Straus veriga h71/h72;
- **h69** — oče **Janez Brinec ISTI vseh 5×** (1888+1889+1890+1894+1895);
  mati **5. različno branje** (Strauš → Strauš → Straus → Kure → Mure? [~]
  MERI — verjetno variante 1–2 pravih imen);
- **h30** — Nikolaj Šegina? [~] × Marjeta Mihelt [~]: **3. DRUŽINA v 6
  letih — 2× MENJAVA GOSPODINJSTVA** (Milek 1890–91 → Jakljevič 1893 →
  Šegina 1895) — **najbolj nestabilna hiša vzorca**;
- **h29** — Janez Kuhar?/Kuklar? [~] × Katarina Klobučar [~]: **MENJAVA
  GOSPODINJSTVA** — hiša epidemije 1886 (Mileh ×3) + »hiša kuge« (Milek ×
  Križan 1888+1892) → povsem nova zveza; **epidemija popolnoma prekinjena**;
- **h91** — Janez Muc [~] (»mlinar in kovač?«) × Ana Kure [~]: **2. VPIS —
  mati ISTA, oče MENJAN** (Novak 1893 → Muc 1895 — ponovna poroka ali
  napaka branja [~] MERI);
- **h46** — Anton Brodarič [~] × Marija Klobučan? [~]: **2. VPIS ISTA
  zveza** (P88 r43) — **2. dokaz luknje 41–60**;
- **h24** — 3. VPIS ISTA zveza Brinec/Brime × Jakobec/Jakobič
  (1887+1893+1895) + **r48 DVOM** (zgoraj);
- **h12** — 3. VPIS (oče Dragoš ISTI 3×; mati 3. branje Civlkovič?/
  Druppovič?/Cvitkovič? [~] — trije bralci iste/nenavadne matere);
- **h65** — 4. VPIS (oče Milek/Mihelt Kurrent varianta [~]; mati Katarina
  Požek ISTA 2×: 1887 + 1895);
- **h87 NOVA** — Marko Pegdirec bajtar × Marjeta Pegdirec: **PEGDIREC
  PRVIČ STARŠI** (familija, ki je do zdaj prevladovala kot botra/matere —
  P89 7/14 botrskih); podcelica Nikol. Hrižan × Marija Željko — h63 (oče
  Hrižan 1887–1892 4×) + Željko veriga [~];
- **h20 NOVA** — Peter Pezdirec? ¼ × Doroteja Šlepec; podcelica Matija
  Mihelt × Ana? Požek **zelo blizu para h65 r43** (Mihelt z dvema ženama?
  ali napaka [~] MERI);
- **h37 NOVA** — Peter Pezdirec ¼ × Marija Lužanič? [~]: **ANOMALIJA —
  isti oče ime+status kot h20 r40, druga žena!** (dva istoimenska moža —
  oče+sin? — ali napaka [~] MERI).

**Željko veriga 6 signalov**: h1 (1888+1892) + h60 (1893+1894) + h91/h87/
h66 podcelice + h25 botra. **DUHOVNIKI (TRIJE hkrati — P86: dva)**: Jan
Jelenuš/Jelez? [~] **9** (dominanta) + Jos. Rauq [~] **4** (april–september)
+ **NOV Franc Klunng? [~] 2** (od septembra; Klunnq/Klunng variante).
Babice: **0 zabeleženih** (NOVELA).

**Integracija**: skripta `scripts/p90_parish_baptism_1895.py` (**I1–I10**,
`--check` PASS) + dokaz `research/issue17/parish-baptism-1895.json`
(SAMPLE-TRANSCRIPTION-1895) + `parish.ts` HOUSE_VITALS 164 → **179**
(15 zasidranih 1895; vsi DOCUMENTED; komentar P90 z novelama) +
**qa-p90-parish-baptism-1895** (91. kontrola; celoven neodvisen preracun:
okvir z novelo (stran == sken − 2 za celo leto; sken 73 NI citiran)/NOVELA
babica 15 praznih/PT 12/2/sidra h58–h29 (14 + DVOM)/NOVE hiše 20/37/87
(brez priora)/kontinuitete 26 pinov/vitals 179; dve obliki repo/produkcija)
+ qa-p85 h30 dovoli 1895 blok + qa-p87 h12 dovoli 1895 blok + qa-p88
h46/h91 dovolita 1895 bloka + qa-p86/p87/p88/p89 vitals pini 164 → 179 +
p80 skripta I7 P90 scoping (vitals 179) + p85/p86/p87/p88 skripti I10
kumulativno (185; hiše 67; vesolja brez 1895 blokov). Kartica NI dodana
(vzorec P77–P90). Lekcije (11. primer): ① PT klasifikacija iz osnutka
(9/5: 20/30/37/87/91 »izven nabora«) NI ustreza verigi chain-full-pt-ps
(dejansko **12/2** — 20/30/37/87/91 so VSE v naboru; 46+58 v luknji) —
skripta je ujela napako dokaza in dokaz popravljen; ② števec duhovnikov v
osnutku (8+3+2=13) NI ustreza 15 vpisom — neodvisen preracun **9+4+2=15**
(dokaz popravljen: Rauq april–september, ne februar); ③ p85 h30 ima 2 vpisa
(r51+r52 dvojčka) → any/all-based pin namesto len==1. Veriga p60–p67 +
p70–p90 --check PASS (28 skript, vse exit 0; p68 zamrznjen po C2; p69
izven verige); tsc 0 / lint 0; /api/qa dev **91/91** (qa-p90 True).

**nextSteps**: ① P91 = leto 1896 (prelom str. 83 row 1; skeni 85+ — 85–88
že v /tmp/p90; stran == sken − 2); ② mrliška knjiga 04894 leta 1887–1896:
smrti prvih žen — dokaz menjav h58 (Ana Dragoš → Katarina Kambic?) in h91
(Novak → Muc); ③ per-hišne kronologije tri-virskih hiš 13/36/71 — h36
(Rognjavas? 36, r65) zdaj 5 vir; ④ luknja 41–60: 15 dokazanih (46 2. dokaz);
naslednja priložnost v 1896; ⑤ Željko (h1+h60+h87+h91 podcelice) in
Pegdirec (h87+h40 starši) verige — PUA/ATLAS presek naprej; ⑥ preveriti
hišo 24: ali obstaja ločena hiša 21 z Toško/Simec gospodinjstvom (dvom r48).

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…, statična projekcija;
disciplina I9).

## §68 — P91: župnija Podzemelj — krstna knjiga 04105, polno leto 1896 (issue #18) — 2026-10-16

**SAMPLE-TRANSCRIPTION-1896** (MERI, NE odloča; v7 join nespremenjen).
P90 nextSteps ①: širitev vzorca po letih (P79 1886 → … → P90 1895 →
**P91 1896**).

**Okvir**: skeni 85–92 == tiskane strani 83–90. **NOVELA P89 POTRJENA
3. LETO: stran == sken − 2 ZA CELO LETO** (sken 73 podvojen, NI citiran);
glava **»1896« na str. 83** po 1895 row 73; leto 1896 ima **94 zveznih
vrstic — NAJDALJŠE doslej** (1894: 90); **prelom 1897 na str. 91 = sken 93
po row 94** — oznake se ponastavijo na 1, **novela P83 potrjena 9. leto**.
Skeni 85–94 preneseni v /tmp/p91 (85–88 kopirani iz /tmp/p90; ročna faza,
NI v repu); izrezi 2x (L/R) + hišne forenzike 5x–10x za vseh 14 Griblje
vrstic; **referenčna primerjava** (Gradac 25 isti pisar) za Kurrent 5/6;
sken 93 pregledan za prelom 1897.

**Vzorec 1896**: **14 vpisov / 14 hiš — NARE (3. leto** po P87 1892/P89
1894): 9, 14, 31, 36, 1, 25, 46, 26, 41, 15, 63, 45, 53, 30. **3 NOVE hiše
(9, 14, 45)**. Skupaj s P79–P90: **199 vpisov / 71 hiš čez tri knjige in
ENAJST LET**. **NOVA LUKNJA ŠTEVILKA: h45 (16. dokazana v 41–60 — prva
nova od P88**; PT_GAP_KNOWN dobi +45) + **h41 4. dokaz + h46 3. dokaz +
h53 3. dokaz** — luknja zdaj 16 dokazanih. **NOVELA babica potrjena
2. LETO**: 14/14 PRAZNO (1895: 15; 1894: Trotter 11×) — **Trotter žene
1896 0×** (tudi kot botra izginejo). Statusi: **½ zemljak 12 + bajtar 2**
(r13 Pendirec + r70 Straus) — **prvo leto brez ¼ zemljaka** (novela P85,
7. leto). **NOV duhovnik Fr. Šuvar? [~] 9** (dominanta, Januar–Junij) +
Jos. Rauq [~] 4 (Feb/Sep/Okt/Dec) + r5 brez podpisa (3. primer po P86
r39/P87 r70) — **P90 trojica se krči** (Klunng in Jelenuš izginejo).
0 nezakonskih. **MATI PODCELICA (X × Y) izgine** (po prvi dokumentaciji
P90). **Dojenčijska umrljivost**: † r2 (3/3. 96), r31 (29/3. 97?), r53
(19.96?) + r5 krsta PRAZNA (umrl pred krstom?) — 4 od 14 vpisov.

**KURRENT FORENZIKA (4 popravki z 5x–10x izrezi + referencami)**: r25
»26« → **jasno 25** (referenčna primerjava z Gradac 25, isti pisar —
Kurrent 5 ima kljuko + ločeno skledo, 6 zaprti lok), r31 »16« → **jasno
46** (4 z vodoravnim trtcom), r92 »25« → **jasno 30** (podolgovata zanka
0; starša Šegina × Mihelt = h30 1895 to potrdita), r13 »37?« → **jasno 31**
(1 z razpiko).

**Sidra**:
- **h1** — Nikolaj Željko [~] ½ × Katarina Kure: **3. VPIS ISTA ZVEZA**
  (1888 P83 »Zeljth« [~] + 1892 P87 + 1896 — **8 let, 2. najdaljša zveza
  vzorca**); **botra ISTI priimki kot starši vse 3×** (začarani krog
  familije); **ŽELJKO VERIGA 8 signalov** (h1 ×3 + h60 ×2 + podcelice
  h91/h87/h66 + botra h25 + **botra h46 NOVO**);
- **h63** — Nikolaj Hrižan? [~]: **OČE ISTI VSEH 5× (1887–1896 — najbolj
  konstanten oče na eni hiši**; Prižan/Hrigian/Križan/Hrižan variante
  istega podpisa); mati Pendirec/Pegdirec variante;
- **h30** — Nikolaj Šegina? × Marjeta Mihelt?: **ISTA ZVEZA 2. LETO**
  (1895+1896) — **3. DRUŽINA se je UNESELILA** po 2 menjavah;
- **h41** — Matija Hušič? × Neža Jakobič?: **4. VPIS ISTA ZVEZE**
  (1890×2 + 1893 + 1896 — **najbolj stabilna zveza na luknji**);
- **h15** — Janez Jaklič? × Marija Brinec: **3. VPIS ISTA ZVEZA**
  (1887 »Jakšič?« + 1893 + 1896 — Kurrent J/Š variante);
- **h36** — Janez Križan? × Katarina Straucelj?: **2. VPIS** (1894+1896);
  tri-virska hiša dobi **5. in 6. vir**; KRIŽAN 2. GENERACIJA (status ¼ → ½);
- **h53** — Janez Pendirec? × Marija Hrižan: **3. VPIS VARIANTE**
  (1891 Pozdirec × Križan + 1894 Pegdirec × Hrižan + 1896 — Kurrent P/K +
  K/H variante istih dveh familij);
- **h46** — Anton Brodarič: 3. VPIS + **MATI MENJANA/varianta**
  (Klobučar/Klobučan 1893+1895 → Kramarič? 1896 [~] MERI); botra Nikolaj
  Željko = Željko veriga;
- **h31** — Marko Pendirec? bajtar × Katarina Žugelj?: **MENJAVA
  GOSPODINJSTVA** (Fapič × Straus 1894 → 1896 — 2. menjava na h31);
- **h25** — Janez Klepec? × Katarina Tome?: **KLEPEC NAZAJ** (poroka
  04455 1886 Klepec h25; 1893 Hrižan × Požek menjava → 1896 vrnitev
  originalne familije [~]);
- **h26** — Janez Jakobič? × Marija Stubljar?: **ANOMALIJA — ISTI priimki
  kot h75 zveza** (1892+1894) — 3. vpis zveze na **DRUGI hiši** (75 → 26:
  selitev gospodinjstva ali napaka [~] MERI; forenzika 10x vztraja 26);
- **h9/h14 NOVE** — h14: **neimenovan otrok** »N. moškega spola« + krsta
  PRAZNA + brez botre/podpisa (**najbolj fragmentaren vpis vzorca**; oče
  Brinec = h69 familija? [~]);
- **h45 NOVA** — Martin Straus? bajtar × Barbara Doroteja? [~]: **NOVA
  LUKNJA ŠTEVILKA**; botra **POD TRAKOM** [?]; **Straus signal na TRETJI
  hiši** (h71 Jurij + h72 Matija + h45 Martin [~] MERI); ime Martin (prvi
  prebir Marija [~]).

**Integracija**: skripta `scripts/p91_parish_baptism_1896.py` (**I1–I10**,
`--check` PASS) + dokaz `research/issue17/parish-baptism-1896.json`
(SAMPLE-TRANSCRIPTION-1896) + `parish.ts` HOUSE_VITALS 179 → **193**
(14 zasidranih 1896; vsi DOCUMENTED; komentar P91 z novelama) +
**qa-p91-parish-baptism-1896** (92. kontrola; celoven neodvisen preracun:
okvir z novelo (stran == sken − 2; 94 vrstic; sken 73 NI citiran)/NOVELA
babica 14 praznih/NOVA LUKNJA 45 pin/PT 10/4/sidra h9–h30 (14)/NOVE hiše
9/14/45 brez priora/kontinuitete 25 pinov/vitals 193; dve obliki
repo/produkcija) + **atlas.ts PT_GAP_KNOWN + 45** (16. dokazana) +
qa-p85 h30/h41 dovolita 1896 bloka + qa-p86 h53 dovoli 1896 blok + qa-p88
h46 dovoli 1896 blok + qa-p86/p87/p88/p89/p90 vitals pini 179 → 193 +
p80 skripta I7 P91 scoping (vitals 193) + p85/p86/p87/p88/p89/p90 skripti
I10 kumulativno (199; hiše 70; vesolja brez 1896 blokov). Kartica NI
dodana (vzorec P77–P91). Lekcije (12. primer): ① Kurrent 5/6 — r25 prvi
prebir 26, 10x izrez dvomljiv → **referenčna primerjava z isto številko
iste roke (Gradac 25, r34)** je razrešila: jasno 25 (skladno s Klepec
familijo h25!); ② Kurrent 1/4 (r31 46) in 5/0 (r92 30) — starševska
konzistenca (Šegina × Mihelt = h30) kot sekundarna potrditev; ③ Python
vstavljanje je pustilo `]` namesto `];` na koncu HOUSE_VITALS — p81 regex
`\];` ni več našel arrayja (UnboundLocal past: gnezdena `def e_by_row(row)`
senči modulsko `e_by_row(entries, row)`); veriga (p81) ujela, popravljeno;
④ p87 h75 Kurrent variante (Jakobčič/Sušljar 1892 vs Jakobič/Stubljar
1894) — variantno tolerantni pini. Veriga p60–p67 + p70–p91 --check PASS
(29 skript, vse exit 0; p68 zamrznjen po C2; p69 izven verige; p80/p81
samo z --check); tsc 0 / lint 0; /api/qa dev **92/92** (qa-p91 True).

**nextSteps**: ① P92 = leto 1897 (prelom str. 91 row 1; skeni 93+ — 93 že
v /tmp/p91; stran == sken − 2); ② mrliška knjiga 04894 leta 1887–1896:
smrti prvih žen — dokaz menjav h58 (Dragoš → Kambic?), h91 (Novak → Muc),
h31 (Fapič → Pendirec), h46 (Klobučar → Kramarič?); ③ h26/h75 selitvena
hipoteza: Jakobič × Stubljar 75 → 26 — preveriti h26/h75 v mrliški 04894 +
kataster 1825; ④ luknja 41–60: 16 dokazanih (45 NOVA); naslednje priložnosti
v 1897; ⑤ Željko veriga 8 signalov + Straus 3 hiše (h71/h72/h45) — PUA/
ATLAS presek naprej; ⑥ Fr. Šuvar? identifikacija (župnijski arhiv
Podzemelj — župniki/kaplani 1896) [~].

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…, statična projekcija;
disciplina I9).

## §69 — P92: župnija Podzemelj — krstna knjiga 04105, polno leto 1897 (issue #18) — 2026-10-16

**SAMPLE-TRANSCRIPTION-1897** (MERI, NE odloča; v7 join nespremenjen).
§68 nextSteps ①: širitev vzorca po letih (P79 1886 → … → P91 1896 →
**P92 1897**).

**Okvir**: skeni 93–101 == tiskane strani 91–98. **NOVELA P92 — SKEN 97 =
PODVOJEN (duplikat s96 = str. 94; 2. znani duplikat po skenu 73)** —
NOVELA P89 (stran == sken − 2) velja **samo do skena 96**, od skena 98
stran == sken − 3; **premik offseta je ARTEFAKT DUPLIKATA, ne nova
številčenja**. Glava **»Leto 1897« na str. 91** po 1896 row 94; leto 1897
ima **85 vrstic**; **prelom 1898 na str. 98 = sken 101 row 86** — oznake
se ponastavijo na 1, **novela P83 potrjena 10. leto**. Skeni 93–104
preneseni v /tmp/p92 (93 kopiran iz /tmp/p91; p92_fetch po vzoru p91; ročna
faza, NI v repu); izrezi 2x (L/R) + hišne forenzike 5x (pas popravljen na
x 520–645) + datumski izrezi 5x–8x + stolpec zaporednih številk 6x (s99
raztrgan — rešen s kontinuiteto s98 51–58 → s99 59); 20 kandidatov →
**19 potrjenih Griblje** (2 izključena: s93 r11 »Grisice« — forenzika jasno
ne-Griblje; s99 r65 »Otok 6«).

**Vzorec 1897**: **19 vpisov / 18 hiš — NARE (4. leto** po P87 1892/P89
1894/P91 1896): 12, 32, 10, 24, 37, 54, 60, 2, 43, 23, 46, 31, 16, 40, 20,
31, 61, 65, 45 — **h31 2 VPISA V ENEM LETU** (r51 Sapič? × Straus + r64
Straus? × Jakobič — **STRAUS KOMPLEKS**: 1894 Fapič?×Straus → 1896
Pendirec?×Žugelj menjava → 1897 obe nazaj); **3 NOVE hiše (10, 40, 43)**;
**NOVA LUKNJA ŠTEVILKA 43 (17. dokazana v 41–60** — PT_GAP_KNOWN dobi +43;
h43 številka NA RAZPOKI [~]) + h54 2. dokaz + h60 4. dokaz + h45/h46
luknji; kumulativ **217 vpisov / 74 hiš** čez tri knjige in **DVANAEST
LET** (193 + 18 = 211 vitals; h61 sidro ZDRUŽENO s P79-era placeholderjem
— ne dupliran).

**ČEZ-FAZNA POTRDITEV h61**: izvirna prepis hiše 61 (issue #17, prej P79)
je imela minimalen placeholder »krščen Anton — oče Miha P.—« (scan 100,
stran 49 po stari predpostavki); P92 5x forenzika dopolni: **Janez Muc
bajtar × Ana Kure, stran 97 po noveli** — blok združen v P79 sekciji.

**PRVI NEZAKONSKI VPIS OD P90**: r31 Florijan (h43) — **OČE PRAZEN, mati
Katarina Pozdirec SAMA MATI ¼ zemljatva** (novela P85 ulomek, 8. leto).

**NOVELA babica POTRJENA 3. LETO**: 19/19 PRAZNO (1895: 15; 1896: 14) —
Trotter žene 0× 3. leto.

**DOJENČIJSKA UMRLJIVOST 7/19 — NAJVIŠJE doslej** (P91: 4/14): † r12
(24/1.98?), r15 (5/9.97?), r25 (17/9.97?), r28 (16/2.98?), r29 (7/6.97),
r38 (3/9.99?), r59 (3/9.98?).

**Duhovniki**: Šuvar (1896 dominant, 9×) **IZGINE** — **Klun 11×
(dominanta) + Rauq 8× — MEŠANO LETO** (preplet skozi vse mesece, ne
pol-sezonsko).

**Statusi**: ½ × 16 + bajtar × 2 (r79 Muc + r84 Straus) + ¼ × 1 (sama
mati).

**KURRENT FORENZIKA 6 POPRAVKOV**: ① h23/h24 (r21 jasno 24 + r38 jasno 23
— DVE RAZLIČNI Brinec hiši, prvi prebir »oba 23« napačen) ② s93 r11
»Grablje?« → jasno GRISICE (druga vas — izključena; isto št. 2 kot Griblje
r29!) ③ s99 r65/66 »Griblje 11?« → jasno OTOK (izključena) ④ s98 r53
»Griblje 10?« → jasno 16 ⑤ row številke s99 59/62/64 (Kurrent 5/6) ⑥ h45
mati = **Barbara Spudič** (5x — **POPRAVEK P91 prebira »Doroteja? [~]«**).

**Matičar pripisi 20. st. 6 vpisov** (najgostejše doslej): r41 † 15.3.1931,
r52 poroka 1919 + † 22.7.1981, r62 † 2.1.1980, r64 poroka 29.1.1934, r79
zakonca Mihelk Katarina † 26.5.1979 + EHS ČG, r80 † 14.5.1989 + EHS ČG.

**Sidra**: h45 (Straus bajtar × Spudič — **2. VPIS ISTA ZVEZA** 1896+1897 +
POPRAVEK matere), h46 (Brodarič **4. VPIS** + **mati 3. VARIANTA**: Klobučar
1893/95 → Kramarič? 1896 → Harašimovič? 1897 [~]; botra Željko = veriga),
h31 (Straus kompleks 2 vpisa), h60 (Željko × Brodarič ISTA zveza — 4. dokaz
luknje), h61 (Muc bajtar × Kure; **botra Nikolaj Željko + Katarina Kure =
h1 PAR KOT BOTRA** — ŽELJKO VERIGA, začarani krog kot P91 h1), h24/h23
(dve Brinec hiši — 8. pin h24), h63 **IZGINE** (oče konstanten 5× 1887–96 —
konec serije; botra Hrižan 3× v letu po izgini), h2 5. pin, h12 4. pin,
h65 5. pin. Željko veriga zdaj 10 signalov.

**Dokaz** research/issue17/parish-baptism-1897.json (SAMPLE-TRANSCRIPTION-
1897; ročna faza — skeni v /tmp/p92, NI v repu; delovni p92_fetch/p92_crops
v scripts/tmp).

**Skripta** scripts/p92_parish_baptism_1897.py (deterministični
verifikator, I1–I10, --check PASS: knjiga 200 + inventar 326, citirani
skeni 8/8 JPEG 200 (97 podvojen ni citiran), okvir + piecewise page_of_scan
(− 2 do 96 / − 3 od 98) + rowsTotal 85 + duplikat 97 + prelom 1898 + NOVELA
babica 19 praznih + NEZAKONSKI r31 + PT 13/5 (43 NOVA — I6 preverja tudi
PT_GAP_KNOWN v atlas.ts) + sidra 19 + I8 čez-letne kontinuitete (h45/h46/
h31/h60/h2/h12/h24/h32/h61/h65/h16/h20/h23/h37/h54 — scan-pini) + runtime
projekcija 19/211 + kumulativ 217/74 + duhovniki (11, 8) + † 7).

**Integracija**: parish.ts HOUSE_VITALS 193 → 211 (18 novih 1897 blokov +
sidro h61 združeno; vsi DOCUMENTED; komentar P92 z novelama P92/P83) +
qa-parish.ts qa-p92 (93. kontrola; celoven neodvisen preracun; dve obliki
repo/produkcija) + atlas.ts PT_GAP_KNOWN + 43 (17. dokazana; komentar P92)
+ qa-p79/p80 filtri scoperani na originalni P79 vzorec (1897 samo h61 —
polno leto = qa-p92) + qa-p87 h12 / qa-p88 h23+h46 / qa-p90 h20+h37 /
qa-p91 h45 dovolijo 1897 bloke + qa-p85–p91 vitals pini 193 → 211 + p80
skripta I7 211 + p85–p91 skripti kumulativno (217; hiše 73; EV-only 6).
Veriga p60–p67 + p70–p92 --check PASS (30 skript, vse exit 0; p68
zamrznjen po C2; p69 izven verige; p80/p81 samo z --check); tsc 0 / lint 0;
/api/qa dev **93/93** (qa-p92 True).

**v7 runtime join NESPREMENJEN** (sha256 4bb40370…, statična projekcija;
disciplina I9).

**nextSteps**: ① P93 = leto 1898 (prelom str. 98 row 1 = sken 101; skeni
102+; stran == sken − 3 do naslednjega duplikata); ② mrliška knjiga 04894
1887–1896: smrti prvih žen — dokaz menjav h58 (Dragoš → Kambic?), h91
(Novak → Muc), h31 (Fapič → Pendirec → Sapič?), h46 (Klobučar → Kramarič?
→ Harašimovič?); ③ h45 Straus × Spudič: POPRAVEK P91 — preveriti poroko v
04455 (04455 1896? Straus × Spudič); ④ h26/h75 selitvena hipoteza naprej;
⑤ luknja 41–60: 17 dokazanih (43 NOVA) — 41–60 ima 20 števil, 3 manjkajo
(42, 48, 49, 50, 51 manjkajo? — preveriti PT_GAP_KNOWN vs 41–60: 41, 43,
44, 45, 46, 47, 52–60 = 15 + 2?); ⑥ Željko veriga 10 signalov; ⑦ Fr. Klun
identifikacija (župnijski arhiv Podzemelj) [~].

## §70 — P93: župnija Podzemelj — krstna knjiga 04105, polno leto 1898 (issue #18) — 2026-10-16

**SAMPLE-TRANSCRIPTION-1898** (MERI, NE odloča; v7 join nespremenjen).
§69 nextSteps ①: širitev vzorca po letih (P79 1886 → … → P92 1897 →
**P93 1898**).

**Okvir**: skeni 101–109 == tiskane strani 98–106. **NOVELA P92 POTRJENA**:
stran == sken − 3 **ZA CELO LETO** (brez novih duplikatov; sken 105 =
str. 102 **brez Griblje vrstic** — pregledan, ni citiran; sken 101 = str. 98
brez potrjenih Griblje — r5 je Grišiniče). Glava **»1898.« na str. 98** po
1897 row 85; leto 1898 ima **96 vrstic**; **prelom 1899 na str. 106 =
sken 109 row 97→1** — oznake se ponastavijo, **novela P83 potrjena 11.
leto**; **1899 row 1 = Griblje 12 Marija — novo leto se začne z Griblji**.
Skeni 101–113 preneseni v /tmp/p93 (101 kopiran iz /tmp/p92; p93_fetch po
vzoru p92; ročna faza, NI v repu); izrezi 2x (L/R) + hišne forenzike 5x–6x
(pasovi popravljeni — r20/r30/r37/r42/r63/r76/r78/r79/r89/r96 re-crop po
odklonih) + imenske forenzike 4x–6x (Hrigar/Hrižan, Podrinc/Pendirec,
Šbrodarič/Brodarič, Vetročnik, Vrhovec) + datumski fragmenti; **15
kandidatov → 12 potrjenih Griblje** (3 izključeni: s101 r5 »Grišiniče 33«,
s107 r76 »Šriglje?«, s102 r20 **LEVI DEL UNIČEN** — desni del preživel:
Jurij Straus × Marija Jakofin, botra Matija Straucel × Barbara Jakofin;
verjetno Griblje [~], NEŠTET).

**Vzorec 1898**: **12 vpisov / 12 hiš — NARE (5. leto** po P87/P89/P91/P92):
40, 69, 89, 18, 32, 36, 33, 48, 63, 52, 53, 90 — **3 NOVE hiše (18, 48, 89)**
+ 9 ponovitev; kumulativ **229 vpisov / 77 hiš** čez tri knjige in
**TRINAJST let**.

**NOVA LUKNJA ŠTEVILKA: h48 (18. dokazana v 41–60** — PT_GAP_KNOWN dobi
+48; forenzika 6x: jasno 48, ne 40 — **dvojna zanka = 8**; prvi prebir
»40« napačen) + **h52 PRVI TRDNI PIN** (1887 block [~] preživel trojno
korekcijo 52→04→15; 1898 forenzika 5x: jasno 52) — luknja zdaj **18
dokazanih**. h18/h89 = NOVI številki izven luknje (18/89 v PT verigi 1825;
Kurrent 9 z dolgim repom γ-oblika pri 69/89).

**VRNITEV h63**: oče **Nikolaj Hrižan [Križan/Prižan] ISTI 6×** (1887 +
1889 + 1890 + 1892 + 1896 + 1898, brez 1897) — **P92 zaključek »h63
IZGINE — konec serije« POPRAVLJEN**; najbolj konstanten oče vzorca;
dojenček Jožef **† 6/6.1900** (dojenčijska umrljivost 1/12 potrjena + r37
[~] možna — najnižja po P92 7/19).

**NAJGOSTEJŠE GIBANJE GOSPODINJSTEV V VZORCU (4 rotacije v enem letu)**:
① h69 **MENJAVA** — Brinec (5 vpisov 1888–95) → **Nikolaj Straus × Marija
Jakobšič** (Straus na 4. hiši h71/h72/h45/h69; otrok Alojzij † 6.1.1983
»v Gribljah« po matičarjem pripisu — register sam potrjuje vas); ② h33
**MENJAVA** — Brinec (1889) → Dehlič × Rožek (**stari h33 oče Matija
Brinec zdaj BOTRA**); ③ **SELITEV Berkopne × Klobučar h40 (1897) → h48
(1898)** — ISTA ZVEZA, druga hiša; ④ h40 **MENJAVA** → **Anton Brodarič ×
Marija Milek** (= h46 oče 1893–97 — rotacija [~]; **očetovo ime PREČRTANO
v izvirniku** brez vidne zamenjave).

**ŠOLSKA HIŠA h90**: **TRETJI UČITELJ** — Kopitar (1890 + 1892) → **Alojzij
Vetročnik [~] UČITELJ × Leopolda Schmelzer** (nemški priimek); botr učitelj
**Ivan Vrhovec [~ Arhovec]** + Apolonija Majnik [~] — tretja učiteljska
generacija (1890 botra Janez Barle, 1892 nadučitelj botra). Zadnja Griblje
vrstica leta (24./29. 12.).

**Duhovniki**: **Rauq (Jos.) 8×** dominant (nadaljuje iz 1897) + **Šturm
(Fr.) 3×** + 1 neberljiv (r42) — **Klun (11× 1897) IZGINE**. **NOVELA
babica POTRJENA 4. LETO**: 12/12 PRAZNO (Trotter 0×). Statusi: ½ zemljak
× 10 + ¼ × 2 (r22 Straus, r72 Berkopne) + učitelj × 2. **0 nezakonskih**
med Griblji (r29 Obveca z praznima staršema = druga vas). **Matičar
pripisi 20./21. st. v 9 od 12 vpisov** (EMŠO blok 1982–83, † 1951/1963/
1974?/1975/1981/1983, poroke 1921/1922/1924/1928/1929) — najgostejša
pokritost doslej.

**KURRENT FORENZIKA 6 popravkov/odločitev**: ① s101 r5 »Griblje 39?« →
jasno **GRIŠINIČE 33** (druga vas — izključena); ② s107 r76 »Griblje?« →
jasno **ŠRIGLJE?** (druga vas — izključena); ③ s102 r20 **LEVI DEL
UNIČEN** (modri matičar pripisi 1971–83 + raztrgana meja); ④ s107 r72
»40?« → jasno **48** (6x); ⑤ s106 r63 »56?« → jasno **36** (5x); ⑥ s103
r22 »2?« → jasno **69** + r30 »81/31?« → jasno **89** (Kurrent 9 z repom).
Priimki: **Hrigar/Hrigovc = Hrižan/Križan cluster [~]** (po P91/P92),
**Podrinc = Pendirec cluster [~]** (po P86–P92), **Urk = Urh cluster [~]**
(po P87–P92). **ŽELJKO VERIGA 2 nova signala** (r14 botra Marija Željko +
r30 botra Nikolaj Željko — skupaj 12); **Kure signal** (r89 botra Ana
Kure — h1 familija); **Šimec**: r37 oče Matija Šimec = r89 botra (ista
oseba oče + botra v enem letu); Podrinc/Pendirec cluster 6 pojavitev
(r30 oče Marko = r78 botra).

**Integracija**: parish.ts HOUSE_VITALS **211 → 223** (+12 blokov 1898,
vsi DOCUMENTED; komentar P93 z okvirjem); atlas.ts PT_GAP_KNOWN **+48**
(18. dokazana); qa-parish.ts **qa-p93** (94. kontrola; celoven neodvisen
preracun: okvir − 3/brez duplikatov/NOVELA babica 12 praznih/NOVA LUKNJA
48 pin + SELITEV/VRNITEV h63/h52 TRDNI pin/sidra 12/PT 9/3/NOVE hiše 18/
48/89/kontinuitete 22 pinov (scan-pini)/vitals 223); dovoljenja 1898:
qa-p85 h90, qa-p86 h53, qa-p92 h40 (allow mehanizem); vitals pini 211 →
223 (7 testov); **POPRAVI ZASTARELIH SKRIPT (regresije po P92)**: p80
I7 (PT_GAP_HOUSES posodobljen +43/45/46/48 + scoping 38/9 + vitals 223),
p85–p92 (filtri vesolja lastnega leta — poznejši bloki 1897/1898 ne
spreminjajo zgodovinske klasifikacije novih hiš: p85 + 1897/1898, p86 +
1897/1898, p87 + 1897/1898, p88 + 1897/1898, p89 + 1895–1898 filter,
p90 + 1896–1898 filter + None-varna repeatHouses, p91 + 1897/1898 filter
+ kumulativ 199/71 POPRAVLJEN nazaj na lastni JSON, p92 + 1898 filter);
vseh 14 skript p80–p93 --check **PASS** (exit 0). Kartica NI dodana
(vzorec P77–P93). tsc 0 / lint 0; **/api/qa dev 94/94** (qa-p93 True);
v7 NESPREMENJEN.

**nextSteps**: ① **P94 = leto 1899** (prelom str. 106 row 1 = sken 109;
skeni 110–113 že v /tmp/p93; 1899 row 1 = Griblje 12 Marija!); ② mrliška
knjiga 04894 1887–1896: smrti prvih žen — dokaz menjav h69 (Brinec →
Straus 1898!), h33 (Brinec → Dehlič), h40/h48 (Berkopne selitev), h90
(Kopitar → Vetročnik); ③ poročna 04455: Straus × Spudič (potrditev h45
popravka) ali Berkopne × Klobučar; ④ Željko veriga 12 signalov; ⑤ luknja
41–60: 18 dokazanih (48 NOVA) — manjkajo še 42, 49, 50, 51 (in 41–60 = 20
števil; preveriti PT_GAP_KNOWN: 41, 43–48, 52–60 = 16); ⑥ produkcija
Vercel: po rate-limit resetu (~2026-10-17 18:24 UTC) dohiti P90–P93 →
QA 94/94.

## §71 — P94: župnija Podzemelj — krstna knjiga 04105, polno leto 1899 (issue #18) — 2026-10-17

**SAMPLE-TRANSCRIPTION-1899** (MERI, NE odloča; v7 join nespremenjen).
§70 nextSteps ①: širitev vzorca po letih (P79 1886 → … → P93 1898 →
**P94 1899**).

**Okvir**: skeni 109 row 97 – 118 row 104 == tiskane strani 106–115.
**NOVELA P92 POTRJENA**: stran == sken − 3 **ZA CELO LETO** (brez novih
duplikatov; sken 118 = str. 115 **samo okvir** — ni citiran za vpise).
**1899 r1 = Griblje 12 Marija na str. 106** (P93 napoved — novo leto se
začne z Griblji); leto 1899 ima **104 vrstic**; **prelom 1900 NA SREDINI
str. 115 = sken 118 row 105** — **PRVIČ V VZORCU** se novo leto NE začne
na novi strani (prazne vrstice + glava »1900.«); 1900 row 1 = Krasinec —
**prvič z drugo vasjo**; **novela P83 potrjena 12. leto**.

**VSI vpisi z Griblji: 15 vpisov / 15 hiš — NARE (6. leto)** po
P87/P89/P91/P92/P93 — in **PRVO LETO BREZ znotraj-letnih ponovitev**
(vsaka hiša 1×): 12, 46, 27, 60, 59, 22, 41, 21, 40, 1, 30, 75, 57, 49,
34 — **2 NOVI hiši** + 13 ponovitev; skupaj s P79–P93 vzorec **244 vpisov
/ 79 hiš čez tri knjige in ŠTIRNAJST LET** (238 vitals).

**NOVA ŠTEVILKA h22** (v PT naboru 1825 — ATLAS_HOUSES že vsebuje 22;
prvi matrični dokaz; forenzika 7x: jasno 22): oče **Nikolaj Milek [~] ×
Marija Klepec** — NOVA ZVEZA (Milek cluster h65/h29/h30/h70 brez tega
para; mati [~ ista oseba kot botra h60 Marija Klepac — botra 13.3. +
mati 20.3. v 1 tednu]; † 2/[5-6].99 — dojenčnica). **NOVA LUKNJA ŠTEVILKA
h49 — 19. dokazana v 41–60** (PT_GAP_KNOWN +49; forenzika 8x: jasno 49;
**luknja zdaj 42/50/51**): oče **Nikolaj Brodarič × Marjeta Milek** — NOVA
ZVEZA (Nikolaj Brodarič = **botra h48 1898 → oče h49 1899**); botra
Nikolaj [S]Žegina? [Segina?] + Katarina Berkopeč [Berkopne?] (¼);
dojenčnica **† 24/6.1900** (~7 mesecev).

**h60 TRDNI PIN**: 4. VPIS ISTA ZVEZA **Željko × Brodarič**
(1893+1894+1897+1899) + **3. ISTA BOTRA PARA Pendirec × Klepac**
(1893+1894+1899) — hišna št. **pod modrim pripisom**: kanalna forenzika
(temen sloj »…o 6o«) + **STRUKTURNA POTRDITEV** (oče = h60 oče + botra
para = h60). **ŽELJKO VERIGA 13.+14. signal** (oče h60 + botra h57
Nikolaj Željko). **SEGINA VERIGA 3 signali v enem letu** (oče h1 r61 +
botra h49 r94 + botra h34 r100 Nikolaj Segina).

**h40 TRETJA DRUŽINA V TRIH LETIH** (najgostejša rotacija vzorca):
Berkopne (1897) → Brodarič (1898 [~]) → **Martin Straus bajtar × Barbara
Spudič** (1899) — **STRAUS × SPUDIČ = POTRDITEV poročnega lead-a 04455**
(§70 nextSteps ③). **MENJAVE GOSPODINJSTEV 1899**: h1 **Željko
(1888–96) → Nikolaj Segina × Marjeta Milek** (**SEGINA VERIGA: h70 1893 →
h30 1895 → h1 1899 — 3 hiše / 6 let**; kraj »Griblja« varianta — smrtna
opomba POTRJUJE Griblje: † 31.3.1975 v Gribljah); h30 **4. DRUŽINA v 9
letih** (Milek → Jakljevič 1893 → Šegina 1895 → **Janez Županič 1899** —
**ŽUPANIČ CLUSTER 3 signali**: h73 1894 + h30 + botra Ana Županič);
h34 **2. DRUŽINA** (Šimec 1887 → **Nikolaj Šilak? × Katarina Klobučar**);
h57 **OČE MENJAVA** Peter Pezdirec (1888–94) → **Miha Pozdirec** (brata?
sin?; Miha = botra h41 1896).

**Kontinuitete**: h46 **5. VPIS ISTA ZVEZA** očeta (4. varianta matere:
Klobučar? → Kramarič? → Harašimovič? → **Škaradinič?** — priimek potrjen
pri Krasinec 32); h27 **6. VPIS** (oče 2. branje: Stukar/Stubhar 1893 →
**Knekar? 1899**; botra h21 Janez Knekar = **KRIŽNI SKLIC** z očetom
h27); h41 **4. VPIS ISTA ZVEZA** (Kušič × Jakobič); h21 4. vpis — 2. VPIS
ISTA ZVEZA Požek × Šimec; h75 **3. VPIS ISTA ZVEZA** (Jakobič × Stubljar
— 4. pisavska varianta priimka matere); h59 2. vpis (1889 NEZAKONSKA
Marinka — 1899 PRVI imenovani oče: Simič × Kure); h12 **mati MENJAVA [~]**
(Straus 1897 → Cvitkovič 1899; botra 1899 = 1897 mati?! — možna zamenjava
celic P92). 0 nezakonskih; **NOVELA babica POTRJENA 5. LETO: 15/15
PRAZNO/poškodovano**; **DOJENČIJSKA UMRLJIVOST 3/15** (r1 † 25/6.99 [~],
r26 † 2/[5-6].99 [~], r94 † 24/6.00) — višja kot P93 1/12. **DUHOVNIKI**:
Šturm (Fr.) 6× + Rauq (Jos.) 4× + **Klun (Fr.) 2× VRNITEV** iz 1897 + 3
neberljivih (r71 raztrgan, r94/r100 »Jos. Kergo?«). Statusi: ½ zemljak
× 14 + **bajtar × 1** (r43 Straus). **KURRENT FORENZIKA**: r13 hišna pod
pripisom (kanalna + strukturna — 60 TRDNO); r89 **datum UNIČEN**
(raztrgan rob str. 113 — ~november po sosedi r90); r71 datum popravek
(»23« + »2« nad — verjetno 2.10. + krst 3.10.); r94 jasno 49 (ne 34 —
dvojna forenzika z r100); r25 **NEŠTET** (matičar ČRNO nadpisal kraj +
hišno — ime Jožef; po vzoru P93 r20); r27 Berkoviše + r93 »Germ«
izključeni (drugi vasi). Matičar pripisi 20./21. st. v večini vpisov
(† 1964/1965/1969/1975/1984, poroke 1921/1926/1930, EMŠO blok).

**Integracija**: parish.ts HOUSE_VITALS **223 → 238** (+15 blokov 1899,
vsi DOCUMENTED; komentar P94 z okvirjem; h59 blok popravljen — 1889
Marinka nezakonska, NE Rudolf/Pezdirec); atlas.ts PT_GAP_KNOWN **+49**
(19. dokazana); qa-parish.ts **qa-p94** (95. kontrola; celoven neodvisen
preracun: okvir − 3/brez duplikatov/prelom 1900 NA SREDINI strani/NOVELA
babica 15/NOVA LUKNJA 49 + 19. dokazana/h60 TRDNI PIN + 4. VPIS + 3.
BOTRA PARA/h40 STRAUS × SPUDIČ + TRETJA DRUŽINA + bajtar/sidra 13/PT 9/6/
NOVI hiši 22+49 brez priora/kontinuitete 27 pinov/vitals 238); dovoljenja
1899: qa-p85 h30 + h41, qa-p87 h12 + h75, qa-p88 h46, qa-p92 h40 (allow
mehanizem); vitals pini 223 → 238 (8 testov); **POPRAVI ZASTARELIH
SKRIPT (regresije po P93)**: p80 I7 (vitals 238), p85–p92 (filtri
vesolja + 1899: p85/p86/p87/p88/p89/p90/p91 nabori + 1899, p92 filter
1898 → (1898, 1899)), p85–p93 (vitals 238 + kumulativ 244 + hiše 78);
vseh 15 skript p80–p94 --check **PASS** (exit 0). Kartica NI dodana
(vzorec P77–P94). tsc 0 / lint 0; **/api/qa dev 95/95** (qa-p94 True);
v7 NESPREMENJEN (p76 --check PASS).

**nextSteps**: ① **P95 = leto 1900** (prelom str. 115 row 105 = sken 118;
skeni 119–120 že v /tmp/p94; 1900 row 1 = Krasinec — novo leto prvič
začne z drugo vasjo; potrebni skeni 119–125+); ② mrliška knjiga 04894
1887–1896: smrti prvih žen — dokaz menjav h69/h33/h40/h48/h90; ③ poročna
04455: **Straus × Spudič** (krstno POTRJENA — najti poroko: datum + hiši)
ali Berkopne × Klobučar; ④ Željko veriga 14 signalov + Segina veriga 3
signali v enem letu; ⑤ luknja 41–60: 19 dokazanih (49 NOVA) — manjkajo še
42, 50, 51; ⑥ produkcija Vercel: dohiti P94 → QA 95/95.

## §72 — P95: župnija Podzemelj — krstna knjiga 04105, polno leto 1900 (issue #18) — 2026-10-17

**SAMPLE-TRANSCRIPTION-1900** (MERI, NE odloča; v7 join nespremenjen).
§71 nextSteps ①: širitev vzorca po letih (P79 1886 → … → P94 1899 →
**P95 1900**).

**Okvir**: skeni 118 row 105 (SREDINA str. 115 — P94 dokazano) – 124
row 77 == tiskane strani 115–121. **NOVELA P92 POTRJENA**: stran ==
sken − 3 **ZA CELO LETO** (118→115 … 124→121; brez novih duplikatov).
**1900 r1 = Krasinec Matija (2./2. Januar)** — **PRVIČ se novo leto začne
z DRUGO VASJO** (ne Griblji); leto 1900 ima **77 vrstic**; sken 121 =
**DVA podatkovna panela** (r33–44 levo + r45–56 desno), sken 122 = DVA
starševska panela (citiran v dokazu za starše r45/r46, brez data vpisov);
skeni **r51–56 FIZIČNO RAZTRGANE** (podatki izgubljeni, starši znani);
sken 125 = str. 122 = glava 1901 (samo okvir).

**VSI vpisi z Griblji: 16 vpisov / 16 hiš — NARE (7. leto)** po
P87/P89/P91/P92/P93/P94 — in **2. LETO BREZ znotraj-letnih ponovitev**:
1, 67, 10, 32, 65, 20, 14, 90, 23, 9, 54, 16, 58, 31, 25, 45 — **1 NOVA
hiša** + 15 ponovitev; skupaj s P79–P94 vzorec **260 vpisov / 80 hiš čez
tri knjige in PETNAEST LET** (254 vitals).

**NOVA HIŠA h67** (prvi matrični dokaz; hiša v PT naboru 1825 —
ATLAS_HOUSES vsebuje 67 v bloku 61–99; **80. hiša vzorca**): oče **Nikolaj
Straus [~] gumbar** (status »2 gumbar« ali »½ gumbar« — Kurrent 2/½ dvom)
× **Marija Jakopič** — **STRAUS gumbar mreža** (h45 Martin Straus, h31
mati Straus, botri Straus na h58/h32/h28); EMŠO matičarja
1002900505074 = roj. 10.02.1900 (ujema se z vrstico!); podpis v raztrganem
robu — neberljiv.

**SCOPING POPRAVKI 1900** (celostranski pregled): r5→r3 + r8→r6 (margini
str. 115 raztrgani — 8 vrstic, SEKVENCA BREZ ANOMALIJE; scopingova
hipoteza o 2 nenumeriranih vrsticah **ZAVRŽENA**: Barbara = r7, Jožef =
r8); r27→r28…r30→r31 (scoping izpustil r27 Otok 8); **4 IZPUŠČENE vrstice
najdene** (r45 h16, r46 h58, r59 h31, r63 h25); **scopingov r49 »Griblje
51 NOVA LUKNJA« ZAVRŽEN** — vrstica bere **Primostek 5** — **luknja
42/50/51 NESPREMENJENA** (19 dokazanih v 41–60). **PT 13/3** (45/54/58 v
luknji — vsi trije že dokazani prej; **58 NI v PT verigi** — PT_GAP_KNOWN
že vsebuje 58).

**NOVELA babica: stolpec PRVIČ IZPOLNJEN po 15 letih** (1886–99 prazen!):
**Fottre/Foča 7× + Hrižan 1×** + 6 praznih + 2 neberljiv/raztrgan.
**DUHOVNIKI: Šturm 0× — PRVIČ V VZORCU** (po 6× v 1899) + Rauq 9× +
**Perg 4× + Klunček 2× (nov duhovnik)** + 1 neberljiv.

**Ključne kontinuitete**: h1 **ŽELJKO VRNITEV**: 1888–96 Nikolaj Željko ×
Katarina Kure → 1899 Segina → 1900 **Jurij Željko × Barbara Kure** —
Jurij Željko = **BOTER h1 1888 → OČE 1900** (**ŽELJKO signal 15**); h31
**6. PIN ISTA ZVEZA Martin Papič × Marjeta Straus** (1887+1890+1891+1894+
1897+1900 — **najdaljša zaporedna zveza vzorca**; 11. vpis); h45 **3. PIN
ISTA ZVEZA Martin Straus × Barbara Spudič** (1896+1897+1900) — **04455
POROČNI LEAD: krstno 3× POTRJENA ista zveza — iskati poroko v 04455**;
h90 **ŠOLSKA HIŠA 4. PIN**: ISTA UČITELJSKA DRUŽINA Vetročnik × Schmelzer
(1898 r27 Alojzij) — hči **Leopoldina po materi Leopoldi!**; učitelji:
Kopitar (1890–92) → Vetročnik (1898–1900); **KONFLIKT DATUMA r30**:
vrstica »40 jun« [~] vs matičarjev EMŠO 2405900505109 = roj. 24.05.1900 —
MERI: EMŠO avtoritativno (matičar je bral civilni register); h23 **4. PIN
ISTA ZVEZA Brinec × Dehlič** (1893+1894+1897+1900) — **P88 1893 »Debič?«
= Dehlič REŠENO** z 1900 forenziko; h14 2. VPIS — **1896 (P91) oče MERI
dvom (»ali drug Janez Brinec?«) → 1900 forenzika REŠUJE P91**; h58 **5.
PIN + PRVA MENJAVA ŽENE** na h58 (1889–95 Ana Dragoš → 1900 **Katarina
Kranbič**); h32 **8. PIN** — 1893 (P88) »Meh/Mrh?« **POTRJENO** z 1900
»Meh« (KURRENT U/M varianta istega priimka ALI prava menjava — MERI);
h65 **6. VPIS ISTI OČE** Matija [Milek] (1887–1900) + 5. varianta matere
(Tožek?); h20 **3. PIN** Pendirec × Klepec (1897+1900); **MENJAVE
GOSPODINJSTEV**: h10 (Brinec/Perdune 1897 → **Grabrijan × Pozdirec** —
scoping »Gmajrjan?« POPRAVLJENO), h9 (Jakobič/Žumič 1896 → **Muc × Kure**
— Kure = h1 mati rodbina, križni sklic; svinčnik »Štumer?«), h16
(Jaklič/Brinec 1897 → **Novak × Šilak** — **ŠILAK križni sklic** z h16
1886 mrliško), h25 (Klepec/Tome 1896 → **Brinec × Segina** — **SEGINA
signal 4**: mati Katarina Segina + boter Leopold Šegina). **h54 starši
RAZTRGANI** (sken 122 levo fizično odtrgan — **edina izguba staršev med
Griblje vpisi 1900**); r19 dnevi RAZTRGANI + mati IME PREČRTANO; pripis
»Umrla dne 14.3.1954« pripisnost r30/r31 dvomna (MERI: po položaju črte
r31, dvom v honesty). **DOJENČIJSKA UMRLJIVOST 5/16** (r3 † 1907 ~7 let,
r23 † 2/6.00 ~1 mesec, r45 † 7/11.02, r46 † 8/5.03, r69 † 9/2.03 ~15
mesecev). **EMŠO blok matičarja** (r6/r28/r31 — vsi ujemajo z vrsticami!).
Matičar pripisi v 13/16 vpisov († 1954/1955/1965/1969?/1977/1980/1982/
1984/1985/1991, poroke 1921/1933/19??).

**Integracija**: parish.ts HOUSE_VITALS **238 → 254** (+16 blokov 1900,
vsi DOCUMENTED; komentar P95 z okvirjem); atlas.ts PT_GAP_KNOWN
**NESPREMENJEN** (P95: brez novih — scopingov h51 ZAVRŽEN; luknja
42/50/51 ostaja; 45/54/58 = ponovitve že dokazanih); qa-parish.ts
**qa-p95** (96. kontrola; celoven neodvisen preracun: okvir − 3/brez
duplikatov/sken 122 starševska/NOVELA babica 6+8/NOVA HIŠA 67 + prvi
matrični dokaz + 80. hiša + gumbar/h1 ŽELJKO VRNITEV + BOTER h1 1888/h31
6. PIN + najdaljša zveza/h45 3. PIN + 04455/h90 ŠOLSKA HIŠA 4. PIN +
Leopoldina/h23 4. PIN + REŠENO/h58 5. PIN + MENJAVA ŽENE + Kranbič/sidra
16/PT 13/3/NOVA hiša 67 brez priora/kontinuitete 28 pinov/vitals 254);
dovoljenja 1900: qa-p85 h90, qa-p88 h23, qa-p90 h20, qa-p91 h9 + h14 +
h45, qa-p92 h10 (allow mehanizem); vitals pini 238 → 254 (9 testov);
**POPRAVI ZASTARELIH SKRIPT (regresije po P94)**: p80 I7 (vitals 254),
p85–p92 (filtri vesolja + 1900: nabori + 1900), p85–p94 (vitals 254 +
kumulativ 260 + hiše 79); vseh 16 skript p80–p95 --check **PASS**
(exit 0). Kartica NI dodana (vzorec P77–P95). tsc 0 / lint 0; **/api/qa
dev 96/96** (qa-p95 True); v7 NESPREMENJEN (p76 --check PASS).

**nextSteps**: ① **P96 = leto 1901** (glava na str. 122 = sken 125; skeni
125–128 že v /tmp/p95); ② mrliška knjiga 04894 1887–1896: smrti prvih
žen — dokaz menjav h1/h10/h16/h58/h9 + »Okljuka?« mikrotoponim (r15) v
zemljevidih 1825/1870; ③ poročna 04455: **Straus × Spudič** (krstno 3×
POTRJENA — najti poroko: datum + hiši) ali Berkopne × Klobučar; ④ h51/
h42/h50 v mrliški 04894 + poročni 04455 (luknja 42/50/51); ⑤ Željko
veriga 15 signalov + Segina veriga 4 signali; ⑥ produkcija Vercel:
dohiti P95 → QA 96/96.

## §72 — P96: župnija Podzemelj — krstna knjiga 04105, polno leto 1901 (issue #18) — 2026-10-17

**SAMPLE-TRANSCRIPTION-1901** (MERI, NE odloča; v7 join nespremenjen).
§71 nextSteps ①: širitev vzorca po letih (P79 1886 → … → P95 1900 →
**P96 1901**).

**Okvir**: glava **»1901.« na sredini str. 122** (sken 125, P95 dokazano)
– **row 87 na str. 129** (sken 135; **glava »1902« na dnu iste strani**)
== tiskane strani **122–129** (**87 vrstic**). **NOVELA P96 — TRIJE
podvojeni skeni**: **127/128** (str. 124: sken 127 z dvema belima
matičarskima nalepkama čez r32/r33; sken 128 = ISTA stran z nalepkama
**PREPOGNJENIMA** na levi rob → **r32/r33 REŠENI**: Juni 1/2 Primostek 2
Anton EMŠO 01.06.1901 + Gradac 32?/33? Jožef EMŠO 01.06.1901; nalepki
1989 = † Zagreb/† Črnomelj), **129/130** (str. 125), **133/134** (str.
128). Stran == sken **− 3** (125–127) / **− 4** (129–130 → 125) /
**− 5** (131–132 → 126–127) / **− 6** (135 → 129).

**NOVELA formata**: od str. 125 (sken 129) skeni = **celo-spread**
fotografije — LEVA stran = podatkovna tabela (Zaporedna št./Mesec in dan/
Rojstni kraj/Hiša/Ime/Vera/Spola/Stan), DESNA stran = Roditelja + Botra +
Babica pomočnica + Podpis mašnika krščevalca; vrstični pasovi sovpadajo
po y (isti fizični list). **NOVELA mesecev**: **r65–r69 NOVEMBER**
(EMŠO r66 08.11.1901 + r68 16.11.1901) — zgodnje branje »December« za
r65–r69 NAPAČNO; December se začne na r70 (marker + EMŠO r83 18.12.1901);
**r36 »Jurij«? = JUNI** (sekvence r38 29/29 Juni → r39 »July 10/10«
vsiljuje).

**VSI vpisi z Griblji: 10 vpisov / 9 hiš**: 12, 12, 7, 54, 2, 17, 65,
24, 19, 44 — **h12 ×2 = PRVA PONOVITEV znotraj leta po 1893** (NARE
zaporedje 1894–1900 prekinjeno po 8 letih; r1 Peter 3./4. Januar Gregor
Juvan? × Barbura Cvetkovič vs r36 Alojzij 17./17. Juni **Matija Straus ×
Marija Jakobič** — več-družinska hiša/menjava; pripis † 17/6.02 —
dojenček) — **1 NOVA hiša (19) + 8 ponovitev**; skupaj s P79–P95 vzorec
**270 vpisov / 81 hiš čez tri knjige in ŠESTNAJST LET** (264 vitals).

**NOVA HIŠA h19** (prvi matrični dokaz; hiša v PT naboru 1825 — brez
spremembe atlas.ts; **81. hiša vzorca**): oče **Nikolaj Hriče? [~]
bajtar** (najemnik kmeta) × Cecilija Hvalica? [~]; Katarina (21./21.
November); botra pod madežem [~]; podpis Jos. Rauq. h24 pripis »Umrła
11.10.1946 griblje št 24« **SAMOPOTRJUJE hišo** (Ivana, Janez Božek? ×
Ana Finec? [Simec? — F/S dvom]; 9. VPIS). h7 Kurrent 2/7 dvom [~] —
**EMŠO 2107901505598 = 21.07.1901 sidro** (Marija, Jakob Toter ×
Katarina Jakobšič — oče = rodbina babice Marjeta Toter!). h65 **EMŠO
1110901503024 = 11.10.1901 sidro** (Doroteja, Matija Mitek? [Mrtek?] ×
Katarina Pošek?; 7. VPIS ISTI OČE Milek 1887–1900). **PT 7/2** — h44
(3. VPIS: Francišek, Martin Jurajevič bajtar × Marjana Krašovec) + h54
(4. VPIS: Anton, Peter Gruzec? žajfar × Ana Butala) v luknji — **oba že
v PT_GAP_KNOWN → brez novih številk**; **luknja 42/50/51
NESPREMENJENA** (19 dokazanih).

**DUHOVNIKI: Kulbinek? 7×** (= P95 »Klunček?« — isti podpis, **boljše
branje na spread formatu**) + **Jos. Rauq 2×** + **NOV podpis Fran.
Dostál 1×** (češko priimek; tudi ne-Griblje r63/r67/r70/r71/r80/r83).
**NOVELA babica 2. leto izpolnjeno**: **Toter 6×** (r1/r36/r48/r57/r65/
r69 — oče r48 Jakob Toter = rodbina babice!) + **Mavrefič** (r81) +
**Mikl** (r59) + **Tolar?** (r51) + **Tome** (r52) — **10/10
imenovanih**. Nezakonski 0 (okvir r54 mati »samska dekla« — Cerkvišče
31, ne-Griblje). **DOJENČIJSKA UMRLJIVOST 2/10** (r36 † 17/6.02, r52 †
17/3.03; okvir še r79 † 11/2.02 — ne-Griblje). **EXCLUDED**: r35
(Griblje [~], ime Anton [~], hiša pod prosojnim trakom + spodnji rob
odtrgan — neuporabno za vitals; **odprt lead**: konflikt h24 r65 — ista
hiša ne more imeti dveh dojenčkov Jun+Nov iste matere; starši Jožef?
Hrušov? × Marija Javhnik?) + r47 (bela matičarska nalepka 26.01.1989 —
† Novo mesto; ime Neža [~]; starši **Jurij Straus × Barbura Jakobič**,
botra Janez Kralj + Marija Urh — **MOŽEN Griblje vpis** (Straus mreža),
hiša nedokazljiva; za str. 125 NI podvojenega skena z odprtimi
nalepkami).

**Integracija**: parish.ts HOUSE_VITALS **254 → 264** (+10 blokov 1901,
vsi DOCUMENTED; komentar P96 z okvirjem + novelami); atlas.ts
PT_GAP_KNOWN **NESPREMENJEN** (P96: brez novih — 44/54 že vsebovani;
luknja 42/50/51 ostaja); qa-parish.ts **qa-p96** (97. kontrola;
celoven neodvisen preracun: trije dup pari + stran == sken − 3/− 4/
− 5/− 6/NOVELA formata spread/NOVELA mesecev November/NOVA HIŠA 19 +
81. hiša + bajtar/h12 ×2 PRVA ponovitev po 1893/sidra EMŠO
2107901505598 + 1110901503024/babica 10/10 + Toter 6×/duhovniki
Kulbinek? 7× + Rauq 2× + Dostál 1×/PT 7/2/NOVA hiša 19 brez
priora/kontinuitete 8 pinov/vitals 264); dovoljenja 1901: qa-p85 h7
([1890, 1901]), qa-p87 h12 ([1892…1899, 1901]) (allow mehanizem);
vitals pini 254 → 264 (10 testov); **POPRAVI ZASTARELIH SKRIPT
(regresije po P95)**: p80 I7 (vitals 264), p85–p92 (filtri vesolja +
1901; vitals 264 + kumulativ 270 + hiše 80), p93 (vitals 264 +
kumulativ 270 + hiše 80), p94/p95 (filtri vesolja izključujejo 1901/
1900+1901 — zgodovinske klasifikacije zamrznjene); vseh **17 skript
p80–p96** --check **PASS** (exit 0). Kartica NI dodana (vzorec
P77–P96). tsc 0 / lint 0; **/api/qa dev 97/97** (qa-p96 True); v7
NESPREMENJEN (p76 --check PASS). QA popravki po prvi oceni: qa-p96
whatSi babica tokeni (h7 »babice« → »babica«, h65 + h44 babica
manjkala) + qa-p85/qa-p87 allow liste (+ 1901 bloki).

**nextSteps**: ① **P97 = leto 1902** (glava »1902« na dnu str. 129 =
sken 135; skeni 135–140 že v /tmp/p96 — 6 strani; pričakovano ~10–15
novih skenov); ② mrliška knjiga 04894 1887–1896: smrti prvih žen — dokaz
menjav h1/h10/h16/h58/h9 + dojenčki † iz krstnih (r36/r52 1901); ③
poročna 04455: **Straus × Spudič** (krstno 3× POTRJENA — najti poroko:
datum + hiši) ali **Straus × Jakobič** (h12 r36 — nova zveza 1901); ④
h51/h42/h50 v mrliški 04894 + poročni 04455 (luknja 42/50/51); ⑤ r35
lead: hiša pod trakom (sken 127/128 ponovni pregled z novim
obdelovalnim pasom); ⑥ produkcija Vercel: dohiti P96 → QA 97/97.

## §73 — P97: župnija Podzemelj — krstna knjiga 04105, polno leto 1902 (issue #18) — 2026-10-17

**SAMPLE-TRANSCRIPTION-1902** (MERI, NE odloča; v7 join nespremenjen).
§72 nextSteps ①: širitev vzorca po letih (P79 1886 → … → P96 1901 →
**P97 1902**).

**Okvir**: glava **»1902« (podčrtana) na dnu str. 129** (sken 135, P96
dokazano; r1 = Podzemelj 6 Marija 1./1. Januar; **rows 1–7 na dnu str. 129**,
r7 v pregibu) – **row 81 na str. 136** (sken 144; **glava »1903.« NA SREDINI
str. 136** — kot prelom 1900 NA SREDINI str. 115 (P94); **1903 r1 = Griblje
24** 4./5. Januar — novo leto spet začne Griblje; P98 lead) == tiskane
strani **129–136** (**81 vrstic**). Stran == sken **− 6** (135–137) /
**− 7** (139–141) / **− 8** (143–144). **NOVELA P97 — DVA podvojena para
skenov**: **137/138** (str. 131) in **141/142** (str. 134).

**NOVELA formata**: 1902 = **NOVA TISKANA knjiga** — naslov »Rojstna in
krstna knjiga.«, **predtiskan okvir z vsemi kolonami na ENI strani** (podatki
+ Roditelja + Botra + Babica + Podpis — KONEC spread-formata 1901), predtiskano
**»Leto 18|02«** (duhovnik dopisal »02« v 19.-stoletno formo).

**VSI vpisi z Griblji: 12 vpisov / 12 hiš**: 58, 87, 30, 22, 3, 27, 77, 16,
91, 36, 25, 14 — **NARE se nadaljuje (8. leto)** po prekinitvi 1901 (h12 ×2)
in **PRVO LETO VZORCA BREZ NOVIH HIŠ** (1886–1901 je vsako leto dodalo vsaj
eno; **h3 = 1889, h87 = 1895 — obe že v vitals**); skupaj s P79–P96 vzorec
**282 vpisov / 81 hiš čez tri knjige in SEDEMNAJST LET** (276 vitals).

**PT 11/1** — h58 v luknji 41–60 (že v PT_GAP_KNOWN — brez novih številk);
**luknja 42/50/51 NESPREMENJENA** (19 dokazanih). Sidra: h30 **SEGINA
VRNITEV** (r16 oče **Nikolaj Segina [~] × Marjeta Milek [~]** — hišna
forenzika 4× **jasno 30, NE 36!** — SEGINA veriga h70 1893 → h30 1895 →
h1 1899 → h30 1902, **signal 5**); h25 (r59 **4. VPIS — 1900+1902 ISTA
ZVEZA Matija Brinec × Katarina Segina** + boter **Danijel Segina** — signali
5+6; EMŠO sidro **r39 0307902505120 → 03.07.1902** na h27); h16 (r46
**STRAUS × SPUDIČ — TRETJA hiša istega para: h45 1896/1897/1900 → h40 1899 →
h16 1902** — **04455 POROČNI LEAD krstno 5× POTRJEN**).

**MENJAVE/BRANJA DRUŽIN**: h87 (r12 — **1895 Marko Pegdirec? = 1902 »Perdinec?«
KURRENT — VERJETNO ISTI oče**; botra **Marija Željko** — ŽELJKO signal 16;
1895 podcelica že Nikol. Hrižan × Marija Željko!), h77 (Pošek 1890 →
**Nikolaj Cindrič cevljar** 1902), h27 (**7. VPIS** — Knekar?/Stukar? →
**Janez Šimec × Marija Kure** — ŠIMEC križni sklic h34 1887), h22 (r28 —
žena **Klepec 1899 → Ana Žurrič? 1902** — MERI; ime otroka pod modrimi
matičarskimi zapisi — temno črnilo »Alojzij«, 4× zoom), h3 (1889 Nikolaj
Županič? → **Matija Papič? × Katarina Novak**), h58 (r8 — oče **»Janez
Povk?«** — nova branja po 1900 Kranbič ženi), h91 (r50 — **»Murov?« = Muc?**
— 1895 Janez Muc mlinar/kovač, **ISTA žena Ana Kure**), h36 (r51 — **6. VPIS
— Janez Vrižan? [Križan?] × Katarina Straus**, botri **Straus par**).

**DUHOVNIKI: Dostál 8×** (podpis **»Stanislav Dostál«** v 5/8 vpisov:
r28/r39/r50/r59/r75; P96 1901 **»Fran. Dostál«** — isti duhovnik z dvema
zapisoma imena ALI dva — MERI, odprt) + **Jos. Rauq 4×** — **Kulbinek 0×**
(po 7× v 1901!) + **Šturm 0×**. **NOVELA babica 3. leto izpolnjeno**:
**Toter 9×** + Adamič? 2× (r8 Barbura, r16 Marija) + Papič? 1× (r32) —
**12/12 imenovanih**. **ŽELJKO signali 16+17** (r12 botra Marija Željko na
h87 + r50 boter Nikolaj Željko? na h91 — h1 rodbina).

**DOJENČIJSKA UMRLJIVOST 3/12** (r16 † 8/2.03, r46 † 1/9.03, r51 † 1/5.03;
okvir: r4 Primostek 14 † 2/11.02 — ne-Griblje; r8 † 13/1.04 otrok ~1 leto +
r32 † 25/8.1912 otrok 10 let — ne šteta med dojenčke). Nezakonski 0 (okvir:
r34 Podgomej? nezakonski + r37 Zamaj? **mrtvorojen** nezakonski — bež,
ne-Griblje). **Okvirna anomalija: r72/r73 Boršt — BRATA, oba † 15/6.1918
(prva svetovna vojna!)**. **EXCLUDED**: r33 (Griblje [~] Ana, **hiša pod
modrim matičarskim zapisom »zap. št. 4524/1«** — kanalna filtracija ni
pokazala temnega črnila; starši Matija Hrišič? × Nina? Jakobšič?, botra
Jakob + Katarina Toter; † 19.10.1981 Novo mesto — **odprt lead**: civilni
register bi razkril hišo) + r62 (bela matičarska nalepka 15.01.1995 Piran —
vas/hiša nedokazljiva; Žugelj botra = možen Griblje signal).

**Peskovnik-nadomestilo (novost P97)**: med fazo je sandbox ponastavil
/home/z/muzej + /tmp — repo obnovljen iz GitHub zrcala (b5a25d7 = P96, PAT
avtoriteta; GitLab vir resnice == b5a25d7, potrjeno prejšnjo sejo), /tmp/p97
skeni ponovno prenešeni (p97_fetch), P97 artefakti rekonstruirani iz sejine
forenzike (vse transkripcije ostale v seji). Lekcija: dvorogi push PO vsaki
fazi je rešil vsa dela (nič ni bilo izgubljeno).

**Integracija**: parish.ts HOUSE_VITALS **264 → 276** (+12 blokov 1902, vsi
DOCUMENTED; komentar P97 z okvirjem + novelami); atlas.ts PT_GAP_KNOWN
**NESPREMENJEN** (58 že vsebovan; luknja 42/50/51 ostaja); qa-parish.ts
**qa-p97** (98. kontrola; celoven neodvisen preracun: dva dup pari + stran ==
sken − 6/− 7/− 8/NOVELA formata NOVA TISKANA/NARE 0 ponovitev/PRVO LETO brez
novih hiš/SEGINA VRNITEV h30 + STRAUS×SPUDIČ h16/ŽELJKO signali
16+17/babica 12/12 + Toter 9×/duhovniki Dostál 8× + Stanislav 5× + Rauq 4× +
Kulbinek 0×/kontinuitete 12 pinov/vitals 276); dovoljenja 1902: qa-p85 h30 +
h77, qa-p88 h91, qa-p90 h87, qa-p91 h14, qa-p94 h22 (allow mehanizem);
vitals pini 264 → 276 (11 testov); **POPRAVI ZASTARELIH SKRIPT (regresije po
P96)**: p80 (vitals 276), p85–p92 (filtri vesolja + 1902), p93 (vitals 276 +
kumulativ 282), p94/p95/p96 (filtri izključujejo 1902 — zgodovinske
klasifikacije zamrznjene); vseh **18 skript p80–p97** --check **PASS**
(exit 0). Kartica NI dodana (vzorec P77–P97). tsc 0 / lint 0; **/api/qa dev
98/98** (qa-p97 True); v7 NESPREMENJEN. QA popravki po prvi oceni: qa-p97
babica literal (h87 »Marjeta Tota« → »Marjeta Toter«, h22 »Toter (Marjeta)«
→ »Marjeta Toter«) + Stanislav Dostál 5× (ne 6×) + †-števec na »dojenček«
ključko (matičarske † zapisе vsebujejo tudi †).

**nextSteps**: ① **P98 = leto 1903** (glava »1903.« SREDINA str. 136 = sken
144; 1903 r1 = Griblje 24; skeni 141–152 že prenešeni — stran == sken − 8 do
naslednjega dup para); ② mrliška knjiga 04894 1887–1896: smrti prvih žen +
dojenčki † iz krstnih (r16/r46/r51 1902); ③ poročna 04455: **Straus ×
Spudič** (krstno 5× na treh hišah! — najti poroko: datum + hiši); ④ h51/
h42/h50 (luknja 42/50/51); ⑤ r33 lead: civilni register (zap. št. 4524/1
MMK Novo mesto 1981) razkrije hišo; ⑥ produkcija Vercel: dohiti P97 → QA
98/98.

## §74 · P99 — župnija Podzemelj, krstna knjiga 04105, polno leto 1904 (issue #18; 2026-10-18)

**Okvir (forenzika skenov 152–160, /tmp/p99)**: glava »1904« (podčrtana) POD
r82 na str. 143 (sken 152 — P98 dokazano; 1904 r1 = Krasinec 37 Ana 5./5.
Januar — P98 lead POTRJEN) – row 90 na str. 150 (sken 160; glava »1905«
podčrtana pod r90; 1905 r1 = Gradac 45? Antonija 2./7.? Januar — P100 lead)
== tiskane strani 143–150, **90 vrstic — NAJDALJŠE leto registra doslej**
(prej 1894: 90 tudi? NE — 1894 = 90; izenačeno). **NOVELA P99**: EN podvojen
par skenov (155/156 = str. 146, rows 35–46; s156 jasnejši); **stran == sken
− 9 (152–155) / − 10 (157–160)** — premik offseta za dup par (vzorec P98
− 8/− 9); format = NOVA TISKANA knjiga (kot 1902–1903, predtisk
»Leto 18|04«).

**Vzorec (vsi vpisi z Griblji)**: **20 vpisov / 19 hiš + 1 NEBERLJIVA** (r69
hiša pod modrim pripisom matičarke + poševno prečrtana — brez vitals bloka):
22, 87, 15, 88, 24, 54, 16, 60, 36, 6, 66, 43, 21, 50, 65, 45, 91, 69, 42 —
**NARE 10. leto** (vsaka znana hiša 1×; 1901 edini prelom z h12 ×2).
**3 NOVE HIŠE po dveh letih brez novih**: h6 (nabor PT 1–40 — prvi vpis) +
h42 in h50 (**20. in 21. dokazana številka luknje 41–60 — luknja ostaja SAMO
pri h51!**); h88 = prvi KRSTNI vpis (hiša že v mrliški 04894/1886). Kumulativ
**313 vpisov / 84 hiš čez tri knjige in DEVETNAJST let** (307 vitals). PT
13/6 (42/43/45/50/54/60 v luknji — 42 + 50 NOVI, 43/45/54/60 že dokazani;
luknja zdaj 21 dokazanih).

**Sidra**: r2 h22 3. VPIS (**POŽEK signal** — boter Janez Požek = h30 oče
1902/03; oče Nikolaj Milek = 1902 ISTI); r14 h87 3. VPIS (oče Marko Podrinec
bajtar — KURRENT ISTI oče Pegdirec/Perdinec → Podrinec, NI menjava — P97
lekcija); r15 h15 8. VPIS (**BRINEC signal** — mati Marija Brinec); r16 h88
PRVI KRSTNI VPIS (oče Peter Brinec? + boter Janez Brinec? — 2. in 3. Brinec
oseba); r18 h24 **11. VPIS — ŠE VEDNO najbolj vpisovana gibriljska hiša
registra** + **29. FEBRUAR (prestopno leto 1904 — edini 29.2. vpis do 1904)**
+ pripis razveljavitve zakonske zveze 25.11.1947/29.12.1948 + † 30.1.1983
Zagreb; r31 h16 6. VPIS (Strausova/Spudičeva hiša — poročna 04455 lead); r38
h36 10. VPIS; r46 h6 NOVA (**ŽELJKO signal** — boter Nikol Željko); r65 h50
NOVA (**ŠTRUCELJ signal** — mati Doroteja Štrucelj = h22 rod 1902; boter
Matija Pozdirec); r90 h42 NOVA (**ŠTRAUS signal** — oče Matija Štraus, 2.
Strausova oseba 1904; ZADNJA vrstica leta); r78 h45 4. VPIS (**SPUDIČ
signal** — mati Barbara Spudič; **EMŠO 2610904505164 = 26.10.1904**; †
14.10.2003 Metlika — **98 let, najdaljše življenje letnika 1904**); r80 h91
4. VPIS (**MUC KONTINUITETA potrjena** — oče Janez Muc bajtar; 1895 Muc +
1902 Murov? [~] ISTA žena Kure); r82 h69 8. VPIS (ŽELJKO signal — oče Janez
Željko bajtar). MILEK signali (r2 h22 oče + r73 h65 oče Matija Milek [1901
Mitek? KURRENT] + r57 h21 boter Matija Milek); MIH signal r69 (mati in
babica ISTA — Marija Mih). **EMŠO kampanja 1982–84** (pripisi »Šimonič Miri«
+ datumi 20.12.1982/28.12.1982/30.12.1982/12.6.1984) — sidra celo leto: r8
21.01., r45 28.06., r48 20.07., r77 25.10., r78 26.10., r79 28.10., r89
20.12.1904 (+ r19 EXCLUDED 2007).

**Duhovniki (celo leto)**: Jos. Ravq 38× + Dostál 32× (Stanislav 29× —
januar z naslovom »Kaplan«; Flavi? 3× [~]) + **NOV KAPLAN Hugo Hengsfeld 13×
(od r67; »Kapp.«) — MENJAVA KAPLANOV sredi leta** + neberljivi 5× +
mrtvorojena 2×; Kulbinek 0×. Na Gribljih: Dostál 10 (vsi Stanislav) + Ravq 8
+ Hengsfeld 1 (r80) + neberljiv 1 (r90). **Babica (celo leto) 85 imenovanih /
5 praznih** (r24, r54, r55, r83, r86 »—«) — na Gribljih: **Toter 10×** + Mih
4× + Mavretič 3× + Delak 1× + Aleksič 1× + pod trakom 1× (r16; 20/20
izpolnjeno).

**Anomalije**: r19 (**VSTAVLJEN vpis brez kraja/hiše** — pripis matičarke
Vesne Šimonič 15.05.2007; EMŠO 0303904505822 = 3.3.1904 moški (5) —
NESKLADJE z ženskim imenom Jožefa; **EXCLUDED**); r24 (Mlake »preh. dvor«
Marko — oče PRAZEN, mati »Marija Hudorovič cigarka«, babica »—« — najbolj
obrobni vpis); r25/r26 + r36/r37 (**DVOJČKI** — oba para † dojenčka: r25 4
dni + r26 8 dni; r36+r37 † 9.3.1905 ~9 mes.); r41 + r84 (**MRTVOROJENA
»Z.mrtvorajen«, krsta »—«**; r41 z botri + podpisom Ravq, r84 popolnoma
prazen); r42 (TRETJI otrok Ane Jurajevič v 26 dneh — oče »Jožef
Kržan/Krožan« NESKLADJE z r36/37); r45 (isti Martin Žugelj × DVE ženi < 6
mes. — MERI); r69 (hiša neberljiva — edini 1904 vpis brez hiše); r40 (†
9.11.1918 — **dan pred premirjem**, 14 let). Umrljivost dojenčkov 8 +
mrtvorojena 2 + nezakonski 2.

**Integracija**: dokaz `research/issue17/parish-baptism-1904.json`
(SAMPLE-TRANSCRIPTION-1904; MERI, NE odloča) + verifikator
`scripts/p99_parish_baptism_1904.py` (**I1–I10**, `--check` PASS) +
`parish.ts` HOUSE_VITALS 288 → **307** (19 novih 1904 blokov; vsi z
whatEn + status) + QA 99 → **100/100** (nova qa-p99-parish-baptism-1904:
100. kontrola — okvir + NARE 10. leto + 3 NOVE hiše + PT 13/6 + 15
kontinuitetnih pinov + signali POŽEK 2×/ŽELJKO 2×/BRINEC 2×/ŠTRUCELJ/ŠTRAUS/
SPUDIČ/MUC + babica 19/19 + Toter 10× + duhovniki Dostál 10 (vsi Stanislav)
+ Ravq 7 v blokih + Hengsfeld 1 + Kulbinek 0× + vitals 307) +
**atlas.ts PT_GAP_KNOWN + 42 + 50** (21. dokazani — luknja ostaja samo h51)
+ qa-p88 h91 / qa-p90 h87 / qa-p91 h45 / qa-p92 h43 / qa-p94 h22 dovolijo
1904 bloke (allow mehanizem) + qa-p86–p98 vitals pini 288 → 307 +
**POPRAVI ZASTARELIH SKRIPT (regresije po P98)**: p80 (vitals 307), p85–p98
vitals 307 + kumulativ 313 + hiše vitals 83, p85/p87/p88/p90 izključitvene
terke + 1904 — vseh **21 skript p79–p99** `--check` PASS (exit 0). Kartica
NI dodana (vzorec P77–P99). tsc 0 / lint 0; **/api/qa dev 100/100** (qa-p99
True); v7 NESPREMENJEN.

**nextSteps**: ① **P100 = leto 1905** (glava »1905« pod r90 na str. 150 =
sken 160; 1905 r1 = Gradac 45? Antonija 2./7.? Januar; skeni 160+ prenesti);
② mrliška knjiga 04894 1887–1896: smrti prvih žen + dojenčki † iz krstnih;
③ poročna 04455: **Straus × Spudič** (krstno 5× + 1904 ŠTRAUS r90 + SPUDIČ
r78 — 2. osebi istega leta!); ④ h51 (ZADNJA nedokazana številka luknje
41–60!); ⑤ r19 lead: EMŠO 0303904505822 (moški 1904) + pripis 2007 razkrije
vstavljen vpis; ⑥ produkcija Vercel: dohiti P99 → QA 100/100.


## §75 · P100 — župnija Podzemelj, krstna knjiga 04105, polno leto 1905 (issue #18; 2026-10-18)

**Okvir (forenzika skenov 160–169, /tmp/p100)**: glava »1905« POD r90 na
str. 150 (sken 160 — P99 dokazano; 1905 r1 = Gradac 45 Antonija 2./7.
Januar — P99 lead POTRJEN) – row 87 na str. 157 (sken 169; glava »1906«
na str. 158 = sken 170/171; 1906 r1 = »Gorn?« 34 Jožef 1./1. — P101 lead)
== tiskane strani 150–157, **87 vrstic**. **NOVELA P100**: DVA podvojena
para skenov (164/165 = str. 154, rows 40–51 + 168/169 = str. 157, rows
76–87) + dup par 170/171 (str. 158) = ŽE leto 1906; **stran == sken
− 10 (160–164) / − 11 (165–168) / − 12 (169–170) / − 13 (171+)** — premik
offseta za vsak dup par (vzorec P97 −6/−7/−8, P98 −8/−9, P99 −9/−10).
Format = **spread** (levo data, desno Roditelja/Botra/Babica; naslov
razporejen čez obe strani).

**Vzorec (vsi vpisi z Griblji)**: **16 vpisov / 15 hiš**: 1, 5, 6, 7, 11,
12×2, 22, 23, 25, 34, 39, 42, 48, 58, 66 — **NARE PRELOM** (h12 ×2: r4
Neža + r15 Ana — 2. intra-letna ponovitev po 1901; več-družinska hiša).
**0 NOVIH hiš** (vse 15 že dokumentirane; drugo leto zapored brez novih).
h42 (NOVA 1904) ponovitev že 1905 — **MENJAVA DRUŽINE** (Štraus →
Perdinec/Pezdirec). **LETO VELIKIH VRZELI**: h39 **18 let** (1886→1905 —
NAJDALJŠA v vzorcu!), h11 15 let (1890→1905), h1 4 leta (1900→1905), h66
17 let (1887→1904). Kumulativ **329 vpisov / 84 hiš čez tri knjige in
DVAJSET let** (323 vitals). PT **12/3** (42/48/58 v luknji — vsi
ponovitve; luknja 41–60 ostaja SAMO pri h51).

**Sidra**: r4 h12 9. VPIS + **RAZVELJAVITEV ZAKONA** (sodišče Novo mesto
23.5.1949 — 1. gribeljska razveljavitev v krstni knjigi!) + EMŠO
1201905505202; r49 h6 **2. VPIS ZAPORED** (ISTA botra Nikolaj Željko +
Marija Klepec kot 1904! + vijolični pripis »Po odloči Okrajnega sodišča v
Črnomelju« + **EMŠO NESKLADJE SPOLA** — 0607905500076 ženski znak, ime
Janez moški); r69 h58 **8. VPIS** (ISTI PAR Janez Požek × Katarina Kambič —
P98 rešitev 3. POTRDITEV; † 26.2.1906 dojenček); r66 h25 5. VPIS (Brinec ×
Šegina — 3. dokumentacija); r62 h22 4. VPIS (Nikolaj Milek 1904 oče + botra
Ana Požek — POŽEK signal); r82 h66 3. VPIS (Hrižan signal; † 1944 — 2.
svetovna vojna); r50 h7 3. VPIS (Jakob Toter × Katarina Jakobšič — 1901
par); r14 h5 3. VPIS (Matija Štrucelj = 1903 oče); r19 h34 4. VPIS (SEGINA
signal — boter Nikolaj Šegina); r28/r29/r31/r42/r57/r65 (vrzeli in
kontinuitete).

**Duhovniki (celo leto 87)**: **Hengsfeld 54× DOMINANT** + Ravq 26 +
Dostál 1 [~] + neberljivo 5 (odrezani) — na Gribljih Hengsfeld 8 + Ravq 7
+ odrezan 1 (r15). **Babica (celo leto)**: 78 imenovanih / 5 praznih / 3
neberljive — na Gribljih **16/16: Toter 12× + Mih 3× (r19 = varianta
»Mih [~ Muh] Marija«) + Kambič [~] 1×**. **EMŠO kampanja 1982–84**: 17
sidr celo knjigo; 4 na Gribljih (r4/r14/r19/r49; r49 neskladje spola).

**Anomalije**: r8 Gradac 55 **VSTAVLJEN vpis 03.09.2007** (2. primer po
P99 r19; non-Griblje); r49 vijolični sodni pripis + neskladje spola;
r71/r72 Boršt 19 **dvojčka** (ditto vrstica); r85 Gradac **žandar
Wachtmeister** (2. po 1903 Morvet); r76/r79/r84 **»Hudorovac samska
ciganka«** nezakonski + legitimizacija 1915; r73 razveza Zagreb; †
dojenčka r66 + r69. EXCLUDED: 4 (r2 pripis pokrije kraj/hišo, r3 + r27
odrezani v skenih, r40 bela nalepka).

**Integracija**: parish.ts + 16 blokov HOUSE_VITALS 1905 (307 → 323; vsi
status DOCUMENTED, spread pageOfScan novela) + qa-p100-parish-baptism-1905
(**101. kontrola** — okvir + NARE PRELOM + 0 novih hiš + VRZELI 18/15 let +
RAZVELJAVITEV ZAKONA + h6 2. ZAPORED + h58 Požek×Kambič + h25 Brinec×Šegina
+ 15 kontinuitetnih pinov + babica 16/16 (Toter 12 + Mih 3 vklj. varianta
»Mih [~ Muh] Marija« + Kambič [~]) + duhovniki Ravq 7/Hengsfeld 8/Kulbinek
0× + EMŠO 4 sidra) + qa-p85 h7 / qa-p87 h12 / qa-p88 h23 / qa-p93 h48 /
qa-p94 h22 dovolijo 1905 bloke (allow mehanizem) + qa-p86–p99 vitals pini
307 → 323 + **POPRAVI ZASTARELIH SKRIPT (regresije po P99)**: p80 (vitals
323), p85–p99 vitals 323 + kumulativ 329 + hiše vitals 83, p85/p87/p88/
p91/p92/p94/p95 horizon filtri + 1905 (+ 1903/1904 kjer manjkalo), p96
inline terka + 1905, p93/p97/p98/p99 NOVI vesoljni filtri (vitals_pre99/
pre1903/pre1904/pre1905), p95/p96/p97/p98 I6 PT_GAP_KNOWN asercije 42/50
`not in` → `in` (zastarele od P99 — skrite za I10 FAIL-i) — vseh **22
skript p79–p100** `--check` PASS (exit 0). Kartica NI dodana (vzorec
P77–P100). tsc 0 / lint 0; **/api/qa dev 101/101** (qa-p100 True); v7
NESPREMENJEN.

**nextSteps**: ① **P101 = leto 1906** (glava »1906« na str. 158 = sken
170/171; 1906 r1 = »Gorn?« 34 Jožef 1./1.; skeni 170+ prenesti); ② mrliška
knjiga 04894 1887–1896: smrti prvih žen + dojenčki † iz krstnih (r69 h58
† 26.2.1906 lead!); ③ poročna 04455: **Straus × Spudič** (krstno 5×; 1904
ŠTRAUS r90 + SPUDIČ r78 — 2. osebi istega leta); ④ h51 (ZADNJA nedokazana
številka luknje 41–60!); ⑤ produkcija Vercel: dohiti P100 → QA 101/101;
⑥ EMŠO neskladje r49 (0607905500076) — obravnava kot P99 r19.
