import os

import numpy as np
import pygame
from numpy.random import randint

from objects.animation import Animate
from objects.body import Body


class CelestialBodyT(Body):

	def __init__(self, game, mass, radius, x, y, vx, vy, color, real=False):
		Body.__init__(self, game, mass, x, y, vx, vy)
		self.radius = radius
		self.color = color
		self.type = "planet"
		self.light_sources = {}
		self.has_tail = False
		self.tail_list = []
		if real:
			self.planet_mass = 1E28
			self.red_star_mass = 1E30
			self.black_hole_mass = 1E40
			self.luminosity_factor = 20
		else:
			self.planet_mass = 1E14
			self.red_star_mass = 1E15
			self.black_hole_mass = 1E20
			self.luminosity_factor = 1

	def update(self):
		self.light_sources = {}
		self.type_update()
		Body.update(self)
		if self.type == "planet":
			self.light_source_update()
		self.create_tail()
		self.update_tail()

	def render(self, display, x, y, zoom, space):
		if self.type == "star":
			if self.subclass == "yellow star":
				self.draw_lighting(display, int(self.radius * zoom), space, mul=6)
				self.draw_lighting(display, int(self.radius * zoom), space, mul=3)
				self.draw_lighting(display, int(self.radius * zoom), space, mul=2)
			elif self.subclass == "red star":
				self.draw_lighting(display, int(self.radius * zoom), space, 4, (5, 0, 0))
				self.draw_lighting(display, int(self.radius * zoom), space, 2, (5, 0, 0))
		self.draw_tail(display)
		display.blit(self.render_type(zoom),
					 space.transform_coordinates(self.pos[0] - self.radius, self.pos[1] - self.radius))

	def collision_check(self, otherBody):
		return otherBody != self and np.linalg.norm(self.pos - otherBody.pos) <= self.radius + otherBody.radius

	def type_update(self):
		G = 6.67E-11
		c = 3E8
		if self.black_hole_mass > self.mass >= self.planet_mass:
			self.has_tail = False
			if (self.type != "star" or self.subclass != "red star") and self.mass < 1E15:
				self.type = "star"
				self.subclass = "red star"
				self.color = (255, 0, 0)
				path = os.path.join(self.game.sprite_dir, "celestial bodies")
				self.image = pygame.image.load(os.path.join(path, "red star.png")).convert()
				self.image.set_colorkey("black")
				self.luminosity = 10000 * self.luminosity_factor
			elif (self.type != "star" or self.subclass != "yellow star") and self.mass >= 1E15:
				self.type = "star"
				self.subclass = "yellow star"
				self.color = (255, 255, 0)
				path = os.path.join(self.game.sprite_dir, "celestial bodies")
				self.image = pygame.image.load(os.path.join(path, "sun.png")).convert()
				self.animation = Animate(self.game, [self.game.fps for _ in range(4)], "yellow star")
				self.image.set_colorkey("black")
				self.luminosity = 1000000 * self.luminosity_factor
			self.mass -= self.mass * (1E-7 / self.game.fps)
		if self.mass < self.planet_mass:
			self.type = "planet"
		if self.mass >= self.black_hole_mass:
			self.type = "black hole"
			self.radius = 2 + 2 * G * self.mass / c ** 2

	# TODO: add more types

	def draw_lighting(self, display, radius, space, mul=2, color=(5, 5, 0)):
		aura = pygame.Surface((radius * 2 * mul, radius * 2 * mul))
		pygame.draw.circle(aura, color, (radius * mul, radius * mul), radius * mul)
		aura.set_colorkey("black")
		display.blit(aura,
					 space.transform_coordinates(self.pos[0] - self.radius * mul, self.pos[1] - self.radius * mul),
					 special_flags=pygame.BLEND_RGB_ADD)

	def light_source_update(self):
		for key, body in CelestialBodyT.bodies.items():
			if body.type == "star":
				r = self.pos - body.pos
				d = np.linalg.norm(r)
				r /= d
				rp = np.matmul(np.array(((0, -1), (1, 0))), r)
				self.light_sources[key] = (r, d, rp)

	def create_tail(self):
		if self.type == "planet" and self.has_tail:
			for key, star in self.light_sources.items():
				if star[1] < 300:
					if CelestialBodyT.bodies[key].subclass == "yellow star":
						l = 1
					else:
						l = 0.5
					tail = Tail(self.game, self.pos[0], self.pos[1], star[0], star[1], l)
					self.tail_list.append(tail)

	def update_tail(self):
		for tail in self.tail_list:
			tail.update()
			if tail.current_time <= 0:
				self.tail_list.pop(0)

	# TODO: make normal list delete functionality

	def draw_tail(self, display):
		for tail in self.tail_list:
			tail.render(display)

	def render_type(self, zoom):
		radius = int(self.radius * zoom)
		if self.type == "planet":
			image = pygame.Surface((radius * 2, radius * 2))
			if len(self.light_sources) != 0:
				image.fill("white")
				color1 = tuple(map(lambda x: int(x / 20), self.color))
				pygame.draw.circle(image, color1, (radius, radius), radius)
				image.set_colorkey("white")
				for key, body in self.light_sources.items():
					light_part = pygame.Surface((radius * 2, radius * 2))
					a = CelestialBodyT.bodies[key].luminosity
					color = list(map(lambda x: x * .95 * (
							a / (body[1] - CelestialBodyT.bodies[key].radius - self.radius + np.sqrt(a)) ** 2),
									 self.color))
					for i in range(3):
						if color[i] > 255:
							color[i] = 255
					r1 = body[0]
					r2 = body[2]
					x1, x2 = r2 * radius, -r2 * radius
					x3, x4 = tuple(x2 - r1 * radius + np.array((radius, radius))), tuple(
						x1 - r1 * radius + np.array((radius, radius)))
					x1, x2 = tuple(x1 + np.array((radius, radius))), tuple(x2 + np.array((radius, radius)))
					pygame.draw.polygon(light_part, color, (x1, x2, x3, x4))
					light_part.set_colorkey("black")
					image.blit(light_part, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
			else:
				pygame.draw.circle(image, self.color, (radius, radius), radius)
				image.set_colorkey("black")
			return image
		elif self.type == "star":
			image = self.image
			if self.subclass == "yellow star":
				image = self.animation.current_frame()
			image = pygame.transform.scale(image, (radius * 2, radius * 2))
			return image
		elif self.type == "black hole":
			image = pygame.Surface((radius * 2, radius * 2))
			image.fill("white")
			pygame.draw.circle(image, "orange", (radius, radius), radius)
			pygame.draw.circle(image, "black", (radius, radius), radius - 1)
			image.set_colorkey("white")
			return image


class Tail:

	def __init__(self, game, x, y, r, d, l):
		self.game = game
		self.x, self.y = x, y
		self.scatter = 10
		a = 50000 * l
		self.length = a / (d + a ** 0.5) ** 2
		self.vx, self.vy = r[0] + randint(-100, 100) / (100 * self.scatter), r[1] + randint(-100, 100) / (
				100 * self.scatter)
		self.radius = randint(1, 4)
		self.life_time = self.game.fps * self.length
		self.current_time = self.life_time
		self.image = pygame.Surface

	# TODO: make normal zooming

	def update(self):
		self.x += self.vx
		self.y += self.vy
		self.current_time -= 1

	def render(self, display):
		radius = self.radius * self.game.state_stack[3].zoom
		image = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(image, "white", (radius, radius), radius)
		image.set_colorkey("black")
		image.set_alpha(int(255 / self.life_time * self.current_time))
		display.blit(image, self.game.state_stack[3].transform_coordinates(self.x - self.radius, self.y - self.radius))
