// P232 — celostansko branje skenov KRSTNE PREDZGODOVINE 04104 (12/15, leto 1874!).
// LEAD-P231 + P232-PROBE: MEJA-1873/74 = s37/s38 (glave: s36–s37='Jahr 1873'-Dezember-tail,
//   s38–s45='Jahr 1874'!) — foliacija-'sken−3' 33–42 SEKVENČNO (s44='41'-P231-pričakovano-✓!).
// ISKAMO: TAIL-1873 (s37-Dezember-28+! + 'finis-Anni-1873'-kalligrafija-LAHKO!), MEJA-1873/74
//   (SREDI-PAGI-s37-VARIANTA?-ali-DVO-STRANSKA-s37/s38?-ali-NEKAJ-DRUGEGA!), leto 1874 (s38–s44),
//   TAIL-1874 (s45–s47-r5-P231-ŽE-VLM: zap-72–87-VIDEN-×2-strani!-Dez-26–31!-SREDI-PAGI-s47-MEJA-1874/75!).
// ★★★ POZOR: TROJNI-DUPLIKATI-LAHKO-se-ponovijo (s60=s61=s62-P231!) — 'sken−3'-velja-do-s60!
// ★★★ Q3-probe-KONFLIKT: s38-r1-'September-zap46-Griblje-Anna'?! — CELA-STRANA-RAZREŠI!
// Izhod: /tmp/p232/vlm-page/sNN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p232";
const OUT_DIR = "/tmp/p232/vlm-page";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2).map(s => 's' + parseInt(s.slice(1), 10));
const SCANS = fs.readdirSync(IN_DIR).filter(f => /^s\d+\.jpg$/.test(f))
  .map(f => f.replace('.jpg', '')).sort((a, b) => parseInt(a.slice(1)) - parseInt(b.slice(1)))
  .filter(s => FILTER.length === 0 || FILTER.includes(s));

function promptFor(scan) {
  return `To je CELLOTEN sken strani KRSTNE matične knjige župnije Podzemelj (obdobje 1871–1885 — STAREJŠI zvezek, STAREJŠA pisava!), slovenska Kurrent pisava (nemški gotski vpliv). Sken = ${scan}.
KONTEKST: to je STAREJŠI zvezek krstne knjige. Iskamo leto 1874 = 12/15-predzgodovinska-linija — zato so tukaj lahko ZAKLJUČEK leta 1873 (tail-Dezember + 'finis-Anni-1873'-kalligrafija!), MEJA-1873/74 (RESTART-številčenja-z1 + glava!), leto 1874, ali TAIL-1874 (s45–s47 = ŽE-POTRJEN-TAIL-1874-P231: s45-zap-72–79!-s46-zap-80–87!-s47-r1–r5-Dez-26–31!-potem-SREDI-PAGI-'Jänner'-1875-prelom!).
ZNANO-IZ-P232-PROBE: glave — s36–s37='Jahr 1873' / s38–s45='Jahr 1874'; foliacija-'sken−3': s36='33'-s37='34'-s38='35'-s39='36'-s40='37'-s41='38'-s42='39'-s43='40'-s44='41'-s45='42' (SEKVENČNO!).
★★★ PROBE-KONFLIKT-ZA-RAZREŠITI: s38-r1-probe-je-prebrala-'zap-46-September-7/8-Griblje-Anna'?! Če-je-s38-res-1874-začetek,-r1-mora-biti-RESTART-z1-Jänner! Preveri POZORNO prvo-vrstico + VSE-vrstice-s38 (kje-točno-je-RESTART-z1?-ali-je-s38-SREDI-PAGI-meja-1873-tail-+1874-start?-ali-je-probe-napačno-bral?).
★★★ FOLIACIJA: v zgornjem-levem-kotu je gola-svinčna-cifra (arhivarjeva-foliacija, vzorec-'sken−3': s36='33'...s45='42'). Preberi in zapiši cifro — če je neberljiva, napiši null.
★★★ TAIL-1874-ŽE-ZNANO-P231: s47-r1–r5 = Dez-26–31 (r1-Dez-26/26-Dobravce-h13! + r2-Dez-26/27-Krasine-h10! + r3-Dez-28/28-GRIBLJE-h22-Maria-MILEK-oče+Maria-PEZDIRE-matec-Dovgan-podpis! + r4-Dez-28/29-GRIBLJE-h65-Maria-MILEK-oče+Harasinič-matec-Dovgan! + r5-Dez-31/31-Certoviše-h11-Anna-'izvršena-4.3.1953-dekret-št.9'-MODRI!); s45-zap-72–79 (r2-†22.10.1930-MODRI!); s46-zap-80–87 (r3-umrl-28/11.1944[?]-MODRI!-r4-umrl-13.7.1949-CHICAGO-military-MODRI!-r3-oče-Johann-Perdic-GRIBLJE-h4!). POTRDI-to-vrstice-1:1!

Struktura tabele (stolpci, levo → desno; LAHKO se razlikuje — starejša forma! opisuj TOČNO kaj vidiš):
1. Zaporedna številka vrstice (ročno; vsako leto se restarta na 1!)
2. Mesec in dan rojstva ter dan krsta (meseci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember)
3. Bivališče: vas (npr. Griblje, Krasinec, Dobravice/Dobravce, Primostek, Gradac, Podžemelj/Podzemelj, Hrast/Hrnelj, Certoviše, Malše, Boršt, Klošter, Otok, Giriče/Geriče, Vranoviče, Begunja vas, Boginja vas, Ohljuka, Prilozje, Krivoglavce, Zemelj, Grem, Dragoše, Gorice, Maršiči, Paunoviče, Dolga vas, Kaplišče, Lemež) + hišna številka (poseben ozek stolpec — POZOR: Kurrent 3/5/8 zmeda, 7 = γ-forma s prečko!)
4. Ime otroka
5. Spola (moški/ženski kljukice »1«) + zakoniti/nezakoniti (včasih ločeni stolpci!)
6. Ime in priimek očeta (+ stan/gospodarska enota: npr. ¼/½/¾/1 Ganzl, Gütl, zemljiščni kmeti)
7. Ime in priimek (roj. dekliško) matere
8. Botra/botri (ime + priimek + stan — pogosto 2 osebi!)
9. Podpis duhovnika krstilnika (Kurrent-ligatura 'Prieſter' — dolgi ſ + in!; v-1875-so-bili-podpisi-'Hoggia/Roggja/Hoggin-Coop'-in-'Franz-Dovgan'!)
10. Opomba (npr. poznejši pripisi o poroki/smrti — MODRI/ČRNILO-†-pripisi!)

PRAVILA:
- Prepiši VSAKO vrstico tabele (od zgoraj navzdol) s čim več natančnostjo. Negotovo z [~], neberljivo z [?].
- ZAPOREDNA ŠTEVILKA: beri IZ KLJUČNEGA STOLPCA najbolj LEVO! Ne zaznamuj številk iz starostnega ali hišnega stolpca!
- POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko (γ-forma!); 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki; 3 je zrcalna-E; 3/5/8 zmeda.
- Še posebej NATAČNO pri VASI: poišči VSE vrstice, kjer je vas »Griblje« (ali varianta Griblj/Grible/Griable/Griße/Grile) — to so ključne!
- Posebej zapiši VSE MARKERJE: letnica-glava »Jahr 18 ..« (ali PRAZNA glava!), velike črte/veliki cifri čez vrsto, VSOTNA-vrsta (lahko z RAZPETIMI CIFRAMI čez stolpce), 'finis-Anni'-kalligrafija (VELIKA-ČRKovana-čez-dno-strani!), mesečni prelomi, prazne vrste, restart zaporedne številke na 1, PREČRTANE vrstice, svinčna-foliacija-zgornji-levi-kot!
- Če stran vsebuje ZAČETEK leta 1874 (restart-številčenja-na-1 ALBO 'finis-Anni-1873'-kalligrafija ALBO prva-Jänner-vrstica-1874), to jasno označi z MEJA.
- Če stran vsebuje ZAKLJUČEK leta 1873 (tail-Dezember-vrstice-pred-restartom), to jasno označi z TAIL.
- Če stran vsebuje ZAKLJUČEK leta 1874 (tail-Dezember-vrstice-1874-pred-'Jänner'-1875-prelomom-s47-SREDI-PAGI!), to jasno označi z TAIL.
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
