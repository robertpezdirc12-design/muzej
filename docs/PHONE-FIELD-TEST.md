# Terenski preizkus na telefonu — protokol (P38, izhaja iz MUSEUM-AUDIT §9 točka 2)

> Stanje po reviziji: obiskovalni tok (QR, GPS, AR, offline) je **preverjen v kodi
> in na produkciji, NEPREVERJEN na fizični napravi**. Ta protokol je kontrolni
> list za preizkus na kraju samem; vsak korak ima pričakovani izid in mesto za
> zapis. Izpolnjen list se prilepi v komentar GitHub issue-ja (ali odpre nov
> issue); popravki se razporedijo v faze (P3x) po običajnem pravilu
> dokaz → popravek → QA test.

## 0. Pogoji (pred odhodom)

| # | Postavka | Pričakovano | Zapis |
|---|---|---|---|
| 0.1 | Naprava: Android ≥ 10 ali iOS ≥ 15, GPS + zadnja kamera | — | ______ |
| 0.2 | Brskalnik: Chrome (Android) / Safari (iOS) | — | ______ |
| 0.3 | URL produkcije: `https://griblje-museum.vercel.app` | naslovnica se naloži | ______ |
| 0.4 | Preveri `GET /api/qa` (naprej ali na mestu; HTTP 200) | `ok: true`, vseh 39 testov | ______ |
| 0.5 | Omrežje na mestu (Griblje): signal / dobra 4G? | zapiši operaterja | ______ |

## 1. Vhod prek QR kode

| # | Korak | Pričakovano | Zapis |
|---|---|---|---|
| 1.1 | Natisni `public/qr/vstop.png` (ali uporabi na zaslonu druge naprave) in skeniraj | odpre se domača stran v brskalniku | ______ |
| 1.2 | Skeniraj `public/qr/spot-cerkev.png` | odpre se viza postaje *Cerkev sv. Vida* z globoko povezavo `?casovni=…&spot=cerkev` | ______ |
| 1.3 | Ponovi za 2 poljubni postaji (od 9: cerkev, jedro, kolpa, ribnik, gornje, meja, mlini, otok, cerkvisce) | pravilna postaja, pravilna letnica | ______ |
| 1.4 | Globoka povezava `?exponat=<slug>` (npr. `?exponat=griblje-vas`) | zapis MVG se odpre neposredno | ______ |
| 1.5 | Globoka povezava `?atlas=hiša-73` | atlas odpre hišo 73 (veriga do MVG-010) | ______ |

## 2. GPS in lokacijske postaje

| # | Korak | Pričakovano | Zapis |
|---|---|---|---|
| 2.1 | Odpostavi dovoljenje za lokacijo ob prvem pozivu | poziv pride, po soglasju brez napake | ______ |
| 2.2 | Na postaji *Cerkev sv. Vida* (EŠD 2122) odpremo zemljevid | lastna lega + postaja na karti; razdalja realistična (±50 m na prostem) | ______ |
| 2.3 | Zapri/hodi: logika blizu/daleč (ar-camera) | kazalec stanja se posodablja brez zamrzovanja | ______ |
| 2.4 | V stavbi / brez signala | pošten predogled, ne zablokirana stran | ______ |

## 3. AR kamera (brez očal)

| # | Korak | Pričakovano | Zapis |
|---|---|---|---|
| 3.1 | Dovoli kamer ob vstopu v AR način | živ video zadnje kamere | ______ |
| 3.2 | Model cerkve (GLB) lebdi nad sliko kamere | model viden, zasidran v smeri objekta (kompas + GPS azimut) | ______ |
| 3.3 | Zavrti se za ~90° | model uide iz sredine; azimut se posodobi | ______ |
| 3.4 | Android: *Scene Viewer* / iOS: *Quick Look* iz `model-viewer` (`ar-modes="webxr scene-viewer quick-look"`, USDZ obstaja) | model v prostoru (floor placement) | ______ |
| 3.5 | Brez kompasa (brskalnik brez dovoljenja) | fiksni model, brez zrušitve | ______ |
| 3.6 | Brez kamere (zavrnjeno dovoljenje) | arhivsko ozadje, brez zrušitve | ______ |

## 4. Avdio vodnik (govorne skripte)

| # | Korak | Pričakovano | Zapis |
|---|---|---|---|
| 4.1 | Na postaji predvajaj »glas muzeja« | predvaja brskalniški `speechSynthesis`; transkript viden na kartici | ______ |
| 4.2 | Preklopi jezik SL→EN med predvajanjem | govor se ustavi/preklopi na EN skripto | ______ |
| 4.3 | Tikaj se gor (izklop zaslona, druga aplikacija) | predvajanje ne zasede zvoka, ob vrnitvi stanje pošteno | ______ |

## 5. Offline (PWA, service worker v19)

| # | Korak | Pričakovano | Zapis |
|---|---|---|---|
| 5.1 | Obišči naslovnico + 2 zapisa z omrežjem; nato vklopi letalski način | ponovni odprtje naslovnice iz predpomnilnika (precache `/`) | ______ |
| 5.2 | Letalski način: odpri že shranjen zapis | vsebina iz SWR predpomnilnika; brez belega zaslona | ______ |
| 5.3 | Letalski način: zemljevid | ploščice OSM niso offline — pričakovano označen propad, ne zrušitev | ______ |
| 5.4 | Izklopi letalski način | sinhronizacija poteka brez posega | ______ |

## 6. Jeziki, temni način, dostopnost na terenu

| # | Korak | Pričakovano | Zapis |
|---|---|---|---|
| 6.1 | SL/EN preklopnik na 3 različnih zaslonih | vsi vidni nizi preklopijo | ______ |
| 6.2 | Sistemski temni način | muzej sledi nastavitvi | ______ |
| 6.3 | Sonce + maksimalna svetlost: berljivost ključnih zaslonov | subjektivna ocena 1–5 | ______ |
| 6.4 | Členi zanje na dotik (QR kartice, gumbi postaj) | dovolj veliki cilji (≥ 44 px), brez prekrivanj | ______ |

## 7. Povzetek terenskega preizkusa

- Datum/ura: ______ · Vreme: ______ · Naprava: ______
- Uspešni koraki: ______/26
- Neuspešni koraki (št. + kratek opis): ______
- Svetlobni / senzorski posebni pogoji (kompas kalibracija, IP67 dež …): ______

**Pravilo po preizkusu:** vsak neuspešen korak dobi issue z vsebino tega zapisa
(korak, pričakovano, dejansko, naprava, različica brskalnika, zaslonska slika
če je mogoče). Popravki ne spreminjajo dokazov, dokler niso preverjeni —
isti standard kot v MUSEUM-AUDIT §9.
