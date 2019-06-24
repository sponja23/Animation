class Engine:
	def __init__(self, canvas, **kwargs):
		self.objects = {}
		self.nextId = 0
		
		self.canvas = canvas

		

	def addBody(self, body):
		body.attachTo(self)
		

	def getId(self):
		self.nextId += 1
		return f"body_{self.nextId - 1}"


