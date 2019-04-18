import numpy as np
from drawable import Drawable, assertPoint, Point, Animation, Line, updateObjects
import colors
from functions import identity

class Grid(Drawable):
	def __init__(self, center, size, separation_size, **kwargs):
		self.centerPoint = assertPoint(center)
		self.width, self.height = size
		self.vertical_separation, self.horizontal_separation = separation_size
		self.ratio = kwargs.get("ratio", 1.0)
		self.range = (
				((-self.width/2) / self.ratio, (self.width/2) / self.ratio),
				((-self.height/2) / self.ratio, (self.height/2) / self.ratio)
			)

		self.min_x, self.max_x = self.range[0]
		self.min_y, self.max_y = self.range[1]

		self.defaultColor = kwargs.get("defaultColor", colors.default_color)
		self.axisColor = kwargs.get("axisColor", self.defaultColor)
		self.gridLineColor = kwargs.get("gridLineColor", self.axisColor)

		super().__init__(**kwargs)

		del self.color

		self.objects = []
		
	def inRange(self, point):
		if isinstance(point, Point):
			x, y = point.x, point.y
		else:
			x, y = point

		return (self.min_x <= x <= self.max_x) and (self.min_y <= y <= self.max_y)

	def getPoint(self, point):
		assert(self.inRange(point))
		if isinstance(point, Point):
			x, y = point.x, point.y
		else:
			x, y = point

		x *= self.ratio
		y *= -self.ratio
		return self.centerPoint + (x, y)

	def getObjectColor(self):
		return self.defaultColor # Change

	def draw(self, window):
		for x_coord in np.arange(0, self.width / 2, self.vertical_separation):
			window.drawLine(self.centerPoint - (x_coord, self.height / 2), self.centerPoint + (-x_coord, self.height / 2), self.gridLineColor)
			window.drawLine(self.centerPoint + (x_coord, self.height / 2), self.centerPoint + (x_coord, -self.height / 2), self.gridLineColor)

		for y_coord in np.arange(0, self.height / 2, self.horizontal_separation):
			window.drawLine(self.centerPoint - (self.width / 2, y_coord), self.centerPoint + (self.width / 2, -y_coord), self.gridLineColor)
			window.drawLine(self.centerPoint + (self.width / 2, y_coord), self.centerPoint + (-self.width / 2, y_coord), self.gridLineColor)

		window.drawLine(self.centerPoint - (self.width / 2, 0), self.centerPoint + (self.width / 2, 0), self.axisColor, width = 2)
		window.drawLine(self.centerPoint - (0, self.height / 2), self.centerPoint + (0, self.height / 2), self.axisColor, width = 2)

		updateObjects(window, self.objects)

	def adaptPoint(self, point):
		assert(self.inRange(point))
		point.x, point.y = self.getPoint(point).get()

	def addObject(self, obj):
		if hasattr(obj, "attachTo"):
			obj.attachTo(self)

class GridObject(Drawable):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def adapt(self, grid):
		pass

class Curve(GridObject):
	def __init__(self, function, range, **kwargs):
		self.function = function
		self.range = range
		self.distance = range[1] - range[0]
		self.step = kwargs.get("step", self.distance / 100)
		
		super().__init__(**kwargs)

	def domain(self):
		return np.arange(self.range[0], self.range[1] + self.step, self.step)

	def points(self, window):
		return [self.function(x) for x in self.domain()]

	def draw(self, window):
		assert(self.parentGrid is not None)
		prev_point = None
		for x, y in self.points(window):
			x, y = self.transformation.apply((x, y), window)
			if not self.parentGrid.inRange((x, y)):
				continue

			point = self.parentGrid.getPoint((x, y))

			window.putPixel(point, self.color)

			if prev_point is not None: window.drawLine(prev_point, point, self.color)
			prev_point = point

class Graph(Curve):
	def __init__(self, function, range, **kwargs):
		super().__init__(function, range, **kwargs)

	def points(self, window):
		return ((x, self.function(x)) for x in self.domain())


class TimeCurve(Curve, Animation):
	def __init__(self, function, range, **kwargs):
		Curve.__init__(self, function, range, **kwargs)
		Animation.__init__(self, **kwargs)

	def points(self, window):
		return (self.function(x, window.time * self.speed) for x in self.domain())

class TimeGraph(TimeCurve):
	def __init__(self, function, range, **kwargs):
		super().__init__(function, range, **kwargs)

	def points(self, window):
		return zip(self.domain(), super().points(window))

class ParametricPath(GridObject, Animation):
	def __init__(self, function, **kwargs):
		self.function = function
		Animation.__init__(self, **kwargs)
		GridObject.__init__(self, **kwargs)

	def getPoint(self, window):
		point = self.function(window.time * self.speed)
		coords = self.parentGrid.getPoint(point)
		return coords

	def draw(self, window):
		window.putPixel(self.getPoint(window), self.color)

class Vector(Point):
	def __init__(self, x, y, **kwargs):
		super().__init__(x, y)

	def draw(self, window):
		assert(self.parentGrid is not None)
		window.drawLine(self.parentGrid.getPoint((0, 0)), Point(*self.transformation.apply(self.get())), self.color)
