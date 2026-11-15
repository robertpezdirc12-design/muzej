from PIL import Image
im = Image.open("research/issue17/p261-work/s18.jpg")
W,H = im.size
out = "research/issue17/p262-work/"
im.save(out+"p262_full.png")
# left/right page halves, upscaled
for name, box in [("L",(0,0,W//2+40,H)), ("R",(W//2-40,0,W,H))]:
    c = im.crop(box)
    s = 1.6
    c = c.resize((int(c.width*s), int(c.height*s)), Image.LANCZOS)
    c.save(out+f"p262_page{name}.png")
# left margin strip (dates/numbers) full height, wide zoom
m = im.crop((0,0,300,H)).resize((int(300*3), int(H*3)), Image.LANCZOS)
m.save(out+"p262_margins.png")
# horizontal bands x 6 per page
bands = 6
for pi,(x0,x1) in enumerate([(0,W//2+40),(W//2-40,W)]):
    bh = H//bands
    for b in range(bands):
        y0 = b*bh; y1 = min(H, y0+bh+18)
        c = im.crop((x0,y0,x1,y1))
        s = 2.0
        c = c.resize((int(c.width*s), int(c.height*s)), Image.LANCZOS)
        c.save(out+f"p262_p{pi+1}_b{b+1}.png")
print("ok", W, H)
