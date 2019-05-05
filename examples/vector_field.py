from init import *

canvas.addObject(VectorField(lambda x, y: (x * y, y ** 2), range=[-5, 5], step=.5, maxLength=0.5))

canvas.loop(60)