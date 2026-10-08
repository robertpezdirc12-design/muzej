# P3 — Paleografska preverba PT (2. krog) + PUA nadaljevanje (2026-10-08)

Nadaljevanje po issue #17 (priporočila 17-z), izvedeno brez novega issueja po naročilu uporabnika (»odlicno nadaljuj«).

## Kaj je narejeno
1. **PT paleografija 2. krog** — 9 VLM klicev, črka-za-črko, sveži izrezi → `paleografija-pt.json` + `src/data/atlas/research.ts` (PT_PALEOGRAPHY_P3). Popravki APLICIRANI v register (2-krožna konvergenca): renumeracija str. 4 (36–41→35–40; hiša 41 ne obstaja), 15 lastniških popravkov (Veith, Lebing, Bödig, Brinig, Strauß, Ihmeyer, Zollamt, K-priimek), 4 dodane vrstice (7, 71½, 76½, 99).
2. **PUA stran 11** (črka H) — 4 vnosi → `pua-stran-11.json` + PUA_CONTINUATION (22 vrstic, 9 strani).
3. **PDF-i vseh 7 serij ponovno preneseni** iz VAČ (po resetu peskovnika): `download/atlas-1825/n83/` (gitignore — glej VAČ metodo spodaj).

## Kaj je blokirano (pošteno)
- **PUA str. 12–20**: branje se je začelo, a je bil VLM dostop prekinjen (gateway 401 X-Token po resetu peskovnika). Slike strani 11–20 so bile pretvorjene; surovi izpisi 12–14 so bili izgubljeni z /tmp. Nadaljevanje: glej metodo.
- **Hiša 90**: tri medsebojno izključujoča branja (Kavalar/Bumiller/Ihmeyer) — ostaja ILLEGIBLE.

## VAČ metoda (ponovljiva)
1. Stran podrobnosti: `https://vac.sjas.gov.si/vac/search/details?id={vacId}` (curl -sk — VAČ ima nepopolno TLS verigo)
2. IIIF manifest: `https://vac.sjas.gov.si/vac/iiif/pdf-manifest?uodid={vacId}&docid={docId}`
3. PDF: `https://vac.sjas.gov.si/vac/util/tifyPdfDownload?uodid={vacId}&docid={docId}`
   - vacId: PUA 373417, PT 373416, PS 373415, PZ 373419, PV 373418, PR 373414, PG 373413
   - docId: 41782 (PUA), 41781 (PT), 41780 (PS), 41784 (PZ), 41783 (PV), 41779 (PR), 41778 (PG)

## Poštenost
- Surovi izpisi VLM 2. kroga izgubljeni (reset /tmp); strukturirani zapisi so v JSON-ih tu in v research.ts.
- Vsi statusi ostajajo REVIEW — strojno branje (tudi 2. krog) ni dokazni vir; dokončna potrditev je človeška paleografija.
- Register: 101 → 105 vrstic (nič-zguba: prečrtana dvojnica 34 ostaja kot dokumentirana vrstica).
