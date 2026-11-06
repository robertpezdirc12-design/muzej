// P221 — branje trakov (križ page-VLM). Izhod: /tmp/p221/vlm-traki/tX_sYY.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p221/traki";
const OUT_DIR = "/tmp/p221/vlm-traki";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2);
const FILES = fs.readdirSync(IN_DIR).filter(f => /^t\d+_s\d+\.png$/.test(f))
  .sort((a, b) => {
    const [t1, s1] = a.replace('.png', '').split('_s');
    const [t2, s2] = b.replace('.png', '').split('_s');
    return parseInt(s1) - parseInt(s2) || parseInt(t1.slice(1)) - parseInt(t2.slice(1));
  })
  .filter(f => FILTER.length === 0 || FILTER.some(x => f.includes(x)));

function promptFor(file) {
  return `To je HORIZONTALNI TRAK (izrez) razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (leto 1885, Kurrent pisava). Datoteka = ${file}.
Vsaka VRSTICA tabele se razteza CEZ obe strani razprt lista: LEVA stran = Post-Nr (zaporedna), mesec+dan rojstva/krsta, vas (Geburtsort), hišna št., ime otroka, Religion/Geschlecht/Ehelich; DESNA stran = starši (oče+stan, mati+dekliški priimek), botri (Pathen), babica, duhovnik.

NALOGA: Prepiši VSE vrstice, ki so vidne v tem traku (od zgoraj navzdol). Za vsako vrstico:
- zaporedna številka (najbolj levi stolpec! Kurrent cifre: 7=γ-forma s prečko, 3/5/8 zmeda!)
- mesec + dan rojstva in dan krsta
- vas (POZOR: vsi vpisi z vasjo Griblje/Grible/Griable so KLJUČNI!)
- hišna številka
- ime otroka
- oče (ime+priimek+stan), mati (ime+roj. priimek)
- botra/botri
- duhovnik (podpis)
- morebitne POZNEJŠE Pripise (modri/rdeči črnilo: † datum smrti, poroka, ...)

Negotovo z [~], neberljivo z [?]. Če je trak PRAZEN (samo črte tabele), reci to.
Izhod: SAMO en veljaven JSON (brez ograj):
{"trak": "${file}", "vrstice": [{"zaporedna": "...", "datum": "...", "vas": "...", "hisna": "...", "otrok": "...", "ocec": "...", "matec": "...", "botra": "...", "duhovnik": "...", "pripis": "..."}], "opomba": "..."}`;
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
  for (let attempt = 1; attempt <= 6; attempt++) {
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
      if (attempt === 6) throw e;
      await new Promise(r => setTimeout(r, /429|Too many/.test(e.message) ? 30000 : 3000 * attempt));
    }
  }
}

async function main() {
  const inst = await ZAI.create();
  for (const f of FILES) {
    const out = `${OUT_DIR}/${f.replace('.png', '')}.json`;
    if (fs.existsSync(out)) { console.log(`${f}: ŽE`); continue; }
    try {
      const res = await readImg(inst, `${IN_DIR}/${f}`, f);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      console.log(`${f}: OK vrstice=${res.vrstice?.length ?? 0}`);
    } catch (e) {
      console.error(`${f}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
