import numpy as np
from drawable import colors
from drawable.math import *
from drawable.shapes import *
from drawable.animations import *
from drawable.drawable import *
from canvas import Canvas
from backends import cv2Backend, PygameBackend

pygame = PygameBackend
cv2 = cv2Backend

canvas = Canvas((2000, 2000), backend = cv2, ratio = 200, fps = 24, debug = True)

canvas.addObject(Grid((1, 1)))

canvas.addObject(VectorField(lambda x, y: (x, np.sin(y)), range=[-10, 10], step=.25, maxLength=0.25))

if isinstance(canvas.backend, PygameBackend):
	canvas.loop(60)

def record(time, filename):
	canvas.startRecording(f"{filename}.avi")
	canvas.play(time)
	canvas.stopRecording()

def save_frame(filename):
	canvas.saveFrame(f"{filename}.jpg")

canvas.advance(10)
save_frame("test")