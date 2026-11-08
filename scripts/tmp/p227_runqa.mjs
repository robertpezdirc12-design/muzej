import { runQA } from '/home/z/my-project/src/lib/qa.ts';
const r = runQA({});
console.log('ok:', r.ok, '| passed:', r.passed, '| failed:', r.failed, '| testov:', r.tests.length);
for (const f of r.tests.filter(t => !t.pass)) console.log('FAIL:', f.id, '::', String(f.detail).slice(0, 300));
const p227 = r.tests.filter(t => /p227/.test(t.id));
for (const t of p227) console.log(t.pass ? '✓' : '✗', t.id, '::', String(t.detail).slice(0, 220));
