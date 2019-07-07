import pygame
from . import colors
import numpy as np
import sys

sys.path.append("..")

from utils import ensureArray, ensureList, ensureTuple

class Drawable:
	def __init__(self, **kwargs):
		self.id = kwargs.get("id", None)
		self.color = tuple(map(int, kwargs.get("color", colors.default_color)))
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
			self.color = ensureTuple(self.canvas.getObjectColor())
		if self.id is None:
			self.id = self.canvas.getObjectId()
		self.canvas.objects[self.id] = self

	def bind(self, propertyName, function):
		self.bindings[propertyName] = function

	def beforeDraw(self):
		for f in self.onBeforeDraw:
			f(self)
		for name in self.bindings:
			setattr(self, name, self.bindings[name]())

	def draw(self):
		pass

class Point(Drawable):
	def __init__(self, coords, **kwargs):
		self.pos = ensureArray(coords)
		super().__init__(**kwargs)

	def draw(self):
		self.canvas.putPixel(self.pos, self.color)

class Text(Drawable):
	def __init__(self, start, content, font, **kwargs):
		self.start = ensureArray(start)
		self.font = font
		self.content = content
		self.size = kwargs.get("size", 1)

		super().__init__(**kwargs)
	
	def draw(self):
		self.canvas.drawText(self.start, self.content, self.font, self.color, size=self.size)