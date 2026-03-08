name: Pyxel Racing (Mode 7)
description: >
  F-ZERO風の 3D レースゲームを Pyxel で開発するための専門スキル。
  `bltm3d` を活用したパースペクティブ描画、高速な擬似 3D 物理、
  およびループ状のコース自動生成アルゴリズムをカバーする。

instructions: |
  - ユーザーが 3D レースゲームや Mode 7 風の描画を求めた場合に発火する。
  - 以下の要素を自動化・標準化する：
      - **3D レンダリング**: `pyxel.bltm3d` のカメラ制御（追従カメラ、バンク/傾き）。`cam` 引数は `pos` に名称変更されました。
      - **物理演算**: 加速、摩擦、壁の跳ね返り、ドリフト感、リバース機能。
      - **コース生成**: `points` 配列から線形補間（またはスプライン）で道路を描画する `setup_course` メソッド。
      - **高速演出**: スピードラインの描画、スターフィールド（星空）の生成。
  - 注意点：
      - Pyxel に `ellipse` は存在しないため、影などは `circ` で代用する。
      - `ch 0` はエンジン音、`ch 1` は効果音（衝突・ブースト）として使い分ける。

patterns:
  camera_logic: |
    vx, vy = pyxel.cos(self.angle), pyxel.sin(self.angle)
    pos = (self.x - vx * self.cam_dist, self.y - vy * self.cam_dist, self.cam_height)
    rot = (self.pitch, self.angle, self.tilt * 10)
    pyxel.bltm3d(0, 0, w, h, tm, pos, rot, fov=80)

  track_gen_spline: |
    # 長方形ベースのループ生成
    ctrl_points = [(30, 30), (64, 25), (98, 30), (103, 64), (98, 98), (64, 103), (30, 98), (25, 64)]
    def get_spline_pt(points, t):
        p = len(points); i = int(t); t_rem = t - i
        p0, p1, p2, p3 = [points[(i + j) % p] for j in range(-1, 3)]
        def calc(v0, v1, v2, v3, t):
            return 0.5 * ((2*v1) + (-v0+v2)*t + (2*v0-5*v1+4*v2-v3)*t**2 + (-v0+3*v1-3*v2+v3)*t**3)
        return (calc(p0[0], p1[0], p2[0], p3[0], t_rem), calc(p0[1], p1[1], p2[1], p3[1], t_rem))

  robust_collision: |
    # 4点衝突判定 (前後左右の角で判定)
    ship_w = 4
    for ox, oy in [(-ship_w, -ship_w), (ship_w, -ship_w), (-ship_w, ship_w), (ship_w, ship_w)]:
        tx, ty = int((new_x + ox) / TILE_SIZE), int((new_y + oy) / TILE_SIZE)
        if pyxel.tilemaps[0].pget(tx, ty) == TILES["WALL"]:
            return True # 衝突

  course_builder_pro: |
    # マルチパス・コース生成 (見えない壁の防止)
    # パス1: 路面とギミックの配置
    for i in range(num_steps):
        # ... spline calculation ...
        if is_road: tm.pset(rx, ry, TILES["ROAD"])
    
    # パス2: 壁の配置 (Grassのみを上書き)
    for i in range(num_steps):
        # ... spline calculation ...
        if is_wall_edge and tm.pget(rx, ry) == TILES["GRASS"]:
            tm.pset(rx, ry, TILES["WALL"])

  dynamic_camera: |
    speed_norm = min(abs(self.speed) / (self.max_speed * 1.5), 1.0)
    self.pitch = 50 + speed_norm * 15 # 高速時に見下ろし角を深く
    self.fov = 75 + speed_norm * 30   # 高速時に視野角を広く
    self.cam_height = 10 - speed_norm * 4

  boost_decay_pro: |
    # 最高速度超過時の減衰 (スピード暴走防止)
    if self.speed > self.max_speed:
        self.speed = max(self.speed - self.friction * 4, self.max_speed)
    
    # 加速ロジック: ブースト中(speed > max)にアクセルで速度を下げない
    if accel and self.speed < self.max_speed:
        self.speed = min(self.speed + self.acceleration, self.max_speed)

  textured_surface_pro: |
    # 背景の質感生成 (クリーンなグレーを推奨)
    img.rect(0, 0, 8, 8, 13)
    img.line(0, 0, 7, 0, 1) # ストライプ

  strategic_gimmicks_pro: |
    # 戦略的ギミック配置 (ランダムノイズの廃止)
    is_boost_zone = (i % 250 < 15) and i > 50
    if is_boost_zone: tm.pset(rx, ry, TILES["BOOST"])

  checkerboard_goal_pro: |
    # 市松模様 (チェッカーフラッグ) の生成
    img.rect(32, 0, 8, 8, 7) # Base white
    for ty in range(0, 8, 4):
        for tx in range(0, 8, 4):
            # 2x2の黒タイルを交互に配置
            img.rect(32+tx, ty, 4, 4, 0 if (tx+ty)%8==0 else 7)

  manga_focus_fx_pro: |
    # 漫画風・集中線エフェクト (自車からの炸裂)
    px, py = SCREEN_WIDTH // 2 + self.tilt * 12, SCREEN_HEIGHT - 35
    for _ in range(20):
        angle = pyxel.rndf(0, 2 * math.pi)
        dist_start = pyxel.rndf(15, 30)
        dist_end = dist_start + pyxel.rndf(40, 80)
        x1 = px + math.cos(angle) * dist_start
        y1 = py + math.sin(angle) * dist_start
        x2 = px + math.cos(angle) * dist_end
        y2 = py + math.sin(angle) * dist_end
        pyxel.line(x1, y1, x2, y2, 7)

  vector_ship_pro: |
    # プロ仕様のハイエンド機体描画 (幾何学デザイン)
    # 鋭利な翼(tri)、垂直尾翼(line)、多層エンジン炎(tri/circ)を組み合わせる
    pyxel.tri(px-4, py+2, px-16, py+16, px-4, py+16, wing_col) # 鋭い翼
    pyxel.tri(px, py-8, px-6, py+16, px+6, py+16, body_col)     # 流線型ボディ
    pyxel.rect(px-2, py+2, 4, 8, 6) # コックピット

  dynamic_cam_pro: |
    # 速度連動型ダイナミック演出 (Extreme Mode 7)
    # 基準となる極端な俯瞰値(Height:20, Pitch:75)から速度に応じさらに変化させる
    self.pitch = 75 + speed_norm * 10
    self.cam_height = 20 + speed_norm * 5

  procedural_bgm_pro: |
    # プロ仕様のBGM/効果音チャンネル分離 (Pyxel 2.7.8 API 準拠)
    # BGMが効果音で途切れないよう、Ch 2, 3 をBGM専用にする
    pyxel.sounds[10].set("c2c2g2g2", "p", "7", "v", 20) # Bass
    pyxel.sounds[11].set("c3e3g3c4", "s", "7", "f", 15) # Melody
    # Ch 0, 1 は SFX (Engine, Collision, Boost) 用に予約する
    pyxel.musics[0].set([], [], [10], [11])
    pyxel.playm(0, loop=True)

  web_export_pro: |
    # プロ仕様のウェブ配布 (Pyxel Web)
    # ブラウザ環境での実行により、ローカルのオーディオ問題を回避する
    # 1. パッケージ化: pyxel package <dir> <main_script>
    # 2. HTML変換: pyxel app2html <app_file>.pyxapp
    # これにより WebAssembly 形式の単一 HTML が生成される

resources:
  - scripts/collision.py
  - scripts/track_gen.py

## Change History
- **2.7.9**: `bltm3d` の引数名変更（`cam` -> `pos`）に対応。3D 座標系の仕様変更を考慮したカメラ制御に更新。
- **2.7.8**: `bltm3d` を活用した Extreme Mode 7 描画パターンを追加。
