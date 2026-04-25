# P3 Craft アイコン候補 第4弾 — テキスト配置固定、シェイプのみバリエーション
# Usage: py -3.14 tools/generate_icons_v4.py

import os
import time
from pathlib import Path
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
BATCH_NAME = "batch4_shape_vars"
OUTPUT_DIR = Path(__file__).parent.parent / "icons_generated" / BATCH_NAME
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "imagen-4.0-fast-generate-001"

# テキスト配置は固定: P3大きく上、Craft小さめ下、重なりあり
TEXT = "Large bold black 'P3' text at upper portion, smaller bold black 'Craft' text below it. Text overlaps with the colored shapes behind."
COLOR = "MUST use exactly two colors: green (#2ECC71) and orange (#E67E22). No other colors except black text and white background."
BASE = f"Square app icon, 1024x1024. Clean, modern, minimal, professional. White background. {COLOR} {TEXT}"

PROMPTS = [
    # === 三角バリエーション ===
    f"{BASE} Green triangle pointing right behind P3, orange triangle pointing left behind Craft. Triangles large and overlapping with text.",
    f"{BASE} Green triangle pointing down-right at top-left area, orange triangle pointing up-left at bottom-right area. Sharp acute triangles.",
    f"{BASE} Two large equilateral triangles: green one behind P3 rotated 15 degrees, orange one behind Craft rotated -15 degrees.",
    f"{BASE} Green right-angled triangle filling top-left quarter, orange right-angled triangle filling bottom-right quarter. Text overlaid on both.",
    f"{BASE} Thin tall green triangle pointing up behind P3, wide flat orange triangle pointing right behind Craft.",
    f"{BASE} Green triangle pointing up behind the letter P, orange triangle pointing down behind the number 3. Craft text below both.",

    # === 台形・平行四辺形 ===
    f"{BASE} Green trapezoid shape behind P3, wider at top narrower at bottom. Orange trapezoid behind Craft, wider at bottom narrower at top.",
    f"{BASE} Green parallelogram tilted 20 degrees behind P3. Orange parallelogram tilted -20 degrees behind Craft. Dynamic diagonal feel.",
    f"{BASE} Green trapezoid at top spanning full width, orange trapezoid at bottom spanning full width. Both behind text. Ribbon-like.",
    f"{BASE} Green rhombus behind P3, orange rhombus behind Craft. Both rotated 45 degrees, diamond shapes.",

    # === 矢印・シェブロン ===
    f"{BASE} Green chevron/arrow pointing right behind P3. Orange chevron/arrow pointing right behind Craft. Both arrows stacked vertically.",
    f"{BASE} Large green arrow pointing down-right behind P3 text. Large orange arrow pointing up-right behind Craft text.",
    f"{BASE} Green double chevron >> behind P3. Orange double chevron >> behind Craft. Speed/motion feel.",
    f"{BASE} Single large green arrowhead at top-left, single large orange arrowhead at bottom-right. Text P3 and Craft centered between them.",

    # === シェイプサイズ・距離バリエーション ===
    f"{BASE} Very large green triangle covering 40% of icon behind P3. Small orange triangle accent near Craft. Asymmetric balance.",
    f"{BASE} Small green triangle tucked tight behind P3 letters. Small orange triangle tucked tight behind Craft letters. Compact, close to text.",
    f"{BASE} Green and orange triangles touching each other at center, forming a bowtie/hourglass shape. P3 above the junction, Craft below.",
    f"{BASE} Green triangle top-left and orange triangle bottom-right, both pushed to corners with lots of white space between them. P3 and Craft centered.",

    # === ユニークな構図 ===
    f"{BASE} Green pennant/flag shape waving behind P3. Orange pennant/flag shape waving behind Craft. Dynamic movement feel.",
    f"{BASE} Green lightning bolt shape behind P3. Orange lightning bolt behind Craft. Energy, craft, creation theme.",
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
                    filepath = OUTPUT_DIR / f"icon_{i+1:02d}_{j+1}.png"
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

    # ギャラリー更新
    gallery_root = OUTPUT_DIR.parent
    all_images = []
    for d in sorted(gallery_root.iterdir()):
        if d.is_dir():
            imgs = sorted(d.glob("icon_*.png"))
            if imgs:
                all_images.append((d.name, imgs))
    if not all_images:
        return
    sections = []
    tc = 0
    for bn, imgs in all_images:
        rows = [f'<div class="card"><img src="{bn}/{i.name}" loading="lazy"/><p>{bn}/{i.stem}</p></div>' for i in imgs]
        tc += len(imgs)
        sections.append(f'<h2>{bn}（{len(imgs)}枚）</h2><div class="grid">{"".join(rows)}</div>')
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>P3 Craft アイコン候補</title>
<style>body{{font-family:sans-serif;background:#f5f5f5;padding:20px}}h1{{text-align:center}}h2{{margin-top:40px;border-bottom:2px solid #ddd;padding-bottom:8px}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin-top:12px}}.card{{background:white;border-radius:8px;padding:6px;text-align:center;box-shadow:0 2px 4px rgba(0,0,0,.1);cursor:pointer;transition:transform .1s}}.card:hover{{transform:scale(1.05)}}.card img{{width:100%}}.card p{{margin:4px 0 0;font-size:11px;color:#666}}</style></head><body>
<h1>P3 Craft アイコン候補（全{tc}枚）</h1>{''.join(sections)}</body></html>"""
    with open(gallery_root / "gallery.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[INFO] ギャラリー更新済み")

if __name__ == "__main__":
    main()
