// P233 — branje ločilnih krops sheet-X1/X2/X3.png (definitivna ločitev DUELOV za 18 Griblje-vrstic!).
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p233/krops';

const CTX = `To je vertikalna zaporedja IZREZOV (povečava ×2.6) iz KRSTNE matične knjige župnije Podzemelj, leto 1873 (STAREJŠA Kurrent-pisava). Vsak izrez = DEL ENE vrstice tabele: 'LEVO' = zaporedna-št. + mesec/dan rojstva/krsta + vas + hišna-št. + ime otroka; 'DESNO' = oče (+ stan) + mati + botra/botri + duhovnik + MODRI-pripisi; 'HISNA' = samo hišna-številka-stolpec; 'ZAP' = samo zaporedna-št.-kontrola.
VAŠE: Griblje (Grible/Griblj/Griable), Krasinec, Dobravice, Gradac, Podzemelj, Certoviše/Cerkviše, Boršt, Klošter, Otok, Vranoviče, Prilozje, Zemelj, Grem, Kaplišče, Hradine, Malše...
MESeci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember (POZOR: J-zanka!-N-vs-M-vs-O-vs-S-prva-črka!).
CIFRE (Kurrent): 1=ozka-črtica-BREZ-zanke (vs-2-ima-osnovo!), 4=zanka, 5≈6, 7=γ-s-prečko, 3/5/8-zmeda. ★★★ 10/20/30 + 1x/2x + 3x/5x-zmede!
Zapiši TOČNO kaj vidiš; negotovo z [~], neberljivo z [?]. Če polje ni v izrezu, napiši null.`;

const TASKS = [
 { sheet: 'sheet-X1.png', extra: `Izrezi so iz skenov s28 (11-vrstic!-März/April!-zap-pričakovano-10–20 ali 20–30-DUEL!) in s29 (11-vrstic!-April/Mai!-zap-21–31!) in s30 (8-vrstic!-Mai/Juli!-zap-32–39!). ISKAMO: (1) TOČNE zaporedne številke Griblje-vrstic!, (2) TOČNE hišne številke (h16/24? h34/28? h37/27? h13? h31/33? h49?), (3) TOČNE mesece (März/April/Mai/Juli-DUELI!), (4) priimke (Šilar/Gilart-Hilart-DUEL!-Hrič/Flurič!-Jakhofič!-Bezdur/Legdirc!-Brodarič!-Perdisek-PEZDIRC-garble!).`,
   items: ['s28-r4-LEVO', 's28-r4-DESNO', 's28-r8-LEVO', 's28-r8-DESNO', 's28-r9-LEVO', 's28-r9-DESNO', 's29-r2-LEVO', 's29-r2-DESNO', 's29-r7-LEVO', 's29-r7-DESNO', 's30-r7-LEVO', 's30-r7-DESNO'] },
 { sheet: 'sheet-X2.png', extra: `Izrezi so iz skenov s31 (11-vrstic!-Juni/Juli!-zap-40–50!) in s32 (10-vrstic!-Juli/August!-zap-51–60!) in s33 (8-vrstic!-August!-zap-61–68!). ISKAMO: (1) hišne številke (h1? h40-DUEL-P232-continuum! h69? h74/64? h8?), (2) priimke (Štefko/Stelko!-Ležir/PEZDIRC-garble-★★★-h40-×2-DUEL-z-1874!-Glušac/Kuss!-Hambič/Kambič!-BRODARIČ-matec-×2!-Jakopic/Glaspić!-Novac/MILEK-DUEL!), (3) †12.3.1938-MODRI-pripis-s31-r11!, (4) matec-s33-r8-PRAZNO/prečrtano?`,
   items: ['s31-r7-LEVO', 's31-r7-DESNO', 's31-r11-LEVO', 's31-r11-DESNO', 's32-r4-LEVO', 's32-r4-DESNO', 's32-r5-LEVO', 's32-r5-DESNO', 's33-r5-LEVO', 's33-r5-DESNO', 's33-r8-LEVO', 's33-r8-DESNO'] },
 { sheet: 'sheet-X3.png', extra: `Izrezi so iz skenov s34 (10-vrstic!-October!-zap-69–78!), s35 (9-vrstic!-Oct/Nov!-zap-79–87-POTRJENO!) in s36 (10-vrstic!-November!-zap-88–97-P232-POTRJENO!). ISKAMO: (1) s34-r5-h53 + oče-Pegdire-PEZDIRC!, (2) s35-r2-vs-r3-DUEL (kaj-dejansko-stoji-v-r2-in-r3?!-Carolina-Sušnik-vs-Michael-Logar/Lozar-Pustkar!-h37-vs-h57!), (3) s36-r5-oče-JAKOFČIČ-vs-JAKOŠA-DUEL + zap-92, (4) s36-r6-oče-Guveč-vs-HURE + botra-Mihelč-vs-MILEK-P232-DUEL + zap-93, (5) s36-r7-h41-vs-h11-DUEL + ime-Katharina-vs-Kaspar-DUEL + oče-Grmič-vs-KUMIĆ-DUEL + matec-DRAGOŠ + zap-94, (6) s36-r1-zap-88-KONTROLA.`,
   items: ['s34-r5-LEVO', 's34-r5-HISNA', 's34-r5-DESNO', 's35-r2-LEVO', 's35-r2-DESNO', 's35-r3-LEVO', 's35-r3-HISNA', 's35-r3-DESNO', 's36-r5-LEVO', 's36-r5-DESNO', 's36-r6-LEVO', 's36-r6-DESNO', 's36-r7-LEVO', 's36-r7-DESNO', 's36-r1-ZAP'] },
];

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{'), b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON');
  return JSON.parse(t.slice(a, b + 1));
}

for (const t of TASKS) {
  const outPath = `/tmp/p233/xread-${t.sheet.replace('sheet-', '').replace('.png', '')}.json`;
  if (fs.existsSync(outPath)) { console.log(`${t.sheet}: ŽE`); continue; }
  const b64 = fs.readFileSync(`${DIR}/${t.sheet}`).toString('base64');
  const prompt = `${CTX}

${t.extra}

Izrezi (zaporedje po labelah): ${t.items.join(' | ')}.

Izhod: SAMO veljaven JSON:
{"izrezi":[{"label":"s28-r4-LEVO","zap":"...|null","mesec":"...|null","roj":"...|null","krst":"...|null","vas":"...|null","hisna":"...|null","otrok":"...|null","ocec":"...|null","matec":"...|null","botra":"...|null","duhovnik":"...|null","opomba":"...|null","opomba2":"..."}]}`;
  let done = false;
  for (let attempt = 1; attempt <= 4 && !done; attempt++) {
    try {
      const r = await Promise.race([
        inst.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 240000))
      ]);
      const c = r?.choices?.[0]?.message?.content || '';
      const j = parseContent(c);
      fs.writeFileSync(outPath, JSON.stringify(j, null, 2));
      console.log(`${t.sheet}: OK (${j.izrezi?.length} izrezov)`);
      done = true;
    } catch (e) {
      console.error(`${t.sheet}: poskus ${attempt} FAIL ${e.message.slice(0, 80)}`);
      if (/429|Too many/.test(e.message)) await new Promise(r2 => setTimeout(r2, 45000));
      else await new Promise(r2 => setTimeout(r2, 8000));
    }
  }
  if (!done) console.error(`${t.sheet}: KONČNO-FAIL`);
  await new Promise(r => setTimeout(r, 20000));
}
console.log('X-READ-KONČANO');
