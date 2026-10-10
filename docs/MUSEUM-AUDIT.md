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
| Produkcija | `griblje-museum.vercel.app` (Vercel; sinhroniziran z repozitorijem — GitHub Actions deploy, žeton do 14. 10. 2026) |
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
| Koordinate | 94/114 s GPS znotraj Bele krajine (45,30–45,90 N, 14,60–15,80 E); zastavica `coordsApprox` pri vseh razen natančne točke ZooKeys (MVG-103) | ⚠️ 20 zapisov brez GPS — zavestne odločitve, ne vrzel (pesem/šega brez fiksne točke, regionalni zapisi, tradicija z odprtim iskanjem, najdišči brez javnih koordinat — utemeljitve v §14), glej §9 |
| Datumi | 101 zapisov z `yearFrom`; 13 z `null` (tematski zapisi z besedilnim `periodSi`, npr. »verska dediščina«) | ⚠️ 4 prazgodovinski zapisi so bili nevidni na časovnici — **popravljeno** (glej §8) |
| Negativna leta | 4 zapisi (MVG-060 −800, MVG-083 −4500…200, MVG-095 −1000…−700, MVG-113 −1200…−800) — prazgodovinska najdišča, `periodSi` jih pravilno poimenuje (»pribl. 4500 pr. n. št.«) | ⚠️ prikaz »−4500« namesto »4500 pr. n. št.« — **popravljeno** (glej §8) |
| Kategorije | 6 veljavnih: kraj 50, sege 21, gospodarstvo 13, vojna 13, narava 12, kolpa 5 | ✓ |
| Podvojitve naslovov | 0 | ✓ |
| Dogodki | 11; naslovi SL/EN, datumi, zunanje povezave vse veljavne | ✓ |
| Extra (galerije, citati, sorodni) | 114 vnosov po slugu | ✓ (zgodovina: 2 obešeni povezavi na MVG-114 sta bili P19 odstranjeni; P24 ju je povrnil, ker zapis zdaj obstaja) |

### 2.2 Viri in dokazljivost (točka 3)

| Predmet | Rezultat |
|---|---|
| Skupno navedb virov | **594** (473 unikatnih `sourceKey`; povprečno 5,2 na zapis; min 1, max 26; P24: +4 za MVG-114) |
| ⚠️ Razlika s README/meta | README in meta.json sta trdila 589 — **popravljeno na 590** (glej §8) |
| Zapisi brez vsaj enega vira | 0/114 |
| Viri brez podatka o licenci | 0/594 |
| Vrste virov | objava 263, spletni-vir 202, fotografija 106, arhiv 16, zemljevid 5, pričevanje 2 |
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
| Posamezni viri | 594/594 z licenco v `sources[].license` (razporeditev po 127 vrstah licenc v `/api/provenance`) |
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
| `/api/provenance` | 594 navedb; 114/114 z virom; 0 brez licence |
| `/api/opendata` | števci 114/594/11/6; licenca CC BY-SA 4.0 |
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
  česa NE (PS 135 strani in PZ 59 strani izrecno odprtih; vsa strojna
  branja REVIEW; 156 geometrij brez dokazanih hišnih št.).
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
4. **Kaj je odprto in kateri dokaz manjka?** (a) PS: poln prepis 135 strani —
   dokaz = vrstice registra (kontrolna vsota 2607); (b) PZ: 59 strani tabel
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

### Zavestne izločitve (20 zapisov brez GPS — utemeljitve)

1. **Pesem/šega brez fiksne točke (precedens P24):** MVG-065 kresovanje
   (kresi na gričih pozemeljske fare — ni ene točke; P24 ga je navedel kot
   vzor za MVG-114), MVG-114 kresna pesem (1895; pesem ni točka na karti).
2. **Najdišči brez javnih koordinat:** MVG-113 Srednje njive (Arheološki
   vestnik 71.14, celoten PDF prebran — 1 omemba, 0 koordinat; Mason 2001
   ostaja TO_COLLECT), MVG-083 arheološko najdišče ob Kolpi (EŠD 10094 —
   register namerno ne objavlja koordinat najdišč; njive Kohane, Požekov vrt
   in Krasinec–Vrh so mikrotoponimi brez javnih koordinat).
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
