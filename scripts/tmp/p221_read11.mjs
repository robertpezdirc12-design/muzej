import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
const inst = await ZAI.create();
const b64 = fs.readFileSync('/tmp/p221/krop-grib/r11_s198_zap_dno.png').toString('base64');
const r = await inst.chat.completions.createVision({
  messages: [{ role: 'user', content: [
    { type: 'text', text: `To je MIKRO-IZREZ (8× povečava) SPODNJE POLOVICE zaporednega stolpca razprte strani krstne knjige (1885). Preštej in preberi VSAK vpisani znak/številko OD ZGORAJ NAVZDOL — vključno s prečrtanimi, robnimi, svinčnikovimi. Za vsakega napiši: (a) grob vertikalni položaj v % izreza (0=zgoraj, 100=dno), (b) vrednost, (c) ali je prečrtan/roben/svinčnik vs. črnilo-v-tabeli, (d) ali stoji v ČRTI TABELE (med horizontalnimi črtami = prava vrstica) ALI NA ROBU/NAD/POD tabelo (marginalija!). Na koncu povej, koliko PRAVIH vrstic-tabele (z ordinalom v črnilu med horizontalnimi črtami) je vidnih. Izhod: samo JSON {"znaki": [{"poz": 0-100, "vrednost": "...", "tip": "crtilo|svincnik|robni", "v_vrsti": true|false}], "pravih_vrstic": N, "opomba": "..."}` },
    { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
  ]}],
  thinking: { type: 'disabled' }
});
console.log(r.choices[0].message.content);
