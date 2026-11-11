from PIL import Image
import os
OUT = '/tmp/p256/D'
# s4 r2-r5 (y: r2 379-518, r3 518-657, r4 657-796, r5 796-935) + s5 r4/r5 (r4 621-748, r5 748-875)
JOBS = [
    ('s4r2_dt2', 's4', 35, 255, 365, 530),
    ('s4r3_dt2', 's4', 35, 255, 505, 670),
    ('s4r4_dt2', 's4', 35, 255, 645, 810),
    ('s4r5_dt2', 's4', 35, 255, 785, 950),
    ('s5r4_dt2', 's5', 35, 255, 610, 760),
    ('s5r5_dt2', 's5', 35, 255, 735, 890),
]
for name, tag, x0, x1, y0, y1 in JOBS:
    im = Image.open(f'/tmp/p256/{tag}.jpg')
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width*5, c.height*5), Image.LANCZOS)
    c.save(f'{OUT}/{name}.jpg', quality=92)
    print(name, c.size)
