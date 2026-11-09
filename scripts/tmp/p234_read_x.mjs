// P234 — branje ločilnih X-sheetov (17-GRIBLJE-vrstic-1872 — definitivne-ločitve!).
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p234/krops';

const CTX = `To je vertikalna zaporedja IZREZOV (povečava ×2.6) iz KRSTNE matične knjige župnije Podzemelj, leto 1872 (STAREJŠA Kurrent-pisava z nemškim gotskim vplivom). Vsak izrez = DEL ENE vrstice tabele: 'LEVO' = zaporedna-št. + mesec/dan rojstva/krsta + vas + hišna-št. + ime otroka; 'DESNO' = oče (+ stan) + mati + botra/botri + duhovnik + MODRI-pripisi; 'ZAP-super' = samo zaporedna-št.-kontrola.
VAŠE: Griblje (Grible/Griblj/Griable/Grihle), Krasinec, Dobravice, Gradac, Podzemelj, Cerovišče/Cerkviše, Boršt, Klošter, Otok, Vranoviče, Prilozje, Zemelj, Grem, Kapljišče, Hradine, Malše, Dragoše, Geriče...
MESeci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember (POZOR: J-zanka-pri-Jänner/Juni/July!-N-vs-M-vs-O-vs-S-prva-črka!).
CIFRE (Kurrent): 1=ozka-črtica-BREZ-zanke (vs-2-ima-osnovo!), 4=zanka, 5≈6, 7=γ-s-prečko, 3/5/8-zmeda. 10/20/30 + 1x/2x-zmede!
Zapiši TOČNO kaj vidiš; negotovo z [~], neberljivo z [?]. Če polje ni v izrezu, napiši null.`;

const TASKS = [
 { sheet: 'X-P234-1.png', extra: `Izrezi-so-iz-s14 (11-vrstic!-Jänner!-z1–z11!-RESTART-z1-NA-r1!) in-s15 (10!-Februar!-z12–z21!) in-s16 (9!-z22–z30!-meseci-garbage-mogoči!) in-s17 (10!-März–Mai!-z31–z40!) in-s18 (10!-Mai/Juni!-z41–z50!). ISKAMO: (1) s14-r1-ZAP = '1'-RESTART-KONTROLA!, (2) hišne-številke (h11? h30? h3? h44? h9? h38? h24?), (3) priimke (Zumič?!-DRAGOŠ-matec!-Petek/Dire-Gündler?!-HRIŽAN!-ŠIMEC-boter!-KRAUP+HLOBUČAR!-Luket+DRAGOŠ-boter!-ŠIMEC-oče+Anna-DRAGOŠ-botra+MODRI-pripis-'poročena-18.2.1919-†16.3.!'-Princ+Ivanc+Ložek!), (4) TOČNE-mesece (s16-r6 = April?!-ne-November!), (5) s18-r10-ZAP = '50'-KONTROLA-verige!`,
   items: 's14-r1-LEVO | s14-r1-DESNO | s14-r1-ZAP-super | s15-r3-LEVO | s15-r3-DESNO | s16-r6-LEVO | s16-r6-DESNO | s17-r4-LEVO | s17-r4-DESNO | s17-r6-LEVO | s17-r6-DESNO | s17-r8-LEVO | s17-r8-DESNO | s18-r7-LEVO | s18-r7-DESNO | s18-r10-ZAP-kontrola' },
 { sheet: 'X-P234-2.png', extra: `Izrezi-so-iz-s19 (9!-Juni/July!-z51–z59!) in-s20 (9!-Juli/Aug!-z60–z68!) in-s21 (11!-Aug!-z69–z79!) in-s23 (10!-Okt/Nov!-z90–z99!) in-s24 (11!-Nov/Dez!-z100–z109-r7-PREČRTANA!) in-s25 (6!-Dez-TAIL!-z110–z115!). ISKAMO: (1) priimke (s19-r9-oče-'Pegdic'-PEZDIRC-GARBLE-★★★ + KLOBUČAR/KRIŽAN-botra!; s20-r2-oče-'Doblič'-DEBLIČ-GARBLE + BRODARIČ-boter!; s20-r4-matec-'Anna-PEZDIRC' + boter-'Michael-PEZDIRC'-★★★-DVOJNI!; s21-r6-oče-'LEZDIRC'-PEZDIRC-GARBLE-★★★-h40-CONTINUUM-P232/P233!-matec-'Jahofčič'-JAKOFČIČ!-botra-SIMEC+KLOBUČAR!; s23-r10-botra-'Anna-PEGHIRC'-PEZDIRC-GARBLE-★★★!; s24-r4-matec-'Katharina-JAKOFČIČ'!-boter-'Peter-Hlobuar'-HLOBUČAR!; s25-r5-TAIL-1872!-oče-Mihelič-matec-'Anna-Kribžan'-HRIŽAN!), (2) s24-r7-PREČRTANA-KONTROLA (je-celotna-vrstica-prečrtana-z-velikim-X?!-ali-je-normalna?!), (3) s25-r5-ZAP-'115'-ali-'116'-ali-drugo?-TAIL-ŠTEVILKA!, (4) s25-r6-ZAP-TAIL-KONTROLA (kaj-je-v-zadnji-vrstici?!-prazna?!-številka?!), (5) mesece-s19-r9 (Juni-11?-July-11?-Jänner-?!), (6) MODRI-pripisi (s17-r8-'poročena-18.2.1919'!-drugi?!).`,
   items: 's19-r9-LEVO | s19-r9-DESNO | s20-r2-LEVO | s20-r2-DESNO | s20-r4-LEVO | s20-r4-DESNO | s21-r6-LEVO | s21-r6-DESNO | s23-r3-LEVO | s23-r3-DESNO | s23-r8-LEVO | s23-r8-DESNO | s23-r10-LEVO | s23-r10-DESNO | s24-r4-LEVO | s24-r4-DESNO | s24-r7-PREČRTANA | s25-r2-LEVO | s25-r2-DESNO | s25-r5-LEVO | s25-r5-DESNO | s25-r6-ZAP-TAIL' },
];

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{'), b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON');
  return JSON.parse(t.slice(a, b + 1));
}

for (const t of TASKS) {
  const outPath = `/tmp/p234/xread-${t.sheet.replace('.png', '')}.json`;
  if (fs.existsSync(outPath)) { console.log(`${t.sheet}: ŽE`); continue; }
  const b64 = fs.readFileSync(`${DIR}/${t.sheet}`).toString('base64');
  const prompt = `${CTX}

${t.extra}

Izrezi (zaporedje po labelah): ${t.items}.

Izhod: SAMO veljaven JSON:
{"izrezi":[{"label":"s14-r1-LEVO","zap":"...|null","mesec":"...|null","roj":"...|null","krst":"...|null","vas":"...|null","hisna":"...|null","otrok":"...|null","ocec":"...|null","matec":"...|null","botra":"...|null","duhovnik":"...|null","opomba":"...|null"}]}`;
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
      for (const i of j.izrezi || []) {
        const k = [i.zap ? `zap=${i.zap}` : null, i.mesec, i.roj ? `roj=${i.roj}` : null, i.vas ? `vas=${String(i.vas).slice(0,10)}` : null, i.hisna ? `h=${i.hisna}` : null, i.otrok ? `${String(i.otrok).slice(0,12)}` : null, i.ocec ? `oč:${String(i.ocec).slice(0,22)}` : null, i.opomba ? `OP:${String(i.opomba).slice(0,30)}` : null].filter(Boolean).join(' | ');
        console.log(`  ${i.label}: ${k}`);
      }
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
console.log('P234-X-READ-KONČANO');
