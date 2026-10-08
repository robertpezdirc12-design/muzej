// Branje manjkajočih strani PUA (35–49) — brez sonde (kvota že dvignjena, 2026-10-08 ~16:05)
// Vsaka stran takoj shranjena v research/p3/pua-raw/pua-NN.json
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import { execSync } from 'child_process';

const RAW_DIR = 'research/p3/pua-raw';
const PAGES = Array.from({ length: 15 }, (_, i) => 35 + i);

async function readPage(zai, page) {
  const png = `/tmp/pua-pages/pua-${String(page).padStart(2, '0')}.png`;
  execSync(`python3 -c "from PIL import Image; im=Image.open('${png}').convert('RGB'); im.save('/tmp/pua-send.jpg', quality=92)"`);
  const b64 = fs.readFileSync('/tmp/pua-send.jpg').toString('base64');
  const prompt = `To je stran ${page} katastrskega registra lastnikov (PUA — "Besitzer-Protokoll" / Lastniški protokol) za k.o. Griblje iz franciscejskega katastra 1825, napisan v nemški Kurrent pisavi.

Prepiši VSAKE vrstico registra črka-za-črko, natanko kot je napisano (ne popravljaj črkovanja!). Vsak vnos ima stolpce: zaporedna številka, ime in priimek lastnika (kot je napisano), status/poklic (Bauer, Häusler, Bürger...), hišna številka (Haus), in številke parcel razdeljene po sekcijah (I, II, III, IV, V) ter b.P. (bauparzelle) opombe.

PRAVILA:
- Negotova branja označi z [~], neberljiva z [?]
- Ne izmišljuj vsebine; če stolpec manjka, pusti prazen
- Izpusti glavo strani in morebitne ponovljene naslove
- Izhod: JSON tabela objektov { "row": <zap. št.>, "name": "...", "status": "...", "house": ..., "sections": {"I": "...", ...}, "bP": "...", "note": "..." }
- Na koncu dodaj polje "pageNote" z opombo o splošni berljivosti strani`;

  const completion = await zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: prompt },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  return completion.choices[0]?.message?.content ?? '';
}

async function main() {
  const missing = PAGES.filter(p => !fs.existsSync(`${RAW_DIR}/pua-${String(p).padStart(2, '0')}.json`));
  if (!missing.length) { console.log('vse strani 35–49 že prebrane'); return; }
  console.log(`manjka ${missing.length} strani: ${missing.join(', ')}`);
  const zai = await ZAI.create();
  let done = 0, failed = [];
  for (const p of missing) {
    const out = `${RAW_DIR}/pua-${String(p).padStart(2, '0')}.json`;
    if (fs.existsSync(out)) continue;
    const t0 = Date.now();
    let raw = null;
    for (let attempt = 1; attempt <= 3; attempt++) {
      try { raw = await readPage(zai, p); break; }
      catch (e) {
        console.error(`stran ${p}: poskus ${attempt}: ${e.message.slice(0, 80)}`);
        await new Promise(res => setTimeout(res, 12000));
      }
    }
    if (raw) {
      fs.writeFileSync(out, raw);
      done++;
      console.log(`stran ${p}: OK (${((Date.now() - t0) / 1000).toFixed(0)} s, ${raw.length} znakov)`);
    } else {
      failed.push(p);
      console.error(`stran ${p}: NEUSPEH po 3 poskusih`);
    }
  }
  console.log(`\nPREBRANIH: ${done}/${missing.length}; neuspešnih: ${failed.length ? failed.join(', ') : 'nič'}`);
}
main();
