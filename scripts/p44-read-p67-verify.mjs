// P44 — 2c krog: p67 VERIFIKACIJA s PV kontekstom — preveri posamične celice proti
// znanim kontrolam (PV izpis rabe tal: Acker 413, Wiesen 88, Weiden 636 joch...).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

const PAGES_DIR = '/tmp/p44-pz-pages';
const RAW_DIR = 'research/issue11/pz-raw';

const PROMPT = `To je rekapitulacijska tabela "Specifischer Ausweis der Endresultate" za občino Grüble (Kurrent, 1825). Ista stran je bila že 4-krat prebrana; branja se pri NEKATERIH celicah RAZHAJAJO. Tvoja naloga je VERIFIKACIJA posamičnih celic — preberi ZDOBAVNO samo te:

1. Acker razred I: površina (Joch + Klafter)? — prej: 80 j 842 kl (3× stabilno)
2. Acker razred II: površina? — prej: 234 j 120 kl, ALE izkaz rabe tal (PV, 10. 1. 1825) pravi Acker SKUPAJ 413 j 870 kl. Preveri: ali je II = 234 ali 334? Ali obstaja razred III (ali IV) — kakšna je njegova površina?
3. Wiesen I: 15 j 1594 kl (stabilno) — potrdi.
4. Wiesen II: 29 ali 39 j 818 kl? PV pravi Wiesen SKUPAJ (I+II+morebitni III) = 88 j 1808 kl. Obstaja Wiesen III?
5. Kleine Gärten: 3 j 612 ali 619 kl? PV: vrtovi skupaj ~2 j 123 kl.
6. Gröšere Gärten: koliko JOCH (prej: 0/neberljivo) in koliko klafter (105 ali 405)?
7. Weingärten: 7 j 42 kl — potrdi (PV pravi 7 j 665 kl).
8. Hutweiden: 113 ali 118 j, 702 kl?
9. Weiden mit Holznutzung: 558 j — koliko KLAFTER (prej: 558/858/46)? Veljavna kontrola s str. 65: Weiden SKUPAJ = 636 j 263 kl.
10. Bauarea: 1 j — koliko klafter (1199/799)?
11. Summa vrstica: 1152 j 495 kl; Brutto 8872 fl 5¾ kr; Rein 4492 fl 51 kr — potrdi vse tri.
12. ALI na strani obstaja še KAKA vrstica, ki je nisem naštel (med Wiesen II in Kleine Gärten, ali med Weingärten in Hutweiden)?

IZHOD: SAMO veljaven JSON brez markdown:
{"verifications":[{"no":1,"finding":"npr. 'Acker I: 80 j 842 kl — POTRJENO'","confidence":"clear|~|?"}],"extraRowsFound":"opis morebitnih dodatnih vrstic ali 'nobenih'","summaCheck":"potrditev/ popravek vsote","pageNote":"1 stavek"}
V nizih NE uporabljaj narekovajev ", uporabljaj ' ali »«.`;

function extractJson(text) {
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) return null;
  try { return JSON.parse(m[0]); } catch {}
  try { return JSON.parse(m[0].replace(/,(\s*[}\]])/g, '$1')); } catch {}
  return null;
}

async function main() {
  const out = `${RAW_DIR}/pz-67-verify.json`;
  if (fs.existsSync(out)) { console.log('že obstaja'); return; }
  const zai = await ZAI.create();
  const b64 = fs.readFileSync(path.join(PAGES_DIR, 'pz-67.jpg')).toString('base64');
  for (let a = 1; a <= 4; a++) {
    try {
      const c = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: PROMPT },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      const parsed = extractJson(c.choices[0]?.message?.content ?? '');
      fs.writeFileSync(out, JSON.stringify({
        page: 67, phase: 'p44-pass2c-verify',
        readAt: new Date().toISOString(), parseOk: parsed !== null,
        structured: parsed, raw: parsed ? undefined : (c.choices[0]?.message?.content ?? '').slice(0, 8000)
      }, null, 1));
      console.log(parsed ? 'JSON OK' : 'samo raw');
      return;
    } catch (e) {
      const wait = /429|rate/i.test(String(e.message)) ? 60 * a : 15;
      console.log(`poskus ${a} padel, čakam ${wait}s`);
      await new Promise(r => setTimeout(r, wait * 1000));
    }
  }
}
main().catch(e => { console.error('FATAL', e); process.exit(1); });
