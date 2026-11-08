// P218 wide-trak pass — 4 horizontalni trakovi na stran (9 strani = 36 izrezov), x 0.02–0.88.
// Namen: natančna rekonstrukcija vrstic + marginov (page-VLM-y-band je bil nezanesljiv!).
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p218';
fs.mkdirSync(`${TMP}/traki`, { recursive: true });
const PAGES = [11, 12, 13, 14, 15, 16, 17, 18, 19];
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
console.log('P218 traki: 36 izrezov');
