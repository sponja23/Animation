import numpy as np
from numpy import pi

def distance(x0, y0, x1, y1):
	return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** .5

def arrow_offset(start, end, length, target_angle):
	line_angle = np.arctan2((start.y - end.y), (start.x - end.x))
	arrow_angle_1 = line_angle - target_angle
	arrow_angle_2 = np.pi / 2 - line_angle - target_angle 
	sign_x = 1 if start.x < end.x else -1
	sign_y = 1 if start.y < end.y else -1

	arrow_point_1 = end + (sign_x * length * np.cos(arrow_angle_1), sign_y * length * np.sin(arrow_angle_1))
	arrow_point_2 = end + (sign_x * length * np.cos(arrow_angle_2), sign_y * length * np.sin(arrow_angle_2))

	print(arrow_point_1, arrow_point_2)

	return (arrow_point_1, arrow_point_2)


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