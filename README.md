# Pyxel Pattern - Agentic Development Suite

Pyxel 2.0+ に対応した **AI エージェント用開発スキルスイート** と、そのテストとして作った **ローグライクゲーム** のサンプルプロジェクトです。

## 🌟 目的
本プロジェクトは、Gemini CLI などの AI エージェントが Pyxel ゲームエンジンを最大限に活用するためのSKILLSを作成することを目的としました。

単なるコードサンプルではなく、Pyxel の最新仕様（WASM対応、ネイティブ衝突判定、BGM自動生成など）を AI が正しく理解し、開発者に提供できるかもしれません。

## 🛠️ Pyxel Development Suite (Agent Skills)
`.agents/skills/Pyxel_dev_suite` に格納されている 8 つのサブスキルが、開発の全工程をサポートします。

1.  **Core**: アプリ基盤と最新の数学・乱数関数の活用。
2.  **Sprite**: コードベースのスプライト定義と回転・拡縮描画。
3.  **Animation**: 状態遷移（待機・走り等）を管理する Animator クラス。
4.  **Map Processing**: Tilemap への直接操作とカメラスクロール。
5.  **Collision**: ネイティブ `tilemaps[].collide` を用いた高速衝突判定。
6.  **Audio**: `gen_bgm` によるプロシージャル BGM 生成と SE 再生。
7.  **Web Export**: WASM (Web) パッケージ化と HTML 出力の自動化。
8.  **Skill Refiner**: GitHub の最新ソースを解析し、スキル定義自体を常に最新化するメタスキル。

## 🎮 応用例: 探索者と闇の迷宮 (Roguelike Gold)
これらのスキルを組み合わせて作成された、本格的なターン制ローグライクゲームです。

- **特徴**:
    - **視界制限 (Fog of War)**: プレイヤーの周囲数マスしか見えない緊張感。
    - **ネイティブ衝突判定**: 快適で正確な移動ロジック。
    - **自動生成BGM**: シーン（タイトル・プレイ・死亡）に応じた動的な音楽。
    - **UI/UX**: HPバー、アイコン、日本語メッセージ、被弾時のフラッシュ演出。

### 🚀 実行方法 (Local)
本プロジェクトは `uv` を使用して依存関係を管理しています。

```bash
# 依存関係のインストールと実行
uv run src/roguelike/main.py
```

### 🌐 Web プレビュー / 書き出し
VS Code の Pyxel 拡張機能を使用してブラウザで即座に実行できるほか、以下のコマンドで配布用 HTML を生成できます。

```bash
uv run pyxel app2html src/roguelike/main.py
```

## 📂 ディレクトリ構成
- `.agents/skills/Pyxel_dev_suite/`: AI エージェント用スキル定義
- `src/roguelike/`: 応用例としてのゲームソースコード
- `pyproject.toml`: `uv` 用のプロジェクト構成

## 📜 ライセンス
それぞれのライブラリのライセンスに従います。その他は、MIT Licenseです。
