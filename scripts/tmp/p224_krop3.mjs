// P224 krop pass-3 — kalibrirani-HIŠNI-STRIPi (celoten-hišni-stolpec-na-enkrat!) + re-krops + foliacija-spoj:
// STRIPi (x0.44–0.68 — hišni-stolpec!): s150, s151, s154, s155, s156, s158, s159, s160
// RE-KROPS: z31_s151_grib3, z71_s156_grib3, z85_s158_grib3, z95_s159_grib3
// FOLIACIJA-SPOJ: s162/s163/s164-pag (skok-s161→s165: '155'→'160' = sken−6-ali-sken−5?!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p224';
fs.mkdirSync(`${TMP}/krop3`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop3/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}

// --- HIŠNI-STRIPi (top-down-vsi-številki!) ---
for (const p of [150, 151, 154, 155, 156, 158, 159, 160]) await crop(`s${p}_hisna_strip`, p, 0.14, 0.99, 0.44, 0.68, 5.5);

// --- RE-KROPS (driftane-vrstice!) ---
await crop('z31_s151_grib3', 151, 0.495, 0.625, 0.02, 0.88, 2.8);
await crop('z71_s156_grib3', 156, 0.775, 0.92, 0.02, 0.98, 3.0);
await crop('z85_s158_grib3', 158, 0.545, 0.675, 0.02, 0.88, 2.8);
await crop('z95_s159_grib3', 159, 0.785, 0.92, 0.02, 0.98, 3.0);

// --- FOLIACIJA-SPOJ (s161='155' vs s165='160' — skok ali misread?!) ---
for (const p of [162, 163, 164]) await crop(`arb_s${p}_pag3`, p, 0.02, 0.17, 0.02, 0.42, 3.4);

console.log('P224 krop pass-3: stripi-8 + re-krops-4 + pag-3');
