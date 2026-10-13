// P57 (dodatek) — TARČNO ponovno branje stolpcev "N:o des Grundstückes" + "Haus Nro."
// za strani 3–4 iz povečanih izrezov leve tabele (3× Lanczos, metoda arbitracije P41).
// Razlog: pri polnostranskem branju je VLM stolpec Haus Nro. sistematično odbral
// napačno ("6a/6b/6o" oz. vse "1") — dvomestne hišne številke (60–66 ...) so v
// Kurrentu zamenljive z malimi črkami; izrez + ožji poziv = arbitracija.
// Vhod: /tmp/ps34/crop{3,4}-left.jpg
// Izhod: research/issue17/ps-raw/ps-00{3,4}-cols{,2}.json
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const OUT_DIR = 'research/issue17/ps-raw';

function promptFor(page) {
  const rng = page === 3 ? '1–20' : '21–40';
  return `Ta izrez prikazuje LEVI del tabele katastrskega registra "Der Grund-Parcellen der Gemeinde GRÜBLE" (stran ${page}, franciscejski kataster 1825, nemška Kurrent pisava). Stolpci od leve: "N:o des Blattes" (rimske številke ali ditó pika), "Bezeichnung des Eigentümers" (pretežno prazno), "N:o des Grundstückes" (številke ${rng}), podstopca Dominical/Rustikal (pretežno prazno), OZKI stolpec z isto številko "1" v vsaki vrstici (to NISO hišne številke), in stolpec "Haus Nro." z DVOMESTNimi hišnimi številkami (npr. 60, 61, 62, 63, 64, 65, 66, 51, 31, 29, 34, 11, 18, 0 ...).

PRAVILA:
- Prepiši ZA VSAKO VRSTICO (od zgoraj navzdol, VSEH 20 vrstic): številko parcele in hišno številko.
- Številke TOČNO kot so napisane (ne popravljaš, ne ugibaš po vrstnem redu!).
- OZKI stolpec z istimi "1" preskoči — hišna številka je NASLEDNJI stolpec za njim.
- Negotovo branje označi z [~] takoj za številko, neberljivo z [?].
- Izhod: SAMO veljaven NDJSON (20 vrstic, brez ograj in komentarjev):
{"grund": "...", "hausNr": "..."}`;
}

async function readCrop(zai, page, pass) {
  const img = `/tmp/ps34/crop${page}-left.jpg`;
  const b64 = fs.readFileSync(img).toString('base64');
  const call = zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(page) },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  const completion = await Promise.race([
    call,
    new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))
  ]);
  return completion;
}

async function main() {
  const jobs = [];
  for (const a of process.argv.slice(2)) {
    const [pStr, nStr] = a.split(':');
    const p = Number(pStr);
    if (!p) continue;
    if (nStr) jobs.push([p, Number(nStr)]);
    else jobs.push([p, 1], [p, 2]);
  }
  if (!jobs.length) for (const p of [3, 4]) jobs.push([p, 1], [p, 2]);
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const [p, n] of jobs) {
    const out = `${OUT_DIR}/ps-00${p}-cols${n === 1 ? '' : n}.json`;
    if (fs.existsSync(out)) { console.log(`stran ${p} kolone prehod ${n}: že obstaja, preskočim`); ok++; continue; }
    const t0 = Date.now();
    let completion = null;
    for (let attempt = 1; attempt <= 6; attempt++) {
      try {
        console.log(`stran ${p} kolone prehod ${n}: poskus ${attempt} ...`);
        completion = await readCrop(zai, p, n);
        break;
      }
      catch (e) {
        const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
        console.error(`stran ${p} kolone prehod ${n}: poskus ${attempt} napaka: ${e.message.slice(0, 120)}`);
        if (!is429 && attempt >= 4) break;
        await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
      }
    }
    if (completion) {
      const content = completion.choices[0]?.message?.content ?? '';
      const rec = {
        page: p,
        kind: 'cols',
        pass: n,
        model: 'glm-5v-turbo',
        created: Math.floor(Date.now() / 1000),
      };
      if (completion.usage) rec.usage = completion.usage;
      rec.content = content;
      fs.writeFileSync(out, JSON.stringify(rec, null, 1) + '\n');
      console.log(`stran ${p} kolone prehod ${n}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, ${content.length} znakov)`);
      ok++;
    } else {
      console.error(`stran ${p} kolone prehod ${n}: NEUSPEH po vseh poskusih`);
      fail++;
    }
    await new Promise(r => setTimeout(r, 4000));
  }
  console.log(`KONEC: ${ok} OK, ${fail} NEUSPEH`);
  process.exit(fail > 0 ? 1 : 0);
}

main();
