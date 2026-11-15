from PIL import Image
im = Image.open("research/issue17/p261-work/s18.jpg")
out="research/issue17/p262-work/"
for k,(y0,y1) in {"dates_top":(275,880),"dates_bot":(860,1330)}.items():
    c=im.crop((95,y0,300,y1)); c=c.resize((c.width*4,c.height*4), Image.LANCZOS); c.save(out+k+".png")
    print(k, c.size)
