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
  PRESENT_BUILDINGS,
  BUILDING_STATUS,
  type PreparedBuilding,
  type BuildingPresence,
} from "@/lib/village3d";

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
  private wallsMat: THREE.MeshLambertMaterial;
  private roofsMat: THREE.MeshLambertMaterial;
  private growthWallsMat: THREE.MeshLambertMaterial;
  private growthRoofsMat: THREE.MeshLambertMaterial;
  private presentMat: THREE.MeshLambertMaterial;
  private groundPlane: THREE.Mesh;
  private churchRoot: THREE.Group | null = null;

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

    this.renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
    });
    this.renderer.setClearColor(0x000000, 0);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

    this.camera = new THREE.PerspectiveCamera(62, 1, 0.4, 4000);
    this.camera.rotation.order = "YXZ";

    /* svetloba: topla podvečerna sončna */
    const hemi = new THREE.HemisphereLight(0xf4ead2, 0x9a8a6a, 1.05);
    this.scene.add(hemi);
    const sun = new THREE.DirectionalLight(0xffe6bd, 1.15);
    sun.position.set(280, 420, -160);
    this.scene.add(sun);

    /* tla — v AR prosojna (video se vidi), v orbitu polna */
    this.groundPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(3200, 3200),
      new THREE.MeshLambertMaterial({ color: 0xb3a787 }),
    );
    this.groundPlane.rotation.x = -Math.PI / 2;
    this.groundPlane.position.y = -0.06;
    this.groundPlane.visible = opts.mode === "orbit";
    this.scene.add(this.groundPlane);

    /* cone rabe tal (RECONSTRUCTED) */
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
      this.scene.add(m);
    }

    /* Kolpa — georeferencirana struga */
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
    this.scene.add(kolpa);

    /* stavbe — instancirane */
    const box = new THREE.BoxGeometry(1, 1, 1);
    box.translate(0, 0.5, 0);
    const gable = gableGeometry();

    this.wallsMat = new THREE.MeshLambertMaterial({
      color: 0xd8cdb8,
      transparent: true,
      opacity: 1,
    });
    this.roofsMat = new THREE.MeshLambertMaterial({
      color: 0x8a7040,
      transparent: true,
      opacity: 1,
    });
    this.growthWallsMat = new THREE.MeshLambertMaterial({
      color: 0xc2b08c,
      transparent: true,
      opacity: 0,
    });
    this.growthRoofsMat = new THREE.MeshLambertMaterial({
      color: 0x9a7a4a,
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
    this.scene.add(this.walls1825, this.roofs1825, this.wallsGrowth, this.roofsGrowth);

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
  }

  /** orbit: vrnitev na začetni pogled */
  resetView() {
    if (this.mode !== "orbit") return;
    this.camera.position.set(430, 400, 560);
    if (this.controls) {
      this.controls.target.set(0, 8, 0);
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
    this.scene.traverse((o) => {
      const any = o as unknown as {
        geometry?: THREE.BufferGeometry;
        material?: THREE.Material | THREE.Material[];
      };
      any.geometry?.dispose?.();
      const m = any.material;
      if (Array.isArray(m)) m.forEach((x) => x.dispose());
      else m?.dispose?.();
    });
    this.renderer.dispose();
  }

  /* ── notranje ── */

  /** barve duhov 1825 po statusu (Kaj je izginilo?) — ghost=true v »danes« */
  private applyPresenceColors(ghost: boolean) {
    const base = new THREE.Color(0xd8cdb8);
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
    this.controls.target.set(0, 8, 0);
    this.controls.maxPolarAngle = Math.PI * 0.49;
    this.controls.minDistance = 40;
    this.controls.maxDistance = 2200;
    this.camera.position.set(430, 400, 560);
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
    if (this.disposed) return;
    this.raf = requestAnimationFrame(this.loop);

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
    const showGrowth = this.vis.growthOpacity > 0.05;
    this.wallsGrowth.visible = showGrowth;
    this.roofsGrowth.visible = showGrowth;
    this.wallsPresent.visible = this.vis.presentOpacity > 0.04;

    if (this.mode === "orbit") {
      this.controls?.update();
    } else {
      /* AR: kamera na GPS (+ izravnava kompasa) */
      const yawTarget =
        (this.compassYaw ?? 0) + this.manualYaw;
      const pitchTarget = this.manualPitch;
      this.curYaw += (yawTarget - this.curYaw) * 0.15;
      this.curPitch += (pitchTarget - this.curPitch) * 0.15;
      let px = 300;
      let pz = 340;
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
