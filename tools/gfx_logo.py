"""타이틀 로고(TITLE_LOGO, 256x512 RGBA8) 한글화.
원본 罪と罰의 금빛 질감을 '금박 바탕'으로 만든 뒤 한글 죄/와/벌 모양으로 오려 넣고,
부제 宇宙の後継者를 '우주의 후계자'로 바꾼다. SIN AND PUNISHMENT 와 ™ 는 유지."""
import os, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gxtex, gxenc

VF = os.path.join(HERE, 'fonts', 'PretendardVariable.ttf')
TITLE_FONT = (VF, 930)          # (폰트 경로, 굵기) — 시안별로 바꾼다
SUB_FONT = (VF, 700)
# 글자 배치 (x0, y0, x1, y1): 원본 罪 / と / 罰 자리와 비슷하게
BOXES = {'죄': (70, 56, 222, 214), '와': (104, 220, 190, 270), '벌': (70, 276, 222, 432)}
SUB = '우주의 후계자'
SUB_COLOR = (150, 72, 30)
SUB_X, SUB_Y0, SUB_Y1 = 48, 171, 428
ROUGH = 0.7                      # 가장자리 거칠기(px)
BOLD = 0                         # 획 두껍게(px, 가는 붓글씨 폰트용)
SS = 4


def glyph_mask(ch, box, font_spec):
    x0, y0, x1, y1 = box; W, H = (x1 - x0) * SS, (y1 - y0) * SS
    f = ImageFont.truetype(font_spec[0], 400)
    if font_spec[0].endswith('Variable.ttf'): f.set_variation_by_axes([font_spec[1]])
    im = Image.new('L', (600, 600)); ImageDraw.Draw(im).text((50, 50), ch, font=f, fill=255)
    im = im.crop(im.getbbox()).resize((W, H), Image.LANCZOS)   # 칸에 꽉 채움(원본처럼 네모꼴)
    if BOLD:
        im = im.filter(ImageFilter.MaxFilter(2 * int(BOLD * SS) + 1)).filter(ImageFilter.GaussianBlur(SS * 0.5))
    return np.asarray(im, np.float32) / 255


def roughen(m, seed):
    rng = np.random.default_rng(seed)
    h, w = m.shape
    dx = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 1.5 * SS)
    dy = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 1.5 * SS)
    dx *= ROUGH * SS / (dx.std() + 1e-6); dy *= ROUGH * SS / (dy.std() + 1e-6)
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    r = cv2.remap(m, gx + dx, gy + dy, cv2.INTER_LINEAR, borderValue=0)
    # 가장자리의 잘게 갈라진 붓자국
    speck = cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), 1.2 * SS)
    edge = (r > 0.05) & (r < 0.95)
    r = np.where(edge & (speck < np.quantile(speck, 0.12)), r * 0.5, r)
    return np.clip(r, 0, 1)


def gold_field(img):
    """원본 제목 글자의 색으로 만든 금박 바탕.
    큰 색 흐름은 알파 가중 블러(정규화 합성곱)로 퍼뜨리고, 반짝이 알갱이는 원본의 고주파 성분을 입힌다."""
    A = img[:, :, 3].astype(np.float32) / 255; rgb = img[:, :, :3].astype(np.float32)
    w = (A > 0.8).astype(np.float32); w[:, :66] = 0; w[425:470, :] = 0
    num = cv2.GaussianBlur(rgb * w[:, :, None], (0, 0), 10); den = cv2.GaussianBlur(w, (0, 0), 10)[:, :, None]
    base = num / np.maximum(den, 1e-4)
    # 고주파(반짝이·결) 성분: 원본 글자 안쪽에서만 뽑아 타일처럼 반복
    hp = (rgb - cv2.GaussianBlur(rgb, (0, 0), 3)) * w[:, :, None]
    ys, xs = np.where(w > 0)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    tile = hp[y0:y1, x0:x1]; tw = w[y0:y1, x0:x1]
    detail = np.zeros_like(rgb); cnt = np.zeros(rgb.shape[:2], np.float32)
    rng = np.random.default_rng(7)
    for _ in range(60):   # 무작위 위치에 겹쳐 찍어 빈틈 없이 채움
        oy = rng.integers(-tile.shape[0] // 2, img.shape[0] - tile.shape[0] // 2)
        ox = rng.integers(-tile.shape[1] // 2, img.shape[1] - tile.shape[1] // 2)
        sy0, sx0 = max(0, oy), max(0, ox); sy1 = min(img.shape[0], oy + tile.shape[0]); sx1 = min(img.shape[1], ox + tile.shape[1])
        if sy1 <= sy0 or sx1 <= sx0: continue
        t = tile[sy0 - oy:sy1 - oy, sx0 - ox:sx1 - ox]; m = tw[sy0 - oy:sy1 - oy, sx0 - ox:sx1 - ox]
        upd = (m > 0) & (cnt[sy0:sy1, sx0:sx1] == 0)
        detail[sy0:sy1, sx0:sx1][upd] = t[upd]; cnt[sy0:sy1, sx0:sx1][upd] = 1
    field = np.where(w[:, :, None] > 0, rgb, base + detail)
    return np.clip(field, 0, 255)


def build(arc):
    off, w, h, fmt = gxenc.tex_info(arc, 'TITLE_LOGO')
    img = gxtex.decode(bytes(arc[off:]), w, h, fmt).copy()
    gold = gold_field(img)
    out = img.astype(np.float32)
    # 원본 제목·부제 지우기 (SIN AND PUNISHMENT·™ 줄은 남김)
    keep = np.zeros(img.shape[:2], bool); keep[434:470, :] = True
    tit = (np.arange(w)[None, :] >= 66) | ((np.arange(h)[:, None] >= 160) & (np.arange(h)[:, None] < 434))
    clear = tit & ~keep
    out[clear, 3] = 0
    # 부제 열(宇宙の後継者 + 후리가나)
    out[160:434, 20:68, 3] = 0
    # 아래쪽(罰 꼬리 + SIN AND PUNISHMENT + ™) 지우고 영문 줄을 새로 쓴다
    out[425:470, :, 3] = 0
    import fontgen
    fe = fontgen.make_font(VF, 8); fe.set_variation_by_axes([650])
    txt = 'SIN AND PUNISHMENT'
    im = Image.new('L', (256 * SS, 20 * SS)); d = ImageDraw.Draw(im)
    ref = fe.getbbox('S'); step = (216 - 35) * SS / (len(txt) - 1)
    for k, c in enumerate(txt):
        d.text((35 * SS + k * step - fe.getlength(c) / 2 + fe.getlength('M') / 2, 2 * SS - ref[1]), c, font=fe, fill=255)
    ft = fontgen.make_font(VF, 5); ft.set_variation_by_axes([600])
    d.text((201 * SS, 16 * SS - ft.getbbox('T')[1]), 'TM', font=ft, fill=255)
    mm = np.asarray(im.resize((256, 20), Image.LANCZOS), np.float32) / 255
    reg = out[437:457]; a1 = mm[:, :, None]
    reg[:, :, :3] = np.array([146, 107, 86]) * a1 + reg[:, :, :3] * (1 - a1); reg[:, :, 3:4] = np.maximum(reg[:, :, 3:4], a1 * 255)
    # 제목
    for i, (ch, box) in enumerate(BOXES.items()):
        x0, y0, x1, y1 = box
        m = roughen(glyph_mask(ch, box, TITLE_FONT), i)
        m = cv2.resize(m, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA)
        # 가장자리 쪽을 조금 어둡게(원본의 그을린 느낌)
        dist = cv2.distanceTransform((m > 0.5).astype(np.uint8), cv2.DIST_L2, 3)
        shade = 0.55 + 0.45 * np.clip(dist / 4.0, 0, 1)
        reg = out[y0:y1, x0:x1]
        col = gold[y0:y1, x0:x1] * shade[:, :, None]
        a0 = reg[:, :, 3:4] / 255; a1 = m[:, :, None]
        na = a1 + a0 * (1 - a1)
        reg[:, :, :3] = (col * a1 + reg[:, :, :3] * a0 * (1 - a1)) / np.maximum(na, 1e-6)
        reg[:, :, 3:4] = na * 255
    # 부제 세로쓰기
    f = ImageFont.truetype(SUB_FONT[0], 1)
    import fontgen
    f = fontgen.make_font(SUB_FONT[0], 21)
    if SUB_FONT[0].endswith('Variable.ttf'): f.set_variation_by_axes([SUB_FONT[1]])
    chars = [c for c in SUB if c != ' ']
    gaps = SUB.index(' ')                      # '우주의' 다음에 반 칸 띄움
    n = len(chars); pitch = (SUB_Y1 - SUB_Y0) / (n + 0.5)
    ref = f.getbbox('한')
    for k, c in enumerate(chars):
        y = SUB_Y0 + pitch * (k + (0.5 if k >= gaps else 0))
        im = Image.new('L', (40 * SS, 40 * SS)); ImageDraw.Draw(im).text((20 * SS - f.getlength(c) / 2, 4 * SS - ref[1]), c, font=f, fill=255)
        mm = np.asarray(im.resize((40, 40), Image.LANCZOS), np.float32) / 255
        ys, xs = int(round(y)) - 4, SUB_X - 20
        reg = out[ys:ys + 40, xs:xs + 40]
        a0 = reg[:, :, 3:4] / 255; a1 = mm[:, :, None]; na = a1 + a0 * (1 - a1)
        reg[:, :, :3] = (np.array(SUB_COLOR) * a1 + reg[:, :, :3] * a0 * (1 - a1)) / np.maximum(na, 1e-6)
        reg[:, :, 3:4] = na * 255
    gxenc.replace(arc, 'TITLE_LOGO', np.clip(np.round(out), 0, 255).astype(np.uint8))


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3:   # 시안 비교용: 폰트파일 [거칠기] [굵기보정]
        TITLE_FONT = (os.path.join(HERE, 'fonts', sys.argv[3]), 930)
        if len(sys.argv) > 4: ROUGH = float(sys.argv[4])
        if len(sys.argv) > 5: BOLD = float(sys.argv[5])
    arc = bytearray(open(src, 'rb').read()); build(arc); open(dst, 'wb').write(arc)
