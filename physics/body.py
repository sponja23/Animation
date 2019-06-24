import numpy as np

class Body:
	def __init__(self, boundary, **kwargs):
		self.id = kwargs.get("id", None)
		self.boundary = boundary
		
		self.mass = kwargs.get("mass", 1)
		self.velocity = kwargs.get("velocity", np.array((0, 0)))
		self.forces = []
		self.permanentForces = {}

		self.engine = kwargs.get("engine", None)
		self.sprite = kwargs.get("sprite", None)
		self.color = kwargs.get("color", None)
		self.invisible = kwargs.get("invisible", False)

	def attachTo(self, engine):

		self.engine = engine
		self.canvas = engine.canvas
		
		if self.id is None:
			self.id = self.engine.getId()
		
		self.engine.objects[self.id] = self

		if self.sprite is None and not self.invisible:
			self.sprite = self.boundary.getSprite(self.color if self.color is not None else self.canvas.default_color)
			self.sprite.id = self.id + "_sprite"
			self.sprite.attachTo(self.canvas)

	def move(deltaPos):
		self.boundary.move(deltaPos)
		self.sprite.move(deltaPos)

	def rotate(self, theta):
		self.boundary.rotate(theta)
		self.sprite.rotate(theta)
		
	def addForce(self, force):
		self.forces.append(force)

	def update(self):
		dt = self.canvas.deltaTime / 1000 # seconds
		self.applyForces(dt)
		self.move(self.velocity * dt)

	def applyForces(self, dt):
		resultForce = np.sum(self.forces + self.permanentForces.values(), axis = 0)
		self.forces = []
		self.velocity += (resultForce / self.mass) * dt


	@property
	def center(self):
		return self.boundary.center()
