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
  - 画面サイズやパレット (16色) を考慮した設計。

inputs:
  - width: 画面幅 (デフォルト: 160)
  - height: 画面高さ (デフォルト: 120)
  - title: ウィンドウタイトル
  - fps: フレームレート (デフォルト: 30)

outputs:
  - App クラスのボイラープレートコード
  - 実行用エントリーポイント
