// P232 — branje ločilnih krops X1–X3 (definitivna ločitev garble-DUELOV!).
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p232/krops';

const TASKS = [
  { sheet: 'sheet-X1.png', prompt: `To je vertikalna zaporedja 12-izrezov iz strani krstne matične knjige župnije Podzemelj (leto 1873/1874 — STAREJŠA Kurrent-pisava!). Vsak izrez = 1-vrstica (LEVO=datumi+vas+hišna+ime / DESNO=starši+botra+duhovnik / POLNO=cela-vrstica / HISNA=zoom-hišnega-stolpca / MESEC=zoom-meseca).
LOČI naslednje DUELE po številki izreza:
(1) s37-r1: zaporedna-cifra (28-ali-98? Kurrent-9-lahko-videti-kot-2!) + mesec/dan (Dezember-28/29?) + vas (Kloster?) + hisna (69?)
(2) s37-r2: RESTART-vrstica — mesec ('Jänner'?), dan rojstva (1.?) in krsta (4.?), vas (Gradac?), hisna (31?), ime (Maria?), oče (Martin-Malešič?), VELIKA-kalligrafija-'Initium-anni-Domini-1874' — ali-jo-vidiš-nad-vrstico?
(3) s37-r2-MESEC: kaj-točno-piše-v-mesecni-celici?
(4-5) s37-r4 Griblje-Anton: dan (14/14?), hisna (12?), oče (Johann-Dragoš/Dragas?), matec (Anna-Dragoš/Dragas-roj.-Jakofčič?), botra (Joseph+Anna-Jakofčič-ali-samo-Maria-Jakofčič?-Koliko-oseb? Katera-imena?), duhovnik-podpis ('Dovgan'-'Schwinger'-'Schringer'-'Coop'?)
(6-8) s38-r1 Griblje-Anna: mesec (Februar/Feber?), dan (7/8?), hisna (46-ali-drugačna?), oče (Marcus-+priimek: Hribuar/Gribovc/Hlobučar/Grilc?-Kaj-točno-črke?-in-stan: ½-Ganzl-ali-¾-Ganzl?), matec (Katharina-Milek?), botra (Mathias-Kruel/Krucel/Krušič + kdo-še? Anna-Milek? Lovrenc?)
(9-10) s38-r3 Griblje-Anna: hisna (45-ali-25-ali-druga?), oče (Mathias-Brune/Brime/Brimec?), matec (Maria-Marvin/Markovin/Horvat?), botra (Peter-Milek + kdo-še? Ana-Kuhar/Hulak/Lovrenc?)
(11) s39-r3: vas (Griblje-ali-KEJ-DRUGEGA?-pozorno!-Grible/Griable/Gribl-…?), hisna (1?), mesec/dan (April-11/11?-März?), ime (Maria?), oče (Martin-+priimek?-kaj-piše-poleg-'kajfežl/christian'?-ali-je-to-drugega?), matec (Margaretha-+priimek? Teran/Teranik?), botra (Nikolaus-Tomc + Katarina-?)
(12) s39-r5 Griblje-Katharina: oče (Mathias-Strauch/Strohm/Braučič/Brunčič?-Kaj-točno?), matec (Agnes-Klobučar?), botra (Mathias-isti-kot-oče? + Maria-Klobučar + kaj-je-'Lužana'?)
Izhod: SAMO veljaven JSON: {"izrezi":[{"label":"1","ločitev":"...","podrobnosti":"..."}, ...]}` },
  { sheet: 'sheet-X2.png', prompt: `To je vertikalna zaporedja 12-izrezov iz strani krstne matične knjige župnije Podzemelj (leto 1874 — STAREJŠA Kurrent-pisava!). Vsak izrez = 1-vrstica (LEVO=datumi+vas+hišna+ime / DESNO=starši+botra+duhovnik / POLNO=cela-vrstica).
LOČI naslednje DUELE po številki izreza:
(1) s39-r5 LEVO: MESEC (März-ali-April?-pozorno-na-prvo-črko!) + dan (13/13?) + hisna (44?)
(2) s39-r6 LEVO: mesec + dan (15/16?) + hisna (18?) + matec (Theresia-Janapič/Zunjič/Janapičič?-kaj-točno?)
(3) s39-r6 DESNO: oče (Georgius-Simec-+stan: ¼-Ganzl-ali-½?-+pridevek-Hlepec/Klepec/Grbec?) + botra (Mathias-+priimek? + Anna-+priimek-Jablajočič/Janapič?) + opomba-desno (†-datum?-3.2.1933?-ali-nič?)
(4) s39-r8 POLNO: vas (Griblje-ali-druga-vas?!) + hisna (30?) + mesec/dan (April-18/18?) + ime (Josefa?) + oče (Mathias-Herbavec?-priimek-točno!) + matec (Gerdrna/Gertruda-+priimek-Love/Lojda/Levar?) + botra (Janez-Herbavec + Maria-Herbavec?)
(5) s39-r9 POLNO: vas (Griblje!) + mesec (April/März?) + dan (19/19?) + hisna (48?) + ime (Maria?) + oče (Johann-+priimek: Klobučar/Kolbl/Koblar?-TOČNO!) + matec (Barbara-+priimek: Pezdirc/Prahin/Perdic-★★★ KLJUČNO!) + botra (Mathias-+priimek-Strauch/Braučič? + Barbara-+priimek-Brodarič/Braučič?)
(6) s40-r3 POLNO: MESEC (kaj-piše?-June/July/August-neberljivo?) + dan (21/21?) + vas (Griblje?) + hisna (39?) + ime (Mathias?) + oče (Miklo/Miłko-Mathias?-priimek: Jarrec/Jarmec/Simec/Zimec-★★★!) + matec (Katharina-+priimek-Jakofič/Jakhovič/Jakopič?) + botra (Anton-+priimek + Maria-+priimek-Klobučar/Hlabin?)
(7) s42-r7 LEVO: mesec (August?) + dan (15/16?) + hisna (40-ali-10-ali-49?) + ime (Johann?)
(8) s42-r7 DESNO: oče (Mathias-+priimek: Zupančič/Zgajdire/Zudince/Pegdire-★★★!) + matec (Dora-+priimek-Jakofčič/Sathošič/Jakofina?) + botra (Anton-Brodarič/Homac + Maria-Milek/Lovren?)
(9) s43-r4 DESNO: oče (Georg-+priimek-Felk/Zelko/Velk? + stan ¼-ali-½?) + matec (Katharina-rod.-Hrižan/Križan?) + botra (Johan-+priimek-Felah/Pilak/Folak? + žena-Anna + Margaretha-+priimek-Begić/Bizdivec?)
(10) s43-r5 DESNO: oče (Anton-Brodarič/Brodaric-+stan ½-ali-¼-'Griblnar/Ganzl/Gärtler'?) + matec (Barbara-+priimek: Pezdirc/Bizdivec/Perdic-★★★ KLJUČNO!) + botra (Mathias-Deblič/Deklič + Katharina-+priimek-Pezdir/Bizdivec?)
(11) s44-r1 DESNO: oče (Johan/Johann-+priimek: Jaškovič/Jakofčič/Jaškofič-★★★! + stan ¼-götl-ali-½-Gärtler?) + matec (Maria-rod.-isti-priimek?) + botra (Nicolaus-+priimek-Kelho/Kefho/Kelčho? + Anna-Dragos + kdo-še?)
(12) s44-r3 DESNO: oče (Mathias-+priimek-Jakopič/Jakofčič-+stan) + matec (Maria-rod.-Hrižan/Križan/Hrižman?) + boter (Michael-+priimek-Pezdirc/Petohne/Perdike-★★★ KLJUČNO!) + botra (Anna-+priimek?) + opomba (modri-pripis: preseljen/poročen-19.3.1882?-kaj-točno?)
Izhod: SAMO veljaven JSON: {"izrezi":[{"label":"1","ločitev":"...","podrobnosti":"..."}, ...]}` },
  { sheet: 'sheet-X3.png', prompt: `To je vertikalna zaporedja 12-izrezov iz strani krstne matične knjige župnije Podzemelj (leto 1874/1875 — STAREJŠA Kurrent-pisava!). Vsak izrez = 1-vrstica (LEVO=datumi+vas+hišna+ime / DESNO=starši+botra+duhovnik / POLNO=cela-vrstica / HISNA=zoom-hišnega-stolpca / MES=zoom-meseca+zap).
LOČI naslednje DUELE po številki izreza:
(1) s45-r2 LEVO: mesec (November?) + dan (1/1?) + hisna (66-ali-64?) + ime (Katharina?) + oče (Johann-+priimek: Priban/Pritzau/Grižan/Križan/Hrižan-★★★ TOČNO!)
(2) s45-r2 DESNO: oče-stan (Halter/¼-Ganzl?) + matec (Katharina-+priimek: mihil/Michel/Vidmar?) + botra (Peter-Legdire/Legdirec-Levanman/Lavman? + Anna-+priimek-Brune/Primic?) + MODRI-pripis (†-datum?-22.10.1930?)
(3) s45-r5 LEVO: hisna (32-ali-52-ali-62-★★★!) + mesec/dan (November-8/9?) + ime (Katharina?)
(4) s45-r5 DESNO: oče (Johann-Legdire/Legdirec? + stan ¼-G.?) + matec (Maria-+priimek-Voralt/Vorak/Novak/Donak?) + botra (Maurus-Klobučar + Maria-?)
(5) s46-r2 DESNO: oče (Peter-+priimek-Hrižan/Križan-★★!) + matec (Dorothea-isti-priimek?) + botra (Georgius-+priimek-Kump/Kumpar/Pircer? + Maria/Anna-+priimek-Lah/Lumpi?)
(6) s46-r3 LEVO: mesec (November?) + dan (28/28?) + hisna (40-ali-4-★★★ P231-pravi-h4!)
(7) s46-r3 DESNO: oče (Johann-+priimek-Pegdire/Perdic/Pezdirc-★★★!) + matec (Anna-+priimek-Pahovič/Jakofčič?) + botra (Mathias-Debelič/Deblin? + Barbara-+priimek-Hlovenčič/Vrboučan?) + MODRI-pripis (†-datum-1947?)
(8) s47-r1 MES+zap: zap-cifra + mesec (Dezember?) + dan (26/26?) + vas (Dobravce?) + hisna (13?) + ime (Maria?)
(9) s47-r3 HISNA: cifra (22-ali-42-★★★!)
(10) s47-r4 POLNO: ime (Maria-ali-Franziska-★★?) + dan (28/29?) + vas (Griblje?) + hisna (65?) + oče (Mathias-Milek?) + matec (Katharina-Harasinič?) + boter (Peter-+priimek-Perdic/Perchke/Perdike/PEZDIRC-★★★!) + botra (Anna-+priimek-Putlar/Turk/Loman?)
(11) s47-r7 POLNO: leto-obdobje (1875-z2!) + ime (Vinolans/Mikloša-Nicolaus?) + vas (Griblje?) + hisna (30?) + oče (PRAZNO/nezakonski?) + matec (Theresia-+priimek-Perhovac/Petohovac-'eg.-paroch.-Lipnik'?) + botra (Nicolaus-Hrižan + Rosa-Hrižan-★★ DVOJNI!)
(12) s46-r4 POLNO: vas (Krasinec?) + hisna (21?) + ime (Mathias-Anton?) + oče (Josef-Muc/MUC?) + MODRI-pripis ('umrl-dne-13.7.1949-v-CHICAGO-military-service-record'?)
Izhod: SAMO veljaven JSON: {"izrezi":[{"label":"1","ločitev":"...","podrobnosti":"..."}, ...]}` },
];

for (const t of TASKS) {
  const outPath = `/tmp/p232/x-${t.sheet.replace('sheet-', '').replace('.png', '')}.json`;
  if (fs.existsSync(outPath)) { console.log(`${t.sheet}: ŽE`); continue; }
  const b64 = fs.readFileSync(`${DIR}/${t.sheet}`).toString('base64');
  let done = false;
  for (let attempt = 1; attempt <= 4 && !done; attempt++) {
    try {
      const r = await Promise.race([
        inst.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: t.prompt },
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
      fs.writeFileSync(outPath, JSON.stringify(j, null, 2));
      console.log(`${t.sheet}: OK`);
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
console.log('P232-X-READ-KONČANO');
