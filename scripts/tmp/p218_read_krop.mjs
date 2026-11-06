// P218 — generični KROP-reader (38 izrezov → JSON). Vzorec P217. Izhod: /tmp/p218/krop-reads/<ime>.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const DIR = '/tmp/p218/krop-grib';
const OUT = '/tmp/p218/krop-reads';
fs.mkdirSync(OUT, { recursive: true });

const ZAP_PROMPT = `To je LEVI ROB (stolpec zaporednih številk) skena mrliške matične knjige župnije Podzemelj (Kurrent pisava).
Preberi VSAKO zaporedno številko od zgoraj navzdol. POZOR KURRENT CIFRE: 4 ima ZANKO; 1 je OZKA ČRTICA; 7 ima prečko (γ-forma — NE zamenjaj z 8!); 5 je lahko podobna 6; 3/5/8 zmeda; 0 je široka elipsa; 9 ima DOLGI REP navzdol.
Odgovori SAMO z JSON: {"stevilke": ["...", ...], "opomba": "katera številka je negotova in zakaj"}`;

const ROW_PROMPT = `To je ena vrstica (ali del vrstice) mrliške matične knjige župnije Podzemelj (Kurrent pisava, nemški gotski vpliv).
Stolpci: mesec+dan smrti / dan pokopa | vas (npr. Griblje, Krasinec, Gradac, Podžemelj, Otok, Klošter/Kloster, Zemelj, Grem...) + hišna št. | ime, priimek, stan | vere/spola | starost (število + enota: J=let, M=mesecev, T=tednov, dni, uri) | bolezen/vzrok smrti | previden | podpis.
POZOR: Kurrent 3/5/8 zmeda; hišne številke: 4 ima zanko, 1 je ozka črtica, 7 = γ-forma s prečko! '½' = pol, '¼' = četrt (Gübler/Gütler = kmet-sosed; 'Kind' = otrok; 'Witwe' = vdova; 'Ablaber' = podkmet).
Preberi NATAČNO besedo za besedo; negotovo z [~], neberljivo z [?]. Odgovori SAMO z JSON:
{"zaporedna": "...", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "previden": "...", "duhovnik": "...", "opomba": "..."}`;

const PAS_PROMPT = `To je DESNI PAS 1–2 vrstic mrliške matične knjige Podzemelj (Kurrent, ZOOM!): stolpci starost / bolezen-vzrok / previden / podpis (morda tudi hišna št. če je v pasu).
POZOR KURRENT CIFRE: 4 ima ZANKO; 1 je OZKA ČRTICA; 7 ima prečko (γ!); 3/5/8 zmeda; 5≈6. Starost: J=let, M=Mt=mesecev, T=tednov, dni, uri.
Preberi ZGORNJO in SPODNJO vrstico (če sta 2) besedo za besedo; negotovo z [~]. Odgovori SAMO z JSON:
{"zgornja": {"starost": "...", "bolezen": "...", "previden": "..."}, "spodnja": {"starost": "...", "bolezen": "...", "previden": "..."}, "stolpci_v_pasu": "opis kateri stolpci so vidni", "opomba": "..."}`;

const PROMPTS = {
  arb_s11_meja: `To je MEJA-dokaz mrliške matične knjige Podzemelj (Kurrent): KONEC leta 1858 (tail-vrstice + VSOTNA-vrsta) in ZAČETEK leta 1859 (rokopisna LETNICA-glava + restart na zaporedno št. 1 + prve vrstice Jänner).
POMEMBNO: VSOTNA-vrsta leta 1858 lahko vsebuje RAZPETE CIFRE (npr. '1 8 5 9' čez stolpce = MARKER naslednjega leta!). Oceni: (a) katere tail-vrstice so vidne (zaporedne št. 54–57?), (b) kaj piše v vsotni vrsti, (c) rokopisna letnica-glava (pričakovano '1859'! — DUEL: prejšnja-VLM je brala tudi '1858'/'1857'!).
Odgovori SAMO z JSON: {"tail_vrstice": "opis (zaporedne št. + vasi)", "vsotna_vrsta": "natančen opis vsebine (cifre!)", "rokopisna_letnica": "natančno 4 cifre", "duel_1859_vs_1858": "katera-pravilna + zakaj (glyph-opis)", "restart_prva_vrstica": "vas + hišna + ime + starost", "opomba": "..."}`,
  s19_glava: `To je GLAVA skena mrliške matične knjige Podzemelj: NATISNJEN naslov 'Sterb-Buch.' (dvojni naslovni list novega zvezka!) + rokopisna LETNICA-glava + mesec December. Pričakovana letnica: 1859 (DUEL: prejšnja-VLM je brala '1857' na sosednji strani!).
Odgovori SAMO z JSON: {"natisnjen_naslov": "kaj točno piše", "rokopisna_letnica": "natančno 4 cifre", "duel_1859_vs_1857": "katera-pravilna + zakaj (glyph-opis)", "mesec": "...", "opomba": "..."}`,
  s11_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), MEJA-1858/59: zgorej TAIL-1858 (pričakovano 54–57), nato VSOTNA-vrsta (morda brez številke ali z vsoto), nato RESTART-1859 (pričakovano 1–7!). Preštej in preberi vsako!
Odgovori SAMO z JSON: {"stevilke": ["..."], "vsotna_lokacija": "kje je vsotna vrsta v stolpcu", "restart_kje": "pri kateri poziciji se začne 1", "opomba": "..."}`,
  s12_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), leto 1859 (nadaljevanje po restartu-z1–z7 na prejšnji strani!). Pričakovano: 8–20 (13 vrst). DUEL: ali je ZADNJA številka 19 ali 20 (nasilnja-stran se začne s 20!)? Oceni natančno!
Odgovori SAMO z JSON: {"stevilke": ["..."], "duel_zadnja_19_vs_20": "katera-pravilna + zakaj", "opomba": "..."}`,
  s13_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), leto 1859. Pričakovano: 20–33 (14 vrst) ALI 21–34 (če je 20 na prejšnji strani!). DUEL: PRVA številka 20-vs-21? + ali katerakoli številka MANJKA/SE PONOVI?
Odgovori SAMO z JSON: {"stevilke": ["..."], "duel_prva_20_vs_21": "katera-pravilna + zakaj", "opomba": "..."}`,
  s15_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), leto 1859. Pričakovano: 45–56 (12 vrst) ALI 45–55 (če je 56 na naslednji strani!). DUEL: ZADNJA številka 55-vs-56? Oceni natančno (5≈6-KURRENT-ZMEDA!)!
Odgovori SAMO z JSON: {"stevilke": ["..."], "duel_zadnja_55_vs_56": "katera-pravilna + zakaj (glyph-opis)", "opomba": "..."}`,
  s16_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), leto 1859. Pričakovano: 56–67 (12 vrst) ALI 57–67 (če je 56 na prejšnji strani!). DUEL: PRVA številka 56-vs-57? + rokopisna letnica-obroba pri glavi (pričakovano '1859' — prejšnja-VLM-brala-'1857'!).
Odgovori SAMO z JSON: {"stevilke": ["..."], "duel_prva_56_vs_57": "katera-pravilna + zakaj", "letnica_glava": "...", "opomba": "..."}`,
  s18_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent), leto 1859 (tail!). DUEL: prejšnja-VLM-brala-'90–100' — KROP-P217-potrjeno-'PRAVILNE-SO-80–91'! Ponovno oceni desetice 8-vs-9 za vsako številko (12 vrst)!
Odgovori SAMO z JSON: {"stevilke": ["..."], "duel_80_vs_90": "katera-pravilna + zakaj (glyph-opis prve cifre)", "opomba": "..."}`,
  s19_zap_stolpec: `To je LEVI ROB (zaporedne številke) skena mrliške matične knjige Podzemelj (Kurrent) — NASLOVNI-LIST-novega-zvezka ('Sterb-Buch.' natisnjen!), a duhovnik je NADALJEVAL-December-1859-vpise! Pričakovano: 93–103 (11 vrst; prejšnja-stran-konča-na-91! → ali je PRVA-92 ali 93? LUKNJA-92?) — ALI so številke drugačne (DUEL: P217-faza-je-pričakovala-z92–z112!)!
Odgovori SAMO z JSON: {"stevilke": ["..."], "duel_prva_92_vs_93": "katera-pravilna + zakaj", "zadnja_stevilka": "natančno", "opomba": "..."}`,
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
      if (attempt === 3) throw e;
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
