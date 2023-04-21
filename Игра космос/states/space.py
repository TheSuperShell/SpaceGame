import os
import pygame
import time
from numpy.random import randint

from objects.body import Body
from objects.celestial_body_t import CelestialBodyT
from objects.particles import Particles
from objects.simulated_path import SimulatedPath
from objects.simulation import Simulation
from objects.trail import Trail
from states.pause_menu import PauseMenu
from states.state import State


class Space(State):
	def __init__(self, game):
		State.__init__(self, game)
		self.create_bg()
		self.celestial_bodies = {}
		self.trails = pygame.sprite.Group()
		self.simulated_path = pygame.sprite.Group()
		self.trail = False
		self.timeFlow = True
		self.time = 0
		self.time_multiplier = 1
		self.timeReverse = False
		self.simulation = False
		self.future_time = 1
		self.frame_number = 1
		self.display_x, self.display_y = 0, 0
		self.zoom = 1

		self.screen_drag = False
		self.screen_drag_x, self.screen_drag_y = 0, 0
		self.planet_to_lock_on = -1

		self.menu = Interface(self.game)

	def update(self, dt, action):
		# self.createParticles(action)
		# for particle in Particles.particle_list:
		#     particle.update()
		self.menu.update(action)
		if not self.menu.menu_rect.collidepoint(pygame.mouse.get_pos()):
			self.update_screen(action)
			self.create_random_body(action)
		self.update_planet_lock()
		self.update_zoom(action)
		self.time_freeze(action)
		self.time_reverse(action)
		self.time_speed_up(action)
		self.time_speed_down(action)
		self.trail_switch(action)
		# self.simulation_switch(action)
		self.out_of_boundaries()
		for _, body in self.celestial_bodies.items():
			if self.collision(body):
				break
		self.update_pos()
		self.update_trails()
		# if self.simulation:
		#     self.simulate_path()
		# elif len(self.simulated_path) != 0:
		#     Simulation.refresh()
		#     pygame.sprite.Group.empty(self.simulated_path)
		if action["back"]:
			new_state = PauseMenu(self.game)
			new_state.enter_state()
		self.game.reset_keys()
		self.frame_number += 1
		if self.frame_number == 20:
			self.frame_number = 0

	def render(self, display):
		display.blit(self.bg_image, (int(- 100 - self.display_x / 100), int(- 100 - self.display_y / 100)))
		display.blit(self.bg_image_layer_2, (int(- 100 - self.display_x / 50), int(- 100 - self.display_y / 50)))
		self.trails_render(display)
		for _, body in self.celestial_bodies.items():
			body.render(display, self.display_x, self.display_y, self.zoom, self)
		# self.particle_render(display)
		# if self.simulation:
		#     self.draw_simulated_path(display)
		#     self.game.draw_text(display, "Simulating", 30, "white", self.game.DISPLAY_W - 170, self.game.DISPLAY_H - 230)
		length2 = len("x" + str(float(self.time_multiplier))) * 20
		if not self.timeFlow:
			self.game.draw_text(display, "Pause", 40, "white", self.game.DISPLAY_W - 120, self.game.DISPLAY_H - 180)
		if self.timeReverse:
			self.game.draw_text(display, "Reverse", 40, "white", self.game.DISPLAY_W - 160, self.game.DISPLAY_H - 130)
		self.game.draw_text(display, "x" + str(float(self.time_multiplier)), 40, "white",
							self.game.DISPLAY_W - 20 - length2, self.game.DISPLAY_H - 80)
		self.time_render(display)
		self.menu.render(display)

	def particle_render(self, display):
		for particle in Particles.particle_list:
			x, y = self.transform_coordinates(particle.x, particle.y)
			display.blit(particle.image, (x, y))

	def time_render(self, display):
		length = len(str(int(self.time)) + " s") * 20
		self.game.draw_text(display, str(int(self.time)) + " s", 40, "white", self.game.DISPLAY_W - 20 - length,
							self.game.DISPLAY_H - 30)

	def create_bg(self):
		self.bg_image = pygame.Surface((1920 + 200, 1080 + 200))
		for _ in range(450):
			pygame.draw.circle(self.bg_image,
							   randint(180, 256, 3),
							   (randint(0, max(1920 + 200, 1080 + 200), 2)),
							   randint(1, 4))
		self.bg_image_layer_2 = pygame.Surface((1920 + 200, 1080 + 200))
		for _ in range(450):
			pygame.draw.circle(self.bg_image_layer_2, randint(180, 256, 3),
							   (randint(0, max(1920 + 200, 1080 + 200), 2)), randint(1, 4))
		self.bg_image_layer_2.set_colorkey("black")

		self.grid = pygame.Surface((1920, 1080))
		for i in range(20):
			pygame.draw.line(self.grid, "white", (int(1920 / 20 * i), 1080), (int(1920 / 20 * i), 0))
		for i in range(11):
			pygame.draw.line(self.grid, "white", (1920, int(1080 / 11 * i)), (0, int(1080 / 11 * i)))
		self.grid.set_colorkey("black")
		self.grid.set_alpha(150)

	def create_particles(self, action):
		if action["rmb_s"]:
			for _ in range(30):
				a = Particles(self.game, (pygame.mouse.get_pos()[0] + 2 * self.display_x + (self.zoom - 1) * (
						self.game.DISPLAY_W / 2 + 2 * self.display_x)) / self.zoom,
							  (pygame.mouse.get_pos()[1] + 2 * self.display_y + (self.zoom - 1) * (
									  self.game.DISPLAY_H / 2 + 2 * self.display_y)) / self.zoom)
				Particles.particle_list.append(a)

	def create_random_body(self, action):
		if self.menu.selected == 2 and action["lmb_s"] and self.frame_number % 5 == 0:
			self.game.reset_keys()
			b = CelestialBodyT(self.game, randint(1, 10000) * 10 ** 10, randint(1, 20),
							   (pygame.mouse.get_pos()[0] + 2 * self.display_x + (self.zoom - 1) * (
									   self.game.DISPLAY_W / 2 + 2 * self.display_x)) / self.zoom,
							   (pygame.mouse.get_pos()[1] + 2 * self.display_y + (self.zoom - 1) * (
									   self.game.DISPLAY_H / 2 + 2 * self.display_y)) / self.zoom,
							   float(randint(-100, 101)), float(randint(-100, 101)),
							   [randint(0, 256) for _ in range(3)])
			self.celestial_bodies[b.id] = b

	def create_trail(self, x, y, color):
		if self.trail:
			x1, y1 = 0, 0
			if self.planet_to_lock_on != -1 and self.planet_to_lock_on in CelestialBodyT.bodies:
				x1 = 2 * self.display_x
				y1 = 2 * self.display_y
			new_trail = Trail(self.game, x - x1, y - y1, color)
			self.trails.add(new_trail)

	def update_screen(self, action):
		if self.menu.selected == 0:
			if action["lmb_s"] and not self.screen_drag:
				if self.planet_to_lock_on != -1:
					self.planet_to_lock_on = -1
					pygame.sprite.Group.empty(self.trails)
				self.screen_drag_x, self.screen_drag_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
				self.screen_drag = True
			elif self.screen_drag and action["lmb_s"]:
				self.display_x, self.display_y = self.display_x + (
						- pygame.mouse.get_pos()[0] + self.screen_drag_x) / self.zoom, self.display_y + (
														 - pygame.mouse.get_pos()[
															 1] + self.screen_drag_y) / self.zoom
				if self.display_x < -10000 / 2:
					self.display_x = -10000 / 2
				if self.display_y < -7000 / 2:
					self.display_y = -7000 / 2
				if self.display_x > (10000 - self.game.DISPLAY_W) / 2:
					self.display_x = (10000 - self.game.DISPLAY_W) / 2
				if self.display_y > (7000 - self.game.DISPLAY_H) / 2:
					self.display_y = (7000 - self.game.DISPLAY_H) / 2
				self.screen_drag = False
			elif self.screen_drag:
				self.screen_drag = False

		if action['lmb']:
			for key, body in CelestialBodyT.bodies.items():
				a = - body.radius < pygame.mouse.get_pos()[0] - self.transform_coordinates(body.pos[0], body.pos[1])[
					0] < body.radius
				b = - body.radius < pygame.mouse.get_pos()[1] - self.transform_coordinates(body.pos[0], body.pos[1])[
					1] < body.radius
				if a and b and self.menu.selected == 1:
					self.planet_to_lock_on = key
					pygame.sprite.Group.empty(self.trails)
					break
				if a and b and self.menu.selected == 3:
					del self.celestial_bodies[key]
					del CelestialBodyT.bodies[key]
					break

	def transform_coordinates(self, x, y):
		return ((x - 2 * self.display_x - self.game.DISPLAY_W / 2) * self.zoom + self.game.DISPLAY_W / 2,
				(y - 2 * self.display_y - self.game.DISPLAY_H / 2) * self.zoom + self.game.DISPLAY_H / 2)

	def update_planet_lock(self):
		if self.planet_to_lock_on != -1 and self.planet_to_lock_on in CelestialBodyT.bodies:
			x = CelestialBodyT.bodies[self.planet_to_lock_on].pos[0]
			y = CelestialBodyT.bodies[self.planet_to_lock_on].pos[1]
			self.display_x = (x - self.game.DISPLAY_W / 2) / 2
			self.display_y = (y - self.game.DISPLAY_H / 2) / 2
		elif self.planet_to_lock_on != -1:
			self.planet_to_lock_on = -1

	def update_zoom(self, action):
		if action["scroll_up"]:
			self.zoom += 0.1
			if self.zoom > 4:
				self.zoom = 4
		if action["scroll_down"]:
			self.zoom -= 0.1
			if self.zoom < 0.1:
				self.zoom = 0.1

	def update_trails(self):
		for trail in self.trails:
			trail.update()

	def update_pos(self):
		if self.timeFlow:
			# if self.frame_number % 19 == 0:
			#     Simulation.refresh()
			#     pygame.sprite.Group.empty(self.simulated_path)
			for _, body in self.celestial_bodies.items():
				if self.frame_number % 2 == 0:
					self.create_trail(body.pos[0], body.pos[1], body.color)
				body.updateVelocity()
			for _, body in self.celestial_bodies.items():
				body.update()
			self.time += self.game.timeStep

	def trails_render(self, display):
		for trail in self.trails:
			trail.render(display, self.display_x, self.display_y, self.zoom, self.planet_to_lock_on)

	def out_of_boundaries(self):
		for key, body in self.celestial_bodies.items():
			if not -10000 - body.radius < body.pos[
				0] < self.game.DISPLAY_W + 10000 + body.radius or not -7000 - body.radius < body.pos[
				1] < self.game.DISPLAY_H + 7000 + body.radius:
				body.delete()
				del self.celestial_bodies[key]
				print("body deleted")
				break

	def trail_switch(self, action):
		if action["t"]:
			self.trail = not self.trail
			self.game.reset_keys()

	def simulation_switch(self, action):
		if action["g"]:
			self.simulation = not self.simulation
			self.game.reset_keys()

	def time_reverse(self, action):
		if action["r"]:
			self.game.timeStep *= -1
			self.game.reset_keys()
			self.timeReverse = not self.timeReverse

	def time_freeze(self, action):
		if action["space"]:
			self.timeFlow = not self.timeFlow
			self.game.reset_keys()

	def time_speed_up(self, action):
		if action["up"]:
			self.game.timeStep *= 2
			self.time_multiplier *= 2
			self.game.reset_keys()

	def time_speed_down(self, action):
		if action["down"]:
			self.game.timeStep /= 2
			self.time_multiplier /= 2
			self.game.reset_keys()

	def collision(self, other_body):
		for key, body in self.celestial_bodies.items():
			if body.collision_check(other_body):
				if body.mass >= other_body.mass:
					temp_mass = body.mass
					Body.bodies[key].mass += other_body.mass
					new_volume = Body.bodies[key].radius ** 3 * Body.bodies[key].mass / temp_mass
					Body.bodies[key].radius = new_volume ** (1 / 3)
					Body.bodies[key].velocity = (
														temp_mass * body.velocity + other_body.mass * other_body.velocity) / body.mass
					body.color = [i for i in map(lambda x, y: int((x + y) / 2), body.color, other_body.color)]
					body.png = False
					other_body.delete()
					del self.celestial_bodies[other_body.id]
					return True
		return False

	def simulate_path(self):
		if len(self.simulated_path) == 0:
			self.simulate(10)

	def draw_simulated_path(self, display):
		if self.simulation:
			for sim in self.simulated_path:
				sim.draw(display, self.display_x, self.display_y, self.zoom)
			for key, body in Simulation.simulated_bodies.items():
				temp = pygame.Surface((body.radius * 2 * self.zoom, body.radius * 2 * self.zoom))
				color = "white"
				if body.color == "boom":
					color = "red"
				pygame.draw.circle(temp, color, (body.radius * self.zoom, body.radius * self.zoom),
								   body.radius * self.zoom)
				temp.set_colorkey("black")
				temp.set_alpha(50)
				dis_x, dis_y = self.display_x, self.display_y
				x1, y1 = 0, 0
				if self.planet_to_lock_on != -1:
					dis_x, dis_y = 0, 0
					x1 = Simulation.simulated_bodies[self.planet_to_lock_on].pos[0]
					y1 = Simulation.simulated_bodies[self.planet_to_lock_on].pos[1]
					x1 = (x1 - self.game.DISPLAY_W / 2)
					y1 = (y1 - self.game.DISPLAY_H / 2)
				display.blit(temp, ((body.pos[0] - body.radius - x1) * self.zoom - 2 * dis_x - (self.zoom - 1) * (
						self.game.DISPLAY_W / 2 + 2 * dis_x),
									(body.pos[1] - body.radius - y1) * self.zoom - 2 * dis_y - (self.zoom - 1) * (
											self.game.DISPLAY_H / 2 + 2 * dis_y)))

	def simulate(self, time_limit):
		start = time.time()
		timer = 0
		counter = 0
		collision = False
		for key, body in self.celestial_bodies.items():
			a = Simulation(self.game, body.mass, body.radius, body.pos[0], body.pos[1], body.velocity[0],
						   body.velocity[1], body.color)
			a.id = key
			Simulation.simulated_bodies[a.id] = a
		while not collision and timer < time_limit:
			for key, body in Simulation.simulated_bodies.items():
				body.updateVelocity()
			if counter == 1:
				for key, body in Simulation.simulated_bodies.items():
					x, y = 0, 0
					if self.planet_to_lock_on != -1 and self.planet_to_lock_on in CelestialBodyT.bodies:
						x = Simulation.simulated_bodies[self.planet_to_lock_on].pos[0]
						y = Simulation.simulated_bodies[self.planet_to_lock_on].pos[1]
						x = (x - self.game.DISPLAY_W / 2)
						y = (y - self.game.DISPLAY_H / 2)
					path = SimulatedPath(self.game, body.color, body.pos[0] - x, body.pos[1] - y)
					self.simulated_path.add(path)
					counter = 0
			for _, body in Simulation.simulated_bodies.items():
				body.update()
				for _, otherBody in Simulation.simulated_bodies.items():
					if body.collision_check(otherBody):
						collision = True
						body.color = "boom"
						otherBody.color = "boom"
						break
				if collision:
					break
			timer += Simulation.dTime
			counter += 1
		self.future_time = self.time + timer
		finish = time.time()
		print(finish - start)

	def restart(self):
		self.celestial_bodies = {}
		pygame.sprite.Group.empty(self.trails)
		pygame.sprite.Group.empty(self.simulated_path)
		CelestialBodyT.restart()


class Interface:

	def __init__(self, game):
		self.game = game
		path = os.path.join(self.game.assets_dir, "menu")
		self.image = pygame.image.load(os.path.join(path, "main gui.png")).convert()
		self.image = pygame.transform.scale(self.image, (550, 150))
		self.menu_rect = self.image.get_rect()
		self.menu_rect.y = self.game.DISPLAY_H - 150
		self.on = True
		temp = pygame.Surface((60, 20))
		self.close_button = temp.get_rect()
		self.close_button.x = 485
		self.close_button.y = 10 + self.menu_rect.y
		self.go_to_menu = self.menu_rect.y

		self.options = []
		for i in range(5):
			option = pygame.Surface((80, 80))
			rect = option.get_rect()
			rect.y = 40 + self.menu_rect.y
			rect.x = 30 + i * 100
			self.options.append(rect)

		self.cursor = pygame.image.load(os.path.join(path, "selector.png")).convert()
		self.cursor = pygame.transform.scale(self.cursor, (88, 88))
		self.cursor.set_colorkey("black")
		self.ghost_cursor = self.cursor.copy()
		self.ghost_cursor.set_alpha(150)
		self.selected = 0
		self.cursor_y = 36
		self.cursor_x = 26
		self.ghost_cursor_x = 26

	def animation(self):
		if self.menu_rect.y < self.go_to_menu:
			self.menu_rect.y += 6
			self.close_button.y += 6
		if self.menu_rect.y > self.go_to_menu:
			self.menu_rect.y -= 6
			self.close_button.y -= 6

	def close(self, action):
		if self.close_button.collidepoint(pygame.mouse.get_pos()) and action["lmb"]:
			if self.on:
				self.on = False
				self.go_to_menu += 118
			elif not self.on:
				self.on = True
				self.go_to_menu -= 118

	def update(self, action):
		self.ghost_cursor_x = self.cursor_x
		self.close(action)
		if self.on:
			self.update_cursor(action)
		self.animation()

	def render(self, display):
		image = self.image.copy()
		image.blit(self.ghost_cursor, (self.ghost_cursor_x, self.cursor_y))
		image.blit(self.cursor, (self.cursor_x, self.cursor_y))
		if not self.on:
			image.set_alpha(150)
		else:
			image.set_alpha(200)
		display.blit(image, (0, self.menu_rect.y))

	def update_cursor(self, action):
		for i in range(5):
			if self.options[i].collidepoint(pygame.mouse.get_pos()):
				self.ghost_cursor_x = 26 + i * 100
				if action["lmb"]:
					self.cursor_x = 26 + i * 100
					self.selected = i
