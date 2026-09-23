"""TPL 단일 이미지 읽기 (팔레트 C4/C8 포함)"""
import struct
import numpy as np
import gxtex


def info(t):
    n, tbl = struct.unpack('>II', t[4:12])
    ih, ph = struct.unpack('>II', t[tbl:tbl + 8])
    h, w, fmt, doff = struct.unpack('>HHII', t[ih:ih + 12])
    return w, h, fmt, doff, ph


def _pal(t, ph):
    n, _, pfmt, poff = struct.unpack('>HBxII', t[ph:ph + 12])
    raw = t[poff:poff + 2 * n]
    out = np.zeros((n, 4), np.uint8)
    for i in range(n):
        v = raw[2 * i] << 8 | raw[2 * i + 1]
        if pfmt == 0:   # IA8
            out[i] = (raw[2 * i + 1],) * 3 + (raw[2 * i],)
        elif pfmt == 1:
            out[i] = gxtex.c565(v) + (255,)
        else:           # RGB5A3
            if v & 0x8000:
                out[i] = ((v >> 10 & 31) * 255 // 31, (v >> 5 & 31) * 255 // 31, (v & 31) * 255 // 31, 255)
            else:
                out[i] = ((v >> 8 & 15) * 17, (v >> 4 & 15) * 17, (v & 15) * 17, (v >> 12 & 7) * 255 // 7)
    return out, pfmt


def decode(t):
    w, h, fmt, doff, ph = info(t)
    if fmt in (8, 9):
        pal, _ = _pal(t, ph)
        bw, bh = (8, 8) if fmt == 8 else (8, 4)
        idx = np.zeros((((h + bh - 1) // bh) * bh, ((w + bw - 1) // bw) * bw), np.int32); p = doff
        for by in range(0, idx.shape[0], bh):
            for bx in range(0, idx.shape[1], bw):
                for y in range(bh):
                    for x in range(bw):
                        if fmt == 8:
                            v = (t[p] >> (4 if x % 2 == 0 else 0)) & 15
                            if x % 2 == 1: p += 1
                        else:
                            v = t[p]; p += 1
                        idx[by + y, bx + x] = v
        return pal[idx][:h, :w], fmt
    return gxtex.decode(t[doff:], w, h, fmt), fmt
