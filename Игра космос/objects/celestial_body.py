from objects.body import Body
import numpy as np
import os, pygame

class CelestialBody(Body):
    
    
    def __init__(self, game, mass, radius, x, y, vx, vy, color):
        Body.__init__(self, game, mass, x, y, vx, vy)
        self.radius = radius
        self.color = color
        self.png = False
        if type(color) == str and len(color) > 4 and color[-4:] == ".png":
            folder = os.path.join(self.game.sprite_dir, "celestial bodies")
            self.body_image = pygame.image.load(os.path.join(folder, color))
            self.color = (255, 255, 255)
            self.png = True
        
    def update(self):
        Body.update(self)
        
        
    def collision_check(self, otherBody):
        return otherBody != self and np.linalg.norm(self.pos - otherBody.pos) <= self.radius + otherBody.radius
    
    def render(self, display, x, y, zoom, space):
        radius = self.radius * zoom
        if not self.png:
            body_image = pygame.Surface((radius * 2, radius * 2))
            pygame.draw.circle(body_image, self.color, (radius, radius), radius)
            body_image.set_colorkey("black")
        else:
            body_image = pygame.transform.scale(self.body_image, (int(radius * 2), int(radius * 2)))
        display.blit(body_image, space.transform_coordinates(self.pos[0] - self.radius, self.pos[1] - self.radius))
        
    
    

    
    