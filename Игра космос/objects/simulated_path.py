import pygame


class SimulatedPath(pygame.sprite.Sprite):
	def __init__(self, game, color, x, y):
		super().__init__()
		self.game = game
		self.image = pygame.Surface((8, 8))
		pygame.draw.circle(self.image, color, (3, 3), 3)
		self.image.set_colorkey("black")
		self.image.set_alpha(30)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def draw(self, display, x, y, zoom):
		if self.game.state_stack[3].planet_to_lock_on != -1:
			x, y = 0, 0
		display.blit(self.image, (self.rect.x * zoom - 2 * x - (zoom - 1) * (self.game.DISPLAY_W / 2 + 2 * x),
								  self.rect.y * zoom - 2 * y - (zoom - 1) * (self.game.DISPLAY_H / 2 + 2 * y)))
