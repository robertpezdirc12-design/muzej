// P44 — issue #11: branje PZ strani 4–67 (tabele cenilnih razredov kultur).
// Deterministično upravljanje: vsaka stran en VLM klic, surovi izpisi v
// research/issue11/pz-raw/pz-NN.json (resume po obstoječih datotekah).
// 429 backoff: 60/120/240/480 s, max 5 poskusov na stran.
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

const PAGES_DIR = '/tmp/p44-pz-pages';
const RAW_DIR = 'research/issue11/pz-raw';
fs.mkdirSync(RAW_DIR, { recursive: true });

// strani 4–67 (64); že vzorčene strani (20/30/40/50/60) beremo znova z
// enotnim promptom 1. kroga — divergence iz issue #11 ostajajo odprte.
const LO = 4, HI = 67;
const PAGES = Array.from({ length: HI - LO + 1 }, (_, i) => LO + i);

function imgFor(page) {
  const f = path.join(PAGES_DIR, `pz-${String(page).padStart(2, '0')}.jpg`);
  if (!fs.existsSync(f)) throw new Error(`manjka slika: ${f}`);
  return fs.readFileSync(f).toString('base64');
}

const PROMPT = `To je stran ${'{PAGE}'} katastrskega cenilnega elaborata (PZ — "Catastral-Schätzungs-Elaborat") za občino Grüble/Griblje iz franciscejskega katastra 1825, napisana v nemški Kurrent pisavi z rdečimi rubrikami. Elaborat vsebuje: (a) §§ odseke po kulturah z narativnim opisom in majhnimi povzetkovnimi tabelami v fl/kr, (b) tiskane primerjalne obrazce "Resultate der benützten Behelfe" s pridelki po razredih (Metzen/Centner/Eimer), (c) del "Veranschlagung des Cultur-Aufwandes und Darstellung des Rein-Ertrages" s §§, ki se začnejo znova pri 1.

NALOGA: prepiši VSE tabele in številske vrstice na tej strani. Za vsako tabelo zapiši kulturo (npr. Ackerland, Wiesen, Weingärten, Gärten, Hutweide/Weiden, Bau-Area), oznako razreda (I, II, III, IV, ...), površino (Joch + Klafter; 1 Joch = 1600 kv. Klafter), vrednosti (fl/kr — Rob-Ertrag, Cultur-Aufwand, Rein-Ertrag, Tarif, Anschlag — kjer so), pridelke (Metzen/Centner/Eimer) in vsote (Summe/Total). Prepiši tudi § naslove in kratko vsebino narativa (1 stavek na §).

PRAVILA:
- Negotova branja označi z [~], neberljiva z [?]; ne izmišljuj števk
- Števke piši TOČNO kot so napisane (ne popravljaj aritmetike)
- Če je strani več tabel, prepiši vse; če je stran čista narativa brez tabel, to zapiši
- Ohrani vrstni red vrstic kot na strani

IZHOD: SAMO JSON (brez markdown oznak):
{
  "page": ${'{PAGE}'},
  "pageKind": "narrative+table" | "table" | "narrative" | "certification" | "blank" | "other",
  "sections": [
    {
      "culture": "kot zapisano",
      "par": "§. št. ali null",
      "narrativeBrief": "1 stavek ali null",
      "rows": [
        {
          "label": "razred/oznaka vrstice (I/II/III/Summe/...)",
          "areaJoch": "številka ali null ali [?]",
          "areaKlafter": "številka ali null ali [?]",
          "values": "fl/kr vrednosti točno kot zapisane (npr. 'Rob 16 fl 50½ kr; Rein 7 fl 35 kr') ali null",
          "yields": "pridelki (Metzen/Centner/Eimer) ali null",
          "rawText": "cela vrstica črka-za-črko (skrajšano na 120 znakov)",
          "confidence": "clear | ~ | ?"
        }
      ]
    }
  ],
  "pageNote": "berljivost strani, posebnosti (rdeči vpisi, prečrtave) v 1-2 stavkih"
}`;

async function readPage(zai, page, attempt = 1) {
  try {
    const completion = await zai.chat.completions.createVision({
      messages: [{ role: 'user', content: [
        { type: 'text', text: PROMPT.replace(/\{PAGE\}/g, String(page)) },
        { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${imgFor(page)}` } }
      ]}],
      thinking: { type: 'disabled' }
    });
    return { ok: completion.choices[0]?.message?.content ?? '' };
  } catch (e) {
    const msg = String(e.message || e);
    const is429 = /429|rate/i.test(msg);
    if (attempt < 5) {
      const wait = is429 ? 60 * Math.pow(2, attempt - 1) : 15;
      console.log(`  stran ${page}: poskus ${attempt} padel (${msg.slice(0, 80)}), čakam ${wait}s...`);
      await new Promise(r => setTimeout(r, wait * 1000));
      return readPage(zai, page, attempt + 1);
    }
    return { err: msg.slice(0, 200) };
  }
}

function extractJson(text) {
  // VLM lahko ovije izhod v ```json ...``` — olupi
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) return null;
  try { return JSON.parse(m[0]); } catch { return null; }
}

async function main() {
  const missing = PAGES.filter(p => !fs.existsSync(path.join(RAW_DIR, `pz-${String(p).padStart(2, '0')}.json`)));
  if (!missing.length) { console.log('vse strani 4–67 že prebrane'); return; }
  console.log(`P44 branje PZ: ${missing.length} strani od ${PAGES.length} (range ${LO}–${HI})`);
  const zai = await ZAI.create();
  let done = 0, failed = 0;
  for (const page of missing) {
    const t0 = Date.now();
    const r = await readPage(zai, page);
    const ms = Date.now() - t0;
    if (r.ok !== undefined) {
      const parsed = extractJson(r.ok);
      const out = {
        page,
        phase: 'p44-pass1',
        readAt: new Date().toISOString(),
        parseOk: parsed !== null,
        structured: parsed,
        raw: parsed ? undefined : r.ok.slice(0, 4000)
      };
      fs.writeFileSync(path.join(RAW_DIR, `pz-${String(page).padStart(2, '0')}.json`), JSON.stringify(out, null, 1));
      done++;
      console.log(`  [${done}/${missing.length}] pz-${page}: ${parsed ? 'JSON OK' : 'samo raw'} (${(ms / 1000).toFixed(0)}s)`);
    } else {
      failed++;
      console.log(`  [${done}/${missing.length}] pz-${page}: NAPAKA po 5 poskusih — ${r.err}`);
    }
  }
  console.log(`KONEC: ${done} prebranih, ${failed} spodletelih`);
}

main().catch(e => { console.error('FATAL:', e); process.exit(1); });
