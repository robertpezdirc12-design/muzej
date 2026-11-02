// P191 · PT-luknja-18 FINALNI REPORT (po zaključku mrliške linije 39/39).
// Vse tri knjige so popolnoma prebrane (krstna 04105: 1887–1919 · poročna
// 04455: 1886–1922 · mrliška 04894: 1886–1924), zato je korpus FINALEN in
// to je definivno stanje PT-luknje: za vsako od 18 hiš (41–60 brez h41/h50)
// izračuna vse dokaze po knjigah. Izpis: research/issue17/pt-luknja-18-final.json
//
// Zagon: bun scripts/tmp/p191-pt-luknja.ts
import { writeFileSync } from "node:fs";
import { HOUSE_VITALS } from "../../src/data/atlas/parish";

const GAP = ["42", "43", "44", "45", "46", "47", "48", "49", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60"];

const byBook = (sig: string) => HOUSE_VITALS.filter((v) => v.bookSignature === sig);

// ——— korpus ———
const vitalsTotal = HOUSE_VITALS.length;
const counts: Record<string, number> = {};
for (const v of HOUSE_VITALS) counts[v.bookSignature] = (counts[v.bookSignature] ?? 0) + 1;
const housesAll = new Set(HOUSE_VITALS.map((v) => v.houseNo));

// ——— 18 luknja-hiš ———
const gapHouses = GAP.map((hn) => {
  const blocks = HOUSE_VITALS.filter((v) => v.houseNo === hn);
  const perBook: Record<string, number> = {};
  for (const v of blocks) perBook[v.bookSignature] = (perBook[v.bookSignature] ?? 0) + 1;
  const years = blocks.map((v) => v.year).sort((a, b) => a - b);
  const via: string[] = [];
  if (perBook["04105"]) via.push("krstna-04105");
  if (perBook["04455"]) via.push("poročna-04455");
  if (perBook["04894"]) via.push("mrliška-04894");
  return {
    houseNo: hn,
    blocksTotal: blocks.length,
    byBook: { "04105": perBook["04105"] ?? 0, "04455": perBook["04455"] ?? 0, "04894": perBook["04894"] ?? 0 },
    firstYear: years[0] ?? null,
    lastYear: years[years.length - 1] ?? null,
    years,
    dokazVia: via,
  };
});

const trueHoles = gapHouses.filter((g) => g.blocksTotal === 0).map((g) => g.houseNo);
const closed = gapHouses.filter((g) => g.blocksTotal > 0);

const report = {
  phase: "P191",
  title: "PT-luknja-18 — finalni dokazi po zaključku mrliške linije 39/39 (knjiga 04894 popolnoma digitalizirana)",
  generatedAt: new Date().toISOString(),
  definition: {
    gapRange: "hiše 41–60 brez h41 (izven vzorca) in h50 (04455-dokazana)",
    gapHouses: GAP,
    note: "p80-skripta-set 18 (PT_GAP_HOUSES) ≠ qa doc-list 15 (P80_PT_GAP = 18 brez h45/h47/h55 — dokazi geometrija/filtra)",
  },
  corpus: {
    vitalsTotal,
    byBook: counts,
    housesDistinctAll: housesAll.size,
    housesNote: "raw-distinct v HOUSE_VITALS = 95; p80-vzorec = 94 · korpus = 93 (pogoji filtra v qa-parish I7)",
  },
  gapStatus: {
    total: GAP.length,
    withDokaz: closed.length,
    trueHoles,
    dokazOnlyMrliška: gapHouses.filter((g) => g.blocksTotal > 0 && g.byBook["04105"] === 0 && g.byBook["04455"] === 0).map((g) => g.houseNo),
    dokazOnlyPoročna: gapHouses.filter((g) => g.byBook["04455"] > 0 && g.byBook["04894"] === 0).map((g) => g.houseNo),
  },
  gapHouses,
};

const out = "/home/z/muzej/research/issue17/pt-luknja-18-final.json";
writeFileSync(out, JSON.stringify(report, null, 1) + "\n", "utf-8");

console.log(`korpus: vitals=${vitalsTotal} · po knjigah: ${JSON.stringify(counts)} · hiš=${housesAll.size}`);
console.log(`PT-luknja-18: z dokazom ${closed.length}/18 · prave luknje (0 blokov): ${trueHoles.length ? trueHoles.join(", ") : "NIČ!"}`);
for (const g of gapHouses) {
  console.log(
    `  h${g.houseNo}: ${String(g.blocksTotal).padStart(2)} blokov (k${g.byBook["04105"]}/p${g.byBook["04455"]}/m${g.byBook["04894"]}) · ${g.firstYear ?? "—"}–${g.lastYear ?? "—"} · ${g.dokazVia.join(" + ") || "BREZ DOKAZA!"}`,
  );
}
console.log(`zapisano: ${out}`);
