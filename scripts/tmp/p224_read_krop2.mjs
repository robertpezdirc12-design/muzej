// P224 — branje kropov pass-2 (re-krops + hišni-hi-zoomi + posebni). Izhod: /tmp/p224/vlm-krop2/NN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p224/krop2";
const OUT_DIR = "/tmp/p224/vlm-krop2";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2);
const FILES = fs.readdirSync(IN_DIR).filter(f => /^.*\.png$/.test(f))
  .filter(f => FILTER.length === 0 || FILTER.some(x => f.includes(x)));

function promptFor(file) {
  const isHi = file.includes('_hisna_hi');
  if (isHi) {
    const duels = {
      z22_s150: "page-VLM-'14 [~11?]' vs-krop-'[?1]' — kandidati: 14 / 11 / 1!",
      z23_s150: "page-VLM-'73 [~43?]' vs-krop-'43 [~]' — kandidati: 73 / 43!",
      z54_s154: "page-VLM-'66 [~65/66]' vs-krop-'65' — kandidati: 66 / 65!",
      z58_s155: "page-VLM-'41' vs-krop-'11 [~]' — kandidati: 41 / 11!",
      z90_s159: "page-VLM-'14' vs-krop-'74' — kandidati: 14 / 74!",
      z91_s159: "page-VLM-'11' vs-krop-'44' — kandidati: 11 / 44!",
      z92_s159: "page-VLM-'13' vs-krop-'43' — kandidati: 13 / 43!",
      z97_s160: "page-VLM-'47' vs-krop-'17 [~]' — kandidati: 47 / 17!",
    }[file.replace('_hisna_hi.png', '')];
    return `To je OZEK IZREZ HIŠNEGA STOLPCA (Hiſ-Nr.) iz ene vrstice KRSTNE matične knjige župnije Podzemelj (leto 1882, Kurrent pisava). Datoteka = ${file}.
${duels ? `ZNANI-DUEL: ${duels}` : 'Preberi hišno številko s čim več natančnostjo.'}
NALOGA: Preberi ROČNO vpisano hišno številko (1–3 cifre). POZOR NA KURRENT: 1 = ozka črtica; 4 = zankasta; 7 = γ-forma s prečko; 3/5/8 zmeda; 2/4 zmeda; 6/0 zmeda. Obštrni pripisi/prečrti NE veljajo!
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "hisna": "...", "cifre_posamezno": ["...", "..."], "opomba": "..."}`;
  }
  if (file.includes('s160_mesec_wide')) {
    return `To je IZREZ LEVEGA DELA razprte strani KRSTNE matične knjige Podzemelj (leto 1882): MESEČNI STOLPEC z labelami + zaporedne številke + hišne številke. Datoteka = ${file}.
NALOGA: Za VSAKO vrstico OD ZGORAJ NAVZDOL preberi: zaporedna št. + MESEC-LABELA (če je vidna — napiši TOČNO besedo!) + dan rojstva + dan krsta.
KLJUČNO VPRAŠANJE: vrste z96–z103 (zap. 96–103) — ali ima VRSTA-1 (z96) MESEC-LABELO in kaj PIŠE: ‹November› ali ‹Dezember›?! (PRED tem blokom je z95-DEZEMBER-16 na prejšnji strani; DNEVI tukaj: 16,16,18,23,23,24,24,31 — November-NIMA-31.! če je labela 'Dezember' ALBO če je vrsta-1-BREZ-labele (carry-over iz z92-Dezember!) → blok je DEZEMBER!)
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "vrstice": [{"zap": "96", "labela_vidna": true, "mesec": "...", "rojen": "...", "krsten": "..."}], "sklep": "kratek-sklep-o-mesecu-z96–z103", "opomba": "..."}`;
  }
  if (file.includes('s147_dno')) {
    return `To je SPODNJI DEL razprte strani KRSTNE matične knjige Podzemelj (konec leta 1881). Datoteka = ${file}.
NALOGA:
1. Ali pod zadnjo vrstico (z89) obstaja ZAKLJUČNI MARKER: beseda ‹finis› / ‹Finitum› / ‹Summa› / ‹Anno 1881› / RAZPETE cifre '1 8 8 1' črez stolpce? Prepiši TOČNO kaj je napisano!
2. Preberi vse ročne pripise v tem območju.
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "zakljucni_marker": "...", "vsotna_cifre": "...", "pripisi": ["..."], "opomba": "..."}`;
  }
  if (file.includes('s157_pag2')) {
    return `To je ZGORNJI LEVI KOT razprte strani KRSTNE matične knjige Podzemelj (1882) z GOLO SVINČNO PAGINACIJO arhivarja. Datoteka = ${file}.
NALOGA: Preberi svinčno številko (2–3 cifre). ZNANI-DUEL: page-VLM-'154' vs-krop-'157' — pričakovano po seriji 'sken−6' = ‹151›! Kandidati: 151 / 154 / 157. POZOR: Kurrent 1 = ozka črtica, 4 = zankasta, 7 = γ-s-prečko, 5/6 zmeda!
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "paginacija": "...", "cifre_posamezno": ["..."], "opomba": "..."}`;
  }
  if (file.includes('s148_glava_zap')) {
    return `To je ZGORNJI DEL razprte strani KRSTNE matične knjige Podzemelj — MEJA-1881/82 (glava + prvi vpisi leta 1882). Datoteka = ${file}.
NALOGA:
1. Preberi LETNIČNO GLAVO: natisnjeno 'Jahr 18__' + ročno dopisane cifre. Ali so cifre RAZPETE/posebej velike (vsotna-stil)?
2. Ali je kakšen BESEDNI marker (Initium/Inicip annos Domini / Summa / finis ...)?
3. Preberi prve 2–3 vrstice: zaporedna št. + mesec + dan + vas + hišna + ime otroka.
Izhod: SAMO en veljaven JSON (brez ograj):
{"izrez": "${file}", "letnica_glava": "...", "razpete": "...", "besedni_markerji": ["..."], "vrstice": [{"zaporedna": "...", "mesec": "...", "rojen": "...", "vas": "...", "hisna": "...", "otrok": "..."}], "opomba": "..."}`;
  }
  return `To je ENA VRSTICA (izrez) razprte strani KRSTNE matične knjige župnije Podzemelj (leto 1882, Kurrent pisava). Datoteka = ${file}.
NALOGA — prepiši vrstico S ČIM VEČ NATAČNOSTJO: zaporedna št. (levi stolpec!), mesec+dan rojstva/krsta, vas (Griblje-ali-ne!), hišna št., ime otroka+spol, oče (ime+priimek+stan), mati (ime+roj.), botra/botri, duhovnik, POZNEJŠI-PRIPISI (modro/rdeče!).
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
      const summary = res.hisna ? `hisna=${res.hisna}` :
        res.vrstice ? `vrstic=${res.vrstice.length}${res.sklep ? ' | ' + String(res.sklep).slice(0, 90) : ''}` :
        res.paginacija ? `pag=${res.paginacija}` :
        res.zaporedna ? `zap=${res.zaporedna} vas=${res.vas} hisna=${res.hisna}` :
        res.zakljucni_marker !== undefined ? `marker=${String(res.zakljucni_marker).slice(0, 90)}` : JSON.stringify(res).slice(0, 90);
      console.log(`${f}: OK ${String(summary).slice(0, 160)}`);
    } catch (e) {
      console.error(`${f}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
