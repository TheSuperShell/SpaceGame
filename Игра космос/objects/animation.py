import pygame
import os


class Animate():
	def __init__(self, game, timings, sprite_name):
		self.game = game
		self.timings = timings
		self.sprite_name = sprite_name
		self.animation_dir = os.path.join(self.game.object_animation_dir, self.sprite_name)

		self.frame_number = 0

		self.animation_frames = []
		for i in range(1, len(self.timings) + 1):
			file_name = self.sprite_name + str(i)
			frame = pygame.image.load(os.path.join(self.animation_dir, file_name + ".png")).convert()
			frame.set_colorkey("black")
			for _ in range(self.timings[i - 1]):
				self.animation_frames.append(frame.copy())
		self.amount_of_frames = len(self.animation_frames)

	def current_frame(self):
		if self.frame_number == self.amount_of_frames:
			self.frame_number = 0
		image = self.animation_frames[self.frame_number]
		self.frame_number += 1
		return image
