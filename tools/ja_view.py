"""번역 검수용: translation/ko.json 에 일본어 원문을 붙여 work/ja/script_with_ja.json 으로 쓴다.
원문은 게임 데이터라 저장소에 넣지 않는다. 메뉴 문자열은 원본 main.dol 에서 읽고,
자막 원문은 이미지라서 직접 옮겨 적은 work/ja/subs_ja_all.txt(`id<TAB>원문`)가 있으면 붙인다."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from paths import ROOT, ORIG, KO_JSON


def dec(s):
    o = ''; i = 0
    while i < len(s):
        c = s[i]
        if c == 1: o += '{01}'; i += 1
        elif c == 0xFF: o += '{FF}'; i += 1
        elif c >= 0x81: o += s[i:i + 2].decode('cp932'); i += 2
        else: o += chr(c); i += 1
    return o


def main():
    dol = open(os.path.join(ORIG, 'main.dol'), 'rb').read()
    d = json.load(open(KO_JSON, encoding='utf8'))
    ja = {}
    p = os.path.join(ROOT, 'work', 'ja', 'subs_ja_all.txt')
    if os.path.isfile(p):
        for line in open(p, encoding='utf8'):
            k, t = line.rstrip('\r\n').split('\t', 1); ja[k] = t.replace('\\n', '\n')
    for x in d['system']:
        o = int(x['id'], 16); x['ja'] = dec(dol[o:dol.index(b'\0', o)])
    for x in d['subtitles']:
        x['ja'] = ja.get(x['id'], '')
    out = os.path.join(ROOT, 'work', 'ja', 'script_with_ja.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(d, open(out, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(out)


if __name__ == '__main__':
    main()
