import numpy as np
from drawable import colors
from drawable.math import *
from drawable.shapes import *
from drawable.animations import *
from canvas import Canvas

canvas = Canvas((800, 800), ratio = 50, debug = True)

canvas.addObject(Grid((1, 1)))

range = np.arange(-5, 6, .5)
points = np.transpose(np.meshgrid(range, range))
points = points.reshape(-1, points.shape[-1])

canvas.addObject(VectorField(lambda x, y: (x * y, y ** 2), range=[-5, 5], step=.5, maxLength=0.5))

canvas.loop(60) # freq in Hz
