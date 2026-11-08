// P228 krop — probe s99–s106: FOLIACIJA ('sken−6' — s99='93' pričakovana!) + ZAP-STOLPCI + GLAVE + s106-MEJA
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p228';
fs.mkdirSync(`${TMP}/krop`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
const args = process.argv.slice(2);
const ONLY = args.length ? args : null;
async function maybe(name, fn) { if (ONLY && !ONLY.includes(name)) return; await fn(); }

// --- FOLIACIJA (gola-svinčna-'sken−6'!) — zgoraj-levo ---
for (const p of [99, 100, 101, 102, 103, 104, 105, 106]) await maybe(`arb_s${p}_pag`, () => crop(`arb_s${p}_pag`, p, 0.0, 0.17, 0.02, 0.42, 3.2));

// --- GLAVA ('Jahr 1878'?) s99 + s106 (spodaj-desno!) ---
for (const p of [99, 106]) await maybe(`arb_s${p}_glava`, () => crop(`arb_s${p}_glava`, p, 0.02, 0.13, 0.42, 0.99, 3.2));

// --- s106 MEJA (VSOTNA + glava + restart-z1-1879!) ---
await maybe('arb_s106_meja', () => crop('arb_s106_meja', 106, 0.02, 0.99, 0.02, 0.62, 2.6));
await maybe('arb_s106_vsotna', () => crop('arb_s106_vsotna', 106, 0.60, 0.85, 0.02, 0.62, 3.4));

// --- ZAP-STOLPCI (ordinalna-linija s99!) ---
for (const p of [99, 100, 105]) await maybe(`s${p}_zap_stolpec`, () => crop(`s${p}_zap_stolpec`, p, 0.05, 0.99, 0.02, 0.115, 5.0));

console.log('KROPI KONČANI');
