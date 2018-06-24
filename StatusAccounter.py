import EventManager

class StatusAccounter(object):
	def __init__(self, n):
		self.maxPlayer = n
		self.kill = [0 for i in range(n)]
		self.death = [0 for i in range(n)]
		self.summon = [0 for i in range(n)]
		self.damage = [0 for i in range(n)]

	def init(self):
		for i in range(self.maxPlayer):
			self.kill[i] = 0
			self.death[i] = 0
			self.summon[i] = 0
			self.damage[i] = 0
		EventManager.instance.addEvent("kills")
		EventManager.instance.addEvent("deaths")
		EventManager.instance.addEvent("damage")
		EventManager.instance.addEvent("summons")
		EventManager.instance.addListener("kills", self.incKills)
		EventManager.instance.addListener("deaths", self.incDeaths)
		EventManager.instance.addListener("damage", self.incDamage)
		EventManager.instance.addListener("summons", self.incSummons)

	def incKills(self, playerNo, cnt):
		self.kill[playerNo] += cnt

	def incDeaths(self, playerNo, cnt):
		self.death[playerNo] += cnt

	def incDamage(self, playerNo, cnt):
		self.damage[playerNo] += cnt

	def incSummons(self, playerNo, cnt):
		self.summon[playerNo] += cnt
