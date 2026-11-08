// P57 — branje strani 3–4 registra PS ("Der Grund-Parcellen der Gemeinde GRÜBLE")
// = začetek glavnega registra, številke 1–40 (Blatt I), ki ju P38/P56 izbora NISTA
// vključila (edini vir številk 1–36 je bil S3 zapadek, str. 138–139).
// Metoda P41/p44: 3 neodvisna VLM prehoda na stran, glm-5v-turbo, [~] negotovo /
// [?] neberljivo; številke TOČNO kot napisane (ne popravlja, ne sešteva).
// Vhod: /tmp/ps34/send-<page>.jpg (VAČ pdfPageImage uodid 373415 docid 41780
//        + page=3/4; 2× Lanczos upscale, JPEG q92 — recept p41/P3 README).
// Izhod: research/issue17/ps-raw/ps-003{,-pass2,-pass3}.json + ps-004{...}.json
//        (isti format kot obstoječi ps-raw: {page, model, created, usage, content},
//        content = NDJSON vrstic; vsotna vrstica strani ločeno v polju "summa").
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const OUT_DIR = 'research/issue17/ps-raw';
const IMG_DIR = '/tmp/ps34';

const HEADERS = `Glava tabele (obojestranska registrska oblika, kot na straneh 5+ istega protokola):
LEVI del: "N:o des Blattes | Bezeichnung des Eigentümers (podstopca: Gebäude der Grundstücke — Dominical | Rustikal) | N:o des Grundstückes | Haus Nro. | Vor- und Zuname | Stand | Wohnort".
DESNI del ("Des Grundstückes"): "Kultura Gattung | Flächen Inhalt (podstopca: N:o | Quadrat. Joch. | Klafter) | Classe | Reiner Ertrag in Metall Münze (fl. | kr.) | Capital Werth nach p.Crt. (fl. | kr.) | Anmerkung".
Ugotovljeno iz sosledja (kontrola, ne podatek): stran 3 nosi N:o des Grundstückes ~1–20, stran 4 ~21–40; prva vrstica strani nosi Blatt "I".`;

function promptFor(page) {
  return `To je stran ${page} katastrskega registra "Der Grund-Parcellen der Gemeinde GRÜBLE" (k.o. Griblje, franciscejski kataster 1825), nemška Kurrent pisava, deloma v RDEČEM tušu. ${HEADERS}

PRAVILA:
- Prepiši VSAKO vrstico tabele, črka-za-črko, številke TOČNO kot so napisane (ne popravljaš, ne seštevaš!).
- Stolpec "N:o" znotraj Flächen Inhalt (referenčna številka znotraj Blatt) NE prepiši — samo Quadrat. Joch. in Klafter.
- Negotovo branje označi z [~], neberljivo z [?]. Ne izmišljuj vsebine; prazno stolpce pusti null.
- Blatt ("N:o des Blattes") je rimska številka ("I"); piši samo v vrstici, kjer je dejansko izpisano, drugače null.
- Rdeče tuširane dopise (robni zapisi, prek vrstic, prečrtanja, "Rgr.", letnice 1843/1860/1866, "Dito", "Gründe von ..." itd.) zapiši v anmerkung TISTE vrstice, na katero se nanašajo; prečrtano vrstico vseeno prepiši (vsebina ostaja) in v anmerkung dodaj "prečrtano".
- Zadnjo vsotno vrstico na dnu strani (rdeči tuš, "Summa"/"Ftreag" ...) NE vključi med vrstice — samodejno je izpiši kot ZADNJI NDJSON objekt z obliko {"summa": {"label": "...", "joch": "...", "klafter": "...", "red": true, "extra": "..."}}, če je na strani vidna.
- Izhod: SAMO veljaven NDJSON (ena vrstica = ena vrstica tabele, brez ograj, brez komentarjev), objekti v tem tvorcu:
{"blatt": "..." ali null, "parzella": "...", "hausNr": "..." ali null, "name": "...", "stand": "..." ali null, "wohnort": "..." ali null, "kultur": "...", "joch": "..." ali null, "klafter": "..." ali null, "klasse": "..." ali null, "ertragFl": "..." ali null, "ertragKr": "..." ali null, "anmerkung": "..." ali null}`;
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
  // čvrsti časovni omejitev — ob visečem klicu vrnemo napako in poskusimo znova
  const completion = await Promise.race([
    call,
    new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 240s')), 240000))
  ]);
  return completion;
}

async function main() {
  // podpora za posamezne prehode: "3" (vse 3 prehode strani 3) ali "3:2" (samo stran 3, prehod 2)
  const args = process.argv.slice(2);
  const jobs = [];
  if (args.length) {
    for (const a of args) {
      const [pStr, nStr] = a.split(':');
      const p = Number(pStr);
      if (!p) continue;
      if (nStr) jobs.push([p, Number(nStr)]);
      else jobs.push([p, 1], [p, 2], [p, 3]);
    }
  } else {
    for (const p of [3, 4]) jobs.push([p, 1], [p, 2], [p, 3]);
  }
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const [p, n] of jobs) {
      const suffix = n === 1 ? '' : `-pass${n}`;
      const out = `${OUT_DIR}/ps-00${p}${suffix}.json`;
      if (fs.existsSync(out)) { console.log(`stran ${p} prehod ${n}: že obstaja, preskočim`); ok++; continue; }
      const t0 = Date.now();
      let completion = null;
      for (let attempt = 1; attempt <= 6; attempt++) {
        try {
          console.log(`stran ${p} prehod ${n}: poskus ${attempt} ...`);
          completion = await readPage(zai, p, n);
          break;
        }
        catch (e) {
          const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
          console.error(`stran ${p} prehod ${n}: poskus ${attempt} napaka: ${e.message.slice(0, 120)}`);
          if (!is429 && attempt >= 4) break;
          await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
        }
      }
      if (completion) {
        const content = completion.choices[0]?.message?.content ?? '';
        const rec = {
          page: p,
          pass: n,
          model: 'glm-5v-turbo',
          created: Math.floor(Date.now() / 1000),
        };
        if (completion.usage) rec.usage = completion.usage;
        rec.content = content;
        fs.writeFileSync(out, JSON.stringify(rec, null, 1) + '\n');
        console.log(`stran ${p} prehod ${n}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, ${content.length} znakov, ${content.split('\n').filter(l => l.trim()).length} NDJSON vrstic)`);
        ok++;
      } else {
        console.error(`stran ${p} prehod ${n}: NEUSPEH po vseh poskusih`);
        fail++;
      }
      await new Promise(r => setTimeout(r, 4000));
  }
  console.log(`KONEC: ${ok} OK, ${fail} NEUSPEH`);
  process.exit(fail > 0 ? 1 : 0);
}

main();
