// P204: KROP vseh 39 Griblje-vrstic leta 1873 za fokusirano VLM-forenziko
// (recept P196/P197: frakcijske koordinate, kontekst ±1.2 vrstice, sharp 1.7×)
import sharp from 'sharp';
import fs from 'fs';

const TMP = '/tmp/p204';
const ent = JSON.parse(fs.readFileSync(`${TMP}/entries_1873.json`, 'utf-8'));
const grib = ent.griblje_entries;

// tabela-y-območje per sken (glava ~0.10–0.14; dno ~0.97)
const YT = { a: 0.14, b: 0.97 };
const n_vrst_map = { 102: 12, 103: 12, 105: 14, 106: 12, 107: 13, 108: 13, 109: 13, 110: 13, 111: 12, 112: 12, 113: 13, 114: 13, 115: 12, 116: 12, 117: 13, 118: 14, 119: 13 };

fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });

const seen = new Set();
for (const e of grib) {
  const key = `${e.sken}r${e.vrsta_sken}`;
  if (seen.has(key)) continue; // s103 duplikat-sken zaščita
  seen.add(key);
  const n = n_vrst_map[e.sken] ?? 13;
  const h = (YT.b - YT.a) / n;               // višina vrstice (frakcija)
  const yC = YT.a + (e.vrsta_sken - 0.5) * h; // center vrstice
  const y0 = Math.max(0.02, yC - 1.2 * h);
  const y1 = Math.min(0.995, yC + 1.2 * h);
  const meta = await sharp(`${TMP}/s${e.sken}.jpg`).metadata();
  const left = Math.round(0.0 * meta.width);
  const top = Math.round(y0 * meta.height);
  const width = Math.round(0.72 * meta.width) - left;
  const height = Math.round(y1 * meta.height) - top;
  const out = `${TMP}/krop-grib/z${e.z}_s${e.sken}r${e.vrsta_sken}_h${(e.hisna ?? '?').toString().replace(/\W/g, '')}.png`;
  await sharp(`${TMP}/s${e.sken}.jpg`)
    .extract({ left, top, width, height })
    .resize({ width: Math.min(Math.round(width * 1.7), 1600) })
    .png()
    .toFile(out);
  console.log('OK', out.split('/').pop());
}
console.log(`SKUPAJ: ${seen.size} kropov`);
