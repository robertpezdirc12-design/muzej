// P211 krop — 6 KROP-dokazov (sandboX-reset-regeneracija po receptu iz prejšnje seje):
// 1. arb_s51_glava  — letnica-invarianta '1866' (MEJA-1866/67-s51 restart; 49.-POTRDITEV!)
// 2. z58_s56_mesec  — ULEDBA-#10: smrt-29-Juni → pokop-1-Juli (mesec-'Juli'-KROP!)
// 3. z34z35_s55     — DVOJČKA-MRTVOROJENA 'Totgeborenes Kind' (VLM-'Posmrhlanski/Turškorojeni'-FALSIFIKACIJA!)
// 4. z90_s59        — 2-OSEBI-V-1-VRSTICI ('Laufbarend'-Anton + Marko-Požar[?])
// 5. z41_s55        — starost-DUEL ('1 leto'-KROP-vs-'19 J'-VLM) + h14-Pezdirc
// 6. z22_s53        — K-glyph-DUEL 'Kusić[~]' + hiša-DUEL (A=11-vs-B=41!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p211';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// 1. glava s51 (celoten zgornji del z VELIKO-LETVICO)
await crop('arb_s51_glava', 51, 0.02, 0.52, 0.02, 0.62, 2.2);
// 2. z58 = zadnja vrstica s56 (13 vrst) — mesec + pokop stolpca
await crop('z58_s56_mesec', 56, 0.90, 0.995, 0.08, 0.55, 3.0);
// 3. z34/z35 = prvi dve vrstici s55 (12 vrst) — anomalija
await crop('z34z35_s55_anomalija', 55, 0.09, 0.27, 0.02, 0.88, 2.6);
// 4. z90 = 8. vrstica s59 (12 vrst, z83–z94)
await crop('z90_s59_anomalia', 59, 0.60, 0.78, 0.02, 0.88, 2.6);
// 5. z41 = 8. vrstica s55 (12 vrst, z34–z45) — starost + hiša
await crop('z41_s55_h14', 55, 0.58, 0.75, 0.02, 0.88, 2.6);
// 6. z22 = 2. vrstica s53 (13 vrst, z21–z33) — ime + hiša
await crop('z22_s53_ime', 53, 0.13, 0.28, 0.25, 0.85, 3.0);
console.log('GOTOV');
// 7. z22 = hiša-duel (A=11-vs-B=41) — vas+hiša stolpca
await crop('z22_s53_hisa', 53, 0.14, 0.28, 0.02, 0.48, 3.2);
