// P219 — generični vzporedni VLM-reader (concurrency 3). Uporaba: bun p219_read_par.mjs traki|krop [filtri...]
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const MODE = process.argv[2] || 'traki';
const FILTER = process.argv.slice(3);

const DIR = MODE === 'traki' ? '/tmp/p219/traki' : '/tmp/p219/krop-grib';
const OUT = MODE === 'traki' ? '/tmp/p219/trak-reads' : '/tmp/p219/krop-reads';
fs.mkdirSync(OUT, { recursive: true });

const TRAK_PROMPT = `To je VODORAVNI TRAK (¼ strani razprtega naslovnega lista ali tabele) mrliške matične knjige župnije Podzemelj (Kurrent pisava, leto 1857/1858 — STAREJŠA pisava!). Vidni so lahko: letnica-glava (rokopisno diagonalno), mesec-glave (Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember — rokopisno čez vrsto), TABLE-VRSTICE, VSOTNA-vrsta (morda z RAZPETIMI CIFRAMI '1 8 5 8' ali '1 8 5 9' čez stolpce = P214-TIP-MARKER!), prazne vrste.
Stolpci vrstic: ZAPOREDNA ŠT. (levi rob, ročno!) | mesec+dan smrti / dan pokopa | vas + hišna št. | ime, priimek, stan | vere/spola (kljukice) | starost | bolezen/vzrok | previden | podpis.
POZOR KURRENT: 4-zanka; 1-ozka-črtica; 7-γ-s-prečko (NE 8!); 5≈6; 3/5/8-zmeda; 9-dolgi-rep. Hišne: ista pravila. '½'='pol', '¼'='četrt'.
PRAVILA:
- Prepiši VSAKO vidno table-vrstico od zgoraj navzdol. Preskoči mesečne glave (a jih OZNAČI v mesec_glave!).
- ZAPOREDNA ŠT. beri IZ LEVEGA ROBA! Če vrstica NIMA številke, zaporedna = "".
- Če je trak del NASLOVNEGA LISTA ('Sterb-Buch.' fraktura), to označi!
- Negotovo z [~], neberljivo z [?].
- Izhod: SAMO en veljaven JSON:
{"trak": "opis kaj je vidnega", "letnica_glava": "rokopisna letnica ali null", "mesec_glave": ["..."], "vrstice": [{"pozicija": 1, "zaporedna": "26", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "previden": "...", "duhovnik": "...", "opomba": "..."}], "opomba": "..."}`;

const ROW_PROMPT = `To je ena vrstica (ali del vrstice) mrliške matične knjige župnije Podzemelj (Kurrent pisava, 1857/1858 — STAREJŠA pisava!).
Stolpci: mesec+dan smrti / dan pokopa | vas (npr. Griblje, Krasinec, Gradac, Podžemelj, Otok, Klošter/Kloster, Zemelj, Grem, Dobravce, Cerkviče, Prilozje, Vranoviče, Goriče...) + hišna št. | ime, priimek, stan | vere/spola | starost (število + enota: J=let, M=mesecev, T=tednov, dni, uri) | bolezen/vzrok smrti | previden | podpis.
POZOR: Kurrent 3/5/8 zmeda; hišne številke: 4 ima zanko, 1 je ozka črtica, 7 = γ-forma s prečko! '½' = pol, '¼' = četrt (Gübler/Gütler = kmet-sosed; 'Kind' = otrok; 'Witwe' = vdova; 'Ablaber' = podkmet; 'Zwilling' = dvojček!).
Preberi NATAČNO besedo za besedo; negotovo z [~], neberljivo z [?]. Odgovori SAMO z JSON:
{"zaporedna": "...", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "previden": "...", "duhovnik": "...", "opomba": "..."}`;

const PAS_PROMPT_STR = `To je DESNI PAS 1–2 vrstic mrliške knjige Podzemelj (Kurrent, ZOOM!): starost / bolezen-vzrok / previden / podpis. Preberi besedo za besedo; negotovo z [~]. Odgovori SAMO z JSON: {"zgornja": {"starost": "...", "bolezen": "...", "previden": "...", "duhovnik": "..."}, "spodnja": {"starost": "...", "bolezen": "...", "previden": "...", "duhovnik": "..."}, "opomba": "..."}`;


const PROMPTS = {
  arb_s7_meja: `To je MEJA-dokaz mrliške matične knjige Podzemelj (Kurrent): KONEC leta 1857 (tail-vrstice December: pričakovano 2 vrstici — Gradac + GRIBLJE!) in ZAČETEK leta 1858 (VSOTNA-MARKER-vrsta + rokopisna LETNICA-glava '1858'? + RESTART na zaporedno št. 1 + prve vrstice Jänner).
POMEMBNO: VSOTNA-vrsta leta 1857 vsebuje RAZPETE CIFRE (pričakovano '1 8 5 8' čez stolpce = P214-TIP-MARKER naslednjega leta 1858!). Oceni: (a) katere tail-vrstice so vidne (zaporedne št. 73–74? vasi? imena?), (b) kaj točno piše v vsotni vrsti (cifre!), (c) rokopisna letnica-glava (DUEL '1858'-vs-'1857'-možen!).
Odgovori SAMO z JSON: {"tail_vrstice": "opis (zaporedne št. + vas + ime + starost)", "vsotna_vrsta": "natančen opis (cifre!)", "rokopisna_letnica": "natančno 4 cifre", "duel_1858_vs_1857": "katera-pravilna + zakaj (glyph-opis)", "restart_prva_vrstica": "vas + hišna + ime + starost", "opomba": "..."}`,
  arb_s9_glava: `To je GLAVA skena mrliške matične knjige Podzemelj (Kurrent): NASLOVNI LIST 'Sterb-Buch.' (natisnjeno!) + DIAGONALNA rokopisna LETNICA-glava čez prvo vrstico + prve vrstice (April?). Pričakovana letnica: 1858 (DUEL: '1859'-možen-misread — zadnja cifra 8-vs-9!).
Odgovori SAMO z JSON: {"natisnjen_naslov": "kaj piše", "rokopisna_letnica": "natančno 4 cifre", "duel_1858_vs_1859": "katera-pravilna + zakaj (glyph-opis zadnje cifre!)", "prva_vrstica": "mesec + dan + vas + ime", "opomba": "..."}`,
  arb_s10_glava: `To je GLAVA skena mrliške matične knjige Podzemelj (Kurrent): NASLOVNI LIST 'Sterb-Buch.' (natisnjeno!) + rokopisna letnica/glava + prve vrstice (Juni/July?). Pričakovano: nadaljevanje leta 1858 (vrstice ~40!). Oceni letnico in zaporedno št. prve vidne vrstice (DUEL: page-VLM-je-bral-'30'-KURRENT-3/4/5-ZMEDA!).
Odgovori SAMO z JSON: {"natisnjen_naslov": "kaj piše", "rokopisna_letnica": "letnica ali null", "prva_zaporedna": "natančno", "duel_40_vs_30": "katera-pravilna + zakaj (glyph-opis!)", "prva_vrstica": "mesec + dan + vas + ime", "opomba": "..."}`,
  arb_s11_meja: `To je MEJA-dokaz mrliške matične knjige Podzemelj (Kurrent): KONEC leta 1858 (tail-vrstice 54–57: Zemelj + Krasinec-×2 + Gradac — P218-potrjeno!) + VSOTNA-vrsta z RAZPETIMI CIFRAMI ('1 8 5 9' = MARKER-naslednjega-leta-1859!) + RESTART-1859 (z1–z7). Ponovno oceni: (a) tail-vrstice (zaporedne št. + vasi), (b) vsotna-vrsta (cifre!), (c) restart-prva-vrstica. GLYPH-ANALIZA: '1858'-tail-glava (BREZ-'9'!) + '1 8 5 9'-vsotna (P218-KROP-potrjeno!).
Odgovori SAMO z JSON: {"tail_vrstice": "opis (zaporedne št. + vasi + imena)", "vsotna_vrsta": "natančen opis (cifre!)", "rokopisna_letnica_tail": "natančno 4 cifre", "restart_prva_vrstica": "vas + hišna + ime + starost", "opomba": "..."}`,
  z15_s8_pas: PAS_PROMPT_STR,
  z17_s8_pas: PAS_PROMPT_STR,
  z27_s9_pas: PAS_PROMPT_STR,
  z39_s9_pas: PAS_PROMPT_STR,
  z52_s10_pas: PAS_PROMPT_STR,
  s8_r12_duh: `To je PODPIS duhovnika v eni vrstici mrliške knjige Podzemelj (Kurrent-ligatura). Preberi ime duhovnika (npr. 'Joh. Knavs', 'J. Skrbiec[?]', 'Jzef Mally[?]'). Odgovori SAMO z JSON: {"podpis": "...", "opomba": "..."}`,
  s9_r1_duh: `To je PODPIS duhovnika v eni vrstici mrliške knjige Podzemelj (Kurrent-ligatura). Preberi ime duhovnika. Odgovori SAMO z JSON: {"podpis": "...", "opomba": "..."}`,
  s10_r1_duh: `To je PODPIS duhovnika v eni vrstici mrliške knjige Podzemelj (Kurrent-ligatura). Preberi ime duhovnika. Odgovori SAMO z JSON: {"podpis": "...", "opomba": "..."}`,
  s7_zap_tail_kot: `To je SPODNJI-LEVI-KOT skena mrliške knjige Podzemelj (Kurrent): zadnje restart-vrstice Jänner 1858. Vidne številke: 8, 9, 10, 11 + ZADNJA-VRSTICA (datuma 29./31.) — ali ima ZADNJA vrstica številko ali je LEVI-STOLPEC-PRAZEN (NEŠTEVILČENA — pričakovano PRAZNO!)?
Odgovori SAMO z JSON: {"stevilke": ["8", "9", "10", "11", "..."], "zadnja_vrstica": "IMA-ŠTEVILKO ali PRAZNO (NEŠTEVILČENA!)", "opomba": "..."}`,
  arb_s8_glava: `To je GLAVA skena mrliške matične knjige Podzemelj (Kurrent): NASLOVNI LIST 'Sterb-Buch.' + DIAGONALNA rokopisna LETNICA-glava (pričakovano '1858'!) + prva vrstica (1. Februar).
Odgovori SAMO z JSON: {"rokopisna_letnica": "natančno 4 cifre", "duel_1858_vs_drugo": "glyph-opis", "prva_vrstica": "mesec + vas + ime", "opomba": "..."}`,
  s7_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), MEJA-1857/58: zgoraj TAIL-1857 (pričakovano 73–74!), nato VSOTNA-vrsta (morda z razpetimi '1 8 5 8'!), nato RESTART-1858 (pričakovano 1–12!). Preštej in preberi vsako! NE zamenjaj številke '74' z '71' (4-zanka!) ali '1' z '7'.
Odgovori SAMO z JSON: {"stevilke": ["..."], "vsotna_lokacija": "kje je vsotna vrsta", "restart_kje": "pri kateri poziciji se začne 1", "opomba": "..."}`,
  s8_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), leto 1858 (nadaljevanje po restartu-1–12 na prejšnji strani!). Pričakovano: 12–25 (14 vrst; ALI 13–25 = 13 vrst če je 12-duel na prejšnji strani!). DUEL: PRVA številka 12-vs-13? Oceni natančno (Kurrent-1/2/3!).
Odgovori SAMO z JSON: {"stevilke": ["..."], "duel_prva_12_vs_13": "katera-pravilna + zakaj", "opomba": "..."}`,
  s9_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), leto 1858 (April–Juni). Pričakovano: 26–39 (14 vrst). DUEL: PRVA številka 26-vs-18-vs-28 (Kurrent-2/8-ZMEDA!)? + ali katerakoli številka MANJKA/SE PONOVI?
Odgovori SAMO z JSON: {"stevilke": ["..."], "duel_prva": "katera-pravilna + zakaj", "opomba": "..."}`,
  s10_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), leto 1858 (July–October). Pričakovano: 40–53 (14 vrst). DUEL: PRVA številka 40-vs-30-vs-41 (Kurrent-3/4-ZMEDA — page-VLM-je-bral-'30–33'!)? Preštej VSE številke!
Odgovori SAMO z JSON: {"stevilke": ["..."], "duel_prva_40_vs_30": "katera-pravilna + zakaj", "opomba": "..."}`,
  s11_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), MEJA-1858/59: zgoraj TAIL-1858 (pričakovano 54–57 — P218-KROP-potrjeno!), nato VSOTNA ('1 8 5 9'-razpeto!), nato RESTART-1859 (1–7). Preštej in preberi vsako!
Odgovori SAMO z JSON: {"stevilke": ["..."], "vsotna_lokacija": "kje", "restart_kje": "pri kateri poziciji", "opomba": "..."}`,
};

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

const CONC = 2;

async function readOne(zai, name) {
  const out = `${OUT}/${name}.json`;
  if (fs.existsSync(out)) { console.log(`${name}: ŽE`); return; }
  const b64 = fs.readFileSync(`${DIR}/${name}.png`).toString('base64');
  const prompt = PROMPTS[name] || (MODE === 'traki' ? TRAK_PROMPT : ROW_PROMPT);
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      const completion = await Promise.race([
        zai.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 180000))
      ]);
      const c = completion?.choices?.[0]?.message?.content;
      if (!c) throw new Error('prazna vsebina');
      const res = parseContent(c);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      const zap = (res.vrstice || res.stevilke || []).map?.(v => (typeof v === 'string' ? v : v.zaporedna) || '·').join(',') ?? '';
      console.log(`${name}: OK n=${res.vrstice?.length ?? (res.stevilke?.length ?? '?')} zap=[${String(zap).slice(0, 90)}]`);
      return;
    } catch (e) {
      console.error(`  ${name}: poskus ${attempt} ni OK (${e.message})`);
      if (attempt === 4) console.error(`${name}: FAIL-KONČNO ${e.message}`);
      else await new Promise(r => setTimeout(r, 4000 * attempt));
    }
  }
}

async function main() {
  const inst = await ZAI.create();
  const names = fs.readdirSync(DIR).filter(f => f.endsWith('.png')).map(f => f.replace('.png', ''))
    .filter(n => FILTER.length === 0 || FILTER.includes(n)).sort();
  const q = [...names];
  const workers = Array.from({ length: CONC }, async () => {
    while (q.length) {
      const n = q.shift();
      await readOne(inst, n);
    }
  });
  await Promise.all(workers);
  console.log('P219 read-par done:', MODE);
}
main().catch(e => { console.error(e); process.exit(1); });
