import pygame


class Trail(pygame.sprite.Sprite):
	def __init__(self, game, x, y, color):
		super().__init__()
		self.game = game
		self.image = pygame.Surface((1, 1)).convert()
		self.image.fill(color)
		self.transp = 255
		self.x = x
		self.y = y

	def update(self):
		self.transp -= self.game.fps / 240
		self.image.set_alpha(int(self.transp))
		if self.transp <= 1:
			pygame.sprite.Sprite.kill(self)

	def render(self, display, x, y, zoom, lock):
		if lock != -1:
			x, y = 0, 0
		display.blit(self.image, ((self.x - 2 * x - self.game.DISPLAY_W / 2) * zoom + self.game.DISPLAY_W / 2,
								  (self.y - 2 * y - self.game.DISPLAY_H / 2) * zoom + self.game.DISPLAY_H / 2))
