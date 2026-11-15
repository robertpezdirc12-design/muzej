import io
def show(p,a,b):
    ls=io.open(p,encoding="utf-8").read().splitlines()
    print("="*15,p)
    for i in range(a-1,min(b,len(ls))): print(i+1,ls[i])
show("scripts/p252_parish_synthesis_04455.py",1,40)
