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
TRAVNIK; razcep K1/K2 (§21) + semantika 7 par referenc; potrditev vseh strojnih
branj. Vsi statusi REVIEW.
