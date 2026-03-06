name: Pyxel Map Processing
description: >
  Pyxel のタイルマップを解析し、描画、座標変換、動的なタイル操作、
  カメラ制御を自動化するスキル。
  `pyxel.bltm` の最新機能（回転・拡縮）や、組み込み衝突判定との連携をサポートする。

instructions: |
  - ユーザーがマップの描画、スクロール、地形変化に関する要求をした場合に発火する。
  - 以下の処理を自動化する：
      - `pyxel.bltm(x, y, tm, u, v, w, h, [colkey], [rotate], [scale])` 呼び出しの生成
      - カメラ座標 (`camera_x`, `camera_y`) に基づく描画ロジック
      - 指定座標のタイル取得 (`pyxel.tilemaps[n].pget(x, y)`) と書き換え (`pset`)
      - タイル座標 (tx, ty) とワールド座標 (wx, wy) の変換ロジック
      - `Pyxel_Collision` スキルで利用する壁タイルのリスト（`[(u, v), ...]`）の定義
  - Pyxel の 8タイルマップ (0〜7)、256x256 サイズを前提とする。

inputs:
  - tilemap_index: タイルマップ番号 (0-7)
  - tile_size: タイルサイズ (通常 8)
  - camera_target: カメラが追従するオブジェクト (Player等)
  - scroll_speed: スクロールの滑らかさ

outputs:
  - マップ描画関数 (`draw_map(camera_x, camera_y)`)
  - カメラ更新ロジック (`update_camera()`)
  - 地形衝突・変化用のヘルパー関数
