from init import *

canvas.addObject(TimeCurve(lambda x, t: (x, np.sin(x) * 2 * np.sin(t) + 3), [-10, 10], color=colors.red, speed=5))
canvas.addObject(TimeCurve(lambda x, t: (x, np.sin(x + t)), [-10, 10], color=colors.green, speed=5))
canvas.addObject(TimeCurve(lambda x, t: (x, np.sin(x * np.sin(t)) - 3), [-10, 10], color=colors.blue, speed=5))

canvas.loop(60)