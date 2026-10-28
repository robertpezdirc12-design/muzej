// P154 — VLM branje forenzičnih izrezov mrliške 04894 (leto 1888).
// Metoda P153: neodvisni VLM prehodi, glm-5v-turbo, [~] negotovo;
// Kurrent cifre TOČNO kot napisane. Izhod: /tmp/p154/vlm-fx/<crop>.json
// Uporaba: node scripts/tmp/p154_read.mjs           (vsi izrezi)
//          node scripts/tmp/p154_read.mjs s14       (filter)
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
import path from 'path';

const IN_DIR = '/tmp/p154/fx';
const OUT_DIR = '/tmp/p154/vlm-fx';
fs.mkdirSync(OUT_DIR, { recursive: true });

function promptFor(name) {
  const half = name.endsWith('L.png') ? 'LEVI' : 'DESNI';
  return `To je ${half} izrez ENIH-DOIH vrstic iz MRLIŠKE matične knjige župnije Podzemelj (leto 1888), slovenska Kurrent pisava (nemški gotski vpliv).

${half} izrez vsebuje stolpce:
${half === 'LEVI' ? `1. Zaporedna številka vrstice (ročno; letno restartirana)
2. Mesec in dan smrti ter dan pokopa (meseci ročno: Januarj, Februar, Marcej, April, Maj, Junij, Julij, Avgust, September, Oktober, November, December)
3. Bivališče mrličevo: vas (npr. Griblje, Krasinec, Dobravice, Primostek, Gradac, Podžemelj, Hrnelj, Certoviše, Malše, Boršt, Klošter, Otak, Giriče, Vranoviče, Begunja vas, Boginja vas, Ohljuka, Prilozje, Krivoglavce) + hišna številka (poseben ozek stolpec — POZOR: Kurrent 3/5/8 zmeda!)
4. Ime, priimek in stan mrličev (stan = ½/¼ zemlj., gospoštvo, kmetlja, bajtar, holar, kolar, gemž., deklina, sin, hči, vdova, žena, fant ...)` : `1. Vere: katoliška/nekatoliška (kljukice »1«)
2. Spola: moškega/ženskega (kljukice »1«)
3. Starost (številka + enota: let/leto/leta, mesecev, dni, tednov, uri/ure, minuti)
4. Bolezen ali vzrok smrti (npr. Sušica, Nadluka, Plučnica, Vodernica, Slabost, Božjast, Davica, Krast, Marbmil, Gliste, Disenteria, Griža, Mertvod, Kolera, Karast ...)
5. Previden (a) ali ne (»previden« = prejEL zakramente?)
6. Podpis duhovnika pokopovalca (npr. Ant. Glibe coop., Jos. Romey, Andrej Glibel/Glibo/Gliebe, franz Dovgan)
7. Opomba (navadno prazna)`}

PRAVILA:
- Prepiši TOČNO kot napisano — ne popravljaš, ne ugibaš običajnih oblik. Negotovo z [~], neberljivo z [?].
- POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko; 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki; hišna številka 88 = dve visoki zanki!
- Vrstice ločene s horizontalnimi črtami — indeksiraš od zgoraj (1 = prva vidna).
- Če je izrez del vrstice, prepiši le vidno.
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez markdown):
{"vrstice": [{"row": 1, "zaporedna": "6", "mesec": "Februar", "smrt": "3.", "pokop": "5.", "vas": "Griblje", "hisna": "72", "ime": "Barbara Straus", "stan": "½ zemlj. žena", "starost": "22 let", "bolezen": "...", "previden": "1", "duhovnik": "...", "opomba": null}], "marker": "opis ali null", "opomba": "..."}`;
}

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readStrip(zai, img, name) {
  const b64 = fs.readFileSync(img).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(name) },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  let completion;
  for (let attempt = 1; attempt <= 6; attempt++) {
    completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))
    ]).catch(e => {
      if (String(e.message).includes('429') && attempt < 6) {
        console.log(`  ${name}: 429, poskus ${attempt}/6 — čakam ${attempt * 20}s`);
        return new Promise(res => setTimeout(() => res(null), attempt * 20000));
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
  const files = fs.readdirSync(IN_DIR).filter(f => f.endsWith('.png') && f.includes(filter)).sort();
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const f of files) {
    const out = path.join(OUT_DIR, f.replace('.png', '.json'));
    if (fs.existsSync(out)) { console.log(`${f}: že obstaja`); ok++; continue; }
    try {
      const r = await readStrip(zai, path.join(IN_DIR, f), f);
      fs.writeFileSync(out, JSON.stringify({ crop: f, ...r }, null, 1));
      console.log(`${f}: OK (${(r.vrstice || []).length} vrstic)`);
      ok++;
    } catch (e) {
      console.log(`${f}: FAIL ${e.message}`);
      fail++;
    }
  }
  console.log(`SKUPAJ: ${ok} OK / ${fail} FAIL`);
}

main().catch(e => { console.error(e); process.exit(1); });
