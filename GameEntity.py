import pygame
import sys
import ResourceManager
import SceneManager
import EventManager


class GameEntity(object):
	WINDOWSIZE = (800, 600)



	def __init__(self):
		self._windowContext = None
		self.isRunning = False



	def init(self):
		# init pygame and window context
		pygame.init()
		self._windowContext = pygame.display.set_mode(self.WINDOWSIZE)

		# init game managers
		ResourceManager.instance.init()
		SceneManager.instance.init()
		EventManager.instance.init()

		return True



	def run(self):
		SceneManager.instance.run()



	def destroy(self):
		EventManager.instance.destroy()
		SceneManager.instance.destroy()
		ResourceManager.instance.destroy()



	def getWindowContext(self):
		return self._windowContext



instance = GameEntity()
