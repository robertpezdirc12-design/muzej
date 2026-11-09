// P235 — celostansko branje skenov KRSTNE PREDZGODOVINE 04104 (15/15, leto 1871!).
// PROBE: glave s9–s13-'Jahr 1871' (pričakovane 5/5!) + foliacija-'sken−3'-pričakovana s13='10'-...-s9='6'
//   + s1–s8-UREJANJE-KONCA-LINIJE (meja-1870/71-LAHKO-že-tukaj!-ali-knjiga-začne-z-1871!).
// ISKAMO: leto 1871 (VSE-s1–s13!-Jänner–Dezember!), ZAČETEK-1871 (RESTART-z1!-MEJA-1870/71-KJER-KOLI!),
//   TAIL-1871 (Dezember!-s13-tail-pričakovano-12-vrstic!), GLAVE-'Jahr 1871', DUHOVNIKI-1871 (ločilni-R-zoom!),
//   + 1870-kontekst-LAHKO (če-knjiga-začne-z-1870!-tail-1870-vrstice!).
// ★★★ POZOR: 1-DUPLIKAT-še-vedno-neznana-lokacija-s1–s13! (s28=s29-P234!-s60=s61=s62-TROJNI-P231!) — foliacija-LAHKO-skoči!
//   + Q3-probe-zap-branja-so-LAHKO-MISREADI (KURRENT-1/2-zmeda!) — MESECI-so-kronološki — zap-RAZREŠI-s-kontekstom!
// Izhod: /tmp/p235/vlm-page/sNN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p235";
const OUT_DIR = "/tmp/p235/vlm-page";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2).map(s => 's' + parseInt(s.slice(1), 10));
const SCANS = fs.readdirSync(IN_DIR).filter(f => /^s\d+\.jpg$/.test(f))
  .map(f => f.replace('.jpg', '')).sort((a, b) => parseInt(a.slice(1)) - parseInt(b.slice(1)))
  .filter(s => FILTER.length === 0 || FILTER.includes(s));

function promptFor(scan) {
  return `To je CELLOTEN sken strani KRSTNE matične knjige župnije Podzemelj (obdobje 1870–1872 — STAREJŠI zvezek, STAREJŠA pisava!), slovenska Kurrent pisava (nemški gotski vpliv). Sken = ${scan}.
KONTEKST: to je ZAČETEK zvezka krstne knjige (s1 = najmanjša-datoteka — verjetno naslovna-stran ALBO prva-pag!). Iskamo leto 1871 = 15/15-ZADNJE-predzgodovinska-linija — tukaj je lahko ZAČETEK zvezka/leta 1870 (tail-1870!-ALI-naslovna-stran!), ZAČETEK leta 1871 (RESTART-zaporedne-številke-na-1!-Jänner!-glava-'Jahr 1871'!-'Initium-anni-Domini-1871'-kalligrafija-LAHKO!), leto 1871 (Jänner–Dezember!), ALI zaključek leta 1871 (tail-Dezember + 'finis-Anni-1871'-kalligrafija-LAHKO!) — naslednja-stran-s14 = že-'Jahr 1872'-restart-z1-Jänner-5 (P234-potrjeno!).
★★★ FOLIACIJA: v zgornjem-levem-kotu je gola-svinčna-cifra (arhivarjeva-foliacija, vzorec-'sken−3'-'kontinuiteta: s13-pričakovana-'10'-...-s9-'6'-s14-'11'-P234!'). Preberi in zapiši cifro — če je neberljiva ALBO KOT-PRAZEN (naslovna-stran!), napiši null.

Struktura tabele (stolpci, levo → desno; LAHKO se razlikuje — starejša forma! opisuj TOČNO kaj vidiš):
1. Zaporedna številka vrstice (ročno; vsako leto se restarta na 1!)
2. Mesec in dan rojstva ter dan krsta (meseci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember)
3. Bivališče: vas (npr. Griblje, Krasinec, Dobravice/Dobravce, Primostek, Gradac, Podžemelj/Podzemelj, Certoviše/Cerovišče, Malše, Boršt, Klošter, Otok, Giriče/Geriče, Vranoviče, Begunja vas, Boginja vas, Ohljuka, Prilozje, Krivoglavce, Zemelj, Grem, Dragoše, Gorice, Maršiči, Paunoviče, Dolga vas, Kaplišče/Kapljišče, Lemež) + hišna številka (poseben ozek stolpec — POZOR: Kurrent 3/5/8 zmeda, 7 = γ-forma s prečko!)
4. Ime otroka
5. Spola (moški/ženski kljukice »1«) + zakoniti/nezakoniti (včasih ločeni stolpci!)
6. Ime in priimek očeta (+ stan/gospodarska enota: npr. ¼/½/¾/1 Ganzl, Gütl, zemljiščni kmeti)
7. Ime in priimek (roj. dekliško) matere
8. Botra/botri (ime + priimek + stan — pogosto 2 osebi!)
9. Podpis duhovnika krstilnika (Kurrent-ligatura 'Prieſter' — dolgi ſ + in!; 1872-X-open-Lekcija: PODPISE-SISTEMATIČNO-EKSTRAHIRAJ!-poskusi-prebrati-VSAK-podpis!-1871-duhovniki-LAHKO-drugi!)
10. Opomba (npr. poznejši pripisi o poroki/smrti — MODRI/ČRNILO-†-pripisi!)

PRAVILA:
- Prepiši VSAKO vrstico tabele (od zgoraj navzdol) s čim več natančnostjo. Negotovo z [~], neberljivo z [?].
- ZAPOREDNA ŠTEVILKA: beri IZ KLJUČNEGA STOLPCA najbolj LEVO! Ne zaznamuj številk iz starostnega ali hišnega stolpca! POZOR: KURRENT-1/2-zmeda ('1'-s-serifom-≈-'2'!) — če-zap-NI-jasno, napiši best-guess-z-[~]!
- POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko (γ-forma!); 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki; 3 je zrcalna-E; 3/5/8 zmeda.
- Še posebej NATAČNO pri VASI: poišči VSE vrstice, kjer je vas »Griblje« (ali varianta Griblj/Grible/Griable/Grihle/Grile) — to so ključne!
- Posebej zapiši VSE MARKERJE: letnica-glava »Jahr 18 ..«, velike črte/veliki cifri čez vrsto, VSOTNA-vrsta, 'finis-Anni'-kalligrafija, 'Initium-anni-Domini'-kalligrafija, mesečni prelomi, prazne vrste, RESTART zaporedne številke na 1, PREČRTANE vrstice, svinčna-foliacija, NASLOVNA-STRAN (s1!).
- Če stran vsebuje ZAKLJUČEK leta 1870 (tail-Dezember-1870-vrstice + 'finis-Anni-1870'-kalligrafija-LAHKO!), to jasno označi z TAIL-1870.
- Če stran vsebuje ZAČETEK leta 1871 (restart-številčenja-na-1 ALBO prva-Jänner-vrstica-1871 + glava-'Jahr 1871' + 'Initium-anni-Domini-1871'-kalligrafija-LAHKO!), to jasno označi z MEJA-1871.
- Če stran vsebuje ZAKLJUČEK leta 1871 (tail-Dezember-vrstice + 'finis-Anni-1871'-kalligrafija-LAHKO!), to jasno označi z TAIL.
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez markdown):
{"skan": "${scan}", "struktura": "opis (glava, št. vrstic, posebnosti, kalligrafija?, naslovna?)", "leto": "najbolj verjetna letnica ali null", "meja": "opis ali null", "tail": "opis ali null", "foliacija": "cifra ali null", "vrstice": [{"vrsta": 1, "zaporedna": "1", "mesec": "Jänner", "rojen": "5.", "krsten": "7.", "vas": "Griblje", "hisna": "12", "otrok": "...", "spol": "moški|ženski", "zakonit": "zakoniti|nezakoniti|null", "ocec": "...", "matec": "...", "botra": "...", "duhovnik": "...", "opomba": null}], "markerji": ["opis ali ..."], "opomba": "..."}`;
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
