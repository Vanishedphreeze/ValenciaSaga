import pygame
import sys
import GameEntity
import ResourceManager
import SceneManager
import EventManager
import BattleAIManager
import GameObject
import CharacterUI
import BoardUI
import PlayerUI
import BattleCore
import BattleStatus
import RangeIndicator
import StartScene
import MoveTutorialScene
from SceneBase import SceneBase

class AttackTutorialScene(SceneBase):
	def __init__(self):
		super().__init__()
		self.image = None
		self.movingObject = None

		# (index, pos, source)
		# index: index in hand/characDict
		# pos: original pos on screen
		# source is the same as _cursorFocus
		# 1 player1, 2 player2, 3 board
		self.movingObjectInfo = None

		self.status = None

		# testObject = GameObject.GameObject()

		self.cursorImage = None
		self.cursor = GameObject.GameObject()

		self.player1Hand = PlayerUI.PlayerUI()
		self.player2Hand = PlayerUI.PlayerUI()
		self.boardUI = BoardUI.BoardUI()
		self.indicator = RangeIndicator.RangeIndicator()

		self._cursorFocus = 0
		# 0 lost focus, 1 player1, 2 player2, 3 board

		self.waitForAttackOpt = False
		self.waitForAttackCharacPos = None
		self.waitForAttackCharacRange = None
		self.bufferOpt = None
		self.bufferCharac = None

		dpos = None

		self.battleBg = GameObject.GameObject()

		self.attackHint = GameObject.GameObject()
		self.attackHintCursor1 = GameObject.GameObject()
		self.attackHintCursor2 = GameObject.GameObject()
		self.skipButton = GameObject.GameObject()

		self.isInWaitState = False
		self.waitCnt = 90



	def init(self):
		super().init()

		# load resources
		ResourceManager.instance.load("MainCharacTemplet", "json", "MainCharacterTemplet.json")
		ResourceManager.instance.load("CharacTemplet", "json", "CharacterTemplet.json")
		ResourceManager.instance.load("archer0", "image", "archer0.png")
		ResourceManager.instance.load("archer1", "image", "archer1.png")
		ResourceManager.instance.load("athos0", "image", "athos0.png")
		ResourceManager.instance.load("athos1", "image", "athos1.png")
		ResourceManager.instance.load("berserker0", "image", "berserker0.png")
		ResourceManager.instance.load("berserker1", "image", "berserker1.png")
		ResourceManager.instance.load("cavalier0", "image", "cavalier0.png")
		ResourceManager.instance.load("cavalier1", "image", "cavalier1.png")
		ResourceManager.instance.load("knight0", "image", "knight0.png")
		ResourceManager.instance.load("knight1", "image", "knight1.png")

		ResourceManager.instance.load("red", "image", "red.png")
		ResourceManager.instance.load("blue", "image", "blue.png")

		ResourceManager.instance.load("AttackHint1", "image", "Hint_Move.png")
		ResourceManager.instance.load("AttackHint2", "image", "Hint_Attack.png")
		ResourceManager.instance.load("HintCursor1", "image", "HintCursor1.png")
		ResourceManager.instance.load("HintCursor2", "image", "HintCursor2.png")
		ResourceManager.instance.load("Good", "image", "good.png")
		ResourceManager.instance.load("Skip", "image", "Skip.png")

		ResourceManager.instance.load("BattleBg", "image", "BattleBg.png")

		self.battleBg.init(ResourceManager.instance.getResourceHandler("BattleBg"), (0, 0), (800, 600))

		self.statusFont = pygame.font.Font(None, 30)

		BattleCore.instance.init()
		self.status = BattleCore.instance.getBattleStatusHandler()
		if not isinstance(self.status, BattleStatus.BattleStatus):
			print("UIlayer: BattleStatus type wrong")

		self.image = pygame.image.load("crop.jpg")
		self.cursorImage = pygame.image.load("cursor.png")

		self.cursor.init(self.cursorImage, (50, 50), (50, 50))
		self.boardUI.init((100, 160), (60, 60), self.status.board)

		# player2 at the top
		self.player2Hand.init((40, 50), (60, 60), self.status.playerList[1])

		# player1 at the bottom
		self.player1Hand.init((40, 500), (60, 60), self.status.playerList[0])

		# player 0 / player 
		self.indicator.init(self.status.board, self.status.playerList[0], self.boardUI)

		# attack hint
		self.attackHint.init(ResourceManager.instance.getResourceHandler("AttackHint1"), (357, 253), (306, 110)) 
		self.attackHintCursor1.init(ResourceManager.instance.getResourceHandler("HintCursor1"), (421, 362), (28, 35))
		self.attackHintCursor2.init(ResourceManager.instance.getResourceHandler("HintCursor2"), (305, 310), (19, 30))
		self.skipButton.init(ResourceManager.instance.getResourceHandler("Skip"), (700, 0), (100, 50))





	def start(self):
		super().start()
		BattleCore.instance.start()

		self.boardUI.update()
		self.player1Hand.update()
		self.player2Hand.update()


		self.indicator.displayMode = 3

		BattleCore.instance.loadStatus("AttackTutorialData.txt")

		self.indicator.setFocus((2, 3), self.status.board.getCharacByPos((2, 3)))

		self.boardUI.update()
		self.player1Hand.update()
		self.player2Hand.update()



	def update(self, events):
		super().update(events)

		if self.isInWaitState:
			for event in events:
				if event.type == pygame.QUIT:
					SceneManager.instance.switchScene(None)
			self.waitCnt -= 1
			if self.waitCnt <= 0:
				print("Good")
				SceneManager.instance.switchScene(MoveTutorialScene.MoveTutorialScene())
			return None

		if self.waitForAttackOpt:
			self.attackHint.position = (417, 253)[:]
			self.attackHintCursor1.position = (481, 362)[:]
			self.attackHintCursor2.position = (800, 600)[:]
			self.attackHint.changeAvatar(ResourceManager.instance.getResourceHandler("AttackHint2"))

		for event in events:
			if event.type == pygame.QUIT:
				SceneManager.instance.switchScene(None)

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 2: 
					pass

				if event.button == 1 and not self.waitForAttackOpt: # left button
					if self.skipButton.pointCollide(event.pos):
						SceneManager.instance.switchScene(StartScene.StartScene())


					for (index, (pos, cUI)) in self.boardUI.characUIDict.items():
						if cUI.pointCollide(event.pos):
							if cUI.owner == 0 and cUI.state == 0:
								self.movingObject = cUI
								self.movingObjectInfo = (index, pos, 3)
								self.dpos = [event.pos[0] - self.movingObject.position[0], event.pos[1] - self.movingObject.position[1]]
								self.bufferCharac = self.status.board.getCharacByPos((pos[1], pos[0]))
							self.indicator.setFocus((pos[1], pos[0]), self.status.board.getCharacByPos((pos[1], pos[0])))
							self.indicator.displayMode = 3
							break


			if event.type == pygame.MOUSEMOTION:
				# print(self.boardUI.getPosOnBoard(event.pos))
				if self.player1Hand.isPosOnBoard(event.pos):
					self._cursorFocus = 1
				elif self.player2Hand.isPosOnBoard(event.pos):
					self._cursorFocus = 2
				elif self.boardUI.isPosOnBoard(event.pos):
					self._cursorFocus = 3
				else:
					self._cursorFocus = 0 
				# print(self._cursorFocus)

				if self._cursorFocus == 1:
					self.cursor.position = list(self.player1Hand.getPosOnScreen(self.player1Hand.getPosOnBoard(event.pos)))
				elif self._cursorFocus == 2:
					self.cursor.position = list(self.player2Hand.getPosOnScreen(self.player2Hand.getPosOnBoard(event.pos)))
				elif self._cursorFocus == 3:
					self.cursor.position = list(self.boardUI.getPosOnScreen(self.boardUI.getPosOnBoard(event.pos)))
				else:
					pass

				# self.cursor.position = list(self.boardUI.getPosOnScreen(self.boardUI.getPosOnBoard(event.pos)))
				if self.movingObject != None and event.buttons[0] == 1:
					self.movingObject.position[0] = event.pos[0] - self.dpos[0]
					self.movingObject.position[1] = event.pos[1] - self.dpos[1]

			if event.type == pygame.MOUSEBUTTONUP:
				self.indicator.displayMode = 0
				#####################################################################################################################################################################
				# self.indicator.setFocus(*self.status.board.characDict[0])
				#####################################################################################################################################################################
				if event.button == 3: # right button
					if self.waitForAttackOpt:
						print("attack cancelled")
						self.boardUI.update()
						# self.player1Hand.update()
						# self.player2Hand.update()
						self.indicator.displayMode = 0
						self.waitForAttackOpt = False

				if event.button == 1: # left button
					# operation test here
					# if this opt is not legal, undo.
					# else, update boardUI, etc.

					if self.waitForAttackOpt:
						UIpos = self.waitForAttackCharacPos
						UItargetPos = self.boardUI.getPosOnBoard(event.pos)
						dist = abs(UItargetPos[0] - UIpos[0]) + abs(UItargetPos[1] - UIpos[1])
						if UItargetPos[0] == UIpos[0] and UItargetPos[1] == UIpos[1]:
							print("only move is banned") 
							# BattleCore.instance.pushForward(self.bufferOpt)
							self.boardUI.update()
							# self.player1Hand.update()
							# self.player2Hand.update()

						elif self.status.board.getCharacByPos((UItargetPos[1], UItargetPos[0])) != None and dist <= self.waitForAttackCharacRange and UItargetPos[1] == 3 and UItargetPos[0] == 6:
							print("attack")
							# attack(pos, targetPos)
							BattleCore.instance.pushForward(self.bufferOpt)
							BattleCore.instance.pushForward( (2, ( (UIpos[1], UIpos[0]), (UItargetPos[1], UItargetPos[0]) ) ) )


							# print("//////////////////////////\nAttcker:")
							# BattleCore.instance.showStatusAtPos((UIpos[1], UIpos[0]))
							# print("//////////////////////////\nDefender:")
							# BattleCore.instance.showStatusAtPos((UItargetPos[1], UItargetPos[0]))
							# print("//////////////////////////")


							self.boardUI.update()
							self.attackHint.changeAvatar(ResourceManager.instance.getResourceHandler("Good"))
							self.isInWaitState = True
							# self.player1Hand.update()
							# self.player2Hand.update()
						else:
							print("attack cancelled")
							self.boardUI.update()
							# self.player1Hand.update()
							# self.player2Hand.update()

						self.indicator.displayMode = 0
						self.waitForAttackOpt = False

					elif self.movingObject != None:
						if self.movingObjectInfo[2] == 3: # boardUI
							if self._cursorFocus == 3: # board: move / attack
								# only move now
								UIpos = self.movingObjectInfo[1]
								UItargetPos = self.boardUI.getPosOnBoard(event.pos)

								if UIpos[0] == UItargetPos[0] and UIpos[1] == UItargetPos[1]:
									print("only attack without move")
									self.movingObject.position = list(self.boardUI.getPosOnScreen(self.movingObjectInfo[1])[:])

									self.bufferOpt = (1, ( (UIpos[1], UIpos[0]), (UItargetPos[1], UItargetPos[0]) ) )
									self.movingObject.position = list(self.boardUI.getPosOnScreen(UItargetPos)[:])
									# self.boardUI.update()
									# self.player1Hand.update()
									# self.player2Hand.update()

									# when moved wait for attack opt.
									self.waitForAttackOpt = True
									self.waitForAttackCharacPos = UItargetPos
									self.waitForAttackCharacRange = self.status.board.getCharacByPos((UIpos[1], UIpos[0])[:]).status["RNG"]

									# 注意这里如果换成不push，要保存charac信息。
									self.indicator.setFocus((UItargetPos[1], UItargetPos[0]), self.bufferCharac)
									self.indicator.displayMode = 2



								elif self.boardUI.boardUI[UItargetPos[0]][UItargetPos[1]] != -1: # do nothing
									self.movingObject.position = list(self.boardUI.getPosOnScreen(self.movingObjectInfo[1])[:])
									pass

								else:
									print("move")
									# move(pos, targetPos)

									# 在这里不要pushforward，把操作存起来，之后一起push。注意判断移动合法性
									if (UItargetPos[1], UItargetPos[0]) in self.indicator.reachable:
										self.bufferOpt = (1, ( (UIpos[1], UIpos[0]), (UItargetPos[1], UItargetPos[0]) ) )
										self.movingObject.position = list(self.boardUI.getPosOnScreen(UItargetPos)[:])
										# self.boardUI.update()
										# self.player1Hand.update()
										# self.player2Hand.update()

										# when moved wait for attack opt.
										self.waitForAttackOpt = True
										self.waitForAttackCharacPos = UItargetPos
										self.waitForAttackCharacRange = self.status.board.getCharacByPos((UIpos[1], UIpos[0])[:]).status["RNG"]

										# 注意这里如果换成不push，要保存charac信息。
										self.indicator.setFocus((UItargetPos[1], UItargetPos[0]), self.bufferCharac)
										self.indicator.displayMode = 2
									else:
										print("move out of range or cancelled")
										self.movingObject.position = list(self.boardUI.getPosOnScreen(self.movingObjectInfo[1])[:])

							else: # illegal
								print("UIlayer: illegal operation")
								self.movingObject.position = list(self.boardUI.getPosOnScreen(self.movingObjectInfo[1])[:])

						self.movingObject = None
						self.movingObjectInfo = None

		# self.player.update()
		for (index, (pos, cUI)) in self.boardUI.characUIDict.items():
			cUI.update()

		for (index, (pos, cUI)) in self.player2Hand.characUIDict.items():
			cUI.update()

		for (index, (pos, cUI)) in self.player1Hand.characUIDict.items():
			cUI.update()

		self.cursor.update()



	def draw(self):
		super().draw()
		# dict uses hash table. this could not control the sequence of rendering
		self.battleBg.draw(self.screen)

		self.indicator.draw(self.screen)

		for (index, (pos, cUI)) in self.boardUI.characUIDict.items():
			cUI.draw(self.screen)

		for (index, (pos, cUI)) in self.player2Hand.characUIDict.items():
			cUI.draw(self.screen)

		for (index, (pos, cUI)) in self.player1Hand.characUIDict.items():
			cUI.draw(self.screen)

		self.attackHint.draw(self.screen)
		self.skipButton.draw(self.screen)
		self.attackHintCursor1.draw(self.screen)
		self.attackHintCursor2.draw(self.screen)

		# self.cursor.draw(self.screen)



	def destroy(self):
		super().destroy()
		# self.player.destroy()
		self.cursor.destroy()
		ResourceManager.instance.unload("MainCharacTemplet")
		ResourceManager.instance.unload("CharacTemplet")
		ResourceManager.instance.unload("archer0")
		ResourceManager.instance.unload("archer1")
		ResourceManager.instance.unload("athos0")
		ResourceManager.instance.unload("athos1")
		ResourceManager.instance.unload("berserker0")
		ResourceManager.instance.unload("berserker1")
		ResourceManager.instance.unload("cavalier0")
		ResourceManager.instance.unload("cavalier1")
		ResourceManager.instance.unload("knight0")
		ResourceManager.instance.unload("knight1")

		ResourceManager.instance.unload("red")
		ResourceManager.instance.unload("blue")

		ResourceManager.instance.unload("AttackHint1")
		ResourceManager.instance.unload("AttackHint2")
		ResourceManager.instance.unload("HintCursor1")
		ResourceManager.instance.unload("HintCursor2")
		ResourceManager.instance.unload("Good")
		ResourceManager.instance.unload("Skip")

		ResourceManager.instance.unload("BattleBg")
