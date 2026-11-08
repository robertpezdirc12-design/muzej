// P214 krop — KROP-dokazi (leto 1863 = 23/29!):
// MEJA-dokazi (2): s35 vsotna-vrsta-1862 + restart-'1863'-glava+z1
// GRIBLJE-VRSTICE (7): s35 z2 + s36 z12/z18 + s37 z26/z27/z33/z38 (full-row 2.8×!)
// PAS-izrezi (7): desni-pas x0.55–0.95 (hisna+starost+bolezen zoom; z sosedom zgoraj = kalibracija!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p214';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// --- MEJA-dokazi s35 (tail z55–z60 + vsota + RESTART-'1863'+z1–z2; 15 vrst, start≈0.115, band≈0.0575) ---
// vrsta 7 = vsota (y≈0.46), vrsta 8 = z1-restart (y≈0.505), vrsta 9 = z2 (y≈0.56)
await crop('arb_s35_vsota', 35, 0.42, 0.51, 0.02, 0.60, 3.0);
await crop('arb_s35_glava', 35, 0.46, 0.57, 0.02, 0.60, 3.0);
// --- GRIBLJE full-row izrezi ---
await crop('z2_s35_grib', 35, 0.545, 0.645, 0.02, 0.88, 2.8);
await crop('z12_s36_grib', 36, 0.255, 0.355, 0.02, 0.88, 2.8);
await crop('z18_s36_grib', 36, 0.60, 0.70, 0.02, 0.88, 2.8);
await crop('z26_s37_grib', 37, 0.20, 0.30, 0.02, 0.88, 2.8);
await crop('z27_s37_grib', 37, 0.255, 0.355, 0.02, 0.88, 2.8);
await crop('z33_s37_grib', 37, 0.60, 0.70, 0.02, 0.88, 2.8);
await crop('z38_s37_grib', 37, 0.885, 0.975, 0.02, 0.88, 2.8);
// --- PAS-izrezi (x0.55–0.95 @3.2×; zgornja-meja-vključuje-soseda = kalibracija!) ---
await crop('z2_s35_pas', 35, 0.51, 0.65, 0.55, 0.95, 3.2);
await crop('z12_s36_pas', 36, 0.22, 0.36, 0.55, 0.95, 3.2);
await crop('z18_s36_pas', 36, 0.565, 0.70, 0.55, 0.95, 3.2);
await crop('z26_s37_pas', 37, 0.165, 0.30, 0.55, 0.95, 3.2);
await crop('z27_s37_pas', 37, 0.22, 0.36, 0.55, 0.95, 3.2);
await crop('z33_s37_pas', 37, 0.565, 0.70, 0.55, 0.95, 3.2);
await crop('z38_s37_pas', 37, 0.85, 0.98, 0.55, 0.95, 3.2);
console.log('P214 krop pass-1: 16 izrezov');
