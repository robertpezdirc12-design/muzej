// P221 — branje kropov (Griblje-vrstice + zap-stolpci + arb-dokazi). Izhod: /tmp/p221/vlm-krop/NN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p221/krop-grib";
const OUT_DIR = "/tmp/p221/vlm-krop";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2);
const FILES = fs.readdirSync(IN_DIR).filter(f => /^.*\.png$/.test(f))
  .filter(f => FILTER.length === 0 || FILTER.some(x => f.includes(x)));

function promptFor(file) {
  const isZap = file.includes('_zap_stolpec');
  const isPag = file.includes('_pag');
  if (isZap) {
    return `To je navpični IZREZ ZAPOREDNEGA STOLPCA (najbolj LEVI stolpec tabele) razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (leto 1884/1885, Kurrent pisava). Datoteka = ${file}.
NALOGA: Preberi VSAKO ročno vpisano zaporedno številko, OD ZGORAJ NAVZDOL, v vrstnem redu. To je številčenje leta 1885 (restart na 1!) ali rep leta 1884.
POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko (γ-forma!); 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki; 3/5/8 zmeda. Palični prečrti (revizija) NE veljajo za cifre!
Če je katera številka PREČRTANA in ob nji DOPISANA nova, to zapiši kot "102[prečrtano]/103[dopisano]".
Če je številka neberljiva, zapiši [?]. Če je vrstica PRAZNA (brez številke), zapiši null.
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "stevilke": ["1", "2", ...], "opomba": "..."}`;
  }
  if (isPag) {
    return `To je ZGORNJI LEVI DEL razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (1884/1885, Kurrent pisava). Datoteka = ${file}.
NALOGA:
1. Preberi ročno vpisano PAGINACIJO (svinčnik arhivarja, npr. 'Pag. 203' ali samo številka) — če je vidna. POZOR: Kurrent cifre, 3/5/8 zmeda, 0/6/9 zmeda!
2. Preberi LETNIČNO GLAVO tabele: natisnjeno 'Jahr 18 ..' + ročno dopisane cifre (npr. '85' ali '86'!). Če je letnica nadčrtana/popravljena, to zapiši!
3. Opiši, ali je na strani NTISNJEN NASLOV ('Geburts- und Tauf-Buch.' / 'Rojstna in krstna knjiga.') in kje.
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "paginacija": "...", "letnica_glava": "...", "naslov": "...", "opomba": "..."}`;
  }
  return `To je ENA VRSTICA (izrez) razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (leto 1885, Kurrent pisava). Datoteka = ${file}.
Vsaka vrstica: LEVA stran = zaporedna št., mesec+dan rojstva/krsta, vas (Geburtsort), hišna št., ime otroka, Religion/Geschlecht/Ehelich; DESNA stran = starši (oče: ime+priimek+stan; mati: ime+roj. priimek), botri (Pathen: ime+stan), babica, duhovnik.

NALOGA — prepiši vrstico S ČIM VEČ NATAČNOSTJO:
- zaporedna številka (levi stolpec!)
- mesec + dan rojstva + dan krsta
- vas (KLJUČNO: ali je Griblje/Grible/Griable ali druga vas! Kurrent 'G'-forma!)
- hišna številka (Kurrent 3/5/8 zmeda, 7=γ-forma!)
- ime otroka + spol
- oče (ime+priimek+stan: ¼/½/¾/1 Ganzl, Gärtler, Gütl, Hübler, kmet/Bauer ...)
- mati (ime + roj. dekliški priimek)
- botra/botri (ime+priimek+stan)
- duhovnik (podpis)
- POZNEJŠI PRIPISI (modro/rdeče: † datum smrti, poroka, maticni pregled ...) — ZAPIŠI TOČNO!

Negotovo z [~], neberljivo z [?]. Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "zaporedna": "...", "mesec": "...", "rojen": "...", "krsten": "...", "vas": "...", "hisna": "...", "otrok": "...", "spol": "...", "ocec": "...", "matec": "...", "botra": "...", "duhovnik": "...", "pripis": "...", "opomba": "..."}`;
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
  for (let attempt = 1; attempt <= 6; attempt++) {
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
      if (attempt === 6) throw e;
      await new Promise(r => setTimeout(r, /429|Too many/.test(e.message) ? 30000 : 3000 * attempt));
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
      const summary = res.stevilke ? `stevilke=${res.stevilke.join(',')}` : `zap=${res.zaporedna} vas=${res.vas} hisna=${res.hisna} otrok=${res.otrok}`;
      console.log(`${f}: OK ${String(summary).slice(0, 150)}${res.paginacija ? ' pag=' + res.paginacija : ''}${res.letnica_glava ? ' glava=' + res.letnica_glava : ''}`);
    } catch (e) {
      console.error(`${f}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
