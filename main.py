from window import Window
from drawable import *
from math_drawable import *
import colors

window = Window(1000, 600)

window.addObject(ParametricPath((200, 200), lambda t: (np.sin(t) % 5, t % 5), 0, color = colors.green))

def draw_rect(window, *args):
	x, y, width, height = map(int, args)
	window.addObject(Rectangle((x, y), width, height, color=colors.white))

window.addCommand("draw-rect", draw_rect)

while 1:
	window.update()
