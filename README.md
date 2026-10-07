# 죄와 벌 우주의 후계자 (Wii) 한글 패치

*Sin and Punishment: Star Successor* (Wii, 일본판 `R2VJ01`) 비공식 한국어 팬 패치입니다.
대사는 일본어판 원문을 기준으로 번역했습니다.

**제작: arqhive** · **최신 버전: [v1.0.2](../../releases/tag/v1.0.2)**

한식구 카페 하스피님의 한글 패치([원본 글](https://cafe.naver.com/hansicgu/35057))를 활용해 제작했습니다. 번역을 다시 다듬고, 폰트와 자막을 새로 그리고, 그래픽 한글화 범위를 넓혔습니다.

- 메뉴, 옵션, 튜토리얼, 경고·오류 메시지 등 게임 텍스트 305개를 한글화했습니다.
- 컷신 자막 270줄을 한글화했습니다. 자막은 이미지라 39장을 새로 그렸습니다.
- 스테이지 이름, Wii 스트랩·재퍼 주의 화면, 엔딩 스태프롤, 타이틀 로고, Wii 메뉴 배너·아이콘을 한글화했습니다.
- 한글 글꼴은 원본 느낌에 맞춰 골랐습니다. 메뉴·설명문은 나눔고딕, 컷신 자막은 둘기마요(원본처럼 기울임), 스테이지 이름은 본명조, 나머지 그래픽은 Pretendard입니다.
- **파일 단위 패처라 덤프·변환 형태(ISO, WBFS 등)가 달라도 적용되고, 패치 크기는 약 6MB입니다.**

> 이 저장소에는 **게임 데이터(롬·디스크 이미지, 추출한 원문 대사, 그래픽, 스크린샷)가 들어 있지 않습니다.**
> 패치를 만들거나 적용하려면 본인이 소유한 게임에서 직접 덤프한 원본이 필요합니다.

## 사용자용: 패치 적용

### 준비물

- 일본판 디스크 이미지(게임 ID `R2VJ01`). 북미·유럽판에는 적용할 수 없습니다.
  - ISO, WBFS 모두 됩니다. 아래 지원 형식을 참고하세요.
  - 하스피님 한글판처럼 이미 패치한 이미지에는 적용할 수 없습니다. 원본 일본판을 쓰세요.
- Windows 10 이상. 패처에 필요한 도구(wit, xdelta3)가 들어 있어 따로 설치할 것이 없습니다.
- 빈 공간 약 6GB(풀어 둔 파일과 결과 이미지).

### 지원 형식

| 원본 | 적용 | 결과 |
|---|---|---|
| ISO (정본 덤프, WBFS에서 변환한 ISO 등) | ○ | ISO |
| WBFS | ○ | WBFS |
| CISO, WIA, WDF | ○ | ISO |
| RVZ | × | Dolphin에서 ISO로 변환한 뒤 적용 |
| NKit | × | NKit 도구로 원본 ISO로 복원한 뒤 적용 |

덤프·변환 방법에 따라 MD5가 달라도 게임 파일만 같으면 적용됩니다.

### 적용 방법

1. [배포 페이지](../../releases/latest)에서 `R2VJ_KPatch_v1.0.2.zip`을 받아 압축을 풉니다.
2. 원본 이미지(ISO 또는 WBFS)를 `패치하기.bat` 위에 끌어다 놓습니다.
   - 원본을 `패치하기.bat`과 같은 폴더에 넣고 더블클릭해도 됩니다.
   - 폴더에 이미지가 여러 개 있으면 경로를 물어봅니다. 파일을 창에 끌어다 놓고 Enter를 누르세요.
3. 창에 `완료`가 나올 때까지 기다립니다. 보통 1분 안팎이 걸립니다. 진행 중에는 창을 닫지 마세요.
4. 원본과 같은 폴더에 결과 파일이 생깁니다. 원본은 바뀌지 않습니다.
   - ISO 원본 → `Tsumi to Batsu - Sora no Koukeisha (Korean) [R2VJ01].iso`
   - WBFS 원본 → `Tsumi to Batsu - Sora no Koukeisha (Korean) [R2VJ01].wbfs`

#### 결과 형식을 바꾸고 싶을 때

ISO 원본에서 WBFS를 만들거나 그 반대로 하려면, 패처 폴더에서 PowerShell을 열고 결과 파일 이름을 원하는 확장자로 지정합니다.

```
powershell -ExecutionPolicy Bypass -File patch.ps1 "원본.iso" "결과.wbfs"
```

#### 실행 방법별 안내

- **Dolphin**: 결과 ISO나 WBFS를 게임 목록 폴더에 넣거나 파일을 직접 엽니다.
- **Wii·Wii U vWii (USB Loader GX)**: FAT32 USB는 4GB가 넘는 파일을 담지 못하므로 **WBFS를 권합니다**. `wbfs/Tsumi to Batsu - Sora no Koukeisha (Korean) [R2VJ01]/R2VJ01.wbfs`처럼 폴더와 파일 이름을 맞춰 넣습니다. ISO를 쓰려면 NTFS USB를 쓰세요.

#### 오류가 날 때

| 메시지 | 원인·해결 |
|---|---|
| 죄와 벌 우주의 후계자(R2VJ01)가 아닙니다 | 북미·유럽판이거나 다른 게임입니다. 일본판만 됩니다. |
| 원본 게임 파일이 다릅니다 | 이미 패치한 이미지거나 손상된 덤프입니다. 원본 일본판에 적용하세요. |
| RVZ는 지원하지 않습니다 | Dolphin 게임 목록에서 우클릭 → 파일 변환 → ISO로 바꾼 뒤 다시 실행하세요. |
| wit.exe 실행 실패 | 빈 공간(약 6GB)이 모자라거나 원본 파일이 손상됐습니다. |

패처는 이미지를 풀어 바뀐 게임 파일 4개에만 파일별 차분을 적용하고 다시 묶습니다. 파일마다 적용 전후 MD5를 검사하므로 원본이 맞지 않으면 멈추고 알려 줍니다.
결과 이미지의 MD5는 원본 덤프에 따라 달라질 수 있지만 게임 내용은 같습니다.

자세한 방법은 [`README_한국어.txt`](release/README_한국어.txt)를 참고하세요.

### 실행 환경

- **확인함**: Dolphin, Wii U vWii.

### 알려진 문제

- Wii 메뉴에 표시되는 채널 이름은 일본어 그대로입니다. 일본판 본체 글꼴에 한글이 없기 때문입니다.
- 메뉴 버튼, 점수 표시, 결과 화면 같은 영어 그래픽은 일본판에서도 영어라 그대로 두었습니다.
- 유럽판에만 있는 게임 중 음성 자막과 노래 가사 자막은 일본판에 해당 데이터가 없어 넣을 수 없습니다.

## 개발자용: 직접 빌드

### 요구 사항

- Python 3.11 이상. `pip install -r requirements.txt`로 numpy, Pillow, opencv-python을 설치합니다.
- 일본판 ISO. 저장소 루트나 `iso/`에 두거나 환경 변수 `TSUMI2_JP_ISO`로 지정합니다.
- [Wiimms ISO Tools](https://wit.wiimm.de/)(`wit`). PATH에 두거나 환경 변수 `WIT`로 지정합니다. `tools/bin/`에 풀어 두어도 됩니다.
- xdelta3 3.1.0. PATH에 두거나 환경 변수 `XDELTA3`로 지정합니다. `tools/bin/xdelta3.exe`에 두어도 됩니다.
- 폰트(나눔고딕, 본명조, Pretendard)는 `tools/fonts/`에 들어 있습니다.
- 컷신 자막용 둘기마요는 파일 재배포가 금지라 들어 있지 않습니다. [눈누](https://noonnu.cc/font_page/122)에서 받아 PC에 설치하거나 `tools/fonts/dovemayo_bold.otf`로 두세요.

### 빌드

```bash
# 배포용 패처: 빌드 → 바뀐 파일별 차분 + 패처 스크립트 + wit·xdelta3 → release/R2VJ_KPatch_v1.0.2.zip
python tools/make_patcher.py 1.0.2

# (v1.0.1까지의 방식) 원본 배치를 유지한 ISO와 ISO 통째 xdelta. 특정 원본 ISO에만 맞아 배포에는 쓰지 않음
python tools/make_patch.py 1.0.1
```

처음 실행하면 일본판 ISO를 `work/iso_all/`에 풉니다. 그 뒤 바뀌는 파일 4개(`main.dol`, `MsgFont.brfnt`, `texture.arc`, `opening.bnr`)를 만들고, 원본과의 파일별 xdelta 차분과 사용자용 패처(`patcher/`의 `패치하기.bat`, `patch.ps1`)를 zip으로 묶습니다.
Windows Git Bash에서는 `PYTHONIOENCODING=utf-8`을 붙이세요.

### 번역 수정

- 번역은 [`translation/ko.json`](translation/ko.json)의 `ko` 값을 고칩니다. `system`은 게임 텍스트, `subtitles`는 컷신 자막입니다.
- `system` 항목은 원래 자리에 덮어쓰므로 `slot` 바이트(한글 2, 반각 1, 끝 1)를 넘으면 빌드가 멈춥니다.
- `{01}{FF}…`는 색과 버튼 강조용 제어 코드이고 `%s`는 버튼 이름이 들어가는 자리라 그대로 둡니다.
- 번역되지 않은 일본어 문자열이 남아 있으면 빌드가 멈춥니다.
- 원문을 옆에 두고 보려면 `python tools/ja_view.py`를 실행합니다. 게임 텍스트 원문은 원본 `main.dol`에서 읽어 `work/ja/script_with_ja.json`에 씁니다. 자막 원문은 이미지라 직접 옮겨 적은 `work/ja/subs_ja_all.txt`가 있을 때만 붙습니다.
- 그림 글씨는 [`tools/gfx_stage.py`](tools/gfx_stage.py)(스테이지 이름), [`tools/gfx_strap.py`](tools/gfx_strap.py)(주의 화면), [`tools/gfx_staff.py`](tools/gfx_staff.py)(스태프롤), [`tools/gfx_logo.py`](tools/gfx_logo.py)(타이틀 로고) 안의 문자열을 고칩니다.
- 타이틀 로고와 Wii 메뉴 배너·아이콘은 [`tools/assets/`](tools/assets)의 완성 PNG를 그대로 넣습니다. 크기를 바꾸지 말고 같은 이름으로 교체하세요. 파일이 없으면 `gfx_logo.py`와 `banner.py`가 코드로 그립니다.
- 그래픽 전후 비교 이미지는 `python tools/gfx_compare.py work/iso_all/DATA/files/texture.arc work/cmp.png M_BG02`처럼 만듭니다.

### 폴더 구조

```
tools/             빌드·패치 도구 (paths.py가 기준 경로와 외부 도구를 찾음)
patcher/           사용자용 패처 스크립트(패치하기.bat, patch.ps1)
  fonts/           나눔고딕·본명조·Pretendard 폰트와 OFL 라이선스
  assets/          타이틀 로고·Wii 메뉴 배너 완성 이미지
  bin/             (git 제외) wit, xdelta3
translation/
  ko.json          번역 (게임 텍스트·컷신 자막, 한국어만)
docs/
  TECHNICAL.md     파일 포맷과 한글화 방식
  releases/        릴리즈 노트 사본
release/           사용자 설명서(패처 zip은 릴리즈에만 첨부)
work/              (git 제외) 추출 원본·원문·빌드 결과
```

### 기술 문서

파일 포맷과 한글화 방식은 [`docs/TECHNICAL.md`](docs/TECHNICAL.md)에 정리했습니다.

## 변경 내역

전체 내역은 [`CHANGELOG.md`](CHANGELOG.md)에 있습니다.

## 크레딧·라이선스

- 이 저장소의 도구 코드, 한국어 번역문, 문서: [MIT License](LICENSE) (© 2026 arqhive).
- 원본 한글 패치: 한식구 카페 하스피님 ([원본 글](https://cafe.naver.com/hansicgu/35057)).
- 나눔고딕: NAVER, [SIL Open Font License 1.1](tools/fonts/OFL-NanumGothic.txt).
- 본명조(Noto Serif KR): Google·Adobe, [SIL Open Font License 1.1](tools/fonts/OFL-NotoSerifKR.txt).
- Pretendard: 길형진, [SIL Open Font License 1.1](tools/fonts/OFL.txt).
- 둘기마요: 둘기마요, [라이선스](https://noonnu.cc/font_page/122)(판매 외 상업 이용·임베딩 가능, 파일 재배포 금지). 컷신 자막 이미지에만 쓰고 파일은 넣지 않았습니다.
- 패처에 동봉하는 [wit](https://wit.wiimm.de/)은 GPL-2.0, [xdelta3](https://github.com/jmacd/xdelta)는 Apache-2.0입니다.

## 면책

비공식 팬 번역이며 Nintendo와 관련이 없습니다. 「죄와 벌 우주의 후계자」 관련 상표·저작권은 Nintendo와 트레저에 있습니다.
패치를 적용한 게임 파일의 배포를 금지합니다.
