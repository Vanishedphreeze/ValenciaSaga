import pygame
import sys
import ResourceManager
from SceneBase import SceneBase
# from TestScene import TestScene
from BattleScene import BattleScene

class GameEntity(object):
	FPS = 60
	WINDOWSIZE = (800, 600)



	def __init__(self):
		self._curScene = BattleScene()

		self._windowContext = None
		self._clock = None
		self.isRunning = False



	def init(self):
		# init pygame and window context
		pygame.init()
		self._windowContext = pygame.display.set_mode(self.WINDOWSIZE)
		self._clock = pygame.time.Clock()

		# init game managers
		ResourceManager.instance.init()

		# load scene， this should be in SceneManager
		if isinstance(self._curScene, SceneBase) :
			self._curScene.init()
			return True
		else:
			# raise RuntimeError('SceneType mismatch.')
			print('SceneType mismatch')
			return False



	def run(self):
		self._curScene.start()

		while self._curScene.isRunning :
			'''
			# Event dispatcher, write in a new class if necessary
			for event in events :
				# print(event)
				if event.type == pygame.QUIT :
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN :
					self.isPressed = True
					self.isClick = True
				elif event.type == pygame.MOUSEBUTTONUP :
					self.isPressed = False

				if event.type == pygame.MOUSEMOTION :
					self.mousepos = event.pos
			'''

			self._curScene.update(pygame.event.get())
			self._curScene.draw()
			pygame.display.flip()
			self._clock.tick(self.FPS)

		# if the scene should be destroyed...
		self._curScene.destroy()



	def destroy(self):
		self._curScene.destroy()



	def getWindowContext(self):
		return self._windowContext



instance = GameEntity()
