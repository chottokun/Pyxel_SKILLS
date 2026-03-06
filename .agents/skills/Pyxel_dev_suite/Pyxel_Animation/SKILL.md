name: Pyxel Animation
description: >
  Pyxel プロジェクトにおけるアニメーションの状態遷移、更新、描画を
  自動化するスキル。Animator クラスによるステートベースの管理コードを
  生成し、複雑なアクション制御を簡略化する。

instructions: |
  - ユーザーがアニメーション定義、キャラクターのアクション制御に関する要求をした場合に発火する。
  - 以下の要素を自動化する：
      - アニメーション辞書 (`ANIMATIONS`) の生成: { "state": [frames...], "speed": n }
      - ステート管理機能を持つ `Animator` クラスの生成
      - 状態遷移 (`animator.set_state("run")`) の自動化
      - ループ再生、一回のみ再生の切り替え
      - `update()` 内でのフレーム進捗計算と `draw()` 内での描画コード
  - スプライト管理スキル (`Pyxel_Sprite`) の `SPRITES` 辞書と連携する設計。

inputs:
  - animation_states: [ { "state": "idle", "frames": ["player_0", "player_1"], "speed": 10 }, ... ]
  - loop: ループするかどうか (デフォルト: True)

outputs:
  - Animator クラス
  - ANIMATIONS 定数定義
  - 各アクションに応じた状態遷移コード

resources:
  - resources/animation_examples.md
