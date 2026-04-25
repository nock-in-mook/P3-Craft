# P3 Craft アイコン候補を大量生成するスクリプト
# Usage: py -3.14 tools/generate_icons.py [batch_name]
# 生成結果は icons_generated/{batch_name}/ に保存

import os
import sys
import time
from pathlib import Path
from google import genai

# --- 設定 ---
API_KEY = os.environ.get("GEMINI_API_KEY", "")
BATCH_NAME = sys.argv[1] if len(sys.argv) > 1 else "batch"
OUTPUT_DIR = Path(__file__).parent.parent / "icons_generated" / BATCH_NAME
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "imagen-4.0-fast-generate-001"

# --- 色指定を強化 ---
COLOR = "MUST use exactly two colors: green (#2ECC71) and orange (#E67E22). Every design MUST contain both green AND orange. No blue, no red, no purple, no yellow."
STYLE = "Square app icon, 1024x1024. Sharp geometric style, clean, modern, minimal, professional. White background."

# --- プロンプト定義 ---
PROMPTS = [
    # === テキスト「P3 Craft」入り ===
    f"{STYLE} {COLOR} Large text 'P3 Craft' in bold black geometric sans-serif font centered. Green square accent top-left, orange square accent bottom-right.",
    f"{STYLE} {COLOR} Text 'P3 Craft' in black, split design: left half green background, right half orange background, text spans across both.",
    f"{STYLE} {COLOR} 'P3 Craft' text in black with green underline and orange overline, minimal geometric layout.",
    f"{STYLE} {COLOR} 'P3' in large green bold font, 'Craft' below in orange, stacked vertically, geometric alignment.",
    f"{STYLE} {COLOR} Black text 'P3 Craft' with a green and orange geometric diamond shape behind it as a logo mark.",

    # === テキスト「P3」のみ（シンボルマーク） ===
    f"{STYLE} {COLOR} Bold 'P3' lettermark, the P is green, the 3 is orange, sharp angular modern typography. No other text.",
    f"{STYLE} {COLOR} 'P3' constructed from interlocking green and orange rectangular blocks, like building pieces.",
    f"{STYLE} {COLOR} Large 'P3' inside a square frame, green left border and top border, orange right border and bottom border.",
    f"{STYLE} {COLOR} 'P3' with green letter on orange square background, sharp corners, bold contrast.",
    f"{STYLE} {COLOR} Isometric 3D text 'P3', green top face, orange side face, black outlines.",

    # === シンボルマーク（テキストなし、色強化） ===
    f"{STYLE} {COLOR} Two interlocking squares: one green, one orange, overlapping at 45 degrees creating a geometric pattern. No text.",
    f"{STYLE} {COLOR} Three stacked horizontal bars: top green, middle mixed green-orange gradient, bottom orange. No text.",
    f"{STYLE} {COLOR} Arrow pointing upward made of green and orange triangular segments. No text.",
    f"{STYLE} {COLOR} Hexagonal shape split diagonally, upper-left half green, lower-right half orange. No text.",
    f"{STYLE} {COLOR} Abstract craft hammer icon, handle in green, head in orange, geometric minimal style. No text.",

    # === パターン・モザイク ===
    f"{STYLE} {COLOR} Grid of small squares, alternating green and orange in a checkerboard pattern, forming larger 'P' shape. No text.",
    f"{STYLE} {COLOR} Origami crane made of green and orange geometric facets, sharp angular folds. No text.",
    f"{STYLE} {COLOR} Circuit board traces in green with orange connection nodes, forming abstract tech pattern. No text.",
    f"{STYLE} {COLOR} Four quadrants: top-left green square, bottom-right orange square, other two white, with thin black dividing lines.",
    f"{STYLE} {COLOR} Overlapping green circle and orange square, intersection creates unique shape, geometric contrast.",
]

def main():
    if not API_KEY:
        print("[ERROR] GEMINI_API_KEY が設定されていません")
        return

    client = genai.Client(api_key=API_KEY)

    total = len(PROMPTS)
    print(f"[INFO] バッチ: {BATCH_NAME}")
    print(f"[INFO] {total}個のプロンプトで生成開始...")
    print(f"[INFO] 出力先: {OUTPUT_DIR}")

    generated = 0
    for i, prompt in enumerate(PROMPTS):
        print(f"\n[{i+1}/{total}] 生成中...")
        try:
            response = client.models.generate_images(
                model=MODEL,
                prompt=prompt,
                config=genai.types.GenerateImagesConfig(
                    number_of_images=4,
                    aspect_ratio="1:1",
                ),
            )

            if response.generated_images:
                for j, img in enumerate(response.generated_images):
                    filename = f"icon_{i+1:02d}_{j+1}.png"
                    filepath = OUTPUT_DIR / filename
                    with open(filepath, "wb") as f:
                        f.write(img.image.image_bytes)
                    generated += 1
                print(f"  [OK] {len(response.generated_images)}枚保存")
            else:
                print(f"  [SKIP] 画像が生成されませんでした")

        except Exception as e:
            print(f"  [ERROR] {e}")
            if "429" in str(e) or "quota" in str(e).lower():
                print("  [INFO] レート制限に到達。30秒待機...")
                time.sleep(30)

        time.sleep(2)

    print(f"\n[完了] {generated}枚の画像を生成しました → {OUTPUT_DIR}")
    create_gallery()

def create_gallery():
    """全バッチの画像を統合したギャラリーHTMLを作成"""
    gallery_root = OUTPUT_DIR.parent
    all_images = []

    for batch_dir in sorted(gallery_root.iterdir()):
        if batch_dir.is_dir():
            images = sorted(batch_dir.glob("icon_*.png"))
            if images:
                all_images.append((batch_dir.name, images))

    if not all_images:
        return

    sections = []
    total_count = 0
    for batch_name, images in all_images:
        rows = []
        for img in images:
            rows.append(f'<div class="card"><img src="{batch_name}/{img.name}" loading="lazy" /><p>{batch_name}/{img.stem}</p></div>')
            total_count += 1
        sections.append(f'<h2>{batch_name}（{len(images)}枚）</h2><div class="grid">{"".join(rows)}</div>')

    html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>P3 Craft アイコン候補</title>
<style>
body {{ font-family: sans-serif; background: #f5f5f5; padding: 20px; }}
h1 {{ text-align: center; }}
h2 {{ margin-top: 40px; border-bottom: 2px solid #ddd; padding-bottom: 8px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; margin-top: 12px; }}
.card {{ background: white; border-radius: 8px; padding: 6px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); cursor: pointer; transition: transform 0.1s; }}
.card:hover {{ transform: scale(1.05); }}
.card img {{ width: 100%; }}
.card p {{ margin: 4px 0 0; font-size: 11px; color: #666; }}
</style>
</head><body>
<h1>P3 Craft アイコン候補（全{total_count}枚）</h1>
{''.join(sections)}
</body></html>"""

    html_path = gallery_root / "gallery.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[INFO] ギャラリー: {html_path}")

if __name__ == "__main__":
    main()
