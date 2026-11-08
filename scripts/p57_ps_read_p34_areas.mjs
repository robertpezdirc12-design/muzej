// P57 (dodatek 2) — TARČNO ponovno branje stolpca površin (Flächen Inhalt → Klafter)
// za strani 3–4 iz povečanih izrezov (3× Lanczos, metoda arbitracije P41).
// Razlog: polnostransko branje ima tveganja na posameznih števkah (Kurrent 6/8, 2/3,
// 0/4, vodilna 7) — izrezi so arbitracijski sloj (ob Likih ugotovitvah v delovnem
// dnevniku: r.11 p3 = 729 ne 129, r.12 p3 = 79 ne 39, r.32 p4 = 42 ne 92).
// Vhod: /tmp/ps34/crop{3,4}-areas.jpg
// Izhod: research/issue17/ps-raw/ps-00{3,4}-areas{n}.json
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const OUT_DIR = 'research/issue17/ps-raw';

function promptFor(page) {
  const rng = page === 3 ? '1–20' : '21–40';
  return `Ta izrez prikazuje stolpec površin ("Flächen Inhalt", podstopec Quadrat-Klafter) katastrskega registra "Der Grund-Parcellen der Gemeinde GRÜBLE" (stran ${page}, franciscejski kataster 1825, Kurrent pisava). Vrstice ustrezajo števikam parcel ${rng} (od zgoraj navzdol).

PRAVILA:
- Prepiši VSAKO vidno površino (številka v levem delu izreza, ob levem robu celice), številke TOČNO kot so napisane (ne popravljaš, ne ugibaš!).
- Kurrent: 7 ima dolgo horizontalno zaključko (ne zamenjaj z 1!), 4 je podobna "h", 6/8 se lahko zamenjata, 0 je samo oval brez repa.
- PRAZNA celica (kjer ni številke — npr. prečrtana ali nikoli zapisana) = vpiši [?] v tabelo kot "klafter": "[?]".
- Prečrtane številke vseeno prepiši (vsebina ostaja).
- Vsotna vrsta "Fürtrag" na dnu (če je vidna v izrezu) = vrstica 20 z oznako "fürtrag": true.
- Izhod: SAMO veljaven NDJSON (20 vrstic, brez ograj in komentarjev):
{"vrstica": 1, "klafter": "...", "fürtrag": false}`;
}

async function readCrop(zai, page, pass) {
  const img = `/tmp/ps34/crop${page}-areas.jpg`;
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
    else jobs.push([p, 1], [p, 2], [p, 3]);
  }
  if (!jobs.length) for (const p of [3, 4]) jobs.push([p, 1], [p, 2], [p, 3]);
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const [p, n] of jobs) {
    const out = `${OUT_DIR}/ps-00${p}-areas${n === 1 ? '' : n}.json`;
    if (fs.existsSync(out)) { console.log(`stran ${p} površine prehod ${n}: že obstaja, preskočim`); ok++; continue; }
    const t0 = Date.now();
    let completion = null;
    for (let attempt = 1; attempt <= 6; attempt++) {
      try {
        console.log(`stran ${p} površine prehod ${n}: poskus ${attempt} ...`);
        completion = await readCrop(zai, p, n);
        break;
      }
      catch (e) {
        const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
        console.error(`stran ${p} površine prehod ${n}: poskus ${attempt} napaka: ${e.message.slice(0, 120)}`);
        if (!is429 && attempt >= 4) break;
        await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
      }
    }
    if (completion) {
      const content = completion.choices[0]?.message?.content ?? '';
      const rec = {
        page: p,
        kind: 'areas',
        pass: n,
        model: 'glm-5v-turbo',
        created: Math.floor(Date.now() / 1000),
      };
      if (completion.usage) rec.usage = completion.usage;
      rec.content = content;
      fs.writeFileSync(out, JSON.stringify(rec, null, 1) + '\n');
      console.log(`stran ${p} površine prehod ${n}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, ${content.length} znakov)`);
      ok++;
    } else {
      console.error(`stran ${p} površine prehod ${n}: NEUSPEH po vseh poskusih`);
      fail++;
    }
    await new Promise(r => setTimeout(r, 4000));
  }
  console.log(`KONEC: ${ok} OK, ${fail} NEUSPEH`);
  process.exit(fail > 0 ? 1 : 0);
}

main();
