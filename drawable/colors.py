import numpy as np

black  = np.array((   0,   0,   0))
red    = np.array(( 255,   0,   0))
green  = np.array((   0, 255,   0))
blue   = np.array((   0,   0, 255))
white  = np.array(( 255, 255, 255))

default_color = black
background_color = white

def interpolation(color1, color2, parameter):
	return ((color2 - color1) * parameter + color1)