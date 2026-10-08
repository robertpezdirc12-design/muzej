// PUA branje — VLM, stran za stranjo (metoda P3: 1 klic/stran, [~] negotovo, [?] neberljivo)
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import { execSync } from 'child_process';

const RAW_DIR = 'research/p3/pua-raw';

async function readPage(zai, page) {
  const png = `/tmp/pua-pages/pua-${String(page).padStart(2, '0')}.png`;
  // JPEG kvaliteta 92 za manjšo velikost
  execSync(`python3 -c "from PIL import Image; im=Image.open('${png}').convert('RGB'); im.save('/tmp/pua-send.jpg', quality=92)"`);
  const b64 = fs.readFileSync('/tmp/pua-send.jpg').toString('base64');
  const prompt = `To je stran ${page} katastrskega registra lastnikov (PUA — "Neue Häuser-Sequence"? ne, to je "Besitzer-Protokoll" / Lastniški protokol) za k.o. Griblje iz franciscejskega katastra 1825, napisan v nemški Kurrent pisavi.

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
  const pages = process.argv.slice(2).map(Number);
  if (!pages.length) { console.error('usage: bun scripts/pua-read.mjs <page>...'); process.exit(1); }
  const zai = await ZAI.create();
  for (const p of pages) {
    const out = `${RAW_DIR}/pua-${String(p).padStart(2, '0')}.json`;
    if (fs.existsSync(out)) { console.log(`stran ${p}: že obstaja, preskočim`); continue; }
    const t0 = Date.now();
    let raw = null;
    for (let attempt = 1; attempt <= 5; attempt++) {
      try {
        raw = await readPage(zai, p);
        break;
      } catch (e) {
        const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
        console.error(`stran ${p}: poskus ${attempt} napaka: ${e.message.slice(0, 80)}`);
        if (!is429 && attempt >= 2) break;
        await new Promise(r => setTimeout(r, 25000));
      }
    }
    if (raw) {
      fs.writeFileSync(out, JSON.stringify({ page: p, raw, ms: Date.now() - t0 }, null, 1));
      console.log(`stran ${p}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, ${raw.length} znakov)`);
    } else {
      console.error(`stran ${p}: NEUSPEH po vseh poskusih`);
    }
    await new Promise(r => setTimeout(r, 4000));
  }
}
main();
