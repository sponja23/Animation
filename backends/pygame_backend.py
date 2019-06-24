import pygame
import sys
import numpy as np
from .base_backends import InteractiveBackend
from matplotlib import image

class PygameBackend(InteractiveBackend):
	def __init__(self, size, canvas, **kwargs):
		super().__init__(size, canvas, **kwargs)
		self.screen = pygame.display.set_mode(self.size)
		self.transformation = self.inverse_transformation = np.array([[1., 0.],
																	  [0., -1.]])

	def update(self):
		pygame.display.flip()
		for event in pygame.event.get():
			self.handleEvent(event)

	def fill(self, color):
		self.screen.fill(color)

	def handleEvent(self, event):
		if event.type == pygame.MOUSEMOTION:
			self.canvas.fire("mouseMove", event.pos, event.rel)

		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.mouseButtons[event.button] = True
			self.canvas.fire("mouseDown", event.pos, event.button)

		elif event.type == pygame.MOUSEBUTTONUP:
			self.mouseButtons[event.button] = False
			self.canvas.fire("mouseUp", event.pos, event.button)

		elif event.type == pygame.KEYDOWN:
			self.keyPressed[pygame.key.name(event.key)] = True

		elif event.type == pygame.KEYUP:
			self.keyPressed[pygame.key.name(event.key)] = False
			self.canvas.fire("keyPress", pygame.key.name(event.key))

		elif event.type == pygame.QUIT:
			sys.exit()

	def putPixel(self, point, color):
		self.screen.set_at(point, color)

	def drawLine(self, start, end, color, **kwargs):
		pygame.draw.line(self.screen, color, start, end, kwargs.get("width", 1))

	def drawRectangle(self, start, width, height, color, **kwargs):
		pygame.draw.rect(self.screen, color, (*start, width, height), kwargs.get("width", 0))

	def drawCircle(self, center, radius, color, **kwargs):
		pygame.draw.circle(self.screen, color, center, radius, kwargs.get("width", 0))

	def drawPolygon(self, points, color, **kwargs):
		pygame.draw.polygon(self.screen, color, points, kwargs.get("width", 0))

	def drawConvexPolygon(self, points, color, **kwargs):
		self.drawPolygon(points, color, **kwargs)

	def drawImage(self, point, image):
		self.screen.blit(image, point)

	def drawText(self, point, content, font, **kwargs):
		image = font.render(content, False, color)
		self.drawImage(point, image)

	def saveFrame(self, filename):
		array = pygame.surfarray.array3d(self.screen).swapaxes(0,1)
		image.imsave(f"output/image/{filename}", array)

