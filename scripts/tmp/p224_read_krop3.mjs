// P224 — branje kropov pass-3 (hišni-stripi + re-krops + foliacija-spoj). Izhod: /tmp/p224/vlm-krop3/NN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p224/krop3";
const OUT_DIR = "/tmp/p224/vlm-krop3";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2);
const FILES = fs.readdirSync(IN_DIR).filter(f => /^.*\.png$/.test(f))
  .filter(f => FILTER.length === 0 || FILTER.some(x => f.includes(x)));

function promptFor(file) {
  if (file.includes('_hisna_strip')) {
    return `To je navpični IZREZ HIŠNEGA STOLPCA (Hiſ-Nr.) celotne razprte strani KRSTNE matične knjige župnije Podzemelj (leto 1882, Kurrent pisava). Datoteka = ${file}.
NALOGA: Preberi VSAKO ročno vpisano hišno številko OD ZGORAJ NAVZDOL (v vrstnem redu vrstic!). Če je vrstica PRAZNA (brez hišne št.), zapiši null.
POZOR NA KURRENT: 1 = ozka črtica (NI zanke!); 4 = zankasta; 7 = γ-forma s prečko; 3/5/8 zmeda; 2/4 zmeda; 6/0 zmeda; 11 = dve črtici. Obštrni pripisi (moder svinčnik, letnice) NE veljajo!
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "stevilke": ["1", "2", null, ...], "opomba": "..."}`;
  }
  if (file.includes('_pag3')) {
    return `To je ZGORNJI LEVI KOT razprte strani KRSTNE matične knjige Podzemelj (1882/1883) z GOLO SVINČNO PAGINACIJO arhivarja. Datoteka = ${file}.
NALOGA: Preberi svinčno številko (2–3 cifre). SERIJA-'sken−6': s157='151', s159='153', s160='154', s161='155' — pričakovano: s162='156', s163='157', s164='158'! (Alternativa: če je '160/161/162' → skok-v-seriji!) POZOR: Kurrent 6/0 zmeda (zanka-spodaj-vs-zgoraj!), 7/1, 3/5/8!
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "paginacija": "...", "cifre_posamezno": ["..."], "opomba": "..."}`;
  }
  return `To je ENA VRSTICA (izrez) razprte strani KRSTNE matične knjige župnije Podzemelj (leto 1882, Kurrent pisava). Datoteka = ${file}.
NALOGA — prepiši vrstico S ČIM VEČ NATAČNOSTJO: zaporedna št. (levi stolpec!), mesec+dan rojstva/krsta, vas (Griblje-ali-ne!), hišna št., ime otroka+spol, oče (ime+priimek+stan), mati (ime+roj.), botra/botri, duhovnik, POZNEJŠI-PRIPISI (modro/rdeče!).
Negotovo z [~], neberljivo z [?]. Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "zaporedna": "...", "mesec": "...", "rojen": "...", "krsten": "...", "vas": "...", "hisna": "...", "otrok": "...", "spol": "...", "ocec": "...", "matec": "...", "botra": "...", "duhovnik": "...", "pripis": "...", "opomba": "..."}`;
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
  for (let attempt = 1; attempt <= 10; attempt++) {
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
      await new Promise(r => setTimeout(r, /429|Too many/.test(e.message) ? 120000 : 8000 * attempt));
    }
  }
}

async function main() {
  const inst = await ZAI.create();
  for (const f of FILES) {
    await new Promise(r => setTimeout(r, 12000));
    const out = `${OUT_DIR}/${f.replace('.png', '')}.json`;
    if (fs.existsSync(out)) { console.log(`${f}: ŽE`); continue; }
    try {
      const res = await readImg(inst, `${IN_DIR}/${f}`, f);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      const summary = res.stevilke ? `stevilke=${JSON.stringify(res.stevilke).slice(0, 120)}` :
        res.paginacija ? `pag=${res.paginacija}` :
        `zap=${res.zaporedna} vas=${res.vas} hisna=${res.hisna} otrok=${res.otrok}`;
      console.log(`${f}: OK ${String(summary).slice(0, 170)}`);
    } catch (e) {
      console.error(`${f}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
