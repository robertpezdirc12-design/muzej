// P224 krop pass-1 — KROP-dokazi (krstna 04104, leto 1882 = 4/15!):
// ZAP-STOLPCI (15): s147–s161 (tail-1881-z83–z89 + finis + 1882-z1–z106 + restart-1883!)
// FOLIACIJA (6): s148/s153/s157/s159/s160/s161 (gola-svinčna-'sken−5'-serija! — s157-'154'-DUEL!)
// MEJA (2): arb_s147_finis (tail-1881 + 'finis' + vsotna-'anni-1881'!) + arb_s148_meja (glava-'1 8 8 2' + restart-z1!)
// MESEC-STOLPCI (3): s160 (z96–z103-ANOMALIJA-Nov-po-Dez-16!) + s159 (Dez-label-z92?) + s156 (z71-Okt/Nov-DUEL!)
// GRIBLJE-VRSTICE (25): vse-Griblje-1882!
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p224';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// geometrije: razprti-listi; ytop 0.165; B = (0.975−0.165)/n-vrstic (page-VLM-števec!)
const N = { 147: 7, 148: 8, 149: 9, 150: 8, 151: 8, 152: 7, 153: 9, 154: 8, 155: 7, 156: 7, 157: 8, 158: 8, 159: 8, 160: 8, 161: 10 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }

// --- ZAP-stolpci (ordinalna-linija!) ---
for (const p of Object.keys(N)) await crop(`s${p}_zap_stolpec`, +p, 0.05, 0.99, 0.02, 0.115, 5.0);

// --- FOLIACIJA + glave (gola-svinčna-serija!) ---
for (const p of [148, 153, 157, 159, 160, 161]) await crop(`arb_s${p}_pag`, p, 0.02, 0.17, 0.02, 0.42, 3.2);

// --- MEJA (1881/82!) ---
await crop('arb_s147_finis', 147, 0.04, 0.99, 0.02, 0.62, 2.6);  // tail-1881-z83–z89 + 'finis' + vsotna-'anni-1881'
await crop('arb_s148_meja', 148, 0.02, 0.60, 0.02, 0.62, 2.8);   // glava-'Jahr 18 82' + VSOTNA? + restart-z1-Jän-2!

// --- MESEC-STOLPCI (anomalije!) ---
await crop('s160_mesec_stolpec', 160, 0.10, 0.99, 0.09, 0.42, 4.0);  // z96–z103: Nov-po-Dez-16-ANOMALIJA!
await crop('s159_mesec_stolpec', 159, 0.10, 0.99, 0.09, 0.42, 4.0);  // z88–z95: Dez-label-pri-z92?
await crop('s156_mesec_stolpec', 156, 0.10, 0.99, 0.09, 0.42, 4.0);  // z71: Okt/Nov-DUEL!

// --- GRIBLJE full-rows (page-VLM-vrsta-indeksi, 1-based → idx0 = vrsta−1) ---
const G = [
  [148, 1, 'z02_s148_grib'],   // Anna h45
  [148, 6, 'z07_s148_grib'],   // Maria h15 — pripis-1955!
  [149, 1, 'z10_s149_grib'],   // Johann h27[~] — Kustar × Klobučar
  [150, 4, 'z22_s150_grib'],   // Agnes h14[~11?] — mati-DRAGOŠ!
  [150, 5, 'z23_s150_grib'],   // Mathias h73[~43?] — mati-PEZDIRC-Pegdire!
  [151, 3, 'z29_s151_grib'],   // Katharina h1 — Želifo × Kuržan[?]
  [151, 5, 'z31_s151_grib'],   // Josef h28[?] — LAZAR × Skarasinič + Brodarič!
  [152, 0, 'z34_s152_grib'],   // Barbara h46 — Klobučar × Mihelčič
  [153, 2, 'z43_s153_grib'],   // Maria h21 — POŽEK × Perne — pripis-†1919!
  [154, 5, 'z54_s154_grib'],   // Johann h66[~65/66] — MILEK-Milech!
  [155, 0, 'z58_s155_grib'],   // Maria h41 — Igrec × Jakofčič — pripis-1937!
  [156, 6, 'z71_s156_grib'],   // Barbara h5 — Primc[?] — MESEC-DUEL!
  [157, 1, 'z73_s157_grib'],   // Georg h40 — Petir × Jarševič
  [157, 2, 'z74_s157_grib'],   // Anton h62[~] — Hure × Brižan
  [158, 5, 'z85_s158_grib'],   // Maria h38 — Pozeb × DRAGOŠ[?]
  [158, 7, 'z87_s158_grib'],   // Barbara h16 — Fitalj × Nemanič
  [159, 1, 'z89_s159_grib'],   // Nicolaus h13 — mati-PEZDIRC-Pezdirc!
  [159, 2, 'z90_s159_grib'],   // Nicolaus h14 — mati+botra-PEZDIRC-Perdiuc!
  [159, 3, 'z91_s159_grib'],   // Josef h11 — pripis-1966!
  [159, 4, 'z92_s159_grib'],   // Johann h13 — Vlašič × Bruhar
  [159, 7, 'z95_s159_grib'],   // Barbara h35 — pripis-1971!
  [160, 1, 'z97_s160_grib'],   // Catharina h47 — anomalija-blok!
  [160, 3, 'z99_s160_grib'],   // Maria h13 — anomalija-blok + KRIŽAN-botra!
  [161, 1, 'z105_s161_grib'],  // DVOJČEK-Mathias h68!
  [161, 2, 'z106_s161_grib'],  // DVOJČEK-Barbara h68!
];
for (const [s, idx, name] of G) { const [a, b] = row(s, idx); await crop(name, s, a, b, 0.02, 0.88, 2.8); }

console.log('P224 krop pass-1: ' + (15 + 6 + 2 + 3 + 25) + ' izrezov');
