// P223 krop pass-1 — KROP-dokazi (krstna 04104, leto 1883 = 3/15!):
// ZAP-STOLPCI (15): s159–s173 (ordinalna-linija-1882-tail-z88–z106 + 1883-z1–z99 + restart-1884!)
// FOLIACIJA (4): s161/s165/s169/s173 (pag = sken+13-re-potrditev!)
// MEJA (1): arb_s161_meja (tail-1882-z104–z106 + VSOTNA-'1/8/8/3' + restart-z1!)
// GRIBLJE-VRSTICE (20): vse-Griblje-1883!
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p223';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// geometrije: razprti-listi; ytop 0.165; B = (0.975−0.165)/n-vrstic (page-VLM-števec!)
const N = { 159: 8, 160: 8, 161: 10, 162: 9, 163: 8, 164: 8, 165: 9, 166: 9, 167: 9, 168: 8, 169: 8, 170: 8, 171: 8, 172: 8, 173: 8 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }

// --- ZAP-stolpci (ordinalna-linija!) ---
for (const p of Object.keys(N)) await crop(`s${p}_zap_stolpec`, +p, 0.05, 0.99, 0.02, 0.115, 5.0);

// --- FOLIACIJA + glave (pag = sken+13!) ---
for (const p of [161, 165, 169, 173]) await crop(`arb_s${p}_pag`, p, 0.02, 0.17, 0.02, 0.42, 3.2);

// --- MEJA ---
await crop('arb_s161_meja', 161, 0.04, 0.60, 0.02, 0.62, 2.8);  // tail-1882-z104–z106 + VSOTNA-'1/8/8/3' + restart-z1

// --- GRIBLJE full-rows (page-VLM-vrsta-indeksi, 1-based → idx0 = vrsta−1) ---
const G = [
  [161, 8, 'z05_s161_grib'],                     // Katharina h28 — pripis-MMK!
  [162, 0, 'z07_s162_grib'],                     // Barbara h20 — oče-Perdič-PEZDIRC-grafija!
  [163, 1, 'z17_s163_grib'],                     // Josef h7 — mati-STRUCELJ!
  [163, 6, 'z22_s163_grib'],                     // Anna h39 — pripis-MMK-1940!
  [164, 1, 'z25_s164_grib'],                     // Margaretha h8
  [164, 4, 'z28_s164_grib'],                     // Peter h35[~]
  [165, 0, 'z32_s165_grib'],                     // Maria h25 — pripis-poroka-1957!
  [166, 2, 'z43_s166_grib'],                     // Georg h17[~7?] — botra-Simec/Kure!
  [167, 2, 'z52_s167_grib'],                     // Anton h55 — oče-Peršinc-PEZDIRC!
  [167, 8, 'z58_s167_grib'],                     // Barbara h19 — pripis-MMK-1959!
  [168, 0, 'z59_s168_grib'],                     // Mathias h24 — pripis-garble!
  [168, 2, 'z61_s168_grib'],                     // Maria h90[~70?] — hiša-DUEL!
  [169, 6, 'z73_s169_grib'],                     // Barbara h1 — oče-Lesko!
  [170, 1, 'z76_s170_grib'],                     // Rikhardsina[?] h51[?] — ime-garble!
  [170, 3, 'z78_s170_grib'],                     // Matthäus h37[?] — hiša-DUEL-z1-paralela!
  [171, 5, 'z88_s171_grib'],                     // Katharina h25[~] — P222-lead!
  [172, 3, 'z94_s172_grib'],                     // Nicolaus h11 — mati-DRAGOŠ! pripis-1910!
  [172, 5, 'z96_s172_grib'],                     // Anna h18[~vs-63!] — mati-Peddire-PEZDIRC! hiša-DUEL!
  [172, 6, 'z97_s172_grib'],                     // Barbara h29 — mati-KRIŽAN!
  [173, 0, 'z99_s173_tail_grib'],                // Peter — vas-X-open-'OBržuh/Obrije[?]'! TAIL-1883!
];
for (const [s, idx, name] of G) { const [a, b] = row(s, idx); await crop(name, s, a, b, 0.02, 0.88, 2.8); }

console.log('P223 krop pass-1: ' + (15 + 4 + 1 + 20) + ' izrezov');
