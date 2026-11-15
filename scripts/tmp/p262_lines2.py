from PIL import Image
im = Image.open("research/issue17/p261-work/s18.jpg").convert("L")
W,H=im.size; px=im.load()
prof=[]
for y in range(200,H):
    dark=sum(1 for x in range(340,960) if px[x,y]<150)
    prof.append((y,dark))
vals=[d for _,d in prof]
mean=sum(vals)/len(vals)
sd=(sum((v-mean)**2 for v in vals)/len(vals))**0.5
th=mean+2.2*sd
print("mean",round(mean,1),"sd",round(sd,1),"th",round(th,1))
peaks=[]
for y,d in prof:
    if d>th:
        if peaks and y-peaks[-1][-1]<=4: peaks[-1].append(y)
        else: peaks.append([y])
print([(g[0],g[-1]) for g in peaks])
