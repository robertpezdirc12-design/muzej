import { runQA } from "@/lib/qa";
const r = await runQA();
console.log(`QA: ${r.passed}/${r.tests.length} ${r.ok ? "VSE OK" : "NAPAKE!"}`);
for (const t of r.tests.filter((x) => !x.pass)) console.log("  FAIL:", t.id, "—", t.error ?? "");
const p10 = r.tests.find((t) => t.id.includes("p10"));
if (p10) console.log(`\nP10 test: ${p10.pass ? "✓ PASS" : "✗ FAIL"}\n  ${p10.detailSi?.slice(0, 300)}`);
