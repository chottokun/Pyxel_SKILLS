import pyxel

class Audio:
    @staticmethod
    def setup():
        # --- SFX (Ch 3) ---
        pyxel.sounds[0].set("e2e1e2e1", "p", "3", "v", 8)   # Engine (Reduced volume)
        pyxel.sounds[1].set("c2c1", "n", "7", "f", 15)      # Collision
        pyxel.sounds[2].set("g2g3g4b4", "s", "7", "f", 12)  # Boost
        pyxel.sounds[3].set("c3e3g3c4", "p", "7", "v", 15)  # Lap / Clear
        pyxel.sounds[4].set("c3", "p", "7", "v", 10)        # Beep Low
        pyxel.sounds[5].set("c4", "p", "7", "v", 15)        # Beep High
        
        # --- BGM (Ch 0, 1, 2) ---
        # Sound 10: Techno Bassline
        pyxel.sounds[10].set("c2c2g2g2c2c2g2g2", "p", "3", "v", 8)
        
        # Sound 11 & 12: Heroic Racing Melody
        pyxel.sounds[11].set("c3e3g3c4e3g3c4e4", "s", "4", "f", 8)
        pyxel.sounds[12].set("f3a3c4f4e4c4g3e3", "s", "4", "f", 8)
        
        # Sound 13: Drum (Snare/Hi-hat noise)
        pyxel.sounds[13].set("g1g1g1g1", "n", "2", "f", 8)
        
        # Music 0: 
        # Ch 0: Bass (10), Ch 1: Melody (11, 12), Ch 2: Drums (13), Ch 3: SFX
        pyxel.musics[0].set([10], [11, 12], [13], [])
        pyxel.playm(0, loop=True)

    @staticmethod
    def play_engine():
        if pyxel.frame_count % 30 == 0:
            pyxel.play(3, 0)

    @staticmethod
    def play_collision():
        pyxel.play(3, 1)

    @staticmethod
    def play_boost():
        pyxel.play(3, 2)

    @staticmethod
    def play_lap():
        pyxel.play(3, 3)
        
    @staticmethod
    def play_beep_low():
        pyxel.play(3, 4)

    @staticmethod
    def play_beep_high():
        pyxel.play(3, 5)
