import struct
def parse(d):
    assert d[:4]==b'NARC'
    n,ns,ds=struct.unpack('>III',d[4:16])
    nb=0x10+n*16
    out=[]
    for i in range(n):
        fl,no,do,sz=struct.unpack('>IIII',d[0x10+i*16:0x20+i*16])
        e=d.index(b'\0',nb+no); name=d[nb+no:e].decode('latin1')
        out.append((name,ds+do,sz,fl))
    return out
