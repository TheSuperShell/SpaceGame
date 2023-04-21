from objects.celestial_body import CelestialBody
from objects.body import Body
import numpy as np

class Simulation(CelestialBody):
    
    simulated_bodies = {}
    dTime = 0.1
    
    def __init__(self, game, mass, radius, x, y, vx, vy, color):
        CelestialBody.__init__(self, game, mass, radius, x, y, vx, vy, color)
        del CelestialBody.bodies[self.id]
        
    def updateVelocity(self):
        for key, otherBody in Simulation.simulated_bodies.items():
            if otherBody != self:
                G = 6.67E-11
                dist = np.linalg.norm(self.pos - otherBody.pos) * self.game.scale_factor
                acceleration = G * otherBody.mass / dist ** 3 * (otherBody.pos - self.pos) * self.game.scale_factor
                self.velocity = self.velocity + acceleration * Simulation.dTime
                
    def update(self):
        self.pos = self.pos + self.velocity * Simulation.dTime / self.game.scale_factor
        
    @staticmethod
    def refresh():
        Simulation.simulated_bodies = {}