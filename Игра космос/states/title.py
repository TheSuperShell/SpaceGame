from states.state import State
from states.animations.title_animation import TitleAnimation
import pygame
import numpy as np

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.bg_image = game.bg_image
        self.animated_text = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.game.draw_text(self.animated_text, 'press Enter', 15, "white", self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 50)
        self.animated_text.set_colorkey("black")
        self.transp = 255
        self.iter = 0.
        
    
    def alpha_set(self):
        self.animated_text.set_alpha(self.transp)
        self.transp = int(255 * np.cos(self.iter / 180 * np.pi) ** 2)
        self.iter += 1
        
        
    
    def update(self, delta_time, actions):
        self.alpha_set()
        if actions["start"]:
            new_state = TitleAnimation(self.game)
            new_state.enter_state()
        self.game.reset_keys()
        
    def render(self, display):
        display.blit(self.bg_image, (-100, -100))
        display.blit(self.animated_text, (0,0))
        self.game.draw_text(display, "2D Space Simulator", 40, "blue", self.game.DISPLAY_W/2 + 3, self.game.DISPLAY_H/2 + 3)
        self.game.draw_text(display, "2D Space Simulator", 40, "white", self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
        
        