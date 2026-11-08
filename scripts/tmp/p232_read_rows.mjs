// P232 — branje vrstičnih krops R-<scan>.png (definitiven prepis vsake vrstice 1874 + tail-1873).
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p232/krops';
const OUTD = '/tmp/p232/rows';
fs.mkdirSync(OUTD, { recursive: true });

const SCANS = [37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47];

const FILTER = process.argv.slice(2).map(Number);
const LIST = FILTER.length ? SCANS.filter(s => FILTER.includes(s)) : SCANS;

function promptFor(scan) {
  return `To je vertikalno složen niz izrezov VRSTIC iz strani KRSTNE matične knjige župnije Podzemelj (leto 1873/1874 — STAREJŠI zvezek, STAREJŠA Kurrent-pisava z nemškim gotskim vplivom). Sken = s${scan}. Vsak izrez = ENA vrstica tabele (polna širina: datumi, vas, hišna št., ime, spol, starši, botra, duhovnik, opombe). Zadnji izrez = 'ZAP-levo' = samo levi del prve vrstice (zaporedna številka + mesec + dan, večje povečavo).

STOLPCI (levo→desno): zaporedna številka (ročno, ozek) | mesec in dan rojstva | dan krsta | vas (Geburtsort) | hišna št. (Haus-Nr., ozek!) | ime otroka | spol (kljukice) | zakoniti/nezakoniti | oče (+ stan: ¼/½/¾ Ganzl, Gärtler, Hübler, Söllner, Inwohner...) | mati (roj. dekliško) | botra/botri (2 osebi!) | opombe (MODRI/ČRNILO pripisi o poroki/smrti!) | podpis duhovnika (Kurrent: 'Dovgan'/'Dovogan'/'Hoggia/Roggja/Hoggin-Coop'-ligature!).

PRAVILA:
- Prepiši VSAKO vrstico natančno. Negotovo z [~], neberljivo z [?]. Če je polje PRAZNO (npr. oče pri nezakonskih!), napiši PRAZNO.
- MESECI: Jänner, Feber/Februar, März, April, Mai, Juni, July, August, September, October, November, Dezember. POZOR pri prvi črki: Jänner(J-zanka) vs Dezember(D)! Ne sklepi iz konteksta — beri pisavo!
- CIFRE (Kurrent): 4 ima zanko; 1 = ozka črtica; 7 = γ-forma s prečko; 5 podobna 6; 3/5/8 zmeda; 2 ima osnovo.
- VASI: Griblje (ključna! varianti Grible/Griblj/Griable), Krasinec, Dobravice, Primostek, Gradac, Podzemelj, Certoviše, Boršt, Klošter/Kloster, Otok, Goriče/Giriče, Vranoviče, Begunja vas, Boginja vas, Prilozje, Zemelj, Grem, Dragoše, Maršiči, Kaplišče, Krivoglavce, Paunoviče, Dolga vas, Lemež, Ohljuka, Malše...
- HIŠNA ŠTEVILKA: ozek stolpec — 3/5/8 zmeda, 7 s prečko!
- ZAPOREDNA: beri iz najbolj levega ozkega stolpca! Pogosto PRAZNO/nevidno — to zapiši kot null!
- MODRI/ČRNI pripisi ob straneh († datum, poroka) = poznejše opombe — vedno zapiši!
- Izhod: SAMO veljaven JSON:
{"skan":"s${scan}","vrstice":[{"vrsta":1,"zap":null,"mesec":"...","roj":"...","krst":"...","vas":"...","hisna":"...","otrok":"...","spol":"...","zakonit":null,"ocec":"...","matec":"...","botra":"...","opomba":null,"duhovnik":"..."}],"opombe":"..."}`;
}

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{'), b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON');
  return JSON.parse(t.slice(a, b + 1));
}

async function readSheet(img, scan) {
  const b64 = fs.readFileSync(img).toString('base64');
  for (let attempt = 1; attempt <= 5; attempt++) {
    try {
      const completion = await Promise.race([
        inst.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: promptFor(scan) },
            { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 240000))
      ]);
      const c = completion?.choices?.[0]?.message?.content;
      if (!c) throw new Error('prazna vsebina');
      return parseContent(c);
    } catch (e) {
      console.error(`  s${scan}: poskus ${attempt} FAIL (${e.message.slice(0, 60)})`);
      if (attempt === 5) throw e;
      await new Promise(r => setTimeout(r, /429/.test(e.message) ? 40000 : 5000));
    }
  }
}

let first = true;
for (const scan of LIST) {
  const out = `${OUTD}/s${scan}.json`;
  if (fs.existsSync(out)) { console.log(`s${scan}: ŽE`); continue; }
  if (!first) await new Promise(r => setTimeout(r, 22000));
  first = false;
  try {
    const res = await readSheet(`${DIR}/R-${scan}.png`, scan);
    fs.writeFileSync(out, JSON.stringify(res, null, 2));
    const g = (res.vrstice || []).filter(v => /ribl/i.test(v.vas || '')).length;
    console.log(`s${scan}: OK vrstic=${res.vrstice?.length} Griblje=${g}`);
  } catch (e) {
    console.error(`s${scan}: KONČNO-FAIL ${e.message.slice(0, 80)}`);
  }
}
console.log('ROWS-READ-KONČANO');
