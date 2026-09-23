"""원본 파일(work/orig) → 한글 적용 → work/iso_all/DATA 에 바뀐 파일 4개를 쓴다.
ISO와 패치는 tools/make_patch.py 가 만든다."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import textenc, fontgen, subgen, gfx_stage, gfx_strap, gfx_staff, gfx_logo, banner, subs
from paths import ORIG, ISO_DATA as ISO_DIR


def check_coverage():
    """main.dol 텍스트 구역에서 가나가 든 문자열이 모두 translation/ko.json 에 있는지 검사한다."""
    a = open(os.path.join(ORIG, 'main.dol'), 'rb').read()
    covered = {o for o, _ in textenc.load_text()}
    ignore = {0x2f53aa, 0x2f545e, 0x2f546a, 0x2f551e}   # 가나 문자표(데이터)
    miss = []
    for lo, hi in ((0x2c3da0, 0x2d82e0), (0x2d82e0, 0x315440), (0x317680, 0x31a8e0)):
        i = lo
        while i < hi:
            if a[i] == 0: i += 1; continue
            j = a.index(b'\0', i); s = a[i:j]; k = 0; kana = 0; ok = True
            while k < len(s):
                c = s[k]
                if c in (1, 0xFF, 0x0A) or 0x20 <= c < 0x7F: k += 1; continue
                if (0x81 <= c <= 0x84 or 0x88 <= c <= 0x9F or 0xE0 <= c <= 0xEA) and k + 1 < len(s):
                    try: ch = s[k:k + 2].decode('cp932')
                    except UnicodeDecodeError: ok = False; break
                    kana += 'ぁ' <= ch <= 'ヺ' or ch == 'ー'; k += 2; continue
                ok = False; break
            if ok and kana >= 2 and i not in covered and i not in ignore: miss.append(i)
            i = j + 1
    if miss:
        raise SystemExit('번역 누락 문자열: ' + ', '.join(hex(m) for m in miss))


def patch_dol():
    check_coverage()
    res, hmap, errs = textenc.encode_all()
    if errs:
        raise SystemExit(f'슬롯 초과: {[hex(e[0]) for e in errs]}')
    dol = bytearray(open(os.path.join(ORIG, 'main.dol'), 'rb').read())
    for off, slot, enc in res:
        dol[off:off + slot] = enc + b'\0' * (slot - len(enc))
    open(os.path.join(ISO_DIR, 'sys', 'main.dol'), 'wb').write(dol)
    return hmap


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    hmap = patch_dol()
    n = fontgen.build(os.path.join(ORIG, 'MsgFont.brfnt'), os.path.join(ISO_DIR, 'files', 'MsgFont.brfnt'),
                      hmap, fontgen.FONT_PATH, 21)
    print('main.dol, MsgFont.brfnt 적용 (한글', n[0], '자)')
    miss, _ = subgen.build_textures(os.path.join(ORIG, 'texture.arc'), os.path.join(ISO_DIR, 'files', 'texture.arc'))
    if miss:
        raise SystemExit(f'자막 번역 누락: {miss}')
    print('texture.arc 컷신 자막 적용')
    tpath = os.path.join(ISO_DIR, 'files', 'texture.arc')
    arc = bytearray(open(tpath, 'rb').read())
    gfx_stage.build(arc); gfx_strap.build(arc); gfx_staff.build(arc); gfx_logo.build(arc)
    open(tpath, 'wb').write(arc)
    print('그래픽 적용: 스테이지 이름, 주의 화면, 스태프롤, 타이틀 로고')
    banner.build(os.path.join(ORIG, 'opening.bnr'), os.path.join(ISO_DIR, 'files', 'opening.bnr'),
                 subs.load_tex(tpath, 'TITLE_LOGO')[0])
    print('opening.bnr 배너·아이콘 적용')

if __name__ == '__main__':
    main()
