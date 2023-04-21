from states.state import State
from objects.celestial_body_t import CelestialBodyT
from objects.simulation import Simulation
import pygame, os
import numpy as np
from numpy.random import randint

class PlanetCreation(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.game.state_stack[-2].simulation = True
        pygame.sprite.Group.empty(self.game.state_stack[-2].simulated_path)
        self.menu_img = pygame.Surface((self.game.DISPLAY_W *.25, self.game.DISPLAY_H*.7))
        self.menu_img.fill("white")
        self.menu_x, self.menu_y = self.game.DISPLAY_W*.1, self.game.DISPLAY_H*.15
        self.menu_options = {0: "mass", 1: "radius", 2: "delete", 3: "create", 4: "Exit"}
        self.index = 0
        self.not_available_color = (150, 150, 150)
        self.radius_option = 10
        self.mass_options = {0: "100 kg", 1: "Planet", 2: "Star"}
        self.mass_index = 0
        
        self.created = False
        self.planet_x, self.planet_y = 0, 0
        self.velocity_y, self.velocity_x = 0, 0
        self.id = -1
        self.mass = 100
        
        self.cursor_radius = 15
        self.cursor_img = pygame.Surface((self.cursor_radius  * 2, self.cursor_radius * 2))
        self.cursor_img.fill("white")
        pygame.draw.circle(self.cursor_img, "black", (self.cursor_radius, self.cursor_radius), self.cursor_radius)
        pygame.draw.circle(self.cursor_img, "white", (self.cursor_radius, self.cursor_radius), self.cursor_radius - 3)
        self.cursor_img.set_colorkey("white")
        self.cursor_pos_y = self.menu_y + self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))) 
        self.cursor_x, self.cursor_y = self.menu_x + 40 - self.cursor_radius, self.cursor_pos_y - self.cursor_radius
        
    
    def update_cursor(self, actions):
        if actions["down"]:
            self.index = (self.index + 1) % len(self.menu_options)
        elif actions["up"]:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_y = self.cursor_pos_y + (self.index * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options)))) - self.cursor_radius
    
        
    def update(self, delta_time, actions):
        self.color_update()
        self.update_cursor(actions)
        self.radius_update(actions)
        self.mass_update(actions)
        self.creat_update(actions)
        self.update_velocity(actions)
        if actions["back"]:
            self.exit_state()
        if actions["start"]:
            self.transition_state()
        self.game.reset_keys()
        
    def render(self, display):
        self.prev_state.prev_state.render(display)
        self.prev_state.prev_state.draw_simulated_path(display)
        self.draw_planet_ghost(display, self.created)
        self.menu_img.fill("white")
        self.game.draw_text(self.menu_img, "Mass:", 10, "black", self.game.DISPLAY_W *.25 / 2, -40 + self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        self.game.draw_text(self.menu_img, self.mass_options[self.mass_index], 20, "black", self.game.DISPLAY_W *.25 / 2, self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        self.game.draw_text(self.menu_img, "Radius:", 10, "black", self.game.DISPLAY_W *.25 / 2, -40 + 2 * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        self.game.draw_text(self.menu_img, str(self.radius_option), 20, "black", self.game.DISPLAY_W *.25 / 2, 2 * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        self.game.draw_text(self.menu_img, "Delete", 20, self.not_available_color, self.game.DISPLAY_W *.25 / 2, 3 * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        self.game.draw_text(self.menu_img, "Create", 20, self.not_available_color, self.game.DISPLAY_W *.25 / 2, 4 * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        self.game.draw_text(self.menu_img, "Exit", 30, "black", self.game.DISPLAY_W *.25 / 2, 5 * self.game.DISPLAY_H*.7 / (1 + (len(self.menu_options))))
        self.menu_img.set_alpha(150)
        self.cursor_img.set_alpha(150)
        display.blit(self.menu_img, (self.menu_x, self.menu_y))
        display.blit(self.cursor_img, (self.cursor_x, self.cursor_y))
        
    def draw_planet_ghost(self, display, created):
        if created: 
            alpha = 0
        else:
            alpha = 100
        radius = self.radius_option * self.prev_state.prev_state.zoom
        planet_phost = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(planet_phost, "white", (radius, radius) , radius)
        planet_phost.set_colorkey("black")
        planet_phost.set_alpha(alpha)
        display.blit(planet_phost, (self.planet_x, self.planet_y))
        
    def update_velocity(self, action):
        if action['lmb'] and self.created:
            vx, vy = 0, 0
            zoom = self.prev_state.prev_state.zoom * 2
            scale = 1
            if self.game.scale_factor != 1:
                scale = self.game.scale_factor / 30000
            x, y = CelestialBodyT.bodies[self.id].pos
            x, y = self.prev_state.prev_state.transform_coordinates(x, y)
            if self.prev_state.prev_state.planet_to_lock_on != -1:
                vx, vy = CelestialBodyT.bodies[self.prev_state.prev_state.planet_to_lock_on].velocity
            self.velocity_x, self.velocity_y = vx + (pygame.mouse.get_pos()[0] - x) * scale / zoom, vy +  (pygame.mouse.get_pos()[1] - y) * scale / zoom
            self.prev_state.prev_state.celestial_bodies[self.id].velocity = np.array((self.velocity_x, self.velocity_y))
            CelestialBodyT.bodies[self.id].velocity = np.array((self.velocity_x, self.velocity_y))
            Simulation.simulated_bodies = {}
            pygame.sprite.Group.empty(self.prev_state.prev_state.simulated_path)
            self.prev_state.prev_state.simulate(80)
            self.game.reset_keys()
            
    def calculate_orbit(self, x, y):
        G =  6.67E-11
        r0 = CelestialBodyT.bodies[self.prev_state.prev_state.planet_to_lock_on].pos
        r1 = np.array((x, y))
        r = (r1 - r0) * self.game.scale_factor
        v = np.sqrt(G * CelestialBodyT.bodies[self.prev_state.prev_state.planet_to_lock_on].mass / np.linalg.norm(r))
        turn_matrix = np.array(((0, 1), (-1, 0)))
        r = np.matmul(turn_matrix, r) / np.linalg.norm(r)
        print(v)
        return (v * r[0], v * r[1])
        
    def creat_update(self, action):
        if action["lmb"] and not self.created:
            self.created = True
            display_x = self.prev_state.prev_state.display_x
            display_y = self.prev_state.prev_state.display_y
            zoom = self.prev_state.prev_state.zoom
            x = (pygame.mouse.get_pos()[0] + 2 * display_x + (zoom - 1) * (self.game.DISPLAY_W / 2 + 2 * display_x)) / zoom
            y = (pygame.mouse.get_pos()[1] + 2 * display_y + (zoom - 1) * (self.game.DISPLAY_H / 2 + 2 * display_y)) / zoom
            vx, vy = 0, 0
            if self.prev_state.prev_state.planet_to_lock_on != -1:
                v = self.calculate_orbit(x, y)
                vx, vy = CelestialBodyT.bodies[self.prev_state.prev_state.planet_to_lock_on].velocity
                vx += v[0]
                vy += v[1]
            new_planet = CelestialBodyT(self.game, self.mass, self.radius_option, x, y, vx, vy, [randint(0, 256) for _ in range(3)])
            self.prev_state.prev_state.celestial_bodies[new_planet.id] = new_planet
            self.id = new_planet.id
            self.prev_state.prev_state.simulate(100)
            self.game.reset_keys()
        elif not self.created:
            self.planet_x, self.planet_y = pygame.mouse.get_pos()[0] - self.radius_option * self.prev_state.prev_state.zoom , pygame.mouse.get_pos()[1] - self.radius_option * self.prev_state.prev_state.zoom
        
    def radius_update(self, action):
        if (action["scroll_up"] or action["scroll_down"] or self.menu_options[self.index] == "radius") and not self.created:
            if action["right"] or action["scroll_up"]:
                self.radius_option += 1
                if self.radius_option >= 100:
                    self.radius_option -= 1
            if action["left"] or action["scroll_down"]:
                self.radius_option -= 1
                if self.radius_option <= 0:
                    self.radius_option += 1
    
    def mass_update(self, action):
        if self.menu_options[self.index] == "mass" and not self.created:
            if action["right"]:
                self.mass_index = (self.mass_index + 1) % len(self.mass_options)
            if action["left"]:
                self.mass_index = (self.mass_index - 1) % len(self.mass_options)
        if self.mass_index == 0:
            self.mass = 100
        elif self.mass_index == 1:
            self.mass = 1E13
        elif self.mass_index == 2:
            self.mass = 1E16
                
    def color_update(self):
        if self.created:
            self.not_available_color = "black"
        else:
            self.not_available_color = (150, 150, 150)
        
    def transition_state(self):
        if self.menu_options[self.index] == "delete" and self.created:
            self.created = False
            del self.prev_state.prev_state.celestial_bodies[self.id]
            del CelestialBodyT.bodies[self.id]
            Simulation.simulated_bodies = {}
            pygame.sprite.Group.empty(self.prev_state.prev_state.simulated_path)
        elif self.menu_options[self.index] == "create" and self.created:
            self.created = False
            Simulation.simulated_bodies = {}
            pygame.sprite.Group.empty(self.prev_state.prev_state.simulated_path)
        elif self.menu_options[self.index] == "Exit":
            self.exit_state()