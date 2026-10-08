// VLM ploščično skeniranje listov N83 — toponimi z relativnimi pozicijami (P9)
// Metoda: list razdelimo na ploščice (grid), VLM prebere napise v vsaki ploščici
// in poda pozicijo centra besedila v % ploščice. Pretvorba v globalne px.
// Validacija na A02 (cerkev px 1995,577 — GEOTRUTH, issue #14).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import { execSync } from 'child_process';

const SHEETS = {
  a02: { file: 'public/atlas/n83-a02.jpg', w: 3010, h: 2158 },
  a03: { file: 'public/atlas/n83-a03.jpg', w: 2645, h: 2154 },
  a04: { file: 'public/atlas/n83-a04.jpg', w: 2645, h: 2158 },
  a05: { file: 'public/atlas/n83-a05.jpg', w: 2634, h: 2165 },
};

// grid: 5 stolpcev × 4 vrstice, 12 % prekrivanje
const GRID = { cols: 5, rows: 4, overlap: 0.12 };

function tileFor(sheet, col, row) {
  const s = SHEETS[sheet];
  const tw = s.w / GRID.cols;
  const th = s.h / GRID.rows;
  const ox = col === 0 ? 0 : -GRID.overlap * tw;
  const oy = row === 0 ? 0 : -GRID.overlap * th;
  const x0 = Math.max(0, Math.round(col * tw + ox));
  const y0 = Math.max(0, Math.round(row * th + oy));
  const x1 = Math.min(s.w, Math.round((col + 1) * tw + (col === GRID.cols - 1 ? 0 : GRID.overlap * tw)));
  const y1 = Math.min(s.h, Math.round((row + 1) * th + (row === GRID.rows - 1 ? 0 : GRID.overlap * th)));
  return { x0, y0, x1, y1 };
}

const PROMPT = (sheet) => `To je izrezek (ploščica) grafičnega katastrskega lista ${sheet.toUpperCase()} iz franciscejskega katastra 1825 za k.o. Griblje (Bela krajina), napisan v nemški Kurrent pisavi. List prikazuje parcele, hiše, reko Kolpo (vzhod) in napise krajnih/vrstnih imen.

Naloga: preberi VSE besedilne napise, ki jih vidiš na tej ploščici:
- krajevna imena (vasi, zaselki: npr. Grüble, Adleschitz, Zaplje...)
- vrstna imena (Flurnamen: njive, travniki, gozdovi)
- oznake občin/mej (npr. »Katastralgemeinde ...«)
- morebitne številke hiš ob imenih

Za vsak napis podaj:
1. "text": prepis natanko kot je napisano (Kurrent; negotovo [~], neberljivo [?])
2. "conf": "high" | "med" | "low" — zaupanje v branje
3. "xPct": vodoravna lega CENTRA besedila v % širine ploščice (0 = levi rob, 100 = desni rob)
4. "yPct": navpična lega centra besedila v % višine ploščice (0 = zgornji rob, 100 = spodnji rob)
5. "kind": "settlement" (naselbinski napis) | "flurname" (vrstno ime) | "boundary" (mejni/mejna občina) | "other"

Izhod: SAMO JSON tabela (brez proze). Če ni nobenega napisa: []`;

async function scanTile(zai, sheet, col, row) {
  const t = tileFor(sheet, col, row);
  const png = SHEETS[sheet].file;
  execSync(`python3 -c "
from PIL import Image
im = Image.open('${png}')
tile = im.crop((${t.x0}, ${t.y0}, ${t.x1}, ${t.y1}))
tile = tile.resize((int(tile.width*1.6), int(tile.height*1.6)), Image.LANCZOS)
tile.save('/tmp/p9-tile.jpg', quality=92)
"`);
  const b64 = fs.readFileSync('/tmp/p9-tile.jpg').toString('base64');
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: PROMPT(sheet) },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      return r.choices?.[0]?.message?.content ?? '';
    } catch (e) {
      const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
      console.error(`  tile ${col},${row} poskus ${attempt}: ${e.message.slice(0, 60)}`);
      if (!is429 && attempt >= 2) break;
      await new Promise(r2 => setTimeout(r2, 20000));
    }
  }
  return null;
}

function parseJSON(text) {
  if (!text) return null;
  let t = text.trim();
  const i = t.indexOf('[');
  const j = t.lastIndexOf(']');
  if (i >= 0 && j > i) t = t.slice(i, j + 1);
  try { return JSON.parse(t); } catch { return null; }
}

async function main() {
  const sheet = process.argv[2];
  if (!SHEETS[sheet]) { console.error('usage: bun scripts/georef-tiles.mjs <a02|a03|a04|a05>'); process.exit(1); }
  const zai = await ZAI.create();
  const outDir = 'research/georef-n83/tiles-vlm';
  fs.mkdirSync(outDir, { recursive: true });
  const labels = [];
  for (let row = 0; row < GRID.rows; row++) {
    for (let col = 0; col < GRID.cols; col++) {
      const t = tileFor(sheet, col, row);
      const t0 = Date.now();
      const raw = await scanTile(zai, sheet, col, row);
      const arr = parseJSON(raw);
      if (!arr) { console.log(`tile ${col},${row}: NEUSPEH (${((Date.now()-t0)/1000).toFixed(0)}s)`); continue; }
      for (const e of arr) {
        if (typeof e?.xPct !== 'number' || typeof e?.yPct !== 'number' || !e?.text) continue;
        const gx = t.x0 + (e.xPct / 100) * (t.x1 - t.x0);
        const gy = t.y0 + (e.yPct / 100) * (t.y1 - t.y0);
        labels.push({
          text: String(e.text).slice(0, 80), conf: e.conf ?? 'low', kind: e.kind ?? 'other',
          tile: `${col},${row}`, px: [Math.round(gx), Math.round(gy)],
        });
      }
      console.log(`tile ${col},${row}: ${arr.length} napisov (${((Date.now()-t0)/1000).toFixed(0)}s)`);
      await new Promise(r2 => setTimeout(r2, 2500));
    }
  }
  fs.writeFileSync(`${outDir}/${sheet}-labels.json`, JSON.stringify({ sheet, scanned: new Date().toISOString(), labels }, null, 1));
  const settlements = labels.filter(l => l.kind === 'settlement' || l.kind === 'boundary');
  console.log(`\nSKUPAJ: ${labels.length} napisov (${settlements.length} naselbinskih/mejnih) → ${outDir}/${sheet}-labels.json`);
}

main();
