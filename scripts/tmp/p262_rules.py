from PIL import Image
import numpy as np
im = Image.open("research/issue17/p261-work/s18.jpg").convert("L")
a = np.asarray(im, dtype=np.float32)
h,w = a.shape
# horizontal rule detection across table body x 380..2050
seg = a[:, 380:2050]
dark = (seg < 110).sum(axis=1)
xs = w
thr = int(0.55*(2050-380))
rows=[]
y=0
while y < h:
    if dark[y] > thr:
        j=y
        while j<h and dark[j]>thr*0.6: j+=1
        rows.append((y,j)); y=j
    else: y+=1
print("rules:", rows)
print("page w,h:", w, h)
