# P3 Craft アイコン候補 第3弾 — icon_01_3 ベースのバリエーション
# Usage: py -3.14 tools/generate_icons_v3.py

import os
import sys
import time
from pathlib import Path
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
BATCH_NAME = "batch3_variations"
OUTPUT_DIR = Path(__file__).parent.parent / "icons_generated" / BATCH_NAME
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "imagen-4.0-fast-generate-001"

COLOR = "MUST use exactly two colors: green (#2ECC71) and orange (#E67E22). Every design MUST contain both green AND orange. No other colors except black text and white background."
BASE = f"Square app icon, 1024x1024. Clean, modern, minimal, professional. White background. {COLOR}"

PROMPTS = [
    # === 三角シェイプ バリエーション ===
    f"{BASE} Two triangles: green triangle top-left corner, orange triangle bottom-right corner. Large bold 'P3' in black at top center, smaller 'Craft' text below. Geometric, sharp edges.",
    f"{BASE} Green triangle pointing right at top-left, orange triangle pointing left at bottom-right. 'P3' large black text overlapping the green shape, 'Craft' below in smaller black text.",
    f"{BASE} Large green right-angled triangle in top-left, large orange right-angled triangle in bottom-right, both touching corners. 'P3 Craft' in bold black centered between them.",
    f"{BASE} Two triangles facing each other diagonally: green top-left, orange bottom-right. Text 'P3' in large bold black overlaid on the green triangle, 'Craft' overlaid on the orange triangle.",
    f"{BASE} Small green triangle top-left, small orange triangle bottom-right. Oversized 'P3' in black fills most of the icon, tiny 'Craft' underneath.",

    # === 台形シェイプ バリエーション ===
    f"{BASE} Green trapezoid shape at top-left, orange trapezoid at bottom-right, arranged diagonally. 'P3' large bold black text center-top, 'Craft' smaller below.",
    f"{BASE} Wide green trapezoid spanning the top of the icon, narrow orange trapezoid at the bottom. 'P3 Craft' in bold black text centered vertically.",
    f"{BASE} Green parallelogram top-left, orange parallelogram bottom-right, both at 30-degree angle. 'P3' overlapping the green shape, 'Craft' overlapping the orange shape.",
    f"{BASE} Two trapezoids: green one at top tilted right, orange one at bottom tilted left, creating dynamic diagonal composition. Bold 'P3' in black between them, 'Craft' below.",

    # === テキスト配置バリエーション（P3大きめ＋Craft小さめ） ===
    f"{BASE} Very large bold 'P3' in black at upper portion, much smaller 'Craft' in black below. Green geometric accent shape top-left corner, orange accent shape bottom-right corner. Triangular shapes.",
    f"{BASE} 'P3' takes up 60% of the icon in huge bold black font. 'Craft' in tiny text bottom-right. Green triangle top-left behind the P, orange triangle bottom-right behind Craft.",
    f"{BASE} Stacked layout: 'P3' in massive black bold letters at top, 'Craft' in thin black letters at bottom. Green diagonal stripe behind P3, orange diagonal stripe behind Craft.",
    f"{BASE} 'P3' in extra-bold black, slightly left-aligned. 'Craft' in light-weight black font, right-aligned below. Green triangle accent top-left, orange triangle accent bottom-right.",

    # === シェイプとテキストの重なり ===
    f"{BASE} Large green triangle top-left with 'P3' in white text inside it. Orange triangle bottom-right with 'Craft' in white text inside it. Sharp geometric.",
    f"{BASE} Green trapezoid behind the letters 'P3' making them appear as knockout/reversed text. Orange trapezoid behind 'Craft'. Both shapes overlapping slightly in the middle.",
    f"{BASE} Full-bleed green triangle covering top-left half of icon. Full-bleed orange triangle covering bottom-right half. 'P3' in white on green area, 'Craft' in white on orange area.",
    f"{BASE} Green chevron shape pointing right with 'P3' overlaid in black. Orange chevron below pointing right with 'Craft' overlaid in black. Stacked vertically.",

    # === ダイナミックな構図 ===
    f"{BASE} Green triangle and orange triangle almost touching at center, creating an hourglass negative space. 'P3' in bold black at top, 'Craft' at bottom.",
    f"{BASE} Large green arrow/chevron pointing down-right at top-left. Large orange arrow/chevron pointing up-left at bottom-right. 'P3 Craft' in bold black at exact center.",
    f"{BASE} Diagonal split: top-left area has scattered small green triangles, bottom-right has scattered small orange triangles. 'P3' huge black text center, 'Craft' small below.",
    f"{BASE} Green and orange triangles arranged like origami birds flying diagonally. 'P3' in large black text, 'Craft' smaller, both center-aligned.",
]

def main():
    if not API_KEY:
        print("[ERROR] GEMINI_API_KEY が設定されていません")
        return

    client = genai.Client(api_key=API_KEY)
    total = len(PROMPTS)
    print(f"[INFO] バッチ: {BATCH_NAME}")
    print(f"[INFO] {total}個のプロンプトで生成開始...")

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
                print(f"  [SKIP] 画像なし")
        except Exception as e:
            print(f"  [ERROR] {e}")
            if "429" in str(e) or "quota" in str(e).lower():
                print("  [INFO] レート制限。30秒待機...")
                time.sleep(30)
        time.sleep(2)

    print(f"\n[完了] {generated}枚 → {OUTPUT_DIR}")
    create_gallery()

def create_gallery():
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
<html><head><meta charset="utf-8"><title>P3 Craft アイコン候補</title>
<style>
body {{ font-family: sans-serif; background: #f5f5f5; padding: 20px; }}
h1 {{ text-align: center; }}
h2 {{ margin-top: 40px; border-bottom: 2px solid #ddd; padding-bottom: 8px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; margin-top: 12px; }}
.card {{ background: white; border-radius: 8px; padding: 6px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); cursor: pointer; transition: transform 0.1s; }}
.card:hover {{ transform: scale(1.05); }}
.card img {{ width: 100%; }}
.card p {{ margin: 4px 0 0; font-size: 11px; color: #666; }}
</style></head><body>
<h1>P3 Craft アイコン候補（全{total_count}枚）</h1>
{''.join(sections)}
</body></html>"""
    with open(gallery_root / "gallery.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[INFO] ギャラリー更新済み")

if __name__ == "__main__":
    main()
