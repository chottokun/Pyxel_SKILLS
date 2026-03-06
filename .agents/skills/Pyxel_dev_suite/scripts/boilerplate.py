import pyxel

class App:
    def __init__(self, width=160, height=120, title="Pyxel App"):
        pyxel.init(width, height, title=title)
        # TODO: Load resources
        # pyxel.load("assets.pyxres")
        
        # Initialize game state
        self.x = 0
        self.y = 0
        
        pyxel.run(self.update, self.draw)

    def update(self):
        # Handle input
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 2
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 2
            
        # Update game objects
        pass

    def draw(self):
        # Clear screen
        pyxel.cls(0)
        
        # Draw game objects
        pyxel.rect(self.x, self.y, 8, 8, 9)
        
        # Draw UI
        pyxel.text(5, 5, f"POS: {self.x}, {self.y}", 7)

if __name__ == "__main__":
    App()
