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
| Produkcija | `griblje-museum.vercel.app` (Vercel, povezan z GitLabom; sinhroniziran z repozitorijem 9. 10. 2026 prek CLI deploya) |
| Obstoječi testi | lastna QA zbirka (`src/lib/qa.ts`, 23 testov), atlas integrity (11 preverb), ESLint, tsc |
| Odprti issueji | #1 (ta revizija) — edini |

## 2. Inventar podatkov (točka 2)

Viri: `src/data/museum/exhibits.json`, `events.json`, `extra.json`, `meta.json`;
`src/data/atlas/*` (13 datotek). Preverjeno z determinističnim skriptom
(`audit_issue1.py` v peskovniku revizorja, rezultati spodaj).

### 2.1 Zbirka eksponatov

| Predmet | Rezultat | Ocena |
|---|---|---|
| Število zapisov | 113 | ✓ ujema se z README in meta.json |
| Muzejske številke | MVG-001 → MVG-113, vse unikatne, oblika `MVG-\d{3}` | ⚠️ README je trdil »MVG-001 → MVG-114« — **popravljeno** (glej §8) |
| ID-ji in slugi | 113 unikatnih ID-jev, 113 unikatnih slugov, oblika veljavna | ✓ |
| Naslovi SL/EN | 113/113 obojezično | ✓ |
| Povzetki in zgodbe | 113/113 s povzetki, 113/113 s poljema `storySi`/`storyEn` | ✓ |
| Slike | 106/113 s sliko; vseh 106 datotek obstaja v `public/`; 106/106 z `imageCredit` | ✓ 7 zapisov brez slike (namerno: npr. dogodki, izseljenstvo) |
| 3D model | 1 (cerkev sv. Vida, GLB + USDZ, obe datoteki obstajata, kredit navdan) | ✓ |
| Koordinate | 36/113 s GPS znotraj Bele krajine (45,30–45,90 N, 14,60–15,80 E); vse z zastavico `coordsApprox`, kjer je približek | ⚠️ 77 zapisov brez GPS — znana vrzel, glej §9 |
| Datumi | 100 zapisov z `yearFrom`; 13 z `null` (tematski zapisi z besedilnim `periodSi`, npr. »verska dediščina«) | ⚠️ 4 prazgodovinski zapisi so bili nevidni na časovnici — **popravljeno** (glej §8) |
| Negativna leta | 4 zapisi (MVG-060 −800, MVG-083 −4500…200, MVG-095 −1000…−700, MVG-113 −1200…−800) — prazgodovinska najdišča, `periodSi` jih pravilno poimenuje (»pribl. 4500 pr. n. št.«) | ⚠️ prikaz »−4500« namesto »4500 pr. n. št.« — **popravljeno** (glej §8) |
| Kategorije | 6 veljavnih: kraj 50, sege 20, gospodarstvo 13, vojna 13, narava 12, kolpa 5 | ✓ |
| Podvojitve naslovov | 0 | ✓ |
| Dogodki | 11; naslovi SL/EN, datumi, zunanje povezave vse veljavne | ✓ |
| Extra (galerije, citati, sorodni) | 113 vnosov po slugu | ⚠️ 2 obešeni povezavi »sorodni« na neobstoječi MVG-114 — **popravljeno** (glej §8) |

### 2.2 Viri in dokazljivost (točka 3)

| Predmet | Rezultat |
|---|---|
| Skupno navedb virov | **590** (470 unikatnih `sourceKey`; povprečno 5,2 na zapis; min 1, max 26) |
| ⚠️ Razlika s README/meta | README in meta.json sta trdila 589 — **popravljeno na 590** (glej §8) |
| Zapisi brez vsaj enega vira | 0/113 |
| Viri brez podatka o licenci | 0/590 |
| Vrste virov | objava 259, spletni-vir 202, fotografija 106, arhiv 16, zemljevid 5, pričevanje 2 |
| Lestvica zanesljivosti | 4-stopenska, vsak zapis ima veljaven `evidenceStatus`: DOCUMENTED 88, CORROBORATED 15, TRADITION 8, TESTIMONY 2 |
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
| Posamezni viri | 590/590 z licenco v `sources[].license` (razporeditev po 125 vrstah licenc v `/api/provenance`) |
| Slike | 106/106 z `imageCredit` |
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
| `/api/qa` (lokalno, produkcijska zgradba) | **ok: true, 23/23 PASS** (vključno `qa-p12-village-life`) |
| `/api/atlas/integrity` | **11/11 PASS** (hiše, viri, E2E veriga hiša 73→MVG-010, georeferenca, EŠD 2122, vektorizacija, matrike …) |
| `/api/provenance` | 590 navedb; 113/113 z virom; 0 brez licence |
| `/api/opendata` | števci 113/590/11/6; licenca CC BY-SA 4.0 |
| Produkcija (`griblje-museum.vercel.app`) | 200; QA 23/23 po deployu te revizije (glej §10) |

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
| 1 | Integriteta 113 zapisov (ID, naslovi, jeziki, slike, kategorije) | **DONE** |
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
| 12 | Licence (CC BY-SA 4.0 plastovito, OSM, 106/106 kreditov) | **DONE** |
| 13 | API-ji statični, brez vnosa, escaping | **DONE** |
| 14 | Testni nabor (lint/build/QA/integrity) | **DONE** (rezultati v §7.2) |
| 15 | GPS koordinate 77/113 zapisov | **MISSING** (znana vrzel; ne izmišljujemo — zbirajo se iz virov) |
| 16 | Zapis MVG-114 »Kresna pesem (1888)« | **NAČRTOVANO** (rezerviran v `extra.json` related; ni v zbirki) |
| 17 | Popravljanje 34 prikritih TS napak (`ignoreBuildErrors`) | **DONE (P17)** — 0 napak, zastavica odstranjena |
| 18 | Surove kode vrst virov vidne obiskovalcu (npr. »objava«) | **PARTIAL** — kozmetika; predlog: slovar oznak SL/EN |
| 19 | Neuporabljene env spremenljivke na Vercelu + Prisma ostanki | **DONE (P15+P17)** — AI ključa (OPENROUTER, ELEVENLABS) odstranjena s Vercela in `z-ai-web-dev-sdk` iz package.json (P15); Prisma odstranjen v celoti (P17: `prisma/`, `src/lib/db.ts`, obe odvisnosti, db:* skripti, 17 neuporabljenih paketov). `DATABASE_URL`/`DIRECT_URL` sta ostali na Vercelu (neškodljivi, neuporabljeni — potencialno edini zapis povezave do zbirke, zato ju ne brišemo brez lastnika) |
| 20 | Pin MVG-095 v načinu časovnega potovanja na karti | **PARTIAL** — obdobje (−1000…−700) je pred najmanjšim letom drsnika (1468); privzeti pogled piko prikaže, časovno potovanje jo skrije (semantična odločitev, dokumentirano) |

### Naslednji konkretni koraki (po prednostni)

1. **Posneti človeški glas** (domačin) po obstoječih skriptah iz
   `src/data/atlas/narrations.ts` (neobvezno izboljšanje; postopek v
   `public/audio/timespots/README.md`) — človeški posnetek ni AI model.
2. **Preizkus obiskovalnega toka na telefonu** (QR vhod, GPS, AR kamera, offline) — lastnik z
   napravo; po potrebi popravki.
3. **Dopolnjevanje GPS koordinat** iz verodostojnih virov (77 zapisov) — postopoma, z viri.
4. **Odstraniti `ignoreBuildErrors`** in odpraviti 30 TS napak po sklopih (začetek:
   `museum-research.tsx` integrityEn → integritySi, `exhibit-detail.tsx` Sheet props).
5. **Dodati MVG-114** (Kresna pesem 1888), ko so viri zbrani — povezavi se samodejno prikažeta.
6. **Počistiti neuporabljene env spremenljivke in Prismo** (manjša površina, hitrejši build).

## 10. Definition of Done — stanje

- [x] Podatkovni inventar in napake so dokumentirani (§2, §7, skript `audit_issue1.py`)
- [x] Pot obiskovalca je preverjena v kodi/produkciji in **izrecno označena kot nepreverjena na telefonu** (§4)
- [x] Zemljevidi 1812 in AR/GPS so označeni po dejanskem stanju (§3, §5, matrika §9)
- [x] Kritične napake so popravljene brez izgube vsebine (§8: nevidni prazgodovinski zapisi, mrtvi gumbi MVG-114, napačno štetje)
- [x] Poročilo vsebuje teste, vire in naslednje konkretne korake (§7.2, §2–§6, §9)
