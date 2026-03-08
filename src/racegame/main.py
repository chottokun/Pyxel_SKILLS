import pyxel
import math
from constants import *
from audio import Audio
from track import Track
from player import Player

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel F-ZERO 2.7.9")
        
        # Audio & Assets
        Audio.setup()
        self.track = Track()
        
        # Initial Player Position (Near Start Line)
        sx, sy = self.track.get_spline_pt(0)
        nx, ny = self.track.get_spline_pt(0.01)
        angle = math.degrees(math.atan2(ny-sy, nx-sx))
        self.player = Player(sx * TILE_SIZE, sy * TILE_SIZE, angle)
        
        # Camera State
        self.cam_dist = CAM_DIST_BASE
        self.cam_height = CAM_HEIGHT_BASE
        self.pitch = PITCH_BASE
        self.fov = FOV_BASE
        
        # Game State
        self.state = STATE_COUNTDOWN
        self.countdown_timer = 90 # 3 seconds @ 30fps
        self.frame_count = 0
        self.lap_start_frame = 0
        self.best_time = float('inf')
        self.particles = [] # (x, y, z, vx, vy, vz, col, life)
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        # Reset to Start Line (Rescue Bug)
        if pyxel.btnp(pyxel.KEY_R):
            sx, sy = self.track.get_spline_pt(0)
            nx, ny = self.track.get_spline_pt(0.01)
            self.player.x, self.player.y = sx * TILE_SIZE, sy * TILE_SIZE
            self.player.angle = math.degrees(math.atan2(ny-sy, nx-sx))
            self.player.speed = 0
            self.player.vx = 0
            self.player.vy = 0
            self.lap_start_frame = self.frame_count
            self.state = STATE_COUNTDOWN
            self.countdown_timer = 90
            return

        self.frame_count += 1
        
        # Update Particles
        for p in self.particles[:]:
            p[0] += p[3]; p[1] += p[4]; p[2] += p[5]
            p[7] -= 1
            if p[7] <= 0: self.particles.remove(p)

        if self.state == STATE_COUNTDOWN:
            self.countdown_timer -= 1
            if self.countdown_timer % 30 == 0:
                if self.countdown_timer > 0:
                    Audio.play_beep_low()
                else:
                    Audio.play_beep_high()
                    self.state = STATE_RACING
                    self.lap_start_frame = self.frame_count
            return

        # Player Update
        old_speed = self.player.speed
        tile = self.player.update(self.track)
        
        # Collision Detection for Sparks (Speed drop)
        if old_speed > 2.0 and self.player.speed < 0:
             self.spawn_spark(self.player.x, self.player.y)

        # Lap Logic
        if tile == TILES["START"]:
            if self.frame_count - self.lap_start_frame > 300: # Anti-glitch
                lap_time = self.frame_count - self.lap_start_frame
                self.best_time = min(self.best_time, lap_time)
                self.lap_start_frame = self.frame_count
                Audio.play_lap()

        # Dynamic Camera (Extreme Mode 7)
        speed_norm = min(abs(self.player.speed) / (MAX_SPEED * 1.5), 1.0)
        self.pitch = PITCH_BASE + speed_norm * 10
        self.fov = FOV_BASE + speed_norm * 20
        self.cam_height = CAM_HEIGHT_BASE + speed_norm * 5
        self.cam_dist = CAM_DIST_BASE + speed_norm * 8

    def spawn_spark(self, x, y):
        for _ in range(10):
            self.particles.append([
                x, y, 2, # x, y, z
                pyxel.rndf(-2, 2), pyxel.rndf(-2, 2), pyxel.rndf(1, 4), # vx, vy, vz
                pyxel.rndi(7, 10), 15 # col, life
            ])

    def draw(self):
        pyxel.cls(0)
        
        # Starfield & Sky
        for i in range(SCREEN_HEIGHT // 2):
            c = 1 if i < 30 else (5 if i < 60 else 0)
            pyxel.line(0, i, SCREEN_WIDTH, i, c)
            if pyxel.rndf(0, 1) < 0.01:
                pyxel.pset(pyxel.rndi(0, SCREEN_WIDTH), i, 7)

        # Mode 7 Render (bltm3d)
        vx, vy = pyxel.cos(self.player.angle), pyxel.sin(self.player.angle)
        pos = (self.player.x - vx * self.cam_dist, self.player.y - vy * self.cam_dist, self.cam_height)
        rot = (self.pitch, self.player.angle, self.player.tilt * 10)
        pyxel.bltm3d(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, pos, rot, fov=self.fov)
        
        # Render Particles using blt3d (Square particles as 3D effect)
        for p in self.particles:
            # blt3d(x, y, w, h, img, u, v, [u_w], [v_h], [colkey], [cam], [rot], [fov])
            # Simplified: Draw a colored pixel/rect in 3D-ish way if possible, 
            # or just project to screen. Since blt3d is for images, we use a trick.
            pyxel.rect(p[0], p[1], 1, 1, p[6]) # Actually bltm3d is more for the map.

        # Manga Focus Line FX
        if self.player.speed > MAX_SPEED:
            self.draw_focus_lines()

        # Player Draw
        self.player.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 35)

        # HUD & Minimap
        self.draw_hud()
        self.draw_minimap()

        # Countdown UI
        if self.state == STATE_COUNTDOWN:
            num = (self.countdown_timer // 30) + 1
            txt = str(num) if num > 0 else "GO!"
            col = 7 if num > 0 else 10
            pyxel.text(SCREEN_WIDTH // 2 - 4, SCREEN_HEIGHT // 2 - 20, txt, col)

    def draw_minimap(self):
        # Window Background (Solid dark with white border)
        pyxel.rect(MMAP_X - 1, MMAP_Y - 1, MMAP_SIZE + 2, MMAP_SIZE + 2, 1)
        pyxel.rectb(MMAP_X - 1, MMAP_Y - 1, MMAP_SIZE + 2, MMAP_SIZE + 2, 7)
        
        # Draw Accurate Spline Path (64 steps for smooth curve)
        num_steps = 64
        total_len = len(self.track.ctrl_points)
        for i in range(num_steps):
            t1 = (i / num_steps) * total_len
            t2 = ((i + 1) / num_steps) * total_len
            p1 = self.track.get_spline_pt(t1)
            p2 = self.track.get_spline_pt(t2)
            
            x1, y1 = MMAP_X + p1[0] / MMAP_SCALE, MMAP_Y + p1[1] / MMAP_SCALE
            x2, y2 = MMAP_X + p2[0] / MMAP_SCALE, MMAP_Y + p2[1] / MMAP_SCALE
            
            # Draw road with thicker feel (offset lines)
            pyxel.line(x1, y1, x2, y2, 13) 

        # Draw Start Line Marker
        sp = self.track.get_spline_pt(0)
        pyxel.pset(MMAP_X + sp[0] / MMAP_SCALE, MMAP_Y + sp[1] / MMAP_SCALE, 10)
            
        # Draw Player (Precise position mapping)
        px = MMAP_X + (self.player.x / TILE_SIZE) / MMAP_SCALE
        py = MMAP_Y + (self.player.y / TILE_SIZE) / MMAP_SCALE
        
        # Blinking dot for player
        p_col = 8 if pyxel.frame_count % 10 < 5 else 7
        pyxel.circ(px, py, 1, p_col)
        
        # Rank / Lap Info
        pyxel.text(MMAP_X - 12, MMAP_Y + MMAP_SIZE + 5, "POS: 1st/1", 7)

    def draw_focus_lines(self):
        px, py = SCREEN_WIDTH // 2 + self.player.tilt * 12, SCREEN_HEIGHT - 35
        for _ in range(20):
            angle = pyxel.rndf(0, 2 * math.pi)
            dist_start = pyxel.rndf(15, 30)
            dist_end = dist_start + pyxel.rndf(40, 80)
            x1 = px + math.cos(angle) * dist_start
            y1 = py + math.sin(angle) * dist_start
            x2 = px + math.cos(angle) * dist_end
            y2 = py + math.sin(angle) * dist_end
            pyxel.line(x1, y1, x2, y2, 7 if pyxel.frame_count % 2 == 0 else 12)

    def draw_hud(self):
        # Bottom Bar
        pyxel.rect(0, 130, SCREEN_WIDTH, 20, 0)
        pyxel.line(0, 130, SCREEN_WIDTH, 130, 7)
        
        # Speedometer
        max_v = MAX_SPEED * 1.8
        sl = int((abs(self.player.speed) / max_v) * 90)
        pyxel.rect(5, 142, 90, 4, 1)
        pyxel.rect(5, 142, sl, 4, 10 if self.player.speed <= MAX_SPEED else 8)
        pyxel.text(5, 134, f" {int(abs(self.player.speed)*100)} KM/H", 7)
        
        # Time
        ct = self.frame_count - self.lap_start_frame
        pyxel.text(110, 134, f"TIME: {ct//30:02d}.{(ct%30)*3:02d}", 7)
        if self.best_time != float('inf'):
            pyxel.text(110, 142, f"BEST: {self.best_time//30:02d}.{(self.best_time%30)*3:02d}", 11)

if __name__ == "__main__":
    App()
