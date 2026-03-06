name: Pyxel Skill Refiner
description: >
  Pyxel プロジェクトにおける他のスキル定義 (SKILL.md) やテンプレートを、
  GitHub の最新ソースコード (https://github.com/kitao/pyxel) に基づいて
  解析、評価、およびブラッシュアップするメタスキル。
  スキルの正確性と実用性を常に最新の状態に保つ役割を担う。

instructions: |
  - ユーザーが「Pyxel スキルの更新」「コードの最適化」「最新 API への対応」を求めた場合に発火する。
  - 以下のステップを実行してスキルをブラッシュアップする：
      1. Research: GitHub から `python/pyxel/__init__.pyi` を取得し、最新の API シグネチャを確認。
      2. Comparison: 既存の `SKILL.md` や `scripts/` の定義と、最新 API の変更点（追加された引数、非推奨のメソッド等）を比較。
      3. Optimization: 非効率な自作ロジック（例：独自の衝突判定ループ）を、最新の組み込み機能（例：`Tilemap.collide`）へ置き換える提案・修正を行う。
      4. Best Practice: 最新の Pyxel 開発トレンド（クラスベース、リソース管理、GitHub の Examples）を反映させる。
  - 修正後は、スキルの `description` や `instructions` も日本語で分かりやすく更新する。

inputs:
  - target_skill_path: ブラッシュアップ対象のスキルディレクトリ (例: ./Pyxel_Sprite)
  - github_source: Pyxel 公式リポジトリの URL (デフォルト: https://github.com/kitao/pyxel)

outputs:
  - 更新された `SKILL.md` の内容
  - 最新 API に基づく最適化された Python スクリプト
  - 変更内容（なぜ更新されたか、どのようなメリットがあるか）の技術レポート
