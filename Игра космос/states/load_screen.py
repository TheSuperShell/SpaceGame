from states.state import State
from states.solar_system import SolarSystem
from states.infinity import Infinity
from states.save_1 import Save1
from states.real_sol import RealSol
import pygame

class LoadScreen(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.bg_image = self.game.bg_image
        self.buttons_color = (255, 255, 255)
        
        self.choice = {0: "Solar System", 1: "Empty", 3: "Real Solar", 2: "save 1", 4: "Back"}
        self.cursor_index = 0
        
        self.cursor_radius = 15
        self.cursor_image = pygame.Surface((self.cursor_radius * 2, self.cursor_radius * 2))
        self.cursor_image.fill("yellow")
        pygame.draw.circle(self.cursor_image, (255, 255, 255), (self.cursor_radius, self.cursor_radius), self.cursor_radius)
        pygame.draw.circle(self.cursor_image, "black", (self.cursor_radius, self.cursor_radius), self.cursor_radius - 3)
        self.cursor_image.set_colorkey("yellow")
        self.cursor_x = self.game.DISPLAY_W/2 - 220
        self.cursor_pos_y = self.game.DISPLAY_H/2 - 80
        self.cursor_y = self.cursor_pos_y
        
    def update_cursor(self, action):
        if action["up"]:
            self.cursor_index = (self.cursor_index - 1) % 5
        if action["down"]:
            self.cursor_index = (self.cursor_index + 1) % 5
        self.cursor_y = self.cursor_pos_y + 80 * self.cursor_index
        
    def transition_state(self):
        if self.cursor_index == 0:
            new_state = SolarSystem(self.game)
            new_state.enter_state()
        elif self.cursor_index == 1:
            new_state = Infinity(self.game)
            new_state.enter_state()
        elif self.cursor_index == 4:
            self.exit_state()
        elif self.cursor_index == 2:
            new_state = Save1(self.game)
            new_state.enter_state()
        elif self.cursor_index == 3:
            new_state = RealSol(self.game)
            new_state.enter_state()
        
        
    def update(self, dt, action):
        self.update_cursor(action)
        if action["back"]:
            self.exit_state()
        if action["start"]:
            self.transition_state()
        self.game.reset_keys()
            
    def render(self, display):
        display.blit(self.bg_image, (-100, -100))
        self.game.draw_text(display, "Load screen", 40, "blue", self.game.DISPLAY_W/2 + 3, 100 + 3)
        self.game.draw_text(display, "Load screen", 40, "white", self.game.DISPLAY_W/2, 100)
        self.game.draw_text(display, "Solar System", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 80)
        self.game.draw_text(display, "Empty", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
        self.game.draw_text(display, "Save 1", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 80)
        self.game.draw_text(display, "Real Solar", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 160)
        self.game.draw_text(display, "Back", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 240)
        display.blit(self.cursor_image, (self.cursor_x - self.cursor_radius, self.cursor_y - self.cursor_radius))
        