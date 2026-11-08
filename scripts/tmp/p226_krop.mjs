// P226 krop pass-1 — KROP-dokazi (krstna 04104, leto 1880 = 6/15!):
// ZAP-STOLPCI: s129–s135 (+s119–s128 ko znani row-števci!) — ordinalna-linija z1–z122!
// FOLIACIJA: s129–s135 (gola-svinčna-'sken−6' — s129='123'-pričakovana! s132='126'-VLM! s135='129'-P225!)
// MEJA: arb_s129_meja (glava-'Jahr 1880' + zap-71–78-nadaljevanje!) + arb_sX_meja (restart-z1!)
// MESEC-STOLPCI: s131 (Sep-blok!) + s132 (Dez-blok!) + s135 (Dez-tail-z116–z122 + Finis!)
// GRIBLJE-VRSTICE: znane-iz-page-VLM (dopolnjeno-po-branju!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p226';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// geometrije: razprti-listi; ytop 0.165; B = (0.975−0.165)/n-vrstic (page-VLM-števec!)
const N = { 129: 8, 130: 7, 131: 8, 132: 8, 133: 7, 134: 8, 135: 7 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }

const args = process.argv.slice(2);
const ONLY = args.length ? args : null;

async function maybe(name, fn) { if (ONLY && !ONLY.includes(name)) return; await fn(); }

// --- ZAP-stolpci (ordinalna-linija!) ---
for (const p of [129, 130, 131, 132, 133, 134, 135]) await maybe(`s${p}_zap_stolpec`, () => crop(`s${p}_zap_stolpec`, p, 0.05, 0.99, 0.02, 0.115, 5.0));

// --- FOLIACIJA (gola-svinčna-'sken−6'!) ---
for (const p of [129, 130, 131, 132, 133, 134, 135]) await maybe(`arb_s${p}_pag`, () => crop(`arb_s${p}_pag`, p, 0.02, 0.17, 0.02, 0.42, 3.2));

// --- MEJA (glava-'Jahr 1880' na s129! + Finis na s135!) ---
await maybe('arb_s129_meja', () => crop('arb_s129_meja', 129, 0.02, 0.60, 0.02, 0.62, 2.8));
await maybe('arb_s135_finis', () => crop('arb_s135_finis', 135, 0.04, 0.99, 0.02, 0.62, 2.6));

// --- MESEC-STOLPCI (chronologija!) ---
await maybe('s131_mesec_stolpec', () => crop('s131_mesec_stolpec', 131, 0.10, 0.99, 0.09, 0.42, 4.0));
await maybe('s132_mesec_stolpec', () => crop('s132_mesec_stolpec', 132, 0.10, 0.99, 0.09, 0.42, 4.0));
await maybe('s135_mesec_stolpec', () => crop('s135_mesec_stolpec', 135, 0.10, 0.99, 0.09, 0.42, 4.0));
await maybe('s133_mesec_stolpec', () => crop('s133_mesec_stolpec', 133, 0.10, 0.99, 0.09, 0.42, 4.0));

// --- GRIBLJE full-rows (page-VLM-vrsta-indeksi, 1-based → idx0 = vrsta−1) ---
const G = [
  [129, 1, 'z72_s129_grib'],   // Anna h24 — oče-Jakob-Hribar! (July-20)
  [131, 2, 'z88_s131_grib'],   // Nicolaus h10 (Sep-13)
  [131, 3, 'z89_s131_grib'],   // Anna h43 (Sep-24)
  [132, 1, 'z95_s132_grib'],   // Johann h18 (Dec-15/16)
  [132, 5, 'z99_s132_grib'],   // Katharina h33 (Dec-23/24) — PEZDIRC-botra/boter!
  [132, 7, 'z101_s132_grib'],  // Katharina h29 (Dec-27)
  [133, 2, 'z104_s133_grib'],  // Maria h44 (Nov-4/5-DUEL-mesec?!) — hiša-'44'-VLM!
];
for (const [s, idx, name] of G) { const [a, b] = row(s, idx); await maybe(name, () => crop(name, s, a, b, 0.02, 0.88, 2.8)); }

console.log('P226 krop pass-1 DONE');
