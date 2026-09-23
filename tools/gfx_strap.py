"""Wii 주의 화면(STRAPA_JP / STRAPB_JP / ZAPPER_JP) 한글화.
글자 영역만 흰색으로 지우고, 원본 색(파랑+연한 테두리, 회색, 빨강)으로 다시 쓴다.
화면에서 가로로 늘어나 표시되므로 글자를 가로 XS 배로 눌러 그린다."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gxenc, gxtex

VF = os.path.join(HERE, 'fonts', 'PretendardVariable.ttf')
SS = 4
XS = 0.8
BLUE, GRAY, RED = (0, 172, 222), (125, 125, 125), (231, 18, 28)
BLUE_EDGE = (231, 247, 255)

R = lambda t: ('R', t)   # 빨간 강조 구간
STRAP_BLUE = [
    ['스트랩을 손목에 걸고, ', R('스토퍼'), '로 단단히 고정해 주세요.'],
    ['꼭 쥐고, 손에서 놓거나 던지지 마세요.'],
    ['Wii 리모컨 재킷을 씌워 사용하기를 권장합니다.'],
]
SPEC = {
    'STRAPA_JP': [
        dict(erase=(200, 228, 492, 302), box=(206, 236, 482, 298), lines=[['주위에 사람이나 물건이 없는지'], ['잘 확인하세요.']], color=GRAY, px=21),
        dict(erase=(24, 362, 496, 470), box=(34, 368, 482, 466), lines=STRAP_BLUE, color=BLUE, edge=BLUE_EDGE, px=21),
    ],
    'STRAPB_JP': [
        dict(erase=(228, 229, 496, 336), box=(239, 250, 482, 330), lines=[['확장 컨트롤러를 쓸 때는'], ['스트랩의 끈을'], [R('플러그의 고리'), '에 걸어 주세요.']], color=GRAY, px=21),
        dict(erase=(24, 362, 496, 470), box=(34, 368, 482, 466), lines=STRAP_BLUE, color=BLUE, edge=BLUE_EDGE, px=21),
    ],
    'ZAPPER_JP': [
        dict(erase=(33, 47, 259, 85), box=(36, 48, 256, 84), lines=[['Wii 재퍼를 사용할 경우']], color=GRAY, px=21, align='center'),
        dict(erase=(305, 308, 478, 391), box=(310, 310, 476, 390), lines=[['Wii 리모컨이 단단히'], ['고정되었는지'], ['확인하세요.']], color=RED, px=21),
        dict(erase=(24, 420, 496, 472), box=(34, 424, 482, 466), lines=[['Wii 재퍼를 두 손으로 꼭 잡아 주세요.']], color=BLUE, edge=BLUE_EDGE, px=25),
    ],
}


def font(px):
    import fontgen
    f = fontgen.make_font(VF, px)
    f.set_variation_by_axes([560])
    return f


def draw_block(img, spec):
    x0, y0, x1, y1 = spec['erase']
    img[y0:y1, x0:x1, :3] = 255
    bx0, by0, bx1, by1 = spec['box']
    px = spec['px']; lines = spec['lines']
    while True:
        f = font(px)
        widths = [sum(f.getlength(s if isinstance(s, str) else s[1]) for s in ln) / SS * XS for ln in lines]
        if max(widths) <= bx1 - bx0 or px <= 14: break
        px -= 1
    ref = f.getbbox('한'); ink = (ref[3] - ref[1]) / SS
    W, H = (bx1 - bx0), (by1 - by0)
    # 색 채널별 마스크: 기본색, 빨강
    masks = {c: Image.new('L', (int(W / XS * SS) + 8, H * SS)) for c in ('base', 'R')}
    pitch = H / len(lines)
    for i, ln in enumerate(lines):
        x = 0.0
        if spec.get('align') == 'center':
            lw = sum(f.getlength(s if isinstance(s, str) else s[1]) for s in ln)
            x = (W / XS * SS - lw) / 2
        y = pitch * i + (pitch - ink) / 2
        for seg in ln:
            key, t = ('base', seg) if isinstance(seg, str) else seg
            ImageDraw.Draw(masks[key]).text((x, y * SS - ref[1]), t, font=f, fill=255)
            x += f.getlength(t)
    out = {}
    for k, m in masks.items():
        m = m.resize((max(1, int(m.width * XS)), m.height), Image.LANCZOS)
        m = m.resize((m.width // SS, H), Image.LANCZOS)
        out[k] = np.asarray(m, np.float32)[:, :W] / 255
    reg = img[by0:by1, bx0:bx0 + out['base'].shape[1]].astype(np.float32)
    allm = np.maximum(out['base'], out['R'])
    if spec.get('edge'):
        e = np.asarray(Image.fromarray((allm * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)), np.float32) / 255
        reg[:, :, :3] = reg[:, :, :3] * (1 - e[:, :, None]) + np.array(spec['edge']) * e[:, :, None]
    for k, col in (('base', spec['color']), ('R', RED)):
        m = out[k][:, :, None]
        reg[:, :, :3] = reg[:, :, :3] * (1 - m) + np.array(col) * m
    img[by0:by1, bx0:bx0 + reg.shape[1]] = np.clip(np.round(reg), 0, 255).astype(np.uint8)
    return px


def build(arc):
    for tname, blocks in SPEC.items():
        off, w, h, fmt = gxenc.tex_info(arc, tname)
        img = gxtex.decode(bytes(arc[off:]), w, h, fmt).copy()
        for b in blocks:
            draw_block(img, b)
        gxenc.replace(arc, tname, img)


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    arc = bytearray(open(src, 'rb').read()); build(arc); open(dst, 'wb').write(arc)
