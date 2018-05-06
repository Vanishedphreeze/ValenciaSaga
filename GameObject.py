import pygame

class GameObject(object):
	def __init__(self):
		self._originalAvatar = None 
		self._Avatar = None
		self.size = None
		self._preSize = None
		self.position = None # top left corner
		# rotation = None



	# don't care about value-passing
	def init(self, image, pos, size):
		'''
		self.size = [size[0], size[1]]
		self.position = [pos[0], pos[1]]
		self._preSize = [self.size[0], self.size[1]]
		self._originalAvatar = image
		self._Avatar = pygame.transform.smoothscale(self._originalAvatar, (self.size[0], self.size[1]) )
		# self.rotation = 0
		'''
		self.size = list(size[:])
		self.position = list(pos[:])
		self._preSize = list(self.size[:])
		self._originalAvatar = image
		self._Avatar = pygame.transform.smoothscale(self._originalAvatar, self.size)
		# self.rotation = 0



	# gameObject does not load images, use resource manager.
	def changeAvatar(self, image):
		self._originalAvatar = image
		self._Avatar = pygame.transform.smoothscale(self._originalAvatar, self.size)



	def start(self):
		pass



	def update(self):
		pass



	def draw(self, screen):
		if not self.size == self._preSize:
			print("sizeChanged")
			self._preSize = list(self.size[:])
			self._Avatar = pygame.transform.smoothscale(self._originalAvatar, self.size)
		screen.blit(self._Avatar, self.position)



	def destroy(self):
		pass


	# for some tests
	def _drawProto(self, screen):
		screen.blit(self._originalAvatar, self.position)