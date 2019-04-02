import pygame
from function import checkRectangularBounds, checkCircularBounds

def checkArray(x):
	return hasattr(x, "__getitem__")

def checkRectangularBounds(x, y, x0, y0, width, height):
	return (x >= x0 and
			x <= x0 + width and
			y >= y0 and
			y <= y0 + height)

def assertPoint(x):
	if checkArray(x):
		return Point(*x)
	return x

class Drawable:
	def __init__(self, **kwargs):
		self.color = kwargs.get("color", (255, 255, 255))

	def move(self, dx, dy):
		raise NotImplemented

	def changeColor(self, color):
		self.color = color

	def draw(self, window, time = None):
		raise NotImplemented

class Point(Drawable):
	def __init__(self, x, y, **kwargs):
		self.x = int(x)
		self.y = int(y)
		super().__init__(**kwargs)

	def get(self):
		return (self.x, self.y)

	def move(self, dx, dy):
		self.x += dx
		self.y += dy

	def draw(self, window):
		window.putPixel(self.get(), self.color)

	def collides(self, x, y):
		return self.x == x and self.y == y

	def __add__(self, other):
		if checkArray(other):
			return Point(self.x + other[0], self.y + other[1])
		else:
			return Point(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		if checkArray(other):
			return Point(self.x - other[0], self.y - other[1])
		else:
			return Point(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		return Point(self.x * other, self.y * other)

	def __div__(self, other):
		return Point(self.x / other, self.y / other)

class Line(Drawable):
	def __init__(self, start, end, **kwargs):
		self.startPoint = assertPoint(start)
		self.endPoint = assertPoint(end)

		super().__init__(**kwargs)

	@property	
	def centerPoint(self):
		return (self.startPoint + self.endPoint) / 2

	def move(self, dx, dy):
		self.startPoint.move(dx, dy)
		self.endPoint.move(dx, dy)

	def draw(self, window):
		window.drawLine(self.startPoint, self.endPoint, self.color)

	def collides(self, x, y):
		return checkRectangularBounds(x, y,
						   min(self.startPoint.x, self.endPoint.x),
						   min(self.startPoint.y, self.endPoint.y),
						   abs(self.startPoint.x - self.endPoint.x),
						   abs(self.startPoint.y - self.endPoint.y))

class Rectangle(Drawable):
	def __init__(self, start, width, height, **kwargs):
		self.startPoint = assertPoint(start)
		self.width = width
		self.height = height

		super().__init__(**kwargs)

	@property
	def centerPoint(self):
		return Point(self.startPoint.x + self.width / 2, self.startPoint.y + self.height / 2)

	def move(self, dx, dy):
		self.startPoint.move(dx, dy)

	def draw(self, window):
		window.drawRectangle(self.startPoint, self.width, self.height, self.color)

	def collides(self, x, y):
		return checkRectangularBounds(x, y, *self.startPoint.get(), self.width, self.height)

class Text(Drawable):
	def __init__(self, start, font, content, **kwargs):
		self.startPoint = assertPoint(start)
		self.font = font
		self.content = content
		super().__init__(**kwargs)

		self.updateSurface()

	def updateSurface(self):
		self.surface = self.font.render(self.content, False, self.color)

	def changeText(self, content):
		self.content = content
		self.updateSurface()

	def changeColor(self, color):
		self.color = color
		self.updateSurface()

	def move(self, dx, dy):
		self.startPoint.move(dx, dy)

	def draw(self, window):
		window.drawImage(self.surface, self.startPoint)

	def collides(self, x, y):
		return checkRectangularBounds(x, y, *self.startPoint.get(), self.surface.get_width(), self.surface.get_height())

class Circle(Drawable):
	def __init__(self, center, radius, **kwargs):
		self.centerPoint = assertPoint(center)
		self.startPoint = self.centerPoint
		self.radius = radius
		super().__init__(**kwargs)

	def move(self, dx, dy):
		self.centerPoint.move(dx, dy)

	def draw(self, window):
		window.drawCircle(self.centerPoint, self.radius)

	def collides(self, x, y):
		return functions.distance(*self.centerPoint.get(), x, y) < self.radius
