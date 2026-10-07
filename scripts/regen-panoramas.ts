import ZAI from "z-ai-web-dev-sdk";
import fs from "fs";

const COMMON = "CRITICAL equirectangular rules: the horizon line must be placed EXACTLY at 50% of the image height — the entire top half of the image is sky and clouds only, the entire bottom half is land and water. The extreme left edge and the extreme right edge of the image must show the same continuous open scenery (meadow grass and sky), so that the panorama wraps around seamlessly. Historical year 1825: absolutely no cars, no vehicles, no power lines, no paved roads, no modern buildings, no people, no animals, no text, no watermark. Photorealistic, naturalistic detail, muted earthy palette.";

const PROMPTS: Record<string, string> = {
  "jedro-1825": `Seamless equirectangular 360 degree panorama, 2:1 aspect ratio. Historical reconstruction of the core of a Slovenian village in 1825, Bela krajina. Viewpoint: standing in the middle of the village on a narrow earthen lane. Center of the image: a low grassy hill in the middle distance with a small white baroque church with a wooden bell tower and a walled churchyard with cemetery crosses; a dirt lane runs ahead toward the church hill. Around the viewer on both sides of the lane: small timber farmhouses with steep gabled roofs of wooden shingles and thatch, wooden fences, low barns, wooden hayracks, kitchen gardens, stacked firewood. Right side of the image: the land opens into meadows with a river glinting far in the distance. Left side: more scattered timber farmhouses, then fields and a dark oak-beech forest edge. Soft morning light of late summer, gentle haze, long shadows. ${COMMON}`,
  "kolpa-1825": `Seamless equirectangular 360 degree panorama, 2:1 aspect ratio. Historical landscape reconstruction of the Kolpa river in Bela krajina, Slovenia, in 1825. Viewpoint: standing on a grassy riverbank, a calm green river about forty meters wide flowing slowly with gentle ripples. Center and left of center: flat riverside meadows stretching inland, a scattered village of small timber farmhouses with steep shingled gabled roofs far in the distance, thin morning smoke rising from one chimney. Right of center: the river curves away, pebble banks and willows along the near shore. Far right and behind: the far bank rises into a low wooded terrace of oak and beech forest. Left edge: open meadow. Early autumn morning, golden low light, thin mist over the water, soft reflections. ${COMMON}`,
};

async function main() {
  const zai = await ZAI.create();
  for (const [name, prompt] of Object.entries(PROMPTS)) {
    const out = `/tmp/pano/${name}.png`;
    let ok = false;
    for (let attempt = 1; attempt <= 3 && !ok; attempt++) {
      try {
        const res = await zai.images.generations.create({ prompt, size: "2048x1024" as "1024x1024" });
        const b64 = res.data?.[0]?.base64;
        if (!b64) throw new Error("no image");
        fs.writeFileSync(out, Buffer.from(b64, "base64"));
        console.log(`OK ${name}`);
        ok = true;
      } catch (e) {
        console.error(`FAIL ${name} #${attempt}: ${e}`);
        await new Promise((r) => setTimeout(r, 2500 * attempt));
      }
    }
    if (!ok) process.exit(1);
  }
}
main();
