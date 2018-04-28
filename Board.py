from CharacterBase import CharacterBase

class Board(object):
	# beware: board is a list, do NOT modify the range
	# be careful if you wanna insert one character more than once
	# it is better to use memory recycle
	
	HEIGHT = 5
	WIDTH = 10
	board = None

	# index : (pos, character)
	characDict = None

	# index++ when charater inserted into dict
	_index = 0

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

	# this function does not judge MOV >= dist
	def moveCharac(self, pos, targetPos):
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

	def printBoard(self):
		print("----------------")
		for i in self.board:
			print(i)