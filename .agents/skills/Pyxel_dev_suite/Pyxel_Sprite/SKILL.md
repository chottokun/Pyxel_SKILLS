name: Pyxel Sprite Management
description: >
  Pyxel Editor (.pyxres) や外部 PNG からスプライト情報を定義・抽出し、
  `pyxel.blt` による描画コードと `SPRITES` 辞書を自動生成するスキル。
  透明色、反転に加え、最新APIの「回転 (`rotate`)」と「拡縮 (`scale`)」にも対応。

instructions: |
  - ユーザーがスプライト定義、描画、画像読み込みに関する要求をした場合に発火する。
  - 以下の要素を自動化する：
      - `SPRITES` 辞書の生成: { "name": (bank, u, v, w, h, [colkey]) }
      - `pyxel.blt(x, y, img, u, v, w, h, [colkey], [rotate], [scale])` の抽象化
      - 外部画像の読み込み (`pyxel.images[n].load(x, y, filename)`)
      - 反転描画 (w, h の符号反転) の対応
  - Pyxel の仕様（画像バンク 0〜2、透明色は通常 0 番、サイズは 256x256）を前提とする。

inputs:
  - pyxres_path: .pyxres ファイルのパス (任意)
  - image_path: 外部画像 (.png) のパス (任意)
  - sprites: [ { "name": "player", "u": 0, "v": 0, "w": 8, "h": 8, "colkey": 0 }, ... ]
  - bank: 使用する画像バンク (0〜2)

outputs:
  - SPRITES 定数定義 (Python dict)
  - スプライト描画用のメソッド (`draw_sprite(name, x, y, flip_x=False, flip_y=False, rotate=None, scale=None)`)

resources:
  - resources/sprite_examples.md
