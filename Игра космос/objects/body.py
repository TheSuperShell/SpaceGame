import numpy as np
import pygame


class Body():
	bodies = {}
	G = 6.67E-11

	def __init__(self, game, mass, x, y, vx, vy):
		body_id = 0
		while body_id in Body.bodies:
			body_id += 1

		self.id = body_id
		self.game = game
		self.mass = mass
		self.pos = np.array((x, y))
		self.velocity = np.array((vx, vy))
		Body.bodies[self.id] = self

	def updateVelocity(self):
		for _, otherBody in Body.bodies.items():
			if otherBody != self:
				dist = np.linalg.norm(self.pos - otherBody.pos) * self.game.scale_factor
				acceleration = Body.G * otherBody.mass / dist ** 3 * (otherBody.pos - self.pos) * self.game.scale_factor
				self.velocity = self.velocity + acceleration * self.game.timeStep

	def delete(self):
		del Body.bodies[self.id]

	@staticmethod
	def restart():
		Body.bodies = {}

	def update(self):
		self.pos = self.pos + self.velocity * self.game.timeStep / self.game.scale_factor

	def render(self, display, space):
		display.blit(self.body_image, space.transform_coordinates(self.pos[0] - self.radius, self.pos[1] - self.radius))
