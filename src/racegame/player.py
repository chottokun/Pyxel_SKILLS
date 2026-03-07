import pyxel
import math
from constants import *
from audio import Audio

class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0
        self.vx = 0
        self.vy = 0
        self.tilt = 0
        self.ship_w = 4 # Collision width

    def update(self, track):
        accel = pyxel.btn(pyxel.KEY_UP)
        brake = pyxel.btn(pyxel.KEY_DOWN)
        
        # 1. Forward/Backward Speed Control
        if accel:
            if self.speed < MAX_SPEED:
                self.speed = min(self.speed + ACCELERATION, MAX_SPEED)
        elif brake:
            self.speed = max(self.speed - DECELERATION * 2, REV_SPEED)
        else:
            if self.speed > MAX_SPEED:
                self.speed = max(self.speed - FRICTION * 4, MAX_SPEED)
            elif self.speed > 0:
                self.speed = max(self.speed - FRICTION, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + FRICTION, 0)

        # 2. Turning & Drift Logic
        is_turning = False
        h_turn_speed = TURN_SPEED * (0.6 + 0.4 * (abs(self.speed) / MAX_SPEED))
        target_tilt = 0
        if abs(self.speed) > 0.01: # Reduced from 0.05 for better low-speed control
            turn_mod = 1.0 if self.speed > 0 else -1.0
            if pyxel.btn(pyxel.KEY_LEFT):
                self.angle -= h_turn_speed * turn_mod
                target_tilt = -1.2 # Stronger tilt for drift feel
                is_turning = True
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.angle += h_turn_speed * turn_mod
                target_tilt = 1.2
                is_turning = True
        
        self.tilt += (target_tilt - self.tilt) * 0.15

        # 3. Momentum & Drift Physics (The "Slide" Effect)
        # Calculate where the ship "wants" to go
        target_vx = pyxel.cos(self.angle) * self.speed
        target_vy = pyxel.sin(self.angle) * self.speed
        
        # Grip factor: How fast the velocity vector matches the ship's angle
        # During turns, grip is lower, causing a slide.
        grip = 0.12 if not is_turning else 0.06
        if self.speed > MAX_SPEED: grip *= 0.5 # Less grip at boost speed
        
        self.vx += (target_vx - self.vx) * grip
        self.vy += (target_vy - self.vy) * grip
        
        # Movement
        new_x, new_y = self.x + self.vx, self.y + self.vy
        
        # 4. Collision Detection
        collision = False
        avg_tile = TILES["ROAD"]
        
        for ox, oy in [(-self.ship_w, -self.ship_w), (self.ship_w, -self.ship_w), 
                       (-self.ship_w, self.ship_w), (self.ship_w, self.ship_w)]:
            tile = track.get_tile_at(new_x + ox, new_y + oy)
            if tile == TILES["WALL"]:
                collision = True
                break
            if tile in [TILES["BOOST"], TILES["START"], TILES["GRASS"]]:
                avg_tile = tile

        if collision:
            self.speed *= -0.2 # Milder bounce
            self.vx *= -0.3
            self.vy *= -0.3
            self.x -= self.vx
            self.y -= self.vy
            Audio.play_collision()
        else:
            if avg_tile == TILES["GRASS"]:
                self.speed *= 0.9
                self.vx *= 0.95
                self.vy *= 0.95
            elif avg_tile == TILES["BOOST"]:
                if self.speed < MAX_SPEED * 1.6:
                    Audio.play_boost()
                    self.speed = min(self.speed + 1.2, MAX_SPEED * 1.8)
            self.x, self.y = new_x, new_y

        if abs(self.speed) > 0.1:
            Audio.play_engine()
        
        return avg_tile

    def draw(self, px, py):
        # High-End Vector Ship (Geometric Design)
        tx = self.tilt * 12
        gh = math.sin(pyxel.frame_count * 0.3) * 1.5
        sha_r = max(2, 4 - int(gh))
        
        # Shadow
        pyxel.circ(px+tx, py+16, sha_r, 1)
        
        is_boost = self.speed > MAX_SPEED
        body_col = 12 if not is_boost else 8
        wing_col = 5 if not is_boost else 14
        
        # Wings (Sharp & Aggressive)
        pyxel.tri(px-4+tx, py+gh+2, px-16+tx, py+gh+16, px-4+tx, py+gh+16, wing_col)
        pyxel.tri(px+4+tx, py+gh+2, px+16+tx, py+gh+16, px+4+tx, py+gh+16, wing_col)
        pyxel.line(px-16+tx, py+gh+16, px-4+tx, py+gh+16, 1)
        pyxel.line(px+16+tx, py+gh+16, px+4+tx, py+gh+16, 1)
        
        # Vertical Fins
        pyxel.line(px-10+tx, py+gh+8, px-10+tx, py+gh+16, 7)
        pyxel.line(px+10+tx, py+gh+8, px+10+tx, py+gh+16, 7)
        
        # Main Body
        pyxel.tri(px+tx, py+gh-8, px-6+tx, py+gh+16, px+6+tx, py+gh+16, body_col)
        
        # Cockpit
        pyxel.rect(px-2+tx, py+gh+2, 4, 8, 6)
        pyxel.rect(px-1+tx, py+gh+3, 2, 4, 12)
        
        # Engine Flame
        if abs(self.speed) > 0.1:
            power = abs(self.speed) / MAX_SPEED
            th = min(30, int(power * 20))
            f_col = 10 if is_boost else 7
            pyxel.tri(px-4+tx, py+gh+16, px+4+tx, py+gh+16, px+tx, py+gh+16+th, f_col)
            if is_boost:
                pyxel.tri(px-2+tx, py+gh+16, px+2+tx, py+gh+16, px+tx, py+gh+16+th//2, 7)
                pyxel.circ(px+tx, py+gh+16+th, 2, 9)
