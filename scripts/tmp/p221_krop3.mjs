// P221 krop pass-3 — re-crops zgrešenih vrstic + hi-zoom dueli (geometrija-kalibracija iz pass-1/2!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p221';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// s187: vrstici z5 + z6 (zgornji del tabele)
await crop('r3_z05_z06_s187', 187, 0.10, 0.36, 0.02, 0.88, 3.0);
// s188: z20 (zadnja vrstica)
await crop('r3_z20_s188', 188, 0.80, 0.99, 0.02, 0.88, 3.0);
// s189: z26 (Maria-Griblje) + z27/z28 (Johann + Margaretha-Griblje)
await crop('r3_z26_s189', 189, 0.44, 0.66, 0.02, 0.88, 3.0);
await crop('r3_z27_z28_s189', 189, 0.66, 0.99, 0.02, 0.88, 3.0);
// s193: z57 (Michael-Griblje) + z59 (Marko/Maria/Martin-DUEL!) + z62 (Georg-Griblje)
await crop('r3_z57_s193', 193, 0.30, 0.48, 0.02, 0.88, 3.0);
await crop('r3_z59_s193', 193, 0.50, 0.70, 0.02, 0.88, 3.0);
await crop('r3_z62_s193', 193, 0.78, 0.99, 0.02, 0.88, 3.0);
// s194: z68 (Mathias-Griblje h55)
await crop('r3_z68_s194', 194, 0.50, 0.72, 0.02, 0.88, 3.0);
// s196: z78 (Katharina — hiša-TRI-DUEL 17/29/9!) + z82 (Katharina h2) + z85 (Mathias — mati-PEZDIRC!)
await crop('r3_z78_s196', 196, 0.10, 0.32, 0.02, 0.88, 3.0);
await crop('r3_z82_s196', 196, 0.48, 0.70, 0.02, 0.88, 3.0);
await crop('r3_z85_s196', 196, 0.78, 0.99, 0.02, 0.88, 3.0);
// s199: z104 (Anton-Griblje-h8-TAIL!) — vrstici so višje (y ~0.2–0.6)
await crop('r3_z104_s199', 199, 0.28, 0.62, 0.02, 0.88, 3.0);
// hi-zoom hišni-stolpec: z37-s190 (55/53-duel) + z78-s196 (17/29/9-TRI!) + z59-s193 (27/47/37-TRI!)
await crop('r3_hisna_z37_s190', 190, 0.855, 0.99, 0.26, 0.50, 6.0);
await crop('r3_hisna_z78_s196', 196, 0.10, 0.24, 0.26, 0.50, 6.0);
await crop('r3_hisna_z59_s193', 193, 0.50, 0.64, 0.26, 0.50, 6.0);
console.log('P221 krop pass-3: 15 izrezov');
