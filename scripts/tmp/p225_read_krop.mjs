// P225 — branje kropov (krstna 1881) (Griblje-vrstice + zap-stolpci + pag + meja + mesec-stolpci). Izhod: /tmp/p224/vlm-krop/NN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p224/krop-grib";
const OUT_DIR = "/tmp/p224/vlm-krop";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2);
const FILES = fs.readdirSync(IN_DIR).filter(f => /^.*\.png$/.test(f))
  .filter(f => FILTER.length === 0 || FILTER.some(x => f.includes(x)));

function promptFor(file) {
  const isZap = file.includes('_zap_stolpec');
  const isPag = file.includes('_pag');
  const isMesec = file.includes('_mesec_stolpec');
  const isMeja = file.includes('arb_s135_finis') || file.includes('arb_s136_meja');
  if (isZap) {
    return `To je navpični IZREZ ZAPOREDNEGA STOLPCA (najbolj LEVI stolpec tabele) razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (leto 1880/1881, Kurrent pisava). Datoteka = ${file}.
NALOGA: Preberi VSAKO ročno vpisano zaporedno številko, OD ZGORAJ NAVZDOL, v vrstnem redu. To je številčenje repa leta 1881 (z83–z89 + 'finis'!) ALI leta 1882 (restart na 1 na s148-vrsta1! z1–z106!) ALI rep-1882+z-restart-1883 (s161: z104–z106 + prazna + 1–6!).
POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko (γ-forma!); 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki; 3/5/8 zmeda. Palični prečrti (revizija) NE veljajo za cifre!
Če je številka PREČRTANA in ob nji DOPISANA nova, to zapiši kot "111[prečrtano]/1[dopisano]".
Če je številka neberljiva, zapiši [?]. Če je vrstica PRAZNA (brez številke), zapiši null. Če vidiš RAZPETE/VELIKE cifre čez stolpec (vsotna-marker) ali besedo 'finis', to posebej omeni v opomba.
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "stevilke": ["1", "2", ...], "opomba": "..."}`;
  }
  if (isPag) {
    return `To je ZGORNJI LEVI DEL razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (1881/1882, Kurrent pisava). Datoteka = ${file}.
NALOGA:
1. Preberi ročno vpisano PAGINACIJO (gola svinčna številka arhivarja, npr. '152' ali '154' — BREZ 'Pag.'-predpone na starejši formi!) — če je vidna. POZOR: Kurrent cifre, 2/4 zmeda (ozka zankasta 2 VS zankasta 4!), 3/5/8 zmeda, 0/6/9 zmeda!
2. Preberi LETNIČNO GLAVO tabele: natisnjeno 'Jahr 18 ..' + ročno dopisane cifre (npr. '81'/'82'!). Če je letnica nadčrtana/popravljena, to zapiši!
3. Opiši, ali je na strani NTISNJEN NASLOV ('Geburts- und Tauf-Buch.') in kje.
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "paginacija": "...", "letnica_glava": "...", "naslov": "...", "opomba": "..."}`;
  }
  if (isMesec) {
    return `To je navpični IZREZ MESEČNEGA STOLPCA (mesec + dan rojstva/krsta) razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (leto 1881, Kurrent pisava). Datoteka = ${file}.
NALOGA: Preberi VSAKO vrstico OD ZGORAJ NAVZDOL: mesečna labela (Jänner/Feber/März/April/Mai/Juni/July/August/September/October/November/Dezember — NAPIŠI TOČNO KAJ JE NAPISANO!) + dan rojstva + dan krsta.
KLJUČNO: na ${file.includes('s160') ? "TEJ STRANI (s160) je anomalija — vrste z96–z103 so bile prebrane kot NOVEMBER 16–30, a PRED njimi je z95-DEZEMBER-16! Preberi mesec PRI VSAKI VRSTI EKSTREMNO NATAČNO — ali je ‹November› ali ‹Dezember›?! (Pisar je lahko napisal November-labelo NAKNADNO-blok — ali pa gre za misread!)" : "tej strani pisar VČASIH napiše mesečno labelo SAMO NA PRVI VRSTICI bloka (carry-over-vzorec!) — če labela MANJKA, vrsta pripada bloku ZGORAJ! NAPIŠI, ali je labela vidna ali ne!"}
POZOR: Kurrent 'Dezember' = D-e-z; 'November' = N-o-v — prva črka je KLJUČNA (D-vs-N)! Dan: 1 ozka črtica; 4 zanka; 7 γ-prečka; 3/5/8 zmeda.
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "vrstice": [{"vrsta": 1, "labela_vidna": true, "mesec": "...", "rojen": "...", "krsten": "..."}], "opomba": "..."}`;
  }
  if (isMeja) {
    return `To je IZREZ MEJE-MED-LETI razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (Kurrent pisava). Datoteka = ${file}.
${file.includes('s135_finis') ? 'Ta stran (s135) naj bi vsebovala TAIL-1880 (zadnje vrstice 116–122 Dezember) + besedo FINIS + glavo-Jahr-18-80 + morebitno VSOTNO-VRSTO 1-8-8-0.' : 'Ta stran (s136) naj bi vsebovala MEJO-1880/81: letnično glavo (natisnjeno Jahr 18__ + ročno 81), morebitno VSOTNO-VRSTO in RESTART zaporednega številčenja na 1 (prva vrstica leta 1881 = Jänner 1. — pričakovano GRIBLJE-h55-Agnes!).'}
NALOGA:
1. Prepiši VSE vidne besedilne markere (finis? Initium/Inicip annos Domini? Summa? Jahr ...) TOČNO.
2. Preberi vsotno-vrsto/razpete cifre, če so vidne (posamezne cifre ločene s presledki).
3. Preberi zaporedne številke vrstic (levi stolpec) od zgoraj navzdol.
4. Prepiši PRVE 2–3 vrstice podatkov (mesec/dan/vas/hišna/ime) če so vidne.
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "besedilni_markerji": ["..."], "vsotna_cifre": "...", "zap_stevilke": ["..."], "vrstice": [{"zaporedna": "...", "mesec": "...", "rojen": "...", "vas": "...", "hisna": "...", "otrok": "..."}], "opomba": "..."}`;
  }
  return `To je ENA VRSTICA (izrez) razprte dvostranske strani KRSTNE matične knjige župnije Podzemelj (leto 1881, Kurrent pisava). Datoteka = ${file}.
Vsaka vrstica: LEVA stran = zaporedna št., mesec+dan rojstva/krsta, vas (Geburtsort), hišna št., ime otroka, Religion/Geschlecht/Ehelich; DESNA stran = starši (oče: ime+priimek+stan; mati: ime+roj. priimek), botri (Pathen: ime+stan), babica, duhovnik.

NALOGA — prepiši vrstico S ČIM VEČ NATAČNOSTJO:
- zaporedna številka (levi stolpec!)
- mesec + dan rojstva + dan krsta
- vas (KLJUČNO: ali je Griblje/Grible/Griable ali druga vas! Kurrent 'G'-forma! POZOR: Maršiči/Primoštek/Krasinec niso Griblje!)
- hišna številka (Kurrent 3/5/8 zmeda, 7=γ-forma, 2/4 zmeda!)
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
      if (attempt === 8) throw e;
      await new Promise(r => setTimeout(r, /429|Too many/.test(e.message) ? 120000 : 8000 * attempt));
    }
  }
}

async function main() {
  const inst = await ZAI.create();
  for (const f of FILES) {
    await new Promise(r => setTimeout(r, 12000));
    const out = `${OUT_DIR}/${f.replace('.png', '')}.json`;
    if (fs.existsSync(out)) { console.log(`${f}: ŽE`); continue; }
    try {
      const res = await readImg(inst, `${IN_DIR}/${f}`, f);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      const summary = res.stevilke ? `stevilke=${res.stevilke.join(',')}` :
        res.vrstice && res.vrstice[0] && res.vrstice[0].mesec !== undefined ? `vrstic=${res.vrstice.length}` :
        `zap=${res.zaporedna} vas=${res.vas} hisna=${res.hisna} otrok=${res.otrok}`;
      console.log(`${f}: OK ${String(summary).slice(0, 140)}${res.paginacija ? ' pag=' + res.paginacija : ''}${res.vsotna_cifre ? ' vsotna=' + res.vsotna_cifre : ''}`);
    } catch (e) {
      console.error(`${f}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
