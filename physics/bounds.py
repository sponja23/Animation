from ..utils import ensureArray
from ..drawable.shapes import Polygon
import numpy as np

class Bound:
	def __init__(self, **kwargs):
		pass

	def move(self, deltaPos):
		raise NotImplemented

	def rotate(self, theta):
		raise NotImplemented

	def getSprite(self, color):
		raise NotImplemented

	@property 	
	def center(self):
		raise NotImplemented

class PolygonBound(Bound): # Only supports convex polygon
	def __init__(self, points, **kwargs):
		self.points = [ensureArray(p) for p in points]
		self.area = self.computeArea()
		super().__init__(**kwargs)

	def computeArea(self):
		x = points[:, 0]
		y = points[:, 1]
		n = len(x)
		i0, i1 = np.arange(-n + 1, 1), np.arange(-1, n - 1)
		return abs((x * (y.take(i1) - y.take(i0))).sum()) / 2.0

	@property
	def center(self):
		return np.sum(self.points, axis=0) / len(self.points)

	def getSprite(self, color):
		

	def move(self, deltaPos):
		self.points += deltaPos

class CircleBound(Bound):
	def __init__(self, center, radius, **kwargs):
		self.center = center
		self.radius = radius
		self.area = self.computeArea()
		super().__init__(**kwargs)

	def computeArea(self):
		return np.pi * self.radius ** 2

	def move(self, deltaPos):
		self.center += deltaPos

	def rotate(self, theta):
