"use client";

/**
 * MINI-SCENES (issue #12, P1) — proceduralne scene oddaljenih točk.
 *
 * Knossos vzorec segmentacije: oddaljene točke (mlini ~4,6 km, cerkvišče
 * ~2,2 km od vasi) ne pokažejo praznega pogleda na oddaljeno vas, ampak
 * lastno LAHKO sceno, zgrajeno iz three.js primitivov (brez datotek —
 * ničesar se ne nalaga po omrežju, velikost ≈ 0 MB):
 *
 *  · mlini     — vodni mlin ob Kolpi: hiša z dvokapnico, kolesnica z
 *               lopaticami (se vrti), jez, toča, reka, drevesa. V letu
 *               »danes« mlin postane duh (jantorno žični) in kolo miruje —
 *               »Kaj je izginilo« ista slovnična znamenja kot pri hišah.
 *               INTERPRETACIJA vrste (žimaln), ne konkretnega mlina.
 *  · cerkvišče — tri cerkvice, ki jih ni več (Turki ~1408): trije rdeči
 *               duhovi (utripajo) + trdna bela kapelica 1994 — edini kamen,
 *               ki danes nosi spomin. Postavitev cerkvic je INTERPRETACIJA
 *               (za dve legi domnevno znani, tretja neznana).
 *
 * Vsa merila so pohlevna (hiša mlina ~4 m, cerkvica ~5 m z zvonikom,
 * kapelica ~2,3 m) in dokumentirana v ASSET_ORIENTATIONS (procedural:*).
 */

import * as THREE from "three";

export type MiniSceneId = "mlini" | "cerkvisce";

export interface MiniSceneHandle {
  group: THREE.Group;
  /** animacija na vsak frame (t = sekunde od zagona) */
  tick: (t: number) => void;
  /** leto: mlini — 2026 = duh (kolo miruje); cerkvišče — brez spremembe */
  setYear: (year: 1825 | 1900 | 2026) => void;
  dispose: () => void;
}

/* ── skupna geometrija dvokapnice (baza y=0, enotska) ── */
function gableGeometry(): THREE.BufferGeometry {
  const A = [-0.5, 0, -0.5], B = [0.5, 0, -0.5], C = [0.5, 0, 0.5],
    D = [-0.5, 0, 0.5], E = [0, 1, -0.5], F = [0, 1, 0.5];
  const tris = [
    A, E, B, D, C, F,
    B, E, F, B, F, C,
    A, D, F, A, F, E,
  ];
  const pos = new Float32Array(tris.length * 3);
  tris.forEach((v, i) => pos.set(v as number[], i * 3));
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  g.computeVertexNormals();
  return g;
}

/* ── trak vode/poti skozi točke, širina w ── */
function ribbonGeometry(
  pts: { x: number; z: number }[],
  w: number,
  y: number,
): THREE.BufferGeometry {
  const verts: number[] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p = pts[i], q = pts[i + 1];
    const dx = q.x - p.x, dz = q.z - p.z;
    const len = Math.hypot(dx, dz) || 1;
    const nx = (-dz / len) * (w / 2), nz = (dx / len) * (w / 2);
    verts.push(
      p.x + nx, y, p.z + nz, p.x - nx, y, p.z - nz, q.x + nx, y, q.z + nz,
      q.x + nx, y, q.z + nz, p.x - nx, y, p.z - nz, q.x - nx, y, q.z - nz,
    );
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(verts, 3));
  g.computeVertexNormals();
  return g;
}

/* ── drevo (deblna + krošnja) ── */
function tree(x: number, z: number, s = 1): THREE.Group {
  const g = new THREE.Group();
  const trunk = new THREE.Mesh(
    new THREE.CylinderGeometry(0.14 * s, 0.2 * s, 1.5 * s, 6),
    new THREE.MeshLambertMaterial({ color: 0x5a4530 }),
  );
  trunk.position.y = 0.75 * s;
  const crown = new THREE.Mesh(
    new THREE.SphereGeometry(1.25 * s, 10, 8),
    new THREE.MeshLambertMaterial({ color: 0x4a6741 }),
  );
  crown.position.y = 2.1 * s;
  crown.scale.y = 1.15;
  g.add(trunk, crown);
  g.position.set(x, 0, z);
  return g;
}

/* ── križ (na zvonik/kapelico) ── */
function cross(h: number): THREE.Group {
  const g = new THREE.Group();
  const mat = new THREE.MeshLambertMaterial({ color: 0x4f4a42 });
  const v = new THREE.Mesh(new THREE.BoxGeometry(0.06, h, 0.06), mat);
  v.position.y = h / 2;
  const arm = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.06, 0.06), mat);
  arm.position.y = h * 0.72;
  g.add(v, arm);
  return g;
}

/* ════════════════════════════════════════════════════════════════════════
 *  MLINI — proceduralna scena vodnega mlina (INTERPRETACIJA vrste)
 * ════════════════════════════════════════════════════════════════════════ */

function buildMillScene(): MiniSceneHandle {
  const group = new THREE.Group();
  const disposables: (THREE.BufferGeometry | THREE.Material)[] = [];
  const track = <T extends THREE.BufferGeometry | THREE.Material>(x: T): T => {
    disposables.push(x);
    return x;
  };

  /* Kolpa — rečni trak vzdolž x (z ≈ −12), širina 20 m */
  const river = new THREE.Mesh(
    track(ribbonGeometry(
      [{ x: -60, z: -12 }, { x: -20, z: -11 }, { x: 20, z: -13 }, { x: 60, z: -12 }],
      20, 0.1,
    )),
    track(new THREE.MeshBasicMaterial({
      color: 0x6f9ec4, transparent: true, opacity: 0.8,
      depthWrite: false, side: THREE.DoubleSide,
    })),
  );
  group.add(river);

  /* jez — kamnita pregrada čez reko (Krajinski park Kolpa: kamnita pregrada) */
  const weirMat = track(new THREE.MeshLambertMaterial({ color: 0x8d8880 }));
  const weir = new THREE.Mesh(track(new THREE.BoxGeometry(26, 1.3, 2.6)), weirMat);
  weir.position.set(0, 0.35, -12);
  group.add(weir);

  /* toča (mlinski kanal) — od jeza pod mlin, širina 3 m */
  const stream = new THREE.Mesh(
    track(ribbonGeometry(
      [{ x: 2, z: -11 }, { x: 2, z: 0 }, { x: 2, z: 8 }, { x: 2.5, z: 16 }],
      3, 0.14,
    )),
    track(new THREE.MeshBasicMaterial({
      color: 0x7dabc8, transparent: true, opacity: 0.75,
      depthWrite: false, side: THREE.DoubleSide,
    })),
  );
  group.add(stream);

  /* mlinjska hiša — 7 × 5,5 m, zid 2,8 m, dvokapnica; stoji OB toči */
  const wallMat = track(new THREE.MeshLambertMaterial({
    color: 0x7a5c3a, transparent: true, opacity: 1,
  }));
  const roofMat = track(new THREE.MeshLambertMaterial({
    color: 0x4f3b26, transparent: true, opacity: 1,
  }));
  const walls = new THREE.Mesh(track(new THREE.BoxGeometry(7, 2.8, 5.5)), wallMat);
  walls.position.set(2, 1.4, 7.5);
  const gable = track(gableGeometry());
  const roof = new THREE.Mesh(gable, roofMat);
  roof.position.set(2, 2.8, 7.5);
  roof.scale.set(7, 2, 5.5);
  group.add(walls, roof);

  /* okno — topla luč: mlinar je doma (emisivna ploskev na južni steni) */
  const windowMat = track(new THREE.MeshBasicMaterial({ color: 0xffc66e }));
  const win = new THREE.Mesh(track(new THREE.PlaneGeometry(0.9, 0.9)), windowMat);
  win.position.set(2, 1.7, 10.26);
  group.add(win);

  /* kolesnica z lopaticami — v verticalni ravnini, os vzdolž x,
     na severni čelni steni (kjer voda pride iz toče) */
  const wheelGroup = new THREE.Group();
  wheelGroup.position.set(2, 1.55, 4.6);
  const woodMat = track(new THREE.MeshLambertMaterial({
    color: 0x5d452c, transparent: true, opacity: 1,
  }));
  const torusGeo = track(new THREE.TorusGeometry(1.5, 0.09, 8, 26));
  for (const off of [-0.3, 0.3]) {
    const ring = new THREE.Mesh(torusGeo, woodMat);
    ring.rotation.y = Math.PI / 2;
    ring.position.x = off;
    wheelGroup.add(ring);
  }
  /* hub + ray (š4) + 12 lopatic */
  const hubGeo = track(new THREE.CylinderGeometry(0.22, 0.22, 0.85, 8));
  const hub = new THREE.Mesh(hubGeo, woodMat);
  hub.rotation.z = Math.PI / 2;
  wheelGroup.add(hub);
  const spokeGeo = track(new THREE.BoxGeometry(0.1, 2.9, 0.12));
  for (let i = 0; i < 4; i++) {
    const sp = new THREE.Mesh(spokeGeo, woodMat);
    sp.rotation.x = (i * Math.PI) / 4;
    wheelGroup.add(sp);
  }
  const paddleGeo = track(new THREE.BoxGeometry(0.62, 0.5, 0.08));
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2;
    const p = new THREE.Mesh(paddleGeo, woodMat);
    p.position.set(0, Math.sin(a) * 1.72, Math.cos(a) * 1.72);
    p.rotation.x = -a;
    wheelGroup.add(p);
  }
  group.add(wheelGroup);

  /* drevesa ob reki — določena, ne naključna */
  for (const [tx, tz, s] of [
    [-14, 2, 1], [-9, -3, 1.2], [10, 1, 0.9], [13, -2, 1.1],
    [-20, 4, 1.3], [18, 5, 1], [7, 14, 1.2], [-4, 15, 0.9],
  ] as const) {
    group.add(tree(tx, tz, s));
  }

  /* stanje leta: 2026 = duh (kolo miruje, jantorna žica) */
  let year: 1825 | 1900 | 2026 = 1825;
  const solidMats = [wallMat, roofMat, woodMat];

  return {
    group,
    tick: (t: number) => {
      /* kolo se vrti (~0,7 rad/s), dokler mlin živi; v »danes« miruje */
      if (year !== 2026) wheelGroup.rotation.x = t * 0.7;
      /* voda rahlo utripa — življenje reke */
      (river.material as THREE.MeshBasicMaterial).opacity =
        0.75 + Math.sin(t * 0.8) * 0.05;
    },
    setYear: (y: 1825 | 1900 | 2026) => {
      year = y;
      const ghost = y === 2026;
      for (const m of solidMats) {
        m.wireframe = ghost;
        m.opacity = ghost ? 0.42 : 1;
        if (ghost) m.color.setHex(0xe0a63a);
        else if (m === wallMat) m.color.setHex(0x7a5c3a);
        else if (m === roofMat) m.color.setHex(0x4f3b26);
        else m.color.setHex(0x5d452c);
      }
      if (ghost) wheelGroup.rotation.x = 0;
      win.visible = !ghost;
    },
    dispose: () => {
      for (const d of disposables) d.dispose();
    },
  };
}

/* ════════════════════════════════════════════════════════════════════════
 *  CERKVIŠČE — trije duhovi cerkvic + kapelica 1994
 * ════════════════════════════════════════════════════════════════════════ */

function churchGhost(): { group: THREE.Group; mat: THREE.MeshLambertMaterial } {
  const group = new THREE.Group();
  const mat = new THREE.MeshLambertMaterial({
    color: 0xe06a5a, /* opečno rdeča — »ni je več« (ista kot hiše 1825) */
    transparent: true,
    opacity: 0.4,
    wireframe: true,
  });
  /* ladja 4,2 × 7 m, zid 2,7 m + dvokapnica */
  const walls = new THREE.Mesh(new THREE.BoxGeometry(4.2, 2.7, 7), mat);
  walls.position.y = 1.35;
  const roof = new THREE.Mesh(gableGeometry(), mat);
  roof.position.y = 2.7;
  roof.scale.set(4.2, 1.9, 7);
  /* zvonik na čelu: 2 × 2 m, do 4,6 m + piramida + križ */
  const tower = new THREE.Mesh(new THREE.BoxGeometry(2, 1.9, 2), mat);
  tower.position.set(0, 3.65, -2.5);
  const pyr = new THREE.Mesh(new THREE.ConeGeometry(1.55, 1.2, 4), mat);
  pyr.position.set(0, 5.2, -2.5);
  pyr.rotation.y = Math.PI / 4;
  const cr = cross(1.1);
  cr.position.set(0, 5.8, -2.5);
  group.add(walls, roof, tower, pyr, cr);
  return { group, mat };
}

function buildCerkvisceScene(): MiniSceneHandle {
  const group = new THREE.Group();
  const ghosts: { g: THREE.Group; mat: THREE.MeshLambertMaterial; phase: number }[] = [];

  /* tri cerkvice — postavitev INTERPRETACIJA (razsežni trikotnik ~60 m) */
  const placements: { x: number; z: number; rot: number; phase: number }[] = [
    { x: -34, z: -18, rot: 0.35, phase: 0 },
    { x: 28, z: -30, rot: -0.5, phase: 2.1 },
    { x: -4, z: 26, rot: 0.1, phase: 4.2 },
  ];
  for (const p of placements) {
    const { group: cg, mat } = churchGhost();
    cg.position.set(p.x, 0, p.z);
    cg.rotation.y = p.rot;
    group.add(cg);
    ghosts.push({ g: cg, mat, phase: p.phase });
  }

  /* kapelica 1994 — trdna, bela (edini ohranjeni kamen) */
  const chapelMat = new THREE.MeshLambertMaterial({ color: 0xe8e4da });
  const chapel = new THREE.Group();
  const base = new THREE.Mesh(
    new THREE.BoxGeometry(1.9, 1.7, 1.9),
    chapelMat,
  );
  base.position.y = 0.85;
  const roof = new THREE.Mesh(
    new THREE.ConeGeometry(1.6, 0.9, 4),
    new THREE.MeshLambertMaterial({ color: 0x6b675f }),
  );
  roof.position.y = 2.15;
  roof.rotation.y = Math.PI / 4;
  const cr = cross(0.7);
  cr.position.y = 2.6;
  chapel.add(base, roof, cr);
  chapel.position.set(14, 0, -34);
  chapel.rotation.y = -0.3;
  group.add(chapel);

  /* dve drevesi ob jameh (Jelenja in Vodena jama sta v zapisu) */
  group.add(tree(-16, -2, 1.1), tree(20, -8, 0.9));

  return {
    group,
    tick: (t: number) => {
      /* duhovi utripajo — spomin diha */
      for (const gh of ghosts) {
        gh.mat.opacity = 0.3 + 0.13 * Math.sin(t * 1.3 + gh.phase);
      }
    },
    setYear: () => {
      /* cerkvišče: duhovi v VSAKEM letu — porušene so bile že pred 1825 */
    },
    dispose: () => {
      group.traverse((o) => {
        const any = o as unknown as {
          geometry?: THREE.BufferGeometry;
          material?: THREE.Material | THREE.Material[];
        };
        any.geometry?.dispose?.();
        const m = any.material;
        if (Array.isArray(m)) m.forEach((x) => x.dispose());
        else m?.dispose?.();
      });
    },
  };
}

/* ── javni gradnik ── */

export function buildMiniScene(id: MiniSceneId): MiniSceneHandle {
  return id === "mlini" ? buildMillScene() : buildCerkvisceScene();
}
