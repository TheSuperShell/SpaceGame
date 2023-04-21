from objects.celestial_body_t import CelestialBodyT
from states.space import Space


class RealSol(Space):
	def __init__(self, game):
		Space.__init__(self, game)
		self.game.scale_factor = 300000000
		self.createBodies()
		self.time_multiplier = 1
		self.game.timeStep = 720

	def createBodies(self):
		sun = CelestialBodyT(self.game, 2E30, 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2, 0., 0.,
							 (255, 255, 0), True)
		self.celestial_bodies[sun.id] = sun
		earth = CelestialBodyT(self.game, 6E24, 10, self.game.DISPLAY_W / 2 + 500, self.game.DISPLAY_H / 2, 0., -30000.,
							   (80, 80, 255), True)
		self.celestial_bodies[earth.id] = earth
		mercury = CelestialBodyT(self.game, 3E23, 5, self.game.DISPLAY_W / 2 + 193, self.game.DISPLAY_H / 2, 0.,
								 -48000., (255, 255, 200), True)
		self.celestial_bodies[mercury.id] = mercury
		venus = CelestialBodyT(self.game, 5E24, 8, self.game.DISPLAY_W / 2 + 360, self.game.DISPLAY_H / 2, 0., -35000.,
							   (230, 190, 100), True)
		self.celestial_bodies[venus.id] = venus
		mars = CelestialBodyT(self.game, 6E23, 6, self.game.DISPLAY_W / 2 + 767, self.game.DISPLAY_H / 2, 0., -24000.,
							  (255, 100, 100), True)
		self.celestial_bodies[mars.id] = mars
		jupiter = CelestialBodyT(self.game, 1.9E27, 20, self.game.DISPLAY_W / 2 + 2600, self.game.DISPLAY_H / 2, 0.,
								 -13000., (255, 190, 100), True)
		self.celestial_bodies[jupiter.id] = jupiter
		saturn = CelestialBodyT(self.game, 5.7E26, 15, self.game.DISPLAY_W / 2 + 4780, self.game.DISPLAY_H / 2, 0.,
								-9700., (230, 190, 100), True)
		self.celestial_bodies[saturn.id] = saturn

	def time_render(self, display):
		length = len(str(int(self.time / 86400)) + " days") * 20
		self.game.draw_text(display, str(int(self.time / 86400)) + " days", 40, "white",
							self.game.DISPLAY_W - 20 - length, self.game.DISPLAY_H - 30)
