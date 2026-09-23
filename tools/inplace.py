"""원본 ISO의 배치를 그대로 두고 바뀐 파일만 교체해 작은 xdelta가 나오는 ISO를 만든다.
1) wit로 원본을 배치 유지 복호화(work/dec.iso)
2) 바뀐 파일을 원래 자리에 덮어쓰기(작은 파일은 0으로 채움)
3) 바뀐 2MB 그룹의 H0/H1/H2 해시를 직접 계산해 기록
4) wit로 암호화(work/R.iso) — 해시는 다시 계산하지 않으므로 3)의 값이 그대로 쓰인다
5) 원본 ISO 복사본에 바뀐 그룹만 R에서 옮기고, H3 표·TMD 해시 갱신 후 가짜 서명
사용법: python tools/inplace.py 출력.iso
cygwin wit는 한글이 든 절대경로를 못 읽으므로 ROOT 기준 상대경로로 넘긴다."""
import os, sys, hashlib, shutil, subprocess, struct
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import wiidisc, paths
from paths import ROOT
from wiidisc import CL, HDR, DATA, GROUP

POFF = 0xF800000
FILES = {   # ISO 안 경로 : 새 파일 (ROOT 기준)
    'sys/main.dol': 'work/iso_all/DATA/sys/main.dol',
    'files/MsgFont.brfnt': 'work/iso_all/DATA/files/MsgFont.brfnt',
    'files/texture.arc': 'work/iso_all/DATA/files/texture.arc',
    'files/opening.bnr': 'work/iso_all/DATA/files/opening.bnr',
}
sha1 = lambda b: hashlib.sha1(b).digest()


def wit(*args):
    subprocess.run([os.path.relpath(paths.wit(), ROOT), *args, '-q'], check=True, cwd=ROOT)


def main(out_iso):
    os.chdir(ROOT)
    jp = paths.jp_iso(); jp_rel = os.path.relpath(jp, ROOT)
    print('1) 복호화'); wit('copy', jp_rel, 'work/dec.iso', '--psel', 'WHOLE', '--enc', 'DECRYPT', '--overwrite')
    f = open('work/dec.iso', 'r+b'); P = wiidisc.Part(f, POFF); fs = P.files()
    groups = set()
    print('2) 파일 교체')
    for k, p in FILES.items():
        off, sz = fs[k]
        if sz is None: sz = os.path.getsize(os.path.join('work', 'orig', 'main.dol'))
        d = open(p, 'rb').read()
        if len(d) > sz: raise SystemExit(f'{k}: 원본 자리({sz})보다 큼({len(d)})')
        d += b'\0' * (sz - len(d))
        P.write_data(off, d)
        for c in range(off // DATA, (off + sz - 1) // DATA + 1): groups.add(c // GROUP)
        print(f'   {k} {sz} bytes')
    ncl = P.data_size // CL
    print('3) 해시 재계산:', len(groups), '그룹')
    h3 = {}
    for g in sorted(groups):
        cls = range(g * GROUP, min((g + 1) * GROUP, ncl))
        h0 = {}; data = {}
        for c in cls:
            f.seek(P.cluster_pos(c) + HDR); d = f.read(DATA); data[c] = d
            h0[c] = b''.join(sha1(d[i * 0x400:(i + 1) * 0x400]) for i in range(31))
        h1 = {}
        for sg in range(8):
            sub = [c for c in cls if (c - g * GROUP) // 8 == sg]
            h1[sg] = b''.join(sha1(h0[c]) for c in sub).ljust(0xA0, b'\0')
        h2 = b''.join(sha1(h1[sg]) for sg in range(8))
        for c in cls:
            sg = (c - g * GROUP) // 8
            hdr = h0[c] + b'\0' * 0x14 + h1[sg] + b'\0' * 0x20 + h2 + b'\0' * 0x20
            assert len(hdr) == HDR
            f.seek(P.cluster_pos(c)); f.write(hdr)
        h3[g] = sha1(h2)
    f.close()
    print('4) 암호화'); wit('copy', 'work/dec.iso', 'work/R.iso', '--psel', 'WHOLE', '--enc', 'ENCRYPT', '--overwrite')
    print('5) 합치기'); shutil.copyfile(jp, out_iso)
    F = open(out_iso, 'r+b'); R = open('work/R.iso', 'rb')
    for g in sorted(groups):
        a = P.cluster_pos(g * GROUP); n = min(GROUP, ncl - g * GROUP) * CL
        R.seek(a); F.seek(a); F.write(R.read(n))
    # H3 표(평문)
    F.seek(POFF + P.h3_off); H3 = bytearray(F.read(0x18000))
    for g, v in h3.items(): H3[g * 20:g * 20 + 20] = v
    F.seek(POFF + P.h3_off); F.write(H3)
    # TMD: 콘텐츠 해시 갱신 + 가짜 서명(서명 0, 0x1C8~ 값을 바꿔 SHA1 첫 바이트 00)
    F.seek(POFF + P.tmd_off); tmd = bytearray(F.read(P.tmd_size))
    tmd[0x4:0x104] = b'\0' * 0x100
    tmd[0x1F4:0x208] = sha1(bytes(H3))
    for i in range(1 << 32):
        struct.pack_into('>I', tmd, 0x1C8, i)
        if sha1(bytes(tmd[0x140:]))[0] == 0: break
    F.seek(POFF + P.tmd_off); F.write(tmd)
    F.close(); R.close()
    os.remove('work/R.iso'); os.remove('work/dec.iso')
    print('완료:', out_iso)


if __name__ == '__main__':
    main(sys.argv[1])
