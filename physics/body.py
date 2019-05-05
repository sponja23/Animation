import numpy as np

class Body:
	def __init__(self, boundary, **kwargs):
		self.boundary = boundary
		self.position
		
		self.mass = kwargs.get("mass", 1)
		self.velocity = kwargs.get("velocity", np.array((0, 0)))
		self.forces = []
		self.permanentForces = []

		self.engine = kwargs.get("engine", None)
		self.sprite = kwargs.get("sprite", None)
		self.color = kwargs.get("color", None)

	def attachTo(self, engine):
		self.engine = engine
		self.canvas = engine.canvas
		self.engine.objects.append(self)

		if self.sprite is None:
			self.sprite = self.boundary.getSprite(self.color if self.color is not None else self.canvas.default_color)

	def move(deltaPos):
		self.boundary.move(deltaPos)

	def addForce(self, force):
		self.forces.append(force)

	def update(self):
		dt = self.canvas.deltaTime / 1000 # seconds
		self.applyForces(dt)
		self.move(self.velocity * dt)

	def applyForces(self, dt):
		resultForce = np.sum(self.forces + self.permanentForces, axis=0) / (len(self.forces) + len(self.permanentForces))
		self.forces = []
		self.velocity += (resultForce / self.mass) * dt

	@property
	def center(self):
		return self.boundary.center
	
