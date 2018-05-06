from CharacterBase import CharacterBase
from queue import Queue


class Board(object):
	# beware: board is a list, do NOT modify the range
	# be careful if you wanna insert one character more than once
	# it is better to use memory recycle
	
	HEIGHT = 5
	WIDTH = 10

	# used by function reachable
	dx = (0, 1, 0, -1)
	dy = (1, 0, -1, 0)

	def __init__(self):
		self.board = None

		# index : (pos, character)
		self.characDict = None

		# index++ when charater inserted into dict
		self._index = 0



	def init(self):
		self.board = [[-1 for i in range(Board.WIDTH)] for i in range(Board.HEIGHT)]
		self.characDict = {}



	def addCharac(self, pos, charac):
		if not isinstance(charac, CharacterBase):
			print("character type mismatch.")
			return False
		if pos[0] < 0 or pos[0] >= Board.HEIGHT or pos[1] < 0 or pos[1] >= Board.WIDTH or self.board[pos[0]][pos[1]] != -1:
			print("illegal position.")
			return False

		self.characDict[self._index] = [pos, charac]
		self.board[pos[0]][pos[1]] = self._index
		self._index += 1
		return True



	# no range judge, careful
	def removeCharac(self, pos):
		# print("del board", pos, self.board[pos[0]][pos[1]])
		if self.board[pos[0]][pos[1]] != -1:
			self.characDict.pop(self.board[pos[0]][pos[1]])
			self.board[pos[0]][pos[1]] = -1



	def getCharacByPos(self, pos):
		if self.board[pos[0]][pos[1]] == -1:
			return None
		else:
			return self.characDict[self.board[pos[0]][pos[1]]][1]



	# it judges block and dist
	def moveCharac(self, pos, targetPos):
		if targetPos[0] < 0 or targetPos[0] >= Board.HEIGHT or targetPos[1] < 0 or targetPos[1] >= Board.WIDTH:
			print("Move out from board.")
			return False

		if self.board[targetPos[0]][targetPos[1]] != -1:
			print("illegal move.")
			return False

		charac = self.getCharacByPos(pos)
		if not self.reachable(pos, targetPos, charac.status["MOV"]):
			return False

		self.characDict[self.board[pos[0]][pos[1]]][0] = targetPos
		self.board[targetPos[0]][targetPos[1]] = self.board[pos[0]][pos[1]]
		self.board[pos[0]][pos[1]] = -1
		return True



	# this does NOT judge block and dist
	def superMoveCharac(self, pos, targetPos):
		if targetPos[0] < 0 or targetPos[0] >= Board.HEIGHT or targetPos[1] < 0 or targetPos[1] >= Board.WIDTH:
			print("Move out from board.")
			return False

		if self.board[targetPos[0]][targetPos[1]] == -1:
			self.characDict[self.board[pos[0]][pos[1]]][0] = targetPos
			self.board[targetPos[0]][targetPos[1]] = self.board[pos[0]][pos[1]]
			self.board[pos[0]][pos[1]] = -1
		else:
			print("illegal move.")
			return False

		return True



	# def swapCharac(self, pos, dpos):
	# this function does not judge whether you have reached before.
	def reachable(self, pos, targetPos, maxStep):
		if pos[0] == targetPos[0] and pos[1] == targetPos[1]:
			return True
		q = Queue()
		q.put((tuple(pos[:]), maxStep))
		while not q.empty():
			curInfo = q.get()
			for i in range(4):
				nextPos = (curInfo[0][0] + Board.dx[i], curInfo[0][1] + Board.dy[i])
				restStep = curInfo[1] - 1
				if restStep < abs(targetPos[0] - nextPos[0]) + abs(targetPos[1] - nextPos[1]):
					continue
				if nextPos[0] < 0 or nextPos[0] >= Board.HEIGHT or nextPos[1] < 0 or nextPos[1] >= Board.WIDTH:
					continue
				charac = self.getCharacByPos(nextPos)
				if charac == None or charac.owner == self.getCharacByPos(pos).owner:
					if nextPos[0] == targetPos[0] and nextPos[1] == targetPos[1]:
						return True
					q.put((nextPos, restStep))

		return False



	def resetAllMoveState(self):
		for (index, (pos, charac)) in self.characDict.items():
			charac.state = 0



	def printBoard(self):
		print("----------------")
		for i in self.board:
			print(i)