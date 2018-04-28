import BattleCore

BattleCore.instance.init()
BattleCore.instance.start()

while True:
	optList = []
	a = [-1 for i in range(5)]
	'''
	opt[0] == 0: # summon(playerNo, handIndex, posOnBoard)
	opt[0] == 1: # move(pos, targetPos)
	opt[0] == 2: # attack(pos, targetPos)
	'''
	for i in range(5):
		a[i] = int(input())

	if a[0] == 3:
		BattleCore.instance.showStatusAtPos((a[1], a[2]))
		continue
	elif a[0] == 0:
		optList.append( (a[0], (a[1], a[2], (a[3], a[4])) ) )
	else:
		optList.append( (a[0], ((a[1], a[2]), (a[3], a[4])) ) )

	BattleCore.instance.pushForward(tuple(optList))