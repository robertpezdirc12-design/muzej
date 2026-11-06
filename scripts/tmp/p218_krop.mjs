// P218 krop — KROP-dokazi (leto 1859 = 27/29!):
// MEJA-dokaz (1): s11 tail-1858 (54–57) + VSOTNA-'1 8 5 9'-marker + '1859'-glava + restart-z1!
// ZAP-STOLPCI (7): s11/s12/s13/s15/s16/s18(KROP-80–91-reverdict)/s19(93–103?-duel-vs-P217-z95/z100!)
// GRIBLJE-VRSTICE (22) + DVOJNA-21 + z20-duel + z56-duel + s19-glava
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p218';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// band po straneh (vrstice čez y 0.09–0.98)
const B = { 11: 0.0742, 12: 0.0685, 13: 0.0636, 14: 0.0809, 15: 0.0742, 16: 0.0742, 17: 0.0742, 18: 0.0742 };
function row(sken, vrsta, ytop = 0.09) { const b = B[sken]; const y0 = ytop + (vrsta - 1) * b; return [y0 - 0.006, y0 + b + 0.006]; }
// --- MEJA-dokaz s11 ---
await crop('arb_s11_meja', 11, 0.05, 0.42, 0.02, 0.62, 2.6);
await crop('s11_zap_stolpec', 11, 0.05, 0.99, 0.02, 0.115, 5.0);
// --- ZAP-stolpci duel-dokazi ---
await crop('s12_zap_stolpec', 12, 0.05, 0.99, 0.02, 0.115, 5.0);
await crop('s13_zap_stolpec', 13, 0.05, 0.99, 0.02, 0.115, 5.0);
await crop('s15_zap_stolpec', 15, 0.05, 0.99, 0.02, 0.115, 5.0);
await crop('s16_zap_stolpec', 16, 0.05, 0.99, 0.02, 0.115, 5.0);
await crop('s18_zap_stolpec', 18, 0.05, 0.99, 0.02, 0.115, 5.0);
await crop('s19_zap_stolpec', 19, 0.05, 0.99, 0.02, 0.115, 5.0);
await crop('s19_glava', 19, 0.03, 0.18, 0.02, 0.60, 2.6);
// --- GRIBLJE full-rows (22) + strukturne ---
let [a, b2] = row(11, 11); await crop('z6_s11_grib', 11, a, b2, 0.02, 0.88, 2.8);          // h69 Jän
[a, b2] = row(12, 2);  await crop('z9_s12_grib', 12, a, b2, 0.02, 0.88, 2.8);              // h21 Feb
[a, b2] = row(12, 9);  await crop('z16_s12_grib', 12, a, b2, 0.02, 0.88, 2.8);             // h37 Mär
[a, b2] = row(12, 12); await crop('z19_s12_grib', 12, a, b2, 0.02, 0.88, 2.8);             // h39 Mär
[a, b2] = row(12, 13); await crop('z20_s12_row', 12, a, b2, 0.02, 0.88, 2.8);              // z20-DUEL (mesec!)
[a, b2] = row(13, 1);  await crop('z20_s13_row', 13, a, b2, 0.02, 0.88, 2.8);              // z20-März-tail?
[a, b2] = row(13, 2);  await crop('z21_s13_dvojna', 13, a, b2, 0.02, 0.88, 2.8);           // DVOJNA-21!
[a, b2] = row(13, 5);  await crop('z24_s13_grib', 13, a, b2, 0.02, 0.88, 2.8);             // h65 Apr
[a, b2] = row(13, 6);  await crop('z25_s13_grib', 13, a, b2, 0.02, 0.88, 2.8);             // h57 Apr
[a, b2] = row(13, 12); await crop('z31_s13_grib', 13, a, b2, 0.02, 0.88, 2.8);             // h5 Mai
[a, b2] = row(13, 13); await crop('z32_s13_grib', 13, a, b2, 0.02, 0.88, 2.8);             // h19 Mai
[a, b2] = row(14, 1);  await crop('z34_s14_grib', 14, a, b2, 0.02, 0.88, 2.8);             // h26 Mai
[a, b2] = row(14, 2);  await crop('z35_s14_grib', 14, a, b2, 0.02, 0.88, 2.8);             // h58 Mai
[a, b2] = row(15, 2);  await crop('z46_s15_grib', 15, a, b2, 0.02, 0.88, 2.8);             // h52 Jul
[a, b2] = row(15, 8);  await crop('z52_s15_grib', 15, a, b2, 0.02, 0.88, 2.8);             // h39 Aug
[a, b2] = row(15, 9);  await crop('z53_s15_grib', 15, a, b2, 0.02, 0.88, 2.8);             // h5 Aug
[a, b2] = row(15, 12); await crop('z56_s15_row', 15, a, b2, 0.02, 0.88, 2.8);              // z56-DUEL!
[a, b2] = row(16, 1);  await crop('z56_s16_row', 16, a, b2, 0.02, 0.88, 2.8);              // z56-DUEL!
[a, b2] = row(16, 2);  await crop('z57_s16_grib', 16, a, b2, 0.02, 0.88, 2.8);             // h19 Aug
[a, b2] = row(16, 6);  await crop('z61_s16_grib', 16, a, b2, 0.02, 0.88, 2.8);             // h33 Aug
[a, b2] = row(16, 9);  await crop('z64_s16_grib', 16, a, b2, 0.02, 0.88, 2.8);             // h74 Aug
[a, b2] = row(16, 10); await crop('z65_s16_grib', 16, a, b2, 0.02, 0.88, 2.8);             // h29 Aug
[a, b2] = row(17, 6);  await crop('z73_s17_grib', 17, a, b2, 0.02, 0.88, 2.8);             // h20 Sep/Okt
[a, b2] = row(17, 9);  await crop('z76_s17_grib', 17, a, b2, 0.02, 0.88, 2.8);             // h24 Okt
[a, b2] = row(18, 2);  await crop('z81_s18_grib', 18, a, b2, 0.02, 0.88, 2.8);             // h52 Okt (KROP-margin!)
[a, b2] = row(18, 7);  await crop('z86_s18_grib', 18, a, b2, 0.02, 0.88, 2.8);             // h21 Nov (KROP-margin!)
// s19: tabela nižje (naslovni list!) — y-top 0.15, 11 vrst
const B19 = 0.0755;
function row19(vrsta) { const y0 = 0.15 + (vrsta - 1) * B19; return [y0 - 0.006, y0 + B19 + 0.006]; }
[a, b2] = row19(2); await crop('z94_s19_grib', 19, a, b2, 0.02, 0.88, 2.8);                // h49 Dez (P217-'z95'!)
[a, b2] = row19(5); await crop('z97_s19_grib', 19, a, b2, 0.02, 0.88, 2.8);                // h65 Dez (P217-'z100'!)
// --- PAS-izrezi (ključni dueli) ---
[a, b2] = row(11, 11); await crop('z6_s11_pas', 11, a, b2, 0.55, 0.95, 3.2);
[a, b2] = row19(2); await crop('z94_s19_pas', 19, a, b2, 0.55, 0.95, 3.2);
[a, b2] = row19(5); await crop('z97_s19_pas', 19, a, b2, 0.55, 0.95, 3.2);
[a, b2] = row(18, 2); await crop('z81_s18_pas', 18, a, b2, 0.55, 0.95, 3.2);
console.log('P218 krop pass-1: 38 izrezov');
