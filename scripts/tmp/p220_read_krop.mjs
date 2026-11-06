// P220 — krop-reader (21 izrezov → JSON). Izhod: /tmp/p220/krop-reads/NAME.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const DIR = '/tmp/p220/krop-grib';
const OUT = '/tmp/p220/krop-reads';
fs.mkdirSync(OUT, { recursive: true });

const PROMPT = `To je ZOOM-IZREZ (del strani ali stolpec) mrliške matične knjige župnije Podzemelj (Kurrent pisava, leto 1857/1858 — STAREJŠA pisava!). 
Stolpci vrstic (česar je vidno): ZAPOREDNA ŠT. (levi rob, ročno) | mesec+dan smrti / dan pokopa | vas + hišna št. | ime, priimek, stan | vere/spola | starost | bolezen/vzrok | previden | podpis duhovnika.
POZOR KURRENT: 4-zanka; 1-ozka-črtica; 7-γ-s-prečko (NE 8!); 5≈6; 3/5/8-zmeda; 9-dolgi-rep. Hišne: ista pravila. '½'='pol', '¼'='četrt'. Meseci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember.
PRAVILA:
- Če je izrez NAVPIČNI STOLPEC (zaporedne številke): prepiši VSAKO vidno številko od zgoraj navzdol, natančno (vključno s praznimi/prostori med številkami). Opozori, če katera MANJKA ali je neberljiva!
- Če je izrez VRSTICA: prepiši VSE vidne celote (vas, hišna, ime, stan, starost, bolezen, podpis) — črka-za-črko, brez popravlj
- Če so vidni MARKERJI (letnica-glava '1857'/'1858', VSOTNA z razpetimi ciframi '1 8 5 7'/'1 8 5 8', dvojna črta, naslovni-natis 'Sterb-Buch.'), to OZNAČI!
- Negotovo z [~], neberljivo z [?].
- Izhod: SAMO en veljaven JSON:
{"kaj": "opis izreza", "zaporedne": ["...", ...] (samo pri stolpcih, sicer null), "vrstice": [{"pozicija": 1, "zaporedna": "...", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "duhovnik": "..."}] (samo pri vrsticah, sicer null), "markerji": ["..."], "opomba": "..."}`;

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readKrop(zai, name) {
  const b64 = fs.readFileSync(`${DIR}/${name}.png`).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: PROMPT },
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
      const res = await readKrop(inst, name);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      const zap = res.zaporedne ? ` zap=[${res.zaporedne.join(',')}]` : '';
      const vr = res.vrstice ? ` vrst=${res.vrstice.length}` : '';
      console.log(`${name}: OK${zap}${vr}`);
    } catch (e) {
      console.error(`${name}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
