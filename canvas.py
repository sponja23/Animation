import numpy as np
import sys
from collections import OrderedDict
from drawable import colors
from drawable.drawable import Text
from utils import ensureArray
from backends.pygame_backend import PygameBackend
from time import sleep
from ui import Menu

def panning(self, pos, rel):
	if self.backend.isKeyPressed("space") and self.backend.isButtonPressed(1):
		self.center += rel

def screenCap(self, key):
	if key == 'p':
		self.backend.saveFrame("screen.jpg")

def zooming(self, pos, button): # TODO
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

def setTextToTime(self):
	self.content = str(self.canvas.time / 1000)

def openMenuFunction(keybind):
	def openMenu(self, key):
		if key == keybind:
			self.displayMenu()
	return openMenu

class EventHandler:
	def __init__(self, types):
		self.handlers = {t: [] for t in types}

	def add(self, *types):
		for t in types:
			self.handlers[t] = []

	def on(self, type, function):
		self.handlers[type].append(function)

	def fire(self, canvas, type, *args, **kwargs):
		for handler in self.handlers[type]:
			handler(canvas, *args, **kwargs)


class Canvas:
	def __init__(self, size, **kwargs):
		self.objects = {}
		self.nextObjectId = 0
		
		self.animations = {}
		self.nextAnimationId = 0
		
		self.size = size
		self.backgroundColor = kwargs.get("backgroundColor", colors.background_color)
		self.defaultColor = kwargs.get("defaultColor", colors.default_color)

		self.ratio = kwargs.get("ratio", 1.0)
		self.center = ensureArray(kwargs.get("center", [self.size[0]/2, self.size[1]/2]))

		self.backend = kwargs.get("backend", PygameBackend)(size, self, **kwargs)

		self.time = kwargs.get("startTime", 0)
		self.deltaTime = None

		self.data = OrderedDict({})

		self.debug = kwargs.get("debug", False)
		self.handler = EventHandler(types=["tick"])
		self.on("tick", type(self).onTick)

		self.fps = self.backend.fps
		self.frame_time = 1000 / self.fps

		if self.backend.interactive: self.init_interactive(**kwargs)
		if self.debug: self.init_debug(**kwargs)


	def init_debug(self, **kwargs):
		self.addObject(Text((0, 0), "", "monospace", color=colors.black, onBeforeDraw=setTextToTime,
					   		bindings={"start": lambda: self.inverseTransform((10, self.size[1] - 20))}))


#
#
#  EVENTS
#
#

	def fire(self, type, *args, **kwargs):
		self.handler.fire(self, type, *args, **kwargs)

	def on(self, type, function):
		self.handler.on(type, function)

	def init_interactive(self, **kwargs):
		self.handler.add("mouseDown", "mouseUp", "mouseMove", "keyPress")

		self.menu = Menu(self)
		self.menu.addOption("Quit", lambda canvas: sys.exit(), hotkey='q')

		if kwargs.get("movement", True):
			self.handler.on("mouseDown", zooming)
			self.handler.on("mouseMove", panning)
		if kwargs.get("screenCap", True):
			self.handler.on("keyPress", screenCap)
		if self.debug:
			self.handler.on("mouseDown", printPoint)

		self.handler.on("keyPress", openMenuFunction(kwargs.get("menu_key", 'e')))

	def displayMenu(self):
		print("\n" + '\n'.join([f"[{option.hotkey}] {option.name}" for option in self.menu.getOptions() if option.enabled]))
		self.menu.choose(input('> ')).execute()

	def onTick(self, time_passed):
		pass

#
#
#  GEOMETRY
#
#


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
		return self.backend.transformation @ [[self.ratio, 0], 
						 					  [0, self.ratio]]
	
	@property
	def inverse_transformation(self):
		return self.backend.inverse_transformation @ [[1.0/self.ratio, 0],
						 					  		  [0, 1.0/self.ratio]]
	
	def transform(self, point):
		return tuple([int(x) for x in (self.transformation @ point + self.center)])

	def inverseTransform(self, point):
		return self.inverse_transformation @ (point - self.center) 

	def inRange(self, point):
		return (self.min_x <= point[0] <= self.max_x and self.min_y < point[1] < self.max_y)

#
#
#  OBJECTS
#
#


	def addObject(self, object):
		object.attachTo(self)
		return object.id

	def getObjectId(self):
		self.nextObjectId += 1
		return f"sprite_{self.nextObjectId - 1}"

	def getObjectColor(self):
		return self.defaultColor # TODO


#
#
#  ANIMATIONS
#
#

	def addAnimation(self, animation):
		animation.attachTo(self)
		return animation.id

	def getAnimationId(self):
		self.nextAnimationId += 1
		return f"animation_{self.nextAnimationId - 1}"

	def pauseAnimations(self):
		for id, animation in self.animations.items():
			animation.pause()

	def unpauseAnimations(self):
		for id, animation in self.animations.items():
			animation.unpause()

	def toggleAnimations(self):
		for id, animation in self.animations.items():
			animation.togglePause()

#
#
#  FRAMES
#
#

	def newFrame(self):
		self.backend.fill(self.backgroundColor)

	def advance(self, time_passed=None): # milliseconds
		if time_passed is None:
			time_passed = self.frame_time
		self.newFrame()
		self.deltaTime = time_passed
		self.time += self.deltaTime
		self.update(time_passed)

	def play(self, time): # seconds
		n_frames = int(time * self.fps)
		for i in range(1, n_frames + 1):
			if self.debug:
				print(f"Playing {int((i / n_frames) * 100)}%\r", end="")
			self.advance()

	def jump(self, time):
		self.newFrame()
		self.deltaTime = None
		self.time = time
		self.update()

	def update(self, time_passed = None):
		for id, obj in self.objects.items():
			obj.beforeDraw()
			obj.draw()
		self.fire("tick", time_passed)
		self.backend.update()

	def loop(self, frequency=None): # frequency in Hz; Can't be stopped
		if not self.backend.interactive:
			raise NotImplemented
		while 1:
			if frequency is None:
				frequency = self.backend.fps
			self.advance(int(1000 / frequency)) # in ms
			sleep(1 / frequency) # in seconds

#
#
#  SAVING
#
#



	def startRecording(self, filename, **kwargs):
		self.backend.startRecording(filename, **kwargs)

	def stopRecording(self):
		self.backend.stopRecording()

	def saveFrame(self, filename):
		self.backend.saveFrame(filename)


#
#
#  DRAWING
#
#

	def putPixel(self, position, color):
		self.backend.putPixel(self.transform(position), color)

	def drawLine(self, start, end, color, **kwargs):
		self.backend.drawLine(self.transform(start), self.transform(end), tuple(color), **kwargs)

	def drawRectangle(self, start, width, height, color, **kwargs):
		self.backend.drawRectangle(self.transform(start), int(width * self.ratio), int(height * self.ratio), tuple(color), **kwargs)

	def drawCircle(self, center, radius, color, **kwargs):
		self.backend.drawCircle(self.transform(center), int(radius * self.ratio), tuple(color), **kwargs)

	def drawPolygon(self, points, color, **kwargs):
		self.backend.drawPolygon([self.transform(p) for p in points], tuple(color), **kwargs)

	def drawConvexPolygon(self, points, color, **kwargs):
		self.backend.drawConvexPolygon([self.transform(p) for p in points], tuple(color), **kwargs)

	def drawImage(self, point, image):
		self.backend.drawImage(self.transform(point), image)

	def drawArrow(self, start, end, color):
		length = np.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
		p1, p2 = arrow_points(start, end, min(length / 4, .20), np.pi/6)
		p1, p2, start, end = map(self.transform, [p1, p2, start, end])
		self.backend.drawLine(start, end, tuple(color), width=2)
		self.backend.drawConvexPolygon([end, p1, p2], tuple(color))

	def drawText(self, point, text, font, color, **kwargs):
		self.backend.drawText(self.transform(point), text, font, tuple(color), **kwargs)



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
