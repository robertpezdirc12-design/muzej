// P234 — celostansko branje skenov KRSTNE PREDZGODOVINE 04104 (14/15, leto 1872!).
// PROBE: glave s19–s25-'Jahr 1872' (7/7!) + s26–s28-'Jahr 1873' (3/3!) → MEJA-1872/73 = s25/s26!
//   + foliacija-'sken−3'-SEKVENČNO-s19–s28 = 16–25 (10/10-visoko!-BREZ-duplikatov!)
//   + s19-r1-'zap-1-Jänner-3-Gradac-Maria' (★★★ RESTART-z1-1872-NA-s19!-MEJA-1871/72-PRED-s19!).
// ISKAMO: leto 1872 (s19–s25!-Jänner–November–Dezember!), TAIL-1872 (Dezember!), GLAVE-'Jahr 1872',
//   + s26/s27-1873-z1–z10-KONTEKST (P233-model: z1–z10-PRED-s28!-NA-s26/s27!-ARITMETIČNO!).
// ★★★ POZOR: Q3-probe-zap-branja-so-LAHKO-MISREADI (1,5,14,13,6,9,17-neskladno!-KURRENT-1/2-zmeda!)
//   — MESECI-so-kronološki (J→Juli→Aug→Sep→Okt→Nov!) — zap-RAZREŠI-s-kontekstom!
// Izhod: /tmp/p234/vlm-page/sNN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p234";
const OUT_DIR = "/tmp/p234/vlm-page";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2).map(s => 's' + parseInt(s.slice(1), 10));
const SCANS = fs.readdirSync(IN_DIR).filter(f => /^s\d+\.jpg$/.test(f))
  .map(f => f.replace('.jpg', '')).sort((a, b) => parseInt(a.slice(1)) - parseInt(b.slice(1)))
  .filter(s => FILTER.length === 0 || FILTER.includes(s));

function promptFor(scan) {
  return `To je CELLOTEN sken strani KRSTNE matične knjige župnije Podzemelj (obdobje 1871–1885 — STAREJŠI zvezek, STAREJŠA pisava!), slovenska Kurrent pisava (nemški gotski vpliv). Sken = ${scan}.
KONTEKST: to je STAREJŠI zvezek krstne knjige. Iskamo leto 1872 = 14/15-predzgodovinska-linija — tukaj je lahko ZAČETEK leta 1872 (RESTART-zaporedne-številke-na-1!-Jänner!-glava-'Jahr 1872'!), leto 1872 (Jänner–Dezember!), ZAKLJUČEK leta 1872 (tail-Dezember + 'finis-Anni-1872'-kalligrafija-LAHKO!), ALI že začetek leta 1873 (glava-'Jahr 1873'!-restart-z1!-Jänner-1873!).
ZNANO-IZ-P234-PROBE: glave — s19–s25-VSE-'Jahr 1872' (7/7!), s26–s28-'Jahr 1873' (3/3!-s28-P233-potrjen!); foliacija-'sken−3'-SEKVENČNO: s19='16'-s20='17'-s21='18'-s22='19'-s23='20'-s24='21'-s25='22'-s26='23'-s27='24'-s28='25' (10/10-BREZ-duplikatov!); prve-vrstice-probe (ZAP-BRANJA-SO-LAHKO-MISREADI-KURRENT-1/2-ZMEDA!-MESECI-KRONOLOŠKI!): s19-r1-'zap-1?-Jänner-3-Gradac-1-Maria'-s20-r1-'zap-5?-Juli-12-Kapljišče'-s21-r1-'zap-14?-August-14-Gradac'-s22-r1-'zap-13?-September-17-Cerovišče'-s23-r1-'zap-6?-October-13-Primostek'-s24-r1-'zap-9?-November-12-Cerovišče'-s25-r1-'zap-17?-November-20'-s26-r1-'zap-3?-Jänner-3-Gradac-3-Anna'-s27-r1-'zap-2?-Jänner-2'-s28-r1-'zap-11-März-3-Podzemelj-Mathildis' (P233-potrjen!).
★★★ FOLIACIJA: v zgornjem-levem-kotu je gola-svinčna-cifra (arhivarjeva-foliacija, vzorec-'sken−3'). Preberi in zapiši cifro — če je neberljiva, napiši null.

Struktura tabele (stolpci, levo → desno; LAHKO se razlikuje — starejša forma! opisuj TOČNO kaj vidiš):
1. Zaporedna številka vrstice (ročno; vsako leto se restarta na 1!)
2. Mesec in dan rojstva ter dan krsta (meseci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember)
3. Bivališče: vas (npr. Griblje, Krasinec, Dobravice/Dobravce, Primostek, Gradac, Podžemelj/Podzemelj, Certoviše/Cerovišče, Malše, Boršt, Klošter, Otok, Giriče/Geriče, Vranoviče, Begunja vas, Boginja vas, Ohljuka, Prilozje, Krivoglavce, Zemelj, Grem, Dragoše, Gorice, Maršiči, Paunoviče, Dolga vas, Kaplišče/Kapljišče, Lemež) + hišna številka (poseben ozek stolpec — POZOR: Kurrent 3/5/8 zmeda, 7 = γ-forma s prečko!)
4. Ime otroka
5. Spola (moški/ženski kljukice »1«) + zakoniti/nezakoniti (včasih ločeni stolpci!)
6. Ime in priimek očeta (+ stan/gospodarska enota: npr. ¼/½/¾/1 Ganzl, Gütl, zemljiščni kmeti)
7. Ime in priimek (roj. dekliško) matere
8. Botra/botri (ime + priimek + stan — pogosto 2 osebi!)
9. Podpis duhovnika krstilnika (Kurrent-ligatura 'Prieſter' — dolgi ſ + in!; v-1873-so-bili-'Dovgan'-'Pihlár'-'Roblek-Kaplan'-'Bobleh-Kaplan'-'Dolenc'-garble!-1872-LAHKO-drugi!)
10. Opomba (npr. poznejši pripisi o poroki/smrti — MODRI/ČRNILO-†-pripisi!)

PRAVILA:
- Prepiši VSAKO vrstico tabele (od zgoraj navzdol) s čim več natančnostjo. Negotovo z [~], neberljivo z [?].
- ZAPOREDNA ŠTEVILKA: beri IZ KLJUČNEGA STOLPCA najbolj LEVO! Ne zaznamuj številk iz starostnega ali hišnega stolpca! POZOR: KURRENT-1/2-zmeda ('1'-s-serifom-≈-'2'!) — če-zap-NI-jasno, napiši best-guess-z-[~]!
- POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko (γ-forma!); 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki; 3 je zrcalna-E; 3/5/8 zmeda.
- Še posebej NATAČNO pri VASI: poišči VSE vrstice, kjer je vas »Griblje« (ali varianta Griblj/Grible/Griable/Grihle/Grile) — to so ključne!
- Posebej zapiši VSE MARKERJE: letnica-glava »Jahr 18 ..«, velike črte/veliki cifri čez vrsto, VSOTNA-vrsta, 'finis-Anni'-kalligrafija, 'Initium-anni-Domini'-kalligrafija, mesečni prelomi, prazne vrste, RESTART zaporedne številke na 1, PREČRTANE vrstice, svinčna-foliacija!
- Če stran vsebuje ZAČETEK leta 1872 (restart-številčenja-na-1 ALBO prva-Jänner-vrstica-1872 + glava-'Jahr 1872'), to jasno označi z MEJA.
- Če stran vsebuje ZAKLJUČEK leta 1872 (tail-Dezember-vrstice + 'finis-Anni-1872'-kalligrafija-LAHKO!), to jasno označi z TAIL.
- Če stran vsebuje ZAČETEK leta 1873 (restart-na-1 + glava-'Jahr 1873' + Jänner-1873), to jasno označi z MEJA-1873 (kontekst-za-P233!).
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
