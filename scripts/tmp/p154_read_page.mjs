// P154 — celostansko branje skenov mrliške 04894 (leto 1888).
// Neodvisni VLM prehod na celoten sken, glm-5v-turbo, [~] negotovo.
// Izhod: /tmp/p154/vlm-page/sNN.json
// Uporaba: node scripts/tmp/p154_read_page.mjs            (vsi skeni)
//          node scripts/tmp/p154_read_page.mjs s14        (filter)
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
import path from 'path';

const IN_DIR = '/tmp/p154';
const OUT_DIR = '/tmp/p154/vlm-page';
fs.mkdirSync(OUT_DIR, { recursive: true });

const SCANS = ['s13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21', 's22'];

function promptFor(scan) {
  return `To je CELLOTEN sken strani MRLIŠKE matične knjige župnije Podzemelj (leto 1888/1889), slovenska Kurrent pisava (nemški gotski vpliv). Sken = ${scan}.

Struktura tabele (stolpci, levo → desno):
1. Zaporedna številka vrstice (ročno; vsako leto se restarta na 1!)
2. Mesec in dan smrti ter dan pokopa (meseci ročno: Januarj, Februar, Marzec, April, Maj, Junij, Julij, Avgust, September, Oktober, November, December)
3. Bivališče mrličevo: vas (npr. Griblje, Krasinec, Dobravce/Dobravice, Primostek, Gradac, Podzemelj, Hrnelj, Certoviše/Certovše, Malše, Gornje, Boršt, Klošter, Otak, Giriče, Vranoviče, Gern, Dragoše, Boginja vas, Ohljuka) + hišna številka (poseben ozek stolpec)
4. Ime, priimek in stan mrličev
5. Vere (kat./nekat.) + spola (moš./žens.) — kljukice »1«
6. Starost (številka + enota: let/leto/leta, mesecev, dni, tednov, uri/ure, minuti)
7. Bolezen ali vzrok smrti (npr. Sušica, Nadluka, Plunica, Vodenica, Uspavice, Slabost, Božjast, Davica, Krastelj, Marbmil, Gliste, Irija, Plučni mrah, Griža, Jetika, Mertvod ...)
8. Previden ali ne (»previden« = prejEL zakramente)
9. Podpis duhovnika pokopovalca (npr. franz Dovgan, Andrej Glibel/Glibo/Gliebe, Ant. Glibe coop., Jos. Romej ...)
10. Opomba

PRAVILA:
- Prepiši VSAKO vrstico tabele (od zgoraj navzdol) s čim več natančnosti. Negotovo z [~], neberljivo z [?].
- POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko; 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki.
- Še posebej NATAČNO pri VASI: poišči VSE vrstice, kjer je vas »Griblje« (ali varianta Griblj/Grible) — to so ključne!
- Posebej zapiši VSE MARKERJE: letnica-glava »Leto 18 ..« (ali PRAZNA glava!), veliki cifri čez vrsto (npr. »1 8 8 9«), mesečni prelomi (»Januarj 1889«), prazne vrste, nove številčne kolumny (restart zaporedne številke na 1!).
- Če stran vsebuje ZAČETEK novega leta (restart številčenja ali letnica 1889), to jasno označi.
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez markdown):
{"skan": "${scan}", "struktura": "opis (glave, št. vrstic, posebnosti)", "vrstice": [{"vrsta": 1, "zaporedna": "1", "mesec": "Februar", "smrt": "5.", "pokop": "7.", "vas": "Griblje", "hisna": "12", "ime": "...", "stan": "...", "spol": "žensko", "starost": "60 let", "bolezen": "Sušica", "previden": "1", "duhovnik": "...", "opomba": null}], "markerji": ["opis ali ..."], "opomba": "..."}`;
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
  const call = zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(scan) },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  const completion = await Promise.race([
    call,
    new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 240s')), 240000))
  ]);
  return parseContent(completion.choices[0].message.content);
}

async function main() {
  const filter = process.argv[2] || '';
  const scans = SCANS.filter(s => s.includes(filter));
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const s of scans) {
    const out = path.join(OUT_DIR, `${s}.json`);
    if (fs.existsSync(out)) { console.log(`${s}: že obstaja`); ok++; continue; }
    try {
      const r = await readPage(zai, path.join(IN_DIR, `${s}.jpg`), s);
      fs.writeFileSync(out, JSON.stringify(r, null, 1));
      console.log(`${s}: OK (${(r.vrstice || []).length} vrstic; markerji: ${(r.markerji || []).length})`);
      ok++;
    } catch (e) {
      console.log(`${s}: FAIL ${e.message}`);
      fail++;
    }
  }
  console.log(`SKUPAJ: ${ok} OK / ${fail} FAIL`);
}

main().catch(e => { console.error(e); process.exit(1); });
