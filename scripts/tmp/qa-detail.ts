import { runQA } from "../../src/lib/qa";
const r = runQA();
const t: Record<string, unknown> = r.tests.find((x: { id: string }) => x.id === "qa-p18-timeline-stops") as Record<string, unknown>;
console.log("ključi testa:", Object.keys(t));
for (const k of Object.keys(t)) {
  const v = t[k];
  if (typeof v === "string" && v.length > 20) console.log(`  ${k}: ${v.slice(0, 200)}`);
}
