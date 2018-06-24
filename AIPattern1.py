from queue import Queue
import CharacterBase
import Player
import Board
from AIBase import AIBase

class AIPattern1(AIBase):
	# used by function step
	dx = (1, -1, 0, 0, 1, 1, -1, -1, 2, 0, -2, 0)
	dy = (0, 0, 1, -1, -1, 1, 1, -1, 0, 2, 0, -2)

	def __init__(self):
		super().__init__()
		# self.boardHandler = None
		# self.playerHandler = None
		# (pos, charac)
		self.unmoved = None
		# restores charac that can't reach enemy
		self.moveList = None
		self.pos_mainCharac = None
		# judges whether it is necessary to attempt attack
		self.moveFlag = None
		# is it necessary to judge whether main character is moved?
		self.shouldSummon = None



	def prepare(self):
		super().prepare()
		self.moveFlag = False

		self.unmoved = []
		self.moveList = []
		self.pos_mainCharac = None
		for (index, (pos, charac)) in self.boardHandler.characDict.items():
			if charac.owner == self.playerHandler.index:
				if not charac.ctype == 10: # mainCharac
					self.unmoved.append((pos, charac))
				else:
					self.pos_mainCharac = (pos, charac)

		self.unmoved.sort(key = getKey)
		self.unmoved.append(self.pos_mainCharac)

		self.shouldSummon = False

		# print()



# 行动模式1：
# while 未行动列表还有人物：
# 	从高hp单位枚举（主将优先级最低）：
# 		如果能砍死人就砍, high atk first
# 		continue
# 	从高hp单位枚举（除主将外）：
# 		如果能砍到人就砍, high atk first
# 		continue
# 	从高hp单位全员向敌将方向移动，优先横向。
# 	（break）

	def step(self):
		super().step()
		print("AI said: OK I'm playing!")
		# if recvOpt[0] == 0: # summon(playerNo, handIndex, posOnBoard)
		# elif recvOpt[0] == 1: # move(pos, targetPos)
		# elif recvOpt[0] == 2: # attack(pos, targetPos)
		
		# 暂时没有考虑行军。打不到人的都原地站着了。
		# if len(self.unmoved) == 0:
		# 	return ((-1, ), )

		# if main charac not attacked, try summon a character.
		if self.shouldSummon:
			optList = []
			if self.pos_mainCharac[1].state < 2:
				for p in range(4):
					mainCharacPos = self.boardHandler.characDict[self.playerHandler.index][0]
					summonPos = (mainCharacPos[0] + AIPattern1.dx[p], mainCharacPos[1] + AIPattern1.dy[p])
					if summonPos[0] < 0 or summonPos[0] >= Board.Board.HEIGHT or summonPos[1] < 0 or summonPos[1] >= Board.Board.WIDTH:
						continue
					if self.boardHandler.getCharacByPos(summonPos) == None:
						optList.append( 
							(0, (self.playerHandler.index, 0, summonPos) ) 
						)
						break

			optList.append( (-1, ) )
			return(tuple(optList))
	


		movedIndex = None
		firstEnemyList = None
		firstReached = None
		
		# remember the index that should be removed from 
		removeList = []
		
		for i in range(len(self.unmoved)):
			# this for finding if there's enemy reachable
			######################################################################
			pos = self.unmoved[i][0]
			charac = self.unmoved[i][1]

			# (enemyPos, charac, where_stand_to_kill)
			enemyList = []

			q = Queue()
			reached = set()

			# find enemies and push in queue
			r = 0
			if charac.status["RNG"] == 1:
				r = 4
			elif charac.status["RNG"] == 2:
				r = 12
			else:
				print("AI said: Can't process range larger than 2")

			for j in range(r):
				nextPos = (pos[0] + AIPattern1.dx[j], pos[1] + AIPattern1.dy[j])
				if nextPos[0] < 0 or nextPos[0] >= Board.Board.HEIGHT or nextPos[1] < 0 or nextPos[1] >= Board.Board.WIDTH:
					continue
				nextPosCharac = self.boardHandler.getCharacByPos(nextPos)
				if nextPosCharac != None and nextPosCharac.owner != charac.owner:
					enemyList.append((nextPos, nextPosCharac, pos))

			# pos, stepleft
			q.put((tuple(pos), charac.status["MOV"]))
			reached.add(tuple(pos))

			while not q.empty():
				curPos, curStepLeft = q.get()

				# find enemies and push in queue
				# if there's ally in cur position, don't do this.
				if self.boardHandler.getCharacByPos(curPos) == None:
					r = 0
					if charac.status["RNG"] == 1:
						r = 4
					elif charac.status["RNG"] == 2:
						r = 12
					else:
						print("AI said: Can't process range larger than 2")

					for j in range(r):
						nextPos = (curPos[0] + AIPattern1.dx[j], curPos[1] + AIPattern1.dy[j])
						if nextPos[0] < 0 or nextPos[0] >= Board.Board.HEIGHT or nextPos[1] < 0 or nextPos[1] >= Board.Board.WIDTH:
							continue
						nextPosCharac = self.boardHandler.getCharacByPos(nextPos)
						if nextPosCharac != None and nextPosCharac.owner != charac.owner:
							enemyList.append((nextPos, nextPosCharac, curPos))

				# if no step left, do nothing. else go
				if curStepLeft == 0:
					continue

				for j in range(4):
					nextPos = (curPos[0] + AIPattern1.dx[j], curPos[1] + AIPattern1.dy[j])
					if nextPos[0] < 0 or nextPos[0] >= Board.Board.HEIGHT or nextPos[1] < 0 or nextPos[1] >= Board.Board.WIDTH:
						continue
					if nextPos in reached:
						continue
					nextPosCharac = self.boardHandler.getCharacByPos(nextPos)
					if nextPosCharac == None or nextPosCharac.owner == charac.owner:
						q.put((nextPos, curStepLeft - 1))
						reached.add(nextPos)

			##### end ################################################################# 

			# if he can't reach anyone, move him into moveList.
			# removeList tags the index should be removed in self.unmoved. remember to remove in reversal.
			# for pos_charac_standPos in enemyList:
			# 	print(pos_charac_standPos)
			# print(":::::")

			if len(enemyList) == 0:
				removeList.append(i)
			elif firstReached == None and charac.ctype != 10:
				firstEnemyList = enemyList
				firstReached = i


			# finding if there's someone to kill
			maxATK = -1
			pos_target_standPos = None
			for pos_charac_standPos in enemyList:
				if pos_charac_standPos[1].status["HP"] < charac.status["ATK"]:
					if pos_charac_standPos[1].status["ATK"] > maxATK:
						maxATK = pos_charac_standPos[1].status["ATK"]
						pos_target_standPos = pos_charac_standPos

			if pos_target_standPos != None: #kill him!
				self.unmoved.pop(i)

				##############################################################################
				# print("\n\npop in kill\nunmoved: ")
				# for a in self.unmoved:
				# 	print(a)
				# print("\nremove List :")
				# print(removeList)
				# print("\n")
				# for x in range(len(removeList)):
				# 	print("poping: %d", removeList[-1 - x])
				# 	self.moveList.append(self.unmoved.pop(removeList[-1 - x]))
				##############################################################################

				
				return (
					(1, (pos, pos_target_standPos[2])),	
					(2, (pos_target_standPos[2], pos_target_standPos[0]))
				)

		# for loop finished


		# if there's no one can reach, all move forward 
		# temporarily no move
		if firstReached == None:
			optList = []
			# All Million, Push Forward!
			# 这沙雕AI没人打就只会往左跑，一次一格
			for pos_charac in self.unmoved:
				optList.append(
					(1, (pos_charac[0], ( pos_charac[0][0], pos_charac[0][1] - 1)))
				)

			self.unmoved = []

			self.shouldSummon = True
			return (tuple(optList))

		# no one can kill, then get first charac's list, find the highest attack, just hit once.

		for pos_charac_standPos in firstEnemyList:
			print(pos_charac_standPos)

		maxATK = -1
		pos_target_standPos = None
		for pos_charac_standPos in firstEnemyList:
			if pos_charac_standPos[1].status["ATK"] > maxATK:
				maxATK = pos_charac_standPos[1].status["ATK"]
				pos_target_standPos = pos_charac_standPos

		if pos_target_standPos != None: #hit him!
			tempPos = self.unmoved.pop(firstReached)[0]

			####################################################
			# print("\n\npop in hit\nunmoved: ")
			# for a in self.unmoved:
			# 	print(a)
			# print("\nremove List :")
			# print(removeList)
			# print("\n")
			# for y in range(len(removeList)):
			# 	print("poping: %d", removeList[-1 - y])
			# 	self.moveList.append(self.unmoved.pop(removeList[-1 - y]))
			####################################################


			return (
				(1, (tempPos, pos_target_standPos[2])),	
				(2, (pos_target_standPos[2], pos_target_standPos[0]))
			)
		
		# function should'n run here, 
		print("AI said: What? It seems I've gone wrong.")
		return((-1, ), )


	def destroy(self):
		super().destroy()



def getKey(pos_charac):
	return pos_charac[1].status["HP"]
