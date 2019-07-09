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
		self.startTime = self.canvas.time
		self.canvas.animations[self.id] = self

	@property
	def time(self):
		if self.paused:
			return self.lastPausedTime
		return self.canvas.time - self.pausedFor - self.startTime

	def pause(self):
		if not self.paused:
			self.lastPausedTime = self.canvas.time
			self.paused = True

	def unpause(self):
		if self.paused:
			self.pausedFor += self.canvas.time - self.lastPausedTime 
			self.paused = False

	def reset(self):
		self.startTime = self.canvas.time

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

		self.distance = distance(self.start, self.end)
		self.normalized_direction = ((self.end - self.start) / self.distance)

		if "time" in kwargs:
			self.speed = (self.distance / kwargs["time"]) * .001

	def getPoint(self, time):
		return self.start + self.normalized_direction * time * self.speed

class SegmentPath(LinePath):
	def __init__(self, start, end, **kwargs):
		super().__init__(start, end, **kwargs)

	def getPoint(self, time):
		if time * self.speed >= self.distance:
			return self.end
		return super().getPoint(time)

def findPlace(l, n):
	for i, x in enumerate(l):
		if x > n:
			return i - 1

class PointPath(Path):
	def __init__(self, points, **kwargs):
		self.points = [ensureArray(p) for p in points]
		super().__init__(**kwargs)

		self.distances = [distance(p1, p2) for p1, p2 in zip(self.points, self.points[1:])]
		self.total_distance = sum(self.distances)
		self.fractions = [distance / self.total_distance for distance in self.distances]

		self.normalized_vectors = [(p2 - p1) / distance(p1, p2) for p1, p2, in zip(self.points, self.points[1:])]

		if "time" in kwargs:
			self.total_time = kwargs["time"]
		else:
			self.total_time = total_distance

		self.speed = self.total_distance / self.total_time
		self.durations = [self.total_time * fraction for fraction in self.fractions]
		self.startTimes = [sum(self.durations[:part]) for part in range(len(self.points))]


		print(self.startTimes)

	def getPoint(self, time):
		time *= .001
		if time >= self.total_time:
			return self.points[-1]
		i = findPlace(self.startTimes, time)
		return self.points[i] + self.normalized_vectors[i] * (time - self.startTimes[i]) * self.speed

class PolygonPath(PointPath):
	def __init__(self, points, **kwargs):
		super().__init__(points + [points[0]], **kwargs)

class CyclicPolygonPath(PolygonPath):
	def __init__(self, points, **kwargs):
		super().__init__(points, **kwargs)

	def getPoint(self, time):
		time = (time * .001) % self.total_time
		i = findPlace(self.startTimes, time)
		return self.points[i] + self.normalized_vectors[i] * (time - self.startTimes[i]) * self.speed
