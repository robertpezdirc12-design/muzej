// p237_measure2.ts — dodatne meritve: 1885-MILEK, h65/h69 preseki, Mathias-veriga
import { HOUSE_VITALS } from "../../src/data/atlas/parish";

const MILIČ_RE =
  /MILIČ|MILEK|MIHELČ|MIHELIČ|MIHELIK|Mihelik|Milech|Milhoeluc|MILCH|Mihelk|Mihelt|Mihek|Milih|Mihelitsch|Mihelj|Mihelčič|Mihelovic|Milek\[|Mileh\[|Mek\/Milek|Milek-variant|MILEK-grafija/i;

console.log("=== 1885 (04104) vse 'Mile'-sublice ===");
for (const h of HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1885)) {
  const m = /Mile|Milih|Milih|Mihel|Mulk|Mulk|Milc/i.exec(h.whatSi);
  if (m) console.log(`h${h.houseNo} · s${h.scan} → …${h.whatSi.slice(Math.max(0, m.index - 60), m.index + 60).replace(/\s+/g, " ")}…`);
}

console.log("\n=== h65 bloki: Milek-družina vs ostali (po knjigah) ===");
for (const k of ["04104", "04105", "04106", "04894", "04455"]) {
  const vsi = HOUSE_VITALS.filter((h) => h.houseNo === "65" && h.bookSignature === k);
  const milek = vsi.filter((h) => MILIČ_RE.test(h.whatSi));
  console.log(`${k}: h65=${vsi.length} · Milek-nit=${milek.length} · ostali=${vsi.length - milek.length}`);
  for (const h of vsi.filter((h) => !MILIČ_RE.test(h.whatSi)))
    console.log(`   OSTALI: ${k} · ${h.year} → ${h.whatSi.slice(0, 90).replace(/\s+/g, " ")}…`);
}

console.log("\n=== Mathias/Matija + h65 veriga (vse knjige) ===");
for (const h of HOUSE_VITALS.filter((h) => h.houseNo === "65" && /Mathias|Matija|Matihe/i.test(h.whatSi)))
  console.log(`${h.bookSignature} · ${h.year} → ${h.whatSi.slice(0, 100).replace(/\s+/g, " ")}…`);

console.log("\n=== h69 bloki: priimki + Milek-botra presek ===");
for (const h of HOUSE_VITALS.filter((h) => h.houseNo === "69" && MILIČ_RE.test(h.whatSi)))
  console.log(`PRESEK: ${h.bookSignature} · ${h.year} → ${h.whatSi.slice(0, 110).replace(/\s+/g, " ")}…`);

console.log("\n=== MILIČ-family per year v 04105 (kronologija) ===");
const byYear = new Map<number, number>();
for (const h of HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && MILIČ_RE.test(h.whatSi)))
  byYear.set(h.year, (byYear.get(h.year) ?? 0) + 1);
console.log([...byYear.entries()].sort((a, b) => a[0] - b[0]).map(([y, c]) => `${y}:${c}`).join(" · "));
