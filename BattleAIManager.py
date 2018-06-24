import CharacterBase
import Player
import Board
import BattleCore
from AIBase import AIBase
from AIPattern1 import AIPattern1
# from AITutorialPattern import AITutorialPattern



# now BattleAIManager only supports one AI
class BattleAIManager(object):
	def __init__(self):
		self.boardHandler = None
		self.playerHandler = None
		self.AI = AIPattern1()



	def init(self, board, player):
		if not isinstance(self.AI, AIBase):
			print('AIType mismatch')
			return None

		self.boardHandler = board
		self.playerHandler = player
		self.AI.init(board, player)



	def run(self):
		# get AI's opt sequence here if necessary
		self.AI.prepare()
		while True:
			optList = self.AI.step()
			for opt in optList:
				BattleCore.instance.pushForward(opt)
				if opt[0] == -1:
					# AI ends the turn.
					return



instance = BattleAIManager()