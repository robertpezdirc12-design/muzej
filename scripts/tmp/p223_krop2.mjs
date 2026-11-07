// P223 krop pass-2 — HI-ZOOM dvomi (kalibracija!):
// HIŠNA-HI (4): z96 (18-vs-63-DUEL!), z61 (90-vs-70!), z78 (37-?), z76 (51-?)
// VAS-HI (1): z99 (X-open-'OBržuh/Obrije[?]'!)
// PRIPIS-HI (4): z05 (MMK-1962?), z59 (garble-1965?), z17 (1858?), z22 (1940?)
// PAG-HI (2): s161 (155-vs-156-5/6-garble!), s173 (gola-'168'-vs-Pag-186-X-open!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p223';
fs.mkdirSync(`${TMP}/krop2`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 2000) }).png().toFile(`${TMP}/krop2/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1} sc${sc}`);
}
const N = { 159: 8, 160: 8, 161: 10, 162: 9, 163: 8, 164: 8, 165: 9, 166: 9, 167: 9, 168: 8, 169: 8, 170: 8, 171: 8, 172: 8, 173: 8 };
const YT = 0.165, YB = 0.975;
function rowY(sken, idx0) { const B = (YB - YT) / N[sken]; return [YT + idx0 * B, (YB - YT) / N[sken]]; }

// --- HIŠNA-HI (dueli!) ---
{ const [y0, B] = rowY(172, 5); await crop('z96_s172_hisna_hi', 172, y0 - 0.008, y0 + B + 0.008, 0.28, 0.55, 6.0); }   // 18-vs-63!
{ const [y0, B] = rowY(168, 2); await crop('z61_s168_hisna_hi', 168, y0 - 0.008, y0 + B + 0.008, 0.28, 0.55, 6.0); }   // 90-vs-70!
{ const [y0, B] = rowY(170, 3); await crop('z78_s170_hisna_hi', 170, y0 - 0.008, y0 + B + 0.008, 0.28, 0.55, 6.0); }   // 37-?
{ const [y0, B] = rowY(170, 1); await crop('z76_s170_hisna_hi', 170, y0 - 0.008, y0 + B + 0.008, 0.28, 0.55, 6.0); }   // 51-?
{ const [y0, B] = rowY(164, 4); await crop('z28_s164_hisna_hi', 164, y0 - 0.008, y0 + B + 0.008, 0.28, 0.55, 6.0); }   // 35[~]
{ const [y0, B] = rowY(166, 2); await crop('z43_s166_hisna_hi', 166, y0 - 0.008, y0 + B + 0.008, 0.28, 0.55, 6.0); }   // 17[~7?]

// --- VAS-HI (z99 X-open!) ---
{ const [y0, B] = rowY(173, 0); await crop('z99_s173_vas_hi', 173, y0 - 0.008, y0 + B + 0.008, 0.115, 0.36, 6.0); }

// --- PRIPIS-HI (desna stran — MMK-era!) ---
{ const [y0, B] = rowY(161, 8); await crop('z05_s161_pripis_hi', 161, Math.max(0.05, y0 - 0.006), y0 + B + 0.006, 0.55, 0.99, 5.0); }  // umrla-18.12.1962?
{ const [y0, B] = rowY(168, 0); await crop('z59_s168_pripis_hi', 168, Math.max(0.05, y0 - 0.006), y0 + B + 0.006, 0.55, 0.99, 5.0); }  // rojen-10.7.1965?
{ const [y0, B] = rowY(163, 1); await crop('z17_s163_pripis_hi', 163, Math.max(0.05, y0 - 0.006), y0 + B + 0.006, 0.55, 0.99, 5.0); }  // 9/10-1858?
{ const [y0, B] = rowY(163, 6); await crop('z22_s163_pripis_hi', 163, Math.max(0.05, y0 - 0.006), y0 + B + 0.006, 0.55, 0.99, 5.0); }  // 6.1.1940?
{ const [y0, B] = rowY(172, 3); await crop('z94_s172_pripis_hi', 172, Math.max(0.05, y0 - 0.006), y0 + B + 0.006, 0.55, 0.99, 5.0); }  // 1910-Pillkburk?
{ const [y0, B] = rowY(167, 8); await crop('z58_s167_pripis_hi', 167, Math.max(0.05, y0 - 0.006), y0 + B + 0.006, 0.55, 0.99, 5.0); }  // 8.10.1959?
{ const [y0, B] = rowY(166, 2); await crop('z43_s166_pripis_hi', 166, Math.max(0.05, y0 - 0.006), y0 + B + 0.006, 0.55, 0.99, 5.0); }  // 16.1.1949?
{ const [y0, B] = rowY(165, 0); await crop('z32_s165_pripis_hi', 165, Math.max(0.05, y0 - 0.006), y0 + B + 0.006, 0.55, 0.99, 5.0); }  // poroka-1957?

// --- PAG-HI (foliacija!) ---
await crop('s161_pag_hi', 161, 0.02, 0.13, 0.02, 0.30, 8.0);   // 155-vs-156!
await crop('s173_pag_hi', 173, 0.02, 0.13, 0.02, 0.30, 8.0);   // gola-'168' (vs-Pag-186-X-open!)

console.log('P223 krop pass-2: 20 izrezov');
