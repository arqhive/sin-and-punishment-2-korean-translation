"""기준 경로와 외부 도구 위치."""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

WORK = os.path.join(ROOT, 'work')
ORIG = os.path.join(WORK, 'orig')                 # 원본에서 뽑은 바뀌는 파일 4개
EXTRACT = os.path.join(WORK, 'iso_all')           # wit 로 푼 전체 파티션 (DATA 가 빌드 출력 자리)
ISO_DATA = os.path.join(EXTRACT, 'DATA')
KO_JSON = os.path.join(ROOT, 'translation', 'ko.json')
FONTS = os.path.join(HERE, 'fonts')

JP_ISO_NAME = 'Tsumi to Batsu - Sora no Koukeisha (Japan).iso'
CHANGED = ['sys/main.dol', 'files/MsgFont.brfnt', 'files/texture.arc', 'files/opening.bnr']


def jp_iso():
    """일본판 ISO: 환경 변수 TSUMI2_JP_ISO → 저장소 루트 → iso/ 순서로 찾는다."""
    for p in (os.environ.get('TSUMI2_JP_ISO'), os.path.join(ROOT, JP_ISO_NAME), os.path.join(ROOT, 'iso', JP_ISO_NAME)):
        if p and os.path.isfile(p):
            return p
    raise SystemExit(f'일본판 ISO를 찾을 수 없습니다. 저장소 루트에 "{JP_ISO_NAME}"를 두거나 TSUMI2_JP_ISO로 지정하세요.')


def tool(env, exe, local):
    """외부 도구: 환경 변수 → tools/bin → PATH."""
    for p in (os.environ.get(env), os.path.join(HERE, 'bin', *local)):
        if p and os.path.isfile(p):
            return p
    p = shutil.which(exe)
    if p:
        return p
    raise SystemExit(f'{exe}를 찾을 수 없습니다. PATH에 두거나 환경 변수 {env}로 지정하세요.')


def wit():
    return tool('WIT', 'wit', ('wit-v3.05a-r8638-cygwin64', 'bin', 'wit.exe'))


def xdelta3():
    return tool('XDELTA3', 'xdelta3', ('xdelta3.exe',))
