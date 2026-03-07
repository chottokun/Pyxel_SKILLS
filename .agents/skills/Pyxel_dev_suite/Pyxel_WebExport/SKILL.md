name: Pyxel Web & Deployment
description: >
  Pyxel プロジェクトを Web (WASM) 用にパッケージ化し、
  ブラウザで実行可能な形式に変換、または配布用ファイルを生成するスキル。
  Pyxel 2.7.8 以降の最新の単一 HTML 出力仕様に完全対応する。

instructions: |
  - ユーザーが「Web で公開したい」「ブラウザで動かしたい」場合に発火する。
  - 以下の Pyxel 2.7.8 準拠のフローを自動化する：
      1. **インポートの修正 (最重要)**: 
         - Web版 (Pyodide) は `runpy.run_path` で実行されるため、起動スクリプト内での相対インポート (`from .constants import ...`) は失敗する。
         - パッケージ内のインポートは `from constants import ...` のように直接記述するように修正する。
      2. **パッケージ化**: `pyxel package APP_DIR STARTUP_SCRIPT` を実行。
         - 注意: `APP_DIR` はプロジェクトディレクトリ、`STARTUP_SCRIPT` はその中のメインファイル。
      3. **HTML変換**: `pyxel app2html PYXEL_APP_FILE` を実行。
         - 生成された HTML は CDN を介して Pyxel WASM ランタイムをロードし、Base64 化されたアプリを実行する。
  - Web版での制約チェック：
      - `ImportError`: 相対インポートを排除したか。
      - `VFS (Virtual File System)`: 実行時、リソースファイルは `APP_DIR` と同じルートに配置されている必要がある。

inputs:
  - app_dir: アプリケーションのディレクトリ (例: src/racegame)
  - startup_script: 起動スクリプト名 (例: main.py)

outputs:
  - `racegame.pyxapp` (中間パッケージ)
  - `racegame.html` (最終配布用 HTML)
