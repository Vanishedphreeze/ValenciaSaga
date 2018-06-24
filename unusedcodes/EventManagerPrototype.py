class EventManager(object):
	def __init__(self):
		self._event = {}



	# event : str 
	def addEvent(self, event):
		self._event[event] = set()



	def removeEvent(self, event):
		self._event.pop(event)



	def addListener(self, event, func):
		if hasattr(func, '__call__'):
			self._event[event].add(func)
		else:
			print("not a function")



	def removeListener(self, event, func):
		if hasattr(func, '__call__'):
			self._event[event].remove(func)
		else:
			print("not a function")



	def call(self, event, *args):
		for func in self._event[event]:
			func(args)
