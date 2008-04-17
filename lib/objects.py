##########################
#objects.py
#class library including charactors
#and other misc objects for a platformer
###########################
import pygame
from pygame.locals import *


class mainChar(pygame.sprite.Sprite):
	"""The main character of the game
	"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.evManager = evManager
		self.evManager.RegisterListener( self )
		if mainChar.image = None:
			mainChar.image, mainChar.rect = load_png('ball.png')

		self.image = mainChar.image
		screen = pygame.display.get_surface()


	
	def Move(self, direction):
		if direction == "jump":
			#TODO: make character jump
		elif direction == "left":
			#TODO
		elif direction == "right":
			#TODO
		elif direction == "duck":
			#TODO: make character duck, could be tricky as hell
	def Notify(self, event):
		if isinstance( event, CharactorMoveRequest ):
			self.Move( event.direction )



class bounceBall(pygame.sprite.Sprite):
	"""A ball that bounces around the screen
	"""
	image = None
	
	def __init__(self, vector):
		pygame.sprite.Sprite.__init__(self)
		self.evManager = evManager
		self.evManager.RegisterListener( self )

		if bounceBall.image is None:
			bounceBall.image, bounceBall.rect = load_png('ball.png')
			
		self.image = bounceBall.image
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.vector = vector
	def update(self):
		newpos = self.calcnewpos(self.rect,self.vector)
		self.rect = newpos

	def calcnewpos(self,rect,vector):
		(angle,z) = vector
		(dx, dy) = (z*math.cos(angle), z*math.sin(angle))
		return rect.move(dx,dy)

#class Background(pygame.Surface):
#	def __init__(self):
		


