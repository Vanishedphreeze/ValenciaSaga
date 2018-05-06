import random
import GameObject
import CharacterUI
import Player
import pygame

class PlayerUI(object):
	def __init__(self):
		self.handImage = None
		self.startPos = None
		self._endPos = None
		self.size = None # n * m
		self.step = None

		self.boardUI = None
	    # index : (pos, character)
		self.characUIDict = None

		self.logicPlayerHandler = None

	# intend to pass value

	# in render/input pos is Horizontal - Vertical, (800, 600)
	# but in logic, pos is Vertical - Horizontal, (5, 10)
	# all positions in UI layer is same to pygame renderer.
	# to pass opts / get info with logic, reverse the postion, board, etc.

	'''
	def obsoluted_init(self, startPos, size, step):
		
		# self.startPos = (startPos[0], startPos[1])
		# self.size = (size[0], size[1])
		# self.step = (step[0], step[1])

		self.startPos = tuple(startPos[:])
		self.size = tuple(size[:])
		self.step = tuple(step[:])
		self.boardUI = [[-1 for i in range(size[1])] for i in range(size[0])]
		self.characUIDict = {}
		self._endPos = self.startPos[0] + size[0] * step[0], self.startPos[1] + size[1] * step[1]
	'''



	def init(self, startPos, step, logicPlayerHandler):
		self.handImage = pygame.image.load("crop.jpg")

		self.logicPlayerHandler = logicPlayerHandler
		if not isinstance(self.logicPlayerHandler, Player.Player):
			print("UIlayer: Player type wrong")

		self.startPos = tuple(startPos[:])
		self.size = (Player.Player.MAXHAND, 1)
		self.step = tuple(step[:])
		self.boardUI = [[-1 for i in range(self.size[1])] for i in range(self.size[0])]
		self.characUIDict = {}
		self._endPos = self.startPos[0] + self.size[0] * step[0], self.startPos[1] + self.size[1] * step[1]
		


	def getPosOnBoard(self, mousePos):
		x = int((mousePos[0] - self.startPos[0]) / self.step[0])
		y = int((mousePos[1] - self.startPos[1]) / self.step[1])

		if x >= self.size[0]:
			x = self.size[0] - 1
		elif x < 0:
			x = 0

		if y >= self.size[1]:
			y = self.size[1] - 1 
		elif y < 0:
			y = 0

		return (x, y)



	def getPosOnScreen(self, pos):
		x = pos[0] * self.step[0] + self.startPos[0]
		y = pos[1] * self.step[1] + self.startPos[1]
		return (x, y)



	def moveCharac(self, pos, targetPos):
		if targetPos[0] < 0 or targetPos[0] >= self.size[0] or targetPos[1] < 0 or targetPos[1] >= self.size[1]:
			print("Move out from board.")
			return False

		if self.boardUI[targetPos[0]][targetPos[1]] == -1:
			self.characUIDict[self.boardUI[pos[0]][pos[1]]][0] = targetPos[:]
			self.boardUI[targetPos[0]][targetPos[1]] = self.boardUI[pos[0]][pos[1]]
			self.boardUI[pos[0]][pos[1]] = -1
		else:
			print("illegal move.")
			return False

		return True



	def isPosOnBoard(self, pos):
		return pos[0] in range(self.startPos[0], self._endPos[0]) and pos[1] in range(self.startPos[1], self._endPos[1])



	'''
	# this func doesn't check n!
	def _generate(self, n):
		cnt = 0
		while cnt < n :
			pos = random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)
			if self.boardUI[pos[0]][pos[1]] == -1:
				self.boardUI[pos[0]][pos[1]] = cnt
				self.characUIDict[cnt] = [pos[:], CharacterUI.CharacterUI()]
				cnt += 1
				# print(pos)
	'''



	# ensure that the index in logic is the same in UI  
	# this is not the best solution, optimize it if necessary
	def update(self):
		for i in range(self.size[0]):
			self.boardUI[i][0] = -1
		for i in range(len(self.logicPlayerHandler.hand)):
			self.boardUI[i][0] = self.logicPlayerHandler.hand[i]

		self.characUIDict = {}
		# use CharacterUI pool if necessary
		for i in range(len(self.logicPlayerHandler.hand)):
			self.characUIDict[i] = [(i, 0), CharacterUI.CharacterUI()]
			self.characUIDict[i][1].init(self.logicPlayerHandler.hand[i].type, self.logicPlayerHandler.hand[i].owner, self.getPosOnScreen((i, 0)), (50, 50))
			self.characUIDict[i][1].setStatus(self.logicPlayerHandler.hand[i].status["ATK"], self.logicPlayerHandler.hand[i].status["HP"])


