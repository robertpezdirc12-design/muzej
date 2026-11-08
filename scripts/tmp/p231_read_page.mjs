// P231 — celostansko branje skenov KRSTNE PREDZGODOVINE 04104 (11/15, leto 1875!).
// LEAD-P230: MEJA-1875/76 = s64/s65-DVO-STRANSKA (ŽE-POTRJENA!) — s64 = glava-'Jahr 1875'
//   + TAIL-×4-vrstic (r1-Dez-1/1-Krasine-h15! + r2-Dez-3/3-Zemelj-h17-MUC! + r3-Dez-26/26-GRIBLJE-h11-Anna!
//   + r4-Dez-18/19-RETRO-Gradac-h55!) + ★★★ 'finis-Anni-1875'-VELIKA-KALLIGRAFIJA-spodaj!
//   s65 = glava-'Jahr 1876' + RESTART-z1-5./5.-JÄNNER.
// ISKAMO: MEJA-1874/75 — PRED s64 → probe-s57–s64 (DESCENDING!).
//   Pričakovana gola-pag-'sken−5': s57='52' (s64='59'!-s58='53'!).
//   POZOR: 'finis-Anni'-kalligrafija-LAHKO-se-ponovi ('finis-Anni-1874' na meji!).
//   zap-stolpci-pričakovani-VIDNI (vs-100-1876!).
// Izhod: /tmp/p231/vlm-page/sNN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p231";
const OUT_DIR = "/tmp/p231/vlm-page";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2).map(s => 's' + parseInt(s.slice(1), 10));
const SCANS = fs.readdirSync(IN_DIR).filter(f => /^s\d+\.jpg$/.test(f))
  .map(f => f.replace('.jpg', '')).sort((a, b) => parseInt(a.slice(1)) - parseInt(b.slice(1)))
  .filter(s => FILTER.length === 0 || FILTER.includes(s));

function promptFor(scan) {
  return `To je CELLOTEN sken strani KRSTNE matične knjige župnije Podzemelj (obdobje 1871–1885 — STAREJŠI zvezek, STAREJŠA pisava!), slovenska Kurrent pisava (nemški gotski vpliv). Sken = ${scan}.
KONTEKST: to je STAREJŠI zvezek krstne knjige. Iskamo leto 1875 = 11/15-predzgodovinska-linija — zato so tukaj lahko ZAKLJUČEK leta 1874 (tail + VSOTNA/'finis-Anni-1874'-kalligrafija!), MEJA-1874/75 (glava-'Jahr 1875' + restart-številčenja!), leto 1875, ali TAIL-1875 (s64 = ŽE-POTRJEN-TAIL-1875: glava-'Jahr 1875' + 4-vrstice-December + velika-kalligrafija-'finis-Anni-1875'-na-dnu-strani!).
ZNANO-IZ-P230: s64 = 4-vrstice (r1-Dez-1/1-Krasine-h15! + r2-Dez-3/3-Zemelj-h17-oče-MUC! + r3-Dez-26/26-GRIBLJE-h11-Anna! + r4-Dez-18/19-RETRO-Gradac-h55!) + 'finis-Anni-1875'-KALLIGRAFIJA ('finis'-levo-sredina + 'An-ni-1-8-75'-desno!); s65 = glava-'Jahr 1876' + RESTART-zap-1-na-dan-5./5.-Jänner.
★★★ POZOR: velika-kalligrafija-'finis-Anni'-se-LAHKO-PONOVI — če stran ima 'finis-Anni-1874'-kalligrafijo ALBO glavo-'Jahr 1875', to je MEJA-1874/75 — to jasno OZNAČI z MEJA!
★★★ FOLIACIJA: v zgornjem-levem-kotu je gola-svinčna-cifra (arhivarjeva-foliacija, vzorec-'sken−5': s57='52'-pričakovano, s58='53', s64='59'-ŽE-POTRJENO!). Preberi in zapiši cifro — če je neberljiva, napiši null.

Struktura tabele (stolpci, levo → desno; LAHKO se razlikuje — starejša forma! opisuj TOČNO kaj vidiš):
1. Zaporedna številka vrstice (ročno; vsako leto se restarta na 1!)
2. Mesec in dan rojstva ter dan krsta (meseci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember)
3. Bivališče: vas (npr. Griblje, Krasinec, Dobravice/Dobravce, Primostek, Gradac, Podžemelj/Podzemelj, Hrast/Hrnelj, Certoviše, Malše, Boršt, Klošter, Otok, Giriče/Geriče, Vranoviče, Begunja vas, Boginja vas, Ohljuka, Prilozje, Krivoglavce, Zemelj, Grem, Dragoše, Gorice, Maršiči, Paunoviče, Dolga vas, Kaplišče, Lemež) + hišna številka (poseben ozek stolpec — POZOR: Kurrent 3/5/8 zmeda, 7 = γ-forma s prečko!)
4. Ime otroka
5. Spola (moški/ženski kljukice »1«) + zakoniti/nezakoniti (včasih ločeni stolpci!)
6. Ime in priimek očeta (+ stan/gospodarska enota: npr. ¼/½/¾/1 Ganzl, Gütl, zemljiščni kmeti)
7. Ime in priimek (roj. dekliško) matere
8. Botra/botri (ime + priimek + stan — pogosto 2 osebi!)
9. Podpis duhovnika krstilnika (Kurrent-ligatura 'Prieſter' — dolgi ſ + in!; v-1876-so-bili-podpisi-'Hoggia/Roggja/Hoggin-Coop'-in-'Franz-Dovgan'!)
10. Opomba (npr. poznejši pripisi o poroki/smrti — MODRI/ČRNILO-†-pripisi!)

PRAVILA:
- Prepiši VSAKO vrstico tabele (od zgoraj navzdol) s čim več natančnostjo. Negotovo z [~], neberljivo z [?].
- ZAPOREDNA ŠTEVILKA: beri IZ KLJUČNEGA STOLPCA najbolj LEVO! Ne zaznamuj številk iz starostnega ali hišnega stolpca!
- POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko (γ-forma!); 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki; 3/5/8 zmeda.
- Še posebej NATAČNO pri VASI: poišči VSE vrstice, kjer je vas »Griblje« (ali varianta Griblj/Grible/Griable) — to so ključne!
- Posebej zapiši VSE MARKERJE: letnica-glava »Jahr 18 ..« (ali PRAZNA glava!), velike črte/veliki cifri čez vrsto, VSOTNA-vrsta (lahko z RAZPETIMI CIFRAMI čez stolpce), 'finis-Anni'-kalligrafija (VELIKA-ČRKovana-čez-dno-strani!), mesečni prelomi, prazne vrste, restart zaporedne številke na 1, PREČRTANE vrstice, svinčna-foliacija-zgornji-levi-kot!
- Če stran vsebuje ZAČETEK leta 1875 (glava-'Jahr 1875' ALBO restart-številčenja ALBO 'finis-Anni-1874'-kalligrafija), to jasno označi z MEJA.
- Če stran vsebuje ZAKLJUČEK leta 1874 (tail-vrstice pred restartom/glavo-'Jahr 1875'), to jasno označi z TAIL.
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez markdown):
{"skan": "${scan}", "struktura": "opis (glave, št. vrstic, posebnosti, kalligrafija?)", "leto": "najbolj verjetna letnica ali null", "meja": "opis ali null", "tail": "opis ali null", "foliacija": "cifra ali null", "vrstice": [{"vrsta": 1, "zaporedna": "1", "mesec": "Jänner", "rojen": "5.", "krsten": "7.", "vas": "Griblje", "hisna": "12", "otrok": "...", "spol": "moški|ženski", "zakonit": "zakoniti|nezakoniti|null", "ocec": "...", "matec": "...", "botra": "...", "duhovnik": "...", "opomba": null}], "markerji": ["opis ali ..."], "opomba": "..."}`;
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
  const inst = await ZAI.create();
  let first = true;
  for (const scan of SCANS) {
    const out = `${OUT_DIR}/${scan}.json`;
    if (fs.existsSync(out)) { console.log(`${scan}: ŽE`); continue; }
    if (!first) await new Promise(r => setTimeout(r, 25000));
    first = false;
    try {
      const res = await readPage(inst, `${IN_DIR}/${scan}.jpg`, scan);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      const n = res.vrstice?.length ?? 0;
      console.log(`${scan}: OK vrstice=${n} leto=${res.leto} meja=${res.meja ? 'DA' : '-'} tail=${res.tail ? 'DA' : '-'} foliacija=${res.foliacija ?? '-'} struktura=${String(res.struktura || '').slice(0, 70)}`);
    } catch (e) {
      console.error(`${scan}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
