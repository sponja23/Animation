from init import *

range = np.arange(-5, 6, .4)
points = np.transpose(np.meshgrid(range, range))
points = points.reshape(-1, points.shape[-1])

canvas.addObject(VectorField(lambda x, y: (x * y, y ** 2), points, maxLength=0.5))

canvas.loop(60)