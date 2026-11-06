import { runQA } from '/home/z/my-project/muzej-backup/src/lib/qa.ts';
const r = runQA({});
console.log('ok:', r.ok, '| passed:', r.passed, '| failed:', r.failed, '| testov:', r.tests.length);
for (const f of r.tests.filter(t => !t.pass)) console.log('FAIL:', f.id, '::', String(f.detail).slice(0, 200));
const p203 = r.tests.filter(t => /p203/.test(t.id));
for (const t of p203) console.log(t.pass ? '✓' : '✗', t.id);
