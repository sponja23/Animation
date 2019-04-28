import pygame
import sys
from collections import defaultdict

class PygameBackend:
	def __init__(self, size, canvas, **kwargs):
		self.interactive = True

		self.width, self.height = self.size = size
		self.screen = pygame.display.set_mode(self.size)
		self.canvas = canvas
		
		self.mouseButtons = [False for i in range(6)]
		self.keyPressed = defaultdict(lambda: False)

	def fill(self, color):
		pygame.display.flip()
		for event in pygame.event.get():
			self.handleEvents(event)
		self.screen.fill(color)

	def handleEvents(self, event):
		if event.type == pygame.MOUSEMOTION:
			self.canvas.mouseMove(event.pos, event.rel)

		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.mouseButtons[event.button] = True
			self.canvas.mouseDown(event.pos, event.button)

		elif event.type == pygame.MOUSEBUTTONUP:
			self.mouseButtons[event.button] = False
			self.canvas.mouseUp(event.pos, event.button)

		elif event.type == pygame.KEYDOWN:
			self.keyPressed[pygame.key.name(event.key)] = True

		elif event.type == pygame.KEYUP:
			self.keyPressed[pygame.key.name(event.key)] = False
			self.canvas.keyPressed(pygame.key.name(event.key))

		elif event.type == pygame.QUIT:
			sys.exit()

	def isKeyPressed(self, key):
		return self.keyPressed[key]

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

	def drawImage(self, point, image):
		self.screen.blit(image, point)
