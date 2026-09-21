# cross <제외할 게임 키>  — company | crush | overtime
cross() {
  echo '<section class="sec surface">'
  echo '  <div class="wrap">'
  echo '    <div class="sec-head"><span class="eyebrow">Same universe</span><h2>같은 세계관의 다른 게임</h2>'
  echo '    <p>회사는 마왕성, 대표는 마왕, 직원은 몬스터, 고객은 용사. 벌써아침의 게임은 이 규칙을 공유합니다.</p></div>'
  echo '    <div class="cross">'
  [ "$1" != "company" ] && cat <<'X'
      <a class="xcard" href="dungeon.html">
        <img src="../assets/img/card-kiwoogi.webp" alt="" width="800" height="450" loading="lazy">
        <div><b>던전 컴퍼니</b><span>방치형 RPG · Android · iOS · Web</span></div>
      </a>
X
  [ "$1" != "crush" ] && cat <<'X'
      <a class="xcard" href="crush.html">
        <img src="../assets/img/crush/card-crush.webp" alt="" width="800" height="450" loading="lazy">
        <div><b>던전 크러시</b><span>매치3 퍼즐 · Android · iOS</span></div>
      </a>
X
  [ "$1" != "overtime" ] && cat <<'X'
      <a class="xcard" href="overtime.html">
        <img src="../assets/img/title.webp" alt="" width="1280" height="720" loading="lazy">
        <div><b>마왕님 야근 사수</b><span>아레나 서바이버 · Windows</span></div>
      </a>
X
  echo '    </div>'
  echo '  </div>'
  echo '</section>'
}
