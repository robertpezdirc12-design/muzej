from PIL import Image
import os
OUT = '/tmp/p256/R'
os.makedirs(OUT, exist_ok=True)
JOBS = [
    ('s4_R1', 's4', 1090, 2144, 280, 830),   # vrstice 1–5 (starši ženina/neveste, priče, urkunde, podpis)
    ('s5_R1', 's5', 1090, 2124, 230, 520),   # vrstici 1–2
    ('s6_R1', 's6', 1090, 2103, 295, 560),   # vrstice 1–3
]
for name, tag, x0, x1, y0, y1 in JOBS:
    im = Image.open(f'/tmp/p256/{tag}.jpg')
    W, H = im.size
    c = im.crop((x0, y0, min(x1, W), min(y1, H)))
    c = c.resize((int(c.width*1.8), int(c.height*1.8)), Image.LANCZOS)
    c.save(f'{OUT}/{name}.jpg', quality=90)
    print(name, c.size)
