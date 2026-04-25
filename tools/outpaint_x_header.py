# X用ヘッダー画像をbg_4.pngのoutpaintingで生成
# Gemini API の Imagen edit/outpaint 機能を試す
# Usage: py -3.14 tools/outpaint_x_header.py

import os
import io
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
PROJECT_ROOT = Path(__file__).parent.parent
SRC_BG = PROJECT_ROOT / "icons_generated" / "header_candidates" / "round1" / "bg_4.png"
LOGO = PROJECT_ROOT / "site" / "logo.png"
OUT_DIR = PROJECT_ROOT / "icons_generated" / "x_header_candidates"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 元画像 1408x768 (16:9) を中央に置いて、左右に拡張して 3:1 (約 2304x768) にしたい
# 出力後にPILで 1500x500 にリサイズ
SRC_W, SRC_H = 1408, 768
TARGET_W = SRC_H * 3   # 3:1 比率での目標幅 = 2304
EXTEND = (TARGET_W - SRC_W) // 2   # 左右に追加する幅

def build_canvas_and_mask():
    """元画像を中央に配置した拡張キャンバスとマスクを作る
       マスク: 白=outpaint対象、黒=保持"""
    src = Image.open(SRC_BG).convert("RGB")
    canvas = Image.new("RGB", (TARGET_W, SRC_H), (255, 255, 255))
    canvas.paste(src, (EXTEND, 0))

    mask = Image.new("L", (TARGET_W, SRC_H), 255)   # 全体白
    # 中央の元画像領域だけ黒（保持）
    inner = Image.new("L", (SRC_W, SRC_H), 0)
    mask.paste(inner, (EXTEND, 0))

    return canvas, mask

def main():
    if not API_KEY:
        print("[ERROR] GEMINI_API_KEY 未設定")
        return

    canvas, mask = build_canvas_and_mask()
    canvas_path = OUT_DIR / "canvas.png"
    mask_path = OUT_DIR / "mask.png"
    canvas.save(canvas_path)
    mask.save(mask_path)
    print(f"[INFO] canvas: {canvas.size}, mask: {mask.size}")

    client = genai.Client(api_key=API_KEY)

    prompt = (
        "Extend the existing image naturally. "
        "Continue the scattered triangles pattern: green triangles on the left side, "
        "orange triangles on the right side, both flowing toward the corners. "
        "Pure white background. Same style and color tones as the central existing image. "
        "Triangles small, varied in size and rotation. "
        "Absolutely NO text, NO words, NO letters."
    )

    # google-genai SDK の edit_image を試す
    try:
        # canvas.png を入力、mask.png でマスク領域指定
        with open(canvas_path, "rb") as f:
            canvas_bytes = f.read()
        with open(mask_path, "rb") as f:
            mask_bytes = f.read()

        response = client.models.edit_image(
            model="imagen-3.0-capability-001",
            prompt=prompt,
            reference_images=[
                types.RawReferenceImage(
                    reference_image=types.Image(image_bytes=canvas_bytes, mime_type="image/png"),
                    reference_id=0,
                ),
                types.MaskReferenceImage(
                    reference_image=types.Image(image_bytes=mask_bytes, mime_type="image/png"),
                    reference_id=1,
                    config=types.MaskReferenceConfig(
                        mask_mode="MASK_MODE_USER_PROVIDED",
                        mask_dilation=0.01,
                    ),
                ),
            ],
            config=types.EditImageConfig(
                edit_mode="EDIT_MODE_OUTPAINT",
                number_of_images=4,
                output_mime_type="image/png",
            ),
        )
        if not response.generated_images:
            print("[ERROR] 応答に画像なし")
            return

        for i, img in enumerate(response.generated_images, 1):
            out_raw = OUT_DIR / f"outpaint_{i}.png"
            with open(out_raw, "wb") as f:
                f.write(img.image.image_bytes)
            print(f"  [OK] {out_raw.name}")

            # 1500x500 にリサイズ + ロゴ合成
            bg = Image.open(out_raw).convert("RGB").resize((1500, 500), Image.LANCZOS)
            logo = Image.open(LOGO).convert("RGBA")
            LH = 320
            ratio = LH / logo.height
            nw = int(logo.width * ratio)
            logo = logo.resize((nw, LH), Image.LANCZOS)
            x, y = (1500 - nw) // 2, (500 - LH) // 2
            bg.paste(logo, (x, y), logo)
            out_final = OUT_DIR / f"x_header_{i}.jpg"
            bg.save(out_final, "JPEG", quality=88, optimize=True)
            print(f"  [OK] {out_final.name} ({out_final.stat().st_size / 1024:.1f} KB)")

    except Exception as e:
        print(f"[ERROR] outpaint 失敗: {type(e).__name__}: {e}")
        return

if __name__ == "__main__":
    main()
