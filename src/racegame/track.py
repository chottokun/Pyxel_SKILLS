import pyxel
import math
from constants import TRACK_SIZE, TILE_SIZE, TILES

class Track:
    def __init__(self):
        self.ctrl_points = [
            (30, 30), (64, 25), (98, 30), 
            (103, 64), (98, 98), (64, 103), 
            (30, 98), (25, 64)
        ]
        self.setup_assets()
        self.setup_course()

    def setup_assets(self):
        # Image Bank 0: Tilesets
        img = pyxel.images[0]
        # Clean Gray ROAD (Stripe pattern)
        img.rect(0, 0, 8, 8, 13)
        img.line(0, 0, 7, 0, 1)
        
        img.rect(8, 0, 8, 8, 3)   # Grass
        
        # Walls with texture (Hatching)
        img.rect(16, 0, 8, 8, 4)
        for i in range(0, 8, 2):
            img.line(16+i, 0, 16+i+2, 8, 12)
            
        # Boost with neon pink arrows
        img.rect(24, 0, 8, 8, 8) 
        img.line(26, 2, 28, 4, 7); img.line(30, 2, 28, 4, 7); img.line(28, 4, 28, 6, 7)
        
        # Checkerboard START (Pro Pattern)
        img.rect(32, 0, 8, 8, 7)
        for ty in range(0, 8, 4):
            for tx in range(0, 8, 4):
                img.rect(32+tx, ty, 4, 4, 0 if (tx+ty)%8==0 else 7)

    def get_spline_pt(self, t):
        p = len(self.ctrl_points); i = int(t); t_rem = t - i
        p0, p1, p2, p3 = [self.ctrl_points[(i + j) % p] for j in range(-1, 3)]
        def calc(v0, v1, v2, v3, t):
            return 0.5 * ((2*v1) + (-v0+v2)*t + (2*v0-5*v1+4*v2-v3)*t**2 + (-v0+3*v1-3*v2+v3)*t**3)
        return (calc(p0[0], p1[0], p2[0], p3[0], t_rem), calc(p0[1], p1[1], p2[1], p3[1], t_rem))

    def setup_course(self):
        tm = pyxel.tilemaps[0]
        # Clear Track with Grass
        for ty in range(TRACK_SIZE):
            for tx in range(TRACK_SIZE):
                tm.pset(tx, ty, TILES["GRASS"])
                
        num_steps = 2000
        # Pass 1: Road and Gimmicks
        for i in range(num_steps):
            t = (i / num_steps) * len(self.ctrl_points)
            tx, ty = self.get_spline_pt(t)
            itx, ity = int(tx), int(ty)
            
            road_rad = 9
            is_boost_zone = (i % 250 < 15) and i > 50
            
            for dy in range(-road_rad + 1, road_rad):
                for dx in range(-road_rad + 1, road_rad):
                    if dx*dx + dy*dy <= (road_rad-1)**2:
                        rx, ry = itx+dx, ity+dy
                        if 0 <= rx < TRACK_SIZE and 0 <= ry < TRACK_SIZE:
                            if i < 4: # Start line
                                tm.pset(rx, ry, TILES["START"])
                            elif is_boost_zone and abs(dx) < 2 and abs(dy) < 2:
                                tm.pset(rx, ry, TILES["BOOST"])
                            else:
                                if tm.pget(rx, ry) not in [TILES["START"], TILES["BOOST"]]:
                                    tm.pset(rx, ry, TILES["ROAD"])

        # Pass 2: Walls (Only overwrite Grass)
        for i in range(num_steps):
            t = (i / num_steps) * len(self.ctrl_points)
            tx, ty = self.get_spline_pt(t)
            itx, ity = int(tx), int(ty)
            
            road_rad = 9
            for dy in range(-road_rad, road_rad+1):
                for dx in range(-road_rad, road_rad+1):
                    d2 = dx*dx + dy*dy
                    if (road_rad-1)**2 < d2 <= road_rad**2:
                        rx, ry = itx+dx, ity+dy
                        if 0 <= rx < TRACK_SIZE and 0 <= ry < TRACK_SIZE:
                            if tm.pget(rx, ry) == TILES["GRASS"]:
                                tm.pset(rx, ry, TILES["WALL"])

    def get_tile_at(self, x, y):
        tx, ty = int(x / TILE_SIZE), int(y / TILE_SIZE)
        if 0 <= tx < TRACK_SIZE and 0 <= ty < TRACK_SIZE:
            return pyxel.tilemaps[0].pget(tx, ty)
        return TILES["WALL"]
