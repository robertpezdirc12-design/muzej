// P215 — generični KROP-reader (23 izrezov → JSON). Vzorec: PROMPTS-po-imenu, createVision,
// thinking-disabled, 3-retry, 120s-timeout. Izhod: /tmp/p215/krop-reads/<ime>.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const DIR = '/tmp/p215/krop-grib';
const OUT = '/tmp/p215/krop-reads';
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
  arb_s30_vsota: `To je VSOTNA VRSTA mrliške matične knjige Podzemelj (Kurrent, ZOOM — LEVA STRAN razpona, konec leta 1861). Posamezne CIFRE so razporejene po stolpcih. HIPOTEZA: cifre = LETNICA '1862' razpeta čez stolpce (1|8|6|2)!
Odgovori SAMO z JSON: {"cifre_po_stolpcih": [{"stolpec": "...", "vrednost": "cifra"}], "tabela_cifer": "vse videne cifre levo→desno", "je_letnica_1862": "da/ne/morda + zakaj", "opomba": "..."}`,
  s30_vsota_desno: `To je DESNA STRAN vsotne vrste mrliške matične knjige Podzemelj (Kurrent, ZOOM — konec leta 1861). Cifre v stolpcih (pričakovano '6' in '2' — letnica '1862'!).
Odgovori SAMO z JSON: {"cifre_po_stolpcih": [{"stolpec": "...", "vrednost": "cifra"}], "tabela_cifer": "vse videne cifre levo→desno", "opomba": "..."}`,
  s30_zap_stolpec: `To je LEVI ROB (datum-stolpec + zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent). Pričakovanje: glava-letnica '1861' (bledo, nad November!) + vrste 49–54 (robovi delno odrezani). DUEL: prejšnja-VLM-branja '29–34' — oceni 4-vs-2-vs-5 natančno!
Odgovori SAMO z JSON: {"glava_letnica": "kaj piše v glavi (če je berljivo)", "stevilke": ["..."], "duel_49_vs_29": "katera-branja-pravilna + zakaj (glyph-opis)", "opomba": "..."}`,
  arb_s30_glava: `To je MEJA-dokaz mrliške matične knjige Podzemelj (Kurrent): VSOTNA-vrsta (cifri na levi strani!) + dvojna-črta + RESTART novega leta: 'Jänner' + prva vrstica (zaporedna št. 1, vas Podzemelj, Andreas Pezdirc). Ali je kje ročno vpisana LETNICA '1862'?
Odgovori SAMO z JSON: {"vsotna_cifri_levo": ["..."], "rokopisna_letnica_vidna": "da/ne + kje", "restart_mesec": "...", "restart_vrstica": "vas + hisna + ime", "opomba": "..."}`,
  z1_s30_pezdirc: ROW_PROMPT,
  z4_s30_grib: ROW_PROMPT,
  z54_s30_grib: ROW_PROMPT,
  z10_s31_grib: ROW_PROMPT,
  z11_s31_grib: ROW_PROMPT,
  z14_s31_grib: ROW_PROMPT,
  z17_s31_grib: ROW_PROMPT,
  z41_s34_grib: ROW_PROMPT,
  z43_s34_grib: ROW_PROMPT,
  z48_s34_grib: ROW_PROMPT,
  z50_s34_grib: ROW_PROMPT,
  z30_s32_grib: ROW_PROMPT,
  z4_s30_pas: PAS_PROMPT,
  z54_s30_pas: PAS_PROMPT,
  z1_s30_pas: PAS_PROMPT,
  z10_s31_pas: PAS_PROMPT,
  z11_s31_pas: PAS_PROMPT,
  z14_s31_pas: PAS_PROMPT,
  z17_s31_pas: PAS_PROMPT,
  z41_s34_pas: PAS_PROMPT,
  z43_s34_pas: PAS_PROMPT,
  z48_s34_pas: PAS_PROMPT,
  z50_s34_pas: PAS_PROMPT,
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
