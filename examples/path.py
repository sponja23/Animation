from init import *

canvas.addObject(Curve(lambda x: (np.sin(x), np.cos(x)), [0, 6.29]))
path = ParametricPath(lambda t: (np.sin(t), np.cos(t)))
canvas.addAnimation(path)

canvas.addObject(Vector([0, 1], bindings={"end": path.point}))

canvas.addObject(TimeCurve(lambda x, t: (x, np.cos(x + t)), [-5, 5], color = colors.blue))
canvas.addObject(Line([0, 0], [0, 0], bindings={"start": lambda: (0, path.point()[1]), "end": path.point}, color = colors.blue))

canvas.addObject(TimeCurve(lambda x, t: (np.sin(x + t), x), [-5, 5], color = colors.red))
canvas.addObject(Line([0, 0], [0, 0], bindings={"start": lambda: (path.point()[0], 0), "end": path.point}, color = colors.red))

canvas.loop(60)