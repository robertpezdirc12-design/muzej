from PIL import Image
im = Image.open("research/issue17/p261-work/s18.jpg")
out="research/issue17/p262-work/"
crops = {
 "z_wohn6": (250,300,520,390, 6),
 "z_wohn7": (250,455,520,540, 6),
 "z_marg_6_12": (90,290,300,1500, 3.2),
}
for k,(x0,y0,x1,y1,s) in crops.items():
    c=im.crop((x0,y0,x1,y1))
    c=c.resize((int(c.width*s),int(c.height*s)), Image.LANCZOS)
    c.save(out+k+".png")
print("ok")
