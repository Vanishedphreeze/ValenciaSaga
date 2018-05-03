class CharacterBase(object):
	def __init__(self):
		self.poolIndex = 0
		self.owner = 0
		self.status = {
			"HP" : 30,
			"ATK" : 15,
			"DEF" : 8,
			"INT" : 15,
			"RES" : 8,
			"SPD" : 10,
			"MOV" : 4,
			"RNG" : 1
		}