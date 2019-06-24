import colorsys

black  = (   0,   0,   0)
red    = ( 255,   0,   0)
green  = (   0, 255,   0)
blue   = (   0,   0, 255)
white  = ( 255, 255, 255)

default_color = black
background_color = white

def interpolation(c1, c2, p): # 0 <= p <= 1
	c1_hsv = colorsys.rgb_to_hsv(*[a / 255 for a in c1])
	c2_hsv = colorsys.rgb_to_hsv(*[a / 255 for a in c2])

	distances = [(a - b) % 1 for a, b in zip(c2_hsv, c1_hsv)]
	color = [(start + p * dist) % 1 for start, dist in zip(c1_hsv, distances)]

	for i in range(3):
		if color[i] == 0 and c1_hsv[i] != 0 and c2_hsv[i] != 0:
			color[i] = 1


	return tuple(a * 255 for a in colorsys.hsv_to_rgb(*color))