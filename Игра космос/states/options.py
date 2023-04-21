from states.state import State
import pygame

class Options(State):
    
    
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.bg_image = self.game.bg_image
        self.buttons_color = (255, 255, 255)
        
        self.choice = {0: "resolution", 1: "Controls", 2: "Back"}
        self.cursor_index = 0
        
        self.resolutions = {0: "1920 x 1080", 1: "1280 x 720", 2: "720 x 480"}
        self.resolution_index = self.game.resolution_index
        
        self.cursor_radius = 15
        self.cursor_image = pygame.Surface((self.cursor_radius * 2, self.cursor_radius * 2))
        self.cursor_image.fill("yellow")
        pygame.draw.circle(self.cursor_image, (255, 255, 255), (self.cursor_radius, self.cursor_radius), self.cursor_radius)
        pygame.draw.circle(self.cursor_image, "black", (self.cursor_radius, self.cursor_radius), self.cursor_radius - 3)
        self.cursor_image.set_colorkey("yellow")
        self.cursor_x = self.game.DISPLAY_W/2 - 260
        self.cursor_pos_y = self.game.DISPLAY_H/2 - 80
        self.cursor_y = self.cursor_pos_y
        
        self.fullscreen = self.game.fullscreen
        
    def update_cursor(self, action):
        if action["right"] and self.cursor_index == 0:
            self.resolution_index = (self.resolution_index - 1) % len(self.resolutions)
            self.game.resolution_index = self.resolution_index
            self.resolution_change()
        if action["left"] and self.cursor_index == 0:
            self.resolution_index = (self.resolution_index + 1) % len(self.resolutions)
            self.game.resolution_index = self.resolution_index
            self.resolution_change()
        if action["up"]:
            self.cursor_index = (self.cursor_index - 1) % len(self.choice)
        if action["down"]:
            self.cursor_index = (self.cursor_index + 1) % len(self.choice)
        self.cursor_y = self.cursor_pos_y + 80 * self.cursor_index
        
    def resolution_change(self):
        self.game.DISPLAY_W = int(self.resolutions[self.resolution_index].split(" x ")[0])
        self.game.DISPLAY_H = int(self.resolutions[self.resolution_index].split(" x ")[1])
        self.game.display = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.game.window = pygame.display.set_mode((self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.cursor_x = self.game.DISPLAY_W/2 - 260
        self.cursor_pos_y = self.game.DISPLAY_H/2 - 80
        self.cursor_y = self.cursor_pos_y
        self.prev_state.cursor_x = self.game.DISPLAY_W/2 - 260
        self.prev_state.cursor_pos_y = self.game.DISPLAY_H/2 - 80
        self.prev_state.cursor_y = self.cursor_pos_y
        self.game.reset_keys()
        
    def transition_state(self):
        if self.cursor_index == 0:
            pass
        elif self.cursor_index == 1:
            if self.fullscreen == "OFF":
                self.fullscreen = "ON"
            else:
                self.fullscreen = "OFF"
            pygame.display.toggle_fullscreen()
        elif self.cursor_index == 2:
            self.exit_state()
        
        
    def update(self, dt, action):
        self.update_cursor(action)
        if action["back"]:
            self.exit_state()
        if action["start"]:
            self.transition_state()
        self.game.reset_keys()
            
    def render(self, display):
        display.blit(self.bg_image, (-100, -100))
        self.game.draw_text(display, "Options", 40, "blue", self.game.DISPLAY_W/2 + 3, 100 + 3)
        self.game.draw_text(display, "Options", 40, "white", self.game.DISPLAY_W/2, 100)
        self.game.draw_text(display, "Resolution:", 15, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 120)
        self.game.draw_text(display, f"{self.resolutions[self.resolution_index]}", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 80)
        self.game.draw_text(display, f"Full screen: {self.fullscreen}", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
        self.game.draw_text(display, "Back", 30, self.buttons_color, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 80)
        display.blit(self.cursor_image, (self.cursor_x - self.cursor_radius, self.cursor_y - self.cursor_radius))
        