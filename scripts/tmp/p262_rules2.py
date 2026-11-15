from PIL import Image
import numpy as np
im = Image.open("research/issue17/p261-work/s18.jpg").convert("L")
a = np.asarray(im, dtype=np.float32)
h,w=a.shape
seg = a[:, 400:2050]
dark = (seg < 130).sum(axis=1)
idx = np.argsort(dark)[::-1][:60]
print(sorted(idx.tolist()))
print([int(dark[i]) for i in sorted(idx.tolist())])
