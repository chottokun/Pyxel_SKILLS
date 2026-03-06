import pyxel

# タイル定義 (u, v)
TILE_FLOOR = (0, 0)
TILE_WALL = (1, 0)
TILE_STAIRS = (2, 0) # 階段
TILE_CHEST = (3, 0)  # 宝箱

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rooms = []

    def generate(self, floor_num):
        # 最新の API: tilemaps[0] を使用
        tm = pyxel.tilemaps[0]
        tm.imgsrc = 0
        for y in range(self.height):
            for x in range(self.width):
                tm.pset(x, y, TILE_WALL)
        
        self.rooms = []
        for _ in range(6 + min(floor_num, 4)):
            room_w, room_h = pyxel.rndi(3, 5), pyxel.rndi(3, 5)
            room_x = pyxel.rndi(1, self.width - room_w - 1)
            room_y = pyxel.rndi(1, self.height - room_h - 1)

            for y in range(room_y, room_y + room_h):
                for x in range(room_x, room_x + room_w):
                    tm.pset(x, y, TILE_FLOOR)

            if self.rooms:
                prev_x, prev_y = self.rooms[-1]
                self._create_corridor(prev_x, prev_y, room_x + room_w // 2, room_y + room_h // 2)

            self.rooms.append((room_x + room_w // 2, room_y + room_h // 2))

        sx, sy = self.rooms[-1]
        tm.pset(sx, sy, TILE_STAIRS)

        for i in range(len(self.rooms) - 1):
            if pyxel.rndi(0, 3) == 0:
                cx, cy = self.rooms[i]
                if tm.pget(cx, cy) == TILE_FLOOR:
                    tm.pset(cx, cy, TILE_CHEST)

    def _create_corridor(self, x1, y1, x2, y2):
        tm = pyxel.tilemaps[0]
        x, y = x1, y1
        while x != x2:
            tm.pset(x, y, TILE_FLOOR)
            x += 1 if x < x2 else -1
        while y != y2:
            tm.pset(x, y, TILE_FLOOR)
            y += 1 if y < y2 else -1

    def draw(self, player_x, player_y, view_radius):
        tm = pyxel.tilemaps[0]
        px, py = int(player_x // 8), int(player_y // 8)
        
        for ty in range(self.height):
            for tx in range(self.width):
                dist = abs(tx - px) + abs(ty - py)
                if dist <= view_radius:
                    tile = tm.pget(tx, ty)
                    pyxel.blt(tx * 8, ty * 8, 0, tile[0] * 8, tile[1] * 8, 8, 8)
