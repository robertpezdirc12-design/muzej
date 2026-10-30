// P162 — forenzično branje izrezov (leto 1896, mrliška 04894).
// Bere /tmp/p162/crops/manifest.json (trakovi x2.2 + celice x3.0) in
// primerjalno sliko cifr. Izhod: /tmp/p162/forensic/<name>.json
// Uporaba: node scripts/tmp/p162_forensic.mjs           (vse)
//          node scripts/tmp/p162_forensic.mjs griblje   (filter po imenu)
// NASVET (P158): FOREGROUND, sekvenčno!
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
import path from 'path';

const CROPS = '/tmp/p162/crops';
const OUT_DIR = '/tmp/p162/forensic';
fs.mkdirSync(OUT_DIR, { recursive: true });

const STRIP_PROMPT = (name, meta) => `To je VERTIKALNI IZREZ (trak) ENA VRSTICA iz MRLIŠKE matične knjige župnije Podzemelj, leto 1896, slovenska Kurrent pisava. Izrez: ${name} (sken s${meta.scan}, vrsta ${meta.vrsta}).

Stolpci (levo → desno): zaporedna št. | mesec + dan smrti | dan pokopa | vas | hišna št. | ime, priimek in stan mrličev | vere/spola kljukice | starost | bolezen ali vzrok smrti | previden | podpis duhovnika | opomba.

PRAVILA:
- Prepiši TO ENO vrstico z maksimalno natančnostjo. Negotovo z [~], neberljivo z [?].
- KURRENT CIFRE: 4 = γ-forma z zanko; 7 = γ-forma s prečko; 1 = ozka črtica; 9 = zaprta zanka gor + rep; pozor 3/5/8 zmeda.
- Hišna številka je v ozkem stolpcu takoj za vasjo.
- Starost = številka + enota (let/leto/leta, mesecev/meseca, dni, tednov, uri).
- Če je na izrezu vidna VELIKA PODČRTANA LETNICA (npr. 1896. ali 1897.), to zapiši v polje "marker".
- Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${name}", "zaporedna": "...", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "previden": "...", "duhovnik": "...", "marker": null, "opomba": "..."}`;

const CELL_PROMPT = (name, meta) => `To je IZREZ CELICE "Starost" iz MRLIŠKE matične knjige župnije Podzemelj (leto 1896, Kurrent pisava). Izrez: ${name} (sken s${meta.scan}, vrsta ${meta.vrsta}).

Preberi številko in enoto (let/leto/leta, mesecev, dni, tednov, uri). KURRENT CIFRE: 4 = γ-forma (odprt zgornji del, zanka/spodnji preklop); 9 = ZAPRTA okrogla zanka zgoraj + spustni rep; 7 = γ-forma s prečko; 2 = zvitek z osnovo.
Opiši obliko vsake številke (ima zaprto zanko ali odprt γ?).
Izhod: SAMO en veljaven JSON:
{"izrez": "${name}", "starost": "...", "oblika": "oplika cifrah", "gotovost": "visoka/srednja/nizka"}`;

const COMPARE_PROMPT = `Slika vsebuje TRI panele (ločena z belimi vertikalnimi pasovi) iz iste MRLIŠKE knjige (Kurrent pisava):
- Panel 1 (levi): sporna starost — ali je to "42" ali "92"?
- Panel 2 (srednji): REFERENCA — znano "95 let" (prva cifra = 9)
- Panel 3 (desni): REFERENCA — znano "4 leta" (cifra = 4)

Primerjaj oblike cifr: Kurrent "9" ima ZAPRTA okrogla zanka zgoraj + spustni rep; Kurrent "4" je γ-forma (odprta zgoraj, prekrižana/spodnja zanka).
Izhod: SAMO en veljaven JSON:
{"panel1": "kaj piše + zakaj", "panel2": "opis 9", "panel3": "opis 4", "sklep": "panel 1 je 42 ali 92 in zakaj", "gotovost": "visoka/srednja/nizka"}`;

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function read(zai, img, prompt) {
  const b64 = fs.readFileSync(img).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: prompt },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  let completion;
  for (let attempt = 1; attempt <= 4; attempt++) {
    completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))
    ]).catch(e => {
      if (attempt < 4) {
        console.log(`  poskus ${attempt}/4 napak (${e.message})`);
        return new Promise(res => setTimeout(() => res(null), attempt * 10000));
      }
      throw e;
    });
    if (completion) break;
  }
  if (!completion) throw new Error('vsi poskusi izčrpani');
  return parseContent(completion.choices[0].message.content);
}

async function main() {
  const filter = process.argv[2] || '';
  const man = JSON.parse(fs.readFileSync(path.join(CROPS, 'manifest.json'), 'utf8'));
  const jobs = [];
  for (const s of man.strips) jobs.push({ kind: 'strip', name: s.name, meta: s });
  for (const c of man.cells) jobs.push({ kind: 'cell', name: c.name, meta: c });
  const filtered = jobs.filter(j => j.name.includes(filter));
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const j of filtered) {
    const out = path.join(OUT_DIR, `${j.name}.json`);
    if (fs.existsSync(out)) { console.log(`${j.name}: že obstaja`); ok++; continue; }
    try {
      const prompt = j.kind === 'strip'
        ? STRIP_PROMPT(j.name, j.meta) : CELL_PROMPT(j.name, j.meta);
      const r = await read(zai, j.meta.file, prompt);
      fs.writeFileSync(out, JSON.stringify({ ...j.meta, read: r }, null, 1));
      const rr = r.starost || r.vas || '';
      console.log(`${j.name}: OK (starost/vas: ${String(rr).slice(0, 30)})`);
      ok++;
    } catch (e) {
      console.log(`${j.name}: FAIL ${e.message}`);
      fail++;
    }
  }
  // primerjalna slika cifr
  if ('primerjava-cifer'.includes(filter) || !filter) {
    const outC = path.join(OUT_DIR, 'primerjava-cifer.json');
    if (!fs.existsSync(outC)) {
      try {
        const r = await read(zai, path.join(CROPS, 'primerjava-cifer.png'), COMPARE_PROMPT);
        fs.writeFileSync(outC, JSON.stringify(r, null, 1));
        console.log(`primerjava-cifer: OK (sklep: ${String(r.sklep).slice(0, 60)})`);
        ok++;
      } catch (e) {
        console.log(`primerjava-cifer: FAIL ${e.message}`);
        fail++;
      }
    } else { console.log('primerjava-cifer: že obstaja'); ok++; }
  }
  console.log(`SKUPAJ: ${ok} OK / ${fail} FAIL`);
}

main().catch(e => { console.error(e); process.exit(1); });
