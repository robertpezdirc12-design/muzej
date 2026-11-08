#!/usr/bin/env python3
"""
Gen-QR — AR TIME SPOTS tablice za fizični muzej (issue #11).

Nîmes la Romaine vzorec: QR koda na lokaciji → URL v mobilnem brskalniku,
brez trgovine z aplikacijami, brez računa, brez namestitve (PWA poskrbi
za offline). Vsaka točka dobe svojo kodo, ki odpre časovni stroj na
njeni letnici in s kontekstom točke:

    https://griblje-museum.vercel.app/?casovni=1825&spot=cerkev

Izhod: public/qr/spot-<id>.png (temno na svetli podlagi muzeja — 100 %
nasprotje za zanesljivo skeniranje na dotik sonca).
Ponovni zagon ob spremembi točk (src/data/atlas/timespots.ts) — spremenljivke
so tu fizično vpisane, ker skript teče izven Next.js.
"""

from pathlib import Path

import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_M

BASE = "https://griblje-museum.vercel.app"
OUT = Path(__file__).resolve().parent.parent / "public" / "qr"

# ID → URL parameter letnice (mora biti sinhron s spotYearParam v timespots.ts)
SPOTS: list[tuple[str, str, str]] = [
    # (id, casovni param, naslov za dnevnik)
    ("cerkev", "1825", "Cerkev sv. Vida"),
    ("jedro", "1825", "Jedro vasi — Grüble"),
    ("kolpa", "1825", "Kolpa — življenje ob reki"),
    ("ribnik", "1900", "Vaški ribnik"),
    ("gornje", "1825", "Gornje Griblje — zaselki in spomenik"),
    ("meja", "danes", "Meja ob Kolpi — danes in duhovi"),
    # issue #12 (P1) — oddaljene točke z lastno vsebino
    ("mlini", "1825", "Mlini ob Kolpi"),
    ("otok", "danes", "Partizansko letališče Otok 1944–45"),
    ("cerkvisce", "danes", "Cerkvišče — tri cerkvice, ki jih ni več"),
]

# barvna paleta muzeja (svetla podlaga #F7F3EB, črnilo skoraj-črno)
FG = "#171310"
BG = "#F7F3EB"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for spot_id, year, title in SPOTS:
        url = f"{BASE}/?casovni={year}&spot={spot_id}"
        qr = qrcode.QRCode(
            version=None,
            error_correction=ERROR_CORRECT_M,
            box_size=12,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=FG, back_color=BG).convert("RGB")

        # oznaka pod kodo: naslov + URL — tisk na A6 je samozadosten
        W, H = img.size
        label_h = 92
        canvas = Image.new("RGB", (W, H + label_h), BG)
        canvas.paste(img, (0, 0))

        from PIL import ImageDraw, ImageFont

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
        draw.text((24, H + 10), title, fill=FG, font=f_title)
        draw.text((24, H + 56), url, fill="#5a5049", font=f_url)

        path = OUT / f"spot-{spot_id}.png"
        canvas.save(path, optimize=True)
        print(f"  {path.relative_to(OUT.parent.parent)}  {canvas.size[0]}x{canvas.size[1]}  {url}")


if __name__ == "__main__":
    main()
