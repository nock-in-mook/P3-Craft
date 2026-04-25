# Google Play Console デベロッパーヘッダー画像生成
# Imagenで「白背景＋緑オレンジ三角散布」の16:9素材を生成 → PILで確定ロゴ中央合成 → 4096x2304 JPEG出力
#
# Usage: py -3.14 tools/generate_header.py

import os
import time
from io import BytesIO
from pathlib import Path
from PIL import Image
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
PROJECT_ROOT = Path(__file__).parent.parent
CANDIDATES_DIR = PROJECT_ROOT / "icons_generated" / "header_candidates"
CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
LOGO_PATH = PROJECT_ROOT / "site" / "logo.png"  # グレー枠除去済み（remove_logo_border.py 結果）

MODEL = "imagen-4.0-fast-generate-001"
TARGET_W, TARGET_H = 4096, 2304   # Google Play Console ヘッダー画像推奨サイズ
LOGO_HEIGHT = 1500                 # 中央配置するロゴの高さ（バナー高2304に対して約65%）

# プロンプト: 中央領域は空け、四隅に三角を集中配置（中央にロゴを後で重ねるため）
PROMPT = (
    "Wide horizontal banner image, 16:9 aspect ratio. "
    "Pure white background. Scattered small filled triangles in only two colors: "
    "green (#2ECC71) on the upper-left and lower-left areas, "
    "orange (#E67E22) on the upper-right and lower-right areas. "
    "Triangles are small, varied in size and rotation, flowing diagonally toward the corners. "
    "Center horizontal area (about 40% width centered) is mostly empty white space. "
    "Clean, minimal, modern, professional brand banner design. "
    "Absolutely NO text, NO words, NO letters, NO logos."
)

def composite(bg_path: Path, logo_path: Path, out_path: Path):
    """背景画像にロゴを中央合成して 4096x2304 JPEGで保存"""
    bg = Image.open(bg_path).convert("RGB")
    bg = bg.resize((TARGET_W, TARGET_H), Image.LANCZOS)

    logo = Image.open(logo_path).convert("RGBA")
    ratio = LOGO_HEIGHT / logo.height
    new_w = int(logo.width * ratio)
    logo = logo.resize((new_w, LOGO_HEIGHT), Image.LANCZOS)

    x = (TARGET_W - new_w) // 2
    y = (TARGET_H - LOGO_HEIGHT) // 2
    bg.paste(logo, (x, y), logo)

    bg.save(out_path, "JPEG", quality=88, optimize=True)
    return out_path

def main():
    if not API_KEY:
        print("[ERROR] GEMINI_API_KEY が未設定")
        return
    if not LOGO_PATH.exists():
        print(f"[ERROR] ロゴが見つからない: {LOGO_PATH}")
        return

    client = genai.Client(api_key=API_KEY)
    print(f"[INFO] Imagenで背景4枚生成中（16:9）...")

    response = client.models.generate_images(
        model=MODEL,
        prompt=PROMPT,
        config=genai.types.GenerateImagesConfig(
            number_of_images=4,
            aspect_ratio="16:9",
        ),
    )

    if not response.generated_images:
        print("[ERROR] 画像生成失敗（応答が空）")
        return

    print(f"[OK] {len(response.generated_images)}枚生成 → ロゴ合成中...")
    results = []
    for i, img in enumerate(response.generated_images, 1):
        bg_path = CANDIDATES_DIR / f"bg_{i}.png"
        with open(bg_path, "wb") as f:
            f.write(img.image.image_bytes)

        out_path = CANDIDATES_DIR / f"header_{i}.jpg"
        composite(bg_path, LOGO_PATH, out_path)
        size_kb = out_path.stat().st_size / 1024
        print(f"  [OK] {out_path.name} ({size_kb:.1f} KB)")
        results.append(out_path)

    print(f"\n[完了] {len(results)}候補 → {CANDIDATES_DIR}")
    print(f"  プレビュー: gallery_header.html を生成中...")

    # 候補プレビュー用HTML
    cards = "".join(
        f'<div class="card"><img src="{p.name}" loading="lazy"/><p>{p.stem}</p></div>'
        for p in results
    )
    html = f"""<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<title>P3 Craft ヘッダー候補</title>
<style>
body{{font-family:sans-serif;background:#222;color:#eee;padding:20px;margin:0}}
h1{{text-align:center}}
.grid{{display:grid;grid-template-columns:1fr;gap:20px;max-width:1400px;margin:20px auto}}
.card{{background:#fff;border-radius:8px;padding:8px;box-shadow:0 4px 12px rgba(0,0,0,.4)}}
.card img{{width:100%;display:block}}
.card p{{color:#444;margin:8px 0 0;font-size:13px;text-align:center}}
</style></head><body>
<h1>P3 Craft ヘッダー候補（4枚）</h1>
<div class="grid">{cards}</div>
</body></html>"""
    (CANDIDATES_DIR / "gallery_header.html").write_text(html, encoding="utf-8")
    print(f"  → {CANDIDATES_DIR / 'gallery_header.html'}")

if __name__ == "__main__":
    main()
