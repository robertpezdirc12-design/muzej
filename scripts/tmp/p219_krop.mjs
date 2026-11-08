// P219 krop — KROP-dokazi (leto 1858 = 28/29!):
// MEJA-dokazi (3): arb_s7_meja (tail-1857 73–74 + VSOTNA-'1 8 5 8'-marker + restart-z1!) +
//   arb_s9_glava + arb_s10_glava (naslovna-lista-diagonalne-letnice!) + arb_s11_meja (re-križ-P218!)
// ZAP-STOLPCI (5): s7/s8/s9/s10/s11 (5× — čista-ordinalna-linija-1–57-dokaz!)
// GLAVA-s8: diagonalna-'1858'!
// GRIBLJE-VRSTICE (12): s8-z15/z16/z17 (Zwillinge!) + s9-z27/z37/z39 + s10-z42/z47/z51/z52
//   + s7-tail-z73/z74 (1857-MEJA!) + s11-tail-54–57 (4 — re-križ!)
// PAS-izrezi (5) + PODPISI (3)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p219';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// geometrije: naslovni-listi (s7/s9/s10): ytop 0.155; s8: ytop 0.155; s11: P218 (0.09/0.0742)
const G = {
  7:  { ytop: 0.155, B: 0.0508, restart0: 0.32 },   // tail r1–r2 + vsotna + restart r1–r12
  8:  { ytop: 0.155, B: 0.0515 },                    // rows 12–25 (14)
  9:  { ytop: 0.155, B: 0.0564 },                    // rows 26–39 (14)
  10: { ytop: 0.155, B: 0.0564 },                    // rows 40–53 (14)
  11: { ytop: 0.09,  B: 0.0742 },                    // P218: tail 54–57 (r1–r4) + vsotna (r5) + restart 1–7 (r6–r12)
};
function row(sken, idx0) { const g = G[sken]; const y0 = g.ytop + idx0 * g.B; return [y0 - 0.006, y0 + g.B + 0.006]; }
// s7 restart-vrstice (z1 = idx0 0 pri 0.32): posebna geometrija
function row7restart(idx0) { const y0 = 0.32 + idx0 * 0.0508; return [y0 - 0.006, y0 + 0.0508 + 0.006]; }

// --- MEJA-dokazi ---
await crop('arb_s7_meja', 7, 0.05, 0.45, 0.02, 0.62, 2.6);
await crop('arb_s9_glava', 9, 0.10, 0.26, 0.02, 0.40, 3.0);
await crop('arb_s10_glava', 10, 0.10, 0.26, 0.02, 0.40, 3.0);
await crop('arb_s11_meja', 11, 0.05, 0.42, 0.02, 0.62, 2.6);
await crop('s8_glava_1858', 8, 0.11, 0.24, 0.02, 0.30, 3.0);
// --- ZAP-stolpci (5×) ---
for (const p of [7, 8, 9, 10, 11]) await crop(`s${p}_zap_stolpec`, p, 0.05, 0.99, 0.02, 0.115, 5.0);
// --- GRIBLJE full-rows (1858) ---
let [a, b2] = row(8, 3);  await crop('z15_s8_grib', 8, a, b2, 0.02, 0.88, 2.8);   // Griblje h49-vs-19-DUEL!
[a, b2] = row(8, 4);      await crop('z16_s8_grib', 8, a, b2, 0.02, 0.88, 2.8);   // h19 Ana Simic
[a, b2] = row(8, 5);      await crop('z17_s8_grib', 8, a, b2, 0.02, 0.88, 2.8);   // h19 Zwilling!
[a, b2] = row(9, 1);      await crop('z27_s9_grib', 9, a, b2, 0.02, 0.88, 2.8);   // Griblje h19 Kreite!
[a, b2] = row(9, 11);     await crop('z37_s9_grib', 9, a, b2, 0.02, 0.88, 2.8);   // h60 Juni
[a, b2] = row(9, 13);     await crop('z39_s9_grib', 9, a, b2, 0.02, 0.88, 2.8);   // h65 Keržan?
[a, b2] = row(10, 2);     await crop('z42_s10_grib', 10, a, b2, 0.02, 0.88, 2.8); // h3 Horvat-Kind
[a, b2] = row(10, 7);     await crop('z47_s10_grib', 10, a, b2, 0.02, 0.88, 2.8); // h2 Fenz
[a, b2] = row(10, 11);    await crop('z51_s10_grib', 10, a, b2, 0.02, 0.88, 2.8); // h44 Strovs
[a, b2] = row(10, 12);    await crop('z52_s10_grib', 10, a, b2, 0.02, 0.88, 2.8); // h50 PADIRE-PEZDIRC-MREŽA!
// --- s7-tail (1857-MEJA) + s11-tail (1858 re-križ) ---
[a, b2] = row(7, 0);      await crop('z73_s7_tail', 7, a, b2, 0.02, 0.88, 2.8);   // 1857 Gradac
[a, b2] = row(7, 1);      await crop('z74_s7_tail', 7, a, b2, 0.02, 0.88, 2.8);   // 1857 GRIBLJE h36!
for (let i = 0; i < 4; i++) { [a, b2] = row(11, i); await crop(`s11_tail_z${54 + i}`, 11, a, b2, 0.02, 0.88, 2.8); }
// --- PAS-izrezi (ključni dueli) ---
[a, b2] = row(8, 3);  await crop('z15_s8_pas', 8, a, b2, 0.55, 0.95, 3.2);
[a, b2] = row(8, 5);  await crop('z17_s8_pas', 8, a, b2, 0.55, 0.95, 3.2);
[a, b2] = row(9, 1);  await crop('z27_s9_pas', 9, a, b2, 0.55, 0.95, 3.2);
[a, b2] = row(9, 13); await crop('z39_s9_pas', 9, a, b2, 0.55, 0.95, 3.2);
[a, b2] = row(10, 12); await crop('z52_s10_pas', 10, a, b2, 0.55, 0.95, 3.2);
// --- PODPISI (duhovnik-dueli) ---
[a, b2] = row(8, 0);  await crop('s8_r12_duh', 8, a, b2, 0.72, 0.95, 4.0);
[a, b2] = row(9, 0);  await crop('s9_r1_duh', 9, a, b2, 0.72, 0.95, 4.0);
[a, b2] = row(10, 0); await crop('s10_r1_duh', 10, a, b2, 0.72, 0.95, 4.0);
console.log('P219 krop pass-1: 33 izrezov');
