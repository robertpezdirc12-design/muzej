#!/usr/bin/env python3
"""Interpretativni 3D model cerkve sv. Vida v Gribljah (MVG-002).

Proceduralna izdelava z low-poly primitivi v trimesh-u; izvoz v GLB za
<model-viewer> na strani zapisa. Paleta sledi spletišču: kremna / terakota.
"""
import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial

# ── materiali (kremna / terakota paleta spletišča) ──────────────────────────
M_STENA = PBRMaterial(baseColorFactor=[0.949, 0.925, 0.878, 1.0], roughnessFactor=0.9, metallicFactor=0.0, name="stena")
M_STREHA = PBRMaterial(baseColorFactor=[0.659, 0.310, 0.208, 1.0], roughnessFactor=0.75, metallicFactor=0.0, name="streha")
M_TEMNO = PBRMaterial(baseColorFactor=[0.176, 0.129, 0.102, 1.0], roughnessFactor=0.6, metallicFactor=0.0, name="temno")
M_KAMEN = PBRMaterial(baseColorFactor=[0.804, 0.784, 0.733, 1.0], roughnessFactor=0.95, metallicFactor=0.0, name="kamen")
M_ZLAT = PBRMaterial(baseColorFactor=[0.871, 0.678, 0.255, 1.0], roughnessFactor=0.35, metallicFactor=0.85, name="zlati_kriz")


def box(extents, center, material):
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(center)
    m.visual.material = material
    return m


def hull(points, material):
    m = trimesh.Trimesh(vertices=np.array(points, dtype=float))
    m = m.convex_hull
    m.visual.material = material
    return m


# ── geometrija (metri, velikost vaške cerkve) ──────────────────────────────
NAVA_L, NAVA_W, NAVA_H = 15.0, 7.0, 5.0   # ladja: dolžina, širina, višina stene
STREHA_H = 3.2                              # višina dvokapne strehe
TOWER_W, TOWER_H = 4.6, 17.0                # zvonik: tloris, višina do strehe
SPIRE_H = 4.2                               # piramidna kapica
APSE_R, APSE_H = 3.3, 4.6                   # apsida: polmer, višina
N_SEG = 24                                  # segmentov loka apside

meshes = []

# tloris: središče ladje v (0,0,·); zahod (zvonik) proti -x, vzhod (apsida) proti +x
cx, cz = 0.0, 0.0

# kamnita ploščad (valjek zavrtimo iz osi Z v osi Y)
plat = trimesh.creation.cylinder(radius=12.5, height=0.5, sections=48)
plat.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
plat.apply_translation([cx, -0.25, cz])
plat.visual.material = M_KAMEN
meshes.append(plat)

# ladja
meshes.append(box([NAVA_L, NAVA_H, NAVA_W], [cx, NAVA_H / 2, cz], M_STENA))

# dvokapna streha ladje (prizma) — rahlo presega stene (napuč)
ovh = 0.45
y_eav = NAVA_H
y_ridge = NAVA_H + STREHA_H
x0, x1 = cx - NAVA_L / 2 - ovh, cx + NAVA_L / 2 + ovh
z0, z1 = cz - NAVA_W / 2 - ovh, cz + NAVA_W / 2 + ovh
roof_pts = [
    [x0, y_eav, z0], [x1, y_eav, z0],       # južno napuč
    [x0, y_eav, z1], [x1, y_eav, z1],       # severno napuč
    [x0, y_ridge, cz], [x1, y_ridge, cz],   # sleme
]
meshes.append(hull(roof_pts, M_STREHA))

# zvonik na zahodni strani
tx = cx - NAVA_L / 2 - TOWER_W / 2 + 1.2   # delno vstavljena v ladjo
meshes.append(box([TOWER_W, TOWER_H, TOWER_W], [tx, TOWER_H / 2, cz], M_STENA))

# piramidna kapica zvonika (s presekom)
sx0, sx1 = tx - TOWER_W / 2 - 0.55, tx + TOWER_W / 2 + 0.55
sz0, sz1 = cz - TOWER_W / 2 - 0.55, cz + TOWER_W / 2 + 0.55
spire_pts = [
    [sx0, TOWER_H, sz0], [sx1, TOWER_H, sz0],
    [sx0, TOWER_H, sz1], [sx1, TOWER_H, sz1],
    [tx, TOWER_H + SPIRE_H, cz],
]
meshes.append(hull(spire_pts, M_STREHA))

# križ na kapici
cym = TOWER_H + SPIRE_H
meshes.append(box([0.16, 1.5, 0.16], [tx, cym + 0.75, cz], M_ZLAT))
meshes.append(box([0.85, 0.16, 0.16], [tx, cym + 1.05, cz], M_ZLAT))

# zvonilno nadstropje: temni vložki na vseh 4 straneh
bell_y = TOWER_H - 1.9
inset = 0.04
meshes.append(box([0.3, 2.6, 1.15], [tx - TOWER_W / 2 - inset, bell_y, cz], M_TEMNO))
meshes.append(box([0.3, 2.6, 1.15], [tx + TOWER_W / 2 + inset, bell_y, cz], M_TEMNO))
meshes.append(box([1.15, 2.6, 0.3], [tx, bell_y, cz - TOWER_W / 2 - inset], M_TEMNO))
meshes.append(box([1.15, 2.6, 0.3], [tx, bell_y, cz + TOWER_W / 2 + inset], M_TEMNO))

# apsida na vzhodni strani — polvaljek (ročna triangulacija)
ax = cx + NAVA_L / 2
verts, faces = [], []
for i in range(N_SEG + 1):
    th = -np.pi / 2 + np.pi * i / N_SEG
    px, pz = ax + APSE_R * np.sin(th), cz + APSE_R * np.cos(th)
    verts.append([px, 0.0, pz])
    verts.append([px, APSE_H, pz])
for i in range(N_SEG):
    b0, b1 = 2 * i, 2 * i + 2
    faces += [[b0, b0 + 1, b1 + 1], [b0, b1 + 1, b1]]
bi = len(verts)
verts += [[ax, 0.0, cz - APSE_R], [ax, 0.0, cz + APSE_R], [ax, APSE_H, cz + APSE_R], [ax, APSE_H, cz - APSE_R]]
faces += [[bi, bi + 1, bi + 2], [bi, bi + 2, bi + 3]]
apse = trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
apse.visual.material = M_STENA
meshes.append(apse)

# streha apside — polstorž
cone_v, cone_f = [], []
apex = [ax, APSE_H + 2.6, cz]
ring = []
for i in range(N_SEG + 1):
    th = -np.pi / 2 + np.pi * i / N_SEG
    ring.append([ax + APSE_R * np.sin(th), APSE_H, cz + APSE_R * np.cos(th)])
ai = len(cone_v)
for p in ring:
    cone_v.append(p)
cone_v.append(apex)
for i in range(N_SEG):
    cone_f.append([ai + i, ai + i + 1, ai + N_SEG + 1])
bi = len(cone_v)
cone_v += [ring[0], ring[-1], apex]
cone_f += [[bi, bi + 1, bi + 2]]
cone = trimesh.Trimesh(vertices=np.array(cone_v), faces=np.array(cone_f), process=True)
cone.visual.material = M_STREHA
meshes.append(cone)

# okna ladje — ozki temni vložki (jug + sever)
for side in (-1, 1):
    for k in range(4):
        wx = cx - NAVA_L / 2 + 2.6 + k * 3.1
        meshes.append(box([1.05, 2.3, 0.22], [wx, NAVA_H / 2 + 0.65, cz + side * (NAVA_W / 2 + 0.02)], M_TEMNO))

# okno v apsidi
meshes.append(box([0.3, 1.8, 1.0], [ax + APSE_R + 0.02, APSE_H / 2 + 0.5, cz], M_TEMNO))

# glavni portal na zahodni strani zvonika + stopnice
meshes.append(box([0.3, 2.6, 1.5], [tx - TOWER_W / 2 - 0.02, 1.3, cz], M_TEMNO))
for s in range(3):
    meshes.append(box([1.3 - s * 0.35, 0.22, 2.2 - s * 0.4], [tx - TOWER_W / 2 - 0.65 - s * 0.45, 0.28 + s * 0.24, cz], M_KAMEN))

# sakristija na severni strani ladje
meshes.append(box([4.2, 3.9, 3.8], [cx + 3.4, 1.95 + 0.5, cz + NAVA_W / 2 + 1.6], M_STENA))
meshes.append(box([4.8, 0.5, 4.4], [cx + 3.4, 3.9 + 0.5 + 0.25, cz + NAVA_W / 2 + 1.6], M_STREHA))

# ── sestava scene in izvoz ──────────────────────────────────────────────────
scene = trimesh.Scene()
for i, m in enumerate(meshes):
    scene.add_geometry(m, node_name=f"del_{i:02d}")

b = scene.bounding_box.bounds
scene.apply_translation([-(b[0][0] + b[1][0]) / 2, 0.0, -(b[0][2] + b[1][2]) / 2])

out = "public/models/cerkev-sv-vida.glb"
import os
os.makedirs("public/models", exist_ok=True)
glb_data = scene.export(file_type="glb")
with open(out, "wb") as f:
    f.write(glb_data)

check = trimesh.load(out)
print(f"izvoženo: {out} ({os.path.getsize(out) / 1024:.0f} KB)")
bb = check.bounding_box.bounds
print(f"velikost modela: x={bb[1][0] - bb[0][0]:.1f}m, y={bb[1][1] - bb[0][1]:.1f}m, z={bb[1][2] - bb[0][2]:.1f}m")
print(f"geometrij: {len(check.geometry)}")
