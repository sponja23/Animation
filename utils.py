import numpy as np

PI = np.pi

def ensureArray(obj, **kwargs):
	if not isinstance(obj, np.ndarray):
		return np.array(obj, **kwargs)
	return obj

def ensureList(obj):
	if type(obj) is not list and type(obj) is not tuple:
		return [obj]
	return obj

def ensureTuple(obj):
	if type(obj) is not tuple:
		return tuple(obj)
	return obj

def distance(p1, p2):
	return np.linalg.norm(p1 - p2)

def areParalel(line1, line2):
	p11, p12 = line1
	p21, p22 = line2
	return ((p11[1] - p12[1]) / (p11[0] - p12[0]) == (p22[1] - p21[1]) / (p22[0] - p21[0]))

def vectorAngle(v):
	return np.atan2(*v)

def isConvex(points):
	try:
		if len(points) < 3:
			return False

		old = points[-2]
		new = points[-1]
		new_direction = vectorAngle(new - old)

		angle_sum = 0.0
		for index, point in enumerate(points):
			old, old_direction = new, new_direction
			new = point
			new_direction = vectorAngle(new - old)
			
			if old == new:
				return False

			angle = new_direction - old_direction
			if angle <= -PI:
				angle += 2 * PI
			elif angle > PI:
				angle -= 2 * PI

			if index == 0:
				if angle == 0.0:
					return False
				orientation = +1.0 if angle > 0 else -1.0
			elif orientation * angle <= 0.0: # different sign or 0
				return False

			angle_sum += angle

		return abs(round(angle_sum / (2 * PI))) == 1

	except (ArithmeticError, TypeError, ValueError):
		return False


