import pygame
import sys
import GameEntity
import GameObject
import CharacterUI
import BoardUI
from SceneBase import SceneBase

class BattleScene(SceneBase):
	def __init__(self):
		super().__init__()
		self.image = None
		self.movingObject = None
		# (index, pos, source)
		self.movingObjectInfo = None

		# testObject = GameObject.GameObject()

		self.cursorImage = None
		self.cursor = GameObject.GameObject()

		self.player1Hand = BoardUI.BoardUI()
		self.player2Hand = BoardUI.BoardUI()
		self.boardUI = BoardUI.BoardUI()

		self._cursorFocus = 0
		# 0 lost focus, 1 player1, 2 player2, 3 board

		self.dpos = None

	def init(self):
		super().init()
		self.image = pygame.image.load("crop.jpg")
		self.cursorImage = pygame.image.load("cursor.png")
		# self.player.init(self.image, (0, 0), (50, 50))
		self.cursor.init(self.cursorImage, (50, 50), (50, 50))
		# self.testObject.init(self.cursorImage, (700, 400), (60, 180))

		self.boardUI.init((100, 160), (10, 5), (60, 60))
		self.boardUI._generate(5)
		for (index, (pos, cUI)) in self.boardUI.characUIDict.items():
			cUI.init(self.image, self.boardUI.getPosOnScreen(pos), (50, 50))

		# player2 at the top
		self.player2Hand.init((40, 50), (12, 1), (60, 60))
		self.player2Hand._generate(5)
		for (index, (pos, cUI)) in self.player2Hand.characUIDict.items():
			cUI.init(self.image, self.player2Hand.getPosOnScreen(pos), (50, 50))

		# player1 at the bottom
		self.player1Hand.init((40, 500), (12, 1), (60, 60))
		self.player1Hand._generate(5)
		for (index, (pos, cUI)) in self.player1Hand.characUIDict.items():
			cUI.init(self.image, self.player1Hand.getPosOnScreen(pos), (50, 50))


	def start(self):
		super().start()
		# self.player.start()

	def update(self, events):
		super().update(events)

		for event in events:
			# print(event)
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
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


		# print(self.mousepos)
		# if self.isClick and not self.isDragging and //inRange//:

		# self.player.update()
		self.cursor.update()

	def draw(self):
		super().draw()
		# self.player.draw(self.screen)
		# 标号小的在前，能否daoxu遍历

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
