from PIL import Image
im = Image.open("research/issue17/p261-work/s18.jpg")
out="research/issue17/p262-work/"
for k,(x0,y0,x1,y1,s) in {
 "z6_date": (95,300,360,390, 8),
 "z7_date": (95,455,360,545, 8),
 "z6_beystand": (1490,290,1900,400, 5),
 "z6_sig": (1930,290,2115,420, 6),
}.items():
    c=im.crop((x0,y0,x1,y1)); c=c.resize((int(c.width*s),int(c.height*s)), Image.LANCZOS); c.save(out+k+".png")
print("ok")
