from states.state import State
from states.controls import Controls
from states.planet_creation import PlanetCreation
from objects.celestial_body import CelestialBody
import pygame, os, json

class PauseMenu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.menu_img = pygame.Surface((self.game.DISPLAY_W *.3, self.game.DISPLAY_H*.7))
        self.menu_img.fill("white")
        self.menu_x, self.menu_y = self.game.DISPLAY_W*.1 , self.game.DISPLAY_H*.15
        self.menu_options = {0: "Resume", 1: "Save", 2: "Create custom", 3: "Controls", 4: "Exit"}
        self.index = 0
        self.saved = False
        
        
        self.cursor_radius = 15
        self.cursor_img = pygame.Surface((self.cursor_radius  * 2, self.cursor_radius * 2))
        self.cursor_img.fill("white")
        pygame.draw.circle(self.cursor_img, "black", (self.cursor_radius, self.cursor_radius), self.cursor_radius)
        pygame.draw.circle(self.cursor_img, "white", (self.cursor_radius, self.cursor_radius), self.cursor_radius - 3)
        self.cursor_img.set_colorkey("white")
        self.cursor_pos_y = self.menu_y + self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))) 
        self.cursor_x, self.cursor_y = self.menu_x + 50 - self.cursor_radius, self.cursor_pos_y - self.cursor_radius
        
    
    def update_cursor(self, actions):
        if actions["down"]:
            self.index = (self.index + 1) % len(self.menu_options)
        elif actions["up"]:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_y = self.cursor_pos_y + (self.index * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options)))) - self.cursor_radius
    
        
    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions["back"]:
            self.exit_state()
        if actions["start"]:
            self.transition_state()
        self.game.reset_keys()
        
    def render(self, display):
        self.prev_state.render(display)
        self.menu_img.fill("white")
        self.game.draw_text(self.menu_img, "Resume", 30, "black", self.game.DISPLAY_W *.3 / 2, self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        if self.saved:
            self.game.draw_text(self.menu_img, "Saved!", 30, (50, 255, 50), self.game.DISPLAY_W *.3 / 2, 2 * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        else:
            self.game.draw_text(self.menu_img, "Save", 30, "black", self.game.DISPLAY_W *.3 / 2, 2 * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        self.game.draw_text(self.menu_img, "Create Planet", 15, "black", self.game.DISPLAY_W *.3 / 2, 3 * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        self.game.draw_text(self.menu_img, "Controls", 30, "black", self.game.DISPLAY_W *.3 / 2, 4 * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        self.game.draw_text(self.menu_img, "Exit", 30, "black", self.game.DISPLAY_W *.3 / 2, 5 * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        display.blit(self.menu_img, (self.menu_x, self.menu_y))
        display.blit(self.cursor_img, (self.cursor_x, self.cursor_y))
        
        
    def transition_state(self):
        if self.menu_options[self.index] == "Resume":
            self.exit_state()
        elif self.menu_options[self.index] == "Save" and not self.saved:
            self.saved = True
            with open(os.path.join(self.game.save_dir, "save 1.txt"), 'w') as save_file:
                for _, body in CelestialBody.bodies.items():
                    new_dict = {}
                    new_dict["mass"] = body.mass
                    new_dict["radius"] = body.radius
                    new_dict["x"] = float(body.pos[0])
                    new_dict['y'] = float(body.pos[1])
                    new_dict["vx"] = float(body.velocity[0])
                    new_dict["vy"] = float(body.velocity[1])
                    new_dict["color"] = body.color
                    json.dump(new_dict, save_file)
                    save_file.write('\n')
        elif self.menu_options[self.index] == "Create custom":
            new_state = PlanetCreation(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == "Controls":
            new_state = Controls(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == "Exit":
            self.game.scale_factor = 1
            self.game.display_x, self.game.display_y = 0, 0
            self.prev_state.restart()
            self.exit_state()
            self.prev_state.prev_state.exit_state()
            self.prev_state.prev_state.prev_state.exit_state()
            self.game.timeStep = 1 / self.game.fps