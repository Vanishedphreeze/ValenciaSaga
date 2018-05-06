import copy

class CharacterBase(object):
	def __init__(self, ctype, status = None):
		self.poolIndex = 0
		self.owner = 0
		# 0 berserker, 1 knight, 2 cavalier, 3 sniper, 10 mainCharac
		self.type = ctype

		# state: 0 not moved, 1 moved, attacked
		self.state = 0

		# get status from json files
		if status == None:
			self.status = {
				"ATK" : 4,
				"HP" : 4,
				"MOV" : 2,
				"RNG" : 1
			}
		else:
			self.status = copy.deepcopy(status)
