# 죄와 벌 우주의 후계자 (Wii) 한글 패치

*Sin and Punishment: Star Successor* (Wii, 일본판 `R2VJ01`) 비공식 한국어 팬 패치입니다.
대사는 일본어판 원문을 기준으로 번역했습니다.

**제작: arqhive** · **최신 버전: [v1.0](../../releases/tag/v1.0)**

한식구 카페 하스피님의 한글 패치([원본 글](https://cafe.naver.com/hansicgu/35057))를 활용해 제작했습니다. 번역을 다시 다듬고, 폰트와 자막을 새로 그리고, 그래픽 한글화 범위를 넓혔습니다.

- 메뉴, 옵션, 튜토리얼, 경고·오류 메시지 등 게임 텍스트 305개를 한글화했습니다.
- 컷신 자막 270줄을 한글화했습니다. 자막은 이미지라 39장을 새로 그렸습니다.
- 스테이지 이름, Wii 스트랩·재퍼 주의 화면, 엔딩 스태프롤, 타이틀 로고, Wii 메뉴 배너·아이콘을 한글화했습니다.
- 한글 폰트는 Pretendard로 원본 글꼴처럼 외곽선과 그림자를 넣어 그렸습니다.
- **원본과 같은 4.7GB 디스크 크기와 파일 배치를 유지합니다.**

> 이 저장소에는 **게임 데이터(롬·디스크 이미지, 추출한 원문 대사, 그래픽, 스크린샷)가 들어 있지 않습니다.**
> 패치를 만들거나 적용하려면 본인이 소유한 게임에서 직접 덤프한 원본이 필요합니다.

## 사용자용: 패치 적용

### 준비물

- 일본판 ISO. 북미·유럽판에는 적용할 수 없습니다. WBFS·RVZ로 갖고 있다면 Dolphin이나 Wii Backup Manager로 ISO로 바꾼 뒤 적용하세요.
- xdelta 패치 도구. [Delta Patcher](https://github.com/marco-calautti/DeltaPatcher)(GUI)나 [xdelta3](https://github.com/jmacd/xdelta-gpl/releases)(명령줄)를 쓰면 됩니다.

### 적용 방법

1. [배포 페이지](../../releases/latest)에서 `SinAndPunishment2_KO_v1.0.xdelta`를 받습니다.
2. 일본판 원본 ISO에 패치를 적용합니다. 하스피님 한글판 ISO에 덧씌우는 패치가 아닙니다. xdelta3에서는 다음처럼 실행합니다.

   ```
   xdelta3 -d -s "Tsumi to Batsu - Sora no Koukeisha (Japan).iso" SinAndPunishment2_KO_v1.0.xdelta "Tsumi to Batsu - Sora no Koukeisha (Korean).iso"
   ```

3. 결과 파일의 확인값을 아래 표와 비교합니다.

자세한 방법은 [`README_한국어.txt`](release/README_한국어.txt)를 참고하세요.

### 파일 확인값

| 항목 | 원본 일본판 | 패치 적용 결과 (v1.0) |
|---|---|---|
| 크기 | 4,699,979,776 바이트 | 4,699,979,776 바이트 |
| CRC32 | `4780998F` | `B686AB1B` |
| MD5 | `fd9f83599cb9962e3ba8137b19454c1f` | `ec38ddc271137a5eab30f48a61349349` |
| SHA-1 | `cf4225060f76f3d8842a63bcdbe00313bb5cc155` | `ffb251ec8c06bf01f910c6153966a5a30081e001` |
| SHA-256 | `1e9f75a0826902ed0a8cb7094f6e5428ad9619eb485e04e0b4313982a8d60470` | `6f32a42d91167f2a03728d34402539fc0be5f9d06301feae346fd602a31ce28d` |

원본 파일명 예: `Tsumi to Batsu - Sora no Koukeisha (Japan).iso`

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
- xdelta3. PATH에 두거나 환경 변수 `XDELTA3`로 지정합니다.
- 폰트(Pretendard)는 `tools/fonts/`에 들어 있습니다.

### 빌드

```bash
# ISO 추출, 한글 적용, 원본 배치를 유지한 ISO 생성, xdelta 생성, 적용 결과 검증
python tools/make_patch.py 1.0
```

일본판 ISO를 `work/iso_all/`에 풀고, 바뀌는 파일 4개(`main.dol`, `MsgFont.brfnt`, `texture.arc`, `opening.bnr`)를 만든 뒤 원본 ISO의 같은 자리에 덮어씁니다.
바뀐 부분의 파티션 해시만 다시 계산하므로 패치가 작고, 같은 입력이면 결과는 바이트 단위로 같습니다.
Windows Git Bash에서는 `PYTHONIOENCODING=utf-8`을 붙이세요.

### 번역 수정

- 번역은 [`translation/ko.json`](translation/ko.json)의 `ko` 값을 고칩니다. `system`은 게임 텍스트, `subtitles`는 컷신 자막입니다.
- `system` 항목은 원래 자리에 덮어쓰므로 `slot` 바이트(한글 2, 반각 1, 끝 1)를 넘으면 빌드가 멈춥니다.
- `{01}{FF}…`는 색과 버튼 강조용 제어 코드이고 `%s`는 버튼 이름이 들어가는 자리라 그대로 둡니다.
- 번역되지 않은 일본어 문자열이 남아 있으면 빌드가 멈춥니다.
- 원문을 옆에 두고 보려면 `python tools/ja_view.py`를 실행합니다. 게임 텍스트 원문은 원본 `main.dol`에서 읽어 `work/ja/script_with_ja.json`에 씁니다. 자막 원문은 이미지라 직접 옮겨 적은 `work/ja/subs_ja_all.txt`가 있을 때만 붙습니다.
- 그림 글씨는 [`tools/gfx_stage.py`](tools/gfx_stage.py)(스테이지 이름), [`tools/gfx_strap.py`](tools/gfx_strap.py)(주의 화면), [`tools/gfx_staff.py`](tools/gfx_staff.py)(스태프롤), [`tools/gfx_logo.py`](tools/gfx_logo.py)(타이틀 로고) 안의 문자열을 고칩니다.
- 그래픽 전후 비교 이미지는 `python tools/gfx_compare.py work/iso_all/DATA/files/texture.arc work/cmp.png M_BG02`처럼 만듭니다.

### 폴더 구조

```
tools/             빌드·패치 도구 (paths.py가 기준 경로와 외부 도구를 찾음)
  fonts/           Pretendard 폰트와 OFL 라이선스
translation/
  ko.json          번역 (게임 텍스트·컷신 자막, 한국어만)
docs/
  TECHNICAL.md     파일 포맷과 한글화 방식
  releases/        릴리즈 노트 사본
release/           배포용 xdelta 패치와 사용자 설명서
work/              (git 제외) 추출 원본·원문·빌드 결과
```

### 기술 문서

파일 포맷과 한글화 방식은 [`docs/TECHNICAL.md`](docs/TECHNICAL.md)에 정리했습니다.

## 변경 내역

전체 내역은 [`CHANGELOG.md`](CHANGELOG.md)에 있습니다.

## 크레딧·라이선스

- 이 저장소의 도구 코드, 한국어 번역문, 문서: [MIT License](LICENSE) (© 2026 arqhive).
- 원본 한글 패치: 한식구 카페 하스피님 ([원본 글](https://cafe.naver.com/hansicgu/35057)).
- Pretendard: 길형진, [SIL Open Font License 1.1](tools/fonts/OFL.txt).

## 면책

비공식 팬 번역이며 Nintendo와 관련이 없습니다. 「죄와 벌 우주의 후계자」 관련 상표·저작권은 Nintendo와 트레저에 있습니다.
패치를 적용한 게임 파일의 배포를 금지합니다.
