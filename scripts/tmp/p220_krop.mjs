// P220 krop — KROP-dokazi (leto 1857 = 29/29 — ZADNJE leto knjige 04106!):
// KNJIGA-START (1): arb_s2_start ('1857'-glava + restart-z1 + NASLOVNA-LISTA-'Sterb-Buch.'-razprta!)
// MEJA-dokaz re-križ (1): arb_s7_meja (tail-1857-z73/z74 + VSOTNA-'1 8 [5 8]'-marker-P214-TIP-3.-INSTANCE!)
// ZAP-STOLPCI (7): s2–s7 (ordinalna-linija-1–74-dokaz! + s3-z32-ordinal-proba + s7-tail-ordinali!)
// GRIBLJE-VRSTICE (12): s2-z4/z5/z10 + s4-z45 + s5-z50/z56/z58 + s6-z61/z71 + s7-tail-z73/z74
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p220';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// geometrije: razprti-naslovni-listi (s2–s7): ytop 0.155; B = (0.97−0.155)/n-vrstic
const G = {
  2: { ytop: 0.155, B: (0.97 - 0.155) / 16 },
  3: { ytop: 0.155, B: (0.97 - 0.155) / 16 },
  4: { ytop: 0.155, B: (0.97 - 0.155) / 13 },
  5: { ytop: 0.155, B: (0.97 - 0.155) / 13 },
  6: { ytop: 0.155, B: (0.97 - 0.155) / 14 },
  7: { ytop: 0.155, B: 0.0508 },   // P219-geometrija (tail r1–r2 + vsotna + restart r1–r12)
};
function row(sken, idx0) { const g = G[sken]; const y0 = g.ytop + idx0 * g.B; return [y0 - 0.010, y0 + g.B + 0.010]; }

// --- KNJIGA-START + MEJA-dokazi ---
await crop('arb_s2_start', 2, 0.10, 0.40, 0.02, 0.62, 2.6);   // naslovna-lista + '1857'-glava + restart-z1
await crop('arb_s7_meja', 7, 0.05, 0.45, 0.02, 0.62, 2.6);    // re-križ-P219: tail + VSOTNA-'1 8 [5 8]'!
// --- ZAP-stolpci (ordinalna-linija!) ---
for (const p of [2, 3, 4, 5, 6]) await crop(`s${p}_zap_stolpec`, p, 0.05, 0.99, 0.02, 0.115, 5.0);
await crop('s7_zap_tail', 7, 0.14, 0.30, 0.02, 0.115, 5.0);   // tail-ordinali-73/74-proba!
// --- GRIBLJE full-rows ---
let [a, b2] = row(2, 3);  await crop('z04_s2_grib', 2, a, b2, 0.02, 0.88, 2.8);
[a, b2] = row(2, 4);      await crop('z05_s2_grib', 2, a, b2, 0.02, 0.88, 2.8);
[a, b2] = row(2, 9);      await crop('z10_s2_grib', 2, a, b2, 0.02, 0.88, 2.8);
[a, b2] = row(3, 15);     await crop('z32_s3_zadnja', 3, a, b2, 0.02, 0.88, 2.8);  // ordinal-proba!
[a, b2] = row(4, 12);     await crop('z45_s4_grib', 4, a, b2, 0.02, 0.88, 2.8);
[a, b2] = row(5, 4);      await crop('z50_s5_grib', 5, a, b2, 0.02, 0.88, 2.8);
[a, b2] = row(5, 10);     await crop('z56_s5_grib', 5, a, b2, 0.02, 0.88, 2.8);
[a, b2] = row(5, 12);     await crop('z58_s5_grib', 5, a, b2, 0.02, 0.88, 2.8);
[a, b2] = row(6, 2);      await crop('z61_s6_grib', 6, a, b2, 0.02, 0.88, 2.8);
[a, b2] = row(6, 12);     await crop('z71_s6_grib', 6, a, b2, 0.02, 0.88, 2.8);
[a, b2] = row(7, 0);      await crop('z73_s7_tail', 7, a, b2, 0.02, 0.88, 2.8);
[a, b2] = row(7, 1);      await crop('z74_s7_tail', 7, a, b2, 0.02, 0.88, 2.8);   // GRIBLJE-h36-TAIL!
console.log('P220 krop pass-1: 21 izrezov');
