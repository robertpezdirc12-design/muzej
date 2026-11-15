from PIL import Image
im = Image.open("research/issue17/p261-work/s18.jpg")
out="research/issue17/p262-work/"
ys=[285,455,620,790,960,1130,1300]
for i,y in enumerate(ys, start=6):
    h=215 if i<12 else 200
    for tag,(x0,x1) in [("L",(60,1095)),("R",(1095,2110))]:
        c=im.crop((x0,y,x1,min(1500,y+h)))
        s=2.6
        c=c.resize((int(c.width*s),int(c.height*s)), Image.LANCZOS)
        c.save(out+f"row{i}_{tag}.png")
print("ok")
