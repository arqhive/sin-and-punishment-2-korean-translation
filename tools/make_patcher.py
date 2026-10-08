"""배포용 파일 단위 패처 만들기 (disc-file-patcher 방식).
빌드한 뒤 바뀐 게임 파일 4개마다 원본과의 xdelta 차분을 만들고, 사용자용 패처(패치하기.bat + patch.ps1)와
wit·xdelta3 를 한 폴더와 zip 으로 묶는다. ISO 통째 xdelta와 달리 덤프·변환 형태(정본 ISO, WBFS,
WBFS에서 변환한 ISO 등)가 달라 MD5가 달라도 게임 파일만 같으면 적용된다.
사용: python tools/make_patcher.py <버전>
결과: release/R2VJ_KPatch_v<버전>/ 과 같은 이름의 .zip (둘 다 git 제외, zip 은 릴리즈에 첨부)"""
import hashlib, os, shutil, subprocess, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import paths
from paths import ROOT, ORIG, ISO_DATA, CHANGED

GAME_ID = 'R2VJ01'
TITLE = '죄와 벌 우주의 후계자'
RESULT = f'Tsumi to Batsu - Sora no Koukeisha (Korean) [{GAME_ID}]'
WIT_FILES = ('bin/wit.exe', 'bin/cygwin1.dll', 'bin/cygz.dll', 'bin/cygcrypto-1.1.dll', 'bin/cygncursesw-10.dll')


def md5(b):
    return hashlib.md5(b).hexdigest()


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2:
        raise SystemExit('사용법: python tools/make_patcher.py <버전>')
    name = f'R2VJ_KPatch_v{sys.argv[1]}'
    rel_dir = os.path.join(ROOT, 'release')
    out = os.path.join(rel_dir, name)

    import make_patch, build
    make_patch.prepare()
    build.main()   # 바뀐 파일 4개를 work/iso_all/DATA 에 쓴다(원본은 work/orig)

    xd = os.path.abspath(paths.xdelta3())
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, 'data'))
    lines = []
    for i, rel in enumerate(CHANGED):
        old = os.path.join(ORIG, os.path.basename(rel)); new = os.path.join(ISO_DATA, *rel.split('/'))
        a, b = open(old, 'rb').read(), open(new, 'rb').read()
        if a == b:
            continue
        patch = f'{i:03d}.xdelta'
        # -A= : 차분 헤더에 원본·결과 파일 경로(PC 사용자 폴더명)를 남기지 않는다
        subprocess.run([xd, '-e', '-f', '-9', '-S', 'djw', '-A=', '-s', old, new, os.path.join(out, 'data', patch)], check=True)
        # 모드, 차분 파일, 경로, 원본 MD5, 결과 MD5
        lines.append('\t'.join(('raw', patch, rel, md5(a), md5(b))))
    with open(os.path.join(out, 'data', 'manifest.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    with open(os.path.join(out, 'data', 'config.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'id={GAME_ID}\ntitle={TITLE}\nresult={RESULT}\n')

    pdir = os.path.join(ROOT, 'patcher')
    for f in os.listdir(pdir):
        shutil.copy2(os.path.join(pdir, f), os.path.join(out, f))
    shutil.copy2(os.path.join(rel_dir, 'README_한국어.txt'), os.path.join(out, 'README_한국어.txt'))
    wit_root = os.path.dirname(os.path.dirname(os.path.abspath(paths.wit())))   # .../wit-v3.05a-.../
    os.makedirs(os.path.join(out, 'bin'))
    for f in WIT_FILES:
        shutil.copy2(os.path.join(wit_root, *f.split('/')), os.path.join(out, 'bin', os.path.basename(f)))
    shutil.copy2(os.path.join(wit_root, 'gpl-2.0.txt'), os.path.join(out, 'bin', 'wit-gpl-2.0.txt'))
    shutil.copy2(xd, os.path.join(out, 'bin', 'xdelta3.exe'))

    zpath = out + '.zip'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for dp, _, fs in os.walk(out):
            for f in sorted(fs):
                p = os.path.join(dp, f)
                z.write(p, os.path.join(name, os.path.relpath(p, out)))
    size = sum(os.path.getsize(os.path.join(out, 'data', f)) for f in os.listdir(os.path.join(out, 'data')))
    print(f'파일 {len(lines)}개, 차분 합계 {size / 1e6:.2f} MB, zip {os.path.getsize(zpath) / 1e6:.2f} MB')
    print('패처:', out)


if __name__ == '__main__':
    main()
