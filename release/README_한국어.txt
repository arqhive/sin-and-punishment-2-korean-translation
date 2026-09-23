죄와 벌 우주의 후계자 한글패치 v1.0 (Wii / 일본판 기준)
========================================================

■ 준비물
  - 일본판 ISO   Tsumi to Batsu - Sora no Koukeisha (Japan).iso
      CRC32 4780998F / MD5 fd9f83599cb9962e3ba8137b19454c1f
      (WBFS·RVZ 등으로 갖고 계시면 ISO로 변환 후 사용)
  - 패치 파일     SinAndPunishment2_KO_v1.0.xdelta
  - 패치 도구     xdelta3 또는 Delta Patcher 같은 GUI 도구

■ 적용 방법
  1) Delta Patcher (GUI)
     - Original file: 일본판 ISO
     - XDelta patch:  SinAndPunishment2_KO_v1.0.xdelta
     - Apply patch 클릭

  2) xdelta3 (명령줄)
     xdelta3 -d -s "Tsumi to Batsu - Sora no Koukeisha (Japan).iso" SinAndPunishment2_KO_v1.0.xdelta "Tsumi to Batsu - Sora no Koukeisha (Korean).iso"

  ※ 일본판 원본에 적용합니다. 하스피님 한글판 ISO에 덧씌우지 마세요.

■ 결과 파일 확인 (여기와 다르면 원본 ISO가 다른 것입니다)
  CRC32  B686AB1B
  MD5    ec38ddc271137a5eab30f48a61349349
  SHA1   ffb251ec8c06bf01f910c6153966a5a30081e001
  SHA256 6f32a42d91167f2a03728d34402539fc0be5f9d06301feae346fd602a31ce28d
  크기   4,699,979,776 바이트

■ 한글화 범위
  - 게임 텍스트: 메뉴, 옵션, 튜토리얼, 경고·오류 메시지
  - 컷신 자막 전체
  - 그래픽: 스테이지 이름, Wii 주의 화면, 스태프롤, 타이틀 로고,
    Wii 메뉴 배너·아이콘

■ 확인 환경
  - Dolphin
  - Wii U vWii

■ 알려진 사항
  - Wii 메뉴에 표시되는 채널 이름은 일본어 그대로입니다.
  - 메뉴 버튼·점수 표시 같은 영어 그래픽은 원본(일본판)도 영어라 그대로 두었습니다.
  - 잘못된 번역이나 깨진 글자를 발견하면 제보해 주세요.

■ 크레딧
  - 한식구 카페 하스피님의 한글 패치를 활용해 제작했습니다.
    https://cafe.naver.com/hansicgu/35057
  - 폰트: Pretendard (SIL Open Font License 1.1)

■ 제보·문의
  https://github.com/arqhive/sin-and-punishment-2-korean-translation/issues

※ 이 패치에는 게임 데이터가 들어 있지 않습니다. 정품 ISO가 있어야 사용할 수 있습니다.
