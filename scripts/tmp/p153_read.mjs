// P153 — VLM branje izrezov mrliške knjige 04894 (leto 1887).
// Metoda P57/P59: neodvisni VLM prehodi na izrez, glm-5v-turbo, [~] negotovo;
// Kurrent številke TOČNO kot napisane. Izhod: /tmp/p153/vlm/<crop>.json
// Uporaba: node scripts/tmp/p153_read.mjs            (vsi izrezi)
//          node scripts/tmp/p153_read.mjs s06-r10    (filter)
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
import path from 'path';

const IN_DIR = process.env.VLM_DIR || '/tmp/p153/rows';
const OUT_DIR = '/tmp/p153/vlm';
fs.mkdirSync(OUT_DIR, { recursive: true });

function promptFor(name) {
  const half = name.endsWith('L.png') ? 'LEVI' : 'DESNI';
  return `To je ${half} izrez ENIH-DOIH vrstic iz MRLIŠKE matične knjige župnije Podzemelj (leto 1887/1888), slovenska Kurrent pisava (nemški gotski vpliv).

${half} izrez vsebuje stolpce:
${half === 'LEVI' ? `1. Zaporedna številka vrstice (ročno, levo ob robu)
2. Mesec in dan smrti ter dan pokopa (dva stolpca; meseci napisani ročno: Januarj, Februar, Marzec, April, Maj, Junij, Julij, Avgust, September, Oktober, November, December)
3. Bivališče mrličevo: mesto/trg/vas (npr. Griblje, Krasinec, Dobravce, Primostek, Gradac, Podzemelj, Hrnelj, Certoviše, Malše, Gornje, Boršt, Klošter, Otak, Giriče, Vranoviče, Gern, Dragoše, Boginja vas, Ohljuka) + hišna številka (poseben ozek stolpec)
4. Ime, priimek in stan mrličev (npr. »Marija Šimec, ½ Hobarjeva žena« — stan = ½/¼ zemljak, kmetlja, bajtar, holar/kolar, gemžgah, deklina, sin, hči, vdova, žena, fant ...)` : `1. Vere: katoliška/nekatoliška (kljukice »1«)
2. Spola: moškega/ženskega (kljukice »1«)
3. Starost (številka + enota: let/leto/leta, mesecev, dni, tednov, uri/ure, minuti)
4. Bolezen ali vzrok smrti (npr. Sušica = jetika/tuberkuloza, Nadluka = davica/difterija, Plunica = pljučnica?, Vodenica = vodenica/edem, Uspavice = krčavice?, Slabost, Božjast/Božjask = krči, Davica, Krastelj/Krastelj, Marbmil = marazem?, Gliste, Irija ...)
5. Previden (a) ali ne (»previden« = prejEL zakramente?)
6. Podpis duhovna pokopovalca (npr. franz Dovgan, Andrej Glibel/Glibo/Gliebe, Jos Romej, Ant. Glibe coop.)
7. Opomba (navadno prazna)`}

PRAVILA:
- Prepiši TOČNO kot napisano — ne popravljaš, ne ugibaš običajnih oblik. Negotovo branje označi z [~] (za vrednostjo), neberljivo z [?].
- POZOR NA KURRENT CIFRE: številka 4 ima zanko; 1 je ozka črtica; 7 ima prečko; 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki.
- Vrstice so ločene s horizontalnimi črtami — vsako vrstico pripiši njenemu indeksu od zgoraj (1 = prva vidna vrstica v izrezu).
- Če izrez vsebuje le del vrstice, prepiši le vidno.
- Če je v izrezu ročno letnica-glava (»Leto 18..«) ali velik ciferni marker (npr. »1888« čez vrstico) ali mesečni prelom (»Januarj«), to posebej zapiši v "marker".
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez markdown):
{"vrstice": [{"row": 1, "zaporedna": "1", "mesec": "Januarj", "smrt": "1.", "pokop": "3.", "vas": "Griblje", "hisna": "44", "ime": "Matija Šproch", "stan": "½ zemlj.", "starost": "48 let", "bolezen": "Nadluka", "previden": "1", "duhovnik": "franz Dovgan", "opomba": null}], "marker": "opis ali null", "opomba": "..."}`;
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
  const call = zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(name) },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  const completion = await Promise.race([
    call,
    new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))
  ]);
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
