import BattleCore

BattleCore.instance.init()
BattleCore.instance.start()

while True:
	'''
	opt[0] == 0:  # summon(playerNo, handIndex, posOnBoard)
	opt[0] == 1:  # move(pos, targetPos)
	opt[0] == 2:  # attack(pos, targetPos)
	opt[0] == -1: # end main phase
	'''
	protoc = int(input())
	opt = None

	if protoc == 0:
		playerNo = int(input())
		handIndex = int(input())
		posOnBoard = int(input()), int(input())
		opt = (protoc, (playerNo, handIndex, posOnBoard))
	elif protoc == 1:
		pos = int(input()), int(input())
		targetPos = int(input()), int(input())
		opt = (protoc, (pos, targetPos))
	elif protoc == 2:
		pos = int(input()), int(input())
		targetPos = int(input()), int(input())
		opt = (protoc, (pos, targetPos))
	elif protoc == 3:
		pos = int(input()), int(input())
		BattleCore.instance.showStatusAtPos(pos)
		continue
	elif protoc == -1:
		opt = (protoc, )


	BattleCore.instance.pushForward(opt)