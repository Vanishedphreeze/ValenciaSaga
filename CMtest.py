import Player
import CharacterBase
import Board
import BattleManager

player1 = Player.Player()
player2 = Player.Player()
board = Board.Board()

playerlist = (player1, player2)

index = 0
for p in playerlist:
    p.init(index)
    index += 1

# create some cards 
ch = []
for i in range(10):
   ch.append(CharacterBase.CharacterBase())

# print(ch)

# put some cards in hand
for i in range(5):
    player1.hand.append(ch[i])

for i in range(5, 10):
    player2.hand.append(ch[i])

print(player1.hand)
print(player2.hand)

board.init()

BattleManager.instance.init(board, playerlist)

BattleManager.instance.summon(1, 2, (2, 3))
board.printBoard()
print(player2.hand)

BattleManager.instance.summon(0, 2, (2, 3)) # illegal
BattleManager.instance.summon(0, 2, (2, 2))
board.printBoard()
print(player1.hand)

BattleManager.instance.move((2, 2), (2, 3)) # illegal
BattleManager.instance.move((2, 2), (4, 5)) # illegal
BattleManager.instance.move((2, 2), (4, 4)) # pos (4,4)
board.printBoard()
BattleManager.instance.move((4, 4), (3, 2)) # pos (3,2)
board.printBoard()
BattleManager.instance.move((2, 3), (0, 0))
BattleManager.instance.move((2, 3), (0, 1))  # illegal
BattleManager.instance.move((0, 1), (-1, -1)) # illegal
board.printBoard()