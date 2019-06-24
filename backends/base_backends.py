from collections import defaultdict
import numpy as np

class Backend:
	def __init__(self, size, canvas, **kwargs):
		self.width, self.height = self.size = size
		self.canvas = canvas

		self.interactive = False
		self.transformation = None
		self.inverse_transformation = None

		self.fps = float(kwargs.get("fps", 24))

	def update(self):
		raise NotImplemented

	def fill(self, color):
		raise NotImplemented

	def putPixel(self, point, color):
		raise NotImplemented

	def drawLine(self, start, end, color, **kwargs):
		raise NotImplemented

	def drawRectangle(self, start, width, height, color, **kwargs):
		raise NotImplemented

	def drawCircle(self, center, radius, color, **kwargs):
		raise NotImplemented

	def drawPolygon(self, points, color, **kwargs):
		raise NotImplemented

	def drawImage(self, point, image):
		raise NotImplemented

	def drawText(self, point, content, font, color, **kwargs):
		raise NotImplemented

class InteractiveBackend(Backend):
	def __init__(self, size, canvas, **kwargs):
		super().__init__(size, canvas, **kwargs)

		self.interactive = True

		self.mouseButtons = [False for i in range(6)]
		self.keyPressed = defaultdict(lambda: False)

	def isKeyPressed(self, key):
		return self.keyPressed[key]

	def isButtonPressed(self, button):
		return self.mouseButtons[button]

	def handleEvent(self, event): # Must fire the canvas' events, and generally be called once during a fill() call
		raise NotImplemented

class WriterBackend(Backend):
	def __init__(self, size, canvas, **kwargs):
		super().__init__(size, canvas, **kwargs)

		self.recording = False

		self.frame = np.zeros((*self.size, 3))
		self.transformation = np.array([[+1.,  0 ],
										[ 0 , -1.]])
		self.inverse_transformation = np.array([[-1.,  0 ],
												[ 0 , +1.]])

	def startRecording(self, filename, **kwargs):
		raise NotImplemented

	def stopRecording(self):
		raise NotImplemented

	def saveFrame(self, filename):
		raise NotImplemented