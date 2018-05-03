import pygame
import sys
import GameEntity
import GameObject
import CharacterUI
import BoardUI
from SceneBase import SceneBase

class TestScene(SceneBase):
	def __init__(self):
		super().__init__()
		self.image = None
		self.characterUIPool = [CharacterUI.CharacterUI() for i in range(10)]
		self.movingObject = None

		self.cursorImage = None
		self.cursor = GameObject.GameObject()

		self.boardUI = BoardUI.BoardUI()

		self.dpos = None

	def init(self):
		super().init()
		self.image = pygame.image.load("crop.jpg")
		self.cursorImage = pygame.image.load("cursor.png")
		# self.player.init(self.image, (0, 0), (50, 50))
		for cUI in self.characterUIPool:
			cUI.init(self.image, (0, 0), (50, 50))
		self.cursor.init(self.cursorImage, (50, 50), (50, 50))
		self.boardUI.init((60, 60), (5, 5), (100, 100))

	def start(self):
		super().start()
		# self.player.start()
		for cUI in self.characterUIPool:
			cUI.start()

	def update(self, events):
		super().update(events)

		for event in events:
			# print(event)
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: # left button
					for cUI in self.characterUIPool:
						if cUI.pointCollide(event.pos):
							self.movingObject = cUI
							self.dpos = [event.pos[0] - self.movingObject.position[0], event.pos[1] - self.movingObject.position[1]]
							break

			if event.type == pygame.MOUSEMOTION:
				print(self.boardUI.getPosOnBoard(event.pos))
				self.cursor.position = list(self.boardUI.getPosOnScreen(self.boardUI.getPosOnBoard(event.pos)))
				if self.movingObject != None and event.buttons[0] == 1:
					self.movingObject.position[0] = event.pos[0] - self.dpos[0]
					self.movingObject.position[1] = event.pos[1] - self.dpos[1]

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1: # left button
					# operation test here
					# if this opt is not legal, undo.
					# else, update boardUI, etc.
					self.movingObject = None


		# print(self.mousepos)
		# if self.isClick and not self.isDragging and //inRange//:

		# self.player.update()
		for cUI in self.characterUIPool:
			cUI.update()
		self.cursor.update()

	def draw(self):
		super().draw()
		# self.player.draw(self.screen)
		# 标号小的在前，能否daoxu遍历
		for cUI in self.characterUIPool:
			cUI.draw(self.screen)
		self.cursor.draw(self.screen)

	def destroy(self):
		super().destroy()
		# self.player.destroy()
		for cUI in self.characterUIPool:
			cUI.destroy()
		self.cursor.destroy()
