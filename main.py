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

canvas = Canvas((800, 800), backend = pygame, ratio = 50, fps = 24, debug = True)

canvas.addObject(Grid((1, 1)))

path = CyclicPolygonPath([(0,0), (0,1), (1,1), (1,0)], time=5)
canvas.addAnimation(path)
canvas.addObject(Vector((0, 0), bindings={"end": path.point}, color=colors.red))

if isinstance(canvas.backend, PygameBackend):
	canvas.loop(60)

def record(time, filename):
	canvas.startRecording(f"{filename}.avi")
	canvas.play(time)
	canvas.stopRecording()

def save_frame(filename):
	canvas.saveFrame(f"{filename}.jpg")