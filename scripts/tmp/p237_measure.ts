// p237_measure.ts — meritve za P237 FORENZIKA NITI (MILIČ↔MILEK, duhovniki, h69)
import { HOUSE_VITALS } from "../../src/data/atlas/parish";

const MILIČ_RE =
  /MILIČ|MILEK|MIHELČ|MIHELIČ|MIHELIK|Mihelik|Milech|Milhoeluc|MILCH|Mihelk|Mihelt|Mihek|Milih|Mihelitsch|Mihelj|Mihelčič|Mihelovic|Milek\[|Mileh\[|Mek\/Milek|Milek-variant|MILEK-grafija/i;

const KNJIGE = ["04104", "04105", "04106", "04894", "04455"] as const;

function snippet(s: string, m: RegExpExecArray): string {
  const a = Math.max(0, m.index - 45);
  return s.slice(a, m.index + 55).replace(/\s+/g, " ").trim();
}

console.log("=== 1) MILIČ/MILEK/MIHELČ — bloki po knjigi ===");
for (const k of KNJIGE) {
  const bloki = HOUSE_VITALS.filter((h) => h.bookSignature === k);
  const zadeti = bloki.filter((h) => MILIČ_RE.test(h.whatSi));
  console.log(`${k}: ${zadeti.length}/${bloki.length} blokov`);
  for (const h of zadeti) {
    const m = MILIČ_RE.exec(h.whatSi)!;
    console.log(`   ${k} · ${h.year} · h${h.houseNo} · s${h.scan ?? "?"} → …${snippet(h.whatSi, m)}…`);
  }
}

console.log("\n=== 2) MILIČ-nit v 04104 po letih (različni bloki) ===");
for (let y = 1871; y <= 1885; y++) {
  const zadeti = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === y && MILIČ_RE.test(h.whatSi));
  if (zadeti.length) console.log(`${y}: ${zadeti.length} → h[${zadeti.map((h) => h.houseNo).join(",")}]`);
}

console.log("\n=== 3) h69 — vse knjige ===");
const h69 = HOUSE_VITALS.filter((h) => h.houseNo === "69");
for (const h of h69) {
  console.log(`${h.bookSignature} · ${h.year} · s${h.scan ?? "?"} · p${h.page ?? "?"} → ${h.whatSi.slice(0, 160).replace(/\s+/g, " ")}…`);
}

console.log("\n=== 4) WEISEL/WENZEL/WESSELY — po knjigi ===");
const D_RE = /Weisel|Wenzel|Wessely/i;
for (const k of KNJIGE) {
  const zadeti = HOUSE_VITALS.filter((h) => h.bookSignature === k && D_RE.test(h.whatSi));
  console.log(`${k}: ${zadeti.length}`);
  for (const h of zadeti) {
    const m = D_RE.exec(h.whatSi)!;
    console.log(`   ${k} · ${h.year} · h${h.houseNo} → …${snippet(h.whatSi, m)}…`);
  }
}

console.log("\n=== 5) h65 (MILIČ→MILEK→PEZDIRC nit) — vse knjige ===");
for (const h of HOUSE_VITALS.filter((h) => h.houseNo === "65")) {
  console.log(`${h.bookSignature} · ${h.year} → ${h.whatSi.slice(0, 110).replace(/\s+/g, " ")}…`);
}

console.log(`\nTOTAL HOUSE_VITALS = ${HOUSE_VITALS.length}`);
console.log("po knjigah:", KNJIGE.map((k) => `${k}=${HOUSE_VITALS.filter((h) => h.bookSignature === k).length}`).join(" · "));
