import json
import pygame

class ResourceManager(object):
	def __init__(self):
		self._resourceMap = {}



	def init(self):
		# load default resources
		self.loadFont("defaultFont", None, 30)
		return True



	# load resource from disk
	def load(self, rname, rtype, rpath):
		if rtype == "text":
			file = open(rpath, "r")
			resource = file.read()
			self._resourceMap[rname] = resource

		elif rtype == "json":
			file = open(rpath, "r")
			resource = json.loads(file.read())
			self._resourceMap[rname] = resource

		elif rtype == "image":
			resource = pygame.image.load(rpath)
			self._resourceMap[rname] = resource



	def loadFont(self, rname, fontName, size):
		resource = pygame.font.Font(fontName, size)
		self._resourceMap[rname] = resource



	def unload(self, rname):
		if not rname in self._resourceMap:
			print("Resource Manager: No such Resource.")
			return None
		self._resourceMap.pop(rname)



	def addResource(self, rname, resource):
		self._resourceMap[rname] = resource



	def getResourceHandler(self, rname):
		if not rname in self._resourceMap:
			print("Resource Manager:" + rname + " No such Resource.")
			return None
		return self._resourceMap[rname]



	def removeResource(self, rname):
		self._resourceMap.pop(rname)



	def destroy(self):
		pass # temporarily



instance = ResourceManager()
