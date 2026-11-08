// P194 — celostansko branje skenov MRLIŠKE PREDZGODOVINE 04106 (leto 1883 = 3/29!).
// Strategija: s187–s192 (celo leto 1883 + tail-z69–z75-na-s192-že-P193!); pag == sken − 6.
// Izhod: /tmp/p194/vlm-page/sNN.json
// Uporaba: node scripts/tmp/p194_read_page.mjs            (vsi preneseni)
//          node scripts/tmp/p194_read_page.mjs s200 s202  (filter)
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
import path from 'path';

const IN_DIR = '/tmp/p194';
const OUT_DIR = '/tmp/p194/vlm-page';
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2);
const SCANS = fs.readdirSync(IN_DIR).filter(f => /^s\d+\.jpg$/.test(f))
  .map(f => f.replace('.jpg', '')).sort((a, b) => parseInt(a.slice(1)) - parseInt(b.slice(1)))
  .filter(s => FILTER.length === 0 || FILTER.includes(s));

function promptFor(scan) {
  return `To je CELLOTEN sken strani MRLIŠKE matične knjige župnije Podzemelj (obdobje 1857–1885 — STAREJŠA pisava!), slovenska Kurrent pisava (nemški gotski vpliv). Sken = ${scan}.

Struktura tabele (stolpci, levo → desno; LAHKO se razlikuje od mlajših knjig!):
1. Zaporedna številka vrstice (ročno; vsako leto se restarta na 1!)
2. Mesec in dan smrti ter dan pokopa (meseci ročno: Januar, Februar, March, April, Mai, Juni, Juli, August, September, Oktober, November, December)
3. Bivališče mrličevo: vas (npr. Griblje, Krasinec, Dobravice, Primostek, Gradac, Podžemelj/Podzemelj, Hrast/Hrnelj, Certoviše, Malše, Boršt, Klošter, Otok, Giriče, Vranoviče, Begunja vas, Boginja vas, Ohljuka, Prilozje, Krivoglavce, Zemelj, Grem) + hišna številka (poseben ozek stolpec — POZOR: Kurrent 3/5/8 zmeda, 7 = γ-forma s prečko!)
4. Ime, priimek in stan mrličev
5. Vere (kat./nekat.) + spola (moš./žens.) — kljukice »1«
6. Starost (številka + enota: let/leto/leta, mesecev, dni, tednov, uri/ure, minuti)
7. Bolezen ali vzrok smrti (npr. Sušica, Nadluka, Pljučnica, Vodenica, Slabost, Božjast, Davica, Krastelj, Marbmil/Marmil, Gliste, Griža, Jetika, Mertvod, Nadruha, Habost, Bele, Merlica/Mrzlica ...)
8. Previden ali ne (»previden« = prejel zakramente; včasih izpisano »sv. olje«)
9. Podpis duhovnika pokopovalca
10. Opomba

PRAVILA:
- Prepiši VSAKO vrstico tabele (od zgoraj navzdol) s čim več natančnosti. Negotovo z [~], neberljivo z [?].
- POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko (γ-forma!); 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki.
- Še posebej NATAČNO pri VASI: poišči VSE vrstice, kjer je vas »Griblje« (ali varianta Griblj/Grible) — to so ključne!
- Posebej zapiši VSE MARKERJE: letnica-glava »Leto 18 ..« (ali PRAZNA glava!), veliki cifri čez vrsto (npr. »— 1885. —«), mesečni prelomi (»Januar 1885«), prazne vrste, nove številčne kolumne (restart zaporedne številke na 1!).
- Če stran vsebuje ZAČETEK novega leta (restart številčenja ali letnica-glava), to jasno označi z MEJA.
- Če je stran PRAZNA ali vsebuje samo okras/vezni list, to zapiši.
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez markdown):
{"skan": "${scan}", "struktura": "opis (glave, št. vrstic, posebnosti)", "leto": "najbolj verjetna letnica ali null", "meja": "opis ali null", "vrstice": [{"vrsta": 1, "zaporedna": "1", "mesec": "Februar", "smrt": "5.", "pokop": "7.", "vas": "Griblje", "hisna": "12", "ime": "...", "stan": "...", "starost": "60 let", "bolezen": "Sušica", "previden": "1", "duhovnik": "...", "opomba": null}], "markerji": ["opis ali ..."], "opomba": "..."}`;
}

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readPage(zai, img, scan) {
  const b64 = fs.readFileSync(img).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(scan) },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  let completion;
  for (let attempt = 1; attempt <= 5; attempt++) {
    completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 240000))
    ]);
    try {
      const c = completion?.choices?.[0]?.message?.content;
      if (!c) throw new Error('prazna vsebina');
      return parseContent(c);
    } catch (e) {
      console.error(`  ${scan}: poskus ${attempt} ni OK (${e.message})`);
      if (attempt === 5) throw e;
      await new Promise(r => setTimeout(r, 3000 * attempt));
    }
  }
}

async function main() {
  const zai = await import('z-ai-web-dev-sdk').then(m => m.default || m).catch(() => null)
    || await import('file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js').then(m => m.default || m);
  const inst = await (zai.create ? zai.create() : zai.default?.create?.() || zai.create());
  for (const scan of SCANS) {
    const out = `${OUT_DIR}/${scan}.json`;
    if (fs.existsSync(out)) { console.log(`${scan}: ŽE`); continue; }
    try {
      const res = await readPage(inst, `${IN_DIR}/${scan}.jpg`, scan);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      const n = res.vrstice?.length ?? 0;
      console.log(`${scan}: OK vrstice=${n} leto=${res.leto} meja=${res.meja ? 'DA' : '-'}`);
    } catch (e) {
      console.error(`${scan}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
