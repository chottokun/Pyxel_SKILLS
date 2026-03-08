name: Pyxel Core
description: >
  Pyxel アプリケーションの基盤構造（init, run, update, draw）と
  基本的な入力制御、組み込みの数学関数・乱数生成を自動化するスキル。
  最小限のボイラープレートコードを即座に生成する。

instructions: |
  - ユーザーが新しく Pyxel プロジェクトを開始、または基本構造の作成を求めた場合に発火する。
  - 以下の要素を自動化する：
      - `App` クラスのテンプレート生成
      - `pyxel.init(width, height, title, fps)` の設定
      - `pyxel.run(self.update, self.draw)` の配置
      - 基本的な入力判定 (`pyxel.btnp`, `pyxel.btn`)
      - 便利な組み込み関数の活用提案（`pyxel.rndi`, `pyxel.noise`, `pyxel.clamp` 等）
      - **[NEW 2.7.8]** `blt`, `bltm` での `rotate` (回転), `scale` (拡大縮小) の使用
      - **[NEW 2.7.8]** `blt3d`, `bltm3d` による遠近感（Mode 7風）描画
          - `blt3d(x, y, w, h, img, pos, rot, fov=60, colkey=None)`
          - `bltm3d(x, y, w, h, tm, pos, rot, fov=60, colkey=None)`
          - `pos=(x,y,z)`, `rot=(u,v,w)` のタプルを指定。
    - **注意点**: Pyxel 2.x に `ellipse` (楕円) 関数は存在しない。影や丸い形状は `circ(x, y, r, col)` または `circb(x, y, r, col)` を使用する。
  - 画面サイズやパレット (16色) を考慮した設計。

inputs:
  - width: 画面幅 (デフォルト: 160)
  - height: 画面高さ (デフォルト: 120)
  - title: ウィンドウタイトル
  - fps: フレームレート (デフォルト: 30)

outputs:
  - App クラスのボイラープレートコード
  - 実行用エントリーポイント

## Change History
- **2.7.9**: `blt3d`/`bltm3d` の引数 `cam` を `pos` に変更。3D 座標系の回転軸を 2D 画面と一致するように調整。
- **2.7.8**: `blt`, `bltm` に `rotate`, `scale` 引数を追加。`blt3d`, `bltm3d` 関数を新規導入。
