from Board import Board
from CharacterBase import CharacterBase
from Player import Player
import EventManager



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
	def summon(self, playerNo, handIndex, posOnBoard, operator):
		# judge operator
		if operator != playerNo:
			print("No authorization.")
			return False

		# judge the hand range
		if handIndex >= len(self._playerList[playerNo].hand):
			print("Hand index out of range")
			return False

		# judge main character state
		if self._playerList[playerNo].mainCharac.state > 1:
			print("Summoned or main character moved")
			return False

		# judge the summon pos
		# attention. first two summoned character, index = 0, 1.
		# if this changed, it will not work.
		mainCharacPos = self._boardInstance.characDict[playerNo][0]
		dist = abs(mainCharacPos[0] - posOnBoard[0]) + abs(mainCharacPos[1] - posOnBoard[1])
		if dist > 1:
			print("Summoned out of range")
			return False

		# set main charac, summoned charac's state = 2
		if self._summon(playerNo, handIndex, posOnBoard):
			self._playerList[playerNo].mainCharac.state = 2
			self._boardInstance.getCharacByPos(posOnBoard).state = 2
			EventManager.instance.call("summons", playerNo, 1)
			return True
		else:
			return False



	def _summon(self, playerNo, handIndex, posOnBoard):
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
			self._playerList[playerNo].isMainCharacOnBoard = True
			return True
		else:
			return False



	# this function judges move range
	def move(self, pos, targetPos, operator):
		# judge charac exists
		charac = self._boardInstance.getCharacByPos(pos)
		if charac == None:
			print("Invalid character position")
			return False

		# judge operator
		if charac.owner != operator:
			print("No authorization.")
			return False

		# judge charac state
		if charac.state > 0:
			print("Character moved, attacked, or just summoned.")
			return False
		
		# judge move range
		dist = abs(targetPos[0] - pos[0]) + abs(targetPos[1] - pos[1])
		if charac.status["MOV"] <  dist:
			print("Move out of range")
			return False

		# set character state = 1
		if self._move(pos, targetPos):
			charac.state = 1
			return True
		else:
			return False



	def _move(self, pos, targetPos):	
		return self._boardInstance.moveCharac(pos, targetPos)



	# attack does not care which owner it belongs to
	def attack(self, pos, targetPos, operator):
		attacker = self._boardInstance.getCharacByPos(pos)
		target = self._boardInstance.getCharacByPos(targetPos)

		# judge charac exists
		if attacker == None or target == None:
			print("Invalid attacker/target position")
			return False

		# judge operator
		if attacker.owner != operator:
			print("No authorization.")
			return False

		# judge charac state
		if attacker.state > 1:
			print("Character attacked or just summoned.")
			return False

		# judge whether in same team
		if attacker.owner == target.owner:
			print("illegal to attack teammates")
			return False

		# judge attack range
		dist = abs(targetPos[0] - pos[0]) + abs(targetPos[1] - pos[1])
		if attacker.status["RNG"] <  dist:
			print("Attack out of range")
			return False

		if self._attack(pos, targetPos):
			attacker.state = 2
			return True
		else:
			return False



	def _attack(self, pos, targetPos):
		attacker = self._boardInstance.getCharacByPos(pos)
		target = self._boardInstance.getCharacByPos(targetPos)

		# is this nessesary to put hpdec into a function?
		# dead processes should be in event system
		if target.status["HP"] > attacker.status["ATK"]:
			tempDamage = attacker.status["ATK"]
		else:
			tempDamage = target.status["HP"]
		target.status["HP"] -= attacker.status["ATK"]
		EventManager.instance.call("damage", attacker.owner, tempDamage)

		# character dead
		if target.status["HP"] <= 0:
			self._boardInstance.removeCharac(targetPos)
		else:
			# return attack
			dist = abs(targetPos[0] - pos[0]) + abs(targetPos[1] - pos[1])
			if target.status["RNG"] >= dist:
				attacker.status["HP"] -= target.status["ATK"]
				if attacker.status["HP"] <= 0:
					self._boardInstance.removeCharac(pos)
					EventManager.instance.call("kills", attacker.owner, 1)
					EventManager.instance.call("deaths", target.owner, 1)


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