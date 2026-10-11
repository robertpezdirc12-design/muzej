// P44 — 2. krog: ciljna ponovna branja ključnih strani (vsota/razred tabele).
// Strani: 25, 63, 65, 67 (vsote), 12/13/15 (odrezani izpisi), 50 (divergentna).
// Rezultati v research/issue11/pz-raw/pz-NN-pass2.json
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

const PAGES_DIR = '/tmp/p44-pz-pages';
const RAW_DIR = 'research/issue11/pz-raw';

const TASKS = [
  {
    page: 67,
    why: 'REKAPITULACIJA Endresultate — vsota vrstic 1037 j ≠ Summa 1152 j → manjkajo razredi',
    prompt: `To je REKAPITULACIJSKA tabela "Specifischer Ausweis der Endresultate" (Veranschlagung des Cultur-Aufwandes und Darstellung des Rein-Ertrages) za občino Grüble. Preberi VSAKO vrstico tabele od zgoraj navzdol — pričakovanih je 12–16 vrstic razredov (Acker I/II/III, Wiesen I/II/III, Gärten več vrst, Weingärten, Hutweiden, Weiden mit Holznutzung, Bauarea, ...) + zaključna vrstica Summa.

Stolpci so približno: Culturgattung | Classe | Fläche (Joch, Klafter) | Brutto-Ertrag pro Joch (fl, kr) | Brutto-Ertrag im Ganzen (fl, kr) | Cultur-Aufwand/Compensation pro Joch | Rein-Ertrag pro Joch (fl, kr) | Rein-Ertrag der Classe (fl, kr) | Rein-Ertrag der Culturgattung.

ZNANE KONTROLE (iz 1. kroga): Summa ≈ 1152 Joch 495 Klafter; Bruto skupaj ≈ 8872 fl 5¾ kr; Rein skupaj ≈ 4492 fl 51 kr; Acker I ≈ 80 j 842 kl; Acker II ≈ 234 j 120 kl.

IZHOD: SAMO veljaven JSON brez markdown:
{"page":67,"rows":[{"culture":"...","class":"I/II/III/C/-","areaJoch":st_ali_null,"areaKlafter":st_ali_null,"bruttoPerJoch":"fl/kr kot zapisano","bruttoTotal":"fl/kr","compensation":"fl/kr","reinPerJoch":"fl/kr","reinClasse":"fl/kr","reinGattung":"fl/kr ali null","confidence":"clear|~|?"}],"summa":{"areaJoch":st,"areaKlafter":st,"bruttoTotal":"fl/kr","reinTotal":"fl/kr","confidence":"..."},"rowCount":st,"pageNote":"1-2 stavka o berljivosti"}
V nizih NE uporabljaj narekovajev ", uporabljaj ' ali »«.`
  },
  {
    page: 63,
    why: 'velika tabela parcel s Pacht (Acker I/II, Wiesen, Weingärten) — razjasni stolpce',
    prompt: `To je velika ročna tabela parcel z najemninami (Pacht) za občino Grüble — verjetno "Darstellung" za Acker I. Klasse, II. Klasse, Wiesen, Weingärten. Vsaka vrstica: zaporedna številka parcele, površina (Joch + Klafter ALI samo Klafter?), Pacht zneski (fl, kr), mogoče "Gleichheit" stolpec.

PREBERI: (1) natančne NASLOVE stolpcev/tabel na strani (rdeče rubrike!), (2) VSE vrstice parcel (pričakovanih 15–25), (3) vsote (Summe) na dnu vsake tabele.

ZNANA KONTROLA (1. krog): 16 vrstic; števke kot 457, 759, 727, 443, 252, 1128, 68, 969 — razjasni, ali so to Klafter površine, Pacht v kr, ali kaj drugega.

IZHOD: SAMO veljaven JSON brez markdown:
{"page":63,"tables":[{"title":"naslov tabele kot zapisan","columns":"opis stolpcev po vrstnem redu","rows":[{"no":st_ali_null,"label":"...","areaJoch":st_ali_null,"areaKlafter":st_ali_null,"pacht":"fl/kr","other":"drugo","raw":"cela vrstica skrajšana na 100 znakov","confidence":"clear|~|?"}],"summe":"vsota tabele ali null"}],"pageNote":"1-2 stavka"}
V nizih NE uporabljaj narekovajev ", uporabljaj ' ali »«.`
  },
  {
    page: 65,
    why: 'Hutweide tabela (12 vrstic) — površine razredov pašnikov',
    prompt: `To je velika tabela za Hutweide/Weide (pašnike) za občino Grüble — verjetno "Specifischer Ausweis" ali "Darstellung" z vrsticami po parcelah/razredih (npr. Land Nr. 1, 2, ...). Vsaka vrstica ima lahko: zaporedno št., ime/lokalno ime, površino (Joch + Klafter), Brutto-Ertrag, Cultur-Aufwand, Rein-Ertrag (fl/kr).

PREBERI: (1) naslove stolpcev (rdeče rubrike), (2) VSE vrstice (pričakovanih 10–15), (3) vsote na dnu.

ZNANA KONTROLA (1. krog): vrstice "1. Land 22 j 463 kl", "18 j 547 kl", Pacht/Ertrag zneski; PV pravi Weiden = 636 j 263 kl skupno.

IZHOD: SAMO veljaven JSON brez markdown:
{"page":65,"tableTitle":"naslov","columns":"opis stolpcev","rows":[{"no":st_ali_null,"name":"ime/oznaka","areaJoch":st_ali_null,"areaKlafter":st_ali_null,"values":"fl/kr zneski točno","raw":"cela vrstica do 100 znakov","confidence":"clear|~|?"}],"summe":"vsota ali null","pageNote":"1-2 stavka"}
V nizih NE uporabljaj narekovajev ", uporabljaj ' ali »«.`
  },
  {
    page: 25,
    why: 'rdeče popravljene vsote (388 j 946 kl / 1980 kl) — kontekst',
    prompt: `To je stran elaborata Grüble z rdeče popravljeno površinsko vsoto (1. krog je prebral ~388 Joch 946 Klafter in ~1980 Klafter). Preberi: (1) kateri §§ naslovi so na strani, (2) VSE številske vnose (površine Joch/Klafter, zneski fl/kr) TOČNO, (3) kaj rdeči vpisi popravljajo.

IZHOD: SAMO veljaven JSON brez markdown:
{"page":25,"sections":[{"title":"naslov/§","rows":[{"label":"...","areaJoch":st_ali_null,"areaKlafter":st_ali_null,"values":"fl/kr ali opis","raw":"vrstica do 100 znakov","confidence":"clear|~|?"}]}],"redInk":"kaj pomenijo rdeči vpisi (1 stavek)","pageNote":"1 stavek"}
V nizih NE uporabljaj narekovajev ", uporabljaj ' ali »«.`
  },
  { page: 12, why: 'odrezan izpis 1. kroga — celostno ponovno branje', prompt: null },
  { page: 13, why: 'odrezan izpis 1. kroga — celostno ponovno branje', prompt: null },
  { page: 15, why: 'odrezan izpis 1. kroga — celostno ponovno branje', prompt: null },
  {
    page: 50,
    why: 'zgodovinsko divergentna stran (Acker razred I: 3 branja se razhajajo)',
    prompt: `To je stran "Veranschlagung des Cultur-Aufwandes und Darstellung des Rein-Ertrages" §. 1 za Ackerland razred I. Zgodovinska težava: TRI prejšnja branja se RAZHAJAJO (Rob-Ertrag 20 ali 25 fl 44 kr; Anschlag 8 fl 10½ / 10 fl 30½ / 10 fl 41½; Rein-Ertrag 12/13/15 fl 5 kr) in NOBENA kombinacija ni aritmetično konsistentna.

PREBERI ZDOBAVNO vsako števko: (1) § naslov, (2) VSAKO številsko vrstico (Rob-Ertrag/Gesammt-Ertrag, Cultur-Aufwand, Tarif/somernost, Anschlag, Rein-Ertrag — pro Joch in im Ganzen), (3) preveri seštevanje/odštevanje v glavi in zapiši obe strani računa.

IZHOD: SAMO veljaven JSON brez markdown:
{"page":50,"rows":[{"label":"Rob-Ertrag pro Joch","fl":st_ali_null,"kr":"npr. 44 ali 44½","raw":"kot zapisano","confidence":"clear|~|?"}],"arithmetic":"zapisani račun po besedilu (npr. 20 fl 44 kr − 8 fl 39 kr = 12 fl 5 kr)","pageNote":"1-2 stavka"}
V nizih NE uporabljaj narekovajev ", uporabljaj ' ali »«.`
  },
];

const DEFAULT_PROMPT = (page) => `To je stran ${page} katastrskega cenilnega elaborata (PZ) za občino Grüble 1825, nemška Kurrent pisava. Prepiši VSE tabele in številske vrstice (kulture, razredi, površine Joch/Klafter, zneski fl/kr, pridelki Metzen/Centner/Eimer, vsote). Negotova mesta označi [~], neberljiva [?]. Ohrani vrstni red.

IZHOD: SAMO veljaven JSON brez markdown:
{"page":${page},"pageKind":"narrative|table|narrative+table|certification|other","sections":[{"culture":"...","par":"§ ali null","rows":[{"label":"...","areaJoch":st_ali_null,"areaKlafter":st_ali_null,"values":"fl/kr ali opis","yields":"pridelki ali null","raw":"vrstica do 100 znakov","confidence":"clear|~|?"}]}],"pageNote":"1-2 stavka"}
V nizih NE uporabljaj narekovajev ", uporabljaj ' ali »«.`;

function imgFor(page) {
  return fs.readFileSync(path.join(PAGES_DIR, `pz-${String(page).padStart(2, '0')}.jpg`)).toString('base64');
}

function extractJson(text) {
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) return null;
  let t = m[0];
  try { return JSON.parse(t); } catch {}
  // poskus: odstrani sledilne vejice, ubegnjene narekovaje pusti
  try { return JSON.parse(t.replace(/,(\s*[}\]])/g, '$1')); } catch {}
  return null;
}

async function read(zai, page, prompt, attempt = 1) {
  try {
    const c = await zai.chat.completions.createVision({
      messages: [{ role: 'user', content: [
        { type: 'text', text: prompt },
        { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${imgFor(page)}` } }
      ]}],
      thinking: { type: 'disabled' }
    });
    return { ok: c.choices[0]?.message?.content ?? '' };
  } catch (e) {
    if (attempt < 5) {
      const wait = /429|rate/i.test(String(e.message)) ? 60 * Math.pow(2, attempt - 1) : 15;
      console.log(`  p${page}: poskus ${attempt} padel, čakam ${wait}s`);
      await new Promise(r => setTimeout(r, wait * 1000));
      return read(zai, page, prompt, attempt + 1);
    }
    return { err: String(e.message).slice(0, 200) };
  }
}

async function main() {
  const zai = await ZAI.create();
  for (const t of TASKS) {
    const out = `research/issue11/pz-raw/pz-${String(t.page).padStart(2, '0')}-pass2.json`;
    if (fs.existsSync(out)) { console.log(`p${t.page}: pass2 že obstaja`); continue; }
    const prompt = t.prompt ?? DEFAULT_PROMPT(t.page);
    const r = await read(zai, t.page, prompt);
    if (r.ok !== undefined) {
      const parsed = extractJson(r.ok);
      fs.writeFileSync(out, JSON.stringify({
        page: t.page, phase: 'p44-pass2', why: t.why,
        readAt: new Date().toISOString(), parseOk: parsed !== null,
        structured: parsed, raw: parsed ? undefined : r.ok.slice(0, 8000)
      }, null, 1));
      console.log(`p${t.page}: ${parsed ? 'JSON OK' : 'samo raw'} (${t.why.slice(0, 40)}...)`);
    } else {
      console.log(`p${t.page}: NAPAKA — ${r.err}`);
    }
  }
}
main().catch(e => { console.error('FATAL', e); process.exit(1); });
