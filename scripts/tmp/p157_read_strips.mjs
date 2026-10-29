// P157 — VLM branje L/R trakov Griblje-vrstic 1891 (metoda P153/P155).
// Neodvisni prehodi, glm-5v-turbo, [~] negotovo; Kurrent TOČNO kot napisano.
// Izhod: /tmp/p157/vlm-strips/<name>.json
// Uporaba: node scripts/tmp/p157_read_strips.mjs            (vsi)
//          node scripts/tmp/p157_read_strips.mjs s31-33     (filter)
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
import path from 'path';

const IN_DIR = '/tmp/p157/strips';
const OUT_DIR = '/tmp/p157/vlm-strips';
fs.mkdirSync(OUT_DIR, { recursive: true });

function promptFor(name) {
  const half = name.endsWith('L.png') ? 'LEVI' : 'DESNI';
  const year = name.startsWith('s28') ? '1891 (leto se je začelo — velik podčrtan marker »1891«)' :
               name.startsWith('s34') ? '1892 (leto se je začelo — velika glava »1892«)' : '1891';
  return `To je ${half} izrez ENIH-DOIH vrstic iz MRLIŠKE matične knjige župnije Podzemelj (leto ${year}), slovenska Kurrent pisava (nemški gotski vpliv).

${half} izrez vsebuje stolpce:
${half === 'LEVI' ? `1. Zaporedna številka vrstice (ročno, levo ob robu)
2. Mesec in dan smrti ter dan pokopa (dva stolpca; meseci ročno: Januarj, Februar, Marcej, April, Maj, Junij, Julij, Avgust, September, Oktober, November, December)
3. Bivališče mrličevo: vas (npr. Griblje, Krasinec, Dobravice, Primostek, Gradac, Podžemelj, Hrnelj, Certoviše, Malše, Boršt, Klošter, Otok, Giriče, Vranoviče, Prilozje, Boginja vas, Zemelj) + hišna številka (poseben ozek stolpec — POZOR: Kurrent 3/5/8 zmeda, 1/4 zmeda!)
4. Ime, priimek in stan mrličev (stan = ½/⅓/¼ zemljak, kmetlja, bajtar, kolar, gemžga, dekla, sin, hči, vdova, žena, fant, gostilnar ...)` : `1. Vere: katoliška/nekatoliška (kljukice »1«)
2. Spola: moškega/ženskega (kljukice »1«; včasih besedno »moškega spola« / »ženskega spola«)
3. Starost (številka + enota: let/leto/leta, mesecev, dni, tednov, uri/ure, minuti)
4. Bolezen ali vzrok smrti (npr. Sušica, Nadluka, Pljučnica, Vodenica, Slabost, Božjast, Davica, Krastelj, Marbmil, Gliste, Griža, Jetika, Mertvod, Nadruha, Bele/Bule, Habost, Hojlica, Šarost ...)
5. Previden (a) ali ne (»previden« = prejEL zakramente; včasih izpisano »sv. olje«)
6. Podpis duhovnika pokopovalca (npr. Jos. Ramej/Rauq, Jos. Rup, Nikolaj Belavič kaplan, Jos. Čuček župnik, Ivan Šašelj župnik Adlešiči, p. Matija Novak kaplan, Jos. Češarek coadj./coop.)
7. Opomba (navadno prazna) — OPRAVIČIJO: rdeče kredne oznake so kasnejši arhivski pripisi, jih zabeleži ločeno!`}

PRAVILA:
- Prepiši TOČNO kot napisano — ne popravljaš, ne ugibaš običajnih oblik. Negotovo branje označi z [~] (za vrednostjo), neberljivo z [?].
- POZOR NA KURRENT CIFRE: številka 4 ima zanko; 1 je ozka črtica; 7 ima prečko; 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki.
- Vrstice so ločene s horizontalnimi črtami — vsako vrstico pripiši njenemu indeksu od zgoraj (1 = prva vidna vrstica v izrezu).
- Če je v izrezu ročno letnica-glava (»Leto 18 ..«), velik ciferni marker (npr. podčrtan »1891«) ali mesečni prelom (»Januarj«), to posebej zapiši v "marker".
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez markdown):
{"vrstice": [{"row": 1, "zaporedna": "13.", "mesec": "Marcej", "smrt": "6.", "pokop": "8.", "vas": "Griblje", "hisna": "61", "ime": "Katarina Novak", "stan": "vdova, kolarica", "starost": "95 let", "bolezen": "Slabost", "previden": "1", "duhovnik": "Jos. Rauq", "opomba": null}], "marker": "opis ali null", "rdece-oznake": "opis ali null", "opomba": "..."}`;
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
  for (let attempt = 1; attempt <= 5; attempt++) {
    completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 240s')), 240000))
    ]).catch(e => {
      if (attempt < 5) {
        console.log(`  ${name}: poskus ${attempt}/5 napak (${e.message}) — čakam ${attempt * 15}s`);
        return new Promise(res => setTimeout(() => res(null), attempt * 15000));
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
    if (fs.existsSync(out)) { ok++; continue; }
    try {
      const r = await readStrip(zai, path.join(IN_DIR, f), f);
      fs.writeFileSync(out, JSON.stringify(r, null, 1));
      const n = (r.vrstice || []).length;
      console.log(`${f}: OK (${n} vrstic)`);
      ok++;
    } catch (e) {
      console.log(`${f}: FAIL ${e.message}`);
      fail++;
    }
  }
  console.log(`SKUPAJ: ${ok} OK / ${fail} FAIL`);
}

main().catch(e => { console.error(e); process.exit(1); });
