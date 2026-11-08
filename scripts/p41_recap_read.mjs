// P41 — paleografija str. 140–143 (rekapitulacija + Abschluß der Gemeinde)
// 3 neodvisna VLM prehoda na stran, [~] negotovo / [?] neberljivo (metoda P36/PUA).
// Vhod: /tmp/ps140/send-<page>.jpg (VAČ pdfPageImage, 2× Lanczos upscale, JPEG q92)
// Izhod: research/issue17/ps-recap-paleo-raw/pass<n>-page<p>.json
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const OUT_DIR = 'research/issue17/ps-recap-paleo-raw';
const IMG_DIR = '/tmp/ps140';

const HEADERS = `Glava tabele (obojestranska registrska oblika): LEVI del: "N:o des Blattes | Bezeichnung der Classen | N:o der Parzelle | Dominical | Rustical | (podpisni stolpci) | Haus N:o | Vor- und Zuname | Stand. | Wohnort." DESNI del: "Des Grundstücks: Kulturs Gattung | Flächen Inhalt: N:o, Quadrat.-Joch., Klafter | Classe | Reinertrag in Metall Münze: fl., kr. | CapitalWert pr. Ct.: fl., kr. | Anmerkung".`;

function promptFor(page) {
  if (page === 140) {
    return `To je stran 140 katastrskega registra lastnikov ("Seznam zemljiških parcel") za k.o. Griblje, franciscejski kataster 1825, napisana v nemški Kurrent pisavi, deloma s RDEČIM tušem. ${HEADERS}

Na LEVI strani je napisan naslov "Recapitulation" in VRSTICE PO HIŠAH (okvirno hišne št. 121½, 122, 123, ..., 135) z Joch/Klafter površinami in nekaj rdečimi vsotnimi vrsticami ("Summa ...").
Na DESNI strani je v rdečem tušu napisan sklop "Abschluß der Gemeinde": več vrstic z oznako (Summa der Bauplätze / Zinsb. Bauplätze / Summe der Bauplätze / Area der Gemeinde) in paroma dve številki (stolpca Joch | Klafter), ter na dnu datum/podpis.

PRAVILA:
- Prepiši VSAKO vrstico obeh strani, črka-za-črko, številke TOČNO kot so napisane (ne popravljaš, ne seštevaš!).
- Negotovo branje označi z [~], neberljivo z [?]. Ne izmišljuj vsebine.
- Označi, katera vrstica je v rdečem tušu ("red": true).
- Izhod: SAMO veljaven JSON brez ograj in komentarjev:
{"left": [{"blatt": "...", "classen": "...", "parzelle": "...", "dominical": "...", "rustical": "...", "hausNo": "...", "name": "...", "stand": "...", "wohnort": "...", "joch": "...", "klafter": "...", "red": false, "note": "..."}],
 "right": [{"label": "...", "joch": "...", "klafter": "...", "red": true, "note": "..."}],
 "pageNote": "splošna berljivost strani"}`;
  }
  if (page === 141) {
    return `To je stran 141 katastrskega registra lastnikov za k.o. Griblje, franciscejski kataster 1825, nemška Kurrent pisava, deloma rdeči tuš. ${HEADERS}

LEVI del: naslov "Recapitulation", večina stolpcev PRAZNIH, ob desnem robu levi strani je vidnih nekaj majhnih številskih parov (npr. 101 253, 89 78 ...) — prepiši jih po vrsticah, kot jih vidiš.
DESNI del: zgoraj pridelek prejšnjih vrstic, pod njim pa v RDEČEM tušu tabela z glavo (okvirno "Parf. | Quadrat. | Joch. | Klafter.") in VRSTICAMI, ki v vsaki vrstici nosijo dve številski referenci (npr. 830, 1188) in površino (Joch | Klafter); sledijo vsotne vrstice (Summa, Summa in der Gemeinde) z rdečimi številkami, opomba v Kurrentu ("Ohne ..."), navedba overovitve/letnice 1826 in podpisi (k.k. komisar, žig).

PRAVILA:
- Prepiši VSAKO vrstico, številke TOČNO kot so napisane (ne popravljaš, ne seštevaš!).
- Negotovo branje označi z [~], neberljivo z [?]. Ne izmišljuj vsebine.
- Izhod: SAMO veljaven JSON brez ograj in komentarjev:
{"left": [{"cells": ["...", "..."], "note": "..."}],
 "right": [{"parf1": "...", "parf2": "...", "joch": "...", "klafter": "...", "red": true, "note": "..."}],
 "summaries": [{"label": "...", "value1": "...", "value2": "...", "red": true, "note": "..."}],
 "bottomText": "opomba + overovitev + podpisi [~]/[?]",
 "pageNote": "splošna berljivost strani"}`;
  }
  if (page === 142) {
    return `To je stran 142 katastrskega registra lastnikov za k.o. Griblje, franciscejski kataster 1825, nemška Kurrent pisava. ${HEADERS}

Na strani je naslov "Verzeichnis" (kazalo) in abecedni SEZNAM LASTNIKOV s zaporednimi številkami (okvirno 1–72), stolpci: zap. št., ime, priimek, status (zapisano), kraj; na desnem delu pa naprej številke Blatt/Parzelle in imena.

PRAVILA:
- Prepiši VSAKO vrstico, črka-za-črko; številke točno kot napisane.
- Negotovo branje označi z [~], neberljivo z [?]. Ne izmišljuj vsebine.
- Izhod: SAMO veljaven JSON brez ograj in komentarjev:
{"rows": [{"no": "...", "vorname": "...", "zuname": "...", "stand": "...", "wohnort": "...", "blatt": "...", "parzelle": "...", "note": "..."}],
 "pageNote": "splošna berljivost strani"}`;
  }
  return `To je stran 143 (ZADNJA stran) katastrskega registra lastnikov za k.o. Griblje, franciscejski kataster 1825. Na strani so le 3 VRSTICE v RDEČEM tušu (kontrolne vsote): okvirno "Summa der Bauplätze" s številko 102, "» der Grundparzellen" s številko 2505, in "Zusammen" s številko 2607 — prepiši TOČNO, kaj je napisano, številke znak za znak.

PRAVILA:
- Negotovo branje označi z [~], neberljivo z [?].
- Izhod: SAMO veljaven JSON brez ograj in komentarjev:
{"rows": [{"label": "...", "value": "...", "red": true, "note": "..."}],
 "pageNote": "splošna berljivost strani"}`;
}

async function readPage(zai, page, pass) {
  const img = `${IMG_DIR}/send-${page}.jpg`;
  const b64 = fs.readFileSync(img).toString('base64');
  const call = zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(page) },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  // čvrsti časovni omejitev 150 s — ob visečem klicu vrnemo napako in poskusimo znova
  const completion = await Promise.race([
    call,
    new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 240s')), 240000))
  ]);
  return completion.choices[0]?.message?.content ?? '';
}

async function main() {
  const argvPages = process.argv.slice(2).map(Number).filter(Boolean);
  const pages = argvPages.length ? argvPages : [140, 141, 142, 143];
  const passes = [1, 2, 3];
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const p of pages) {
    for (const n of passes) {
      const out = `${OUT_DIR}/pass${n}-page${p}.json`;
      if (fs.existsSync(out)) { console.log(`stran ${p} prehod ${n}: že obstaja, preskočim`); ok++; continue; }
      const t0 = Date.now();
      let raw = null;
      for (let attempt = 1; attempt <= 6; attempt++) {
        try {
          console.log(`stran ${p} prehod ${n}: poskus ${attempt} ...`);
          raw = await readPage(zai, p, n);
          break;
        }
        catch (e) {
          const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
          console.error(`stran ${p} prehod ${n}: poskus ${attempt} napaka: ${e.message.slice(0, 120)}`);
          if (!is429 && attempt >= 4) break;
          await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
        }
      }
      if (raw) {
        fs.writeFileSync(out, JSON.stringify({ page: p, pass: n, model: 'glm-5v-turbo', created: Math.floor(Date.now() / 1000), raw, ms: Date.now() - t0 }, null, 1));
        console.log(`stran ${p} prehod ${n}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, ${raw.length} znakov)`);
        ok++;
      } else {
        console.error(`stran ${p} prehod ${n}: NEUSPEH po vseh poskusih`);
        fail++;
      }
      await new Promise(r => setTimeout(r, 4000));
    }
  }
  console.log(`KONEC: ${ok} OK, ${fail} NEUSPEH`);
  process.exit(fail > 0 ? 1 : 0);
}

main();
