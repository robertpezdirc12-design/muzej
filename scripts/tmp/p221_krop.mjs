// P221 krop pass-1 — KROP-dokazi (krstna 04104, leto 1885 = 1/15 NOVA-LINIJA!):
// ZAP-STOLPCI (15): s185–s199 (ordinalna-linija-1–104-dokaz + s189-28-dup + s190-29-duel + s197/s198-vrzel-93–96 + s199-prečrtani-102/103!)
// FOLIACIJA (6): s185/s188/s190/s193/s195/s196 (pag = sken+13-hipoteza! + s190-'1886'-glava-DUEL + NASLOVNA-sredi-letnika!)
// MEJA (1): arb_s186_meja (tail-1884 + VSOTNA + restart-z1!)
// TAIL (1): arb_s199_tail (prečrtani-102/103→103/104 + GRIBLJE-h8-Anton + brez-vsotne!)
// GRIBLJE-VRSTICE (24): vse-Griblje-1885!
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p221';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// geometrije: razprti-listi; ytop 0.165; B = (0.975−0.165)/n-vrstic (page-VLM-števec!)
const N = { 185: 8, 186: 7, 187: 8, 188: 8, 189: 8, 190: 9, 191: 9, 192: 8, 193: 8, 194: 8, 195: 7, 196: 8, 197: 7, 198: 8, 199: 2 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }

// --- ZAP-stolpci (ordinalna-linija!) ---
for (const p of Object.keys(N)) await crop(`s${p}_zap_stolpec`, +p, 0.05, 0.99, 0.02, 0.115, 5.0);

// --- FOLIACIJA + glave (pag = sken+13 + '1886'-duel + NASLOVNA!) ---
for (const p of [185, 188, 190, 193, 195, 196]) await crop(`arb_s${p}_pag`, p, 0.02, 0.17, 0.02, 0.42, 3.2);

// --- MEJA + TAIL ---
await crop('arb_s186_meja', 186, 0.04, 0.52, 0.02, 0.62, 2.8);  // tail-1884 + VSOTNA + restart-z1
await crop('arb_s199_tail', 199, 0.04, 0.62, 0.02, 0.62, 2.8);  // prečrtani-102/103→103/104 + GRIBLJE-h8!

// --- GRIBLJE full-rows (page-VLM-vrsta-indeksi, 1-based → idx0 = vrsta−1) ---
const G = [
  [186, 2, 'z01_s186_grib'],                     // restart-z1 Mathias h21 (Jan 1/1)
  [187, 0, 'z05_s187_grib'],                     // Martin (Jan 29) — oče-Popić + †1888-pripis!
  [187, 1, 'z06_s187_grib'],                     // Anna h31[~]
  [188, 1, 'z14_s188_grib'],                     // Marija h6[duel-61-trak!] — oče-Požek!
  [188, 2, 'z15_s188_grib'],                     // Mathias h11[duel-41-trak!] — oče-Plavc!
  [188, 7, 'z20_s188_grib'],                     // Johan h63
  [189, 5, 'z26_s189_grib'],                     // Maria h49[duel-17-trak!]-ordinal-26/27-DUEL!
  [189, 7, 'z28_s189_grib'],                     // Margaretha h28 — ordinal-28/29-DUEL!
  [190, 1, 'z30_s190_grib'],                     // Georg h45[duel-42-trak!] — oče-Pegivec!
  [190, 4, 'z33_s190_grib'],                     // Mathias h1[~] — oče-ŽELKO!
  [190, 8, 'z37_s190_grib'],                     // Johann h53[duel-55!] — oče-Simec!
  [192, 0, 'z47_s192_grib'],                     // Katharina h33[duel-53-trak!] — oče-Pegdic!
  [192, 1, 'z48_s192_grib'],                     // Mathias h33[duel-35-trak!] — h33-×2-hipoteza!
  [193, 1, 'z56_s193_grib'],                     // Mathias h16
  [193, 2, 'z57_s193_grib'],                     // Michael h24 — ordinal-57/58-DUEL!
  [193, 4, 'z59_s193_grib'],                     // Maria h27[duel-47-trak!] — oče-Hrizon!
  [193, 7, 'z62_s193_grib'],                     // Georg h19[duel-17-trak!] — oče-Hval!
  [194, 0, 'z63_s194_grib'],                     // Janez h58 — oče-Piček-mati-DRAGOŠ!
  [194, 1, 'z64_s194_grib'],                     // Janez h9 (samo-page-VLM!)
  [194, 5, 'z68_s194_grib'],                     // Mathias h55 — oče-Simic!
  [196, 0, 'z78_s196_grib'],                     // Katharina h17[duel-29-trak!] — oče-Pogelb?
  [196, 4, 'z82_s196_grib'],                     // Katharina h2 — oče-Hlebec!
  [196, 7, 'z85_s196_grib'],                     // Mathias h39[ep91?-duel-23-trak!] — ordinal-85/88-DUEL! — mati-PEZDIRC!
  [199, 1, 'z104_s199_tail_grib'],               // Anton h8 — TAIL-1885! — botra-KRIŽAN!
];
for (const [s, idx, name] of G) { const [a, b] = row(s, idx); await crop(name, s, a, b, 0.02, 0.88, 2.8); }

// --- 1884-TAIL kontekst (2 Griblje-1884!) ---
{ const [a, b] = row(185, 2); await crop('z1884_t5_s185_tail', 185, a, b, 0.02, 0.88, 2.8); }   // Johann h62 (Dec 8)
{ const [a, b] = row(186, 1); await crop('z1884_t13_s186_tail', 186, a, b, 0.02, 0.88, 2.8); }  // Mathias h43 (Dec 30, †28.12.1887!)
console.log('P221 krop pass-1: 48 izrezov');
