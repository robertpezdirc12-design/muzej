// P63 — 3. neodvisen prehod: fokusirani izrezi kolon p139 (Dominical/Rustical/
// Haus @ 5× in Stand/Wohnort @ 5×) + re-read spodnje polovice (Parzelle
// 51–60). Oči = prehod A, tail-139-* (celi izrezi) = prehod B, to = prehod C.
// Izhod: research/issue17/ps-raw/tail-139-cols-<part>.json
// Uporaba: node scripts/p63_ps_read_cols.mjs   (vseh 5 delov, skip-existing)
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const OUT_DIR = 'research/issue17/ps-raw';
const IMG_DIR = '/tmp/p63';

function promptFor(part) {
  const base = `Izrez iz strani 139 zaključka registra "Der Grund-Parcellen der Gemeinde GRÜBLE" (k.o. Griblje, 1825), nemška Kurrent pisava, deloma rdeči tuš. Prepiši številke TOČNO kot so napisane (ne popravljaš, ne seštevaš, ne ugibaš zlogov).
KURRENT PRAVILA: 4 ima zanko in je podobna 8/9; 1 je ozka črtica; 7 ima prečko; 5 je podobna 6/3; 3 ima zgornjo horizontalno črtico in odprto spodaj. Preštej cifre vsake številke. Negotovo [~], neberljivo [?]. Prazna celica null. Izhod: SAMO en veljaven JSON (brez ograj, brez komentarjev).`;
  if (part === 'colsL-a' || part === 'colsL-b') {
    return `${base}
Izrez vsebuje 3 stolpce: "Dominical." | "Rustical." (3 podkolone, navadno prazne) | "Haus Nº." (pogosto rdeči tuš). ${part === 'colsL-a' ? 'Vrstice 1–10 tabele (Parzelle 41–50); prva vidna vrstica = row 1.' : 'Vrstice 11–20 tabele (Parzelle 51–60); prva vidna vrstica = row 11. Pod debelo črto sta vsoti (običajno dvomestni) — vpiši ju v "vsote".'}
Izhod: {"vrstice": [{"row": 1, "dominical": "1", "rustical": null, "haus": "1082"}], "vsote": [{"kol": "dominical", "vrednost": "82"}, {"kol": "haus", "vrednost": "81"}], "opomba": "..."} — "vsote" samo v delu b (ali prazen seznam).`;
  }
  if (part === 'colsR-a' || part === 'colsR-b') {
    return `${base}
Izrez vsebuje 2 stolpca: "Stand." | "Wohnort." (Wohnort pogosto rdeči tuš). ${part === 'colsR-a' ? 'Vrstice 1–10 tabele (Parzelle 41–50); prva vidna vrstica = row 1.' : 'Vrstice 11–20 tabele (Parzelle 51–60); prva vidna vrstica = row 11. Pod debelo črto sta vsoti — vpiši ju v "vsote".'}
Izhod: {"vrstice": [{"row": 1, "stand": null, "wohnort": "63"}], "vsote": [{"kol": "stand", "vrednost": "125"}, {"kol": "wohnort", "vrednost": "183"}], "opomba": "..."} — "vsote" samo v delu b (ali prazen seznam).`;
  }
  return `${base}
Izrez vsebuje 3–4 stolpce spodnje polovice tabele: "Nro. der Parzelle" (51–60) | "Dominical." | "Rustical." (prazne podkolone) | "Haus Nº." (rdeči tuš). Pod debelo črto sta vsoti (pod Dominical in pod Haus). POZOR: Parzelle so 51–60 (naraščajoče) — to je samokontrola.
Izhod: {"vrstice": [{"row": 11, "parzelle": "51", "dominical": "1", "rustical": null, "haus": "960"}], "vsote": [{"kol": "dominical", "vrednost": "82"}, {"kol": "haus", "vrednost": "81"}], "opomba": "..."}`;
}

const PARTS = ['colsL-a', 'colsL-b', 'colsR-a', 'colsR-b', 'full-b2'];
const IMG_OF = {
  'colsL-a': 'p139-colsL-a.jpg',
  'colsL-b': 'p139-colsL-b.jpg',
  'colsR-a': 'p139-colsR-a.jpg',
  'colsR-b': 'p139-colsR-b.jpg',
  'full-b2': 'p139-full-b2.jpg',
};

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const part of PARTS) {
    const out = `${OUT_DIR}/tail-139-${part}.json`;
    if (fs.existsSync(out)) { console.log(`${part}: že obstaja, preskočim`); ok++; continue; }
    const t0 = Date.now();
    let completion = null;
    for (let attempt = 1; attempt <= 6; attempt++) {
      try {
        console.log(`${part}: poskus ${attempt} ...`);
        const b64 = fs.readFileSync(`${IMG_DIR}/${IMG_OF[part]}`).toString('base64');
        completion = await Promise.race([
          zai.chat.completions.createVision({
            messages: [{ role: 'user', content: [
              { type: 'text', text: promptFor(part) },
              { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
            ]}],
            thinking: { type: 'disabled' }
          }),
          new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))
        ]);
        break;
      }
      catch (e) {
        const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
        console.error(`${part}: poskus ${attempt} napaka: ${e.message.slice(0, 120)}`);
        if (!is429 && attempt >= 4) break;
        await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
      }
    }
    if (completion) {
      const content = completion.choices[0]?.message?.content ?? '';
      const rec = { part, model: 'glm-5v-turbo', created: Math.floor(Date.now() / 1000) };
      if (completion.usage) rec.usage = completion.usage;
      try {
        rec.parsed = parseContent(content);
        rec.content = content;
      } catch (e) {
        rec.content = content;
        rec.parseError = e.message;
        console.error(`${part}: JSON PARSE NAPAKA — ${e.message.slice(0, 80)}`);
      }
      fs.writeFileSync(out, JSON.stringify(rec, null, 1) + '\n');
      const nr = rec.parsed ? rec.parsed.vrstice?.length ?? '?' : '?';
      console.log(`${part}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, vrstice ${nr})`);
      ok++;
    } else {
      console.error(`${part}: NEUSPEH po vseh poskusih`);
      fail++;
    }
    await new Promise(r => setTimeout(r, 3000));
  }
  console.log(`KONEC: ${ok} OK, ${fail} NEUSPEH`);
  process.exit(fail > 0 ? 1 : 0);
}

main();
