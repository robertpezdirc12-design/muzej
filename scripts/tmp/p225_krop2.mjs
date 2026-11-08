// P225 krop pass-2 — re-krops: 5-problematičnih-vrstic (geometrija-1-vrstico-nizko!) +
// foliacijski-DUELI-×5 (s138/s143/s145/s146/s147!) + hi/ime-zoomi (z15-34/37! z48-Justina! z52-Marta/Maria!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p224';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
const N = { 135: 7, 136: 7, 137: 7, 138: 7, 139: 7, 140: 7, 141: 7, 142: 8, 143: 8, 144: 8, 145: 8, 146: 8, 147: 7 };
const YT = 0.165, YB = 0.975;
function band(sken, i0, i1) { const B = (YB - YT) / N[sken]; return [YT + i0*B - 0.015, Math.min(0.999, YT + (i1+1)*B + 0.020)]; }

// --- 1. Problem-vrstice: ŠIROKI-pasi (idx0-shift +1!) ---
{ const [a,b] = band(139, 5, 7); await crop('rk_z28_s139_wide', 139, a, b, 0.02, 0.92, 2.6); }   // z27–z28-tail
{ const [a,b] = band(141, 3, 6); await crop('rk_z40_s141_wide', 141, a, b, 0.02, 0.92, 2.2); }   // z39–z42 (z40+z42!)
{ const [a,b] = band(141, 5, 7); await crop('rk_z42_s141_wide', 141, a, b, 0.02, 0.92, 2.6); }   // z41–z42
{ const [a,b] = band(144, 6, 8); await crop('rk_z66_s144_wide', 144, a, b, 0.02, 0.92, 2.6); }   // z65–z66-tail
{ const [a,b] = band(146, 5, 7); await crop('rk_z81_s146_wide', 146, a, b, 0.02, 0.92, 2.6); }   // z80–z81
{ const [a,b] = band(142, 4, 6); await crop('rk_z48_s142_wide', 142, a, b, 0.02, 0.92, 2.4); }   // z47–z49 (z48!)

// --- 2. FOLIACIJA-DUELI-×5 (zoom zgornji-levi-kot!) ---
for (const p of [138, 143, 145, 146, 147]) await crop(`rk2_s${p}_pag2`, p, 0.03, 0.14, 0.02, 0.30, 5.0);

// --- 3. HI/IME-zoomi ---
{ const [a,b] = band(138, 0, 0); await crop('rk_z15_s138_cell2', 138, a, b, 0.09, 0.30, 6.0); }  // z15-hi: 34-vs-37!
{ const [a,b] = band(143, 1, 1); await crop('rk_z52_s143_cell3', 143, a, b, 0.09, 0.34, 5.5); }  // z52-ime: Marta-vs-Maria + hi-51
{ const [a,b] = band(142, 5, 5); await crop('rk_z48_s142_cell3', 142, a, b, 0.09, 0.34, 5.5); }  // z48-ime: JustynAnna/Justina + hi-62

// --- 4. MEJA-zoom: s136-glava-'Jahr 1881.' (natisnjeno+ročno-81!) + s135-'finis' ---
await crop('rk_s136_glava', 136, 0.03, 0.12, 0.02, 0.35, 6.0);
await crop('rk_s135_finis_zoom', 135, 0.86, 1.00, 0.55, 0.98, 4.0);
console.log('P225 krop pass-2: 13 izrezov');
