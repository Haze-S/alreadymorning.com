head_open() {
cat <<H
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>$1</title>
<meta name="description" content="$2">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22><rect width=%2232%22 height=%2232%22 fill=%22%23131A2B%22/><rect x=%2210%22 y=%2210%22 width=%2212%22 height=%2212%22 fill=%22%23E8833A%22/></svg>">
</head>
<body>
H
}

site_header() {
  # $1 = current page key (home|about|games)
  h=""; a=""; g=""
  case "$1" in home) h=' aria-current="page"';; about) a=' aria-current="page"';; games) g=' aria-current="page"';; esac
cat <<H
<header class="hd">
  <div class="hd-in">
    <a class="mark" href="index.html"><i></i>벌써아침</a>
    <nav class="gnb">
      <a href="index.html"$h>홈</a>
      <a href="games.html"$g>게임</a>
      <a href="about.html"$a>회사 소개</a>
      <a href="mailto:contact@alreadymorning.com">문의</a>
    </nav>
    <details class="mnav">
      <summary aria-label="메뉴 열기"><span></span><span></span><span></span></summary>
      <div class="mnav-panel">
        <a href="index.html">홈</a>
        <a href="games.html">게임</a>
        <a href="about.html">회사 소개</a>
        <a href="mailto:contact@alreadymorning.com">문의</a>
      </div>
    </details>
  </div>
</header>
H
}

site_footer() {
cat <<'H'
<footer class="ft">
  <div class="wrap ft-grid">
    <div class="ft-brand">
      <span class="mark"><i></i>벌써아침</span>
    </div>
    <div>
      <h4>Games</h4>
      <nav>
        <a href="dungeon.html">던전 컴퍼니</a>
        <a href="crush.html">던전 크러시</a>
        <a href="overtime.html">마왕님 야근 사수</a>
      </nav>
    </div>
    <div>
      <h4>Company</h4>
      <nav>
        <a href="about.html">회사 소개</a>
        <a href="mailto:support@alreadymorning.com">게임 문의</a>
        <a href="mailto:contact@alreadymorning.com">사업·제휴 문의</a>
      </nav>
    </div>
    <div>
      <h4>Legal</h4>
      <nav>
        <a href="terms.html">이용약관</a>
        <a href="privacy.html">개인정보처리방침</a>
        <a href="odds.html">확률 공시</a>
      </nav>
    </div>
  </div>
  <div class="wrap ft-biz">
    <span>상호 벌써아침</span>
    <span>대표 송현정</span>
    <span>사업자등록번호 818-10-02994</span>
    <span>통신판매업 신고번호 제 2026-부산진구-1275 호</span>
    <span>부산광역시 부산진구 연수로 29</span>
    <span>070-7954-6929</span>
  </div>
  <div class="wrap ft-meta">
    <span>© 2026 벌써아침</span>
    <a href="mailto:support@alreadymorning.com">support@alreadymorning.com</a>
  </div>
</footer>
</body>
</html>
H
}
