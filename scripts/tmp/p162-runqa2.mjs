import { runQA } from '/home/z/muzej/src/lib/qa.ts';
const r = runQA({});
console.log('top keys:', Object.keys(r));
const arr = r.tests || r.checks || [];
if (arr.length) console.log('sample item:', JSON.stringify(arr[0]).slice(0, 300));
