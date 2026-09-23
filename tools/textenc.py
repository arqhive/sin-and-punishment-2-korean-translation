"""translation/ko.json -> main.dol 문자열 인코딩.
한글 음절은 SJIS 한자 영역 코드(0x889F~)를 순서대로 할당하고, 폰트에 같은 코드로 글리프를 넣는다."""
import json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load_text(path=os.path.join(ROOT, 'translation', 'ko.json')):
    doc = json.load(open(path, encoding='utf8'))
    return [(int(x['id'], 16), x['ko']) for x in doc['system']]


def load_slots():
    doc = json.load(open(os.path.join(ROOT, 'translation', 'ko.json'), encoding='utf8'))
    return {int(x['id'], 16): x['slot'] for x in doc['system']}


def is_hangul(ch):
    return 0xAC00 <= ord(ch) <= 0xD7A3


def code_iter():
    """한글 전용 코드: SJIS 사용자 정의 영역 0xF040~0xFCFC (게임 판별 범위 81-9F, E0-FC 안).
    원래 가나·한자 코드와 겹치지 않아, 번역되지 않은 일본어가 엉뚱한 한글로 보이는 일이 없다."""
    lead, trail = 0xF0, 0x40
    while True:
        yield lead << 8 | trail
        trail += 1
        if trail == 0x7F:
            trail += 1
        if trail > 0xFC:
            lead += 1
            trail = 0x40
            assert lead <= 0xFC


def build_map(entries):
    chars = sorted({c for _, t in entries for c in t if is_hangul(c)})
    it = code_iter()
    return {c: next(it) for c in chars}


NO_HALFWIDTH = set('#$&,:=?@[]^`')  # '_'는 NAND 디버그 문구 전용이라 그대로 둔다
TOKEN = re.compile(r'\{([0-9A-F]{2})\}')


def join_space(txt):
    """하단 도움말 줄은 줄바꿈을 공백 없이 이어 붙이므로, 글줄 사이 줄바꿈 앞에 공백을 넣는다."""
    # 첫 줄바꿈(메뉴 제목과 설명 사이)은 도움말 줄에 포함되지 않으므로 그대로 둔다
    i = txt.find('\n')
    if i < 0:
        return txt
    return txt[:i + 1] + re.sub(r'(?<=[^\n ])\n(?=[^\n])', ' \n', txt[i + 1:])


def encode(txt, hmap):
    txt = join_space(txt)
    b = bytearray()
    i = 0
    while i < len(txt):
        m = TOKEN.match(txt, i)
        if m:
            b.append(int(m.group(1), 16)); i = m.end(); continue
        c = txt[i]
        if is_hangul(c):
            v = hmap[c]; b += bytes([v >> 8, v & 0xFF])
        elif c in NO_HALFWIDTH:  # 원본 폰트에 반각 글리프가 없는 기호는 전각으로
            b += chr(ord(c) + 0xFEE0).encode('cp932')
        elif ord(c) < 0x80:
            b.append(ord(c))
        else:
            b += c.encode('cp932')
        i += 1
    return bytes(b)


def encode_all():
    ents = load_text(); slots = load_slots(); hmap = build_map(ents)
    res = []; errs = []
    for off, t in ents:
        enc = encode(t, hmap)
        slot = slots[off]
        if len(enc) + 1 > slot:
            errs.append((off, len(enc) + 1, slot, t))
        res.append((off, slot, enc))
    return res, hmap, errs


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    res, hmap, errs = encode_all()
    print(len(res), 'strings,', len(hmap), 'hangul syllables')
    for off, n, s, t in errs:
        print(f'OVER {off:#x} need {n} slot {s}: {t!r}')
    used = sorted({c for _, t in load_text() for c in t if not is_hangul(c) and ord(c) >= 0x80})
    print('non-ascii non-hangul chars:', ''.join(used))
