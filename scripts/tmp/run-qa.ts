// Požene celoten QA test muzeja in izpiše rezultate.
import { runQA } from "../../src/lib/qa";

const report = runQA();
const failed = report.tests.filter((t: { pass: boolean }) => !t.pass);
console.log(`QA: ${report.passed}/${report.tests.length} testov prestanih`);
if (failed.length > 0) {
  console.log("\nNEUSPELI TESTI:");
  for (const f of failed) console.log(`  ✗ ${f.id}: ${f.detailSi ?? f.detail ?? ""}`);
  process.exit(1);
}
console.log("Vsi testi prestani.");
for (const t of report.tests) {
  if (/timeline|p10|p12/.test(t.id)) console.log(`  ✓ ${t.id}: ${String(t.detailSi ?? "").slice(0, 130)}`);
}
