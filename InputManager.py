class InputManager(object):
	isMouseKeyPress = None
	isMouseKeyDown = None
	isMouseKeyUp = None
	mousePos = None
	mouseRel = None
	# 1~5: l, mid, r, u, d

	def init(self):
		isMouseKeyPress = [0 for i in range(6)]
		isMouseKeyDown = [0 for i in range(6)]
		isMouseKeyUp = [0 for i in range(6)]

	def update(self):
		# not finnished yet.
		pass

instance = InputManager()