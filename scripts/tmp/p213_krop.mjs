// P213 krop — KROP-dokazi (leto 1864 = 22/29!):
// STRUKTURA (5): s40_zap_top/bot (3–16?) + s41_zap_top/bot (17–30 vs 18–31 DUEL!) + s42_zap_top (z31-potrja)
// DUELI (1): z89_s46_alter (starost: svež-VLM-'55-tednov-5-dni' vs P212-KROP-'3-tedni-izbrisano')
// GRIBLJE-VRSTICE (17): s40 z6/z9/z10/z12/z13 + s41 z19/z28/z30 + s42 z31/z33/z34/z35/z36/z44 + s44 z61/z64 + s45 z85
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p213';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// --- STRUKTURA: zap-stolpci s40/s41 (DUEL z17 + z30-vs-z31!) ---
await crop('s40_zap_top', 40, 0.10, 0.55, 0.02, 0.25, 2.2);
await crop('s40_zap_bot', 40, 0.53, 0.97, 0.02, 0.25, 2.2);
await crop('s41_zap_top', 41, 0.10, 0.55, 0.02, 0.25, 2.2);
await crop('s41_zap_bot', 41, 0.53, 0.97, 0.02, 0.25, 2.2);
await crop('s42_zap_top', 42, 0.10, 0.30, 0.02, 0.30, 3.0);
// --- DUEL z89 (s46 vrsta2): starost-korekcija-v-zapisu ---
await crop('z89_s46_alter', 46, 0.19, 0.30, 0.02, 0.88, 3.0);
// --- GRIBLJE-VRSTICE s40 (14 vrst z3–z16, row1=z3, band 0.0607, start 0.12) ---
await crop('z6_s40_grib', 40, 0.29, 0.39, 0.02, 0.88, 2.8);
await crop('z9_s40_grib', 40, 0.47, 0.57, 0.02, 0.88, 2.8);
await crop('z10_s40_grib', 40, 0.54, 0.64, 0.02, 0.88, 2.8);
await crop('z12_s40_grib', 40, 0.66, 0.76, 0.02, 0.88, 2.8);
await crop('z13_s40_grib', 40, 0.72, 0.82, 0.02, 0.88, 2.8);
// --- s41 (14 vrst z17–z30, row1=z17) ---
await crop('z19_s41_grib', 41, 0.23, 0.33, 0.02, 0.88, 2.8);
await crop('z28_s41_grib', 41, 0.78, 0.88, 0.02, 0.88, 2.8);
await crop('z30_s41_grib', 41, 0.89, 0.98, 0.02, 0.88, 2.8);
// --- s42 (14 vrst z31–z44, row1=z31) ---
await crop('z31_s42_grib', 42, 0.11, 0.21, 0.02, 0.88, 2.8);
await crop('z33_s42_grib', 42, 0.23, 0.33, 0.02, 0.88, 2.8);
await crop('z34_s42_grib', 42, 0.29, 0.39, 0.02, 0.88, 2.8);
await crop('z35_s42_grib', 42, 0.35, 0.45, 0.02, 0.88, 2.8);
await crop('z36_s42_grib', 42, 0.41, 0.51, 0.02, 0.88, 2.8);
await crop('z44_s42_grib', 42, 0.89, 0.98, 0.02, 0.88, 2.8);
// --- s44 (14 vrst z60–z73, row1=z60) ---
await crop('z61_s44_grib', 44, 0.17, 0.27, 0.02, 0.88, 2.8);
await crop('z64_s44_grib', 44, 0.35, 0.45, 0.02, 0.88, 2.8);
// --- s45 (14 vrst z74–z87, row1=z74) ---
await crop('z85_s45_grib', 45, 0.78, 0.88, 0.02, 0.88, 2.8);
console.log('GOTOV — 23 izrezov');
