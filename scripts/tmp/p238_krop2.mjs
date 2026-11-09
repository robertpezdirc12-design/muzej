// P238 krop pass-2 — ŠIROKI-OKNI (neenakomerne-vrstice-razprti-listov!):
// polovična-okna po straneh + ciljni-stolpci
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p238';
fs.mkdirSync(`${TMP}/krop2`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.round((y1-y0)*meta.height) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1900) }).png().toFile(`${TMP}/krop2/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}

// --- s56: spodnja-polovica (restart-vpis-1 + konec-tail-18) ---
await crop('w56_dol', 56, 0.50, 0.99, 0.02, 0.98, 2.4);
// --- s56: zgornja-polovica (tail-15/16 Griblje-47×34!) ---
await crop('w56_gor', 56, 0.08, 0.55, 0.02, 0.98, 2.4);

// --- s57: trije pasovi (vpisi 2–6) ---
await crop('w57_a', 57, 0.10, 0.42, 0.02, 0.98, 2.4);
await crop('w57_b', 57, 0.38, 0.70, 0.02, 0.98, 2.4);
await crop('w57_c', 57, 0.66, 0.99, 0.02, 0.98, 2.4);

// --- s58: zgornja-polovica (vpis 7 datum-duel + vpis 8 Straus-h71) ---
await crop('w58_gor', 58, 0.08, 0.55, 0.02, 0.98, 2.4);
// --- s58: spodnja-polovica (vpisi 9–10 kontekst) ---
await crop('w58_dol', 58, 0.50, 0.99, 0.02, 0.98, 2.4);

// --- s59: trije pasovi (vpisi 11–15) ---
await crop('w59_a', 59, 0.10, 0.38, 0.02, 0.98, 2.4);
await crop('w59_b', 59, 0.34, 0.62, 0.02, 0.98, 2.4);
await crop('w59_c', 59, 0.58, 0.99, 0.02, 0.98, 2.4);

// --- s60: zgornja-polovica (vpis 16 Brinec-h26!) ---
await crop('w60_gor', 60, 0.08, 0.48, 0.02, 0.98, 2.4);

// --- s61: zgornja-polovica (vpis 22 Jakobič-h13×23!) ---
await crop('w61_gor', 61, 0.08, 0.52, 0.02, 0.98, 2.4);

console.log('KONČANO');
