import { runQA } from '/home/z/my-project/src/lib/qa.ts';
const r = runQA({});
console.log('ok:', r.ok, '| passed:', r.passed, '| failed:', r.failed, '| testov:', r.tests.length);
for (const f of r.tests.filter(t => !t.pass)) console.log('FAIL:', f.id, '::', String(f.detail).slice(0, 300));
const p197 = r.tests.filter(t => /p197/.test(t.id));
for (const t of p197) console.log(t.pass ? '✓' : '✗', t.id, '::', String(t.detail).slice(0, 200));
