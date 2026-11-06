// P221 traki — 4 horizontalni trakovi na stran (s185–s199 = 15 strani = 60 izrezov), x 0.02–0.88.
// Namen: križ page-VLM (razprti dvostranski listi — vsaka vrstica čez obe strani!).
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p221';
fs.mkdirSync(`${TMP}/traki`, { recursive: true });
const PAGES = [185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199];
const BANDS = [[0.05, 0.28], [0.28, 0.51], [0.51, 0.74], [0.74, 0.98]];
for (const p of PAGES) {
  const meta = await sharp(`${TMP}/s${p}.jpg`).metadata();
  for (let i = 0; i < BANDS.length; i++) {
    const [y0, y1] = BANDS[i];
    await sharp(`${TMP}/s${p}.jpg`).extract({ left: Math.round(0.02*meta.width), top: Math.round(y0*meta.height), width: Math.round(0.86*meta.width), height: Math.round((y1-y0)*meta.height) })
      .resize({ width: Math.min(Math.round(0.86*meta.width*2.2), 1800) }).png().toFile(`${TMP}/traki/t${i+1}_s${p}.png`);
  }
  console.log(`s${p}: 4 traki OK`);
}
console.log('P221 traki: 60 izrezov');
