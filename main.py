import numpy as np
from window import Window
from drawable import *
from grid import *
from functions import *
import colors

window = Window(800, 800)

grid = Grid((400, 400), (800, 800), (50, 50), defaultColor=colors.black, ratio=50)

window.addObject(grid)

curve = TimeCurve(lambda x, t: (np.sin((x + t) ** 2), x / 2 + np.sin(t + x)), [-10, 10], step=0.1)
curve.transformation = identity

grid.addObject(Vector(-1, 2, color = colors.red))

def draw_rect(window, *args):
	x, y, width, height = map(int, args)
	window.addObject(Rectangle((x, y), width, height, color=colors.white))

window.addCommand("draw-rect", draw_rect)

while 1:
	window.update()
