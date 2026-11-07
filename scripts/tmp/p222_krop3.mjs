// P222 krop pass-3 — zadnje forenzike: z60-NEW-CANDIDATE! + hišna-x-fix + zap-re-kalibracija (s173/s174/s176/s178/s180/s186) + z85-hišna
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p222';
fs.mkdirSync(`${TMP}/krop3`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 2000) }).png().toFile(`${TMP}/krop3/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1} sc${sc}`);
}
const N = { 173: 8, 174: 7, 175: 9, 176: 8, 177: 8, 178: 10, 179: 10, 180: 10, 181: 8, 182: 8, 183: 9, 184: 11, 185: 8, 186: 7 };
const YT = 0.165, YB = 0.975;
function rowY(sken, idx0) { const B = (YB - YT) / N[sken]; return [YT + idx0 * B, B]; }

// --- ZAP-HI re-kalibracija (6) ---
for (const p of [173, 174, 176, 178, 180, 186]) await crop(`s${p}_zap_hi3`, p, 0.05, 0.99, 0.015, 0.12, 6.0);

// --- z60-NEW-CANDIDATE (s180 vrsta2 = idx1): full row + vas-hi ---
{ const [y0, B] = rowY(180, 1); await crop('z60_s180_row', 180, y0 - 0.008, y0 + B + 0.008, 0.02, 0.92, 3.0); }
{ const [y0, B] = rowY(180, 1); await crop('z60_s180_vas_hi', 180, y0 - 0.008, y0 + B + 0.008, 0.10, 0.40, 6.0); }

// --- hišna-hi x-fix (wider!) ---
{ const [y0, B] = rowY(176, 2); await crop('z26_s176_hisna_hi2', 176, y0 - 0.008, y0 + B + 0.008, 0.30, 0.72, 5.0); }
{ const [y0, B] = rowY(184, 0); await crop('z93_s184_hisna_hi2', 184, y0 - 0.008, y0 + B + 0.008, 0.30, 0.72, 5.0); }
{ const [y0, B] = rowY(183, 0); await crop('z85_s183_hisna_hi2', 183, y0 - 0.008, y0 + B + 0.008, 0.30, 0.72, 5.0); }
{ const [y0, B] = rowY(173, 1); await crop('z01_s173_hisna_hi2', 173, y0 - 0.008, y0 + B + 0.008, 0.30, 0.72, 5.0); }
{ const [y0, B] = rowY(181, 6); await crop('z75_s181_hisna_hi2', 181, y0 - 0.008, y0 + B + 0.008, 0.30, 0.72, 5.0); }
console.log('P222 krop pass-3: 13 izrezov');
