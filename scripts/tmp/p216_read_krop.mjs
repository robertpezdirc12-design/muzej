// P216 — generični KROP-reader (23 izrezov → JSON). Vzorec: PROMPTS-po-imenu, createVision,
// thinking-disabled, 3-retry, 120s-timeout. Izhod: /tmp/p216/krop-reads/<ime>.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const DIR = '/tmp/p216/krop-grib';
const OUT = '/tmp/p216/krop-reads';
fs.mkdirSync(OUT, { recursive: true });

const ZAP_PROMPT = `To je LEVI ROB (stolpec zaporednih številk) skena mrliške matične knjige župnije Podzemelj (Kurrent pisava).
Preberi VSAKO zaporedno številko od zgoraj navzdol. POZOR KURRENT CIFRE: 4 ima ZANKO; 1 je OZKA ČRTICA; 7 ima prečko (γ-forma — NE zamenjaj z 8!); 5 je lahko podobna 6; 3/5/8 zmeda; 0 je široka elipsa.
Odgovori SAMO z JSON: {"stevilke": ["...", ...], "opomba": "katera številka je negotova in zakaj"}`;

const ROW_PROMPT = `To je ena vrstica (ali del vrstice) mrliške matične knjige župnije Podzemelj (Kurrent pisava, nemški gotski vpliv).
Stolpci: mesec+dan smrti / dan pokopa | vas (npr. Griblje, Krasinec, Gradac, Podžemelj, Otok, Klošter/Kloster, Zemelj, Grem...) + hišna št. | ime, priimek, stan | vere/spola | starost (število + enota: J=let, M=mesecev, T=tednov, dni, uri) | bolezen/vzrok smrti | previden | podpis.
POZOR: Kurrent 3/5/8 zmeda; hišne številke: 4 ima zanko, 1 je ozka črtica, 7 = γ-forma s prečko! '½' = pol, '¼' = četrt (Gübler/Gütler = kmet-sosed; 'Kind' = otrok; 'Witwe' = vdova).
Preberi NATAČNO besedo za besedo; negotovo z [~], neberljivo z [?]. Odgovori SAMO z JSON:
{"zaporedna": "...", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "previden": "...", "duhovnik": "...", "opomba": "..."}`;

const PAS_PROMPT = `To je DESNI PAS 1–2 vrstic mrliške matične knjige Podzemelj (Kurrent, ZOOM!): stolpci starost / bolezen-vzrok / previden / podpis (morda tudi hišna št. če je v pasu).
POZOR KURRENT CIFRE: 4 ima ZANKO; 1 je OZKA ČRTICA; 7 ima prečko (γ!); 3/5/8 zmeda; 5≈6. Starost: J=let, M=Mt=mesecev, T=tednov, dni, uri.
Preberi ZGORNJO in SPODNJO vrstico (če sta 2) besedo za besedo; negotovo z [~]. Odgovori SAMO z JSON:
{"zgornja": {"starost": "...", "bolezen": "...", "previden": "..."}, "spodnja": {"starost": "...", "bolezen": "...", "previden": "..."}, "stolpci_v_pasu": "opis kateri stolpci so vidni", "opomba": "..."}`;

const PROMPTS = {
  arb_s25_vsota: `To je VSOTNA VRSTA mrliške matične knjige Podzemelj (Kurrent, ZOOM — LEVA STRAN razpona, konec leta 1860). Posamezne CIFRE so razporejene po stolpcih. HIPOTEZA: cifre = LETNICA '1861' razpeta čez stolpce (1|8|6|1)! Pod njo je vidna rokopisna glava '1861' + 'Jänner'.
Odgovori SAMO z JSON: {"cifre_po_stolpcih": [{"stolpec": "...", "vrednost": "cifra"}], "rokopisna_glava": "kaj piše pod vsotno (letnica + mesec)", "je_letnica_1861": "da/ne/morda + zakaj", "opomba": "..."}`,
  arb_s25_glava: `To je MEJA-dokaz mrliške matične knjige Podzemelj (Kurrent): rokopisna LETNICA-gava (pričakovano '1861') + 'Jänner' + prva vrstica novega leta (zaporedna št. 1).
Odgovori SAMO z JSON: {"rokopisna_letnica": "natančno 4 cifre", "prva_mesec_beseda": "...", "zaporedna_1_vrstica": "vas + hišna + ime + starost", "opomba": "..."}`,
  z1_s25_restart: `To je RESTART-vrstica novega leta mrliške matične knjige Podzemelj (Kurrent): zaporedna št. 1, Jänner, vas, hišna št., ime, stan, starost, bolezen.
Odgovori SAMO z JSON: {"zaporedna": "1", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "previden": "...", "duhovnik": "...", "opomba": "..."}`,
  s23_zap_stolpec: `To je LEVI ROB (zaporedne številke + datumi) skena mrliške matične knjige Podzemelj (Kurrent), leto 1860. Pričakovanje: glava '1860' + vrste 40–52 (ali 41–53 — DUEL!). Datum vrste 1 = July 20/21.
Odgovori SAMO z JSON: {"glava_letnica": "...", "stevilke": ["..."], "prva_vrsta_margin": "40 ali 41 ali drugo + zakaj", "opomba": "..."}`,
  s24_zap_stolpec: `To je LEVI ROB (zaporedne številke + datumi) skena mrliške matične knjige Podzemelj (Kurrent), leto 1860. Pričakovanje: glava '1860' + vrste 53–66! Datum vrste 1 = '27. | 28.' — kateri MESEC (avgust-nadaljevanje ali september-glava šele pri vrsti 2)?
Odgovori SAMO z JSON: {"glava_letnica": "...", "stevilke": ["..."], "prva_vrsta_mesec": "avgust ali september + zakaj (kje stoji 'September'-glava)", "opomba": "..."}`,
  s25_zap_stolpec: `To je LEVI ROB (zaporedne številke + datumi) skena mrliške matične knjige Podzemelj (Kurrent), konec 1860. Pričakovanje: tail-vrste z margini 53–59 (napaka-v-registru: prejšnja-stran-že-ima-53–66!) + vsotna-vrsta z marginom '60' + restart 1–5 z glavo '1861'!
Odgovori SAMO z JSON: {"glava_letnica": "...", "tail_stevilke": ["..."], "vsotna_margin": "...", "restart_stevilke": ["..."], "opomba": "..."}`,
  s25_zap_tight: `To je ULTRA-ZOOM levega roba mrliške matične knjige Podzemelj (Kurrent): zaporedne številke tail-vrst (pričakovano 53, 54, 55, 56, 57, 58, 59) + margin vsotne vrste (pričakovano '60')!
Odgovori SAMO z JSON: {"stevilke": ["..."], "vsotna_margin": "...", "opomba": "..."}`,
  z7_s26_grib: ROW_PROMPT,
  z11_s26_grib: ROW_PROMPT,
  z14_s26_grib: ROW_PROMPT,
  z15_s26_grib: ROW_PROMPT,
  z17_s26_grib: ROW_PROMPT,
  z18_s26_grib: ROW_PROMPT,
  z20_s28_grib: ROW_PROMPT,
  z30_s28_grib: ROW_PROMPT,
  z32_s28_grib: ROW_PROMPT,
  z61_s24_grib: ROW_PROMPT,
  z65_s24_grib: ROW_PROMPT,
  z7_s26_pas: PAS_PROMPT,
  z11_s26_pas: PAS_PROMPT,
  z14_s26_pas: PAS_PROMPT,
  z15_s26_pas: PAS_PROMPT,
  z17_s26_pas: PAS_PROMPT,
  z20_s28_pas: PAS_PROMPT,
  z30_s28_pas: PAS_PROMPT,
  z32_s28_pas: PAS_PROMPT,
};

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readKrop(zai, name) {
  const b64 = fs.readFileSync(`${DIR}/${name}.png`).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: PROMPTS[name] || ROW_PROMPT },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  for (let attempt = 1; attempt <= 3; attempt++) {
    const completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 120000))
    ]);
    try {
      const c = completion?.choices?.[0]?.message?.content;
      if (!c) throw new Error('prazna vsebina');
      return parseContent(c);
    } catch (e) {
      console.error(`  ${name}: poskus ${attempt} ni OK (${e.message})`);
      if (attempt === 4) throw e;
      await new Promise(r => setTimeout(r, 3000 * attempt));
    }
  }
}

async function main() {
  const FILTER = process.argv.slice(2);
  const names = fs.readdirSync(DIR).filter(f => f.endsWith('.png')).map(f => f.replace('.png', ''))
    .filter(n => FILTER.length === 0 || FILTER.includes(n)).sort();
  const inst = await ZAI.create();
  for (const name of names) {
    const out = `${OUT}/${name}.json`;
    if (fs.existsSync(out)) { console.log(`${name}: ŽE`); continue; }
    try {
      const res = await readKrop(inst, name);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      console.log(`${name}: OK ${JSON.stringify(res).slice(0, 110)}`);
    } catch (e) {
      console.error(`${name}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
