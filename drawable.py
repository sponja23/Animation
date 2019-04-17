import pygame
import colors
from functions import identity

def checkArray(x):
	return hasattr(x, "__getitem__")

def checkBounds(x, y, x0, y0, width, height):
	return (x >= x0 and
			x <= x0 + width and
			y >= y0 and
			y <= y0 + height)

def assertPoint(x):
	if checkArray(x): return Point(*x)
	return x

class Drawable:
	def __init__(self, **kwargs):
		self.color = kwargs.get("color", colors.default_color)
		self.defaultColor = "color" not in kwargs
		self.transformation = kwargs.get("transformation", identity)

		if "grid" in kwargs:
			self.attachTo(kwargs["grid"])
		else:
			self.parentGrid = None


	def move(self, dx, dy):
		raise NotImplemented

	def attachTo(self, grid):
		self.parentGrid = grid
		if self.defaultColor:
			self.color = self.parentGrid.getObjectColor()
		self.adapt(grid)
		grid.objects.append(self)

	def adapt(self, grid):
		raise NotImplemented

	def changeColor(self, color):
		self.color = color

	def draw(self, window, time = None):
		raise NotImplemented

class Animation(Drawable):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.speed = kwargs.get("speed", 1) * 0.001

def updateObjects(window, components):
	for obj in reversed(components):
		obj.draw(window)

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
		window.putPixel(self.transformation.apply(self.get(), window))

	def collides(self, x, y):
		return self.x == x and self.y == y

	def __ensure_int(self):
		self.x = int(self.x)
		self.y = int(self.y)

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

	def __iadd__(self, other):
		if checkArray(other):
			dx, dy = other
		else: 
			dx, dy = other.x, other.y

		self.x += dx
		self.y += dy
		self.__ensure_int()

	def __isub__(self, other):
		if checkArray(other):
			dx, dy = other
		else:
			dx, dy = other.x, other.y

		self.x -= dx
		self.y -= dy
		self.__ensure_int()

	def __imul__(self, other):
		self.x *= other
		self.y *= other
		self.__ensure_int()

	def __idiv__(self, other):
		self.x /= other
		self.y /= other
		self.__ensure_int()

	def __repr__(self):
		return f"Point({self.x}, {self.y})"

	def adapt(self, grid):
		self.x, self.y = grid.getPoint().get()

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
		window.drawLine(self.transformation.apply(self.startPoint, window), self.transformation.apply(self.endPoint, window), self.color)

	def collides(self, x, y):
		return checkBounds(x, y,
						   min(self.startPoint.x, self.endPoint.x),
						   min(self.startPoint.y, self.endPoint.y),
						   abs(self.startPoint.x - self.endPoint.x),
						   abs(self.startPoint.y - self.endPoint.y))

	def adapt(self, grid):
		grid.adaptPoint(self.startPoint)
		grid.adaptPoint(self.endPoint)

class Arrow(Line):
	def __init__(self, start, end, **kwargs):
		super().__init__(start, end, **kwargs)

	def draw(self, window):
		window.drawArrow(self.transformation.apply(self.startPoint), self.transformation.apply(self.endPoint), self.color)

class Rectangle(Drawable):
	def __init__(self, start, width, height, **kwargs):
		self.startPoint = assertPoint(start)
		self.width = width
		self.height = height

		super().__init__(**kwargs)

		del self.transformation

	@property
	def centerPoint(self):
		return Point(self.startPoint.x + self.width / 2, self.startPoint.y + self.height / 2)

	def move(self, dx, dy):
		self.startPoint.move(dx, dy)

	def draw(self, window):
		window.drawRectangle(self.startPoint, self.width, self.height, self.color)

	def collides(self, x, y):
		return checkBounds(x, y, *self.startPoint.get(), self.width, self.height)

	def adapt(self, grid):
		grid.adaptPoint(self.startPoint)
		self.width *= grid.ratio
		self.height *= grid.ratio


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
		return checkBounds(x, y, *self.startPoint.get(), self.surface.get_width(), self.surface.get_height())

class Circle(Drawable):
	def __init__(self, center, radius, **kwargs):
		self.centerPoint = assertPoint(center)
		self.radius = radius
		super().__init__(**kwargs)

	def move(self, dx, dy):
		self.centerPoint.move(dx, dy)

	def draw(self, window):
		window.drawCircle(self.centerPoint, self.radius)

	def collides(self, x, y):
		return functions.distance(*self.centerPoint.get(), x, y) < self.radius

class Polygon(Drawable):
	def __init__(self, *points, **kwargs):
		self.points = [assertPoint(p) for p in points]
		super().__init__(**kwargs)

	def draw(self, window):
		for p1, p2 in zip(self.points, self.points[1:]):
			window.drawLine(self.transformation.apply(p1, window), self.transformation.apply(p2, window), self.color)
		window.drawLine(self.transformation.apply(self.points[-1], window), self.transformation.apply(self.points[0], window), self.color)

	def adapt(self, grid):
		for p in self.points:
			grid.adaptPoint(p)