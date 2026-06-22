#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SHIBA MART JAPAN - Shopee 枠(フレーム)画像ジェネレーター
- 1000x1000 / 中央透明 / 上バナー / 下バー / 左上 日本丸シール
- 透過(アルファ)を保持したPNGを output/ に出力する
- まずは 1色(navy)・1枚 を確実に生成する用途

使い方:
    python3 frame_generator.py
色を変える場合は下の COLOR_NAME を "navy"/"red"/"green"/"gold" に変更。
"""

from PIL import Image, ImageDraw, ImageFont
import os, sys

# ============================================================
# CONFIG  ここだけ変えれば調整できます
# ============================================================
SHOP_NAME    = "SHIBA MART JAPAN"      # 下バーのメイン店名
SUBTITLE     = "100% Authentic Japan"  # 下バーのサブ
BANNER_TEXT  = "Direct from Japan"      # 上バナーの文言(国旗は自動描画)
STICKER_TOP  = "日本"                   # 左上丸シール 上段
STICKER_BTM  = "JAPAN"                  # 左上丸シール 下段

SIZE         = 1000                     # 正方形サイズ(px)
COLOR_NAME   = "navy"                   # navy / red / green / gold
OUTPUT_DIR   = os.path.join(os.path.dirname(__file__), "output")
OUTPUT_NAME  = f"shibamart_frame_{COLOR_NAME}.png"   # 固定名(raw URLを不変にするため)

# レイアウト比率 (SIZEに対する割合)
BANNER_H_R   = 0.13     # 上バナー高さ
BAR_H_R      = 0.165    # 下バー高さ
BORDER_W     = 9        # 外周ボーダー太さ(0で無し)
DRAW_FLAG    = True     # 上バナーに日本国旗を描くか

# テーマ色 (バナー/バー/シールの地色)
COLORS = {
    "navy":  (31, 58, 95),
    "red":   (150, 32, 38),
    "green": (24, 72, 58),
    "gold":  (140, 104, 40),
}

# フォント候補(見つかった最初のものを使う)。手動指定したい場合は FONT_OVERRIDE にパスを入れる
FONT_OVERRIDE = None
FONT_CANDIDATES = [
    "/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc",   # macOS bold
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Hiragino Sans GB.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",   # Linux
    "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Bold.otf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
]
# ============================================================


def find_font_path():
    if FONT_OVERRIDE and os.path.exists(FONT_OVERRIDE):
        return FONT_OVERRIDE
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    print("[!] 日本語太字フォントが自動検出できませんでした。", file=sys.stderr)
    print("    下記のいずれかのパスを FONT_OVERRIDE に設定して再実行してください:", file=sys.stderr)
    for p in FONT_CANDIDATES:
        print("      -", p, file=sys.stderr)
    sys.exit(1)


def darken(rgb, f):
    return tuple(max(0, min(255, int(c * f))) for c in rgb)


def load_font(path, size):
    # .ttc は index=0 を使用
    try:
        return ImageFont.truetype(path, size, index=0)
    except Exception:
        return ImageFont.truetype(path, size)


def center_text(draw, cx, cy, text, font, fill, anchor="mm"):
    draw.text((cx, cy), text, font=font, fill=fill, anchor=anchor)


def draw_jp_flag(draw, cx, cy, w, h):
    """白地に赤丸の日本国旗を (cx,cy) 中心に描く"""
    x0, y0 = cx - w / 2, cy - h / 2
    x1, y1 = cx + w / 2, cy + h / 2
    # 白地(薄い枠付き)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=h * 0.12,
                           fill=(255, 255, 255), outline=(210, 210, 210), width=2)
    # 赤丸
    r = h * 0.30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(188, 0, 45))


def main():
    font_path = find_font_path()
    color = COLORS[COLOR_NAME]
    bar_dark = darken(color, 0.55)

    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))   # 完全透明ベース
    d = ImageDraw.Draw(img)

    banner_h = int(SIZE * BANNER_H_R)
    bar_h = int(SIZE * BAR_H_R)

    # --- 外周ボーダー(任意) ---
    if BORDER_W > 0:
        inset = BORDER_W // 2 + 2
        d.rounded_rectangle([inset, inset, SIZE - inset, SIZE - inset],
                            radius=int(SIZE * 0.03), outline=color, width=BORDER_W)

    # --- 上バナー ---
    d.rectangle([0, 0, SIZE, banner_h], fill=color)
    banner_font = load_font(font_path, int(banner_h * 0.42))
    cy = banner_h // 2
    if DRAW_FLAG:
        fh = int(banner_h * 0.5)
        fw = int(fh * 1.45)
        # フラグ+テキストをまとめて中央寄せ
        tb = d.textbbox((0, 0), BANNER_TEXT, font=banner_font)
        tw = tb[2] - tb[0]
        gap = int(banner_h * 0.18)
        total = fw + gap + tw
        start = (SIZE - total) / 2
        draw_jp_flag(d, start + fw / 2, cy, fw, fh)
        d.text((start + fw + gap, cy), BANNER_TEXT, font=banner_font,
               fill=(255, 255, 255), anchor="lm")
    else:
        center_text(d, SIZE // 2, cy, BANNER_TEXT, banner_font, (255, 255, 255))

    # --- 下バー ---
    by0 = SIZE - bar_h
    d.rectangle([0, by0, SIZE, SIZE], fill=bar_dark)
    name_font = load_font(font_path, int(bar_h * 0.40))
    sub_font = load_font(font_path, int(bar_h * 0.19))
    center_text(d, SIZE // 2, by0 + int(bar_h * 0.38), SHOP_NAME, name_font, (255, 255, 255))
    center_text(d, SIZE // 2, by0 + int(bar_h * 0.72), SUBTITLE, sub_font, (214, 219, 229))

    # --- 左上 丸シール ---
    sr = int(SIZE * 0.082)             # 半径
    scx = scy = int(SIZE * 0.105)      # 中心(左上コーナー)
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=color,
              outline=(255, 255, 255), width=max(3, sr // 16))
    st_font = load_font(font_path, int(sr * 0.62))
    sb_font = load_font(font_path, int(sr * 0.40))
    center_text(d, scx, scy - int(sr * 0.26), STICKER_TOP, st_font, (255, 255, 255))
    center_text(d, scx, scy + int(sr * 0.34), STICKER_BTM, sb_font, (255, 255, 255))

    # --- 保存 (PNG, アルファ保持) ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
    img.save(out, "PNG")

    # --- 透過セルフチェック ---
    px = img.load()
    center_alpha = px[SIZE // 2, SIZE // 2][3]
    mid_alpha = px[SIZE // 2, int(SIZE * 0.45)][3]
    print(f"[OK] 生成: {out}")
    print(f"     size={img.size}  mode={img.mode}  font={os.path.basename(font_path)}")
    print(f"     中央アルファ={center_alpha} (0=完全透明が正常)  中段アルファ={mid_alpha}")
    if center_alpha == 0:
        print("     ✅ 中央は透明です（商品が透けて見えます）")
    else:
        print("     ⚠️ 中央が透明ではありません。レイアウトを確認してください")


if __name__ == "__main__":
    main()
