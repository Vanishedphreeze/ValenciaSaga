import pygame
import sys
import GameEntity
import ResourceManager
import SceneManager
import GameObject
from SceneBase import SceneBase
import StartScene
# import NewBattleScene

class ResultScene(SceneBase):
	def __init__(self):
		super().__init__()
		self.result = GameObject.GameObject()
		self.battleBg = GameObject.GameObject()
		self.accounter = ResourceManager.instance.getResourceHandler("Accounter")
		self.statusFont = None
		self.playerStatus = [GameObject.GameObject() for i in range(5)]
		self.enemyStatus = [GameObject.GameObject() for i in range(5)]



	def init(self):
		super().init()
		ResourceManager.instance.load("BattleBg", "image", "BattleBg.png")
		self.battleBg.init(ResourceManager.instance.getResourceHandler("BattleBg"), (0, 0), (800, 600))

		res = ResourceManager.instance.getResourceHandler("result")
		if res == 1:
			ResourceManager.instance.load("Result", "image", "Win.png")
		else:
			ResourceManager.instance.load("Result", "image", "Lose.png")
		self.result.init(ResourceManager.instance.getResourceHandler("Result"), (100, 50), (600, 300))

		self.statusFont = ResourceManager.instance.getResourceHandler("defaultFont")
		# self.status.init(self.statusFont.render("Hint: Summon your servants to defeat enemy!", True, (255, 0, 0)), (30, 30), (10, 10))
		self.playerStatus[0].init(self.statusFont.render("Player",                                  True, (255, 0, 0)), (100, 380), (10, 10))
		self.playerStatus[1].init(self.statusFont.render("kill:" + str(self.accounter.kill[0]),     True, (255, 0, 0)), (100, 410), (10, 10))
		self.playerStatus[2].init(self.statusFont.render("dead:" + str(self.accounter.death[0]),    True, (255, 0, 0)), (100, 440), (10, 10))
		self.playerStatus[3].init(self.statusFont.render("summon:" + str(self.accounter.summon[0]), True, (255, 0, 0)), (100, 470), (10, 10))
		self.playerStatus[4].init(self.statusFont.render("damage:" + str(self.accounter.damage[0]), True, (255, 0, 0)), (100, 500), (10, 10))
		self.enemyStatus[0].init(self.statusFont.render("Enemy",                                    True, (255, 0, 0)), (500, 380), (10, 10))
		self.enemyStatus[1].init(self.statusFont.render("kill:" + str(self.accounter.kill[1]),      True, (255, 0, 0)), (500, 410), (10, 10))
		self.enemyStatus[2].init(self.statusFont.render("dead:" + str(self.accounter.death[1]),     True, (255, 0, 0)), (500, 440), (10, 10))
		self.enemyStatus[3].init(self.statusFont.render("summon:" + str(self.accounter.summon[1]),  True, (255, 0, 0)), (500, 470), (10, 10))
		self.enemyStatus[4].init(self.statusFont.render("damage:" + str(self.accounter.damage[1]),  True, (255, 0, 0)), (500, 500), (10, 10))



		print(self.accounter.kill[0])
		print(self.accounter.death[0])
		print(self.accounter.summon[0])
		print(self.accounter.damage[0])



	def start(self):
		super().start()



	def update(self, events):
		super().update(events)
		for event in events:
			if event.type == pygame.QUIT:
				SceneManager.instance.switchScene(None)
			if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
				SceneManager.instance.switchScene(StartScene.StartScene())
				# SceneManager.instance.switchScene(NewBattleScene.NewBattleScene())



	def draw(self):
		super().draw()
		self.result.draw(self.screen)
		for p in self.playerStatus:
			p._drawProto(self.screen)
		for e in self.enemyStatus:
			e._drawProto(self.screen)



	def destroy(self):
		super().destroy()
		ResourceManager.instance.unload("Result")

