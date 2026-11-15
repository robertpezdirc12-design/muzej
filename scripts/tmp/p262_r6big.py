from PIL import Image
im = Image.open("research/issue17/p261-work/s18.jpg")
c=im.crop((180,285,1000,440)); c=c.resize((c.width*4,c.height*4), Image.LANCZOS)
c.save("research/issue17/p262-work/r06L_big.png"); print(c.size)
