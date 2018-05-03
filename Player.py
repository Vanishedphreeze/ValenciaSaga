import random
import CharacterBase

class Player(object):
	# index will get a number when BattleCore Init
	MAXHAND = 7

	def __init__(self):
		self.index = None
		self.hand = None
		self.deck = None
		# onBoardCharacter = None

	def init(self, index):
		self.index = index
		self.hand = []
		self.deck = []
		# self.onBoardCharacter = []
		# load deck shouid be here

	# draw cards, if len(deck) < n, draw len(deck)
	def draw(self, n):
		for i in range(n):
			if len(self.deck) > 0:
				if len(self.hand) < 7:
					self.hand.append(self.deck.pop())
				else:
					self.deck.pop()

	# Fisher–Yates shuffle algorithm
	def shuffle(self):
		i = len(self.deck) - 1
		while i > 0:
			p = random.randint(0, i)
			self.deck[i], self.deck[p] = self.deck[p], self.deck[i]
			i -= 1

	# create random deck. only used for testing BattleTest
	# here charac.poolindex is to check whether shuffle is done

	'''
	status = {
		"HP" : 30,
		"ATK" : 15,
		"DEF" : 8,
		"INT" : 15,
		"RES" : 8,
		"SPD" : 10,
		"MOV" : 4,
		"RNG" : 1
	}
	'''

	def createRandDeck(self, n):
		for i in range(n):
			temp = CharacterBase.CharacterBase()

			# for testing shuffle
			temp.poolIndex = i
			
			# modifying charac data
			temp.status["HP"] += random.randint(-5, 5)
			temp.status["ATK"] += random.randint(-2, 2)
			temp.status["DEF"] += random.randint(-2, 2)
			temp.status["INT"] += random.randint(-2, 2)
			temp.status["RES"] += random.randint(-2, 2)
			temp.status["SPD"] += random.randint(-1, 1)
			temp.status["RNG"] += random.randint(0, 1)

			# push into deck
			self.deck.append(temp)


	def printDeckIndex(self):
		for i in self.deck:
			print(i.poolIndex)