"""opening.bnr(Wii 메뉴 배너·아이콘) 로고 교체.
새 TITLE_LOGO(texture.arc)에서 잘라 축소해 bnr_logo1/2(+그림자), logo_sp2_s(아이콘)를 만든다.
TPL은 같은 크기로 제자리 교체 → banner.bin/icon.bin 재압축(LZ77) → IMD5 → 바깥 U8 재구성.
IMET 헤더(압축 전 크기·이름·MD5)는 바뀌지 않는다."""
import os, sys, struct
import numpy as np, cv2
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import u8, tpl, subs

# (TPL 이름, 원본 로고에서 잘라 올 영역 (x0,y0,x1,y1), 대상 영역 (x0,y0,x1,y1), 종류)
JOBS = [   # (TPL 이름, [(원본 로고 잘라 올 영역, 대상 영역), ...], 종류)
    ('bnr_logo1.tpl', [((66, 50, 225, 432), (0, 0, 99, 200)), ((30, 434, 226, 462), (0, 200, 99, 211))], 'color'),
    ('bnr_logo1sh.tpl', [((66, 50, 225, 432), (1, 1, 51, 103)), ((30, 434, 226, 462), (1, 103, 51, 108))], 'shadow'),
    ('bnr_logo2.tpl', [((30, 165, 70, 432), (0, 0, 24, 180))], 'color'),
    ('bnr_logo2sh.tpl', [((30, 165, 70, 432), (1, 1, 16, 87))], 'shadow'),
    ('logo_sp2_s.tpl', [((30, 50, 225, 462), (0, 0, 39, 82))], 'color'),
]


def render(logo, job, shape):
    name, parts, kind = job
    h, w = shape
    out = np.zeros((h, w, 4), np.float32); al = np.zeros((h, w), np.float32)
    for (sx0, sy0, sx1, sy1), (tx0, ty0, tx1, ty1) in parts:
        src = logo[sy0:sy1, sx0:sx1].astype(np.float32)
        pm = src.copy(); pm[:, :, :3] *= pm[:, :, 3:4] / 255      # 알파 가중 축소
        sm = cv2.resize(pm, (tx1 - tx0, ty1 - ty0), interpolation=cv2.INTER_AREA)
        a = sm[:, :, 3:4]; rgb = np.where(a > 0, sm[:, :, :3] * 255 / np.maximum(a, 1e-3), 0)
        out[ty0:ty1, tx0:tx1, :3] = rgb; out[ty0:ty1, tx0:tx1, 3] = a[:, :, 0]
        al[ty0:ty1, tx0:tx1] = a[:, :, 0]
    if kind == 'shadow':
        out[:] = 0; out[:, :, 3] = np.clip(cv2.GaussianBlur(al, (0, 0), 1.0) * 1.3, 0, 255)
    return np.clip(np.round(out), 0, 255).astype(np.uint8)


def _rgb5a3(c):
    r, g, b, a = [int(v) for v in c]
    if a >= 0xE0:
        return 0x8000 | (r >> 3) << 10 | (g >> 3) << 5 | (b >> 3)
    return (a >> 5) << 12 | (r >> 4) << 8 | (g >> 4) << 4 | (b >> 4)


def write_tpl(t, img):
    t = bytearray(t)
    w, h, fmt, doff, ph = tpl.info(bytes(t))
    if fmt == 3:   # IA8
        raw = bytearray()
        for by in range(0, h + 3 & ~3, 4):
            for bx in range(0, w + 3 & ~3, 4):
                for y in range(4):
                    for x in range(4):
                        yy, xx = by + y, bx + x
                        if yy < h and xx < w: raw += bytes([img[yy, xx, 3], img[yy, xx, 0]])
                        else: raw += b'\0\0'
        t[doff:doff + len(raw)] = raw
        return bytes(t)
    assert fmt == 9
    n, _, pfmt, poff = struct.unpack('>HBxII', t[ph:ph + 12])
    assert pfmt == 2, pfmt
    q = Image.fromarray(img, 'RGBA').quantize(colors=n, method=Image.Quantize.FASTOCTREE)
    pal = np.array(q.getpalette('RGBA')[:4 * n] + [0] * max(0, 4 * n - len(q.getpalette('RGBA')))).reshape(-1, 4)[:n]
    idx = np.asarray(q)
    for i in range(n):
        struct.pack_into('>H', t, poff + 2 * i, _rgb5a3(pal[i]))
    raw = bytearray()
    for by in range(0, (h + 3) & ~3, 4):
        for bx in range(0, (w + 7) & ~7, 8):
            for y in range(4):
                for x in range(8):
                    yy, xx = by + y, bx + x
                    raw.append(int(idx[yy, xx]) if yy < h and xx < w else 0)
    t[doff:doff + len(raw)] = raw
    return bytes(t)


def patch_inner(inner, logo):
    inner = bytearray(inner)
    _, _, fs = u8.u8_list(bytes(inner))
    for p, i, o, sz in fs:
        nm = p.split('/')[-1]
        for job in JOBS:
            if job[0] == nm:
                t = bytes(inner[o:o + sz]); w, h, *_ = tpl.info(t)
                inner[o:o + sz] = write_tpl(t, render(logo, job, (h, w)))
    return bytes(inner)


def rebuild_outer(u8b, repl):
    """바깥 U8(meta/banner.bin 등)의 파일 데이터를 교체하고 오프셋을 다시 계산한다."""
    root, ents, files = u8.u8_list(u8b)
    b = bytearray(u8b); data_start = struct.unpack('>I', b[12:16])[0]
    out = bytearray(b[:data_start]); pos = data_start
    for p, i, o, sz in files:
        d = repl.get(p, bytes(u8b[o:o + sz]))
        while len(out) % 32: out.append(0)
        pos = len(out); out += d
        struct.pack_into('>II', out, root + i * 12 + 4, pos, len(d))
    while len(out) % 32: out.append(0)
    return bytes(out)


def build(bnr_src, bnr_dst, logo):
    d = open(bnr_src, 'rb').read()
    head, outer = d[:0x600], d[0x600:]
    _, _, fs = u8.u8_list(outer); repl = {}
    for p, i, o, sz in fs:
        if p.endswith(('banner.bin', 'icon.bin')):
            inner, comp = u8.imd5_unwrap(outer[o:o + sz])
            repl[p] = u8.imd5_wrap(patch_inner(inner, logo), comp)
    open(bnr_dst, 'wb').write(head + rebuild_outer(outer, repl))


if __name__ == '__main__':
    arc, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    logo = subs.load_tex(arc, 'TITLE_LOGO')[0]
    build(src, dst, logo)
