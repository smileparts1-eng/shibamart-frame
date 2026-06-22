# SHIBA MART JAPAN — Shopee 枠画像

Shopee 出品時に商品画像1枚目へ自動合成する**透明PNG枠**を生成・ホスティングするためのリポジトリ。

## 中身
- `frame_generator.py` — Pillowで枠PNGを生成（設定は冒頭の CONFIG ブロック）
- `output/shibamart_frame_navy.png` — 生成された枠（**ホスティング対象 / 透過保持**）

## 生成
```bash
pip install pillow
python3 frame_generator.py        # output/ に PNG 出力
```
色は `COLOR_NAME` を `navy/red/green/gold` に変更。日本語太字フォントは自動検出（Mac=ヒラギノ / Linux=Noto Sans CJK）。

## ホスティング（raw URL）
このPNGを GitHub に push すると、固定の raw URL で参照できる：
```
https://raw.githubusercontent.com/<user>/<repo>/main/output/shibamart_frame_navy.png
```
**ファイル名を変えなければ URL は不変** → 枠を作り直しても `git push` するだけでスプレッドシート側のURL欄はそのままで反映される。

## 運用メモ
- スプレッドシート（出品ツール本体）は他人作で編集不可。URL欄への貼り付けは手動で1回だけ。
- 透過が白く潰れると中央が白板になり商品が隠れる → **透過保持を最優先**（スクリプトは中央アルファ=0をセルフチェック）。
