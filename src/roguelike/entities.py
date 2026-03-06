import pyxel

class Entity:
    def __init__(self, x, y, u, v, colkey=0):
        self.x = x * 8 
        self.y = y * 8
        self.u = u 
        self.v = v
        self.colkey = colkey
        self.hp = 10
        self.max_hp = 10
        self.shake = 0

    def move(self, dx, dy, wall_tiles):
        adj_dx, adj_dy = pyxel.tilemap(0).collide(self.x, self.y, 8, 8, dx * 8, dy * 8, wall_tiles)
        self.x += adj_dx
        self.y += adj_dy
        # 実際に移動したかどうかを返す
        return adj_dx != 0 or adj_dy != 0

    def draw(self):
        off_x = pyxel.rndi(-self.shake, self.shake) if self.shake > 0 else 0
        pyxel.blt(self.x + off_x, self.y, 0, self.u, self.v, 8, 8, self.colkey)
        if self.shake > 0: self.shake -= 1

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 8, 0)
        self.max_hp = 40
        self.hp = 40

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 24, 8, 0)
        self.hp = 10

    def take_turn(self, player, wall_tiles):
        """
        戻り値: True なら攻撃した、False なら移動（または待機）した
        """
        dx = 1 if player.x > self.x else -1 if player.x < self.x else 0
        dy = 1 if player.y > self.y else -1 if player.y < self.y else 0
        
        # すでに隣接しているかチェック
        is_adjacent = abs(player.x - self.x) <= 8 and abs(player.y - self.y) <= 8
        
        if is_adjacent:
            # 隣接していれば移動せず攻撃フラグを立てる
            return True
        else:
            # 隣接していなければ移動する
            self.move(dx, dy, wall_tiles)
            return False
