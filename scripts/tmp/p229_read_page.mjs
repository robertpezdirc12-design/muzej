// P229 — celostansko branje skenov KRSTNE PREDZGODOVINE 04104 (9/15, leto 1877!).
// LEAD-P228: MEJA-1877/78-ŽE-NAJDENA (s92/s93!-RESTART-z1-1878-[8↔9]-JÄNNER-Boginja-vas-h14!).
// 1877 = z1–z91-91-vpisov-pričakovano (TAIL-z86–z91-Dezember-ŽE-VLM-s92!) → MEJA-1876/77-pred-s92
//   → probe-s85–s92-DESCENDING! — gola-pag-'sken−5'-pričakovana-s85='80' (s86='81'/s91='86'/s92='87'-P228!).
// Izhod: /tmp/p229/vlm-page/sNN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p229";
const OUT_DIR = "/tmp/p229/vlm-page";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2).map(s => 's' + parseInt(s.slice(1), 10));
const SCANS = fs.readdirSync(IN_DIR).filter(f => /^s\d+\.jpg$/.test(f))
  .map(f => f.replace('.jpg', '')).sort((a, b) => parseInt(a.slice(1)) - parseInt(b.slice(1)))
  .filter(s => FILTER.length === 0 || FILTER.includes(s));

function promptFor(scan) {
  return `To je CELLOTEN sken strani KRSTNE matične knjige župnije Podzemelj (obdobje 1871–1885 — STAREJŠI zvezek, STAREJŠA pisava!), slovenska Kurrent pisava (nemški gotski vpliv). Sken = ${scan}.
KONTEKST: to je STAREJŠI zvezek krstne knjige (mlajši zvezek 04105 se začne 1886). Iskamo leto 1877 = 9/15-predzgodovinska-linija — zato so tukaj lahko ZAKLJUČEK leta 1876 (tail + VSOTNA/velike-cifre-'1/8/7/6'/'Jahr 1876'), MEJA-1876/77 (VSOTNA/velike-cifre-'1/8/7/7'-ali-glava-'Jahr 1877' + restart-številčenja-z1!), leto 1877, ali TAIL-1877 (Dezember-11–30: z86-Gradaz + z87-Krasine + z88-Zemelj + z89-GRIBLJE-h33 + z90/z91-Gradac — ŽE-VLM-v-P228!) — MEJA-1877/78 ŽE-POTRJENA: s92 = ZADNJA-1877-stran (tail-z86–z91 + glava-'Jahr 1877'-na-s92!), s93 = prva-1878-stran (RESTART-z1-NA-DAN-[8↔9]-JÄNNER-Boginja-vas-h14!).
ZNANO-IZ-P228: s92 = TAIL-1877 (z86–z91-Dezember-11–30!-6-vrstic!) + glava-'Jahr 1877'-BREZ-VSOTNE/velikih-cifer (P225-TIP!). Iskamo: MEJA-1876/77 ('Jahr 1877'-glava + RESTART-z1-1877!) — PRED-s92 → probe-s85–s92-DESCENDING (po potrebi nazaj!).
POZOR-PAG-KONVENCIJA: pričakovana GOLA-SVINČNA-foliacija 'sken−5' (paralela-1878-okno: s92='87'/s93='88'...!-P228-POTRJENA!) — pričakovana-s85='80'/s86='81'/s87='82'/s88='83'/s89='84'/s90='85'/s91='86'! — če vidiš številko na dnu strani (sredina-spodaj, svinčnik!), to ZAPIŠI v markerje! POZOR-ANOMALIJA: opiši MESECE TOČNO tako kot so napisani — ne sklepaj! ('…ember'-failure-mode iz P223/P224/P225/P227/P228!)

Struktura tabele (stolpci, levo → desno; LAHKO se razlikuje — starejša forma! opisuj TOČNO kaj vidiš):
1. Zaporedna številka vrstice (ročno; vsako leto se restarta na 1!)
2. Mesec in dan rojstva ter dan krsta (meseci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember)
3. Bivališče: vas (npr. Griblje, Krasinec, Dobravice/Dobravce, Primostek, Gradac, Podžemelj/Podzemelj, Hrast/Hrnelj, Certoviše, Malše, Boršt, Kloster/Klošter, Otok, Giriče/Geriče, Vranoviče, Begunja vas, Boginja vas, Ohljuka, Prilozje, Krivoglavce, Zemelj, Grem, Dragoše, Gorice, Maršiči, Paunoviče, Dolga vas, Kaplišče, Lemež) + hišna številka (poseben ozek stolpec — POZOR: Kurrent 3/5/8 zmeda, 7 = γ-forma s prečko!)
4. Ime otroka
5. Spola (moški/ženski kljukice »1«) + zakoniti/nezakoniti (včasih ločeni stolpci!)
6. Ime in priimek očeta (+ stan/gospodarska enota: npr. ¼/½/¾/1 Ganzl, Gütl, zemljiščni kmeti)
7. Ime in priimek (roj. dekliško) matere
8. Botra/botri (ime + priimek + stan — pogosto 2 osebi!)
9. Podpis duhovnika krstilnika (Kurrent-ligatura 'Prieſter' — dolgi ſ + in!)
10. Opomba (npr. poznejši pripisi o poroki/smrti!)

PRAVILA:
- Prepiši VSAKO vrstico tabele (od zgoraj navzdol) s čim več natančnostjo. Negotovo z [~], neberljivo z [?].
- ZAPOREDNA ŠTEVILKA: beri IZ KLJUČNEGA STOLPCA najbolj LEVO! Ne zaznamuj številk iz starostnega ali hišnega stolpca!
- POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko (γ-forma!); 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki; 3/5/8 zmeda.
- Še posebej NATAČNO pri VASI: poišči VSE vrstice, kjer je vas »Griblje« (ali varianta Griblj/Grible/Griable) — to so ključne!
- Posebej zapiši VSE MARKERJE: letnica-glava »Leto 18 ..« (ali PRAZNA glava!), velike črte/veliki cifri čez vrsto (npr. »— 80. —« ali »/ 80«), VSOTNA-vrsta (lahko z RAZPETIMI CIFRAMI čez stolpce), mesečni prelomi, prazne vrste, restart zaporedne številke na 1, PREČRTANE vrstice!
- NASLOVNI LIST ('Tauf-Buch.' natisnjeno): če je stran naslovni list (BREZ vpisov ALI z vpisi čez naslov), to OZNAČI v "struktura"!
- Če stran vsebuje ZAČETEK leta 1877 (restart številčenja ali letnica-glava-'Jahr 1877' ali vsotna-marker ali velike-cifre-'1/8/7/7'), to jasno označi z MEJA.
- Če stran vsebuje ZAKLJUČEK leta 1876 (tail-vrstice pred restartom/vsotno/glavo-'Jahr 1877'), to jasno označi z TAIL.
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez markdown):
{"skan": "${scan}", "struktura": "opis (glave, št. vrstic, posebnosti, naslovni-list?)", "leto": "najbolj verjetna letnica ali null", "meja": "opis ali null", "tail": "opis ali null", "vrstice": [{"vrsta": 1, "zaporedna": "1", "mesec": "Jänner", "rojen": "5.", "krsten": "7.", "vas": "Griblje", "hisna": "12", "otrok": "...", "spol": "moški|ženski", "zakonit": "zakoniti|nezakoniti|null", "ocec": "...", "matec": "...", "botra": "...", "duhovnik": "...", "opomba": null}], "markerji": ["opis ali ..."], "opomba": "..."}`;
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
  for (let attempt = 1; attempt <= 12; attempt++) {
    try {
      completion = await Promise.race([
        make(),
        new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 240000))
      ]);
      const c = completion?.choices?.[0]?.message?.content;
      if (!c) throw new Error('prazna vsebina');
      return parseContent(c);
    } catch (e) {
      const is429 = /429|too many/i.test(e.message);
      console.error(`  ${scan}: poskus ${attempt} ni OK (${e.message.slice(0, 90)})`);
      if (attempt === 8) throw e;
      await new Promise(r => setTimeout(r, is429 ? 150000 : 5000 * attempt));
    }
  }
}

async function main() {
  const inst = await ZAI.create();
  // DESCENDING: s91 ← s85 (meja-iščemo-nazaj!)
  for (const scan of SCANS.reverse()) {
    const out = `${OUT_DIR}/${scan}.json`;
    if (fs.existsSync(out)) { console.log(`${scan}: ŽE`); continue; }
    try {
      const res = await readPage(inst, `${IN_DIR}/${scan}.jpg`, scan);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      const n = res.vrstice?.length ?? 0;
      console.log(`${scan}: OK vrstice=${n} leto=${res.leto} meja=${res.meja ? 'DA' : '-'} tail=${res.tail ? 'DA' : '-'} struktura=${String(res.struktura || '').slice(0, 80)}`);
    } catch (e) {
      console.error(`${scan}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
