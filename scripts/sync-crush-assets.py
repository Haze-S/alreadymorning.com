#!/usr/bin/env python3
"""던전 크러시 스토어 리소스를 사이트용 webp 로 변환해 assets/img/crush/ 에 넣는다.

dungeon-crush 레포의 `store/` 가 원본이다. 화질 수정(dungeon-crush#52) 처럼
스크린샷을 다시 찍은 뒤 이 스크립트를 돌리면 사이트 이미지가 한 번에 갱신된다.

    python3 scripts/sync-crush-assets.py ../dungeon-crush

규격은 docs/crush-brief.md 의 표와 같다. 파일명·크기를 바꾸면 사이트 HTML 의
width/height 속성도 함께 고쳐야 한다.
"""
import sys
import pathlib

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow 가 필요하다:  pip install Pillow")

# 원본 경로 -> (출력 파일명, 목표 크기, 크롭 여부)
JOBS = [
    ("store/screenshots/04-boss-cut.png",   "crush-shot-boss-cut.webp",    (540, 960),  False),
    ("store/screenshots/05-boss-board.png", "crush-shot-boss-board.webp",  (540, 960),  False),
    ("store/screenshots/02-specials.png",   "crush-shot-specials.webp",    (540, 960),  False),
    ("store/screenshots/01-map.png",        "crush-shot-map.webp",         (540, 960),  False),
    ("store/screenshots/03-boss-card.png",  "crush-shot-boss-card.webp",   (540, 960),  False),
    ("store/feature-1024x500.png",          "crush-feature.webp",          (1024, 500), False),
    ("store/feature-1024x500.png",          "card-crush.webp",             (800, 450),  True),
    ("store/icon-512.png",                  "crush-icon.webp",             (256, 256),  False),
]

QUALITY = 82


def center_crop_to_ratio(im, ratio):
    """가운데를 기준으로 목표 비율까지 잘라낸다."""
    w, h = im.size
    if w / h > ratio:
        new_w = int(h * ratio)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = int(w / ratio)
    top = (h - new_h) // 2
    return im.crop((0, top, w, top + new_h))


def main():
    if len(sys.argv) != 2:
        sys.exit(f"사용법: {sys.argv[0]} <dungeon-crush 레포 경로>")

    src_root = pathlib.Path(sys.argv[1]).expanduser().resolve()
    out_dir = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img" / "crush"

    if not src_root.is_dir():
        sys.exit(f"원본 경로를 찾을 수 없다: {src_root}")
    out_dir.mkdir(parents=True, exist_ok=True)

    missing, written = [], []
    for rel, out_name, size, crop in JOBS:
        src = src_root / rel
        if not src.exists():
            missing.append(rel)
            continue
        im = Image.open(src).convert("RGB")
        if crop:
            im = center_crop_to_ratio(im, size[0] / size[1])
        im = im.resize(size, Image.LANCZOS)
        dst = out_dir / out_name
        im.save(dst, "WEBP", quality=QUALITY, method=6)
        written.append(f"  {out_name:<30} {size[0]}x{size[1]}  {dst.stat().st_size // 1024} KB")

    if written:
        print(f"{len(written)}개 갱신 -> {out_dir}")
        print("\n".join(written))
    if missing:
        print("\n원본 없음 (건너뜀):")
        for m in missing:
            print(f"  {m}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
