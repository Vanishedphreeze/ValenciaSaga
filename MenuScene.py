import pygame
import sys
import GameEntity
import ResourceManager
import SceneManager
import GameObject
from SceneBase import SceneBase
import BattleScene
import BattleTutorialScene
import SummonTutorialScene
import AttackTutorialScene
import MoveTutorialScene
# from NewBattleScene import NewBattleScene

class MenuScene(SceneBase):
	def __init__(self):
		super().__init__()
		self.menuBg = GameObject.GameObject()
		self.gameStart = GameObject.GameObject()
		self.gameContinue = GameObject.GameObject()
		self.gameTutorial = GameObject.GameObject()
		self.gameExit = GameObject.GameObject()
		self.flag = False



	def init(self):
		super().init()
		ResourceManager.instance.load("menuBg", "image", "TitleBg.png")
		ResourceManager.instance.load("gameStart", "image", "start.png")
		ResourceManager.instance.load("gameContinue", "image", "continue.png")
		ResourceManager.instance.load("gameTutorial", "image", "tutorial.png")
		ResourceManager.instance.load("gameExit", "image", "exit.png")
		self.menuBg.init(ResourceManager.instance.getResourceHandler("menuBg"), (0, 0), (800, 600))
		self.gameStart.init(ResourceManager.instance.getResourceHandler("gameStart"), (325, 200), (150, 50))
		self.gameContinue.init(ResourceManager.instance.getResourceHandler("gameContinue"), (325, 300), (150, 50))
		self.gameTutorial.init(ResourceManager.instance.getResourceHandler("gameTutorial"), (325, 400), (150, 50))
		self.gameExit.init(ResourceManager.instance.getResourceHandler("gameExit"), (325, 500), (150, 50))



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
				# SceneManager.instance.switchScene(BattleScene.BattleScene())
				# SceneManager.instance.switchScene(NewBattleScene())
				if self.gameStart.pointCollide(event.pos):
					# print("start")
					ResourceManager.instance.addResource("isContinue", False)
					SceneManager.instance.switchScene(BattleScene.BattleScene())
					# SceneManager.instance.switchScene(BattleTutorialScene.BattleTutorialScene())
				elif self.gameContinue.pointCollide(event.pos):
					# print("continue")
					ResourceManager.instance.addResource("isContinue", True)
					SceneManager.instance.switchScene(BattleScene.BattleScene())
				elif self.gameTutorial.pointCollide(event.pos):
					# print("tutorial")
					SceneManager.instance.switchScene(SummonTutorialScene.SummonTutorialScene())
				elif self.gameExit.pointCollide(event.pos):
					SceneManager.instance.switchScene(None)



	def draw(self):
		super().draw()
		self.menuBg.draw(self.screen)
		self.gameStart.draw(self.screen)
		self.gameContinue.draw(self.screen)
		self.gameTutorial.draw(self.screen)
		self.gameExit.draw(self.screen)



	def destroy(self):
		super().destroy()
		ResourceManager.instance.unload("menuBg")
		ResourceManager.instance.unload("gameStart")
		ResourceManager.instance.unload("gameContinue")
		ResourceManager.instance.unload("gameTutorial")
		ResourceManager.instance.unload("gameExit")

