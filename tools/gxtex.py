import numpy as np, struct
BLK={0:(8,8,4),1:(8,4,8),2:(8,4,8),3:(4,4,16),4:(4,4,16),5:(4,4,16),6:(4,4,32),14:(8,8,4)}
def size(w,h,f):
    bw,bh,bpp=BLK[f]; return ((w+bw-1)//bw)*((h+bh-1)//bh)*bw*bh*bpp//8
def c565(v):
    r=(v>>11)&31;g=(v>>5)&63;b=v&31
    return (r<<3|r>>2, g<<2|g>>4, b<<3|b>>2)
def decode(d,w,h,f):
    bw,bh,bpp=BLK[f]; out=np.zeros((((h+bh-1)//bh)*bh,((w+bw-1)//bw)*bw,4),np.uint8); p=0
    for by in range(0,out.shape[0],bh):
        for bx in range(0,out.shape[1],bw):
            if f==6:
                ar=d[p:p+32];gb=d[p+32:p+64];p+=64
                for i in range(16):
                    out[by+i//4,bx+i%4]=(ar[2*i+1],gb[2*i],gb[2*i+1],ar[2*i])
                continue
            if f==14:
                for sb in range(4):
                    c0,c1=struct.unpack('>HH',d[p:p+4]); idx=struct.unpack('>I',d[p+4:p+8])[0]; p+=8
                    a=c565(c0);b=c565(c1)
                    if c0>c1: pal=[a+(255,),b+(255,),tuple((2*x+y)//3 for x,y in zip(a,b))+(255,),tuple((x+2*y)//3 for x,y in zip(a,b))+(255,)]
                    else: pal=[a+(255,),b+(255,),tuple((x+y)//2 for x,y in zip(a,b))+(255,),(0,0,0,0)]
                    ox=bx+(sb%2)*4; oy=by+(sb//2)*4
                    for i in range(16):
                        out[oy+i//4,ox+i%4]=pal[(idx>>(30-2*i))&3]
                continue
            for y in range(bh):
                for x in range(bw):
                    if f==0:
                        v=(d[p]>>(4 if x%2==0 else 0))&15; v*=17; px=(v,v,v,255)
                        if x%2==1: p+=1
                    elif f==1: v=d[p];p+=1;px=(v,v,v,255)
                    elif f==2: v=d[p];p+=1;i=(v&15)*17;a=(v>>4)*17;px=(i,i,i,a)
                    elif f==3: a=d[p];i=d[p+1];p+=2;px=(i,i,i,a)
                    elif f==4: v=d[p]<<8|d[p+1];p+=2;px=c565(v)+(255,)
                    elif f==5:
                        v=d[p]<<8|d[p+1];p+=2
                        if v&0x8000: r=(v>>10)&31;g=(v>>5)&31;b=v&31;px=(r*255//31,g*255//31,b*255//31,255)
                        else: a=(v>>12)&7;r=(v>>8)&15;g=(v>>4)&15;b=v&15;px=(r*17,g*17,b*17,a*255//7)
                    out[by+y,bx+x]=px
    return out[:h,:w]
