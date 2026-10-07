import ZAI from "z-ai-web-dev-sdk";
import fs from "fs";

const PROMPT = `Seamless equirectangular 360 degree panorama, 2:1 aspect ratio. Historical landscape reconstruction of the Kolpa river in Bela krajina, Slovenia, in the year 1825. Viewpoint: standing on a grassy wild riverbank, a calm green river about forty meters wide flowing slowly with gentle ripples. Center and left of center of the image: flat riverside meadows stretching inland, with a scattered village of small timber farmhouses with steep shingled gabled roofs very far in the distance, thin morning smoke rising from one chimney. Right of center: the river curves away, pebble banks and willows along the near shore. Far right and behind the viewer: the far bank rises into a low wooded terrace of oak and beech forest. Left edge: open meadow with a lone wooden hayrack. There are NO roads, NO paths, NO trails, NO bridges, NO boats, NO buildings near the bank — only wild nature: water, grass, pebbles, willows, distant forest. Early autumn morning, golden low light from the east, thin mist over the water, soft reflections. CRITICAL equirectangular rules: the horizon line must be placed EXACTLY at 50% of the image height — the entire top half of the image is sky and clouds only, the entire bottom half is land and water. The extreme left edge and the extreme right edge of the image must show the same continuous open scenery (river meadow and sky), so the panorama wraps around seamlessly. Historical year 1825: absolutely no cars, no vehicles, no roads, no power lines, no modern buildings, no people, no animals, no text, no watermark. Photorealistic, naturalistic detail, muted earthy palette of green water, grass and weathered wood.`;

async function main() {
  const zai = await ZAI.create();
  const out = "/tmp/pano/kolpa-1825.png";
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const res = await zai.images.generations.create({ prompt: PROMPT, size: "2048x1024" as "1024x1024" });
      const b64 = res.data?.[0]?.base64;
      if (!b64) throw new Error("no image");
      fs.writeFileSync(out, Buffer.from(b64, "base64"));
      console.log("OK kolpa");
      return;
    } catch (e) {
      console.error(`FAIL #${attempt}: ${e}`);
      await new Promise((r) => setTimeout(r, 2500 * attempt));
    }
  }
  process.exit(1);
}
main();
