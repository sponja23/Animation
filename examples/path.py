from init import *

path1 = ParametricPath(lambda t: (2 * np.sin(t), 2 * np.cos(t)), speed = 5, canvas = canvas)
path2 = path1 + ParametricPath(lambda t: (np.sin(3 * t), np.cos(7 * t)), speed = 5, canvas = canvas)

canvas.addObject(Vector((0, 0), bindings={"end": path1.point}, color=colors.red))
canvas.addObject(Vector((0, 0), bindings={"start": path1.point, "end": path2.point}, color=colors.blue))

canvas.addObject(ParametricTraceCurve(path2.point, 0, speed=1000, step=10))

canvas.loop(60)