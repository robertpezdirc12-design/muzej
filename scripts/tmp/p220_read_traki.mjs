// P220 — trak-reader (32 izrezov → JSON). Izhod: /tmp/p220/trak-reads/tN_sM.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const DIR = '/tmp/p220/traki';
const OUT = '/tmp/p220/trak-reads';
fs.mkdirSync(OUT, { recursive: true });

const TRAK_PROMPT = `To je VODORAVNI TRAK (¼ strani razprtega naslovnega lista ali tabele) mrliške matične knjige župnije Podzemelj (Kurrent pisava, leto 1857 (KNJIGA-SE-ZAČNE-1857!) / 1858 — STAREJŠA pisava!). Vidni so lahko: letnica-glava (rokopisno diagonalno), mesec-glave (Jänner, Feber/Februar, März, April, Mai, Juni, July, August, September, October, November, Dezember — rokopisno čez vrsto), TABLE-VRSTICE, VSOTNA-vrsta (morda z RAZPETIMI CIFRAMI '1 8 5 7' ali '1 8 5 8' čez stolpce = P214-TIP-MARKER!), prazne vrste.
Stolpci vrstic: ZAPOREDNA ŠT. (levi rob, ročno!) | mesec+dan smrti / dan pokopa | vas + hišna št. | ime, priimek, stan | vere/spola (kljukice) | starost | bolezen/vzrok | previden | podpis.
POZOR KURRENT: 4-zanka; 1-ozka-črtica; 7-γ-s-prečko (NE 8!); 5≈6; 3/5/8-zmeda; 9-dolgi-rep. Hišne: ista pravila. '½'='pol', '¼'='četrt'.
PRAVILA:
- Prepiši VSAKO vidno table-vrstico od zgoraj navzdol. Preskoči mesečne glave (a jih OZNAČI v mesec_glave!).
- ZAPOREDNA ŠT. beri IZ LEVEGA ROBA! Če vrstica NIMA številke, zaporedna = "".
- Če je trak del NASLOVNEGA LISTA ('Sterb-Buch.' fraktura), to označi!
- Negotovo z [~], neberljivo z [?].
- Izhod: SAMO en veljaven JSON:
{"trak": "opis kaj je vidnega", "letnica_glava": "rokopisna letnica ali null", "mesec_glave": ["...", ...], "vrstice": [{"pozicija": 1, "zaporedna": "26", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "previden": "...", "duhovnik": "...", "opomba": "..."}], "opomba": "..."}`;

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readTrak(zai, name) {
  const b64 = fs.readFileSync(`${DIR}/${name}.png`).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: TRAK_PROMPT },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  for (let attempt = 1; attempt <= 3; attempt++) {
    const completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 150000))
    ]);
    try {
      const c = completion?.choices?.[0]?.message?.content;
      if (!c) throw new Error('prazna vsebina');
      return parseContent(c);
    } catch (e) {
      console.error(`  ${name}: poskus ${attempt} ni OK (${e.message})`);
      if (attempt === 3) throw e;
      await new Promise(r => setTimeout(r, 3000 * attempt));
    }
  }
}

async function main() {
  const FILTER = process.argv.slice(2);
  const names = fs.readdirSync(DIR).filter(f => f.endsWith('.png')).map(f => f.replace('.png', ''))
    .filter(n => FILTER.length === 0 || FILTER.includes(n)).sort();
  const inst = await ZAI.create();
  for (const name of names) {
    const out = `${OUT}/${name}.json`;
    if (fs.existsSync(out)) { console.log(`${name}: ŽE`); continue; }
    try {
      const res = await readTrak(inst, name);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      const zap = (res.vrstice || []).map(v => v.zaporedna || '·').join(',');
      console.log(`${name}: OK n=${res.vrstice?.length ?? 0} zap=[${zap}] glave=${JSON.stringify(res.mesec_glave).slice(0, 70)}`);
    } catch (e) {
      console.error(`${name}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
