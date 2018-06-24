import CharacterBase
import Player
import Board
from AIBase import AIBase

class AITutorialPattern(AIBase):
	def __init__(self):
		super().__init__()
		# self.boardHandler = None
		# self.playerHandler = None
		# (pos, charac)
		self.unmoved = None
		self.pos_mainCharac = None
		# is it necessary to judge whether main character is moved?



	def prepare(self):
		super().prepare()
		self.unmoved = []
		self.pos_mainCharac = None
		for (index, (pos, charac)) in self.boardHandler.characDict.items():
			if charac.owner == self.playerHandler.index:
				if not charac.ctype == 10: # mainCharac
					self.unmoved.append((pos, charac))
				else:
					self.pos_mainCharac = (pos, charac)

		self.unmoved.sort(key = getKey)
		self.unmoved.append(self.pos_mainCharac)

		# print()



	def step(self):
		super().step()
		print("AI said: OK I move!")
		# if recvOpt[0] == 0: # summon(playerNo, handIndex, posOnBoard)
		# elif recvOpt[0] == 1: # move(pos, targetPos)
		# elif recvOpt[0] == 2: # attack(pos, targetPos)
		
		if len(self.unmoved) == 0:
			return ((-1, ), )

		pos = self.pos_mainCharac[0]
		targetPos = (pos[0], pos[1] - 1)
		self.unmoved.pop(0)

		return ((1, (pos, targetPos)), )



	def destroy(self):
		super().destroy()



def getKey(pos_charac):
	return pos_charac[1].status["HP"]