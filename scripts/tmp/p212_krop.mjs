// P212 krop — 15 KROP-dokazov (leto 1865 = 21/29!):
// 1. arb_s46_glava  — letnica-invarianta '1865' (MEJA-1864/65-s46 restart; 50.-POTRDITEV!)
// 2. arb_s46_tail   — tail-1864 December (z85–87-gaplje-duel: 4 ali 7 vrst?)
// 3. z74_s45_zap    — zap-stolpec-duel (74/75/76-KROP-vs-71/72/73-VLM; s44/s45-overlap-rešitev!)
// 4-15. Griblje-vrstice 1865: z1(s46), z8,z9,z11,z13,z17,z18(s47), z24(s48), z36(s49), z50,z63(s50)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p212';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// 1. glava s46 (MEJA-1864/65: letvica + dvojna-črta + restart-z1)
await crop('arb_s46_glava', 46, 0.25, 0.72, 0.02, 0.65, 2.4);
// 2. tail s46 (1864-December-vrstice — koliko jih je?)
await crop('arb_s46_tail', 46, 0.02, 0.42, 0.02, 0.88, 2.6);
// 3. s45 zap-stolpec (prve 3 vrstice: 74/75/76 vs 71/72/73)
await crop('z74_s45_zap', 45, 0.10, 0.36, 0.02, 0.52, 3.0);
// 4. z1 s46 (row5, +letvica-shift)
await crop('z1_s46_grib', 46, 0.44, 0.60, 0.02, 0.88, 2.8);
// 5-10. s47 (14 vrst, z8–z21; band 0.0607)
await crop('z8_s47_grib', 47, 0.12, 0.20, 0.02, 0.88, 2.8);
await crop('z9_s47_grib', 47, 0.18, 0.26, 0.02, 0.88, 2.8);
await crop('z11_s47_grib', 47, 0.30, 0.38, 0.02, 0.88, 2.8);
await crop('z13_s47_grib', 47, 0.42, 0.50, 0.02, 0.88, 2.8);
await crop('z17_s47_grib', 47, 0.66, 0.75, 0.02, 0.88, 2.8);
await crop('z18_s47_grib', 47, 0.72, 0.81, 0.02, 0.88, 2.8);
// 11. z24 s48 (row3)
await crop('z24_s48_grib', 48, 0.24, 0.32, 0.02, 0.88, 2.8);
// 12. z36 s49 (row1)
await crop('z36_s49_grib', 49, 0.12, 0.20, 0.02, 0.88, 2.8);
// 13-14. s50 (15 vrst, z50–z64; band 0.0567)
await crop('z50_s50_grib', 50, 0.12, 0.20, 0.02, 0.88, 2.8);
await crop('z63_s50_grib', 50, 0.81, 0.90, 0.02, 0.88, 2.8);
console.log('GOTOV');
// 15. z20 s47 (row13) + 16. z8-re-crop (tighter)
await crop('z20_s47_grib', 47, 0.84, 0.93, 0.02, 0.88, 2.8);
await crop('z8_s47_grib2', 47, 0.14, 0.24, 0.02, 0.88, 2.8);
