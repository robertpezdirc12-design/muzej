from PIL import Image
import statistics
im = Image.open("research/issue17/p261-work/s18.jpg").convert("L")
W,H = im.size
px = im.load()
# detect horizontal lines: dark fraction across x=330..1050
rows=[]
for y in range(H):
    dark=0
    for x in range(330,1050,4):
        if px[x,y] < 120: dark+=1
    rows.append(dark)
mx=max(rows)
cands=[y for y,d in enumerate(rows) if d > mx*0.55]
# group
groups=[]
for y in cands:
    if groups and y-groups[-1][-1]<=3: groups[-1].append(y)
    else: groups.append([y])
print("max",mx)
print([ (g[0],g[-1]) for g in groups ])
