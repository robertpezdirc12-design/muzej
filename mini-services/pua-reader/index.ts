// P5-b watcher — mini-service (port 3031)
// Sondira VLM kvoto vsakih 5 min; ob dvigu samodejno prebere PUA strani 35–49
// (vsaka stran se shrani TAKOJ), nato požene deterministično analizo:
//   python3 scripts/pua-parse.py → scripts/pua-gen-ts.py → pua-pt-cross.py → pua-pt-wbridge.py
// Integracija v research.ts + QA + commit ostane ročna (glavni agent).
//
// GET /status  — polno stanje (kvota, prebrane strani, faza, pipeline log)
// GET /healthz — življenski znak
// POST /probe  — takojšnja sonda (ne čaka cikla)
import { createServer } from 'http';
import { execSync } from 'child_process';
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const PORT = 3031;
const ROOT = '/home/z/my-project';
const RAW_DIR = `${ROOT}/research/p3/pua-raw`;
const PNG_DIR = '/tmp/pua-pages';
const STATE_FILE = `${ROOT}/research/p5/reader-state.json`;
const LOG_FILE = `${ROOT}/research/p5/auto-log.txt`;
const PAGES = Array.from({ length: 15 }, (_, i) => 35 + i);
const PROBE_INTERVAL_MS = 5 * 60 * 1000;

interface State {
  startedAt: string;
  phase: 'probing' | 'reading' | 'pipeline' | 'done' | 'error';
  quota: 'unknown' | '429' | 'OK';
  lastProbeAt: string | null;
  lastOkAt: string | null;
  probesTotal: number;
  pagesRead: number[];
  pipeline: { step: string; ok: boolean; at: string }[];
  lastError: string | null;
  log: string[];
}

const state: State = {
  startedAt: new Date().toISOString(),
  phase: 'probing',
  quota: 'unknown',
  lastProbeAt: null,
  lastOkAt: null,
  probesTotal: 0,
  pagesRead: PAGES.filter(p => fs.existsSync(`${RAW_DIR}/pua-${String(p).padStart(2, '0')}.json`)),
  pipeline: [],
  lastError: null,
  log: [],
};

// --- persistence ---
function saveState() {
  try {
    fs.writeFileSync(STATE_FILE, JSON.stringify({ ...state, log: state.log.slice(-50) }, null, 1));
  } catch { /* ignore */ }
}
function ev(line: string) {
  const stamp = new Date().toISOString().slice(11, 19);
  const entry = `${stamp} ${line}`;
  state.log.push(entry);
  console.log(entry);
  try { fs.appendFileSync(LOG_FILE, `${new Date().toISOString()} pua-reader: ${line}\n`); } catch { /* ignore */ }
  saveState();
}

// --- VLM ---
let zai: any = null;
async function getZai() {
  if (!zai) zai = await ZAI.create();
  return zai;
}

async function probe(): Promise<{ ok: boolean; ms: number; err?: string }> {
  const t0 = Date.now();
  try {
    const z = await getZai();
    await z.chat.completions.createVision({
      messages: [{ role: 'user', content: [
        { type: 'text', text: 'Odgovori samo z: OK' },
        { type: 'image_url', image_url: { url: 'data:image/jpeg;base64,' + Buffer.from('/9j/4AAQSkZJRg==').toString('base64') } }
      ]}],
      thinking: { type: 'disabled' }
    });
    return { ok: true, ms: Date.now() - t0 };
  } catch (e: any) {
    return { ok: false, ms: Date.now() - t0, err: String(e?.message ?? e).slice(0, 120) };
  }
}

const PROMPT = (page: number) => `To je stran ${page} katastrskega registra lastnikov (PUA — "Besitzer-Protokoll" / Lastniški protokol) za k.o. Griblje iz franciscejskega katastra 1825, napisan v nemški Kurrent pisavi.

Prepiši VSAKE vrstico registra črka-za-črko, natanko kot je napisano (ne popravljaj črkovanja!). Vsak vnos ima stolpce: zaporedna številka, ime in priimek lastnika (kot je napisano), status/poklic (Bauer, Häusler, Bürger...), hišna številka (Haus), in številke parcel razdeljene po sekcijah (I, II, III, IV, V) ter b.P. (bauparzelle) opombe.

PRAVILA:
- Negotova branja označi z [~], neberljiva z [?]
- Ne izmišljuj vsebine; če stolpec manjka, pusti prazen
- Izpusti glavo strani in morebitne ponovljene naslove
- Izhod: JSON tabela objektov { "row": <zap. št.>, "name": "...", "status": "...", "house": ..., "sections": {"I": "...", ...}, "bP": "...", "note": "..." }
- Na koncu dodaj polje "pageNote" z opombo o splošni berljivosti strani`;

async function readPage(page: number): Promise<string> {
  const png = `${PNG_DIR}/pua-${String(page).padStart(2, '0')}.png`;
  execSync(`python3 -c "from PIL import Image; im=Image.open('${png}').convert('RGB'); im.save('/tmp/pua-send-${page}.jpg', quality=92)"`);
  const b64 = fs.readFileSync(`/tmp/pua-send-${page}.jpg`).toString('base64');
  const z = await getZai();
  const completion = await z.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: PROMPT(page) },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  return completion.choices[0]?.message?.content ?? '';
}

function missingPages(): number[] {
  return PAGES.filter(p => !fs.existsSync(`${RAW_DIR}/pua-${String(p).padStart(2, '0')}.json`));
}

async function readAll(): Promise<boolean> {
  state.phase = 'reading';
  ev(`faza branje: manjka ${missingPages().length} strani`);
  let failStreak = 0;
  for (const p of missingPages()) {
    const out = `${RAW_DIR}/pua-${String(p).padStart(2, '0')}.json`;
    if (fs.existsSync(out)) continue;
    const t0 = Date.now();
    let raw: string | null = null;
    for (let attempt = 1; attempt <= 2; attempt++) {
      try { raw = await readPage(p); break; }
      catch (e: any) {
        ev(`stran ${p} poskus ${attempt} napaka: ${String(e?.message ?? e).slice(0, 80)}`);
        await new Promise(r => setTimeout(r, 20000));
      }
    }
    if (raw) {
      fs.writeFileSync(out, JSON.stringify({ page: p, raw, ms: Date.now() - t0, via: 'pua-reader@3031' }, null, 1));
      state.pagesRead.push(p);
      ev(`stran ${p}: PREBRANA (${raw.length} znakov, ${((Date.now() - t0) / 1000).toFixed(0)}s)`);
      failStreak = 0;
    } else {
      ev(`stran ${p}: NEUSPEH — kvota verjetno spet padla, prekinjam branje`);
      state.quota = '429';
      failStreak++;
      break;
    }
    await new Promise(r => setTimeout(r, 8000));
  }
  return failStreak === 0;
}

function runPipeline() {
  state.phase = 'pipeline';
  const steps: [string, string][] = [
    ['parse', 'python3 scripts/pua-parse.py'],
    ['gen-ts', 'python3 scripts/pua-gen-ts.py'],
    ['pt-cross', 'python3 scripts/pua-pt-cross.py'],
    ['pt-wbridge', 'python3 scripts/pua-pt-wbridge.py'],
  ];
  let allOk = true;
  for (const [name, cmd] of steps) {
    try {
      const out = execSync(cmd, { cwd: ROOT, timeout: 120000, encoding: 'utf8' }).slice(0, 2000);
      state.pipeline.push({ step: name, ok: true, at: new Date().toISOString() });
      ev(`pipeline ${name}: OK — ${out.split('\n')[0].slice(0, 100)}`);
    } catch (e: any) {
      state.pipeline.push({ step: name, ok: false, at: new Date().toISOString() });
      ev(`pipeline ${name}: NAPAKA — ${String(e?.message ?? e).slice(0, 150)}`);
      allOk = false;
      break;
    }
  }
  if (allOk) {
    state.phase = 'done';
    ev('PIPELINE ZAKLJUČEN: strani 35–49 prebrane + parse + gen + obe analizi. Integracija v research.ts čaka ročno.');
  } else {
    state.phase = 'error';
    state.lastError = 'pipeline failed — glej log';
  }
  saveState();
}

// --- main loop ---
async function mainLoop() {
  ev(`pua-reader zagnan (port ${PORT}); manjka ${missingPages().length} strani; interval sonde ${PROBE_INTERVAL_MS / 1000}s`);
  if (!missingPages().length) {
    // vse že prebrane → samo pipeline (če še ni bil pognan) in status
    if (state.pipeline.length === 0) runPipeline();
    else state.phase = 'done';
    saveState();
    return;
  }
  for (;;) {
    state.probesTotal++;
    const r = await probe();
    state.lastProbeAt = new Date().toISOString();
    if (r.ok) {
      state.quota = 'OK';
      state.lastOkAt = state.lastProbeAt;
      ev(`sonda OK (${r.ms}ms) — kvota dvignjena!`);
      const ok = await readAll();
      if (ok) { runPipeline(); return; }
      // kvota padla med branjem → nazaj na sondiranje
      ev('nazaj k sondiranju (kvota padla med branjem)');
    } else {
      state.quota = '429';
      ev(`sonda 429 (${r.ms}ms, skupno ${state.probesTotal})`);
    }
    saveState();
    await new Promise(res => setTimeout(res, PROBE_INTERVAL_MS));
  }
}

// --- HTTP status API ---
const server = createServer((req, res) => {
  const url = (req.url ?? '').split('?')[0];
  if (req.method === 'GET' && url === '/healthz') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('pua-reader alive');
    return;
  }
  if (req.method === 'GET' && (url === '/' || url === '/status')) {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      ...state,
      pagesMissing: missingPages(),
      pid: process.pid,
      uptimeMin: Math.round((Date.now() - Date.parse(state.startedAt)) / 60000),
    }, null, 1));
    return;
  }
  if (req.method === 'POST' && url === '/probe') {
    res.writeHead(202, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ queued: true }));
    probe().then(r => {
      state.probesTotal++;
      state.lastProbeAt = new Date().toISOString();
      state.quota = r.ok ? 'OK' : '429';
      if (r.ok) state.lastOkAt = state.lastProbeAt;
      ev(`ročna sonda: ${r.ok ? 'OK' : '429'} (${r.ms}ms)`);
      saveState();
    });
    return;
  }
  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('not found — GET /status | GET /healthz | POST /probe');
});

server.listen(PORT, () => {
  console.log(`pua-reader status API on :${PORT}`);
});

process.on('SIGTERM', () => { ev('SIGTERM — ugašam'); process.exit(0); });
process.on('SIGINT', () => { ev('SIGINT — ugašam'); process.exit(0); });

mainLoop().catch(e => {
  state.phase = 'error';
  state.lastError = String(e?.message ?? e).slice(0, 200);
  ev(`FATALNA NAPAKA: ${state.lastError}`);
  saveState();
});
