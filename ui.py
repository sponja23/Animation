class Menu:
	def __init__(self, canvas):
		self.canvas = canvas
		self.options = []
		self.path = []

	def choose(self, key):
		if key == "..":
			self.path.pop()
		for option in self.getOptions():
			if option.name == key or option.hotkey == key:
				if type(option) == SubMenu:
					self.path += name
					return self
				else:
					return option

	def add(self, option, path=[]):
		option.canvas = self.canvas
		self.getOptions(path).append(option)

	def addOption(self, name, action, **kwargs):
		option = Option(name, action, **kwargs)
		option.canvas = self.canvas
		self.getOptions(kwargs.get("path", [])).append(option)

	def getOptions(self, path=None):
		if path == None:
			path = self.path
		return self.options if len(path) == 0 else self.options[path[0]].getOptions(path[1:])

	def execute(self):
		self.canvas.displayMenu()

class Option:
	def __init__(self, name, action, **kwargs):
		self.canvas = None
		self.name = name
		self.action = action
		self.enabled = kwargs.get("enabled", True)
		self.hotkey = kwargs.get("hotkey", None)

	def execute(self):
		self.action(self.canvas)

class SubMenu(Menu, Option):
	def __init__(self, name, **kwargs):
		Menu.__init__(self, None)
		Option.__init__(self, name, None, **kwargs)


