import numpy as np
from numpy import pi

def distance(x0, y0, x1, y1):
	return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** .5

# def arrow_offset(start, end, length, angle):
# 	alpha = np.arctan((start.y - end.y) / (start.x - end.x)) - angle
# 	if start.x < end.x:
# 		if start.y < end.y:
# 			alpha -= pi/4
# 			return (
# 					+10/np.sin(alpha), -10/np.cos(alpha),
# 					-10/np.sin(-alpha), +10/np.cos(-alpha)
# 				)

def dot(v, w):
	return sum(x0 * x1 for x0, x1 in zip(v, w))

class Transformation:
	def __init__(self, function, **kwargs):
		self.function = function

	def apply(self, input, window = None):
		return self.function(self, input, window)

class LinearTransformation(Transformation):
	def __init__(self, matrix, **kwargs):
		self.matrix = matrix
		super().__init__(lambda self, input, window: [dot(row, input) for row in self.matrix], **kwargs)

	def __mul__(self, other):
		return LinearTransformation(np.array([self.apply(row) for row in other.matrix]))

	def __imul__(self, other):
		self.matrix = (self * other).matrix

identity = LinearTransformation((
		(1, 0),
		(0, 1)
	))

rotate45 = LinearTransformation((
		(np.cos(np.pi/4), -np.sin(np.pi/4)),
		(np.sin(np.pi/4), np.cos(np.pi/4))
	))

rotate90 = LinearTransformation((
		(0, 1),
		(1, 0)
	))

enlarge2 = LinearTransformation((
		(2, 0),
		(0, 2)
	))

diminish2 = LinearTransformation((
		(.5, 0),
		(0, .5)
	))

shear_right = LinearTransformation((
		(1, 1),
		(0, 1)
	))

shear_left = LinearTransformation((
		(1, 0),
		(1, 1)
	))