name: Pyxel Web & Deployment
description: >
  Pyxel プロジェクトを Web (WASM) 用にパッケージ化し、
  ブラウザで実行可能な形式に変換、または配布用ファイルを生成するスキル。
  VS Code 拡張機能や Pyxel Web プレビューとの連携を最適化する。

instructions: |
  - ユーザーが「Web で公開したい」「ブラウザで動かしたい」「配布ファイルを作りたい」場合に発火する。
  - 以下の処理を自動化する：
      1. パッケージ化: `pyxel package APP_DIR STARTUP_SCRIPT` を生成。
      2. HTML出力: `pyxel app2html PYXEL_APP_FILE` を実行して .html を生成。
      3. VS Code連携: VS Code の Pyxel 拡張機能を用いたブラウザプレビューの案内。
  - Web版での制約（ファイルパスの扱い、特定の `os` モジュールが使えない等）のチェックを行う。
  - GitHub Pages へのデプロイ手順や、URL パラメータによる実行オプションを提案する。

inputs:
  - app_dir: アプリケーションのディレクトリ (例: src/roguelike)
  - startup_script: 起動スクリプト (例: main.py)
  - output_format: 出力形式 (pyxapp / html / exe)

outputs:
  - 実行すべきパッケージ化コマンド
  - 生成された配布ファイル (.html / .pyxapp)
  - ブラウザプレビューの手順
