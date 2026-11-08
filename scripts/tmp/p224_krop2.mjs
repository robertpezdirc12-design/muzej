// P224 krop pass-2 — re-krops z ročnimi y-okni (drift!) + hišne-hi-zoome + posebni:
// RE-KROPS (drift-down-popravki): z7_s148, z31_s151, z85_s158, z95_s159, z99_s160, z106_s161, z71_s156
// HIŠNI-HI-ZOOMI (DUELI!): z22(14/11), z23(73/43), z54(66/65), z58(41/11), z90(14/74), z91(11/44),
//   z92(13/43), z97(47/17), z99(13), z29(1), z31(28), z74(62), z89(13), z105+106(68), z2(45), z34(46), z43(21)
// POSEBNI: s160_mesec_wide (z96-labela!), s147_dno (finis + vsotna-1881!), s157_pag2 ('151/154/157'-DUEL!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p224';
fs.mkdirSync(`${TMP}/krop2`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop2/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}

// --- RE-KROPS (ročna-y-okna!) ---
await crop('z07_s148_grib2', 148, 0.745, 0.865, 0.02, 0.88, 2.8);
await crop('z31_s151_grib2', 151, 0.595, 0.715, 0.02, 0.88, 2.8);
await crop('z85_s158_grib2', 158, 0.635, 0.755, 0.02, 0.88, 2.8);
await crop('z95_s159_grib2', 159, 0.845, 0.975, 0.02, 0.98, 2.8);
await crop('z99_s160_grib2', 160, 0.415, 0.545, 0.02, 0.88, 2.8);
await crop('z106_s161_grib2', 161, 0.305, 0.395, 0.02, 0.88, 2.8);
await crop('z71_s156_grib2', 156, 0.835, 0.985, 0.02, 0.75, 3.0);

// --- POSEBNI ---
await crop('s160_mesec_wide', 160, 0.10, 0.99, 0.02, 0.47, 4.2);   // z96-labela + meseci z96–z103!
await crop('s147_dno', 147, 0.80, 1.00, 0.02, 0.98, 3.0);          // finis + vsotna-'anni-1881'?
await crop('s157_pag2', 157, 0.03, 0.16, 0.02, 0.30, 5.0);         // '151/154/157'-DUEL!
await crop('s148_glava_zap', 148, 0.10, 0.30, 0.02, 0.50, 4.0);    // glava-'Jahr 18 82' + z1-z2-zap-region!

// --- HIŠNI-HI-ZOOMI (x-okno: vas+hišna-stolpec!) ---
const H = [
  [148, 0.245, 0.375, 'z02_s148_hisna_hi'],    // h45
  [148, 0.745, 0.865, 'z07_s148_hisna_hi'],    // h15
  [149, 0.255, 0.375, 'z10_s149_hisna_hi'],    // h27
  [150, 0.545, 0.665, 'z22_s150_hisna_hi'],    // 14/11-DUEL!
  [150, 0.645, 0.765, 'z23_s150_hisna_hi'],    // 73/43-DUEL!
  [151, 0.495, 0.615, 'z29_s151_hisna_hi'],    // h1
  [151, 0.595, 0.715, 'z31_s151_hisna_hi'],    // h28
  [152, 0.155, 0.275, 'z34_s152_hisna_hi'],    // h46
  [153, 0.355, 0.475, 'z43_s153_hisna_hi'],    // h21
  [154, 0.745, 0.865, 'z54_s154_hisna_hi'],    // 66/65-DUEL!
  [155, 0.155, 0.275, 'z58_s155_hisna_hi'],    // 41/11-DUEL!
  [156, 0.835, 0.985, 'z71_s156_hisna_hi'],    // h5
  [157, 0.245, 0.365, 'z73_s157_hisna_hi'],    // h40
  [157, 0.345, 0.465, 'z74_s157_hisna_hi'],    // h62
  [158, 0.635, 0.755, 'z85_s158_hisna_hi'],    // h38
  [158, 0.845, 0.975, 'z87_s158_hisna_hi'],    // h16
  [159, 0.245, 0.365, 'z89_s159_hisna_hi'],    // h13
  [159, 0.345, 0.465, 'z90_s159_hisna_hi'],    // 14/74-DUEL!
  [159, 0.445, 0.565, 'z91_s159_hisna_hi'],    // 11/44-DUEL!
  [159, 0.545, 0.665, 'z92_s159_hisna_hi'],    // 13/43-DUEL!
  [160, 0.245, 0.365, 'z97_s160_hisna_hi'],    // 47/17-DUEL!
  [160, 0.415, 0.545, 'z99_s160_hisna_hi'],    // h13
  [161, 0.225, 0.395, 'z105_106_s161_hisna_hi'], // h68-×2-DVOJČKI!
];
for (const [s, a, b, name] of H) await crop(name, s, a, b, 0.30, 0.62, 6.0);

console.log('P224 krop pass-2: re-krops-7 + posebni-4 + hi-zoomi-23');
