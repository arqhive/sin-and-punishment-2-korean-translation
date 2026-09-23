"""스테이지 선택 화면(M_BG02/03) 아래쪽 스테이지 이름 교체.
'STAGE n' 라벨은 그대로 두고, 「이름」과 이름 아래 밑줄만 다시 그린다.
원본 스타일: 검은 굵은 글씨(약 10° 기울임, 장체), 가는 「」, 흰 번짐, 이중 밑줄."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gxenc, gxtex

VF = os.path.join(HERE, 'fonts', 'PretendardVariable.ttf')
NAMES = {  # (텍스처, 칸 x, 칸 y) : 이름
    ('M_BG02', 0, 391): '탈출', ('M_BG02', 0, 455): '폐허 도시',
    ('M_BG02', 256, 391): '해저동굴', ('M_BG02', 256, 455): '감옥 위성',
    ('M_BG03', 0, 391): '식인 숲', ('M_BG03', 0, 455): '거대 모래폭풍',
    ('M_BG03', 256, 391): '인공 후지산', ('M_BG03', 256, 455): '분기',
}
X0, X1 = 60, 252          # 이름 영역(칸 기준 x)
TOP, BOT = 2, 41          # 괄호 포함 글자 영역(칸 기준 y)
TEXT_H = 35               # 한글 잉크 높이
SLANT = 0.18              # 기울기(tan)
SS = 4
BG = (244, 245, 245)


def render_name(txt, wmax):
    """괄호 포함 이름 마스크(0~1)를 돌려준다. 높이 BOT-TOP."""
    H = BOT - TOP
    f = ImageFont.truetype(VF, 60 * SS); f.set_variation_by_axes([900])
    ref = f.getbbox('한')
    t = Image.new('L', (int(f.getlength(txt)) + 20 * SS, 90 * SS))
    ImageDraw.Draw(t).text((0, 10 * SS - ref[1]), txt, font=f, fill=255)
    t = t.crop(t.getbbox())
    th = TEXT_H * SS
    tw = t.width * th / t.height
    # 괄호: 가는 선, 글자 높이 전체
    lw = int(2.2 * SS); arm = int(9 * SS); gap = int(6 * SS)
    total = lambda w: lw + gap + w + gap + lw
    maxw = (wmax - SLANT * H) * SS
    if total(tw) > maxw:
        tw = maxw - 2 * (lw + gap)          # 원본처럼 가로로 눌러 맞춘다
    t = t.resize((int(tw), th), Image.LANCZOS)
    W = int(total(tw)); Hs = H * SS
    im = Image.new('L', (W, Hs)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, lw, int(Hs * 0.62)], fill=255); d.rectangle([0, 0, arm, lw], fill=255)            # 「
    d.rectangle([W - lw, int(Hs * 0.38), W, Hs], fill=255); d.rectangle([W - arm, Hs - lw, W, Hs], fill=255)  # 」
    im.paste(t, (lw + gap, (Hs - th) // 2 + int(1.5 * SS)), t)
    # 기울임
    sh = int(SLANT * Hs)
    im = im.transform((W + sh, Hs), Image.AFFINE, (1, SLANT, -sh, 0, 1, 0), Image.BICUBIC)
    im = im.resize(((W + sh) // SS, H), Image.LANCZOS)
    return np.asarray(im, np.float32) / 255


def build(arc):
    for tname in ('M_BG02', 'M_BG03'):
        off, w, h, fmt = gxenc.tex_info(arc, tname)
        img = gxtex.decode(bytes(arc[off:]), w, h, fmt).astype(np.float32)
        for (tn, cx, cy), txt in NAMES.items():
            if tn != tname: continue
            ul = img[cy + 36:cy + 52, cx + 57].copy()        # 라벨과 이름 사이 밑줄 단면(RGBA)
            x_clear = cx + X0 - 6
            img[cy - 2:cy + 52, x_clear:cx + 256, :3] = BG; img[cy - 2:cy + 52, x_clear:cx + 256, 3] = 0
            g = render_name(txt, X1 - X0)
            gh, gw = g.shape
            # 밑줄을 이름 끝까지 연장
            x_end = cx + X0 + gw + 1
            img[cy + 36:cy + 52, x_clear:x_end] = ul[:, None, :]
            # 흰 번짐 + 검은 글자
            m = Image.fromarray((g * 255).astype(np.uint8))
            glow = np.asarray(m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.0)), np.float32) / 255
            ys, xs = cy + TOP, cx + X0
            reg = img[ys:ys + gh, xs:xs + gw]
            a0 = reg[:, :, 3] / 255
            ag = np.maximum(a0, np.clip(glow * 0.75, 0, 1))
            rgb = np.where((glow * 0.75 > a0)[:, :, None], np.array(BG, np.float32), reg[:, :, :3])
            af = g + ag * (1 - g)
            rgb = (rgb * (ag * (1 - g))[:, :, None]) / np.maximum(af, 1e-6)[:, :, None]
            reg[:, :, :3] = rgb; reg[:, :, 3] = af * 255
        gxenc.replace(arc, tname, np.clip(np.round(img), 0, 255).astype(np.uint8))


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    arc = bytearray(open(src, 'rb').read()); build(arc); open(dst, 'wb').write(arc)
