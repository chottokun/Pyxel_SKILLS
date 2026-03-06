import pyxel

class Animator:
    def __init__(self, animations, default_state="idle"):
        """
        animations: { "state": { "frames": [(u, v, w, h), ...], "speed": n, "loop": True }, ... }
        """
        self.animations = animations
        self.state = default_state
        self.frame_index = 0
        self.tick = 0
        self.is_finished = False

    def set_state(self, new_state, force=False):
        if self.state != new_state or force:
            self.state = new_state
            self.frame_index = 0
            self.tick = 0
            self.is_finished = False

    def update(self):
        anim = self.animations.get(self.state)
        if not anim:
            return

        self.tick += 1
        if self.tick >= anim["speed"]:
            self.tick = 0
            self.frame_index += 1
            
            if self.frame_index >= len(anim["frames"]):
                if anim.get("loop", True):
                    self.frame_index = 0
                else:
                    self.frame_index = len(anim["frames"]) - 1
                    self.is_finished = True

    def draw(self, x, y, img=0, colkey=0, flip_x=False, flip_y=False, rotate=None, scale=None):
        anim = self.animations.get(self.state)
        if not anim:
            return

        u, v, w, h = anim["frames"][self.frame_index]
        
        # Handle flipping
        w = -w if flip_x else w
        h = -h if flip_y else h
        
        # 新しいPyxel API: rotate と scale に対応
        pyxel.blt(x, y, img, u, v, w, h, colkey, rotate=rotate, scale=scale)

# Example Usage:
# ANIMATIONS = {
#     "idle": { "frames": [(0,0,8,8), (8,0,8,8)], "speed": 15, "loop": True },
#     "run":  { "frames": [(16,0,8,8), (24,0,8,8)], "speed": 8, "loop": True }
# }
# animator = Animator(ANIMATIONS)
# animator.update()
# animator.draw(player.x, player.y, rotate=45, scale=2.0)
