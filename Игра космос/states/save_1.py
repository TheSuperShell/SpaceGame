from states.space import Space
from objects.celestial_body import CelestialBody
import os, json


class Save1(Space):
    def __init__(self, game):
        Space.__init__(self, game)
        self.loadBodies()
        
    def loadBodies(self):
        with open(os.path.join(self.game.save_dir, "save 1.txt")) as save_file:
            for line in save_file:
                new = json.loads(line)
                new_body = CelestialBody(self.game, new["mass"], new["radius"], new["x"], new["y"], new["vx"], new["vy"], new["color"])
                self.celestial_bodies[new_body.id] = new_body
        
    def update(self, delta_time, action):
        Space.update(self, delta_time, action)
        
        
    
    def render(self, display):
        Space.render(self, display)
        