"use client";

/**
 * VILLAGE SCENE — proceduralni 3D prizor vasi Griblje (three.js, issue #10).
 *
 * En prizor, dva načina:
 *  · "ar"     — kamera telefona v ozadju (video), prizor čez; kamera stoji
 *               na uporabnikovem GPS (ali na 360° stališču pri cerkvi, issue #12),
 *               kompas obrača pogled (kot ar-camera);
 *  · "orbit"  — prosto vrtenje/zoom (ATLAS 3D zavihek, namizje).
 *
 * Stavbe: InstancedMesh (sten BoxGeometry + dvokapnice prizma) iz 156 katastrskih
 * podlatn; ~1900 dodana zgostitev jedra (ločen instancovan, poudarjen); "danes"
 * = KAJ JE IZGINILO (issue #12): duhovi 1825 obarvani po statusu (🟢 obstaja,
 * 🟡 negotovo, 🔴 ni je več — primerjava z OSM) + današnje OSM stavbe kot
 * digitalni dvojček (samo orbit; v AR se danes vidi skozi kamero).
 * Cerkev sv. Vida: obstoječi muzejski GLB model na svoji dokumentirani
 * lokaciji. Tla: cone rabe tal + Kolpa (georef struga).
 */

import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import {
  BUILDINGS_1825,
  GROWTH_1900,
  GROUND_ZONES,
  KOLPA_LOCAL,
  CHURCH,
  CORE_CENTER,
  PRESENT_BUILDINGS,
  BUILDING_STATUS,
  toLocal,
  TREES,
  SMOKE_CHIMNEYS,
  type PreparedBuilding,
  type BuildingPresence,
} from "@/lib/village3d";
import { buildMiniScene, type MiniSceneId } from "./mini-scenes";

export type SceneMode = "ar" | "orbit";
export type SceneYear = 1825 | 1900 | 2026;

export interface PickResult {
  kind: "1825" | "growth" | "present";
  x: number;
  z: number;
  w: number;
  d: number;
  dist: number;
  /** status stavbe 1825 v primerjavi z OSM (samo kind="1825") */
  presence?: BuildingPresence;
  /** indeks v BUILDINGS_1825 (kind="1825") ali PRESENT_BUILDINGS (kind="present") */
  index?: number;
}

export interface CaptionSpec {
  title: string;
  sub: string;
  credit: string;
}

const EYE_H = 1.6;

/* ── enotska geometrija dvokapnice (baza y=0, w×d×h = 1) ── */
function gableGeometry(): THREE.BufferGeometry {
  const A = [-0.5, 0, -0.5], B = [0.5, 0, -0.5], C = [0.5, 0, 0.5],
    D = [-0.5, 0, 0.5], E = [0, 1, -0.5], F = [0, 1, 0.5];
  const tris = [
    A, E, B,  /* čelna ustnica (−z) */
    D, C, F,  /* zadnja ustnica (+z) */
    B, E, F, B, F, C, /* desna ploskev */
    A, D, F, A, F, E, /* leva ploskev */
  ];
  const pos = new Float32Array(tris.length * 3);
  tris.forEach((v, i) => pos.set(v as number[], i * 3));
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  /* UV map: roof slopes tile from ridge to eaves; gable ends map separately. */
  g.setAttribute(
    "uv",
    new THREE.Float32BufferAttribute([
      0, 0, 0.5, 1, 1, 0,
      0, 0, 1, 0, 0.5, 1,
      0, 1, 0, 0, 1, 0,
      0, 1, 1, 0, 1, 1,
      0, 1, 1, 1, 1, 0,
      0, 1, 1, 0, 0, 0,
    ], 2),
  );
  g.computeVertexNormals();
  return g;
}

/* ── trak (Kolpa) skozi točke, širina w ── */
function ribbonGeometry(pts: { x: number; z: number }[], w: number): THREE.BufferGeometry {
  const verts: number[] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p = pts[i], q = pts[i + 1];
    const dx = q.x - p.x, dz = q.z - p.z;
    const len = Math.hypot(dx, dz) || 1;
    const nx = -dz / len * (w / 2), nz = dx / len * (w / 2);
    const y = 0.12;
    const pL = [p.x + nx, y, p.z + nz], pR = [p.x - nx, y, p.z - nz];
    const qL = [q.x + nx, y, q.z + nz], qR = [q.x - nx, y, q.z - nz];
    verts.push(...pL, ...pR, ...qL, ...qL, ...pR, ...qR);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(verts, 3));
  g.computeVertexNormals();
  return g;
}

/**
 * Proceduralni, deterministični materiali za prikaz — niso nadomestilo za
 * izmerjene teksture konkretnih stavb. Namenjeni so boljši svetlobi in
 * materialnosti medtem, ko zbiramo preverjene terenske fotografije.
 */
function makePlasterTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 256;
  const ctx = canvas.getContext("2d");
  if (!ctx) return new THREE.CanvasTexture(canvas);
  const image = ctx.createImageData(256, 256);
  for (let y = 0; y < 256; y++) {
    for (let x = 0; x < 256; x++) {
      let n = (Math.imul(x + 17, 374761393) ^ Math.imul(y + 31, 668265263)) >>> 0;
      n = Math.imul(n ^ (n >>> 13), 1274126177) >>> 0;
      const grain = (n % 31) - 15;
      const grime = Math.max(0, (y - 196) / 60) * 8;
      const wash = Math.sin(y * 0.065 + Math.sin(x * 0.035) * 2.2) * 3.5;
      const i = (y * 256 + x) * 4;
      image.data[i] = THREE.MathUtils.clamp(216 + grain + wash - grime, 0, 255);
      image.data[i + 1] = THREE.MathUtils.clamp(204 + grain + wash - grime, 0, 255);
      image.data[i + 2] = THREE.MathUtils.clamp(183 + grain + wash - grime, 0, 255);
      image.data[i + 3] = 255;
    }
  }
  ctx.putImageData(image, 0, 0);
  /* nežni razpokani sledovi ometa; umetni material, ne dokumentiran vzorec */
  ctx.strokeStyle = "rgba(108,91,69,0.18)";
  ctx.lineWidth = 0.7;
  for (let i = 0; i < 20; i++) {
    const x = (i * 47 + 19) % 256;
    const y = (i * 73 + 31) % 220;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + ((i % 3) - 1) * 2.5, y + 9 + (i % 8) * 2);
    ctx.stroke();
  }
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
  texture.anisotropy = 4;
  return texture;
}

function makeRoofTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 512;
  const ctx = canvas.getContext("2d");
  if (!ctx) return new THREE.CanvasTexture(canvas);
  ctx.fillStyle = "#66513c";
  ctx.fillRect(0, 0, 512, 512);
  /* ploščice so namenoma generična interpretacija, ne trditev o vseh strehah 1825 */
  for (let row = 0; row < 23; row++) {
    const y = row * 23;
    const offset = row % 2 ? -13 : 0;
    for (let col = -1; col < 18; col++) {
      const seed = (Math.imul(row + 5, 73856093) ^ Math.imul(col + 9, 19349663)) >>> 0;
      const tone = seed % 32;
      const r = 116 + tone;
      const g = 72 + Math.floor(tone * 0.57);
      const b = 43 + Math.floor(tone * 0.3);
      const x = col * 31 + offset;
      ctx.fillStyle = `rgb(${r},${g},${b})`;
      ctx.fillRect(x + 1, y + 1, 29, 21);
      ctx.strokeStyle = "rgba(40,29,21,0.48)";
      ctx.lineWidth = 1;
      ctx.strokeRect(x + 1.5, y + 1.5, 28, 20);
      ctx.strokeStyle = "rgba(235,190,138,0.14)";
      ctx.beginPath();
      ctx.moveTo(x + 3, y + 3);
      ctx.lineTo(x + 27, y + 3);
      ctx.stroke();
    }
  }
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
  texture.anisotropy = 4;
  return texture;
}

function makeGroundTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 256;
  const ctx = canvas.getContext("2d");
  if (!ctx) return new THREE.CanvasTexture(canvas);
  ctx.fillStyle = "#718562";
  ctx.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 1300; i++) {
    const seed = (Math.imul(i + 7, 2246822519) ^ Math.imul(i + 13, 3266489917)) >>> 0;
    const x = seed % 256;
    const y = (seed >>> 8) % 256;
    const size = 1 + (seed % 5);
    const tones = ["rgba(34,67,37,0.20)", "rgba(195,174,114,0.17)", "rgba(222,216,164,0.09)", "rgba(36,52,31,0.13)"];
    ctx.fillStyle = tones[seed % tones.length];
    ctx.fillRect(x, y, size, size * ((seed % 3) + 1));
  }
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(64, 64);
  texture.anisotropy = 4;
  return texture;
}

interface YearVisual {
  wallsOpacity: number;
  roofsOpacity: number;
  wallsWire: boolean;
  growthOpacity: number;
  showGrowth: boolean;
  /** današnje OSM stavbe (samo orbit: digitalni dvojček) */
  presentOpacity: number;
  showPresent: boolean;
}

const YEAR_VISUALS: Record<SceneYear, YearVisual> = {
  1825: { wallsOpacity: 1, roofsOpacity: 1, wallsWire: false, growthOpacity: 0, showGrowth: false, presentOpacity: 0, showPresent: false },
  1900: { wallsOpacity: 1, roofsOpacity: 1, wallsWire: false, growthOpacity: 0.96, showGrowth: true, presentOpacity: 0, showPresent: false },
  2026: { wallsOpacity: 0.3, roofsOpacity: 0.06, wallsWire: true, growthOpacity: 0, showGrowth: false, presentOpacity: 0.85, showPresent: true },
};

/* barve statusov duhov 1825 v načinu »danes« (Kaj je izginilo?) */
const PRESENCE_COLORS: Record<BuildingPresence, THREE.Color> = {
  exists: new THREE.Color(0x35c287), /* smaragdna — stoji še danes */
  uncertain: new THREE.Color(0xe0a63a), /* jantorna — negotovo */
  gone: new THREE.Color(0xe06a5a), /* opečno rdeča — ni je več */
};

export class VillageScene {
  private renderer: THREE.WebGLRenderer;
  private scene = new THREE.Scene();
  private camera: THREE.PerspectiveCamera;
  private controls: OrbitControls | null = null;
  private raf = 0;
  private disposed = false;
  private ro: ResizeObserver;

  private walls1825: THREE.InstancedMesh;
  private roofs1825: THREE.InstancedMesh;
  private wallsGrowth: THREE.InstancedMesh;
  private roofsGrowth: THREE.InstancedMesh;
  private wallsPresent: THREE.InstancedMesh;
  private wallsMat: THREE.MeshStandardMaterial;
  private roofsMat: THREE.MeshStandardMaterial;
  private growthWallsMat: THREE.MeshStandardMaterial;
  private growthRoofsMat: THREE.MeshStandardMaterial;
  private presentMat: THREE.MeshLambertMaterial;
  private groundPlane: THREE.Mesh;
  /** cone rabe tal + Kolpa + DREVESA — skupaj, da jih mini-scena skrije */
  private envGroup = new THREE.Group();
  /** Hišna vrata, okenski okvirji, podzidki in strešni robovi — isti model za orbit in AR. */
  private facadeGroup = new THREE.Group();
  private facadeMaterials: THREE.Material[] = [];
  private churchRoot: THREE.Group | null = null;

  /* P12: drevesa (instancirana debla + listave/iglavci kroni) */
  private treeTrunks: THREE.InstancedMesh;
  private treeCrownsDec: THREE.InstancedMesh;
  private treeCrownsCon: THREE.InstancedMesh;

  /* P12: dim iz dimnikov (sprajti — interpretacija, vas živi) */
  private smokeGroup = new THREE.Group();
  private smokeTex: THREE.CanvasTexture | null = null;
  private smokeSprites: { spr: THREE.Sprite; phase: number; x: number; z: number; top: number }[] = [];

  /** mini-scena oddaljene točke (issue #12 — mlini/cerkvišče) */
  private mini: {
    id: MiniSceneId;
    handle: import("./mini-scenes").MiniSceneHandle;
    center: { x: number; z: number };
  } | null = null;
  private miniStart = performance.now();

  private mode: SceneMode;
  private year: SceneYear = 1825;
  private vis: YearVisual = { ...YEAR_VISUALS[1825] };

  /* AR pozicioniranje */
  private fix: { x: number; z: number } | null = null;
  /** dvig oči nad tlemi (360° vzpon pri cerkvi) */
  private fixElev = 0;
  private compassYaw: number | null = null;
  private manualYaw = 0;
  private manualPitch = 0;
  private curYaw = 0;
  private curPitch = 0;
  private curX = 300;
  private curZ = 320;
  private hasFixEver = false;

  private canvas: HTMLCanvasElement;
  private onPick: ((p: PickResult | null) => void) | undefined;
  private pointerDown: { x: number; y: number; t: number } | null = null;
  private dragging = false;

  constructor(
    canvas: HTMLCanvasElement,
    opts: {
      mode: SceneMode;
      onPick?: (p: PickResult | null) => void;
      onCompassNeeded?: () => void;
    },
  ) {
    this.canvas = canvas;
    this.mode = opts.mode;
    this.onPick = opts.onPick;
    /* razhroščevanje P12 (namensko testno vezje) */
    if (typeof window !== "undefined") {
      (window as unknown as { __vscene?: VillageScene }).__vscene = this;
    }

    this.renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
    });
    this.renderer.setClearColor(0x000000, 0);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.08;

    this.camera = new THREE.PerspectiveCamera(62, 1, 0.4, 4000);
    this.camera.rotation.order = "YXZ";

    /* svetloba: topla podvečerna sončna */
    const hemi = new THREE.HemisphereLight(0xf4ead2, 0x9a8a6a, 1.05);
    this.scene.add(hemi);
    const sun = new THREE.DirectionalLight(0xffe6bd, 1.15);
    sun.position.set(280, 420, -160);
    this.scene.add(sun);

    /* tla — v AR prosojna (video se vidi), v orbitu polna */
    const groundTexture = makeGroundTexture();
    this.groundPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(3200, 3200),
      new THREE.MeshStandardMaterial({
        color: 0xc4c3a0,
        map: groundTexture,
        roughness: 1,
      }),
    );
    this.groundPlane.rotation.x = -Math.PI / 2;
    this.groundPlane.position.y = -0.06;
    this.groundPlane.visible = opts.mode === "orbit";
    this.scene.add(this.groundPlane);

    /* cone rabe tal (RECONSTRUCTED) — v envGroup (mini-scena jih skrije) */
    for (const z of GROUND_ZONES) {
      const [x1, z1, x2, z2] = z.rect;
      const w = Math.max(2, x2 - x1);
      const d = Math.max(2, z2 - z1);
      const m = new THREE.Mesh(
        new THREE.PlaneGeometry(w, d),
        new THREE.MeshBasicMaterial({
          color: z.color,
          transparent: true,
          opacity: z.opacity,
          depthWrite: false,
          side: THREE.DoubleSide,
        }),
      );
      m.rotation.x = -Math.PI / 2;
      m.position.set((x1 + x2) / 2, 0.03, (z1 + z2) / 2);
      this.envGroup.add(m);
    }

    /* Kolpa — georeferencirana struga (tudi v envGroup) */
    const kolpa = new THREE.Mesh(
      ribbonGeometry(KOLPA_LOCAL, 22),
      new THREE.MeshBasicMaterial({
        color: 0x6f9ec4,
        transparent: true,
        opacity: 0.8,
        depthWrite: false,
        side: THREE.DoubleSide,
      }),
    );
    this.envGroup.add(kolpa);
    this.scene.add(this.envGroup);

    /* ── P12: DREVESA — gozdne cone gosto, loke razpršeno (interpretacija;
       enota v envGroup, da mini-scena skrije) ── */
    {
      const trunkGeo = new THREE.CylinderGeometry(0.16, 0.26, 1, 5);
      trunkGeo.translate(0, 0.5, 0);
      const crownDecGeo = new THREE.IcosahedronGeometry(1, 0);
      const crownConGeo = new THREE.ConeGeometry(1, 1.9, 6);
      crownConGeo.translate(0, 0.85, 0);
      const decCount = TREES.filter((t) => t.kind === "dec").length;
      const conCount = TREES.filter((t) => t.kind === "con").length;
      const trunkMat = new THREE.MeshLambertMaterial({ color: 0x6d5233 });
      const crownDecMat = new THREE.MeshLambertMaterial({ color: 0x4d6b3f });
      const crownConMat = new THREE.MeshLambertMaterial({ color: 0x3a5a3a });
      this.treeTrunks = new THREE.InstancedMesh(trunkGeo, trunkMat, TREES.length);
      this.treeCrownsDec = new THREE.InstancedMesh(crownDecGeo, crownDecMat, Math.max(1, decCount));
      this.treeCrownsCon = new THREE.InstancedMesh(crownConGeo, crownConMat, Math.max(1, conCount));

      const m4 = new THREE.Matrix4();
      const q = new THREE.Quaternion();
      const yAxis = new THREE.Vector3(0, 1, 0);
      const pos = new THREE.Vector3();
      const scl = new THREE.Vector3();
      const crownCol = new THREE.Color();
      let iDec = 0;
      let iCon = 0;
      TREES.forEach((t, i) => {
        q.setFromAxisAngle(yAxis, (i * 2.399) % (Math.PI * 2)); /* zlati kot */
        /* deblo: do višine 55 % drevesa */
        pos.set(t.x, 0, t.z);
        scl.set(1, t.h * 0.55, 1);
        m4.compose(pos, q, scl);
        this.treeTrunks.setMatrixAt(i, m4);
        /* krošnja: nad deblom */
        if (t.kind === "dec") {
          pos.set(t.x, t.h * 0.55, t.z);
          const r = t.h * 0.32;
          scl.set(r, r * 0.9, r);
          m4.compose(pos, q, scl);
          this.treeCrownsDec.setMatrixAt(iDec, m4);
          /* rahlo raznolike barve listja */
          crownCol.setHSL(0.28 + ((i * 0.618) % 0.05), 0.42, 0.3 + ((i * 0.37) % 0.09));
          this.treeCrownsDec.setColorAt(iDec, crownCol);
          iDec++;
        } else {
          pos.set(t.x, t.h * 0.5, t.z);
          const r = t.h * 0.2;
          scl.set(r, t.h * 0.55, r);
          m4.compose(pos, q, scl);
          this.treeCrownsCon.setMatrixAt(iCon, m4);
          iCon++;
        }
      });
      this.treeTrunks.instanceMatrix.needsUpdate = true;
      this.treeCrownsDec.instanceMatrix.needsUpdate = true;
      this.treeCrownsCon.instanceMatrix.needsUpdate = true;
      if (this.treeCrownsDec.instanceColor) this.treeCrownsDec.instanceColor.needsUpdate = true;
      this.treeTrunks.frustumCulled = false;
      this.treeCrownsDec.frustumCulled = false;
      this.treeCrownsCon.frustumCulled = false;
      this.envGroup.add(this.treeTrunks, this.treeCrownsDec, this.treeCrownsCon);
    }

    /* ── P12: DIM iz dimnikov — 8 jedrnih domačij, sprajti z mehkim
       prehodom; vidno v 1825/~1900 (ne »danes«, ne mini-scena) ── */
    {
      const cv = document.createElement("canvas");
      cv.width = 64;
      cv.height = 64;
      const ctx = cv.getContext("2d");
      if (ctx) {
        const gr = ctx.createRadialGradient(32, 32, 2, 32, 32, 30);
        gr.addColorStop(0, "rgba(240,238,232,0.55)");
        gr.addColorStop(0.55, "rgba(232,228,220,0.22)");
        gr.addColorStop(1, "rgba(232,228,220,0)");
        ctx.fillStyle = gr;
        ctx.fillRect(0, 0, 64, 64);
      }
      this.smokeTex = new THREE.CanvasTexture(cv);
      const smokeMat = new THREE.SpriteMaterial({
        map: this.smokeTex,
        transparent: true,
        depthWrite: false,
        opacity: 0.5,
      });
      SMOKE_CHIMNEYS.forEach((c, ci) => {
        for (let k = 0; k < 6; k++) {
          const spr = new THREE.Sprite(smokeMat.clone());
          spr.userData.chimney = ci;
          spr.userData.slot = k;
          this.smokeGroup.add(spr);
          this.smokeSprites.push({
            spr,
            phase: ci * 1.3 + k * 1.1,
            x: c.x,
            z: c.z,
            top: c.top,
          });
        }
      });
      this.scene.add(this.smokeGroup);
    }

    /* stavbe — instancirane */
    const box = new THREE.BoxGeometry(1, 1, 1);
    box.translate(0, 0.5, 0);
    const gable = gableGeometry();

    const plasterTexture = makePlasterTexture();
    const roofTexture = makeRoofTexture();
    this.wallsMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      map: plasterTexture,
      roughness: 0.96,
      transparent: true,
      opacity: 1,
    });
    this.roofsMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      map: roofTexture,
      roughness: 0.94,
      transparent: true,
      opacity: 1,
    });
    this.growthWallsMat = new THREE.MeshStandardMaterial({
      color: 0xd0c1a2,
      map: plasterTexture,
      roughness: 1,
      transparent: true,
      opacity: 0,
    });
    this.growthRoofsMat = new THREE.MeshStandardMaterial({
      color: 0xd0b18c,
      map: roofTexture,
      roughness: 1,
      transparent: true,
      opacity: 0,
    });

    this.walls1825 = new THREE.InstancedMesh(box, this.wallsMat, BUILDINGS_1825.length);
    this.roofs1825 = new THREE.InstancedMesh(gable, this.roofsMat, BUILDINGS_1825.length);
    this.wallsGrowth = new THREE.InstancedMesh(box, this.growthWallsMat, GROWTH_1900.length);
    this.roofsGrowth = new THREE.InstancedMesh(gable.clone(), this.growthRoofsMat, GROWTH_1900.length);

    const m4 = new THREE.Matrix4();
    const q = new THREE.Quaternion();
    const pos = new THREE.Vector3();
    const scl = new THREE.Vector3();
    const yAxis = new THREE.Vector3(0, 1, 0);

    /* današnje stavbe (OSM posnetek) — digitalni dvojček, sivo-zelena masa,
       višine ocenjene (enake za vse: OSM višin ne hrani) */
    this.presentMat = new THREE.MeshLambertMaterial({
      color: 0x6b7566,
      transparent: true,
      opacity: 0,
    });
    this.wallsPresent = new THREE.InstancedMesh(
      box,
      this.presentMat,
      PRESENT_BUILDINGS.length,
    );
    PRESENT_BUILDINGS.forEach((b, i) => {
      pos.set(b.x, 0, b.z);
      scl.set(b.w, 2.8, b.d);
      m4.compose(pos, q, scl);
      this.wallsPresent.setMatrixAt(i, m4);
    });
    this.wallsPresent.instanceMatrix.needsUpdate = true;
    this.wallsPresent.frustumCulled = false;
    this.wallsPresent.visible = false;
    this.scene.add(this.wallsPresent);

    const fill = (
      mesh: THREE.InstancedMesh,
      arr: { x: number; z: number; w: number; d: number; rotY: number; wallH: number; roofH: number }[],
      roof: boolean,
    ) => {
      arr.forEach((b, i) => {
        q.setFromAxisAngle(yAxis, b.rotY);
        pos.set(b.x, roof ? b.wallH : 0, b.z);
        scl.set(b.w, roof ? b.roofH : b.wallH, b.d);
        m4.compose(pos, q, scl);
        mesh.setMatrixAt(i, m4);
      });
      mesh.instanceMatrix.needsUpdate = true;
      mesh.frustumCulled = false;
    };

    fill(this.walls1825, BUILDINGS_1825, false);
    fill(this.roofs1825, BUILDINGS_1825, true);
    fill(this.wallsGrowth, GROWTH_1900, false);
    fill(this.roofsGrowth, GROWTH_1900, true);
    this.wallsGrowth.visible = false;
    this.roofsGrowth.visible = false;

    /*
     * Arhitekturna plast (vse dimenzije so interpretativne, tlorisi pa merjeni):
     * podzidek, opaž/eaves, vrata in okna v instancah; ostane dovolj lahka za telefon.
     * Ne prikaže se v »duhovih« 2026, da podrobnosti ne lažno predstavljajo
     * dokumentirano podobo stavb, kjer je le tloris kataster.
     */
    type DetailPose = { x: number; y: number; z: number; rotY: number; w: number; h: number; d: number };
    const poses = {
      plinth: [] as DetailPose[],
      eaves: [] as DetailPose[],
      ridge: [] as DetailPose[],
      door: [] as DetailPose[],
      doorJamb: [] as DetailPose[],
      doorLintel: [] as DetailPose[],
      windowFrame: [] as DetailPose[],
      windowGlass: [] as DetailPose[],
      windowMullion: [] as DetailPose[],
    };
    const addPose = (
      list: DetailPose[],
      b: { x: number; z: number; w: number; d: number; rotY: number },
      lx: number, y: number, lz: number, w: number, h: number, d: number,
    ) => {
      const c = Math.cos(b.rotY);
      const s = Math.sin(b.rotY);
      list.push({
        x: b.x + lx * c + lz * s,
        y,
        z: b.z - lx * s + lz * c,
        rotY: b.rotY,
        w, h, d,
      });
    };
    for (const b of BUILDINGS_1825) {
      /* kamnit podzidek, rahlo izven tlorisa */
      addPose(poses.plinth, b, 0, 0.13, 0, b.w + 0.34, 0.26, b.d + 0.34);
      /* leseni kapni robovi in slemenska letev — geometrija je orientacijska */
      for (const side of [-1, 1]) {
        addPose(poses.eaves, b, side * (b.w / 2), b.wallH + 0.02, 0, 0.13, 0.13, b.d + 0.18);
      }
      addPose(poses.ridge, b, 0, b.wallH + b.roofH - 0.035, 0, 0.09, 0.09, b.d + 0.14);

      if (b.w < 4.8 || b.d < 3.2) continue;
      const isBarn = b.w > 18;
      const doorW = Math.min(isBarn ? 2.1 : 1.02, b.w * (isBarn ? 0.19 : 0.17));
      const doorH = Math.min(isBarn ? 2.35 : 2.02, b.wallH * 0.78);
      const doorX = b.w > 9 ? -b.w * 0.18 : 0;
      /* glavna vrata na južni/čelni strani; lokacija in oblika sta tipološka ocena */
      addPose(poses.door, b, doorX, doorH / 2, -b.d / 2 - 0.075, doorW, doorH, 0.075);
      addPose(poses.doorJamb, b, doorX - doorW / 2 - 0.055, doorH / 2, -b.d / 2 - 0.105, 0.11, doorH + 0.12, 0.12);
      addPose(poses.doorJamb, b, doorX + doorW / 2 + 0.055, doorH / 2, -b.d / 2 - 0.105, 0.11, doorH + 0.12, 0.12);
      addPose(poses.doorLintel, b, doorX, doorH + 0.06, -b.d / 2 - 0.105, doorW + 0.22, 0.12, 0.12);

      /* okna dodamo samo bolj verjetnim stanovanjskim objektom v jedru;
         ne trdimo, da so ti posamezni odprtini zgodovinsko dokazani. */
      if (b.core && b.w >= 6 && b.w <= 18 && b.d >= 4) {
        const positions = b.w > 10
          ? [-b.w * 0.23, b.w * 0.23]
          : [doorX < 0 ? b.w * 0.23 : -b.w * 0.23];
        for (const face of [-1, 1]) {
          for (const wx of positions) {
            const ww = Math.min(0.72, b.w * 0.11);
            const wh = 0.72;
            const wy = Math.min(1.7, b.wallH * 0.64);
            const surface = face * (b.d / 2);
            addPose(poses.windowFrame, b, wx, wy, surface + face * 0.062, ww + 0.16, wh + 0.16, 0.09);
            addPose(poses.windowGlass, b, wx, wy, surface + face * 0.12, ww, wh, 0.055);
            addPose(poses.windowMullion, b, wx, wy, surface + face * 0.155, 0.045, wh, 0.035);
            addPose(poses.windowMullion, b, wx, wy, surface + face * 0.156, ww, 0.045, 0.035);
          }
        }
      }
    }

    const detailBox = new THREE.BoxGeometry(1, 1, 1);
    const makeDetailMesh = (items: DetailPose[], material: THREE.Material) => {
      if (!items.length) return;
      const mesh = new THREE.InstancedMesh(detailBox, material, items.length);
      items.forEach((b, i) => {
        const qDetail = new THREE.Quaternion().setFromAxisAngle(yAxis, b.rotY);
        const pDetail = new THREE.Vector3(b.x, b.y, b.z);
        const sDetail = new THREE.Vector3(b.w, b.h, b.d);
        mesh.setMatrixAt(i, new THREE.Matrix4().compose(pDetail, qDetail, sDetail));
      });
      mesh.instanceMatrix.needsUpdate = true;
      mesh.frustumCulled = false;
      this.facadeGroup.add(mesh);
      this.facadeMaterials.push(material);
    };
    const detailMaterial = (color: number) => new THREE.MeshStandardMaterial({
      color,
      roughness: 0.9,
      transparent: true,
      opacity: 1,
      depthWrite: false,
    });
    makeDetailMesh(poses.plinth, detailMaterial(0x746858));
    makeDetailMesh(poses.eaves, detailMaterial(0x5e462e));
    makeDetailMesh(poses.ridge, detailMaterial(0x735638));
    makeDetailMesh(poses.door, detailMaterial(0x65452d));
    makeDetailMesh(poses.doorJamb, detailMaterial(0xb39b73));
    makeDetailMesh(poses.doorLintel, detailMaterial(0x9b8058));
    makeDetailMesh(poses.windowFrame, detailMaterial(0xb39b73));
    makeDetailMesh(poses.windowGlass, detailMaterial(0x35443f));
    makeDetailMesh(poses.windowMullion, detailMaterial(0x60472f));
    this.facadeGroup.visible = true;

    this.scene.add(this.walls1825, this.roofs1825, this.wallsGrowth, this.roofsGrowth, this.facadeGroup);

    /* statusne barve duhov 1825 (Kaj je izginilo?) — instanceColor se
       MNOŽI z barvo materiala, zato v režimu 1825/1900 vsem bela (brez spremembe)
       in v režimu »danes« razmerje ciljna/materialna. */
    this.applyPresenceColors(false);

    /* cerkev sv. Vida — muzejski GLB na dokumentirani lokaciji */
    new GLTFLoader().load(
      "/models/cerkev-sv-vida.glb",
      (g) => {
        if (this.disposed) return;
        const root = new THREE.Group();
        root.add(g.scene);
        const bb = new THREE.Box3().setFromObject(g.scene);
        const h = Math.max(0.5, bb.max.y - bb.min.y);
        const s = CHURCH.targetH / h;
        g.scene.scale.setScalar(s);
        g.scene.position.set(-bb.min.x * s, -bb.min.y * s, -bb.min.z * s);
        root.position.set(CHURCH.x, 0, CHURCH.z);
        this.churchRoot = root;
        this.scene.add(root);
      },
      undefined,
      () => undefined, /* GLB ne uspe → jedro ostane brez cerkve, ni kritično */
    );

    /* velikost + zanka */
    this.ro = new ResizeObserver(() => this.resize());
    this.ro.observe(canvas.parentElement ?? canvas);
    this.resize();

    if (opts.mode === "orbit") this.enableOrbit();
    this.attachPointer();
    this.loop();
  }

  /* ── javni API ── */

  setMode(mode: SceneMode) {
    if (mode === this.mode) return;
    this.mode = mode;
    if (mode === "orbit") {
      this.enableOrbit();
    } else if (this.controls) {
      this.controls.dispose();
      this.controls = null;
    }
    this.groundPlane.visible = mode === "orbit";
    this.resize();
  }

  setYear(year: SceneYear) {
    this.year = year;
    this.mini?.handle.setYear(year);
  }

  /** mini-scena oddaljene točke (issue #12): lastna proceduralna vsebina
      namesto vasi, ki je tu 2–10 km stran. anchor = koordinata točke. */
  setMiniScene(
    id: MiniSceneId | null,
    anchor?: { lat: number; lng: number } | null,
  ) {
    if (this.mini) {
      this.scene.remove(this.mini.handle.group);
      this.mini.handle.dispose();
      this.mini = null;
    }
    if (!id || !anchor) {
      /* nazaj na vas: vrni vse plasti (orbit/tla glede na način) */
      this.walls1825.visible = true;
      this.roofs1825.visible = true;
      this.facadeGroup.visible = true;
      this.envGroup.visible = true;
      this.groundPlane.visible = this.mode === "orbit";
      this.smokeGroup.visible = this.year !== 2026;
      if (this.churchRoot) this.churchRoot.visible = true;
      /* growth/present vidnost v naslednjem frame povrne zanka */
      this.wallsGrowth.visible = this.vis.growthOpacity > 0.05;
      this.roofsGrowth.visible = this.vis.growthOpacity > 0.05;
      this.wallsPresent.visible = this.vis.presentOpacity > 0.04;
      return;
    }
    const handle = buildMiniScene(id);
    const { x, z } = toLocal(anchor.lat, anchor.lng);
    handle.group.position.set(x, 0, z);
    handle.setYear(this.year);
    this.scene.add(handle.group);
    this.mini = { id, handle, center: { x, z } };
    this.miniStart = performance.now();
    /* skrij vas — predogled se usmeri na središče mini scene */
    this.walls1825.visible = false;
    this.roofs1825.visible = false;
    this.facadeGroup.visible = false;
    this.wallsGrowth.visible = false;
    this.roofsGrowth.visible = false;
    this.wallsPresent.visible = false;
    this.envGroup.visible = false;
    this.groundPlane.visible = false;
    this.smokeGroup.visible = false;
    if (this.churchRoot) this.churchRoot.visible = false;
  }

  /** orbit: vrnitev na začetni pogled */
  resetView() {
    if (this.mode !== "orbit") return;
    /* P12: pogled s severa — vas v ospredju, Kolpa desno, Brezov gozd za njim */
    this.camera.position.set(
      CORE_CENTER.x + 85,
      330,
      CORE_CENTER.z - 880,
    );
    if (this.controls) {
      this.controls.target.set(CORE_CENTER.x, 8, CORE_CENTER.z);
      this.controls.update();
    }
  }

  setFix(x: number | null, z: number | null, elev?: number) {
    if (x != null && z != null) {
      this.fix = { x, z };
      this.fixElev = elev ?? 0;
      this.hasFixEver = true;
    } else {
      this.fix = null;
      this.fixElev = 0;
    }
  }

  setCompassYaw(deg: number | null) {
    this.compassYaw = deg;
  }

  /** Historical Panorama (issue #13): skrij prizor — raf preskoči render,
      GPU miruje, dokler je aktiven 360° pogled (prizor ostane živ v spominu).
      Ob ponovnem priklicu se zanka samodejno znova zažene (brez dvojne). */
  private hidden = false;
  setHidden(h: boolean) {
    const was = this.hidden;
    this.hidden = h;
    if (!h && was && !this.disposed) {
      /* zanka je obstala med skritostjo — znova zaženi */
      cancelAnimationFrame(this.raf);
      this.raf = requestAnimationFrame(this.loop);
    }
  }

  /** vlečenje prstom po zaslonu (izpad kompasa / popravek) */
  nudgeLook(dxPx: number, dyPx: number) {
    const k = 0.12;
    this.manualYaw -= dxPx * k;
    this.manualPitch = THREE.MathUtils.clamp(
      this.manualPitch - dyPx * k * 0.6,
      -55,
      65,
    );
  }

  capture(video: HTMLVideoElement | null, cap: CaptionSpec): string | null {
    const w = Math.max(640, Math.floor(this.canvas.clientWidth));
    const h = Math.max(480, Math.floor(this.canvas.clientHeight));
    const out = document.createElement("canvas");
    out.width = w;
    out.height = h;
    const ctx = out.getContext("2d");
    if (!ctx) return null;

    /* video kot ozadje (cover) */
    if (video && video.readyState >= 2) {
      const vw = video.videoWidth, vh = video.videoHeight;
      const scale = Math.max(w / vw, h / vh);
      const dw = vw * scale, dh = vh * scale;
      ctx.drawImage(video, (w - dw) / 2, (h - dh) / 2, dw, dh);
    } else {
      ctx.fillStyle = "#101610";
      ctx.fillRect(0, 0, w, h);
    }

    /* 3D plast — render v istem tiku, da je buffer veljaven */
    this.renderer.render(this.scene, this.camera);
    ctx.drawImage(this.renderer.domElement, 0, 0, w, h);

    /* napisnica */
    const barH = Math.round(h * 0.115);
    const grad = ctx.createLinearGradient(0, h - barH * 1.6, 0, h);
    grad.addColorStop(0, "rgba(8,12,9,0)");
    grad.addColorStop(0.35, "rgba(8,12,9,0.82)");
    grad.addColorStop(1, "rgba(8,12,9,0.95)");
    ctx.fillStyle = grad;
    ctx.fillRect(0, h - barH * 1.6, w, barH * 1.6);
    ctx.textBaseline = "alphabetic";
    ctx.fillStyle = "#f2eee6";
    ctx.font = `600 ${Math.round(h * 0.034)}px Georgia, 'Times New Roman', serif`;
    ctx.fillText(cap.title, Math.round(w * 0.04), h - barH);
    ctx.fillStyle = "rgba(242,238,230,0.85)";
    ctx.font = `${Math.round(h * 0.022)}px Georgia, serif`;
    ctx.fillText(cap.sub, Math.round(w * 0.04), h - barH * 0.55);
    ctx.fillStyle = "rgba(242,238,230,0.6)";
    ctx.font = `${Math.round(h * 0.02)}px Georgia, serif`;
    ctx.fillText(cap.credit, Math.round(w * 0.04), h - barH * 0.18);

    try {
      return out.toDataURL("image/png");
    } catch {
      return null;
    }
  }

  dispose() {
    this.disposed = true;
    cancelAnimationFrame(this.raf);
    this.ro.disconnect();
    this.controls?.dispose();
    this.removePointer();
    if (this.mini) {
      this.scene.remove(this.mini.handle.group);
      this.mini.handle.dispose();
      this.mini = null;
    }
    this.smokeTex?.dispose();
    for (const s of this.smokeSprites) {
      (s.spr.material as THREE.SpriteMaterial).dispose();
    }
    const disposedTextures = new Set<THREE.Texture>();
    const disposeMaterial = (material: THREE.Material) => {
      const map = (material as THREE.Material & { map?: THREE.Texture }).map;
      if (map && !disposedTextures.has(map)) {
        map.dispose();
        disposedTextures.add(map);
      }
      material.dispose();
    };
    this.scene.traverse((o) => {
      const any = o as unknown as {
        geometry?: THREE.BufferGeometry;
        material?: THREE.Material | THREE.Material[];
      };
      any.geometry?.dispose?.();
      const m = any.material;
      if (Array.isArray(m)) m.forEach(disposeMaterial);
      else if (m) disposeMaterial(m);
    });
    this.renderer.dispose();
  }

  /* ── notranje ── */

  /** barve duhov 1825 po statusu (Kaj je izginilo?) — ghost=true v »danes« */
  private applyPresenceColors(ghost: boolean) {
    /* material color is white now because the plaster tint comes from its texture. */
    const base = new THREE.Color(0xffffff);
    const c = new THREE.Color();
    for (let i = 0; i < BUILDINGS_1825.length; i++) {
      if (ghost) {
        const target = PRESENCE_COLORS[BUILDING_STATUS[i] ?? "uncertain"];
        c.setRGB(target.r / base.r, target.g / base.g, target.b / base.b);
      } else {
        c.setRGB(1, 1, 1);
      }
      this.walls1825.setColorAt(i, c);
    }
    if (this.walls1825.instanceColor) {
      this.walls1825.instanceColor.needsUpdate = true;
    }
  }

  private enableOrbit() {
    this.controls = new OrbitControls(this.camera, this.canvas);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    /* GEOTRUTH: tarča orbita = središče vasi 1825 (ne sodobnega izhodišča) */
    this.controls.target.set(CORE_CENTER.x, 8, CORE_CENTER.z);
    this.controls.maxPolarAngle = Math.PI * 0.49;
    this.controls.minDistance = 40;
    this.controls.maxDistance = 2200;
    /* P12: pogled s severa — vas v ospredju, Kolpa desno, Brezov gozd za njim */
    this.camera.position.set(
      CORE_CENTER.x + 85,
      330,
      CORE_CENTER.z - 880,
    );
    this.camera.lookAt(this.controls.target);
  }

  private attachPointer() {
    this.canvas.addEventListener("pointerdown", this.handleDown);
    this.canvas.addEventListener("pointermove", this.handleMove);
    this.canvas.addEventListener("pointerup", this.handleUp);
  }

  private removePointer() {
    this.canvas.removeEventListener("pointerdown", this.handleDown);
    this.canvas.removeEventListener("pointermove", this.handleMove);
    this.canvas.removeEventListener("pointerup", this.handleUp);
  }

  private handleDown = (e: PointerEvent) => {
    this.pointerDown = { x: e.clientX, y: e.clientY, t: performance.now() };
    this.dragging = false;
  };

  private handleMove = (e: PointerEvent) => {
    if (!this.pointerDown) return;
    const dx = e.clientX - this.pointerDown.x;
    const dy = e.clientY - this.pointerDown.y;
    if (Math.abs(dx) + Math.abs(dy) > 6) this.dragging = true;
    if (this.mode === "ar" && this.dragging) {
      this.nudgeLook(dx, dy);
      this.pointerDown = { x: e.clientX, y: e.clientY, t: this.pointerDown.t };
    }
  };

  private handleUp = (e: PointerEvent) => {
    const pd = this.pointerDown;
    this.pointerDown = null;
    if (!pd || this.dragging) return;
    if (performance.now() - pd.t > 600) return;
    this.onPick?.(this.screenPick(e.clientX, e.clientY));
  };

  screenPick(clientX: number, clientY: number): PickResult | null {
    const r = this.canvas.getBoundingClientRect();
    const ndc = new THREE.Vector2(
      ((clientX - r.left) / r.width) * 2 - 1,
      -((clientY - r.top) / r.height) * 2 + 1,
    );
    const ray = new THREE.Raycaster();
    ray.setFromCamera(ndc, this.camera);
    const targets = [this.wallsPresent, this.walls1825, this.wallsGrowth].filter(
      (m) => m.visible,
    );
    const hits = ray.intersectObjects(targets, false);
    const hit = hits[0];
    if (!hit || hit.instanceId == null) return null;
    if (hit.object === this.wallsPresent) {
      const src = PRESENT_BUILDINGS[hit.instanceId];
      if (!src) return null;
      return {
        kind: "present",
        index: hit.instanceId,
        x: src.x,
        z: src.z,
        w: src.w,
        d: src.d,
        dist: Math.hypot(this.camera.position.x - src.x, this.camera.position.z - src.z),
      };
    }
    const isGrowth = hit.object === this.wallsGrowth;
    const src: PreparedBuilding | (typeof GROWTH_1900)[number] = isGrowth
      ? GROWTH_1900[hit.instanceId]
      : BUILDINGS_1825[hit.instanceId];
    if (!src) return null;
    return {
      kind: isGrowth ? "growth" : "1825",
      index: isGrowth ? undefined : hit.instanceId,
      presence: isGrowth ? undefined : (BUILDING_STATUS[hit.instanceId] ?? "uncertain"),
      x: src.x,
      z: src.z,
      w: src.w,
      d: src.d,
      dist: Math.hypot(
        this.camera.position.x - src.x,
        this.camera.position.z - src.z,
      ),
    };
  }

  private resize() {
    const parent = this.canvas.parentElement;
    const w = parent?.clientWidth || this.canvas.clientWidth || 640;
    const h = parent?.clientHeight || this.canvas.clientHeight || 480;
    this.renderer.setSize(w, h, false);
    this.camera.aspect = w / Math.max(1, h);
    this.camera.updateProjectionMatrix();
  }

  private loop = () => {
    if (this.disposed || this.hidden) return;
    this.raf = requestAnimationFrame(this.loop);

    /* mini-scena (issue #12): lastna vsebina, vas skrita */
    if (this.mini) {
      this.mini.handle.tick((performance.now() - this.miniStart) / 1000);
      if (this.mode === "ar") {
        if (this.fix) {
          /* na lokaciji: kamera na GPS, kompas obrača pogled */
          const yawTarget = (this.compassYaw ?? 0) + this.manualYaw;
          const pitchTarget = this.manualPitch;
          this.curYaw += (yawTarget - this.curYaw) * 0.15;
          this.curPitch += (pitchTarget - this.curPitch) * 0.15;
          this.curX += (this.fix.x - this.curX) * 0.2;
          this.curZ += (this.fix.z - this.curZ) * 0.2;
          this.camera.position.set(this.curX, EYE_H, this.curZ);
          this.camera.rotation.set(
            THREE.MathUtils.degToRad(this.curPitch),
            THREE.MathUtils.degToRad(-this.curYaw),
            0,
          );
        } else if (!this.hasFixEver) {
          /* predogled brez GPS: kamera počasi kroži okoli središča scene
             in gleda vanj — prizor je VEDNO viden (vlečenje zamika krog) */
          const t = (performance.now() - this.miniStart) / 1000;
          const a = t * 0.12 + THREE.MathUtils.degToRad(this.manualYaw);
          const R = 36;
          this.curX = this.mini.center.x + Math.sin(a) * R;
          this.curZ = this.mini.center.z + Math.cos(a) * R;
          this.camera.position.set(this.curX, EYE_H + 2.5, this.curZ);
          this.camera.lookAt(this.mini.center.x, 2.2, this.mini.center.z);
        }
      }
      this.renderer.render(this.scene, this.camera);
      return;
    }

    /* preklop letnice: mehko bližanje ciljnim vrednostim */
    const tv = YEAR_VISUALS[this.year];
    this.vis.wallsOpacity += (tv.wallsOpacity - this.vis.wallsOpacity) * 0.09;
    this.vis.roofsOpacity += (tv.roofsOpacity - this.vis.roofsOpacity) * 0.09;
    this.vis.growthOpacity += (tv.growthOpacity - this.vis.growthOpacity) * 0.09;
    /* današnje stavbe: digitalni dvojček samo v orbitu (AR kaže danes skozi kamero) */
    const presentTarget =
      tv.showPresent && this.mode === "orbit" ? tv.presentOpacity : 0;
    this.vis.presentOpacity += (presentTarget - this.vis.presentOpacity) * 0.09;
    if (this.wallsMat.wireframe !== tv.wallsWire) {
      /* zamenjaj žični način, ko je prehod že blizu konca */
      if (Math.abs(this.vis.wallsOpacity - tv.wallsOpacity) < 0.35) {
        this.wallsMat.wireframe = tv.wallsWire;
        /* ob preklopu v/a iz duhov prebarvaj stavbe po statusu */
        this.applyPresenceColors(tv.wallsWire);
      }
    }
    this.wallsMat.opacity = this.vis.wallsOpacity;
    this.roofsMat.opacity = this.vis.roofsOpacity;
    this.growthWallsMat.opacity = this.vis.growthOpacity;
    this.growthRoofsMat.opacity = this.vis.growthOpacity;
    this.presentMat.opacity = this.vis.presentOpacity;
    const detailOpacity = this.wallsMat.wireframe ? 0 : this.vis.wallsOpacity;
    for (const material of this.facadeMaterials) {
      (material as THREE.Material & { opacity: number }).opacity = detailOpacity;
    }
    this.facadeGroup.visible = detailOpacity > 0.015;
    const showGrowth = this.vis.growthOpacity > 0.05;
    this.wallsGrowth.visible = showGrowth;
    this.roofsGrowth.visible = showGrowth;
    this.wallsPresent.visible = this.vis.presentOpacity > 0.04;

    /* ── P12: dim iz dimnikov — veda živosti vasi (1825/~1900) ── */
    this.smokeGroup.visible = this.year !== 2026;
    if (this.smokeGroup.visible) {
      const now = performance.now() / 1000;
      for (const s of this.smokeSprites) {
        const cyc = 6.5; /* sekund na oblak */
        const t = (now + s.phase) % cyc / cyc; /* 0→1 */
        const rise = 7 + t * 6; /* dvig nad dimnik */
        const sway = Math.sin(t * 5 + s.phase) * (0.4 + t * 1.6);
        const sc = 1.2 + t * 4.2;
        s.spr.position.set(s.x + sway, s.top + rise, s.z + sway * 0.6);
        s.spr.scale.set(sc, sc, 1);
        const fade = Math.sin(Math.PI * t); /* mehak vstop/izstop */
        (s.spr.material as THREE.SpriteMaterial).opacity = 0.42 * fade;
      }
    }

    if (this.mode === "orbit") {
      this.controls?.update();
    } else {
      /* AR: kamera na GPS (+ izravnava kompasa) */
      const yawTarget =
        (this.compassYaw ?? 0) + this.manualYaw;
      const pitchTarget = this.manualPitch;
      this.curYaw += (yawTarget - this.curYaw) * 0.15;
      this.curPitch += (pitchTarget - this.curPitch) * 0.15;
      /* predogled brez GPS: kroži nad jedrom vasi 1825 (GEOTRUTH center) */
      let px = CORE_CENTER.x + 300;
      let pz = CORE_CENTER.z + 340;
      if (this.fix) {
        px = this.fix.x;
        pz = this.fix.z;
      } else if (!this.hasFixEver) {
        /* predogled: počasi kroži okoli jedra */
        this.curYaw += 0.05;
      }
      this.curX += (px - this.curX) * 0.25;
      this.curZ += (pz - this.curZ) * 0.25;
      this.camera.position.set(this.curX, EYE_H + this.fixElev, this.curZ);
      this.camera.rotation.set(
        THREE.MathUtils.degToRad(this.curPitch),
        THREE.MathUtils.degToRad(-this.curYaw),
        0,
      );
    }

    this.renderer.render(this.scene, this.camera);
  };
}
