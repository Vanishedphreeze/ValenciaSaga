import CharacterBase
import Player
import Board

class AIBase(object):
	def __init__(self):
		self.boardHandler = None
		self.playerHandler = None



	def init(self, board, player):
		self.boardHandler = board
		self.playerHandler = player



	def prepare(self):
		pass
		


	# returns operation once a time when call
	def step(self):
		return None



	def destroy(self):
		pass