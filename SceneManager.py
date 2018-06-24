import sys
import pygame
from SceneBase import SceneBase
# from TestScene import TestScene
# from BattleScene import BattleScene
from StartScene import StartScene

class SceneManager(object):
	FPS = 60

	def __init__(self):
		self._curScene = None
		self._nextScene = None
		self._clock = None

		self._isCurSceneRunning = False



	def init(self):
		self._curScene = StartScene()
		self._clock = pygame.time.Clock()
		return True



	def run(self):
		while self._curScene != None:
			if isinstance(self._curScene, SceneBase) :
				self._curScene.init()
			else:
				# raise RuntimeError('SceneType mismatch.')
				print('SceneType mismatch')
				continue

			self._curScene.start()
			self._isCurSceneRunning = True

			while self._isCurSceneRunning:
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
			self._curScene = self._nextScene



	def destroy(self):
		# self._curScene.destroy()
		pass



	def switchScene(self, scene):
		self._nextScene = scene
		self._isCurSceneRunning = False



instance = SceneManager()