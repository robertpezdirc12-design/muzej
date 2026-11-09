// P238 krop pass-3 — ULTRA-ZOOM (vpis-2-hiša-duel 6/60 + zap-stolpec s57 + glava-leta):
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p238';
fs.mkdirSync(`${TMP}/krop3`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.round((y1-y0)*meta.height) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1900) }).png().toFile(`${TMP}/krop3/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}

// --- s57 ZAP-STOLPEC (vpisne številke — 3/4-duel!) ---
await crop('u57_zap', 57, 0.05, 0.99, 0.015, 0.10, 6.0);
// --- s57 GLAVA + vpis-2-nadstropje (veliko-leto + datum + št.-2) ---
await crop('u57_glava', 57, 0.05, 0.30, 0.015, 0.55, 4.0);
// --- s57 VPIS-2 naslovni-del (vas+hiša ženina IN neveste — 6/60-duel!) ---
await crop('u57_v2_naslovi', 57, 0.12, 0.34, 0.30, 0.99, 4.0);
// --- s56 GLAVA (tail-15 + veliko-1884 + Pag) ---
await crop('u56_glava', 56, 0.02, 0.28, 0.02, 0.60, 4.0);
// --- s58 VPIS-7 datum-duel (4/24/14-Feb!) ---
await crop('u58_v7_datum', 58, 0.10, 0.30, 0.02, 0.45, 4.5);
// --- s61 GLAVA (vpis-22 + veliko-1886 + 1/8/8/6!) ---
await crop('u61_glava', 61, 0.02, 0.30, 0.02, 0.55, 4.0);

console.log('KONČANO');
