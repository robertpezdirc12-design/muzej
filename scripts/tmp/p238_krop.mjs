// P238 krop pass-1 — KROP-dokazi (poročna 04455, leto 1885 = 1/13 NOVA-LINIJA!):
// RESTART (1): s56-meja (tail-1884 vpisi 15–18 + restart-vpis-1!)
// VPIS-4-DUEL (5): s57 vse-vrstice (2,3,4?,5,6 — VLM-dva-branja-se-spreminjata!)
// GRIBLJE-VRSTICE: s56-r5 (Pozek 58/38-duel!), s57-r1 (Drugoš h60-duel!), s57-r4 (Straus h32),
//   s58-r1 (Jakovič datum 4/24-Feb-duel!), s58-r2 (Straus h71!), s59-r1 (Hure h29-duel!),
//   s59-r2 (Novak h15-duel!), s59-r3 (Minich h9-duel!), s60-r1 (Brinec h26!), s61-r1 (Jakobič h13×23!)
// FOLIACIJA (6): s56–s61 (pag = sken−1-hipoteza!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p238';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.round((y1-y0)*meta.height) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// geometrije: razprti-listi; ytop 0.165; B = (0.975−0.165)/n-vrstic
const N = { 56: 5, 57: 5, 58: 4, 59: 5, 60: 6, 61: 4 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }

// --- FOLIACIJA (pag = sken−1!) ---
for (const p of Object.keys(N)) await crop(`arb_s${p}_pag`, +p, 0.02, 0.17, 0.30, 0.98, 3.2);

// --- MEJA s56 (tail-1884 + restart-1) ---
await crop('arb_s56_meja', 56, 0.04, 0.72, 0.02, 0.62, 2.6);

// --- VPIS-4-DUEL: s57 vse-5-vrstic ---
for (let i = 0; i < 5; i++) { const [y0, y1] = row(57, i); await crop(`arb_s57_r${i+1}`, 57, y0, y1, 0.02, 0.98, 2.2); }

// --- GRIBLJE-VRSTICE + datumi-dueli ---
const G = [
  [56, 4, 'p01_s56_grib'],   // vpis 1 — Pozek h58/38-duel × Silah h34!
  [57, 0, 'p02_s57_grib'],   // vpis 2 — Drugoš h60-duel × Felško!
  [57, 3, 'p05_s57_grib'],   // vpis 5 — Bahoric × Straus h32!
  [58, 0, 'p07_s58_datum'],  // vpis 7 — datum 4/24-Feb-duel + PEZDIREC-starši!
  [58, 1, 'p08_s58_grib'],   // vpis 8 — Straus h71!
  [59, 0, 'p11_s59_grib'],   // vpis 11 — Hure h29-duel!
  [59, 1, 'p12_s59_grib'],   // vpis 12 — Novak h15-duel!
  [59, 2, 'p13_s59_grib'],   // vpis 13 — Minich h9-duel!
  [60, 0, 'p16_s60_grib'],   // vpis 16 — Brinec h26!
  [61, 0, 'p22_s61_grib'],   // vpis 22 — Jakobič h13 × Stubler h23!
];
for (const [sken, idx0, name] of G) { const [y0, y1] = row(sken, idx0); await crop(name, sken, y0, y1, 0.02, 0.98, 2.2); }

// --- s61-RESTART-1886 (veliko-leto + vpisi 1–3 kontekst) ---
await crop('arb_s61_restart', 61, 0.30, 0.72, 0.02, 0.98, 2.2);

console.log('KONČANO');
