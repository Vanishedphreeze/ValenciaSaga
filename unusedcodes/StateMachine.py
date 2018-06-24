import pygame
import StateNode

class StateMachine(object):
	def __init__(self):
		self.currentState = None



	def init(self, startState):
		self.currentState = startState
		startState.start()



	def transition(self, **kwargs):
		self.currentState = self.currentState.transition(**kwargs)



	def update(self):
		self.currentState.update()



	# more effective method
	def _loadStateMachine(self):
		neutral = StateNode.StateNode()
		neutral.init()
		moveDrag = StateNode.StateNode()
		moveDrag.init()
		neutral.addTransition(moveDrag, (
				lambda eventType:
					eventType == pygame.MOUSEBUTTONDOWN
			)
		)
		neutral.setStartFunc(
			lambda :
				print("########### neutral start.")
		)
		neutral.setUpdateFunc(
			lambda :
				print("neutral")
		)
		moveDrag.addTransition(neutral, (
				lambda eventType:
					eventType == pygame.MOUSEBUTTONUP
			)
		)
		moveDrag.setStartFunc(
			lambda :
				print("########### movedrag start.")
		)
		moveDrag.setUpdateFunc(
			lambda :
				print("movedrag")
		)

		self.init(neutral)



