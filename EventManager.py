class EventManager(object):
	def __init__(self):
		self._event = {}



	def init(self):
		pass



	# event : str 
	def addEvent(self, event):
		self._event[event] = set()



	def removeEvent(self, event):
		self._event.pop(event)



	def addListener(self, event, func):
		if hasattr(func, '__call__'):
			self._event[event].add(func)
		else:
			print("EventManager: not a function")



	def removeListener(self, event, func):
		if hasattr(func, '__call__'):
			self._event[event].remove(func)
		else:
			print("EventManager: not a function")



	def call(self, event, *args):
		for func in self._event[event]:
			func(*args)



	def destroy(self):
		pass



instance = EventManager()