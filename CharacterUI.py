import pygame
from GameObject import GameObject

class CharacterUI(GameObject):
	'''
	# index on board
	index = None
	# this should be init somewhere
	posOnBoard = None
	'''

	def pointCollide(self, pos):
		if pos[0] in range(self.position[0], self.position[0] + self.size[0]) and pos[1] in range(self.position[1], self.position[1] + self.size[1]):
			return True
		else:
			return False