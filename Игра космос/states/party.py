from states.state import State
import pygame, os

class PartyMenu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        
    def update(self, delta_time, actions):
        if actions["back"]:
            self.exit_state()
        self.game.reset_keys()
        
    def render(self, display):
        display.fill("white")
        self.game.draw_text(display, "PARTY MENU", 60, (0, 0, 0), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)