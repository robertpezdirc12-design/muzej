#!/usr/bin/env python3
"""
Vstopni QR — MUSEUM VISITOR EXPERIENCE (issue #15).

Vstopna tablica fizičnega muzeja: koda odpre dobrodošlico obiskovalca
(?obisk=1) — prvi zaslon, ki razloži obisk brez vodiča:

    https://griblje-museum.vercel.app/?obisk=1

Enak vizualni stil kot spot tablice (gen-qr.py) — svetla podlaga
muzeja, skoraj-črno črnilo, oznaka pod kodo za samozadosten tisk.
"""

from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont
from qrcode.constants import ERROR_CORRECT_M

BASE = "https://griblje-museum.vercel.app"
URL = f"{BASE}/?obisk=1"
OUT = Path(__file__).resolve().parent.parent / "public" / "qr"

FG = "#171310"
BG = "#F7F3EB"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=12,
        border=4,
    )
    qr.add_data(URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color=FG, back_color=BG).convert("RGB")

    W, H = img.size
    label_h = 92
    canvas = Image.new("RGB", (W, H + label_h), BG)
    canvas.paste(img, (0, 0))

    draw = ImageDraw.Draw(canvas)
    try:
        f_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 34
        )
        f_url = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 22
        )
    except OSError:
        f_title = ImageFont.load_default()
        f_url = ImageFont.load_default()
    draw.text((24, H + 10), "VSTOP V MUZEJ GRIBLJE", fill=FG, font=f_title)
    draw.text((24, H + 56), URL, fill="#5a5049", font=f_url)

    path = OUT / "vstop.png"
    canvas.save(path, optimize=True)
    print(f"  {path.relative_to(OUT.parent.parent)}  {canvas.size[0]}x{canvas.size[1]}  {URL}")


if __name__ == "__main__":
    main()
