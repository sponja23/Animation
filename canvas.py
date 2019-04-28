from collections import deque
import numpy as np
from drawable import colors
from drawable.drawable import ensureArray
from backends.pygame_backend import PygameBackend
from time import sleep

def panning(self, pos, rel):
	if self.backend.isKeyPressed("space") and self.backend.mouseButtons[1]:
		self.center += rel

def zooming(self, pos, button):
	if button == 4:
		amount = 5 if self.backend.isKeyPressed("left shift") else 1
		if self.ratio - amount > 5:
			self.ratio -= amount

	elif button == 5:
		amount = 5 if self.backend.isKeyPressed("left shift") else 1
		self.ratio += amount

def printPoint(self, pos, button):
	if button == 1:
		print(pos, self.inverseTransform(pos))

class Canvas:
	def __init__(self, size, **kwargs):
		self.size = size
		self.backgroundColor = kwargs.get("backgroundColor", colors.background_color)
		self.defaultColor = kwargs.get("defaultColor", colors.default_color)

		self.ratio = kwargs.get("ratio", 1.0)
		self.center = ensureArray(kwargs.get("center", [self.size[0]/2, self.size[1]/2]))

		self.backend = kwargs.get("backend", PygameBackend)(size, self, **kwargs)

		self.objects = deque([])

		self.time = kwargs.get("startTime", 0)
		self.delta_time = None

		self.data = {}

		self.debug = kwargs.get("debug", False)

		if self.backend.interactive: self.init_interactive(**kwargs)

	def init_interactive(self, **kwargs):
		self.onMouseDown = []
		self.onMouseUp = []
		self.onMouseMove = []
		self.onKeyPress = []

		if kwargs.get("movement", True):
			self.onMouseMove.append(panning)
			self.onMouseDown.append(zooming)

		if self.debug:
			self.onMouseDown.append(printPoint)


	@property
	def min_x(self):
		return -self.center[0] / self.ratio

	@property 	
	def max_x(self):
		return (self.size[0] - self.center[0]) / self.ratio

	@property 	
	def min_y(self):
		return -(self.size[1] - self.center[1]) / self.ratio

	@property 	
	def max_y(self):
		return self.center[1] / self.ratio

	@property
	def transformation(self):
		return np.array([[self.ratio,  0], 
						 [0, -self.ratio]])
	
	@property
	def inverse_transformation(self):
		return np.array([[1.0/self.ratio,  0],
						 [0, -1.0/self.ratio]])
	
	def transform(self, point):
		return [int(x) for x in (self.transformation @ point + self.center)]

	def inverseTransform(self, point):
		return self.inverse_transformation @ (point - self.center) 

	def addObject(self, object):
		object.attachTo(self)

	def inRange(self, point):
		return (self.min_x <= point[0] <= self.max_x and self.min_y < point[1] < self.max_y)

	def getObjectColor(self):
		return self.defaultColor # TODO

	def advance(self, time_passed):
		self.backend.fill(self.backgroundColor)
		self.delta_time = time_passed
		self.time += self.delta_time
		self.update()

	def jump(self, time):
		self.backend.fill(self.backgroundColor)
		self.delta_time = None
		self.time = time
		self.update()

	def update(self):
		for obj in reversed(self.objects):
			obj.beforeDraw()
			obj.draw()

	def mouseDown(self, pos, button):
		pos = np.array(pos)
		for handler in self.onMouseDown:
			handler(self, pos, button)

	def mouseUp(self, pos, button):
		pos = np.array(pos)
		for handler in self.onMouseUp:
			handler(self, pos, button)

	def mouseMove(self, pos, rel):
		pos, rel = np.array(pos), np.array(rel)
		for handler in self.onMouseMove:
			handler(self, pos, rel)

	def keyPressed(self, key):
		for handler in self.onKeyPress:
			handler(self, keyPress)

	def putPixel(self, position, color):
		self.backend.putPixel(self.transform(position), color)

	def drawLine(self, start, end, color, **kwargs):
		self.backend.drawLine(self.transform(start), self.transform(end), color, **kwargs)

	def drawRectangle(self, start, width, height, color, **kwargs):
		self.backend.drawRectangle(self.transform(start), width * self.ratio, height * self.ratio, color, **kwargs)

	def drawCircle(self, center, radius, color, **kwargs):
		self.backend.drawCircle(self.transform(center), radius * self.ratio, color, **kwargs)

	def drawPolygon(self, points, color, **kwargs):
		self.backend.drawPolygon([self.transform(p) for p in points], color, **kwargs)

	def drawImage(self, point, image):
		self.backend.drawImage(self.transform(point), image)

	def drawArrow(self, start, end, color):
		length = np.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
		p1, p2 = arrow_points(start, end, min(length / 4, .20), np.pi/6)
		p1, p2, start, end = map(self.transform, [p1, p2, start, end])
		self.backend.drawLine(start, end, color, width=2)
		self.backend.drawPolygon([end, p1, p2], color, width=0)

	def loop(self, frequency=60): # frequency in Hz; Can't be stopped
		while 1:
			self.advance(int(1000 / frequency)) # in ms
			sleep(1 / frequency) # in seconds

def arrow_points(start, end, length, target_angle):
	if start[0] == end[0]:
		line_angle = np.pi/2 if start[1] < end[1] else -np.pi/2
	else:
		line_angle = np.arctan((start[1] - end[1]) / (start[0] - end[0]))
	arrow_angle_1 = line_angle - target_angle
	arrow_angle_2 = np.pi / 2 - line_angle - target_angle 

	sign_x = 1 if start[0] > end[0] else -1
	sign_y = sign_x

	arrow_point_1 = (end[0] + sign_x * length * np.cos(arrow_angle_1), end[1] + sign_y * length * np.sin(arrow_angle_1))
	arrow_point_2 = (end[0] + sign_x * length * np.sin(arrow_angle_2), end[1] + sign_y * length * np.cos(arrow_angle_2))

	return (arrow_point_1, arrow_point_2)
