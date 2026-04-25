# X用ヘッダー画像生成（1500x500 = 3:1）
# Imagenで16:9を生成し、横方向に三角が広く分布するプロンプトを使う
# その後、上下を軽くクロップして3:1にし、ロゴを中央合成
#
# Usage: py -3.14 tools/generate_x_header.py

import os
from pathlib import Path
from PIL import Image
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
PROJECT_ROOT = Path(__file__).parent.parent
OUT_DIR = PROJECT_ROOT / "icons_generated" / "x_header_candidates"
OUT_DIR.mkdir(parents=True, exist_ok=True)
LOGO = PROJECT_ROOT / "site" / "logo.png"

MODEL = "imagen-4.0-fast-generate-001"
TARGET_W, TARGET_H = 1500, 500
LOGO_HEIGHT = 320

PROMPT = (
    "Wide horizontal banner background, 16:9 aspect ratio. "
    "Pure white background. "
    "Green triangles distributed across the entire LEFT HALF of the image - "
    "spread horizontally from far-left edge toward the center, forming a wide horizontal band. "
    "Orange triangles distributed across the entire RIGHT HALF - "
    "spread horizontally from the center toward the far-right edge, forming a wide horizontal band. "
    "The triangles must be DISTRIBUTED HORIZONTALLY ACROSS THE WIDTH, "
    "not just clustered in the corners. "
    "Triangles should be visible across most of the image height, "
    "so cropping the top and bottom slightly will not remove them. "
    "Triangles small to medium-sized, varied rotation, flowing organically. "
    "Center 25% of the image width is empty white space (for logo overlay). "
    "Clean, minimal, modern brand banner. "
    "Absolutely NO text, NO words, NO letters, NO logos."
)

def crop_3to1_and_compose(bg_path: Path, out_path: Path):
    """16:9画像を3:1にクロップ → ロゴ合成 → 1500x500 JPEGで保存"""
    bg = Image.open(bg_path).convert("RGB")
    # 16:9 を 3:1 へ。横幅維持、縦を 1/3 にクロップ（上下から均等に削除）
    src_w, src_h = bg.size
    target_h = src_w // 3
    if target_h > src_h:
        # 万が一の保険: 想定外なら横を縮める
        target_h = src_h
        target_w = src_h * 3
        x = (src_w - target_w) // 2
        bg = bg.crop((x, 0, x + target_w, src_h))
    else:
        y = (src_h - target_h) // 2
        bg = bg.crop((0, y, src_w, y + target_h))
    # 1500x500 へリサイズ
    bg = bg.resize((TARGET_W, TARGET_H), Image.LANCZOS)

    logo = Image.open(LOGO).convert("RGBA")
    ratio = LOGO_HEIGHT / logo.height
    nw = int(logo.width * ratio)
    logo = logo.resize((nw, LOGO_HEIGHT), Image.LANCZOS)
    x, y = (TARGET_W - nw) // 2, (TARGET_H - LOGO_HEIGHT) // 2
    bg.paste(logo, (x, y), logo)
    bg.save(out_path, "JPEG", quality=88, optimize=True)

def main():
    if not API_KEY:
        print("[ERROR] GEMINI_API_KEY 未設定")
        return

    client = genai.Client(api_key=API_KEY)
    print("[INFO] Imagenで16:9背景4枚生成中（横分布プロンプト）...")

    response = client.models.generate_images(
        model=MODEL,
        prompt=PROMPT,
        config=genai.types.GenerateImagesConfig(
            number_of_images=4,
            aspect_ratio="16:9",
        ),
    )

    if not response.generated_images:
        print("[ERROR] 画像生成失敗")
        return

    print(f"[OK] {len(response.generated_images)}枚生成 → 3:1クロップ＋ロゴ合成")
    for i, img in enumerate(response.generated_images, 1):
        bg_path = OUT_DIR / f"bg_{i}.png"
        with open(bg_path, "wb") as f:
            f.write(img.image.image_bytes)
        out_path = OUT_DIR / f"x_header_{i}.jpg"
        crop_3to1_and_compose(bg_path, out_path)
        kb = out_path.stat().st_size / 1024
        print(f"  [OK] {out_path.name} ({kb:.1f} KB)")

    print(f"\n[完了] → {OUT_DIR}")

if __name__ == "__main__":
    main()
