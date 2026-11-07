// P222 krop pass-2 — kalibracija + hi-zoom (P221-recept: pass-1-zgrešeni → pass-2!):
// ZAP-HI (7): s175 (re-15–23!), s181 (76?), s182 (korekcije!), s183 (84-dup-vs-85!), s184 (93–102-10-vrstic?), s177 (popravki-×7!), s179 (top-48/49-prečr!)
// VRSTICA-RE-CROPS (7): z61, z65, z75, z84, z95, z105, z110 (geometry-shift-UP-1-row!)
// HIŠNA/VAS/ORDINAL-HI (5): z93-hiša (48/18/8!), z99-vas (Griblje/Podplanina!), z01-hiša (34/37!), z26-hiša (33/58/38!), z86-s183-ordinal (84-dup!) + z52-vas + z105-pripis/oče
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p222';
fs.mkdirSync(`${TMP}/krop2`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 2000) }).png().toFile(`${TMP}/krop2/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1} sc${sc}`);
}
const N = { 173: 8, 174: 7, 175: 9, 176: 8, 177: 8, 178: 10, 179: 10, 180: 10, 181: 8, 182: 8, 183: 9, 184: 10, 185: 8, 186: 7 };
const YT = 0.165, YB = 0.975;
function rowY(sken, idx0) { const B = (YB - YT) / N[sken]; return [YT + idx0 * B, (YB - YT) / N[sken]]; }

// --- ZAP-HI (re-kalibracija!) ---
await crop('s175_zap_hi', 175, 0.05, 0.99, 0.015, 0.12, 6.0);
await crop('s181_zap_hi', 181, 0.05, 0.99, 0.015, 0.12, 6.0);
await crop('s182_zap_hi', 182, 0.05, 0.99, 0.015, 0.12, 6.0);
await crop('s183_zap_hi', 183, 0.05, 0.99, 0.015, 0.12, 6.0);
await crop('s184_zap_hi', 184, 0.05, 0.99, 0.015, 0.12, 6.0);
await crop('s177_zap_hi', 177, 0.05, 0.99, 0.015, 0.12, 6.0);
await crop('s179_zap_hi', 179, 0.05, 0.99, 0.015, 0.12, 6.0);

// --- VRSTICA-RE-CROPS (geometry-shift-UP-1-row: idx0 = vrsta−2) ---
const RECROP = [
  [180, 2, 'z61_s180_re'],    // caught z62 → shift UP
  [180, 6, 'z65_s180_re'],    // caught z66 → shift UP
  [181, 6, 'z75_s181_re'],    // caught z76 → shift UP
  [182, 7, 'z84_s182_re'],    // partial-right → full row, wider x
  [184, 2, 'z95_s184_re'],    // caught Dobrave-row → shift UP
  [185, 2, 'z105_s185_re'],   // caught z106-Gradac → shift UP
  [185, 7, 'z110_s185_re'],   // garbage → re-crop
];
for (const [s, idx, name] of RECROP) {
  const [y0, B] = rowY(s, Math.max(0, idx - 1));
  await crop(name, s, Math.max(0.05, y0 - 0.006), Math.min(0.99, y0 + B + 0.006), 0.02, 0.92, 3.0);
}

// --- HI-ZOOM kolumni (dueli!) ---
// z93-s184 (vrsta1): hišna-stolpec hi-zoom
{ const [y0, B] = rowY(184, 0); await crop('z93_s184_hisna_hi', 184, y0 - 0.008, y0 + B + 0.008, 0.30, 0.52, 6.0); }
// z99-s184 (vrsta7): vas-stolpec hi-zoom
{ const [y0, B] = rowY(184, 6); await crop('z99_s184_vas_hi', 184, y0 - 0.008, y0 + B + 0.008, 0.115, 0.34, 6.0); }
// z01-s173 (vrsta2): hišna hi-zoom
{ const [y0, B] = rowY(173, 1); await crop('z01_s173_hisna_hi', 173, y0 - 0.008, y0 + B + 0.008, 0.28, 0.52, 6.0); }
// z26-s176 (vrsta3): hišna hi-zoom
{ const [y0, B] = rowY(176, 2); await crop('z26_s176_hisna_hi', 176, y0 - 0.008, y0 + B + 0.008, 0.28, 0.55, 6.0); }
// s183 vrsta1: ordinal + hišna hi-zoom (84-dup!)
{ const [y0, B] = rowY(183, 0); await crop('z85_s183_ordinal_hi', 183, y0 - 0.008, y0 + B + 0.008, 0.02, 0.52, 5.0); }
// z52-s179 (vrsta4): vas hi-zoom (Griblje-vs-Praproče!)
{ const [y0, B] = rowY(179, 3); await crop('z52_s179_vas_hi', 179, y0 - 0.008, y0 + B + 0.008, 0.115, 0.36, 6.0); }
// z105-s185 (vrsta3): pripis + oče hi-zoom (desna stran!)
{ const [y0, B] = rowY(185, 2); await crop('z105_s185_oc_hi', 185, Math.max(0.05, y0 - 0.006), y0 + B + 0.006, 0.44, 0.92, 4.5); }
console.log('P222 krop pass-2: 21 izrezov');
