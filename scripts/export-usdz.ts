/**
 * EXPORT USDZ — cerkev sv. Vida: GLB → USDZ (issue #12, iOS AR Quick Look).
 *
 * iOS Safari ne podpira WebXR, <model-viewer> pa tam AR zažene prek
 * AR Quick Look, ki potrebuje USDZ. Zato dual-model po vzoru Nîmes:
 *   Android/WebXR → cerkev-sv-vida.glb
 *   iPhone        → cerkev-sv-vida.usdz (iOS Quick Look)
 *
 * Uporaba: bun scripts/export-usdz.ts
 * (three.js USDZExporter, brez tekstur — GLB ima samo baseColorFactor)
 */

import * as fs from "node:fs";
import * as path from "node:path";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { USDZExporter } from "three/examples/jsm/exporters/USDZExporter.js";

const GLB = path.resolve("public/models/cerkev-sv-vida.glb");
const OUT = path.resolve("public/models/cerkev-sv-vida.usdz");

const data = fs.readFileSync(GLB);
const loader = new GLTFLoader();

loader.parse(
  data.buffer.slice(
    data.byteOffset,
    data.byteOffset + data.byteLength,
  ) as ArrayBuffer,
  "",
  async (gltf) => {
    const root = gltf.scene;
    /* USDZExporter pričakuje normalo na vsaki geometriji */
    root.traverse((o) => {
      const m = o as THREE.Mesh;
      if (m.isMesh && m.geometry && !m.geometry.getAttribute("normal")) {
        m.geometry.computeVertexNormals();
      }
    });
    root.updateMatrixWorld(true);

    /* Quick Look privzame metre — model GLB je v metrih (13 m višine po
       skali v village-scene). USDZ pusti v isti skali. */
    const exporter = new USDZExporter();
    const usdz = await exporter.parseAsync(root, {
      maxTextureSize: 1024,
    });
    fs.writeFileSync(OUT, Buffer.from(usdz));
    const kb = (fs.statSync(OUT).size / 1024).toFixed(1);
    console.log(`OK: ${OUT} (${kb} KB)`);
    process.exit(0);
  },
  (err) => {
    console.error("GLTF parse failed:", err);
    process.exit(1);
  },
);
