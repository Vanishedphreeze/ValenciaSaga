import pygame
import ResourceManager
from GameObject import GameObject

class CharacterUI(GameObject):
	def __init__(self):
		super().__init__()
		self.atk = 0
		self.hp = 0
		self.hpUI = GameObject()
		self.atkUI = GameObject()
		self.statusFont = None
		self.hpUIdpos = (35, 35) 
		self.atkUIdpos = (2, 35)
		self.type = 0
		self.owner = 0
		self.state = 0

	'''
	# index on board
	index = None
	# this should be init somewhere
	posOnBoard = None
	'''



	def setStatus(self, atk, hp):
		self.atk = atk
		self.hp = hp



	def init(self, imageNo, owner, state, pos, size):
		# 0 berserker, 1 knight, 2 cavalier, 3 sniper, 10 mainCharac
		# sepciallized
		self.owner = owner
		self.state = state

		if imageNo == 0:
			image = ResourceManager.instance.getResourceHandler("berserker" + str(owner))
		elif imageNo == 1:
			image = ResourceManager.instance.getResourceHandler("knight" + str(owner))
		elif imageNo == 2:
			image = ResourceManager.instance.getResourceHandler("cavalier" + str(owner))
		elif imageNo == 3:
			image = ResourceManager.instance.getResourceHandler("archer" + str(owner))
		elif imageNo == 10:
			image = ResourceManager.instance.getResourceHandler("athos" + str(owner))
		else:
			print("UILayer: Illegal imageNo")

		super().init(image, pos, size) 

		# super().init(image, pos, size)
		#self.statusFont = pygame.font.Font(None, 30)
		self.statusFont = ResourceManager.instance.getResourceHandler("defaultFont")
		self.hpUI.init(self.statusFont.render(str(self.hp), True, (255, 0, 0)), pos, size)
		self.atkUI.init(self.statusFont.render(str(self.atk), True, (255, 0, 0)), pos, size)
		# here size is useless, unless using draw.



	def update(self):
		super().update()
		self.hpUI.position = [self.position[0] + self.hpUIdpos[0], self.position[1] + self.hpUIdpos[1]]
		self.atkUI.position =  [self.position[0] + self.atkUIdpos[0], self.position[1] + self.atkUIdpos[1]]
		self.hpUI.changeAvatar(self.statusFont.render(str(self.hp), True, (255, 0, 0)))
		self.atkUI.changeAvatar(self.statusFont.render(str(self.atk), True, (255, 0, 0)))
		# print(self.hp)



	def draw(self, screen):
		super().draw(screen)
		self.hpUI._drawProto(screen)
		self.atkUI._drawProto(screen)



	def pointCollide(self, pos):
		if pos[0] in range(self.position[0], self.position[0] + self.size[0]) and pos[1] in range(self.position[1], self.position[1] + self.size[1]):
			return True
		else:
			return False