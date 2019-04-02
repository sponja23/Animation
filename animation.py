import numpy as np
import pygame
from drawable import Drawable

class Animation(Drawable):
	def __init__(self, **kwargs):
		self.stop = False
		self.stoppedTime = 0

		super().__init__(**kwargs)

	def toggleAnimation(self, time = 0):
		self.stop = not self.stop
		self.stoppedTime = time

class CyclicAnimation(Animation):
	def __init__(self, **kwargs):
		self.period = kwargs.get("period", 1000)
		super().__init__(**kwargs)