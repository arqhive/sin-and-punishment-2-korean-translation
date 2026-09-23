"""MsgFont.brfnt 재구성: 원본의 ASCII/기호/전각 영숫자 글리프는 유지하고,
가나·한자 칸을 비워 한글 글리프(원본과 같은 흰 글자+검은 외곽선+그림자)로 채운다."""
import os, struct, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import textenc

FONT_PATH = os.path.join(HERE, 'fonts', 'Pretendard-SemiBold.otf')
SS = 4  # 슈퍼샘플링 배율


def parse(d):
    t = d.find(b'TGLP')
    hdr = d[t:t + 0x30]
    cw, ch, base, maxw, ssz, nsh, fmt, cols, rows, sw, shh, so = struct.unpack('>BBBBIHHHHHHI', d[t + 8:t + 0x20])
    assert fmt == 2  # IA4
    sheets = []
    for s in range(nsh):
        raw = d[so + s * ssz: so + (s + 1) * ssz]
        I = np.zeros((shh, sw), np.uint8); A = np.zeros((shh, sw), np.uint8); p = 0
        for by in range(0, shh, 4):
            for bx in range(0, sw, 8):
                blk = np.frombuffer(raw[p:p + 32], np.uint8).reshape(4, 8); p += 32
                I[by:by + 4, bx:bx + 8] = blk & 15; A[by:by + 4, bx:bx + 8] = blk >> 4
        sheets.append((I, A))
    w = d.find(b'CWDH')
    first, last = struct.unpack('>HH', d[w + 8:w + 12])
    widths = [tuple(struct.unpack('>bBb', d[w + 16 + 3 * i:w + 19 + 3 * i])) for i in range(last - first + 1)]
    cmap = {}
    p = d.find(b'CMAP')
    while p != -1:
        a, b, m = struct.unpack('>HHH', d[p + 8:p + 14])
        if m == 0:
            base0 = struct.unpack('>H', d[p + 20:p + 22])[0]
            for c in range(a, b + 1): cmap[c] = base0 + c - a
        elif m == 1:
            for c in range(a, b + 1):
                g = struct.unpack('>H', d[p + 20 + 2 * (c - a):p + 22 + 2 * (c - a)])[0]
                if g != 0xFFFF: cmap[c] = g
        else:
            n = struct.unpack('>H', d[p + 20:p + 22])[0]
            for i in range(n):
                c, g = struct.unpack('>HH', d[p + 22 + 4 * i:p + 26 + 4 * i]); cmap[c] = g
        p = d.find(b'CMAP', p + 4)
    finf = d[0x10:0x30]
    return dict(hdr=hdr, cw=cw, ch=ch, cols=cols, rows=rows, sw=sw, shh=shh, ssz=ssz,
                sheets=sheets, widths=widths, cmap=cmap, finf=finf)


def make_font(path, px):
    """'한'의 잉크 높이가 px 픽셀이 되도록 크기를 맞춘다."""
    lo, hi = 8 * SS, 60 * SS
    while lo < hi:
        mid = (lo + hi) // 2
        bb = ImageFont.truetype(path, mid).getbbox('한')
        if bb[3] - bb[1] < px * SS: lo = mid + 1
        else: hi = mid
    return ImageFont.truetype(path, lo)


def render_hangul(ch, font, cw, chh, top=3, left=1):
    """원본 한자 글리프와 같은 스타일로 한 글자를 그려 (I,A) 4비트 배열과 (left, 폭)을 돌려준다."""
    W, H = cw * SS, chh * SS
    ref = font.getbbox('한')
    body = Image.new('L', (W, H))
    # 모든 음절을 같은 원점에 찍어 기준선·자간을 통일
    ImageDraw.Draw(body).text(((left + 1) * SS - ref[0], top * SS - ref[1]), ch, font=font, fill=255)
    b = np.asarray(body, np.float32) / 255
    # 외곽선(1px)과 그림자(오른쪽 아래 1~2px)
    outline = np.asarray(body.filter(ImageFilter.MaxFilter(2 * SS + 1)), np.float32) / 255
    sh1 = np.roll(np.roll(outline, SS, 0), SS, 1)
    sh2 = np.roll(np.roll(outline, 2 * SS, 0), 2 * SS, 1)

    def down(x):
        return x.reshape(chh, SS, cw, SS).mean(axis=(1, 3))
    b1, o1, s1, s2 = down(b), down(outline), down(sh1), down(sh2)
    alpha = np.maximum.reduce([b1, o1, s1 * 0.85, s2 * 0.45])
    inten = np.where(alpha > 0, np.clip(b1 / np.maximum(alpha, 1e-6), 0, 1), 0)
    A = np.round(alpha * 15).astype(np.uint8)
    I = np.round(inten * 15).astype(np.uint8)
    I[A == 0] = 0
    xs = np.where(A.max(axis=0) > 0)[0]
    return I, A, (int(xs.min()) if len(xs) else 0, int(xs.max() - xs.min() + 1) if len(xs) else 0)


def encode_ia4(I, A):
    h, w = I.shape; out = bytearray()
    v = (A << 4 | I).astype(np.uint8)
    for by in range(0, h, 4):
        for bx in range(0, w, 8):
            out += v[by:by + 4, bx:bx + 8].tobytes()
    return bytes(out)


def build(src, dst, hmap, font_path, px=19):
    d = open(src, 'rb').read(); F = parse(d)
    cw, chh, cols = F['cw'], F['ch'], F['cols']
    per = cols * F['rows']; cap = per * len(F['sheets'])
    keep_codes = {c: g for c, g in F['cmap'].items()
                  if c < 0x100 or c >> 8 == 0x81 or 0x824F <= c <= 0x829A}
    keep = set(keep_codes.values())
    nglyph = len(F['widths'])
    free = [i for i in range(nglyph) if i not in keep] + list(range(nglyph, cap))
    if len(hmap) > len(free):
        raise SystemExit(f'글리프 칸 부족: {len(hmap)} > {len(free)}')
    widths = list(F['widths']) + [(0, 0, 0)] * (cap - nglyph)
    font = make_font(font_path, px)
    newmap = dict(keep_codes)
    used = 0
    for (ch, code), gi in zip(sorted(hmap.items(), key=lambda x: x[1]), free):
        I, A, (left, gw) = render_hangul(ch, font, cw, chh)
        s, r = divmod(gi, per); x = (r % cols) * (cw + 1); y = (r // cols) * (chh + 1)
        F['sheets'][s][0][y:y + chh, x:x + cw] = I
        F['sheets'][s][1][y:y + chh, x:x + cw] = A
        widths[gi] = (left, gw, left + gw - 1)
        newmap[code] = gi; used = max(used, gi + 1)
    # 사용 안 하는 가나/한자 칸은 비운다(깨진 글자가 섞여 보이지 않도록 매핑도 제거)
    nglyph2 = max(used, max(keep) + 1)
    # --- 직렬화 ---
    sheets_raw = b''.join(encode_ia4(I, A) for I, A in F['sheets'])
    tglp = bytearray(F['hdr']); tglp_size = 0x30 + len(sheets_raw)
    struct.pack_into('>I', tglp, 4, tglp_size)
    struct.pack_into('>I', tglp, 0x2C, 0x60)
    cwdh_off = 0x30 + tglp_size
    ent = b''.join(struct.pack('>bBb', *widths[i]) for i in range(nglyph2))
    cwdh = bytearray(b'CWDH' + b'\0' * 4 + struct.pack('>HHI', 0, nglyph2 - 1, 0) + ent)
    while len(cwdh) % 4: cwdh += b'\0'
    struct.pack_into('>I', cwdh, 4, len(cwdh))
    cmap1_off = cwdh_off + len(cwdh)
    # CMAP 1: ASCII 직접 테이블, CMAP 2: 나머지 전부 스캔 방식
    a0, a1 = 0x20, 0x7B
    tbl = b''.join(struct.pack('>H', newmap.get(c, 0xFFFF)) for c in range(a0, a1 + 1))
    c1 = bytearray(b'CMAP' + b'\0' * 4 + struct.pack('>HHHHI', a0, a1, 1, 0, 0) + tbl)
    while len(c1) % 4: c1 += b'\0'
    struct.pack_into('>I', c1, 4, len(c1))
    rest = sorted((c, g) for c, g in newmap.items() if not (a0 <= c <= a1))
    body = struct.pack('>H', len(rest)) + b''.join(struct.pack('>HH', c, g) for c, g in rest)
    c2 = bytearray(b'CMAP' + b'\0' * 4 + struct.pack('>HHHHI', 0, 0xFFFF, 2, 0, 0) + body)
    while len(c2) % 4: c2 += b'\0'
    struct.pack_into('>I', c2, 4, len(c2))
    cmap2_off = cmap1_off + len(c1)
    struct.pack_into('>I', c1, 0x10, cmap2_off + 8)
    finf = bytearray(F['finf'])
    struct.pack_into('>III', finf, 0x10, 0x38, cwdh_off + 8, cmap1_off + 8)
    total = 0x10 + len(finf) + len(tglp) + len(sheets_raw) + len(cwdh) + len(c1) + len(c2)
    hdr = b'RFNT' + struct.pack('>HHIHH', 0xFEFF, 0x0104, total, 0x10, 5)
    out = hdr + finf + tglp + sheets_raw + cwdh + c1 + c2
    assert len(out) == total
    open(dst, 'wb').write(out)
    return len(hmap), len(free), len(out)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    res, hmap, errs = textenc.encode_all()
    assert not errs, errs
    src = sys.argv[1]; dst = sys.argv[2]
    fp = os.path.join(HERE, 'fonts', sys.argv[3]) if len(sys.argv) > 3 else FONT_PATH
    px = int(sys.argv[4]) if len(sys.argv) > 4 else 19
    print(build(src, dst, hmap, fp, px))
