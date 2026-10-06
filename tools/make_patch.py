"""배포용 패치 만들기: 추출 → 빌드 → 원본 배치 유지 ISO → xdelta → 적용 결과 검증.
사용법: python tools/make_patch.py 1.0"""
import os, sys, shutil, subprocess, hashlib, zlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import paths
from paths import ROOT, WORK, ORIG, EXTRACT, ISO_DATA, CHANGED


def run(args, **kw):
    subprocess.run(args, check=True, **kw)


def hashes(path):
    crc = 0; md5 = hashlib.md5(); sha1 = hashlib.sha1(); sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(1 << 24)
            if not b: break
            crc = zlib.crc32(b, crc); md5.update(b); sha1.update(b); sha256.update(b)
    return dict(size=os.path.getsize(path), crc32=f'{crc:08X}', md5=md5.hexdigest(),
                sha1=sha1.hexdigest(), sha256=sha256.hexdigest())


def prepare():
    """work/iso_all(전체 파티션)과 work/orig(바뀌는 파일 원본)를 준비한다."""
    os.makedirs(WORK, exist_ok=True)
    if not os.path.isdir(ISO_DATA):
        print('일본판 ISO 추출 중...')
        jp = os.path.relpath(paths.jp_iso(), ROOT)
        run([os.path.relpath(paths.wit(), ROOT), 'x', jp, os.path.relpath(EXTRACT, ROOT), '--psel', 'ALL', '-q'], cwd=ROOT)
        if os.path.isdir(ORIG): shutil.rmtree(ORIG)
    if not os.path.isdir(ORIG):
        os.makedirs(ORIG)
        for rel in CHANGED:
            shutil.copyfile(os.path.join(ISO_DATA, rel), os.path.join(ORIG, os.path.basename(rel)))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2:
        raise SystemExit('사용법: python tools/make_patch.py <버전>')
    ver = sys.argv[1]
    prepare()
    import build, inplace
    build.main()
    out_iso = os.path.join(WORK, 'SinAndPunishment2_KO.iso')
    inplace.main(out_iso)
    os.makedirs(os.path.join(ROOT, 'release'), exist_ok=True)
    patch = os.path.join(ROOT, 'release', f'R2VJ_KPatch_v{ver}.xdelta')
    jp = paths.jp_iso(); xd = paths.xdelta3()
    rel = lambda p: os.path.relpath(p, ROOT)   # 패치 헤더에 절대경로(사용자 폴더명)가 남지 않게 상대경로로 넘긴다
    print('xdelta 생성 중...')
    run([xd, '-e', '-9', '-f', '-B', '1073741824', '-s', rel(jp), rel(out_iso), rel(patch)], cwd=ROOT)
    print('적용 결과 검증 중...')
    check = os.path.join(WORK, 'applied_check.iso')
    run([xd, '-d', '-f', '-s', rel(jp), rel(patch), rel(check)], cwd=ROOT)
    a, b = hashes(check), hashes(out_iso)
    os.remove(check)
    if a != b:
        raise SystemExit('검증 실패: xdelta 적용 결과가 빌드 결과와 다릅니다.')
    print('패치:', patch, os.path.getsize(patch), '바이트')
    for name, h in (('원본', hashes(jp)), ('결과', b)):
        print(name, h)


if __name__ == '__main__':
    main()
