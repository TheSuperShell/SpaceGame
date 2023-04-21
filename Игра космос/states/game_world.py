from states.state import State
from states.pause_menu import PauseMenu
import pygame, os
import numpy as np
from numpy.random import randint

class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.bg_image = game.bg_image
        self.player = Player(game)
        
    def update(self, delta_time, actions):
        if actions["back"]:
            self.game.reset_keys()
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions)
    
    def render(self, display):
        display.blit(self.bg_image, (0,0))
        self.player.render(display)
        
class Player():
    def __init__(self, game):
        self.game = game
        self.load_sprites()
        self.position_x, self.position_y = 200, 200
        self.current_frame, self.last_frame_update = 0, 0
        
    def update(self, delta_time, actions):
        direction_x = actions["right"] - actions["left"]
        direction_y = actions["down"] - actions["up"]
        
        self.position_x += 100 * delta_time * direction_x
        self.position_y += 100 * delta_time * direction_y
        self.animate(delta_time, direction_x, direction_y)
        
    def render(self, display):
        display.blit(self.curr_image, (self.position_x, self.position_y))
        
    def animate(self, delta_time, direction_x, direction_y):
        self.last_frame_update += delta_time
        
        if not (direction_x or direction_y):
            self.curr_image = self.curr_anim_list[0]
            return
        
        if direction_x:
            if direction_x > 0: self.curr_anim_list = self.right_sprites
            else: self.curr_anim_list = self.left_sprites
        if direction_y:
            if direction_y > 0: self.curr_anim_list = self.front_sprites
            else: self.curr_anim_list = self.back_sprites
            
        if self.last_frame_update > .15:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame +1) % len(self.curr_anim_list)
            self.curr_image = self.curr_anim_list[self.current_frame]
            
    def load_sprites(self):
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.front_sprites, self.back_sprites, self.left_sprites, self.right_sprites = [], [], [], []
        
        for i in range(1, 5):
            self.front_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_front" + str(i) + ".png")))
            self.back_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_back" + str(i) + ".png")))
            self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_right" + str(i) + ".png")))
            self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_left" + str(i) + ".png")))
            
        self.curr_image = self.front_sprites[0]
        self.curr_anim_list = self.front_sprites