# Muzej vasi Griblje — digitalni muzej vasi ob Kolpi

Večjezični digitalni muzej resnične vasi v Beli krajini (občina Črnomelj, Slovenija).
Zbirka: **113 zapisov** s trajnimi muzejskimi številkami (MVG-001 → MVG-114), **589 dokazljivih virov**,
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
| `src/data/museum/exhibits.json` | 113 zapisov (naslovi, povzetki, zgodbe, viri, koordinate) |
| `src/data/museum/events.json` | 9 dogodkov |
| `src/data/museum/meta.json` | metapodatki muzeja, lestvica zanesljivosti, 6 zgodb |
| `src/data/museum/extra.json` | postaje življenja, trditve, sorodni zapisi, postaje sprehoda |
| `public/images/authentic/` | 101 fotografija z navedbami avtorjev |

## Licenca

- Vsebina zbirke: **CC BY-SA 4.0**
- Zemljevidski podatki: © OpenStreetMap prispevali
- Slike: licenca posamezne slike je navedena v zapisu (Wikimedia Commons in javni viri)

## Provenanca

Spletišje je bilo obnovljeno iz zadnjega delujočega produkcjskega deploymenta
(2026-10-06 11:32 UTC) po incidentu z neavtoriziranim dostopom do GitHub računa.
Vsa vsebina, besedila, viri in slike izhajajo iz izvirne zbirke.

## Povezava GitLab ↔ Vercel

Produkcija teče na Vercelu: **https://griblje-museum.vercel.app**

| Plast | Stanje |
|---|---|
| Kanonični repozitorij | `markec-group/muzej` (veja `main`) — vsebina identična produkciji |
| Deploy sprožilec | `robert.pezdirc12/muzej` (osebni, zasebni) — nanj je povezan Vercel |
| Samodejni deploy | ✅ AKTIVEN — vsak push na `main` deploy repozitorija zgradi in objavi Vercel |
| Skrivnost | `VERCEL_TOKEN` shranjen kot maskirana CI/CD spremenljivka projekta |

### Zakaj dva repozitorija?

Brezplačni (Hobby) Vercel načrt ne povezuje **zasebnih repozitorijev v lasti skupin**
(zahteva Pro) — zato je Vercel povezan na zasebni osebni repozitorij
`robert.pezdirc12/muzej`, ki služi kot *deploy sprožilec*. Skupinski repozitorij
`markec-group/muzej` ostaja kanonična kopija z enako vsebino in zgodovino.

**Pri vsaki spremembi potisni na OBE repozitorija:**

```bash
git push gitlab main   # kanonična kopija (markec-group/muzej)
git push deploy main   # sprožilec samodejnega deploya (robert.pezdirc12/muzej)
```

### Ročni deployment (iz klona repozitorija)

```bash
git clone https://gitlab.com/markec-group/muzej.git
cd muzej
npx --yes vercel@latest deploy --prod --yes \
  --token="$VERCEL_TOKEN" \
  --project=griblje-museum \
  --scope=robertpezdirc12-designs-projects
```

#
## ATLAS 1825 (GitLab issue #2)

Zgodovinska katastrska slika vasi (franciscejski kataster, k.o. Griblje št. 83 / Grüble):

- **arhivski viri** — Arhiv RS, fond SI AS 176/N/N83, 9 enot javno dostopnih prek
  [VAČ](https://vac.sjas.gov.si) (listi A01/A02, skica, opis meje, seznami parcel,
  stavbni protokol 1825, abecedni lastniki, raba, cenilni elaborat);
- **georeferencirana lista** A01 in A02 kot slikovni prekrivki nad OSM (Leaflet),
  prosojnost 0–100 %, cerkev sv. Vida kot kontrolna točka (VERIFIED);
- **register hiš 1–98** (80 prebranih zapisov, status REVIEW — Kurrent rokopis),
  lastniki (navzkrižno PT × PUA), parcelni sklici;
- **vektorizacija** 156 objektov ~1825 iz lista A02 (RECONSTRUCTED);
- **dokazni vmesnik**: vir → trditev → dokaz → povezave (N083PT str. + VAČ povezave);
- **pokritost + negativni rezultati** — raziskovalna provenienca vključno s statusi
  VERIFIED/DOCUMENTED/REVIEW/RECONSTRUCTED/APPROXIMATE/TO_COLLECT/NOT_FOUND;
- **globa povezava** `?atlas=hiša-75` (hiša št. 73 — demonstracijska veriga do MVG-010).

API (statični, brez runtime AI):

- `GET /api/atlas` — celoten podatkovni model (JSON, provenienca vključena);
- `GET /api/atlas/geojson` — prostorski sloji (GeoJSON, CRS84);
- `GET /api/atlas/integrity` — test povezav hiša ↔ parcela ↔ lastnik ↔ vir (9 preverjanj).

## Varnost

Žeton `VERCEL_TOKEN` je v GitLabu shranjen izključno kot **maskirana CI/CD
spremenljivka** in ni v repozitoriju. Datoteki `.gitignore` in `.vercelignore`
preprečujeta prenos `.env*` in lokalnih datotek pri deployu.
