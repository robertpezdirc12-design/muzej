// P215 krop — KROP-dokazi (leto 1862 = 24/29!):
// MEJA-dokazi (3): s30 vsotna-vrsta-'1862'-KANDIDAT (3.-instance-invariante!) + restart-z1-PEZDIRC-glava + zap-stolpec-tail ('49–54'-vs-VLM-'29–34'-DUEL!)
// GRIBLJE-VRSTICE (9): s30 z4 + s31 z10/z11/z14/z17 + s34 z41/z43/z48/z50 (full-row 2.8×!)
// TAIL-1861-GRIBLJE (1): s30 z54-Požek (POŽEK-h67[~69!]-nit!)
// ANOMALIJA (1): s32 z30-'Mrtvogrobnik[~Mrtvorojenček?]'
// PAS-izrezi (7): desni-pas x0.55–0.95 (hisna+starost+bolezen zoom; sosedi = kalibracija!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p215';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// --- MEJA-dokazi s30 (14 vrst: tail-z49–z54 + vsota + RESTART-z1–z7; start≈0.115, band≈0.0604) ---
// r6=z54 (y≈0.417–0.477), r7=vsota (y≈0.477–0.537), r8=z1-PEZDIRC (y≈0.537–0.597), r11=z4 (y≈0.719–0.779)
await crop('arb_s30_vsota', 30, 0.455, 0.565, 0.02, 0.60, 3.0);
await crop('arb_s30_glava', 30, 0.505, 0.625, 0.02, 0.60, 3.0);
await crop('z1_s30_pezdirc', 30, 0.525, 0.635, 0.02, 0.88, 2.8);
await crop('z4_s30_grib', 30, 0.695, 0.805, 0.02, 0.88, 2.8);
await crop('z54_s30_grib', 30, 0.405, 0.515, 0.02, 0.88, 2.8);
await crop('s30_zap_stolpec', 30, 0.10, 0.56, 0.02, 0.115, 5.0);
// --- GRIBLJE full-row izrezi s31 (16 vrst: z8–z23; band≈0.0528) ---
// r3=z10 (0.221–0.273), r4=z11 (0.273–0.326), r7=z14 (0.432–0.484), r10=z17 (0.590–0.643)
await crop('z10_s31_grib', 31, 0.205, 0.315, 0.02, 0.88, 2.8);
await crop('z11_s31_grib', 31, 0.255, 0.365, 0.02, 0.88, 2.8);
await crop('z14_s31_grib', 31, 0.415, 0.525, 0.02, 0.88, 2.8);
await crop('z17_s31_grib', 31, 0.575, 0.685, 0.02, 0.88, 2.8);
// --- GRIBLJE full-row izrezi s34 (15 vrst: z40–z54; band≈0.0563) ---
// r2=z41 (0.171–0.228), r4=z43 (0.284–0.340), r9=z48 (0.563–0.620), r11=z50 (0.676–0.732)
await crop('z41_s34_grib', 34, 0.155, 0.265, 0.02, 0.88, 2.8);
await crop('z43_s34_grib', 34, 0.265, 0.375, 0.02, 0.88, 2.8);
await crop('z48_s34_grib', 34, 0.545, 0.655, 0.02, 0.88, 2.8);
await crop('z50_s34_grib', 34, 0.660, 0.770, 0.02, 0.88, 2.8);
// --- ANOMALIJA s32 z30-'Mrtvogrobnik' (r7: 0.432–0.484) ---
await crop('z30_s32_grib', 32, 0.415, 0.525, 0.02, 0.88, 2.8);
// --- PAS-izrezi (x0.55–0.95 @3.2×; sosedi = kalibracija!) ---
await crop('z4_s30_pas', 30, 0.665, 0.80, 0.55, 0.95, 3.2);
await crop('z54_s30_pas', 30, 0.37, 0.505, 0.55, 0.95, 3.2);
await crop('z1_s30_pas', 30, 0.495, 0.63, 0.55, 0.95, 3.2);
await crop('z10_s31_pas', 31, 0.19, 0.315, 0.55, 0.95, 3.2);
await crop('z11_s31_pas', 31, 0.24, 0.365, 0.55, 0.95, 3.2);
await crop('z14_s31_pas', 31, 0.40, 0.525, 0.55, 0.95, 3.2);
await crop('z17_s31_pas', 31, 0.56, 0.685, 0.55, 0.95, 3.2);
await crop('z41_s34_pas', 34, 0.14, 0.265, 0.55, 0.95, 3.2);
await crop('z43_s34_pas', 34, 0.25, 0.375, 0.55, 0.95, 3.2);
await crop('z48_s34_pas', 34, 0.53, 0.655, 0.55, 0.95, 3.2);
await crop('z50_s34_pas', 34, 0.645, 0.77, 0.55, 0.95, 3.2);
console.log('P215 krop pass-1: 24 izrezov');
