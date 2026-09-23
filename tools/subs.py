"""컷신 자막: SPRX(줄 사각형) 파싱, 텍스처 입출력 공용 모듈."""
import os, sys, struct, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import narc, gxtex
import numpy as np

ISO = os.path.join(ROOT, 'work', 'iso_all', 'DATA', 'files')   # 원본 그대로인 스테이지 arc 에서 SPRX 를 읽는다


def sprx_all():
    """{세트명: dict(arc, names, sprites=[(tex, x0,y0,u0,v0,x1,y1,u1,v1)])}"""
    out = {}
    for f in sorted(glob.glob(os.path.join(glob.escape(ISO), 's0*.arc'))):
        a = open(f, 'rb').read()
        for n, o, s, fl in narc.parse(a):
            if not n.startswith('TX'): continue
            d = a[o:o + s]; nt, ns = d[4], d[5]
            p0, p1, p2 = struct.unpack('>III', d[0x10:0x1c])
            names = [d[p0 + 16 * i:p0 + 16 * i + 16].split(b'\0')[0].decode().split('.')[0].upper() for i in range(nt)]
            spr = []
            for i in range(ns):
                e = d[p2 + i * 0x28:p2 + i * 0x28 + 0x28]
                _, tex, _ = struct.unpack('>HHI', e[:8])
                spr.append((tex // 256,) + struct.unpack('>8f', e[8:]))
            out[n] = dict(arc=os.path.basename(f), off=o, size=s, names=names, sprites=spr)
    if len(out) != 19:
        raise SystemExit(f'자막 세트를 {len(out)}개만 찾았습니다(19개여야 함). {ISO} 를 확인하세요.')
    return out


def load_tex(arcpath, name):
    a = open(arcpath, 'rb').read()
    for n, o, s, fl in narc.parse(a):
        if n == name:
            d = a[o:o + s]; i = d.find(b'TEX0')
            w, h, fmt, _ = struct.unpack('>HHII', d[i + 0x1c:i + 0x28]); do = struct.unpack('>I', d[i + 0x10:i + 0x14])[0]
            return gxtex.decode(d[i + do:], w, h, fmt), fmt
    raise KeyError(name)


def rect(sp, w, h):
    tex, x0, y0, u0, v0, x1, y1, u1, v1 = sp
    return int(round(u0 * w)), int(round(v0 * h)), int(round(u1 * w)), int(round(v1 * h))
