from sys import path
import numpy as np

path.append("../")

from canvas import Canvas
from drawable import colors
from drawable.math import *
from drawable.shapes import *
from drawable.animations import *

canvas = Canvas((800, 800), ratio = 50)

canvas.addObject(Grid((1, 1)))