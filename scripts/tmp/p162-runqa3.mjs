import { runQA } from '/home/z/muzej/src/lib/qa.ts';
const r = runQA({});
console.log('ok:', r.ok, '| passed:', r.passed, '| failed:', r.failed, '| testov:', r.tests.length);
for (const f of r.tests.filter(t => !t.pass)) console.log('FAIL:', f.id, '::', String(f.detail).slice(0, 200));
const p162 = r.tests.filter(t => /p162|p163/.test(t.id));
for (const t of p162) console.log(t.pass ? '✓' : '✗', t.id, '::', String(t.detail).slice(0, 140));
