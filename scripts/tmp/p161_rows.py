#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P161 — detekcija vrstic mrliške 04894, leto 1895 (skeni 51–56).
P158-lekcija: POLNOŠIRINSKO (x-band 0.06–0.94) je bilo 8/9 uspešno —
P159/P160-lekcija: če fail → L/R pol-širinsko + diag-kalibracija.
Vrstice: s51-dno (1895 zap 1–9) + s52 (10–21) + s53 (22–33) + s54 (34–45)
+ s55-top (46–52; meja '— 1896. —' + restart). Izhod: /tmp/p161/lines.json."""
from PIL import Image, ImageDraw
import numpy as np, os, json

OUT = "/tmp/p161"
os.makedirs(OUT, exist_ok=True)

SCANS = (51, 52, 53, 54, 55, 56)


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


def ink(a, w, y0, y1, x0f, x1f, th=0.55):
    band = a[y0 + 3:y1 - 3, int(w * x0f):int(w * x1f)]
    return float((band < th).mean())


def main():
    report = {}
    for scan in SCANS:
        im = Image.open(f"{OUT}/s{scan:02d}.jpg")
        w, h = im.size
        a = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
        rep = {"w": w, "h": h}
        # 1) POLNOŠIRINSKO (P158-repair)
        best = None
        for th, cov in ((0.35, 0.22), (0.30, 0.18), (0.45, 0.30), (0.65, 0.28)):
            lines = find_lines(a, int(w * 0.06), int(w * 0.94), int(h * 0.03), int(h * 0.99), th, cov)
            iv = intervals(lines, h)
            if best is None or len(iv) > len(best[2]):
                best = (th, cov, iv, lines)
            if len(iv) >= 11:
                break
        rep["full"] = {"th": best[0], "cov": best[1], "n": len(best[2])}
        if len(best[2]) >= 10:
            rep["mode"] = "full"
            rep["intervals"] = best[2]
        else:
            # 2) L/R pol-širinsko (P159/P160 metoda)
            rep["mode"] = "LR"
            for name, (x0f, x1f) in (("L", (0.10, 0.42)), ("R", (0.60, 0.88))):
                bb = None
                for th in (0.45, 0.50, 0.55, 0.60):
                    lines = find_lines(a, int(w * x0f), int(w * x1f), int(h * 0.03), int(h * 0.99), th, 0.28)
                    iv = intervals(lines, h)
                    if bb is None or len(iv) > len(bb[1]):
                        bb = (th, iv, lines)
                    if len(iv) >= 12:
                        break
                rep[name] = {"th": bb[0], "n": len(bb[1]), "intervals": bb[1]}
        report[f"s{scan:02d}"] = rep
        print(f"s{scan:02d}: mode={rep['mode']} full_n={rep['full']['n']}", flush=True)
    json.dump(report, open(f"{OUT}/lines.json", "w"), indent=1)

    # diag-PNG: črte + intervali na vsakem skenu
    for scan in SCANS:
        rep = report[f"s{scan:02d}"]
        im = Image.open(f"{OUT}/s{scan:02d}.jpg").convert("RGB")
        dr = ImageDraw.Draw(im)
        w, h = im.size
        if rep["mode"] == "full":
            for (y0, y1) in rep["intervals"]:
                dr.line([(0, y0), (w, y0)], fill=(255, 0, 0), width=3)
                dr.line([(0, y1), (w, y1)], fill=(0, 160, 255), width=3)
        else:
            for side in ("L", "R"):
                for (y0, y1) in rep[side]["intervals"]:
                    x = 0 if side == "L" else w // 2
                    dr.line([(x, y0), (x + w // 2, y0)], fill=(255, 0, 0), width=3)
                    dr.line([(x, y1), (x + w // 2, y1)], fill=(0, 160, 255), width=3)
        im.save(f"{OUT}/diag-s{scan:02d}.png")
    print("diag-PNG: shranjeni")


if __name__ == "__main__":
    main()
