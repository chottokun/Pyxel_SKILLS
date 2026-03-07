name: Pyxel Development Suite
description: >
  Pyxel プロジェクト（2.1.0 ~ 2.7.8+）における開発をサポートするスキル。
  グラフィックス、オーディオ、マップ処理に加え、
  2.7.8+ で導入された Mode 7 風の描画機能（回転、拡大縮小、3D 遠近感）をサポートする。

instructions: |
  - このスイートは以下の8つの独立スキルで構成される：
      1. Core Skill: `pyxel.init`, `pyxel.run`, 基本的な入力制御
      2. Sprite Skill: `pyxel.blt` と .pyxres 画像バンク管理
      3. Animation Skill: フレーム更新と Animator クラス
      4. Map Processing Skill: `pyxel.tilemap`, `pget/pset`, カメラ制御
      5. Collision Skill: AABB とタイル衝突判定
      6. Audio Skill: `pyxel.play`, `pyxel.playm`, 効果音・音楽制御
      7. Web Export: WASM (Web) 用のパッケージ化、HTML出力
      8. Skill Refiner: スキル定義そのものを GitHub の最新仕様で更新

  - ユーザーの要求内容に応じて、該当するサブスキルを自動的に選択して実行する。
  - 各スキルは Pyxel の仕様（画像バンク0〜3、タイルサイズ8/16/32px、
    tilemap(0) など）を前提とする。
  - 生成コードは Python 3.10+ を前提とし、ユーザーがそのまま貼り付けて
    使用できる形式にする。
  - スキル間の依存関係は以下の通り：
      - Animation Skill は Sprite Skill の SPRITES 辞書を利用する。
      - Collision Skill は Map Processing Skill の BLOCK_TILES を利用する。
      - 全体として Core Skill の `update/draw` 構造に従う。
      - Web Export は配布用ファイルの生成を担当する。
      - Skill Refiner は他の全てのスキルをブラッシュアップする役割を持つ。

subskills:
  - core: ./Pyxel_Core/SKILL.md
  - sprite: ./Pyxel_Sprite/SKILL.md
  - animation: ./Pyxel_Animation/SKILL.md
  - map: ./Pyxel_MapProcessing/SKILL.md
  - collision: ./Pyxel_Collision/SKILL.md
  - audio: ./Pyxel_Audio/SKILL.md
  - web: ./Pyxel_WebExport/SKILL.md
  - refiner: ./Pyxel_SkillRefiner/SKILL.md

inputs:
  - task: 実行したい処理（core / sprite / animation / map / collision / audio）
  - params: 各スキルに渡すパラメータ

outputs:
  - Python コードスニペット
  - 必要に応じて補助スクリプト（scripts/）の利用提案

resources:
  - scripts/
  - resources/
  - Pyxel_Core/
  - Pyxel_Sprite/
  - Pyxel_Animation/
  - Pyxel_MapProcessing/
  - Pyxel_Collision/
  - Pyxel_Audio/