"""컷신 자막 텍스처(TX*_*) 생성: translation/ko.json → texture.arc 안 IA4 텍스처를 제자리 교체.
각 줄은 SPRX 사각형 안에 가운데 정렬로 그리고, 넘치면 글자 크기를 줄인다."""
import os, sys, struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import subs, narc, fontgen

FONT = os.path.join(HERE, 'fonts', 'Pretendard-SemiBold.otf')
SS = 4
BASE_PX = 23      # '한' 잉크 높이(원본 자막 가나와 비슷하게)
MIN_PX = 16
MARGIN = 6        # 사각형 좌우 여백


def load_subs(path=os.path.join(ROOT, 'translation', 'ko.json')):
    import json
    return {x['id']: x['ko'] for x in json.load(open(path, encoding='utf8'))['subtitles']}


_fonts = {}
def font(px):
    if px not in _fonts:
        _fonts[px] = fontgen.make_font(FONT, px)
    return _fonts[px]


TRACK = 1.0       # 자간(px)


PUNCT = set('!?.,…~』」)')


def _track(txt, i):
    """i번째 글자 뒤 자간. 다음 글자가 문장부호면 붙인다."""
    return 0 if i + 1 >= len(txt) or txt[i + 1] in PUNCT else TRACK


def line_width(txt, f):
    return sum(f.getlength(c) / SS + _track(txt, i) for i, c in enumerate(txt))


def draw_line(d, x, y, txt, f):
    for i, c in enumerate(txt):
        d.text((x, y), c, font=f, fill=255)
        x += f.getlength(c) + _track(txt, i) * SS


def render_sprite(txt, w, h):
    """사각형(w,h) 하나를 IA4용 (I,A) 0~15 배열로 그린다."""
    txt = txt.replace('   ', ' ')   # 원문 전각 공백 간격 → em 공백
    lines = txt.split('\n')
    px = BASE_PX
    while px > MIN_PX and max(line_width(l, font(px)) for l in lines) + 6 > w - 2 * MARGIN:
        px -= 1
    f = font(px)
    ref = f.getbbox('한')
    ink = (ref[3] - ref[1]) / SS
    W, H = w * SS, h * SS
    body = Image.new('L', (W, H)); d = ImageDraw.Draw(body)
    n = len(lines); gap = ink * 0.5
    top = (h - (n * ink + (n - 1) * gap)) / 2
    for i, l in enumerate(lines):
        lw = line_width(l, f)
        x = (w - lw) / 2
        y = top + i * (ink + gap) + 1.5
        draw_line(d, x * SS - ref[0], y * SS - ref[1], l, f)
    b = np.asarray(body, np.float32) / 255
    outline = np.asarray(body.filter(ImageFilter.MaxFilter(4 * SS + 1)), np.float32) / 255   # 약 2px 외곽선
    halo = np.asarray(Image.fromarray((outline * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2 * SS)), np.float32) / 255

    def down(x):
        return x.reshape(h, SS, w, SS).mean(axis=(1, 3))
    b1, o1, h1 = down(b), down(outline), down(halo)
    alpha = np.maximum.reduce([b1, o1, h1 * 0.55])
    inten = np.where(alpha > 0, np.clip(b1 / np.maximum(alpha, 1e-6), 0, 1), 0)
    inten = 0.07 + inten * 0.87   # 원본처럼 외곽선은 완전 검정이 아니고 글자는 약간 회색빛 흰색
    A = np.clip(np.round(alpha * 15), 0, 15).astype(np.uint8)
    I = np.clip(np.round(inten * 15), 0, 15).astype(np.uint8)
    I[A == 0] = 0
    return I, A, px


def build_textures(src_arc, dst_arc, report=None):
    X = subs.sprx_all(); S = load_subs()
    a = bytearray(open(src_arc, 'rb').read())
    ents = {n: (o, s) for n, o, s, fl in narc.parse(bytes(a))}
    missing = []; shrunk = []
    for sn, v in X.items():
        # 텍스처별 캔버스
        canv = {}
        for ti, tname in enumerate(v['names']):
            o, s = ents[tname]; d = a[o:o + s]; i = d.find(b'TEX0')
            w, h, fmt, _ = struct.unpack('>HHII', d[i + 0x1c:i + 0x28])
            assert fmt == 2, (tname, fmt)
            canv[ti] = [np.zeros((h, w), np.uint8), np.zeros((h, w), np.uint8), o + i + struct.unpack('>I', d[i + 0x10:i + 0x14])[0]]
        for k, sp in enumerate(v['sprites']):
            key = f'{sn}#{k}'
            if key not in S:
                missing.append(key); continue
            I0, A0, _ = canv[sp[0]]
            H, W = I0.shape
            x0, y0, x1, y1 = subs.rect(sp, W, H)
            I, A, px = render_sprite(S[key], x1 - x0, y1 - y0)
            if px < BASE_PX: shrunk.append((key, px))
            I0[y0:y1, x0:x1] = I; A0[y0:y1, x0:x1] = A
        for ti, (I0, A0, doff) in canv.items():
            raw = fontgen.encode_ia4(I0, A0)
            a[doff:doff + len(raw)] = raw
    open(dst_arc, 'wb').write(a)
    return missing, shrunk


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    m, s = build_textures(os.path.join(ROOT, 'work', 'orig', 'texture.arc'), sys.argv[1])
    print('missing', m); print('shrunk', s)
