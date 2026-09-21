#!/usr/bin/env python3
"""회사 로고 PNG 를 사이트용 SVG 세트로 변환한다.

원본(`logo.png`)은 콘텐츠가 117x115px 밖에 안 되는 저해상도 래스터라
확대하면 뭉개진다. 벡터로 따두면 헤더(작게)·푸터(중간)·OG(크게) 어디서나
같은 파일로 선명하게 쓸 수 있다.

    python3 scripts/build-logo.py ~/Downloads/logo.png

만들어지는 것 (assets/img/):
    logo.svg              전체 락업, 브랜드 네이비  — 밝은 배경용
    logo-light.svg        전체 락업, 흰색           — 네이비 푸터용
    logo-mark-light.svg   AM 심볼만, 흰색           — 네이비 헤더용
    favicon.svg           네이비 사각 + 흰 AM       — 브라우저 탭

재실행하면 덮어쓴다. 원본 로고가 갱신되면 이 스크립트만 다시 돌리면 된다.
"""
import sys
import pathlib

try:
    import numpy as np
    from PIL import Image, ImageFilter
    import potrace
except ImportError as e:
    sys.exit(f"의존성 없음({e}). 필요: pillow, numpy, potracer\n"
             f"  pip install --target <dir> potracer  후 PYTHONPATH 로 지정")

BRAND = "#21374E"   # 원본 로고에서 뽑은 네이비
SS = 6              # 슈퍼샘플링 배율
BLUR = 3.0          # 픽셀 계단을 곡선으로 녹이는 정도
OPTTOL = 0.6        # potrace 곡선 최적화 허용오차 (클수록 가벼움)
DEC = 1             # 좌표 소수점 자리수

# 원본 세로 구간 — 요소 사이 빈 행으로 확인한 값
AM_BAND = (0, 62)   # AM 심볼


def trace(mask_bool):
    """True=글자 인 불리언 배열을 potrace 곡선 목록으로."""
    # potracer 는 True 를 배경으로 취급하므로 뒤집어 넣는다
    return potrace.Bitmap(~mask_bool).trace(
        turdsize=int(2 * SS), alphamax=1.0, opticurve=True, opttolerance=OPTTOL)


def fmt(v, off_y=0.0):
    s = f"%.{DEC}f" % (v / SS - off_y)
    s = s.rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def curve_to_d(curve, off_y=0.0):
    def P(p):
        return f"{fmt(p.x)} {fmt(p.y, off_y)}"
    out = ["M" + P(curve.start_point)]
    for seg in curve:
        if seg.is_corner:
            out.append("L" + P(seg.c) + "L" + P(seg.end_point))
        else:
            out.append("C" + P(seg.c1) + " " + P(seg.c2) + " " + P(seg.end_point))
    out.append("Z")
    return "".join(out)


def curve_top(curve):
    ys = [curve.start_point.y]
    for seg in curve:
        ys.append(seg.end_point.y)
    return min(ys) / SS


def svg(w, h, d, color, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="벌써아침">{extra}'
            f'<path fill="{color}" fill-rule="evenodd" d="{d}"/></svg>')


def main():
    if len(sys.argv) != 2:
        sys.exit(f"사용법: {sys.argv[0]} <logo.png 경로>")
    src = pathlib.Path(sys.argv[1]).expanduser()
    if not src.exists():
        sys.exit(f"원본을 찾을 수 없다: {src}")

    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img"
    out.mkdir(parents=True, exist_ok=True)

    im = Image.open(src).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    w, h = im.size

    big = (im.getchannel("A")
             .resize((w * SS, h * SS), Image.NEAREST)
             .filter(ImageFilter.GaussianBlur(BLUR)))
    curves = list(trace(np.array(big) > 128))

    full = "".join(curve_to_d(c) for c in curves)
    am = [c for c in curves if AM_BAND[0] <= curve_top(c) < AM_BAND[1]]
    am_h = AM_BAND[1]
    am_d = "".join(curve_to_d(c) for c in am)

    files = {
        "logo.svg":            svg(w, h, full, BRAND),
        "logo-light.svg":      svg(w, h, full, "#fff"),
        "logo-mark-light.svg": svg(w, am_h, am_d, "#fff"),
        "favicon.svg":         svg(w, am_h, am_d, "#fff",
                                   extra=f'<rect width="{w}" height="{am_h}" fill="#131A2B"/>'),
    }
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
        print(f"  {name:<22} {len(content.encode()):>7,} bytes")

    print(f"\n원본 {w}x{h}px · 전체 곡선 {len(curves)}개 · AM 심볼 {len(am)}개")


if __name__ == "__main__":
    main()
