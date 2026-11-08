// P226 krop pass-2 — KOMPLET (krstna 04104, leto 1880 = 6/15!):
// ZAP-STOLPCI (16): s120–s135 | FOLIACIJA (17): s119–s135 | MEJA (3): s119-tail + s120-meja + velike-cifre!
// MESEC-STOLPCI (13) | GRIBLJE (22) + POSEBNI (13: dvojčki/Mißgeburt/date-note/name-cross/long-note/Ludblundus...)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p226';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
const N = { 119: 5, 120: 8, 121: 9, 122: 9, 123: 8, 124: 7, 125: 9, 126: 7, 127: 6, 128: 7, 129: 8, 130: 7, 131: 8, 132: 8, 133: 7, 134: 7, 135: 7 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }

// --- ZAP-stolpci ---
for (const p of [120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135]) await crop(`s${p}_zap_stolpec`, p, 0.05, 0.99, 0.02, 0.115, 5.0);
// --- FOLIACIJA ---
for (const p of [119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135]) await crop(`arb_s${p}_pag`, p, 0.02, 0.17, 0.02, 0.42, 3.2);
// --- MEJA ---
await crop('arb_s119_tail', 119, 0.02, 0.99, 0.02, 0.62, 2.4);   // TAIL-1879-z92–z96 + Schnörkel + 'Jahr 1879' + BREZ-VSOTNE!
await crop('arb_s120_meja', 120, 0.02, 0.45, 0.02, 0.62, 2.8);   // velike-cifre-'1/8/8/0' + glava + z1-RESTART-Dobravce-h11!
await crop('arb_s120_velike_cifre', 120, 0.15, 0.30, 0.02, 0.62, 3.2); // P214-TIP-velike-cifre-zoom!
// --- MESEC-STOLPCI (chronologija!) ---
await crop('s120_mesec_stolpec', 120, 0.10, 0.99, 0.04, 0.30, 4.0);  // Jän-3→Feb-3 (z1–z8!)
await crop('s121_mesec_stolpec', 121, 0.10, 0.99, 0.04, 0.30, 4.0);  // Feb-6→Mär-24 (z9–z17!)
await crop('s124_mesec_stolpec', 124, 0.10, 0.99, 0.04, 0.30, 4.0);  // Mär-29→Apr-14 (z35–z41!)
await crop('s125_mesec_stolpec', 125, 0.10, 0.99, 0.04, 0.30, 4.0);  // Apr-18→Mai-8 (z42–z50!)
await crop('s127_mesec_stolpec', 127, 0.10, 0.99, 0.04, 0.30, 4.0);  // Mai-29→Juni-13 (z58–z63!)
await crop('s128_mesec_stolpec', 128, 0.10, 0.99, 0.04, 0.30, 4.0);  // Juni-15→Juli-11 (z64–z70!)
await crop('s130_mesec_stolpec', 130, 0.10, 0.99, 0.04, 0.30, 4.0);  // 'Juni'?-29→Aug-29 (z79–z85! JULI-MISREAD-TARGET!)
await crop('s131_mesec_stolpec', 131, 0.10, 0.99, 0.04, 0.30, 4.0);  // Aug-31→Okt-12 (z86–z93!)
await crop('s133_mesec_stolpec', 133, 0.10, 0.99, 0.04, 0.30, 4.0);  // Nov-2→19 (z102–z108!)
await crop('s134_mesec_stolpec', 134, 0.10, 0.99, 0.04, 0.30, 4.0);  // Nov-19→Dez-3 (z109–z115!)
// --- GRIBLJE full-rows (22!) ---
const G = [
  [121, 1, 'z10_s121_grib'],   // Anna h2 — oče-garble (Milebeč?)
  [121, 2, 'z11_s121_grib'],   // Maria h9 — † 21.8.1935!
  [121, 5, 'z14_s121_grib'],   // Maria h39 — SIMEC-oče!
  [122, 8, 'z26_s122_grib'],   // Anna h13 — KRIŽAN-matec + blue-1969!
  [123, 4, 'z31_s123_grib'],   // Barbara h60 — ŽELKO ×2 + KRIŽAN ×2!
  [124, 0, 'z35_s124_grib'],   // Georg h53 — PEZDIRC ×2!
  [124, 1, 'z36_s124_grib'],   // Anna h35 — KRIŽAN-oče!
  [125, 4, 'z46_s125_grib'],   // Anna h27 — MILEK + BRODARIČ-botra + blue-1957!
  [126, 0, 'z51_s126_grib'],   // Anna h19 — ŠIMEC-boter!
  [126, 3, 'z54_s126_grib'],   // Maria h27 — JAKOFČIČ-botra!
  [127, 0, 'z58_s127_grib'],   // Peter h7 — TOTER-garble + SIMEC-boter!
  [127, 3, 'z61_s127_grib'],   // Joannes h21 — BRODARIČ-botra!
  [128, 1, 'z65_s128_grib'],   // Joannes h24 — JAKOFČIČ-matec!
  [128, 5, 'z69_s128_grib'],   // Anna h42 — KRIŽAN ×2!
  [129, 1, 'z72_s129_grib'],   // Anna h24 — MILEK-botra!
  [131, 2, 'z88_s131_grib'],   // Nicolaus h10
  [131, 3, 'z89_s131_grib'],   // Anna h43 — † 13.9.1940!
  [132, 1, 'z95_s132_grib'],   // Johann h18 — Okt!
  [132, 5, 'z99_s132_grib'],   // Katharina h33 — PEZDIRC ×2-botra/boter!
  [132, 7, 'z101_s132_grib'],  // Katharina h29 — MILEK-oče + KRIŽAN-matec!
  [133, 2, 'z104_s133_grib'],  // Maria h44 — KRIŽAN-matec!
  [134, 5, 'z114_s134_grib'],  // Barbara h5 — NEZAKONSKI + Dez-1/2!
];
for (const [s, idx, name] of G) { const [a, b] = row(s, idx); await crop(name, s, a, b, 0.02, 0.88, 2.8); }
// --- POSEBNI ---
{ const [a,b] = row(120,4); await crop('z05z06_dvojcki_s120', 120, a-0.005, b+0.05, 0.02, 0.88, 2.6); }   // DVOJČKI-Boršt-h20!
{ const [a,b] = row(129,5); await crop('z76z77_missgeburt_s129', 129, a-0.005, b+0.05, 0.02, 0.88, 2.6); } // Mißgeburt ×2!
{ const [a,b] = row(125,7); await crop('z49_datum_opomba_s125', 125, a, b, 0.02, 0.88, 3.0); }            // 'den 17. Juli 1880 zuzschreiben'!
{ const [a,b] = row(132,6); await crop('z100_imenski_popravek_s132', 132, a, b, 0.02, 0.88, 3.0); }       // Alois→Alojzija + att.!
{ const [a,b] = row(133,3); await crop('z105_dolg_pripis_s133', 133, a, b, 0.02, 0.88, 3.0); }            // Maria-Josephina-long-note!
{ const [a,b] = row(134,1); await crop('z110_ludblundus_s134', 134, a, b, 0.02, 0.88, 3.0); }             // krsten-prazen!
{ const [a,b] = row(127,1); await crop('z59_prazen_ocec_s127', 127, a, b, 0.02, 0.88, 3.0); }             // nezakonski + note!
{ const [a,b] = row(126,5); await crop('z56_kaplisee_s126', 126, a, b, 0.02, 0.88, 3.0); }                // nezakonski + X!
{ const [a,b] = row(130,0); await crop('z79_nezakonski_s130', 130, a, b, 0.02, 0.88, 3.0); }              // nezakonski!
{ const [a,b] = row(130,6); await crop('z85_nezakonski_s130', 130, a, b, 0.02, 0.88, 3.0); }              // nezakonski + von-origins!
{ const [a,b] = row(123,3); await crop('z30_nezakonski_s123', 123, a, b, 0.02, 0.88, 3.0); }              // nezakonski!
{ const [a,b] = row(131,1); await crop('z87_spol_x_s131', 131, a, b, 0.02, 0.88, 3.0); }                  // spol-✗-mark!
{ const [a,b] = row(124,4); await crop('z39_opomba_s124', 124, a, b, 0.02, 0.88, 3.0); }                  // '2½ 1788'-note!
{ const [a,b] = row(125,5); await crop('z49b_borst_vas_s125', 125, a, b, 0.02, 0.30, 4.0); }              // Boršt-vas + note!
console.log('P226 krop pass-2 DONE');
