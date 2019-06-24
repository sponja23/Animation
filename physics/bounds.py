from ..utils import ensureArray, distance, areParalel, isConvex
from ..drawable.shapes import Polygon, Circle
import numpy as np

def rotation_matrix(theta):
	theta *= -1
	return np.array([[np.cos(theta), -np.sin(theta)],
					 [np.sin(theta),  np.cos(theta)]])

class Bound:
	def __init__(self, **kwargs):
		self.area = self.computeArea()

	def move(self, deltaPos): # Relative movement
		raise NotImplemented

	def rotate(self, theta): # Clockwise rotation 
		raise NotImplemented

	def getSprite(self, color):
		raise NotImplemented

	@property 	
	def center(self):
		raise NotImplemented

class PolygonBound(Bound):
	def __init__(self, points, **kwargs):
		self.points = [ensureArray(p) for p in points]
		assert(isConvex(self.points))
		super().__init__(**kwargs)

	def center(self):
		return np.sum(self.points, axis=0) / len(self.points)

	def computeArea(self):
		return 0.5 * abs(sum(np.cross(p0, p1) for p0, p1 in zip(self.points, self.points[1:] + [self.points[0]])))

	def getSprite(self, color):
		return ConvexPolygon(self.points, color)

	def move(self, deltaPos):
		self.points += deltaPos

	def rotate(self, theta):
		matrix = rotation_matrix(theta)
		center = self.center()
		self.points = [(matrix @ (p - center)) + center for p in self.points]

class RectangleBound(PolygonBound):
	def __init__(self, points, **kwargs):
		assert(len(points) == 4)
		x, y, z, w = points
		assert(areParalel((x, y), (w, z)))
		assert(areParalel((y, z), (x, w)))
		super().__init__(points, **kwargs)

	def computeArea(self):
		return distance(points[0], points[1]) * distance(points[1], points[2])

class CircleBound(Bound):
	def __init__(self, center, radius, **kwargs):
		self.centerPoint = center
		self.radius = radius
		self.area = self.computeArea()
		super().__init__(**kwargs)

	def center(self):
		return self.centerPoint

	def computeArea(self):
		return np.pi * self.radius ** 2

	def getSprite(self, color):
		return Circle(self.centerPoint, self.radius, color)

	def move(self, deltaPos):
		self.centerPoint += deltaPos

	def rotate(self, theta):
		pass
