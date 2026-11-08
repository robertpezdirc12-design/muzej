#!/usr/bin/env python3
"""Post-proces hero panoram (issue #13):
  1. horizontalni roll — šiv prestavljen v monoton pas (različen δ na posnetek);
  2. navpična kalibracija horizonta — vrstica horizonta -> točno 50 % višine
     (nebo raztegnjeno, tla stisnjena — AI slika ni pravi equirect, mehka
     popravka; dokumentirano v metodologiji vsake panorame);
  3. preklopna združitev šiva (cross-fade ~120 px);
  4. JPEG (q80, progresivno) + predogled 640×320 (q65).

Rezultat: public/panoramas/<ime>.jpg + <ime>-preview.jpg
"""
import sys
from PIL import Image, ImageFilter

# name -> (roll fraction δ, horizonV from top)
SPECS = {
    "cerkev-1825": (0.95, 0.45),
    "jedro-1825": (0.15, 0.38),
    "kolpa-1825": (0.25, 0.25),
}

W, H = 2048, 1024
SEAM_BLEND_PX = 120


def roll_horizontal(img: Image.Image, frac: float) -> Image.Image:
    shift = int(round(frac * W)) % W
    if shift == 0:
        return img
    left = img.crop((shift, 0, W, H))
    right = img.crop((0, 0, shift, H))
    out = Image.new("RGB", (W, H))
    out.paste(left, (0, 0))
    out.paste(right, (W - shift, 0))
    return out


def calibrate_horizon(img: Image.Image, horizon_v: float) -> Image.Image:
    """vrstica horizonta (horizon_v od zgoraj) -> 50 % višine."""
    h_row = int(round(horizon_v * H))
    if abs(h_row - H // 2) <= 2:
        return img
    sky = img.crop((0, 0, W, h_row)).resize((W, H // 2), Image.LANCZOS)
    ground = img.crop((0, h_row, W, H)).resize((W, H // 2), Image.LANCZOS)
    out = Image.new("RGB", (W, H))
    out.paste(sky, (0, 0))
    out.paste(ground, (0, H // 2))
    return out


def blend_seam(img: Image.Image, width_px: int) -> Image.Image:
    """preklopna združitev med desnim in levim robom (mehk šiv)."""
    if width_px <= 0:
        return img
    px = img.load()
    for x in range(width_px):
        a = x / width_px  # 0 pri šivu -> 1 po širini traku
        x2 = W - width_px + x
        for y in range(H):
            r1, g1, b1 = px[x, y]
            r2, g2, b2 = px[x2, y]
            px[x, y] = (
                int(r1 * a + r2 * (1 - a)),
                int(g1 * a + g2 * (1 - a)),
                int(b1 * a + b2 * (1 - a)),
            )
    return img


def main() -> None:
    import os

    os.makedirs("/home/z/my-project/public/panoramas", exist_ok=True)
    for name, (roll, horizon_v) in SPECS.items():
        src = f"/tmp/pano/{name}.png"
        img = Image.open(src).convert("RGB")
        assert img.size == (W, H), f"{name}: {img.size}"
        img = roll_horizontal(img, roll)
        img = calibrate_horizon(img, horizon_v)
        img = blend_seam(img, SEAM_BLEND_PX)
        out = f"/home/z/my-project/public/panoramas/{name}.jpg"
        img.save(out, "JPEG", quality=80, optimize=True, progressive=True)
        prev = img.resize((640, 320), Image.LANCZOS)
        prev_out = f"/home/z/my-project/public/panoramas/{name}-preview.jpg"
        prev.save(prev_out, "JPEG", quality=65, optimize=True, progressive=True)
        print(
            f"OK {name}: roll={roll} horizon {horizon_v}->0.50, "
            f"full={os.path.getsize(out)//1024} KB, "
            f"preview={os.path.getsize(prev_out)//1024} KB"
        )


if __name__ == "__main__":
    sys.exit(main())
