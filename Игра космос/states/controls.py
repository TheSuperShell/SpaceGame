from states.state import State

class Controls(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.bg_image = self.game.bg_image
        self.upped_coord = 80
        self.diff = int((self.game.DISPLAY_H - 300) / 8)
        
    def update(self, dt, action):
        if action["back"]:
            self.exit_state()
            self.game.reset_keys()
    
    def render(self, display):
        display.blit(self.bg_image, (-100, -100))
        self.game.draw_text(display, "Controls", 40, "blue", self.game.DISPLAY_W/2 + 3, self.upped_coord + 3)
        self.game.draw_text(display, "Controls", 40, "white", self.game.DISPLAY_W/2, self.upped_coord)
        self.game.draw_text(display, "SPACE - time stop", 30, "white", self.game.DISPLAY_W/2, self.upped_coord + self.diff)
        self.game.draw_text(display, "w - time speed up", 30, "white", self.game.DISPLAY_W/2, self.upped_coord + self.diff * 2)
        self.game.draw_text(display, "s - time speed down", 30, "white", self.game.DISPLAY_W/2, self.upped_coord + self.diff * 3)
        self.game.draw_text(display, "r - reverse time", 30, "white", self.game.DISPLAY_W/2, self.upped_coord + self.diff * 4)
        self.game.draw_text(display, "t - toggle trails", 30, "white", self.game.DISPLAY_W/2, self.upped_coord + self.diff * 5)
        self.game.draw_text(display, "g - future simulation (EXPERIMENTAL)", 30, "white", self.game.DISPLAY_W/2, self.upped_coord + self.diff *  6)
        self.game.draw_text(display, "LMB - drag the camera", 30, "white", self.game.DISPLAY_W/2, self.upped_coord + self.diff *  7)
        self.game.draw_text(display, "RMB - create random planet", 30, "white", self.game.DISPLAY_W/2, self.upped_coord + self.diff *  8)
        self.game.draw_text(display, "to exit press 'esc'", 20, "white", self.game.DISPLAY_W/2, self.game.DISPLAY_H - 50)
        