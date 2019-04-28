import pygame
from . import colors
import numpy as np

def ensureArray(obj):
	if not isinstance(obj, np.ndarray):
		return np.array(obj)
	return obj

def ensureList(obj):
	if type(obj) is not list and type(obj) is not tuple:
		return list(obj)
	return obj

class Drawable:
	def __init__(self, **kwargs):
		self.color = np.array(list(map(int, kwargs.get("color", colors.default_color))))
		self.defaultColor = "color" not in kwargs
		self.canvas = kwargs.get("canvas", None)
		self.onBeforeDraw = ensureList(kwargs.get("onBeforeDraw", []))

		self.bindings = kwargs.get("bindings", {})

		if "grid" in kwargs:
			self.attachTo(kwargs["grid"])
		else:
			self.parentGrid = None

	def attachTo(self, canvas):
		self.canvas = canvas
		if self.defaultColor:
			self.color = ensureArray(self.canvas.getObjectColor())
		self.canvas.objects.appendleft(self)

	def bind(self, propertyName, function):
		self.bindings[propertyName] = function

	def beforeDraw(self):
		for f in self.onBeforeDraw:
			f(self)
		for name in self.bindings:
			setattr(self, name, self.bindings[name]())

	def draw(self):
		raise NotImplemented

class Point(Drawable):
	def __init__(self, coords, **kwargs):
		self.pos = ensureArray(coords)
		super().__init__(**kwargs)

	def draw(self):
		self.canvas.putPixel(self.pos, self.color)

class Text(Drawable):
	def __init__(self, start, font, content, **kwargs):
		self.start = ensureArray(start)
		self.font = font
		self.content = content
		super().__init__(**kwargs)

		self.updateSurface()

	def updateSurface(self):
		self.surface = self.font.render(self.content, False, self.color)

	def changeText(self, content):
		self.content = content
		self.updateSurface()

	def draw(self):
		self.canvas.drawImage(self.start, self.surface)
