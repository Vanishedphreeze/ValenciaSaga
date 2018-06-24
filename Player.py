import random
import ResourceManager
import CharacterBase

class Player(object):
	# index will get a number when BattleCore Init
	MAXHAND = 7

	def __init__(self):
		self.index = None
		self.hand = None
		self.deck = None
		self.mainCharac = None
		self.isMainCharacOnBoard = False
		# set true when sommon, false when battle over in BattleCore
		# onBoardCharacter = None



	def init(self, index):
		self.index = index
		self.hand = []
		self.deck = []
		templet = ResourceManager.instance.getResourceHandler("MainCharacTemplet")
		self.mainCharac = CharacterBase.CharacterBase(10, templet)
		self.mainCharac.owner = index
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

	# self.status = {
	# 			"ATK" : 4,
	# 			"HP" : 4,
	# 			"MOV" : 2,
	# 			"RNG" : 1
	# 		}



	def createRandDeck(self, n):
		for i in range(n):
			templetList = ResourceManager.instance.getResourceHandler("CharacTemplet")
			code = random.randint(0, len(templetList) - 1)
			temp = CharacterBase.CharacterBase(code, templetList[code])

			# for testing shuffle
			temp.poolIndex = i
			temp.owner = self.index

			characType = random.randint(0, 9)
			if characType == 0:
				temp.status["ATK"] += -1
				temp.status["HP"] += -1
			elif characType in range(1, 3):
				temp.status["ATK"] += -1
				temp.status["HP"] += +1
			elif characType in range(3, 7):
				pass
			elif characType in range(7, 9):
				temp.status["ATK"] += +1
				temp.status["HP"] += -1
			elif characType == 9:
				temp.status["ATK"] += +1
				temp.status["HP"] += +1

			# # modifying charac data
			# temp.status["HP"] += random.randint(-1, 1)
			# temp.status["ATK"] += random.randint(-1, 1)
			# temp.status["MOV"] += random.randint(-1, 1)
			# temp.status["RNG"] += random.randint(0, 1)


			# push into deck
			self.deck.append(temp)



	def printDeckIndex(self):
		for i in self.deck:
			print(i.poolIndex)


	def dump(self):
		temp = {}
		temp["index"] = self.index
		temp["hand"] = []
		for i in range(len(self.hand)):
			temp["hand"].append(self.hand[i].dump())
		temp["deck"] = []
		for i in range(len(self.deck)):
			temp["deck"].append(self.deck[i].dump())
		# temp["mainCharac"] = self.mainCharac.dump()
		temp["isMainCharacOnBoard"] = self.isMainCharacOnBoard
		return temp


	def load(self, data):
		self.index = data["index"]

		self.hand = []
		for i in range(len(data["hand"])):
			self.hand.append(CharacterBase.CharacterBase.load(data["hand"][i]))

		self.deck = []
		for i in range(len(data["deck"])):
			self.deck.append(CharacterBase.CharacterBase.load(data["deck"][i]))

		# fuck this!
		# self.mainCharac = CharacterBase.CharacterBase.load(data["mainCharac"])
		self.isMainCharacOnBoard = data["isMainCharacOnBoard"]

