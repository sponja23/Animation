from ..utils import ensureArray

class Force:
	def __init__(self):
		pass

	def compute(self):
		pass

	def __add__(self, other):
		return CompoundForce(v1, v2, lambda x, y: x + y)

	def __sub__(self, other):
		return 

class ConstantForce(Force):
	def __init__(self, vector):
		self.vector = ensureArray(vector)
		super().__init__()

	def compute(self):
		return self.vector

class CompoundForce(Force):
	def __init__(self, v1, v2, operation):
		self.v1 = v1
		self.v2 = v2
		self.operation = operation
		super().__init__()

	def compute(self):
		return self.operation(v1.compute(), v2.compute())