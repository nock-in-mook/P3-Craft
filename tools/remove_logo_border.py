# ロゴ画像のグレー枠を除去し、内側の白角丸ロゴだけをくりぬく
# 戦略: 中央から flood fill で「グレー以外」を辿り、辿れた領域だけ残して他は透明化
# Usage: py -3.14 tools/remove_logo_border.py
import os
os.environ.setdefault("PYTHONUTF8", "1")

from pathlib import Path
from PIL import Image
import sys
sys.setrecursionlimit(10**6)

ROOT = Path(__file__).parent.parent
SRC = ROOT / "icons_generated" / "favorites" / "p3craft_logo_final.png"
OUT = ROOT / "site" / "logo.png"

# 「グレー枠」とみなす色: ほぼ無彩色 + 中間明度
def is_gray_border(r, g, b):
    if abs(r - g) > 14 or abs(g - b) > 14 or abs(r - b) > 14:
        return False
    v = (r + g + b) / 3
    return 140 <= v <= 235  # ロゴ内の白(>240)・黒(<60)・有彩色は対象外

def main():
    img = Image.open(SRC).convert("RGBA")
    w, h = img.size
    print(f"[INFO] 入力: {SRC.name} {w}x{h}")

    px = img.load()
    # ロゴ本体マスク (False=未到達=削る、True=ロゴの一部として残す)
    keep = bytearray(w * h)  # 0/1 のフラットバイト配列で省メモリ

    # 中央から flood fill (反復、stack)
    cx, cy = w // 2, h // 2
    stack = [(cx, cy)]
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        idx = y * w + x
        if keep[idx]:
            continue
        c = px[x, y]
        r, g, b = c[0], c[1], c[2]
        if is_gray_border(r, g, b):
            continue  # グレー枠で止まる
        keep[idx] = 1
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))

    # マスク外を透明化
    cleared = 0
    for y in range(h):
        for x in range(w):
            if not keep[y * w + x]:
                px[x, y] = (0, 0, 0, 0)
                cleared += 1
    print(f"[INFO] {cleared} px 透明化 / 全 {w*h} px")

    # 出力
    img.save(OUT, "PNG", optimize=True)
    print(f"[OK] {OUT}")

if __name__ == "__main__":
    main()
