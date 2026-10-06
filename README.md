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
| Vsebina | repozitorij `markec-group/muzej` (veja `main`) — identična produkciji |
| Produkcija | uspešno nameščena iz tega repozitorija (Vercel, okolje `production`) |
| CI/CD | `.gitlab-ci.yml` pripravljen; zaživi, ko GitLab račun lahko poganja jobe (glej spodaj) |
| Skrivnost | `VERCEL_TOKEN` shranjen kot maskirana CI/CD spremenljivka projekta |

### Kako omogočiti samodejni deployment ob vsakem pushu na `main`

1. **Priporočena pot — Vercelova GitLab integracija (brez GitLab CI):**
   - Vercel → Account Settings → Login Methods & Connections → poveži **GitLab** (OAuth);
   - nato Projekt `griblje-museum` → Settings → Git → poveži repozitorij `markec-group/muzej`
     (production branch: `main`).
   - Odslej vsak push na `main` zgradi in objavi Vercel sam.
2. **Alternativna pot — GitLab CI pipeline:**
   - GitLab → User Settings → Billing → potrdi plačilno kartico (na brezplačnem načrtu
     je to pogoj za razpoložljivost compute minut);
   - obstoječa `.gitlab-ci.yml` pipeline bo nato samodejno delovala pri vsakem pushu.

### Ročni deployment (iz klona repozitorija)

```bash
git clone https://gitlab.com/markec-group/muzej.git
cd muzej
npx --yes vercel@latest deploy --prod --yes \
  --token="$VERCEL_TOKEN" \
  --project=griblje-museum \
  --scope=robertpezdirc12-designs-projects
```

### Varnost

Žeton `VERCEL_TOKEN` je v GitLabu shranjen izključno kot **maskirana CI/CD
spremenljivka** in ni v repozitoriju. Datoteki `.gitignore` in `.vercelignore`
preprečujeta prenos `.env*` in lokalnih datotek pri deployu.
