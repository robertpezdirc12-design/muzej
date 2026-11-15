from PIL import Image
im = Image.open("research/issue17/p261-work/s18.jpg")
out="research/issue17/p262-work/"
bands = {"r06":(280,440),"r07":(430,585),"r08":(575,730),"r09":(720,875),
         "r10":(865,1020),"r11":(1010,1165),"r12":(1155,1310),"r13":(1300,1462)}
for k,(y0,y1) in bands.items():
    for side,(x0,x1) in {"L":(100,1105),"R":(1085,2120)}.items():
        c=im.crop((x0,y0,x1,y1))
        c=c.resize((int(c.width*2),int(c.height*2)), Image.LANCZOS)
        c.save(out+k+side+".png")
print("done")
