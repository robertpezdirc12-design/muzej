// P176 branje — VLM, sken za skenom (mrliški vpisi 04894, leto 1910)
// Metoda P153–P175: 1 klic/sken, [~] negotovo, [?] neberljivo, ≤2 skena/serijo foreground
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import { execSync } from 'child_process';

const RAW_DIR = '/tmp/p176/raw';
const SCAN_DIR = '/tmp/p176';

async function readScan(zai, scan) {
  const jpg = `${SCAN_DIR}/s${scan}.jpg`;
  const b64 = fs.readFileSync(jpg).toString('base64');
  const prompt = `To je sken ${scan} mrliškega vpisa župnije Griblje (matricula knjiga 04894, leto 1910). Pisava je nemški Kurrent.

Prepiši VSAK mrliški vpis črka-za-črko, natanko kot je napisano (ne popravljaj črkovanja!). Vsak vpis ima stolpce: zaporedna številka (zap. št.), datum smrti (dan + mesec), ime in priimek umrlega, stan (samski/oženjen/vdovec/vdova/otro...), vas, hišna številka, starost, bolezen ali vzrok smrti, prevideni sakramenti (opomba, npr. "sv. olje"), datum pokopa (dan), duhovnik/podpis.

PRAVILA:
- Negotova branja označi z [~], neberljiva z [?]
- Ne izmišljuj vsebine; če stolpec manjka, pusti null
- Če je na vrhu velika glava z letnico (npr. "1910."), to NE gre med vpise — le kot "header" polje
- Če je vrsta prepisana/izbrisana, to zapiši v opombo
- Izhod: JSON objekt { "scan": <sken>, "header": "...", "rows": [ { "zap": <zap. št.>, "mesec": "...", "smrt": "<dan>", "ime": "...", "stan": "...", "vas": "...", "hisa": "<hišna št.>", "starost": "...", "bolezen": "...", "previden": "...", "pokop": "<dan>", "duhovnik": "...", "opomba": null } ] }
- Vsi meseci naj bodo v slovenščini kot so napisani (Januar, Februar...)`;

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
  const scans = process.argv.slice(2).map(Number);
  if (!scans.length) { console.error('usage: bun p176_read_page.mjs <sken>...'); process.exit(1); }
  fs.mkdirSync(RAW_DIR, { recursive: true });
  const zai = await ZAI.create();
  for (const s of scans) {
    const out = `${RAW_DIR}/s${s}.json`;
    if (fs.existsSync(out)) { console.log(`sken ${s}: že obstaja, preskočim`); continue; }
    const t0 = Date.now();
    let raw = null;
    for (let attempt = 1; attempt <= 5; attempt++) {
      try {
        raw = await readScan(zai, s);
        break;
      } catch (e) {
        const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
        console.error(`sken ${s}: poskus ${attempt} napaka: ${e.message.slice(0, 80)}`);
        if (!is429 && attempt >= 2) break;
        await new Promise(r => setTimeout(r, 25000));
      }
    }
    if (raw) {
      fs.writeFileSync(out, JSON.stringify({ scan: s, raw, ms: Date.now() - t0 }, null, 1));
      console.log(`sken ${s}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, ${raw.length} znakov)`);
    } else {
      console.error(`sken ${s}: NEUSPEH po vseh poskusih`);
    }
    await new Promise(r => setTimeout(r, 4000));
  }
}
main();
