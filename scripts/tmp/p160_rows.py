#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P160 — detekcija vrstic mrliške 04894, leto 1894 (skeni 47–51).
P159-lekcija: vladanje 1893 je BLEDO — polnoširinska detekcija FAIL (hrbet + svetel tisk),
zato POL-SIRINSKO L/R (L 0.10–0.42, R 0.60–0.88) z višjimi pragi th 0.45–0.60.
Spread = ENA tabela: L stran = stolpci 1–4 (zaporedna/mesec/vas/ime), R = 5–10.
Izhod: /tmp/p160/lines.json + diag-sNN.png + vas-kontaktne mape (vsi pisani redi)."""
from PIL import Image, ImageDraw
import numpy as np, os, json

OUT = "/tmp/p160"
os.makedirs(OUT, exist_ok=True)

SCANS = (47, 48, 49, 50, 51)
SIDES = {"L": (0.10, 0.42), "R": (0.60, 0.88)}


def find_lines(a, x0, x1, y0, y1, th, cov, gap=4):
    band = a[y0:y1, x0:x1]
    dark = (band < th).mean(axis=1)
    ys = [y for y in range(len(dark)) if dark[y] > cov]
    groups, cur = [], []
    for y in ys:
        if cur and y - cur[-1] <= gap:
            cur.append(y)
        else:
            if cur:
                groups.append(int(np.mean(cur)) + y0)
            cur = [y]
    if cur:
        groups.append(int(np.mean(cur)) + y0)
    return groups


def intervals(lines, h):
    return [(lines[i], lines[i + 1]) for i in range(len(lines) - 1)
            if int(h * 0.032) <= lines[i + 1] - lines[i] <= int(h * 0.10)]


def ink_density(a, w, y0, y1, x0f, x1f, th=0.55):
    band = a[y0 + 3:y1 - 3, int(w * x0f):int(w * x1f)]
    return float((band < th).mean())


def main():
    report = {}
    for scan in SCANS:
        im = Image.open(f"{OUT}/s{scan:02d}.jpg")
        w, h = im.size
        a = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
        rep = {"w": w, "h": h}
        for side, (xf0, xf1) in SIDES.items():
            best = None
            for th in (0.45, 0.50, 0.55, 0.60):
                lines = find_lines(a, int(w * xf0), int(w * xf1), int(h * 0.03), int(h * 0.99), th, 0.28)
                iv = intervals(lines, h)
                if best is None or len(iv) > len(best[1]):
                    best = (th, iv, lines)
                if len(iv) >= 12:
                    break
            th, iv, lines = best
            rows = []
            for (ya, yb) in iv:
                dens = ink_density(a, w, ya, yb, xf0, xf1)
                rows.append({"y0": int(ya), "y1": int(yb), "dens": round(dens, 5),
                             "pisana": dens > 0.006})
            rep[side] = {"th": th, "n": len(iv), "rows": rows}
        report[f"s{scan:02d}"] = rep
        print(f"s{scan:02d}: L={rep['L']['n']} (pisanih {sum(1 for r in rep['L']['rows'] if r['pisana'])}) "
              f"R={rep['R']['n']} (pisanih {sum(1 for r in rep['R']['rows'] if r['pisana'])}) th L={rep['L']['th']} R={rep['R']['th']}")
        # diag
        d = ImageDraw.Draw(im.convert("RGB"))
        for side in ("L", "R"):
            col = (255, 0, 0)
            for i, r in enumerate(rep[side]["rows"]):
                c = col if r["pisana"] else (0, 160, 0)
                d.line([(0 if side == "L" else int(w * 0.5), r["y0"]),
                        (int(w * 0.5) if side == "L" else w, r["y0"])], fill=c, width=4)
                d.line([(0 if side == "L" else int(w * 0.5), r["y1"]),
                        (int(w * 0.5) if side == "L" else w, r["y1"])], fill=(255, 160, 0), width=2)
                d.text((40 if side == "L" else int(w * 0.52), (r["y0"] + r["y1"]) // 2),
                       f"{side}{i}", fill=(0, 0, 255))
        im.convert("RGB").resize((w // 2, h // 2)).save(f"{OUT}/diag-s{scan:02d}.png")
    json.dump(report, open(f"{OUT}/lines.json", "w"))

    # kontaktne mape: vas-stolpec (x 0.18–0.50) vsi pisani L-redi ≥110px, 6 na list, 2.2×
    os.makedirs(f"{OUT}/vas", exist_ok=True)
    for scan in SCANS:
        rep = report[f"s{scan:02d}"]
        im = Image.open(f"{OUT}/s{scan:02d}.jpg")
        w, h = im.size
        pisan = [(i, r) for i, r in enumerate(rep["L"]["rows"])
                 if r["pisana"] and (r["y1"] - r["y0"]) >= 110]
        for k in range(0, len(pisan), 6):
            chunk = pisan[k:k + 6]
            tiles = []
            for i, r in chunk:
                y0, y1 = r["y0"], r["y1"]
                crop = im.crop((int(w * 0.18), y0, int(w * 0.50), y1))
                f = 2.2
                crop = crop.resize((int(crop.width * f), int(crop.height * f)), Image.LANCZOS)
                tile = Image.new("RGB", (crop.width + 70, crop.height), (255, 255, 220))
                tile.paste(crop, (70, 0))
                td = ImageDraw.Draw(tile)
                td.text((5, 10), f"s{scan} L{i}", fill=(0, 0, 0))
                tiles.append(tile)
            W = max(t.width for t in tiles)
            H = sum(t.height for t in tiles)
            sheet = Image.new("RGB", (W, H), (255, 255, 255))
            y = 0
            for t in tiles:
                sheet.paste(t, (0, y))
                y += t.height
            sheet.save(f"{OUT}/vas/s{scan:02d}-{k//6}.png")
    print("vas-kontaktne mape ✓")


if __name__ == "__main__":
    main()
