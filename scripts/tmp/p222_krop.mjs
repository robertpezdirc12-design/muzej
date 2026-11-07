// P222 krop pass-1 — KROP-dokazi (krstna 04104, leto 1884 = 2/15):
// ZAP-STOLPCI (14): s173–s186 (ordinalna-linija-1–112-dokaz!)
// FOLIACIJA (5): s173/s177/s181/s185/s186 (pag = sken+13-hipoteza!)
// MEJA (2): arb_s173_meja (tail-1883-z99 + VSOTNA-'1/8/8/4'-TIP + restart-z1!) + arb_s186_meja (tail-1884 + VSOTNA-1885 + restart!)
// GRIBLJE-VRSTICE (22): vse-Griblje-1884!
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p222';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// geometrije: razprti-listi; ytop 0.165; B = (0.975−0.165)/n-vrstic (page-VLM-števec!)
const N = { 173: 8, 174: 7, 175: 9, 176: 8, 177: 8, 178: 10, 179: 10, 180: 10, 181: 8, 182: 8, 183: 9, 184: 9, 185: 8, 186: 7 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }

// --- ZAP-stolpci (ordinalna-linija!) ---
for (const p of Object.keys(N)) await crop(`s${p}_zap_stolpec`, +p, 0.05, 0.99, 0.02, 0.115, 5.0);

// --- FOLIACIJA + glave (pag = sken+13!) ---
for (const p of [173, 177, 181, 185, 186]) await crop(`arb_s${p}_pag`, p, 0.02, 0.17, 0.02, 0.42, 3.2);

// --- MEJA ---
await crop('arb_s173_meja', 173, 0.04, 0.55, 0.02, 0.62, 2.8);  // tail-1883-z99 + VSOTNA-'1/8/8/4' + restart-z1
await crop('arb_s186_meja', 186, 0.04, 0.52, 0.02, 0.62, 2.8);  // tail-1884-z111+z112 + VSOTNA-'1/8/8/5' + restart-z1 (re-križ-P221!)

// --- GRIBLJE full-rows (page-VLM-vrsta-indeksi, 1-based → idx0 = vrsta−1) ---
const G = [
  [173, 1, 'z01_s173_grib'],                     // RESTART-z1 Johann h34[~3?] — Jänner 1/1!
  [175, 4, 'z19_s175_grib'],                     // Katharina h13 — pripis-gest!
  [175, 6, 'z21_s175_grib'],                     // Peter h5
  [176, 2, 'z26_s176_grib'],                     // Anna h33 — ordinal-misread-'10'-križ!
  [178, 6, 'z44_s178_grib'],                     // Anna h2 — KLEPEC-nit! ordinal-DUEL 44/45!
  [179, 2, 'z51_s179_grib'],                     // Anna h56 — mati-SIMEC! boter-URH!
  [179, 3, 'z52_s179_grib'],                     // Johann h41
  [180, 0, 'z59_s180_grib'],                     // Anna h96[~] — oče-KRIŽAN! mesec-DUEL (Juni-vs-Juli!)
  [180, 2, 'z61_s180_grib'],                     // Barbara Margaritha h68 — Uršič? + mati-POŽEK!
  [180, 6, 'z65_s180_grib'],                     // Maria h69 — NEZAKONIT (oče-prazno!) mati-Brunec!
  [181, 0, 'z69_s181_grib'],                     // Anna h13 — mati-Peglitz[~PEZDIRC?] mesec-DUEL!
  [181, 1, 'z70_s181_grib'],                     // Mathias h22 — pripis-†29/10-1887!
  [181, 6, 'z75_s181_grib'],                     // Josef h43[~13?]
  [182, 1, 'z78_s182_grib'],                     // Johann h20 — oče-Pegolec? mesec-DUEL!
  [182, 7, 'z84_s182_grib'],                     // Katharina h51[~] — ordinal-DUEL 84/83!
  [183, 0, 'z94_s183_grib'],                     // Maria h57[~] — VLM-samos-prečrtana (✗)!
  [184, 0, 'z93_s184_grib'],                     // Michael h48 — LAZAR-nit!
  [184, 2, 'z95_s184_grib'],                     // Mathias h49 — oče-Brodarič + mati-Peghiric-PEZDIRC!
  [184, 6, 'z99_s184_grib'],                     // Johann h23 — vas-DUEL (Griblje-vs-Maršiči!)!
  [185, 2, 'z105_s185_grib'],                    // Johann h62 — oče-DUEL (Kure-vs-Glazar!) — P221-lead!
  [185, 7, 'z110_s185_grib'],                    // Agnes h8
  [186, 1, 'z112_s186_tail_grib'],               // Mathias h43 — PREČRTANA-tail + †28.12.1887!
];
for (const [s, idx, name] of G) { const [a, b] = row(s, idx); await crop(name, s, a, b, 0.02, 0.88, 2.8); }

console.log('P222 krop pass-1: 43 izrezov');
