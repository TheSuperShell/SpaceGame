import pygame
from numpy.random import randint
import numpy as np

class Particles():
    
    particle_list = []
    
    def __init__(self, game, x, y):
        self.game = game
        self.x = x + randint(-1, 1)
        self.y = y + randint(-1, 1)
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, "white", (5, 5), 5)
        self.image.set_colorkey("black")
        v = randint(0, 100) / 100 
        alpha = randint(0, 359) / 180 * np.pi
        self.vx = v * np.sin(alpha)
        self.vy = v * np.cos(alpha)
        self.life_time = 60
        self.age = self.life_time
        
    def update(self):
        self.image.set_alpha(int(300 / self.life_time * self.age))
        self.x += self.vx
        self.y += self.vy
        if self.age <= 0:
            Particles.particle_list.pop(0)
        self.age -= 1