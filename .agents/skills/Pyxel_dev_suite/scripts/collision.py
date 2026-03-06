import pyxel

def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    """Simple AABB collision check between two rectangles."""
    return (x1 < x2 + w2 and
            x2 < x1 + w1 and
            y1 < y2 + h2 and
            y2 < y1 + h1)

def move_with_collision(tm, x, y, w, h, dx, dy, wall_tiles):
    """
    Pyxel 組み込みの Tilemap.collide を利用した高度な衝突判定移動。
    wall_tiles: 衝突するタイルのリスト 例: [(1, 0), (2, 0)] (u, v のタプル)
    
    戻り値: (新しいX座標, 新しいY座標, X方向の衝突有無, Y方向の衝突有無)
    """
    # Pyxelの組み込み機能で、補正された移動量を取得
    adj_dx, adj_dy = pyxel.tilemaps[tm].collide(x, y, w, h, dx, dy, wall_tiles)
    
    new_x = x + adj_dx
    new_y = y + adj_dy
    
    # 意図した移動量と実際の移動量が異なれば衝突したと判定
    hit_x = (dx != 0 and adj_dx == 0)
    hit_y = (dy != 0 and adj_dy == 0)
    
    return new_x, new_y, hit_x, hit_y
