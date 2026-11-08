// P44 — 2b krog: p67 razrez na polovice (zgornja/spodnja) za natančnejše branje
// rekapitulacijske tabele. Zgornja polovica: naslov + prvi razredi; spodnja: ostali + Summa.
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const PAGES_DIR = '/tmp/p44-pz-pages';
const RAW_DIR = 'research/issue11/pz-raw';

const PROMPT = `To je ${'{DEEL}'} STRAN REKAPITULACIJSKE TABELE "Veranschlagung des Cultur-Aufwandes und Darstellung des Rein-Ertrages" (Specifischer Ausweis der Endresultate) za občino Grüble, nemška Kurrent pisava. Tabela ima stolpce: Culturgattung | Classe | Fläche (Joch, Klafter) | Brutto-Ertrag pro Joch (fl,kr) | Brutto im Ganzen (fl,kr) | Compensation pro Joch | Rein-Ertrag pro Joch (fl,kr) | Rein-Ertrag der Classe (fl,kr) | Rein-Ertrag der Culturgattung (fl,kr).

Preberi VSAKO vrstico, ki je Vsaj delno vidna na tej ${'{DEEL}'} strani — tudi vrstice, ki so odrezane na robu (dopiši manjkajoče dele z [~]). Row-count za celo tabelo naj bo 12–16 razredov (Acker I–IV, Wiesen I–III, Kleine/Größere Gärten, Weingärten, Hutweiden, Weiden mit Holznutzung, Bauarea, ...).

IZHOD: SAMO veljaven JSON brez markdown:
{"part":"${'{DEEL}'}","rows":[{"culture":"...","class":"...","areaJoch":st_ali_null,"areaKlafter":st_ali_null,"bruttoPerJoch":"...","bruttoTotal":"...","compensation":"...","reinPerJoch":"...","reinClasse":"...","reinGattung":"... ali null","confidence":"clear|~|?"}],"visibleRowCount":st,"pageNote":"1 stavek"}
V nizih NE uporabljaj narekovajev ", uporabljaj ' ali »«.`;

function prep(page, part) {
  const src = path.join(PAGES_DIR, `pz-${String(page).padStart(2, '0')}.jpg`);
  const out = `/tmp/p44-pz-${page}-${part}.jpg`;
  if (part === 'zgornja') {
    execSync(`python3 -c "from PIL import Image; im=Image.open('${src}'); w,h=im.size; im.crop((0,0,w,int(h*0.55))).save('${out}', quality=94)"`);
  } else {
    execSync(`python3 -c "from PIL import Image; im=Image.open('${src}'); w,h=im.size; im.crop((0,int(h*0.45),w,h)).save('${out}', quality=94)"`);
  }
  return fs.readFileSync(out).toString('base64');
}

function extractJson(text) {
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) return null;
  try { return JSON.parse(m[0]); } catch {}
  try { return JSON.parse(m[0].replace(/,(\s*[}\]])/g, '$1')); } catch {}
  return null;
}

async function main() {
  const zai = await ZAI.create();
  for (const part of ['zgornja', 'spodnja']) {
    const out = `research/issue11/pz-raw/pz-67-half-${part}.json`;
    if (fs.existsSync(out)) { console.log(`${part}: že obstaja`); continue; }
    const prompt = PROMPT.replaceAll('{DEEL}', part.toUpperCase());
    const b64 = prep(67, part);
    let ok = false;
    for (let a = 1; a <= 4 && !ok; a++) {
      try {
        const c = await zai.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        });
        const parsed = extractJson(c.choices[0]?.message?.content ?? '');
        fs.writeFileSync(out, JSON.stringify({
          page: 67, phase: 'p44-pass2b-half', part,
          readAt: new Date().toISOString(), parseOk: parsed !== null,
          structured: parsed, raw: parsed ? undefined : (c.choices[0]?.message?.content ?? '').slice(0, 8000)
        }, null, 1));
        console.log(`${part}: ${parsed ? 'JSON OK' : 'samo raw'}`);
        ok = true;
      } catch (e) {
        const wait = /429|rate/i.test(String(e.message)) ? 60 * a : 15;
        console.log(`${part}: poskus ${a} padel (${String(e.message).slice(0, 60)}), čakam ${wait}s`);
        await new Promise(r => setTimeout(r, wait * 1000));
      }
    }
  }
}
main().catch(e => { console.error('FATAL', e); process.exit(1); });
