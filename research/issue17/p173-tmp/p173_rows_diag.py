#!/usr/bin/env python3
"""P173 — rows detekcija + diag grid (P170/P172 recept).
rows_v3: horizontalna-projekcija detekcija ločilnih vrst; diag: fiksni grid
@ 330–1950 / 135px čez originalno sliko → diag-sNNN.jpg za Read-oči."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

DIR = "/tmp/p173"
OUT = os.path.join(DIR, "rows3.json")

def detect_rows(path):
    im = Image.open(path).convert("L")
    w, h = im.size
    px = im.load()
    # projekcija temnih pik po vrsticah (spodnja 3/4 slike, kjer je tabela)
    proj = []
    for y in range(h):
        dark = 0
        for x in range(0, w, 4):  # vzorčenje vsak 4. piksel
            if px[x, y] < 128:
                dark += 1
        proj.append(dark)
    # ločilne vrstice = lokalni maksimumi projekcije z dolgim tekom temnih pik
    thr = int((w / 4) * 0.35)  # 35% širine temno
    lines = []
    y = 250
    while y < h - 10:
        if proj[y] > thr:
            # najdi center traku
            y0 = y
            while y < h - 1 and proj[y] > thr:
                y += 1
            lines.append((y0 + y) // 2)
        y += 1
    return w, h, lines

def diag_grid(path, out, lines=None, step=135, start=330):
    im = Image.open(path).convert("RGB")
    d = ImageDraw.Draw(im)
    w, h = im.size
    if lines is None:
        lines = list(range(start, 1951, step))
    for i, y in enumerate(lines):
        d.line([(0, y), (w, y)], fill=(255, 0, 0), width=2)
        try:
            f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        except Exception:
            f = None
        d.text((5, y + 3), f"R{i}", fill=(255, 0, 0), font=f)
    # glavni stolpci (x-osi grobe oznake)
    for x, lbl in [(120, "zap"), (330, "mesec"), (480, "smrt"), (640, "pokop"),
                   (830, "vas"), (1050, "hisna"), (1300, "ime"), (1750, "star"),
                   (2000, "bolez"), (2250, "prev"), (2450, "podpis")]:
        d.line([(x, 0), (x, h)], fill=(0, 160, 255), width=1)
        d.text((x + 3, 3), lbl, fill=(0, 160, 255))
    im.save(out, quality=88)

if __name__ == "__main__":
    scans = sys.argv[1:] or ["109", "110", "111", "112", "113", "114", "115", "116"]
    rows = {}
    if os.path.exists(OUT):
        rows = json.load(open(OUT))
    for s in scans:
        p = f"{DIR}/s{s}.jpg"
        w, h, lines = detect_rows(p)
        med = (lines[-1] - lines[0]) // (len(lines) - 1) if len(lines) > 1 else 0
        ok = len(lines) >= 8
        rows[f"s{s}"] = {"w": w, "h": h, "n": len(lines), "med": med,
                         "status": "GOOD" if ok else "FAIL", "lines": lines}
        print(f"s{s}: {len(lines)} linij, med={med}, {'GOOD' if ok else 'FAIL'} → diag")
        diag_grid(p, f"{DIR}/diag-s{s}.jpg", lines=None if not ok else lines)
    json.dump(rows, open(OUT, "w"), indent=1)
