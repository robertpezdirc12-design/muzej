// P234 — branje VERIGA-26-27 sheeta (21-kropov: vsaka-vrstica s26+s27, zap+mesec+dan!).
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p234/krops';

const CTX = `To je 30-IZREZOV (povečava ×3.2) iz KRSTNE matične knjige župnije Podzemelj (Kurrent-1872/1873!). Vsak izrez = LEVI-DEL ENE-vrstice: ZAPoredna-številka (skrajno-levo, ročno!) + mesec + dan-rojstva + dan-krsta (+ začetek-vasi).
IZREZI: s19-r1, s19-r5, s19-r9, s19-r10 (stran-s19, 10-bandov!-Juni/July!-z51–z59/60!); nato s24-r1 ... s24-r11 (stran-s24, 11-bandov!-November/Dezember!-z100–z109!-R7-JE-PREČRTANA-kopija!); nato s25-r1 ... s25-r6 (stran-s25, 6-bandov!-TAIL-leta-1872!-Dezember!-z110–z115/116!-ZADNJA-lahko-PRAZNA!).
★★★ KLJUČNA-VPRAŠANJA: (1) s19-r1-ZAP = '51' (ali-'52'?-'1'?!); (2) s24-r7 = PREČRTANA (brez-zapa?!); (3) s24-zap-verige-z100–z109; (4) s25-zap-verige-z110–z115-ALI-z110–z116?!; (5) s25-r6 = PRAZNA?!; (6) MESECI-s19 (Juni?-July?).
★★★ CIFRE-KURRENT: '1' = ozka-črtica-s-serifom (BREZ-zanke!), '2' = osnova+zgornja-zanka, '3' = zrcalna-E, '4' = zanka, '5' = črta+zanka, '6' = zanka-gor+rep, '7' = γ-s-prečko, '8' = dve-zanki, '9' = zanka+rep, '0' = oval. DVOJKE: '1'-'2'-zmeda (serif!); '117'-trimestno-mogoče!
MESeci: Jänner(J-zanka!), Feber, März, April, Mai, Juni(J!), July(J!), August, September, October, November(N!), Dezember(D!). POZOR: Dezember-vs-Jänner (D-vs-J!).
ZA VSAK izrez preberi: zap (najboljši-guess!-negotovo-[~]!), mesec, dan-rojstva, dan-krsta, vas (če-vidna).
Izhod: SAMO JSON: {"izrezi":[{"label":"s26-r1","zap":"...","zapZan":"visoko|srednje|nizko","mesec":"...","roj":"...","krst":"...","vas":"..."}, ...]}`;

let done = false;
for (let attempt = 1; attempt <= 4 && !done; attempt++) {
  try {
    const b64 = fs.readFileSync(`${DIR}/TAIL-VERIGA.png`).toString('base64');
    const r = await Promise.race([
      inst.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: CTX },
          { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      }),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 240000))
    ]);
    const c = r?.choices?.[0]?.message?.content || '';
    const a = c.indexOf('{'), b = c.lastIndexOf('}');
    if (a < 0 || b < 0) throw new Error('ni JSON');
    const j = JSON.parse(c.slice(a, b + 1));
    fs.writeFileSync('/tmp/p234/xread-TAIL.json', JSON.stringify(j, null, 2));
    for (const i of j.izrezi || []) console.log(`${i.label}: zap=${i.zap} (${i.zapZan}) ${i.mesec} r=${i.roj} k=${i.krst} vas=${i.vas}`);
    done = true;
  } catch (e) {
    console.error(`poskus ${attempt} FAIL ${e.message.slice(0, 100)}`);
    if (/429|Too many/.test(e.message)) await new Promise(r2 => setTimeout(r2, 45000));
    else await new Promise(r2 => setTimeout(r2, 8000));
  }
}
if (!done) console.error('KONČNO-FAIL');
console.log('VERIGA-READ-KONČANO');
