class StateNode(object):
	def __init__(self):
		# (transFunc, StateNode)
		self.transitions = None
		self._onStart = None
		self._onUpdate = None



	def init(self):
		self.transitions = []



	def addTransition(self, stateNode, transFunc):
		if not hasattr(transFunc, '__call__'):
			print("StateMachine: not a function")
		elif not isinstance(stateNode, StateNode):
			print("StateMachine: not a state node")
		else:
			self.transitions.append((stateNode, transFunc))

			

	def removeTransition(self, stateNode, transFunc):
		if not hasattr(transFunc, '__call__'):
			print("StateMachine: not a function")
		elif not isinstance(stateNode, StateNode):
			print("StateMachine: not a state node")
		else:
			self.transitions.remove((stateNode, transFunc))



	# node transition relays on event
	# this function returns next StateNode 
	# if transition fails, return itself.
	def transition(self, **kwargs):
		for (stateNode, transFunc) in self.transitions:
			if transFunc(**kwargs):
				stateNode.start()
				return stateNode
		# if not success
		return self



	def setStartFunc(self, func):
		if not hasattr(func, '__call__'):
			print("StateMachine: not a function")
		self._onStart = func



	def setUpdateFunc(self, func):
		if not hasattr(func, '__call__'):
			print("StateMachine: not a function")
		self._onUpdate = func



	# this function is called when transition
	# if the transition doesn't success, this will not call
	def start(self, *args):
		self._onStart(*args)



	def update(self, *args):
		self._onUpdate(*args)
