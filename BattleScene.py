import pygame
import sys
import GameEntity
import ResourceManager
import GameObject
import CharacterUI
import BoardUI
import PlayerUI
import BattleCore
import BattleStatus
from SceneBase import SceneBase

class BattleScene(SceneBase):
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

		self._cursorFocus = 0
		# 0 lost focus, 1 player1, 2 player2, 3 board

		dpos = None



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

		self.statusFont = pygame.font.Font(None, 30)

		BattleCore.instance.init()
		self.status = BattleCore.instance.getBattleStatusHandler()
		if not isinstance(self.status, BattleStatus.BattleStatus):
			print("UIlayer: BattleStatus type wrong")

		self.image = pygame.image.load("crop.jpg")
		self.cursorImage = pygame.image.load("cursor.png")
		# self.cursorImage = ResourceManager.instance.getResourceHandler("EliwoodImage")
		# self.player.init(self.image, (0, 0), (50, 50))
		self.cursor.init(self.cursorImage, (50, 50), (50, 50))
		# self.testObject.init(self.cursorImage, (700, 400), (60, 180))

		# self.boardUI.obsoluted_init((100, 160), (10, 5), (60, 60))
		self.boardUI.init((100, 160), (60, 60), self.status.board)
		# self.boardUI._generate(5)
		# for (index, (pos, cUI)) in self.boardUI.characUIDict.items():
		# 	cUI.init(self.image, self.boardUI.getPosOnScreen(pos), (50, 50))

		# player2 at the top
		# self.player2Hand.obsoluted_init((40, 50), (12, 1), (60, 60))
		self.player2Hand.init((40, 50), (60, 60), self.status.playerList[1])
		# self.player2Hand._generate(5)
		# for (index, (pos, cUI)) in self.player2Hand.characUIDict.items():
		# 	cUI.init(self.image, self.player2Hand.getPosOnScreen(pos), (50, 50))

		# player1 at the bottom
		# self.player1Hand.obsoluted_init((40, 500), (12, 1), (60, 60))
		self.player1Hand.init((40, 500), (60, 60), self.status.playerList[0])
		# self.player1Hand._generate(5)
		# for (index, (pos, cUI)) in self.player1Hand.characUIDict.items():
		# 	cUI.init(self.image, self.player1Hand.getPosOnScreen(pos), (50, 50))



	def start(self):
		super().start()
		BattleCore.instance.start()

		# this is only for test.
		# BattleCore.instance.pushForward( (0, (0, 0, (2, 2) ) ) )
		# BattleCore.instance.pushForward( (0, (0, 0, (1, 2) ) ) )
		# BattleCore.instance.pushForward( (0, (0, 0, (2, 3) ) ) )

		self.boardUI.update()
		self.player1Hand.update()
		self.player2Hand.update()
		# self.player.start()



	def update(self, events):
		super().update(events)

		for event in events:
			# print(event)
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:

				# right click to end the turn, use other UI later
				if event.button == 2: 
					BattleCore.instance.pushForward((-1, ))
					self.boardUI.update()
					self.player1Hand.update()
					self.player2Hand.update()

				if event.button == 1: # left button
					for (index, (pos, cUI)) in self.player1Hand.characUIDict.items():
						if cUI.pointCollide(event.pos):
							self.movingObject = cUI
							self.movingObjectInfo = (index, pos, 1)
							self.dpos = [event.pos[0] - self.movingObject.position[0], event.pos[1] - self.movingObject.position[1]]
							break

					if self.movingObject == None:
						for (index, (pos, cUI)) in self.player2Hand.characUIDict.items():
							if cUI.pointCollide(event.pos):
								self.movingObject = cUI
								self.movingObjectInfo = (index, pos, 2)
								self.dpos = [event.pos[0] - self.movingObject.position[0], event.pos[1] - self.movingObject.position[1]]
								break

					if self.movingObject == None:
						for (index, (pos, cUI)) in self.boardUI.characUIDict.items():
							if cUI.pointCollide(event.pos):
								self.movingObject = cUI
								self.movingObjectInfo = (index, pos, 3)
								self.dpos = [event.pos[0] - self.movingObject.position[0], event.pos[1] - self.movingObject.position[1]]
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
				if event.button == 1 and self.movingObject != None: # left button
					# operation test here
					# if this opt is not legal, undo.
					# else, update boardUI, etc.

					'''
					if self.movingObjectInfo[2] == 1: # player1Hand
						self.movingObject.position = list(self.player1Hand.getPosOnScreen(self.movingObjectInfo[1])[:])
					elif self.movingObjectInfo[2] == 2: # player2Hand
						self.movingObject.position = list(self.player2Hand.getPosOnScreen(self.movingObjectInfo[1])[:])
					elif self.movingObjectInfo[2] == 3: # boardUI
						self.movingObject.position = list(self.boardUI.getPosOnScreen(self.movingObjectInfo[1])[:])
					'''

					'''
					if self.movingObjectInfo[2] == 1: # player1Hand
						if self._cursorFocus == 3: # board: summon
							# only for test
							print("summon from player1")
							self.movingObject.position = list(self.player1Hand.getPosOnScreen(self.movingObjectInfo[1])[:])
						else: # illegal
							print("UIlayer: illegal operation")
							self.movingObject.position = list(self.player1Hand.getPosOnScreen(self.movingObjectInfo[1])[:])

					elif self.movingObjectInfo[2] == 2: # player2Hand
						if self._cursorFocus == 3: # board: summon
							# only for test
							print("summon from player2")
							self.movingObject.position = list(self.player2Hand.getPosOnScreen(self.movingObjectInfo[1])[:])
						else: # illegal
							print("UIlayer: illegal operation")
							self.movingObject.position = list(self.player2Hand.getPosOnScreen(self.movingObjectInfo[1])[:])

					elif self.movingObjectInfo[2] == 3: # boardUI
						if self._cursorFocus == 3: # board: move / attack
							print("move / attack")
							self.movingObject.position = list(self.boardUI.getPosOnScreen(self.movingObjectInfo[1])[:])
						else: # illegal
							print("UIlayer: illegal operation")
							self.movingObject.position = list(self.boardUI.getPosOnScreen(self.movingObjectInfo[1])[:])
					'''

					if self.movingObjectInfo[2] == 1: # player1Hand
						if self._cursorFocus == 3: # board: summon
							# summon(playerNo, handIndex, posOnBoard)
							print("summon from player1")
							UIpos = self.boardUI.getPosOnBoard(event.pos)
							BattleCore.instance.pushForward( (0, (0, self.movingObjectInfo[0],  (UIpos[1], UIpos[0]) ) ) )
							self.boardUI.update()
							self.player1Hand.update()
							# self.player2Hand.update()
						else: # illegal
							print("UIlayer: illegal operation")
							self.movingObject.position = list(self.player1Hand.getPosOnScreen(self.movingObjectInfo[1])[:])

					elif self.movingObjectInfo[2] == 2: # player2Hand
						if self._cursorFocus == 3: # board: summon
							# summon(playerNo, handIndex, posOnBoard)
							print("summon from player2")
							UIpos = self.boardUI.getPosOnBoard(event.pos)
							BattleCore.instance.pushForward( (0, (1, self.movingObjectInfo[0], (UIpos[1], UIpos[0]) ) ) )
							self.boardUI.update()
							# self.player1Hand.update()
							self.player2Hand.update()

						else: # illegal
							print("UIlayer: illegal operation")
							self.movingObject.position = list(self.player2Hand.getPosOnScreen(self.movingObjectInfo[1])[:])

					elif self.movingObjectInfo[2] == 3: # boardUI
						if self._cursorFocus == 3: # board: move / attack
							# only move now
							UIpos = self.movingObjectInfo[1]
							UItargetPos = self.boardUI.getPosOnBoard(event.pos)

							if UIpos[0] == UItargetPos[0] and UIpos[1] == UItargetPos[1]:
								print("move / attack cancelled")
								self.movingObject.position = list(self.boardUI.getPosOnScreen(self.movingObjectInfo[1])[:])

							elif self.boardUI.boardUI[UItargetPos[0]][UItargetPos[1]] != -1:
								print("attack")
								# attack(pos, targetPos)
								BattleCore.instance.pushForward( (2, ( (UIpos[1], UIpos[0]), (UItargetPos[1], UItargetPos[0]) ) ) )
								print("//////////////////////////\nAttcker:")
								BattleCore.instance.showStatusAtPos((UIpos[1], UIpos[0]))
								print("//////////////////////////\nDefender:")
								BattleCore.instance.showStatusAtPos((UItargetPos[1], UItargetPos[0]))
								print("//////////////////////////")
								self.boardUI.update()
								# self.player1Hand.update()
								# self.player2Hand.update()
							else :
								print("move")
								# move(pos, targetPos)
								BattleCore.instance.pushForward( (1, ( (UIpos[1], UIpos[0]), (UItargetPos[1], UItargetPos[0]) ) ) )
								self.boardUI.update()
								# self.player1Hand.update()
								# self.player2Hand.update()

						else: # illegal
							print("UIlayer: illegal operation")
							self.movingObject.position = list(self.boardUI.getPosOnScreen(self.movingObjectInfo[1])[:])

					# used when single
					'''
					tempPosOnBoard = self.boardUI.getPosOnBoard(event.pos)

					# if there is a character in this pos
					if self.boardUI.boardUI[tempPosOnBoard[0]][tempPosOnBoard[1]] != -1:
						# temporarily no change. add battle here
						self.movingObject.position = list(self.boardUI.getPosOnScreen(self.movingObjectInfo[1])[:])
					else :
						# move, add judges later
						self.boardUI.moveCharac(self.movingObjectInfo[1], tempPosOnBoard)
						# get characterUI info form dict by using Index.
						self.movingObject.position = list(self.boardUI.getPosOnScreen(self.boardUI.characUIDict[self.movingObjectInfo[0]][0][:]))
					'''

					self.movingObject = None
					self.movingObjectInfo = None


		# print(self.mousepos)
		# if self.isClick and not self.isDragging and //inRange//:

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
		# self.player.draw(self.screen)
		# dict uses hash table. this could not control the sequence of rendering

		for (index, (pos, cUI)) in self.boardUI.characUIDict.items():
			cUI.draw(self.screen)

		for (index, (pos, cUI)) in self.player2Hand.characUIDict.items():
			cUI.draw(self.screen)

		for (index, (pos, cUI)) in self.player1Hand.characUIDict.items():
			cUI.draw(self.screen)

		self.cursor.draw(self.screen)
		# self.testObject.draw(self.screen)



	def destroy(self):
		super().destroy()
		# self.player.destroy()
		self.cursor.destroy()
