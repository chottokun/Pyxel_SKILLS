name: Pyxel Collision
description: >
  Pyxel プロジェクトにおける AABB 矩形衝突判定、組み込みのタイル衝突判定 (`Tilemap.collide`)、
  移動時の衝突回避処理を自動化するスキル。
  最新APIを活用した壁抜け防止とキャラ移動のテンプレートを生成する。

instructions: |
  - ユーザーが当たり判定、物理移動、壁の衝突に関する要求をした場合に発火する。
  - 以下の処理を自動化する：
      - AABB（矩形衝突）関数: `check_collision(x1, y1, w1, h1, x2, y2, w2, h2)`
      - タイル衝突判定: Pyxel組み込みの `pyxel.tilemaps[tm].collide(x, y, w, h, dx, dy, walls)` を利用。
      - 壁抜け防止ロジックを含む移動関数 (`move_with_collision(dx, dy)`)
      - レイキャストや一点判定など、用途に合わせた判定メソッドの選択
  - 独自ループによる判定ではなく、C言語レベルで最適化された `collide` を優先する。
  - マップ処理スキル (`Pyxel_MapProcessing`) の `BLOCK_TILES` (タイルの u,v 座標のリスト) と連携する。

inputs:
  - entity_a: 判定対象エンティティ (Player等)
  - block_tiles: 衝突とみなすタイルのリスト 例: [(1,0), (2,0)]
  - offset: 当たり判定の余白 (x, y, w, h)

outputs:
  - `Tilemap.collide` をラップした高レベルな移動ロジック
  - AABB判定ユーティリティ
  - 複数の敵や弾丸と一括で判定を行うためのループ処理

resources:
  - scripts/collision.py
