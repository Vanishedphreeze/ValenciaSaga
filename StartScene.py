import pygame
import sys
import GameEntity
import ResourceManager
import SceneManager
import GameObject
from SceneBase import SceneBase
from BattleScene import BattleScene
from MenuScene import MenuScene
# from NewBattleScene import NewBattleScene

class StartScene(SceneBase):
	def __init__(self):
		super().__init__()
		self.title = GameObject.GameObject()
		self.titleBg = GameObject.GameObject()
		self.pressAnyKey = GameObject.GameObject()
		self.flag = False



	def init(self):
		super().init()
		ResourceManager.instance.load("Title", "image", "Title.png")
		ResourceManager.instance.load("TitleBg", "image", "TitleBg.png")
		ResourceManager.instance.load("PressAnyKey", "image", "PressAnyKey.png")
		self.title.init(ResourceManager.instance.getResourceHandler("Title"), (150, 100), (550, 260))
		self.titleBg.init(ResourceManager.instance.getResourceHandler("TitleBg"), (0, 0), (800, 600))
		self.pressAnyKey.init(ResourceManager.instance.getResourceHandler("PressAnyKey"), (300, 500), (200, 30))



	def start(self):
		super().start()



	def update(self, events):
		super().update(events)
		for event in events:
			# print(event)
			if event.type == pygame.QUIT:
				SceneManager.instance.switchScene(None)

			if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
				self.flag = True

			if (event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP) and self.flag:
				SceneManager.instance.switchScene(MenuScene())
				# SceneManager.instance.switchScene(NewBattleScene())



	def draw(self):
		super().draw()
		self.titleBg.draw(self.screen)
		self.title.draw(self.screen)
		self.pressAnyKey.draw(self.screen)



	def destroy(self):
		super().destroy()
		ResourceManager.instance.unload("Title")
		ResourceManager.instance.unload("TitleBg")
		ResourceManager.instance.unload("PressAnyKey")

