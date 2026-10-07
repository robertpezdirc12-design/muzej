/** Generiranje hero panoram (issue #13) — equirectangular 2048×1024. */
import ZAI from "z-ai-web-dev-sdk";
import fs from "fs";

const PROMPTS: Record<string, string> = {
  "cerkev-1825":
    "Seamless equirectangular 360 degree panorama, 2:1 aspect ratio, horizon exactly at the vertical center of the frame. Historical landscape reconstruction of a small Slovenian village in 1825, Bela krajina region. Viewpoint: standing on a small cemetery hill with an old white baroque church with a modest wooden-shingled bell tower directly behind the viewer. Ahead, center of the image: a scattered village of about thirty small timber farmhouses with steep gabled roofs of wooden shingles and thatch, arranged in two loose clusters, hayracks and wooden fences between them. To the right of center the landscape opens into mowed riverside meadows with a calm green river (the Kolpa) glinting in the distance. To the left, gentle meadows ending in a dark oak and beech forest edge. Foreground: a simple graveyard with a few old wooden and stone crosses and low grass. Early autumn morning, low golden sunlight from the east, long soft shadows, thin mist over the meadows. Photorealistic, painterly naturalistic detail, muted earthy palette of wood, straw and green. No people, no animals, no vehicles, no text, no watermark, no modern objects, no power lines.",
  "jedro-1825":
    "Seamless equirectangular 360 degree panorama, 2:1 aspect ratio, horizon exactly at the vertical center of the frame. Historical reconstruction of the core of a Slovenian village in 1825, Bela krajina. Viewpoint: standing in the middle of the village, on a narrow earthen lane. Center of the image: a low grassy hill in the middle distance with a small white baroque church with a wooden bell tower and a walled churchyard, cemetery crosses visible. Around the viewer on both sides of the lane: small timber farmhouses with steep gabled shingle and thatch roofs, wooden fences, low barns and hayracks, small kitchen gardens, stacked firewood. The lane runs ahead toward the church hill. Right side of the image: the land opens into meadows, a river glinting far in the distance. Left side and behind: more scattered farmhouses, then fields and a dark oak-beech forest edge. Soft morning light of late summer, gentle haze, long shadows across the lane. Photorealistic, muted natural palette of weathered wood, straw, earth and green. No people, no animals, no vehicles, no text, no watermark, no modern objects, no power lines.",
  "kolpa-1825":
    "Seamless equirectangular 360 degree panorama, 2:1 aspect ratio, horizon exactly at the vertical center of the frame. Historical landscape reconstruction of the Kolpa river in Bela krajina, Slovenia, in 1825. Viewpoint: standing on a grassy riverbank on the Slovenian side of a calm green river, about forty meters wide, the water flowing slowly with gentle ripples. Center and left of center of the image: flat riverside meadows stretching inland, with a scattered village of small timber farmhouses with steep shingled gabled roofs in the far distance, thin morning smoke rising from one chimney. Right of center: the river curves away, pebble banks and willows along the near shore. Behind the viewer and to the far right: the far bank rises into a low wooded terrace of oak and beech forest. Left edge: a meadow with a lone wooden hayrack. Early autumn morning, golden low light from the east, thin mist over the water, soft reflections. Photorealistic, painterly naturalistic, muted palette of green water, grass, weathered wood. No people, no animals, no boats, no bridges, no buildings near the bank, no text, no watermark, no modern objects, no power lines.",
};

async function main() {
  const zai = await ZAI.create();
  for (const [name, prompt] of Object.entries(PROMPTS)) {
    const out = `/tmp/pano/${name}.png`;
    if (fs.existsSync(out)) {
      console.log(`skip ${name} (exists)`);
      continue;
    }
    let ok = false;
    for (let attempt = 1; attempt <= 3 && !ok; attempt++) {
      try {
        const res = await zai.images.generations.create({ prompt, size: "2048x1024" as "1024x1024" });
        const b64 = res.data?.[0]?.base64;
        if (!b64) throw new Error("no image in response");
        fs.writeFileSync(out, Buffer.from(b64, "base64"));
        console.log(`OK ${name} (${Math.round(fs.statSync(out).size / 1024)} KB)`);
        ok = true;
      } catch (e) {
        console.error(`FAIL ${name} attempt ${attempt}: ${e}`);
        await new Promise((r) => setTimeout(r, 2000 * attempt));
      }
    }
    if (!ok) process.exit(1);
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
