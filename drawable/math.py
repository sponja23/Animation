import numpy as np
from .drawable import Drawable
from .shapes import Arrow
from . import colors
from .animations import Animation
from utils import ensureArray

class Curve(Drawable):
	def __init__(self, function, range, **kwargs):
		self.function = function
		self.range = range
		self.definedStep = kwargs.get("step", None)
		self.origin = kwargs.get("origin", np.array([0, 0]))
		self.cache = kwargs.get("cache", True)
		self.cached_points = None
		super().__init__(**kwargs)

	@property
	def distance(self):
		return self.range[1] - self.range[0]
	
	@property
	def step(self):
		if self.definedStep is not None:
			return self.definedStep
		return self.distance / 50

	def domain(self):
		return np.arange(self.range[0], self.range[1] + self.step, self.step)

	def points(self, **kwargs):
		return [self.function(x) for x in self.domain()]

	def draw(self):
		prev_point = None

		if self.cache and self.cached_points is None:
			self.cached_points = self.points()

		for x, y in (self.cached_points if self.cache else self.points()):
			if not self.canvas.inRange((x, y)):
				continue

			point = self.origin + np.array([x, y])
			self.canvas.putPixel(point, self.color)

			if prev_point is not None: self.canvas.drawLine(prev_point, point, self.color)
			prev_point = point

class Graph(Curve):
	def __init__(self, function, range, **kwargs):
		super().__init__(function, range, **kwargs)

	def points(self):
		return [(x, self.function(x)) for x in self.domain()]

class TimeCurve(Curve, Animation):
	def __init__(self, function, range, **kwargs):
		kwargs.pop("cache", None)
		Curve.__init__(self, function, range, **kwargs, cache = False)
		Animation.__init__(self, **kwargs)

	def points(self):
		return (self.function(x, self.time * self.speed) for x in self.domain())

class TimeGraph(TimeCurve):
	def __init__(self, function, range, **kwargs):
		super().__init__(function, range, **kwargs)

	def points(self):
		domain = self.domain()
		return zip(domain, super().points(domain=domain))

class ParametricPathCurve(Curve, Animation):
	def __init__(self, function, start=0, length=1, **kwargs):
		kwargs.pop("cache", None)
		Curve.__init__(self, function, [start, start + length], **kwargs, cache = False)
		Animation.__init__(self, **kwargs)

	def domain(self):
		return np.arange(self.range[0] + self.time * self.speed, self.range[1] + self.step + self.canvas.time * self.speed, self.step)

class ParametricTraceCurve(ParametricPathCurve):
	def __init__(self, function, start=0, **kwargs):
		step = kwargs.pop("step", 0.01)
		super().__init__(function, start, 0, **kwargs, step=step)

	def domain(self):
		return np.arange(self.range[0], self.range[1] + self.step + self.time * self.speed, self.step)


class Vector(Arrow):
	def __init__(self, coords, **kwargs):
		super().__init__(kwargs.get("start", (0, 0)), coords, **kwargs)

def point_grid(range, step):
	if hasattr(step, "__getitem__"):
		step_x, step_y = step
	else:
		step_x = step_y = step

	if hasattr(range[0], "__getitem__"):
		range_x, range_y = range
	else:
		range_x = range_y = range

	range_x = np.arange(range_x[0], range_x[1] + step_x, step_x)
	range_y = np.arange(range_y[0], range_y[1] + step_y, step_y)

	points = np.transpose(np.meshgrid(range_x, range_y))

	return points.reshape(-1, points.shape[-1])


class VectorField(Drawable):
	def __init__(self, function, points = None, **kwargs):
		self.function = function
		self.inputPoints = points if points is not None else point_grid(kwargs["range"], kwargs.get("step", 1))
		self.maxLength = kwargs.get("maxLength", 1)
		self.cache = kwargs.get("cache", True)
		self.cached_vectors = None
		self.minColor = kwargs.get("minColor", colors.green)
		self.maxColor = kwargs.get("maxColor", colors.red)
		super().__init__(**kwargs)

	def outputVectors(self, domain = None):
		return [np.array(self.function(*x)) for x in self.inputPoints]

	def draw(self):
		if self.cache and self.cached_vectors is None:
			self.cached_vectors = self.outputVectors()

		for point, vector in zip(self.inputPoints, self.cached_vectors if self.cache else self.outputVectors()):
			length = np.linalg.norm(vector)
			if length != 0:
				ratio = length / self.maxLength
				color = colors.interpolation(self.maxColor, self.minColor, min(1, 2 / ratio))
				if length > self.maxLength:
					vector /= ratio
				self.canvas.drawArrow(point, point + vector, color)
			else:
				self.canvas.drawCircle(point, .04, self.minColor)



class Grid(Drawable):
	def __init__(self, separations, **kwargs):
		self.verticalSeparation, self.horizontalSeparation = separations

		super().__init__(**kwargs)

		self.gridLinesColor = kwargs.get("gridLinesColor", self.color)

	def draw(self):
		for x in np.arange(0, self.canvas.min_x, -self.verticalSeparation):
			self.canvas.drawLine(np.array([x, self.canvas.min_y]), np.array([x, self.canvas.max_y]), self.gridLinesColor)

		for x in np.arange(0, self.canvas.max_x, self.verticalSeparation):
			self.canvas.drawLine(np.array([x, self.canvas.min_y]), np.array([x, self.canvas.max_y]), self.gridLinesColor)

		for y in np.arange(0, self.canvas.min_y, -self.horizontalSeparation):
			self.canvas.drawLine(np.array([self.canvas.min_x, y]), np.array([self.canvas.max_x, y]), self.gridLinesColor)

		for y in np.arange(0, self.canvas.max_y, self.horizontalSeparation):
			self.canvas.drawLine(np.array([self.canvas.min_x, y]), np.array([self.canvas.max_x, y]), self.gridLinesColor)

		self.canvas.drawLine(np.array([self.canvas.min_x, 0]), np.array([self.canvas.max_x, 0]), self.color, width = 2)
		self.canvas.drawLine(np.array([0, self.canvas.min_y]), np.array([0, self.canvas.max_y]), self.color, width = 2)