#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P98 - enojni izrez (sken x0 y0 x1 y1 povecava izhod."""
import sys

from PIL import Image


def main():
    s, x0, y0, x1, y1, z, out = sys.argv[1:]
    s = int(s)
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    z = float(z)
    im = Image.open("/tmp/p98/scan-%02d.jpg" % s)
    b = (x0, y0, x1, y1)
    c = im.crop(b)
    w = int(c.width * z)
    h = int(c.height * z)
    size = (w, h)
    c2 = c.resize(size, Image.LANCZOS)
    c2.save(out, quality=93)
    print("ok", out)


if __name__ == "__main__":
    main()
