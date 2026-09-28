죄와 벌 우주의 후계자 한글패치 v1.0.2 (Wii / 일본판 기준)
========================================================

■ 준비물
  - 일본판 디스크 이미지 (게임 ID R2VJ01)
  - Windows 10 이상 (따로 설치할 프로그램은 없습니다)
  - 빈 공간 약 6GB (풀어 둔 파일 약 1GB + 결과 이미지)

■ 지원 형식
  원본                                   결과
  ISO (정본 덤프, WBFS에서 변환한 ISO)   → ISO
  WBFS                                   → WBFS
  CISO, WIA, WDF                         → ISO
  RVZ   ×  Dolphin에서 ISO로 변환한 뒤 적용
  NKit  ×  NKit 도구로 원본 ISO로 복원한 뒤 적용

  덤프·변환 방법에 따라 MD5가 달라도 게임 파일만 같으면 적용됩니다.
  북미판·유럽판, 이미 한글 패치를 적용한 이미지에는 적용할 수 없습니다.

■ 적용 방법
  1) 압축을 풉니다.
  2) 원본 이미지(ISO 또는 WBFS)를 "패치하기.bat" 위에 끌어다 놓습니다.
     - 원본을 이 폴더에 넣고 "패치하기.bat"을 더블클릭해도 됩니다.
     - 이미지가 여러 개 있으면 경로를 물어봅니다. 파일을 창에 끌어다 놓고 Enter.
  3) "완료"가 나올 때까지 기다립니다(보통 1분 안팎). 진행 중에는 창을 닫지 마세요.
  4) 원본과 같은 폴더에 결과 파일이 생깁니다. 원본은 바뀌지 않습니다.
       ISO 원본  → Tsumi to Batsu - Sora no Koukeisha (Korean) [R2VJ01].iso
       WBFS 원본 → Tsumi to Batsu - Sora no Koukeisha (Korean) [R2VJ01].wbfs

  ※ 결과 형식 바꾸기 (예: ISO 원본 → WBFS 결과)
     이 폴더에서 PowerShell을 열고 결과 파일 확장자를 지정합니다.
       powershell -ExecutionPolicy Bypass -File patch.ps1 "원본.iso" "결과.wbfs"

  ※ 결과 파일의 MD5는 원본에 따라 달라질 수 있습니다. 게임 내용은 같습니다.

■ 실행 방법
  - Dolphin: 결과 ISO나 WBFS를 게임 목록 폴더에 넣거나 직접 엽니다.
  - Wii·Wii U vWii (USB Loader GX): WBFS를 권합니다(FAT32 USB는 4GB 넘는 파일 불가).
      wbfs/Tsumi to Batsu - Sora no Koukeisha (Korean) [R2VJ01]/R2VJ01.wbfs
    처럼 넣습니다. ISO를 쓰려면 NTFS USB를 쓰세요.

■ 오류가 날 때
  - "죄와 벌 우주의 후계자(R2VJ01)가 아닙니다": 북미판·유럽판이거나 다른 게임입니다.
  - "원본 게임 파일이 다릅니다": 이미 패치한 이미지거나 손상된 덤프입니다.
  - "RVZ는 지원하지 않습니다": Dolphin 게임 목록에서 우클릭 → 파일 변환 → ISO.
  - "wit.exe 실행 실패": 빈 공간이 모자라거나 원본 파일이 손상됐습니다.

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

■ 동봉 도구
  - wit (Wiimms ISO Tools, GPL-2.0, https://wit.wiimm.de/) — bin/wit-gpl-2.0.txt
  - xdelta3 (Apache-2.0, https://github.com/jmacd/xdelta)

■ 제보·문의
  https://github.com/arqhive/sin-and-punishment-2-korean-translation/issues

※ 이 패치에는 게임 데이터가 들어 있지 않습니다. 정품 디스크 이미지가 있어야 사용할 수 있습니다.
  비공식 팬 번역이며 Nintendo와 관련이 없습니다. 패치를 적용한 게임 파일의 배포를 금지합니다.
