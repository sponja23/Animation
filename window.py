import sys
import pygame
import numpy as np
import colors
from collections import deque
from drawable import Drawable, Animation, Text, updateObjects
from functions import arrow_offset

forbiddenKeys = (
	pygame.K_RSHIFT,
	pygame.K_LSHIFT,
	pygame.K_RALT,
	pygame.K_LALT,
	pygame.K_RCTRL,
	pygame.K_LCTRL,
	pygame.K_RSUPER,
	pygame.K_LSUPER,
	pygame.K_ESCAPE,
	pygame.K_RETURN,
	pygame.K_BACKSPACE
)

specialKeys = {
	pygame.K_SPACE: " "
}

COMMAND = -1
NORMAL = 0

class Window:
	def __init__(self, width, height, **kwargs):
		self.size = self.width, self.height = width, height
		self.screen = pygame.display.set_mode(self.size)
		self.backgroundColor = kwargs.get("backgroundColor", colors.background_color)
		
		self.objects = deque([])
		
		self.mouseDown = False
		self.selectedObject = None
		
		self.modes = {
			NORMAL: {
				"event": self.handleEvent_normalMode
			},
			COMMAND: {
				"event": self.handleEvent_commandMode
			}
		}
		self.mode = NORMAL

		self.command_text = Text((10, height - 20), commandFont, "> ", color=colors.default_color)
		self.commands = {
			"quit": lambda: sys.exit()
		}

		self.keybinds = {
			pygame.K_BACKSPACE: lambda self: self.removeObject(self.selectedObject)
		}

		self.clock = pygame.time.Clock()
		self.time = 0

	def addCommand(self, name, function):
		self.commands[name] = function

	def addObject(self, obj):
		assert(isinstance(obj, Drawable))
		self.objects.appendleft(obj)

	def removeObject(self, index):
		if index is not None:
			del self.objects[index]

	def update(self):
		for event in pygame.event.get():
			self.handleEvent(event)

		self.screen.fill(self.backgroundColor)

		self.delta_time = self.clock.get_time()
		self.time += self.clock.get_time()

		updateObjects(self, self.objects)

		if self.mode == COMMAND:
			self.command_text.draw(self)

		pygame.display.flip()

		self.clock.tick(60)

	def handleEvent(self, event):
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.toggleCommandMode()
		elif event.type == pygame.QUIT:
			sys.exit()
		else:
			self.modes[self.mode]["event"](event)
		
	def handleEvent_normalMode(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			for i, obj in enumerate(self.objects):
				if hasattr(obj, "collides") and obj.collides(*event.pos):
					self.selectedObject = i
					break
			else:
				self.selectedObject = None
			self.mouseDown = True
		elif event.type == pygame.MOUSEBUTTONUP:
			self.mouseDown = False
		elif event.type == pygame.MOUSEMOTION:
			if self.selectedObject is not None and self.mouseDown:
				self.objects[self.selectedObject].move(*event.rel)
		elif event.type == pygame.KEYDOWN:
			if event.key in self.keybinds:
				self.keybinds[event.key](self)
		

	def toggleCommandMode(self):
		self.mode = NORMAL if self.mode == COMMAND else COMMAND
		self.command_text.changeText("> ")

	def handleEvent_commandMode(self, event):
		if event.type == pygame.KEYDOWN:
			key = event.key
			keys = pygame.key.get_pressed()
			if key == pygame.K_RETURN and len(self.command_text.content) > 2:
				self.executeCommand(self.command_text.content[2:])
				self.command_text.changeText("> ")
				self.toggleCommandMode()
			elif key == pygame.K_BACKSPACE and len(self.command_text.content) > 2:
				if keys[pygame.K_LCTRL]:
					self.command_text.changeText("> ")
				else:
					self.command_text.changeText(self.command_text.content[:-1])
			elif key in specialKeys:
				self.command_text.changeText(self.command_text.content + specialKeys[key])
			elif key not in forbiddenKeys:
				self.command_text.changeText(self.command_text.content + pygame.key.name(key))


	def executeCommand(self, command_text):
		cmd, *params = command_text.split(' ')
		self.commands[cmd](self, *params)
		print(command_text)


	# DRAWING

	def putPixel(self, point, color=None):
		if color is None:
			color = point.color
		self.screen.set_at(point.get(), color)

	def drawLine(self, start, end, color, **kwargs):
		pygame.draw.line(self.screen, color, start.get(), end.get(), kwargs.get("width", 1))

	def drawRectangle(self, start, width, height, color, **kwargs):
		pygame.draw.rect(self.screen, color, (*start.get(), width, height), kwargs.get("line_width", 0))

	def drawCircle(self, center, radius, color, **kwargs):
		pygame.draw.circle(self.screen, color, center.get(), radius, kwargs.get("line_width", 0))

	def drawImage(self, image, point):
		self.screen.blit(image, point.get())

	def drawArrow(self, start, end, color): # TODO
	 	self.drawLine(start, end, color)
	 	p1, p2 = arrow_offset(start, end, 40, np.pi/6)
	 	self.drawLine(end, p1, color)
	 	self.drawLine(end, p2, color)




pygame.init()
pygame.font.init()

commandFont = pygame.font.SysFont("Courier New", 20)