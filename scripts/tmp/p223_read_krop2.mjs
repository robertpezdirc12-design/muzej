// P223 — branje krop2 (hi-zoom dvomi). Izhod: /tmp/p223/vlm-krop/NN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p223/krop2";
const OUT_DIR = "/tmp/p223/vlm-krop";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2);
const FILES = fs.readdirSync(IN_DIR).filter(f => /^.*\.png$/.test(f))
  .filter(f => FILTER.length === 0 || FILTER.some(x => f.includes(x)));

function promptFor(file) {
  const isPag = file.includes('_pag_hi');
  if (isPag) {
    return `To je ZGORNJI LEVI KOT razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (Kurrent pisava). Datoteka = ${file}.
NALOGA: Preberi ročno vpisano SVINČNO PAGINACIJO/FOLIACIJO (npr. '155' ali 'Pag. 190'). POZOR: Kurrent cifre, 3/5/6/8 zmeda! Če je natisnjena oznaka 'Pag.' prisotna, to omeni!
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "paginacija": "...", "pag_oznaka": " Pag.|golo-svinčno", "opomba": "..."}`;
  }
  return `To je HI-ZOOM IZREZ dela vrstice razprte strani KRSTNE matične knjige župnije Podzemelj (leto 1883, Kurrent pisava). Datoteka = ${file}.
Če izrez vsebuje VAS+HIŠNO št.: preberi TOČNO (Kurrent 'G'-forma za Griblje! 3/5/8-zmeda, 7=γ-s prečko!). 
Če vsebuje PRIPIS (modro/rdeče pisalo, poznejši dodatek — MMK/matrični pregled 20. stoletje!): preberi TOČNO vse številke (datum smrti/poroke, letnica!).
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "vas": "...", "hisna": "...", "pripis": "...", "opomba": "..."}`;
}

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readImg(zai, img, file) {
  const b64 = fs.readFileSync(img).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(file) },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  let completion;
  for (let attempt = 1; attempt <= 8; attempt++) {
    completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 240000))
    ]);
    try {
      const c = completion?.choices?.[0]?.message?.content;
      if (!c) throw new Error('prazna vsebina');
      return parseContent(c);
    } catch (e) {
      console.error(`  ${file}: poskus ${attempt} ni OK (${e.message})`);
      if (attempt === 8) throw e;
      await new Promise(r => setTimeout(r, /429|Too many/.test(e.message) ? 90000 : 8000 * attempt));
    }
  }
}

async function main() {
  const inst = await ZAI.create();
  for (const f of FILES) {
    await new Promise(r => setTimeout(r, 8000));
    const out = `${OUT_DIR}/${f.replace('.png', '')}.json`;
    if (fs.existsSync(out)) { console.log(`${f}: ŽE`); continue; }
    try {
      const res = await readImg(inst, `${IN_DIR}/${f}`, f);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      console.log(`${f}: OK vas=${res.vas} hisna=${res.hisna} pripis=${String(res.pripis || '').slice(0, 80)} pag=${res.paginacija || '-'}`);
    } catch (e) {
      console.error(`${f}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
