// P214 — generični KROP-reader (23 izrezov → JSON). Vzorec: PROMPTS-po-imenu, createVision,
// thinking-disabled, 3-retry, 120s-timeout. Izhod: /tmp/p214/krop-reads/<ime>.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const DIR = '/tmp/p214/krop-grib';
const OUT = '/tmp/p214/krop-reads';
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
  arb_s35_vsota: `To je del mrliške matične knjige Podzemelj (Kurrent): VSOTNA VRSTA na koncu leta 1862 (vsota oseb po stolpcih — ver/spol/itd.) + zadnje vrstice leta 1862.
Odgovori SAMO z JSON: {"vsota_stolpci": ["vse številke v vsotni vrsti, levo→desno"], "zadnja_vrstica_1862": "ime + vas + datum", "opomba": "..."}`,
  arb_s35_glava: `To je MEJA-dokaz mrliške matične knjige Podzemelj (Kurrent): RESTART novega leta — ročno vpisana LETNICA (pričakovano '1863') + beseda 'Jänner' + prva vrstica novega leta (zaporedna št. 1).
Odgovori SAMO z JSON: {"rokopisna_letnica": "natančno 4 cifre", "prva_mesec_beseda": "...", "zaporedna_1_vrstica": "vas + hišna + ime + starost", "opomba": "..."}`,
  z27_hisna_tight: `To je STOLPEC hišnih številk (Haus No.) mrliške matične knjige Podzemelj (Kurrent, ULTRA-ZOOM 6×). POMEN: DUEL med branjema '11' / '21' / '31'!
KURRENT CIFRE: 1 = OZKA ČRTICA brez zanke in brez zastavice; 2 = zanka-spodaj+reber-zgoraj; 3 = dva loka desno; 4 ima ZANKO; 7 = γ-forma s prečko.
Odgovori SAMO z JSON: {"stevilka": "najbolj verjetna", "prva_cifra": "1 ali 2 ali 3 — zakaj (glyph-opis)", "druga_cifra": "1 ali 2 ali 4 — zakaj", "alternativa": "druga možnost + zakaj", "opomba": "..."}`,
  z38_alter_tight: `To je STOLPEC starosti (Alter) mrliške matične knjige Podzemelj (Kurrent, ULTRA-ZOOM). Pričakovano: starost dojenčka (npr. '3 ½ J' ali '3 J' ali '3 J 4 M' ali tedni/dni).
Odgovori SAMO z JSON: {"starost": "natančno kaj piše (številka + enota)", "opomba": "..."}`,
  z12_bolezen_tight: `To je STOLPEC bolezni (Krankheit und Todesart) mrliške matične knjige Podzemelj (Kurrent, ZOOM). Vrstica ima 2 pisani vrstici (nemško).
Odgovori SAMO z JSON: {"vrstica1": "...", "vrstica2": "...", "skupaj": "najbolj verjeten nemški izraz", "prevod": "slovensko", "opomba": "..."}`,
  z38_bolezen_tight: `To je STOLPEC bolezni (Krankheit und Todesart) mrliške matične knjige Podzemelj (Kurrent, ZOOM). Pričakovano: 'Dreienßucht' ali podobno (driska-sucht?).
Odgovori SAMO z JSON: {"bolezen": "natančno kaj piše", "prevod": "slovensko", "opomba": "..."}`,
  z2_bolezen_tight2: `To je STOLPEC bolezni (Krankheit und Todesart) mrliške matične knjige Podzemelj (Kurrent, ZOOM). DUEL: 'Gehirnentzündung' (vnetje možganov) vs 'Gichtschmerzen' (protične bolečine) — dolga beseda!
Odgovori SAMO z JSON: {"bolezen": "katera od dveh (ali tretja možnost)", "obrazložitev": "glyph-dokaz (dolžina, začetni črki, konec -ung/-n)", "opomba": "..."}`,
  z12_opomba_tight: `To je STOLPEC opomb (Anmerkung) mrliške matične knjige Podzemelj (Kurrent, ULTRA-ZOOM). Kaj je ročno dopisano?
Odgovori SAMO z JSON: {"opomba": "natančno kaj piše", "prevod": "slovensko", "opomba2": "..."}`,
  s35_vsota_tight: `To je VSOTNA VRSTA mrliške matične knjige Podzemelj (Kurrent, ZOOM — LEVA STRAN razpona). V njej so posamezne CIFRE razporejene po stolpcih. HIPOTEZA: cifre = LETNICA ('1','8','6','3') razpeta čez stolpce!
Odgovori SAMO z JSON: {"cifre_po_stolpcih": [{"stolpec": "zap/Land/Name/...", "vrednost": "cifra"}], "tabela_cifer": "vse videne cifre levo→desno", "je_letnica_1863": "da/ne/morda + zakaj", "opomba": "..."}`,
  s35_vsota_desno: `To je DESNA STRAN vsotne vrste mrliške matične knjige Podzemelj (Kurrent, ZOOM). Cifre v stolpcih Alter/Krankheit/Priester.
Odgovori SAMO z JSON: {"cifre_po_stolpcih": [{"stolpec": "Alter/Versehen/Priester/...", "vrednost": "cifra"}], "tabela_cifer": "vse videne cifre levo→desno", "opomba": "..."}`,
  s39_vsota_tight: `To je VSOTNA VRSTA mrliške matične knjige Podzemelj (Kurrent, ZOOM — LEVA STRAN). HIPOTEZA: cifre = LETNICA '1864' razpeta čez stolpce (1|8|6|4)!
Odgovori SAMO z JSON: {"cifre_po_stolpcih": [{"stolpec": "...", "vrednost": "cifra"}], "tabela_cifer": "vse videne cifre levo→desno", "je_letnica_1864": "da/ne/morda + zakaj", "opomba": "..."}`,
  s39_vsota_desno: `To je DESNA STRAN vsotne vrste mrliške matične knjige Podzemelj (Kurrent, ZOOM). Cifre v stolpcih Alter/Krankheit/Priester (pričakovano '6' in '4'!).
Odgovori SAMO z JSON: {"cifre_po_stolpcih": [{"stolpec": "...", "vrednost": "cifra"}], "tabela_cifer": "vse videne cifre levo→desno", "opomba": "..."}`,
  z64_datumi_tight: `To je DATUMSKI STOLPEC (Jahr, Monat und Tag) mrliške matične knjige Podzemelj (Kurrent, ULTRA-ZOOM 6×). Pričakovan DOKAZ: smrt '31. Dec 1863' + pokop '2. Jänner 1864' — EKSPLICITNI LETNICI čez mejnik let!
Odgovori SAMO z JSON: {"datum_smrti": "natančno (vključno z letnico če je)", "datum_pokopa": "natančno (vključno z letnico če je)", "eksplicitni_letnici": "kateri letnici sta zapisani", "opomba": "..."}`,
  z2_s35_grib: ROW_PROMPT,
  z12_s36_grib: ROW_PROMPT,
  z18_s36_grib: ROW_PROMPT,
  z26_s37_grib: ROW_PROMPT,
  z27_s37_grib: ROW_PROMPT,
  z33_s37_grib: ROW_PROMPT,
  z38_s37_grib: ROW_PROMPT,
  z2_s35_pas: PAS_PROMPT,
  z12_s36_pas: PAS_PROMPT,
  z18_s36_pas: PAS_PROMPT,
  z26_s37_pas: PAS_PROMPT,
  z27_s37_pas: PAS_PROMPT,
  z33_s37_pas: PAS_PROMPT,
  z38_s37_pas: PAS_PROMPT,
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
