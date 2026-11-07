// P222 — branje pass-2 kropov. Izhod: /tmp/p222/vlm-krop3/NN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p222/krop3";
const OUT_DIR = "/tmp/p222/vlm-krop3";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILES = fs.readdirSync(IN_DIR).filter(f => /\.png$/.test(f));

function promptFor(file) {
  const isZap = file.includes('_zap_hi');
  const isHisna = file.includes('_hisna_hi');
  const isVas = file.includes('_vas_hi');
  const isOrd = file.includes('_ordinal_hi');
  if (isZap) {
    return `To je navpični IZREZ ZAPOREDNEGA STOLPCA (najbolj LEVI stolpec tabele) razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (leto 1884, Kurrent pisava, 6× zoom!). Datoteka = ${file}.
NALOGA: Preberi VSAKO ročno vpisano zaporedno številko, OD ZGORAJ NAVZDOL, v vrstnem redu. Poišči VSKE vrstice (tudi stisnjene!). 
POZOR: Kurrent cifre — 1 je ozka črtica; 3/5/8 zmeda; 5/6 zmeda; 6/4 zmeda; 7/9 zmeda; 9/5 zmeda! Črta skozi cifro = PREČRTANJE (revizija pisarja).
Če je številka PREČRTANA in ob nji DOPISANA nova, zapiši kot "81[prečrtano]/82[dopisano]".
Posebej opazi: če se številka PONOVI (duplikat!), če katera MANJKA (preskok!), če so RAZPETE/VELIKE cifre (vsotna!).
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "stevilke": ["1", "2", ...], "opomba": "opis posebnosti (prečrtanja, duplikati, preskoki, prazne vrstice...)"}`;
  }
  if (isHisna) {
    return `To je HIŠNA-ŠTEVILKA KOLONA izreza (hi-zoom) ENE VRSTICE KRSTNE matične knjige župnije Podzemelj (leto 1884, Kurrent). Datoteka = ${file}.
NALOGA: Preberi ročno vpisano HIŠNO ŠTEVILKO. POZOR NA KURRENT CIFRE: 3/5/8 zmeda! 4 ima zanko; 1 je črtica; 7 = γ-s-prečko; 9/5 zmeda; 6/4 zmeda! Če so možne več razlag, naštej VSE (npr. "48 ali 18 ali 8").
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "hisna": "...", "alternative": ["...", ...], "opomba": "..."}`;
  }
  if (isVas) {
    return `To je VAS (Geburtsort) KOLONA izreza (hi-zoom) ENE VRSTICE KRSTNE matične knjige župnije Podzemelj (leto 1884, Kurrent). Datoteka = ${file}.
NALOGA: Preberi ime VASI. Kandidate-vasi: Griblje/Grible/Griable, Krasinec, Dobravice, Primostek, Gradac, Podžemelj/Podzemelj, Hrast, Certoviše/Cerkvišče, Malše, Boršt, Klošter, Otok, Giriče, Vranoviče, Begunja vas, Boginja vas, Ohljuka, Prilozje, Krivoglavce, Zemelj, Grem, Dragoše, Gorice, Maršiči, Paunoviče, Dolga vas, Kaplišče, Lemež. Če je vas Griblje, to POSEBEJ poudari! Če nebereš gotovo, naštej VSE razlage!
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "vas": "...", "alternative": ["...", ...], "je_griblje": true|false|[?], "opomba": "..."}`;
  }
  if (isOrd) {
    return `To je LEVI DEL ENE VRSTICE (zaporedna+datum+vas+hišna, hi-zoom) KRSTNE matične knjige župnije Podzemelj (leto 1884, Kurrent). Datoteka = ${file}.
NALOGA: Preberi: (1) ZAPOREDNO ŠTEVILKO (najbolj levo! 3/5/8 zmeda! 5/6! 6/4! — če več razlag, naštej!), (2) mesec+dan, (3) vas, (4) hišno številko.
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "zaporedna": "...", "zaporedna_alternative": ["..."], "mesec": "...", "rojen": "...", "krsten": "...", "vas": "...", "hisna": "...", "opomba": "..."}`;
  }
  return `To je DESNA STRAN ENE VRSTICE (starši+botri+pripisi, hi-zoom) KRSTNE matične knjige župnije Podzemelj (leto 1884, Kurrent). Datoteka = ${file}.
NALOGA: Prepiši: oče (ime+priimek+stan), mati (ime+roj. priimek), botra/botri, duhovnik, in VSE POZNEJŠE PRIPISE (modro/rdeče črnilo: † smrt, poroka, matrični pregled — preberi TOČNO datume!). Negotovo z [~], neberljivo z [?].
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "ocec": "...", "matec": "...", "botra": "...", "duhovnik": "...", "pripis": "...", "opomba": "..."}`;
}

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readImg(zai, img, file) {
  const b64 = fs.readFileSync(img).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(file) },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  let completion;
  for (let attempt = 1; attempt <= 10; attempt++) {
    completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 240000))
    ]);
    try {
      const c = completion?.choices?.[0]?.message?.content;
      if (!c) throw new Error('prazna vsebina');
      return parseContent(c);
    } catch (e) {
      console.error(`  ${file}: poskus ${attempt} ni OK (${e.message})`);
      if (attempt === 10) throw e;
      await new Promise(r => setTimeout(r, /429|Too many/.test(e.message) ? 120000 : 8000 * attempt));
    }
  }
}

async function main() {
  const inst = await ZAI.create();
  for (const f of FILES) {
    const out = `${OUT_DIR}/${f.replace('.png', '')}.json`;
    if (fs.existsSync(out)) { console.log(`${f}: ŽE`); continue; }
    try {
      const res = await readImg(inst, `${IN_DIR}/${f}`, f);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      const summary = res.stevilke ? `st=${res.stevilke.join(',')}` : JSON.stringify(res).slice(0, 140);
      console.log(`${f}: OK ${String(summary).slice(0, 160)}`);
    } catch (e) {
      console.error(`${f}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
