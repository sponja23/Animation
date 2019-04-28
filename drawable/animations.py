from .drawable import ensureArray
import numpy as np

class Animation:
	def __init__(self, **kwargs):
		self.speed = kwargs.get("speed", 1) * 0.001

class Path(Animation):
	def __init__(self, **kwargs):
		self.canvas = kwargs.get("canvas", None)
		super().__init__(**kwargs)

	def point(self, time = None):
		if time is None:
			time = self.canvas.time

		return ensureArray(self.getPoint(time))

	def __add__(self, other):
		return CompoundPath(self, other, lambda x, y: x + y, canvas=self.canvas or other.canvas)

	def __sub__(self, other):
		return CompoundPath(self, other, lambda x, y: x - y, canvas=self.canvas or other.canvas)

	def getPoint(self, time):
		raise NotImplemented

class CompoundPath(Path):
	def __init__(self, path1, path2, operation, **kwargs):
		self.path1 = path1
		self.path2 = path2
		self.operation = operation
		super().__init__(**kwargs)

	def getPoint(self, time):
		return self.operation(self.path1.point(time), self.path2.point(time))

class ParametricPath(Path):
	def __init__(self, function, **kwargs):
		self.function = function
		self.origin = kwargs.get("origin", np.array([0, 0]))
		super().__init__(**kwargs)

	def getPoint(self, time):
		return self.origin + self.function(time * self.speed)

class PointPath(Path):
	def __init__(self, points, **kwargs):
		self.points = [ensureArray(p) for p in points]

	def getPoint(self, time):
		pass		