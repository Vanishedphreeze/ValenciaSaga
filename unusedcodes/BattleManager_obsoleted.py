from Board import Board
from CharacterBase import CharacterBase
from Player import Player

class BattleManager(object):
	def __init__(self):
		self._boardInstance = None
		self._playerList = None



	# BattleManager should load after board and players
	# player should not change during one match
	def init(self, boardInstance, playerList):
		if not isinstance(boardInstance, Board):
			print("Board type mismatch")
			return False
		if not isinstance(playerList, tuple):
			print("PlayerList type mismatch")
			return False
		for i in playerList:
			if not isinstance(i, Player):
				print("PlayerList type mismatch")
				return False

		self._boardInstance = boardInstance
		self._playerList = playerList
		return True



	# playerNo depends on how we establish playerList
	# charac.owner should be written before 
	def summon(self, playerNo, handIndex, posOnBoard):
		tempCharac = self._playerList[playerNo].hand[handIndex]
		# Beware whether addCharac successful
		if self._boardInstance.addCharac(posOnBoard, tempCharac):
			self._playerList[playerNo].hand.pop(handIndex)
			return True
		else:
			return False



	def summonMainCharac(self, playerNo, posOnBoard):
		tempCharac = self._playerList[playerNo].mainCharac
		# Beware whether addCharac successful
		if self._boardInstance.addCharac(posOnBoard, tempCharac):
			self.isMainCharacOnBoard = True
			return True
		else:
			return False



	# this function judges move range
	def move(self, pos, targetPos):
		charac = self._boardInstance.getCharacByPos(pos)

		if charac == None:
			print("Invalid character position")
			return False

		dist = abs(targetPos[0] - pos[0]) + abs(targetPos[1] - pos[1])
		if charac.status["MOV"] <  dist:
			print("Move out of range")
			return False
			
		return self._boardInstance.moveCharac(pos, targetPos)



	# attack does not care which owner it belongs to
	def attack(self, pos, targetPos):
		attacker = self._boardInstance.getCharacByPos(pos)
		target = self._boardInstance.getCharacByPos(targetPos)

		if attacker == None or target == None:
			print("Invalid attacker/target position")
			return False

		dist = abs(targetPos[0] - pos[0]) + abs(targetPos[1] - pos[1])
		if attacker.status["RNG"] <  dist:
			print("Attack out of range")
			return False

		# is this nessesary to put hpdec into a function?
		# dead processes should be in event system
		# this is only a physical attack
		target.status["HP"] -= attacker.status["ATK"]

		# character dead
		if target.status["HP"] <= 0:
			self._boardInstance.removeCharac(targetPos)

		return True
		# return self._boardInstance.moveCharac(pos, targetPos)




	'''
	def move(self, posOnBoard, dpos):
		charac = self._boardInstance.characterDict[self._boardInstance.board[posOnBoard[0]][posOnBoard[1]]][1]
		if charac.status["MOV"] >= dpos[0] + dpos[1] and self._boardInstance.board[posOnBoard[0] + dpos[0]][posOnBoard[1] + dpos[1]] == -1:
			self._boardInstance.board
		else:
			print("illegal move.")
	'''

instance = BattleManager()