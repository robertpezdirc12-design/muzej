// P233 — celostansko branje skenov KRSTNE PREDZGODOVINE 04104 (13/15, leto 1873!).
// PROBE: VSE-glave-s28–s36-'Jahr 1873' (9/9!) + foliacija-'sken−3'-SEKVENČNO-25–33 (9/9!-BREZ-duplikatov!)
//   + s28-r1-'Mai-3'-Podzemelj + s36-r1-zap-88-Nov-24-Vranoviče (P232!).
// ISKAMO: MEJA-1872/73 (RESTART-z1-Januar-1873-LAHKO-PRED-s28!-ali-SREDI-PAGI-s28?-'finis-Anni-1872'?-'Initium-1873'-kalligrafija?),
//   leto 1873 (s28–s36!), TAIL-1873 (s36-zap-88–97-Nov! + s37-r1-Dez-28/29-P232-ŽE-VLM!).
// ★★★ POZOR: MESEC-MISREADI-Q3 (s30-'März'?!-s31/s32-'Juni'?!-kronologija-ne-pase!) — CELA-STRANA-RAZREŠI (P231/P232-lekcija!).
// Izhod: /tmp/p233/vlm-page/sNN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p233";
const OUT_DIR = "/tmp/p233/vlm-page";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2).map(s => 's' + parseInt(s.slice(1), 10));
const SCANS = fs.readdirSync(IN_DIR).filter(f => /^s\d+\.jpg$/.test(f))
  .map(f => f.replace('.jpg', '')).sort((a, b) => parseInt(a.slice(1)) - parseInt(b.slice(1)))
  .filter(s => FILTER.length === 0 || FILTER.includes(s));

function promptFor(scan) {
  return `To je CELLOTEN sken strani KRSTNE matične knjige župnije Podzemelj (obdobje 1871–1885 — STAREJŠI zvezek, STAREJŠA pisava!), slovenska Kurrent pisava (nemški gotski vpliv). Sken = ${scan}.
KONTEKST: to je STAREJŠI zvezek krstne knjige. Iskamo leto 1873 = 13/15-predzgodovinska-linija — zato so tukaj lahko ZAKLJUČEK leta 1872 (tail-Dezember + 'finis-Anni-1872'-kalligrafija!), MEJA-1872/73 (RESTART-številčenja-z1 + glava!-LAHKO-tudi-PRED-to-stranjo!), leto 1873, ali TAIL-1873 (s36 = ŽE-POTRJEN-zaključek-P232: s36-r1–r10 = zap-88–97-vsi-November (r5-zap-92-GRIBLJE-h6!-r6-zap-93-GRIBLJE-h62!-r7-zap-94-GRIBLJE-h11!) + s37-r1 = Dez-28/29-Kloster-zap-28[~98]-TAIL!).
ZNANO-IZ-P233-PROBE: glave — s28–s36-VSE-'Jahr 1873' (9/9!); foliacija-'sken−3'-SEKVENČNO: s28='25'-s29='26'-s30='27'-s31='28'-s32='29'-s33='30'-s34='31'-s35='32'-s36='33' (BREZ-duplikatov!); prve-vrstice-probe: s28-r1-'Mai-3?-Podzemelj-Mathildis'-s29-r1-'September?-11-Dobrave-36'-s30-r1-'März?-15'-s31-r1-'Juni?-23'-s32-r1-'Juni?-25-Graduc'-s33-r1-'August?-2-Gradac'-s34-r1-'?-Mokrine?-14'-s35-r1-'October-26-Gradac'-s36-r1-'November-24-Vranoviče-11-zap-88' — ★★★ MESCI-SO-LAHKO-MISREADI (kronologija-mora-bit-naraščajoča-od-Januarja-do-Novembra!-P231/P232-lekcija!) — RAZREŠI-kronologijo!
★★★ FOLIACIJA: v zgornjem-levem-kotu je gola-svinčna-cifra (arhivarjeva-foliacija, vzorec-'sken−3'). Preberi in zapiši cifro — če je neberljiva, napiši null.

Struktura tabele (stolpci, levo → desno; LAHKO se razlikuje — starejša forma! opisuj TOČNO kaj vidiš):
1. Zaporedna številka vrstice (ročno; vsako leto se restarta na 1!)
2. Mesec in dan rojstva ter dan krsta (meseci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember)
3. Bivališče: vas (npr. Griblje, Krasinec, Dobravice/Dobravce, Primostek, Gradac, Podžemelj/Podzemelj, Hrast/Hrnelj, Certoviše, Malše, Boršt, Klošter, Otok, Giriče/Geriče, Vranoviče, Begunja vas, Boginja vas, Ohljuka, Prilozje, Krivoglavce, Zemelj, Grem, Dragoše, Gorice, Maršiči, Paunoviče, Dolga vas, Kaplišče, Lemež) + hišna številka (poseben ozek stolpec — POZOR: Kurrent 3/5/8 zmeda, 7 = γ-forma s prečko!)
4. Ime otroka
5. Spola (moški/ženski kljukice »1«) + zakoniti/nezakoniti (včasih ločeni stolpci!)
6. Ime in priimek očeta (+ stan/gospodarska enota: npr. ¼/½/¾/1 Ganzl, Gütl, zemljiščni kmeti)
7. Ime in priimek (roj. dekliško) matere
8. Botra/botri (ime + priimek + stan — pogosto 2 osebi!)
9. Podpis duhovnika krstilnika (Kurrent-ligatura 'Prieſter' — dolgi ſ + in!; v-1873-so-bili-podpisi-'Franz-Dovgan'-in-'Joseph-Pihlár[?]'-garble!)
10. Opomba (npr. poznejši pripisi o poroki/smrti — MODRI/ČRNILO-†-pripisi!)

PRAVILA:
- Prepiši VSAKO vrstico tabele (od zgoraj navzdol) s čim več natančnostjo. Negotovo z [~], neberljivo z [?].
- ZAPOREDNA ŠTEVILKA: beri IZ KLJUČNEGA STOLPCA najbolj LEVO! Ne zaznamuj številk iz starostnega ali hišnega stolpca!
- POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko (γ-forma!); 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki; 3 je zrcalna-E; 3/5/8 zmeda.
- Še posebej NATAČNO pri VASI: poišči VSE vrstice, kjer je vas »Griblje« (ali varianta Griblj/Grible/Griable/Griße/Grile) — to so ključne!
- Posebej zapiši VSE MARKERJE: letnica-glava »Jahr 18 ..« (ali PRAZNA glava!), velike črte/veliki cifri čez vrsto, VSOTNA-vrsta (lahko z RAZPETIMI CIFRAMI čez stolpce), 'finis-Anni'-kalligrafija (VELIKA-ČRKovana-čez-dno-strani!), 'Initium-anni-Domini'-kalligrafija, mesečni prelomi, prazne vrste, restart zaporedne številke na 1, PREČRTANE vrstice, svinčna-foliacija-zgornji-levi-kot!
- Če stran vsebuje ZAČETEK leta 1873 (restart-številčenja-na-1 ALBO 'finis-Anni-1872'-kalligrafija ALBO 'Initium-anni-Domini-1873'-kalligrafija ALBO prva-Jänner-vrstica-1873), to jasno označi z MEJA.
- Če stran vsebuje ZAKLJUČEK leta 1872 (tail-Dezember-vrstice-pred-restartom), to jasno označi z TAIL.
- Če stran vsebuje ZAKLJUČEK leta 1873 (tail-Dezember/November-vrstice-1873-pred-'Jänner'-1874-prelomom-s37!), to jasno označi z TAIL.
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
