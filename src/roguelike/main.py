import pyxel
import sys
import os
import math

sys.path.append(os.path.dirname(__file__))

from map_gen import Map, TILE_WALL, TILE_STAIRS, TILE_CHEST
from entities import Player, Enemy

SCENE_TITLE = 0
SCENE_PLAYING = 1
SCENE_GAMEOVER = 2

class App:
    def __init__(self):
        pyxel.init(160, 120, title="探索者と闇の迷宮・DX", fps=30)
        self.setup_graphics()
        
        self.scene = SCENE_TITLE
        self.high_score = 0
        self.score = 0
        self.floor = 1
        self.player_hp = 40
        self.shake = 0
        self.flash_timer = 0
        self.frame = 0
        self.message = ""
        
        # タイトルBGMを開始
        self.play_scene_bgm()
        
        pyxel.run(self.update, self.draw)

    def setup_graphics(self):
        # タイル画像
        pyxel.images[0].set(0, 0, ["00000000","00500000","00000000","00001000","00000000","01000000","00000000","00000500"])
        pyxel.images[0].set(8, 0, ["11111115","1CC1CC15","1C51C515","11111115","1CC1CC15","1C51C515","11111115","55555555"])
        pyxel.images[0].set(16, 0, ["00000000","07777770","07000070","07777770","00000000","00000000","01111110","11111111"])
        pyxel.images[0].set(24, 0, ["00000000","0AAAAAA0","0A7A7A70","0AAAAAA0","04444440","04444440","00000000","00000000"])
        # アイコン
        pyxel.images[0].set(32, 0, ["00000000","08808800","88888880","88888880","08888800","00888000","00080000","00000000"])
        pyxel.images[0].set(40, 0, ["00000000","00AAA000","0A777A00","0A7A7A00","0A777A00","00AAA000","00000000","00000000"])
        # キャラクター
        pyxel.images[0].set(16, 8, ["000BB000","00BEEB00","0BEEEEE0","0BE77EB0","0BE11EB0","0BEEEEE0","00BEEB00","000BB000"])
        pyxel.images[0].set(24, 8, ["00000000","00222200","02222220","22A22A22","22222222","22222222","02222220","00000000"])

    def play_scene_bgm(self):
        """現在のシーンに応じたBGMを生成・再生する"""
        if self.scene == SCENE_TITLE:
            # プリセット0: 明るい・軽快な曲
            pyxel.gen_bgm(0, 0, 10, play=True)
        elif self.scene == SCENE_PLAYING:
            # プリセット1: 暗い・ダンジョン曲
            pyxel.gen_bgm(1, 1, 123, play=True)
        elif self.scene == SCENE_GAMEOVER:
            # プリセット2: 悲しげ・寂しい曲
            pyxel.gen_bgm(2, 0, 5, play=True)

    def start_game(self, next_floor=False):
        if not next_floor:
            self.floor = 1
            self.score = 0
            self.player_hp = 40
            self.scene = SCENE_PLAYING
            self.play_scene_bgm()
        
        self.game_map = Map(20, 14)
        self.game_map.generate(self.floor)
        
        px, py = self.game_map.rooms[0]
        self.player = Player(px, py)
        self.player.hp = self.player_hp
        
        self.enemies = []
        num_enemies = 1 + min(self.floor // 2, 5) 
        for i in range(1, len(self.game_map.rooms)):
            if len(self.enemies) < num_enemies:
                ex, ey = self.game_map.rooms[i]
                self.enemies.append(Enemy(ex, ey))

        self.message = f"地下 {self.floor} 階へ..."
        self.shake = 0

    def update(self):
        self.frame += 1
        if self.flash_timer > 0: self.flash_timer -= 1
        if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()

        if self.scene == SCENE_TITLE:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.start_game()
        elif self.scene == SCENE_PLAYING:
            self.update_playing()
        elif self.scene == SCENE_GAMEOVER:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.scene = SCENE_TITLE
                self.play_scene_bgm()

    def update_playing(self):
        if self.shake > 0: self.shake -= 1
        player_turn = False
        dx, dy = 0, 0
        
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W): dy = -1
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S): dy = 1
        elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A): dx = -1
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D): dx = 1
        elif pyxel.btnp(pyxel.KEY_SPACE): player_turn = True

        if dx != 0 or dy != 0:
            tx, ty = self.player.x + dx * 8, self.player.y + dy * 8
            target = next((e for e in self.enemies if e.x == tx and e.y == ty), None)
            
            if target:
                target.hp -= 5
                target.shake = 5
                self.message = "魔物を攻撃！"
                self.shake = 4
                pyxel.play(3, 0)
                if target.hp <= 0: 
                    self.enemies.remove(target)
                    self.score += 100
                    self.message = "魔物を討伐！ +100pts"
                player_turn = True
            elif self.player.move(dx, dy, [(1,0)]):
                player_turn = True
                
                tm = pyxel.tilemaps[0]
                px, py = int(self.player.x // 8), int(self.player.y // 8)
                tile = tm.pget(px, py)
                
                if tile == TILE_STAIRS:
                    self.floor += 1
                    self.score += 500
                    self.player_hp = self.player.hp
                    self.start_game(next_floor=True)
                    return
                elif tile == TILE_CHEST:
                    self.player.hp = min(40, self.player.hp + 10)
                    self.score += 200
                    self.message = "薬草で回復！ +200pts"
                    tm.pset(px, py, (0,0))
                    pyxel.play(3, 1)

        if player_turn:
            for enemy in self.enemies:
                did_attack = enemy.take_turn(self.player, [(1,0)])
                if did_attack:
                    self.player.hp -= 3
                    self.message = "ダメージを受けた！"
                    self.shake = 5
                    self.flash_timer = 4
                    pyxel.play(3, 2)
                    if self.player.hp <= 0:
                        self.scene = SCENE_GAMEOVER
                        self.high_score = max(self.high_score, self.score)
                        self.play_scene_bgm() # ゲームオーバー曲

    def draw(self):
        if self.flash_timer > 0: pyxel.cls(8)
        else: pyxel.cls(0)
            
        if self.scene == SCENE_TITLE: self.draw_title()
        elif self.scene == SCENE_PLAYING: self.draw_playing()
        elif self.scene == SCENE_GAMEOVER: self.draw_gameover()

    def draw_title(self):
        pyxel.text(45, 30, "探索者と闇の迷宮", pyxel.frame_count % 16)
        pyxel.text(50, 40, "EXPLORER IN DARK", 7)
        pyxel.blt(76, 55, 0, 16, 8, 8, 8, 0)
        pyxel.text(55, 80, f"HIGH SCORE: {self.high_score:05}", 10)
        if (pyxel.frame_count // 15) % 2 == 0: pyxel.text(52, 100, "PRESS [SPACE] START", 7)

    def draw_playing(self):
        off_x = pyxel.rndi(-self.shake, self.shake) if self.shake > 0 else 0
        off_y = pyxel.rndi(-self.shake, self.shake) if self.shake > 0 else 0
        pyxel.camera(-off_x, -off_y)
        self.game_map.draw(self.player.x, self.player.y, 6)
        px, py = int(self.player.x // 8), int(self.player.y // 8)
        for enemy in self.enemies:
            ex, ey = int(enemy.x // 8), int(enemy.y // 8)
            if abs(ex - px) + abs(ey - py) <= 6: enemy.draw()
        bob = math.sin(self.frame * 0.2) * 1.0
        pyxel.blt(self.player.x, self.player.y + bob, 0, self.player.u, self.player.v, 8, 8, 0)
        pyxel.camera()
        self.draw_interface()

    def draw_gameover(self):
        self.draw_playing()
        pyxel.rect(0, 0, 160, 120, 1)
        pyxel.text(60, 40, "GAME OVER", 8)
        pyxel.text(50, 60, f"REACHED: B{self.floor:02}F", 7)
        pyxel.text(50, 70, f"FINAL SCORE: {self.score:05}", 10)
        if (pyxel.frame_count // 15) % 2 == 0: pyxel.text(45, 100, "PRESS [SPACE] TO TITLE", 7)

    def draw_interface(self):
        pyxel.rect(0, 100, 160, 20, 1)
        pyxel.line(0, 100, 160, 100, 6)
        pyxel.blt(4, 104, 0, 32, 0, 8, 8, 0)
        pyxel.rectb(14, 105, 42, 6, 7)
        hp_width = int((max(0, self.player.hp) / 40) * 40)
        bar_color = 11 if self.player.hp > 15 else 8
        if hp_width > 0: pyxel.rect(15, 106, hp_width, 4, bar_color)
        pyxel.blt(62, 104, 0, 16, 0, 8, 8, 0)
        pyxel.text(72, 106, f"B{self.floor:02}F", 7)
        pyxel.blt(95, 104, 0, 40, 0, 8, 8, 0)
        pyxel.text(105, 106, f"{self.score:05}pts", 10)
        pyxel.text(14, 113, self.message, 10)

if __name__ == "__main__":
    App()
