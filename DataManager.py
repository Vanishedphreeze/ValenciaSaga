class DataManager(object):
	
	def dump(self):
		if dtype == 0: # charac
			temp = {}
			temp["poolIndex"] = self.poolIndex
			temp["owner"] = self.owner
			temp["ctype"] = self.ctype
			temp["state"] = self.state
			temp["status"] = self.status
			return temp
		elif dtype == 1:
			temp = {}
			temp["board"] = self.board
			temp["characDict"] = {}
			for (index, (pos, charac)) in self.characDict.items():
				temp["characDict"][index] = (pos, charac.dump())
			temp["_index"] = self._index
			return temp
		elif dtype == 2:
			savefile = open("savedata.txt", "w")
			temp = {}
			temp["playerList"] = []
			for i in range(len(self.playerList)):
				temp["playerList"].append(self.playerList[i].dump()) 
			temp["board"] = self.board.dump()

			# self._battleStatus saves the handler of board and playerList. it is done while init, so this is no need.
			# the count of turns, initial 0.
			temp["_turn"] = self._turn
			temp["_phase"] = self._phase
			temp["_curPlayer"] = self._curPlayer

			# self._isStarted inited when start.
			# save can only happened in main phase, so battleHandler is no need.

			savefile.write(json.dumps(temp))
			savefile.close()
		elif dtype == 3:
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

		

	def load(dtype, data):
		if dtype == 0: # charac
			charac = CharacterBase(data["ctype"], data["status"])
			charac.poolIndex = data["poolIndex"]
			charac.owner = data["owner"]
			charac.state = data["state"]
			return charac
		elif dtype == 1:
			self.board = data["board"]
			self.characDict = {}
			for (index, (pos, charac)) in data["characDict"].items():
				self.characDict[int(index)] = [pos, CharacterBase.load(charac)]
			self._index = data["_index"]
		elif dtype == 2:
			savefile = open("savedata.txt", "r")
			temp = json.loads(savefile.read())
			# print(temp)

			self.board.load(temp["board"])

			# the number of players should be the same!!!
			for i in range(len(temp["playerList"])):
				self.playerList[i].load(temp["playerList"][i])
				self.playerList[i].mainCharac = self.board.characDict[i][1]
			
			self._turn = temp["_turn"]
			self._phase = temp["_phase"]
			self._curPlayer = temp["_curPlayer"]
		elif dtype == 3:
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
