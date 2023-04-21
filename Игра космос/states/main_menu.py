from states.state import State
from states.load_screen import LoadScreen
from states.controls import Controls
from states.options import Options
import pygame

class MainMenu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.bg_image = self.game.bg_image
        self.buttons_color = (255, 255, 255)
        
        self.choice = {0: "Solar System", 1: "Controls", 2: "options", 3: "Exit"}
        self.cursor_index = 0
        
        self.cursor_radius = 15
        self.cursor_image = pygame.Surface((self.cursor_radius * 2, self.cursor_radius * 2))
        self.cursor_image.fill("yellow")
        pygame.draw.circle(self.cursor_image, (255, 255, 255), (self.cursor_radius, self.cursor_radius), self.cursor_radius)
        pygame.draw.circle(self.cursor_image, "black", (self.cursor_radius, self.cursor_radius), self.cursor_radius - 3)
        self.cursor_image.set_colorkey("yellow")
        self.cursor_x = self.game.DISPLAY_W/2 - 240
        self.cursor_pos_y = self.game.DISPLAY_H/2 - 80
        self.cursor_y = self.cursor_pos_y
        
    def update_cursor(self, action):
        if action["up"]:
            self.cursor_index = (self.cursor_index - 1) % len(self.choice)
        if action["down"]:
            self.cursor_index = (self.cursor_index + 1) % len(self.choice)
        self.cursor_y = self.cursor_pos_y + 80 * self.cursor_index
        
    def transition_state(self):
        if self.cursor_index == 0:
            new_state = LoadScreen(self.game)
            new_state.enter_state()
        elif self.cursor_index == 1:
            new_state = Controls(self.game)
            new_state.enter_state()
        elif self.cursor_index == 3:
            self.game.running, self.game.playing = False, False
        elif self.cursor_index == 2:
            new_state = Options(self.game)
            new_state.enter_state()
        
        
    def update(self, dt, action):
        self.update_cursor(action)
        if action["start"]:
            self.transition_state()
        self.game.reset_keys()
            
    def render(self, display):
        display.blit(self.bg_image, (-100, -100))
        self.game.draw_text(display, "2D Space Simulator", 40, "blue", self.game.DISPLAY_W/2 + 3, 100 + 3)
        self.game.draw_text(display, "2D Space Simulator", 40, "white", self.game.DISPLAY_W/2, 100)
        self.game.draw_text(display, "Start the game", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 80)
        self.game.draw_text(display, "Controls", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
        self.game.draw_text(display, "Options", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 80)
        self.game.draw_text(display, "Exit", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 160)
        display.blit(self.cursor_image, (self.cursor_x - self.cursor_radius, self.cursor_y - self.cursor_radius))
        