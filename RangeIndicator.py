import Board
import Player
import GameObject
import ResourceManager
from queue import Queue

class RangeIndicator(object):
	# used by function update
	dx = (1, -1, 0, 0, 1, 1, -1, -1, 2, 0, -2, 0)
	dy = (0, 0, 1, -1, -1, 1, 1, -1, 0, 2, 0, -2)


	def __init__(self):
		self.boardHandler = None
		
		# only one player because only one player will use this.
		self.playerHandler = None

		# 0: not display, 1: only move, 2: only attack, 3: attack + move, 4 summon
		self.displayMode = None

		# set of pos that reachable. this is in logic sequence, row first.
		self.reachable = None

		# set of pos that ONLY could be reached by attack.
		# if you want to show displayMode == 2, just use dx and dy.
		self.attackable = None

		# (pos, charac), the center of the Indicator
		self.focus = None

        # pool of game object. the size is same as board
		# [[-1 for i in range(self.size[1])] for i in range(self.size[0])]
		self.boardUIHandler = None
		self.reachIndicatorPool = None
		self.attackIndicatorPool = None



	def init(self, boardHandler, playerHandler, boardUIHandler):
		self.boardHandler = boardHandler
		self.playerHandler = playerHandler
		self.boardUIHandler = boardUIHandler
		self.displayMode = 0
		self.reachable = set()
		self.attackable = set()
		self.focus = None
		self.reachIndicatorPool = [[GameObject.GameObject() for i in range(self.boardUIHandler.size[1])] for i in range(self.boardUIHandler.size[0])]
		self.attackIndicatorPool = [[GameObject.GameObject() for i in range(self.boardUIHandler.size[1])] for i in range(self.boardUIHandler.size[0])]

		redimage = ResourceManager.instance.getResourceHandler("red")
		blueimage = ResourceManager.instance.getResourceHandler("blue")

		for i in range(self.boardUIHandler.size[0]):
			for j in range(self.boardUIHandler.size[1]):
				self.reachIndicatorPool[i][j].init(blueimage, self.boardUIHandler.getPosOnScreen((i, j)), (50, 50))
				self.attackIndicatorPool[i][j].init(redimage, self.boardUIHandler.getPosOnScreen((i, j)), (50, 50))



	# Especially, this function should be called after you moved character.
	def setFocus(self, pos, charac):
		self.focus = (pos, charac)
		self.update()



	# this function is no need to be called every frame. 
	def update(self):
		pos = self.focus[0]
		charac = self.focus[1]

		q = Queue()
		self.reachable = set()
		self.attackable = set()

		# find attackable blocks before move
		r = 0
		if charac.status["RNG"] == 1:
			r = 4
		elif charac.status["RNG"] == 2:
			r = 12
		else:
			print("UI Layer: Can't process range larger than 2")

		for j in range(r):
			nextPos = (pos[0] + RangeIndicator.dx[j], pos[1] + RangeIndicator.dy[j])
			if nextPos[0] < 0 or nextPos[0] >= Board.Board.HEIGHT or nextPos[1] < 0 or nextPos[1] >= Board.Board.WIDTH:
				continue
			self.attackable.add(nextPos)


		# pos, stepleft
		q.put((tuple(pos), charac.status["MOV"]))
		self.reachable.add(tuple(pos))


		while not q.empty():
			curPos, curStepLeft = q.get()

			# find attackable blocks 
			r = 0
			if charac.status["RNG"] == 1:
				r = 4
			elif charac.status["RNG"] == 2:
				r = 12
			else:
				print("UI Layer: Can't process range larger than 2")

			for j in range(r):
				nextPos = (curPos[0] + RangeIndicator.dx[j], curPos[1] + RangeIndicator.dy[j])
				if nextPos[0] < 0 or nextPos[0] >= Board.Board.HEIGHT or nextPos[1] < 0 or nextPos[1] >= Board.Board.WIDTH:
					continue
				self.attackable.add(nextPos)


			# if no step left, do nothing. else go
			if curStepLeft == 0:
				continue


			for j in range(4):
				nextPos = (curPos[0] + RangeIndicator.dx[j], curPos[1] + RangeIndicator.dy[j])
				if nextPos[0] < 0 or nextPos[0] >= Board.Board.HEIGHT or nextPos[1] < 0 or nextPos[1] >= Board.Board.WIDTH:
					continue
				if nextPos in self.reachable:
					continue
				nextPosCharac = self.boardHandler.getCharacByPos(nextPos)
				if nextPosCharac == None or nextPosCharac.owner == charac.owner:
					q.put((nextPos, curStepLeft - 1))
					self.reachable.add(nextPos)


		####################### bfs end.

		self.attackable = self.attackable - self.reachable
		# print("attackable: ")
		# print(self.attackable)
		# print("\nreachable: ")
		# print(self.reachable)


	def draw(self, screen):
		# 0: not display, 1: only move, 2: only attack, 3: attack + move
		# self.displayMode = None

		if self.displayMode == 1:
			for (x, y) in self.reachable:
				self.reachIndicatorPool[y][x].draw(screen)
		elif self.displayMode == 2:
			pos = self.focus[0]
			charac = self.focus[1]
			r = 0
			if charac.status["RNG"] == 1:
				r = 4
			elif charac.status["RNG"] == 2:
				r = 12
			else:
				print("UI Layer: Can't process range larger than 2")

			for j in range(r):
				nextPos = (pos[0] + RangeIndicator.dx[j], pos[1] + RangeIndicator.dy[j])
				if nextPos[0] < 0 or nextPos[0] >= Board.Board.HEIGHT or nextPos[1] < 0 or nextPos[1] >= Board.Board.WIDTH:
					continue
				self.attackIndicatorPool[nextPos[1]][nextPos[0]].draw(screen)

		elif self.displayMode == 3:
			for (x, y) in self.reachable:
				self.reachIndicatorPool[y][x].draw(screen)
			for (x, y) in self.attackable:
				self.attackIndicatorPool[y][x].draw(screen)

		# this case has been speciallized
		elif self.displayMode == 4:
			pos = self.boardHandler.characDict[0][0]
			charac = self.boardHandler.characDict[0][1]

			for j in range(4):
				nextPos = (pos[0] + RangeIndicator.dx[j], pos[1] + RangeIndicator.dy[j])
				if nextPos[0] < 0 or nextPos[0] >= Board.Board.HEIGHT or nextPos[1] < 0 or nextPos[1] >= Board.Board.WIDTH:
					continue
				self.reachIndicatorPool[nextPos[1]][nextPos[0]].draw(screen)