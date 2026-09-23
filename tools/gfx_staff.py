"""스태프롤(M_STAF01~05, IA4) 한글화.
이름 줄만 지우고 한글로 다시 쓴다. 영어 직책명·로고·저작권 줄은 원본 그대로.
이름 읽기는 유럽판 스태프롤 로마자 표기를 근거로 일본어 표기법에 맞춰 옮겼다.
川野 成央은 유럽판에 없어 사용자가 알려 준 읽기(Kawano Nario)를 썼다."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gxtex, gxenc, fontgen

FONT = os.path.join(HERE, 'fonts', 'PretendardVariable.ttf')
WEIGHT = 780
TRACK = 2.0   # 원본처럼 넓은 자간(px)
SS = 4
NAME_PX, ROLE_PX = 19, 13

# (텍스처번호, 지울 x0, x1, 줄 y0, y1, 내용)
#   내용: 문자열 = 가운데 정렬 이름
#         ('voice', 역할, 이름) = 캐릭터 음성 줄 (역할은 작게 오른쪽 정렬 + ' / ' + 이름)
#         ('right', 이름) = x0부터 왼쪽 정렬 (노래 페이지 이름)
L = []
def add(t, x0, x1, ys, items):
    for y, it in zip(ys, items):
        L.append((t, x0, x1, y, y + 23, it))

# M_STAF01 : 캐릭터 음성 / 프로그램
add(1, 0, 320, [53, 85, 117, 149, 181, 213, 245], [
    ('voice', '이사 조', '호소야 요시마사'), ('voice', '카치', '요시다 세이코'),
    ('voice', '첸롱 리', '신가키 다루스케'), ('voice', '리터', '이시가미 유이치'),
    ('voice', '아리아나 샤미', '소미 요코'), ('voice', '히바루 야주', '사와시로 미유키'),
    ('voice', '데코 게키쇼', '오카와 도루')])
add(1, 0, 320, [277, 309, 341], ['미네 가오리', '이마루오카 아쓰시', '마스다 다카유키'])
add(1, 320, 512, [54], ['나카가와 아쓰토모'])
add(1, 320, 512, [102, 134, 166, 198, 230, 262, 294], [
    '나카가와 아쓰토모', '니시무라 나쓰키', '우쿄 마사키', '긴바라 슌',
    '다카하시 소이치로', '미부 유키', '마쓰우라 히로토'])
add(1, 320, 512, [341, 374], ['이시다 가즈히코', '산조 가쓰히로'])
# M_STAF02 : 아트 / 모션 / 음악
add(2, 0, 256, [23], ['스즈키 야스시'])
add(2, 0, 256, [70, 102], ['아다치 쓰토무', '오치 미쓰노부'])
add(2, 0, 256, [150, 182, 214, 246, 278, 310], [
    '스즈키 야스시', '후지타 유헤이', '아다치 쓰토무', '기타가와 나오키', '오기노 마코토', '에비하라 노부아키'])
add(2, 0, 256, [359, 391, 423], ['오기노 마코토', '아다치 쓰토무', '스즈키 야스시'])
add(2, 0, 256, [471], ['다케하나 히데유키'])
add(2, 256, 512, [23, 55, 87, 119, 151], [
    '다케하나 히데유키', '고마쓰 요시히로', '오미야 무쓰오', '데쓰카 사토시', '후지타 유헤이'])
add(2, 256, 512, [196], ['한자와 노리오'])
add(2, 256, 512, [244, 276], ['마자와 에이지', '고세키 야스시'])   # Additional Songs 블록(SPRX 미참조지만 통일)
add(2, 256, 512, [420], ['무라타 사토시'])
# M_STAF03 : 협력사 / 디렉터 / 프로듀서
add(3, 0, 512, [21, 53, 85, 117, 148], [
    '(유)릴리스 유니버설 네트워크', '(주)피스', '(주)애틱', '(유)ASORA', '(주)마우스 프로모션'])
add(3, 0, 256, [196], ['나카가와 아쓰토모'])
add(3, 0, 256, [245], ['스즈키 야스시'])
add(3, 0, 256, [293, 325, 357], ['나카가와 아쓰토모', '스즈키 야스시', '스가나미 히데유키'])
add(3, 0, 256, [405, 437], ['핫토리 유리에', '마쓰시타 신고'])
add(3, 256, 512, [197, 229], ['마에가와 마사토', '야마가미 히토시'])
add(3, 256, 512, [277], ['이와타 사토루'])
add(3, 256, 512, [324, 356, 388], ['가와노 나리오', '이토 다카시', '오쿠보 게이스케'])   # 川野 成央: 사용자 확인 읽기(Kawano Nario)
add(3, 256, 512, [436], ['오야마 다케히로'])
# M_STAF04 : 디버그 / 협력사
add(4, 0, 512, [20], ['와타나베 나오키'])
pairs = [('시바야마 야스노리', '이토 아키라'), ('다케우치 아유무', '다케다 히로야'),
         ('사와다 다쓰로', '아사이 미쓰토시'), ('아다치 신고', '히라오 도모히로'),
         ('고야마 겐토', '야마자키 료타'), ('이케다 다케시', '구사카베 다다시'),
         ('미나미자키 도모히로', '하야시 료타로')]
for i, (a, b) in enumerate(pairs):
    y = 68 + 32 * i
    L.append((4, 96, 256, y, y + 23, a)); L.append((4, 256, 416, y, y + 23, b))
L.append((4, 96, 256, 292, 315, '니와 다카시'))
add(4, 0, 512, [340, 388], ['마리오 클럽(주)', '(주)디지털 하츠'])
# M_STAF05 : 노래
add(5, 0, 512, [37], ['「파괴」'])
add(5, 262, 512, [69], [('right', '마자와 에이지')])
add(5, 0, 512, [165], ['「그 시절로」'])
add(5, 262, 512, [197, 229], [('right', '마자와 에이지'), ('right', '마자와 에이지')])
add(5, 262, 512, [261], [('right', '고세키 야스시')])
add(5, 0, 512, [325], ['「그 시절로」'])
add(5, 262, 512, [357, 389], [('right', '마자와 에이지'), ('right', '마자와 에이지')])
add(5, 262, 512, [421], [('right', '고세키 야스시')])

_f = {}
def font(px):
    if px not in _f:
        f = fontgen.make_font(FONT, px); f.set_variation_by_axes([WEIGHT]); _f[px] = f
    return _f[px]


def text_mask(txt, px):
    f = font(px); ref = f.getbbox('한')
    tr = TRACK if px >= NAME_PX else 0.5
    w = int(sum(f.getlength(c) for c in txt) + tr * SS * len(txt)) + 4 * SS
    im = Image.new('L', (w, 30 * SS)); d = ImageDraw.Draw(im); x = 2 * SS
    for c in txt:
        d.text((x, 4 * SS - ref[1]), c, font=f, fill=255); x += f.getlength(c) + tr * SS
    im = im.crop((0, 0, int(x - tr * SS) + 2 * SS, im.height))
    ink_top = 4; ink_h = (ref[3] - ref[1]) / SS
    return im, ink_top, ink_h


def draw(I, A, x, ytop, txt, px, anchor='c', maxw=None):
    """(x, 잉크 윗선 ytop)에 txt를 원본 스타일(흰 글자+검은 외곽선+그림자)로 그린다."""
    im, it, ih = text_mask(txt, px)
    wpx = im.width / SS
    if maxw and wpx > maxw:          # 넘치면 가로로 눌러 맞춘다
        im = im.resize((int(maxw * SS), im.height), Image.LANCZOS); wpx = maxw
    if anchor == 'c': x0 = x - wpx / 2
    elif anchor == 'r': x0 = x - wpx
    else: x0 = x
    X0 = int(np.floor(x0)); Y0 = int(round(ytop - it))
    Wc = int(np.ceil(wpx)) + 6; Hc = im.height // SS + 4
    canv = Image.new('L', (Wc * SS, Hc * SS)); canv.paste(im, (int((x0 - X0) * SS), 0))
    b = np.asarray(canv, np.float32) / 255
    o = np.asarray(canv.filter(ImageFilter.MaxFilter(2 * SS + 1)), np.float32) / 255
    s = np.roll(np.roll(o, SS, 0), SS, 1)
    dn = lambda a: a.reshape(Hc, SS, Wc, SS).mean(axis=(1, 3))
    b, o, s = dn(b), dn(o), dn(s)
    al = np.maximum.reduce([b, o, s * 0.8]); inten = np.where(al > 0, np.clip(b / np.maximum(al, 1e-6), 0, 1), 0)
    ys, xs = slice(Y0, Y0 + Hc), slice(X0, X0 + Wc)
    Ar = A[ys, xs] / 15; Ir = I[ys, xs] / 15
    na = al + Ar * (1 - al)
    ni = (inten * al + Ir * Ar * (1 - al)) / np.maximum(na, 1e-6)
    A[ys, xs] = np.round(na * 15); I[ys, xs] = np.round(ni * 15)


def build(arc):
    for t in range(1, 6):
        name = f'M_STAF0{t}'
        off, w, h, fmt = gxenc.tex_info(arc, name)
        img = gxtex.decode(bytes(arc[off:]), w, h, fmt)
        I = (img[:, :, 0].astype(np.int32) // 17).astype(np.float32); A = (img[:, :, 3].astype(np.int32) // 17).astype(np.float32)
        for (tt, x0, x1, y0, y1, it) in L:
            if tt != t: continue
            if isinstance(it, tuple) and it[0] == 'right':
                A[y0 - 2:y1 + 3, 268:x1] = 0; I[y0 - 2:y1 + 3, 268:x1] = 0
                draw(I, A, 272, y0 + 3, it[1], NAME_PX, 'l', maxw=x1 - 276)
            elif isinstance(it, tuple) and it[0] == 'voice':
                A[y0 - 2:y1 + 3, x0:x1] = 0; I[y0 - 2:y1 + 3, x0:x1] = 0
                draw(I, A, 128, y0 + 8, it[1], ROLE_PX, 'r', maxw=118)
                draw(I, A, 136, y0 + 8, '/', ROLE_PX, 'c')
                draw(I, A, 146, y0 + 3, it[2], NAME_PX, 'l', maxw=x1 - 150)
            else:
                A[y0 - 2:y1 + 3, x0:x1] = 0; I[y0 - 2:y1 + 3, x0:x1] = 0
                draw(I, A, (x0 + x1) / 2, y0 + 3, it, NAME_PX, 'c', maxw=x1 - x0 - 8)
        raw = fontgen.encode_ia4(np.clip(I, 0, 15).astype(np.uint8), np.clip(A, 0, 15).astype(np.uint8))
        arc[off:off + len(raw)] = raw


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    arc = bytearray(open(src, 'rb').read()); build(arc); open(dst, 'wb').write(arc)
