from utils import ensureArray, distance
import numpy as np

class Animation:
	def __init__(self, **kwargs):
		self.canvas = None
		self.id = kwargs.get("id")

		self.speed = kwargs.get("speed", 1) * 0.001
		
		self.paused = kwargs.get("paused", False)
		self.lastPausedTime = None
		self.pausedFor = 0

	def attachTo(self, canvas):
		self.canvas = canvas
		if self.id is None:
			self.id = canvas.getAnimationId()
		self.canvas.animations[self.id] = self

	@property
	def time(self):
		if self.paused:
			return self.lastPausedTime
		return self.canvas.time - self.pausedFor

	def pause(self):
		if not self.paused:
			self.lastPausedTime = self.canvas.time
			self.paused = True

	def unpause(self):
		if self.paused:
			self.pausedFor += self.canvas.time - self.lastPausedTime 
			self.paused = False

	def togglePause(self):
		if not self.paused:
			self.pause()
		else:
			self.unpause()


class Path(Animation):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def point(self, time = None):
		if time is None:
			time = self.time
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

	def pause(self):
		super().pause()
		self.path1.pause()
		self.path2.pause()

	def unpause(self):
		super().unpause()
		self.path1.unpause()
		self.path2.unpause()

	def getPoint(self, time):
		return self.operation(self.path1.point(time), self.path2.point(time))

class ParametricPath(Path):
	def __init__(self, function, **kwargs):
		self.function = function
		self.origin = kwargs.get("origin", np.array([0, 0]))
		super().__init__(**kwargs)

	def getPoint(self, time):
		return self.origin + self.function(time * self.speed)

class CircularPath(Path):
	def __init__(self, center, radius, **kwargs):
		self.center = ensureArray(center)
		self.radius = radius
		super().__init__(**kwargs)

	def getPoint(self, time):
		return self.center + self.radius * np.array([np.cos(time * self.speed), np.sin(time * self.speed)])

class LinePath(Path):
	def __init__(self, start, end, **kwargs):
		self.start = ensureArray(start)
		self.end = ensureArray(end)
		super().__init__(**kwargs)

		if "time" in kwargs:
			self.speed = (distance(self.start, self.end) / kwargs["time"]) * .001

	def getPoint(self, time):
		return self.start + ((self.end - self.start) / distance(self.start, self.end)) * time * self.speed

class SegmentPath(LinePath):
	def __init__(self, start, end, **kwargs):
		super().__init__(start, end, **kwargs)

	def getPoint(self, time):
		if time * self.speed >= distance(self.start, self.end):
			return self.end
		return super().getPoint(time)