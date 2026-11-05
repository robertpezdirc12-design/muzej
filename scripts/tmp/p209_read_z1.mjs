import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
const b64 = fs.readFileSync('/tmp/p209/krop-grib/arb_s69_z1cell.png').toString('base64');
const inst = await ZAI.create();
const make = () => inst.chat.completions.createVision({
  messages: [{ role: 'user', content: [
    { type: 'text', text: `To je IZREZ DATUMSKE-CELICE iz MRLIŠKE matične knjige (meja-letnika!). NALOGA: prepiši TOČNO kaj-je-v-datumski-celici-prve-vrstice-z-ordinalo-'1' — letnica + mesec + dnevi (npr. '1868. Jänner 1.'). Ali-je-letnica-'1868'-ali-'1867'-ali-druga? KURRENT-zmeda-6/8/9-mogoča! + kateri-mesec-glava? Izhod: SAMO JSON: {"celica_z1": "...", "letnica": "...", "mesec": "...", "opomba": "..."}` },
    { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
  ]}],
  thinking: { type: 'disabled' }
});
for (let a = 1; a <= 4; a++) {
  try {
    const c = await Promise.race([make(), new Promise((_, r) => setTimeout(() => r(new Error('t')), 180000))]);
    const t = (c?.choices?.[0]?.message?.content || '').trim().replace(/^```(json)?/i, '').replace(/```$/, '');
    const res = JSON.parse(t.slice(t.indexOf('{'), t.lastIndexOf('}') + 1));
    fs.writeFileSync('/tmp/p209/krop-grib/arb_s69_z1cell.json', JSON.stringify(res, null, 2));
    console.log('OK celica:', res.celica_z1, '| letnica:', res.letnica, '| mesec:', res.mesec);
    process.exit(0);
  } catch (e) { console.error(`poskus ${a} FAIL`); await new Promise(r => setTimeout(r, 2500 * a)); }
}
process.exit(1);
