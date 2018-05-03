import Player
import CharacterBase
import Board
import BattleStatus
import BattleManager

class BattleCore(object):
	# player 
	MAX_PLAYER = 2

	def __init__(self):
		self.playerList = None 
		self.board = None
		self._battleStatus = None

		# the count of turns, initial 0.
		self._turn = 0

		# phase: 
		# 0 draw phase, 
		# 1 standby phase, 
		# 2 main phase,
		# 3 end phase.
		self._phase = 0
		self._curPlayer = 0
		self._isStarted = False

		# to help controlling battle coroutine
		self.battleHandler = None

	# all these phases are coroutines
	# yield returns required type of opts 
	# use battleHandler.send()
	def _drawPhase(self):
		self._phase = 0
		print("draw phase start.")

		# process all effects in queue

		# draw a card
		for player in self.playerList:
			player.draw(1)

		recvOpt = yield None
		print("draw phase end.")

	def _standbyPhase(self):
		self._phase = 1
		print("standby phase start.")

		# process all effects in queue

		recvOpt = yield None
		print("standby phase end.")

	'''
	def _mainPhase(self):
		self._phase = 2
		print("main phase start.")

		# process all effects in queue

		# hang-up the BattleCore, wait for input
		# number 1 is for test, recieving main phase operations form player
		recvOpt = yield 1

		# parse & process all recieved 
		if not isinstance(recvOpt, tuple):
			print("Operation is not tuple")
			return None

		for opt in recvOpt:
			if not isinstance(recvOpt, tuple):
				print("Operation format wrong")
				continue

			# is there possible to use something else?
			args = opt[1]
			print(args)
			if opt[0] == 0: # summon(playerNo, handIndex, posOnBoard)
				BattleManager.instance.summon(args[0], args[1], args[2])
			elif opt[0] == 1: # move(pos, targetPos)
				BattleManager.instance.move(args[0], args[1])
			elif opt[0] == 2: # attack(pos, targetPos)
				BattleManager.instance.attack(args[0], args[1])

		print("main phase end.")
	'''

	# this function recieves opt once a time, until recieved -1 (turn end)
	def _mainPhase(self):
		self._phase = 2
		print("main phase start.")

		while True:
			# hang-up the BattleCore, wait for input
			# return type:
			recvOpt = yield 1

			# parse & process recvOpt
			if not isinstance(recvOpt, tuple):
				print("Operation format wrong")
				continue

			if recvOpt[0] == -1: # main phase end.
				break
			# recvOpt[0]: protocol number
			# recvOpt[1]: args
			args = recvOpt[1]
			print(args)
			if recvOpt[0] == 0: # summon(playerNo, handIndex, posOnBoard)
				BattleManager.instance.summon(args[0], args[1], args[2])
				self.board.printBoard()
			elif recvOpt[0] == 1: # move(pos, targetPos)
				BattleManager.instance.move(args[0], args[1])
				self.board.printBoard()
			elif recvOpt[0] == 2: # attack(pos, targetPos)
				BattleManager.instance.attack(args[0], args[1])
				self.board.printBoard()
			# is there possible to use something else?


		print("main phase end.")

	def _endPhase(self):
		self._phase = 3
		print("end phase start.")

		# process all effects in queue
		recvOpt = yield None
		print("end phase end.")


	# yield from: continuously enum value from one iterator UNTIL it exhausts
	def _battleRoutine(self):
		print("battle start")
		while True:
			print("/////////////////////// player %d, turn %d start." % (self._curPlayer, self._turn))
			yield from self._drawPhase()
			yield from self._standbyPhase()
			yield from self._mainPhase()
			yield from self._endPhase()

			print("/////////////////////// turn %d end." % self._turn)
			self._curPlayer += 1
			if self._curPlayer >= self.MAX_PLAYER:
			   self._turn += 1
			   self._curPlayer = 0

	def init(self):
		self.battleHandler = self._battleRoutine()

		# create players and init
		self.playerList = []
		for i in range(self.MAX_PLAYER):
			self.playerList.append(Player.Player())
			self.playerList[-1].init(i)
		for player in self.playerList:
			player.createRandDeck(10) # this should be removed
			player.shuffle()
			# player.printDeckIndex()

		# create board
		self.board = Board.Board()
		self.board.init()

		# bind & init BattleManager
		BattleManager.instance.init(self.board, tuple(self.playerList))

		# draw 5 cards
		for player in self.playerList:
			player.draw(5)

		# after all inits are done
		self._battleStatus = BattleStatus.BattleStatus(self.playerList, self.board)



	# same as pushForward, returns the type of the required operations
	def start(self):
		if self._isStarted:
			print("the battle has already started.")
			return None
		next(self.battleHandler) # tell coroutine to start battle
		return self.pushForward(None) # is this dangerous to push forward here?

	def getBattleStatusHandler(self):
		return self._battleStatus
		
	# send operations and continue the battle procedure
	# returns (type, status)
	# type: the type of the required operations
	# status: present battle status
	def pushForward(self, opt):
		requiredType = self.battleHandler.send(opt) 
		opt = None # clear opt buffer
		while requiredType == None:
			requiredType = self.battleHandler.send(opt) 
		return requiredType

	# back door.
	def showStatusAtPos(self, pos):
		temp = self.board.getCharacByPos(pos)
		if temp == None:
			print("Character not exist.")
		else:
			print(
				"Pos(%3d,%3d), index = %d :\nOwner : %d\nHP  : %3d\nATK : %3d\nDEF : %3d\nINT : %3d\nRES : %3d\nSPD : %3d\nMOV : %3d\nRNG : %3d\n"
				%(pos[0], pos[1], temp.poolIndex, temp.owner,
				  temp.status["HP"],
				  temp.status["ATK"],
				  temp.status["DEF"],
				  temp.status["INT"],
				  temp.status["RES"],
				  temp.status["SPD"],
				  temp.status["MOV"],
				  temp.status["RNG"]
				  ) 
			)

instance = BattleCore()