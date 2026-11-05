// P216 krop — KROP-dokazi (leto 1861 = 25/29!):
// MEJA-dokazi (2): s25 vsotna-vrsta-'1861'-KANDIDAT (4.-instance!) + restart-glava
// ZAP-DOKAZI (3): s23/s24/s25 zap-stolpci (margin-dueli: s23-'41–53'-vs-'40–52'? + s24-'53–66'-vs-'54–67'? + s25-tail-'53–59'-vs-'67–73'?)
// GRIBLJE-VRSTICE (8): s26 z7/z11/z14/z15/z17 + s28 z20/z30/z32 (full-row!)
// TAIL-1860-GRIBLJE (2): s24 z61-h24 + z65-h30
// ANOMALIJA (1): s26 z18-'April-1[?]-out-of-order'
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p216';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// --- MEJA-dokazi s25 (13 vrst: tail-z67–z73? + vsota + RESTART-z1–z5; start≈0.115, band≈0.065) ---
// r8=vsota (y≈0.57–0.635), r9=z1-restart (y≈0.635–0.70)
await crop('arb_s25_vsota', 25, 0.545, 0.655, 0.02, 0.60, 3.0);
await crop('arb_s25_glava', 25, 0.595, 0.715, 0.02, 0.60, 3.0);
await crop('z1_s25_restart', 25, 0.615, 0.725, 0.02, 0.88, 2.8);
// --- ZAP-DOKAZI (x0.02–0.115 @5×) ---
await crop('s23_zap_stolpec', 23, 0.10, 0.85, 0.02, 0.115, 5.0);
await crop('s24_zap_stolpec', 24, 0.10, 0.92, 0.02, 0.115, 5.0);
await crop('s25_zap_stolpec', 25, 0.10, 0.97, 0.02, 0.115, 5.0);
// --- GRIBLJE full-row izrezi s26 (13 vrst: z6–z18; band≈0.065) ---
// r2=z7 (0.18–0.245), r6=z11 (0.44–0.505), r9=z14 (0.635–0.70), r10=z15 (0.70–0.765), r12=z17 (0.83–0.895), r13=z18 (0.895–0.96)
await crop('z7_s26_grib', 26, 0.17, 0.28, 0.02, 0.88, 2.8);
await crop('z11_s26_grib', 26, 0.43, 0.54, 0.02, 0.88, 2.8);
await crop('z14_s26_grib', 26, 0.62, 0.73, 0.02, 0.88, 2.8);
await crop('z15_s26_grib', 26, 0.69, 0.80, 0.02, 0.88, 2.8);
await crop('z17_s26_grib', 26, 0.82, 0.93, 0.02, 0.88, 2.8);
await crop('z18_s26_grib', 26, 0.88, 0.985, 0.02, 0.88, 2.8);
// --- GRIBLJE full-row izrezi s28 (14 vrst: z19–z32; band≈0.0604) ---
// r2=z20 (0.175–0.236), r12=z30 (0.779–0.84), r14=z32 (0.90–0.96)
await crop('z20_s28_grib', 28, 0.16, 0.27, 0.02, 0.88, 2.8);
await crop('z30_s28_grib', 28, 0.77, 0.88, 0.02, 0.88, 2.8);
await crop('z32_s28_grib', 28, 0.89, 0.985, 0.02, 0.88, 2.8);
// --- TAIL-1860-GRIBLJE s24 (14 vrst; band≈0.0604) ---
// r9=z61 (0.598–0.66), r13=z65 (0.84–0.90)
await crop('z61_s24_grib', 24, 0.59, 0.70, 0.02, 0.88, 2.8);
await crop('z65_s24_grib', 24, 0.83, 0.94, 0.02, 0.88, 2.8);
// --- PAS-izrezi (x0.55–0.95 @3.2×; sosedi = kalibracija!) ---
await crop('z7_s26_pas', 26, 0.15, 0.28, 0.55, 0.95, 3.2);
await crop('z11_s26_pas', 26, 0.41, 0.54, 0.55, 0.95, 3.2);
await crop('z14_s26_pas', 26, 0.60, 0.73, 0.55, 0.95, 3.2);
await crop('z15_s26_pas', 26, 0.67, 0.80, 0.55, 0.95, 3.2);
await crop('z17_s26_pas', 26, 0.80, 0.93, 0.55, 0.95, 3.2);
await crop('z20_s28_pas', 28, 0.14, 0.27, 0.55, 0.95, 3.2);
await crop('z30_s28_pas', 28, 0.75, 0.88, 0.55, 0.95, 3.2);
await crop('z32_s28_pas', 28, 0.87, 0.985, 0.55, 0.95, 3.2);
console.log('P216 krop pass-1: 24 izrezov');
