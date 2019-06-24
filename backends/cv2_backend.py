import numpy as np
import cv2
from matplotlib import image, pyplot as plt
from .base_backends import WriterBackend

class cv2Backend(WriterBackend):
	def __init__(self, size, canvas, **kwargs):
		super().__init__(size, canvas, **kwargs)

		self.fps = float(kwargs.get("fps", 60))

		self.fourcc = cv2.VideoWriter_fourcc(*kwargs.get("codec", "MJPG"))
		self.writer = None
		
	def startRecording(self, filename, **kwargs):
		self.writer = cv2.VideoWriter(f"output/video/{filename}", self.fourcc, kwargs.get("fps", self.fps), self.size)

	def stopRecording(self):
		self.writer.release()
		self.writer = None

	def saveFrame(self, filename):
		image.imsave(f"output/image/{filename}", self.frame.astype(np.uint8))

	def update(self):
		if self.writer is not None:
			self.writer.write(self.frame)

	def fill(self, color):
		self.frame = np.full((*self.size, 3), color, dtype=np.uint8)

	def putPixel(self, point, color):
		if 0 <= point[0] <= self.height and 0 <= point[1] <= self.width:
			self.frame[point[1], point[0]] = color

	def drawLine(self, start, end, color, **kwargs):
		cv2.line(self.frame, start, end, color, kwargs.get("width", 1))

	def drawRectangle(self, start, width, height, color, **kwargs):
		cv2.rectangle(self.frame, start, start + (height, width), color, kwargs.get("width", -1))

	def drawCircle(self, center, radius, color, **kwargs):
		cv2.circle(self.frame, center, radius, color, kwargs.get("width", -1))

	def drawPolygon(self, points, color, **kwargs):
		p = np.array(points).reshape((-1, 1, 2))
		if kwargs.get("width", 0) > 0:
			cv2.polylines(self.frame, [p], True, color, kwargs["width"])
		else:
			cv2.fillPoly(self.frame, [p], color)

	def drawConvexPolygon(self, points, color):
		p = np.array(points).reshape((-1, 1, 2))
		cv2.fillConvexPoly(self.frame, np.array(points), color)

	def drawImage(self, point, image):
		height, width = image.shape[:2]
		self.frame[point[0]:point[0] + height, point[1]:point[1] + width] = image

	def drawText(self, point, text, font, color, **kwargs):
		cv2.putText(self.frame, text, font, kwargs["size"], color)