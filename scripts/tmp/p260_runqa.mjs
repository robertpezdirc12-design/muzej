import { runQA } from '/home/z/my-project/src/lib/qa.ts';
const r = runQA({});
console.log('ok:', r.ok, '| passed:', r.passed, '| failed:', r.failed, '| testov:', r.tests.length);
for (const f of r.tests.filter(t => !t.pass)) console.log('FAIL:', f.id, '::', String(f.detail).slice(0, 300));
const p260 = r.tests.filter(t => /p260|p259|p254|p253/.test(t.id));
for (const t of p260) console.log(t.pass ? 'OK' : 'XX', t.id, '::', String(t.detail).slice(0, 220));
