from states.state import State
from states.main_menu import MainMenu

class TitleAnimation(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.bg_image = self.game.bg_image
        self.title_y = self.game.DISPLAY_H/2
        
    def update(self, dt, action):
        self.title_y -= 4
        if self.title_y <= 100 or action["start"]:
            self.exit_state()
            new_state = MainMenu(self. game)
            new_state.enter_state()  
        self.game.reset_keys()
    
    def render(self, display):
        display.blit(self.bg_image, (-100,-100))
        self.game.draw_text(display, "2D Space Simulator", 40, "blue", self.game.DISPLAY_W/2 + 3, self.title_y + 3)
        self.game.draw_text(display, "2D Space Simulator", 40, "white", self.game.DISPLAY_W/2, self.title_y)