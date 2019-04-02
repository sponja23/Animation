import numpy as np
from drawable import Drawable, assertPoint, checkBounds, Point
from animation import Animation
import colors

class Function(Drawable):
	def __init__(self, start, f, range, **kwargs):
		self.start = assertPoint(start)
		self.function = f
		self.range = range
		self.distance = range[1] - range[0]
		self.step = kwargs.get("step", self.distance / 200)
		self.ratio = kwargs.get("ratio", 10)

		super().__init__(**kwargs)

	def domain(self):
		return np.arange(self.range[0], self.range[1] + self.step, self.step)
	
	def image(self):
		return [self.function(x) for x in self.domain()]

class CartesianGraph(Function):
	def __init__(self, start, f, range, **kwargs):
		self.drawAxis = kwargs.get("axis", False)
		self.axisColor = kwargs.get("axis_color", colors.white)

		super().__init__(start, f, range, **kwargs)
		
		self.updateBounds()

	def updateBounds(self):
		image = self.image()
		min_y = self.start.y - max(image) * self.ratio
		max_y = self.start.y - min(image) * self.ratio
		self.trueStart = Point(self.start.x, min_y)
		self.height = max_y - min_y

	def draw(self, window):
		prev_point = None
		max_y = 0
		min_y = window.height
		for x, y in zip(self.domain(), self.image()):
			x_coord = self.start.x + (x - self.range[0]) * self.ratio
			y_coord = self.start.y - y * self.ratio

			if y_coord > max_y:
				max_y = y_coord

			if y_coord < min_y:
				min_y = y_coord

			result = Point(x_coord, y_coord)
			window.putPixel(result, self.color)

			if prev_point is not None: window.drawLine(prev_point, result, self.color)
			prev_point = result

		if self.drawAxis:
			window.drawLine(self.start, self.start + (self.distance * self.ratio, 0), self.axisColor)
			center_x = self.start.x + self.distance * self.ratio / 2
			window.drawLine(Point(center_x, min_y), Point(center_x, max_y), self.axisColor)

	def move(self, dx, dy):
		self.start.move(dx, dy)
		self.trueStart.move(dx, dy)

	def collides(self, x, y):
		return checkBounds(x, y, *self.trueStart.get(), self.distance * self.ratio, self.height)

class ParametricCurve(Function):
	def __init__(self, start, f, range, **kwargs):
		super().__init__(start, f, range, **kwargs)

	def draw(self, window):
		prev_point = None
		for x, y in self.image():
			x_coord = self.start.x + x * self.ratio
			y_coord = self.start.y - y * self.ratio

			result = Point(x_coord, y_coord)
			window.putPixel(result, self.color)

			if prev_point is not None: window.drawLine(prev_point, result, self.color)
			prev_point = result

class ParametricPath(Animation):
	def __init__(self, start, f, start_val = 0, **kwargs):
		self.startPoint = assertPoint(start)
		self.currentPoint = assertPoint(start)
		self.function = f
		self.currentValue = start_val
		self.ratio = kwargs.get("ratio", 10)
		self.speed = kwargs.get("speed", 0.001)

		super().__init__(**kwargs)

	def draw(self, window):
		if not self.stop:
			self.currentValue += self.speed * window.delta_time
			x, y = self.function(self.currentValue)
			self.currentPoint = self.startPoint + (x * self.ratio, y * self.ratio)
		
		window.putPixel(self.currentPoint, self.color)

	