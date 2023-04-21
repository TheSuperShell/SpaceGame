import os
import pygame
import time
from numpy.random import randint

from states.title import Title


# Class, that initializing the game
class Game:

	def __init__(self):
		pygame.init()
		self.running, self.playing = True, True
		self.actions = {"left": False, "right": False, "up": False, "down": False, "start": False, "back": False,
						"lmb": False, "space": False, "r": False, "t": False, "g": False, "rmb": False,
						"rmb_s": False, "lmb_s": False, "scroll_up": False, "scroll_down": False}
		self.DISPLAY_W, self.DISPLAY_H = 1280, 720
		self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
		self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
		self.dt, self.prev_time = 0, 0
		self.state_stack = []
		self.load_assets()
		self.load_states()
		self.fps = 120
		self.resolution_index = 0
		self.fullscreen = "OFF"
		self.scale_factor = 1
		self.timeStep = 1 / self.fps

		self.number_of_seconds = 1
		self.start_timer = time.time()
		self.frame = 0
		self.average_fps = 0

		pygame.display.set_caption("2d space simulator")

	# main game loop method
	def game_loop(self):
		clock = pygame.time.Clock()
		while self.playing:
			self.get_dt()
			self.fps_meter()
			self.check_events()
			self.update()
			self.render()
			clock.tick(self.fps)

	# method that checks events
	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running, self.playing = False, False
			if event.type == pygame.MOUSEWHEEL:
				if event.y > 0:
					self.actions["scroll_up"] = True
				if event.y < 0:
					self.actions["scroll_down"] = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.actions["lmb"] = True
					self.actions["lmb_s"] = True
				if event.button == 3:
					self.actions['rmb'] = True
					self.actions["rmb_s"] = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_o:
					pass
				if event.key == pygame.K_g:
					self.actions["g"] = True
				if event.key == pygame.K_t:
					self.actions["t"] = True
				if event.key == pygame.K_r:
					self.actions["r"] = True
				if event.key == pygame.K_SPACE:
					self.actions["space"] = True
				if event.key == pygame.K_ESCAPE:
					self.actions["back"] = True
				if event.key == pygame.K_w:
					self.actions["up"] = True
				if event.key == pygame.K_s:
					self.actions["down"] = True
				if event.key == pygame.K_a:
					self.actions["left"] = True
				if event.key == pygame.K_d:
					self.actions["right"] = True
				if event.key == pygame.K_RETURN:
					self.actions["start"] = True
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 3:
					self.actions['rmb_s'] = False
				if event.button == 1:
					self.actions["lmb_s"] = False

	# updates last state
	def update(self):
		self.state_stack[-1].update(self.dt, self.actions)

	# renders last state
	def render(self):
		self.state_stack[-1].render(self.display)
		self.show_fps(self.display)
		self.window.blit(self.display, (0, 0))
		pygame.display.flip()

	def get_dt(self):
		now = time.time()
		self.dt = now - self.prev_time
		self.prev_time = now

	def draw_text(self, surface, text, size, color, x, y):
		font = pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.center = (x, y)
		surface.blit(text_surface, text_rect)

	# all file paths of assets
	def load_assets(self):
		self.assets_dir = os.path.join("assets")
		self.save_dir = os.path.join("save")
		self.sprite_dir = os.path.join(self.assets_dir, "sprites")
		self.font_dir = os.path.join(self.assets_dir, "font")
		self.object_animation_dir = os.path.join(self.sprite_dir, "celestial bodies")
		# bg_dir = os.path.join(self.assets_dir, "map")
		# self.bg_image = pygame.image.load(os.path.join(bg_dir, "bg.png"))

		self.bg_image = pygame.Surface((1920 + 200, 1080 + 200))
		for _ in range(900):
			pygame.draw.circle(self.bg_image, randint(180, 256, 3), randint(0, 2120, 2),
							   randint(1, 4))

	# loading the title state

	def load_states(self):
		self.title_screen = Title(self)
		self.state_stack.append(self.title_screen)

	# resetting keys
	def reset_keys(self):
		for action in self.actions:
			if len(action) <= 2 or action[-2:] != "_s":
				self.actions[action] = False

	def fps_meter(self):
		now = time.time()
		self.frame += 1
		if now - self.start_timer >= self.number_of_seconds:
			self.start_timer = time.time()
			self.average_fps = int(self.frame / self.number_of_seconds)
			self.frame = 0

	def show_fps(self, display):
		length = len(f'{self.average_fps} fps') * 5
		self.draw_text(display, f'{self.average_fps} fps', 10, "white", length, 10)


if __name__ == "__main__":
	g = Game()
	while g.running:
		g.game_loop()
	pygame.quit()
